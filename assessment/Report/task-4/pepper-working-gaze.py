"""
GAZE: Game-Adaptive Zone of Engagement

Adaptive countdown-style game host on Pepper robot.
Novelty: multi-signal emotional inference; face (WS-10) + voice (WS-08)
+ response time + answer correctness, cross-validated so no single
signal is trusted alone.

Authorship (per proposal.pdf):
- Alfie: code architecture, OpenAI integration, facial recognition, AdaptiveEngine, etc
- Salman: game logic, gestures, LEDs, TTS pacing, session save/resume, testing

CRITICAL:
- **PROPOSAL.PDF IS SOURCE OF TRUTH FOR THE INITIAL-INTENDED DESIGN**
- **CONFIG NAO IP INTO ENV LIKE LAST TIME**

TODO:
 - `transcribe()` with Vosk wake-word gate + `
- [ ] offload simpler tasks? to either computation or mini model
- [ ] ensure all facial expression inference is sufficently commented
- [ ] ensure it notices and mitigates when user's disengaged

- [ ] ensure it always listening even when it's talking itself 
- [ ] fix continouation from previous game 5 games to 3 make it says results every 3 rounds for exampe 2 out of 3 is correct and then adapts based in that

- [ ] pirotise face over voice in mulit-singal inference
- [ ] states persist instead of how you look right now
- [ ] re-sensitize how adpative it is based on your constant state e.g. remember how you looked a minute ago
- [ ] ensure it saves all the time not just at least 5 
times 

- [ ] fix dashboard as it is just black when NAO
- [ ] eye colours should change 
- [X] after escalate directly address user's disengagent 
- [X] make it more random for more games as currently it keeps giving mainly the same answers even despite how hard it it is
- [X] make voice very not important
- [X] make it ask for name straight away 
- [ ] saves each time as right now i think only saves after five rounds but adapt at lesst evrery two times

- [ ] Mainly, fix: fix dashboard; saves each time; protise face over voice
""" 

import os, re, sys, json, time, types, wave, struct, tempfile, threading, subprocess, unicodedata
import tkinter as tk
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

print("[booting...] stdlib loaded", flush=True)

import numpy as np
import cv2
from PIL import Image, ImageTk
print("[booting...] numpy + opencv loaded", flush=True)

import paramiko
print("[booting...] paramiko loaded", flush=True)

import sounddevice as sd
import librosa
import soundfile as sf
# Vosk wake-word gate (fifth-layer defence); try/except fails open if the dep is missing, other four layers still protect us.
try:
    from vosk import Model as VoskModel, KaldiRecognizer
    _vosk_import_ok = True
except ImportError:
    VoskModel = None
    KaldiRecognizer = None
    _vosk_import_ok = False
# Silero VAD: pre-Whisper speech-activity gate; import here with audio imports, loader sits later near MODELS_DIR. Fail-open on missing dep.
try:
    from silero_vad import load_silero_vad, read_audio, get_speech_timestamps
    _silero_import_ok = True
except ImportError:
    load_silero_vad = None
    read_audio = None
    get_speech_timestamps = None
    _silero_import_ok = False
print("[booting...] audio stack loaded", flush=True)

from dotenv import load_dotenv
from openai import OpenAI
print("[booting...] openai loaded", flush=True)

import joblib
print("[booting...] loading tensorflow (this is slow on first run)...", flush=True)
import tensorflow as tf
from tensorflow.keras.models import model_from_json
print("[booting...] tensorflow loaded", flush=True)

# ---

# Silero VAD loader; kills most silent-audio hallucinations. Fail-open if model won't instantiate; downstream verbose_json + blacklist still guard.
_silero_model = None
if _silero_import_ok:
    try:
        _silero_model = load_silero_vad()
        print("[booting] silero-vad loaded", flush=True)
    except Exception as _vad_err:
        print(f"[booting] silero-vad failed to load ({_vad_err}); VAD gate disabled", flush=True)

load_dotenv()


NAO_IP       = os.getenv("NAO_IP", "ROBOT_IP")
NAO_USER     = "nao"
NAO_PASS     = "nao"
RECORD_MAX_SECS    = 12 # ceiling (don't record longer than this)
RECORD_MIN_SECS    = 2 # minimum recording before silence-detection kicks in
SILENCE_POLL_SECS  = 0.5 # polling interval for silence detection on Pepper
SILENCE_DURATION   = 1.5 # seconds of silence after speech to trigger stop
CALIBRATION_SECS   = 3 # duration of ambient noise calibration at start-up
ENERGY_BUFFER      = 200 # margin above ambient baseline to set speech threshold
DEFAULT_ENERGY_THRESHOLD = 800  # fallback for if calibration fails
REMOTE_WAV   = "/var/persistent/home/nao/input.wav"
REMOTE_IMG   = "/var/persistent/home/nao/capture.jpg"
LOCAL_WAV    = os.path.join(tempfile.gettempdir(), "gaze_input.wav")
LOCAL_IMG    = os.path.join(tempfile.gettempdir(), "gaze_capture.jpg")
VOLUME_THRESHOLD = 100  # RMS amplitude; below this the WAV is silence/ambient noise, not speech
FACE_CONFIDENCE_THRESHOLD  = 0.5  # below this, facial expression is too uncertain; thus treat as Neutral
VOICE_CONFIDENCE_THRESHOLD = 0.5  # threshold for vocal emotion is too uncertain; treat as neutral
SSH_TIMEOUT  = 10
CMD_TIMEOUT  = 60

# false when connected to pepper; true for testing when no Pepper's camera
USE_LOCAL_CAMERA = os.getenv("GAZE_LOCAL_CAMERA", "false").lower() == "true"

# full local mode to run game loop on MacBook without any Pepper connection
# uses local webcam; Mac microphone, and macOS TTS instead of Pepper-hardware
LOCAL_MODE = os.getenv("GAZE_LOCAL_MODE", "false").lower() == "true"
if LOCAL_MODE:
    USE_LOCAL_CAMERA = True # local mode implies local computer's camera

DEBUG_PREVIEW = LOCAL_MODE
_last_rms = 0.0 # shared with recording thread for overlay
_last_emotion = "" # updated by capture_and_classify

_preview_lock  = threading.Lock()
_preview_state = {"emotion": "Neutral", "confidence": 0.0}
_preview_frame = None # latest annotated BGR frame for the dashboard

# paths to pre-trained models; checks models/ first (portable),
# then falls back to the workshop directory (development repo layout)
SCRIPT_DIR    = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR    = os.path.join(SCRIPT_DIR, "models")
WORKSHOP_DIR  = os.path.join(SCRIPT_DIR, "..", "..", "..", "learning", "workshops") # go backwards to root of repo then go to learning/workshops

def find_model(local_name, workshop_subpath):
    """Resolve a model local models/ dir first, then workshop fallback."""
    local = os.path.join(MODELS_DIR, local_name)
    if os.path.exists(local):
        return local
    return os.path.join(WORKSHOP_DIR, workshop_subpath)

MODEL_JSON    = find_model("model.json", os.path.join("[X]-facial-expression-detection", "model.json"))
MODEL_WEIGHTS = find_model("model_weights.weights.h5", os.path.join("[X]-facial-expression-detection", "model_weights.weights.h5"))
HAAR_CASCADE  = find_model("haarcascade_frontalface_default.xml", os.path.join("[X]-ws-10", "haarcascade_frontalface_default.xml"))
SPEECH_MODEL  = os.path.join(SCRIPT_DIR, "speech_emotion_model.pkl")
VOSK_MODEL_DIR = os.path.join(MODELS_DIR, "vosk-model-small-en-us-0.15")

# Vosk wake-word gate: post-Silero, pre-Whisper fifth-layer defence. User must say "Pepper"/"Gaze" before Whisper ever fires. Fail-open if model doesn't load.
_vosk_model = None
if _vosk_import_ok:
    try:
        _vosk_model = VoskModel(VOSK_MODEL_DIR)
        print("[booting] vosk wake-word model loaded", flush=True)
    except Exception as _vosk_err:
        print(f"[booting] vosk failed to load ({_vosk_err}); wake-word gate disabled", flush=True)

RESPONSE_TIME_BASELINE = 30.0 # seconds; beyond this the user is slow
CORRECTNESS_WINDOW     = 5 # rolling window size
CORRECTNESS_FLOOR      = 0.4 # below thus ease off
CORRECTNESS_CEILING    = 0.8 # above thus ramp up
SILENCE_THRESHOLD      = 2 # consecutive non-responses before intervention
MAX_ROUNDS             = 20 # natural session end

SAVE_FILE = os.path.join(SCRIPT_DIR, "gaze_save.json")

if not os.getenv("OPENAI_API_KEY", "").strip():
    raise SystemExit("ERROR: OPENAI_API_KEY not set. Add it to .env")
client = OpenAI()


class FacialExpressionModel:
    """Pre-trained CNN: 7-classed emotion classifier (48x48 greyscale input)."""

    EMOTIONS = ["Angry", "Disgust", "Fear", "Happy", "Neutral", "Sad", "Surprise"]

    def __init__(self, model_json_path, model_weights_path):
        with open(model_json_path, "r") as f:
            self.model = model_from_json(f.read())
        self.model.load_weights(model_weights_path)
        self.model.make_predict_function()

    # Alfie's
    def predict(self, img):
        """Return (emotion_label, confidence) from the (1, 48, 48, 1) array."""
        preds = self.model.predict(img, verbose=0)
        idx = np.argmax(preds)
        return self.EMOTIONS[idx], float(preds[0][idx])


class SpeechEmotionModel:
    """Pre-trained MLP for vocal emotion classification (WS-08)."""

    EMOTIONS = ["calm", "happy", "fearful", "disgust"]

    def __init__(self, model_path):
        self.model = joblib.load(model_path)

    @staticmethod # static because it requires no instance state (no self) as it's called directly from the game loop with just a WAV path argument
    def extract_features(wav_path: str):
        """Extract the same MFCC/chroma/mel feature vector used in WS-08 training."""
        with sf.SoundFile(wav_path) as sound_file:
            audio = sound_file.read(dtype="float32")
            sample_rate = sound_file.samplerate

        if audio.ndim > 1:
            audio = audio.mean(axis=1)

        # peak-normalise so quieter speakers (post-stroke, brain-injured: the actual target population) won't be penalised by the studio-loud training distribution; loudness thus stops being an implicit feature
        audio = librosa.util.normalize(audio)

        n_fft = 2048
        if len(audio) < n_fft:
            return None

        stft = np.abs(librosa.stft(audio, n_fft=n_fft))

        mfccs = np.mean(librosa.feature.mfcc(
            y=audio, sr=sample_rate, n_mfcc=40).T, axis=0).flatten()
        
        chroma = np.mean(librosa.feature.chroma_stft(
            S=stft, sr=sample_rate).T, axis=0).flatten()
        
        mel = np.mean(librosa.feature.melspectrogram(
            y=audio, sr=sample_rate).T, axis=0).flatten()

        return np.concatenate([mfccs, chroma, mel])

    # Alfie's
    def predict(self, wav_path: str) -> tuple[str, float]:
        """Return (emotion_label, confidence) from a WAV file."""
        features = self.extract_features(wav_path)
        if features is None:
            return "neutral", 0.0

        features = features.reshape(1, -1)
        label = self.model.predict(features)[0]
        proba = self.model.predict_proba(features)[0]
        confidence = float(np.max(proba))
        return label, confidence

# Alfie's
def classify_speech_emotion(speech_model, wav_path: str) -> tuple[str, float]:
    """Classify the vocal emotion from a WAV file."""
    if speech_model is None:
        return "neutral", 0.0
    # VAD gate: MLP was trained on speech; running it on silence or
    # background noise is out-of-distribution and produces rubbush
    if LOCAL_MODE and not has_real_speech(wav_path):
        return "neutral", 0.0
    try:
        return speech_model.predict(wav_path)
    except Exception as e:
        print(f"  Speech emo classify failed: {e}; defaulting to neutral")
        return "neutral", 0.0


class Difficulty(Enum):
    EASY   = 1
    MEDIUM = 2
    HARD   = 3

class InferredState(Enum):
    THRIVING    = "thriving"
    COMFORTABLE = "comfortable"
    STRUGGLING  = "struggling"
    DISENGAGED  = "disengaged"
    FRUSTRATED  = "frustrated"

# Alfie's
class GameType(Enum):
    NUMBERS = "numbers"
    LETTERS = "letters"

BASE_SYSTEM_PROMPT = (
    "You are GAZE: a social-companion robot running on a Pepper humanoid. "
    "You are a companion first and a game host second.\n\n"
    "CONVERSATION GUIDELINES:\n"
    "- NEVER say the words 'Pepper' or 'Gaze' in your replies. These are "
    "the user's wake-word; the robot's own TTS output must not contain them "
    "or the microphone will pick up the tail of your speech and the "
    "wake-word gate will false-positive on the next turn. Refer to yourself "
    "only in the first person ('I', 'me', 'your companion').\n"
    "- Have natural, flowing conversations with the user.\n"
    "- You can play countdown-style games (numbers rounds and letters rounds) "
    "when the moment feels right or the user asks, but do NOT force a game "
    "every single turn.\n"
    "- Each user message includes real-time emotional signals (facial expression, "
    "vocal emotion, volume, response time). Use these signals to adapt your "
    "tone and approach naturally; doN'T mention the signals explicitly.\n"
    "- Keep responses concise: 2-3 sentences maximum. Your words are spoken "
    "aloud via text-to-speech, so brevity is essential.\n"
    "- End every response with a gesture tag on its own line: [gesture:TYPE] "
    "where TYPE is one of: celebrate, encourage, think, wave, calm, energetic, neutral.\n"
    "- If a game is active, acknowledge the user's answer before moving on.\n"
    "- If the user seems disengaged, try a different topic or suggest a game.\n"
    "- If the user asks for more time to think, call request_more_time and "
    "respond warmly.\n"
    "- If the user says the game is too hard or too easy, adjust the difficulty "
    "naturally in your next generate_game_question call.\n"
    "- Be genuinely present; you are the user's companion for this session.\n"
)

@dataclass
class GameState:
    """Essentially tracks whether a countdown game is currently active."""
    active:           bool   = False
    current_question: str    = ""
    current_answer:   str    = ""
    category:         str    = ""
    turn_count:       int    = 0
    waiting:          bool   = False # user asked for more time to think
    last_answer_checked:  bool = False # was a game answer checked this turn?
    last_answer_correct:  bool = False # result of the last answer check

@dataclass # decorator for round results and adaptive decisions
class RoundResult:
    """Record of a single game round."""
    round_number:          int
    game_type:             GameType
    difficulty:            Difficulty
    question:              str
    user_answer:           str
    correct:               bool
    response_time:         float
    facial_expression:     str
    expression_confidence: float
    vocal_emotion:         str
    vocal_emotion_confidence: float
    volume_rms:            float # speech loudness (arousal signal)
    inferred_state:        InferredState
    timestamp:             float = field(default_factory=time.time)

@dataclass
class AdaptiveDecision:
    """Output of the adaptive engine (what to do next)"""
    difficulty:         Difficulty
    game_type:          GameType
    inferred_state:     InferredState
    switch_game:        bool
    give_hint:          bool
    give_encouragement: bool
    tone:               str # "encouraging" | "celebratory" | "calm" | "energetic" | "neutral"


class AdaptiveEngine:
    """Takes all five input signals and *infers* the user's real state. The adaptive engine also evaluates if its previous adaptation worked, feeding that evaluation into the next round's prompt."""

    def __init__(self):
        self.history: list[RoundResult]   = []
        self.current_difficulty            = Difficulty.MEDIUM
        self.current_game                  = GameType.NUMBERS
        self.consecutive_silences          = 0
        self.consecutive_correct           = 0
        self.consecutive_wrong             = 0
        self.games_played: dict[GameType, int] = {g: 0 for g in GameType}
        self.game_switch_count             = 0
        self.adaptation_log: list[dict]    = []
        self.total_correct                 = 0
        self.best_streak                   = 0
        # user's preferred name (captured at session start, persisted across sessions)
        self.user_name: str                = ""
        # rolling list of recently-generated question strings; passed into the
        # generator as a "DO NOT repeat" clause so GPT stops mode-collapsing
        # onto the same ~100-target sets. Capped at 10 entries
        self.recent_questions: list[str]   = []
        # adaptive think-budget; baseline defaults, updated per round by
        # recommend_think_budget() — signals-driven wait time for the user
        self.think_budget_secs       = float(RECORD_MAX_SECS) # hard ceiling
        self.silence_tolerance_secs  = float(SILENCE_DURATION) # post-speech silence
        self.no_speech_max_secs      = 5.0 # give up if no speech at all


    @property
    def round_number(self) -> int:
        return len(self.history) + 1

    def rolling_correctness(self) -> float:
        recent = self.history[-CORRECTNESS_WINDOW:]
        if not recent:
            return 0.5  # no data -> assume middle (neutral)
        return sum(1 for r in recent if r.correct) / len(recent)

    def avg_response_time(self) -> float:
        recent = self.history[-CORRECTNESS_WINDOW:]
        if not recent:
            return RESPONSE_TIME_BASELINE / 2
        return sum(r.response_time for r in recent) / len(recent)


    VOLUME_QUIET = 200 # below this -> low arousal (quiet/disengaged)
    VOLUME_LOUD  = 2000 # above this -> high arousal (excited/frustrated)

    # Alfie's
    def infer_state(self, expression: str, response_time: float,
                    correct: bool, answer_text: str,
                    vocal_emotion: str = "neutral",
                    vocal_conf: float = 0.0,
                    volume_rms: float = 0.0) -> InferredState:
        """
        Weigh all signals to infer the user's state.

        Hierarchy is face-primary: the facial-expression CNN (WS-10) drives
        every state decision; voice is consulted only when face is Neutral
        and the voice signal is both high-confidence AND not `fearful`
        (the MLP's ambient-noise attractor — stuck at 1.00 in silence).

        Five signals in consideration:
          1- facial expression  (CNN, WS-10)  -- PRIMARY
          2- answer correctness (performance) -- PRIMARY
          3- response time      (behavioural) -- PRIMARY
          4- speech volume/RMS  (arousal)     -- secondary
          5- vocal emotion      (MLP, WS-08)  -- advisory tie-breaker only
        """
        correctness = self.rolling_correctness()
        clean = answer_text.strip().lower()
        is_silent = (not clean or clean in {"i don't know", "skip", "pass", "next"}) # if no meaningful input || input matches a skip-command phrase in the set (set over list because it's faster) then indeed silent (True)

        # Arousal bounds calibrated against ambient noise
        high_arousal = volume_rms > self.VOLUME_LOUD
        low_arousal  = 0 < volume_rms < self.VOLUME_QUIET

        # voice is trusted only when it's confidently NOT-fearful; fearful@1.00 is the MLP's silence attractor, never load-bearing
        trust_voice = (vocal_conf >= 0.9 and vocal_emotion != "fearful")

        if is_silent:
            self.consecutive_silences += 1
        else:
            self.consecutive_silences = 0
        if correct:
            self.consecutive_correct += 1
            self.consecutive_wrong   = 0
        else:
            self.consecutive_wrong  += 1
            self.consecutive_correct = 0

        # 1- FACE-PRIMARY RULES -- these fire before voice is ever consulted

        # thriving: performing well + fast responses (face is allowed to be anything here; correctness + speed carry the signal)
        if (correctness >= CORRECTNESS_CEILING and response_time < RESPONSE_TIME_BASELINE * 0.5):
            return InferredState.THRIVING
        if expression == "Angry" and correct and response_time < RESPONSE_TIME_BASELINE * 0.6:
            return InferredState.COMFORTABLE

        # disengaged: silence threshold, or face + slow response + poor performance (Stroke-ward insight via Dr. Amir)
        if self.consecutive_silences >= SILENCE_THRESHOLD:
            return InferredState.DISENGAGED
        if (expression == "Neutral"
                and response_time > RESPONSE_TIME_BASELINE
                and correctness < 0.5):
            return InferredState.DISENGAGED
        if (low_arousal and expression == "Neutral"
                and response_time > RESPONSE_TIME_BASELINE * 0.8):
            return InferredState.DISENGAGED

        # frustrated: negative face + poor performance, or 3+ wrong + negative face, or high arousal + negative face + poor
        if expression in ("Angry", "Disgust") and correctness < CORRECTNESS_FLOOR:
            return InferredState.FRUSTRATED
        if self.consecutive_wrong >= 3 and expression in ("Angry", "Sad", "Fear"):
            return InferredState.FRUSTRATED
        if (high_arousal and expression in ("Angry", "Disgust", "Fear")
                and correctness < CORRECTNESS_FLOOR):
            return InferredState.FRUSTRATED

        # struggling: sadness + slow; poor correctness; fear + wrong
        if expression == "Sad" and response_time > RESPONSE_TIME_BASELINE * 0.7:
            return InferredState.STRUGGLING
        if correctness < CORRECTNESS_FLOOR:
            return InferredState.STRUGGLING
        if expression == "Fear" and not correct:
            return InferredState.STRUGGLING

        # 2- VOICE TIE-BREAKERS -- only fire when face is Neutral AND voice is trustworthy. Voice can nudge but never override a face-driven verdict.
        if expression == "Neutral" and trust_voice:
            if vocal_emotion == "happy" and correct and correctness >= CORRECTNESS_CEILING:
                return InferredState.THRIVING
            if vocal_emotion == "calm" and correctness >= 0.5:
                return InferredState.COMFORTABLE

        return InferredState.COMFORTABLE # default: face gave no negative signal, performance is holding

    # Alfie's
    # Core-decision function

    def decide(self, expression: str, expression_conf: float,
               response_time: float, correct: bool,
               answer_text: str,
               vocal_emotion: str = "neutral",
               vocal_conf: float = 0.0,
               volume_rms: float = 0.0) -> AdaptiveDecision:
        """Return what to do next based on the inferred state."""
        state = self.infer_state(expression, response_time, correct, answer_text,
                                       vocal_emotion, vocal_conf=vocal_conf,
                                       volume_rms=volume_rms)
        correctness = self.rolling_correctness()

        new_difficulty     = self.current_difficulty
        new_game           = self.current_game
        switch_game        = False
        give_hint          = False
        give_encouragement = False
        tone               = "neutral"

        if state == InferredState.THRIVING:
            if self.current_difficulty != Difficulty.HARD:
                new_difficulty = Difficulty(self.current_difficulty.value + 1)
            tone = "energetic"
            if self.consecutive_correct >= 3:
                give_encouragement = True # acknowledge streak

        elif state == InferredState.COMFORTABLE:
            if correctness > 0.7 and self.current_difficulty != Difficulty.HARD:
                new_difficulty = Difficulty(self.current_difficulty.value + 1)
            tone = "neutral"

        elif state == InferredState.STRUGGLING:
            if self.current_difficulty != Difficulty.EASY:
                new_difficulty = Difficulty(self.current_difficulty.value - 1)
            give_hint          = True
            give_encouragement = True
            tone               = "encouraging"

        elif state == InferredState.FRUSTRATED:
            new_difficulty     = Difficulty.EASY
            give_encouragement = True
            tone               = "calm"
            if self.consecutive_wrong >= 4:
                switch_game = True
                new_game    = self.pick_different_game()

        elif state == InferredState.DISENGAGED:
            tone               = "energetic" # robot be engaging
            give_encouragement = True
            if self.consecutive_silences >= 3:
                switch_game = True
                new_game    = self.pick_different_game()

        self.current_difficulty = new_difficulty
        if switch_game:
            self.current_game = new_game
            self.game_switch_count += 1

        self.adaptation_log.append({
            "round":  self.round_number,
            "state":  state.value,
            "action": {"difficulty": new_difficulty.name,
                       "switch": switch_game,
                       "hint": give_hint,
                       "encouragement": give_encouragement},
        })

        return AdaptiveDecision(
            difficulty=new_difficulty, game_type=self.current_game,
            inferred_state=state, switch_game=switch_game,
            give_hint=give_hint, give_encouragement=give_encouragement,
            tone=tone,
        )

    # Alfie's
    def recommend_think_budget(self, state: InferredState, expression: str,
                               prev_response_time: float,
                               consecutive_silences: int, waiting: bool
                               ) -> tuple[float, float, float]:
        """
        Decide how long to wait for the user this turn, from state +
        signals (NOT-trigger phrases). Returns
        (no_speech_max, silence_secs, record_max_secs) for this turn only.

        The LLM's `request_more_time` tool only flips game_state.waiting;
        it never bumps the budget directly. `waiting` is one signal
        among many; accumulated silence, previous response time, facial
        expression, inferred state contribute independently.
        """
        # baseline budget (fast-track: thriving / comfortable)
        no_speech_max   = 5.0
        silence_secs    = float(SILENCE_DURATION)
        record_max_secs = float(RECORD_MAX_SECS)

        # round 1 (no history): stroke-recovery/aphasia users exceed the standard 1.5s silence tolerance. Placed before the rule block so later signals can still push higher.
        if not self.history:
            no_speech_max   = max(no_speech_max, 7.0)
            silence_secs    = max(silence_secs, 2.5)
            record_max_secs = max(record_max_secs, 15.0)

        if state in (InferredState.STRUGGLING, InferredState.FRUSTRATED,
                     InferredState.DISENGAGED):
            no_speech_max   = 8.0
            silence_secs    = 2.5
            record_max_secs = 18.0

        # accumulated silence: graduated extension *before* the state flips
        # to Disengaged. One silent turn nudges the budget; two nudges more;
        # three triggers Disengaged + the extended baseline above.
        if consecutive_silences > 0:
            no_speech_max = max(no_speech_max, 5.0 + consecutive_silences * 1.5)
            silence_secs  = max(silence_secs,  1.5 + consecutive_silences * 0.5)

        if expression in ("Sad", "Fear"):
            no_speech_max = max(no_speech_max, 7.0)
            silence_secs  = max(silence_secs, 2.0)

        if prev_response_time > RESPONSE_TIME_BASELINE:
            no_speech_max = max(no_speech_max, 7.0)
            silence_secs  = max(silence_secs, 2.0)

        # LLM-flagged waiting: honour the signal without letting the LLM
        # own the budget directly; additive bump keeps other cues weighted
        if waiting:
            no_speech_max   += 3.0
            silence_secs    += 1.0
            record_max_secs += 5.0

        # defensive ceiling: no combination of signals should push the
        # recording window past 20s therefore keeps UX bounded and leaves
        # nice amount of headroom under CMD_TIMEOUT (60s) for future additions
        record_max_secs = min(record_max_secs, 20.0)

        self.no_speech_max_secs     = no_speech_max
        self.silence_tolerance_secs = silence_secs
        self.think_budget_secs      = record_max_secs

        return no_speech_max, silence_secs, record_max_secs

    def record_round(self, result: RoundResult):
        self.history.append(result)
        self.games_played[result.game_type] = (
            self.games_played.get(result.game_type, 0) + 1
        )
        if result.correct:
            self.total_correct += 1
        self.best_streak = max(self.best_streak, self.consecutive_correct)

# Salman's
    def pick_different_game(self) -> GameType:
        if self.current_game == GameType.NUMBERS:
            return GameType.LETTERS
        return GameType.NUMBERS

    def get_session_summary(self) -> dict:
        if not self.history:
            return {"rounds": 0}
        total   = len(self.history)
        correct = sum(1 for r in self.history if r.correct)
        return {
            "rounds":             total,
            "correct":            correct,
            "accuracy":           round(correct / total, 2),
            "avg_response_time":  round(sum(r.response_time for r in self.history) / total, 1),
            "games_played":       {g.value: c for g, c in self.games_played.items() if c > 0},
            "game_switches":      self.game_switch_count,
            "best_streak":        self.best_streak,
            "final_difficulty":   self.current_difficulty.name,
        }

    # Alfie's
    # adaptation self-evaluation

    def evaluate_adaptation(self) -> Optional[str]:
        """Evaluate whether the previous round's adaptation worked."""
        if len(self.adaptation_log) < 2 or len(self.history) < 2:
            return None

        prev_strategy = self.adaptation_log[-2]
        curr_strategy = self.adaptation_log[-1]
        prev_round    = self.history[-2]
        curr_round    = self.history[-1]

        prev_state  = prev_strategy["state"]
        curr_state  = curr_strategy["state"]
        prev_action = prev_strategy["action"]

        evaluations = []

        if prev_state in ("struggling", "frustrated"):
            if curr_round.correct and not prev_round.correct:
                evaluations.append(
                    "Previous adaptation WORKED: lowered difficulty and user "
                    "answered correctly this round (was incorrect before)."
                )
            elif not curr_round.correct:
                evaluations.append(
                    "Previous adaptation DID NOT HELP YET: user still struggling "
                    "despite easier difficulty. Consider providing more support."
                )

        # did a difficulty increase overshoot for a thriving user?
        if prev_state == "thriving" and prev_action["difficulty"] == "HARD":
            if curr_round.correct:
                evaluations.append(
                    "Previous adaptation WORKED: increased difficulty and user "
                    "is still performing well."
                )
            elif not curr_round.correct:
                evaluations.append(
                    "Previous adaptation OVERSHOT: increased difficulty but user "
                    "got it wrong. May need to ease back."
                )

        # did a re-engagement attempt work for a disengaged user?
        if prev_state == "disengaged":
            if curr_state != "disengaged":
                evaluations.append(
                    "Previous adaptation WORKED: user was disengaged but is now "
                    f"{curr_state}. Re-engagement was effective."
                )
            else:
                evaluations.append(
                    "Previous adaptation DID NOT HELP: user remains disengaged. "
                    "Try a different approach or switch game type."
                )

        if prev_action.get("switch"):
            if curr_state in ("thriving", "comfortable"):
                evaluations.append(
                    "Game switch WORKED: user transitioned to a positive state."
                )
            elif curr_state in ("struggling", "frustrated", "disengaged"):
                evaluations.append(
                    "Game switch DID NOT HELP: user is still in a negative state."
                )

        if (prev_action.get("encouragement")
                and prev_state in ("struggling", "frustrated")
                and curr_round.response_time < prev_round.response_time):
            evaluations.append(
                "Encouragement appears effective: user responded faster this round."
            )

        if not evaluations:
            return None

        return ("Adaptation evaluation from previous round:\n"
                + "\n".join(f"- {e}" for e in evaluations))


GAME_DESCRIPTIONS = {
    GameType.NUMBERS: (
        "a Countdown-style numbers round. Pick SIX numbers by sampling from "
        "{1,2,3,4,5,6,7,8,9,10,25,50,75,100}; vary the mix each round so no "
        "two rounds in a row feel identical. Pick a TARGET in the range 50-999 "
        "(anywhere in that range — NOT always around 100), reachable from the "
        "chosen six via +, -, *, /. The user must combine the given numbers "
        "with those operators to reach the target. Each number may be used at "
        "most once"
    ),
    GameType.LETTERS: (
        "a Countdown-style letters round: give the user a set of 9 random letters "
        "(a mix of vowels and consonants; vary the letter set every round) and "
        "ask them to form the longest word possible using only those letters. "
        "Each letter can only be used once"
    ),
}

DIFFICULTY_DESCRIPTIONS = {
    Difficulty.EASY:   "easy (straightforward, common knowledge, single-step)",
    Difficulty.MEDIUM: "medium (requires some thought, moderately specific)",
    Difficulty.HARD:   "hard (obscure, multi-step, requires deep knowledge)",
}

TONE_INSTRUCTIONS = {
    "encouraging": "Use a warm, supportive tone. Be patient.",
    "celebratory": "Be enthusiastic and celebratory. The user is doing brilliantly.",
    "calm":        "Use a calm, reassuring tone. No pressure.",
    "energetic":   "Be upbeat and energetic. Keep the energy high.",
    "neutral":     "Use a friendly, natural tone.",
}

# SSH AND PEPPER ROBOT HELPERS
# (adapted from lab-robot-code-fin.py i.e. when 
#  we tested OpenAI on the NAO robot perhaps too early)

def ssh_connect():
    """Open SSH connection to Pepper and return the client."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(NAO_IP, username=NAO_USER, password=NAO_PASS, timeout=SSH_TIMEOUT)
    return ssh

def nao_run(ssh, code):
    """Execute a Python 2 snippet on Pepper via SSH."""
    escaped = code.replace("'", "'\\''")
    try:
        _, stdout, _ = ssh.exec_command(f"python -c '{escaped}'", timeout=CMD_TIMEOUT)
        return stdout.read().decode().strip()
    except Exception as e:
        print(f"  Pepper SSH exec_command dropped: {e}")
        return ""

# Salman's
#listens silent
#not triggered by noise
def nao_calibrate_ambient(ssh) -> int:
    """Calibrate the mic energy threshold to the room."""
    try:
        # NOTE: nao_run() payloads stay at column 0; `python -c` on Pepper
        # rejects leading whitespace thus these blocks can't be indented; I initially done this
        raw = nao_run(ssh, f"""
from naoqi import ALProxy
import time

audio = ALProxy("ALAudioDevice", "127.0.0.1", 9559)
samples = []
start = time.time()
while (time.time() - start) < {CALIBRATION_SECS}:
    samples.append(audio.getFrontMicEnergy())
    time.sleep(0.2)

if samples:
    avg = sum(samples) / len(samples)
    print(int(avg))
else:
    print(0)
""")
        ambient = int(raw) if raw.strip().isdigit() else 0
        threshold = ambient + ENERGY_BUFFER
        print(f"  Ambient energy: {ambient}, speech threshold: {threshold}")
        return threshold
    except Exception as e:
        print(f"  Calibration failed ({e}), using default threshold: {DEFAULT_ENERGY_THRESHOLD}")
        return DEFAULT_ENERGY_THRESHOLD

# Alfie's
def nao_record(ssh, energy_threshold: int = DEFAULT_ENERGY_THRESHOLD,
               record_max_secs: float = RECORD_MAX_SECS,
               silence_secs: float = SILENCE_DURATION):
    """Record audio on Pepper with dynamic silence detection.
        - get robot's front microphone (getFrontMicEnergy) to stop recording early if silence detected
        - calibrated energy threshold to avoid false positives from ambient noise 
        - if getFrontMicEnergy is unsupported (e.g. older firmware), fall back to a safe fixed-duration recording to ensure the demo still works, albeit without silence detection
    """
    # SSH payload in a script wherein it tries to initialise ALAudioDevice to poll getFrontMicEnergy; if that fails due to older firmware fall back to a fixed-duration recording, thus ensuring the demo still works albeit without silence detection
    nao_run(ssh, f""" 
from naoqi import ALProxy
import time

rec  = ALProxy("ALAudioRecorder", "127.0.0.1", 9559)

rec.stopMicrophonesRecording()
rec.startMicrophonesRecording("{REMOTE_WAV}", "wav", 16000, [0, 0, 1, 0])

try:
    audio = ALProxy("ALAudioDevice", "127.0.0.1", 9559)

    speech_detected  = False
    silence_start    = None
    start            = time.time()
    threshold        = {energy_threshold}

    while True:
        elapsed = time.time() - start

        # hard ceiling; never exceed max duration
        if elapsed >= {record_max_secs}:
            break

        # poll front microphone energy level
        energy = audio.getFrontMicEnergy()

        if elapsed < {RECORD_MIN_SECS}:
            # minimum recording period
            if energy > threshold:
                speech_detected = True
            time.sleep({SILENCE_POLL_SECS})
            continue

        if energy > threshold:
            speech_detected = True
            silence_start = None
        else:
            if speech_detected and silence_start is None:
                silence_start = time.time()
            if speech_detected and silence_start is not None:
                if (time.time() - silence_start) >= {silence_secs}:
                    break

        time.sleep({SILENCE_POLL_SECS})

except Exception as e:
    # firmware fallback; getFrontMicEnergy() unsupported on this Pepper
    # fall back to a safe fixed-duration recording so the demo never breaks
    print("  [Silence detection failed: " + str(e) + "] Falling back to fixed-duration recording")
    time.sleep({record_max_secs})

rec.stopMicrophonesRecording()
""")
    sftp = ssh.open_sftp()
    sftp.get(REMOTE_WAV, LOCAL_WAV)
    sftp.close()

# Salman's
 #responses arrive in one block no splitting
#delivered with no pauses
def split_into_sentences(text: str) -> list[str]:
    """Split dialogue into sentences for speech delivery."""
    raw_segments = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = []
    for seg in raw_segments:
        for line in seg.split("\n"):
            cleaned = line.strip()
            if cleaned:
                sentences.append(cleaned)
    return sentences if sentences else [text.strip()]

# Salman's
#single ssh calls
def nao_say(ssh, text):
    """Speak text on Pepper with sentence-level pausing."""
    sentences = split_into_sentences(text)
    safe_sentences = json.dumps(sentences)

    nao_run(ssh, f"""
from naoqi import ALProxy
import time

try:
    tts = ALProxy("ALTextToSpeech", "127.0.0.1", 9559)
    sentences = {safe_sentences}

    for i, sentence in enumerate(sentences):
        tts.say(sentence)
        if i < len(sentences) - 1:
            time.sleep(0.4)
except Exception as e:
    print("  [TTS failed] " + str(e))
""")

# Salman's
#animations with speech
def nao_say_animated(ssh, text):
    """Try animated speech; fall back to plain TTS."""
    safe = json.dumps(text)
    try:
        nao_run(ssh, f"""
from naoqi import ALProxy
ALProxy("ALAnimatedSpeech","127.0.0.1",9559).say({safe})
""")
    except Exception as e:
        print(f"  Animated speech failed mid-sentence: {e}")
        nao_say(ssh, text)

def nao_capture_image(ssh):
    """Capture a photo from Pepper's camera and download it."""
    nao_run(ssh, f"""
from naoqi import ALProxy
pc = ALProxy("ALPhotoCapture","127.0.0.1",9559)
pc.setResolution(2)
pc.setPictureFormat("jpg")
pc.takePicture("{os.path.dirname(REMOTE_IMG)}/", "{os.path.splitext(os.path.basename(REMOTE_IMG))[0]}")
""")
    sftp = ssh.open_sftp()
    sftp.get(REMOTE_IMG, LOCAL_IMG)
    sftp.close()

def nao_track_face(ssh, enable=True):
    """Toggle face tracking on Pepper."""
    try:
        if enable:
            nao_run(ssh, """
from naoqi import ALProxy
ALProxy("ALFaceDetection","127.0.0.1",9559).subscribe("gaze_face")
t = ALProxy("ALTracker","127.0.0.1",9559)
t.registerTarget("Face", 0.1)
t.track("Face")
""")
        else:
            nao_run(ssh, """
from naoqi import ALProxy
t = ALProxy("ALTracker","127.0.0.1",9559)
t.stopTracker()
t.unregisterAllTargets()
try:
    ALProxy("ALFaceDetection","127.0.0.1",9559).unsubscribe("gaze_face")
except Exception as e:
    print("  [Face unsubscribe failed] " + str(e))
""")
    except Exception as e:
        print(f"  Face tracking unavailable: {e}")

# Salman's
#leds
def nao_set_leds(ssh, group, colour, duration=1.0):
    try:
        nao_run(ssh, f"""
from naoqi import ALProxy
ALProxy("ALLeds","127.0.0.1",9559).fadeRGB("{group}", {colour}, {duration})
""")
    except Exception as e:
        print(f"  LED set ignored: {e}")

# LOCAL MODE HELPERS (Mac; no Pepper required)

LOCAL_SAMPLE_RATE = 16000   # Whisper expects 16 kHz; we resample from native rate

LOCAL_SILENCE_RMS   = 40 # default RMS; overridden by local_calibrate_ambient()
_local_speech_detected = False # set by local_record(); used as transcription gate
LOCAL_SILENCE_SECS  = 1.5 # seconds of post-speech silence to stop recording
LOCAL_MIN_SECS      = 1.0 # minimum recording before silence detection kicks in
LOCAL_NO_SPEECH_MAX = 5.0 # stop if no speech detected at all after this many seconds
LOCAL_ENERGY_BUFFER = 50 # margin above ambient baseline for speech detection

# Alfie's
def local_calibrate_ambient() -> int:
    """Calibrate the local-testing (Mac) mic's ambient noise level; mirrors nao_calibrate_ambient() so LOCAL_MODE testing behaves like the robot."""
    global LOCAL_SILENCE_RMS
    dev_info   = sd.query_devices(kind="input")
    dev_index  = dev_info["index"]
    native_rate = int(dev_info["default_samplerate"])
    chunk_size  = int(native_rate * 0.2)
    samples     = []

    print(f"Calibrating Mac mic (stay quiet for {CALIBRATION_SECS}s)...")

    def cb(indata, frames, time_info, status):
        rms = (np.mean(indata.astype(np.float64) ** 2)) ** 0.5
        samples.append(rms)

    with sd.InputStream(samplerate=native_rate, channels=1, dtype="int16",
                        blocksize=chunk_size, device=dev_index, callback=cb):
        time.sleep(CALIBRATION_SECS)

    if samples:
        ambient = int(sum(samples) / len(samples))
    else:
        ambient = 0

    threshold = ambient + LOCAL_ENERGY_BUFFER
    LOCAL_SILENCE_RMS = threshold

    # re-tune the transcription gate. VOLUME_THRESHOLD was initially hardcoded at
    # 500, too high for MacBook built-in mics
    global VOLUME_THRESHOLD
    VOLUME_THRESHOLD = max(LOCAL_SILENCE_RMS * 4, 100)

    # scale arousal thresholds to the room; static (200, 2000) would
    # call a loud speaker in a quiet room the same as a quiet speaker
    # in a noisy lab. 
    AdaptiveEngine.VOLUME_QUIET = max(ambient * 2,  200) # twice as loud as an empty room, thus quiet; 200 enforces an absolute minimum to quiet
    AdaptiveEngine.VOLUME_LOUD  = max(ambient * 10, 2000)

    print(f"  Ambient RMS: {ambient}, silence threshold: {threshold}, "
          f"transcription gate: {VOLUME_THRESHOLD}")
    print(f"  Arousal thresholds: QUIET={AdaptiveEngine.VOLUME_QUIET}, "
          f"LOUD={AdaptiveEngine.VOLUME_LOUD}")
    return threshold

# Alfie's and Salman's
def local_record(max_secs: float = RECORD_MAX_SECS,
                 no_speech_max: float = LOCAL_NO_SPEECH_MAX,
                 silence_secs: float = LOCAL_SILENCE_SECS):
    """Record audio from the Mac's built-in microphone to LOCAL_WAV with silence detection mirroring Pepper's dynamic recording."""
    # explicitly select the default input device (matches test-mic.py behaviour)
    dev_info    = sd.query_devices(kind="input")
    dev_index   = dev_info["index"]
    native_rate = int(dev_info["default_samplerate"])
    sd.default.device = (dev_index, None)
    chunk_size  = int(native_rate * SILENCE_POLL_SECS)

    buffer = []
    speech_detected = False
    silence_start = None
    elapsed = 0.0

    print(f"  Recording from Mac mic (up to {max_secs}s, stops after silence)...")

    def callback(indata, frames, time_info, status):
        buffer.append(indata.copy())

    for attempt in range(2): #one retry if PortAudio error (if the device briefly is unavailable after Pepper usage)
        try:
            with sd.InputStream(samplerate=native_rate, channels=1, dtype="int16",
                                blocksize=chunk_size, callback=callback):
                while elapsed < max_secs:
                    time.sleep(SILENCE_POLL_SECS)
                    elapsed += SILENCE_POLL_SECS

                    if not buffer:
                        continue
                    data = buffer[-1]

                    rms = (np.mean(data.astype(np.float64) ** 2)) ** 0.5 # compute RMS of the latest chunk for real-time feedback
                    global _last_rms
                    _last_rms = rms
                    print(f"\r    [{elapsed:.1f}s] RMS: {rms:.0f} {'▓' if rms > LOCAL_SILENCE_RMS else '░'}", end="", flush=True) # '▓' (U+2593 DARK SHADE) and '░' (U+2591 LIGHT SHADE) extracted from Unicode 1.1 Block Elements

                    if elapsed < LOCAL_MIN_SECS:
                        if rms > LOCAL_SILENCE_RMS:
                            speech_detected = True
                        continue

                    if not speech_detected and elapsed >= no_speech_max:
                        break

                    if rms > LOCAL_SILENCE_RMS:
                        speech_detected = True
                        silence_start = None
                    else:
                        if speech_detected and silence_start is None:
                            silence_start = elapsed
                        if speech_detected and silence_start is not None:
                            if (elapsed - silence_start) >= silence_secs:
                                break
            break  # stream ran to completion
        except sd.PortAudioError as e:
            print(f"\n  [PortAudio error, attempt {attempt + 1}] {e}")
            if attempt == 0:
                time.sleep(0.5) # let CoreAudio release the device
                continue
            print("  Mic unavailable; saving silent recording and continuing.")

    print()

    if buffer:
        audio_native = np.concatenate(buffer).flatten().astype(np.float32) / 32768.0
        # resample to 16 kHz for Whisper
        audio_16k = librosa.resample(audio_native, orig_sr=native_rate, target_sr=LOCAL_SAMPLE_RATE)
        audio_int16 = (audio_16k * 32768.0).astype(np.int16)
    else:
        audio_int16 = np.zeros((0,), dtype=np.int16)

    # expose whether speech was detected so the transcription gate
    # can use it
    global _local_speech_detected
    _local_speech_detected = speech_detected

    with wave.open(LOCAL_WAV, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(LOCAL_SAMPLE_RATE)
        wf.writeframes(audio_int16.tobytes())
    print(f"  Recording saved ({elapsed:.1f}s, speech={'yes' if speech_detected else 'no'}).")

# Alfie's
def local_say(text: str):
    """Speak text using host OS built-in TTS (macOS `say` or Windows SAPI)."""
    try:
        if sys.platform == "win32":
            # Windows: System.Speech SAPI via PowerShell; env-var passes text
            # safely so quotes/apostrophes in the line don't need escaping.
            subprocess.run(
                ["powershell", "-NoProfile", "-Command",
                 "Add-Type -AssemblyName System.Speech;"
                 "(New-Object System.Speech.Synthesis.SpeechSynthesizer)"
                 ".Speak($env:GAZE_TTS_TEXT)"],
                env={**os.environ, "GAZE_TTS_TEXT": text},
                check=True, timeout=30,
            )
        else:
            subprocess.run(["say", text], check=True, timeout=30)
    except Exception as e:
        print(f"  Local TTS broke: {e}")

def say(ssh_tts, text):
    """Dispatch TTS to local or Pepper depending on mode."""
    if LOCAL_MODE:
        local_say(text)
    else:
        nao_say(ssh_tts, text)
    # Flush speaker buffer before next record(), or the mic captures the TTS tail and Vosk false-positives on "Pepper" in the reply, disabling the gate from turn 2 onwards.
    time.sleep(0.5)

# Alfie's and Salman's
def record(ssh, energy_threshold,
           no_speech_max: float = LOCAL_NO_SPEECH_MAX,
           silence_secs: float = LOCAL_SILENCE_SECS,
           record_max_secs: float = RECORD_MAX_SECS):
    """Dispatch recording to local or Pepper depending on mode; 
       per-turn think-budget set by: AdaptiveEngine.recommend_think_budget()."""
    if LOCAL_MODE:
        local_record(max_secs=record_max_secs,
                     no_speech_max=no_speech_max,
                     silence_secs=silence_secs)
    else:
        nao_record(ssh, energy_threshold,
                   record_max_secs=record_max_secs,
                   silence_secs=silence_secs)

# GESTURE MAPPING (Alfie's)
# Each gesture is a motion sequence aligned to the game/emotional context:
#   - celebrate: arms up + small bicep curls, for thriving moments and milestones
#   - encourage: one arm forward with open hand, for encouragement when struggling
#   - think: one hand on chin, for thinking moments and when user is taking long
#   - wave: friendly wave to re-engage when disengaged
#   - calm: slow open-arm gesture, for calming down when frustrated
#   - energetic: quick open-arm raises, for boosting energy when disengaged or thriving
#   - neutral: resting; no gesture-movements as no need due to neutrualness

GESTURE_CODE = {
    "celebrate": """
from naoqi import ALProxy
import time
m = ALProxy("ALMotion","127.0.0.1",9559)
m.setStiffnesses("Arms", 1.0)
names = ["LShoulderPitch","LShoulderRoll","RShoulderPitch","RShoulderRoll"]
m.angleInterpolation(names, [-0.5, 0.3, -0.5, -0.3], [1.0]*4, True)
time.sleep(0.3)
for _ in range(2):
    m.angleInterpolation(["LElbowRoll","RElbowRoll"], [-1.0, 1.0], [0.3]*2, True)
    m.angleInterpolation(["LElbowRoll","RElbowRoll"], [-0.5, 0.5], [0.3]*2, True)
time.sleep(0.2)
m.angleInterpolation(names, [1.4, 0.2, 1.4, -0.2], [1.0]*4, True)
m.setStiffnesses("Arms", 0.0)
""",
    "encourage": """
from naoqi import ALProxy
import time
m = ALProxy("ALMotion","127.0.0.1",9559)
m.setStiffnesses("RArm", 1.0)
names = ["RShoulderPitch","RShoulderRoll","RElbowRoll","RHand"]
m.angleInterpolation(names, [0.2, -0.2, 0.5, 0.8], [1.0]*4, True)
time.sleep(0.6)
m.angleInterpolation(names, [1.4, -0.2, 0.5, 0.0], [1.0]*4, True)
m.setStiffnesses("RArm", 0.0)
""",
    "think": """
from naoqi import ALProxy
import time
m = ALProxy("ALMotion","127.0.0.1",9559)
m.setStiffnesses("RArm", 1.0)
names = ["RShoulderPitch","RShoulderRoll","RElbowYaw","RElbowRoll","RHand"]
m.angleInterpolation(names, [-0.2, -0.1, 0.5, 1.2, 0.3], [1.2]*5, True)
time.sleep(1.0)
m.angleInterpolation(names, [1.4, -0.2, 1.2, 0.5, 0.0], [1.0]*5, True)
m.setStiffnesses("RArm", 0.0)
""",
    "wave": """
from naoqi import ALProxy
import time
m = ALProxy("ALMotion","127.0.0.1",9559)
m.setStiffnesses("RArm", 1.0)
names = ["RShoulderPitch","RShoulderRoll","RElbowYaw","RElbowRoll","RWristYaw","RHand"]
m.angleInterpolation(names, [-0.5,-0.3,1.0,1.0,0.0,1.0], [1.0]*6, True)
for _ in range(3):
    m.angleInterpolation(["RWristYaw"], [0.5], [0.3], True)
    m.angleInterpolation(["RWristYaw"], [-0.5], [0.3], True)
time.sleep(0.3)
m.angleInterpolation(names, [1.4,0.2,1.2,0.5,0.0,0.0], [1.0]*6, True)
m.setStiffnesses("RArm", 0.0)
""",
    "calm": """
from naoqi import ALProxy
import time
m = ALProxy("ALMotion","127.0.0.1",9559)
m.setStiffnesses("Arms", 1.0)
names = ["LShoulderPitch","LShoulderRoll","LHand","RShoulderPitch","RShoulderRoll","RHand"]
m.angleInterpolation(names, [0.5, 0.3, 0.8, 0.5, -0.3, 0.8], [1.5]*6, True)
time.sleep(0.4)
m.angleInterpolation(["LShoulderPitch","RShoulderPitch"], [0.8, 0.8], [1.5]*2, True)
time.sleep(0.3)
m.angleInterpolation(names, [1.4, 0.2, 0.0, 1.4, -0.2, 0.0], [1.2]*6, True)
m.setStiffnesses("Arms", 0.0)
""",
    "energetic": """
from naoqi import ALProxy
import time
m = ALProxy("ALMotion","127.0.0.1",9559)
m.setStiffnesses("Arms", 1.0)
for _ in range(2):
    m.angleInterpolation(
        ["LShoulderPitch","RShoulderPitch"],
        [0.0, 0.0], [0.5]*2, True)
    m.angleInterpolation(
        ["LShoulderPitch","RShoulderPitch"],
        [0.8, 0.8], [0.5]*2, True)
m.angleInterpolation(
    ["LShoulderPitch","LShoulderRoll","RShoulderPitch","RShoulderRoll"],
    [1.4, 0.2, 1.4, -0.2], [1.0]*4, True)
m.setStiffnesses("Arms", 0.0)
""",
    "neutral": """
from naoqi import ALProxy
m = ALProxy("ALMotion","127.0.0.1",9559)
m.setStiffnesses("Arms", 0.0)
""",
}

# Salman's
def nao_gesture(ssh, gesture_type: str):
    """Execute a gesture on Pepper aligned to the game context."""
    code = GESTURE_CODE.get(gesture_type, GESTURE_CODE["neutral"])
    try:
        nao_run(ssh, code)
    except Exception as e:
        print(f"  Gesture {gesture_type!r} did not play: {e}")


# Alfie's
def measure_volume() -> float:
    """RMS amplitude of the WAV (local and Pepper paths)."""
    try:
        with wave.open(LOCAL_WAV, "rb") as wf:
            raw = wf.readframes(wf.getnframes())
            if len(raw) < 2:
                return 0.0
            samples = struct.unpack(f"<{len(raw) // 2}h", raw)
            return (sum(s * s for s in samples) / len(samples)) ** 0.5
    except Exception as e:
        print(f"  Volume RMS calc failed: {e}")
        return 0.0

# Whisper training-set tic-blacklist on silent/near-silent audio (YouTube outros, CJK fillers); stored pre-normalised so is_known_hallucination() matches regardless of decoration.
WHISPER_HALLUCINATIONS = {
    "thank you for watching",
    "thanks for watching",
    "thank you so much for watching",
    "thanks so much for watching",
    "if you enjoyed the video please subscribe and like it",
    "if you enjoyed this video please like and subscribe",
    "please subscribe and like",
    "please like and subscribe",
    "subscribe and like",
    "ill see you next time",
    "see you next time",
    "thank you", "thanks", "bye",
    "you", "mm", "hmm", "uh", "um",
    "おいしいねにかねしたかな",
    "ご視聴ありがとうございました",
    "ありがとうございました",
    "이 영상은 유료광고를 포함하고 있습니다",
    "구독과 좋아요 부탁드립니다",
}

def normalise_for_blacklist(text: str) -> str:
    """Lowercase + NFKC + strip everything except letters/digits/spaces; thus the blacklist matches independent of Whisper's decorations"""
    t = unicodedata.normalize("NFKC", text).lower()
    kept = [ch for ch in t if ch.isalnum() or ch.isspace()]
    return " ".join("".join(kept).split())

def is_known_hallucination(text: str) -> bool:
    norm = normalise_for_blacklist(text)
    return norm == "" or norm in WHISPER_HALLUCINATIONS # return true if norm post-strip empty or matches a known-hallucination phrase

def has_real_speech(wav_path: str, min_speech_ms: int = 500,
                     threshold: float = 0.6) -> bool:
    """Silero VAD pre-gate."""
    if _silero_model is None or get_speech_timestamps is None:
        return True
    try:
        wav = read_audio(wav_path, sampling_rate=LOCAL_SAMPLE_RATE)
        segments = get_speech_timestamps( # pass in the audio and model to return a list of dicts containing the start and end frame indices of genuine speech
            wav, _silero_model,
            sampling_rate=LOCAL_SAMPLE_RATE,
            min_speech_duration_ms=min_speech_ms,
            threshold=threshold,
            return_seconds=False,
        )
        return bool(segments)
    except Exception as e:
        print(f"  Silero VAD check failed ({e}); falling through to Whisper")
        return True

def has_wake_word(wav_path: str) -> bool:
    """
    Vosk wake-word gate. True only if "Pepper" or "Gaze" is heard in the
    WAV. The 3-token grammar restriction (pepper, gaze, [unk])
    constrains but doesn't eliminate false positives; phonetic
    near-neighbours may still match. Fail-open (returns True) if the
    Vosk model didn't load so the four layers still protect from hallucinations.
    """
    if _vosk_model is None or KaldiRecognizer is None:
        return True
    try:
        rec = KaldiRecognizer(_vosk_model, LOCAL_SAMPLE_RATE,
                              json.dumps(["pepper", "gaze", "[unk]"]))
        with wave.open(wav_path, "rb") as wf:
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                rec.AcceptWaveform(data)
        final = json.loads(rec.FinalResult())
        text = (final.get("text") or "").lower()
        return "pepper" in text or "gaze" in text
    except Exception as e:
        print(f"  Vosk wake-word check failed ({e}); falling through to Whisper")
        return True

# Alfie & Salman's
#open ai whisperings and incase fails and in silent
def transcribe(bypass_wake_word: bool = False,
               whisper_prompt: str = "User answers a quiz or chats with a companion robot.") -> str:
    """
    Transcribe the local WAV with Whisper via a five-layer defence:
      1- existing RMS + speech_detected pre-gate (in conversation_loop)
      2- Silero VAD hard gate (this function)
      3- Vosk wake-word gate (requires "Pepper" or "Gaze")
      4- Whisper's own no_speech_prob + avg_logprob (from verbose_json)
      5- aggressively-normalised hallucination blacklist

    Returns "" on failure, on any gate rejecting, or when the
    transcription normalises to a known-hallucination phrase.

    bypass_wake_word=True disables layer 3 for turns where no wake-word
    is expected (e.g. the first-turn name prompt) — the user wouldn't
    say "Pepper Salman", and Vosk would otherwise silently drop the name.
    whisper_prompt lets the caller steer Whisper's decoding bias (e.g.
    toward first-name tokens, away from Whisper's year-number attractor
    on short utterances like "Salman" → "2016").
    """
    if LOCAL_MODE and not _local_speech_detected:
        return ""

    # Layer 2: Silero VAD hard gate
    if LOCAL_MODE and not has_real_speech(LOCAL_WAV):
        print("  Silero VAD found no speech; skipping Whisper.")
        return ""

    # Layer 3: Vosk wake-word gate. User must say "Pepper"/"Gaze"; catches silent audio that slipped past Layers 1-2 (the original hallucination pain case). Skipped when the caller explicitly says so (name prompt).
    if not bypass_wake_word and not has_wake_word(LOCAL_WAV):
        print("  No wake-word detected; skipping Whisper.")
        return ""

    try:
        with open(LOCAL_WAV, "rb") as fh:
            resp = client.audio.transcriptions.create(
                model="whisper-1",
                file=fh,
                response_format="verbose_json",
                temperature=0.0,
                prompt=whisper_prompt,
                timeout=API_TIMEOUT,
            )
        text = (getattr(resp, "text", "") or "").strip()

        # Layer 4: Whisper self-signals (no_speech_prob + avg_logprob + compression_ratio per segment). resp is a Pydantic TranscriptionVerbose thus attribute access (not dict indexing).
        segments = getattr(resp, "segments", None) or []
        if segments:
            no_speech_vals = [s.no_speech_prob for s in segments
                              if getattr(s, "no_speech_prob", None) is not None]
            logprob_vals = [s.avg_logprob for s in segments
                            if getattr(s, "avg_logprob", None) is not None]
            compression_vals = [s.compression_ratio for s in segments
                                if getattr(s, "compression_ratio", None) is not None]
            if no_speech_vals and max(no_speech_vals) > 0.6:
                print(f"  Whisper flagged silence (max no_speech_prob="
                      f"{max(no_speech_vals):.2f}); dropping {text!r}")
                return ""
            if logprob_vals and min(logprob_vals) < -1.0:
                print(f"  Whisper low-confidence (min avg_logprob="
                      f"{min(logprob_vals):.2f}); dropping {text!r}")
                return ""
            # compression_ratio > 2.4 catches repetition loops (e.g. "Q1. Q1. Q1..."); repeating tokens compress well. 2.4 matches local Whisper's default.
            if compression_vals and max(compression_vals) > 2.4:
                print(f"  Whisper repetition loop (max compression_ratio="
                      f"{max(compression_vals):.2f}); dropping {text!r}")
                return ""

        # Layer 5: aggressively-normalised hallucination blacklist
        if is_known_hallucination(text):
            print(f"  Filtered Whisper hallucination: {text!r}")
            return ""

        # Strip leading "Pepper"/"Gaze" so handlers receive just the answer; \b blocks "Pepperoni"/"Gazebo" false positives..
        stripped = re.sub(r'(?i)^\s*(pepper|gaze)\b[,.\s]*', '', text).strip()
        return stripped
    except Exception as e:
        print(f"  Whisper transcribe failed ({e}); returning empty")
        return ""

# Alfie: FACIAL EXPRESSION PIPELINE

def preview_thread_loop(camera, face_model, face_cascade):
    """Continuous camera preview (daemon thread to prevent **catastrophic** failing 
       because terminating main program this background thread will be 
       terminated automatically and won't freeze when the main program exits"""

    global _last_emotion, _preview_frame
    while True:
        ret, frame = camera.read()
        if not ret:
            time.sleep(0.03)
            continue

        gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            emotion, conf = "Neutral", 0.0
        else:
            x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
            roi     = gray[y:y+h, x:x+w]
            resized = cv2.resize(roi, (48, 48))
            inp     = resized[np.newaxis, :, :, np.newaxis]
            emotion, conf = face_model.predict(inp)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        with _preview_lock:
            _preview_state["emotion"]    = emotion
            _preview_state["confidence"] = conf
        _last_emotion = emotion

        label = f"{emotion} ({conf:.0%})"
        cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 255, 0), 2)
        with _preview_lock:
            _preview_frame = frame.copy()

def start_preview_thread(camera, face_model, face_cascade):
    t = threading.Thread(target=preview_thread_loop,
                         args=(camera, face_model, face_cascade),
                         daemon=True)
    t.start()
    return t

# Alfie's
def capture_and_classify(ssh, face_model, face_cascade,
                         local_camera=None) -> tuple[str, float]:
    """Capture a face image and classify the expression.
       Every non-preview-thread path also pushes the annotated frame into
       the shared _preview_frame/_preview_state so GazeDashboard's camera
       panel stays alive in NAO mode (was black before because only the
       LOCAL_MODE preview thread wrote to _preview_frame)."""
    if DEBUG_PREVIEW and local_camera is not None:
        with _preview_lock:
            return _preview_state["emotion"], _preview_state["confidence"]

    if local_camera is not None: # use local camera if available; if unavailable use NAO
        ret, frame = local_camera.read()
        if not ret:
            print("  [Local camera failed] cv2.VideoCapture.read() returned False")
            return "Neutral", 0.0
    else:
        try:
            nao_capture_image(ssh)
            frame = cv2.imread(LOCAL_IMG)
            if frame is None:
                print(f"  cv2.imread returned None for {LOCAL_IMG}")
                return "Neutral", 0.0
        except Exception as e:
            print(f"  Camera frame grab failed: {e}")
            return "Neutral", 0.0

    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        emotion, conf = "Neutral", 0.0
    else:
        x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
        roi     = gray[y:y+h, x:x+w]
        resized = cv2.resize(roi, (48, 48))
        inp     = resized[np.newaxis, :, :, np.newaxis]     # (1, 48, 48, 1)
        emotion, conf = face_model.predict(inp)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # annotate and publish to the dashboard regardless of source; in NAO mode this is the ONLY writer of _preview_frame, thus the fix for the black-panel bug
    label = f"{emotion} ({conf:.0%})"
    cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                0.8, (0, 255, 0), 2)
    global _preview_frame
    with _preview_lock:
        _preview_state["emotion"]    = emotion
        _preview_state["confidence"] = conf
        _preview_frame = frame.copy()

    return emotion, conf


API_TIMEOUT = 10  # 10-second timeout; prevents Pepper freezing if OpenAI/network stalls

# Alfie's
def check_answer(user_answer: str, correct_answer: str,
                 question_context: str) -> bool:
    """Verify the user's answer via GPT."""
    if not user_answer.strip():
        return False

    try:
        resp = client.chat.completions.create(
            model="gpt-4.1",
            messages=[{
                "role": "system",
                "content": (
                    "You are an answer checker. Given a question, the correct answer, "
                    "and the user's spoken answer, determine if the user is correct. "
                    "Be lenient with pronunciation, phrasing, and partial answers that "
                    "demonstrate knowledge. Respond with ONLY 'correct' or 'incorrect'."
                ),
            }, {
                "role": "user",
                "content": (
                    f"Question: {question_context}\n"
                    f"Correct answer: {correct_answer}\n"
                    f"User's answer: {user_answer}"
                ),
            }],
            temperature=0.0,
            timeout=API_TIMEOUT,
        )
        return "correct" in resp.choices[0].message.content.strip().lower()
    except Exception as e:
        print(f"  Answer verifier API failed: {e}")
        return correct_answer.lower().strip() in user_answer.lower().strip()

# Salman: SAVE/LOAD SESSIONS

def save_session(engine: AdaptiveEngine, preferred_game: Optional[GameType] = None,
                 quiet: bool = False):
    """Save session progress so user can continue later.
       quiet=True suppresses the "Session saved to ..." print, used when saving
       after every round so the log doesn't fill up with save confirmations.
    """
    data = {
        "user_name":        engine.user_name,
        "total_correct":    engine.total_correct,
        "best_streak":      engine.best_streak,
        "games_played":     {g.value: c for g, c in engine.games_played.items()},
        "game_switches":    engine.game_switch_count,
        "last_difficulty":  engine.current_difficulty.value,
        "last_game":        engine.current_game.value,
        "preferred_game":   preferred_game.value if preferred_game else None,
        "rounds_played":    len(engine.history),
        "recent_questions": engine.recent_questions[-10:],
        "round_log":        [
            {
                "round":       r.round_number,
                "game":        r.game_type.value,
                "difficulty":  r.difficulty.value,
                "correct":     r.correct,
                "time":        round(r.response_time, 1),
                "expression":  r.facial_expression,
                "vocal":       r.vocal_emotion,
                "state":       r.inferred_state.value,
            }
            for r in engine.history
        ],
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)
    if not quiet:
        print(f"  Session saved to {SAVE_FILE}")

def load_session() -> Optional[dict]:
    """Load a previously saved session, if one exists."""
    if not os.path.exists(SAVE_FILE):
        return None
    try:
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"  Save file corrupt, ignoring: {e}")
        return None

def restore_engine(save_data: dict) -> AdaptiveEngine:
    """Restore engine state from saved data."""
    engine = AdaptiveEngine()
    engine.user_name = save_data.get("user_name", "")
    engine.total_correct = save_data.get("total_correct", 0)
    engine.best_streak = save_data.get("best_streak", 0)
    engine.game_switch_count = save_data.get("game_switches", 0)
    engine.current_difficulty = Difficulty(save_data.get("last_difficulty", 2))
    engine.current_game = GameType(save_data.get("last_game", "numbers"))
    engine.recent_questions = list(save_data.get("recent_questions", []))[-10:]
    for g_val, count in save_data.get("games_played", {}).items():
        try:
            engine.games_played[GameType(g_val)] = count
        except ValueError as e:
            print(f"  Could not restore game type {g_val!r}: {e}")
    return engine

def delete_save():
    """Remove the save file after a completed session or on user request."""
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)

# Alfie: OPENAI FUNCTION-CALLING TOOLS + CONVERSATION HELPERS

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "generate_game_question",
            "description": (
                "Generate a new countdown-style game question. Call this when "
                "the conversation naturally leads to playing a game."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "game_type": {
                        "type": "string",
                        "enum": ["numbers", "letters"],
                        "description": "Type of countdown game round.",
                    },
                    "difficulty": {
                        "type": "string",
                        "enum": ["EASY", "MEDIUM", "HARD"],
                        "description": "Difficulty level for the question.",
                    },
                },
                "required": ["game_type", "difficulty"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_game_answer",
            "description": (
                "Verify whether the user's spoken answer to the current game "
                "question is correct. Call this after the user gives an answer "
                "to an active game question."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "user_answer": {
                        "type": "string",
                        "description": "What the user said.",
                    },
                    "correct_answer": {
                        "type": "string",
                        "description": "The known correct answer.",
                    },
                    "question_context": {
                        "type": "string",
                        "description": "The original question text for context.",
                    },
                },
                "required": ["user_answer", "correct_answer", "question_context"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "evaluate_last_adaptation",
            "description": (
                "Self-evaluate whether the previous round's adaptive strategy "
                "actually helped the user. Returns a natural-language evaluation."
            ),
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "request_more_time",
            "description": (
                "The user has asked for more time to think about the current "
                "game question. Acknowledge their request warmly."
            ),
            "parameters": {"type": "object", "properties": {}},
        },
    },
]

_signal_context = {"text": ""}

# Alfie's
def build_signal_context(engine: AdaptiveEngine,
                         expression: str, expr_conf: float,
                         vocal_emo: str, vocal_conf: float,
                         vol_rms: float, response_time: float) -> str:
    """Build a signal summary string injected alongside every user message so the LLM can adapt its behaviour to the user's real-time emotional state without explicit adaptive-engine instructions."""
    correctness = engine.rolling_correctness()
    recent_faces = [r.facial_expression for r in engine.history[-3:]]
    recent_vocal = [r.vocal_emotion for r in engine.history[-3:]]

    # map raw budget to a semantic label so the LLM reflects pacing without ever seeing or repeating the raw seconds verbatim in dialogue
    if engine.think_budget_secs >= 17.0:
        pacing = "relaxed and patient"
    elif engine.think_budget_secs <= 13.0:
        pacing = "brisk and energetic"
    else:
        pacing = "standard"

    lines = [
        "--- LIVE SIGNALS ---",
        f"Turn: {engine.round_number}",
        f"Face: {expression} ({expr_conf:.0%})  [PRIMARY signal — trust this first]",
        f"Voice: {vocal_emo} ({vocal_conf:.0%})  [advisory only; the vocal model is noisy and often stuck on 'fearful']",
        f"Volume: {vol_rms:.0f} RMS",
        f"Response time: {response_time:.1f}s",
        f"Rolling accuracy (last {CORRECTNESS_WINDOW}): {correctness:.0%}",
        f"System pacing: {pacing}",
    ]
    if recent_faces:
        lines.append(f"Recent faces: {', '.join(recent_faces)}")
    if recent_vocal:
        lines.append(f"Recent vocal: {', '.join(recent_vocal)}")

    return "\n".join(lines)

def converse(conversation: list, tools: list) -> object:
    """Make an OpenAI chat-completion call with function calling."""
    try:
        resp = client.chat.completions.create(
            model="gpt-4.1",
            messages=conversation,
            tools=tools,
            temperature=0.8, # ensure less randomness
            timeout=API_TIMEOUT,
        )
        return resp.choices[0].message
    except Exception as e:
        print(f"  converse() API failed: {e}")
        return types.SimpleNamespace(
            content="I had a brief network hiccup. Let's keep going! [gesture:think]",
            tool_calls=None, role="assistant")

# Alfie's
def execute_tool_call(tool_name: str, tool_args: dict,
                      engine: AdaptiveEngine, game_state: GameState,
                      conversation: list,
                      preferred_game: Optional[GameType],
                      dashboard=None) -> str:
    """Dispatch a function-calling tool invocation and return a JSON string result."""
    if tool_name == "generate_game_question":
        gt = tool_args.get("game_type", "numbers")
        diff = tool_args.get("difficulty", "MEDIUM")
        result = generate_game_question_internal(gt, diff, recent=engine.recent_questions)
        # record the question so the next generation call sees it in the do-not-repeat list; cap at 10 to keep the prompt short
        new_q = result.get("question", "").strip()
        if new_q:
            engine.recent_questions.append(new_q)
            engine.recent_questions = engine.recent_questions[-10:]
        # sync adaptive engine with LLM's chosen difficulty so the engine's next decide() starts from correct baseline
        try:
            engine.current_difficulty = Difficulty[diff]
        except (KeyError, ValueError):
            pass
        game_state.active = True
        game_state.current_question = result.get("question", "")
        game_state.current_answer   = result.get("answer", "")
        game_state.category         = result.get("category", "")
        return json.dumps(result)

    elif tool_name == "check_game_answer":
        ua  = tool_args.get("user_answer", "")
        ca  = tool_args.get("correct_answer", "")
        ctx = tool_args.get("question_context", "")
        is_correct = check_answer(ua, ca, ctx)
        # push result through so the conversation loop can feed it to engine.decide() and record_round() after completion of the tool chain. last_answer_checked flips the "was_game_answer" switch in conversation_loop; without this flag being set, record_round() was silently skipped and rounds_played/total_correct stayed at 0 even after the user answered correctly
        game_state.last_answer_checked = True
        game_state.last_answer_correct = is_correct
        if game_state.active:
            game_state.active = False
        return json.dumps({"correct": is_correct})

    elif tool_name == "evaluate_last_adaptation":
        evaluation = engine.evaluate_adaptation()
        return json.dumps({"evaluation": evaluation})

    elif tool_name == "request_more_time":
        game_state.waiting = True
        return json.dumps({"acknowledged": True})

    else:
        return json.dumps({"error": f"Unknown tool: {tool_name}"})
    
# Alfie's
def process_llm_response(message, conversation: list,
                         engine: AdaptiveEngine, game_state: GameState,
                         preferred_game: Optional[GameType],
                         dashboard=None) -> str:
    """Handle the LLM response, including any tool call chains."""
    msg_dict = {"role": "assistant", "content": message.content or ""}
    if message.tool_calls: # if tool calls are required inject the function-call into convo history so LLM can decide persistence
        msg_dict["tool_calls"] = [
            {
                "id": tc.id,
                "type": "function",
                "function": {"name": tc.function.name, "arguments": tc.function.arguments},
            }
            for tc in message.tool_calls # iterate over each tool call in the message
        ]
    conversation.append(msg_dict)
    # Cap recursive tool calls at 5 rounds to prevent infinite loops
    max_tool_rounds = 5
    current_msg = message
    for _ in range(max_tool_rounds):
        if not current_msg.tool_calls:
            break # kill loop if no more tool calls

        for tc in current_msg.tool_calls:
            fn_name = tc.function.name
            try:
                fn_args = json.loads(tc.function.arguments)
            except json.JSONDecodeError:
                fn_args = {}

            print(f"  Calling tool {fn_name}({fn_args})")
            result_str = execute_tool_call(
                fn_name, fn_args, engine, game_state,
                conversation, preferred_game, dashboard
            )
            print(f"  Tool returned: {result_str[:120]}")
            # append tool's raw string back to shared context
            conversation.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": result_str,
            })
        # Re-prompt LLM with newly appended tool results to continue chain
        current_msg = converse(conversation, TOOLS)
        resp_dict = {"role": "assistant", "content": current_msg.content or ""}
        if current_msg.tool_calls:
            resp_dict["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                }
                for tc in current_msg.tool_calls
            ]
        conversation.append(resp_dict)

    return current_msg.content or ""

# Salman's
#look for gestures
def extract_gesture(text: str) -> str:
    """Parse a [gesture:TYPE] tag from the LLM's response text."""
    match = re.search(r'\[gesture:(\w+)\]', text) # regex to find [gesture:type]
    if match:
        gesture = match.group(1).lower()
        if gesture in GESTURE_CODE:
            return gesture
    return "neutral"

# Alfie's
def generate_game_question_internal(game_type_str: str, difficulty_str: str,
                                    recent: Optional[list[str]] = None) -> dict:
    """Dedicated sub-call for game question generation via OpenAI.
       recent: last ~10 questions shown to the user; passed to the LLM as a
       do-not-repeat clause so we stop mode-collapsing onto 75/50/6/3/8/1→100."""
    try:
        gt = GameType(game_type_str)
    except ValueError:
        gt = GameType.NUMBERS
    try:
        diff = Difficulty[difficulty_str]
    except (KeyError, ValueError):
        diff = Difficulty.MEDIUM

    # Python-side variety seed; GPT-4.1 at t=0.8 still mode-collapses on this constrained task, so we inject a random token to break the attractor
    import secrets
    variety_seed = secrets.token_hex(3)

    prompt = (
        f"Generate {GAME_DESCRIPTIONS[gt]} at {DIFFICULTY_DESCRIPTIONS[diff]} difficulty.\n\n"
        f"Variety seed (use this to randomise your number/letter choice; different each call): {variety_seed}\n\n"
        "Respond with a JSON object (no markdown, no code fences) with exactly these fields:\n"
        '  "question": string — the game question to ask the user\n'
        '  "answer": string — the correct answer\n'
        '  "category": string — specific topic/category of the question'
    )

    if recent:
        bullets = "\n".join(f"- {q}" for q in recent[-10:])
        prompt += (
            "\n\nDO NOT re-use or closely mimic any of these recently-asked "
            "questions. Pick a clearly different number set / target / letter "
            "set so the user experiences fresh material every round:\n"
            f"{bullets}"
        )

    try:
        resp = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You generate countdown-style game questions. Respond only with valid JSON. Each call must produce a genuinely different question from the previous ones; vary targets, number sets, and letter sets across calls."}, # JSON for the function call
                {"role": "user", "content": prompt},
            ],
            temperature=1.0,
            timeout=API_TIMEOUT,
        )
        content = resp.choices[0].message.content.strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[1] if "\n" in content else content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
        return json.loads(content)
    except json.JSONDecodeError:
        return {"question": content, "answer": "", "category": "general"}
    except Exception as e:
        print(f"  Game question gen failed: {e}")
        return {
            "question": "Let's try a quick one: what is 25 + 17?",
            "answer": "42",
            "category": "arithmetic fallback",
        }

# LED COLOUR MAP
# a colour each state; hues chosen for maximum visual separation on Pepper's LED ring
# (off-white and pale-yellow looked near-identical on grey plastic, so those are gone)
LED_COLOURS = {
    InferredState.THRIVING:    0x0000FF00,   # green
    InferredState.COMFORTABLE: 0x0000FFFF,   # cyan
    InferredState.STRUGGLING:  0x00FFFF00,   # yellow
    InferredState.FRUSTRATED:  0x00FF0000,   # red
    InferredState.DISENGAGED:  0x00FF00FF,   # magenta
}


_STATE_COLOURS = {
    InferredState.THRIVING:     "green",
    InferredState.COMFORTABLE:  "blue",
    InferredState.STRUGGLING:   "orange",
    InferredState.FRUSTRATED:   "red",
    InferredState.DISENGAGED:   "grey",
}

class GazeDashboard:
    """Tkinter dashboard for GAZE."""

    CAMERA_W, CAMERA_H = 400, 300

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GAZE Dashboard")
        self.root.resizable(False, False)

        left = tk.Frame(self.root)
        left.grid(row=0, column=0, padx=8, pady=8, sticky="n")

        self.camera_label = tk.Label(left, bg="black",
                                     width=self.CAMERA_W, height=self.CAMERA_H)
        self.camera_label.pack()

        tk.Label(left, text="Conversation:").pack(anchor="w", pady=(6, 0))
        conv_frame = tk.Frame(left)
        conv_frame.pack()
        self._conv_text = tk.Text(conv_frame, font=("Courier", 10),
                                  width=50, height=10, wrap="word",
                                  state="disabled")
        conv_scroll = tk.Scrollbar(conv_frame, command=self._conv_text.yview)
        self._conv_text.configure(yscrollcommand=conv_scroll.set)
        self._conv_text.pack(side="left", fill="both", expand=True)
        conv_scroll.pack(side="right", fill="y")

        right = tk.Frame(self.root)
        right.grid(row=0, column=1, padx=(0, 8), pady=8, sticky="n")

        tk.Label(right, text="GAZE Dashboard",
                 font=("TkDefaultFont", 14, "bold")).pack(pady=(0, 4))

        self._round_var = tk.StringVar(value="Round: -")
        self._score_var = tk.StringVar(value="Score: 0/0")
        self._streak_var = tk.StringVar(value="Streak: 0")
        for var in (self._round_var, self._score_var, self._streak_var):
            tk.Label(right, textvariable=var).pack(anchor="w")

        # transcription: only what the user said; correct answer stays
        # on stdout so watchers don't read it off the screen mid-game
        tk.Label(right, text="").pack()
        tk.Label(right, text="Transcription:",
                 font=("TkDefaultFont", 10, "bold")).pack(anchor="w")
        self._heard_var = tk.StringVar(value="You said: -")
        self._result_var = tk.StringVar(value="")
        tk.Label(right, textvariable=self._heard_var).pack(anchor="w")
        self._result_label = tk.Label(right, textvariable=self._result_var,
                                      font=("TkDefaultFont", 11, "bold"))
        self._result_label.pack(anchor="w")

        tk.Label(right, text="").pack()
        tk.Label(right, text="Live Signals:",
                 font=("TkDefaultFont", 10, "bold")).pack(anchor="w")
        self._face_var   = tk.StringVar(value="Face (CNN):    -")
        self._voice_var  = tk.StringVar(value="Voice (MLP):   -")
        self._vol_var    = tk.StringVar(value="Volume RMS:    -")
        self._time_var   = tk.StringVar(value="Response time: -")
        self._acc_var    = tk.StringVar(value="Rolling acc:   -")
        self._budget_var = tk.StringVar(value="Think budget:  -")
        for var in (self._face_var, self._voice_var, self._vol_var,
                    self._time_var, self._acc_var, self._budget_var):
            tk.Label(right, textvariable=var,
                     font=("Courier", 10)).pack(anchor="w")

        tk.Label(right, text="").pack()
        tk.Label(right, text="Adaptive Decision:",
                 font=("TkDefaultFont", 10, "bold")).pack(anchor="w")
        self._state_var = tk.StringVar(value="State: -")
        self._state_label = tk.Label(right, textvariable=self._state_var,
                                     font=("TkDefaultFont", 11, "bold"))
        self._state_label.pack(anchor="w")

        self._diff_var  = tk.StringVar(value="Difficulty: -")
        self._tone_var  = tk.StringVar(value="Tone: -")
        self._adapt_var = tk.StringVar(value="Adaptations: -")
        for var in (self._diff_var, self._tone_var, self._adapt_var):
            tk.Label(right, textvariable=var).pack(anchor="w")

        # adaptation-eval note (tiny 'grey' text)
        self._eval_var = tk.StringVar(value="")
        self._eval_label = tk.Label(right, textvariable=self._eval_var,
                                    font=("TkDefaultFont", 9), fg="grey",
                                    wraplength=340, justify="left")
        self._eval_label.pack(anchor="w")

        tk.Button(right, text="Quit (Esc)",
                  command=self.quit_app).pack(pady=(10, 0))

        self.root.bind("<Escape>", lambda e: self.quit_app())
        self.root.bind("<Command-q>", lambda e: self.quit_app())
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)

        self.camera_refresh()
        self.signal_refresh()
        self.root.update()


    def camera_refresh(self):
        global _preview_frame
        with _preview_lock:
            frame = _preview_frame

        if frame is not None:
            rgb   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            small = cv2.resize(rgb, (self.CAMERA_W, self.CAMERA_H))
            img   = ImageTk.PhotoImage(Image.fromarray(small))
            self.camera_label.configure(image=img)
            self.camera_label._photo = img      # prevent garbage collection

        self.root.after(50, self.camera_refresh)   # ~20 fps

    def signal_refresh(self):
        with _preview_lock:
            emotion = _preview_state["emotion"]
            conf    = _preview_state["confidence"]
        self._face_var.set(f"Face (CNN):    {emotion} ({conf:.0%})")
        self.root.after(500, self.signal_refresh)   # 2 Hz

    # thread-safe scheduling: tkinter widgets are main-thread only (macOS); root.after(0, fn) queues fn onto the main loop.

    def on_main(self, fn):
        """Schedule fn to run on the main (tkinter) thread."""
        try:
            self.root.after(0, fn)
        except tk.TclError:
            pass


    def update_robot_speech(self, text: str):
        def apply():
            self._conv_text.configure(state="normal")
            self._conv_text.insert("end", f"Robot: {text}\n\n")
            self._conv_text.see("end")
            self._conv_text.configure(state="disabled")
        self.on_main(apply)

    def append_user_speech(self, text: str):
        def apply():
            self._conv_text.configure(state="normal")
            self._conv_text.insert("end", f"You: {text}\n")
            self._conv_text.see("end")
            self._conv_text.configure(state="disabled")
        self.on_main(apply)

    def update_think_budget(self, secs: float):
        """Update the dashboard's adaptive think-budget diagnostic row."""
        def apply():
            self._budget_var.set(f"Think budget:  {secs:.1f}s")
        self.on_main(apply)

    def update_signals(self, round_num: int, user_answer: str, correct_answer: str,
                       correct: bool, expression: str, expr_conf: float,
                       vocal_emo: str, vocal_conf: float, vol_rms: float,
                       response_time: float, rolling_acc: float,
                       total_correct: int, total_rounds: int, streak: int):
        def apply():
            self._round_var.set(f"Round: {round_num}")
            self._score_var.set(f"Score: {total_correct}/{total_rounds}")
            self._streak_var.set(f"Streak: {streak}")

            self._heard_var.set(f"You said: {user_answer if user_answer else '(silence)'}")
            if not correct_answer:
                self._result_var.set("")
                self._result_label.configure(fg="grey")
            elif correct:
                self._result_var.set("CORRECT")
                self._result_label.configure(fg="green")
            elif not user_answer:
                self._result_var.set("NO ANSWER")
                self._result_label.configure(fg="grey")
            else:
                self._result_var.set("INCORRECT")
                self._result_label.configure(fg="red")

            self._face_var.set(f"Face (CNN):    {expression} ({expr_conf:.0%})")
            self._voice_var.set(f"Voice (MLP):   {vocal_emo} ({vocal_conf:.0%})")

            vol_tag = "(loud)" if vol_rms > 2000 else "(quiet)" if vol_rms < VOLUME_THRESHOLD else "(normal)"
            bar_len = min(int(vol_rms / 250), 20)
            meter = "#" * bar_len + "." * (20 - bar_len)
            self._vol_var.set(f"Volume RMS:    {vol_rms:>5.0f} [{meter}] {vol_tag}")
            self._time_var.set(f"Response time: {response_time:.1f}s")
            self._acc_var.set(f"Rolling acc:   {rolling_acc:.0%}")

        self.on_main(apply)

    def update_decision(self, decision, adaptation_eval: str = None):
        state = decision.inferred_state
        def apply():
            self._state_var.set(f"State: {state.value.upper()}")
            self._state_label.configure(fg=_STATE_COLOURS.get(state, "grey"))
            self._diff_var.set(f"Difficulty: {decision.difficulty.name}")
            self._tone_var.set(f"Tone: {decision.tone}")
            flags = []
            if decision.give_hint:          flags.append("hint")
            if decision.give_encouragement: flags.append("encouragement")
            if decision.switch_game:        flags.append(f"switch -> {decision.game_type.value}")
            self._adapt_var.set(f"Adaptations: {', '.join(flags) if flags else 'none'}")
            self._eval_var.set(adaptation_eval if adaptation_eval else "")
        self.on_main(apply)

    def quit_app(self):
        """Kill the entire process from the GUI; clean exit."""
        print("\n  [Dashboard] Quit requested.")
        self.close()
        os._exit(0)

    def close(self):
        try:
            self.root.destroy()
        except tk.TclError:
            pass

NAME_STRIP_PATTERN = re.compile(
    r"^\s*(?:my name is|i'm|i am|call me|it's|this is|you can call me)\s+",
    re.IGNORECASE,
)
NAME_REJECT_YEAR = re.compile(r"^\d+$")   # "2016", "2012" — Whisper's short-utterance attractor

def build_system_prompt(user_name: str = "") -> str:
    """Return BASE_SYSTEM_PROMPT, optionally appended with a name-injection clause. Called once at session start and again the moment the name is captured so every subsequent LLM turn sees the user's name."""
    if user_name and user_name != "friend":
        return (BASE_SYSTEM_PROMPT
                + f"\nThe user's name is {user_name}. Address them by name "
                  "when it feels natural (not in every sentence).\n")
    return BASE_SYSTEM_PROMPT

def ask_for_name(ssh, ssh_tts, dashboard,
                 energy_threshold: int) -> str:
    """Ask the user for their name once, up-front. Returns the cleaned name
    or the string "friend" on failure (never empty).

    Handles three failure modes observed on-robot:
      - Vosk wake-word gate would otherwise drop the name (user won't say "Pepper Salman") -> bypass_wake_word=True.
      - Whisper hallucinates short names as year-numbers ("Salman" -> "2016") -> first-name-biased whisper_prompt + numeric-only reject.
      - User stays silent (overwhelmed, misses the prompt) -> one retry, then soft fallback to "friend" so the session still proceeds."""
    attempts = [
        "Before we start, may I know what to call you? Just your first name is perfect.",
        "Sorry, I didn't catch that. What's your first name?",
    ]
    whisper_name_prompt = (
        "The user is stating their first name, for example: Alfie, Salman, "
        "Sarah, Tom, Priya, Arjun. Transcribe the name exactly; do not "
        "substitute numbers or dates."
    )

    for attempt_text in attempts:
        say(ssh_tts, attempt_text)
        print(f"\nRobot: {attempt_text}")
        dashboard.update_robot_speech(attempt_text)

        if not LOCAL_MODE:
            nao_set_leds(ssh, "EarLeds", 0x0000FF00, 0.3)
        # longer budget than a normal turn; first-time speakers pause before saying their name
        record(ssh, energy_threshold,
               no_speech_max=7.0, silence_secs=2.5, record_max_secs=10.0)

        raw = transcribe(bypass_wake_word=True,
                         whisper_prompt=whisper_name_prompt).strip()
        if not raw:
            print("  Heard: (silence)")
            dashboard.append_user_speech("(silence)")
            continue
        print(f"  Heard: {raw}")
        dashboard.append_user_speech(raw)

        # strip "my name is", "i'm", etc.; then remove trailing punctuation
        cleaned = NAME_STRIP_PATTERN.sub("", raw).strip(" .!?,").strip()
        if not cleaned:
            continue
        # first token only; "Salman Al-Hammad" collapses to "Salman" for TTS friendliness
        cleaned = cleaned.split()[0]
        # reject digit-only Whisper hallucinations ("2016") and unreasonably long tokens
        if NAME_REJECT_YEAR.match(cleaned) or len(cleaned) > 20:
            print(f"  Rejected name candidate: {cleaned!r}")
            continue
        # title-case so TTS pronounces it naturally and the dashboard looks tidy
        return cleaned.title()

    print("  Could not capture a usable name; falling back to 'friend'.")
    return "friend"


def conversation_loop(dashboard, face_model, face_cascade, speech_model,
                       local_camera, ssh, ssh_tts, energy_threshold):
    """Comprehensive main-conversation loop."""
    preferred_game = None
    engine         = AdaptiveEngine()
    game_state     = GameState()


    save_data = load_session()
    saved_name = (save_data.get("user_name") or "").strip() if save_data else ""
    if save_data:
        prev_rounds  = save_data.get("rounds_played", 0)
        prev_correct = save_data.get("total_correct", 0)

        name_prefix = f", {saved_name}" if saved_name else ""
        welcome_back = (
            f"Welcome back{name_prefix}! Last time you played {prev_rounds} rounds "
            f"and got {prev_correct} correct. "
            "Want to continue where you left off, or start fresh?"
        )
        if not LOCAL_MODE:
            nao_track_face(ssh, enable=True)
            nao_set_leds(ssh, "FaceLeds", 0x0000FF00, 1.0)
            nao_gesture(ssh, "wave")
        say(ssh_tts, welcome_back)
        print(f"\nRobot: {welcome_back}")
        dashboard.update_robot_speech(welcome_back)

        print("\nListening for continue/fresh...")
        if not LOCAL_MODE:
            nao_set_leds(ssh, "EarLeds", 0x0000FF00, 0.3)
        record(ssh, energy_threshold)

        expression, expr_conf = capture_and_classify(
            ssh, face_model, face_cascade, local_camera)
        vocal_emo, vocal_conf = classify_speech_emotion(speech_model, LOCAL_WAV)
        vol_rms = measure_volume()
        dashboard.update_signals(
            round_num=0, user_answer="", correct_answer="", correct=False,
            expression=expression, expr_conf=expr_conf,
            vocal_emo=vocal_emo, vocal_conf=vocal_conf,
            vol_rms=vol_rms, response_time=0, rolling_acc=0,
            total_correct=0, total_rounds=0, streak=0,
        )

        resume_text = transcribe()
        if resume_text:
            print(f"  Heard: {resume_text}")
            dashboard.append_user_speech(resume_text)
        else:
            print("  Heard: (silence)")

        lower_resume = resume_text.lower()
        if any(w in lower_resume for w in ["continue", "resume", "yes", "carry on",
                                            "keep going", "where I left", "left off"]):
            engine = restore_engine(save_data)
            preferred_game = engine.current_game
            restore_msg = (
                f"Restoring your previous session"
                f"{f', {engine.user_name}' if engine.user_name else ''}: "
                f"{save_data.get('rounds_played', 0)} rounds on record."
            )
            say(ssh_tts, restore_msg)
            print(f"\nRobot: {restore_msg}")
        else:
            delete_save()
            fresh_msg = "No worries, starting fresh! Your previous save has been cleared."
            say(ssh_tts, fresh_msg)
            print(f"\nRobot: {fresh_msg}")


    if not LOCAL_MODE:
        nao_track_face(ssh, enable=True)
        nao_set_leds(ssh, "FaceLeds", 0x0000FF00, 1.0)
        nao_gesture(ssh, "wave")

    # ask for the user's name straight away (unless already known from a resumed save). Happens BEFORE the greeting so the LLM can address them personally from turn 1.
    if not engine.user_name:
        engine.user_name = ask_for_name(ssh, ssh_tts, dashboard, energy_threshold)
        # persist immediately so a crash mid-session doesn't lose the name
        save_session(engine, preferred_game, quiet=True)

    conversation = [{"role": "system", "content": build_system_prompt(engine.user_name)}]

    # Build a greeting user-prompt that mentions the name if we captured one; the LLM will weave it into a warm opener without being cheesy
    greeting_directive = (
        "[Give a warm, supportive greeting"
        f"{f' that addresses the user by name ({engine.user_name})' if engine.user_name and engine.user_name != 'friend' else ''}. "
        "Mention you can chat, play games, or just hang out. Keep it to 2 sentences.] "
        "[gesture:wave]"
    )
    greeting_msg = converse(
        conversation + [{"role": "user", "content": greeting_directive}],
        TOOLS,
    )
    greeting_text = greeting_msg.content or "Hello! I'm GAZE, lovely to meet you."
    greeting_gesture = extract_gesture(greeting_text)
    greeting_speech  = re.sub(r'\[gesture:\w+\]', '', greeting_text).strip()

    conversation.append({"role": "assistant", "content": greeting_text})

    if not LOCAL_MODE:
        # Spin nao_gesture into daemon thread so hardware-movement doesn't block the greeting speech and instead parallelises 
        gesture_thread = threading.Thread(
            target=nao_gesture,
            args=(ssh, greeting_gesture), daemon=True
        )
        gesture_thread.start()
    say(ssh_tts, greeting_speech)
    print(f"\nRobot: {greeting_speech}")
    dashboard.update_robot_speech(greeting_speech)


    turn_count = 0
    # silent turns skip the LLM call so the robot doesn't pester: tiered
    # disengagement intervention; tier 1 gentle check-in at 3 silences,
    # tier 2 game-switch at 4. Resets when the user next speaks.
    nudge_level = 0

    try:
        while True:
            turn_count += 1
            print(f"\n{'-' * 40} Turn {turn_count} {'-' * 40}")

            print("Capturing expression...")
            expression, expr_conf = capture_and_classify(
                ssh, face_model, face_cascade, local_camera
            )
            if expr_conf < FACE_CONFIDENCE_THRESHOLD:
                print(f"  Expression: {expression} ({expr_conf:.2f}) — LOW CONFIDENCE, treating as Neutral")
                expression = "Neutral"
            else:
                print(f"  Expression: {expression} ({expr_conf:.2f})")

            question_start = time.time()
            print("Listening...")
            if not LOCAL_MODE:
                # brief cyan pulse on the face LEDs so the user can see the robot is actively listening; ears also go green
                nao_set_leds(ssh, "FaceLeds", 0x0000FFFF, 0.2)
                nao_set_leds(ssh, "EarLeds",  0x0000FF00, 0.3)

            # adaptive think-budget based on previous round's state + current face
            prev_state = (engine.history[-1].inferred_state if engine.history
                          else InferredState.COMFORTABLE)
            prev_rt    = engine.history[-1].response_time if engine.history else 0.0
            no_speech_max, silence_secs, record_max_secs = engine.recommend_think_budget(
                state=prev_state, expression=expression,
                prev_response_time=prev_rt,
                consecutive_silences=engine.consecutive_silences,
                waiting=game_state.waiting,
            )
            dashboard.update_think_budget(record_max_secs)

            record(ssh, energy_threshold,
                   no_speech_max=no_speech_max,
                   silence_secs=silence_secs,
                   record_max_secs=record_max_secs)
            response_time = time.time() - question_start

            vocal_emo, vocal_conf = classify_speech_emotion(speech_model, LOCAL_WAV)
            if vocal_conf < VOICE_CONFIDENCE_THRESHOLD:
                print(f"  Vocal emotion: {vocal_emo} ({vocal_conf:.2f}) — LOW CONFIDENCE, treating as neutral")
                vocal_emo = "neutral"
            else:
                print(f"  Vocal emotion: {vocal_emo} ({vocal_conf:.2f})")

            vol_rms = measure_volume()
            print(f"  Volume RMS: {vol_rms:.0f}")

            # (c) Transcribe; local mode uses the per-chunk speech flag, not file-wide RMS (Mac mic SNR averages badly over silence).
            if LOCAL_MODE:
                # double-gate: speech flag + sustained loudness (vol_rms > 2x floor) stops breath/shuffle spikes triggering a Whisper hallucination.
                if _local_speech_detected and vol_rms > LOCAL_SILENCE_RMS * 2:
                    user_text = transcribe()
                else:
                    print(f"  No real speech detected (speech_flag="
                          f"{_local_speech_detected}, vol_rms={vol_rms:.0f}, "
                          f"floor={LOCAL_SILENCE_RMS}); skipping transcription.")
                    user_text = ""
            elif vol_rms >= VOLUME_THRESHOLD:
                user_text = transcribe()
            else:
                print(f"  Volume ({vol_rms:.0f}) below speech threshold "
                      f"({VOLUME_THRESHOLD}), skipping transcription.")
                user_text = ""

            if user_text:
                print(f"  Heard: {user_text}")
                dashboard.append_user_speech(user_text)
                # user spoke; reset the nudge tier so a future silent
                # spell can re-arm tier 1 and escalate from scratch
                nudge_level = 0
            else:
                print("  Heard: (silence)")
                dashboard.append_user_speech("(silence)")
                engine.consecutive_silences += 1

                # surface signals to the observer dashboard even though
                # the LLM is being skipped this turn
                dashboard.update_signals(
                    round_num=turn_count, user_answer="", correct_answer="",
                    correct=False, expression=expression, expr_conf=expr_conf,
                    vocal_emo=vocal_emo, vocal_conf=vocal_conf,
                    vol_rms=vol_rms, response_time=response_time,
                    rolling_acc=engine.rolling_correctness(),
                    total_correct=engine.total_correct,
                    total_rounds=len(engine.history),
                    streak=engine.consecutive_correct,
                )

                # tiered disengagement intervention (proposal: "intervenes to re-engage them", assistive/stroke-rehab analogue); nudge_level guards so each tier fires at most once per silent spell.
                # tier 1: gentle check-in at 3 consecutive silences
                if engine.consecutive_silences >= 3 and nudge_level < 1:
                    name_clause = (f"(their name is {engine.user_name}) "
                                   if engine.user_name and engine.user_name != "friend"
                                   else "")
                    nudge_prompt = [
                        {"role": "system",
                         "content": build_system_prompt(engine.user_name)},
                        {"role": "user",
                         "content": (f"[The user {name_clause}has been quiet for 3 turns. "
                                     "Offer ONE brief, gentle check-in; no "
                                     "question, no nagging. 1 sentence max. "
                                     "Use their name if given.] "
                                     "[gesture:calm]")},
                    ]
                    nudge_msg = converse(nudge_prompt, [])
                    nudge_text = (nudge_msg.content or "").strip()
                    nudge_speech = re.sub(r'\[gesture:\w+\]', '', nudge_text).strip()
                    if not LOCAL_MODE:
                        # recolour eyes to signal the state has shifted; user sees the shift even if they say nothing back
                        nao_set_leds(ssh, "FaceLeds",
                                     LED_COLOURS[InferredState.DISENGAGED], 0.4)
                    if nudge_speech:
                        say(ssh_tts, nudge_speech)
                        print(f"\nRobot (nudge): {nudge_speech}")
                        dashboard.update_robot_speech(nudge_speech)
                    nudge_level = 1

                # tier 2: still silent after the check-in, switch game + warm re-invitation.
                # threshold 4 (not 5): adaptive think-budget stretches each silent turn, so 5 silences ~= 35-47s of dead air, too long for an assistive-robot analogue thus one processing turn between tiers is sufficient
                elif engine.consecutive_silences >= 4 and nudge_level < 2:
                    engine.current_game = engine.pick_different_game()
                    engine.game_switch_count += 1
                    name_clause = (f"(their name is {engine.user_name}) "
                                   if engine.user_name and engine.user_name != "friend"
                                   else "")
                    escalate_prompt = [
                        {"role": "system",
                         "content": build_system_prompt(engine.user_name)},
                        {"role": "user",
                         "content": (f"[The user {name_clause}has gone silent for 4 turns "
                                     f"in a row, even after the gentle check-in. "
                                     f"Open with ONE short sentence that directly "
                                     f"and warmly acknowledges they've gone quiet "
                                     f"(use their name; don't interrogate, don't "
                                     f"apologise); THEN offer a "
                                     f"{engine.current_game.value} round as a soft "
                                     f"alternative. Two sentences total.] "
                                     f"[gesture:calm]")},
                    ]
                    esc_msg    = converse(escalate_prompt, [])
                    esc_text   = (esc_msg.content or "").strip()
                    esc_speech = re.sub(r'\[gesture:\w+\]', '', esc_text).strip()
                    if not LOCAL_MODE:
                        nao_set_leds(ssh, "FaceLeds",
                                     LED_COLOURS[InferredState.DISENGAGED], 0.4)
                        threading.Thread(target=nao_gesture,
                                         args=(ssh, "wave"), daemon=True).start()
                    if esc_speech:
                        say(ssh_tts, esc_speech)
                        print(f"\nRobot (escalate): {esc_speech}")
                        dashboard.update_robot_speech(esc_speech)
                    nudge_level = 2

                continue   # skip the LLM call; just wait for the user

            if user_text.lower().strip() in [
                "stop", "quit", "exit", "goodbye", "bye", "end",
                "i want to stop", "let's stop", "no more",
            ]:
                print("User wants to stop.")
                break

            signal_ctx = build_signal_context(
                engine, expression, expr_conf,
                vocal_emo, vocal_conf, vol_rms, response_time,
            )

            user_msg_content = f"{signal_ctx}\n\nUser says: {user_text}"
            conversation.append({"role": "user", "content": user_msg_content})

            # trim conversation to prevent context overflow
            # keep system message + last 40 messages (20 exchanges)
            if len(conversation) > 42:
                conversation = [conversation[0]] + conversation[-40:]

            if not LOCAL_MODE:
                nao_set_leds(ssh, "EarLeds", 0x000000FF, 0.3)  # blue = thinking

            llm_message = converse(conversation, TOOLS)

            response_text = process_llm_response(
                llm_message, conversation, engine, game_state,
                preferred_game, dashboard
            )

            if not response_text.strip():
                response_text = "I'm here! What would you like to talk about? [gesture:neutral]"

            gesture_type = extract_gesture(response_text)
            speech_text  = re.sub(r'\[gesture:\w+\]', '', response_text).strip()

            if not LOCAL_MODE:
                if engine.adaptation_log:
                    last_state_str = engine.adaptation_log[-1]["state"]
                    try:
                        last_state = InferredState(last_state_str)
                    except ValueError:
                        last_state = InferredState.COMFORTABLE
                    nao_set_leds(
                        ssh, "FaceLeds",
                        LED_COLOURS.get(last_state, 0x00FFFFFF), 0.5
                    )

                gesture_thread = threading.Thread(
                    target=nao_gesture,
                    args=(ssh, gesture_type), daemon=True
                )
                gesture_thread.start()

            if not LOCAL_MODE and gesture_type in ("celebrate", "encourage"):
                nao_say_animated(ssh_tts, speech_text)
            else:
                say(ssh_tts, speech_text)

            print(f"\nRobot: {speech_text}")
            if game_state.active:
                print(f"(Game answer: {game_state.current_answer})")
            dashboard.update_robot_speech(speech_text)

            # (k) Update dashboard (signals + decision if game active)
            # use the actual answer check result from the tool chain
            was_game_answer = game_state.last_answer_checked
            correct = game_state.last_answer_correct if was_game_answer else False

            # Except when the user just asked for more time; skip the
            # engine so it doesn't wrongly count this turn as a miss (fix)
            if not game_state.waiting:
                decision = engine.decide(
                    expression, expr_conf, response_time,
                    correct=correct,
                    answer_text=user_text,
                    vocal_emotion=vocal_emo, vocal_conf=vocal_conf,
                    volume_rms=vol_rms,
                )
                # Record the round result if it was a game answer; if not, skip recording so it doesn't pollute the history with non-game turns
                if was_game_answer:
                    engine.record_round(RoundResult(
                        round_number=turn_count,
                        game_type=engine.current_game,
                        difficulty=engine.current_difficulty,
                        question=game_state.current_question,
                        user_answer=user_text,
                        correct=correct,
                        response_time=response_time,
                        facial_expression=expression,
                        expression_confidence=expr_conf,
                        vocal_emotion=vocal_emo,
                        vocal_emotion_confidence=vocal_conf,
                        volume_rms=vol_rms,
                        inferred_state=decision.inferred_state,
                    ))
                    # save immediately after every round so a crash or
                    # power-cycle loses at most the current turn, not five
                    save_session(engine, preferred_game, quiet=True)

                game_state.last_answer_checked = False

                dashboard.update_signals(
                    round_num=turn_count, user_answer=user_text,
                    correct_answer=game_state.current_answer if was_game_answer else "",
                    correct=correct,
                    expression=expression, expr_conf=expr_conf,
                    vocal_emo=vocal_emo, vocal_conf=vocal_conf,
                    vol_rms=vol_rms, response_time=response_time,
                    rolling_acc=engine.rolling_correctness(),
                    total_correct=engine.total_correct,
                    total_rounds=len(engine.history),
                    streak=engine.consecutive_correct,
                )
                dashboard.update_decision(decision)
            else:
                game_state.waiting = False
                game_state.last_answer_checked = False
                dashboard.update_signals(
                    round_num=turn_count, user_answer=user_text,
                    correct_answer=game_state.current_answer if game_state.active else "",
                    correct=False,
                    expression=expression, expr_conf=expr_conf,
                    vocal_emo=vocal_emo, vocal_conf=vocal_conf,
                    vol_rms=vol_rms, response_time=response_time,
                    rolling_acc=engine.rolling_correctness(),
                    total_correct=engine.total_correct,
                    total_rounds=len(engine.history),
                    streak=engine.consecutive_correct,
                )

            # belt-and-braces auto-save: even on quiet/chat turns where no round was recorded, flush progress every 2 turns so mid-conversation state (name, recent_questions, streaks) is never stale by more than one turn
            if turn_count % 2 == 0:
                save_session(engine, preferred_game, quiet=True)
                print("  [Auto-save]")

    except KeyboardInterrupt:
        print("\n\nInterrupted.")


    save_session(engine, preferred_game)

    summary = engine.get_session_summary()
    print(f"\n{'=' * 60}")
    print("  SESSION SUMMARY")
    print(f"{'=' * 60}")
    for k, v in summary.items():
        print(f"  {k}: {v}")

    if summary.get("rounds", 0) > 0:
        acc = summary["accuracy"]
        streak_note = (f" Your best streak was {summary['best_streak']} in a row!"
                       if summary["best_streak"] >= 3 else "")
        if acc >= 0.8:
            farewell = (
                f"Amazing session! You got {summary['correct']} out of "
                f"{summary['rounds']} right.{streak_note} "
                "Brilliant work! Your progress is saved; see you next time!"
            )
        elif acc >= 0.5:
            farewell = (
                f"Great effort! You scored {summary['correct']} out of "
                f"{summary['rounds']}.{streak_note} "
                "Well played! Your progress is saved; see you next time!"
            )
        else:
            farewell = (
                f"Thanks for playing! You got {summary['correct']} out of "
                f"{summary['rounds']}.{streak_note} "
                "Every round is a learning opportunity. "
                "Your progress is saved; see you next time!"
            )
    else:
        farewell = "It was lovely chatting! Your progress is saved; see you next time!"

    if not LOCAL_MODE:
        nao_gesture(ssh, "wave")
    say(ssh_tts, farewell)
    print(f"\nRobot: {farewell}")

    if local_camera is not None:
        local_camera.release()
    if not LOCAL_MODE:
        nao_track_face(ssh, enable=False)
        nao_set_leds(ssh, "FaceLeds", 0x00000000, 0.5)
        ssh.close()
        ssh_tts.close()
    dashboard.close()
    print("\nGAZE disconnected.")

def main():
    print("=" * 60)
    print("  GAZE — Game-Adaptive Zone of Engagement")
    print("  Adaptive Game System for Pepper Robot")
    print("=" * 60)

    print("\nLoading facial expression model...")
    face_model   = FacialExpressionModel(MODEL_JSON, MODEL_WEIGHTS)
    face_cascade = cv2.CascadeClassifier(HAAR_CASCADE)
    print("  Facial model loaded.")

    speech_model = None
    if os.path.exists(SPEECH_MODEL):
        print("Loading speech emotion model...")
        speech_model = SpeechEmotionModel(SPEECH_MODEL)
        print("  Speech model loaded.")
    else:
        print(f"  Speech emotion model not found at {SPEECH_MODEL}; vocal signal disabled.")
        print("  Run train_speech_model.py to generate it.")

    local_camera = None
    if USE_LOCAL_CAMERA:
        local_camera = cv2.VideoCapture(0)
        print("  Using local webcam for expression detection.")
        if DEBUG_PREVIEW:
            start_preview_thread(local_camera, face_model, face_cascade)
            print("  Preview thread started.")
    else:
        print("  Using Pepper's camera for expression detection.")

    # connect to Pepper (skipped in local mode)
    ssh     = None
    ssh_tts = None
    energy_threshold = DEFAULT_ENERGY_THRESHOLD

    if LOCAL_MODE:
        print("\n  LOCAL MODE: skipping Pepper connection.")
        print("\nCalibrating Mac microphone ambient noise level...")
        local_calibrate_ambient()
    else:
        print(f"\nConnecting to Pepper at {NAO_IP}...")
        ssh     = ssh_connect()
        ssh_tts = ssh_connect()         # dedicated TTS connection
        print("  Connected.")

        print("\nCalibrating ambient noise level (stay quiet for 3 seconds)...")
        energy_threshold = nao_calibrate_ambient(ssh)

    dashboard = GazeDashboard()
    print("  Dashboard launched.")

    conv_thread = threading.Thread(
        target=conversation_loop,
        args=(dashboard, face_model, face_cascade, speech_model,
              local_camera, ssh, ssh_tts, energy_threshold),
        daemon=True,
    )
    conv_thread.start()

    # tkinter mainloop on main thread (needed for macOS); keep camera preview and GUI responsive while the conversation loop blocks on I/O
    dashboard.root.mainloop()

if __name__ == "__main__":
    main()
