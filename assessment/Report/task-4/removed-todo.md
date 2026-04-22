  ⎿  Added 11 lines, removed 46 lines
    1  """
    2  GAZE: Game-Adaptive Zone of Engagement
    3
    4 -Adaptive countdown-style game host ran on Pepper robot.
    5 -Novelty: multi-signal emotional inference: face (WS-10) + voice (WS-08) + resp
    -onse time
    6 -+ answer correctness, ... cross-validated so no single signal is trusted alone
    -.
    4 +Adaptive countdown-style game host on Pepper robot.
    5 +Novelty: multi-signal emotional inference -- face (WS-10) + voice (WS-08)
    6 ++ response time + answer correctness, cross-validated so no single
    7 +signal is trusted alone.
    8
    9 +Authorship (per proposal.pdf):
    10 +  Alfie  -- code architecture, OpenAI integration, facial recognition, Adaptiv
         +eEngine
    11 +  Salman -- game logic, gestures, LEDs, TTS pacing, session save/resume
    12
    9 -
    13  CRITICAL:
      11 --**REMEMBER: PROPOSAL.PDF IS SOURCE OF TRUTH FOR THE INITIAL-INTENDED DESIGN
         -AND FEATURES OF THE CODE.**
    12 --**REMEMBER: CONFIG NAO IP INTO ENV LIKE LAST TIME**
    13 -- [ ] only make listen when 'Pepper' is heard and hopefully this fix the Whisp
         -er hallucinations -`transcribe()` with Vosk wake-word gate + `                     14 +- **PROPOSAL.PDF IS SOURCE OF TRUTH FOR THE INITIAL-INTENDED DESIGN**                15 +- **CONFIG NAO IP INTO ENV LIKE LAST TIME**                                          16         15 -                                                                                     16 -                                                                                     17 +OPEN TODOs:                                                                          18 +- [ ] only make listen when 'Pepper' is heard and hopefully this fix the Whisp          +er hallucinations -`transcribe()`with Vosk wake-word gate +`
    19  - [ ] offload simpler tasks? to either computation or mini model
      20  - [ ] ensure all facial expression inference is sufficently commented
      19 -
    20 -FIXES TODO:
    21 -
    21  - [ ] ensure it notices and mitigates when user's disengaged
      23 -
    24 -Alfie's:
    25 ----------
    26 -- [X] adaptive/chosen difficulties, hints, encouragement, game switching {Adap
         -tiveEngine.decide()`(returns`AdaptiveDecision `)}                                   27 -- [X] user-volume indicate emotional signals {`measure_volume()`; `local_calib
         -rate_ambient()`(sets`VOLUME_QUIET `/`VOLUME_LOUD `)}                                 28 -- [X] adaptive-chosen words or numbers based on inferred user state somehow???          -: `generate_game_question_internal()`+`build_signal_context()`                    29 -- [X] WS-10 CNN facial-expression detection (7-class, 48x48 greyscale):`Facia
         -lExpressionModel.predict()`; `capture_and_classify()`                               30 -- [X] WS-08 MLP speech-emotion recognition (MFCC/chroma/mel features):`Speech
         -EmotionModel.predict()`; `classify_speech_emotion()`                                31 -- [X] countdown-like games (numbers/letters):`GameType `enum;`generate_game_
         -question_internal()`                                                                32 -- [X] multi-signal state inference (face + voice + time + correctness):`Adapt
         -iveEngine.infer_state()`                                                            33 -- [X] adaptation self-evaluation (did the previous adaptation help?):`Adaptiv
         -eEngine.evaluate_adaptation()`                                                      34 -- [X] local testing mode (GAZE_LOCAL_MODE):`local_record()`; `local_say()`; `
         -local_calibrate_ambient()`                                                          35 -- [X] dynamic LLM game generation & answer verification (OpenAI/GPT):`generat
         -e_game_question_internal()`; `check_answer()`                                       36 -- [X] signal-driven think-time budget: new`AdaptiveEngine.recommend_think_bud
         -get()`reading silence, response time, facial expression, inferred state, and           -the`waiting `flag (NOT trigger phrases); updates`engine.think_budget_secs `/          -`engine.silence_tolerance_secs `each round                                          37 -- [X]`request_more_time ` (`execute_tool_call()`) becomes one signal among man          -y rather than the sole path: sets `game_state.waiting = True `which feeds`rec
         -ommend_think_budget()`; never bumps the budget directly                              38 -- [X] inject `Think budget: Xs `into`build_signal_context()`so the LLM's dia          -logue reflects the belief without being told to                                      39 -- [X] 500 ms (0.5s) TTS-tail flush before mic open:`time.sleep(0.5)`at end o          -f`say()`; stops mic capturing Pepper's previous utterance and mis-firing the           -wake-word gate                                                                       40 -                                                                                     41 -Salman's:                                                                            42 ----------                                                                            43 -- [X] scoring, reward milestones, session save/resume — `AdaptiveEngine.check_
         -reward()`; `save_session()`; `load_session()`; `restore_engine()`                   44 -- [X] gestures, LEDs, and speech aligned to inferred state —`nao_gesture()`;           -`nao_set_leds()`; `extract_gesture()`; `LED_COLOURS `map                             45 -- [X] whisper transcription with network timeout fallbacks —`transcribe()`         46 -- [X] ambient noise calibration & dynamic silence detection —`nao_calibrate_a
         -mbient()`; `local_calibrate_ambient()`; `record()`/`local_record()`silence lo          -op                                                                                   47 -- [X] natural TTS sentence-level pacing —`split_into_sentences()`; `nao_say()
         -`; `nao_say_animated()`                                                             48 -- [X] stop the main dashboard leaking the correct answer — remove`_answer_var
         -`label from`GazeDashboard.__init__()`TRANSCRIPTION block; terminal`print(f
         -"(Game answer: ...")`stays for the observer                                         49 -- [X] plumb the budget through recording —`record()`/`local_record()`/`na
         -o_record()`take`no_speech_max `, `silence_secs `params so the recorder's`LOC
         -AL_NO_SPEECH_MAX `/`LOCAL_SILENCE_SECS `/`SILENCE_DURATION `adapt per-round        50 -- [X] dashboard diagnostic "Think budget" row in`GazeDashboard`'s LIVE SIGNAL
         -S — lets the observer watch the belief shift
    51 -
    52 -NICE-TO-HAVE:
    53 -- [ ] make web-search capabilities
    54 -- [ ] make vision-driven capabilities
    55 -- [ ] capability to fetch time and date if the AI determines its useful, encod
         -e this ability into system prompt
    56 -
    22  """
      23
    24  # standard library
