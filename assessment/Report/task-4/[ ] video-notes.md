# GAZE 5-Minute Video Demo -- Script Notes

Brief requirement: "a **video of 5 minutes** describing your contribution and showing clearly a running demo of your work."

---

- [ ] discuss the emotinal recognition deeply
  - [ ] sample-rate bug -- RAVDESS 48 kHz vs mic 16 kHz; Gemini caught it
  - [ ] mel bins 0-24 kHz at training, 0-8 kHz at inference; 3$\times$ spectral warp
  - [ ] fix: `librosa.load(sr=16000)`; retrain; reship pkl
  - [ ] my audit assumed 16 kHz on both sides; Gemini cross-check caught it
  - [ ] cross-modal design masked a silent vocal-channel failure -- hence the novelty
  - [ ] loudness-normalisation = accessibility for quieter brain-injured users
- [ ] find the best HRI-relevant stuff to discuss

## Structure (5 minutes total)

### 0:00--0:30 -- Introduction (30 seconds)


- "This is GAZE: Game-Adaptive Zone of Engagement, an adaptive countdown-style game host integrated into the Pepper robot"
- One-sentence novelty: "The core novelty is multi-signal emotional inference -- the system weighs facial expression, response time, and answer correctness together, rather than trusting any single signal in isolation"
- Brief mention of your contribution split (general code architecture, OpenAI integration, facial recognition, AdaptiveEngine, Background/Method/Conclusion sections)

### 0:30--1:30 -- Architecture Walkthrough (60 seconds)

- Show the system diagram (SYSTEM-DIAGRAM.png or the TikZ version)
- Walk through the four layers: INPUT, PROCESS, GENERATE, OUTPUT
- Mention the SSH architecture: "The system runs on my laptop; Pepper is controlled via SSH. Two connections: one for motors and camera, one for speech, so gestures and speech can run in parallel"
- Mention the WS-10 integration: "Facial expression detection uses the pre-trained CNN from Workshop 10 -- same 48x48 greyscale pipeline, same 7 emotion classes"
- Show the multi-signal inference diagram (the TikZ from the report)

### 1:30--4:00 -- Live Demo on Pepper (150 seconds)

This is the core. Film the following interaction sequence:

**Startup sequence (show):**
- [ ] GAZE connects to Pepper ("Connected")
- [ ] Ambient noise calibration ("Stay quiet for 3 seconds...")
- [ ] Pepper waves, asks game preference ("Numbers or letters?")
- [ ] User says "Numbers"
- [ ] First question generated and spoken with gesture

**Normal gameplay (2-3 rounds showing adaptation):**
- [ ] Answer a question correctly -- show Pepper celebrate, show console output: "Inferred state: comfortable", difficulty stays or ramps
- [ ] Answer a question correctly again -- show streak recognition ("Hat trick!"), show LED colour change to green (thriving)
- [ ] Deliberately answer wrong or stay silent -- show console: "Inferred state: struggling", difficulty drops, hint offered, LED changes to yellow
- [ ] Stay silent again -- show disengagement detection, game switch from numbers to letters

**Key things to narrate during the demo:**
- Point out the console output showing the three raw signals (expression, response time, correctness) and the inferred state
- Point out when the engine overrides the camera reading (e.g. "The camera says Angry but I answered fast and correctly, so the engine correctly infers Comfortable")
- Point out the dynamic prompt changing ("Each round the prompt is freshly assembled from live metrics")
- Point out the gesture running concurrently with speech
- Point out LED colour changes matching inferred state

### 4:00--4:30 -- Session Summary (30 seconds)

- Say "goodbye" or "stop" to end the session
- Show the session summary printed in the console (rounds, accuracy, best streak, game switches)
- Show gaze_save.json being written (progressive save)
- Briefly mention session resumption: "If I restart, Pepper asks if I want to continue where I left off"

### 4:30--5:00 -- Reflection and Novelty (30 seconds)

- Reiterate the core novelty: "The system doesn't just trust the camera. If I look angry but I'm answering quickly and correctly, it knows I'm fine. That's the multi-signal fusion."
- Mention the adaptation self-evaluation: "After each round the engine evaluates whether its previous adaptation actually worked, and feeds that evaluation back into the next prompt"
- One-sentence limitation: "The facial expression model wasn't fine-tuned for this specific environment, so confidence scores can be low under poor lighting"
- Close

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
