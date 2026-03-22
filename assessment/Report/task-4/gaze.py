"""
GAZE: Game-Adaptive Zone of Engagement

- [X] ideas in proposal google doc
- [X] intergrate ws-10 for facial recognition and emotion detection
- [X] Generates games with openai on the fly
- [X] Facial recognition (Happy? frustrated?) if frustrated give hints if happy celebrate via /ws-10
- [X] If bored speeds it up
- [X] If angry - no worries lets try another game ( easier)
- [X] If answers are correct, it gives harder puzzles.
- [X] Make easier if too hard
- [X] If sad games to cheer him up
- [X] Camera - detects face ( emotions) - game logic - open ai generates response - robot speaks and reacts.
- [X] Robot personality - funny , sarcastic , serious.
- [X] Games - puzzles, riddles, trivia, memory games, word games, math games, etc.
- [X] Use openai to generate games and responses based on the user's emotions and performance.
- [X] timer to track how long the user has been playing and adjust the game difficulty accordingly.
- [X] scoring system to track the user's progress and provide feedback on their performance.
- [X] reward system to encourage the user to keep playing and improving their skills.
- [X] feedback system to allow the user to provide feedback on the games to change robot's considerations and personality.
- [X] feature to allow the user to customise the robot's personality and game preferences.
- [X] feature to allow the user to save their progress and continue playing later.
"""

import os
import re
import json
import time
import wave
import struct
import tempfile
import threading
import numpy as np
import cv2
import paramiko
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI
import tensorflow as tf
from tensorflow.keras.models import model_from_json

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
VOLUME_THRESHOLD = 500
SSH_TIMEOUT  = 10
CMD_TIMEOUT  = 60

# false when connected ti pepper; true for testing when no Pepper's camera
USE_LOCAL_CAMERA = os.getenv("GAZE_LOCAL_CAMERA", "false").lower() == "true"

# paths to pre-trained facial expression model (WS-10)
SCRIPT_DIR    = os.path.dirname(os.path.abspath(__file__))
WORKSHOP_DIR  = os.path.join(SCRIPT_DIR, "..", "..", "learning", "workshops")
MODEL_JSON    = os.path.join(WORKSHOP_DIR, "[X]-facial-expression-detection", "model.json")
MODEL_WEIGHTS = os.path.join(WORKSHOP_DIR, "[X]-facial-expression-detection", "model_weights.weights.h5")
HAAR_CASCADE  = os.path.join(WORKSHOP_DIR, "[X]-ws-10", "haarcascade_frontalface_default.xml")

# adaptive engine thresholds
RESPONSE_TIME_BASELINE = 30.0   # seconds — beyond this, user is slow
CORRECTNESS_WINDOW     = 5      # rolling window size
CORRECTNESS_FLOOR      = 0.4    # below thus ease off
CORRECTNESS_CEILING    = 0.8    # above thus ramp up
SILENCE_THRESHOLD      = 2      # consecutive non-responses before intervention
MAX_ROUNDS             = 20     # natural session end

# persistent session save file
SAVE_FILE = os.path.join(SCRIPT_DIR, "gaze_save.json")

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
    TRIVIA     = "trivia"
    RIDDLES    = "riddles"
    WORD_GAMES = "word_games"
    SPELLING   = "spelling"
    MATHS      = "maths"

class Personality(Enum):
    ENCOURAGING = "encouraging"
    SARCASTIC   = "sarcastic"
    SERIOUS     = "serious"

PERSONALITY_PROMPTS = {
    Personality.ENCOURAGING: (
        "Your personality is warm, encouraging, and supportive. "
        "Celebrate every small win. Use phrases like 'You've got this!' and "
        "'Brilliant effort!' Genuinely cheer the user on."
    ),
    Personality.SARCASTIC: (
        "Your personality is playfully sarcastic and witty. "
        "Use dry humour and gentle teasing — never mean-spirited. "
        "Think friendly banter, not cruelty. If they get one wrong just take this piss kindly "
        "joke about it lightly. If they get one right, act surprised."
    ),
    Personality.SERIOUS: (
        "Your personality is calm, focused, and matter-of-fact. "
        "No jokes, no fluff. Deliver questions seriously and cleanly, acknowledge "
        "correct answers briefly, and move on efficiently. "
        "Think quiz show host, not children's entertainer."
    ),
}

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

    Cognitive mapping:
      Perceive   ---> raw signals arrive
      Attend     ---> focus on attentiveness, emotion, performance
      Anticipate ---> assess how user finds current difficulty
      Plan       ---> decide next action (difficulty, game switch, encouragement)
      Predict    ---> consider how chosen action will affect user
      Learn      ---> track what worked across rounds (episodic memory)
      Adapt      ---> refine decisions each subsequent round
    """

    def __init__(self):
        self.history: list[RoundResult]   = []
        self.current_difficulty            = Difficulty.MEDIUM
        self.current_game                  = GameType.TRIVIA
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
                    correct: bool, answer_text: str) -> InferredState:
        """
        Weigh ALL signals together to determine the user's actual state.
        The camera classifies the expression; this method assesses reality.
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

        # ── thriving: performing well regardless of resting face ──
        if (correctness >= CORRECTNESS_CEILING
                and response_time < RESPONSE_TIME_BASELINE * 0.5):
            return InferredState.THRIVING
        # camera says Angry but fast + correct → they're fine
        if expression == "Angry" and correct and response_time < RESPONSE_TIME_BASELINE * 0.6:
            return InferredState.COMFORTABLE

        # ── disengaged: multiple signals pointing to checked-out ──
        if self.consecutive_silences >= SILENCE_THRESHOLD:
            return InferredState.DISENGAGED
        if (expression == "Neutral"
                and response_time > RESPONSE_TIME_BASELINE
                and correctness < 0.5):
            return InferredState.DISENGAGED

        # ── frustrated: struggling + negative expression ──
        if expression in ("Angry", "Disgust") and correctness < CORRECTNESS_FLOOR:
            return InferredState.FRUSTRATED
        if self.consecutive_wrong >= 3 and expression in ("Angry", "Sad", "Fear"):
            return InferredState.FRUSTRATED

        # ── struggling: declining performance + negative signals ──
        if expression == "Sad" and response_time > RESPONSE_TIME_BASELINE * 0.7:
            return InferredState.STRUGGLING
        if correctness < CORRECTNESS_FLOOR:
            return InferredState.STRUGGLING
        if expression == "Fear" and not correct:
            return InferredState.STRUGGLING

        # ── default: comfortable ──
        return InferredState.COMFORTABLE

    # ── core decision function --

    def decide(self, expression: str, expression_conf: float,
               response_time: float, correct: bool,
               answer_text: str) -> AdaptiveDecision:
        """Return what to do next based on inferred state."""
        state       = self.infer_state(expression, response_time, correct, answer_text)
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
        """Pick a game type different from current, preferring least-played."""
        candidates = [g for g in GameType if g != self.current_game]
        candidates.sort(key=lambda g: self.games_played.get(g, 0))
        return candidates[0]

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


#  DYNAMIC PROMPT CONSTRUCTION
# ----------------------------

GAME_DESCRIPTIONS = {
    GameType.TRIVIA:     "a general-knowledge trivia question",
    GameType.RIDDLES:    "a lateral-thinking riddle",
    GameType.WORD_GAMES: "a word game (anagram, synonym/antonym, or definition challenge)",
    GameType.SPELLING:   ("a Countdown-style challenge: give the user a set of random letters "
                          "and ask them to form the longest word possible"),
    GameType.MATHS:      "a mental arithmetic or number-sequence puzzle",
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
                      personality: Personality = Personality.ENCOURAGING,
                      reward_message: Optional[str] = None) -> str:
    """
    Dynamically construct the OpenAI prompt from live metrics.
    This prompt is NEVER the same twice; this changes every round.
    """
    parts = []

    # ── personality ──
    parts.append(PERSONALITY_PROMPTS[personality])

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

        parts.append(
            f"--- LIVE METRICS ---\n"
            f"Round: {engine.round_number}\n"
            f"Rolling correctness (last {CORRECTNESS_WINDOW}): {correctness:.0%}\n"
            f"Avg response time: {avg_time:.1f}s\n"
            f"Recent expressions: {', '.join(recent_expressions) if recent_expressions else 'N/A'}\n"
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
    _, stdout, _ = ssh.exec_command(f"python -c '{escaped}'", timeout=CMD_TIMEOUT)
    return stdout.read().decode().strip()


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

except Exception:
    # firmware fallback — getFrontMicEnergy() unsupported on this Pepper
    # fall back to a safe fixed-duration recording so the demo never breaks
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
    thereby ruining the illusion of a cognitive companion. This function
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
except Exception:
    pass
""")


def nao_say_animated(ssh, text):
    """Try animated speech; fall back to plain TTS."""
    safe = json.dumps(text)
    try:
        nao_run(ssh, f"""
from naoqi import ALProxy
ALProxy("ALAnimatedSpeech","127.0.0.1",9559).say({safe})
""")
    except Exception:
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
except:
    pass
""")
    except Exception:
        pass


def nao_set_leds(ssh, group, colour, duration=1.0):
    """Fade an LED group to a colour."""
    try:
        nao_run(ssh, f"""
from naoqi import ALProxy
ALProxy("ALLeds","127.0.0.1",9559).fadeRGB("{group}", {colour}, {duration})
""")
    except Exception:
        pass


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


def nao_gesture(ssh, gesture_type: str,
                personality: Personality = Personality.ENCOURAGING):
    """
    Execute a gesture on Pepper aligned to the game context AND personality.
    Serious personality  → slower, calmer motions (duration x1.8).
    Sarcastic personality → sharper, snappier motions (duration x0.7).
    Encouraging personality → default timing (unchanged).

    This prevents cognitive dissonance wherein a 'Serious' robot executes
    a highly animated celebration, or an 'Encouraging' robot moves stiffly.
    """
    code = GESTURE_CODE.get(gesture_type, GESTURE_CODE["neutral"])

    # dynamically scale motion durations to match personality
    if personality == Personality.SERIOUS:
        # slower, more restrained movements — calm and deliberate
        code = code.replace("[1.0]", "[1.8]")
        code = code.replace("[0.3]", "[0.55]")
        code = code.replace("[0.5]", "[0.9]")
        code = code.replace("[1.2]", "[2.0]")
        code = code.replace("[1.5]", "[2.5]")
    elif personality == Personality.SARCASTIC:
        # sharper, quicker movements — snappy and theatrical
        code = code.replace("[1.0]", "[0.7]")
        code = code.replace("[0.3]", "[0.2]")
        code = code.replace("[0.5]", "[0.35]")
        code = code.replace("[1.2]", "[0.85]")
        code = code.replace("[1.5]", "[1.05]")
    # encouraging = default timing, no modification needed

    try:
        nao_run(ssh, code)
    except Exception:
        pass


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
    except Exception:
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
            return "Neutral", 0.0
    else:
        try:
            nao_capture_image(ssh)
            frame = cv2.imread(LOCAL_IMG)
            if frame is None:
                return "Neutral", 0.0
        except Exception:
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

    except json.JSONDecodeError:
        # API responded but returned malformed JSON — use raw text as dialogue
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
            "dialogue": "Hmm, let me think about that one. Let's try another!",
            "answer":   "",
            "category": "fallback",
            "gesture":  "think",
        }


def check_answer(user_answer: str, correct_answer: str,
                 question_context: str) -> bool:
    """
    Use OpenAI to judge correctness — handles paraphrasing, partial answers,
    and pronunciation quirks from speech-to-text.

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
        GameType.TRIVIA:     ["trivia", "quiz", "general knowledge", "questions"],
        GameType.RIDDLES:    ["riddle", "riddles", "brain teaser", "lateral"],
        GameType.WORD_GAMES: ["word", "anagram", "synonym", "definition", "vocabulary"],
        GameType.SPELLING:   ["spelling", "countdown", "letters", "letter"],
        GameType.MATHS:      ["math", "maths", "number", "arithmetic", "calculation"],
    }
    for game_type, keywords in mappings.items():
        if any(kw in lower for kw in keywords):
            return game_type
    return None


# ══════════════════════════════════════════════════════════════════════════════
#  PERSONALITY PARSING + FEEDBACK
# ══════════════════════════════════════════════════════════════════════════════

def parse_personality_choice(text: str) -> Optional[Personality]:
    """Parse user's verbal personality preference."""
    lower = text.lower()
    mappings = {
        Personality.ENCOURAGING: ["encouraging", "nice", "friendly", "kind", "supportive", "warm"],
        Personality.SARCASTIC:   ["sarcastic", "funny", "witty", "cheeky", "humour", "humor"],
        Personality.SERIOUS:     ["serious", "focused", "professional", "no nonsense", "straight"],
    }
    for personality, keywords in mappings.items():
        if any(kw in lower for kw in keywords):
            return personality
    return None


def parse_feedback(text: str) -> dict:
    """
    Parse mid-game feedback from the user's speech.
    Detects personality change requests and game preference changes.
    Returns dict with any detected feedback.
    """
    lower = text.lower()
    feedback = {}

    # personality change requests
    personality_triggers = {
        Personality.SARCASTIC:   ["be funnier", "be sarcastic", "more funny", "more sarcastic",
                                  "be witty", "be cheeky", "make it funny"],
        Personality.ENCOURAGING: ["be nicer", "be encouraging", "be kind", "be supportive",
                                  "be warmer", "more encouraging", "be friendly"],
        Personality.SERIOUS:     ["be serious", "be professional", "stop joking",
                                  "no more jokes", "be focused", "more serious"],
    }
    for personality, triggers in personality_triggers.items():
        if any(t in lower for t in triggers):
            feedback["personality"] = personality
            break

    # game change requests
    game_triggers = {
        GameType.TRIVIA:     ["switch to trivia", "play trivia", "do trivia", "trivia please"],
        GameType.RIDDLES:    ["switch to riddles", "play riddles", "do riddles", "riddle please"],
        GameType.WORD_GAMES: ["switch to word", "play word", "do word game", "word game please"],
        GameType.SPELLING:   ["switch to spelling", "play spelling", "do countdown", "spelling please"],
        GameType.MATHS:      ["switch to maths", "play maths", "do maths", "math please",
                              "switch to math", "play math"],
    }
    for game_type, triggers in game_triggers.items():
        if any(t in lower for t in triggers):
            feedback["game"] = game_type
            break

    return feedback


# ══════════════════════════════════════════════════════════════════════════════
#  SAVE / LOAD SESSION
# ══════════════════════════════════════════════════════════════════════════════

def save_session(engine: AdaptiveEngine, personality: Personality,
                 preferred_game: Optional[GameType] = None):
    """Save session progress to disk so the user can continue later."""
    data = {
        "total_correct":    engine.total_correct,
        "best_streak":      engine.best_streak,
        "games_played":     {g.value: c for g, c in engine.games_played.items()},
        "game_switches":    engine.game_switch_count,
        "last_difficulty":  engine.current_difficulty.value,
        "last_game":        engine.current_game.value,
        "personality":      personality.value,
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
    except (json.JSONDecodeError, IOError):
        return None


def restore_engine(save_data: dict) -> tuple[AdaptiveEngine, Personality]:
    """Restore engine state and personality from saved data."""
    engine = AdaptiveEngine()
    engine.total_correct    = save_data.get("total_correct", 0)
    engine.best_streak      = save_data.get("best_streak", 0)
    engine.game_switch_count = save_data.get("game_switches", 0)
    engine.current_difficulty = Difficulty(save_data.get("last_difficulty", 2))
    engine.current_game     = GameType(save_data.get("last_game", "trivia"))
    engine.rewards_given    = set(save_data.get("rewards_given", []))
    for g_val, count in save_data.get("games_played", {}).items():
        try:
            engine.games_played[GameType(g_val)] = count
        except ValueError:
            pass
    personality = Personality(save_data.get("personality", "encouraging"))
    return engine, personality


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
    print("  Cognitive Robotics System for Pepper Robot")
    print("=" * 60)

    # ── load facial expression model ──
    print("\nLoading facial expression model...")
    face_model   = FacialExpressionModel(MODEL_JSON, MODEL_WEIGHTS)
    face_cascade = cv2.CascadeClassifier(HAAR_CASCADE)
    print("  Model loaded.")

    # ── local camera (dev/testing) ──
    local_camera = None
    if USE_LOCAL_CAMERA:
        local_camera = cv2.VideoCapture(0)
        print("  Using local webcam for expression detection.")
    else:
        print("  Using Pepper's camera for expression detection.")

    # ── connect to Pepper ──
    print(f"\nConnecting to Pepper at {NAO_IP}...")
    ssh     = ssh_connect()
    ssh_tts = ssh_connect()         # dedicated TTS connection
    print("  Connected.")

    # ── calibrate ambient noise level ──
    print("\nCalibrating ambient noise level (stay quiet for 3 seconds)...")
    energy_threshold = nao_calibrate_ambient(ssh)

    # ── check for saved session ──
    personality    = Personality.ENCOURAGING     # default
    preferred_game = None
    engine         = AdaptiveEngine()
    resumed        = False

    save_data = load_session()
    if save_data:
        prev_rounds = save_data.get("rounds_played", 0)
        prev_correct = save_data.get("total_correct", 0)
        prev_personality = save_data.get("personality", "encouraging")

        welcome_back = (
            f"Welcome back! Last time you played {prev_rounds} rounds, "
            f"got {prev_correct} correct, and I was in {prev_personality} mode. "
            "Want to continue where you left off, or start fresh?"
        )
        nao_track_face(ssh, enable=True)
        nao_set_leds(ssh, "FaceLeds", 0x0000FF00, 1.0)
        nao_gesture(ssh, "wave", personality)
        nao_say(ssh_tts, welcome_back)
        print(f"\nRobot: {welcome_back}")

        print("\nListening for continue/fresh...")
        nao_set_leds(ssh, "EarLeds", 0x0000FF00, 0.3)
        nao_record(ssh, energy_threshold)

        resume_text = ""
        if check_audio_volume():
            resume_text = transcribe()
            print(f"Heard: {resume_text}")

        lower_resume = resume_text.lower()
        if any(w in lower_resume for w in ["continue", "resume", "yes", "carry on",
                                            "keep going", "where I left", "left off"]):
            engine, personality = restore_engine(save_data)
            resumed = True
            print(f"  Restored: {save_data.get('rounds_played', 0)} rounds, "
                  f"personality={personality.value}")
        else:
            delete_save()
            print("  Starting fresh.")

    # ── OpenAI conversation history (game context continuity) ──
    conversation = [{"role": "system", "content": (
        "You are a Pepper robot game host called GAZE. You play interactive games "
        "with users and adapt based on their emotional state and performance. "
        "Always respond in the exact JSON format requested. Keep dialogue concise "
        "and natural — 2-3 sentences max. "
        + PERSONALITY_PROMPTS[personality]
    )}]

    if not resumed:
        # ── startup sequence ──
        nao_track_face(ssh, enable=True)
        nao_set_leds(ssh, "FaceLeds", 0x0000FF00, 1.0)
        nao_gesture(ssh, "wave", personality)

        # ── ask personality preference ──
        personality_prompt = (
            "Hello! I'm GAZE, your game host. "
            "Before we start, how would you like me to be? "
            "Encouraging and supportive, sarcastic and witty, or serious and focused?"
        )
        nao_say(ssh_tts, personality_prompt)
        print(f"\nRobot: {personality_prompt}")

        print("\nListening for personality choice...")
        nao_set_leds(ssh, "EarLeds", 0x0000FF00, 0.3)
        nao_record(ssh, energy_threshold)

        if check_audio_volume():
            personality_text = transcribe()
            print(f"Heard: {personality_text}")
            chosen_personality = parse_personality_choice(personality_text)
            if chosen_personality:
                personality = chosen_personality
                print(f"  Personality: {personality.value}")
            else:
                print("  Defaulting to encouraging.")
        else:
            print("  No response — defaulting to encouraging.")

        # update system prompt with chosen personality
        conversation[0]["role"] = "system"
        conversation[0]["content"] = (
            "You are a Pepper robot game host called GAZE. You play interactive games "
            "with users and adapt based on their emotional state and performance. "
            "Always respond in the exact JSON format requested. Keep dialogue concise "
            "and natural — 2-3 sentences max. "
            + PERSONALITY_PROMPTS[personality]
        )

        # ── ask game preference ──
        game_prompt = (
            "Great! Now, what would you like to play? "
            "I've got trivia, riddles, word games, spelling challenges, and maths puzzles."
        )
        nao_say(ssh_tts, game_prompt)
        print(f"\nRobot: {game_prompt}")

        print("\nListening for game choice...")
        nao_set_leds(ssh, "EarLeds", 0x0000FF00, 0.3)
        nao_record(ssh, energy_threshold)

        game_choice_text = ""
        chosen_game      = None

        if check_audio_volume():
            game_choice_text = transcribe()
            print(f"Heard: {game_choice_text}")
            chosen_game = parse_game_choice(game_choice_text)

        if chosen_game is None:
            chosen_game = GameType.TRIVIA
            print("  Defaulting to trivia.")
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
        nao_say(ssh_tts, resume_msg)
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
                                  user_game_choice=game_choice_text,
                                  personality=personality)
    game_data = generate_game_response(prompt, conversation)
    conversation.append({"role": "assistant", "content": json.dumps(game_data)})

    current_answer   = game_data.get("answer", "")
    current_question = game_data.get("dialogue", "")

    # deliver first question with gesture
    gesture_thread = threading.Thread(
        target=nao_gesture,
        args=(ssh, game_data.get("gesture", "neutral"), personality),
        daemon=True,
    )
    gesture_thread.start()
    nao_say(ssh_tts, current_question)
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
            # all three signals captured simultaneously

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
            nao_set_leds(ssh, "EarLeds", 0x0000FF00, 0.3)
            nao_record(ssh, energy_threshold)

            response_time = time.time() - question_start

            user_answer = ""
            if check_audio_volume():
                user_answer = transcribe()
                print(f"Heard: {user_answer}")
            else:
                print("(No response detected)")

            # exit keywords
            if user_answer.lower().strip() in [
                "stop", "quit", "exit", "goodbye", "bye", "end",
                "i want to stop", "let's stop", "no more",
            ]:
                print("User wants to stop.")
                break

            # ── FEEDBACK: mid-game personality/game changes ──────────────
            feedback = parse_feedback(user_answer)
            if "personality" in feedback:
                old_p = personality
                personality = feedback["personality"]
                # update system prompt
                conversation[0]["content"] = (
                    "You are a Pepper robot game host called GAZE. You play interactive games "
                    "with users and adapt based on their emotional state and performance. "
                    "Always respond in the exact JSON format requested. Keep dialogue concise "
                    "and natural — 2-3 sentences max. "
                    + PERSONALITY_PROMPTS[personality]
                )
                print(f"  Personality changed: {old_p.value} → {personality.value}")
                personality_ack = f"Got it! Switching to {personality.value} mode."
                nao_say(ssh_tts, personality_ack)
                print(f"Robot: {personality_ack}")

            if "game" in feedback:
                engine.current_game = feedback["game"]
                engine.game_switch_count += 1
                print(f"  User requested game switch to: {feedback['game'].value}")

            # ── PROCESS LAYER ────────────────────────────────────────────
            # check answer + adaptive engine infers state + decides

            nao_set_leds(ssh, "EarLeds", 0x000000FF, 0.3)  # blue = thinking

            correct = (check_answer(user_answer, current_answer, current_question)
                       if user_answer else False)
            print(f"  Correct: {correct}")

            decision = engine.decide(
                expression, expr_conf, response_time, correct, user_answer
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
                inferred_state=decision.inferred_state,
            ))

            # ── REWARD CHECK ─────────────────────────────────────────────
            reward_msg = engine.check_reward()
            if reward_msg:
                print(f"  REWARD: {reward_msg}")

            # ── GENERATE LAYER ───────────────────────────────────────────
            # construct dynamic prompt from live metrics → OpenAI

            prompt    = build_game_prompt(engine, decision,
                                          user_answer=user_answer,
                                          personality=personality,
                                          reward_message=reward_msg)
            game_data = generate_game_response(prompt, conversation)
            conversation.append({"role": "user",      "content": f"User answered: {user_answer}"})
            conversation.append({"role": "assistant",  "content": json.dumps(game_data)})

            current_answer   = game_data.get("answer", "")
            current_question = game_data.get("dialogue", "")

            # ── OUTPUT LAYER ─────────────────────────────────────────────
            # robot speaks + gestures + LEDs — all aligned to inferred state

            gesture_type = game_data.get("gesture", "neutral")

            # LED colour reflects inferred state
            nao_set_leds(
                ssh, "FaceLeds",
                LED_COLOURS.get(decision.inferred_state, 0x00FFFFFF), 0.5
            )

            # gesture and speech run in parallel
            gesture_thread = threading.Thread(
                target=nao_gesture,
                args=(ssh, gesture_type, personality), daemon=True
            )
            gesture_thread.start()
            nao_say(ssh_tts, current_question)

            print(f"\nRobot: {current_question}")
            print(f"(Answer: {current_answer})")

            # ── PROGRESSIVE SAVE ──────────────────────────────────────────
            # auto-save after every round so data survives unexpected crashes
            # (laptop dies, SSH timeout, etc.) — protects report data
            save_session(engine, personality, preferred_game)

    except KeyboardInterrupt:
        print("\n\nInterrupted.")

    # ══════════════════════════════════════════════════════════════════════
    #  SESSION END — save progress + summary
    # ══════════════════════════════════════════════════════════════════════

    # save session so user can continue later
    save_session(engine, personality, preferred_game)

    summary = engine.get_session_summary()
    print(f"\n{'=' * 60}")
    print("  SESSION SUMMARY")
    print(f"{'=' * 60}")
    for k, v in summary.items():
        print(f"  {k}: {v}")

    # farewell — adaptive to performance
    if summary.get("rounds", 0) > 0:
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

    nao_gesture(ssh, "wave", personality)
    nao_say(ssh_tts, farewell)
    print(f"\nRobot: {farewell}")

    # cleanup
    if local_camera is not None:
        local_camera.release()
    nao_track_face(ssh, enable=False)
    nao_set_leds(ssh, "FaceLeds", 0x00000000, 0.5)
    ssh.close()
    ssh_tts.close()
    print("\nGAZE disconnected.")


if __name__ == "__main__":
    main()
