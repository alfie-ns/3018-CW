Here is the Comprehensive Intelligence Dossier for Lecture 3 (Affective Computing), processed via the British AI Lecture Intelligence System (v3.0). This document captures the lecturer’s exact requirements, strategic hints, and intellectual framework, prioritising the elements required for high-band marks.
COMP3018/5018: INTELLIGENCE DOSSIER – LECTURE 3 (AFFECTIVE COMPUTING)
1. CRITICAL ASSESSMENT INTELLIGENCE [HIGHEST PRIORITY]
Direct Coursework Directives (The "Reviewer Lens")
The lecturer provided extremely specific instructions for the Reading Critique coursework (Assessment 1, Task 1/2 or Master's specific task depending on your stream). Failure to adopt this specific "persona" will result in lost marks.
 * The "Reviewer" Persona: You must not write as a student; you must write as a peer reviewer deciding the fate of a paper.
   * Quote: "Imagine yourself a reviewer... read it with the eye from the lens of review. It's not a reader, reviewer. So imagine yourself a reviewer who should say the paper accept or not to accept."
   * Action: Your critique must conclude or imply a decision: is this work valid enough to be published?
 * The "Anti-Summary" Rule: Do not simply summarise the paper.
   * Quote: "It’s not a writing thing... This is a critique. So you have to make critique about the X paper or Y papers... put your hand on those limitations."
 * Selection Strategy:
   * Quote: "Choose a paper that you can find critics about... questions or points of confusion about the paper."
   * Hint: Do not pick a "perfect" paper. Pick one where you can identify flaws in methodology or logic.
Programming Project Implications (Task 4)
The lecturer explicitly linked the workshop content (Facial Expression Recognition) to the practical work.
 * Novelty Requirement: The project requires a "novel intellectual contribution".
 * Implementation Hint: The lecturer suggests that using pre-existing descriptors (libraries) is the modern standard, rather than calculating raw features manually.
   * Quote: "Now you have already some nice people who created descriptor ready that encapsulate all this. So simply speaking, you import this from Python library and just automatically and you have the descriptor ready to go."
2. THE COMPLETE 'ALPHA' BRIEF: STRATEGIC DIRECTIVES
⭐⭐⭐ Top Priority: Employ "Machine Learning Language"
The lecturer explicitly stated that using specific terminology is a marker of competence and employability. Using these terms in your report/presentation will signal "First-Class" understanding.
 * "Inferred": Never say you "see" emotion. You infer it.
   * Quote: "Get familiar to the word inferred. Inferred is like something or something intrinsically unobservable... That's why I infer it through your facial expressions."
 * "Descriptor": Do not say "features" or "variables" when describing the input. Use "Descriptor."
   * Quote: "I'm always encouraging you to use these words because these words say, if I hear these words, if I'm interviewing you for a job... I will understand that this guy Is speaking machine language machine learning... Descriptor in machine learning language."
 * "Characteristic Vector": The mathematical container for your features.
   * Quote: "What do we give to machine lear to machine learning model? Characteristic vector."
⭐⭐ High Priority: Conceptual Pitfalls (Warnings)
 * The "Basic Emotion" Trap: Do not treat emotions as static, isolated events (like Ekman's model). Acknowledging they are "composite" and "time-dependent" shows higher-level analysis.
   * Quote: "This is a really critic that emotions are not basic emotions separately existing emotions are something more composite. So we can have emotions that evolve with time."
 * The "Machine Intelligence" Distinction:
   * Quote: "The question is not whether intelligent machines can have any emotions, but whether machines can be intelligent without any emotions." (Quoting Minsky).
   * Insight: A robot does not need to feel sad to be effective; it needs to recognise sadness and simulate an appropriate response.
⭐ Technical Focus: Audio vs. Visual
 * Audio Pitch Tracking: Understand that this is done in the Frequency Domain, not the Time Domain.
   * Quote: "Calculating pitch frequency in frequency domain is easier for recognizing speech than time domain... frequency demand is more stable."
3. EXHAUSTIVE TOPIC BREAKDOWN
A. Affective Computing (Definition)
 * Lecturer’s Definition: "Effective computing is a computing or computational models that are related to emotional intelligence... a subset of artificial intelligence that measures, understands, simulates and reacts to human emotions."
 * Alternative Name: "Artificial Emotional Intelligence."
 * Core Mechanism: Using awareness of emotions to manage relationships.
B. Models of Emotion (The Theoretical Framework)
The lecturer contrasted three specific models. Understanding the evolution from simple to complex is key.
1. Ekman’s Model (The "Old" Standard)
 * Concept: Seven basic emotions: Anger, Surprise, Disgust, Enjoyment, Fear, Sadness, Contempt.
 * Lecturer’s Critique: "This is very not recent thing... emotions are not basic emotions separately existing."
2. Plutchik’s Wheel (The "Composite" Model)
 * Concept: 8 primary emotions.
 * Key Innovation: Emotions can combine.
 * Formulae (Must Memorise for Report Theory):
   * Primary + Primary = Secondary (e.g., Joy + Trust = Love).
   * Primary + Adjacent Branch = Secondary.
 * Intensity: The wheel accounts for intensity (e.g., Rage > Anger).
3. Russell’s Circumplex Model (The "Dimensional" Model)
 * Concept: Emotions are not lists; they are coordinates on a 2D axis.
 * Dimensions:
   * Hedonic: Pleasure vs. Displeasure (Pleasant/Unpleasant).
   * Arousal: Activation vs. Deactivation (Alert/Calm).
 * Example: "Between surprise and happiness... start by being alert, excited, elated, happy."
C. Speech Emotion Recognition (Audio Pipeline)
This section contained the highest density of technical terminology.
The Pipeline:
Signal Acquisition \rightarrow Signal Processing \rightarrow Feature Extraction \rightarrow Classification.
Key Descriptors (Technical features to reference in reports):
 * Fundamental Frequency (F_0):
   * Significance: Identity cue.
   * Data: Men \approx 100Hz, Women \approx 200Hz, Children \approx 300Hz, Crying Babies \approx 500Hz.
   * Algorithm: YAAPT (Yet Another Algorithm for Pitch Tracking). Quote: "You might find yet strange here, but it's called yapt."
 * MFCC (Mel-Frequency Cepstral Coefficients):
   * Definition: Describes the "overall shape of spectral envelope".
   * Process: Log of frequency spectrum \rightarrow Cosine transform.
 * Zero Crossing Rate (ZCR):
   * Definition: How often the signal crosses the horizontal axis (positive to negative).
   * Application: "When you are angry, your intensity goes high... Spoke so fast... The frequency of the zero crossing points in one emotion is different."
 * Voicing Probability (VP):
   * Definition: Distinction between voiced (vocal cords vibrate, e.g., vowels) and unvoiced (e.g., 'P', 'S') sounds.
D. Facial Expression Recognition (Visual Pipeline)
The Pipeline:
Extract Face (Background Removal) \rightarrow Facial Geometry Estimation \rightarrow Normalisation \rightarrow Classification.
 * Mechanism: Using "Marker Points" (eyes, eyebrows, nose, mouth).
 * Why Normalisation? To remove the impact of head rotations (XYZ axis).
 * Training: Requires a dataset (e.g., sad faces vs. happy faces) to train the model to recognise the geometric configuration of the points.
4. LECTURER’S LEXICON (Terminology Database)
| Term | Lecturer's Definition/Context | Notes |
|---|---|---|
| Inferred | "Something intrinsically unobservable... I cannot see your emotion... I infer it." | Essential for theoretical discussions. |
| Descriptor | "The words that represent the features of a shape or color." | Use this instead of "features" to impress. |
| Characteristic Vector | "You take the features, you put them in a vector... this is what you give to the machine learning model." | Technical implementation term. |
| Multi-disseminated | Refers to the interdisciplinary nature (CS, Psychology, Cognitive Science). | Used to describe the field. |
| YAAPT | "Yet Another Algorithm for Pitch Tracking." | Specific algorithm mentioned for F_0. |
| Hedonic | The Pleasure-Displeasure dimension in Russell's model. | Theoretical term. |
5. COURSEWORK SUCCESS BLUEPRINT
For Task 1 (Cultural Factors) & Task 3 (Literature Review):
 * Use the "Evolution of Models" Narrative: When discussing how robots should perceive emotion, do not just list models. Argue that older models (Ekman) are limited because they lack the "time" variable, whereas Plutchik or Russell offer more "sophisticated" continuous dimensions suitable for dynamic HRI.
 * Integrate "Inference": When discussing how a robot perceives culture-specific cues, frame it as an inference problem—the robot cannot see the culture, it must infer it from observable descriptors (behaviour/appearance).
For Task 4 (Programming Project):
 * The "Novelty" Angle: If building an emotion recognition system, simply implementing a library isn't enough. The "Novel Intellectual Contribution" could be comparing how two different descriptors (e.g., MFCC vs. Pitch alone) affect the accuracy of detecting specific emotions (e.g., is Pitch better for Anger but MFCC better for Sadness?).
 * Validation: Use the "Reviewer Lens" on your own work. What are the limitations of your robot's emotion recognition? (e.g., "It fails when the user turns their head because I didn't normalize the facial geometry enough").
6. META-LEARNING INTELLIGENCE
 * Study Advice: The lecturer emphasizes that modern AI is about integration rather than building from scratch. You are expected to use libraries (Python) that have these descriptors ready-made.
   * Quote: "When I was young... I was calculating this alone... But now you have already some nice people who created descriptor ready."
 * Interactive Testing: The lecturer strongly encouraged testing the facial recognition model with your own laptop camera during the workshop.
   * Action: Do this. It provides the "running demo" required for Assessment 2, Task 4.
7. COMPUTATIONAL THINKING PATTERNS
The Lecturer’s Problem-Solving Protocol:
 * Identification: Isolate the signal (Face from background, Voice from silence).
 * Extraction: Identify the "Descriptor" (Geometric points for face, MFCC/Pitch for voice).
 * Vectorisation: Create the "Characteristic Vector."
 * Inference: Feed vector to ML model to classify the state (Happy/Sad).
 * Synthesis: Robot performs action based on class (e.g., "I am sorry you are sad").
Use this exact 5-step protocol in your "Method and Setup" section for the Programming Project Report.
