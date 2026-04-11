# Salman -- Section 2.4 Outcome & System Analysis (30%)

This section is YOUR responsibility per the proposal contribution split. It carries 30% of the Task 4 mark. Everything below is guidance to ensure your section aligns with the architecture described in Alfie's Methods (Section 2.3) and reads as a cohesive report rather than two siloed contributions.

---

## Core Objective

Prove the multi-signal engine and adaptation logic described in Section 2.3 actually functioned in practice. The marker needs to see that the system did what the report claims it does.

---

## Three Strategic Approaches (pick one or combine)

### 1- The Temporal Case Study

A round-by-round breakdown of a single session, proving the engine caught a frustration streak and resolved it via the `evaluate_adaptation()` logic. Walk through specific rounds showing: inferred state changed, difficulty adjusted, user recovered. This is the most narrative approach and the easiest to write compellingly.

### 2- The Aggregate Metric Defence

Pool data across multiple test runs to prove the statistical efficacy of specific outcome pairs (e.g. success rate of difficulty decreases, frequency of game switches correlating with state recovery). This is stronger academically but requires enough session data.

### 3- The Ablation Scenario

Contrast the multi-signal system's behaviour against a would-be baseline that only uses facial expressions, thereby proving the single-signal problem is genuinely solved. E.g. "In round 7 the camera read Angry but the user answered correctly in 4 seconds; a single-signal system would have eased difficulty unnecessarily, whereas GAZE correctly inferred Comfortable."

---

## Alignment Checklist (link your analysis to Section 2.3)

- [ ] **1- The Whisper Latency Proof:** Explicitly reference the timer architecture from 2.3.2 (timer halts when recording completes, before Whisper API call). When graphing or analysing response times, acknowledge that these measure user deliberation, not network latency.

- [ ] **2- `evaluate_adaptation()` Efficacy:** Report must show concrete outcome pairs from the session data:
    - [ ] Frequency of correct-after-incorrect following a difficulty decrease
    - [ ] Frequency of state-transitions (Frustrated/Disengaged -> Comfortable/Thriving) following a game switch
    - [ ] Frequency of response-time reductions following encouragement

- [ ] **3- The Streak Intervention:** Show empirical evidence of the derived temporal signals (rolling correctness, consecutive silences, consecutive wrong streak) triggering adaptive actions. Cite specific round numbers from the session log.

- [ ] **4- The Fallback Scenario:** State whether the `getFrontMicEnergy()` dynamic silence detection worked on the lab Pepper or whether the fixed-duration fallback activated. If fallback activated, acknowledge the response-time signal was inflated for those rounds and explain how the engine's reliance on correctness and streak signals provided graceful degradation (this is already described in 2.3.3; reference it).

- [ ] **5- Metacognition Bridge:** Explicitly link the action timeline to the `evaluate_adaptation()` self-evaluation loop. Show that the system not only adapted but assessed whether its adaptations worked, and fed that assessment back into the next round's prompt. This is what elevates the system from reactive to cognitive.

---

## Code-to-Report Architecture Map

Use this to reference specific code when writing. Every claim in your section should trace back to a function.

| Code Component | File Location | Report Section | What It Does |
|---|---|---|---|
| `SpeechEmotionModel` class | gaze.py lines 175-225 | 2.3.2 (Signal 3) | WS-08 MLP; returns (emotion, confidence) via `predict_proba()` |
| `capture_and_classify()` | gaze.py lines ~1430-1440 | 2.3.2 (Signal 1) | WS-10 CNN; classifies face into 7 emotions with confidence |
| `FACE_CONFIDENCE_THRESHOLD` / `VOICE_CONFIDENCE_THRESHOLD` | gaze.py lines ~94-95 | 2.3.2 | If model confidence < 0.5, prediction is overridden to Neutral/neutral — defensive against noisy readings |
| `AdaptiveEngine.infer_state()` | gaze.py lines ~418-513 | 2.3.3 | 7 signals in, 5 states out; cross-modal rules |
| `AdaptiveEngine.decide()` | gaze.py lines ~517+ | 2.3.3 | Maps inferred state to difficulty/game-switch/hints/tone |
| `evaluate_adaptation()` | gaze.py (tool function) | 2.3.6 | Compares outcome pairs; feeds self-evaluation into next LLM call |
| `build_signal_context()` | gaze.py (conversation loop) | 2.3.4 | Packages 5 live signals into context block for GPT-4.1 |
| `TOOLS` list (8 function-calling tools) | gaze.py | 2.3.4 | LLM decides which tools to invoke; neuro-symbolic interface |
| `Personality` enum | gaze.py | 2.2 / 2.5 | 4 modes (Cheeky, Mentor, Coach, Therapeutic); injected into system prompt |
| `local_calibrate_ambient()` | gaze.py | 2.3.2 (Signal 2) | Dynamic RMS threshold calibration at startup; replaces static VAD |
| `gaze_save.json` | generated at runtime | 2.4 (your section) | Per-round session log; your primary data source |

---

## Metrics Available from the Session Log

The `gaze_save.json` file and console output provide per-round data:

| Metric | Source | Use it to show... |
|---|---|---|
| `game_type` | round log | Game switches correlating with frustration/disengagement |
| `difficulty` | round log | Difficulty trajectory over the session (ramp up / ease off) |
| `correct` | round log | Accuracy trends; streak patterns |
| `response_time` | round log | Engagement trends; does avg time decrease as session progresses? |
| `facial_expression` | round log | Camera readings vs inferred state (show overrides); readings below 0.5 confidence were auto-overridden to Neutral |
| `vocal_emotion_confidence` | round log | Voice model confidence; readings below 0.5 were auto-overridden to neutral |
| `inferred_state` | round log | Distribution across 5 states; does the system stabilise at Comfortable? |
| `accuracy` | session summary | Overall performance |
| `best_streak` | session summary | Peak engagement |
| `game_switches` | session summary | How often the engine intervened |
| `therapy_interventions` | session summary | How many therapeutic breaks fired |

---

## Vocabulary to Use (matching Alfie's sections)

Use these terms so the report reads as one voice:
- "inferred state" (not "detected emotion")
- "multi-signal fusion" (not "emotion detection")
- "rolling correctness" (not "average score")
- "consecutive wrong streak" (not "error count")
- "graceful degradation" (when discussing fallbacks)
- "neurosymbolic" (when referring to the architecture)
- "cross-modal" (when describing how signals override each other)

---

## What NOT to Do

- Do not describe the architecture again; that is Section 2.3. Reference it ("as described in Section 2.3.3") and analyse the results.
- Do not fabricate session data. Run the system, log the output, analyse what actually happened.
- Do not ignore limitations. If the facial expression model confidence was low under lab lighting, say so. Honest limitations earn marks at the 70%+ boundary.
- Do not forget to cite. Even the Results section should reference papers: e.g. Desai et al. (2013) on trust degradation after failures, Smedegaard (2019) on whether engagement sustained beyond novelty.

---

## Word Budget

You have approximately 600-700 words for this section (the remaining budget after Introduction, Background, Methods, Conclusion, and References). Be dense. Every sentence should either present data or interpret data. No filler.
