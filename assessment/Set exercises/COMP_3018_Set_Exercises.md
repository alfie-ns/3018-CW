---
title: "COMP3018: Set Exercises; Human-Robot Interaction (HRI)"
subtitle: "Cultural Differences and Probabilistic Modelling in Human-Robot Interaction"
header-includes:
  - \usepackage{graphicx}
  - \usepackage{caption}
  - \usepackage{tikz}
  - \usetikzlibrary{positioning, arrows.meta, calc}
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
  - \usepackage{amsmath}
  - \usepackage{amssymb}
  - \definecolor{eastcol}{HTML}{4A90D9}
  - \definecolor{westcol}{HTML}{D94A4A}
  - \definecolor{africacol}{HTML}{5CB85C}
  - \definecolor{trustblue}{HTML}{2E5FA1}
  - \definecolor{loadred}{HTML}{C0392B}
  - \definecolor{annotatered}{HTML}{E74C3C}
  - \definecolor{softgray}{HTML}{888888}
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
- [X] test-tex-figures.md (determine which one then improve via gemini)
- [X] too many latex figures i need to only keep 2 of the best ones,  one that I definitely want to keep is the one where it's a chart (prove to me you know what I mean by chart before you start removing them)
- [X] do ALL TODOs throughout the inline text of the mainbody itself
- [X] utilise transcripts insids the learning/
- [ ] Humanise parts distinctly further so it doesn’t just look AI generated etc
- [ ] verify all page numbers.
- [ ] verify all lecture references are correct with deeper review of lecture materials
- [X] see where i can fit in LaTeX things
- [X] Trust-POMPDP diagram
- [X] perhaps model trust in lates diabram? or just latex the fundamental diagtam of POMDP similar to lecture slied in POMDP lectures (10,11)

# Words-To-Use:

- [X] persons
- [X] use `whom`
- [X] `however, insofar as`
- [X] Approach
- [X] `utilise`
- [X] belief
- [X] talk about nolvety effect in lecture 6
- [X] most-{something} {something}
- [X] would-be
- [X] despite
- [X] contravened
  — [X] humanlike
- [X] watchword
- [X] e.g. `1-` , `2-`, ...
- [X] despite x something y
- [X] and `therefore, `x ` thus {does, e.g. *feeds*` `y` continuously throughout the process `wherein`...
- [X] `as now-{something} the x thus does y continously throughout the process wherein it does z`
- [X] `Whilst`: only used at the start of a sentence
- [X] `Whilst this is true, x may be inclinded to {x} based on...`
- [X] `and thus *x* therefore...`
- [X] `thereof`: of the thing just mentioned
- [X] within
- [X] `wherein`: in which
- [X] `regarding, in regard to`, etc
- [X] `likelihood`
- [X] `thereof`:
- [X] `infer`: conclude from reasoning
- [X] `via`: through
- [X] `wherein`: in which
- [X] `indeed`: in fact

# TODO:

- [X] **Lecturer’s Top Insight:** Be a Reviewer; don’t just argue opinions. Validate every critique with evidence from the literature to ensure it is scientific, not personal.
- [X] INTEGRATE ROBOTIC LaTeX DIAGRAM
- [X] 3018-CW/learning/lectures/5 - utilise/lecture.md (**Task 1 insight!!**)
- [X] 3018-CW/learning/lectures/6 - utilise/lecture.md (**General cw insight**)
- [ ] verify page numbers are correct
- [X] hit word-count*0.1 limit allowance across report
- [X] indeed 10% word-count allowance
- [X] uses 3003-report feedback
- [X] utilise lecture teachings in lec 5-6 etc
- [X] review papers: pros or limitations
- [X] peer-reviewed or conference papers
- [X] very good LaTeX visualisations
- [X] get gemini to crituque thus improve the Tikz figure captions
- [ ] FULL PROOF READ
- [ ] final proof read.

# 1- Task (1): Cultural Differences and HRI Design

## 1.1. Cultural Differences in the Acceptance of Robots (Kaplan, 2004)

Kaplan's 2004 identification of East-West fundamental societal divergence is rooted in a two-way observation in terms of how the culture's differences manifest as follows: "**culture affects the way technology is perceived** and, reciprocally, **technological evolution shapes culture in particular ways**" (Kaplan, 2004, p. 465); i.e. the cultural (habits), theological (religious), and mythological narrative of each region shapes the societal meta-layer *(the deeper cultural wiring controlling how a society receives robots)*.

### 1.1.1 Western Society (The Frankenstein Syndrome)

Western culture has persistently viewed the creation of human-like (humanoid) entities slightly suspiciously. Kaplan (2004) identifies this as the "Frankenstein Syndrome": a culturally-filtered conviction wherein "any artificially created humanoid will necessarily turn against his creator at some point" (p. 475).

This anxiety traces to the West's distinction between nature and culture, which posits "no place for hybrids" in such classifications (Kaplan, 2004, p. 470). The Western cultural narrative therefore frames humanoid robots as a challenge to human specificity (p. 478), and thus, a transgression *(a violation of the boundary between what humans create and what humans are)* against the natural order; as result, Western societies have historically envisioned robotic development towards industrial, non-anthropomorphic *(i.e. purely functional; not social)* applications wherein the machine remains a *tool* rather than a would-be social entity (Kaplan, 2004, p. 473). Kaplan further notes the concept of "narcissistic shields" *(the psychological-defence mechanisms protecting human exceptionalism)* (p. 478), whereby Westerners psychologically distance themselves from machines that erode the human-robot distinction.

### 1.1.2 Eastern Society (Technology Taming and Animism)

Japanese culture exhibits a fundamentally different ontological *(the definition of what counts as a being)* stance. Kaplan (2004) traces this to the Shinto tradition (p. 469), wherein the rigid Western boundary between animate and inanimate is dissolved in favour of what Kaplan describes as a "continuous network of beings" (p. 470). In this view, humanoid robots are not perceived as transgressions but instead as natural extensions.

Furthermore, Kaplan discussed the cultural mechanism of "technology taming" i.e. a recurring historical pattern wherein foreign technologies are domesticated via integration into existing cultural frameworks (p. 466). This ethos aligns with the *kata* tradition of formalised practice, where repetition leads to "maximum stability" (p. 470). The popular *Astro Boy* manga franchise (p. 466) exemplifies this domestication narratively: the robot is cast not as a Frankensteinian threat, but as a heroic companion (p. 466). Kaplan references the Amaterasu myth (p. 469) to argue that Japanese cosmology fundamentally lacks the creator-vs-creation antagonism (the inherent transgression of usurping divine privilege) that underpins Western technophobia, saying simply that "in Japan, no gods created human beings" (p. 476). This cultural openness persists into the contemporary era; as established in the module materials, Japanese society is "probably less sensitive to risks that might appear from robots" than the West (Lecture 5).

### 1.1.3 Implications for HRI Design.

The divergent cultural framings dictate interaction design profoundly within HRI; whilst Westerner persons predominantly prefer robots that maintain clear machine identity markers, thereby preserving the 'narcissistic shield' (Kaplan, 2004, p. 478), Eastern users instead welcome human-like anthropomorphic features that align with the animistic expectations established in Section 1.1.2; Lim, Rooksby and Cross (2021, p. 1321) observed this contrasting preference, confirming that culture significantly influences the acceptance of robotic morphology as Korean participants envisioned human-like robots serving as "social company," whereas US participants instead envisioned theirs as "machine-like" extensions of "household appliances".

Whilst this is true, a Western robot-designer may be inclined to impose universal proxemic standards (culturally-defined personal-space boundaries) based on their own norms. However, non-contact cultures such as Japan maintain larger personal-space buffers, whereas contact cultures such as those in Southern Europe tolerate closer approach distances (Joosse, Lohse and Evers, 2014, pp. 1-2); therefore, a culturally-calibrated model must feed local boundaries into its approach-vector calculations, as failing to respect these bounds contravenes user expectations, effectively alienating the would-be companion (Rios-Martinez, Spalanzani and Laugier, 2015, p. 4).

\begin{figure}[H]
\centering
\includegraphics[width=0.75\textwidth]{image/lecture4-proxemic-zones.png}
\caption{Lecture-4 slide illustrating Hall's four proxemic distance zones and their cultural dependence --- noting the distinction between ``high-contact'' and ``low-contact'' cultures (Bartneck et al., 2020).}
\label{fig:lecture4-proxemic-zones}
\end{figure}

Designers should also account for the novelty effect (Figure~\ref{fig:lecture6-novelty-effect}); users for whom the robot represents an entirely novel stimulus exhibit inflated acceptance ratings. The novelty effect, conventionally framed as "a source of noise in need of reduction" and "behavioural disturbances" obscuring the phenomenon under investigation (Smedegaard, 2019, pp. 411-412), thus feeds skewed data, increasing the likelihood of confounding true cultural preference with transient unfamiliarity. The operative principle is therefore cultural relativism: no universal design policy can accommodate fundamentally different ontological commitments, and researchers cannot infer permanent acceptance from early data; instead, the system must evaluate engagement over time.

\begin{figure}[H]
\centering
\includegraphics[width=0.75\textwidth]{image/lecture6-novelty-effect.png}
\caption{Lecture-6 slide defining the novelty effect in HRI and its mitigation via practice sessions.}
\label{fig:lecture6-novelty-effect}
\end{figure}

## 1.2. African Cultural Factors Influencing HRI Design

Kaplan's (2004, Abstract) abstract *confines* the analysis to the East-West axis, framed explicitly as an inquiry into whether robots are "perceived in the same manner in the West and in Japan"; however, a complete account of cultural factors in HRI must address the African context, wherein distinct philosophical and socio-structural dimensions shape the robot's relational acceptance.

### 1.2.1 Ubuntu Philosophy and Communal Identity:

*Ubuntu*: a Southern African philosophical principle that "a person is a person through other persons" (Metz, 2007, p. 323). Whereas Western HRI design foregrounds individual user experience (Lim, Rooksby and Cross, 2021, p. 1308), Ubuntu-driven design would prioritise communal benefit and relational harmony. A robot operating within an Ubuntu-oriented society should therefore be designed to address the *group* rather than the individual, facilitating collective decision-making and shared resource access; an inference drawn from Metz's (2007, pp. 324-326) emphasis on consensus over dissent and communal resource distribution. This contrasts with the individualised personal-assistant paradigm prevalent in Western HRI.

### 1.2.2 Power Distance and Hierarchical Norms:

Cirasa and Conti's (2025, p. 7) scoping review identifies Hofstede's cultural dimensions framework (a model measuring societal values across indices such as Power Distance and individualism) as dimensions that "significantly affect interactions with technology". Addressing the literature gap outside Western and East Asian spheres, Power Distance can be applied to the African context where many societies score high on this dimension, such that hierarchical authority structures strictly govern social interaction.

In regards to HRI, this suggests that robots interacting with users across different social strata must modulate behaviours accordingly (Cirasa and Conti, 2025, p. 3): deferential language and posture when addressing elders or authoritative figures; a more directive interaction-style when assisting in contexts where the robot is perceived as an institutional representative. Failing to encode these hierarchical norms risks violating deeply held social expectations, thereby undermining trust (Hancock et al., 2011, p. 522).

<!-- OLD DRAFT Version 2 of 1.2.2 (superseded by Version 1 above):
### 1.2.2 Power Distance and Hierarchical Norms:

Cirasa and Conti's (2025, p. 7) scoping review identifies Hofstede's cultural dimensions theory as a primary instrument for assessing cultural impact within HRI. Specifically, they note that Hofstede's framework identifies "power distance" alongside four other dimensions "that vary across cultures and significantly affect interactions with technology". Whilst the authors note a scarcity of research "beyond Western and East Asian contexts", it can be inferred that many African societies score high on this `power distance` dimension, wherein hierarchical authority structures heavily govern social interaction.

In regards to HRI, this suggests that robots interacting with users across different social strata (age, social status, or professional role) must *modulate* their behaviour accordingly via utilisation of deferential language and posture when addressing elders or authority figures; and a more directive interaction style when assisting in contexts where the robot is perceived institutionally as a representative. Failing to encode these hierarchical norms risks contravening deeply held social expectations, thereby undermining trust.
-->

### 1.2.3 Oral Tradition and Multimodal Communication:

African cultures historically have preferred oral knowledge transmission over written documentation (Winschiers-Theophilus and Bidwell, 2013, pp. 12-13). This implicates interaction modality, i.e. voice-driven, narrative-based interfaces using speech processing and *prosodic* (rhythmically patterned) features such as pitch and MFCCs (Lecture 3), may achieve higher engagement than text-heavy GUI paradigms. Furthermore, Lecture 2 established that 65% of daily-life communication is nonverbal; thus, gestural and paralinguistic channels become critical design considerations for African contexts wherein oral expressiveness is culturally normative.

### 1.2.4 Infrastructure and Access Constraints:

- [ ] Despite rapid technological growth, many African regions face infrastructure limitations e.g. intermittent connectivity and limited access to high-specification hardware (Wyche and Steinfield, 2016). HRI systems deployed in these contexts must therefore be robust to connectivity loss, operable on low-power devices, and designed for shared rather than personal ownership, aligning with the communal ethos of Ubuntu.

## 1.3 Regional Design Traits (Appearance and Behaviour)

<!-- - [ ] DONE? -->

The cultural factors identified above dictate distinct morphological-and-behavioural traits (how the robot looks and how it acts) to maximise acceptance (Fong, Nourbakhsh and Dautenhahn, 2003, p. 149).

**(a) The East (Japan).** Because Shinto animism dissolves the natural/artificial boundary (Kaplan, 2004), anthropomorphic or highly expressive aesthetic traits are welcomed. However, to align with the *kata* tradition of harmonious form (Kaplan, 2004, p. 470), the robot's movements must be fluid and graceful rather than purely functional. Behaviourally, the robot should adopt a "side-by-side" cooperative posture rather than an imposing face-to-face stance, reflecting Japanese non-tactile proxemic norms requiring larger personal-space buffers (Joosse, Lohse and Evers, 2014, p. 2; Lecture 4). As Lecture 2 establishes, *haptics* (deliberate physical communication) has beneficial effects primarily within the same social group; hence physical touch is replaced by proxemic attentiveness, maintaining Hall's personal zone of 0.45-1.2m (Rios-Martinez, Spalanzani and Laugier, 2015, p. 5, Table 1).

**(b) The West (Europe/North America).** To avoid triggering the Frankenstein Syndrome and to respect the "narcissistic shield" (Kaplan, 2004, p. 478), Western robots should possess functional, machine-like aesthetic markers (visible joints, metallic surfaces) rather than overtly human-like features, clearly signalling artificiality to prevent descent into the uncanny valley (Mori, 1970). Behaviourally, they must exhibit transparency, explicitly stating operational reasoning to alleviate what Kaplan (2004, p. 475) characterises as anxieties of autonomous transgression. The handshake serves as a *symbolic gesture* (a movement with a culturally agreed-upon meaning) combined with *haptics* (Lecture 2), albeit calibrated to the Mediterranean versus Northern European proxemic distinction (Lecture 4).

**(c) Africa.** Informed by Ubuntu and high Power Distance (Cirasa and Conti, 2025), an African-deployed robot should possess a modest physical stature to avoid perceived challenges to human hierarchical authority. Behaviourally, it must be group-facing rather than dyadic, utilising a warm, highly expressive vocal synthesiser capable of rendering the rich prosodic variations (pitch, tone) necessary for an oral-tradition society (Lecture 3; Winschiers-Theophilus and Bidwell, 2013). Furthermore, as Lecture 2 established that "65% of communication is non-verbal," gestural and paralinguistic channels, specifically *beat gestures* (rhythmic hand movements accentuating speech rhythm) and *iconic gestures* (movements visually representing the subject), become critical design considerations.

## 1.4 Adapting Design Patterns for Sociality (Kahn et al., 2008)

Kahn et al. (2008) identify eight design patterns for sociality in HRI, noting the patterns are "likely under-described" (p. 99). These patterns must be regionally adapted using the traits established in Section 1.3:

**Pattern 1: Initial Introduction (Kahn et al., 2008, p. 100).**

- *(a) East:* Rather than tactile handshakes, the robot must initiate interaction with a calibrated bow, as "in Japan it's very considered impolite if you break the personal distance or space and try to touch somebody" (Lecture 4). The bow angle should parametrically encode social hierarchy recognition.
- *(b) West:* The *Initial Introduction* can incorporate the handshake as a tactile greeting, albeit with sensitivity to the Mediterranean (closer) versus Northern European (distant) proxemic distinctions (Lecture 4).
- *(c) Africa:* Reflecting Ubuntu's communal orientation, the introduction must address groups rather than individuals. Encoding Power Distance norms, the robot must always greet the eldest or most-senior member first (Cirasa and Conti, 2025).

**Pattern 4: Personal Interests and History (Kahn et al., 2008, p. 101).**

- *(a) East:* The robot's backstory can elaborately integrate into the animistic expectation of objects possessing a "spirit" or character (Kaplan, 2004).
- *(b) West:* Self-disclosure must be transparently mechanical, framing its "interests" around its programmed purpose to reinforce the user's ontological comfort (Lecture 1).
- *(c) Africa:* This pattern should be realised via storytelling and voice-based dialogue. The robot must establish *joint attention* (the ability of multiple agents to focus on a shared reference point) via structured eye gaze to maintain narrative authority (Lecture 2; Lecture 3).

**Pattern 5: Recovering From Mistakes (Kahn et al., 2008, p. 101).**

- *(a) East:* The robot should employ indirect acknowledgement strategies that preserve social harmony (Kaplan, 2004, p. 470), avoiding direct self-criticism that may cause discomfort via loss of face.
- *(b) West:* The robot should explicitly explain its error and how it will correct it, prioritising transparency to mitigate the underlying technophobia Kaplan (2004, p. 475) identifies.
- *(c) Africa:* Error recovery must be calibrated to social rank; an unacknowledged error affecting an elder constitutes a severe social violation, and thus recovery must involve deferential posture and movement (Lecture 2) to protect the user's social face within the community.

## 1.5 Summary of Cultural Design Implications

\begin{table}[H]
\centering
\small
\caption{Cultural factors and corresponding HRI design adaptations.}
\begin{tabular}{>{\raggedright\arraybackslash}p{2.2cm}
                >{\raggedright\arraybackslash}p{4.5cm}
                >{\raggedright\arraybackslash}p{5.5cm}}
\toprule
\textbf{Region} & \textbf{Key Cultural Factor} & \textbf{Design Adaptation} \\
\midrule
East (Japan) & Shinto animism; non-tactile norms; \textit{kata} tradition & Bowing protocols; enlarged personal-space buffers; indirect error recovery \\
\addlinespace
West & Frankenstein Syndrome; individualism; narcissistic shields & Machine-identity markers; handshake-ready; transparent self-disclosure \\
\addlinespace
Africa & Ubuntu; high Power Distance; oral tradition & Communal greetings; elder-first hierarchy; voice-driven narrative interfaces \\
\bottomrule
\end{tabular}
\end{table}

- [ ] Kahn et al. (2008) concludes: effective HRI must be "compelling as a lived experience" (p. 103) and thus what constitutes a compelling experience is, as demonstrated above, inseparable from the cultural context thereof.

\newpage

# 2- Task (2): POMDPs in Human-Robot Interaction

<!--
- [ ] FIND PEER-REVIEWED CITATIONS: POMDPs (Partially Observable Markov Decision Processes): a mathematical framework for modelling decision-making problems where the agent has incomplete information about the environment state. They extend MDPs by incorporating uncertainty in state observation, making them particularly suitable for HRI scenarios wherein the robot must infer human mental states (§trust, intent, etc) from noisy sensory data. A POMDP is defined by the tuple $\langle S, A, T, R, \Omega, O, \gamma \rangle$, where $S$ is the set of states, $A$ the set of actions, $T$ the transition function, $R$ the reward function, $\Omega$ the set of observations, $O$ the observation function, and $\gamma$ the discount factor.

- [ ] this needs to change as I am going to incorporate an AI API into the robot's system
-->

## 2.1 The Role of POMDPs in Trust, Cooperation, Coordination, and Collaboration

A Partially Observable Markov Decision Process (POMDP) extends the MDP studied in COMP3003 (Lecture 7) by relaxing full state observability: rather than direct access to the true environment state, the robot can only *infer* it via noisy, incomplete observations (Kaelbling, Littman and Cassandra, 1998). Formally, a POMDP is defined by the tuple $\langle S, A, T, R, \Omega, O, \gamma \rangle$, where $S$ is a finite set of states, $A$ the available actions, $T(s, a, s') = P(s' \mid s, a)$ the transition function, $R: S \times A \rightarrow \mathbb{R}$ the reward function, $\Omega$ a finite set of observations, $O(s', a, o) = P(o \mid s', a)$ the observation function, and $\gamma \in [0,1)$ the discount factor.

To understand the POMDP's utility, one must strictly differentiate interaction paradigms as defined in Lecture 1 (Figure~\ref{fig:lecture1-interaction-paradigms}). **Coexistence** involves agents sharing an environment but completing different tasks, requiring only fully-observable physical states to avoid collisions. **Cooperation** involves a shared workspace and complementary tasks. However, true **collaboration** demands a shared workspace and the *exact same shared goal* (Lecture 1). In collaboration, the robot must continuously align its actions with the human's unobservable mental states: trust, intent, cognitive load. Because the robot is fundamentally blind to these latent variables, the POMDP's belief state $b$ becomes the computational prerequisite for graduating from mere coexistence to true collaboration (Chen et al., 2020). Indeed, Nikolaidis et al. (2017, pp. 621-623) demonstrate this empirically via a "Bounded-Memory Adaptation Model" (BAM) wherein the robot maintains a mixed-observability MDP over the human's latent adaptability, showing that mutual adaptation via belief-space planning significantly outperforms fixed strategies.

\begin{figure}[H]
\centering
\includegraphics[width=0.85\textwidth]{image/lecture1-interaction-paradigms.png}
\caption{Lecture-1 slide defining the four HRI interaction paradigms by interdependency: coexistence, cooperation, collaboration, and instruction. The POMDP framework is necessary for graduating beyond coexistence, as collaboration requires modelling the human's unobservable mental states.}
\label{fig:lecture1-interaction-paradigms}
\end{figure}

\begin{figure}[H]
\centering
\begin{tikzpicture}
\begin{axis}[
    width=11cm, height=5.5cm,
    xlabel={Interaction Cycle},
    ylabel={$b(\text{Med Trust, High Load})$},
    xmin=-0.3, xmax=5.5,
    ymin=0, ymax=0.7,
    xtick={0,1,2,3,4,5},
    xticklabels={$t_0$,$t_1$,$t_2$,$t_3$,$t_4$,$t_5$},
    every axis label/.style={font=\small\sffamily},
    every tick label/.style={font=\scriptsize\sffamily},
    grid=none,
    axis lines=left,
    axis line style={->, thick},
]

% Threshold line
\addplot[dashed, loadred!60, thin] coordinates {(-0.3, 0.45) (5.5, 0.45)};
\node[font=\tiny\sffamily, text=loadred!80, anchor=west] at (axis cs: 4.6, 0.48) {$\tau$: Escalate};

% Prior line
\addplot[dashed, softgray, thin] coordinates {(-0.3, 0.167) (5.5, 0.167)};
\node[font=\tiny\sffamily, text=softgray, anchor=west] at (axis cs: 4.6, 0.20) {Prior: $\frac{1}{6}$};

% Belief trajectory
\addplot[color=loadred, very thick, mark=*, mark size=3.5pt] coordinates {
    (0, 0.167) (1, 0.40) (2, 0.52) (3, 0.38) (4, 0.25) (5, 0.15)
};

% Above/below threshold annotations
\node[font=\scriptsize\sffamily\itshape, text=trustblue] at (axis cs: 0.5, 0.33) {Verbal};
\node[font=\scriptsize\sffamily\itshape, text=loadred] at (axis cs: 1.5, 0.55) {Explain};
\node[font=\scriptsize\sffamily\itshape, text=loadred] at (axis cs: 2.5, 0.53) {Assist};
\node[font=\scriptsize\sffamily\itshape, text=trustblue] at (axis cs: 3.5, 0.30) {Verbal};
\node[font=\scriptsize\sffamily\itshape, text=trustblue] at (axis cs: 4.5, 0.12) {Disengage};

% Threshold crossing marker
\draw[annotatered, thick, ->] (axis cs: 1.6, 0.45) -- (axis cs: 1.6, 0.515)
    node[above, font=\tiny\sffamily\bfseries, text=annotatered] {crosses $\tau$};

\end{axis}
\end{tikzpicture}
\caption{Action selection governed by continuous belief thresholds. When the probabilistic belief $b(\text{Med Trust, High Load})$ exceeds the escalation threshold $\tau = 0.45$ at $t_2$, the policy dictates a discrete shift from Verbal\_Remind to Explain\_Benefits, then Offer\_Physical\_Assist. As trust recovers and the belief drops below $\tau$ (from $t_3$), the robot de-escalates accordingly. This mapping of a continuous belief space to discrete optimal actions fundamentally distinguishes the POMDP from threshold-free LLM approaches.}
\label{fig:action-threshold}
\end{figure}

## 2.2 Uncertainty, Belief States, and Decision-Making

Because the true state is hidden, the POMDP agent maintains a **belief state** $b$: a probability distribution over all possible states $S$, where $b(s)$ represents the agent's subjective probability that the environment is in state $s$, such that $\sum_{s \in S} b(s) = 1$. After taking action $a$ and receiving observation $o$, the belief state is updated via **Bayesian filtering**:

$$
b'(s') = \eta \cdot O(s', a, o) \sum_{s \in S} T(s, a, s') \cdot b(s)
$$

 $\eta$ is a normalisation constant ensuring $\sum_{s'} b'(s') = 1$. This update rule captures the core epistemic challenge of HRI: the robot must continuously revise its model of the human's internal state as new and could-be contradictory evidence arrives. As Lecture 3 discussed regarding affective computing, the robot utilises descriptors (e.g., pitch, MFCCs, zero-crossing rate) to extract observations from the human's behaviour, and thus *feeds* these into the belief update process.

The belief state $b$ therefore serves as a **sufficient statistic** for the entire interaction history, compressing all past actions and observations into a single probability vector (Kaelbling, Littman and Cassandra, 1998). This is precisely why the POMDP exhibits a non-Markovian *policy* (each action depends on the full history $h_t$) whilst maintaining a Markovian *belief update* (the next belief $b'$ depends only on the current belief $b$, the action taken, and the observation received); the belief state absorbs all relevant history, and thus the agent need not store raw trajectories to act optimally.

## 2.3 Challenges of Trust Modelling and the POMDP Response

Trust is a latent psychological variable; it cannot be directly measured, only inferred from observable behavioural indicators. Lee and See (2004, p. 54) define trust as "the attitude that an agent will help achieve an individual's goals in a situation characterised by uncertainty and vulnerability"; a definition foregrounding the latent nature that necessitates probabilistic modelling. Three core challenges arise.

### 2.3.1 The Measurement Problem

Observations such as task compliance rate, response latency, gaze direction (Lecture 2), and verbal affirmations are noisy proxies. Hancock et al.'s (2011, p. 520) meta-analysis of 29 empirical studies confirms this, finding that robot performance-based factors exhibit the strongest correlation with trust (mean r = +0.34, p. 522), yet even these explain only modest variance; a user may comply with a robot's suggestion despite low trust (e.g., due to time pressure), or indeed refuse despite high trust (e.g., due to task complexity), and thus the observation alone does not necessarily disambiguate the latent state.

### 2.3.2 Temporal Dynamics

Trust evolves non-linearly, as it builds slowly through consistent performance but degrades rapidly after errors. This asymmetry is empirically confirmed by Desai et al. (2013, p. 256), who found that "recovery of trust after a reliability drop occurs at a slower pace than the pace at which trust develops before reliability drops". The *Recovering From Mistakes* pattern (Kahn et al., 2008, p. 101) is therefore critical: a robot that acknowledges and corrects errors can arrest trust decay, whereas one that ignores failures risks appearing "aggressive" (Lecture 4).

### 2.3.3 Computational Intractability

Solving POMDPs exactly is PSPACE-complete (Papadimitriou and Tsitsiklis, 1987), as the belief simplex is continuous even with finite $|S|$. Practical HRI applications therefore utilise approximate solvers such as PBVI (Pineau, Gordon and Thrun, 2003) or POMCP (Silver and Veness, 2010) to achieve tractable real-time planning.

The POMDP addresses these challenges by encoding trust as a hidden state variable, observations as probabilistic signals thereof, and actions as trust-modulating strategies (Chen et al., 2020); trust is thereby modelled as a continuously-evolving distribution rather than a brittle threshold-based heuristic (a rigid binary switch ignoring subtle fluctuations).

## 2.4 Proposed Neuro-Symbolic POMDP Model: Neo Robot with OpenAI Cognitive Architecture

To concretise this framework, I propose a neuro-symbolic POMDP model for a Neo (Pepper) humanoid robot augmented with an OpenAI multimodal API, deployed as an elderly medication-adherence assistant. LLMs are powerful observation extractors, capable of parsing unstructured human behaviour into structured probabilistic assessments; however, they are inherently stateless (each API call is independent, with no temporal memory) and prone to hallucination (Ji et al., 2023). Wrapping the API inside a POMDP belief state $b(s)$ therefore provides the temporal scaffold the LLM lacks: a continuously-updated model of the human's latent states (Trust, Cognitive Load) persisting across the full interaction. This neuro-symbolic paradigm, wherein a neural subsystem handles perception whilst a symbolic subsystem governs reasoning, represents what Garcez and Lamb (2023, p. 12389) term the 'third wave' of AI. Ahn et al. (2022) demonstrated via SayCan that LLMs can ground language commands in physical robotic affordances, establishing LLM-directed action selection; however, their architecture lacks the temporal belief maintenance that a POMDP provides.

### 2.4.1 The Neuro-Symbolic Architecture

The Neo robot's onboard sensors (camera, microphone array, tactile sensors) capture raw multimodal data from the elderly user, transmitted to the OpenAI multimodal API serving as the **observation function** ($O$). The API processes this stream, analysing facial action units, extracting prosodic descriptors (pitch, MFCCs, zero-crossing rate) from speech (Lecture 3), and interpreting gestural semantics, to output a structured observation $o \in \Omega$. Crucially, the API provides a probability distribution over possible observations rather than a categorical label, thereby preserving the epistemic uncertainty the POMDP requires. Concretely, if the robot performs Verbal\_Remind and the API observes Hesitate, the belief shifts toward medium-trust, high-load states; $\pi^*(b)$ consequently selects Explain\_Benefits rather than escalating to physical assistance (Figure~\ref{fig:action-threshold}), as the belief indicates the user is cognitively loaded rather than non-compliant.

### 2.4.2 Formal Specification

- **State Space** ($S$): Trust $\in \{$Low, Medium, High$\}$ $\times$ Cognitive Load $\in \{$Low, High$\}$, yielding $|S| = 6$.
- **Action Space** ($A$): $\{$Verbal\_Remind, Explain\_Benefits, Offer\_Physical\_Assist, Increase\_Autonomy, Disengage$\}$. The POMDP selects abstract actions; the API translates these into culturally-calibrated language and gestures via the Neo robot.
- **Observation Space** ($\Omega$): $\{$Comply, Hesitate, Verbal\_Refuse, Ignore, Gaze\_Avert$\}$, extracted by the OpenAI API from the raw multimodal stream.
- **Observation Function** ($O$): $P(o \mid s', a)$ is estimated by the API's multimodal inference; e.g. $P(\text{Comply} \mid \text{HighTrust, LowLoad}, \text{Remind}) = 0.8$, derived from the user's facial configuration and vocal tone.
- **Transition Function** ($T$): Models trust dynamics parametrically. An unneeded Offer\_Physical\_Assist violating personal proxemics (Lecture 4) degrades trust: $P(\text{Low} \mid \text{Med}, \text{Assist}) = 0.6$; conversely, a well-timed Explain\_Benefits yields $P(\text{High} \mid \text{Med}, \text{Explain}) = 0.5$.
- **Reward Function** ($R$): Successful medication adherence yields $R = +10$; preserving user autonomy (choosing Increase\_Autonomy when trust is High) yields $R = +3$; unwanted physical assistance incurs $R = -5$, reflecting the social cost of proxemic violation. Furthermore, mirroring the 'cost of listening' penalty inherent to POMDP information-gathering (as in the Tiger problem), the architecture imposes $R = -1$ for each API observation cycle, thereby penalising excessive polling latency. Notably, both $O$ and $R$ must be culturally parametrised per the findings in Task 1; the proxemic penalty, for instance, should be weighted more heavily for non-contact cultures.

\begin{figure}[H]
\centering
\begin{tikzpicture}
\begin{axis}[
    width=11cm, height=6.5cm,
    xlabel={Evidence},
    ylabel={$b(s)$},
    xmin=-0.3, xmax=2.5,
    ymin=0, ymax=0.75,
    xtick={0, 1, 2},
    xticklabels={$t_0$: Prior, $t_1$: After Hesitate, $t_2$: After Comply},
    ytick={0, 0.1, 0.2, 0.33, 0.4, 0.5, 0.6, 0.7},
    yticklabels={0, 0.1, 0.2, $\frac{1}{3}$, 0.4, 0.5, 0.6, 0.7},
    every axis label/.style={font=\small\sffamily},
    every tick label/.style={font=\scriptsize\sffamily},
    grid=none,
    axis lines=left,
    axis line style={->, thick},
]

% Uniform prior reference
\addplot[dashed, softgray, thin] coordinates {(-0.3, 0.333) (2.5, 0.333)};
\node[font=\tiny\sffamily, text=softgray, anchor=west] at (axis cs: 2.05, 0.36) {Prior: $\frac{1}{3}$};

% High Trust (rises then stays high)
\addplot[color=trustblue, very thick, mark=*, mark size=3.5pt] coordinates {
    (0, 0.333) (1, 0.20) (2, 0.52)
};
\node[font=\scriptsize\sffamily, text=trustblue, anchor=south west] at (axis cs: 1.85, 0.53) {High Trust};

% Medium Trust (spikes then drops) — the dominant non-monotonic line
\addplot[color=loadred, very thick, mark=*, mark size=3.5pt] coordinates {
    (0, 0.333) (1, 0.60) (2, 0.28)
};
\node[font=\scriptsize\sffamily, text=loadred, anchor=south] at (axis cs: 0.85, 0.62) {Med Trust};

% Low Trust (drops monotonically)
\addplot[color=softgray, thick, mark=*, mark size=3pt, dashed] coordinates {
    (0, 0.333) (1, 0.20) (2, 0.20)
};
\node[font=\scriptsize\sffamily, text=softgray, anchor=north west] at (axis cs: 1.85, 0.19) {Low Trust};

% Red delta annotation: Med Trust spike at t1
\draw[annotatered, thick, <->] (axis cs: 1.15, 0.333) -- (axis cs: 1.15, 0.59)
    node[midway, right, font=\tiny\sffamily\bfseries, text=annotatered] {+0.27};

% Red delta annotation: Med Trust drop at t2
\draw[annotatered, thick, <->] (axis cs: 2.15, 0.28) -- (axis cs: 2.15, 0.60)
    node[midway, right, font=\tiny\sffamily\bfseries, text=annotatered] {$-$0.32};

\end{axis}
\end{tikzpicture}
\caption{Simplified belief evolution over a three-state trust space. The medium-trust posterior exhibits non-monotonic behaviour, rising sharply after observing Hesitate at $t_1$, then declining upon Comply at $t_2$. These deviations from the uniform prior demonstrate the Bayesian update mechanism inferring hidden trust states from partial observations, consistent with the non-linear trust dynamics described by Lee and See (2004, p. 54).}
\label{fig:belief-evolution}
\end{figure}

### 2.4.3 Benefits and Limitations

The model's strength lies in neuro-symbolic complementarity (Section 2.4). Unlike traditional solvers such as PBVI (Pineau, Gordon and Thrun, 2003) which struggle with high-dimensional unstructured observations, this approach delegates perceptual dimensionality-reduction to the LLM, thereby preserving the tractability of the belief update. However, the architecture introduces several limitations: 1) a fundamental mathematical friction: the POMDP relies on the Markov property with a stationary observation function $O(s', a, o)$, yet the LLM is inherently non-stationary; its outputs depend on a dynamic context window, meaning the observation function shifts based on the LLM's own internal states, and thus the belief update is technically an approximation rather than an exact sufficient statistic. The practical consequence is insidious: if the LLM's interpretation silently shifts (e.g., following an API version update), the belief state degrades without any mechanism to detect this drift; 2) API latency (200-800ms) may disrupt real-time proxemic responsiveness (Lecture 4); 3) the LLM's stochastic nature means identical inputs may yield different observation distributions, introducing unmodelled noise into the Bayesian update; and 4) the observation model may inherit training-data biases, degrading inference accuracy for elderly users if the model was predominantly trained on younger demographics (Lecture 5).

## 2.5 Ethical and Social Implications

By operationalising trust as a now-computable metric, the POMDP risks enabling exploitation: insofar as the reward function solely prioritises compliance, the optimal policy may learn to time requests when inferred cognitive load is highest. Designers must therefore encode user autonomy into the reward structure, lest assistance erode into manipulation. Sharkey (2014, pp. 69-70) frames this via the Capability Approach: the robot must expand rather than impede access to Nussbaum's central capabilities, and thus the $R = +3$ autonomy bonus is not merely a design preference but an ethical imperative encoding that dignity requires preservation of choice.

The OpenAI API introduces three additional ethical dimensions. Firstly, **hallucination risk**: LLMs generate plausible but factually incorrect outputs (Ji et al., 2023); e.g., in a medication-adherence context, misclassifying confused hesitation as willing compliance could trigger inappropriate actions with direct health consequences. Explainable AI (Lecture 5) therefore becomes non-negotiable: the POMDP must justify *why* it selected a particular action, tracing the decision through the belief state to the specific observations extracted. Secondly, **cloud-data sovereignty**: continuous multimodal processing transmitted to third-party servers risks what Sharkey and Sharkey (2012, pp. 35-36) identify as monitoring that infringes on "the right to privacy" (Figure~\ref{fig:lecture5-privacy-surveillance}); the user's most vulnerable moments are thereby streamed to servers whose data-handling policies cannot be meaningfully audited. Finally, **API latency and proxemic violation**: response delays during a time-critical approach may cause the robot to freeze or fail to yield, behaviour Lecture 4 identifies as "aggressive" (Figure~\ref{fig:lecture4-aggressive-robot}). The ethical watchword is therefore proactive regulation (Lecture 5): designers must encode transparent, auditable constraints *ex ante* into both the reward function and the API pipeline, ensuring the robot does not merely *model* trust but actively *earns* it through explainable, privacy-preserving behaviour.

\begin{figure}[H]
\centering
\includegraphics[width=0.75\textwidth]{image/lecture5-privacy-surveillance.png}
\caption{Lecture-5 slide raising the surveillance concern: ``The AI records what you do and transfers data\ldots\ to whom? Company? Third Party?'' --- directly applicable to the cloud-based OpenAI API pipeline proposed in Section 2.4.}
\label{fig:lecture5-privacy-surveillance}
\end{figure}

\begin{figure}[H]
\centering
\includegraphics[width=0.75\textwidth]{image/lecture4-aggressive-robot.png}
\caption{Lecture-4 slide establishing that a robot which fails to yield during spatial approach ``may appear aggressive'' --- with the annotation ``Is this culturally dependent?'' reinforcing the cultural-calibration argument from Section 1.3.}
\label{fig:lecture4-aggressive-robot}
\end{figure}

# Appendices

- [ ] CRITICAL PRE-SUBMISSION TASK: FINISH AI DECLARATION

## References (Peer-reviewed or Conference only)

### Task (1)'s

- [ ] fetch exact wording fron paper to earn second tick
- [ ] [ ] Cirasa, C. and Conti, D. (2025) 'Mapping trust and cultural dimensions in human-robot interaction: a scoping review approach', *Computers in Human Behavior Reports*, 19, article 100763. Available at: [https://doi.org/10.1016/j.chbr.2025.100763](https://doi.org/10.1016/j.chbr.2025.100763) (Accessed: 21 February 2026).
- [ ] [ ] Fong, T., Nourbakhsh, I. and Dautenhahn, K. (2003) 'A survey of socially interactive robots', *Robotics and Autonomous Systems*, 42(3-4), pp. 143-166. Available at: [https://doi.org/10.1016/S0921-8890(02)00372-X](https://doi.org/10.1016/S0921-8890(02)00372-X) (Accessed: 8 March 2026).
- [ ] [ ] Joosse, M., Lohse, M. and Evers, V. (2014) 'Lost in proxemics: spatial behavior for cross-cultural HRI', in Proceedings of the 2014 ACM/IEEE International Conference on Human-Robot Interaction (HRI '14). Bielefeld: ACM/IEEE, pp. 1-6. Available at: [https://doi.org/10.1145/2559636.2559661](https://doi.org/10.1145/2559636.2559661) (Accessed: 19 February 2026).
- [ ] [ ] Kahn, P.H., Freier, N.G., Kanda, T., Ishiguro, H., MacDorman, K.F., Severson, R.L. and Friedman, B. (2008) 'Design patterns for sociality in human-robot interaction', in *Proceedings of the 3rd ACM/IEEE International Conference on Human-Robot Interaction (HRI '08)*. Amsterdam: ACM Press, pp. 97-104. Available at: [https://dl.acm.org/doi/10.1145/1349822.1349836](https://dl.acm.org/doi/10.1145/1349822.1349836) (Accessed: 15 February 2026).
- [ ] [ ] Kaplan, F. (2004) 'Who is afraid of the humanoid? Investigating cultural differences in the acceptance of robots', *International Journal of Humanoid Robotics*, 1(3), pp. 465-480. Available at: [https://doi.org/10.1142/S0219843604000289](https://doi.org/10.1142/S0219843604000289) (Accessed: 15 February 2026).
- [X] [ ] Lim, V., Rooksby, M. and Cross, E.S. (2021) 'Social robots on a global stage: establishing a role for culture during human-robot interaction', International Journal of Social Robotics, 13(6), pp. 1307-1333. Available at: [https://doi.org/10.1007/s12369-020-00710-4](https://doi.org/10.1007/s12369-020-00710-4) (Accessed: 19 February 2026).
- [ ] [ ] Metz, T. (2007) 'Toward an African moral theory', *Journal of Political Philosophy*, 15(3), pp. 321-341. Available at: [https://doi.org/10.1111/j.1467-9760.2007.00280.x](https://doi.org/10.1111/j.1467-9760.2007.00280.x) (Accessed: 15 February 2026).
- [ ] [ ] Mori, M. (1970) 'The uncanny valley', *Energy*, 7(4), pp. 33-35. Translated by MacDorman, K.F. and Kageki, N. (2012) *IEEE Robotics and Automation Magazine*, 19(2), pp. 98-100. Available at: [https://doi.org/10.1109/MRA.2012.2192811](https://doi.org/10.1109/MRA.2012.2192811) (Accessed: 15 February 2026).
- [ ] [ ] Rios-Martinez, J., Spalanzani, A. and Laugier, C. (2015) 'From proxemics theory to socially-aware navigation: a survey', *International Journal of Social Robotics*, 7(2), pp. 137-153. Available at: [https://doi.org/10.1007/s12369-014-0251-1](https://doi.org/10.1007/s12369-014-0251-1) (Accessed: 21 February 2026).
- [X] [ ] Smedegaard, C.V. (2019) 'Reframing the role of novelty within social HRI: from noise to information', in Proceedings of the 14th ACM/IEEE International Conference on Human-Robot Interaction (HRI '19). Daegu: IEEE Press, pp. 411-420. Available at: [https://doi.org/10.1109/HRI.2019.8673167](https://doi.org/10.1109/HRI.2019.8673167) (Accessed: 19 February 2026).
- [ ] [ ] Winschiers-Theophilus, H. and Bidwell, N.J. (2013) 'Toward an Afro-centric indigenous HCI paradigm', *International Journal of Human-Computer Interaction*, 29(4), pp. 243-255. Available at: [https://doi.org/10.1080/10447318.2013.765763](https://doi.org/10.1080/10447318.2013.765763) (Accessed: 21 February 2026).
- [ ] [ ] Wyche, S. and Steinfield, C. (2016) 'Why don't farmers use cell phones to access market prices? Technology affordances and barriers to market information services adoption in rural Kenya', *Information Technology for Development*, 22(2), pp. 320-333. Available at: [https://doi.org/10.1080/02681102.2015.1048184](https://doi.org/10.1080/02681102.2015.1048184) (Accessed: 15 February 2026).

### Task (2)'s

- [ ] fetch exact wording fron paper to earn second tick
- [ ] make alphabetical
- [X] [ ] Ahn, M., Brohan, A., Brown, N. et al. (2022) 'Do As I Can, Not As I Say: Grounding Language in Robotic Affordances', in *Proceedings of the 6th Conference on Robot Learning (CoRL 2022)*. Auckland: PMLR, pp. 287-318. Available at: https://arxiv.org/abs/2204.01691 (Accessed: 18 February 2026).
- [X] [ ] Chen, M., Nikolaidis, S., Soh, H., Hsu, D. and Srinivasa, S. (2020) 'Trust-aware decision making for human-robot collaboration: model learning and planning', *ACM Transactions on Human-Robot Interaction*, 9(2), Article 9. Available at: [https://personalrobotics.cs.washington.edu/publications/chen2019trust.pdf](https://personalrobotics.cs.washington.edu/publications/chen2019trust.pdf) (Accessed: 15 February 2026).
- [X] [ ] Desai, M., Kaniarasu, P., Medber, M., Steinfeld, A. and Yanco, H. (2013) 'Impact of robot failures and feedback on real-time trust', in *Proceedings of the 8th ACM/IEEE International Conference on Human-Robot Interaction (HRI '13)*. Tokyo: IEEE Press, pp. 251-258. Available at: https://doi.org/10.1109/HRI.2013.6483596 (Accessed: 16 February 2026).
- [X] [ ] Garcez, A.d'A. and Lamb, L.C. (2023) 'Neurosymbolic AI: The 3rd Wave', *Artificial Intelligence Review*, 56(11), pp. 12387-12406. Available at: https://doi.org/10.1007/s10462-023-10448-w (Accessed: 18 February 2026).
- [X] [ ] Hancock, P.A., Billings, D.R., Schaefer, K.E., Chen, J.Y.C., de Visser, E.J. and Parasuraman, R. (2011) 'A meta-analysis of factors affecting trust in human-robot interaction', *Human Factors*, 53(5), pp. 517-527. Available at: [https://journals.sagepub.com/doi/10.1177/0018720811417254](https://journals.sagepub.com/doi/10.1177/0018720811417254) (Accessed: 16 February 2026).
- [X] [ ] Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu, Y., Ishii, E., Bang, Y.J., Madotto, A. and Fung, P. (2023) 'Survey of Hallucination in Natural Language Generation', *ACM Computing Surveys*, 55(12), Article 248. Available at: https://doi.org/10.1145/3571730 (Accessed: 18 February 2026).
- [X] [ ] Kaelbling, L.P., Littman, M.L. and Cassandra, A.R. (1998) 'Planning and acting in partially observable stochastic domains', *Artificial Intelligence*, 101(1-2), pp. 99-134. Available at: [https://doi.org/10.1016/S0004-3702(98)00023-X](https://doi.org/10.1016/S0004-3702(98)00023-X) (Accessed: 15 February 2026).
- [X] [ ] Lee, J.D. and See, K.A. (2004) 'Trust in automation: designing for appropriate reliance', *Human Factors*, 46(1), pp. 50-80. Available at: https://doi.org/10.1518/hfes.46.1.50.30392 (Accessed: 16 February 2026).
- [X] [ ] Nikolaidis, S., Hsu, D. and Srinivasa, S. (2017) 'Human-robot mutual adaptation in collaborative tasks: models and experiments', *International Journal of Robotics Research*, 36(5-7), pp. 618-634. Available at: https://doi.org/10.1177/0278364917690593 (Accessed: 16 February 2026).
- [X] [ ] Papadimitriou, C.H. and Tsitsiklis, J.N. (1987) 'The complexity of Markov decision processes', *Mathematics of Operations Research*, 12(3), pp. 441-450. Available at: [https://web.mit.edu/jnt/www/Papers/J016-87-mdp-complexity.pdf](https://web.mit.edu/jnt/www/Papers/J016-87-mdp-complexity.pdf) (Accessed: 15 February 2026).
- [X] [ ] Pineau, J., Gordon, G. and Thrun, S. (2003) 'Point-based value iteration: an anytime algorithm for POMDPs', in *Proceedings of the 18th International Joint Conference on Artificial Intelligence (IJCAI-03)*. Acapulco: Morgan Kaufmann, pp. 1025-1030. Available at: [https://www.ijcai.org/Proceedings/03/Papers/147.pdf](https://www.ijcai.org/Proceedings/03/Papers/147.pdf)(Accessed: 15 February 2026).
- [X] [ ] Sharkey, A. (2014) 'Robots and human dignity: a consideration of the effects of robot care on the dignity of older people', *Ethics and Information Technology*, 16(1), pp. 63-75. Available at: https://doi.org/10.1007/s10676-014-9338-5 (Accessed: 16 February 2026).
- [X] [ ] Sharkey, A. and Sharkey, N. (2012) 'Granny and the robots: ethical issues in robot care for the elderly', *Ethics and Information Technology*, 14(1), pp. 27-40. Available at: https://doi.org/10.1007/s10676-010-9234-6 (Accessed: 16 February 2026).
- [X] [ ] Silver, D. and Veness, J. (2010) 'Monte-Carlo planning in large POMDPs', in *Advances in Neural Information Processing Systems 23 (NeurIPS 2010)*. Vancouver: Curran Associates, pp. 2164-2172. Available at: https://papers.nips.cc/paper/2010/hash/edfbe1afcf9246bb0d40eb4d8027d90f-Abstract.html (Accessed: 15 February 2026).

## Appendix B: AI Declaration

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
ChatGPT & Finding relevant pages to read in the paper \textbf{(A4)} & If the paper takes too long to consume efficiently \\
\hline
ChatGPT & General conversations via web-search AI about how the topic relates to others' studies \textbf{(A4)} & Few times \\
\hline
ChatGPT & Ideas regarding what Tikz diagrams to visualise \textbf{(A4)} & Once \\
\hline
\end{tabular}

- [X] I understand that the ownership and responsibility for the academic integrity of this submitted assessment falls with me, the student.
- [X] I confirm that all details provide above are an accurate description of how AI was used for this assessment.
