# GAZE ~2.5-Minute Video Demo -- Script Notes

Brief allows up to 5 minutes; chosen target is **~2.5 minutes**, dense and HRI-focused. Covers Alfie's contribution only (multi-signal cognitive loop + wake-word gate); Salman's work (TTS pacing, scoring, LEDs, calibration) deferred to the written Method section.

---

- [ ] discuss the emotinal recognition deeply
  - [ ] sample-rate bug -- RAVDESS 48 kHz vs mic 16 kHz; Gemini caught it
  - [ ] mel bins 0-24 kHz at training, 0-8 kHz at inference; 3$\times$ spectral warp
  - [ ] fix: `librosa.load(sr=16000)`; retrain; reship pkl
  - [ ] my audit assumed 16 kHz on both sides; Gemini cross-check caught it
  - [ ] cross-modal design masked a silent vocal-channel failure -- hence the novelty
  - [ ] loudness-normalisation = accessibility for quieter brain-injured users
- [ ] find the best HRI-relevant stuff to discuss
- [ ] discuss why text-prompts to NAO robot need to not be indented to work probably

## Structure (~2.5 minutes total, 150 s)

Method-and-setup orientated; each shot pairs a function in `gaze.py` with a one-sentence HRI rationale. Line numbers are pinned so you can tab to them live on-camera.

### 0:00--0:10 -- Framing (10 s)

One sentence: *"GAZE's novel contribution is a multi-signal adaptive cognitive loop: infer state, adapt, then evaluate whether the adaptation helped. No single signal is trusted alone."*

### 0:10--0:45 -- Multi-signal state inference (35 s) -- `AdaptiveEngine.infer_state()` @ gaze.py:525

Headline novelty. Separates GAZE from a single-signal classifier wire-up.

- Show the four inputs feeding `infer_state()`: facial expression (WS-10 CNN, 7-class 48$\times$48 greyscale), vocal emotion (WS-08 MLP, MFCC/chroma/mel), response time, answer correctness.
- Show the cross-validation branches inside the function and the `InferredState` output that feeds everything downstream.
- **Narrate:** *"The robot doesn't commit to one signal -- it triangulates. A happy face with a wrong answer and a long response time doesn't read as 'happy'; it reads as 'struggling but hiding it'. Workshop 10 and Workshop 8 gave me two independent inference paths; I use both as votes rather than as an oracle."*
- **Salvage-line from the old script:** *"The camera says Angry but I answered fast and correctly, so the engine correctly infers Comfortable."* That example lands in one sentence; keep it.

### 0:45--1:15 -- Signal-driven think-time budget (30 s) -- `AdaptiveEngine.recommend_think_budget()` @ gaze.py:699

Strongest HRI moment: accommodation-by-inference, not accommodation-by-request.

- Show inputs: silence duration, response time, facial expression, `InferredState`, and `game_state.waiting` flag.
- Show outputs: updated `engine.think_budget_secs` and `engine.silence_tolerance_secs`.
- **Contrast:** *"`request_more_time` exists but is one signal among many -- it sets `waiting = True` which feeds this function; it never bumps the budget directly."*
- **Narrate:** *"I deliberately broke the brittle pattern where asking 'give me more time' is the only way to get more time. The robot infers struggle from silence-plus-expression-plus-history and quietly widens the window. That respects users who can't or won't verbalise the request -- which is most of the stroke-recovery cohort GAZE targets."*

### 1:15--1:40 -- Adaptation self-evaluation (25 s) -- `AdaptiveEngine.evaluate_adaptation()` @ gaze.py:844

Closed-loop cognition. Rare in student projects thus strong for ≥70% marks.

- Show the function asking *"did the last adaptation help?"* and feeding that answer into the next `decide()` call.
- **Narrate:** *"Without this the system would adapt blindly -- make a change and never check. This loop lets GAZE back out of a bad adaptation (e.g. easier difficulty that bored the user) rather than doubling down."*

### 1:40--2:15 -- Wake-word gate + defence-in-depth (35 s) -- `has_wake_word()` @ gaze.py:1651

Only shot with a visible live demo; the other three are cognitive-internal.

- **(10 s live)** Ask a question on-camera, stay silent for 10 s. Console prints `No wake-word detected; skipping Whisper.` Round passes cleanly.
- **(10 s pre-recorded)** Cut to the "bypass-gate" clip: Whisper hallucinating Khmer-script gibberish on the same 60 s of silent audio (from the empirical test; keep the screenshot of `'សានំរានំរានំ... ḏḏḏḏḏ'`).
- **(15 s voice-over on the 5-layer stack):** *"Whisper hallucinates on silent audio -- verified empirically on a 60 s test, it returned Khmer-script gibberish and 'Q1. Q1.' loops 140 times over. The wake-word gate is a fifth defence layer: the robot only listens when addressed by name. This is deliberate addressing ritual, socially analogous to turn-taking in human conversation."*

### 2:15--2:30 -- Close (15 s)

*"Each of these four mechanisms -- multi-signal inference, signal-driven think-time, adaptation self-evaluation, and addressing-ritual gating -- is a direct response to a workshop concept or a documented HRI failure mode. The system is adaptive-by-construction, not adaptive-by-accident."*

---

## Filming Checklist

- [ ] Laptop screen visible (console output showing signals, states, decisions)
- [ ] Pepper visible (gestures, LED colours, speaking)
- [ ] Audio clear (Pepper's speech audible, your narration audible)
- [ ] Show at least one instance of multi-signal override (camera misread corrected by performance signals)
- [ ] Show at least one difficulty adaptation (ramp up or ease off)
- [ ] Show at least one game switch (numbers to letters or vice versa)
- [ ] Show the farewell sequence and session summary
- [ ] Ensure the .env file has the correct NAO_IP before filming

## Things to Say (mark-earning phrases)

- "Multi-signal emotional inference" -- the novelty
- "The engine weighs six signals simultaneously" -- shows depth
- "Cross-modal rules override the camera when performance signals contradict it" -- demonstrates critical design
- "The architecture is neurosymbolic: symbolic rules for state inference, neural LLM for dialogue generation" -- shows awareness
- "The prompt is never the same twice; it is dynamically constructed from live metrics every round" -- demonstrates genuine adaptation
- "WS-10 facial expression model integrated from the workshop" -- shows module engagement
- "Dual SSH connections for concurrent speech and gesture" -- shows engineering thought

## Edge Cases to Avoid During Filming

- Don't let the OpenAI API timeout (ensure good internet connection in the lab)
- Don't let the session run too long (conversation history could hit token limits after ~20 rounds)
- If Pepper's camera fails to detect a face, the system defaults to "Neutral" with 0.0 confidence -- this is fine, narrate it as a graceful fallback
- If `getFrontMicEnergy()` is unsupported, recording falls back to fixed duration -- this is also fine, narrate it
