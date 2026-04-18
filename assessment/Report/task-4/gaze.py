"""
GAZE: Game-Adaptive Zone of Engagement

Adaptive countdown-style game host ran on Pepper robot.
Novelty: multi-signal emotional inference: face (WS-10) + voice (WS-08) + response time
+ answer correctness, ... cross-validated so no single signal is trusted alone.



CRITICAL:
- **REMEMBER: PROPOSAL.PDF IS SOURCE OF TRUTH FOR THE INITIAL-INTENDED DESIGN AND FEATURES OF THE CODE.**
- **REMEMBER: CONFIG NAO IP INTO ENV LIKE LAST TIME**

- [ ] offload simpler tasks? to either computation or mini model
- [ ] ensure all facial expression inference is sufficently commented

FUNDAMENTAL:

[] TODO: seperate clearly mine and Salman's code

Alfie's:
---------
- [X] adaptive/chosen difficulties, hints, encouragement, game switching {AdaptiveEngine.decide()` (returns `AdaptiveDecision`)}
- [X] user-volume indicate emotional signals {`measure_volume()`; `local_calibrate_ambient()` (sets `VOLUME_QUIET`/`VOLUME_LOUD`)}
- [X] adaptive-chosen words or numbers based on inferred user state somehow??? — `generate_game_question_internal()` + `build_signal_context()`
- [X] WS-10 CNN facial-expression detection (7-class, 48x48 greyscale) — `FacialExpressionModel.predict()`; `capture_and_classify()`
- [X] WS-08 MLP speech-emotion recognition (MFCC/chroma/mel features) — `SpeechEmotionModel.predict()`; `classify_speech_emotion()`
- [X] countdown-like games (numbers/letters) — `GameType` enum; `generate_game_question_internal()`
- [X] multi-signal state inference (face + voice + time + correctness) — `AdaptiveEngine.infer_state()`
- [X] adaptation self-evaluation (did the previous adaptation help?) — `AdaptiveEngine.evaluate_adaptation()`
- [X] local testing mode (GAZE_LOCAL_MODE) — `local_record()`; `local_say()`; `local_calibrate_ambient()`
- [X] dynamic LLM game generation & answer verification (OpenAI/GPT) — `generate_game_question_internal()`; `check_answer()`
- [X] can give more time if needed
- [X] signal-driven think-time budget — new `AdaptiveEngine.recommend_think_budget()` reading silence, response time, facial expression, inferred state, and the `waiting` flag (NOT trigger phrases); updates `engine.think_budget_secs` / `engine.silence_tolerance_secs` each round
- [X] `request_more_time` (`execute_tool_call()`) becomes one signal among many rather than the sole path — sets `game_state.waiting = True` which feeds `recommend_think_budget()`; never bumps the budget directly
- [X] inject `Think budget: Xs` into `build_signal_context()` so the LLM's dialogue reflects the belief without being told to

Salman's:
---------
- [X] scoring, reward milestones, session save/resume — `AdaptiveEngine.check_reward()`; `save_session()`; `load_session()`; `restore_engine()`
- [X] gestures, LEDs, and speech aligned to inferred state — `nao_gesture()`; `nao_set_leds()`; `extract_gesture()`; `LED_COLOURS` map
- [X] whisper transcription with network timeout fallbacks — `transcribe()`
- [X] ambient noise calibration & dynamic silence detection — `nao_calibrate_ambient()`; `local_calibrate_ambient()`; `record()`/`local_record()` silence loop
- [X] natural TTS sentence-level pacing — `split_into_sentences()`; `nao_say()`; `nao_say_animated()`
- [X] stop the main dashboard leaking the correct answer — remove `_answer_var` label from `GazeDashboard.__init__()` TRANSCRIPTION block; terminal `print(f"(Game answer: ...")` stays for the observer
- [X] plumb the budget through recording — `record()` / `local_record()` / `nao_record()` take `no_speech_max`, `silence_secs` params so the recorder's `LOCAL_NO_SPEECH_MAX` / `LOCAL_SILENCE_SECS` / `SILENCE_DURATION` adapt per-round
- [X] dashboard diagnostic "Think budget" row in `GazeDashboard`'s LIVE SIGNALS — lets the observer watch the belief shift

NICE-TO-HAVE:
- [ ] make web-search capabilities
- [ ] make vision-driven capabilities  
- [ ] capability to fetch time and date if the AI determines its useful, encode this ability into system prompt 

"""

# standard library
import os, re, sys, json, time, wave, struct, tempfile, threading, subprocess, tkinter as tk
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

print("[booting] stdlib loaded", flush=True)

# data + vision
import numpy as np
import cv2
from PIL import Image, ImageTk
print("[booting] numpy + opencv loaded", flush=True)

# networking
import paramiko
print("[booting] paramiko loaded", flush=True)

# audio
import sounddevice as sd
import librosa
import soundfile as sf
print("[booting] audio stack loaded", flush=True)

# venv + API
from dotenv import load_dotenv
from openai import OpenAI
print("[booting] openai loaded", flush=True)

# ML
import joblib
print("[booting] loading tensorflow (this is slow on first run)...", flush=True)
import tensorflow as tf
from tensorflow.keras.models import model_from_json
print("[booting] tensorflow loaded", flush=True)



# -----------------------------------------------------------------------------------



# Silero VAD: pre-Whisper speech-activity gate; think kills most silent-audio
# hallucinations. Fail-open if it doesn't load, thus the
# downstream verbose_json + blacklist layers still protects the code.
try:
    from silero_vad import load_silero_vad, read_audio, get_speech_timestamps
    _silero_model = load_silero_vad()
    print("[booting] silero-vad loaded", flush=True)
except Exception as _vad_err:
    print(f"[booting] silero-vad failed to load ({_vad_err}); VAD gate disabled", flush=True)
    _silero_model = None
    load_silero_vad = None
    read_audio = None
    get_speech_timestamps = None

# unicodedata is stdlib; used by the hallucination blacklist normaliser
import unicodedata

load_dotenv()


# -- Config --

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

# live debug preview (local mode only)
DEBUG_PREVIEW = LOCAL_MODE
_last_rms = 0.0 # shared with recording thread for overlay
_last_emotion = "" # updated by capture_and_classify

# shared state for continuous preview thread
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

# adaptive engine thresholds
RESPONSE_TIME_BASELINE = 30.0 # seconds; beyond this the user is slow
CORRECTNESS_WINDOW     = 5 # rolling window size
CORRECTNESS_FLOOR      = 0.4 # below thus ease off
CORRECTNESS_CEILING    = 0.8 # above thus ramp up
SILENCE_THRESHOLD      = 2 # consecutive non-responses before intervention
MAX_ROUNDS             = 20 # natural session end

# persistent session-save file
SAVE_FILE = os.path.join(SCRIPT_DIR, "gaze_save.json")

if not os.getenv("OPENAI_API_KEY", "").strip():
    raise SystemExit("ERROR: OPENAI_API_KEY not set. Add it to .env")
client = OpenAI()


# FACIAL EXPRESSION MODEL (WS-10)
# --------------------------------

class FacialExpressionModel:
    """Pre-trained CNN: 7-classed emotion classifier (48x48 greyscale input)."""

    EMOTIONS = ["Angry", "Disgust", "Fear", "Happy", "Neutral", "Sad", "Surprise"]

    def __init__(self, model_json_path, model_weights_path):
        with open(model_json_path, "r") as f:
            self.model = model_from_json(f.read())
        self.model.load_weights(model_weights_path)
        self.model.make_predict_function()

    def predict(self, img):
        """Return (emotion_label, confidence) from the (1, 48, 48, 1) array."""
        preds = self.model.predict(img, verbose=0)
        idx = np.argmax(preds)
        return self.EMOTIONS[idx], float(preds[0][idx])


# SPEECH EMOTION MODEL (WS-08)
# --------------------------------

class SpeechEmotionModel:
    """
    Pre-trained MLP for vocal emotion classification (WS-08).
    MFCC + chroma + mel features extracted from the WAV; fed into the
    trained MLP. Runs alongside the face CNN and thus the inference never
    relies singly in terms of sensor.
    """

    EMOTIONS = ["calm", "happy", "fearful", "disgust"]

    def __init__(self, model_path):
        self.model = joblib.load(model_path)

    @staticmethod
    def extract_features(wav_path: str):
        """Extract the same MFCC/chroma/mel feature vector used in WS-08 training."""
        with sf.SoundFile(wav_path) as sound_file:
            audio = sound_file.read(dtype="float32")
            sample_rate = sound_file.samplerate

        if audio.ndim > 1:
            audio = audio.mean(axis=1)

        # peak-normalise so quieter speakers (post-stroke, brain-injured: the
        # actual target population) won't be penalised by the studio-loud
        # training distribution; loudness thus stops being an implicit feature
        audio = librosa.util.normalize(audio)

        n_fft = 2048
        if len(audio) < n_fft:
            return None

        stft = np.abs(librosa.stft(audio, n_fft=n_fft))

        # compute mean (average) frames to consistent vector-length for consistent MLP-input

        # [ ] TODO: explain why it flattens

        mfccs = np.mean(librosa.feature.mfcc(
            y=audio, sr=sample_rate, n_mfcc=40).T, axis=0).flatten()
        
        chroma = np.mean(librosa.feature.chroma_stft(
            S=stft, sr=sample_rate).T, axis=0).flatten()
        
        mel = np.mean(librosa.feature.melspectrogram(
            y=audio, sr=sample_rate).T, axis=0).flatten()

        return np.concatenate([mfccs, chroma, mel])

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


def classify_speech_emotion(speech_model, wav_path: str) -> tuple[str, float]:
    """
    Classify the vocal emotion from a recorded WAV file.
    Returns ("neutral", 0.0) if the model is unavailable, audio is too
    short, or Silero VAD finds no real speech.

    The MLP is a closed-set 4-class classifier (calm/happy/fearful/
    disgust); fed near-silent audio, it confidently picks whichever
    class the feature noise happens to resemble (often "disgust"),
    thus gating on the VAD prevents out-of-distribution false positives.
    """
    if speech_model is None:
        return "neutral", 0.0
    # VAD gate: MLP was trained on speech; running it on silence or
    # background noise is out-of-distribution and produces rubbush
    if LOCAL_MODE and not _has_real_speech(wav_path):
        return "neutral", 0.0
    try:
        return speech_model.predict(wav_path)
    except Exception as e:
        print(f"  Speech emo classify failed: {e}; defaulting to neutral")
        return "neutral", 0.0


# ENUMS AND DATA CLASSES
# ------------------------

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

class GameType(Enum):
    NUMBERS = "numbers"
    LETTERS = "letters"


# -- Personality system --

class Personality(Enum):
    CHEEKY      = "cheeky"
    MENTOR      = "mentor"
    COACH       = "coach"
    THERAPEUTIC = "therapeutic"

# various personalities for the robot
PERSONALITY_PROMPTS = {
    Personality.CHEEKY: (
        "You are playful, witty, and cheeky. You gently tease when the "
        "user gets something wrong, and instead celebrate with over-the-top enthusiasm when "
        "they get it right, and sprinkle in some light humour throughout. Think of "
        "yourself as the user's fun and slightly mischievous friend."
    ),
    Personality.MENTOR: (
        "You are a wise, patient mentor. You explain things clearly, offer "
        "thoughtful encouragement, and guide the user towards understanding "
        "rather than just giving answers. You ask reflective questions and "
        "celebrate growth over raw performance."
    ),
    Personality.COACH: (
        "You are an energetic, motivational coach. You push the user to do "
        "their best, celebrate effort and determination, use direct and "
        "punchy language, and keep the energy high. You believe in the user "
        "and make sure they know it."
    ),
    Personality.THERAPEUTIC: (
        "You are calm, warm, and emotionally attuned. You prioritise the "
        "user's wellbeing above performance, validate their feelings, use a "
        "gentle and reassuring tone, and never rush. If the user seems "
        "stressed or frustrated, you ease off and primarily offer comfort."
    ),
}


BASE_SYSTEM_PROMPT = (
    "You are GAZE, a social-companion robot running on a Pepper humanoid. "
    "You are a companion first and a game host second.\n\n"
    "CONVERSATION GUIDELINES:\n"
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
    "respond warmly in your personality voice.\n"
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
    volume_rms:            float           # speech loudness (arousal signal)
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



# ADAPTIVE ENGINE
# ----------------

class AdaptiveEngine:
    """
    Takes all three input signals and *infers* the user's real state

    The adaptive engine also evaluates whether its previous adaptation
    actually worked, feeding that evaluation into the next round's prompt.
    """

    def __init__(self):
        self.history: list[RoundResult]   = []
        self.current_difficulty            = Difficulty.MEDIUM
        self.current_game                  = GameType.NUMBERS
        self.consecutive_silences          = 0
        self.consecutive_correct           = 0
        self.consecutive_wrong             = 0
        self.games_played: dict[GameType, int] = {g: 0 for g in GameType}
        self.game_switch_count             = 0
        # tracks what adaptation was applied each round (used by evaluate_adaptation)
        self.adaptation_log: list[dict]    = []
        # reward system; milestones already announced
        self.total_correct                 = 0
        self.best_streak                   = 0
        self.rewards_given: set[str]       = set()
        # adaptive think-budget; baseline defaults, updated per round by
        # recommend_think_budget() — signals-driven wait time for the user
        self.think_budget_secs       = float(RECORD_MAX_SECS) # hard ceiling
        self.silence_tolerance_secs  = float(SILENCE_DURATION) # post-speech silence
        self.no_speech_max_secs      = 5.0 # give up if no speech at all

    # -- properties --

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

    # -- multi-signal state inference --

    # volume thresholds for arousal mapping (RMS of 16-bit PCM)
    VOLUME_QUIET = 200 # below this -> low arousal (quiet/disengaged)
    VOLUME_LOUD  = 2000 # above this -> high arousal (excited/frustrated)

    def infer_state(self, expression: str, response_time: float,
                    correct: bool, answer_text: str,
                    vocal_emotion: str = "neutral",
                    volume_rms: float = 0.0) -> InferredState:
        """
        Weigh all signals together to infer the user's actual state.

        Five signals, each noisy on its own:
          1- facial expression  (CNN, WS-10)
          2- vocal emotion      (MLP, WS-08)
          3- response time      (behavioural)
          4- answer correctness (performance)
          5- speech volume/RMS  (arousal)

        No single signal is trusted alone otherwise a resting face reads as
        "Angry" on the CNN, and a cough reads as "fearful" on the MLP.
        Cross-checking against actual performance.
        """
        correctness = self.rolling_correctness()
        clean = answer_text.strip().lower()
        is_silent = (not clean or clean in {"i don't know", "skip", "pass", "next"}) # if no meaningful input OR input matches a phrase in the set (set over list because it's faster/idiomatic for `in` checks: O(1) hashed lookup vs O(n) scan)

        # volume-based arousal: loud -> high arousal, quiet -> low arousal
        high_arousal = volume_rms > self.VOLUME_LOUD
        low_arousal  = 0 < volume_rms < self.VOLUME_QUIET

        # track streaks
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

        # thriving: performing well, voice confirms positive state --
        if (correctness >= CORRECTNESS_CEILING and response_time < RESPONSE_TIME_BASELINE * 0.5):
            return InferredState.THRIVING
        # voice happy + correct + fast -> thriving even if face is neutral
        if vocal_emotion == "happy" and correct and correctness >= CORRECTNESS_CEILING:
            return InferredState.THRIVING
        # camera says Angry but fast + correct -> they're fine (resting bitch-face)
        if expression == "Angry" and correct and response_time < RESPONSE_TIME_BASELINE * 0.6:
            return InferredState.COMFORTABLE

        # disengaged: multiple signals pointing to checked-out (Stroke-ward insight via Dr. Amir) --
        if self.consecutive_silences >= SILENCE_THRESHOLD:
            return InferredState.DISENGAGED
        if (expression == "Neutral"
                and response_time > RESPONSE_TIME_BASELINE
                and correctness < 0.5):
            return InferredState.DISENGAGED
        # quiet voice + neutral face + slow -> disengaged (confirmed low-arousal)
        if (low_arousal and expression == "Neutral"
                and response_time > RESPONSE_TIME_BASELINE * 0.8):
            return InferredState.DISENGAGED

        # frustrated: both modalities agree on negative state --
        if expression in ("Angry", "Disgust") and correctness < CORRECTNESS_FLOOR:
            return InferredState.FRUSTRATED
        if self.consecutive_wrong >= 3 and expression in ("Angry", "Sad", "Fear"):
            return InferredState.FRUSTRATED
        # loud voice + negative face + failing -> frustrated (confirmed high-arousal)
        if (high_arousal and expression in ("Angry", "Disgust", "Fear")
                and correctness < CORRECTNESS_FLOOR):
            return InferredState.FRUSTRATED
        # voice fearful/disgust + face negative + low correctness -> frustrated
        if (vocal_emotion in ("fearful", "disgust")
                and expression in ("Angry", "Sad", "Fear", "Disgust")
                and correctness < CORRECTNESS_FLOOR):
            return InferredState.FRUSTRATED

        # struggling: declining performance + negative signals --
        if expression == "Sad" and response_time > RESPONSE_TIME_BASELINE * 0.7:
            return InferredState.STRUGGLING
        if correctness < CORRECTNESS_FLOOR:
            return InferredState.STRUGGLING
        if expression == "Fear" and not correct:
            return InferredState.STRUGGLING
        # voice fearful + not correct -> struggling (even if face is neutral)
        if vocal_emotion == "fearful" and not correct:
            return InferredState.STRUGGLING

        # cross-modal override: voice calm + performing OK -> comfortable --
        # prevents false negatives where camera reads a frown but voice is calm
        if vocal_emotion == "calm" and correctness >= 0.5:
            return InferredState.COMFORTABLE

        # default: comfortable --
        return InferredState.COMFORTABLE

    # -- core decision function --

    def decide(self, expression: str, expression_conf: float,
               response_time: float, correct: bool,
               answer_text: str,
               vocal_emotion: str = "neutral",
               volume_rms: float = 0.0) -> AdaptiveDecision:
        """Return what to do next based on the inferred state."""
        state       = self.infer_state(expression, response_time, correct, answer_text,
                                       vocal_emotion, volume_rms=volume_rms)
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

        # commit
        self.current_difficulty = new_difficulty
        if switch_game:
            self.current_game = new_game
            self.game_switch_count += 1

        # log this round's adaptation for evaluate_adaptation()
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
        expression, inferred state all contribute independently.
        """
        # baseline budget (fast-track: thriving / comfortable)
        no_speech_max   = 5.0
        silence_secs    = float(SILENCE_DURATION)
        record_max_secs = float(RECORD_MAX_SECS)

        # round 1: no history, no inferred baseline. Be generous with an
        # unseen user, especially in a stroke-recovery deployment where
        # aphasia makes the standard 1.5s silence tolerance unrealistic.
        # Placed before the rule block so later signals can still push higher.
        if not self.history:
            no_speech_max   = max(no_speech_max, 7.0)
            silence_secs    = max(silence_secs, 2.5)
            record_max_secs = max(record_max_secs, 15.0)

        # state-driven extension: hesitant users need breathing room
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

        # facial expression cue: pensive faces suggest thinking in progress
        if expression in ("Sad", "Fear"):
            no_speech_max = max(no_speech_max, 7.0)
            silence_secs  = max(silence_secs, 2.0)

        # previous response time: slow prior turn hints more time is needed
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

        # expose for dashboard diagnostic + signal-context injection
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

    def check_reward(self) -> Optional[str]:
        """
        Check if the user hit a milestone.
        Returns a reward instruction for the prompt, or None.
        Each milestone fires once per session.
        """
        milestones = [
            ("streak_3",  self.consecutive_correct >= 3,
             "The user just got 3 in a row! Announce 'Hat trick!' and celebrate."),
            ("streak_5",  self.consecutive_correct >= 5,
             "The user is on a 5-answer streak! Announce 'Five-star streak!' "
             "and be genuinely amazed."),
            ("streak_10", self.consecutive_correct >= 10,
             "Incredible — 10 correct in a row! Announce 'Unstoppable!' "
             "and make a big deal of it."),
            ("total_5",   self.total_correct >= 5 and "total_5" not in self.rewards_given,
             "The user has reached 5 correct answers total. Briefly acknowledge the milestone."),
            ("total_10",  self.total_correct >= 10 and "total_10" not in self.rewards_given,
             "The user has hit double digits — 10 correct total! Congratulate them."),
            ("total_15",  self.total_correct >= 15 and "total_15" not in self.rewards_given,
             "15 correct answers! The user is on fire. Acknowledge it enthusiastically."),
        ]
        for key, condition, message in milestones:
            if condition and key not in self.rewards_given:
                self.rewards_given.add(key)
                return message
        return None

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

    # -- adaptation self-evaluation --

    def evaluate_adaptation(self) -> Optional[str]:
        """
        Evaluate whether the previous round's adaptation actually worked.

        Compares the inferred state and performance before and after the
        last adaptation decision, returning a natural-language evaluation
        that is fed into the next prompt so the LLM can adjust accordingly.
        """
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

        # check if a difficulty decrease help a struggling/frustrated user
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

        # did a game switch help?
        if prev_action.get("switch"):
            if curr_state in ("thriving", "comfortable"):
                evaluations.append(
                    "Game switch WORKED: user transitioned to a positive state."
                )
            elif curr_state in ("struggling", "frustrated", "disengaged"):
                evaluations.append(
                    "Game switch DID NOT HELP: user is still in a negative state."
                )

        # did encouragement speed up response?
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


# DYNAMIC PROMPT CONSTRUCTION
# ----------------------------

GAME_DESCRIPTIONS = {
    GameType.NUMBERS: (
        "a Countdown-style numbers round: give the user a set of numbers "
        "(e.g. 25, 50, 75, 100 and some small numbers 1-10) and a target number. "
        "The user must combine the given numbers using +, -, *, / to reach the target. "
        "Make sure the target is reachable from the given numbers"
    ),
    GameType.LETTERS: (
        "a Countdown-style letters round: give the user a set of 9 random letters "
        "(a mix of vowels and consonants) and ask them to form the longest word possible "
        "using only those letters. Each letter can only be used once"
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


# -----------------------------------------------------
# SSH AND PEPPER ROBOT HELPERS
# (adapted from lab-robot-code-fin.py i.e. when 
#  we tested OpenAI on the NAO robot perhaps too early)
# -----------------------------------------------------

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


def nao_calibrate_ambient(ssh) -> int:
    """
    Calibrate the mic energy threshold to the room.
    Sample front-mic energy for CALIBRATION_SECS via ALAudioDevice,
    then set threshold = ambient + ENERGY_BUFFER. Without this, a noisy
    room triggers speech detection constantly, and a quiet room misses
    genuine speech.
    """
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


def nao_record(ssh, energy_threshold: int = DEFAULT_ENERGY_THRESHOLD,
               record_max_secs: float = RECORD_MAX_SECS,
               silence_secs: float = SILENCE_DURATION):
    """
    Record audio on Pepper with dynamic silence detection.

    Polls ALAudioDevice front-mic energy rather than using a fixed
    sleep. Stops when:
      1- speech detected (energy above threshold), THEN
      2- SILENCE_DURATION seconds of silence after speech ends, OR
      3- RECORD_MAX_SECS hard ceiling hit.

    energy_threshold comes from nao_calibrate_ambient() so the recorder
    adapts to the room. If getFrontMicEnergy() is unsupported on this
    firmware, falls back to a fixed-duration recording.
    """
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


def split_into_sentences(text: str) -> list[str]:
    """
    Split dialogue into sentences for speech delivery.
    OpenAI returns dialogue as one unbroken block; without splitting,
    Pepper speaks straight through with no pauses, which sounds robotic.
    Split at (. ? !) whilst keeping abbreviations and decimal numbers.
    """
    # split on sentence-ending punctuation followed by a space or end-of-string
    raw_segments = re.split(r'(?<=[.!?])\s+', text.strip())
    # also split any remaining newlines within segments
    sentences = []
    for seg in raw_segments:
        for line in seg.split("\n"):
            cleaned = line.strip()
            if cleaned:
                sentences.append(cleaned)
    return sentences if sentences else [text.strip()]


def nao_say(ssh, text):
    """
    Speak text on Pepper with sentence-level pausing.
    Sentences are packed into one SSH payload so Pepper handles the
    loop locally. One-SSH-call-per-sentence would add ~1s of round-trip
    per sentence; the 0.4s inter-sentence pause gets lost in that.
    """
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


def nao_set_leds(ssh, group, colour, duration=1.0):
    try:
        nao_run(ssh, f"""
from naoqi import ALProxy
ALProxy("ALLeds","127.0.0.1",9559).fadeRGB("{group}", {colour}, {duration})
""")
    except Exception as e:
        print(f"  LED set ignored: {e}")


# ------------------------------------------------------------------------------
# LOCAL MODE HELPERS (Mac; no Pepper required)
# ------------------------------------------------------------------------------

LOCAL_SAMPLE_RATE = 16000   # Whisper expects 16 kHz; we resample from native rate


LOCAL_SILENCE_RMS   = 40 # default RMS; overridden by local_calibrate_ambient()
_local_speech_detected = False # set by local_record(); used as transcription gate
LOCAL_SILENCE_SECS  = 1.5 # seconds of post-speech silence to stop recording
LOCAL_MIN_SECS      = 1.0 # minimum recording before silence detection kicks in
LOCAL_NO_SPEECH_MAX = 5.0 # stop if no speech detected at all after this many seconds
LOCAL_ENERGY_BUFFER = 50 # margin above ambient baseline for speech detection


def local_calibrate_ambient() -> int:
    """
    Calibrate the local-testing (Mac) mic's ambient noise level; mirrors
    nao_calibrate_ambient() so LOCAL_MODE testing behaves like the robot.
    Sample for CALIBRATION_SECS; set threshold = ambient +
    LOCAL_ENERGY_BUFFER. Without this, the recorder runs to its ceiling
    in any room noisier than the hardcoded default.
    """
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


def local_record(max_secs: float = RECORD_MAX_SECS,
                 no_speech_max: float = LOCAL_NO_SPEECH_MAX,
                 silence_secs: float = LOCAL_SILENCE_SECS):
    """
    Record audio from the Mac's built-in microphone to LOCAL_WAV with
    silence detection mirroring Pepper's dynamic recording behaviour.

    Records at the device's native sample rate then resamples to 16 kHz
    for Whisper compatibility via librosa.
    """
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

    for attempt in range(2):
        try:
            with sd.InputStream(samplerate=native_rate, channels=1, dtype="int16",
                                blocksize=chunk_size, callback=callback):
                while elapsed < max_secs:
                    time.sleep(SILENCE_POLL_SECS)
                    elapsed += SILENCE_POLL_SECS

                    if not buffer:
                        continue
                    data = buffer[-1]

                    rms = (np.mean(data.astype(np.float64) ** 2)) ** 0.5
                    global _last_rms
                    _last_rms = rms
                    print(f"\r    [{elapsed:.1f}s] RMS: {rms:.0f} {'▓' if rms > LOCAL_SILENCE_RMS else '░'}", end="", flush=True)

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

    # concatenate all buffered audio at native rate
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


def record(ssh, energy_threshold,
           no_speech_max: float = LOCAL_NO_SPEECH_MAX,
           silence_secs: float = LOCAL_SILENCE_SECS,
           record_max_secs: float = RECORD_MAX_SECS):
    """Dispatch audio recording to local or Pepper depending on mode,
    honouring the per-turn think-budget set by
    AdaptiveEngine.recommend_think_budget()."""
    if LOCAL_MODE:
        local_record(max_secs=record_max_secs,
                     no_speech_max=no_speech_max,
                     silence_secs=silence_secs)
    else:
        nao_record(ssh, energy_threshold,
                   record_max_secs=record_max_secs,
                   silence_secs=silence_secs)


# ------------------------------------------------------------------------------------
# GESTURE MAPPING
# ------------------------------------------------------------------------------------
# Each gesture is a motion sequence aligned to the game/emotional context:
#   - celebrate: arms up + small bicep curls, for thriving moments and milestones
#   - encourage: one arm forward with open hand, for encouragement when struggling
#   - think: one hand on chin, for thinking moments and when user is taking a while
#   - wave: friendly wave to re-engage when disengaged
#   - calm: slow open-arm gesture, for calming down when frustrated
#   - energetic: quick open-arm raises, for boosting energy when disengaged or thriving
#   - neutral: resting; no gesture-movements as no need
# ------------------------------------------------------------------------------------

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


def nao_gesture(ssh, gesture_type: str):
    """Execute a gesture on Pepper aligned to the game context."""
    code = GESTURE_CODE.get(gesture_type, GESTURE_CODE["neutral"])
    try:
        nao_run(ssh, code)
    except Exception as e:
        print(f"  Gesture {gesture_type!r} did not play: {e}")


# ------------------------------------------------------------------------------
# AUDIO ANALYSIS + TRANSCRIPTION
# ------------------------------------------------------------------------------

def measure_volume() -> float:
    """
    RMS amplitude of the recorded WAV (local and Pepper paths).
    Used as the 5th signal; roughly maps to arousal (e.g. loud = excited or
    frustrated, quiet = calm OR disengaged). Just-volume can't tell
    these pairs apart, thus the engine cross-references face/voice/
    correctness to disambiguate.
    """
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

# [ ] TODO: might need to ask gpt-4.1 to infer if something Whisper hallucinates is actually something the user would say

# Whisper hallucinates these training-set tics on silent/near-silent
# audio (YouTube outros, CJK fillers, minimal-token fallbacks). Stored
# pre-normalised (lowercase, punctuation + symbols already stripped),
# thus `_is_known_hallucination()` matches regardless of decoration.
WHISPER_HALLUCINATIONS = {
    # YouTube-outro tics
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
    # generic closings
    "thank you", "thanks", "bye",
    # single-token junk
    "you", "mm", "hmm", "uh", "um",
    # CJK fillers Whisper emits on silence (pre-normalised)
    "おいしいねにかねしたかな",
    "ご視聴ありがとうございました",
    "ありがとうございました",
    # Korean YouTube sponsorship/ad-disclaimer hallucinations
    "이 영상은 유료광고를 포함하고 있습니다",
    "구독과 좋아요 부탁드립니다",
}


def _normalise_for_blacklist(text: str) -> str:
    """
    Lowercase + NFKC + strip everything except letters/digits/spaces;
    thus the blacklist matches independent of Whisper's decorations
    """
    t = unicodedata.normalize("NFKC", text).lower()
    kept = [ch for ch in t if ch.isalnum() or ch.isspace()]
    return " ".join("".join(kept).split())


def _is_known_hallucination(text: str) -> bool:
    norm = _normalise_for_blacklist(text)
    return norm == "" or norm in WHISPER_HALLUCINATIONS


def _has_real_speech(wav_path: str, min_speech_ms: int = 500,
                     threshold: float = 0.6) -> bool:
    """
    Silero VAD pre-gate. True iff at least `min_speech_ms` of actual
    speech is detected in the WAV at probability >= `threshold`.
    Default threshold bumped from Silero's 0.5 to 0.6, and minimum
    duration from 250ms to 500ms, thus background noise + single-syllable
    mic spikes don't pass as speech. Fail-open (returns True) if the
    VAD model didn't load thus downstream layers still protect us.
    """
    if _silero_model is None or get_speech_timestamps is None:
        return True
    try:
        wav = read_audio(wav_path, sampling_rate=LOCAL_SAMPLE_RATE)
        segments = get_speech_timestamps(
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


def transcribe() -> str:
    """
    Transcribe the local WAV with Whisper via a four-layer defence:
      1- existing RMS + speech_detected pre-gate (in conversation_loop)
      2- Silero VAD hard gate (this function)
      3- Whisper's own no_speech_prob + avg_logprob (from verbose_json)
      4- aggressively-normalised hallucination blacklist

    Returns "" on failure, on any gate rejecting the audio, or when the
    transcription normalises to a known-hallucination phrase.
    """
    if LOCAL_MODE and not _local_speech_detected:
        return ""

    # Layer 2: Silero VAD hard gate
    if LOCAL_MODE and not _has_real_speech(LOCAL_WAV):
        print("  Silero VAD found no speech; skipping Whisper.")
        return ""

    try:
        with open(LOCAL_WAV, "rb") as fh:
            resp = client.audio.transcriptions.create(
                model="whisper-1",
                file=fh,
                response_format="verbose_json",
                temperature=0.0,
                prompt="User answers a quiz or chats with a companion robot.",
                timeout=API_TIMEOUT,
            )
        text = (getattr(resp, "text", "") or "").strip()

        # Layer 3: Whisper's own per-segment silence + low-confidence
        # signals. `resp` is a Pydantic TranscriptionVerbose; segments
        # are objects, thus attribute access (not dict indexing).
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
            # compression_ratio > 2.4 catches repetition loops like
            # "Q1. Q1. Q1..." — repeating tokens compress very well thus
            # a high ratio indicates Whisper has entered a bad loop. 2.4
            # is the same threshold local Whisper uses internally.
            if compression_vals and max(compression_vals) > 2.4:
                print(f"  Whisper repetition loop (max compression_ratio="
                      f"{max(compression_vals):.2f}); dropping {text!r}")
                return ""

        # Layer 4: aggressively-normalised hallucination blacklist
        if _is_known_hallucination(text):
            print(f"  Filtered Whisper hallucination: {text!r}")
            return ""
        return text
    except Exception as e:
        print(f"  Whisper transcribe failed ({e}); returning empty")
        return ""


# ------------------------------------------------------------------------------
# FACIAL EXPRESSION PIPELINE
# ------------------------------------------------------------------------------

def preview_thread_loop(camera, face_model, face_cascade):
    """
    Continuous camera preview (daemon thread).
    Reads frames, runs face detection + classification, updates the
    shared _preview_state, and stores the annotated frame for the
    dashboard. Runs independently of the game loop so the preview
    doesn't freeze between rounds.
    """
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

        # update shared state for capture_and_classify to read
        with _preview_lock:
            _preview_state["emotion"]    = emotion
            _preview_state["confidence"] = conf
        _last_emotion = emotion

        # annotate frame and store for the tkinter dashboard
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


def capture_and_classify(ssh, face_model, face_cascade,
                         local_camera=None) -> tuple[str, float]:
    """
    Capture a face image and classify the expression.
    Uses Pepper's camera by default; local webcam if GAZE_LOCAL_CAMERA=true.
    Returns (emotion_label, confidence).

    In DEBUG_PREVIEW mode with a local camera, reads from the continuous
    preview thread instead of capturing a new frame (avoids duplicate reads).
    """
    # local mode with preview thread running; just read shared state
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
        return "Neutral", 0.0

    x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
    roi     = gray[y:y+h, x:x+w]
    resized = cv2.resize(roi, (48, 48))
    inp     = resized[np.newaxis, :, :, np.newaxis]     # (1, 48, 48, 1)
    return face_model.predict(inp)


# ------------------------------------------------------------------------------
# OPENAI GAME-GENERATION + ANSWER CHECKING
# ------------------------------------------------------------------------------

API_TIMEOUT = 10  # 10-second timeout; prevents Pepper freezing if OpenAI/network stalls


def check_answer(user_answer: str, correct_answer: str,
                 question_context: str) -> bool:
    """
    Verify the user's spoken answer via GPT. Falls back to naive
    string-containment if the API drops, thus the game loop will-never hangs
    on a single question.
    """
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
        # fallback: naive string match so the game loop continues
        print(f"  Answer verifier API failed: {e}")
        return correct_answer.lower().strip() in user_answer.lower().strip()


# ------------------------------------------------------------------------------
# SAVE/LOAD SESSIONS
# ------------------------------------------------------------------------------

def save_session(engine: AdaptiveEngine, preferred_game: Optional[GameType] = None):
    """Save session progress so user can continue later."""
    data = {
        "total_correct":    engine.total_correct,
        "best_streak":      engine.best_streak,
        "games_played":     {g.value: c for g, c in engine.games_played.items()},
        "game_switches":    engine.game_switch_count,
        "last_difficulty":  engine.current_difficulty.value,
        "last_game":        engine.current_game.value,
        "preferred_game":   preferred_game.value if preferred_game else None,
        "rounds_played":    len(engine.history),
        "rewards_given":    list(engine.rewards_given),
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
    engine.total_correct = save_data.get("total_correct", 0)
    engine.best_streak = save_data.get("best_streak", 0)
    engine.game_switch_count = save_data.get("game_switches", 0)
    engine.current_difficulty = Difficulty(save_data.get("last_difficulty", 2))
    engine.current_game = GameType(save_data.get("last_game", "numbers"))
    engine.rewards_given = set(save_data.get("rewards_given", []))
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


# ------------------------------------------------------------------------------
# OPENAI FUNCTION-CALLING TOOLS + CONVERSATION HELPERS
# ------------------------------------------------------------------------------

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
            "name": "check_reward_milestone",
            "description": (
                "Check whether the user has hit a scoring milestone (e.g. "
                "3-in-a-row streak, 10 total correct). Returns the reward "
                "message if a milestone was reached, otherwise null."
            ),
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_session_summary",
            "description": (
                "Retrieve session statistics: total rounds, accuracy, best "
                "streak, games played, etc."
            ),
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "save_progress",
            "description": "Save the current session to disk so it can be resumed later.",
            "parameters": {"type": "object", "properties": {}},
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
            "name": "select_personality",
            "description": "Switch the robot's personality mode mid-session.",
            "parameters": {
                "type": "object",
                "properties": {
                    "personality": {
                        "type": "string",
                        "enum": ["cheeky", "mentor", "coach", "therapeutic"],
                        "description": "The personality mode to switch to.",
                    },
                },
                "required": ["personality"],
            },
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


# -- shared mutable state for signal injection (set before each converse call) --
_signal_context = {"text": ""}


def build_signal_context(engine: AdaptiveEngine,
                         expression: str, expr_conf: float,
                         vocal_emo: str, vocal_conf: float,
                         vol_rms: float, response_time: float) -> str:
    """
    Build a concise signal summary string that is injected alongside every
    user message so the LLM can adapt its behaviour to the user's real-time
    emotional state without needing explicit adaptive-engine instructions.
    """
    correctness = engine.rolling_correctness()
    recent_faces = [r.facial_expression for r in engine.history[-3:]]
    recent_vocal = [r.vocal_emotion for r in engine.history[-3:]]

    # map raw budget to a semantic label so the LLM reflects pacing without
    # ever seeing or repeating the raw seconds verbatim in dialogue
    if engine.think_budget_secs >= 17.0:
        pacing = "relaxed and patient"
    elif engine.think_budget_secs <= 13.0:
        pacing = "brisk and energetic"
    else:
        pacing = "standard"

    lines = [
        "--- LIVE SIGNALS ---",
        f"Turn: {engine.round_number}",
        f"Face: {expression} ({expr_conf:.0%})",
        f"Voice: {vocal_emo} ({vocal_conf:.0%})",
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
    """
    Make an OpenAI chat-completion call with function calling enabled.
    Returns the raw response message object.
    """
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
        # return a minimal mock so the caller can continue
        class _FallbackMsg:
            content = "I had a brief network hiccup. Let's keep going! [gesture:think]"
            tool_calls = None
            role = "assistant"
        return _FallbackMsg()


def execute_tool_call(tool_name: str, tool_args: dict,
                      engine: AdaptiveEngine, game_state: GameState,
                      conversation: list,
                      preferred_game: Optional[GameType],
                      dashboard=None) -> str:
    """
    Dispatch a function-calling tool invocation and return a JSON string result.
    """
    if tool_name == "generate_game_question":
        gt = tool_args.get("game_type", "numbers")
        diff = tool_args.get("difficulty", "MEDIUM")
        result = generate_game_question_internal(gt, diff)
        # sync adaptive engine with LLM's chosen difficulty so
        # the engine's next decide() starts from the correct baseline
        try:
            engine.current_difficulty = Difficulty[diff]
        except (KeyError, ValueError):
            pass
        # update game state
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
        # propagate result so the conversation loop can feed it to
        # engine.decide() and record_round() after the tool chain completes
        game_state.last_answer_checked = True
        game_state.last_answer_correct = is_correct
        if game_state.active:
            game_state.active = False
        return json.dumps({"correct": is_correct})

    elif tool_name == "check_reward_milestone":
        reward = engine.check_reward()
        return json.dumps({"reward": reward})

    elif tool_name == "get_session_summary":
        return json.dumps(engine.get_session_summary())

    elif tool_name == "save_progress":
        save_session(engine, preferred_game)
        return json.dumps({"saved": True})

    elif tool_name == "evaluate_last_adaptation":
        evaluation = engine.evaluate_adaptation()
        return json.dumps({"evaluation": evaluation})

    elif tool_name == "select_personality":
        p_name = tool_args.get("personality", "mentor")
        try:
            new_p = Personality(p_name)
        except ValueError:
            new_p = Personality.MENTOR
        # update the system message in conversation
        personality_fragment = PERSONALITY_PROMPTS[new_p]
        conversation[0]["content"] = BASE_SYSTEM_PROMPT + "\n\nPERSONALITY:\n" + personality_fragment
        if dashboard is not None:
            dashboard.update_personality(new_p.value.upper())
        return json.dumps({"personality": new_p.value, "applied": True})

    elif tool_name == "request_more_time":
        game_state.waiting = True
        return json.dumps({"acknowledged": True})

    else:
        return json.dumps({"error": f"Unknown tool: {tool_name}"})


def process_llm_response(message, conversation: list,
                         engine: AdaptiveEngine, game_state: GameState,
                         preferred_game: Optional[GameType],
                         dashboard=None) -> str:
    """
    Handle the LLM response, including any tool call chains.
    Returns the final text response from the LLM.
    """
    # append the assistant's (gpt's) message (may include tool calls)
    msg_dict = {"role": "assistant", "content": message.content or ""}
    if message.tool_calls:
        msg_dict["tool_calls"] = [
            {
                "id": tc.id,
                "type": "function",
                "function": {"name": tc.function.name, "arguments": tc.function.arguments},
            }
            for tc in message.tool_calls
        ]
    conversation.append(msg_dict)

    # process tool calls in a loop (the LLM may chain multiple)
    max_tool_rounds = 5
    current_msg = message
    for _ in range(max_tool_rounds):
        if not current_msg.tool_calls:
            break

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

            conversation.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": result_str,
            })

        # call the LLM again so it can respond after processing tool results
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


def extract_gesture(text: str) -> str:
    """
    Parse a [gesture:TYPE] tag from the LLM's response text.
    Returns the gesture type string, defaulting to 'neutral' if not found.
    """
    match = re.search(r'\[gesture:(\w+)\]', text) # regex to find [gesture:type]
    if match:
        gesture = match.group(1).lower()
        if gesture in GESTURE_CODE:
            return gesture
    return "neutral"


def generate_game_question_internal(game_type_str: str, difficulty_str: str) -> dict:
    """
    Dedicated sub-call for game question generation via OpenAI.
    Reuses GAME_DESCRIPTIONS and DIFFICULTY_DESCRIPTIONS.
    Returns {question, answer, category}.
    """
    try:
        gt = GameType(game_type_str)
    except ValueError:
        gt = GameType.NUMBERS
    try:
        diff = Difficulty[difficulty_str]
    except (KeyError, ValueError):
        diff = Difficulty.MEDIUM

    prompt = (
        f"Generate {GAME_DESCRIPTIONS[gt]} at {DIFFICULTY_DESCRIPTIONS[diff]} difficulty.\n\n"
        "Respond with a JSON object (no markdown, no code fences) with exactly these fields:\n"
        '  "question": string — the game question to ask the user\n'
        '  "answer": string — the correct answer\n'
        '  "category": string — specific topic/category of the question'
    )

    try:
        resp = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You generate countdown-style game questions. Respond only with valid JSON."}, # JSON is used for the function call
                {"role": "user", "content": prompt},
            ],
            temperature=0.8,
            timeout=API_TIMEOUT,
        )
        content = resp.choices[0].message.content.strip()
        # strip markdown code fences if present
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


# ------------------------------------------------------------------------------
# LED COLOUR MAP
# ------------------------------------------------------------------------------

LED_COLOURS = {
    InferredState.THRIVING:    0x0000FF00,   # green
    InferredState.COMFORTABLE: 0x00FFFFFF,   # white
    InferredState.STRUGGLING:  0x00FFFF00,   # yellow
    InferredState.FRUSTRATED:  0x00FF8000,   # orange
    InferredState.DISENGAGED:  0x000080FF,   # light-blue
}


# ------------------------------------------------------------------------------
# LIVE DASHBOARD (tkinter)
# ------------------------------------------------------------------------------

# text colours; red = bad, green = good, grey = disengaged
_STATE_COLOURS = {
    InferredState.THRIVING:     "green",
    InferredState.COMFORTABLE:  "blue",
    InferredState.STRUGGLING:   "orange",
    InferredState.FRUSTRATED:   "red",
    InferredState.DISENGAGED:   "grey",
}


class GazeDashboard:
    """
    Tkinter dashboard for GAZE.
    All tk widgets touched on the main thread only (macOS requirement);
    the game loop schedules updates via root.after().
    """

    CAMERA_W, CAMERA_H = 400, 300

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GAZE Dashboard")
        self.root.resizable(False, False)

        # left side: camera + conversation
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

        # right side: signals + decision
        right = tk.Frame(self.root)
        right.grid(row=0, column=1, padx=(0, 8), pady=8, sticky="n")

        tk.Label(right, text="GAZE Dashboard",
                 font=("TkDefaultFont", 14, "bold")).pack(pady=(0, 4))

        # round, score, streak, personality
        self._round_var = tk.StringVar(value="Round: -")
        self._score_var = tk.StringVar(value="Score: 0/0")
        self._streak_var = tk.StringVar(value="Streak: 0")
        self._personality_var = tk.StringVar(value="Personality: MENTOR")
        for var in (self._round_var, self._score_var, self._streak_var,
                    self._personality_var):
            tk.Label(right, textvariable=var).pack(anchor="w")

        # transcription — only what the user said; correct answer stays
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

        # live signals — monospace so columns line up
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

        # adaptive decision
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

        # adaptation-eval note (tiny grey text)
        self._eval_var = tk.StringVar(value="")
        self._eval_label = tk.Label(right, textvariable=self._eval_var,
                                    font=("TkDefaultFont", 9), fg="grey",
                                    wraplength=340, justify="left")
        self._eval_label.pack(anchor="w")

        # quit
        tk.Button(right, text="Quit (Esc)",
                  command=self.quit_app).pack(pady=(10, 0))

        self.root.bind("<Escape>", lambda e: self.quit_app())
        self.root.bind("<Command-q>", lambda e: self.quit_app())
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)

        self.camera_refresh()
        self.signal_refresh()
        self.root.update()

    # -- camera feed refresh (runs via root.after) --

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

    # -- thread-safe scheduling --
    # The game loop runs in a daemon thread; tkinter widgets can only be
    # touched from the main thread. root.after(0, fn) is thread-safe and
    # queues fn to execute on the next mainloop iteration.

    def on_main(self, fn):
        """Schedule fn to run on the main (tkinter) thread."""
        try:
            self.root.after(0, fn)
        except tk.TclError:
            pass

    # -- public update methods (safe to call from any thread) --

    def update_robot_speech(self, text: str):
        def _apply():
            self._conv_text.configure(state="normal")
            self._conv_text.insert("end", f"Robot: {text}\n\n")
            self._conv_text.see("end")
            self._conv_text.configure(state="disabled")
        self.on_main(_apply)

    def append_user_speech(self, text: str):
        def _apply():
            self._conv_text.configure(state="normal")
            self._conv_text.insert("end", f"You: {text}\n")
            self._conv_text.see("end")
            self._conv_text.configure(state="disabled")
        self.on_main(_apply)

    def update_think_budget(self, secs: float):
        """Update the dashboard's adaptive think-budget diagnostic row."""
        def _apply():
            self._budget_var.set(f"Think budget:  {secs:.1f}s")
        self.on_main(_apply)

    def update_signals(self, round_num: int, user_answer: str, correct_answer: str,
                       correct: bool, expression: str, expr_conf: float,
                       vocal_emo: str, vocal_conf: float, vol_rms: float,
                       response_time: float, rolling_acc: float,
                       total_correct: int, total_rounds: int, streak: int):
        def _apply():
            self._round_var.set(f"Round: {round_num}")
            self._score_var.set(f"Score: {total_correct}/{total_rounds}")
            self._streak_var.set(f"Streak: {streak}")

            self._heard_var.set(f"You said: {user_answer if user_answer else '(silence)'}")
            if not correct_answer:
                # just a conversational turn; no game answer to mark
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

            # crude ASCII volume meter; enough to eyeball arousal at a glance
            vol_tag = "(loud)" if vol_rms > 2000 else "(quiet)" if vol_rms < VOLUME_THRESHOLD else "(normal)"
            bar_len = min(int(vol_rms / 250), 20)
            meter = "#" * bar_len + "." * (20 - bar_len)
            self._vol_var.set(f"Volume RMS:    {vol_rms:>5.0f} [{meter}] {vol_tag}")
            self._time_var.set(f"Response time: {response_time:.1f}s")
            self._acc_var.set(f"Rolling acc:   {rolling_acc:.0%}")

        self.on_main(_apply)

    def update_decision(self, decision, adaptation_eval: str = None):
        state = decision.inferred_state
        def _apply():
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
        self.on_main(_apply)

    def update_personality(self, name: str):
        """Update the personality indicator label on the dashboard."""
        self.on_main(lambda: self._personality_var.set(f"Personality: {name}"))

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

def conversation_loop(dashboard, face_model, face_cascade, speech_model,
                       local_camera, ssh, ssh_tts, energy_threshold):
    """
    Main-conversation loop. Run a daemon thread so tkinter
    mainloop stays responsive.

    The LLM drives flow via function calling; it decides when to start
    a game round rather than forcing one every turn. GAZE is thus a
    companion first, game host second.
    """
    preferred_game = None
    engine         = AdaptiveEngine()
    game_state     = GameState()
    active_personality = Personality.MENTOR   # default

    # -- 1. Check for saved session (reuses existing load/restore logic) --

    save_data = load_session()
    if save_data:
        prev_rounds  = save_data.get("rounds_played", 0)
        prev_correct = save_data.get("total_correct", 0)

        welcome_back = (
            f"Welcome back! Last time you played {prev_rounds} rounds "
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

        # classify signals during startup (mirrors main loop)
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
                "Restoring your previous session: "
                f"{save_data.get('rounds_played', 0)} rounds on record."
            )
            say(ssh_tts, restore_msg)
            print(f"\nRobot: {restore_msg}")
        else:
            delete_save()
            fresh_msg = "No worries, starting fresh! Your previous save has been cleared."
            say(ssh_tts, fresh_msg)
            print(f"\nRobot: {fresh_msg}")

    # -- 2. Ask user to pick a personality (verbal or default) --

    if not LOCAL_MODE:
        nao_track_face(ssh, enable=True)
        nao_set_leds(ssh, "FaceLeds", 0x0000FF00, 1.0)
        nao_gesture(ssh, "wave")

    personality_prompt = (
        "Hello! I'm GAZE, your companion. Before we begin, you can pick "
        "my personality: cheeky, mentor, coach, or therapeutic. "
        "Or just say hello and I'll be my usual self!"
    )
    retry_prompt = (
        "Sorry, I didn't catch that. Which personality would you like: "
        "cheeky, mentor, coach, or therapeutic?"
    )

    # up to 3 attempts to hear a valid personality; if still nothing,
    # fall back to MENTOR so the session always starts
    personality_selected = False
    for attempt in range(3):
        prompt = personality_prompt if attempt == 0 else retry_prompt
        say(ssh_tts, prompt)
        print(f"\nRobot: {prompt}")
        dashboard.update_robot_speech(prompt)

        print("\nListening for personality choice...")
        if not LOCAL_MODE:
            nao_set_leds(ssh, "EarLeds", 0x0000FF00, 0.3)
        record(ssh, energy_threshold)

        # classify signals during startup
        # face: CNN (WS-10)
        expression, expr_conf = capture_and_classify(
            ssh, face_model, face_cascade, local_camera)
        # voice: MLP (WS-08)
        vocal_emo, vocal_conf = classify_speech_emotion(speech_model, LOCAL_WAV)
        # volume: arousal proxy
        vol_rms = measure_volume()
        dashboard.update_signals(
            round_num=0, user_answer="", correct_answer="", correct=False,
            expression=expression, expr_conf=expr_conf,
            vocal_emo=vocal_emo, vocal_conf=vocal_conf,
            vol_rms=vol_rms, response_time=0, rolling_acc=0,
            total_correct=0, total_rounds=0, streak=0,
        )

        personality_text = transcribe()
        if personality_text:
            print(f"  Heard: {personality_text}")
            dashboard.append_user_speech(personality_text)
            lower_pt = personality_text.lower()
            for p in Personality:
                if p.value in lower_pt:
                    active_personality = p
                    personality_selected = True
                    break
        else:
            print("  Heard: (silence)")

        if personality_selected:
            break

    if not personality_selected:
        print("  No personality heard after retries; defaulting to MENTOR.")

    print(f"  Active personality: {active_personality.value}")
    dashboard.update_personality(active_personality.value.upper())

    # -- 3. Initialise conversation with system prompt + personality --

    personality_fragment = PERSONALITY_PROMPTS[active_personality]
    conversation = [{"role": "system", "content": (
        BASE_SYSTEM_PROMPT + "\nPERSONALITY:\n" + personality_fragment
    )}]

    # -- 4. Warm greeting (personality-appropriate) --

    greeting_msg = converse(
        conversation + [{"role": "user", "content": (
            f"[The user just chose the {active_personality.value} personality. "
            "Give a warm, personality-appropriate greeting. "
            "Mention you can chat, play games, or just hang out. "
            "Keep it to 2 sentences.] [gesture:wave]"
        )}],
        TOOLS,
    )
    greeting_text = greeting_msg.content or "Hello! I'm GAZE, lovely to meet you."
    # strip the gesture tag for speech but extract it
    greeting_gesture = extract_gesture(greeting_text)
    greeting_speech  = re.sub(r'\[gesture:\w+\]', '', greeting_text).strip()

    conversation.append({"role": "assistant", "content": greeting_text})

    if not LOCAL_MODE:
        gesture_thread = threading.Thread(
            target=nao_gesture,
            args=(ssh, greeting_gesture), daemon=True
        )
        gesture_thread.start()
    say(ssh_tts, greeting_speech)
    print(f"\nRobot: {greeting_speech}")
    dashboard.update_robot_speech(greeting_speech)

    # -- 5. Main conversation loop --

    turn_count = 0
    # silent turns skip the LLM call so the robot doesn't pester; one
    # gentle check-in fires after 3 consecutive silences, then waits
    silence_nudge_fired = False

    try:
        while True:
            turn_count += 1
            print(f"\n{'-' * 40} Turn {turn_count} {'-' * 40}")

            # (a) Capture face expression
            print("Capturing expression...")
            expression, expr_conf = capture_and_classify(
                ssh, face_model, face_cascade, local_camera
            )
            if expr_conf < FACE_CONFIDENCE_THRESHOLD:
                print(f"  Expression: {expression} ({expr_conf:.2f}) — LOW CONFIDENCE, treating as Neutral")
                expression = "Neutral"
            else:
                print(f"  Expression: {expression} ({expr_conf:.2f})")

            # (b) Record audio + measure volume + classify vocal emotion
            question_start = time.time()
            print("Listening...")
            if not LOCAL_MODE:
                nao_set_leds(ssh, "EarLeds", 0x0000FF00, 0.3)

            # adaptive think-budget based on previous round's state + current face;
            # slow prior turn / pensive face / hesitant state => more breathing room
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

            # (c) Transcribe
            # In local mode, trust the recording's own speech_detected flag
            # instead of the full-file volume RMS. Mac mics with low SNR
            # average badly across silence, so the RMS gate would either
            # let Whisper hallucinate a sentence out of room tone, or
            # throw away quiet-but-real speech. On Pepper, the calibrated
            # volume threshold is reliable, so the RMS gate is fine there.
            if LOCAL_MODE:
                # double-gate: per-chunk speech flag AND sustained loudness.
                # _local_speech_detected flips on ANY frame above the silence
                # floor, thus one mic spike (a breath, a shuffle) was enough
                # to fire Whisper; Whisper then hallucinated a training-data
                # phrase ("Thank you for watching") from near-silent audio.
                # Requiring vol_rms > 2x floor means sustained audio energy.
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
                # user spoke; reset the nudge flag so a future silent
                # spell can earn its own one-off check-in
                silence_nudge_fired = False
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

                # one-off gentle check-in after 3 consecutive silences
                # (assistive disengagement intervention from proposal);
                # gated by silence_nudge_fired so subsequent silent turns
                # don't fire repeat nudges
                if engine.consecutive_silences >= 3 and not silence_nudge_fired:
                    nudge_prompt = [
                        {"role": "system",
                         "content": BASE_SYSTEM_PROMPT + "\nPERSONALITY:\n"
                                    + personality_fragment},
                        {"role": "user",
                         "content": ("[The user has been quiet for 3 turns. "
                                     "Offer ONE brief, gentle check-in; no "
                                     "question, no nagging. 1 sentence max.] "
                                     "[gesture:calm]")},
                    ]
                    nudge_msg = converse(nudge_prompt, [])
                    nudge_text = (nudge_msg.content or "").strip()
                    nudge_speech = re.sub(r'\[gesture:\w+\]', '', nudge_text).strip()
                    if nudge_speech:
                        say(ssh_tts, nudge_speech)
                        print(f"\nRobot (nudge): {nudge_speech}")
                        dashboard.update_robot_speech(nudge_speech)
                    silence_nudge_fired = True

                continue   # skip the LLM call; just wait for the user

            # (d) Check exit keywords
            if user_text.lower().strip() in [
                "stop", "quit", "exit", "goodbye", "bye", "end",
                "i want to stop", "let's stop", "no more",
            ]:
                print("User wants to stop.")
                break

            # (e) Build signal context
            signal_ctx = build_signal_context(
                engine, expression, expr_conf,
                vocal_emo, vocal_conf, vol_rms, response_time,
            )

            # (f) Append user message (signals + transcription) to conversation
            user_msg_content = f"{signal_ctx}\n\nUser says: {user_text}"
            conversation.append({"role": "user", "content": user_msg_content})

            # trim conversation to prevent context overflow
            # keep system message + last 40 messages (20 exchanges)
            if len(conversation) > 42:
                conversation = [conversation[0]] + conversation[-40:]

            # (g) Call converse() with tools
            if not LOCAL_MODE:
                nao_set_leds(ssh, "EarLeds", 0x000000FF, 0.3)  # blue = thinking

            llm_message = converse(conversation, TOOLS)

            # (h) Process response (handle tool calls)
            response_text = process_llm_response(
                llm_message, conversation, engine, game_state,
                preferred_game, dashboard
            )

            if not response_text.strip():
                response_text = "I'm here! What would you like to talk about? [gesture:neutral]"

            # (i) Extract gesture
            gesture_type = extract_gesture(response_text)
            speech_text  = re.sub(r'\[gesture:\w+\]', '', response_text).strip()

            # (j) Speak + gesture + LEDs
            if not LOCAL_MODE:
                # LED colour reflects latest inferred state if available
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

            # animated speech for celebratory/encouraging gestures
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

            # except when the user just asked for more time; skip the
            # engine so it doesn't wrongly count this turn as a miss (fix)
            if not game_state.waiting:
                decision = engine.decide(
                    expression, expr_conf, response_time,
                    correct=correct,
                    answer_text=user_text,
                    vocal_emotion=vocal_emo, volume_rms=vol_rms,
                )

                # record round if a game answer was checked this turn
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

            # (l) Auto-save every 5 turns
            if turn_count % 5 == 0:
                save_session(engine, preferred_game)
                print("  [Auto-save]")

    except KeyboardInterrupt:
        print("\n\nInterrupted.")

    # ------------------------------------------------------------------------------
    # SESSION END; save progress + farewell + cleanup
    # ------------------------------------------------------------------------------

    save_session(engine, preferred_game)

    summary = engine.get_session_summary()
    print(f"\n{'=' * 60}")
    print("  SESSION SUMMARY")
    print(f"{'=' * 60}")
    for k, v in summary.items():
        print(f"  {k}: {v}")

    # farewell; adaptive to performance
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

    # cleanup
    if local_camera is not None:
        local_camera.release()
    if not LOCAL_MODE:
        nao_track_face(ssh, enable=False)
        nao_set_leds(ssh, "FaceLeds", 0x00000000, 0.5)
        ssh.close()
        ssh_tts.close()
    dashboard.close()
    print("\nGAZE disconnected.")


# ------------------------------------------------------------------------------
#                                     MAIN-GAME LOOP
# ------------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("  GAZE — Game-Adaptive Zone of Engagement")
    print("  Adaptive Game System for Pepper Robot")
    print("=" * 60)

    # -- load facial expression model (WS-10) --
    print("\nLoading facial expression model...")
    face_model   = FacialExpressionModel(MODEL_JSON, MODEL_WEIGHTS)
    face_cascade = cv2.CascadeClassifier(HAAR_CASCADE)
    print("  Facial model loaded.")

    # -- load speech emotion model (WS-08) --
    speech_model = None
    if os.path.exists(SPEECH_MODEL):
        print("Loading speech emotion model...")
        speech_model = SpeechEmotionModel(SPEECH_MODEL)
        print("  Speech model loaded.")
    else:
        print(f"  Speech emotion model not found at {SPEECH_MODEL}; vocal signal disabled.")
        print("  Run train_speech_model.py to generate it.")

    # -- local camera (dev/testing) --
    local_camera = None
    if USE_LOCAL_CAMERA:
        local_camera = cv2.VideoCapture(0)
        print("  Using local webcam for expression detection.")
        # start continuous preview thread so the debug window never freezes
        if DEBUG_PREVIEW:
            start_preview_thread(local_camera, face_model, face_cascade)
            print("  Preview thread started.")
    else:
        print("  Using Pepper's camera for expression detection.")

    # -- connect to Pepper (skipped in local mode) --
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

        # -- calibrate ambient noise level --
        print("\nCalibrating ambient noise level (stay quiet for 3 seconds)...")
        energy_threshold = nao_calibrate_ambient(ssh)

    # -- launch live dashboard --
    dashboard = GazeDashboard()
    print("  Dashboard launched.")

    # -- run conversation loop in a daemon thread so tkinter mainloop stays live --
    conv_thread = threading.Thread(
        target=conversation_loop,
        args=(dashboard, face_model, face_cascade, speech_model,
              local_camera, ssh, ssh_tts, energy_threshold),
        daemon=True,
    )
    conv_thread.start()

    # tkinter mainloop on main thread (required by macOS); keep camera
    # preview and GUI responsive while the conversation loop blocks on I/O
    dashboard.root.mainloop()

if __name__ == "__main__":
    main()
