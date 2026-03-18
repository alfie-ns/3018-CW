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

## DR ALY QUESTIONS:

- [ ]

---

- [ ] relatively talk about how it relates to others, motivation
- [ ] do all page number TODOs
- [ ] CRAMS figure verified -- 5/6 actions appear (Back_Off absent because true state never sustained Low Trust long enough). Update report Task 4 discussion to: 1) explain why the action timeline shows context-sensitive selection (link each action cluster to the reward territory that produced it), 2) note Back_Off correctly absent given the Medium-trust initial state and stress profile, 3) highlight META-ADAPT triggers (red dotted lines) as evidence of metacognition detecting the stress event within 2 steps
- [X] USE ‘misclassified’
- [ ] consider a project wherein it is ‘cogntive robotics’ (lecture 9) ensure it involves what we have learnt in the labs
- [ ] write code like lecturer in: `3018-cw/learning/workshops/[X] emotional-speech-recognition/solution.py`
- [X] ‘persons’
- [ ] make the robot kinda like how I disucssed you should make it in the set exercises
- [ ] discuss mathematical notiation for the POMDP stuff??? (if not done in set exercises)

  - [ ] maths and diagrams affect wordcount?
  - [ ] Trust-POMPDP diagram
  - [X] Cite: Chen, M., Nikolaidis, S., Soh, H., et al., “Trust-Aware Decision Making for Human-Robot Collaboration: Model Learning and Planning”, ACM Trans. Hum.-Robot Interact., 9(2), 2020
  - [ ] model trust in lates diabram? or     just latex the fundamental diagtam of       POMDP similar to lecture slied in POMDP     lectures (10,11)
  - [ ] latex diagram of continous state in POMDP similar to non-monotnoric graph
  - [ ] utilise lec-7 for POMDP insights; similar to machine learning set exercises where i give a quick breakdown if word count allowance
- [ ] args and kwargs (if i can do this)
- [X] peer-reviewed or conference papers
- [ ] In this section, you should focus on providing enough description of the supervised learning, neural network, and naïve Bayes models.
- [ ] Do not assume the reader knows the basics. Dedicate specific paragraphs to explicitly defining the algorithms and the broader category (Supervised Learning) before diving into your implementation.
- [ ] Then, refer to some studies that have utilised neural networks and naïve Bayes models in your area using the selected database
- [ ] Ensure your literature review in the introduction explicitly cites papers that use your specific dataset (or very similar ones), establishing a clear baseline before you begin

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

Ageing populations and a shrinking care workforce have positioned assistive robotics *(the deployment of robotic systems to support humans with physical, cognitive, or social impairments in activities of daily living)* as a prominent technological response to a widening care gap. Robots now administer medication reminders, facilitate rehabilitation exercises, and provide therapeutic companionship in both clinical and domestic settings. Measurably: reduced caregiver burden, improved patient outcomes in controlled trials, and increased social engagement among isolated elderly residents.

However, most-current assistive robots operate at what Cangelosi and Asada (in press, Chapter 1) term the social layer: they react to immediate stimuli but lack the cognitive depth to anticipate user needs, remember past interactions, or reason about their own performance. Sandini, Sciutti and Vernon (2021, p. {TODO}) argue that genuinely effective assistive robots must be *cognitive*: capable of "flexible, context-sensitive action, knowing what they are doing and why they are doing it." Vernon (2014, p. {TODO}) formalises this requirement via a cognition cycle wherein the agent anticipates, learns, and adapts, intersecting these processes with perception and action to achieve autonomy. This essay contends that assistive robotics must graduate from reactive social behaviour to cognitive capability (intelligence deployed *over* the social layer, not vice versa) if it is to deliver sustained, personalised support. The following sections survey the theoretical foundations thereof, evaluate prominent applications through this cognitive lens, discuss the challenges and ethical implications that arise, and identify future directions for the field.

- [ ] ## 1.2. Literature Review

Cognitive robotics, as defined by Cangelosi and Asada ({TODO date}, Chapter 1), lies at the intersection of Robotics, Artificial Intelligence, and Cognitive and Biological Sciences, combining "sensorimotor behaviour, higher-level functions, and social capabilities of an intelligent robot." This interdisciplinary grounding distinguishes it from conventional robotics *(which treats the robot as purely engineered)* and from social robotics *(which addresses interaction behaviour without necessarily modelling the underlying cognitive processes)*. The distinction is consequential: a robot that smiles when a patient smiles is social; a robot that infers *why* the patient is smiling, and adjusts its future strategy accordingly, is cognitive.

Vernon (2014, TODO) synthesises the field's definitional plurality into a core cycle. The European Network for Advancement of Artificial Cognitive Systems (euCognition) catalogued 42 distinct definitions of cognition, yet the common thread across all is: "we anticipate, we learn, we adapt, and we intersect this with perception and action to create autonomy." This cycle provides an architectural checklist for assistive robots: a system that cannot anticipate the outcome of its actions *(prospection)*, learn from past interactions *(memory)*, or adapt its strategy when performance declines *(metacognition)* is, per this framework, not yet cognitive. Sandini, Sciutti and Vernon (2021) further specify that cognitive robots must "reason about own actions and actions of interaction partners"; a capacity termed *theory of mind*, wherein the agent infers another's latent mental state from observable behaviour alone.

Memory, moreover, is not monolithic. Vernon (2014) distinguishes *episodic memory* *(records of specific past experiences and their contextual outcomes)* from *semantic memory* *(general knowledge about the world, including spatial relationships and factual constraints)*. An assistive medication robot, for instance, needs episodic memory to recall that a particular user refused medication after a restless night, and semantic memory to know that certain drugs cannot be co-administered. Whilst the 42-definitions problem confirms the field lacks consensus on what cognition per se *is*, the common thread (anticipation, learning, adaptation) is precisely what effective assistive robotics demands.

- [ ] ## 1.3. Applications

### 1.3.1 Therapeutic and Emotional Support

The PARO therapeutic seal robot represents one of the most-widely deployed assistive platforms in elderly care. Wada and Shibata (2007, p. 974) demonstrate that PARO reduces agitation and improves mood in patients with dementia, utilising tactile sensors and basic auditory processing to modulate its behaviour in response to stroking and vocal stimulation. Clinical trials report reduced cortisol levels and increased social engagement among residents in long-term care facilities, and the platform has indeed been adopted in care homes across Japan, Europe, and the United States.

Notwithstanding these benefits, PARO operates entirely at the reactive layer. It possesses no theory of mind (it cannot infer *why* a patient is agitated: loneliness, pain, confusion) nor episodic memory of what calmed this specific patient previously. A cognitively-equipped therapeutic robot, by contrast, would anticipate mood shifts via prospection *(forward simulation of likely emotional trajectories)*, recall that music soothed this patient yesterday via episodic memory, and adapt its strategy via metacognition when repeated interventions produce diminishing returns. Insofar as PARO's effectiveness plateaus because it cannot personalise its responses over time, the cognitive gap is not merely theoretical but clinically consequential.

### 1.3.2 Medication Adherence and Daily Living Support

Medication non-adherence imposes substantial costs on healthcare systems, and elderly patients with polypharmacy regimens are particularly vulnerable to missed or incorrect doses. Assistive robots deployed in this domain must navigate a fundamentally different challenge from therapeutic companionship: trust and cognitive load are latent psychological variables that cannot be directly measured, only inferred from noisy behavioural proxies. Lee and See (2004, p. 54) define trust as "the attitude that an agent will help achieve an individual's goals in a situation characterized by uncertainty and vulnerability"; a definition foregrounding the latent nature that necessitates probabilistic modelling. A user may comply with a medication prompt despite low trust (e.g. time pressure), or indeed refuse despite high trust (e.g. task complexity), and thus the observation alone does not necessarily disambiguate the latent state (Hancock et al., 2011, p. 522).

The Partially Observable Markov Decision Process (POMDP) provides the formal machinery to address this uncertainty. Chen et al. (2020, p. 6) demonstrate a Trust-POMDP wherein the robot maintains a probabilistic belief distribution over the human's trust level and selects actions that maximise long-term collaboration, showing that belief-space planning significantly outperforms fixed strategies. Garcez and Lamb (2023, p. 12389) identify the neuro-symbolic paradigm as the 'third wave' of AI, wherein neural subsystems (e.g. large language models) handle perception whilst symbolic subsystems (e.g. POMDPs) govern temporal reasoning, thereby providing the temporal scaffold that stateless reactive systems lack.

### 1.3.3 Physical Rehabilitation and Mobility

Robotic exoskeletons and assistive manipulators for stroke recovery and mobility support constitute a third prominent application domain. These systems must adapt in real time not only to the patient's physical state (joint angles, muscle activation patterns) but also to their psychological state: motivation, frustration, and fatigue are latent variables that determine whether a patient perseveres with a rehabilitation exercise or disengages entirely.

Herein, the concept of embodied cognition becomes essential. Pfeifer and Bongard (2007) argue that intelligence is fundamentally shaped by physical interaction with the environment; a rehabilitation robot therefore occupies a uniquely cognitive niche, as it must sense the patient's body, reason about current capabilities, and adapt its assistance accordingly. A purely language-based or screen-based interface cannot achieve this. The cognitive building blocks required (haptic perception, prospective planning of exercise difficulty, episodic memory of the patient's progress trajectory) thus mandate an embodied cognitive architecture rather than a disembodied reactive controller.

- [ ] ## 1.4. Discussion

### 1.4.1 Challenges

Three challenges impede the deployment of cognitively-capable assistive robots. First, computational intractability: solving POMDPs exactly is PSPACE-complete (Papadimitriou and Tsitsiklis, 1987, p. 448), and the continuous belief simplex grows exponentially with state-space dimensionality. Whilst approximate solvers such as point-based value iteration (Kaelbling, Littman and Cassandra, 1998, p. 120) and online tree search mitigate this, real-time cognitive processing within embodied systems remains an open engineering challenge, particularly when multiple latent variables (trust, load, emotion) must be tracked simultaneously.

Second, the measurement problem: trust, cognitive load, and emotional state are latent variables; observations thereof are noisy proxies at best. Hancock et al.'s (2011, p. 522) meta-analysis of 29 empirical studies finds that even the strongest correlates of trust explain only modest variance. Desai et al. (2013, p. 256) further demonstrate that trust dynamics are non-linear, building slowly through consistent performance but degrading rapidly after errors; and thus a single misclassified observation can cascade into inappropriate action selection.

Third, adaptation without exploitation: a robot that infers cognitive load could, in principle, time its medication requests to coincide with periods of high vulnerability, thereby maximising compliance at the expense of user autonomy. The reward function governing the POMDP's policy must therefore encode ethical constraints alongside clinical objectives, ensuring that the optimisation target is genuine adherence rather than coerced compliance.

### 1.4.2 Ethical Implications

Assistive robots operating in intimate care spaces (bedrooms, bathrooms, rehabilitation clinics) collect sensitive behavioural data continuously. Facial expressions, vocal patterns, and movement trajectories constitute biometric data, yet regulatory frameworks have not kept pace with the technology's deployment. Wachter, Mittelstadt and Floridi (2017) demonstrate that even the General Data Protection Regulation provides no enforceable "right to explanation" of automated decisions; a gap that is particularly concerning in healthcare contexts wherein algorithmic recommendations may directly affect patient wellbeing.

Moreover, over-reliance on assistive robots risks eroding the user's functional independence. If a robot consistently anticipates and pre-empts the user's needs via prospection, the user may disengage from self-directed activity, thereby creating a dependency that contradicts the assistive mandate. The responsibility gap compounds this: when a care robot administers incorrect medication, legal liability falls ambiguously between manufacturer, deploying institution, and supervising clinician.

The ethical watchword is therefore proactive regulation: design-stage ethics that anticipate failure modes before deployment, rather than reactive patchwork after harm has occurred. Connecting this to the embodied cognition thesis, if intelligence indeed requires a body, and that body enters the most intimate spaces of vulnerable persons, then the ethical stakes of assistive cognitive robotics are uniquely and inherently high.

- [ ] ## 1.5. Conclusion

Assistive robotics stands at an inflection point. Current systems (PARO, basic medication prompt robots, simple rehabilitation aids) deliver measurable benefits within narrow operational envelopes, yet their reactive architectures limit sustained, personalised effectiveness. The Vernon (2014) cognition cycle provides the architectural blueprint for graduating beyond this plateau: assistive robots that anticipate (prospection), remember (episodic and semantic memory), reason about others' mental states (theory of mind), and monitor their own performance (metacognition) would constitute a qualitative advance over the most-capable systems presently deployed.

The neuro-symbolic paradigm offers a technically viable path toward this vision, as the Trust-POMDP framework demonstrated in medication adherence applications attests (Chen et al., 2020). Future applications will likely extend beyond single-task assistance toward cognitively autonomous home-dwelling companions: robots that proactively monitor health indicators, anticipate daily living needs via episodic memory, and adapt their interaction style to the user's evolving cognitive and emotional state. Sharkey and Sharkey (2012, p. 27) identify this trajectory whilst cautioning that such systems risk replacing rather than supplementing human care, and therefore the field must pursue cognitive capability and ethical governance in concert. Figure~\ref{fig:assistive-trajectory} visualises this trajectory. The ultimate test, per the embodied cognition thesis, is a robot that can sense, remember, anticipate, and adapt within the physical world, whilst respecting the autonomy and dignity of the persons it serves.

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
    {Vernon (2014) cognition cycle building blocks $\longrightarrow$};

% --- Ethical caution annotation ---
\draw[-{Stealth[length=3pt]}, dashed, red!60, thin] (axis cs: 2.9, 2.3) -- (axis cs: 2.9, 2.65);
\node[font=\tiny\sffamily, text=red!70, anchor=west, text width=2.8cm] at (axis cs: 3.0, 2.3)
    {Sharkey \& Sharkey\\(2012): risk of\\replacing human care};

\end{axis}
\end{tikzpicture}
\caption{Trajectory of assistive robotics from reactive single-task systems (PARO) through adaptive belief-based architectures (Trust-POMDP) toward cognitively autonomous home-dwelling companions. Expanding assistive scope without expanding cognitive capability is insufficient; the diagonal trajectory requires both.}
\label{fig:assistive-trajectory}
\end{figure}

- [ ] ## Task-3 References
- [ ] Cangelosi, A. and Asada, M. (in press) *Cognitive Robotics*, Chapter 1. Cambridge, MA: MIT Press.
- [ ] Chen, M., Nikolaidis, S., Soh, H., Hsu, D. and Srinivasa, S. (2020) 'Trust-Aware Decision Making for Human-Robot Collaboration: Model Learning and Planning', *ACM Transactions on Human-Robot Interaction*, 9(2), pp. 1-23.
- [ ] Desai, M., Kaniarasu, P., Medvedev, M., Steinfeld, A. and Yanco, H. (2013) 'Impact of robot failures and feedback on real-time trust', *Journal of Human-Robot Interaction*, 2(1), pp. 251-275.
- [ ] Garcez, A. d'A. and Lamb, L. C. (2023) 'Neurosymbolic AI: The 3rd Wave', *Artificial Intelligence Review*, 56, pp. 12387-12406.
- [ ] Hancock, P. A., Billings, D. R., Schaefer, K. E., Chen, J. Y. C., de Visser, E. J. and Parasuraman, R. (2011) 'A meta-analysis of factors affecting trust in human-robot interaction', *Human Factors*, 53(5), pp. 517-527.
- [ ] Kaelbling, L. P., Littman, M. L. and Cassandra, A. R. (1998) 'Planning and acting in partially observable stochastic domains', *Artificial Intelligence*, 101(1-2), pp. 99-134.
- [ ] Lee, J. D. and See, K. A. (2004) 'Trust in automation: Designing for appropriate reliance', *Human Factors*, 46(1), pp. 50-80.
- [ ] Papadimitriou, C. H. and Tsitsiklis, J. N. (1987) 'The complexity of Markov decision processes', *Mathematics of Operations Research*, 12(3), pp. 441-450.
- [ ] Pfeifer, R. and Bongard, J. (2007) *How the Body Shapes the Way We Think: A New View of Intelligence*. Cambridge, MA: MIT Press.
- [ ] Sandini, G., Sciutti, A. and Vernon, D. (2021) 'Cognitive Robotics', in Ang, M., Khatib, O. and Siciliano, B. (eds.) *Encyclopedia of Robotics*. Berlin: Springer.
- [ ] Sharkey, A. and Sharkey, N. (2012) 'Granny and the robots: ethical issues in robot care for the elderly', *Ethics and Information Technology*, 14(1), pp. 27-40.
- [ ] Vernon, D. (2014) *Artificial Cognitive Systems: A Primer*. Cambridge, MA: MIT Press.
- [ ] Wachter, S., Mittelstadt, B. and Floridi, L. (2017) 'Why a Right to Explanation of Automated Decision-Making Does Not Exist in the General Data Protection Regulation', *International Data Privacy Law*, 7(2), pp. 76-99.
- [ ] Wada, K. and Shibata, T. (2007) 'Living with seal robots: its sociopsychological and physiological influences on the elderly at a care house', *IEEE Transactions on Robotics*, 23(5), pp. 972-980.

# 2- Task (4) Programming Project

## 2.1. Introduction (10%)

## 2.2. Background (10%)

## 2.3. Methods & Setup (35%)

The reward function is structured such that trust maintenance is a precondition for compliance; a naive ratio (e.g. +100 for compliance, -10 for annoyance) would incentivise relentless prompting, whereas state-dependent rewards ensure the robot cannot brute-force adherence at the expense of rapport. An additional repetition penalty discounts any action used consecutively, forcing action diversity. Negative rewards penalise actions mismatched to the user's current state (e.g. assertive prompting when trust is low, lengthy explanations when cognitively overloaded), encoding clinical judgement about when *not* to act.

All interaction data (belief states, action choices, observations, outcomes) are persisted to a database, enabling cross-session learning and adaptation rather than resetting to ignorance each session; this implements the episodic-semantic memory distinction Vernon (2014) identifies, wherein the robot accumulates generalised knowledge about a specific user over time.

## 2.4. Outcome & System Analysis (30%)

## 2.5. Conclusion (10%)

## 2.6. References (5%)

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
