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

# CRITICAL PRE-SUBMISSION CHECKLIST:

- [ ] remove all construction-type stuff eg checkboxs, TODOs, etc before submission

- [ ] Humanise parts distinctly further

- [ ] final proof read.

# 1- Task (1): Cultural Differences and HRI Design

## 1.1. Cultural Differences in the Acceptance of Robots (Kaplan, 2004)

Kaplan (2004) identifies a two-way East-West societal divergence: "Culture affects the way technology is perceived and, in a reciprocal manner, technological evolution shapes culture in particular ways." (*.pdf*-p. 1); i.e. the cultural, theological, and mythological narrative of each region shapes the societal meta-layer *(the deeper cultural wiring controlling how a society receives robots)*.

### 1.1.1 Western Society (The Frankenstein Syndrome)

Western culture has persistently viewed the creation of human-like (humanoid) entities quite suspiciously. Kaplan (2004) identifies this as the '"Frankenstein syndrome": any artificially created humanoid will necessarily turn against his creator at some point' (p. 11, section-4.3, line-7).

This anxiety traces to the West's distinction between nature and culture, which posits "no place for hybrids" in such classifications (Kaplan, 2004, p. 6, section-3.2 line-21). The Western cultural narrative therefore frames humanoid robots as a challenge to human specificity (p. 14, section-5.2, lines-4-6), and thus, a transgression *(violation of the boundary between what humans create, and what humans are)* against the natural order; as result, the convergence of humans and machines remains "both fascinating and frightening" (Kaplan, 2004, p. 15, section-6, lines-36-37), wherein the machine is culturally positioned as a functional instrument rather than a would-be social entity. Kaplan further notes the concept of "narcissistic shields" *(the psychological-defence mechanisms protecting human exceptionalism)* (p. 14, section-5.2, lines-10-11), whereby Westerners psychologically distance themselves from machines that erode the human-robot distinction.

### 1.1.2 Eastern Society (Technology Taming and Animism)

Japanese culture exhibits a fundamentally different ontological *(the definition of what counts as a being)* stance. Kaplan (2004) traces this to the Shinto tradition (p. 5, section-3, lines-2-11), wherein the rigid Western boundary between animate and inanimate is dissolved in favour of what Kaplan describes as a "continuous network of beings" (p. 6, section-3.2, lines-24-25). In this view, humanoid robots are not perceived as transgressions but instead as natural extensions.

Furthermore, Kaplan discussed the cultural mechanism of "technology taming" i.e. a recurring historical pattern wherein foreign technologies are domesticated via integration into existing cultural frameworks (p. 2, section-1, lines-8-9). This ethos aligns with the *kata* tradition of formalised practice, where repetition leads to "maximum stability" (p. 6, section-3.1, line-4). The popular *Astro Boy* manga franchise (p. 2, section-2.1, lines-24-35) exemplifies this domestication narratively. Kaplan references the Amaterasu myth (p. 5, section-3, lines-2-11) to argue that Japanese cosmology fundamentally lacks the creator-vs-creation antagonism (the inherent transgression of usurping divine privilege) that underpins Western technophobia, saying simply that "in Japan, no gods created human beings" (p. 12, section-4.4, line-20). This cultural openness persists into the contemporary era; as established in the module materials, Japanese society is "probably less sensitive to risks that might appear from robots" than the West (Lecture 5).

### 1.1.3 Implications for HRI Design

The divergent cultural framings dictate interaction design profoundly within HRI; whilst Western persons predominantly prefer robots that maintain clear machine identity markers, thereby preserving the 'narcissistic shield' (Kaplan, 2004, p. 14, section-5.2, lines-10-11), Eastern users instead welcome human-like (anthropomorphic) features that align with the animistic expectations established in Section 1.1.2; Lim, Rooksby and Cross (2021, p. 1321) observed this contrasting preference, confirming that culture significantly influences the acceptance of robotic morphology as Korean participants envisioned human-like robots serving as "social company," whereas US participants instead envisioned theirs as "machine-like" extensions of "household appliances".

Whilst this is true, a Western robot-designer may be inclined to impose universal proxemic standards (culturally-defined personal-space boundaries) based on their own norms. However, non-contact cultures such as Japan maintain larger personal-space buffers, whereas contact cultures such as those in Southern Europe tolerate closer approach distances (Joosse, Lohse and Evers, 2014, pp. 1-2); therefore, a culturally-calibrated model must feed local boundaries into its approach-vector calculations, as failing to respect these bounds contravenes user expectations, effectively alienating the would-be companion (Rios-Martinez, Spalanzani and Laugier, 2015, p. 140).

\begin{figure}[H]
\centering
\includegraphics[width=0.75\textwidth]{image/lecture4-proxemic-zones.png}
\caption{Lecture-4 slide illustrating Hall's four proxemic distance zones and their cultural dependence.}
\label{fig:lecture4-proxemic-zones}
\end{figure}

Designers should also account for the novelty effect (Figure~\ref{fig:lecture6-novelty-effect}); users for whom the robot represents an entirely novel stimulus exhibit inflated acceptance ratings. The novelty effect, conventionally framed as "a source of noise in need of reduction" and "behavioural disturbances" obscuring the phenomenon under investigation (Smedegaard, 2019, pp. 411-412; Lecture 6), thus confounds true cultural preference with transient unfamiliarity. The operative principle is therefore cultural relativism: researchers cannot infer permanent acceptance from early data; instead, the system must evaluate engagement over time.

\begin{figure}[H]
\centering
\includegraphics[width=0.75\textwidth]{image/lecture6-novelty-effect.png}
\caption{Lecture-6 slide defining the novelty effect in HRI and its mitigation via practice sessions.}
\label{fig:lecture6-novelty-effect}
\end{figure}

## 1.2. African Cultural Factors Influencing HRI Design

Kaplan's (2004, Abstract) *confines* the analysis to the East-West axis, framed explicitly as an inquiry into whether robots are "perceived in the same manner in the West and in Japan"; however, a complete account should address the African context.

### 1.2.1 Ubuntu Philosophy and Communal Identity:

*Ubuntu*: a Southern African philosophical principle that "a person is a person through other persons" (Metz, 2007, p. 323). Whereas Western HRI design foregrounds individual user experience (Lim, Rooksby and Cross, 2021, p. 1325), Ubuntu-driven design would prioritise communal benefit and relational harmony. A robot operating within an Ubuntu-oriented society should therefore be designed to address the *group* rather than the individual, facilitating collective decision-making and shared resource access; an inference drawn from Metz's (2007, pp. 324-326) emphasis on consensus over dissent and communal resource distribution. This contrasts with the individualised personal-assistant paradigm prevalent in Western HRI.

### 1.2.2 Power Distance and Hierarchical Norms:

Cirasa and Conti's (2025, p. 7) scoping review identifies Hofstede's cultural dimensions framework (a model measuring societal values across indices such as Power Distance and individualism) as dimensions that "significantly affect interactions with technology". Addressing the literature gap outside Western and East Asian spheres, Power Distance can be applied to the African context where societies such as Nigeria and Ghana score high on this dimension, such that hierarchical authority structures strictly govern social interaction.

In regards to HRI, this suggests that robots interacting with users across different social strata must modulate behaviours accordingly (Cirasa and Conti, 2025, p. 7): deferential language and posture when addressing elders or authoritative figures; a more directive interaction-style when assisting in contexts where the robot is perceived as an institutional representative. Failing to encode these hierarchical norms risks violating deeply held social expectations, thereby undermining trust (Hancock et al., 2011, p. 518).

### 1.2.3 Oral Tradition and Multimodal Communication:

African cultures historically have preferred oral knowledge transmission over written documentation (Winschiers-Theophilus and Bidwell, 2013, *.pdf's*-pp. 12-13). This implicates interaction modality, i.e. voice-driven, narrative-based interfaces using speech processing and *prosodic* (tonal) features such as pitch and MFCCs (Lecture 3), may achieve higher engagement than text-heavy GUI paradigms. Furthermore, Lecture 2 established that 65% of daily-life communication is nonverbal; thus, gestural and paralinguistic channels become critical design considerations for African contexts wherein oral expressiveness is culturally normative.

### 1.2.4 Infrastructure and Access Constraints:

Despite rapid technological growth, many African regions face infrastructure limitations e.g. intermittent connectivity and limited access to high-specification hardware (Wyche and Steinfield, 2016, p. 327). HRI systems deployed in these contexts must therefore be robust to connectivity loss, operable on low-power devices, and designed for shared rather than personal ownership, aligning with the communal ethos of Ubuntu.

## 1.3 Regional Design Traits (Appearance and Behaviour)

The cultural factors identified above dictate distinct morphological-and-behavioural traits (how the robot looks and how it acts) to maximise acceptance (Fong, Nourbakhsh and Dautenhahn, 2003, p. 149).

**(a) The East (Japan).** Because Shinto animism dissolves the natural/artificial boundary (Kaplan, 2004, p. 6, section-3.2, lines-14-15), anthropomorphic or highly expressive aesthetic traits are welcomed. However, to align with the *kata* tradition of harmonious form (Kaplan, 2004, p. 6, section-3.1, lines-2-4), the robot's movements need to be fluid and graceful rather than purely functional. Behaviourally, the robot should adopt a "side-by-side" cooperative posture rather than an imposing face-to-face stance, reflecting Japanese non-tactile proxemic norms requiring larger personal-space buffers (Joosse, Lohse and Evers, 2014, p. 2 & Lecture 4). As Lecture 2 establishes, *haptics* (deliberate physical communication) is replaced by proxemic attentiveness in non-tactile cultures, maintaining Hall's personal zone of 0.45-1.2m (Rios-Martinez, Spalanzani and Laugier, 2015, p. 140).

**(b) The West (Europe/North America).** To avoid triggering the Frankenstein Syndrome and to respect the "narcissistic shield" (Kaplan, 2004, p. 14, section-5.2, lines-10-11), Western robots should possess functional, machine-like aesthetic markers (visible joints, metallic surfaces) rather than overtly human-like features, thereby avoiding descent into the uncanny valley (Mori, 1970, p. 98). Behaviourally, they should exhibit transparency, explicitly stating operational reasoning to alleviate what Kaplan (2004, p. 11, section-4.3, lines-16-17) characterises as anxieties of autonomous transgression. The handshake serves as a *symbolic gesture* (a movement with a culturally agreed-upon meaning) combined with *haptics* (Lecture 2), albeit calibrated to the Mediterranean vs Northern European proxemic distinction (Lecture 4).

**(c) Africa.** Informed by Ubuntu and high Power Distance (Cirasa and Conti, 2025, p. 7), an African-deployed robot should possess a modest physical stature to avoid perceived challenges to human hierarchical authority. Behaviourally, it must be group-facing rather than dyadic (one-robot-to-one-user), utilising a warm, highly expressive vocal synthesiser capable of rendering the rich prosodic variations (pitch, tone) necessary for an oral-tradition society (Lecture 3; Winschiers-Theophilus and Bidwell, 2013, *.pdf's*-pp. 12-13). Furthermore Lecture 2 established that "65% of communication is non-verbal," gestural and paralinguistic channels, specifically *beat gestures* (rhythmic hand movements accentuating speech rhythm) and *iconic gestures* (movements visually representing the subject), become critical design considerations.

## 1.4 Adapting Design Patterns for Sociality (Kahn et al., 2008)

Kahn et al. (2008, p. 99) identify eight design patterns for sociality in HRI, noting the patterns are "likely under-described" (p. 99). These patterns must be regionally adapted using the traits established in Section 1.3:

**Pattern 1: Initial Introduction (Kahn et al., 2008, p. 100).**

- *(a) East:* Rather than tactile handshakes, the robot must initiate interaction with a calibrated bow, as "in Japan it's very considered impolite if you break the personal distance or space and try to touch somebody" (Lecture 4). The bow angle should parametrically encode social hierarchy recognition.
- *(b) West:* The *Initial Introduction* can incorporate the handshake as a tactile greeting, albeit with sensitivity to the Mediterranean (closer) versus Northern European (distant) proxemic distinctions (Lecture 4).
- *(c) Africa:* Reflecting Ubuntu's communal orientation, the introduction must address groups rather than individuals. Encoding Power Distance norms, the robot must always greet the eldest or most-senior member first; an inference drawn from the high Power Distance norms identified by Cirasa and Conti (2025, p. 7).

**Pattern 4: Personal Interests and History (Kahn et al., 2008, p. 101).**

- *(a) East:* The robot's backstory can elaborately integrate into the animistic expectation of objects possessing a "spirit" or character (Kaplan, 2004, p. 6, section-3.2, lines-22-25).
- *(b) West:* Self-disclosure must be transparently mechanical, framing its "interests" around its programmed purpose to reinforce the user's ontological comfort (Lecture 1; the Western-"Utilitarian"-robot-as-tool stance).
- *(c) Africa:* This pattern should be realised via storytelling and voice-based dialogue. The robot must establish *joint attention* (the ability of multiple agents to focus on a shared reference point) via structured eye gaze to maintain narrative authority (Lecture 2).

**Pattern 5: Recovering From Mistakes (Kahn et al., 2008, p. 101).**

- *(a) East:* The robot should employ indirect acknowledgement strategies that preserve social harmony (Kaplan, 2004, p. 6, section-3.2, lines-22-25), avoiding direct self-criticism that may cause discomfort via loss of face.
- *(b) West:* The robot should explicitly explain its error and how it will correct it, prioritising transparency to mitigate the underlying technophobia Kaplan (2004, p. 11, section-4.3, lines-5-8) identifies.
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
West & Frankenstein Syndrome; individualism; narcissistic shields & Machine-identity markers; *handshake-ready*; transparent self-disclosure \\
\addlinespace
Africa & Ubuntu; high Power Distance; oral tradition & Communal greetings; elder-first hierarchy; *voice-driven narrative interfaces* \\
\bottomrule
\end{tabular}
\end{table}

- [ ] Kahn et al. (2008) conclude: effective HRI must be "compelling as a lived experience" (p. 103) and thus what constitutes a compelling experience is, as demonstrated above, inseparable from the cultural context thereof.

# 2- Task (2): POMDPs in Human-Robot Interaction

## 2.1 The Role of POMDPs in Trust, Cooperation, Coordination, and Collaboration

A Partially Observable Markov Decision Process (POMDP) extends the MDP introduced in *COMP3003* (Lecture 7) by relaxing full-state observability: the robot can only *infer* the true state via noisy, incomplete observations (Kaelbling, Littman and Cassandra, 1998, Section-3.1, p. 105). Formally, a POMDP is defined by the tuple $\langle S, A, T, R, \Omega, O, \gamma \rangle$, wherein $S$ is a finite set of states, $A$ the available actions, $T(s, a, s') = P(s' \mid s, a)$ the transition function, $R: S \times A \rightarrow \mathbb{R}$ the reward function, $\Omega$ a finite set of observations, $O(s', a, o) = P(o \mid s', a)$ the observation function and $\gamma \in [0,1)$ the discount factor.

To understand the POMDP's utility, one must *differentiate interaction paradigms* as defined in Lecture 1 (Figure~\ref{fig:lecture1-interaction-paradigms}). **Coexistence** is where agents share an environment but complete different tasks, requiring only fully-observable physical states to avoid collisions. **Cooperation** involves a shared workspace and complementary parts of a task. **Coordination** requires temporal alignment: sequencing complementary actions so neither agent blocks nor duplicates the other; the POMDP's belief state enables this by allowing the robot to anticipate *when* to act versus yield based on inferred human intent. However, true **collaboration** demands a shared workspace and the *exact same shared goal* (Lecture 1). In collaboration, the robot must continuously align its actions with the human's unobservable mental states: trust, intent, cognitive load. Because the robot is fundamentally blind to these latent variables, the POMDP's belief state $b$ becomes the computational prerequisite for graduating from mere coexistence to true collaboration (Chen et al., 2020, p. 6). Indeed, Nikolaidis et al. (2017, pp. 621-623) demonstrate this empirically via a "Bounded-Memory Adaptation Model" (BAM) wherein the robot maintains a mixed-observability MDP over the human's latent adaptability, showing mutual adaptation via belief-space planning hugely outperforms fixed strategies.

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
\caption{Action selection governed by continuous belief thresholds. When the probabilistic belief $b(\text{Med Trust, High Load})$ exceeds the escalation threshold $\tau = 0.45$ at $t_2$, the policy dictates a discrete shift from Verbal\_Remind to Explain\_Benefits, then Offer\_Physical\_Assist. As trust recovers and the belief drops below $\tau$ (from $t_3$), the robot de-escalates accordingly.}
\label{fig:action-threshold}
\end{figure}

## 2.2 Uncertainty, Belief States, and Decision-Making

Because the true state is hidden, the POMDP agent maintains a **belief state** $b$: a probability distribution over all possible states $S$, where $b(s)$ represents the agent's subjective probability that the environment is in state $s$, such that $\sum_{s \in S} b(s) = 1$. After taking action $a$ and receiving observation $o$, the belief state is updated via **Bayesian filtering**:

$$
b'(s') = \eta \cdot O(s', a, o) \sum_{s \in S} T(s, a, s') \cdot b(s)
$$

 wherein $\eta$ is a normalisation constant ensuring $\sum_{s'} b'(s') = 1$. This update rule captures the epistemic challenge of HRI: the robot must continuously revise its model of the human's internal state as new and could-be contradictory evidence arrives. As Lecture 3 establishes, the robot utilises affective-computing descriptors (e.g. pitch, MFCCs, zero-crossing rate) to extract observations from the human's behaviour, *feeding* these into the belief update.

The belief state $b$ therefore serves as a **sufficient statistic** for the entire interaction history, compressing all past actions and observations into a single probability vector (Kaelbling, Littman and Cassandra, 1998, Section-3.2, p. 106). This is why the POMDP exhibits a non-Markovian *policy* (each action depends on the full history $h_t$) whilst maintaining a Markovian *belief update* (the next belief $b'$ depends only on the current belief $b$, the action taken, and the observation received); the belief state absorbs all relevant history, and thus the agent need not store raw trajectories to act optimally.

## 2.3 Challenges of Trust Modelling and the POMDP Response

Trust is a latent psychological variable; it cannot be directly measured, only inferred from observable behavioural indicators. Lee and See (2004, *.pdf*-p. 6) define trust as "the attitude that an agent will help achieve an individual's goals in a situation characterized by uncertainty and vulnerability"; a definition foregrounding the latent nature that necessitates probabilistic modelling. Three challenges arise.

### 2.3.1 The Measurement Problem

Observations such as compliance rate, response latency, gaze direction (Lecture 2), and verbal affirmations are noisy proxies (unreliable indirect measures). Hancock et al.'s (2011, p. 520) meta-analysis of 29 empirical studies confirms this, finding that robot performance-based factors exhibit the strongest correlation with trust (mean r = +0.34, p. 522), yet even these explain only modest variance; a user may comply with a robot's suggestion despite low trust (e.g. time pressure), or indeed refuse despite high trust (e.g. due to task complexity), and thus the observation alone does not necessarily disambiguate the latent state.

### 2.3.2 Temporal Dynamics

Trust evolves non-linearly, as it builds slowly through consistent performance but degrades rapidly after errors. This asymmetry is empirically confirmed by Desai et al. (2013, p. 256), who found that "the recovery of trust after a reliability drop occurs at a slower pace than the pace at which trust develops before reliability drops". The *Recovering From Mistakes* pattern (Kahn et al., 2008, p. 101) is therefore critical: a robot that acknowledges and corrects errors can arrest trust decay, whereas one that ignores failures risks appearing aggressive.

### 2.3.3 Computational Intractability

Solving POMDPs exactly is PSPACE-complete (Papadimitriou and Tsitsiklis, 1987, p. 448), as the belief simplex is continuous even with finite $|S|$. Practical HRI applications therefore utilise approximate solvers such as PBVI (Pineau, Gordon and Thrun, 2003, p. 1025) or POMCP (Silver and Veness, 2010, p. 4) for tractable real-time planning.

The POMDP addresses these challenges by encoding trust as a hidden state variable, observations as probabilistic signals thereof, and actions as trust-modulating strategies (Chen et al., 2020, p. 6); trust is therefore modelled as a continuously-evolving distribution rather than a threshold-based heuristic (a rigid binary switch ignoring subtle fluctuations).

## 2.4 Proposed Neuro-Symbolic POMDP Model: Neo Robot with OpenAI Cognitive Architecture

To concretise this framework, I propose a neuro-symbolic POMDP model for a Neo (Pepper) humanoid robot augmented with an OpenAI multimodal API, deployed as an elderly medication-adherence assistant. LLMs are powerful observation extractors, parsing unstructured human behaviour into structured probabilistic assessments; however, they are inherently stateless (each API call is independent, with no temporal memory) and prone to hallucination (Ji et al., 2023, p. 36). Wrapping the API inside a POMDP belief state $b(s)$ therefore provides the temporal scaffold the LLM lacks: a continuously-updated model of the human's latent states (Trust, Cognitive Load). This neuro-symbolic paradigm, wherein a neural subsystem handles perception whilst a symbolic subsystem governs reasoning, represents what Garcez and Lamb (2023, p. 12389) term the 'third wave' of AI. Ahn et al. (2022, p. 4) established via SayCan that LLMs can ground language in robotic affordances, yet their architecture lacks the temporal belief maintenance a POMDP provides.

### 2.4.1 The Neuro-Symbolic Architecture

The Neo robot's onboard sensors (camera, microphone array, tactile sensors) capture multimodal data from the elderly user, transmitted to the OpenAI API serving as the **observation function** ($O$). The API processes this stream, analysing facial action units, extracting prosodic descriptors (pitch, MFCCs, zero-crossing rate) from speech (Lecture 3), and interpreting gestural semantics, to output a structured observation $o \in \Omega$. The API can be prompted to estimate a probability distribution over possible observations rather than a categorical label, preserving the epistemic uncertainty the POMDP requires. If the robot performs Verbal\_Remind and the API observes Hesitate, the belief shifts toward medium-trust, high-load states; $\pi^*(b)$ consequently selects Explain\_Benefits rather than escalating to physical assistance (Figure~\ref{fig:action-threshold}), as the belief indicates the user is cognitively loaded rather than non-compliant.

### 2.4.2 Formal Specification

- **State Space** ($S$): Trust $\in \{$Low, Medium, High$\}$ $\times$ Cognitive Load $\in \{$Low, High$\}$, yielding $|S| = 6$.
- **Action Space** ($A$): $\{$Verbal\_Remind, Explain\_Benefits, Offer\_Physical\_Assist, Increase\_Autonomy, Disengage$\}$. The POMDP selects abstract actions; the API translates these into culturally-calibrated language and gestures via the Neo robot.
- **Observation Space** ($\Omega$): $\{$Comply, Hesitate, Verbal\_Refuse, Ignore, Gaze\_Avert$\}$, extracted by the OpenAI API.
- **Observation Function** ($O$): $P(o \mid s', a)$ is estimated by the API's multimodal inference; e.g. $P(\text{Comply} \mid \text{HighTrust, LowLoad}, \text{Remind}) = 0.8$, derived from the user's facial configuration and vocal tone.
- **Transition Function** ($T$): Models trust dynamics parametrically. An unneeded Offer\_Physical\_Assist violating personal proxemics (Lecture 4) degrades trust: $P(\text{Low} \mid \text{Med}, \text{Assist}) = 0.6$; conversely, a well-timed Explain\_Benefits yields $P(\text{High} \mid \text{Med}, \text{Explain}) = 0.5$.
- **Reward Function** ($R$): Successful medication adherence yields $R = +10$; preserving user autonomy (choosing Increase\_Autonomy when trust is High) yields $R = +3$; unwanted physical assistance incurs $R = -5$, reflecting the social cost of proxemic violation. Mirroring the POMDP's 'cost of listening' penalty (the Tiger problem), the architecture imposes $R = -1$ per observation cycle, penalising excessive polling. Both $O$ and $R$ must be culturally parametrised from the findings in Task 1; the proxemic penalty, for instance, should be weighted more heavily for non-contact cultures.

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
\caption{Simplified belief evolution over a three-state trust space. The medium-trust posterior exhibits non-monotonic behaviour, rising sharply after observing Hesitate at $t_1$, then declining upon Comply at $t_2$. These deviations from the uniform prior demonstrate the Bayesian update mechanism inferring hidden trust states from partial observations, consistent with the non-linear trust dynamics described by Lee and See (2004, *.pdf*-p. 22).}
\label{fig:belief-evolution}
\end{figure}

### 2.4.3 Benefits and Limitations

The model's strength lies in neuro-symbolic complementarity (Garcez and Lamb, 2023, Section 2.4, p. 12389). Unlike traditional solvers such as PBVI (Pineau, Gordon and Thrun, 2003, p. 1025), this approach delegates perceptual dimensionality-reduction to the LLM, preserving belief-update tractability. However, the architecture introduces limitations: 1) a fundamental mathematical friction: the POMDP relies on the Markov property with a stationary observation function $O(s', a, o)$, yet the LLM is inherently non-stationary; its outputs depend on a dynamic context window, meaning the observation function shifts based on the LLM's own internal states, and thus the belief update is technically an approximation rather than an exact sufficient statistic. If the LLM's interpretation silently shifts (e.g. following an API version update), the belief state degrades without any mechanism to detect this drift; 2) API latency (200-800ms) may disrupt real-time proxemic responsiveness (Lecture 4); 3) the LLM's stochastic nature means identical inputs may yield different observation distributions, introducing unmodelled noise into the Bayesian update; and 4) the observation model may inherit training-data biases, degrading inference accuracy for elderly users if predominantly trained on younger demographics (Lecture 5).

## 2.5 Ethical and Social Implications

By operationalising trust as a now-computable metric, the POMDP risks enabling exploitation: insofar as the reward function solely prioritises compliance, the optimal policy may learn to time requests when inferred cognitive load is highest. Designers must therefore encode user autonomy into the reward structure, lest assistance erode into manipulation. Sharkey (2014, pp. 69-70) frames this via the Capability Approach: the robot must expand rather than impede access to Nussbaum's central capabilities, and thus the $R = +3$ autonomy bonus is not merely a design preference but an ethical imperative encoding that dignity requires preservation of choice.

The OpenAI API introduces three additional ethical dimensions. Firstly, **hallucination risk**: LLMs generate plausible but factually incorrect outputs (Ji et al., 2023, p. 36); in a medication-adherence context, misclassifying confused hesitation as willing compliance could trigger inappropriate actions with health consequences. Explainable AI (Lecture 5) therefore becomes non-negotiable: the POMDP must justify *why* it selected a particular action, tracing the decision through the belief state to the observations extracted. Secondly, **cloud-data sovereignty**: continuous multimodal processing transmitted to third-party servers risks what Sharkey and Sharkey (2012, pp. 35-36) identify as monitoring that infringes on "the right to privacy" (Figure~\ref{fig:lecture5-privacy-surveillance}); the user's most vulnerable moments are thereby streamed to servers whose data-handling policies cannot be meaningfully audited. Finally, **API latency and proxemic violation**: response delays during a time-critical approach cause the robot to freeze or fail to yield, behaviour that Lecture 4 identifies as "aggressive" (Figure~\ref{fig:lecture4-aggressive-robot}). The ethical watchword is therefore proactive regulation (Lecture 5): designers must encode transparent, auditable constraints *ex ante* into both the reward function and the API pipeline, ensuring the robot does not merely *model* trust but instead *earns* it through explainable, privacy-preserving behaviour.

\begin{figure}[H]
\centering
\includegraphics[width=0.75\textwidth]{image/lecture5-privacy-surveillance.png}
\caption{Lecture-5 slide raising the surveillance concern: ``The AI records what you do and transfers data\ldots\ to whom? Company? Third Party?''}
\label{fig:lecture5-privacy-surveillance}
\end{figure}

\begin{figure}[H]
\centering
\includegraphics[width=0.75\textwidth]{image/lecture4-aggressive-robot.png}
\caption{Lecture-4 slide establishing that a robot which fails to yield during spatial approach ``may appear aggressive''; with the annotation ``Is this culturally dependent?''}
\label{fig:lecture4-aggressive-robot}
\end{figure}

# Appendices

## References (Peer-reviewed or Conference only)

### Task (1)'s

- Cirasa, C. and Conti, D. (2025) 'Mapping trust and cultural dimensions in human-robot interaction: a scoping review approach', *Computers in Human Behavior Reports*, 19, article 100763. Available at: [https://www.researchgate.net/publication/394316314_Mapping_trust_and_cultural_dimensions_in_Human-Robot_Interaction_A_scoping_review_approach](https://www.researchgate.net/publication/394316314_Mapping_trust_and_cultural_dimensions_in_Human-Robot_Interaction_A_scoping_review_approach) (Accessed: 21 February 2026).

- Fong, T., Nourbakhsh, I. and Dautenhahn, K. (2003) 'A survey of socially interactive robots', *Robotics and Autonomous Systems*, 42(3-4), pp. 143-166. Available at: [https://doi.org/10.1016/S0921-8890(02)00372-X](https://doi.org/10.1016/S0921-8890(02)00372-X) (Accessed: 8 March 2026).

- Hancock, P.A., Billings, D.R., Schaefer, K.E., Chen, J.Y.C., de Visser, E.J. and Parasuraman, R. (2011) 'A meta-analysis of factors affecting trust in human-robot interaction', *Human Factors*, 53(5), pp. 517-527. Available at: [https://www.researchgate.net/publication/51763875_A_Meta-Analysis_of_Factors_Affecting_Trust_in_Human-Robot_Interaction](https://www.researchgate.net/publication/51763875_A_Meta-Analysis_of_Factors_Affecting_Trust_in_Human-Robot_Interaction) (Accessed: 16 February 2026).

- Joosse, M., Lohse, M. and Evers, V. (2014) 'Lost in proxemics: spatial behavior for cross-cultural HRI', *in Proceedings of the 2014 ACM/IEEE International Conference on Human-Robot Interaction (HRI '14)*. Bielefeld: ACM/IEEE, pp. 1-6. Available at: [https://doi.org/10.1145/2559636.2559661](https://doi.org/10.1145/2559636.2559661) (Accessed: 19 February 2026).

- Kahn, P.H., Freier, N.G., Kanda, T., Ishiguro, H., MacDorman, K.F., Severson, R.L. and Friedman, B. (2008) 'Design patterns for sociality in human-robot interaction', *in Proceedings of the 3rd ACM/IEEE International Conference on Human-Robot Interaction (HRI '08)*. Amsterdam: ACM Press, pp. 97-104. Available at: [https://dl.acm.org/doi/10.1145/1349822.1349836](https://dl.acm.org/doi/10.1145/1349822.1349836) (Accessed: 15 February 2026).

- Kaplan, F. (2004) 'Who is afraid of the humanoid? Investigating cultural differences in the acceptance of robots', *International Journal of Humanoid Robotics*, 1(3), pp. 1-16. Available at: [https://www.researchgate.net/publication/220065746_Who_is_Afraid_of_the_Humanoid_Investigating_Cultural_Differences_in_the_Acceptance_of_Robots](https://www.researchgate.net/publication/220065746_Who_is_Afraid_of_the_Humanoid_Investigating_Cultural_Differences_in_the_Acceptance_of_Robots) (Accessed: 15 February 2026).

- Lim, V., Rooksby, M. and Cross, E.S. (2021) 'Social robots on a global stage: establishing a role for culture during human-robot interaction', *International Journal of Social Robotics*, 13(6), pp. 1307-1333. Available at: [https://link.springer.com/article/10.1007/s12369-020-00710-4](https://link.springer.com/article/10.1007/s12369-020-00710-4) (Accessed: 19 February 2026).

- Metz, T. (2007) 'Toward an African moral theory', *Journal of Political Philosophy*, 15(3), pp. 321-341. Available at: [https://www.researchgate.net/publication/227993551_Toward_an_African_Moral_Theory](https://www.researchgate.net/publication/227993551_Toward_an_African_Moral_Theory) (Accessed: 15 February 2026).

- Mori, M. (1970) 'The uncanny valley', *Energy*, 7(4), pp. 33-35. Translated by MacDorman, K.F. and Kageki, N. (2012) *IEEE Robotics and Automation Magazine*, 19(2), pp. 98-100. Available at: [https://www.researchgate.net/publication/254060168_The_Uncanny_Valley_From_the_Field](https://www.researchgate.net/publication/254060168_The_Uncanny_Valley_From_the_Field) (Accessed: 15 February 2026).

- Rios-Martinez, J., Spalanzani, A. and Laugier, C. (2015) 'From proxemics theory to socially-aware navigation: a survey', *International Journal of Social Robotics*, 7(2), pp. 137-153. Available at: [https://www.researchgate.net/publication/276881232_From_Proxemics_Theory_to_Socially-Aware_Navigation_A_Survey](https://www.researchgate.net/publication/276881232_From_Proxemics_Theory_to_Socially-Aware_Navigation_A_Survey) (Accessed: 21 February 2026).

- Smedegaard, C.V. (2019) 'Reframing the role of novelty within social HRI: from noise to information', in Proceedings of the 14th ACM/IEEE *International Conference on Human-Robot Interaction (HRI '19)*. Daegu: IEEE Press, pp. 411-420. Available at: [https://doi.org/10.1109/HRI.2019.8673219](https://doi.org/10.1109/HRI.2019.8673219) (Accessed: 19 February 2026).

- Winschiers-Theophilus, H. and Bidwell, N.J. (2013) 'Toward an Afro-centric indigenous HCI paradigm', *International Journal of Human-Computer Interaction*, 29(4), pp. 243-255. Available at: [https://doi.org/10.1080/10447318.2013.765763](https://doi.org/10.1080/10447318.2013.765763) (Accessed: 21 February 2026).

- Wyche, S. and Steinfield, C. (2016) 'Why don't farmers use cell phones to access market prices? Technology affordances and barriers to market information services adoption in rural Kenya', *Information Technology for Development*, 22(2), pp. 320-333. Available at: [https://doi.org/10.1080/02681102.2015.1048184](https://doi.org/10.1080/02681102.2015.1048184) (Accessed: 15 February 2026).

### Task (2)'s

- Ahn, M., Brohan, A., Brown, N. et al. (2022) 'Do As I Can, Not As I Say: Grounding Language in Robotic Affordances', in *Proceedings of the 6th Conference on Robot Learning (CoRL 2022)*. Auckland: PMLR, pp. 287-318. Available at: [https://arxiv.org/abs/2204.01691](https:
//arxiv.org/abs/2204.01691) (Accessed: 18 February 2026).

- Chen, M., Nikolaidis, S., Soh, H., Hsu, D. and Srinivasa, S. (2020) 'Trust-aware decision making for human-robot collaboration: model learning and planning', *ACM Transactions on Human-Robot Interaction*, 9(2), Article 9. Available at: [https://personalrobotics.cs.washington.edu/publications/chen2019trust.pdf](https://personalrobotics.cs.washington.edu/publications/chen2019trust.pdf) (Accessed: 15 February 2026).

- Desai, M., Kaniarasu, P., Medber, M., Steinfeld, A. and Yanco, H. (2013) 'Impact of robot failures and feedback on real-time trust', in *Proceedings of the 8th ACM/IEEE International Conference on Human-Robot Interaction (HRI '13)*. Tokyo: IEEE Press, pp. 251-258. Available at: [https://ieeexplore.ieee.org/document/6483596](https://ieeexplore.ieee.org/document/6483596) (Accessed: 16 February 2026).

- Garcez, A.d'A. and Lamb, L.C. (2023) 'Neurosymbolic AI: The 3rd Wave', *Artificial Intelligence Review*, 56(11), pp. 12387-12406. Available at: [https://www.researchgate.net/publication/346933355_Neurosymbolic_AI_The_3rd_Wave](https://www.researchgate.net/publication/346933355_Neurosymbolic_AI_The_3rd_Wave) (Accessed: 18 February 2026).

- Hancock, P.A., Billings, D.R., Schaefer, K.E., Chen, J.Y.C., de Visser, E.J. and Parasuraman, R. (2011) 'A meta-analysis of factors affecting trust in human-robot interaction', *Human Factors*, 53(5), pp. 517-527. Available at: [https://www.researchgate.net/publication/51763875_A_Meta-Analysis_of_Factors_Affecting_Trust_in_Human-Robot_Interaction](https://www.researchgate.net/publication/51763875_A_Meta-Analysis_of_Factors_Affecting_Trust_in_Human-Robot_Interaction) (Accessed: 16 February 2026).

- Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu, Y., Ishii, E., Bang, Y.J., Madotto, A. and Fung, P. (2023) 'Survey of Hallucination in Natural Language Generation', *ACM Computing Surveys*, 55(12), Article 248. Available at: [https://www.researchgate.net/publication/358458381_Survey_of_Hallucination_in_Natural_Language_Generation](https://www.researchgate.net/publication/358458381_Survey_of_Hallucination_in_Natural_Language_Generation) (Accessed: 18 February 2026).

- Kaelbling, L.P., Littman, M.L. and Cassandra, A.R. (1998) 'Planning and acting in partially observable stochastic domains', *Artificial Intelligence*, 101(1-2), pp. 99-134. Available at: [https://people.csail.mit.edu/lpk/papers/aij98-pomdp.pdf](https://people.csail.mit.edu/lpk/papers/aij98-pomdp.pdf) (Accessed: 15 February 2026).

- Kahn, P.H., Freier, N.G., Kanda, T., Ishiguro, H., MacDorman, K.F., Severson, R.L. and Friedman, B. (2008) 'Design patterns for sociality in human-robot interaction', *in Proceedings of the 3rd ACM/IEEE International Conference on Human-Robot Interaction (HRI '08)*. Amsterdam: ACM Press, pp. 97-104. Available at: [https://dl.acm.org/doi/10.1145/1349822.1349836](https://dl.acm.org/doi/10.1145/1349822.1349836) (Accessed: 15 February 2026).

- Lee, J.D. and See, K.A. (2004) 'Trust in automation: designing for appropriate reliance', *Human Factors*, 46(1), pp. 50-80. Available at: [https://scispace.com/pdf/trust-in-automation-designing-for-appropriate-reliance-2uiy4o89ga.pdf](https://scispace.com/pdf/trust-in-automation-designing-for-appropriate-reliance-2uiy4o89ga.pdf) (Accessed: 16 February 2026).

- Nikolaidis, S., Hsu, D. and Srinivasa, S. (2017) 'Human-robot mutual adaptation in collaborative tasks: models and experiments', *International Journal of Robotics Research*, 36(5-7), pp. 618-634. Available at: [https://pmc.ncbi.nlm.nih.gov/articles/PMC7449140/](https://pmc.ncbi.nlm.nih.gov/articles/PMC7449140/) (Accessed: 16 February 2026).

- Papadimitriou, C.H. and Tsitsiklis, J.N. (1987) 'The complexity of Markov decision processes', *Mathematics of Operations Research*, 12(3), pp. 441-450. Available at: [https://web.mit.edu/jnt/www/Papers/J016-87-mdp-complexity.pdf](https://web.mit.edu/jnt/www/Papers/J016-87-mdp-complexity.pdf) (Accessed: 15 February 2026).

- Pineau, J., Gordon, G. and Thrun, S. (2003) 'Point-based value iteration: an anytime algorithm for POMDPs', in *Proceedings of the 18th International Joint Conference on Artificial Intelligence (IJCAI-03)*. Acapulco: Morgan Kaufmann, pp. 1025-1030. Available at: [https://www.ijcai.org/Proceedings/03/Papers/147.pdf](https://www.ijcai.org/Proceedings/03/Papers/147.pdf) (Accessed: 15 February 2026).

- Sharkey, A. (2014) 'Robots and human dignity: a consideration of the effects of robot care on the dignity of older people', *Ethics and Information Technology*, 16(1), pp. 63-75. Available at: [https://www.researchgate.net/publication/261960182_Robots_and_human_dignity_A_consideration_of_the_effects_of_robot_care_on_the_dignity_of_older_people](https://www.researchgate.net/publication/261960182_Robots_and_human_dignity_A_consideration_of_the_effects_of_robot_care_on_the_dignity_of_older_people) (Accessed: 16 February 2026).

- Sharkey, A. and Sharkey, N. (2012) 'Granny and the robots: ethical issues in robot care for the elderly', *Ethics and Information Technology*, 14(1), pp. 27-40. Available at: [https://www.dhi.ac.uk/san/waysofbeing/data/governance-crone-sharkey-2012a.pdf](https://www.dhi.ac.uk/san/waysofbeing/data/governance-crone-sharkey-2012a.pdf) (Accessed: 16 February 2026).

- Silver, D. and Veness, J. (2010) 'Monte-Carlo planning in large POMDPs', in *Advances in Neural Information Processing Systems 23 (NeurIPS 2010)*. Vancouver: Curran Associates, pp. 2164-2172. Available at: [https://papers.neurips.cc/paper_files/paper/2010/file/edfbe1afcf9246bb0d40eb4d8027d90f-Paper.pdf](https://papers.neurips.cc/paper_files/paper/2010/file/edfbe1afcf9246bb0d40eb4d8027d90f-Paper.pdf) (Accessed: 15 February 2026).

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
ChatGPT & General conversations via web-search AI about how the paper's topic relates to others' studies \textbf{(A4)} & Few times \\
\hline
ChatGPT & Used to identify which sections were over-weighted relative to mark allocation for trimming to match word-count allowance \textbf{(A2)} & Once \\
\hline
ChatGPT & Traversing papers to find relevant parts to read for the essay \textbf{(A4)} & Quite a few times \\
\hline
\end{tabular}

- [X] I understand that the ownership and responsibility for the academic integrity of this submitted assessment falls with me, the student.
- [X] I confirm that all details provided above are an accurate description of how AI was used for this assessment.
