# GAZE ~2.5-Minute Video Demo -- Script Notes

Brief allows up to 5 minutes; chosen recording-runtime is **~2 minutes** with **2x post-production speedup, hence ~4 minutes of content density**, delivered in a confident, intricate, evidence-backed register. Covers Alfie's contribution only per the gaze22.py docstring authorship, in this left-to-right order: 1) architecture, 2) OpenAI integration, 3) AdaptiveEngine *(the brain of the robot)*, 4) facial-expression pipeline. Salman demonstrates his lane (noise calibration, Pepper speech, gestures, LEDs, session save and resume, testing) separately.

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

## Structure (~2 min recording / ~4 min content density after 2x speedup, 240 s of content)

Method-and-setup orientated; each shot pairs a function in `gaze.py` with a one-sentence HRI rationale. Line numbers are pinned so you can tab to them live on-camera.

### 0:00--0:10 -- Framing (10 s)

One sentence: *"GAZE's novel contribution is a multi-signal adaptive cognitive loop: infer state, adapt, then evaluate whether the adaptation helped. No single signal is trusted alone."*

### 0:10--0:45 -- Multi-signal state inference (35 s) -- `AdaptiveEngine.infer_state()` @ gaze22.py:{very exact page number when screen recording}

Headline novelty. Separates GAZE from a single-signal classifier wire-up.

- Show the five inputs feeding `infer_state()`: facial expression (WS-10 CNN, 7-class 48$\times$48 greyscale), vocal emotion (WS-08 MLP, MFCC/chroma/mel), response time, answer correctness, and volume/RMS.
- Show the cross-validation branches inside the function and the `InferredState` output that feeds everything downstream.
- **Narrate:** *"The robot doesn't commit to one signal -- it triangulates. A happy face with a wrong answer and a long response time doesn't read as 'happy'; it reads as 'struggling but hiding it'. Workshop 10 and Workshop 8 gave me two independent inference paths; I use both as votes rather than as an oracle."*
- **Salvage-line from the old script:** *"The camera says Angry but I answered fast and correctly, so the engine correctly infers Comfortable."* That example lands in one sentence; keep it.

### 0:45--1:15 -- Signal-driven think-time budget (30 s) -- `AdaptiveEngine.recommend_think_budget()` @ gaze22.py:{very exact page number when screen recording}

Strongest HRI moment: accommodation-by-inference, not accommodation-by-request.

- Show inputs: silence duration, response time, facial expression, `InferredState`, and `game_state.waiting` flag.
- Show outputs: updated `engine.think_budget_secs` and `engine.silence_tolerance_secs`.
- **Contrast:** *"`request_more_time` exists but is one signal among many -- it sets `waiting = True` which feeds this function; it never bumps the budget directly."*
- **Narrate:** *"I deliberately broke the brittle pattern where asking 'give me more time' is the only way to get more time. The robot infers struggle from silence-plus-expression-plus-history and quietly widens the window. That respects users who can't or won't verbalise the request -- which is most of the stroke-recovery cohort GAZE targets."*

### 1:15--1:40 -- Adaptation self-evaluation (25 s) -- `AdaptiveEngine.evaluate_adaptation()` @ gaze22.py:{very exact page number when screen recording}

Closed-loop cognition. Rare in student projects thus strong for ≥70% marks.

- Show the function asking *"did the last adaptation help?"* and feeding that answer into the next `decide()` call.
- **Narrate:** *"Without this the system would adapt blindly -- make a change and never check. This loop lets GAZE back out of a bad adaptation (e.g. easier difficulty that bored the user) rather than doubling down."*

### 1:40--2:15 -- Wake-word gate + defence-in-depth (35 s) -- `has_wake_word()` @ gaze22.py:{very exact page number when screen recording}

Only shot with a visible live demo; the other three are cognitive-internal.

- **(10 s live)** Ask a question on-camera, stay silent for 10 s. Console prints `No wake-word detected; skipping Whisper.` Round passes cleanly.
- **(10 s pre-recorded)** Cut to the "bypass-gate" clip: Whisper hallucinating Khmer-script gibberish on the same 60 s of silent audio (from the empirical test; keep the screenshot of `'សានំរានំរានំ... ḏḏḏḏḏ'`).
- **(15 s voice-over on the 5-layer stack):** *"Whisper hallucinates on silent audio -- verified empirically on a 60 s test, it returned Khmer-script gibberish and 'Q1. Q1.' loops 140 times over. The wake-word gate is a fifth defence layer: the robot only listens when addressed by name. This is deliberate addressing ritual, socially analogous to turn-taking in human conversation."*

### 2:15--2:30 -- Close (15 s)

*"Each of these four mechanisms -- multi-signal inference, signal-driven think-time, adaptation self-evaluation, and addressing-ritual gating -- is a direct response to a workshop concept or a documented HRI failure mode. The system is adaptive-by-construction, not adaptive-by-accident."*

### Restructured for gaze22.py (4-pillar order, evidence-backed)

The five segments above are preserved as historical reference; the restructured script herein realigns to gaze22 (delivered to the module leader on 2026-05-02), reorders by Alfie's four pillars per the gaze22.py docstring authorship, and pins on-screen evidence per segment for confident, intricate delivery. Recording target is ~2 min real-time with a 2x post-production speedup, hence ~4 min of content density (240s of content) compressed into ~120s of playback.

#### Segment 1 (Pillar 1): Architecture (50s content, 25s playback)

**If you freeze, anchor on:** *It watches five things at once and no single one wins on its own; they vote.*

References:
- gaze22.py:{very exact page number when screen recording} (docstring header; 5-signal hierarchy, voice rationale, modes, Whisper-gating stack, wake-word history, TCP plus decoupled-detection, authorship -- all in the docstring block)
- gaze22.py:{very exact page number when screen recording} (`has_wake_word()` Vosk gate; **bypassed in production** via `transcribe(bypass_wake_word=True)`; the function is preserved as engineering history)
- gaze22.py:{very exact page number when screen recording} (`has_real_speech()` Silero VAD pre-gate)
- gaze22.py:{very exact page number when screen recording} (`is_known_hallucination()` blacklist plus URL/disclaimer regex; `normalise_for_blacklist()` helper just above)

On-screen evidence: docstring header visible in editor (scroll to show the wake-word-bypassed history and the TCP+decoupled-detection paragraph); jump-cut to the Whisper-Khmer-script-hallucination screenshot.

> *"GAZE is a Pepper game host wherein the robot adapts difficulty, pacing and feedback per turn from five signals; the docstring ranks them: facial expression and answer-correctness and response-time as primary, volume as secondary, vocal emotion as tie-breaker only. Indeed, no single signal is trusted alone (the watchword herein is multi-signal fusion). Voice is consulted only when face is Neutral and confidence clears the 0.9 floor, due to the speech model collapsing to 'fearful' on quiet or noisy robot audio (the docstring records this verbatim). The Whisper-gating stack is now three-tier: Silero VAD here, no_speech_prob downstream from Whisper itself, and a hallucination blacklist plus URL-regex. A Vosk wake-word check was wired early-in to combat Pepper-stream hallucinations, and indeed it worked; however, once HYBRID_LOCAL_INPUT moved mic-input to the Mac (which doesn't hallucinate the same way), wake-word added friction without proportional benefit, hence we now bypass it via `transcribe(bypass_wake_word=True)` (the docstring records the history). The function is preserved as documented engineering iteration. This was hardened empirically; a 60s silent audio test against Whisper directly returned Khmer-script gibberish and 'Q1.' looped 140 times over (screenshot herein), and indeed each remaining layer falls through gracefully if its dependency fails to load, lest a brittle import-chain exclude assistive-tech users disproportionately."*

#### Segment 2 (Pillar 2): OpenAI integration (60s content, 30s playback)

**If you freeze, anchor on:** *The LLM doesn't get retrained; we just change what we tell it about the user every turn.*

References:
- gaze22.py:{very exact page number when screen recording} (TOOLS list; four LLM tools, including `evaluate_last_adaptation`)
- gaze22.py:{very exact page number when screen recording} (`build_signal_context()` LIVE SIGNALS block; semantic pacing label inside)
- gaze22.py:{very exact page number when screen recording} (`converse()` gpt-5.4 chat-completion with tools)
- gaze22.py:{very exact page number when screen recording} (`API_TIMEOUT = 10`; graceful degradation)

On-screen evidence: scroll through `build_signal_context()` with the LIVE SIGNALS block highlighted; switch to a console / log capture of one round's actual injected prompt-context so the marker sees the literal text that GPT-5.4 receives.

> *"The LLM is frozen; we never retrain. Therefore, what makes this thing adaptive is herein -- `build_signal_context()` rebuilds a LIVE SIGNALS block every turn from face, voice, volume, response-time and rolling correctness, and indeed the prompt is never the same twice. Crucially, the symbolic engine *describes* the user to the LLM, the LLM *generates* language conditioned on that description; hence neurosymbolic in the literal sense: symbolic-in the state estimate, neural-in the dialogue. The pacing label maps the raw budget seconds to a semantic cue ('relaxed and patient' versus 'brisk and energetic'), lest the LLM parrot the exact seconds back to the user verbatim. Closed-loop metacognition is achieved by exposing `evaluate_last_adaptation` to the LLM as a callable tool; thereby the LLM may read the engine's self-evaluation and incorporate it into the next utterance. This embodies the measurement problem (the latent emotional state cannot be observed directly; the LIVE SIGNALS block is the engine's running estimate, made legible to the LLM as text). API graceful-degradation sits in `API_TIMEOUT = 10`, a 10-second timeout with a placeholder utterance, hence the round never blocks on a network hiccup."*

#### Segment 3 (Pillar 3): AdaptiveEngine, *the brain of the robot* (90s content, 45s playback)

**If you freeze, anchor on:** *Read, decide, pace, check yourself; one loop every turn.*

References:
- gaze22.py:{very exact page number when screen recording} (`AdaptiveEngine` class header)
- gaze22.py:{very exact page number when screen recording} (`rolling_correctness()` 5-round window)
- gaze22.py:{very exact page number when screen recording} (`infer_state()` multi-signal fusion; face-primary rules; voice tie-break; arousal calibration; voice-trust gate)
- gaze22.py:{very exact page number when screen recording} (`decide()` state-to-policy)
- gaze22.py:{very exact page number when screen recording} (`recommend_think_budget()` per-state pacing; graduated extension formula; Round-1 stroke-recovery grace)
- gaze22.py:{very exact page number when screen recording} (`evaluate_adaptation()` closed-loop self-eval; three evaluation patterns)

On-screen evidence: scroll AdaptiveEngine top-down through the four canonical methods; pin a sticky-corner showing the LIVE SIGNALS block for the same turn so the marker can trace observation, belief-update, policy, pacing, evaluation in one cohesive sequence.

> *"The AdaptiveEngine is essentially the brain of the robot: four canonical methods that close a perceive-decide-pace-evaluate loop every turn. First, `infer_state()` fuses the five signals into one of five InferredStates: THRIVING, COMFORTABLE, STRUGGLING, FRUSTRATED, DISENGAGED. Face is treated as primary; voice is consulted only when face is Neutral *and* vocal confidence clears 0.9, due to the documented voice-collapse-to-fearful issue. Second, `decide()` maps the inferred state to a policy: THRIVING escalates difficulty, STRUGGLING de-escalates and surfaces a hint, DISENGAGED switches game type after three consecutive silences. Third, `recommend_think_budget()` widens the recording window per-state; the graduated extension formula is `no_speech_max = max(no_speech_max, 5.0 + consecutive_silences * 1.5)`, hence pacing rewards patience proportionally rather than as a step function. Round-1 stroke-recovery grace gives a literally-first-turn user 7 seconds before the silence-timer fires whatsoever, contrary to the assistive-tech default of strict timeout. Fourth, `evaluate_adaptation()` closes the loop; it asks 'did the last adaptation help?' across three patterns: did struggling-then-easier flip to correct, did thriving-then-HARD overshoot, did disengaged-then-game-switch re-engage. Without this fourth method the system would adapt blindly and could not back out of a bad call. Rolling correctness holds a 5-round window so single-bad-rounds cannot derail the engine; this is the temporal-context arm that prevents the brain from being one-shot-reactive."*

#### Segment 4 (Pillar 4): Facial-expression pipeline plus RAVDESS sample-rate bug (35s content, 17s playback)

**If you freeze, anchor on:** *Two small classifiers; the voice one had a sample-rate bug, and the cross-modal design hid it.*

References:
- gaze22.py:{very exact page number when screen recording} (`FacialExpressionModel` CNN WS-10; `SpeechEmotionModel` MLP WS-08; `classify_speech_emotion()` helper just below)
- The RAVDESS bug: 48 kHz training versus 16 kHz inference; $48 / 16 = 3$, hence 3$\times$ spectral warp; mel-bins 0-24 kHz at training mapped to 0-8 kHz at inference; classifier collapsed to "fearful". Fix: `librosa.load(sr=16000)` plus retrain plus reship `.pkl`.
- Detection method: Gemini cross-check audit caught it; Alfie's own audit had assumed 16 kHz on both sides.

On-screen evidence: model-summary print of the WS-10 CNN architecture; before/after mel-spectrogram showing the warp; the literal one-line `librosa.load(sr=16000)` fix in the diff.

> *"The facial-expression pipeline is a WS-10 CNN: 48$\times$48 greyscale, seven classes (Angry, Disgust, Fear, Happy, Neutral, Sad, Surprise). Indeed, this is what the engine treats as primary signal in the LIVE SIGNALS block. The vocal classifier alongside it is a WS-08 MLP on MFCC, chroma and mel features, and indeed therein lies the would-be hidden failure: RAVDESS trained at 48 kHz, the Pepper microphone records at 16 kHz, hence $48 / 16 = 3$, a 3$\times$ spectral warp; mel-bins that the model expected to span 0-24 kHz were instead spanning 0-8 kHz at inference, and the classifier consequently collapsed to 'disgust' regardless of the true emotion. My own audit assumed 16 kHz on both sides; a Gemini cross-check caught it. Fix was `librosa.load(sr=16000)` plus a full retrain plus reship of the `.pkl`. Crucially, the cross-modal design masked the silent vocal-channel failure for weeks, and therein lies the novelty (the multi-signal architecture is its own diagnostic instrument; a single-signal system would have been silently broken). Loudness-normalisation is also accessibility-in (quieter brain-injured users would otherwise be triaged below the volume floor whatsoever). One residual skew remains: post-fix, the MLP collapses to 'fearful' on quiet or low-energy audio, due to RAVDESS's actor-exaggerated fear not generalising to real-room speech and mean-pooling collapsing fear's temporal structure (irregular pitch, tremor) into a single vector. Perfecting the classifier in isolation was deprioritised in favour of the multi-signal architecture itself; the skew is therefore engineered-around at the trust-gate (`vocal_conf >= 0.9 and vocal_emotion != 'fearful'` in `AdaptiveEngine.infer_state()`) rather than retrained-out, and indeed this is the measurement-problem framing made operational: a noisy observation channel is gated, not trusted."*

#### Segment 5: Close (5s content, 2-3s playback)

**If you freeze, anchor on:** *Four pieces, none of them adapt on accident.*

> *"The four pillars therefore: architecture, OpenAI integration, AdaptiveEngine, facial-expression pipeline; adaptive-by-construction, not adaptive-by-accident."*

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
- [ ] Editor visible during AdaptiveEngine segment (gaze22.py:{very exact page number when screen recording} scrolled top-down)
- [ ] LIVE SIGNALS block visible on-screen during Segment 2 (gaze22.py:{very exact page number when screen recording} in editor)
- [ ] Whisper-Khmer-script hallucination screenshot ready as cut-in for Segment 1
- [ ] RAVDESS mel-spectrogram before/after warp screenshot ready for Segment 4
- [ ] Console / log capture of one turn's literal LIVE SIGNALS prompt-context for Segment 2 evidence
- [ ] Pace-rehearse before recording; 240s of content into 120s of recording, hence ~2x speech-rate target. Deliver confidently, do not skim or stutter
- [ ] Post-production: apply 2x speed filter; verify intelligibility on first watch-through

## Things to Say (mark-earning phrases)

- "Multi-signal emotional inference" -- the novelty
- "The engine weighs five signals simultaneously" -- shows depth
- "Cross-modal rules override the camera when performance signals contradict it" -- demonstrates critical design
- "The architecture is neurosymbolic: symbolic rules for state inference, neural LLM for dialogue generation" -- shows awareness
- "The prompt is never the same twice; it is dynamically constructed from live metrics every round" -- demonstrates genuine adaptation
- "WS-10 facial expression model integrated from the workshop" -- shows module engagement
- "Dual SSH connections for concurrent speech and gesture" -- shows engineering thought
- "The brain of the robot": a perceive-decide-pace-evaluate loop
- "The cross-modal design is its own diagnostic instrument; a single-signal system would have been silently broken"
- "Loudness-normalisation is accessibility-in for quieter brain-injured users"
- "Neurosymbolic bridge: symbolic-in the state estimate, neural-in the dialogue"
- "This embodies the measurement problem: latent state inferred from noisy multi-signal observation"
- "Closed-loop metacognition; the engine's self-evaluation is exposed back to the LLM as a callable tool"
- "The graduated extension formula rewards patience proportionally, not as a step function"
- "Five-state belief estimate, not a binary engaged-or-not"
- "The engine adapts difficulty and infers the user's state based on the fraction correct over the most recent (up to) five rounds" -- defines rolling correctness in one sentence; spoken cleanly, no jargon
- "The prompt is never the same twice; adaptivity lives in prompt-state, not in the LLM weights"

## Edge Cases to Avoid During Filming

- Don't let the OpenAI API timeout (ensure good internet connection in the lab)
- Don't let the session run too long (conversation history could hit token limits after ~20 rounds)
- If Pepper's camera fails to detect a face, the system defaults to "Neutral" with 0.0 confidence -- this is fine, narrate it as a graceful fallback
- If `getFrontMicEnergy()` is unsupported, recording falls back to fixed duration -- this is also fine, narrate it
- Don't outrun your own narration; 2x post-production speedup is forgiving, but a stuttered original recording stays stuttered after speedup. If you trip on a phrase, restart the take rather than push through.
- Confidence over completeness; if a sentence isn't landing on the take, drop it cleanly. Intricacy comes from concentration, not breathlessness.
