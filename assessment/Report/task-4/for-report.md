# GAZE — Report Architecture Notes
# Use these as raw material; do NOT copy-paste directly into the report.
# Cross-reference code line numbers below against the submitted gaze.py.

---

## BACKGROUND — What makes this cognitively novel

**The cognitive mapping argument (from proposal + code):**
The proposal explicitly maps Pepper's behaviour to Neisser's perceptual cycle and cognitive robotics principles. The code realises each step:
- Perceive: camera captures face, microphone records speech, Python timer tracks response time
- Attend: AdaptiveEngine.infer_state() weighs all three signals simultaneously, not just the camera
- Anticipate: rolling_correctness() over the last 5 rounds predicts whether the user will find the next question too hard or too easy
- Plan: decide() selects difficulty, game type, tone, and whether to give hints
- Predict: the tone and gesture fields passed to OpenAI encode the robot's anticipation of how the user will receive the next question
- Learn: strategy_log (episodic memory) records every decision so patterns can be reviewed post-session
- Adapt: consecutive_correct / consecutive_wrong counters feed directly into the next decision

**Why this is NOT just a chatbot with a camera attached:**
Most LLM-driven HRI work simply passes a text prompt to GPT. GAZE builds a structured state machine (InferredState enum) *before* the LLM is involved. The LLM never sees raw sensor data; it sees a distilled, interpreted state. This separates perception (AdaptiveEngine) from generation (OpenAI), which is architecturally significant.

**Multi-signal fusion vs. single-signal approaches:**
The camera-only baseline would misclassify a user with a resting angry face who is answering quickly and correctly. infer_state() explicitly handles this (line ~269: "camera says Angry but fast + correct → they're fine"). Cite this as evidence of multi-modal reasoning rather than naive sensor fusion.

---

## METHOD & SETUP — What to explain in detail

**System architecture (block diagram already in proposal):**
Three input channels feed into one processing layer feeding into one output layer:
- INPUT: Pepper camera → facial expression CNN (WS-10 model, 7-class, 48×48 greyscale) + microphone → Whisper STT + Python timer
- PROCESS: AdaptiveEngine (pure Python, no ML) infers state, decides action, constructs prompt
- GENERATE: OpenAI gpt-4.1 generates dialogue, correct answer, category, gesture tag as structured JSON
- OUTPUT: ALTextToSpeech + ALMotion (gestures) + ALLeds (LED state) — all three fire simultaneously via threading

**The SSH architecture (worth explaining):**
The system runs on a laptop, not on Pepper directly. All robot control happens via paramiko SSH. Python 2 snippets are executed on the robot via `nao_run()`. This is important to explain because it means:
1- Network latency is a real concern (hence the single-payload nao_say fix)
2- Python 3 (laptop) calls Python 2 (Pepper) — type mismatches are a real risk
3- Two SSH connections are maintained (ssh for motor/LED/camera, ssh_tts for speech) to allow gesture and speech to run in parallel without blocking each other

**The facial expression model:**
- Pre-trained CNN from the WS-10 workshop (not trained fresh for this project — be transparent about this)
- 7 output classes: Angry, Disgust, Fear, Happy, Neutral, Sad, Surprise
- Haar cascade (haarcascade_frontalface_default.xml) for face detection before the CNN runs
- Input: 48×48 greyscale ROI of the largest detected face
- The model is used as a *supporting* signal, never as the sole determinant of state

**Ambient noise calibration:**
3-second silent calibration at startup via ALAudioDevice.getFrontMicEnergy(). Sets energy threshold dynamically as (ambient baseline + 200 buffer). Falls back to default 800 if ALAudioDevice is unsupported. This makes the system environment-adaptive — important for a university lab demo where background noise is unpredictable.

**Dynamic recording vs fixed sleep:**
Original approach: fixed 8-second time.sleep(). Problem: if user answers in 1 second, system hangs in silence for 7 more. New approach: polls microphone energy at 0.5s intervals, stops recording once 1.5s of silence follows detected speech. Hard ceiling of 12s. Firmware fallback to fixed sleep if getFrontMicEnergy() unsupported.

**Prompt construction (key for Method section):**
The prompt is never static. build_game_prompt() assembles it fresh every round from:
- Current personality system prompt
- Live metrics block (rolling correctness %, avg response time, recent expressions, inferred state)
- Adaptive instructions (hint/encouragement/game switch directives)
- Tone instruction mapped from the decision
- Strict JSON response format specification
This means the LLM context changes every round — the robot genuinely adapts rather than running a fixed script.

**Personality system:**
Three modes (ENCOURAGING, SARCASTIC, SERIOUS) injected into the OpenAI system message. Each maps to a distinct prompt string in PERSONALITY_PROMPTS. Gesture motion speeds are also scaled per personality (Serious = 1.8× slower, Sarcastic = 0.7× faster) to ensure physical behaviour matches verbal tone — preventing cognitive dissonance.

**Session persistence:**
gaze_save.json written after every round (progressive save). Stores: round history, correctness log, personality, preferred game, difficulty, rewards given. On restart, user can resume or start fresh. This supports longitudinal use (relevant to the rehabilitation analogy in the proposal).

---

## RESULTS / SYSTEM ANALYSIS — What to analyse and discuss

**Metrics you have access to from the session log:**
- Per-round: game_type, difficulty, correct (bool), response_time, facial_expression, inferred_state
- Session totals: accuracy, avg_response_time, game_switches, best_streak, final_difficulty, therapy_interventions (therapeutic version)
- Strategy log: every decision the engine made with the inferred state and chosen action

**Interesting patterns to look for and discuss:**
- Does difficulty ramp up over a session as the user improves? (final_difficulty vs starting MEDIUM)
- How often does the engine infer COMFORTABLE vs STRUGGLING vs THRIVING? Distribution across rounds shows whether the difficulty calibration is working
- Do game switches correlate with InferredState.FRUSTRATED? (They should — this would validate the engine logic)
- Response time trends: does avg_response_time decrease as the session progresses? (would suggest familiarity / engagement increasing)
- Camera expression vs inferred state divergence: how many rounds did the engine override the raw camera reading? (e.g., Angry expression but COMFORTABLE state)

**Limitations to acknowledge honestly (shows critical thinking):**
- The facial expression CNN was not fine-tuned for this task — it was a workshop model. Confidence scores can be low for non-frontal faces or poor lighting
- VOLUME_THRESHOLD and energy calibration rely on ALAudioDevice — if unsupported on the lab Pepper, recordings fall back to fixed duration
- Response time includes robot speech time (the timer starts at question delivery, not end of speech) — introduce a correction factor if citing absolute values
- The multi-signal fusion uses hand-coded thresholds (CORRECTNESS_FLOOR = 0.4, RESPONSE_TIME_BASELINE = 30s) rather than learned parameters — this is a deliberate design choice (interpretability over ML) but worth acknowledging
- Conversation history grows unboundedly across rounds — for very long sessions (> 20 rounds) this may approach token limits

**What to say about the LLM integration:**
The LLM (gpt-4.1) is used for three distinct tasks: 1) game/dialogue generation, 2) answer correctness checking (semantic, handles speech-to-text quirks), 3) cognitive reframing therapy dialogue. Each has a different temperature (0.8 for generation, 0.0 for answer checking, 0.7 for therapy). Varying temperature by task is worth explicitly mentioning — it shows deliberate design rather than default settings throughout.

---

## Architecture: Graduated Therapeutic Escalation

  The system tracks consecutive_negative (rounds where state is STRUGGLING, FRUSTRATED, or DISENGAGED) and escalates through three intervention levels with a 3-round cooldown
   between interventions to avoid feeling patronising:

  Level 1 -- Episodic Reminiscence (2 consecutive negative states)

- Searches engine.history for the user's most recent correct answer
- Cites it specifically: "Remember 3 rounds ago when you got that riddles question right? You clearly know your stuff."
- Falls back to streak data or generic determination acknowledgment if no past success exists
- Lightest touch; woven into the game flow without a full pause

  Level 2 -- Cognitive Reframing (3 consecutive negative states)

- Sends a specialised prompt to OpenAI requesting an empathetic check-in
- The LLM mirrors the user's detected emotional state and offers exactly two choices: talk about it or switch activities
- Personality-aware (sarcastic robot reframes differently from encouraging robot)
- After speaking, listens for the user's response and parses any game/personality change requests

  Level 3 -- Mindfulness Breathing (4+ consecutive negative states)

- Full game pause; single SSH payload executes on Pepper
- Three breathing cycles: arms rise on inhale, lower on exhale
- LEDs fade between calming blue (inhale) and soft green (exhale)
- Verbal cues guide timing: "Breathe in... Hold... And breathe out..."
- Motor fallback: if arm control fails, delivers verbal-only exercise
- Most intensive intervention, reserved for sustained distress

  Integration points:

- TherapyType enum + thresholds in config
- AdaptiveDecision.therapy_break field carries the therapy type through the decision pipeline
- Therapy executes between PROCESS and GENERATE layers in the game loop
- Post-therapy listener captures user feedback (game/personality changes)
- therapy_count appears in session summary for your Results section
- Intervention logged in strategy_log episodic memory
