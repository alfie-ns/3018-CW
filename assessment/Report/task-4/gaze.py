"""
GAZE: Game-Adaptive Zone of Engagement


- [ ] PROPOSAL.PDF IS SOURCE OF TRUTH FOR THE INTENDED DESIGN AND FEATURES OF THIS CODE.



Adaptive countdown-style game host for the Pepper robot.
Multi-signal emotional inference: face (WS-10) + voice (WS-08) + response time
+ answer correctness, cross-validated so no single signal is trusted alone.

- [ ] adaptive words or numbers based on inferred user state somehow???
- [X] WS-10 CNN facial-expression detection (7-class, 48x48 greyscale)
- [X] WS-08 MLP speech-emotion recognition (MFCC/chroma/mel features)
- [X] countdown-like games (numbers/letters) 
- [X] multi-signal state inference (face + voice + time + correctness)
- [X] adaptive difficulty, hints, encouragement, game switching
- [X] adaptation self-evaluation (did the previous adaptation help?)
- [X] scoring, reward milestones, session save/resume
- [X] gestures, LEDs, and speech aligned to inferred state
- [X] local testing mode (GAZE_LOCAL_MODE)
- [X] dynamic LLM game generation & answer verification (OpenAI/GPT)
- [X] whisper transcription with network timeout fallbacks
- [X] ambient noise calibration & dynamic silence detection
- [X] natural TTS sentence-level pacing

"""

# standard library
import os, re, json, time, wave, struct, tempfile, threading, subprocess
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

print("[boot] stdlib loaded", flush=True)

# data + vision
import numpy as np
import cv2
print("[boot] numpy + opencv loaded", flush=True)

# networking
import paramiko
print("[boot] paramiko loaded", flush=True)

# audio
import sounddevice as sd
import librosa
import soundfile as sf
print("[boot] audio stack loaded", flush=True)

# venv + API
from dotenv import load_dotenv
from openai import OpenAI
print("[boot] openai loaded", flush=True)

# ML
import joblib
print("[boot] loading tensorflow (this is slow on first run)...", flush=True)
import tensorflow as tf
from tensorflow.keras.models import model_from_json
print("[boot] tensorflow loaded", flush=True)

load_dotenv()


# ── Configuration ──

NAO_IP       = os.getenv("NAO_IP", "ROBOT_IP")
NAO_USER     = "nao"
NAO_PASS     = "nao"
RECORD_MAX_SECS    = 12     # hard ceiling — never record longer than this
RECORD_MIN_SECS    = 2      # minimum recording before silence detection kicks in
SILENCE_POLL_SECS  = 0.5    # polling interval for silence detection on Pepper
SILENCE_DURATION   = 1.5    # seconds of silence after speech to trigger stop
CALIBRATION_SECS   = 3      # duration of ambient noise calibration at startup
ENERGY_BUFFER      = 200    # margin above ambient baseline to set speech threshold
DEFAULT_ENERGY_THRESHOLD = 800  # fallback if calibration fails
REMOTE_WAV   = "/var/persistent/home/nao/input.wav"
REMOTE_IMG   = "/var/persistent/home/nao/capture.jpg"
LOCAL_WAV    = os.path.join(tempfile.gettempdir(), "gaze_input.wav")
LOCAL_IMG    = os.path.join(tempfile.gettempdir(), "gaze_capture.jpg")
VOLUME_THRESHOLD = 500  # RMS amplitude; below this the WAV is silence/ambient noise, not speech
SSH_TIMEOUT  = 10
CMD_TIMEOUT  = 60

# live debug preview (local mode only)
DEBUG_PREVIEW = LOCAL_MODE
_last_rms = 0.0          # shared with recording thread for overlay
_last_emotion = ""        # updated by capture_and_classify

# false when connected to pepper; true for testing when no Pepper's camera
USE_LOCAL_CAMERA = os.getenv("GAZE_LOCAL_CAMERA", "false").lower() == "true"

# full local mode — runs entire game loop on Mac without any Pepper connection
# uses local webcam, Mac microphone, and macOS TTS instead of Pepper hardware
LOCAL_MODE = os.getenv("GAZE_LOCAL_MODE", "false").lower() == "true"
if LOCAL_MODE:
    USE_LOCAL_CAMERA = True      # local mode implies local camera

# paths to pre-trained models
SCRIPT_DIR    = os.path.dirname(os.path.abspath(__file__))
WORKSHOP_DIR  = os.path.join(SCRIPT_DIR, "..", "..", "..", "learning", "workshops")
MODEL_JSON    = os.path.join(WORKSHOP_DIR, "[X]-facial-expression-detection", "model.json")
MODEL_WEIGHTS = os.path.join(WORKSHOP_DIR, "[X]-facial-expression-detection", "model_weights.weights.h5")
HAAR_CASCADE  = os.path.join(WORKSHOP_DIR, "[X]-ws-10", "haarcascade_frontalface_default.xml")
SPEECH_MODEL  = os.path.join(SCRIPT_DIR, "speech_emotion_model.pkl")

# adaptive engine thresholds
RESPONSE_TIME_BASELINE = 30.0   # seconds — beyond this, user is slow
CORRECTNESS_WINDOW     = 5      # rolling window size
CORRECTNESS_FLOOR      = 0.4    # below thus ease off
CORRECTNESS_CEILING    = 0.8    # above thus ramp up
SILENCE_THRESHOLD      = 2      # consecutive non-responses before intervention
MAX_ROUNDS             = 20     # natural session end

# persistent session save file
SAVE_FILE = os.path.join(SCRIPT_DIR, "gaze_save.json")

if not os.getenv("OPENAI_API_KEY", "").strip():
    raise SystemExit("ERROR: OPENAI_API_KEY not set. Add it to .env")
client = OpenAI()


#  FACIAL EXPRESSION MODEL (WS-10)
# --------------------------------

class FacialExpressionModel:
    """Pre-trained CNN — 7-class emotion classifier (48x48 greyscale input)."""

    EMOTIONS = ["Angry", "Disgust", "Fear", "Happy", "Neutral", "Sad", "Surprise"]

    def __init__(self, model_json_path, model_weights_path):
        with open(model_json_path, "r") as f:
            self.model = model_from_json(f.read())
        self.model.load_weights(model_weights_path)
        self.model.make_predict_function()

    def predict(self, img):
        """Return (emotion_label, confidence) from a (1, 48, 48, 1) array."""
        preds = self.model.predict(img, verbose=0)
        idx = np.argmax(preds)
        return self.EMOTIONS[idx], float(preds[0][idx])


#  SPEECH EMOTION MODEL (WS-08)
# --------------------------------

class SpeechEmotionModel:
    """
    Pre-trained MLP for vocal emotion classification (WS-08).

    Extracts MFCC, chroma, and mel spectrogram features from a WAV file
    and classifies the speaker's emotional state. This provides a second,
    independent modality alongside the facial expression CNN — thereby
    preventing over-reliance on any single sensor.
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

        n_fft = 2048
        if len(audio) < n_fft:
            return None

        stft = np.abs(librosa.stft(audio, n_fft=n_fft))

        mfccs  = np.mean(librosa.feature.mfcc(
            y=audio, sr=sample_rate, n_mfcc=40).T, axis=0).flatten()
        chroma = np.mean(librosa.feature.chroma_stft(
            S=stft, sr=sample_rate).T, axis=0).flatten()
        mel    = np.mean(librosa.feature.melspectrogram(
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
    Returns ("neutral", 0.0) if the model is unavailable or audio is too short.
    """
    if speech_model is None:
        return "neutral", 0.0
    try:
        return speech_model.predict(wav_path)
    except Exception as e:
        print(f"  [Speech emotion fallback] {e}")
        return "neutral", 0.0


#  ENUMS AND DATA CLASSES
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

DEFAULT_TONE_PROMPT = (
    "Your personality is warm, encouraging, and supportive. "
    "Celebrate every small win. Use phrases like 'You've got this!' and "
    "'Brilliant effort!' Genuinely cheer the user on."
)

@dataclass
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
    tone:               str     # "encouraging" | "celebratory" | "calm" | "energetic" | "neutral"



#  ADAPTIVE ENGINE
# ----------------

class AdaptiveEngine:
    """
    The brain of GAZE.  Takes all three input signals and *infers* the user's
    real state — crucially, it does NOT just trust the camera.

    Examples of multi-signal reasoning:
      Camera=Angry   + fast correct answers        → fine, resting face.  Carry on.
      Camera=Neutral + long silence + low accuracy → disengaged.  Intervene.
      Camera=Sad     + slow + low correctness       → struggling.  Ease off.
      Camera=Happy   + fast correct answers         → thriving.   Ramp up.

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
        # episodic memory — what strategies worked (learning layer)
        self.strategy_log: list[dict]      = []
        # reward system — milestones already announced
        self.total_correct                 = 0
        self.best_streak                   = 0
        self.rewards_given: set[str]       = set()

    # ── properties --

    @property
    def round_number(self) -> int:
        return len(self.history) + 1

    def rolling_correctness(self) -> float:
        recent = self.history[-CORRECTNESS_WINDOW:]
        if not recent:
            return 0.5                  # no data → assume middle
        return sum(1 for r in recent if r.correct) / len(recent)

    def avg_response_time(self) -> float:
        recent = self.history[-CORRECTNESS_WINDOW:]
        if not recent:
            return RESPONSE_TIME_BASELINE / 2
        return sum(r.response_time for r in recent) / len(recent)

    # ── multi-signal state inference --

    def infer_state(self, expression: str, response_time: float,
                    correct: bool, answer_text: str,
                    vocal_emotion: str = "neutral") -> InferredState:
        """
        Weigh ALL signals together to determine the user's actual state.

        Four independent signals are cross-validated:
          1- facial expression  (visual modality — CNN, WS-10)
          2- vocal emotion      (audio modality — MLP, WS-08)
          3- response time      (behavioural)
          4- answer correctness (performance)

        Neither modality is trusted in isolation — the camera may misread
        a resting face, and the voice model may misclassify background noise.
        Cross-referencing both against performance data yields a more robust
        inference than any single signal alone.
        """
        correctness = self.rolling_correctness()
        is_silent   = (not answer_text.strip()
                       or answer_text.strip().lower() in
                       ["", "i don't know", "skip", "pass", "next"])

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

        # ── thriving: performing well, voice confirms positive state ──
        if (correctness >= CORRECTNESS_CEILING
                and response_time < RESPONSE_TIME_BASELINE * 0.5):
            return InferredState.THRIVING
        # voice happy + correct + fast → thriving even if face is neutral
        if vocal_emotion == "happy" and correct and correctness >= CORRECTNESS_CEILING:
            return InferredState.THRIVING
        # camera says Angry but fast + correct → they're fine (resting face)
        if expression == "Angry" and correct and response_time < RESPONSE_TIME_BASELINE * 0.6:
            return InferredState.COMFORTABLE

        # ── disengaged: multiple signals pointing to checked-out ──
        if self.consecutive_silences >= SILENCE_THRESHOLD:
            return InferredState.DISENGAGED
        if (expression == "Neutral"
                and response_time > RESPONSE_TIME_BASELINE
                and correctness < 0.5):
            return InferredState.DISENGAGED

        # ── frustrated: both modalities agree on negative state ──
        if expression in ("Angry", "Disgust") and correctness < CORRECTNESS_FLOOR:
            return InferredState.FRUSTRATED
        if self.consecutive_wrong >= 3 and expression in ("Angry", "Sad", "Fear"):
            return InferredState.FRUSTRATED
        # voice fearful/disgust + face negative + low correctness → frustrated
        if (vocal_emotion in ("fearful", "disgust")
                and expression in ("Angry", "Sad", "Fear", "Disgust")
                and correctness < CORRECTNESS_FLOOR):
            return InferredState.FRUSTRATED

        # ── struggling: declining performance + negative signals ──
        if expression == "Sad" and response_time > RESPONSE_TIME_BASELINE * 0.7:
            return InferredState.STRUGGLING
        if correctness < CORRECTNESS_FLOOR:
            return InferredState.STRUGGLING
        if expression == "Fear" and not correct:
            return InferredState.STRUGGLING
        # voice fearful + not correct → struggling (even if face is neutral)
        if vocal_emotion == "fearful" and not correct:
            return InferredState.STRUGGLING

        # ── cross-modal override: voice calm + performing OK → comfortable ──
        # prevents false negatives where camera reads a frown but voice is calm
        if vocal_emotion == "calm" and correctness >= 0.5:
            return InferredState.COMFORTABLE

        # ── default: comfortable ──
        return InferredState.COMFORTABLE

    # ── core decision function --

    def decide(self, expression: str, expression_conf: float,
               response_time: float, correct: bool,
               answer_text: str,
               vocal_emotion: str = "neutral") -> AdaptiveDecision:
        """Return what to do next based on inferred state."""
        state       = self.infer_state(expression, response_time, correct, answer_text,
                                       vocal_emotion)
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
                give_encouragement = True       # acknowledge streak

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
                new_game    = self._pick_different_game()

        elif state == InferredState.DISENGAGED:
            tone               = "energetic"
            give_encouragement = True
            if self.consecutive_silences >= 3:
                switch_game = True
                new_game    = self._pick_different_game()

        # commit
        self.current_difficulty = new_difficulty
        if switch_game:
            self.current_game      = new_game
            self.game_switch_count += 1

        # episodic memory — log strategy for the learning layer
        self.strategy_log.append({
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

    def record_round(self, result: RoundResult):
        """Store a completed round in history (semantic memory)."""
        self.history.append(result)
        self.games_played[result.game_type] = (
            self.games_played.get(result.game_type, 0) + 1
        )
        if result.correct:
            self.total_correct += 1
        self.best_streak = max(self.best_streak, self.consecutive_correct)

    def check_reward(self) -> Optional[str]:
        """
        Check if the user hit a reward milestone this round.
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

    def _pick_different_game(self) -> GameType:
        """Toggle between the two countdown game variants."""
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

    # ── adaptation self-evaluation ──

    def evaluate_adaptation(self) -> Optional[str]:
        """
        Evaluate whether the previous round's adaptation actually worked.

        Compares the inferred state and performance before and after the
        last adaptation decision, returning a natural-language evaluation
        that is fed into the next prompt so the LLM can adjust accordingly.
        """
        if len(self.strategy_log) < 2 or len(self.history) < 2:
            return None

        prev_strategy = self.strategy_log[-2]
        curr_strategy = self.strategy_log[-1]
        prev_round    = self.history[-2]
        curr_round    = self.history[-1]

        prev_state  = prev_strategy["state"]
        curr_state  = curr_strategy["state"]
        prev_action = prev_strategy["action"]

        evaluations = []

        # did a difficulty decrease help a struggling/frustrated user?
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


#  DYNAMIC PROMPT CONSTRUCTION
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


def build_game_prompt(engine: AdaptiveEngine, decision: AdaptiveDecision,
                      user_answer: str = "", is_first_round: bool = False,
                      user_game_choice: str = "",
                      adaptation_eval: Optional[str] = None,
                      reward_message: Optional[str] = None) -> str:
    """
    Dynamically construct the OpenAI prompt from live metrics.
    This prompt is NEVER the same twice; this changes every round.
    """
    parts = []

    # ── tone ──
    parts.append(DEFAULT_TONE_PROMPT)

    # ── reward milestone ──
    if reward_message:
        parts.append(f"REWARD MILESTONE: {reward_message}")

    # ── game type + difficulty ──
    if is_first_round:
        if user_game_choice:
            parts.append(f"The user chose to play: {user_game_choice}.")
        parts.append(
            f"Generate {GAME_DESCRIPTIONS[decision.game_type]} at "
            f"{DIFFICULTY_DESCRIPTIONS[decision.difficulty]} difficulty."
        )
        parts.append(
            "This is the first question. Give a brief, warm introduction to the game "
            "before asking the question (1-2 sentences max)."
        )
    else:
        # ── live metrics block ──
        correctness       = engine.rolling_correctness()
        avg_time          = engine.avg_response_time()
        recent_expressions = [r.facial_expression for r in engine.history[-3:]]
        recent_vocal       = [r.vocal_emotion for r in engine.history[-3:]]

        parts.append(
            f"--- LIVE METRICS ---\n"
            f"Round: {engine.round_number}\n"
            f"Rolling correctness (last {CORRECTNESS_WINDOW}): {correctness:.0%}\n"
            f"Avg response time: {avg_time:.1f}s\n"
            f"Recent facial expressions: {', '.join(recent_expressions) if recent_expressions else 'N/A'}\n"
            f"Recent vocal emotions: {', '.join(recent_vocal) if recent_vocal else 'N/A'}\n"
            f"Inferred state: {decision.inferred_state.value}\n"
            f"Difficulty: {decision.difficulty.name}"
        )

        if user_answer:
            parts.append(f'The user\'s last answer was: "{user_answer}"')

        # ── adaptive instructions ──
        if decision.switch_game:
            parts.append(
                f"The user seems {decision.inferred_state.value}. Switch to "
                f"{GAME_DESCRIPTIONS[decision.game_type]}. Transition smoothly — "
                "acknowledge the change naturally (e.g. 'Let's try something different!')."
            )

        if decision.give_hint: # if decided to give a hint append hint instruction to prompt
            parts.append(
                "The user is struggling. Include a subtle hint or make the question "
                "more approachable."
            )

        if decision.give_encouragement:
            if decision.inferred_state == InferredState.THRIVING:
                parts.append(
                    "The user is on a streak!!! Acknowledge it enthusiastically. "
                    "Be genuinely impressed."
                )
            elif decision.inferred_state in (InferredState.STRUGGLING,
                                             InferredState.FRUSTRATED):
                parts.append(
                    "Encourage the user warmly. Normalise difficulty. "
                    "Do NOT be condescending — be genuinely supportive."
                )
            elif decision.inferred_state == InferredState.DISENGAGED:
                parts.append(
                    "The user seems disengaged. Re-energise — try humour, "
                    "an interesting fact, or a more engaging question format."
                )

        parts.append(f"Tone: {TONE_INSTRUCTIONS.get(decision.tone, TONE_INSTRUCTIONS['neutral'])}")

        parts.append(
            f"Generate {GAME_DESCRIPTIONS[decision.game_type]} at "
            f"{DIFFICULTY_DESCRIPTIONS[decision.difficulty]} difficulty."
        )

    if adaptation_eval:
        parts.append(f"--- ADAPTATION FEEDBACK ---\n{adaptation_eval}")

    # ── response format ──
    parts.append(
        "\n--- RESPONSE FORMAT ---\n"
        "Respond with a JSON object (no markdown, no code fences) with exactly these fields:\n"
        '  "dialogue": string — what the robot says aloud (reaction to the previous answer + the new question)\n'
        '  "answer": string — the correct answer to the NEW question you just asked\n'
        '  "category": string — specific topic/category of the question\n'
        '  "gesture": string — one of: "celebrate", "encourage", "think", "wave", "calm", "energetic", "neutral"'
    )

    return "\n\n".join(parts)


# --------------------------------------
#  SSH AND PEPPER ROBOT HELPERS
#  (adapted from lab-robot-code-fin.py)
# --------------------------------------

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
        print(f"  [SSH fallback] exec_command failed: {e}")
        return ""


def nao_calibrate_ambient(ssh) -> int:
    """
    Calibrate microphone energy threshold to the current room environment.

    Silently listens for CALIBRATION_SECS seconds via ALAudioDevice,
    samples the front microphone energy at regular intervals, and returns
    the ambient baseline + ENERGY_BUFFER as the speech detection threshold.

    This prevents false positives in noisy labs wherein ambient noise
    exceeds the hardcoded default, and false negatives in quiet rooms
    wherein the threshold is unnecessarily high.
    """
    try:
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


def nao_record(ssh, energy_threshold: int = DEFAULT_ENERGY_THRESHOLD):
    """
    Record audio on Pepper with dynamic silence detection.

    Instead of a fixed sleep, the robot polls its own microphone energy
    via ALAudioDevice. Recording stops when:
      1- speech is detected (energy above threshold), THEN
      2- silence persists for SILENCE_DURATION seconds after speech ends, OR
      3- the hard ceiling RECORD_MAX_SECS is reached.

    The energy_threshold is calibrated at startup via nao_calibrate_ambient()
    so the system adapts to the ambient noise level of the room, thereby
    preventing false positives in noisy labs and false negatives in quiet ones.

    If ALAudioDevice.getFrontMicEnergy() is unsupported on the robot's firmware,
    the inner loop falls back to a safe fixed-duration recording so the demo
    never breaks.
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

        # hard ceiling — never exceed max duration
        if elapsed >= {RECORD_MAX_SECS}:
            break

        # poll front microphone energy level
        energy = audio.getFrontMicEnergy()

        if elapsed < {RECORD_MIN_SECS}:
            # minimum recording period — always wait this long
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
                if (time.time() - silence_start) >= {SILENCE_DURATION}:
                    break

        time.sleep({SILENCE_POLL_SECS})

except Exception as e:
    # firmware fallback — getFrontMicEnergy() unsupported on this Pepper
    # fall back to a safe fixed-duration recording so the demo never breaks
    print("  [Silence detection failed: " + str(e) + "] Falling back to fixed-duration recording")
    time.sleep({RECORD_MAX_SECS})

rec.stopMicrophonesRecording()
""")
    sftp = ssh.open_sftp()
    sftp.get(REMOTE_WAV, LOCAL_WAV)
    sftp.close()


def _split_into_sentences(text: str) -> list[str]:
    """
    Split dialogue into natural sentence-level segments for speech delivery.

    OpenAI frequently returns dialogue as a single unbroken block. Without
    splitting, Pepper rattles off the entire paragraph without breathing,
    thereby ruining the illusion of a conversational companion. This function
    splits at sentence terminators (. ? !) whilst preserving abbreviations
    and decimal numbers.
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
    Speak text on Pepper with natural sentence-level pausing.

    Packs all sentences into a single SSH payload so Pepper handles the
    loop and pauses internally. This eliminates the 1-2 second SSH
    round-trip overhead per sentence that would otherwise ruin the
    carefully designed 0.4s inter-sentence cadence.
    """
    sentences = _split_into_sentences(text)
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
        print(f"  [Animated speech failed] {e}")
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
        print(f"  [Face tracking failed] {e}")


def nao_set_leds(ssh, group, colour, duration=1.0):
    """Fade an LED group to a colour."""
    try:
        nao_run(ssh, f"""
from naoqi import ALProxy
ALProxy("ALLeds","127.0.0.1",9559).fadeRGB("{group}", {colour}, {duration})
""")
    except Exception as e:
        print(f"  [LED failed] {e}")


# ══════════════════════════════════════════════════════════════════════════════
#  LOCAL MODE HELPERS (Mac — no Pepper required)
# ══════════════════════════════════════════════════════════════════════════════

LOCAL_SAMPLE_RATE = 16000   # Whisper expects 16 kHz; we resample from native rate


LOCAL_SILENCE_RMS   = 40      # RMS below this = silence on Mac mic
LOCAL_SILENCE_SECS  = 1.5    # seconds of post-speech silence to stop recording
LOCAL_MIN_SECS      = 1.0    # minimum recording before silence detection kicks in
LOCAL_NO_SPEECH_MAX = 5.0    # stop if no speech detected at all after this many seconds


def local_record(max_secs: float = RECORD_MAX_SECS):
    """
    Record audio from the Mac's built-in microphone to LOCAL_WAV with
    silence detection mirroring Pepper's dynamic recording behaviour.

    Records at the device's native sample rate then resamples to 16 kHz
    for Whisper compatibility via librosa.
    """
    # use the mic's native rate to avoid unsupported-rate hangs
    dev_info    = sd.query_devices(kind="input")
    native_rate = int(dev_info["default_samplerate"])
    chunk_size  = int(native_rate * SILENCE_POLL_SECS)

    buffer = []
    speech_detected = False
    silence_start = None
    elapsed = 0.0

    print(f"  Recording from Mac mic (up to {max_secs}s, stops after silence)...")

    def _callback(indata, frames, time_info, status):
        buffer.append(indata.copy())

    with sd.InputStream(samplerate=native_rate, channels=1, dtype="int16",
                        blocksize=chunk_size, callback=_callback):
        while elapsed < max_secs:
            time.sleep(SILENCE_POLL_SECS)
            elapsed += SILENCE_POLL_SECS

            if not buffer:
                continue
            data = buffer[-1]

            rms = (np.mean(data.astype(np.float64) ** 2)) ** 0.5
            print(f"\r    [{elapsed:.1f}s] RMS: {rms:.0f} {'▓' if rms > LOCAL_SILENCE_RMS else '░'}", end="", flush=True)

            if elapsed < LOCAL_MIN_SECS:
                if rms > LOCAL_SILENCE_RMS:
                    speech_detected = True
                continue

            if not speech_detected and elapsed >= LOCAL_NO_SPEECH_MAX:
                break

            if rms > LOCAL_SILENCE_RMS:
                speech_detected = True
                silence_start = None
            else:
                if speech_detected and silence_start is None:
                    silence_start = elapsed
                if speech_detected and silence_start is not None:
                    if (elapsed - silence_start) >= LOCAL_SILENCE_SECS:
                        break

    print()

    # concatenate all buffered audio at native rate
    if buffer:
        audio_native = np.concatenate(buffer).flatten().astype(np.float32) / 32768.0
        # resample to 16 kHz for Whisper
        audio_16k = librosa.resample(audio_native, orig_sr=native_rate, target_sr=LOCAL_SAMPLE_RATE)
        audio_int16 = (audio_16k * 32768.0).astype(np.int16)
    else:
        audio_int16 = np.zeros((0,), dtype=np.int16)

    with wave.open(LOCAL_WAV, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(LOCAL_SAMPLE_RATE)
        wf.writeframes(audio_int16.tobytes())
    print(f"  Recording saved ({elapsed:.1f}s).")


def local_say(text: str):
    """Speak text using macOS built-in TTS (the 'say' command)."""
    try:
        subprocess.run(["say", text], check=True, timeout=30)
    except Exception as e:
        print(f"  [Local TTS failed] {e}")


def say(ssh_tts, text):
    """Dispatch TTS to local or Pepper depending on mode."""
    if LOCAL_MODE:
        local_say(text)
    else:
        nao_say(ssh_tts, text)


def record(ssh, energy_threshold):
    """Dispatch audio recording to local or Pepper depending on mode."""
    if LOCAL_MODE:
        local_record()
    else:
        nao_record(ssh, energy_threshold)


# ══════════════════════════════════════════════════════════════════════════════
#  GESTURE MAPPING
#  Each gesture is a motion sequence aligned to the game/emotional context.
# ══════════════════════════════════════════════════════════════════════════════

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
        print(f"  [Gesture failed: {gesture_type}] {e}")


# ══════════════════════════════════════════════════════════════════════════════
#  AUDIO ANALYSIS + TRANSCRIPTION
# ══════════════════════════════════════════════════════════════════════════════

def check_audio_volume() -> bool:
    """Return True when the recorded WAV is loud enough to process."""
    try:
        with wave.open(LOCAL_WAV, "rb") as wf:
            raw = wf.readframes(wf.getnframes())
            if len(raw) < 2:
                return False
            samples = struct.unpack(f"<{len(raw) // 2}h", raw)
            rms = (sum(s * s for s in samples) / len(samples)) ** 0.5
            return rms > VOLUME_THRESHOLD
    except Exception as e:
        print(f"  [Volume check failed] {e}")
        return True


def transcribe() -> str:
    """
    Transcribe the local WAV with Whisper, gracefully handling API drops.

    Returns an empty string on failure, which the adaptive engine seamlessly
    interprets as a silent/missed answer via the existing disengagement logic
    — therefore no additional error handling is needed upstream.
    """
    try:
        with open(LOCAL_WAV, "rb") as fh:
            return client.audio.transcriptions.create(
                model="whisper-1", file=fh, timeout=API_TIMEOUT
            ).text.strip()
    except Exception as e:
        print(f"  [Whisper fallback] Transcription failed: {e}")
        return ""


# ══════════════════════════════════════════════════════════════════════════════
#  FACIAL EXPRESSION PIPELINE
# ══════════════════════════════════════════════════════════════════════════════

def capture_and_classify(ssh, face_model, face_cascade,
                         local_camera=None) -> tuple[str, float]:
    """
    Capture a face image and classify the expression.
    Uses Pepper's camera by default; local webcam if GAZE_LOCAL_CAMERA=true.
    Returns (emotion_label, confidence).
    """
    if local_camera is not None:
        ret, frame = local_camera.read()
        if not ret:
            print("  [Local camera failed] cv2.VideoCapture.read() returned False")
            return "Neutral", 0.0
    else:
        try:
            nao_capture_image(ssh)
            frame = cv2.imread(LOCAL_IMG)
            if frame is None:
                print(f"  [Image read failed] cv2.imread returned None for {LOCAL_IMG}")
                return "Neutral", 0.0
        except Exception as e:
            print(f"  [Camera capture failed] {e}")
            return "Neutral", 0.0

    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return "Neutral", 0.0      # no face → default

    # largest detected face
    x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
    roi     = gray[y:y+h, x:x+w]
    resized = cv2.resize(roi, (48, 48))
    inp     = resized[np.newaxis, :, :, np.newaxis]     # (1, 48, 48, 1)

    return face_model.predict(inp)


# ══════════════════════════════════════════════════════════════════════════════
#  OPENAI GAME GENERATION + ANSWER CHECKING
# ══════════════════════════════════════════════════════════════════════════════

API_TIMEOUT = 10  # seconds — prevents Pepper freezing if OpenAI/network stalls


def generate_game_response(prompt: str, conversation: list) -> dict:
    """
    Send the dynamically constructed prompt to OpenAI.
    Returns parsed JSON: {dialogue, answer, category, gesture}.

    Wrapped in a strict timeout with a graceful fallback so the robot
    remains 'alive' and the interaction loop keeps moving even if the
    API call fails or the university network drops mid-request.
    """
    messages = conversation + [{"role": "user", "content": prompt}]

    try:
        resp = client.chat.completions.create(
            model="gpt-4.1",
            messages=messages,
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

    except json.JSONDecodeError as e:
        # API responded but returned malformed JSON — use raw text as dialogue
        print(f"  [OpenAI returned malformed JSON] {e}")
        return {
            "dialogue": content,
            "answer":   "",
            "category": "general",
            "gesture":  "neutral",
        }
    except Exception as e:
        # network timeout, API outage, or any other failure
        print(f"  [API fallback] OpenAI call failed: {e}")
        return {
            "dialogue": f"The OpenAI API call failed: {e}. Let me try again next round!",
            "answer":   "",
            "category": "fallback",
            "gesture":  "think",
        }


def check_answer(user_answer: str, correct_answer: str,
                 question_context: str) -> bool:
    """
    Falls back to a simple string-containment check if the API call fails,
    thereby ensuring the game loop never stalls on answer verification.
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
        print(f"  [API fallback] Answer check failed: {e}")
        return correct_answer.lower().strip() in user_answer.lower().strip()


# ══════════════════════════════════════════════════════════════════════════════
#  GAME CATEGORY SELECTION
# ══════════════════════════════════════════════════════════════════════════════

def parse_game_choice(text: str) -> Optional[GameType]:
    """Parse the user's verbal game choice into a GameType."""
    lower = text.lower()
    mappings = {
        GameType.NUMBERS: ["number", "numbers", "maths", "math", "arithmetic",
                           "calculation", "countdown numbers"],
        GameType.LETTERS: ["letter", "letters", "word", "words", "spelling",
                           "countdown letters", "vocabulary"],
    }
    for game_type, keywords in mappings.items():
        if any(kw in lower for kw in keywords):
            return game_type
    return None


# ══════════════════════════════════════════════════════════════════════════════
#  SAVE / LOAD SESSION
# ══════════════════════════════════════════════════════════════════════════════

def save_session(engine: AdaptiveEngine, preferred_game: Optional[GameType] = None):
    """Save session progress to disk so the user can continue later."""
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
        print(f"  [Save file corrupt] {e}")
        return None


def restore_engine(save_data: dict) -> AdaptiveEngine:
    """Restore engine state from saved data."""
    engine = AdaptiveEngine()
    engine.total_correct    = save_data.get("total_correct", 0)
    engine.best_streak      = save_data.get("best_streak", 0)
    engine.game_switch_count = save_data.get("game_switches", 0)
    engine.current_difficulty = Difficulty(save_data.get("last_difficulty", 2))
    engine.current_game     = GameType(save_data.get("last_game", "numbers"))
    engine.rewards_given    = set(save_data.get("rewards_given", []))
    for g_val, count in save_data.get("games_played", {}).items():
        try:
            engine.games_played[GameType(g_val)] = count
        except ValueError as e:
            print(f"  [Restore skipped invalid game type: {g_val}] {e}")
    return engine


def delete_save():
    """Remove the save file after a completed session or on user request."""
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)


# ══════════════════════════════════════════════════════════════════════════════
#  LED COLOUR MAP
# ══════════════════════════════════════════════════════════════════════════════

LED_COLOURS = {
    InferredState.THRIVING:    0x0000FF00,   # green
    InferredState.COMFORTABLE: 0x00FFFFFF,   # white
    InferredState.STRUGGLING:  0x00FFFF00,   # yellow
    InferredState.FRUSTRATED:  0x00FF8000,   # orange
    InferredState.DISENGAGED:  0x000080FF,   # light blue
}


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN GAME LOOP
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  GAZE — Game-Adaptive Zone of Engagement")
    print("  Adaptive Game System for Pepper Robot")
    print("=" * 60)

    # ── load facial expression model (WS-10) ──
    print("\nLoading facial expression model...")
    face_model   = FacialExpressionModel(MODEL_JSON, MODEL_WEIGHTS)
    face_cascade = cv2.CascadeClassifier(HAAR_CASCADE)
    print("  Facial model loaded.")

    # ── load speech emotion model (WS-08) ──
    speech_model = None
    if os.path.exists(SPEECH_MODEL):
        print("Loading speech emotion model...")
        speech_model = SpeechEmotionModel(SPEECH_MODEL)
        print("  Speech model loaded.")
    else:
        print(f"  Speech emotion model not found at {SPEECH_MODEL} — vocal signal disabled.")
        print("  Run train_speech_model.py to generate it.")

    # ── local camera (dev/testing) ──
    local_camera = None
    if USE_LOCAL_CAMERA:
        local_camera = cv2.VideoCapture(0)
        print("  Using local webcam for expression detection.")
    else:
        print("  Using Pepper's camera for expression detection.")

    # ── connect to Pepper (skipped in local mode) ──
    ssh     = None
    ssh_tts = None
    energy_threshold = DEFAULT_ENERGY_THRESHOLD

    if LOCAL_MODE:
        print("\n  LOCAL MODE — skipping Pepper connection.")
    else:
        print(f"\nConnecting to Pepper at {NAO_IP}...")
        ssh     = ssh_connect()
        ssh_tts = ssh_connect()         # dedicated TTS connection
        print("  Connected.")

        # ── calibrate ambient noise level ──
        print("\nCalibrating ambient noise level (stay quiet for 3 seconds)...")
        energy_threshold = nao_calibrate_ambient(ssh)

    # ── check for saved session ──
    preferred_game = None
    engine         = AdaptiveEngine()
    resumed        = False

    save_data = load_session()
    if save_data:
        prev_rounds = save_data.get("rounds_played", 0)
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

        print("\nListening for continue/fresh...")
        if not LOCAL_MODE:
            nao_set_leds(ssh, "EarLeds", 0x0000FF00, 0.3)
        record(ssh, energy_threshold)

        resume_text = ""
        if check_audio_volume():
            resume_text = transcribe()
            print(f"Heard: {resume_text}")

        lower_resume = resume_text.lower()
        if any(w in lower_resume for w in ["continue", "resume", "yes", "carry on",
                                            "keep going", "where I left", "left off"]):
            engine = restore_engine(save_data)
            resumed = True
            restore_msg = f"Restoring your previous session — {save_data.get('rounds_played', 0)} rounds on record."
            say(ssh_tts, restore_msg)
            print(f"\nRobot: {restore_msg}")
        else:
            delete_save()
            fresh_msg = "No worries, starting fresh! Your previous save has been cleared."
            say(ssh_tts, fresh_msg)
            print(f"\nRobot: {fresh_msg}")

    # ── OpenAI conversation history (game context continuity) ──
    conversation = [{"role": "system", "content": (
        "You are a Pepper robot game host called GAZE. You play interactive "
        "countdown-style games with users and adapt based on their emotional state "
        "and performance. Always respond in the exact JSON format requested. "
        "Keep dialogue concise and natural — 2-3 sentences max. "
        + DEFAULT_TONE_PROMPT
    )}]

    if not resumed:
        # ── startup sequence ──
        if not LOCAL_MODE:
            nao_track_face(ssh, enable=True)
            nao_set_leds(ssh, "FaceLeds", 0x0000FF00, 1.0)
            nao_gesture(ssh, "wave")

        # ── ask game preference ──
        game_prompt = (
            "Hello! I'm GAZE, your game host. "
            "What would you like to play? "
            "I've got a numbers round or a letters round, like Countdown!"
        )
        say(ssh_tts, game_prompt)
        print(f"\nRobot: {game_prompt}")

        print("\nListening for game choice...")
        if not LOCAL_MODE:
            nao_set_leds(ssh, "EarLeds", 0x0000FF00, 0.3)
        record(ssh, energy_threshold)

        game_choice_text = ""
        chosen_game      = None

        if check_audio_volume():
            game_choice_text = transcribe()
            print(f"Heard: {game_choice_text}")
            chosen_game = parse_game_choice(game_choice_text)

        if chosen_game is None:
            chosen_game = GameType.NUMBERS
            default_msg = "I didn't catch a game choice, so I'll start with numbers!"
            say(ssh_tts, default_msg)
            print(f"\nRobot: {default_msg}")
        else:
            print(f"  Selected: {chosen_game.value}")

        engine.current_game = chosen_game
        preferred_game      = chosen_game
    else:
        # resumed session — use saved preferences
        game_choice_text = engine.current_game.value
        preferred_game   = engine.current_game

        resume_msg = (
            f"Alright, picking up where we left off! "
            f"We're playing {engine.current_game.value} at "
            f"{engine.current_difficulty.name.lower()} difficulty."
        )
        say(ssh_tts, resume_msg)
        print(f"\nRobot: {resume_msg}")

    # ── first round ──
    first_decision = AdaptiveDecision(
        difficulty=engine.current_difficulty,
        game_type=engine.current_game,
        inferred_state=InferredState.COMFORTABLE, switch_game=False,
        give_hint=False, give_encouragement=False, tone="neutral",
    )

    prompt    = build_game_prompt(engine, first_decision,
                                  is_first_round=True,
                                  user_game_choice=game_choice_text)
    game_data = generate_game_response(prompt, conversation)
    conversation.append({"role": "assistant", "content": json.dumps(game_data)})

    current_answer   = game_data.get("answer", "")
    current_question = game_data.get("dialogue", "")
    if not current_question.strip():
        current_question = "OpenAI returned empty dialogue. Let me try again next round!"

    # deliver first question with gesture
    if not LOCAL_MODE:
        gesture_thread = threading.Thread(
            target=nao_gesture,
            args=(ssh, game_data.get("gesture", "neutral")),
            daemon=True,
        )
        gesture_thread.start()
    say(ssh_tts, current_question)
    print(f"\nRobot: {current_question}")
    print(f"(Answer: {current_answer})")

    # ══════════════════════════════════════════════════════════════════════
    #  CORE GAME LOOP — INPUT → PROCESS → GENERATE → OUTPUT
    # ══════════════════════════════════════════════════════════════════════

    try:
        while engine.round_number <= MAX_ROUNDS:
            round_num = engine.round_number
            print(f"\n{'─' * 40} Round {round_num} {'─' * 40}")

            # ── INPUT LAYER ──────────────────────────────────────────────
            # all four signals captured: face, voice, time, correctness

            # 1. start timer
            question_start = time.time()

            # 2. facial expression (captured while user thinks)
            print("Capturing expression...")
            expression, expr_conf = capture_and_classify(
                ssh, face_model, face_cascade, local_camera
            )
            print(f"  Expression: {expression} ({expr_conf:.2f})")

            # 3. listen for verbal answer
            print("Listening...")
            if not LOCAL_MODE:
                nao_set_leds(ssh, "EarLeds", 0x0000FF00, 0.3)
            record(ssh, energy_threshold)

            response_time = time.time() - question_start

            # 4. vocal emotion (extracted from the same audio before transcription)
            vocal_emo, vocal_conf = classify_speech_emotion(speech_model, LOCAL_WAV)
            print(f"  Vocal emotion: {vocal_emo} ({vocal_conf:.2f})")

            user_answer = ""
            if check_audio_volume():
                user_answer = transcribe()
                if user_answer:
                    print(f"Heard: {user_answer}")
                else:
                    print("  [Whisper returned empty transcription]")
                    say(ssh_tts, "Sorry, I couldn't make out what you said. I'll treat that as a pass.")
            else:
                print("(No response detected)")
                say(ssh_tts, "I didn't hear a response, so I'll move on.")

            # exit keywords
            if user_answer.lower().strip() in [
                "stop", "quit", "exit", "goodbye", "bye", "end",
                "i want to stop", "let's stop", "no more",
            ]:
                print("User wants to stop.")
                break

            # ── PROCESS LAYER ────────────────────────────────────────────
            # check answer + adaptive engine infers state + decides

            if not LOCAL_MODE:
                nao_set_leds(ssh, "EarLeds", 0x000000FF, 0.3)  # blue = thinking

            correct = (check_answer(user_answer, current_answer, current_question)
                       if user_answer else False)
            print(f"  Correct: {correct}")

            decision = engine.decide(
                expression, expr_conf, response_time, correct, user_answer,
                vocal_emotion=vocal_emo
            )
            print(f"  Inferred state: {decision.inferred_state.value}")
            print(f"  Difficulty: {decision.difficulty.name}")
            if decision.switch_game:
                print(f"  Switching to: {decision.game_type.value}")

            # record round (semantic memory)
            engine.record_round(RoundResult(
                round_number=round_num,
                game_type=engine.current_game,
                difficulty=engine.current_difficulty,
                question=current_question,
                user_answer=user_answer,
                correct=correct,
                response_time=response_time,
                facial_expression=expression,
                expression_confidence=expr_conf,
                vocal_emotion=vocal_emo,
                vocal_emotion_confidence=vocal_conf,
                inferred_state=decision.inferred_state,
            ))

            # ── REWARD CHECK ─────────────────────────────────────────────
            reward_msg = engine.check_reward()
            if reward_msg:
                print(f"  REWARD: {reward_msg}")

            # ── ADAPTATION SELF-EVALUATION ──────────────────────────────
            # evaluate whether the previous round's adaptation worked
            adaptation_eval = engine.evaluate_adaptation()
            if adaptation_eval:
                print(f"  {adaptation_eval}")

            # ── GENERATE LAYER ───────────────────────────────────────────
            # construct dynamic prompt from live metrics → OpenAI

            prompt    = build_game_prompt(engine, decision,
                                          user_answer=user_answer,
                                          reward_message=reward_msg,
                                          adaptation_eval=adaptation_eval)
            game_data = generate_game_response(prompt, conversation)
            conversation.append({"role": "user",      "content": f"User answered: {user_answer}"})
            conversation.append({"role": "assistant",  "content": json.dumps(game_data)})

            current_answer   = game_data.get("answer", "")
            current_question = game_data.get("dialogue", "")
            if not current_question.strip():
                current_question = "OpenAI returned empty dialogue. Let me try again next round!"

            # ── OUTPUT LAYER ─────────────────────────────────────────────
            # robot speaks + gestures + LEDs — all aligned to inferred state

            gesture_type = game_data.get("gesture", "neutral")

            if not LOCAL_MODE:
                # LED colour reflects inferred state
                nao_set_leds(
                    ssh, "FaceLeds",
                    LED_COLOURS.get(decision.inferred_state, 0x00FFFFFF), 0.5
                )

                # gesture and speech run in parallel
                gesture_thread = threading.Thread(
                    target=nao_gesture,
                    args=(ssh, gesture_type), daemon=True
                )
                gesture_thread.start()
            # animated speech for positive states; plain TTS otherwise
            if not LOCAL_MODE and gesture_type in ("celebrate", "encourage"):
                nao_say_animated(ssh_tts, current_question)
            else:
                say(ssh_tts, current_question)

            print(f"\nRobot: {current_question}")
            print(f"(Answer: {current_answer})")

            # ── PROGRESSIVE SAVE ──────────────────────────────────────────
            # auto-save after every round so data survives unexpected crashes
            # (laptop dies, SSH timeout, etc.) — protects report data
            save_session(engine, preferred_game)

    except KeyboardInterrupt:
        print("\n\nInterrupted.")

    # ══════════════════════════════════════════════════════════════════════
    #  SESSION END — save progress + summary
    # ══════════════════════════════════════════════════════════════════════

    # save session so user can continue later
    save_session(engine, preferred_game)

    summary = engine.get_session_summary()
    print(f"\n{'=' * 60}")
    print("  SESSION SUMMARY")
    print(f"{'=' * 60}")
    for k, v in summary.items():
        print(f"  {k}: {v}")

    # farewell — adaptive to performance
    if summary.get("rounds", 0) > 0: # if at least one round was played proceed with feedback otherwise farewell
        acc = summary["accuracy"]
        streak_note = (f" Your best streak was {summary['best_streak']} in a row!"
                       if summary["best_streak"] >= 3 else "")
        if acc >= 0.8:
            farewell = (
                f"Amazing session! You got {summary['correct']} out of "
                f"{summary['rounds']} right.{streak_note} "
                "Brilliant work! Your progress is saved — see you next time!"
            )
        elif acc >= 0.5:
            farewell = (
                f"Great effort! You scored {summary['correct']} out of "
                f"{summary['rounds']}.{streak_note} "
                "Well played! Your progress is saved — see you next time!"
            )
        else:
            farewell = (
                f"Thanks for playing! You got {summary['correct']} out of "
                f"{summary['rounds']}.{streak_note} "
                "Every round is a learning opportunity. "
                "Your progress is saved — see you next time!"
            )
    else:
        farewell = "Thanks for stopping by! See you next time!"

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
    print("\nGAZE disconnected.")


if __name__ == "__main__":
    main()
