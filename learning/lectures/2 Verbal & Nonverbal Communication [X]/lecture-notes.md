Here is a structured, rigorous synthesis of the lecture material, corrected for technical accuracy (e.g., correcting "Henry Markov" to Hidden Markov Models and "Nano paper" to Nao and Pepper) and aligned with Dr. Aly’s conventions.
This is written to the standard of a First-Class set of notes: critical, technical, and derived from first principles.
Lecture Synthesis: Verbal and Non-Verbal Communication in HRI
1. The Fundamental Dichotomy of Communication
Communication regarded as the transfer of information is not merely the exchange of data strings; it is a complex social interplay involving both Verbal (linguistic) and Non-Verbal (paralinguistic/behavioural) cues.
The lecture posits a critical statistic regarding human interaction: 65% of communication is non-verbal.
 * Implication for HRI: A robot focusing solely on Natural Language Processing (NLP) misses the majority of social signals (intent, emotion, engagement). To achieve genuine social presence, a robot must possess multimodal perception capabilities.
The Categories
 * Verbal: Spoken language (oral) and Written text.
 * Non-Verbal: Facial expressions, gestures, postures, haptics (touch), and eye gaze.
2. Non-Verbal Communication: The Hidden Channel
Eye Gaze and Joint Attention
Eye gaze is not merely a sensor input; it is a mechanism for social state inference. In HRI, gaze serves three distinct functions:
 * Intent Inference: Determining the user's object of interest.
 * Social Management: regulating turn-taking in conversation (e.g., looking at a specific person to yield the floor).
 * Joint Attention: The shared focus of two individuals on an object.
> Critical Analysis: A robot with static eyes (like the standard Pepper model) suffers from a "gaze deficit." It cannot indicate attention direction without moving its entire head (using neck actuators). Conversely, robots with animated eyes (projections or LCDs) or actuated eyeballs (like the iCub) can simulate saccadic movements, thereby increasing perceived intelligence and social agency.
> 
Facial Expressions and FACS
To mathematically quantify emotion, we utilise the Facial Action Coding System (FACS).
 * Principle: Emotions are decomposed into specific muscular movements called Action Units (AUs).
 * Application: For a robot to display credible sadness, it is not enough to simply "look sad"; it must manipulate specific control points (actuators or virtual vertices) corresponding to the brow (Corrugator supercilii) and mouth corners (Zygomatic major), matching the biological reality of human expression.
3. Verbal Communication: Physics and Processing
Verbal communication comprises Utterances (the smallest unit of spoken language). To understand how a robot processes this, we must deconstruct speech into its physical components.
The Anatomy of Speech
 * Phonemes: The smallest unit of sound that distinguishes meaning (e.g., the difference between 'P' and 'B').
 * Words: Aggregations of phonemes.
 * Pauses: Silence between words (zero energy).
 * Fillers: Sounds like "um" or "uh."
   * Note: Fillers are not noise; they are conversational signals indicating that the speaker has not relinquished their turn but is processing information. A robust HRI system must distinguish a filler from a terminal pause to avoid interrupting the user.
Prosody
Prosody refers to the tonal features of speech (pitch, loudness, tempo).
 * Significance: The sentence "I am angry" carries different semantic weights depending on the prosody.
 * Machine Learning Task: We treat prosody as a vectorisation problem. We extract features (descriptors) from the audio signal to classify the emotional state (e.g., sad vs. neutral) alongside the textual content.
4. Signal Processing from First Principles
To enable a robot to "hear," we must convert physical sound waves into digital understanding.
Time Domain vs. Frequency Domain
Raw audio is captured in the Time Domain (Amplitude vs. Time). However, this is computationally inefficient for pattern recognition. We transform this data into the Frequency Domain (often using Fourier Transforms) to generate a Spectrogram.
 * Voiced Segments: Created when vocal cords vibrate (e.g., vowels, 'z', 'd'). These appear as high-energy, structured patterns (formants) in the frequency domain.
 * Unvoiced Segments: Produced without vocal cord vibration (e.g., 's', 'f', 'p'). These appear as stochastic noise or high-frequency bursts.
 * Silence: Absence of signal.
Why Frequency Domain?
In the frequency domain, phonemes exhibit distinct spectral signatures (shapes) that remain relatively consistent regardless of volume. This makes feature extraction for Machine Learning models (such as Hidden Markov Models or Gaussian Mixture Models) significantly more robust than analyzing raw amplitude spikes.
5. Challenges in Real-World HRI
The transition from "Lab" to "Wild" introduces variables that degrade recognition accuracy:
 * The Signal-to-Noise Ratio (SNR): Lab environments are pristine. Real environments have background noise. If the microphone is far from the speaker (a problem with mobile robots), the SNR drops, blending the user's voice with environmental noise.
 * Demographic Variance:
   * Elderly Users: Speech is often spontaneous, less articulated, and slower. Models trained on standard datasets (often younger adults reading scripts) fail to generalise to these irregular patterns.
   * Dialects: A model trained on Received Pronunciation (Standard British) may fail to process Scottish or regional dialects due to shifts in phoneme pronunciation.
Critical Synthesis (The "First Class" Argument)
To achieve excellence in this module, one must argue that embodiment dictates communication capability.
A robot is merely a "container" for AI. However, the physical hardware constrains the interaction. A robot like Kaspar (University of Hertfordshire) or iCub has complex facial actuators, allowing for high-fidelity FACS implementation. In contrast, Nao or Pepper rely on static faces. Therefore, if the hardware lacks facial bandwidth, the software must over-compensate using other channels (e.g., exaggerated gestures or coloured LEDs) to convey the missing 65% of non-verbal information.
The integration of Machine Learning is the bridge. We do not hard-code rules; we extract descriptors from gaze, speech, and tone, feeding them into classifiers that allow the robot to probabilistically infer the human's state.
Next Step for Excellence
You have a workshop coming up regarding speech signal analysis. I strongly recommend we create a LaTeX diagram illustrating the signal processing pipeline (Microphone \to FFT \to Spectrogram \to Feature Extraction \to Classification).
Would you like me to generate the TikZ code for that pipeline now to ensure you understand the flow "under the hood"?
