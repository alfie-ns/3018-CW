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
# Words-To-Use:

- [ ] INTEGRATE ROBOTIC LaTeX DIAGRAM
- [ ] most-{something} {something}
- [ ] would-be
- [ ] despite
- [ ] contravened
  — [ ] humanlike
- [ ] watchword
- [ ] e.g. `1-` , `2-`, ...
- [ ] despite x something y
- [ ] and indeed, the robot will...
- [ ] and `therefore, `x ` thus {does, e.g. *feeds*` `y` continuously throughout the process `wherein`...
- [ ] `as now-{something} the x thus does y continously throughout the process wherein it does z`
- [ ] `Whilst`: only used at the start of a sentence
- [ ] `Whilst this is true, x may be inclinded to {x} based on...`
- [ ] `and thus *x* therefore...`
- [ ] `is indeed...`
- [ ] `and indeed...`
- [ ] `however, insofar as`
- [ ] `thereof`: of the thing just mentioned
- [ ] `herein`: in this document
- [ ] Note
- [ ] Approach
- [ ] within
- [ ] `wherein`: in which
- [ ] `regarding, in regard to`, etc
- [ ] `likelihood`
- [ ] `thereof`:
- [ ] `infer`: conclude from reasoning
- [ ] `init`: initialise
- [ ] `use`: use
- [ ] `via`: through
- [ ] `wherein`: in which
- [ ] `indeed`: in fact

# TODO:

- [ ] hit word-count*0.1 limit allowance across report
- [ ] utilise lecture teachings in lec 5-6 etc
- [ ] review papers: pros or limitations
- [ ] indeed 10% word-count allowance
- [ ] peer-reviewed or conference papers
- [ ] very good LaTeX visualisations
- [ ] uses 3003-report feedback??
- [ ] In this section, you should focus on providing enough description of the supervised learning, neural network, and naïve Bayes models.
- [ ] Do not assume the reader knows the basics. Dedicate specific paragraphs to explicitly defining the algorithms and the broader category (Supervised Learning) before diving into your implementation.
- [ ] Then, refer to some studies that have utilised neural networks and naïve Bayes models in your area using the selected database
- [ ] Ensure your literature review in the introduction explicitly cites papers that use your specific dataset (or very similar ones), establishing a clear baseline before you begin
- [ ] TODO.md

# 1- Task (1): Cultural Differences and HRI Design

~1,750-word $\vert$ 40% weighting $\vert$ Questions 1.1-1.5

## 1.1. Cultural Differences in the Acceptance of Robots (Kaplan, 2004)

Kaplan's 2004 identification of East-West fundamental societal divergence is rooted in the observation that "**culture affects the way technology is perceived** and, in a reciprocal manner, **technological evolution shapes culture in particular ways**" (Kaplan, 2004, p. 465); i.e. the cultural (habits), theological (religious), and mythological narratives of each region indeed shape the societal meta-layer *(the underlying philosophical-and-theological frameworks governing robotic integration)* that underpins robot acceptance.

### 1.1.1 Western Society (The Frankenstein Syndrome)

Western culture persistently has viewed the creation of human-like (humanoid) entities with suspicion. Kaplan (2004) identifies this as the "Frankenstein Syndrome": a culturally-filtered conviction wherein "any artificially created humanoid will necessarily turn against its creator" (p. 11).

This anxiety is traceable to the West's distinction between nature and culture, which posits "no place for hybrids" in such classifications (Kaplan, 2004, p. 6). The Western cultural narrative therefore frames the humanoid robot as a challenge to human specificity (p. 12), and thus, a transgression against the natural order; consequently, Western societies have historically envisioned robotic development towards industrial, non-anthropomorphic (instrumentalist) applications wherein the machine remains a *tool* rather than a would-be social entity. Kaplan further notes the concept of "narcissistic shields" *(the psychological defence mechanisms protecting human exceptionalism)* (p. 14), whereby Westerners psychologically distance themselves to manage the discomfort of encountering machines that erode the human-robot distinction.

### 1.1.2 Eastern Society (Technology Taming and Animism)

Japanese culture, by contrast, exhibits a fundamentally different ontological *(the definition of what counts as a 'being')* stance. Kaplan (2004) traces this to the Shinto tradition, wherein the rigid Western boundary between animate and inanimate is dissolved in favour of a "continuous network of beings" (p. 6). In this view, humanoid robots are not perceived as transgressions but instead as natural extensions of an already-spirited world.

Furthermore, Kaplan discusses the cultural mechanism of "technology taming" i.e. a recurring historical pattern wherein foreign technologies are domesticated via integration into existing cultural frameworks (p. 3). This ethos aligns with the *kata* tradition of formalised practice, wherein repetition leads to "maximum stability" (p. 6). The popular *Astro Boy* manga franchise (p. 2) exemplifies this domestication narratively: the robot is cast not as a Frankensteinian threat, but as a heroic companion (p. 2). Kaplan references the Amaterasu myth (p. 5) to argue that Japanese cosmology fundamentally lacks the creator-vs-creation antagonism (the inherent transgression of usurping divine privilege) that underpins Western technophobia, saying simply that "in Japan, no gods created human beings" (p. 12).

### 1.1.3 Implications for HRI Design.

- [ ] These diverged cultural framings consequentially shape interaction design in profound ways. Whilst Western users predominantly prefer robots that maintain clear machine-identity markers, thereby preserving the ‘narcissistic shield’, Eastern users instead welcome anthropomorphic features (imitating human behaviour) that align with animistic expectations. However, insofar as Western designers may be inclined to impose universal proxemic standards based on their own cultural norms, this approach is fundamentally flawed. As Lecture 4 emphasised, ‘every country and each culture has their own concept of proxemics’, and therefore a robot’s spatial behaviour must adapt accordingly: Japanese norms demand larger personal-space buffers and non-tactile greeting protocols, whereas Mediterranean cultures tolerate closer approach distances. The watchword herein is cultural relativism—no universal design policy can accommodate these fundamentally different ontological commitments.

## 1.2 African Cultural Factors Influencing HRI

Whilst Kaplan's (2004) analysis is confined to the East-West axis, a complete account of cultural factors in HRI must address the African context, wherein distinct philosophical and socio-structural dimensions shape technology acceptance.

**Ubuntu Philosophy and Communal Identity.** The most prominent cultural factor is *Ubuntu* — the Southern African philosophical principle that "a person is a person through other persons" (Metz, 2007, p. 323). Whereas Western HRI design typically foregrounds individual user experience, Ubuntu-informed design would prioritise communal benefit and relational harmony. A robot operating within an Ubuntu-oriented society should therefore be designed to address the *group* rather than the individual, facilitating collective decision-making and shared resource access (Metz, 2007). This stands in stark contrast to the individualised personal-assistant paradigm prevalent in Western HRI.

**Power Distance and Hierarchical Norms.** Hofstede's (2001) cultural dimensions framework identifies many African societies as exhibiting high Power Distance — a societal acceptance of hierarchical authority structures. In regard to HRI, this suggests that robots interacting with users across different social strata must modulate their behaviour accordingly: deferential language and posture when addressing elders or authority figures, and indeed a more directive interaction style when assisting in contexts where the robot is perceived as an institutional representative (Hofstede, 2001). Failing to encode these hierarchical norms risks contravening deeply held social expectations, thereby undermining trust.

**Oral Tradition and Multimodal Communication.** African cultures have historically privileged oral knowledge transmission over written documentation (Vansina, 1985). This has direct implications for interaction modality: voice-driven, narrative-based interfaces — utilising speech processing and prosodic features such as pitch and MFCCs (Lecture 3) — may achieve higher engagement than text-heavy GUI paradigms. Furthermore, as Lecture 2 established that "65% of communication is non-verbal," gestural and paralinguistic channels become critical design considerations for African contexts wherein oral expressiveness is culturally normative.

**Infrastructure and Access Constraints.** Despite rapid technological growth, many African regions face infrastructure limitations including intermittent connectivity and limited access to high-specification hardware (Wyche and Steinfield, 2016). HRI systems deployed in these contexts must therefore be robust to connectivity loss, operable on low-power devices, and designed for shared rather than personal ownership — aligning with the communal ethos of Ubuntu.

## 1.3 Regional Design Traits (Appearance and Behaviour)

The cultural factors identified above dictate distinct morphological and behavioural traits to maximise acceptance.

**(a) The East (Japan).** Because Shinto animism dissolves the natural/artificial boundary (Kaplan, 2004), anthropomorphic or highly expressive aesthetic traits are welcomed. However, to align with the *kata* tradition of harmonious form, the robot's movements must be fluid and graceful rather than purely functional. Behaviourally, the robot should adopt a "side-by-side" cooperative posture rather than an imposing face-to-face stance, reflecting Japanese non-tactile proxemic norms requiring larger personal-space buffers (Lecture 4). As Lecture 2 establishes, *haptics* (deliberate physical communication) has beneficial effects primarily within the same social group — hence physical touch is replaced by proxemic attentiveness, maintaining Hall's personal zone (0.5–1.2m).

**(b) The West (Europe/North America).** To avoid triggering the Frankenstein Syndrome and to respect the "narcissistic shield" (Kaplan, 2004, p. 478), Western robots should possess functional, machine-like aesthetic markers (e.g., visible joints, metallic chassis) to clearly signal their artificiality, thereby preventing descent into the uncanny valley (Mori, 1970). Behaviourally, they must exhibit extreme transparency, explicitly stating their operational reasoning to alleviate fears of autonomous transgression. The handshake serves as a *symbolic gesture* (a movement with a culturally agreed-upon meaning) combined with *haptics* (Lecture 2), albeit calibrated to the Mediterranean versus Northern European proxemic distinction (Lecture 4).

**(c) Africa.** Informed by Ubuntu and high Power Distance (Hofstede, 2001), an African-deployed robot should possess a modest physical stature to avoid perceived challenges to human hierarchical authority. Behaviourally, it must be group-facing rather than dyadic, utilising a warm, highly expressive vocal synthesiser capable of rendering the rich prosodic variations (pitch, tone) necessary for an oral-tradition society (Lecture 3; Vansina, 1985). Furthermore, as Lecture 2 established that "65% of communication is non-verbal," gestural and paralinguistic channels — *beat gestures* (rhythmic hand movements accentuating speech rhythm) and *iconic gestures* (movements visually representing the subject) — become critical design considerations.

## 1.4 Adapting Design Patterns for Sociality (Kahn et al., 2008)

Kahn et al. (2008) identify eight "psychological benchmarks" for social robots, noting the design space is "likely under-described" (p. 100). These patterns must be regionally adapted using the traits established in Section 1.3:

**Pattern 1: Initial Introduction (Kahn et al., 2008, p. 100).**

- *(a) East:* Rather than tactile handshakes, the robot must initiate interaction with a calibrated bow, as "in Japan it's very considered impolite if you break the personal distance or space and try to touch somebody" (Lecture 4). The bow angle should parametrically encode social hierarchy recognition.
- *(b) West:* The *Initial Introduction* can incorporate the handshake as a tactile greeting, albeit with sensitivity to the Mediterranean (closer) versus Northern European (distant) proxemic distinctions (Lecture 4).
- *(c) Africa:* Reflecting Ubuntu's communal orientation, the introduction must address groups rather than individuals. Encoding Power Distance norms, the robot must always greet the eldest or most-senior member first (Hofstede, 2001).

**Pattern 2: Personal Interests (Kahn et al., 2008, p. 101).**

- *(a) East:* The robot's backstory can elaborately integrate into the animistic expectation of objects possessing a "spirit" or character (Kaplan, 2004).
- *(b) West:* Self-disclosure must be transparently mechanical, framing its "interests" around its programmed purpose to reinforce the user's ontological comfort — supporting Theory of Mind mechanisms (Lecture 1) whereby the robot must infer the user's mental state.
- *(c) Africa:* This pattern should be realised via storytelling and voice-based dialogue. The robot must establish *joint attention* (the ability of multiple agents to focus on a shared reference point) via structured eye gaze to maintain narrative authority (Lecture 2; Lecture 3).

**Pattern 3: Recovering From Mistakes (Kahn et al., 2008, p. 102).**

- *(a) East:* The robot should employ indirect acknowledgement strategies that preserve social harmony, avoiding direct self-criticism that may cause discomfort via loss of face.
- *(b) West:* The robot should explicitly explain its error and how it will correct it, prioritising transparency to mitigate underlying technophobia.
- *(c) Africa:* Error recovery must be strictly calibrated to social rank. An unacknowledged robot error affecting an elder constitutes a severe social violation; recovery must involve a disproportionately deferential apology to seniors, leveraging posture and movement (Lecture 2) to express contrition, thereby protecting the user's social face within the community.

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

As Kahn et al. (2008) conclude, effective HRI must be "compelling as a lived experience" (p. 104) — and what constitutes a compelling experience is, as demonstrated above, inseparable from the cultural context thereof.

\newpage

# 2- Task (2): POMDPs in Human-Robot Interaction

- [ ] this needs to change as I am going to incorporate an AI API into the robot’s system

## 2.1 The Role of POMDPs in Trust, Cooperation, Coordination, and Collaboration

A Partially Observable Markov Decision Process (POMDP) extends the standard Markov Decision Process (MDP) — as studied in COMP3003 — by relaxing the assumption of full state observability. Whilst an MDP assumes the agent has direct access to the true environment state, a POMDP acknowledges that in most real-world HRI scenarios, the robot can only *infer* the true state via noisy, incomplete observations (Kaelbling, Littman and Cassandra, 1998). Formally, a POMDP is defined by the 7-tuple $\langle S, A, T, R, \Omega, O, \gamma \rangle$, where $S$ is a finite set of states, $A$ the available actions, $T(s, a, s') = P(s' \mid s, a)$ the transition function, $R: S \times A \rightarrow \mathbb{R}$ the reward function, $\Omega$ a finite set of observations, $O(s', a, o) = P(o \mid s', a)$ the observation function, and $\gamma \in [0,1)$ the discount factor.

To understand the POMDP's utility, one must strictly differentiate interaction paradigms as defined in Lecture 1. **Coexistence** involves agents sharing an environment but completing different tasks, requiring only fully-observable physical states to avoid collisions. **Cooperation** involves a shared workspace and complementary tasks. However, true **collaboration** demands a shared workspace and the *exact same shared goal* (Lecture 1). In collaboration, the robot must continuously align its actions with the human's unobservable mental states — trust, intent, cognitive load. Because the robot is fundamentally blind to these latent variables, the POMDP's belief state $b$ becomes the computational prerequisite for graduating from mere coexistence to true collaboration. The POMDP therefore provides the principled mathematical framework for modelling trust, coordinating joint actions under uncertainty, and enabling genuinely collaborative human-robot teams (Chen et al., 2020). Indeed, Nikolaidis et al. (2017, p. 619) demonstrate this empirically via a "Bounded-Memory Adaptation Model" wherein the robot maintains a POMDP over the human's latent type and adapts its policy accordingly — showing that mutual adaptation via belief-space planning significantly outperforms fixed interaction strategies.

## 2.2 Uncertainty, Belief States, and Decision-Making

Because the true state is hidden, the POMDP agent maintains a **belief state** $b$: a probability distribution over all possible states $S$, where $b(s)$ represents the agent's subjective probability that the environment is in state $s$, such that $\sum_{s \in S} b(s) = 1$. After taking action $a$ and receiving observation $o$, the belief state is updated via **Bayesian filtering**:

$$
b'(s') = \eta \cdot O(s', a, o) \sum_{s \in S} T(s, a, s') \cdot b(s)
$$

 $\eta$ is a normalisation constant ensuring $\sum_{s'} b'(s') = 1$. This update rule captures the core epistemic challenge of HRI: the robot must continuously revise its model of the human's internal state as new — and potentially contradictory — evidence arrives. As Lecture 3 discussed regarding affective computing, the robot utilises descriptors (e.g., pitch, MFCCs, zero-crossing rate) to extract observations from the human's behaviour, and thus *feeds* these into the belief update process wherein each observation incrementally refines the robot's understanding.

The belief state $b$ therefore serves as a **sufficient statistic** for the entire interaction history — it compresses all past actions and observations into a single probability vector, enabling decision-making without storing the full trajectory (Kaelbling, Littman and Cassandra, 1998). This is indeed analogous to how a social robot must infer a human's emotional state from noisy multimodal cues (facial expressions, vocal prosody, posture) rather than accessing the "ground truth" of their feelings directly (Lecture 1; Lecture 3).

## 2.3 Challenges of Trust Modelling and the POMDP Response

Trust is a latent psychological variable — it cannot be directly measured, only inferred from observable behavioural indicators. Lee and See (2004, p. 54) formally define trust as "the attitude that an agent will help achieve an individual's goals in a situation characterised by uncertainty and vulnerability" — a definition that foregrounds precisely the latent, goal-dependent nature that necessitates probabilistic modelling. Three core challenges arise. First, **the measurement problem**: observations such as task compliance rate, response latency, gaze direction (Lecture 2), and verbal affirmations are noisy proxies. Hancock et al.'s (2011, p. 520) meta-analysis of 29 empirical studies confirms this difficulty, finding that robot performance-based factors exhibit the strongest correlation with trust (mean r = +0.26), yet even these explain only modest variance — a user may comply with a robot's suggestion despite low trust (e.g., due to time pressure), or indeed refuse despite high trust (e.g., due to task complexity). Second, **temporal dynamics**: trust evolves non-linearly — it builds slowly through consistent performance but degrades rapidly after errors — an asymmetry empirically confirmed by Desai et al. (2013, p. 256), who found that a single autonomous failure eroded trust more than three consecutive successes could rebuild it. The *Recovering From Mistakes* pattern (Kahn et al., 2008, p. 102) is therefore critical: a robot that acknowledges and corrects errors can arrest trust decay, whereas one that ignores failures risks appearing "aggressive" (Lecture 4). Third, **computational intractability**: solving POMDPs exactly is PSPACE-complete (Papadimitriou and Tsitsiklis, 1987), as the belief simplex is continuous even with finite $|S|$. Practical HRI applications therefore utilise approximate solvers — point-based methods such as PBVI (Pineau, Gordon and Thrun, 2003) or online Monte Carlo tree search such as POMCP (Silver and Veness, 2010) — to achieve tractable real-time planning.

The POMDP addresses these challenges by encoding trust as a hidden state variable, observations as probabilistic signals thereof, and actions as trust-modulating strategies (Chen et al., 2020), and thus *trust* cannot be treated as a static binary variable but must be modelled as a continuously-evolving distribution. The belief state thus provides the robot with a principled estimate of trust that is continuously refined, rather than a brittle threshold-based heuristic (a rigid binary switch wherein the subtle fluctuations of trust are ignored)

## 2.4 Proposed POMDP Model: Medication-Assistance Robot

To concretise this framework, I propose a POMDP model for an assistive robot supporting elderly users with medication adherence. The robot must remind the user, offer physical assistance, and calibrate its interaction based on inferred trust.

\begin{figure}[H]
\centering
\begin{tikzpicture}[
    node distance=1.8cm and 2.5cm,
    state/.style={circle, draw, thick, minimum size=1.2cm, fill=blue!10, font=\small},
    obs/.style={rectangle, draw, dashed, thick, minimum size=1.0cm, fill=orange!15, font=\small},
    action/.style={rectangle, rounded corners, draw, thick, minimum size=1.0cm, fill=green!15, font=\small},
    reward/.style={diamond, draw, thick, minimum size=0.8cm, fill=yellow!15, font=\scriptsize},
    >=Stealth,
    every edge/.style={draw, thick, ->}
]
% Time t
\node[state] (st) {$S_t$};
\node[obs, below=of st] (ot) {$O_t$};
\node[action, above=of st] (at) {$A_t$};
\node[reward, right=1.2cm of at] (rt) {$R_t$};

% Time t+1
\node[state, right=3cm of st] (st1) {$S_{t+1}$};
\node[obs, below=of st1] (ot1) {$O_{t+1}$};
\node[action, above=of st1] (at1) {$A_{t+1}$};

% Edges
\draw[->] (st) -- (ot) node[midway, left, font=\scriptsize] {$O$};
\draw[->] (st) -- (st1) node[midway, above, font=\scriptsize] {$T$};
\draw[->] (at) -- (st1);
\draw[->] (at) -- (rt);
\draw[->] (st) -- (rt);
\draw[->] (st1) -- (ot1) node[midway, left, font=\scriptsize] {$O$};
\draw[->] (at) -- (ot1) node[midway, above right, font=\scriptsize] {};

% Labels indicating hidden vs observable
\node[above=0.3cm of st, text=gray, font=\footnotesize\itshape, xshift=-1.5cm] {Latent States};
\node[below=0.3cm of ot, text=gray, font=\footnotesize\itshape, xshift=-1.5cm] {Observable Data};

% Descriptive text
\node[left=0.3cm of st, font=\footnotesize, text=blue!80!black, align=right] {Trust\\Task};
\node[left=0.3cm of ot, font=\footnotesize, text=orange!80!black, align=right] {Comply\\Hesitate};
\end{tikzpicture}
\caption{Dynamic Bayesian Network (DBN) representation of the proposed Trust-POMDP over time ($t \to t+1$). The robot's action ($A_t$) and the user's hidden trust state ($S_t$) probabilistically determine the next trust state ($S_{t+1}$) via the transition function $T$, the reward ($R_t$), and the noisy behavioural observation ($O_{t+1}$) via the observation function $O$.}
\end{figure}

**Formal Specification:**

- **State Space** ($S$): Trust $\in \{$Low, Medium, High$\}$ $\times$ Task $\in \{$Pending, Taken, Refused$\}$, yielding $|S| = 9$.
- **Action Space** ($A$): $\{$Verbal\_Remind, Explain\_Benefits, Offer\_Physical\_Assist, Increase\_Autonomy, Disengage$\}$.
- **Observation Space** ($\Omega$): $\{$Comply, Hesitate, Verbal\_Refuse, Ignore, Gaze\_Avert$\}$.
- **Transition Function** ($T$): Models trust dynamics parametrically. If the true state is Medium Trust and the robot performs Offer\_Physical\_Assist when unneeded — thereby violating personal proxemics (Lecture 4) — trust degrades: $P(\text{Low} \mid \text{Med}, \text{Assist}) = 0.6$, $P(\text{Med} \mid \text{Med}, \text{Assist}) = 0.4$ (summing rigorously to 1.0).

Conversely, a well-timed Explain_Benefits action yields $P(\text{High} \mid \text{Med}, \text{Explain}) = 0.5$, $P(\text{Med} \mid \text{Med}, \text{Explain}) = 0.5$ (with $P(\text{Low} \mid \text{Med}, \text{Explain}) = 0.0$, summing exactly to 1.0 across the state space).

- **Reward Function** ($R$): Successful medication adherence yields $R = +10$; preserving user autonomy (choosing Increase\_Autonomy when trust is High) yields a bonus $R = +3$; unwanted physical assistance incurs a penalty $R = -5$, reflecting the social cost of proxemic violation.

**Benefits and Limitations.** The model's strength lies in its principled handling of the trust-autonomy trade-off: the belief state $b$ herein represents the robot's probabilistic estimate of trust, continuously refined via Bayesian filtering throughout the interaction wherein each observation shifts the distribution. However, the discretisation of trust into three levels introduces information loss, and calibrating the transition probabilities from real behavioural data remains a significant empirical challenge. Furthermore, the model assumes the Markov property — that trust depends only on the current state — whereas in practice, trust dynamics may depend on long interaction histories.

## 2.5 Ethical and Social Implications

The deployment of POMDPs in HRI raises profound ethical concerns. By mathematically operationalising trust, the POMDP framework transforms a once-theoretical psychological concept into a now-computable metric. However, insofar as the reward function solely prioritises task compliance, the optimal policy may learn to *exploit* the user's trust — timing medication requests when inferred cognitive load is highest to force compliance. Therefore, the once-prohibitive computational barrier (now mitigated by approximate solvers) demands that designers explicitly encode user autonomy and informed consent into the reward structure, lest assistance erode into manipulation. Sharkey (2014, p. 64) frames this via the Capability Approach: the robot must preserve the user's capability to function independently, and thus the R = +3 autonomy bonus in our model is not merely a design preference but an ethical imperative — encoding the principle that dignity requires the preservation of choice. Moreover, the observation function raises surveillance concerns: continuously monitoring gaze, speech prosody, and physiological signals to infer trust constitutes pervasive behavioural tracking — what Sharkey and Sharkey (2012, p. 35) term "surveillance by design," wherein ostensibly beneficial monitoring infrastructure becomes indistinguishable from institutional control — which must be balanced against the user's right to privacy (Lecture 1). The ethical watchword is thus transparency — the robot must not merely *model* trust but actively *earn* it through explainable behaviour.

\newpage

# References

## Task (1)'s

- [ ] fetch exact wording fron paper to earn second tick
- [ ] [ ] Hofstede, G. (2001) *Culture's Consequences: Comparing Values, Behaviors, Institutions and Organizations Across Nations*. 2nd edn. Thousand Oaks: Sage Publications.
- [ ] [ ] Kahn, P.H., Freier, N.G., Kanda, T., Ishiguro, H., MacDorman, K.F., Severson, R.L. and Friedman, B. (2008) 'Design patterns for sociality in human-robot interaction', in *Proceedings of the 3rd ACM/IEEE International Conference on Human-Robot Interaction (HRI '08)*. Amsterdam: ACM Press, pp. 97-104. Available at: https://dl.acm.org/doi/10.1145/1349822.1349836 (Accessed: 15 February 2026).
- [ ] [ ] Kaplan, F. (2004) 'Who is afraid of the humanoid? Investigating cultural differences in the acceptance of robots', *International Journal of Humanoid Robotics*, 1(3), pp. 465–480. Available at: https://doi.org/10.1142/S0219843604000289 (Accessed: 15 February 2026).
- [ ] [ ] Metz, T. (2007) 'Toward an African moral theory', *Journal of Political Philosophy*, 15(3), pp. 321–341. Available at: https://doi.org/10.1111/j.1467-9760.2007.00280.x (Accessed: 15 February 2026).
- [ ] [ ] Mori, M. (1970) 'The uncanny valley', *Energy*, 7(4), pp. 33–35. Translated by MacDorman, K.F. and Kageki, N. (2012) *IEEE Robotics and Automation Magazine*, 19(2), pp. 98–100. Available at: https://doi.org/10.1109/MRA.2012.2192811 (Accessed: 15 February 2026).
- [ ] [ ] Vansina, J. (1985) *Oral Tradition as History*. Madison: University of Wisconsin Press.
- [ ] [ ] Wyche, S. and Steinfield, C. (2016) 'Why don't farmers use cell phones to access market prices? Technology affordances and barriers to market information services adoption in rural Kenya', *Information Technology for Development*, 22(2), pp. 320–333. Available at: https://doi.org/10.1080/02681102.2015.1048184 (Accessed: 15 February 2026).

## Task (2)'s

- [ ] fetch exact wording fron paper to earn second tick
- [X] [ ] Chen, M., Nikolaidis, S., Soh, H., Hsu, D. and Srinivasa, S. (2020) 'Trust-aware decision making for human-robot collaboration: model learning and planning', *ACM Transactions on Human-Robot Interaction*, 9(2), Article 9. Available at: [https://personalrobotics.cs.washington.edu/publications/chen2019trust.pdf](https://personalrobotics.cs.washington.edu/publications/chen2019trust.pdf) (Accessed: 15 February 2026).
- [X] [ ] Desai, M., Kaniarasu, P., Medber, M., Steinfeld, A. and Yanco, H. (2013) 'Impact of robot failures and feedback on real-time trust', in *Proceedings of the 8th ACM/IEEE International Conference on Human-Robot Interaction (HRI '13)*. Tokyo: IEEE Press, pp. 251-258. Available at: https://doi.org/10.1109/HRI.2013.6483596 (Accessed: 16 February 2026).
- [X] [ ] Hancock, P.A., Billings, D.R., Schaefer, K.E., Chen, J.Y.C., de Visser, E.J. and Parasuraman, R. (2011) 'A meta-analysis of factors affecting trust in human-robot interaction', *Human Factors*, 53(5), pp. 517-527. Available at: https://doi.org/10.1177/0018720811417254 (Accessed: 16 February 2026).
- [X] [ ] Kaelbling, L.P., Littman, M.L. and Cassandra, A.R. (1998) 'Planning and acting in partially observable stochastic domains', *Artificial Intelligence*, 101(1-2), pp. 99-134. Available at: [https://doi.org/10.1016/S0004-3702(98)00023-X](https://doi.org/10.1016/S0004-3702(98)00023-X) (Accessed: 15 February 2026).
- [X] [ ] Lee, J.D. and See, K.A. (2004) 'Trust in automation: designing for appropriate reliance', *Human Factors*, 46(1), pp. 50-80. Available at: https://doi.org/10.1518/hfes.46.1.50.30392 (Accessed: 16 February 2026).
- [X] [ ] Nikolaidis, S., Hsu, D. and Srinivasa, S. (2017) 'Human-robot mutual adaptation in collaborative tasks: models and experiments', *International Journal of Robotics Research*, 36(5-7), pp. 618-634. Available at: https://doi.org/10.1177/0278364917690593 (Accessed: 16 February 2026).
- [X] [ ] Papadimitriou, C.H. and Tsitsiklis, J.N. (1987) 'The complexity of Markov decision processes', *Mathematics of Operations Research*, 12(3), pp. 441-450. Available at: [https://web.mit.edu/jnt/www/Papers/J016-87-mdp-complexity.pdf](https://web.mit.edu/jnt/www/Papers/J016-87-mdp-complexity.pdf) (Accessed: 15 February 2026).
- [X] [ ] Pineau, J., Gordon, G. and Thrun, S. (2003) 'Point-based value iteration: an anytime algorithm for POMDPs', in *Proceedings of the 18th International Joint Conference on Artificial Intelligence (IJCAI-03)*. Acapulco: Morgan Kaufmann, pp. 1025-1030. Available at: [https://www.ijcai.org/Proceedings/03/Papers/147.pdf](https://www.ijcai.org/Proceedings/03/Papers/147.pdf)(Accessed: 15 February 2026).
- [X] [ ] Sharkey, A. (2014) 'Robots and human dignity: a consideration of the effects of robot care on the dignity of older people', *Ethics and Information Technology*, 16(1), pp. 63-75. Available at: https://doi.org/10.1007/s10676-014-9338-5 (Accessed: 16 February 2026).
- [X] [ ] Sharkey, A. and Sharkey, N. (2012) 'Granny and the robots: ethical issues in robot care for the elderly', *Ethics and Information Technology*, 14(1), pp. 27-40. Available at: https://doi.org/10.1007/s10676-010-9234-6 (Accessed: 16 February 2026).
- [X] [ ] Silver, D. and Veness, J. (2010) 'Monte-Carlo planning in large POMDPs', in *Advances in Neural Information Processing Systems 23 (NeurIPS 2010)*. Vancouver: Curran Associates, pp. 2164-2172. Available at: https://papers.nips.cc/paper/2010/hash/edfbe1afcf9246bb0d40eb4d8027d90f-Abstract.html (Accessed: 15 February 2026).

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
ChatGPT & Finding relevant pages to read in the paper \textbf{(A4)} & if take paper takes too long to consume efficiently \\
\hline
ChatGPT & General conversations via web-search AI about topic-related relates to others' studies \textbf{(A4)} & Few times at the end \\
\hline
\end{tabular}

- [X] I understand that the ownership and responsibility for the academic integrity of this submitted assessment falls with me, the student.
- [X] I confirm that all details provide above are an accurate description of how AI was used for this assessment.
