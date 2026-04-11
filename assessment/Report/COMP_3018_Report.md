---
title: "COMP3018: Report (Literature Review & Programming Project)"
subtitle: "Cognitive Robotics"
header-includes:
  - \usepackage{graphicx}
  - \usepackage{caption}
  - \usepackage{tikz}
  - \usetikzlibrary{positioning, arrows.meta}
  - \usepackage{xcolor}
  - \usepackage{float}
  - \usepackage{array}
  - \usepackage{tabularx}
  - \usepackage{mdframed}
  - \usepackage{booktabs}
  - \usepackage{pgfplots}
  - \pgfplotsset{compat=1.18}
  - \usepackage{listings}
  - \usepackage{hyperref}
  - \usepackage{multirow}
  - |
      \lstset{
        language=Python,
        numbers=left,
        breaklines=true,
        breakatwhitespace=true,
        postbreak=\mbox{\textcolor{gray}{$\hookrightarrow$}\space},
        basicstyle=\ttfamily\small,
        columns=flexible,
        escapeinside={(*@}{@*)},
        showstringspaces=false
      }
---
# TODO

- [ ] verify word count

### VERIFY PAGE NUMBERS (check each against the actual PDF)

#### Vernon, Metta and Sandini (2007) -- `papers/Vernon, Metta and Sandini (2007) - A Survey of Artificial Cognitive Systems.pdf`

| OK?   | Line(s)  | Section    | Citation as written           | Go to page... | You should see...                                                                                    |
| ----- | -------- | ---------- | ----------------------------- | ------------- | ---------------------------------------------------------------------------------------------------- |
| - [ ] | 298, 304 | S1.1, S1.2 | Vernon et al. (2007, p. TODO) | Try p. 155    | Section "What is Cognition?"; cognition cycle diagram (anticipate, learn, adapt + perception/action) |
| - [ ] | 306      | S1.2       | Vernon et al. (2007, p. TODO) | Try p. 163    | Memory section; episodic vs semantic memory distinction (Tulving's taxonomy)                         |

#### Sciutti et al. (2023) -- `papers/Sciutti et al. (2023) - The Present and the Future of Cognitive Robotics.pdf`

| OK?   | Line(s)            | Section   | Citation as written                                                                 | Go to page... | You should see...                                                                                                                 |
| ----- | ------------------ | --------- | ----------------------------------------------------------------------------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| - [ ] | 298, 304, 314, 509 | S1.1-S2.2 | Sciutti et al. (2023, p. 160)                                                       | p. 160        | "flexible, context-sensitive action, knowing what they are doing and why"; "reason about their actions and modify their behavior" |
| - [ ] | 302                | S1.2      | Sciutti et al. (2023, p. 160) -- "intersection of Robotics, AI, Cognitive Sciences" | p. 160        | CHECK: this exact phrase may NOT be here; may come from Sandini, Sciutti & Vernon (2021) encyclopaedia entry instead              |
| - [ ] | 350                | S1.5      | Sciutti et al. (2023, pp. 162-163)                                                  | pp. 162-163   | CHECK: "integrating machine learning techniques with model-based approaches" -- may only be on p. 162, not spanning 163           |

#### Tapus, Matarić and Scassellati (2007) -- `papers/Tapus, Matarić and Scassellati (2007) - Socially Assistive Robotics.pdf`

| OK?   | Line(s) | Section | Citation as written          | Go to page... | You should see...                                                     |
| ----- | ------- | ------- | ---------------------------- | ------------- | --------------------------------------------------------------------- |
| - [ ] | 312     | S1.3.1  | Tapus et al. (2007, p. TODO) | Try p. 35     | PARO listed: "robotic animal toys, such as a seal (i.e., PARO [2])"   |
| - [ ] | 509     | S2.2    | Tapus et al. (2007, p. 35)   | p. 35         | "helping human users through social rather than physical interaction" |

#### Wada and Shibata (2007) -- `papers/Wada and Shibata (2007) - Living With Seal Robots.pdf`

| OK?   | Line(s)  | Section        | Citation as written             | Go to page... | You should see...                                                                                  |
| ----- | -------- | -------------- | ------------------------------- | ------------- | -------------------------------------------------------------------------------------------------- |
| - [ ] | 312, 342 | S1.3.1, S1.4.2 | Wada and Shibata (2007, p. 974) | p. 974        | NEEDS MANUAL CHECK -- download PDF; look for PARO reducing agitation / mood improvement in elderly |

#### Fong, Nourbakhsh and Dautenhahn (2003) -- `papers/Fong, Nourbakhsh and Dautenhahn (2003) - A Survey of Socially Interactive Robots.pdf`

| OK?   | Line(s)  | Section      | Citation as written        | Go to page... | You should see...                                                                                                                                      |
| ----- | -------- | ------------ | -------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| - [ ] | 314      | S1.3.1       | Fong et al. (2003, p. 145) | p. 145        | Section 1.2; Breazeal's four classes of social robots; "shallow models of social cognition" under Social Interface                                     |
| - [ ] | 326      | S1.3.3       | Fong et al. (2003, p. 149) | p. 149        | Section 2.3 Embodiment; "mutual perturbation" / "perturbatory channels"                                                                                |
| - [ ] | 509, 538 | S2.2, S2.3.3 | Fong et al. (2003, p. 148) | p. 148        | CHECK: p. 148 covers design issues, NOT emotion recognition. Try p. 155 (human-oriented perception listing) or p. 156 (speech/facial emotion analysis) |

#### Lee and See (2004) -- `papers/Lee and See (2004) - Trust in Automation Designing for Appropriate Reliance.pdf`

| OK?   | Line(s) | Section | Citation as written       | Go to page... | You should see...                                                                                                                                         |
| ----- | ------- | ------- | ------------------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| - [ ] | 318     | S1.3.2  | Lee and See (2004, p. 54) | p. 54         | Definition in italics: "the attitude that an agent will help achieve an individual's goals in a situation characterized by uncertainty and vulnerability" |

#### Hancock et al. (2011) -- `papers/Hancock et al. (2011) - A Meta-Analysis of Factors Affecting Trust in Human-Robot Interaction.pdf`

| OK?   | Line(s)  | Section        | Citation as written                                                         | Go to page... | You should see...                                                                               |
| ----- | -------- | -------------- | --------------------------------------------------------------------------- | ------------- | ----------------------------------------------------------------------------------------------- |
| - [ ] | 320, 334 | S1.3.2, S1.4.1 | Hancock et al. (2011, p. 522) -- performance strongest predictor            | p. 522        | Table 1; "performance factors were more strongly associated (r = +0.34)"; Cohen's d = +0.71     |
| - [ ] | 318      | S1.3.2         | Hancock et al. (2011, p. 522) -- "observation cannot reliably disambiguate" | p. 522        | CHECK: this POMDP-style claim may NOT appear anywhere in Hancock et al.; possibly misattributed |
| - [ ] | 334      | S1.4.1         | Hancock et al. (2011, p. 522) -- "29 studies, modest variance"              | pp. 520-522   | 29 studies stated on p. 520; overall r = +0.26 on p. 521; paper uses "moderate" not "modest"    |

#### Chen et al. (2020) -- `papers/Chen et al. (2020) - Trust-Aware Decision Making for Human-Robot Collaboration.pdf`

| OK?   | Line(s) | Section | Citation as written      | Go to page...          | You should see...                                                                                                      |
| ----- | ------- | ------- | ------------------------ | ---------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| - [ ] | 320     | S1.3.2  | Chen et al. (2020, p. 6) | p. 6 (article page :6) | Section 3.4 "Maximizing team performance"; Fig. 3 (Trust-POMDP model); "We maintain a belief b over the human's trust" |

#### Garcez and Lamb (2023) -- `papers/Garcez and Lamb (2023) - Neurosymbolic AI The 3rd Wave.pdf`

| OK?   | Line(s)       | Section            | Citation as written              | Go to page...                                                                          | You should see...                                                                                                              |
| ----- | ------------- | ------------------ | -------------------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| - [ ] | 320, 511, 663 | S1.3.2, S2.2, S2.5 | Garcez and Lamb (2023, p. 12389) | Local PDF is arXiv preprint (pp. 1-28); p. 12389 = journal page 3 of published version | CHECK against published*AI Review* version (journal pp. 12387-12406). On ~p. 3: third wave / neural-symbolic labour division |

#### Nikolaidis, Hsu and Srinivasa (2017) -- `papers/Nikolaidis, Hsu and Srinivasa (2017) - Human-Robot Mutual Adaptation in Collaborative Tasks.pdf`

| OK?   | Line(s)  | Section        | Citation as written              | Go to page... | You should see...                                                                               |
| ----- | -------- | -------------- | -------------------------------- | ------------- | ----------------------------------------------------------------------------------------------- |
| - [ ] | 320, 624 | S1.3.2, S2.3.3 | Nikolaidis et al. (2017, p. 625) | p. 625        | "69 samples"; "U = 180, p = 0.048"; MOMDP mutual-adaptation condition                           |
| - [ ] | 334      | S1.4.1         | Nikolaidis et al. (2017, p. 627) | p. 627        | MOMDP discussion; r = -0.066 (no correlation between trustworthiness and inferred adaptability) |

#### Brooks (1991) -- `papers/Brooks (1991).pdf`

| OK?   | Line(s) | Section | Citation as written    | Go to page... | You should see...                                                                                                    |
| ----- | ------- | ------- | ---------------------- | ------------- | -------------------------------------------------------------------------------------------------------------------- |
| - [ ] | 326     | S1.3.3  | Brooks (1991, p. TODO) | ??            | NEEDS MANUAL CHECK -- find argument that intelligence emerges from physical interaction, not abstract representation |

#### Matarić et al. (2007) -- `papers/Mataric et al. (2007).pdf`

| OK?   | Line(s) | Section | Citation as written             | Go to page... | You should see...                                                                                           |
| ----- | ------- | ------- | ------------------------------- | ------------- | ----------------------------------------------------------------------------------------------------------- |
| - [ ] | 326     | S1.3.3  | Matarić et al. (2007, p. TODO) | ??            | NEEDS MANUAL CHECK -- find stroke survivors engaging more with embodied robot than screen-based alternative |

#### Tapus, Ţăpuş and Matarić (2008) -- `papers/Tapus, Tapus and Mataric (2008).pdf`

| OK?   | Line(s) | Section | Citation as written                          | Go to page... | You should see...                                                                                                |
| ----- | ------- | ------- | -------------------------------------------- | ------------- | ---------------------------------------------------------------------------------------------------------------- |
| - [ ] | 326     | S1.3.3  | Tapus, Ţăpuş and Matarić (2008, p. TODO) | ??            | NEEDS MANUAL CHECK -- find adaptive personality matching (interaction distance/speed) improving task performance |

#### Papadimitriou and Tsitsiklis (1987) -- `papers/Papadimitriou and Tsitsiklis (1987) - The Complexity of Markov Decision Processes.pdf`

| OK?   | Line(s) | Section | Citation as written                         | Go to page... | You should see...                                          |
| ----- | ------- | ------- | ------------------------------------------- | ------------- | ---------------------------------------------------------- |
| - [ ] | 332     | S1.4.1  | Papadimitriou and Tsitsiklis (1987, p. 448) | p. 448        | Theorem 6: "The partially observed problem is PSPACE-hard" |

#### Pineau, Gordon and Thrun (2003) -- `papers/Pineau, Gordon and Thrun (2003) - Point-Based Value Iteration An Anytime Algorithm for POMDPs.pdf`

| OK?   | Line(s) | Section | Citation as written           | Go to page... | You should see...                                                     |
| ----- | ------- | ------- | ----------------------------- | ------------- | --------------------------------------------------------------------- |
| - [ ] | 332     | S1.4.1  | Pineau et al. (2003, p. 1025) | p. 1025       | First page / abstract: "Point-Based Value Iteration (PBVI) algorithm" |

#### Kaelbling, Littman and Cassandra (1998) -- `papers/Kaelbling, Littman and Cassandra (1998) - Planning and Acting in Partially Observable Stochastic Domains.pdf`

| OK?   | Line(s)  | Section      | Citation as written             | Go to page... | You should see...                                                                                                                              |
| ----- | -------- | ------------ | ------------------------------- | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| - [ ] | 332, 663 | S1.4.1, S2.5 | Kaelbling et al. (1998, p. 120) | p. 120        | CHECK: p. 120 is the tiger problem (Section 5.1, toy example). For POMDP framework definition try p. 105; for belief-state planning try p. 108 |

#### Silver and Veness (2010) -- `papers/Silver and Veness (2010) - Monte-Carlo Planning in Large POMDPs.pdf`

| OK?   | Line(s) | Section | Citation as written            | Go to page... | You should see...                                                     |
| ----- | ------- | ------- | ------------------------------ | ------------- | --------------------------------------------------------------------- |
| - [ ] | 332     | S1.4.1  | Silver and Veness (2010, p. 1) | p. 1          | Abstract: "Monte-Carlo algorithm for online planning in large POMDPs" |

#### Broadbent, Stafford and MacDonald (2009) -- `papers/Broadbent et al. (2009).pdf`

| OK?   | Line(s) | Section | Citation as written              | Go to page... | You should see...                                                                                |
| ----- | ------- | ------- | -------------------------------- | ------------- | ------------------------------------------------------------------------------------------------ |
| - [ ] | 334     | S1.4.1  | Broadbent et al. (2009, p. TODO) | ??            | NEEDS MANUAL CHECK -- find acceptance depending on matching robot behaviour to user expectations |

#### Desai et al. (2013) -- `papers/Desai et al. (2013) - Impact of Robot Failures and Feedback on Real-Time Trust.pdf`

| OK?   | Line(s)  | Section        | Citation as written         | Go to page... | You should see...                                                                                                                                                        |
| ----- | -------- | -------------- | --------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| - [ ] | 334, 538 | S1.4.1, S2.3.3 | Desai et al. (2013, p. 256) | p. 256        | CHECK: local PDF is conference format with no printed page numbers. Verify against HRI 2013 proceedings. Look for: trust drops after reliability failures, slow recovery |

#### Wachter, Mittelstadt and Floridi (2017) -- `papers/Wachter, Mittelstadt and Floridi (2017) - Why a Right to Explanation Does Not Exist in the GDPR.pdf`

| OK?   | Line(s) | Section | Citation as written            | Go to page...                                     | You should see...                                                                                                        |
| ----- | ------- | ------- | ------------------------------ | ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| - [ ] | 340     | S1.4.2  | Wachter et al. (2017, p. TODO) | Try p. 76 (abstract) or p. 82 (Section 3 heading) | p. 76: "GDPR does not implement a right to explanation"; p. 82: Section heading "Why there is no 'right to explanation'" |

#### Sharkey (2014) -- `papers/Sharkey (2014) - Robots and Human Dignity.pdf`

| OK?   | Line(s) | Section | Citation as written           | Go to page...                   | You should see...                                                                                                                                             |
| ----- | ------- | ------- | ----------------------------- | ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| - [ ] | 342     | S1.4.2  | Sharkey (2014, p. 6 (VERIFY)) | Manuscript p. 6 = journal p. 68 | "a robot that dealt impersonally with an older person, without knowing or using their name or their preferences..." in Nordenfelt Dignity of Identity context |

#### Sharkey and Sharkey (2012) -- `papers/Sharkey and Sharkey (2012) - Granny and the Robots Ethical Issues in Robot Care for the Elderly.pdf`

| OK?   | Line(s) | Section | Citation as written               | Go to page... | You should see...                                                                               |
| ----- | ------- | ------- | --------------------------------- | ------------- | ----------------------------------------------------------------------------------------------- |
| - [ ] | 350     | S1.5    | Sharkey and Sharkey (2012, p. 27) | p. 27         | Abstract/introduction; concerns about reducing human contact. Detailed argument is on pp. 30-31 |

#### Ahn et al. (2022) -- `papers/Ahn et al. (2022) - Do As I Can Not As I Say Grounding Language in Robotic Affordances.pdf`

| OK?   | Line(s) | Section | Citation as written     | Go to page... | You should see...                                                                                                       |
| ----- | ------- | ------- | ----------------------- | ------------- | ----------------------------------------------------------------------------------------------------------------------- |
| - [ ] | 511     | S2.2    | Ahn et al. (2022, p. 1) | p. 1          | Abstract: "constrain the model to propose natural language actions that are both feasible and contextually appropriate" |

#### Smedegaard (2019) -- `papers/Smedegaard (2019) - Reframing the Role of Novelty within Social HRI from Noise to Information.pdf`

| OK?   | Line(s)  | Section    | Citation as written     | Go to page...               | You should see...                                                                                                                    |
| ----- | -------- | ---------- | ----------------------- | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| - [ ] | 511, 663 | S2.2, S2.5 | Smedegaard (2019, p. 4) | p. 4 (= proceedings p. 414) | Novelty as "original feature of experience". CHECK: the novelty-fading engagement claim may be stronger on p. 2 (proceedings p. 412) |

#### Ji et al. (2023) -- `papers/Ji et al. (2023) - Survey of Hallucination in Natural Language Generation.pdf`

| OK?   | Line(s) | Section | Citation as written    | Go to page... | You should see...                                                        |
| ----- | ------- | ------- | ---------------------- | ------------- | ------------------------------------------------------------------------ |
| - [ ] | 647     | S2.3.4  | Ji et al. (2023, p. 3) | p. 3          | "deep learning based generation is prone to hallucinate unintended text" |

---

- [ ] if enough time: ermengent cognitive robot architecture
- [ ] cite Iuliia Kotseruba1 · John K. Tsotsos1
- [ ] use 'inference' natrually, i.e., not so perfect that it is likely ai generated but instead slightly not 100% correct like a human would do, ygm?

## Mentor

Scenario 1) patient takes meds = + 100 points
Scenario 2) Patient is annoyed = -10 points
When you implement tis you need to be careful to structure the rewards such that the system does not pester the patient as it seeks to maximise it's rewards
You'll need to play around with the precise ratios between 1 (behaviour you want to encourage) and 2 (behaviour you want to discourage) to achieve the desired attitude from the robot

## DR ALY QUESTIONS:

- [ ] so maths and code won't affect word count right? However I never explcitly knew if captions within a figure-diagram count towards word count?

---

## First-to-do:

- [ ] **Most critical:** verify all page numbers and sentences manually
- [ ] **Most critical:** verify all links to papers manually
- [ ] do all page number TODOs
- [ ] implement loads of peer-reviewed papers everywhere again

## General:

- [ ] ensure no overused complex words
- [ ] Download Broadbent via Plymouth library
- [ ] Run past Gemini
- [ ] decides the reward based on what it oberserves = inferring the reward
- [ ] discuss POMDP maths
- [ ] use wording from 3018 Task-4 Proposal Google Doc
- [ ] talk about the LfD (learning-from-demonstration)
- [ ] talk about IRL (inverse reinforcement learning)
- [ ] relatively talk about how it relates to others, motivation
- [ ] CRAMS figure verified -- 5/6 actions appear (Back_Off absent because true state never sustained Low Trust long enough). Update report Task 4 discussion to: 1) explain why the action timeline shows context-sensitive selection (link each action cluster to the reward territory that produced it), 2) note Back_Off correctly absent given the Medium-trust initial state and stress profile, 3) highlight META-ADAPT triggers (red dotted lines) as evidence of metacognition detecting the stress event within 2 steps
- [X] USE ‘misclassified’
- [ ] consider a project wherein it is ‘cogntive robotics’ (lecture 9) ensure it involves what we have learnt in the labs
- [ ] write code like lecturer in: `3018-cw/learning/workshops/[X] emotional-speech-recognition/solution.py`
- [ ] ‘persons’
- [ ] make the robot kinda like how I disucssed you should make it in the set exercises
- [ ] discuss mathematical notiation for the POMDP stuff??? (if not done in set exercises)

  - [ ] maths and diagrams affect wordcount?
  - [ ] Trust-POMPDP diagram
  - [X] Cite: Chen, M., Nikolaidis, S., Soh, H., et al., “Trust-Aware Decision Making for Human-Robot Collaboration: Model Learning and Planning”, ACM Trans. Hum.-Robot Interact., 9(2), 2020
  - [ ] model trust in lates diabram? or     just latex the fundamental diagtam of       POMDP similar to lecture slied in POMDP     lectures (10,11)
  - [ ] latex diagram of continous state in POMDP similar to non-monotnoric graph (not about non-monitonic itsekf just a similar graph)
  - [ ] utilise lec-7 for POMDP insights; similar to machine learning set exercises where i give a quick breakdown if word count allowance
- [ ] args and kwargs (if i can do this)
- [X] peer-reviewed or conference papers
- [ ] In this section, you should focus on providing enough description of the supervised learning, neural network, and naïve Bayes models.
- [ ] Do not assume the reader knows the basics. Dedicate specific paragraphs to explicitly defining the algorithms and the broader category (Supervised Learning) before diving into your implementation.
- [ ] Then, refer to some studies that have utilised neural networks and naïve Bayes models in your area using the selected database
- [ ] Ensure your literature review in the introduction explicitly cites papers that use your specific dataset (or very similar ones), establishing a clear baseline before you begin
- [ ] TODO: talk about the LfD (learn-from-demonstration)

  - [ ] TODO: talk about IRL (inverse reinforcement learning)
- [ ] TODO: talk about the LfD (learn-from-demonstration)

  - [ ] TODO: talk about IRL (inverse reinforcement learning)

LECTURE 9 – TODOs FOR ASSESSMENT 2 REPORT
Task 3: Literature Review (Assistive Robotics Essay):
	- [X] Frame assistive robotics as requiring cognitive capabilities, not just social behaviour – use Aly’s hierarchy: “intelligence deployed over the social layer, not vice versa”
	- [X] Reference Sciutti et al. (2023) definition of cognitive robotics (replaced Cangelosi book -- not peer-reviewed)
	- [X] Use Vernon, Metta and Sandini (2007) cognition cycle (replaced Vernon 2014 book -- not peer-reviewed)
	- [X] Discuss theory of mind, prospection, and episodic memory as future directions/current gaps in assistive robotics
	- [X] Acknowledge the 42-definitions problem to argue the field still lacks consensus on what cognition actually is (shows critical thinking)
	- [X] Connect embodied cognition (“intelligence means body”) to ethical implications of robots entering intimate care spaces
Task 4: Programming Project
	- [ ]	GET APPROVAL FROM ALY – confirm extending set exercises POMDP into cognitive architecture implementation is acceptable; confirm simulation-only is fine
	- [ ]	Wait for Lectures 10/11 on cognitive architectures before finalising design – Aly said the building blocks reappear in those lectures
	- [ ]	Explicitly map every system component to Aly’s cognitive building blocks (perception, attention, action selection, memory, learning, reasoning, metacognition, prospection)
	- [ ]	Add metacognition module (new from this lecture) – system monitors its own reasoning, flags when repeated actions produce negative outcomes
	- [ ]	Implement explicit episodic vs semantic memory distinction – Aly specifically said “please distinguish or remember these two”
	- [ ]	Label trust inference as theory of mind explicitly
	- [ ]	Label POMDP planning over future states as prospection explicitly
	- [ ]	Label observation filtering as attention (selective/suppressive)
	- [ ]	Frame all actions as goal-directed (Aly’s term for purposeful cognitive actions vs reactive behaviour)
	- [ ]	Include cognitive architecture diagram in report showing how building blocks interconnect
	- [ ]	Use the term “cognitive architecture” – Aly defined this as the system that “puts all these basic building blocks together and supports the communications between all”
	- [ ]	Frame project as cognitive robotics (not just social robotics) – Aly said nobody has ever done this; “invitation for challenging minds”
	- [ ]	Don’t skip definitional rigour – define cognitive robotics, cognition, and key terms precisely in the Background section
	- [ ]	5-min video: walk through a scenario showing perceive -> attend -> reason -> act -> learn -> adapt cycle in action

Cross-check with Gemini.

# 1- Task (3) Literature Review

- [X] [X] ## 1.1. Introduction

Ageing populations and a shrinking care workforce positioned **assistive robotics** *(human-supportive robots within physical, cognitive, and social realms of impairment affecting daily-living activities)*; a prominent technological response to a widening care gap. The field spans physical prosthetics; surgical assistance; neurodivergent support; exoskeletal rehabilitation, and social companionship; this essay however focuses on *socially* assistive robotics ($SAR$), an assistive-robot subfield wherein the robot "focuses on helping human users through social rather than physical interaction" (Tapus, Matarić and Scassellati, 2007, Abstract), as here most active research and ethical tension converge.

Robots now administer medication reminders, facilitate rehabilitation exercises, and therapeutically companionate in clinical and domestic settings: reduced caregiver burden, improved patient outcomes wherein residents became "more active and more communicative, both with each other and their caregivers" (Wada and Shibata, 2007, p. 973), and increased "social interaction" among elderly residents (Wada and Shibata, 2007, p. 972, Abstract).

However, most-current assistive robots operate at what Sciutti et al. (2023, p. 160) call the social layer: they react to immediate stimuli but lack the cognitive depth to anticipate user needs, remember past interactions, or reason about their own performance. Sciutti et al. argue that effective assistive robots should be *cognitive*: capable of "flexible, context-sensitive action, knowing what they are doing and why they are doing it." Vernon, Metta and Sandini (2007, p. 151) formalise this requirement via a "virtuous cycle that is embedded in an ongoing process of action and perception" (the agent anticipates $\to$ learns $\to$ adapts to achieve autonomy). This essay contends that assistive robotics should graduate from reactive social behaviour to cognitive capability (intelligence deployed *over* the social layer) if it is to deliver sustained, personalised support. The following sections survey the theoretical foundations thereof: evaluate prominent applications through this cognitive lens, discuss challenges and ethical implications, and identify future directions.

- [ ] ## 1.2. Literature Review

*Cognitive robotics:* defined by Sciutti et al. (2023, p. 160), lies at the intersection of Robotics, Artificial Intelligence, and Cognitive and Biological Sciences, combining "sensorimotor behaviour, higher-level functions, and social capabilities of an intelligent robot." This interdisciplinary grounding distinguishes it from conventional robotics *(treats the robot as purely engineered)* and from social robotics *(addresses interaction behaviour without necessarily modelling cognitive processes)*. The distinction is consequential: a robot that smiles when a patient smiles is social; a robot that infers *why* the patient is smiling, and adjusts its future strategy accordingly, is thus *cognitive*.

- [ ] verify following lecture slides

Vernon, Metta and Sandini (2007, p. TODO) synthesise the field's definitional plurality into a core cycle. The European Network for Advancement of Artificial Cognitive Systems (euCognition) catalogued 42 definitions of cognition, yet the common thread therein is: anticipation, learning, and adaptation, intersected with perception and action to create autonomy. This cycle provides an architectural checklist for assistive robots: a system that cannot direct its gaze toward relevant stimuli whilst suppressing irrelevant ones *(selective attention)*, anticipate the outcome of its actions *(prospection)*, learn from past interactions *(memory)*, or adapt its strategy when performance declines *(metacognition)* is, per this framework, not yet cognitive. Sciutti et al. (2023, TODO: verify p. 160) further specify that cognitive robots should "reason about their actions and modify their behavior to improve their effectiveness"; a capacity termed *theory of mind*, wherein the agent infers another's hidden mental state from observable behaviour.

Furthermore, memory is not monolithic. Vernon, Metta and Sandini (2007, p. TODO) distinguish *episodic memory* *(records of specific past experiences and their contextual outcomes)* from *semantic memory* *(general knowledge about the world, including spatial relationships and factual constraints)*. For example, assistive-medication robots need episodic memory to recall that a user refused medication after a restless night, and semantic memory to know certain drugs cannot also be administered. Whilst the 42-definitions problem confirms the field lacks consensus on what cognition per se *is*, the common thread (anticipation, learning, adaptation) is precisely what assistive robotics demands.

- [ ] ## 1.3. Applications

### 1.3.1 Therapeutic and Emotional Support

The PARO therapeutic seal robot represents one of the most-widely deployed platforms within socially assistive robotics (Tapus, Matarić and Scassellati, 2007, p. TODO). Wada and Shibata (2007, p. 974) demonstrate that PARO reduces agitation and improves mood in patients with dementia, utilising tactile sensors and auditory processing to modulate its behaviour in response to touch and voice. Clinical trials report that urinary stress indicators "significantly improved" after PARO's introduction (Wada and Shibata, 2007, p. 978, Table II), thus the platform has been adopted in care homes across Japan, Europe, and the United States.

Notwithstanding these benefits, PARO operates at the reactive layer. It possesses no theory of mind (it cannot infer *why* a patient is agitated: loneliness, pain, confusion) nor episodic memory of what calmed this patient previously. A cognitively-equipped therapeutic robot, by contrast, would anticipate mood shifts via prospection, recall that music soothed this patient yesterday via episodic memory, and adapt its strategy via metacognition. Insofar as PARO's effectiveness plateaus because it cannot personalise its responses over time, the cognitive gap is not merely theoretical but potentially clinically consequential. Fong, Nourbakhsh and Dautenhahn (2003, p. 145) formalise this gap via Breazeal's taxonomy: PARO occupies the 'social interface' level (human-like cues but "shallow models of social cognition"), whereas Sciutti et al.'s (2023, p. 160) vision of robots "knowing what they are doing and why" demands the 'socially intelligent' level. The distance between these levels is the cognitive deficit assistive robotics should close.

### 1.3.2 Medication Adherence and Daily Living Support

Medication non-adherence imposes substantial costs on healthcare systems, and elderly patients with polypharmacy regimens are particularly vulnerable to missed or incorrect doses. Robots in this domain face a different challenge from therapeutic companionship: trust and cognitive load are latent variables that cannot be directly measured, only inferred from noisy behavioural proxies. Lee and See (2004, p. 54) define trust as "the attitude that an agent will help achieve an individual's goals in a situation characterized by uncertainty and vulnerability"; a definition foregrounding the unobservable nature that necessitates probabilistic modelling. A user may comply with a medication prompt despite low trust (e.g. time pressure), or indeed refuse despite high trust (e.g. task complexity), and thus the observation alone cannot reliably disambiguate the underlying state (Hancock et al., 2011, p. 522).

The Partially Observable Markov Decision Process (POMDP) provides formal machinery for this uncertainty. Chen et al. (2020, p. 6) demonstrate a Trust-POMDP wherein the robot maintains a belief distribution over trust and selects actions that maximise long-term collaboration, showing belief-space planning outperforms fixed strategies in the tested collaborative scenario. Garcez and Lamb (2023, p. 12389) identify the neuro-symbolic paradigm as the 'third wave' of AI, wherein neural subsystems (e.g. large language models) handle perception whilst symbolic subsystems (e.g. POMDPs) govern temporal reasoning, providing the temporal scaffold stateless systems lack. Nikolaidis, Hsu and Srinivasa (2017, p. 625) provide empirical corroboration: in a collaborative task (n = 69), robots utilising mutual adaptation via a Mixed Observability MDP (modelling human adaptability as a latent variable) were rated significantly more trustworthy than fixed-policy alternatives (U = 180, p = 0.048). This aligns with Hancock et al.'s (2011, p. 522) finding that robot performance attributes are the strongest trust predictors, whilst demonstrating that belief-space planning as advocated by Chen et al. (2020, p. 6) translates into measurable trust gains.

### 1.3.3 Physical Rehabilitation and Mobility

Robotic exoskeletons and assistive manipulators for stroke recovery and mobility support constitute a third application domain. These systems need to adapt in real time not only to the patient's physical state (joint angles and muscle activation patterns) but also to their psychological state: motivation, frustration, and fatigue are internal variables that determine whether a patient perseveres or disengages.

Embodied cognition becomes essential. Brooks (1991, p. TODO) argues that intelligence emerges from physical interaction with the environment rather than abstract representation, whereas Fong, Nourbakhsh and Dautenhahn (2003, p. 149) operationalise this as "perturbatory coupling": the more channels of mutual influence between robot and environment, the more embodied the system. A rehabilitation robot therefore occupies a uniquely cognitive niche, as it should sense the patient's body, reason about current capabilities, and adapt appropriately. A purely language-based or screen-based interface cannot achieve this; Matarić et al. (2007, p. TODO) confirm as much empirically, finding that stroke survivors engaged more enthusiastically with a physically embodied assistive robot than with screen-based alternatives. Tapus, Ţăpuş and Matarić (2008, p. TODO), in fact show that embodiment alone is insufficient: adaptive personality matching (adjusting interaction distance and speed to the user's traits) further improved task performance, suggesting rehabilitation robots require not just physical presence but cognitive adaptation to the individual. The cognitive building blocks required (haptic perception, prospective planning of difficulty, episodic memory of the patient's trajectory) thus suggest an embodied cognitive architecture is necessary rather than a disembodied controller.

- [ ] ## 1.4. Discussion

### 1.4.1 Challenges

Tapus, Matarić and Scassellati (2007, *.pdf*-p. 6) projected that by 2012 SAR systems would demonstrate "marked improvement in learning/training/recovery of the user"; yet PARO, the most-deployed platform nearly twenty years later, *still* cannot remember yesterday's session. Three challenges explain this stalled trajectory. Firstly, computational intractability: solving $POMDPs$ exactly is PSPACE-complete (Papadimitriou and Tsitsiklis, 1987, p. 448 {TODO VERIFY}), and the belief simplex grows exponentially with state-space dimensionality. Whilst approximate solvers such as point-based value iteration (Pineau, Gordon and Thrun, 2003, p. 1025; Kaelbling, Littman and Cassandra, 1998, p. 120) and online Monte-Carlo tree search (Silver and Veness, 2010, p. 1) mitigate this, real-time cognitive processing within embodied systems remains an open challenge, particularly when multiple unobserved variables (trust, load, emotion) require tracking simultaneously.

Secondly, the measurement problem: trust, cognitive load, and emotional state are not directly observable; observations thereof are noisy proxies at best. Hancock et al.'s (2011, p. 522) meta-analysis of 29 studies finds that even the strongest correlates of trust explain only modest variance, whilst Broadbent, Stafford and MacDonald (2009, p. TODO) note that acceptance itself depends on matching robot behaviour to user expectations rather than trust alone. Desai et al. (2013, p. 256) further demonstrate that trust dynamics are non-linear, building slowly through consistent performance but degrading rapidly after errors; and thus a single misclassified observation can cascade into inappropriate action selection. Nikolaidis, Hsu and Srinivasa (2017, p. 627), however, demonstrate that mutual adaptation partially mitigates this fragility: when the robot models human adaptability as a latent variable, trust persists even during strategy disagreements, suggesting the variance Hancock et al. report may stem from studies that treat the human as a static rather than co-adaptive partner.

Finally, adaptation without exploitation: a robot that runs inference on cognitive load could, in principle, time its medication requests to coincide with periods of high vulnerability, thereby maximising compliance at the expense of user autonomy. The reward function governing the POMDP's policy should therefore encode ethical constraints alongside clinical objectives, ensuring that the optimisation target is genuine adherence rather than coerced compliance.

### 1.4.2 Ethical Implications

Assistive robots operating in intimate care spaces (bedrooms, bathrooms, rehabilitation clinics) continuously collect sensitive behavioural data. Facial expressions, vocal patterns, and movement trajectories constitute biometric data, yet regulatory frameworks have not kept pace with deployment. Wachter, Mittelstadt and Floridi (2017, p. TODO) argue that even the General Data Protection Regulation provides no enforceable "right to explanation" of automated decisions; a gap particularly concerning in healthcare wherein recommendations directly affect patient wellbeing.

Moreover, over-reliance on assistive robots risks eroding functional independence. If a robot consistently anticipates and pre-empts needs via prospection, the user may disengage from self-directed activity, thereby creating a dependency that contradicts the assistive mandate. Sharkey (2014, p. 6 (VERIFY)) frames this via Nordenfelt's 'Dignity of Identity': "a robot that dealt impersonally with an older person, without knowing or using their name or their preferences would also be likely to negatively affect their feelings of dignity." This implies that only cognitively-equipped robots (those with episodic memory of individual users) can avoid dignity violations; reactive systems such as PARO, regardless of their therapeutic benefits (Wada and Shibata, 2007, p. 974), risk infantilisation precisely because they cannot personalise. The responsibility gap compounds this further: when a care robot administers incorrect medication, liability falls ambiguously between manufacturer, deployer, and clinician.

Furthermore, the deployment of assistive robots is not equitable: wealthy nations with sufficient infrastructure and research investment stand to benefit, whilst low-income populations face a widening digital divide in access to care technologies. The question of whether assistive robots displace human carers or augment them remains unresolved.

The ethical watchword is therefore proactive regulation: design-stage ethics that anticipate failure modes before deployment, rather than reactive patchwork after harm. Per the embodied cognition thesis, if intelligence indeed requires a body, and that body enters the most intimate spaces of vulnerable persons, then the ethical stakes of assistive cognitive robotics are uniquely high.

- [ ] ## 1.5. Conclusion

Assistive robotics stands at an inflection point. Current systems (PARO, medication prompt robots, rehabilitation aids) deliver measurable benefits within narrow operational envelopes, yet their reactive architectures limit sustained, personalised effectiveness. The Vernon, Metta and Sandini (2007) cognition cycle provides the architectural blueprint for graduating beyond this plateau: assistive robots that anticipate (prospection), remember (episodic and semantic memory), reason about others' mental states (theory of mind), and monitor their own performance (metacognition) would constitute a qualitative advance over the most-capable systems deployed.

The neuro-symbolic paradigm offers a viable path toward this vision, as the Trust-POMDP framework attests (Chen et al., 2020). Sciutti et al. (2023, pp. 162-163) independently identify the integration of learning with model-based approaches as cognitive robotics' most-prominent trajectory; that this converges with Garcez and Lamb's (2023, p. 12389) 'third wave' thesis from AI theory suggests the direction is robust rather than parochial. Future applications will likely extend beyond single-task assistance toward cognitively autonomous home-dwelling companions: robots that proactively monitor health indicators, anticipate daily needs via episodic memory, and adapt their interaction style to the user's evolving cognitive and emotional state. Sharkey and Sharkey (2012, p. 27) identify this trajectory whilst cautioning that such systems risk replacing rather than supplementing human-care, and therefore the field should pursue cognitive capability and ethical governance in concert. Figure~\ref{fig:assistive-trajectory} visualises this trajectory. The ultimate test, per the embodied cognition thesis, is a robot that can sense, remember, anticipate, and adapt within the physical world, whilst respecting the autonomy and dignity of the persons it serves.

\begin{figure}[H]
\centering
\begin{tikzpicture}
\begin{axis}[
    width=12.5cm, height=8.5cm,
    xlabel={\textbf{Cognitive Architecture Completeness}},
    ylabel={\textbf{Assistive Scope}},
    xmin=-0.3, xmax=3.3,
    ymin=-0.3, ymax=3.3,
    xtick={0, 1, 2, 3},
    xticklabels={None, {\shortstack{Perception\\+ Action}}, {\shortstack{+ Memory\\+ Reasoning}}, {\shortstack{+ Prospection\\+ ToM + Meta.}}},
    ytick={0, 1, 2, 3},
    yticklabels={, Single-task, Multi-domain, {\shortstack{Holistic\\Home Care}}},
    every axis label/.style={font=\sffamily\small},
    every tick label/.style={font=\scriptsize\sffamily, align=center},
    grid=both,
    grid style={gray!20, thin},
    axis lines=left,
    axis line style={->, thick},
    clip=false,
]

% --- Trajectory arrow (background) ---
\draw[-{Stealth[length=5pt]}, line width=2.5pt, color=black!15]
    (axis cs: 0.4, 0.8) -- (axis cs: 2.7, 2.8);
\node[font=\tiny\sffamily\itshape, text=black!35, rotate=37] at (axis cs: 1.8, 2.15) {trajectory};

% --- System 1: PARO ---
\node[circle, fill=red!60, inner sep=4pt, draw=red!80, thick] (paro) at (axis cs: 0.5, 1) {};
\node[font=\scriptsize\sffamily, anchor=south west, text width=3.2cm, align=left] at (axis cs: 0.7, 0.75)
    {\textbf{PARO}\\[-1pt]{\tiny Reactive; no user model;}\\ {\tiny tactile/auditory response only}};

% --- System 2: Trust-POMDP ---
\node[circle, fill=orange!70, inner sep=4pt, draw=orange!90, thick] (pomdp) at (axis cs: 1.6, 1.8) {};
\node[font=\scriptsize\sffamily, anchor=south west, text width=3.5cm, align=left] at (axis cs: 1.85, 1.55)
    {\textbf{Trust-POMDP}\\[-1pt]{\tiny Belief-based; episodic memory;}\\ {\tiny infers hidden trust/load}};

% --- System 3: Future Cognitive Companion ---
\node[circle, fill=green!50!black, inner sep=4pt, draw=green!70!black, thick] (future) at (axis cs: 2.7, 2.8) {};
\node[font=\scriptsize\sffamily, anchor=south east, text width=3.8cm, align=right] at (axis cs: 2.55, 3.15)
    {\textbf{Future: Cognitive Companion}\\[-1pt]{\tiny Prospection + theory of mind +}\\ {\tiny metacognition; proactive holistic care}};

% --- Vernon cycle building blocks along x-axis (bottom annotation) ---
\node[font=\tiny\sffamily\itshape, text=gray, anchor=north] at (axis cs: 1.5, -0.15)
    {Vernon, Metta and Sandini (2007) cognition cycle building blocks $\longrightarrow$};

% --- Ethical caution annotation ---
\draw[-{Stealth[length=3pt]}, dashed, red!60, thin] (axis cs: 2.9, 2.3) -- (axis cs: 2.9, 2.65);
\node[font=\tiny\sffamily, text=red!70, anchor=west, text width=2.8cm] at (axis cs: 3.0, 2.3)
    {Sharkey \& Sharkey\\(2012): risk of\\replacing human care};

\end{axis}
\end{tikzpicture}
\caption{Trajectory of assistive robotics from reactive single-task systems (PARO) through adaptive belief-based architectures (Trust-POMDP) toward cognitively autonomous home-dwelling companions. Expanding assistive scope without expanding cognitive capability is insufficient; the diagonal trajectory requires both.}
\label{fig:assistive-trajectory}
\end{figure}

## 1.6. Task-3 References

### 1.6.1 Papers and Journal Articles

- [ ] verify all links work and extract each papers insights

**REMOVE: one checkmark for working link second for insight gathered**

- [ ] [ ] Broadbent, E., Stafford, R. and MacDonald, B. (2009) 'Acceptance of Healthcare Robots for the Older Population: Review and Future Directions', *International Journal of Social Robotics*, 1(4), pp. 319-330. Available at: https://www.researchgate.net/publication/220397395_Acceptance_of_Healthcare_Robots_for_the_Older_Population_Review_and_Future_Directions (Accessed: 25 March 2026).
- [ ] [ ] Brooks, R. A. (1991) 'Intelligence without representation', *Artificial Intelligence*, 47(1-3), pp. 139-159. Available at: https://people.csail.mit.edu/brooks/papers/representation.pdf (Accessed: 24 March 2026).
- [ ] [ ] Chen, M., Nikolaidis, S., Soh, H., Hsu, D. and Srinivasa, S. (2020) 'Trust-Aware Decision Making for Human-Robot Collaboration: Model Learning and Planning', *ACM Transactions on Human-Robot Interaction*, 9(2), pp. 1-23. Available at: https://arxiv.org/abs/1801.04099 (Accessed: 15 March 2026).
- [ ] [ ] Desai, M., Kaniarasu, P., Medvedev, M., Steinfeld, A. and Yanco, H. (2013) 'Impact of robot failures and feedback on real-time trust', *Journal of Human-Robot Interaction*, 2(1), pp. 251-275. Available at: https://ieeexplore.ieee.org/document/6483596 (Accessed: 20 March 2026).
- [ ] [ ] Fong, T., Nourbakhsh, I. and Dautenhahn, K. (2003) 'A survey of socially interactive robots', *Robotics and Autonomous Systems*, 42(3-4), pp. 143-166. Available at: https://www.cs.cmu.edu/~illah/PAPERS/socialroboticssurvey.pdf (Accessed: 18 March 2026).
- [ ] [ ] Garcez, A. d'A. and Lamb, L. C. (2023) 'Neurosymbolic AI: The 3rd Wave', *Artificial Intelligence Review*, 56, pp. 12387-12406. Available at: https://link.springer.com/article/10.1007/s10462-023-10448-w (Accessed: 20 March 2026).
- [ ] [ ] Hancock, P. A., Billings, D. R., Schaefer, K. E., Chen, J. Y. C., de Visser, E. J. and Parasuraman, R. (2011) 'A meta-analysis of factors affecting trust in human-robot interaction', *Human Factors*, 53(5), pp. 517-527. Available at: https://journals.sagepub.com/doi/10.1177/0018720811417254 (Accessed: 15 March 2026).
- [ ] [ ] Kaelbling, L. P., Littman, M. L. and Cassandra, A. R. (1998) 'Planning and acting in partially observable stochastic domains', *Artificial Intelligence*, 101(1-2), pp. 99-134. Available at: https://people.csail.mit.edu/lpk/papers/aij98-pomdp.pdf (Accessed: 13 March 2026).
- [ ] [ ] Lee, J. D. and See, K. A. (2004) 'Trust in automation: Designing for appropriate reliance', *Human Factors*, 46(1), pp. 50-80. Available at: https://journals.sagepub.com/doi/10.1518/hfes.46.1.50_30392 (Accessed: 15 March 2026).
- [ ] [ ] Matarić, M. J., Eriksson, J., Feil-Seifer, D. J. and Winstein, C. J. (2007) 'Socially assistive robotics for post-stroke rehabilitation', *Journal of NeuroEngineering and Rehabilitation*, 4(5), pp. 1-9. Available at: https://pmc.ncbi.nlm.nih.gov/articles/PMC1821334/ (Accessed: 25 March 2026).
- [ ] [ ] Nikolaidis, S., Hsu, D. and Srinivasa, S. (2017) 'Human-robot mutual adaptation in collaborative tasks: Models and experiments', *The International Journal of Robotics Research*, 36(5-7), pp. 618-634. Available at: https://journals.sagepub.com/doi/10.1177/0278364917690593 (Accessed: 20 March 2026).
- [ ] [ ] Papadimitriou, C. H. and Tsitsiklis, J. N. (1987) 'The complexity of Markov decision processes', *Mathematics of Operations Research*, 12(3), pp. 441-450. Available at: https://web.mit.edu/jnt/www/Papers/J016-87-mdp-complexity.pdf (Accessed: 13 March 2026).
- [ ] [ ] Pineau, J., Gordon, G. and Thrun, S. (2003) 'Point-based value iteration: An anytime algorithm for POMDPs', in *Proceedings of the 18th International Joint Conference on Artificial Intelligence (IJCAI-03)*, pp. 1025-1030. Available at: http://www.cs.cmu.edu/~ggordon/jpineau-ggordon-thrun.ijcai03.pdf (Accessed: 24 March 2026).
- [X] [ ] Sciutti, A., Beetz, M., Inamura, T., Korsah, A., Oh, J., Sandini, G., Shimoda, S. and Vernon, D. (2023) 'The Present and the Future of Cognitive Robotics', *IEEE Robotics & Automation Magazine*, 30(3), pp. 160-163. Available at: https://ieeexplore-ieee-org.plymouth.idm.oclc.org/document/10255092 (Accessed: 18 March 2026).
- [ ] [ ] Sharkey, A. (2014) 'Robots and human dignity: A consideration of the effects of robot care on the dignity of older people', *Ethics and Information Technology*, 16(1), pp. 63-75. Available at: https://philarchive.org/rec/SHARAH-2 (Accessed: 22 March 2026).
- [ ] [ ] Sharkey, A. and Sharkey, N. (2012) 'Granny and the robots: ethical issues in robot care for the elderly', *Ethics and Information Technology*, 14(1), pp. 27-40. Available at: https://philarchive.org/rec/SHAGAT (Accessed: 22 March 2026).
- [ ] [ ] Silver, D. and Veness, J. (2010) 'Monte-Carlo planning in large POMDPs', in *Advances in Neural Information Processing Systems (NeurIPS 23)*, pp. 2164-2172. Available at: https://proceedings.neurips.cc/paper/2010/file/edfbe1afcf9246bb0d40eb4d8027d90f-Paper.pdf (Accessed: 24 March 2026).
- [ ] [ ] Tapus, A., Matarić, M. J. and Scassellati, B. (2007) 'Socially assistive robotics [Grand Challenges of Robotics]', *IEEE Robotics & Automation Magazine*, 14(1), pp. 35-42. Available at: https://scazlab.yale.edu/sites/default/files/files/Tapus-RAM2007.pdf (Accessed: 25 March 2026).
- [ ] [ ] Tapus, A., Ţăpuş, C. and Matarić, M. J. (2008) 'User-robot personality matching and assistive robot behavior adaptation for post-stroke rehabilitation therapy', *Intelligent Service Robotics*, 1(2), pp. 169-183. Available at: https://hal.science/hal-00770108/document (Accessed: 26 March 2026).
- [X] [ ] Vernon, D., Metta, G. and Sandini, G. (2007) 'A Survey of Artificial Cognitive Systems: Implications for the Autonomous Development of Mental Capabilities in Computational Agents', *IEEE Transactions on Evolutionary Computation*, 11(2), pp. 151-180. Available at: [https://www.robotcub.org/misc/papers/07_Vernon_Metta_Sandini_IEEE.pdf](https://www.robotcub.org/misc/papers/07_Vernon_Metta_Sandini_IEEE.pdf) (Accessed: 13 March 2026).
- [ ] [ ] Wachter, S., Mittelstadt, B. and Floridi, L. (2017) 'Why a Right to Explanation of Automated Decision-Making Does Not Exist in the General Data Protection Regulation', *International Data Privacy Law*, 7(2), pp. 76-99. Available at: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2903469 (Accessed: 22 March 2026).
- [ ] [ ] Wada, K. and Shibata, T. (2007) 'Living with seal robots: its sociopsychological and physiological influences on the elderly at a care house', *IEEE Transactions on Robotics*, 23(5), pp. 972-980. Available at: https://ieeexplore.ieee.org/document/4339551 (Accessed: 18 March 2026).

# 2- Task (4) Noval Programming Project

- [ ] verify word count

<!--
- [ ] ensure code-solution matches `proposal.pdf`

References:

```markdown

### 1. Adaptive Companion / Socially Assistive Role (core concept)

- Tapus, Mataric and Scassellati (2007) -- This is your single most important paper. Socially assistive robotics is precisely what GAZE does: a robot that adapts its behaviour to motivate and coach a user. Their framework for robot-assisted therapy (detecting disengagement, adjusting difficulty) maps almost 1:1 onto your core loop.
- Fong, Nourbakhsh and Dautenhahn (2003) -- Foundational survey on socially interactive robots. Use it to ground GAZE within the broader taxonomy of social robots (companion, assistant, coach).
- Kahn et al. (2008) -- Design patterns for sociality in HRI. Directly supports your robot personality modes (encouraging vs. sarcastic) and the idea of building rapport through game interaction.

### 2. Affective Computing / Multi-Signal Fusion (core technical grounding)

- Calvo, R.A. and D'Mello, S. (2010) 'Affect detection: An interdisciplinary review of models, methods, and their applications', *IEEE Transactions on Affective Computing*, 1(1), pp. 18-37. DOI: 10.1109/t-affc.2010.1 -- NOW CITED IN BACKGROUND. Surveys unreliability of single-modality affect detection.
- Poria, S., Cambria, E., Bajpai, R. and Hussain, A. (2017) 'A review of affective computing: From unimodal analysis to multimodal fusion', *Information Fusion*, 37, pp. 98-125. DOI: 10.1016/j.inffus.2017.02.003 -- NOW CITED IN BACKGROUND. The review paper on why fusion beats single-modality.
- Ekman, P. and Friesen, W.V. (1971) 'Constants across cultures in the face and emotion', *Journal of Personality and Social Psychology*, 17(2), pp. 124-129. DOI: 10.1037/h0030377 -- NOW CITED IN METHOD (facial expression). Foundational 7-class emotion taxonomy.
- El Ayadi, M., Kamel, M.S. and Karray, F. (2011) 'Survey on speech emotion recognition: Features, classification schemes, and databases', *Pattern Recognition*, 44(3), pp. 572-587. DOI: 10.1016/j.patcog.2010.09.020 -- NOW CITED IN METHOD (vocal emotion). The SER survey.

### 3. Multi-Signal User State Inference & Adaptive Engine

- Nikolaidis, Hsu and Srinivasa (2017) -- Human-robot *mutual* adaptation in collaborative tasks. Directly supports your adaptive difficulty/game-switching mechanism where the robot adjusts based on inferred user state.
- Kaelbling, Littman and Cassandra (1998) -- Your adaptive engine is essentially a POMDP: user emotional/cognitive state is partially observable (you see facial expression + response time + correctness but not the true internal state). Cite this to give your inference model theoretical grounding.
- Pineau, Gordon and Thrun (2003) and Silver and Veness (2010) -- If you want to frame the adaptive engine formally, these are scalable POMDP solvers. Even if you don't implement a full POMDP, citing them shows you understand the decision-theoretic underpinning of what your weighted-signal inference is approximating.

### 4. Trust & Engagement Over Time

- Desai et al. (2013) -- Impact of robot failures and feedback on real-time trust. Directly relevant: if GAZE generates a bad question or misreads emotion, how does that affect user trust? Supports your feedback system idea.
- Hancock et al. (2011) -- Meta-analysis of trust factors in HRI. Use to justify which signals matter for building trust (robot performance, reliability of adaptation).
- Lee and See (2004) -- Trust in automation. Your system is making autonomous decisions (switching games, adjusting difficulty). This paper grounds *why* the user needs to trust those decisions.
- Chen et al. (2020) -- Trust-aware decision making. Supports the idea that your adaptive engine should factor in whether the user trusts the robot's choices, not just performance metrics.
- Smedegaard (2019) -- Novelty effects in social HRI. Critical for your proposal: initial engagement with Pepper may be high due to novelty, then decline. Your adaptive system needs to sustain engagement *beyond* the novelty phase. Cite this to show awareness of that challenge.

### 5. LLM Integration (OpenAI for Game/Dialogue Generation)

- Ahn et al. (2022) -- Grounding language in robotic affordances ("SayCan"). Cite to justify connecting an LLM to Pepper's physical capabilities (speech, gestures). The LLM generates the game content, but it should be grounded in what Pepper can actually *do*.
- Ji et al. (2023) -- LLM hallucination survey. Critical to acknowledge: if OpenAI generates a trivia question, the answer could be wrong. Your system needs a correctness-verification layer. Shows awareness of a real technical risk.
- Garcez and Lamb (2023) -- Neurosymbolic AI. Your architecture is inherently neurosymbolic: the LLM (neural) handles dialogue generation, but game logic, scoring, and state tracking are symbolic/rule-based. Cite to frame this hybrid approach deliberately rather than accidentally.

### 6. Uncanny Valley / Robot Appearance

- Mori (1970) -- Pepper sits in an interesting spot on the uncanny valley curve (humanoid but clearly not human). Brief cite to justify why Pepper is a suitable platform for a companion role without triggering discomfort.

### 7. Ethics of Robot Companionship

- Sharkey and Sharkey (2012) -- Ethical issues in robot care for the elderly. If GAZE has any therapeutic/wellbeing angle, cite this to show awareness of ethical considerations (e.g., should a robot be a substitute for human interaction?).
- Sharkey (2014) -- Robots and human dignity. Supports ethical grounding of the companion role.
- Wachter, Mittelstadt and Floridi (2017) -- If you're storing user progress/preferences, cite for GDPR and explainability considerations regarding the adaptive engine's decisions.

### 8. Cultural Considerations (if relevant to your report)

- Kaplan (2004), Lim, Rooksby and Cross (2021), Cirasa and Conti (2025) -- All address cultural differences in robot acceptance and trust. Useful if your report discusses how GAZE might be received differently across cultures.

### Less Directly Relevant

- Rios-Martinez et al. (2015) and Joosse et al. (2014) - Proxemics/navigation. Since Pepper is stationary, these are tangential unless you discuss the seating arrangement/distance.
- Papadimitriou and Tsitsiklis (1987) - Complexity of MDPs. Only cite if you formally discuss the computational complexity of your adaptive decision-making.
- Metz (2007), Winschiers-Theophilus and Bidwell (2013), Wyche and Steinfield (2016) - African moral theory / indigenous HCI / technology adoption. Not directly applicable unless you bring in a specific cultural-ethics angle.

```

- [ ] **Strongest citations for the core GAZE concept: Tapus et al. (2007), Sciutti et al. (2023), Nikolaidis et al. (2017), Ahn et al. (2022), and Smedegaard (2019). These five alone cover the adaptive-assistive role, cognitive framing, mutual adaptation, LLM-robot grounding, and the novelty-engagement challenge.**
-->

## 2.1. Introduction (10%)

## 2.2. Background (10%; Alfie)

GAZE sits within socially assistive robotics *(the deployment of robots to support users through social interaction rather than physical contact)*; Tapus, Matarić and Scassellati (2007, p. 35) define this sub-field as systems that "assist users through social interaction." Most-current platforms react to a single input signal (Fong, Nourbakhsh and Dautenhahn, 2003, p. 148), suffering the single-signal problem: a facial-expression classifier misreads resting faces as displeasure; a response-time metric mistakes deliberation for disengagement. Calvo and D'Mello (2010, p. 28) identify "the inherent challenges with unisensory affect detection"; Poria et al. (2017, p. 99) report that multimodal systems were "consistently (85% of systems) more accurate than their best unimodal counterparts, with an average improvement of 9.83%." This demands multi-signal fusion (the system weighs complementary channels together instead of trusting any one alone).

GAZE's core contribution is therefore multi-signal emotional inference: facial expression (CNN, Workshop 10), vocal emotion (MLP, Workshop 8), response time, and answer correctness are fused alongside three derived temporal signals into a single inferred user-state. The architecture is hybrid: GPT-4.1 generates dialogue whilst a symbolic AdaptiveEngine governs state inference, grounding output in Pepper's affordances (Ahn et al., 2022, p. 1). Smedegaard (2019, p. 4) warns that engagement with social robots reflects novelty rather than sustained interest; GAZE targets this via adaptive game-switching.

- [ ] Furthermore, four selectable personality modes, grounded in Tapus, Tapus and Mataric (2008, p. TODO: VERIFY PAGE) and Kahn et al.'s (2008, pp. 97-104) design patterns for sociality, extend static personality matching to dynamic, signal-driven adaptation.

## 2.3. Methods & Setup (35%; Alfie)

### 2.3.1 System Architecture

GAZE operates as a conversational loop rather than a rigid question-answer cycle. Each turn: 1) five emotional signals are captured; 2) the AdaptiveEngine infers user-state; 3) signal context and transcribed speech are sent to GPT-4.1 with function-calling tools; 4) the LLM decides whether to respond conversationally, initiate a game, check an answer, or adjust difficulty; 5) the spoken response, gestures, and LED state are delivered on Pepper concurrently via threading. Computation runs on the laptop; Pepper handles physical I/O. Ensuring all five signals are immediately inferred upon system startup, before the main-conversation loop begins post-personality selection; the dashboard thus reflects live emotional state inference from the moment the user sits down, not solely once gameplay commences.

- [ ] This function-calling architecture is neuro-symbolic: GPT-4.1 governs dialogue and decision-making, whilst the AdaptiveEngine and game logic are exposed as callable tools. This aligns with Garcez and Lamb's (2023, p. TODO: VERIFY 12389) 'third wave' paradigm, wherein neural and symbolic components share a structured interface (cf. Ahn et al., 2022, p. 1).

\begin{figure}[H]
\centering
\includegraphics[width=0.82\textwidth]{task-4/SYSTEM-DIAGRAM.png}
\caption{GAZE system architecture (adapted from the project proposal). Four input channels (facial expression, vocal emotion, response time, answer correctness) feed the AdaptiveEngine (PROCESS), which infers user-state and constructs a dynamic prompt for OpenAI GPT-4.1 (GENERATE); the resultant dialogue, gesture tag, and game-state update are delivered via Pepper's speech, motor, and LED subsystems (OUTPUT) concurrently. The loop circulates to the next round, now adapted.}
\label{fig:system-diagram}
\end{figure}

### 2.3.2 Input Layer: Four Simultaneous Signals

**1- Facial Expression (vision-based).** A pre-trained CNN (Workshop 10) classifies the user's expression into seven categories (Angry, Disgust, Fear, Happy, Neutral, Sad, Surprise) from a $48\times48$ greyscale face region, building upon Ekman and Friesen (1971, pp. 127-128), whose cross-cultural results show that "particular facial behaviors are universally associated with particular emotions," finding that even preliterate (without written language) cultures with "minimal opportunity to have learned to recognize uniquely Western facial expressions" identified the same six emotions; this taxonomy remains "still the most popular perspective for FER" (Li and Deng, 2020, p. 1). Known limitations (cultural bias, resting-face misclassification) are mitigated via cross-modal override.

**2- Verbal Answer (speech-based).** Pepper records audio via `ALAudioRecorder` with dynamic silence detection calibrated to the room's ambient noise level at startup. Recording terminates when 1.5 seconds of silence follows detected speech, or a 12-second hard ceiling is reached. The recorded WAV is transcribed via OpenAI Whisper (`whisper-1`).

**3- Vocal Emotion (audio-based).** The same WAV is passed through a pre-trained MLP (Workshop 8) *before* transcription, classifying vocal state into four emotions (calm, happy, fearful, disgust) via MFCC, chroma, and mel-spectrogram features; El Ayadi, Kamel and Karray (2011, p. 577) identify MFCCs as "the most promising features" for speech-emotion recognition. This provides a second, independent modality; the two may disagree, wherein decision logic arbitrates.

**4- Response Time (engagement-based).** A Python timer measures elapsed time from question delivery to recording completion; the Whisper call occurs *after* the timer halts, isolating deliberation time from API latency.

### 2.3.3 Process Layer: Multi-Signal State Inference

The AdaptiveEngine's `infer_state()` method weighs seven signals to classify the user into one of five states: *Thriving*, *Comfortable*, *Struggling*, *Frustrated*, or *Disengaged*. Four raw inputs are supplemented by three derived temporal signals: rolling correctness over the last five rounds, consecutive silence count, and consecutive wrong-answer streak length. The classification rules combine these in cross-modal ways (see Listing~\ref{lst:infer} and Table~\ref{tab:state-action}): neither visual nor vocal modality is trusted in isolation. GAZE's multi-signal approach, wherein temporal streaks override or corroborate instantaneous readings, addresses the brittleness Desai et al. (2013, p. 256) observe when systems depend on singular, noisy observations. Thresholds (correctness floor 0.4, ceiling 0.8, response-time baseline 30s, consecutive-wrong trigger 3) were derived from pilot testing.

\begin{figure}[H]
\centering
\begin{tikzpicture}[
    every node/.style={font=\sffamily\scriptsize},
    raw/.style={rectangle, rounded corners=2pt, draw=blue!60, fill=blue!8,
                minimum width=2.8cm, minimum height=0.5cm, align=center},
    der/.style={rectangle, rounded corners=2pt, draw=orange!70, fill=orange!10,
                minimum width=2.8cm, minimum height=0.5cm, align=center},
    eng/.style={rectangle, rounded corners=5pt, draw=black!70, fill=gray!10, thick,
                minimum width=2.2cm, minimum height=2.8cm, align=center,
                font=\sffamily\small\bfseries},
    st/.style={rectangle, rounded corners=2pt, draw=black!50,
               minimum width=2.2cm, minimum height=0.5cm, align=center},
    >=Stealth,
]
% Raw inputs
\node[font=\sffamily\tiny\bfseries, text=blue!60] at (0, 2.6) {RAW (per-round)};
\node[raw] (e) at (0, 2)   {Facial Expression};
\node[raw] (v) at (0, 1.2) {Vocal Emotion};
\node[raw] (t) at (0, 0.4) {Response Time};
\node[raw] (c) at (0,-0.4) {Current Correctness};
\node[raw] (a) at (0,-1.2) {Answer Text};
% Derived
\node[font=\sffamily\tiny\bfseries, text=orange!70] at (0, -2.2) {DERIVED (temporal)};
\node[der] (rc) at (0,-2.9) {Rolling Correctness};
\node[der] (cs) at (0,-3.7) {Consec. Silences};
\node[der] (cw) at (0,-4.5) {Consec. Wrong Streak};
% Engine
\node[eng] (eng) at (5.2, -0.5) {\texttt{infer\_state()}\\[3pt]{\scriptsize Cross-modal}\\{\scriptsize weighted rules}};
% States
\node[font=\sffamily\tiny\bfseries, text=black!50] at (10, 2.3) {INFERRED STATE};
\node[st, fill=green!12, draw=green!50!black]  (s1) at (10, 1.6) {THRIVING};
\node[st, fill=white, draw=gray]               (s2) at (10, 0.6) {COMFORTABLE};
\node[st, fill=yellow!15, draw=yellow!70!black] (s3) at (10,-0.4) {STRUGGLING};
\node[st, fill=orange!15, draw=orange!70]       (s4) at (10,-1.4) {FRUSTRATED};
\node[st, fill=blue!8, draw=blue!50]            (s5) at (10,-2.4) {DISENGAGED};
% Arrows: raw to engine
\foreach \n in {e,v,t,c,a} \draw[->,black!40,thick] (\n.east) -- (eng.west |- \n);
% Arrows: derived to engine
\draw[->,black!40,thick] (rc.east) -| ([xshift=-2mm]eng.south west);
\draw[->,black!40,thick] (cs.east) -| (eng.south);
\draw[->,black!40,thick] (cw.east) -| ([xshift=2mm]eng.south east);
% Arrows: engine to states
\foreach \n in {s1,s2,s3,s4,s5} \draw[->,black!40,thick] (eng.east) -- (\n.west);
\end{tikzpicture}
\caption{Multi-signal inference pipeline. Four raw inputs captured each round and three derived temporal signals computed from session history feed into \texttt{infer\_state()}, which applies cross-modal rules (e.g. camera reads \textit{Angry} but user answers fast and correctly $\rightarrow$ \textit{Comfortable}; voice reads \textit{calm} whilst camera frowns $\rightarrow$ cross-modal override to \textit{Comfortable}) to classify the user into one of five states. Neither visual nor vocal modality is trusted in isolation; therefore, the multi-signal novelty.
\label{fig:multi-signal}
\end{figure}

The cross-modal inference rules are shown in Listing~\ref{lst:infer} (extracted from `gaze.py`, *lines 343--438*):

\begin{lstlisting}[caption={Multi-signal inference rules (excerpt from \texttt{gaze.py}).}, label=lst:infer]

# thriving: performing well regardless of resting face

if (correctness >= CORRECTNESS_CEILING
        and response_time < RESPONSE_TIME_BASELINE * 0.5):
    return InferredState.THRIVING

# camera says Angry but fast + correct (*@$\rightarrow$@*) they're fine

if expression == "Angry" and correct
    and response_time < RESPONSE_TIME_BASELINE * 0.6:
    return InferredState.COMFORTABLE

# disengaged: multiple signals pointing to checked-out

if self.consecutive_silences >= SILENCE_THRESHOLD:
    return InferredState.DISENGAGED
if (expression == "Neutral"
        and response_time > RESPONSE_TIME_BASELINE
        and correctness < 0.5):
    return InferredState.DISENGAGED

# frustrated: struggling + negative expression

if expression in ("Angry", "Disgust")
    and correctness < CORRECTNESS_FLOOR:
    return InferredState.FRUSTRATED
if self.consecutive_wrong >= 3
    and expression in ("Angry", "Sad", "Fear"):
    return InferredState.FRUSTRATED
\end{lstlisting}

The `decide()` function then maps the inferred state to concrete adaptive actions: difficulty adjustment (easy, medium, hard), game switching (numbers $\leftrightarrow$ letters when the user is frustrated or disengaged), hint provision, encouragement, and tone selection. This maps onto Nikolaidis, Hsu and Srinivasa's (2017, p. 625) mutual-adaptation paradigm. Table~\ref{tab:state-action} summarises the mapping.

\begin{table}[H]
\centering
\small
\renewcommand{\arraystretch}{1.2}
\begin{tabular}{l c c c c c}
\toprule
\textbf{Inferred State} & \textbf{Difficulty} & \textbf{Game Switch} & \textbf{Hint} & \textbf{Tone} & \textbf{LED Colour} \\
\midrule
Thriving    & $\uparrow$ ramp up     & No  & No  & Energetic    & \textcolor{green!60!black}{Green} \\
Comfortable & $\uparrow$ if $>$70\%  & No  & No  & Neutral      & White \\
Struggling  & $\downarrow$ ease off  & No  & Yes & Encouraging  & \textcolor{yellow!80!black}{Yellow} \\
Frustrated  & $\downarrow\downarrow$ Easy & After 4 wrong & Yes & Calm & \textcolor{orange}{Orange} \\
Disengaged  & ---                    & After 2 silent & No & Energetic & \textcolor{blue!60}{Blue} \\
\bottomrule
\end{tabular}
\caption{State-to-action mapping. The adaptive engine translates each inferred state into a specific combination of difficulty adjustment, game-type switch, hint provision, tone selection, and LED colour. Arrows indicate direction of difficulty change relative to the current level.}
\label{tab:state-action}
\end{table}

### 2.3.4 Generate Layer: Dynamic Prompt Construction

- [ ] Rather than constructing a fixed game prompt each round, GAZE utilises OpenAI function calling to let GPT-4.1 decide which actions to take. Every turn, `build_signal_context()` packages all five live signals into a context block prepended to the user's transcribed speech. This is sent to GPT-4.1 with eight callable tools: `generate_game_question`, `check_game_answer`, `get_adaptive_recommendation`, `check_reward_milestone`, `get_session_summary`, `save_progress`, `evaluate_last_adaptation`, and `select_personality`. The LLM decides which tools to invoke based on context; during natural conversation it calls none, whilst during gameplay it chains `check_game_answer`, `get_adaptive_recommendation`, and `generate_game_question` in a single turn. Separate OpenAI calls handle game-question generation at a creative temperature and answer verification at a deterministic temperature; the latter mitigates the hallucination risk Ji et al. (2023, p. 3) identify. A strict 10-second timeout wraps every API call; if the network stalls, the robot falls back gracefully, thereby ensuring Pepper remains responsive.

### 2.3.5 Output Layer: Aligned Multimodal Response

Speech, gestures, and LED state fire concurrently via threading. Context-aligned gestures (e.g. animated speech for celebratory moments) execute alongside dialogue, whilst LED colours reflect the inferred state, providing a secondary non-verbal feedback channel.

### 2.3.6 Adaptation Self-Evaluation and Session Persistence

After each round, `evaluate_adaptation()` assesses whether the previous adaptation worked by comparing concrete outcome pairs (e.g. did a difficulty decrease produce a correct answer?). The evaluation feeds into the next LLM call, creating a system that learns whether its adaptations are effective. Session progress is saved to `gaze_save.json` after every round, protecting data against unexpected crashes and supporting session resumption.

<!-- POMDP content removed (superseded by GAZE). See git history if needed. -->

## 2.4. Outcome & System Analysis (30%)

## 2.5. Conclusion (10%; Alfie)

GAZE implements multi-signal emotional inference across two independent modalities *(facial expression via WS-10 CNN and vocal emotion via WS-08 MLP)* alongside response time, answer correctness, and derived temporal signals, which yields a more robust user-state estimate than any single channel in isolation. The adaptive engine translates the inferred state into concrete actions and evaluates whether those actions worked; this self-evaluation loop feeds back into the LLM prompt, creating a system that genuinely adapts rather than executing a fixed interaction script. The hybrid architecture (neural generation paired with symbolic rule-based inference) and the adaptive game-switching mechanism directly targets the novelty-decay problem Smedegaard (2019, p. 4) identifies.

- [ ] The conversational architecture, wherein the LLM decides actions via function calling, positions GAZE as a social companion rather than a rigid game host. The selectable personality modes extend Tapus, Tapus and Mataric's (2008, p. TODO: VERIFY PAGE) personality matching from static trait-matching to dynamic, signal-driven adaptation.

The multi-signal approach could transfer to stroke rehabilitation re-engagement (Mataric et al., 2007), educational tutoring, or neurodivergent support. Future work could replace hand-coded thresholds with learned parameters from longitudinal data, and fine-tune both models on in-session Pepper captures.

<!-- NOTE FOR SALMAN: The following limitations should go in section 2.4 (Outcome & System Analysis):
- Facial-expression CNN not fine-tuned for deployment context (Workshop 10 model, general dataset, low confidence under poor lighting)
- Speech-emotion MLP trained on RAVDESS acted-speech corpus; domain mismatch with natural conversational speech, partially mitigated by cross-modal design
- Classification thresholds (correctness floor 0.4, response-time baseline 30s, consecutive-wrong 3) are hand-coded rather than learned; prioritises interpretability over optimisation
- Conversation history grows unboundedly; extended sessions may approach OpenAI token limits -->

## 2.6 Task-4 References (5%)

- [ ] verify all references

### Alfie's

- Ahn, M., Brohan, A., Brown, N., et al. (2022) 'Do As I Can, Not As I Say: Grounding Language in Robotic Affordances', *arXiv preprint arXiv:2204.01691*. Available at: https://arxiv.org/abs/2204.01691 (Accessed: 24 March 2026).

- [X] - [ ] Calvo, R.A. and D'Mello, S. (2010) 'Affect Detection: An Interdisciplinary Review of Models, Methods, and Their Applications', *IEEE Transactions on Affective Computing*, 1(1), pp. 18--37. Available at: [https://www.researchgate.net/publication/220395370_Affect_Detection_An_Interdisciplinary_Review_of_Models_Methods_and_Their_Applications](https://www.researchgate.net/publication/220395370_Affect_Detection_An_Interdisciplinary_Review_of_Models_Methods_and_Their_Applications) (Accessed: 2 April 2026). **VERIFIED: p. 28 -- "the inherent challenges with unisensory affect detection" and "mostly unimodal approaches" (Section 3.7). DOI: 10.1109/t-affc.2010.1**

- Desai, M., Kaniarasu, P., Medvedev, M., Steinfeld, A. and Yanco, H. (2013) 'Impact of robot failures and feedback on real-time trust', *Journal of Human-Robot Interaction*, 2(1), pp. 251--275. Available at: https://ieeexplore.ieee.org/document/6483596 (Accessed: 20 March 2026).

- [X] - [ ] Ekman, P. and Friesen, W.V. (1971) 'Constants Across Cultures in the Face and Emotion', *Journal of Personality and Social Psychology*, 17(2), pp. 124--129. Available at: [http://www.communicationcache.com/uploads/1/0/8/8/10887248/constants_across_cultures_in_the_face_and_emotion.pdf](http://www.communicationcache.com/uploads/1/0/8/8/10887248/constants_across_cultures_in_the_face_and_emotion.pdf) (Accessed: 2 April 2026). **VERIFIED: p. 128 -- "particular facial behaviors are universally associated with particular emotions" and "minimal opportunity to have learned to recognize uniquely Western facial expressions" (Discussion). DOI: 10.1037/h0030377**
- [X] - [ ] El Ayadi, M., Kamel, M.S. and Karray, F. (2011) 'Survey on speech emotion recognition: Features, classification schemes, and databases', *Pattern Recognition*, 44(3), pp. 572--587. Available at: [https://www.sciencedirect.com/science/article/pii/S0031320310004619](https://www.sciencedirect.com/science/article/pii/S0031320310004619) (Accessed: 2 April 2026). **VERIFIED: p. 577 -- "the MFCC are the most promising features" for speech representation (Section 3.2 conclusion). DOI: 10.1016/j.patcog.2010.09.020**

- Fong, T., Nourbakhsh, I. and Dautenhahn, K. (2003) 'A survey of socially interactive robots', *Robotics and Autonomous Systems*, 42(3--4), pp. 143--166. Available at: https://www.cs.cmu.edu/~illah/PAPERS/socialroboticssurvey.pdf (Accessed: 18 March 2026).
- Garcez, A. d'A. and Lamb, L. C. (2023) 'Neurosymbolic AI: The 3rd Wave', *Artificial Intelligence Review*, 56, pp. 12387--12406. Available at: https://link.springer.com/article/10.1007/s10462-023-10448-w (Accessed: 20 March 2026).
- Ji, Z., Lee, N., Frieske, R., et al. (2023) 'Survey of Hallucination in Natural Language Generation', *ACM Computing Surveys*, 55(12), pp. 1--38. Available at: https://dl.acm.org/doi/10.1145/3571730 (Accessed: 22 March 2026).

- [X] - [ ] Li, S. and Deng, W. (2020) 'Deep Facial Expression Recognition: A Survey', *IEEE Transactions on Affective Computing*, 13(3), pp. 1195--1215. Available at: [http://www.whdeng.cn/Li_Deng_Survey.pdf](http://www.whdeng.cn/Li_Deng_Survey.pdf) (Accessed: 2 April 2026). **VERIFIED: p. 1 -- "The categorical model that describes emotions in terms of discrete basic emotions is still the most popular perspective for FER." DOI: 10.1109/TAFFC.2020.2981446**

- Kaelbling, L. P., Littman, M. L. and Cassandra, A. R. (1998) 'Planning and acting in partially observable stochastic domains', *Artificial Intelligence*, 101(1--2), pp. 99--134. Available at: https://people.csail.mit.edu/lpk/papers/aij98-pomdp.pdf (Accessed: 13 March 2026).

- [X] - [ ] Poria, S., Cambria, E., Bajpai, R. and Hussain, A. (2017) 'A review of affective computing: From unimodal analysis to multimodal fusion', *Information Fusion*, 37, pp. 98--125. Available at: [https://dspace.stir.ac.uk/bitstream/1893/25490/1/affective-computing-review.pdf](https://dspace.stir.ac.uk/bitstream/1893/25490/1/affective-computing-review.pdf) (Accessed: 2 April 2026). **VERIFIED: p. 99 -- "consistently (85% of systems) more accurate than their best unimodal counterparts, with an average improvement of 9.83%." DOI: 10.1016/j.inffus.2017.02.003**

- Nikolaidis, S., Hsu, D. and Srinivasa, S. (2017) 'Human-robot mutual adaptation in collaborative tasks: Models and experiments', *The International Journal of Robotics Research*, 36(5--7), pp. 618--634. Available at: https://journals.sagepub.com/doi/10.1177/0278364917690593 (Accessed: 20 March 2026).
- Sciutti, A., Beetz, M., Inamura, T., et al. (2023) 'The Present and the Future of Cognitive Robotics', *IEEE Robotics \& Automation Magazine*, 30(3), pp. 160--163. Available at: https://ieeexplore-ieee-org.plymouth.idm.oclc.org/document/10255092 (Accessed: 18 March 2026).
- Smedegaard, C. V. (2019) 'Reframing the Role of Novelty within Social HRI: From Noise to Information', in *Proceedings of the 14th ACM/IEEE International Conference on Human-Robot Interaction (HRI '19)*, pp. 411--420. Available at: https://dl.acm.org/doi/10.1109/HRI.2019.8673219 (Accessed: 22 March 2026).
- Tapus, A., Matarić, M. J. and Scassellati, B. (2007) 'Socially assistive robotics [Grand Challenges of Robotics]', *IEEE Robotics \& Automation Magazine*, 14(1), pp. 35--42. Available at: https://scazlab.yale.edu/sites/default/files/files/Tapus-RAM2007.pdf (Accessed: 25 March 2026).

## 2.7. Appendix

### 2.7.1. Code

### 2.7.2. Video Demo

- YouTube link: [test](test)

# Appendices

## Appendix A: AI Declaration

\begin{figure}[H]
\centering
\includegraphics[width=0.55\textwidth]{image/ai-decl.png}
\caption{Student Declaration of AI Tool use in this Assessment Table}
\end{figure}

I declare that I've used the AI tools listed below whilst preparing this assessment. I've read and understood the University of Plymouth's policy on the use of AI tools in assessment and confirm that my use falls within the coursework's allowed categories, i.e. \textbf{A2 (Planning and Structuring Projects)} and \textbf{A4 (Research Assistance)}.

\renewcommand{\arraystretch}{1.1}
\setlength{\tabcolsep}{4pt}

\begin{tabular}{|>{\raggedright\arraybackslash}p{3.2cm}|
                >{\raggedright\arraybackslash}p{8cm}|
                >{\raggedright\arraybackslash}p{4cm}|}
\hline
\textbf{AI Tool Used} & \textbf{Purpose of Use} & \textbf{Extent of Use} \\
\hline
ChatGPT & Brainstorming project ideas and structuring the report \textbf{(A2)} & Initial brainstorming and final outline stages \\
\hline
ChatGPT & Reviewing structural alignment against grading criteria and mapping word-count budgets \textbf{(A2)} & After and midway through section-drafting \\
\hline
ChatGPT & Finding relevant pages to read in the paper \textbf{(A4)} & Few times if the paper is too long \\
\hline
ChatGPT & General conversations via web-search AI about prevalent papers to read about how the topics relates to others' studies \textbf{(A4)} & Few times at the end \\
\hline
\end{tabular}

- [X] I understand that the ownership and responsibility for the academic integrity of this submitted assessment falls with me, the student.
- [X] I confirm that all details provided above are an accurate description of how AI was used for this assessment.
