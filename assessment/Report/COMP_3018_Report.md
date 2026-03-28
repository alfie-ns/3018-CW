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

- [ ] EMERGENT COGNITIVE ARCHITECTURE
- [ ] cite Iuliia Kotseruba1 · John K. Tsotsos1

## Mentor

Scenario 1) patient takes meds = + 100 points
Scenario 2) Patient is annoyed = -10 points
When you implement tis you need to be careful to structure the rewards such that the system does not pester the patient as it seeks to maximise it's rewards
You'll need to play around with the precise ratios between 1 (behaviour you want to encourage) and 2 (behaviour you want to discourage) to achieve the desired attitude from the robot

## DR ALY QUESTIONS:

- [X] so maths and code won't affect word count right? However I never explcitly knew if captions within a figure-diagram count towards word count?

---

## First-to-do:

- [ ] **Most critical:** verify all page numbers and sentences manually
- [ ] **Most critical:** verify all links to papers manually
- [ ] integrate 'gage'
- [ ] do all page number TODOs
- [ ] implement loads of peer-reviewed papers everywhere again

## General:

- [ ] Download Bemelmans and Broadbent via Plymouth library
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
	- [X] Reference Cangelosi & Asada definition of cognitive robotics
	- [X] Use Vernon (2014) cognition cycle (Anticipate -> Learn -> Adapt + Perception <-> Action = Autonomy) as a framing device for what effective assistive robots need
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

- [ ] ## 1.1. Introduction

Ageing populations and a shrinking care workforce have positioned assistive robotics *(the deployment of robotic systems to support humans with physical, cognitive, or social impairments in activities of daily living)* as a prominent technological response to a widening care gap. Robots now administer medication reminders, facilitate rehabilitation exercises, and provide therapeutic companionship in clinical and domestic settings. Measurably: reduced caregiver burden, improved patient outcomes in controlled trials, and increased social engagement among isolated elderly residents.

However, most-current assistive robots operate at what Sciutti et al. (2023, p. 160) term the social layer: they react to immediate stimuli but lack the cognitive depth to anticipate user needs, remember past interactions, or reason about their own performance. Sciutti et al. argue that effective assistive robots must be *cognitive*: capable of "flexible, context-sensitive action, knowing what they are doing and why they are doing it." Vernon, Metta and Sandini (2007, p. TODO) formalise this requirement via a cognition cycle wherein the agent anticipates, learns, and adapts, intersecting these processes with perception and action to achieve autonomy. This essay contends that assistive robotics must graduate from reactive social behaviour to cognitive capability (intelligence deployed *over* the social layer, not vice versa) if it is to deliver sustained, personalised support. The following sections survey the theoretical foundations thereof, evaluate prominent applications through this cognitive lens, discuss challenges and ethical implications, and identify future directions.

- [ ] ## 1.2. Literature Review

Cognitive robotics, as defined by Sciutti et al. (2023, p. 160) and introduced within the module (Lecture 9, slides 4-5), lies at the intersection of Robotics, Artificial Intelligence, and Cognitive and Biological Sciences, combining "sensorimotor behaviour, higher-level functions, and social capabilities of an intelligent robot." This interdisciplinary grounding distinguishes it from conventional robotics *(which treats the robot as purely engineered)* and from social robotics *(which addresses interaction behaviour without necessarily modelling cognitive processes)*. The distinction is consequential: a robot that smiles when a patient smiles is social; a robot that infers *why* the patient is smiling, and adjusts its future strategy accordingly, is cognitive.

Vernon, Metta and Sandini (2007, p. TODO) synthesise the field's definitional plurality into a core cycle (Lecture 9, slide 14). The European Network for Advancement of Artificial Cognitive Systems (euCognition) catalogued 42 distinct definitions of cognition (Lecture 9, slide 13), yet as Aly explained, the common thread across all is: "we anticipate, we learn, we adapt, and we intersect this with perception and action to create autonomy." This cycle provides an architectural checklist for assistive robots: a system that cannot anticipate the outcome of its actions *(prospection)*, learn from past interactions *(memory)*, or adapt its strategy when performance declines *(metacognition)* is, per this framework, not yet cognitive. Sciutti et al. (2023, p. 160) further specify that cognitive robots must "reason about their actions and modify their behavior to improve their effectiveness"; a capacity termed *theory of mind*, wherein the agent infers another's latent mental state from observable behaviour.

Memory, moreover, is not monolithic. Vernon, Metta and Sandini (2007, p. TODO) distinguish *episodic memory* *(records of specific past experiences and their contextual outcomes)* from *semantic memory* *(general knowledge about the world, including spatial relationships and factual constraints)*. An assistive medication robot, for instance, needs episodic memory to recall that a user refused medication after a restless night, and semantic memory to know certain drugs cannot be co-administered. Whilst the 42-definitions problem confirms the field lacks consensus on what cognition per se *is*, the common thread (anticipation, learning, adaptation) is precisely what assistive robotics demands.

- [ ] ## 1.3. Applications

### 1.3.1 Therapeutic and Emotional Support

The PARO therapeutic seal robot represents one of the most-widely deployed platforms within socially assistive robotics (Tapus, Matarić and Scassellati, 2007, p. TODO). Wada and Shibata (2007, p. 974) demonstrate that PARO reduces agitation and improves mood in patients with dementia, utilising tactile sensors and auditory processing to modulate its behaviour in response to touch and voice. Clinical trials report reduced cortisol levels and increased social engagement among residents (Bemelmans et al., 2012, p. TODO), thus the platform has been adopted in care homes across Japan, Europe, and the United States.

Notwithstanding these benefits, PARO operates at the reactive layer. It possesses no theory of mind (it cannot infer *why* a patient is agitated: loneliness, pain, confusion) nor episodic memory of what calmed this patient previously. A cognitively-equipped therapeutic robot, by contrast, would anticipate mood shifts via prospection *(forward simulation of likely emotional trajectories)*, recall that music soothed this patient yesterday via episodic memory, and adapt its strategy via metacognition when interventions produce diminishing returns. Insofar as PARO's effectiveness plateaus because it cannot personalise its responses over time, the cognitive gap is not merely theoretical but clinically consequential. Fong, Nourbakhsh and Dautenhahn (2003, p. 145) formalise this gap via Breazeal's taxonomy: PARO occupies the 'social interface' level (human-like cues but "shallow models of social cognition"), whereas Sciutti et al.'s (2023, p. 160) vision of robots "knowing what they are doing and why" demands the 'socially intelligent' level. The distance between these levels is the cognitive deficit assistive robotics must close.

### 1.3.2 Medication Adherence and Daily Living Support

Medication non-adherence imposes substantial costs on healthcare systems, and elderly patients with polypharmacy regimens are particularly vulnerable to missed or incorrect doses. Robots in this domain must navigate a different challenge from therapeutic companionship: trust and cognitive load are latent variables that cannot be directly measured, only inferred from noisy behavioural proxies. Lee and See (2004, p. 54) define trust as "the attitude that an agent will help achieve an individual's goals in a situation characterized by uncertainty and vulnerability"; a definition foregrounding the latent nature that necessitates probabilistic modelling. A user may comply with a medication prompt despite low trust (e.g. time pressure), or indeed refuse despite high trust (e.g. task complexity), and thus the observation alone cannot reliably disambiguate the latent state (Hancock et al., 2011, p. 522).

The Partially Observable Markov Decision Process (POMDP) provides formal machinery for this uncertainty. Chen et al. (2020, p. 6) demonstrate a Trust-POMDP wherein the robot maintains a belief distribution over trust and selects actions that maximise long-term collaboration, showing belief-space planning outperforms fixed strategies. Garcez and Lamb (2023, p. 12389) identify the neuro-symbolic paradigm as the 'third wave' of AI, wherein neural subsystems (e.g. large language models) handle perception whilst symbolic subsystems (e.g. POMDPs) govern temporal reasoning, providing the temporal scaffold stateless systems lack. Nikolaidis, Hsu and Srinivasa (2017, p. 625) provide empirical corroboration: in a collaborative task (n = 69), robots utilising mutual adaptation via a Mixed Observability MDP (modelling human adaptability as a latent variable) were rated significantly more trustworthy than fixed-policy alternatives (U = 180, p = 0.048). This aligns with Hancock et al.'s (2011, p. 522) finding that robot performance attributes are the strongest trust predictors, whilst demonstrating that belief-space planning as advocated by Chen et al. (2020, p. 6) translates into measurable trust gains.

### 1.3.3 Physical Rehabilitation and Mobility

Robotic exoskeletons and assistive manipulators for stroke recovery and mobility support constitute a third application domain. These systems must adapt in real time not only to the patient's physical state (joint angles, muscle activation patterns) but also to their psychological state: motivation, frustration, and fatigue are latent variables that determine whether a patient perseveres or disengages.

Herein, embodied cognition becomes essential. Brooks (1991, p. TODO) argues that intelligence emerges from physical interaction with the environment rather than abstract representation, whereas Fong, Nourbakhsh and Dautenhahn (2003, p. 149) operationalise this as "perturbatory coupling": the more channels of mutual influence between robot and environment, the more embodied the system. A rehabilitation robot therefore occupies a uniquely cognitive niche, as it must sense the patient's body, reason about current capabilities, and adapt accordingly. A purely language-based or screen-based interface cannot achieve this. The cognitive building blocks required (haptic perception, prospective planning of exercise difficulty, episodic memory of the patient's trajectory) thus mandate an embodied cognitive architecture rather than a disembodied controller.

- [ ] ## 1.4. Discussion

### 1.4.1 Challenges

Three challenges impede the deployment of cognitively-capable assistive robots. Firstly, computational intractability: solving POMDPs exactly is PSPACE-complete (Papadimitriou and Tsitsiklis, 1987, p. 448), and the belief simplex grows exponentially with state-space dimensionality. Whilst approximate solvers such as point-based value iteration (Pineau, Gordon and Thrun, 2003, p. 1025; Kaelbling, Littman and Cassandra, 1998, p. 120) and online Monte-Carlo tree search (Silver and Veness, 2010, p. 1) mitigate this, real-time cognitive processing within embodied systems remains an open challenge, particularly when multiple latent variables (trust, load, emotion) must be tracked simultaneously.

Secondly, the measurement problem: trust, cognitive load, and emotional state are latent variables; observations thereof are noisy proxies at best. Hancock et al.'s (2011, p. 522) meta-analysis of 29 studies finds that even the strongest correlates of trust explain only modest variance, whilst Broadbent, Stafford and MacDonald (2009, p. TODO) note that acceptance itself depends on matching robot behaviour to user expectations rather than trust alone. Desai et al. (2013, p. 256) further demonstrate that trust dynamics are non-linear, building slowly through consistent performance but degrading rapidly after errors; and thus a single misclassified observation can cascade into inappropriate action selection. Nikolaidis, Hsu and Srinivasa (2017, p. 627), however, demonstrate that mutual adaptation partially mitigates this fragility: when the robot models human adaptability as a latent variable, trust persists even during strategy disagreements, suggesting the variance Hancock et al. report may stem from studies that treat the human as a static rather than co-adaptive partner.

Finally, adaptation without exploitation: a robot that infers cognitive load could, in principle, time its medication requests to coincide with periods of high vulnerability, thereby maximising compliance at the expense of user autonomy. The reward function governing the POMDP's policy should therefore encode ethical constraints alongside clinical objectives, ensuring that the optimisation target is genuine adherence rather than coerced compliance.

### 1.4.2 Ethical Implications

Assistive robots operating in intimate care spaces (bedrooms, bathrooms, rehabilitation clinics) continuously collect sensitive behavioural data. Facial expressions, vocal patterns, and movement trajectories constitute biometric data, yet regulatory frameworks have not kept pace with deployment. Wachter, Mittelstadt and Floridi (2017, p. TODO) demonstrate (DEMONSTRATE RIGHT WORD HERE?) that even the General Data Protection Regulation provides no enforceable "right to explanation" of automated decisions; a gap particularly concerning in healthcare wherein recommendations directly affect patient wellbeing.

Moreover, over-reliance on assistive robots risks eroding functional independence. If a robot consistently anticipates and pre-empts needs via prospection, the user may disengage from self-directed activity, thereby creating a dependency that contradicts the assistive mandate. Sharkey (2014, p. 6 (VERIFY)) frames this via Nordenfelt's 'Dignity of Identity': "a robot that dealt impersonally with an older person, without knowing or using their name or their preferences would also be likely to negatively affect their feelings of dignity." This implies that only cognitively-equipped robots (those with episodic memory of individual users) can avoid dignity violations; reactive systems such as PARO, notwithstanding their therapeutic benefits (Wada and Shibata, 2007, p. 974), risk infantilisation precisely because they cannot personalise. The responsibility gap compounds this further: when a care robot administers incorrect medication, liability falls ambiguously between manufacturer, deployer, and clinician.

The ethical watchword is therefore proactive regulation: design-stage ethics that anticipate failure modes before deployment, rather than reactive patchwork after harm. Per the embodied cognition thesis, if intelligence indeed requires a body, and that body enters the most intimate spaces of vulnerable persons, then the ethical stakes of assistive cognitive robotics are uniquely high.

- [ ] ## 1.5. Conclusion

Assistive robotics stands at an inflection point. Current systems (PARO, medication prompt robots, rehabilitation aids) deliver measurable benefits within narrow operational envelopes, yet their reactive architectures limit sustained, personalised effectiveness. The Vernon, Metta and Sandini (2007) cognition cycle provides the architectural blueprint for graduating beyond this plateau: assistive robots that anticipate (prospection), remember (episodic and semantic memory), reason about others' mental states (theory of mind), and monitor their own performance (metacognition) would constitute a qualitative advance over the most-capable systems deployed.

The neuro-symbolic paradigm offers a viable path toward this vision, as the Trust-POMDP framework attests (Chen et al., 2020). Sciutti et al. (2023, pp. 162-163) independently identify the integration of learning with model-based approaches as cognitive robotics' most-prominent trajectory; that this converges with Garcez and Lamb's (2023, p. 12389) 'third wave' thesis from AI theory suggests the direction is robust rather than parochial. Future applications will likely extend beyond single-task assistance toward cognitively autonomous home-dwelling companions: robots that proactively monitor health indicators, anticipate daily needs via episodic memory, and adapt their interaction style to the user's evolving cognitive and emotional state. Sharkey and Sharkey (2012, p. 27) identify this trajectory whilst cautioning that such systems risk replacing rather than supplementing human-care, and therefore the field must pursue cognitive capability and ethical governance in concert. Figure~\ref{fig:assistive-trajectory} visualises this trajectory. The ultimate test, per the embodied cognition thesis, is a robot that can sense, remember, anticipate, and adapt within the physical world, whilst respecting the autonomy and dignity of the persons it serves.

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
    {\textbf{Trust-POMDP}\\[-1pt]{\tiny Belief-based; episodic memory;}\\ {\tiny infers latent trust/load}};

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

- [X] [ ] Sciutti, A., Beetz, M., Inamura, T., Korsah, A., Oh, J., Sandini, G., Shimoda, S. and Vernon, D. (2023) 'The Present and the Future of Cognitive Robotics', IEEE Robotics
  & Automation Magazine, 30(3), pp. 160-163. Available at: [https://ieeexplore-ieee-org.plymouth.idm.oclc.org/document/10255092](https://ieeexplore-ieee-org.plymouth.idm.oclc.org/document/10255092) (Accessed: 18 March 2026).
- [ ] [ ] Bemelmans, R., Gelderblom, G. J., Jonker, P. and de Witte, L. (2012) 'Socially assistive robots in elderly care: a systematic review into effects and effectiveness', *Journal of the American Medical Directors Association*, 13(2), pp. 114-120. Available at: https://pubmed.ncbi.nlm.nih.gov/21450215/ (Accessed: 25 March 2026).
- [ ] [ ] Broadbent, E., Stafford, R. and MacDonald, B. (2009) 'Acceptance of Healthcare Robots for the Older Population: Review and Future Directions', *International Journal of Social Robotics*, 1(4), pp. 319-330. Available at: https://link.springer.com/article/10.1007/s12369-009-0030-6 (Accessed: 25 March 2026).
- [ ] [ ] Brooks, R. A. (1991) 'Intelligence without representation', *Artificial Intelligence*, 47(1-3), pp. 139-159. Available at: https://people.csail.mit.edu/brooks/papers/representation.pdf (Accessed: 24 March 2026).
- [ ] [ ] Chen, M., Nikolaidis, S., Soh, H., Hsu, D. and Srinivasa, S. (2020) 'Trust-Aware Decision Making for Human-Robot Collaboration: Model Learning and Planning', *ACM Transactions on Human-Robot Interaction*, 9(2), pp. 1-23. Available at: https://arxiv.org/abs/1801.04099 (Accessed: 15 March 2026).
- [ ] [ ] Desai, M., Kaniarasu, P., Medvedev, M., Steinfeld, A. and Yanco, H. (2013) 'Impact of robot failures and feedback on real-time trust', *Journal of Human-Robot Interaction*, 2(1), pp. 251-275. Available at: https://ieeexplore.ieee.org/document/6483596 (Accessed: 20 March 2026).
- [ ] [ ] Fong, T., Nourbakhsh, I. and Dautenhahn, K. (2003) 'A survey of socially interactive robots', *Robotics and Autonomous Systems*, 42(3-4), pp. 143-166. Available at: https://www.cs.cmu.edu/~illah/PAPERS/socialroboticssurvey.pdf (Accessed: 18 March 2026).
- [ ] [ ] Garcez, A. d'A. and Lamb, L. C. (2023) 'Neurosymbolic AI: The 3rd Wave', *Artificial Intelligence Review*, 56, pp. 12387-12406. Available at: https://link.springer.com/article/10.1007/s10462-023-10448-w (Accessed: 20 March 2026).
- [ ] [ ] Hancock, P. A., Billings, D. R., Schaefer, K. E., Chen, J. Y. C., de Visser, E. J. and Parasuraman, R. (2011) 'A meta-analysis of factors affecting trust in human-robot interaction', *Human Factors*, 53(5), pp. 517-527. Available at: https://journals.sagepub.com/doi/10.1177/0018720811417254 (Accessed: 15 March 2026).
- [ ] [ ] Kaelbling, L. P., Littman, M. L. and Cassandra, A. R. (1998) 'Planning and acting in partially observable stochastic domains', *Artificial Intelligence*, 101(1-2), pp. 99-134. Available at: https://people.csail.mit.edu/lpk/papers/aij98-pomdp.pdf (Accessed: 13 March 2026).
- [ ] [ ] Lee, J. D. and See, K. A. (2004) 'Trust in automation: Designing for appropriate reliance', *Human Factors*, 46(1), pp. 50-80. Available at: https://journals.sagepub.com/doi/10.1518/hfes.46.1.50_30392 (Accessed: 15 March 2026).
- [ ] [ ] Nikolaidis, S., Hsu, D. and Srinivasa, S. (2017) 'Human-robot mutual adaptation in collaborative tasks: Models and experiments', *The International Journal of Robotics Research*, 36(5-7), pp. 618-634. Available at: https://journals.sagepub.com/doi/10.1177/0278364917690593 (Accessed: 20 March 2026).
- [ ] [ ] Papadimitriou, C. H. and Tsitsiklis, J. N. (1987) 'The complexity of Markov decision processes', *Mathematics of Operations Research*, 12(3), pp. 441-450. Available at: https://web.mit.edu/jnt/www/Papers/J016-87-mdp-complexity.pdf (Accessed: 13 March 2026).
- [ ] [ ] Pineau, J., Gordon, G. and Thrun, S. (2003) 'Point-based value iteration: An anytime algorithm for POMDPs', in *Proceedings of the 18th International Joint Conference on Artificial Intelligence (IJCAI-03)*, pp. 1025-1030. Available at: http://www.cs.cmu.edu/~ggordon/jpineau-ggordon-thrun.ijcai03.pdf (Accessed: 24 March 2026).
- [ ] [ ] Sharkey, A. (2014) 'Robots and human dignity: A consideration of the effects of robot care on the dignity of older people', *Ethics and Information Technology*, 16(1), pp. 63-75. Available at: https://philarchive.org/rec/SHARAH-2 (Accessed: 22 March 2026).
- [ ] [ ] Sharkey, A. and Sharkey, N. (2012) 'Granny and the robots: ethical issues in robot care for the elderly', *Ethics and Information Technology*, 14(1), pp. 27-40. Available at: https://philarchive.org/rec/SHAGAT (Accessed: 22 March 2026).
- [ ] [ ] Silver, D. and Veness, J. (2010) 'Monte-Carlo planning in large POMDPs', in *Advances in Neural Information Processing Systems (NeurIPS 23)*, pp. 2164-2172. Available at: https://proceedings.neurips.cc/paper/2010/file/edfbe1afcf9246bb0d40eb4d8027d90f-Paper.pdf (Accessed: 24 March 2026).
- [ ] [ ] Tapus, A., Matarić, M. J. and Scassellati, B. (2007) 'Socially assistive robotics [Grand Challenges of Robotics]', *IEEE Robotics & Automation Magazine*, 14(1), pp. 35-42. Available at: https://scazlab.yale.edu/sites/default/files/files/Tapus-RAM2007.pdf (Accessed: 25 March 2026).
- [ ] [ ] Vernon, D., Metta, G. and Sandini, G. (2007) 'A Survey of Artificial Cognitive Systems: Implications for the Autonomous Development of Mental Capabilities in Computational Agents', *IEEE Transactions on Evolutionary Computation*, 11(2), pp. 151-180. Available at: https://www.robotcub.org/misc/papers/07_Vernon_Metta_Sandini_IEEE.pdf (Accessed: 13 March 2026).
- [ ] [ ] Wachter, S., Mittelstadt, B. and Floridi, L. (2017) 'Why a Right to Explanation of Automated Decision-Making Does Not Exist in the General Data Protection Regulation', *International Data Privacy Law*, 7(2), pp. 76-99. Available at: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2903469 (Accessed: 22 March 2026).
- [ ] [ ] Wada, K. and Shibata, T. (2007) 'Living with seal robots: its sociopsychological and physiological influences on the elderly at a care house', *IEEE Transactions on Robotics*, 23(5), pp. 972-980. Available at: https://ieeexplore.ieee.org/document/4339551 (Accessed: 18 March 2026).

# 2- Task (4) Programming Project

- [ ] ensure code-solution matches `proposal.pdf`

References:

```markdown

### 1. Adaptive Companion / Socially Assistive Role (core concept)

- Tapus, Mataric and Scassellati (2007) -- This is your single most important paper. Socially assistive robotics is precisely what GAZE does: a robot that adapts its behaviour to motivate and coach a user. Their framework for robot-assisted therapy (detecting disengagement, adjusting difficulty) maps almost 1:1 onto your core loop.
- Fong, Nourbakhsh and Dautenhahn (2003) -- Foundational survey on socially interactive robots. Use it to ground GAZE within the broader taxonomy of social robots (companion, assistant, coach).
- Kahn et al. (2008) -- Design patterns for sociality in HRI. Directly supports your robot personality modes (encouraging vs. sarcastic) and the idea of building rapport through game interaction.

### 2. Cognitive Robotics Framework (perceive-attend-anticipate-plan-learn-adapt)

- Sciutti et al. (2023) -- Cite this to justify framing GAZE as a *cognitive* robot. Their definition of cognitive robotics maps onto your 6-point "How is cognitive" section almost verbatim.

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

- Ahn et al. (2022) -- Grounding language in robotic affordances ("SayCan"). Cite to justify connecting an LLM to Pepper's physical capabilities (speech, gestures). The LLM generates the game content, but it must be grounded in what Pepper can actually *do*.
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

- Rios-Martinez et al. (2015) and Joosse et al. (2014) -- Proxemics/navigation. Since Pepper is stationary, these are tangential unless you discuss the seating arrangement/distance.
- Papadimitriou and Tsitsiklis (1987) -- Complexity of MDPs. Only cite if you formally discuss the computational complexity of your adaptive decision-making.
- Metz (2007), Winschiers-Theophilus and Bidwell (2013), Wyche and Steinfield (2016) -- African moral theory / indigenous HCI / technology adoption. Not directly applicable unless you bring in a specific cultural-ethics angle.

```

**Strongest citations for the core GAZE concept: Tapus et al. (2007), Sciutti et al. (2023), Nikolaidis et al. (2017), Ahn et al. (2022), and Smedegaard (2019). These five alone cover the adaptive-assistive role, cognitive framing, mutual adaptation, LLM-robot grounding, and the novelty-engagement challenge.**

- [ ] 'anticipate'

## 2.1. Introduction (10%)

## 2.2. Background (10%; Alfie)

GAZE sits within socially assistive robotics *(the deployment of robots to support users through social interaction rather than physical contact)*; Tapus, Matarić and Scassellati (2007, p. 35) define this sub-field as systems that "assist users through social interaction," thereby distinguishing it from physically assistive platforms such as exoskeletons. Most-current platforms in this domain react to a single input signal, and thus suffer from what might be termed the single-signal problem: a facial-expression classifier alone misreads a resting face as displeasure, whilst a response-time metric alone mistakes thoughtful deliberation for disengagement. Sciutti et al. (2023, p. 160) argue that cognitive robots require "flexible, context-sensitive action, knowing what they are doing and why they are doing it"; this demands multi-signal fusion wherein the system weighs complementary modalities together rather than trusting any one in isolation.

The novelty herein is therefore multi-signal emotional inference: the system simultaneously captures facial expression via a pre-trained CNN (integrated from Workshop 10), response time via a Python timer, and answer correctness via speech-to-text combined with LLM-based answer verification. Crucially, the inference layer operates on more than these three raw inputs; it derives additional temporal signals including rolling correctness *(accuracy over a sliding window of the last five rounds)*, consecutive silence count *(how many rounds the user said nothing or explicitly skipped)*, and consecutive wrong-answer streaks. The engine then fuses all six signals into a single inferred user-state governing all downstream adaptation. This architecture is neurosymbolic per Garcez and Lamb (2023, p. 12389): the neural subsystem (OpenAI GPT-4.1) generates games and dialogue, whilst the symbolic AdaptiveEngine governs state inference and difficulty adjustment via interpretable, hand-coded rules. Grounding LLM output in Pepper's physical affordances *(what the robot can actually do: speak, gesture, illuminate LEDs)* follows the affordance-aware principle advocated by Ahn et al. (2022, p. 1), wherein language models are constrained to actions the robot can perform. Smedegaard (2019, p. 4) further warns that initial engagement with social robots often reflects novelty rather than sustained interest; GAZE's adaptive game-switching mechanism is therefore designed to sustain engagement beyond this novelty phase by responding to inferred disengagement with variety rather than repetition.

## 2.3. Methods & Setup (35%; Alfie)

### 2.3.1 System Architecture

GAZE operates across four sequential layers: 1- INPUT captures three simultaneous signals from the user; 2- PROCESS fuses these via the AdaptiveEngine to infer the user's true emotional-cognitive state; 3- GENERATE constructs a dynamic prompt and dispatches it to OpenAI GPT-4.1 for game and dialogue generation; 4- OUTPUT delivers speech, gestures, and LED feedback on Pepper in parallel. The system runs on a laptop (Python 3.13) connected to Pepper via SSH (paramiko); two dedicated SSH connections are maintained (one for motor, LED, and camera commands; a second exclusively for text-to-speech), thereby enabling gesture and speech to execute concurrently without blocking. All robot-side code executes as Python 2 snippets via `nao_run()`, which escapes the code string and runs it remotely via `exec_command()`. This architectural split means computationally intensive processing (the facial-expression CNN inference, OpenAI API calls, and the entire adaptive-engine decision logic) runs on the laptop, whilst Pepper handles only physical I/O.

### 2.3.2 Input Layer: Three Simultaneous Signals

**1- Facial Expression (vision-based).** A pre-trained CNN from Workshop 10 classifies the user's expression into one of seven categories (Angry, Disgust, Fear, Happy, Neutral, Sad, Surprise) from a 48$\times$48 greyscale face region. The Haar cascade (`haarcascade_frontalface_default.xml`) detects faces via `detectMultiScale(gray, 1.3, 5)`; the largest detected face is selected *(the user sitting directly opposite Pepper)*. Pepper's camera captures a JPEG via `ALPhotoCapture`, transferred to the laptop via SFTP and fed through the same preprocessing pipeline utilised in the workshop: greyscale conversion $\rightarrow$ face detection $\rightarrow$ ROI crop and resize to 48$\times$48 $\rightarrow$ reshape to (1, 48, 48, 1). The model returns both the predicted emotion label and a confidence score; the label feeds into state inference, whilst the confidence is logged for post-session analysis.

**2- Verbal Answer (speech-based).** Pepper records audio via `ALAudioRecorder` with dynamic silence detection. At startup, the system calibrates the ambient noise level *(adapting to the specific room environment)* by sampling `ALAudioDevice.getFrontMicEnergy()` for three seconds and setting the speech threshold as the ambient baseline plus a 200-unit buffer. During recording, the system polls microphone energy at 0.5-second intervals; recording terminates when 1.5 seconds of silence follows detected speech, or a 12-second hard ceiling is reached. If `getFrontMicEnergy()` is unsupported on the lab Pepper's firmware, the system falls back to a safe fixed-duration recording, thereby ensuring the demo never breaks regardless of firmware version. The recorded WAV is transferred via SFTP and transcribed via OpenAI Whisper (`whisper-1`).

**3- Response Time (engagement-based).** A Python timer measures elapsed time from question delivery to answer receipt. This signal captures engagement independently of correctness or expression; a correct answer delivered after 25 seconds of deliberation indicates a fundamentally different user-state from one delivered in 3, and thus warrants different adaptive behaviour.

### 2.3.3 Process Layer: Multi-Signal State Inference

The AdaptiveEngine's `infer_state()` method weighs six signals simultaneously to classify the user into one of five states: *Thriving*, *Comfortable*, *Struggling*, *Frustrated*, or *Disengaged*. The three raw inputs (facial expression, response time, current-round correctness) are supplemented by three derived temporal signals: rolling correctness over the last five rounds, consecutive silence count *(rounds where the user said nothing, "skip", or "I don't know")*, and consecutive wrong-answer streak length. This is the core novelty and wherein multi-signal fusion operates; the inference rules combine these signals in non-obvious, cross-modal ways. For instance: if the camera reads *Angry* but the user answers quickly and correctly, the engine infers *Comfortable* *(it is merely their resting face)*; if the camera reads *Neutral* but response time exceeds the 30-second baseline and rolling correctness falls below 50\%, the triple conjunction triggers *Disengaged*; and if the user has answered incorrectly three rounds consecutively and the camera reads *Sad* or *Fear*, the engine infers *Frustrated* regardless of response speed. Fong, Nourbakhsh and Dautenhahn (2003, p. 148) identify "emotion recognition" as a key capability for socially interactive robots, yet most implementations rely on a single modality; GAZE's weighted multi-signal approach, wherein temporal streaks override or corroborate instantaneous readings, addresses the brittleness that Desai et al. (2013, p. 256) observe when systems depend on singular, noisy observations.

The `decide()` function then maps the inferred state to concrete adaptive actions: difficulty adjustment (easy, medium, hard), game switching (numbers $\leftrightarrow$ letters when the user is frustrated or disengaged), hint provision, encouragement, and tone selection. This maps onto the mutual-adaptation paradigm identified by Nikolaidis, Hsu and Srinivasa (2017, p. 625), wherein the robot adjusts its strategy based on an evolving model of the user rather than following a fixed policy.

### 2.3.4 Generate Layer: Dynamic Prompt Construction

The prompt sent to GPT-4.1 is never static. `build_game_prompt()` assembles it fresh every round from: the current tone instruction, live metrics (rolling correctness percentage, average response time, recent facial expressions, inferred state), adaptive instructions (hints, encouragement, game-switch directives), and a strict JSON response-format specification requiring `dialogue`, `answer`, `category`, and `gesture` fields. Three distinct OpenAI calls serve different purposes at different temperatures: game generation (temp = 0.8 for creative variety), answer verification (temp = 0.0 for deterministic correctness checking), and the therapeutic reframing check-in (temp = 0.7 for empathetic but controlled dialogue). Ji et al. (2023, p. 3) identify hallucination *(the generation of plausible but factually incorrect content)* as a prominent risk of LLM-generated output; the separate answer-verification call at zero temperature mitigates this by treating correctness as a classification task rather than open generation.

### 2.3.5 Output Layer: Aligned Multimodal Response

Speech, gestures, and LED state fire concurrently via threading. A gesture library of seven context-aligned motions *(celebrate, encourage, think, wave, calm, energetic, neutral)* maps to `ALMotion.angleInterpolation()` sequences executed on the motor SSH connection, whilst `ALTextToSpeech` runs on the dedicated TTS connection in a separate thread. LED colours reflect the inferred state (green for *Thriving*, white for *Comfortable*, yellow for *Struggling*, orange for *Frustrated*, blue for *Disengaged*), providing a secondary non-verbal feedback channel. Speech is split into sentence-level segments with 0.4-second inter-sentence pauses packed into a single SSH payload, thereby eliminating per-sentence SSH round-trip overhead that would otherwise ruin the conversational cadence.

### 2.3.6 Adaptation Self-Evaluation and Session Persistence

After each round, `evaluate_adaptation()` assesses whether the previous round's adaptation worked: did a difficulty decrease help a struggling user answer correctly? Did a game switch re-engage a disengaged one? Did encouragement speed up response time? This evaluation is injected into the next prompt as an `ADAPTATION FEEDBACK` block, thereby informing the LLM of the adaptation's outcome so it can adjust its dialogue accordingly. The result is a system that does not merely adapt, but learns whether its adaptations are effective, and communicates that learning to the generation layer. Session progress (round history, difficulty trajectory, correctness log, rewards given) is saved to `gaze_save.json` after every round via progressive save, protecting data against unexpected crashes (laptop battery, SSH timeout) and supporting session resumption on return.

<!-- PRESERVED: The following content (reward functions, personality presets, TikZ figure) is from the earlier POMDP trust-model version of the project, superseded by the GAZE implementation above. Kept for reference; remove before final submission.

The reward function is structured trust maintenance is a precondition for compliance; a naive ratio (e.g. +100 for compliance, -10 for annoyance) would incentivise relentless prompting, whereas state-dependent rewards ensure the robot cannot brute-force adherence at the expense of rapport. An additional repetition penalty discounts any action used consecutively, forcing action diversity. Negative rewards penalise actions mismatched to the user's current state (e.g. assertive prompting when trust is low, lengthy explanations when cognitively overloaded), encoding clinical judgement about when *not* to act.

Crucially, the ratio between encouragement (context-sensitive bonuses) and discouragement (context-sensitive penalties) determines the robot's behavioural attitude. Three configurable personality presets scale these ratios: *cautious* (penalty weight 1.5$\times$, bonus weight 0.8$\times$, load sensitivity 1.5$\times$) produces a patient-first robot that backs off readily under high cognitive load; *balanced* (1.0$\times$ throughout) represents the default; *assertive* (penalty weight 0.7$\times$, bonus weight 1.3$\times$, trust drive 1.3$\times$) pursues compliance more aggressively. The same base reward values and state-action conditions are shared across all three; only the scaling differs. This design permits direct comparison of how reward-ratio tuning shapes emergent behaviour on identical scenarios, thereby isolating the effect of the encouragement-to-discouragement balance on the robot's interaction strategy.

\begin{figure}[H]
\centering
\begin{tikzpicture}
\begin{axis}[
    width=12cm, height=8cm,
    xlabel={\textbf{Trust Level}},
    ylabel={$R(s,\;\texttt{Direct\_Prompt})$},
    xmin=0.5, xmax=3.5,
    ymin=-6, ymax=9,
    xtick={1, 2, 3},
    xticklabels={High, Medium, Low},
    every axis label/.style={font=\sffamily\small},
    every tick label/.style={font=\small\sffamily},
    grid=both,
    grid style={gray!20, thin},
    axis lines=left,
    axis line style={->, thick},
    clip=false,
    legend style={at={(0.03,0.97)}, anchor=north west, font=\scriptsize\sffamily,
                  draw=gray!40, fill=white, fill opacity=0.9},
]

% --- R = 0 reference line ---
\draw[dashed, gray!60, thin] (axis cs: 0.5, 0) -- (axis cs: 3.5, 0)
    node[right, font=\tiny\sffamily\itshape, text=gray] {$R = 0$};

% --- Cautious ---
\addplot[color=blue!70, thick, mark=*, mark size=3pt, mark options={fill=blue!70}]
    coordinates {(1, 5.20) (2, 2.00) (3, -4.50)};
\addlegendentry{Cautious}

% --- Balanced ---
\addplot[color=gray!70, thick, mark=*, mark size=3pt, mark options={fill=gray!70}]
    coordinates {(1, 5.50) (2, 2.00) (3, -3.00)};
\addlegendentry{Balanced}

% --- Assertive ---
\addplot[color=red!70, thick, mark=*, mark size=3pt, mark options={fill=red!70}]
    coordinates {(1, 7.15) (2, 2.60) (3, -2.10)};
\addlegendentry{Assertive}

% --- Delta annotation at Low Trust ---
\draw[<->, red!60, thick] (axis cs: 3.15, -4.50) -- (axis cs: 3.15, -2.10);
\node[font=\tiny\sffamily, text=red!70, anchor=west] at (axis cs: 3.25, -3.30)
    {$\Delta = 2.40$};

% --- Delta annotation at High Trust ---
\draw[<->, red!60, thick] (axis cs: 0.85, 5.20) -- (axis cs: 0.85, 7.15);
\node[font=\tiny\sffamily, text=red!70, anchor=east] at (axis cs: 0.78, 6.18)
    {$\Delta = 1.95$};

% --- Point labels ---
\node[font=\tiny\sffamily, text=blue!70, anchor=south east] at (axis cs: 2.95, -4.50)
    {$-4.50$};
\node[font=\tiny\sffamily, text=red!70, anchor=north west] at (axis cs: 3.05, -2.10)
    {$-2.10$};
\node[font=\tiny\sffamily, text=red!70, anchor=south west] at (axis cs: 1.05, 7.15)
    {$+7.15$};
\node[font=\tiny\sffamily, text=blue!70, anchor=north west] at (axis cs: 1.05, 5.20)
    {$+5.20$};

\end{axis}
\end{tikzpicture}
\caption{Reward for \texttt{Direct\_Prompt} as trust degrades (cognitive load held at Low). The cautious personality penalises assertive action at Low Trust nearly twice as heavily as the assertive personality ($-4.50$ vs $-2.10$), whilst the assertive personality amplifies the bonus at High Trust ($+7.15$ vs $+5.20$). The widening gap at Low Trust demonstrates how penalty-weighted ratios produce a robot that strongly avoids rapport-damaging actions when trust is absent.}
\label{fig:personality-reward}
\end{figure}

All interaction data (belief states, action choices, observations, outcomes) are persisted to a database, enabling cross-session learning and adaptation rather than resetting to ignorance each session; this implements the episodic-semantic memory distinction Vernon (2014) identifies, wherein the robot accumulates generalised knowledge about a specific user over time.
END OF PRESERVED OLD CONTENT -->

## 2.4. Outcome & System Analysis (30%)

## 2.5. Conclusion (10%; Alfie)

GAZE: multi-signal emotional inference *(facial expression, response time, answer correctness, rolling accuracy trends, silence streaks, and consecutive-wrong streaks)* thereby yielding a more robust user-state estimate than any single channel in isolation. The adaptive engine translates the inferred state into concrete actions (difficulty adjustment, game switching, encouragement) and evaluates whether those actions worked; this self-evaluation loop is fed back into the LLM prompt, thereby creating a system that genuinely adapts rather than executing a fixed interaction script. The neurosymbolic architecture *(symbolic AdaptiveEngine governing state inference; neural GPT-4.1 generating dialogue)* aligns with Garcez and Lamb's (2023, p. 12389) 'third wave' thesis, and the affordance-grounded LLM integration ensures generated content remains within Pepper's physical capabilities per Ahn et al. (2022, p. 1). Insofar as the system addresses Smedegaard's (2019, p. 4) novelty-decay concern via adaptive game switching, GAZE represents an approach to sustained engagement rather than transient interaction.

Notwithstanding, several limitations warrant honesty: The facial-expression CNN was not fine-tuned for this deployment context; it is the Workshop 10 model trained on a general facial-expression dataset, and confidence scores under poor lighting or non-frontal angles are expectedly low. The multi-signal inference thresholds (correctness floor of 0.4, response-time baseline of 30 seconds) are hand-coded rather than learned, prioritising interpretability over optimisation; a deliberate design choice, albeit one that limits adaptability to novel user populations. Conversation history grows unboundedly across rounds, and extended sessions may therefore approach OpenAI's token limits. Future work could formalise the hand-coded inference rules as a Partially Observable Markov Decision Process wherein the user's true emotional-cognitive state is a latent variable inferred via belief-space planning (Kaelbling, Littman and Cassandra, 1998, p. 120), and fine-tune the expression model on in-session Pepper captures to improve classification accuracy within the specific deployment environment.

## 2.6 References (5%)

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
ChatGPT & Finding relevant pages to read in the paper \textbf{(A4)} & Few times if the paper is too long \\
\hline
ChatGPT & General conversations via web-search AI about prevalent papers to read about how the topics relates to others' studies \textbf{(A4)} & Few times at the end \\
\hline
\end{tabular}

- [X] I understand that the ownership and responsibility for the academic integrity of this submitted assessment falls with me, the student.
- [X] I confirm that all details provide above are an accurate description of how AI was used for this assessment.
