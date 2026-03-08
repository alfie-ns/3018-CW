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
<!--
- [ ] do ALL TODOs throughout the inline text of the mainbody itself

- [ ] utilise transcripts

- [ ] Humanise parts distinctly further so it doesn’t just look AI generated etc

- [ ] see where i can fit in LaTeX things  
- [ ] Trust-POMPDP diagram
- [ ] perhaps model trust in lates diabram? or just latex the fundamental diagtam of POMDP similar to lecture slied in POMDP lectures (10,11)

- [ ] CRITICAL: fix word counts
    - [ ] task 1 over by 150 words
    - [ ] task 2 under by 150 words

- [ ] verify all page numbers.
- [ ] verify word count is within 10% allowance across this report.

- [ ] verify all lecture references are correct with deeper review of lecture materials 




# Words-To-Use:



- [ ] persons
- [ ] belief

- [ ] **Lecturer's Top Insight:** Be a Reviewer; don't just argue opinions. Validate every critique with evidence from the literature to ensure it is scientific, not personal.
- [ ] INTEGRATE ROBOTIC LaTeX DIAGRAM
- [ ] 3018-CW/learning/lectures/5 [ ] - utilise/lecture.md (**Task 1 insight!!**)
- [ ] 3018-CW/learning/lectures/6 [ ] - utilise/lecture.md (**General cw insight**)
- [ ] use `whom`
- [ ] talk about nolvety effect in lecture 6
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

- [ ] verify page numbers are correct
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
-->

# 1- Task (1): Cultural Differences and HRI Design

~1,750-word $\vert $ 40% weighting $\vert$ Questions 1.1-1.5

## 1.1. Cultural Differences in the Acceptance of Robots (Kaplan, 2004)

Kaplan's 2004 identification of East-West fundamental societal divergence is rooted in a two-way observation in terms of how the culture's differences manifest as follows: "**culture affects the way technology is perceived** and, reciprocally, **technological evolution shapes culture in particular ways**" (Kaplan, 2004, p. 465); i.e. the cultural (habits), theological (religious), and mythological narrative of each region shapes the societal meta-layer *(the deeper cultural wiring controlling how a society receives robots)*.

### 1.1.1 Western Society (The Frankenstein Syndrome)

Western culture has persistently viewed the creation of human-like (humanoid) entities slightly suspiciously. Kaplan (2004) identifies this as the "Frankenstein Syndrome": a culturally-filtered conviction wherein "any artificially created humanoid will necessarily turn against his creator at some point" (p. 475).

This anxiety traces to the West's distinction between nature and culture, which posits "no place for hybrids" in such classifications (Kaplan, 2004, p. 470). The Western cultural narrative therefore frames humanoid robots as a challenge to human specificity (p. 478), and thus, a transgression *(a violation of the boundary between what humans create and what humans are)* against the natural order; as result, Western societies have historically envisioned robotic development towards industrial, non-anthropomorphic *(i.e. purely functional; not social)* applications wherein the machine remains a *tool* rather than a would-be social entity (Kaplan, 2004, p. 473). Kaplan further notes the concept of "narcissistic shields" *(the psychological-defence mechanisms protecting human exceptionalism)* (p. 478), whereby Westerners psychologically distance themselves from machines that erode the human-robot distinction.

### 1.1.2 Eastern Society (Technology Taming and Animism)

Japanese culture exhibits a fundamentally different ontological *(the definition of what counts as a being)* stance. Kaplan (2004) traces this to the Shinto tradition (p. 469), wherein the rigid Western boundary between animate and inanimate is dissolved in favour of what Kaplan describes as a "continuous network of beings" (p. 470). In this view, humanoid robots are not perceived as transgressions but instead as natural extensions.

Furthermore, Kaplan discussed the cultural mechanism of "technology taming" i.e. a recurring historical pattern wherein foreign technologies are domesticated via integration into existing cultural frameworks (p. 466). This ethos aligns with the *kata* tradition of formalised practice, where repetition leads to "maximum stability" (p. 470). The popular *Astro Boy* manga franchise (p. 466) exemplifies this domestication narratively: the robot is cast not as a Frankensteinian threat, but as a heroic companion (p. 466). Kaplan references the Amaterasu myth (p. 469) to argue that Japanese cosmology fundamentally lacks the creator-vs-creation antagonism (the inherent transgression of usurping divine privilege) that underpins Western technophobia, saying simply that "in Japan, no gods created human beings" (p. 476). This cultural openness persists into the contemporary era; as established in the module materials, Japanese society is "probably less sensitive to risks that might appear from robots" than the West (Lecture 5).

### 1.1.3 Implications for HRI Design.

The divergent cultural framings dictate interaction design profoundly within HRI; whilst Westerners predominantly prefer robots that maintain clear machine identity markers, thereby preserving the 'narcissistic shield' (Kaplan, 2004, p. 478), Eastern users instead welcome human-like anthropomorphic features that align with the animistic expectations established in Section 1.1.2; Lim, Rooksby and Cross (2021, p. 1321) observed this contrasting preference, confirming that culture significantly influences the acceptance of robotic morphology as Korean participants envisioned human-like robots serving as "social company," whereas US participants instead envisioned theirs as "machine-like" extensions of "household appliances".

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

African cultures historically have preferred oral knowledge transmission over written documentation (Winschiers-Theophilus and Bidwell, 2013, pp. 12-13). This implicates interaction modality, i.e. voice-driven, narrative-based interfaces using speech processing and *prosodic* (rhythmically patterned) features such as pitch and MFCCs (Figure~\ref{fig:lecture3-speech-features}), may achieve higher engagement than text-heavy GUI paradigms. Furthermore, Lecture 2 (Figure~\ref{fig:peter-quote}) established that 65% of daily-life communication is nonverbal; thus, gestural and paralinguistic channels become critical design considerations for African contexts wherein oral expressiveness is culturally normative.

\begin{figure}[H]
\centering
\includegraphics[width=0.75\textwidth]{image/peter-quote.png}
\caption{Lecture-2 slide illustrating the prominence of non-verbal communication in daily life.}
\label{fig:peter-quote}
\end{figure}

\begin{figure}[H]
\centering
\includegraphics[width=0.75\textwidth]{image/lecture3-speech-features.png}
\caption{Lecture-3 slide listing speech acoustic features, including fundamental frequency (F0) and MFCCs.}
\label{fig:lecture3-speech-features}
\end{figure}

### 1.2.4 Infrastructure and Access Constraints:

- [ ] Despite rapid technological growth, many African regions face infrastructure limitations e.g. intermittent connectivity and limited access to high-specification hardware (Wyche and Steinfield, 2016). HRI systems deployed in these contexts must therefore be robust to connectivity loss, operable on low-power devices, and designed for shared rather than personal ownership, aligning with the communal ethos of Ubuntu.

## 1.3 Regional Design Traits (Appearance and Behaviour)

<!-- - [ ] DONE? -->

The cultural factors identified above dictate distinct morphological-and-behavioural traits (how the robot looks and how it acts) to maximise acceptance (Fong, Nourbakhsh and Dautenhahn, 2003, p. 149); Figure~\ref{fig:proxemic-comparison} illustrates how these frameworks approach robot strategies per region.

\begin{figure}[H]
\centering
\begin{tikzpicture}[
    robot/.style args={#1}{rectangle, rounded corners=3pt, draw=black!70, thick,
                  minimum width=0.9cm, minimum height=1.4cm, fill=#1!15,
                  font=\scriptsize\sffamily\bfseries},
    human/.style={circle, draw=black!60, very thick, minimum size=0.8cm,
                  fill=white, font=\scriptsize\sffamily\bfseries},
    zonelabel/.style={font=\tiny\sffamily, text=#1!80!black},
    regiontitle/.style={font=\small\sffamily\bfseries,
                        text=#1!80!black},
    traitbox/.style args={#1}{rectangle, rounded corners=2pt, draw=#1!60,
                     fill=#1!5, text width=3.8cm, font=\tiny\sffamily,
                     inner sep=4pt, align=left},
    >=Stealth
]

% ===== EAST (JAPAN) =====
\begin{scope}[shift={(0,0)}]
    \node[regiontitle=eastcol] at (0, 3.2) {(a) East (Japan)};
    \draw[eastcol!30, fill=eastcol!5, dashed] (0,0) circle (2.4cm);
    \draw[eastcol!50, fill=eastcol!10, dashed] (0,0) circle (1.5cm);
    \node[zonelabel=eastcol] at (0, -2.6) {Social zone ($1.2$--$3.7$m)};
    \node[zonelabel=eastcol] at (0, 1.7) {Personal ($0.5$--$1.2$m)};
    \node[human] (hE) at (0, 0) {H};
    \node[robot=eastcol] (rE) at (2.1, 0.3) {R};
    \draw[->, eastcol, thick, dashed] (rE.west) -- +(-0.5, 0)
        node[midway, above, font=\tiny\sffamily\itshape, text=eastcol!80] {bow};
    \node[traitbox=eastcol] at (0, -3.8) {%
        \textbf{Morphology:} Anthropomorphic, fluid\\
        \textbf{Approach:} Side-by-side;
        enlarged buffer\\
        \textbf{Greeting:} Calibrated bow (no touch)\\
        \textbf{Basis:} Shinto animism;
        \textit{kata}
    };
\end{scope}

% ===== WEST (EUROPE/NA) =====
\begin{scope}[shift={(6.5,0)}]
    \node[regiontitle=westcol] at (0, 3.2) {(b) West (Europe/N.\ America)};
    \draw[westcol!30, fill=westcol!5, dashed] (0,0) circle (2.4cm);
    \draw[westcol!50, fill=westcol!10, dashed] (0,0) circle (1.5cm);
    \node[zonelabel=westcol] at (0, -2.6) {Social zone ($1.2$--$3.7$m)};
    \node[zonelabel=westcol] at (0, 1.7) {Personal ($0.5$--$1.2$m)};
    \node[human] (hW) at (0, 0) {H};
    \node[robot=westcol] (rW) at (1.3, 0) {R};
    \draw[<->, westcol, thick] (hW.east) -- (rW.west)
        node[midway, above, font=\tiny\sffamily\itshape, text=westcol!80] {handshake};
    \node[traitbox=westcol] at (0, -3.8) {%
        \textbf{Morphology:} Machine-identity markers\\
        \textbf{Approach:} Face-to-face;
        personal zone\\
        \textbf{Greeting:} Haptic handshake (symbolic)\\
        \textbf{Basis:} Narcissistic shield;
        transparency
    };
\end{scope}

% ===== AFRICA =====
\begin{scope}[shift={(13,0)}]
    \node[regiontitle=africacol] at (0, 3.2) {(c) Africa};
    \draw[africacol!30, fill=africacol!5, dashed] (0,0.1) circle (2.4cm);
    \draw[africacol!50, fill=africacol!10, dashed] (0,0.1) circle (1.5cm);
    \node[zonelabel=africacol] at (0, -2.6) {Group social zone};
    \node[zonelabel=africacol] at (0, 1.8) {Communal space};
    \node[human, minimum size=0.7cm] (hA1) at (-0.5, 0.5) {E};
    \node[human, minimum size=0.7cm, font=\tiny\sffamily\bfseries] (hA2) at (0.5, 0.5) {H};
    \node[human, minimum size=0.7cm, font=\tiny\sffamily\bfseries] (hA3) at (0, -0.4) {H};
    \node[robot=africacol, minimum height=1.1cm, minimum width=0.7cm]
        (rA) at (2.1, -0.1) {R};
    \draw[->, africacol, thick, dashed] (rA.north west) -- (hA1.east)
        node[midway, above, font=\tiny\sffamily\itshape, text=africacol!80, yshift=1pt] {elder first};
    \node[traitbox=africacol] at (0, -3.8) {%
        \textbf{Morphology:} Modest stature;
        non-imposing\\
        \textbf{Approach:} Group-facing;
        peripheral entry\\
        \textbf{Greeting:} Elder-first;
        voice-driven narrative\\
        \textbf{Basis:} Ubuntu; Power Distance; oral trad.
    };
\end{scope}

% ===== Legend =====
\node[font=\tiny\sffamily, text=black!60, align=center] at (6.5, -5.5) {%
    Proxemic zones adapted from Rios-Martinez, Spalanzani and Laugier (2015):
    Intimate ($<$0.5m) $\vert$
    Personal (0.5--1.2m) $\vert$
    Social (1.2--3.7m) $\vert$
    Public ($>$3.7m).
    \\
    \textbf{H} = Human \quad \textbf{E} = Elder \quad \textbf{R} = Robot \quad
    Dashed circles = culturally-calibrated approach boundaries.
};

\end{tikzpicture}
\caption{Culturally-adapted proxemic zones and robot approach strategies across three regional paradigms.
The robot's spatial positioning, greeting modality, and morphological design are calibrated to the cultural frameworks identified in Sections 1.1--1.2 (Rios-Martinez, Spalanzani and Laugier, 2015; Kaplan, 2004; Cirasa and Conti, 2025).}
\label{fig:proxemic-comparison}
\end{figure}

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

- [X] define POMDPs
- [ ] work out word count*0.1 allowance

<!--
- [ ] FIND PEER-REVIEWED CITATIONS: POMDPs (Partially Observable Markov Decision Processes): a mathematical framework for modelling decision-making problems where the agent has incomplete information about the environment state. They extend MDPs by incorporating uncertainty in state observation, making them particularly suitable for HRI scenarios wherein the robot must infer human mental states (§trust, intent, etc) from noisy sensory data. A POMDP is defined by the tuple $\langle S, A, T, R, \Omega, O, \gamma \rangle$, where $S$ is the set of states, $A$ the set of actions, $T$ the transition function, $R$ the reward function, $\Omega$ the set of observations, $O$ the observation function, and $\gamma$ the discount factor.

- [ ] this needs to change as I am going to incorporate an AI API into the robot's system
-->

## 2.1 The Role of POMDPs in Trust, Cooperation, Coordination, and Collaboration

A Partially Observable Markov Decision Process (POMDP) extends the MDP studied in COMP3003 (Lecture 7) by relaxing full state observability (Figure~\ref{fig:pomdp-graphical-model}): rather than direct access to the true environment state, the robot can only *infer* it via noisy, incomplete observations (Kaelbling, Littman and Cassandra, 1998). Formally, a POMDP is defined by the tuple $\langle S, A, T, R, \Omega, O, \gamma \rangle$, where $S$ is a finite set of states, $A$ the available actions, $T(s, a, s') = P(s' \mid s, a)$ the transition function, $R: S \times A \rightarrow \mathbb{R}$ the reward function, $\Omega$ a finite set of observations, $O(s', a, o) = P(o \mid s', a)$ the observation function, and $\gamma \in [0,1)$ the discount factor.

To understand the POMDP's utility, one must strictly differentiate interaction paradigms as defined in Lecture 1 (Figure~\ref{fig:lecture1-interaction-paradigms}). **Coexistence** involves agents sharing an environment but completing different tasks, requiring only fully-observable physical states to avoid collisions. **Cooperation** involves a shared workspace and complementary tasks. However, true **collaboration** demands a shared workspace and the *exact same shared goal* (Lecture 1). In collaboration, the robot must continuously align its actions with the human's unobservable mental states: trust, intent, cognitive load. Because the robot is fundamentally blind to these latent variables, the POMDP's belief state $b$ becomes the computational prerequisite for graduating from mere coexistence to true collaboration. The POMDP therefore provides the principled framework for modelling trust and enabling genuinely collaborative human-robot teams (Chen et al., 2020). Indeed, Nikolaidis et al. (2017, pp. 621-623) demonstrate this empirically via a "Bounded-Memory Adaptation Model" (BAM) wherein the robot maintains a mixed-observability MDP over the human's latent adaptability, showing that mutual adaptation via belief-space planning significantly outperforms fixed strategies.

\begin{figure}[H]
\centering
\includegraphics[width=0.85\textwidth]{image/lecture1-interaction-paradigms.png}
\caption{Lecture-1 slide defining the four HRI interaction paradigms by interdependency: coexistence, cooperation, collaboration, and instruction. The POMDP framework is necessary for graduating beyond coexistence, as collaboration requires modelling the human's unobservable mental states.}
\label{fig:lecture1-interaction-paradigms}
\end{figure}

\begin{figure}[H]
\centering
\begin{tikzpicture}[
    node distance=2.0cm and 2.5cm,
    state/.style={circle, draw=blue!70, thick, minimum size=1.0cm,
                  fill=blue!10, font=\small\sffamily},
    obs/.style={circle, draw=orange!70, thick, minimum size=1.0cm,
                fill=orange!10, font=\small\sffamily},
    action/.style={rectangle, rounded corners=2pt, draw=green!60, thick,
                   minimum width=0.8cm, minimum height=0.6cm,
                   fill=green!10, font=\scriptsize\sffamily},
    >=Stealth
]

% Hidden states (middle row)
\node[state] (s0) at (0, 1.5) {$s_0$};
\node[state] (s1) at (3.5, 1.5) {$s_1$};
\node[state] (s2) at (7, 1.5) {$s_2$};
\node[state] (s3) at (10.5, 1.5) {$s_3$};
\node at (11.8, 1.5) {$\cdots$};

% Observations (bottom row)
\node[obs] (o1) at (3.5, -0.5) {$o_1$};
\node[obs] (o2) at (7, -0.5) {$o_2$};
\node[obs] (o3) at (10.5, -0.5) {$o_3$};

% Actions (top row)
\node[action] (a0) at (1.75, 3.5) {$a_0$};
\node[action] (a1) at (5.25, 3.5) {$a_1$};
\node[action] (a2) at (8.75, 3.5) {$a_2$};

% State transitions Pr(s'|s,a)
\draw[->, thick, blue!60] (s0) -- (s1) node[midway, below, font=\tiny\sffamily\itshape] {$\Pr(s'|s,a)$};
\draw[->, thick, blue!60] (s1) -- (s2);
\draw[->, thick, blue!60] (s2) -- (s3);

% Observation emissions Pr(e|s)
\draw[->, thick, orange!60] (s1) -- (o1) node[midway, right, font=\tiny\sffamily\itshape] {$\Pr(e|s)$};
\draw[->, thick, orange!60] (s2) -- (o2);
\draw[->, thick, orange!60] (s3) -- (o3);

% Action influence on state transitions
\draw[->, thick, green!50, dashed] (a0) -- (s1);
\draw[->, thick, green!50, dashed] (a1) -- (s2);
\draw[->, thick, green!50, dashed] (a2) -- (s3);

% === THE "UMBRELLA" (Lecture 7): action-to-action and observation-to-action arcs ===
% Action to next action (policy depends on history)
\draw[->, thick, purple!40] (a0) to[bend left=25] (a1);
\draw[->, thick, purple!40] (a1) to[bend left=25] (a2);
% Observation to next action (observations inform future decisions)
\draw[->, thick, purple!40] (o1) to[bend right=40] (a1);
\draw[->, thick, purple!40] (o2) to[bend right=40] (a2);
% Long-range observation-to-action arcs (history dependency)
\draw[->, thick, purple!20] (o1) to[bend right=50] (a2);

% Labels
\node[font=\tiny\sffamily, text=blue!70, above left=0.05cm of s0] {Hidden};
\node[font=\tiny\sffamily, text=orange!70, below=0.1cm of o1] {Observable};

% Grey dashed box around hidden states
\draw[dashed, gray!50, rounded corners=5pt] (-0.8, 0.7) rectangle (11.5, 2.3);
\node[font=\tiny\sffamily\itshape, text=gray!70] at (5.25, 0.85) {Latent states (Trust $\times$ Cognitive Load) --- not directly accessible};

% Umbrella label
\node[font=\tiny\sffamily\itshape, text=purple!60] at (5.25, 4.3) {``Umbrella'' (Lecture 7): policy depends on \textbf{entire} action-observation history};

\end{tikzpicture}
\caption{POMDP graphical model. Hidden states $s_t$ (blue) evolve via $\Pr(s'|s,a)$, influenced by actions $a_t$ (green). Observations $o_t$ (orange) are emitted via $\Pr(e|s)$. Critically, the purple ``umbrella'' arcs show that each action depends on \textit{all} prior actions and observations (the history $h_t$), making the POMDP policy non-Markovian even though the belief update itself is Markovian (Lecture 7; Kaelbling, Littman and Cassandra, 1998).}
\label{fig:pomdp-graphical-model}
\end{figure}

## 2.2 Uncertainty, Belief States, and Decision-Making

Because the true state is hidden, the POMDP agent maintains a **belief state** $b$: a probability distribution over all possible states $S$, where $b(s)$ represents the agent's subjective probability that the environment is in state $s$, such that $\sum_{s \in S} b(s) = 1$. After taking action $a$ and receiving observation $o$, the belief state is updated via **Bayesian filtering**:

$$
b'(s') = \eta \cdot O(s', a, o) \sum_{s \in S} T(s, a, s') \cdot b(s)
$$

 $\eta$ is a normalisation constant ensuring $\sum_{s'} b'(s') = 1$. This update rule captures the core epistemic challenge of HRI: the robot must continuously revise its model of the human's internal state as new and could-be contradictory evidence arrives. As Lecture 3 discussed regarding affective computing, the robot utilises descriptors (e.g., pitch, MFCCs, zero-crossing rate) to extract observations from the human's behaviour, and thus *feeds* these into the belief update process whereby each observation incrementally refines the robot's understanding.

The belief state $b$ therefore serves as a **sufficient statistic** for the entire interaction history, compressing all past actions and observations into a single probability vector (Kaelbling, Littman and Cassandra, 1998).

## 2.3 Challenges of Trust Modelling and the POMDP Response

Trust is a latent psychological variable; it cannot be directly measured, only inferred from observable behavioural indicators. Lee and See (2004, p. 54) define trust as "the attitude that an agent will help achieve an individual's goals in a situation characterised by uncertainty and vulnerability"; a definition foregrounding the latent nature that necessitates probabilistic modelling. Three core challenges arise.

### 2.3.1 The Measurement Problem

Observations such as task compliance rate, response latency, gaze direction (Lecture 2), and verbal affirmations are noisy proxies. Hancock et al.'s (2011, p. 520) meta-analysis of 29 empirical studies confirms this, finding that robot performance-based factors exhibit the strongest correlation with trust (mean r = +0.34, p. 522), yet even these explain only modest variance; a user may comply with a robot's suggestion despite low trust (e.g., due to time pressure), or indeed refuse despite high trust (e.g., due to task complexity), and thus the observation alone cannot reliably disambiguate the latent state.

### 2.3.2 Temporal Dynamics

Trust evolves non-linearly, as it builds slowly through consistent performance but degrades rapidly after errors. This asymmetry is empirically confirmed by Desai et al. (2013, p. 256), who found that "recovery of trust after a reliability drop occurs at a slower pace than the pace at which trust develops before reliability drops". The *Recovering From Mistakes* pattern (Kahn et al., 2008, p. 101) is therefore critical: a robot that acknowledges and corrects errors can arrest trust decay, whereas one that ignores failures risks appearing "aggressive" (Lecture 4).

### 2.3.3 Computational Intractability

Solving POMDPs exactly is PSPACE-complete (Papadimitriou and Tsitsiklis, 1987), as the belief simplex is continuous even with finite $|S|$. Practical HRI applications therefore utilise approximate solvers such as PBVI (Pineau, Gordon and Thrun, 2003) or POMCP (Silver and Veness, 2010) to achieve tractable real-time planning.

The POMDP addresses these challenges by encoding trust as a hidden state variable, observations as probabilistic signals thereof, and actions as trust-modulating strategies (Chen et al., 2020); trust is thereby modelled as a continuously-evolving distribution rather than a brittle threshold-based heuristic (a rigid binary switch ignoring subtle fluctuations).

## 2.4 Proposed Neuro-Symbolic POMDP Model: Neo Robot with OpenAI Cognitive Architecture

To concretise this framework, I propose a neuro-symbolic POMDP model for a Neo (Pepper) humanoid robot augmented with an OpenAI multimodal API, deployed as an elderly medication-adherence assistant. LLMs are powerful observation extractors, capable of parsing unstructured human behaviour into structured probabilistic assessments; however, they are inherently stateless (each API call is independent, with no temporal memory) and prone to hallucination (Ji et al., 2023). Wrapping the API inside a POMDP belief state $b(s)$ therefore provides the temporal scaffold the LLM lacks: a continuously-updated model of the human's latent states (Trust, Cognitive Load) persisting across the full interaction. This neuro-symbolic paradigm, wherein a neural subsystem handles perception whilst a symbolic subsystem governs reasoning, represents what Garcez and Lamb (2023, p. 12389) term the 'third wave' of AI. Ahn et al. (2022) demonstrated via SayCan that LLMs can ground language commands in physical robotic affordances, establishing LLM-directed action selection; however, their architecture lacks the temporal belief maintenance that a POMDP provides, a gap this model directly addresses.

\begin{figure}[H]
\centering
\begin{tikzpicture}[
    node distance=1.5cm and 2.0cm,
    block/.style args={#1}{rectangle, rounded corners=3pt, draw=black!70, thick,
                  minimum width=2.5cm, minimum height=1.0cm, fill=#1,
                  font=\scriptsize\sffamily, align=center},
    human/.style={circle, draw=black!60, very thick, minimum size=0.9cm,
                  fill=white, font=\small\sffamily\bfseries},
    >=Stealth
]

% Bottom row: Neural perception pathway
\node[human] (H) at (0, 0) {H};
\node[below=0.15cm of H, font=\tiny\sffamily\itshape] {Elderly User};

\node[block=purple!20, text width=2.0cm] (neo) at (3.5, 0)
    {Neo Sensors\\{\tiny Camera, Mic,}\\{\tiny Touch}};

\node[block=teal!20, text width=2.8cm, minimum height=1.2cm] (api) at (7.5, 0)
    {\textbf{OpenAI API}\\{\tiny Multimodal LLM}\\{\tiny (Vision + Speech)}};
\node[below=0.15cm of api, font=\tiny\sffamily\itshape, text=teal!70] {$O(s', a, o)$};

\node[block=orange!20, text width=1.8cm] (obs) at (11.5, 0)
    {$o \in \Omega$\\{\tiny Comply,}\\{\tiny Hesitate, \ldots}};

% Top row: Symbolic reasoning pathway
\node[block=blue!20, text width=3.0cm, minimum height=1.2cm] (belief) at (11.5, 3)
    {\textbf{Belief Update}\\{\tiny $b'(s') = \eta \cdot O \cdot \sum T \cdot b$}};
\node[above=0.1cm of belief, font=\tiny\sffamily\itshape, text=blue!70] {POMDP Temporal Engine};

\node[block=green!20, text width=2.2cm] (policy) at (7.5, 3)
    {$\pi^*(b)$\\{\tiny Optimal}\\{\tiny Policy}};

\node[block=red!20, text width=2.2cm] (exec) at (3.5, 3)
    {Execution\\{\tiny NLG + Gesture}\\{\tiny via OpenAI}};

% Arrows: perception pathway
\draw[->, thick] (H) -- (neo);
\draw[->, thick] (neo) -- (api) node[midway, above, font=\tiny\sffamily\itshape] {raw data};
\draw[->, thick] (api) -- (obs) node[midway, above, font=\tiny\sffamily\itshape] {$P(o|s',a)$};

% Arrows: up to POMDP
\draw[->, thick] (obs) -- (belief);

% Arrows: reasoning pathway
\draw[->, thick] (belief) -- (policy) node[midway, above, font=\tiny\sffamily\itshape] {$b$};
\draw[->, thick] (policy) -- (exec) node[midway, above, font=\tiny\sffamily\itshape] {$a \in A$};

% Arrow: back to human
\draw[->, thick] (exec) -- (H) node[midway, left, font=\tiny\sffamily\itshape, align=center] {speech +\\gesture};

\node[block=blue, text width=1.6cm, minimum height=0.7cm, font=\tiny\sffamily] (states) at (14.5, 3)
    {$S$: Trust\\$\times$ Cog.\ Load};
\draw[->, dashed, draw=blue!40] (states.west) -- (belief.east);

% Subsystem labels
\node[font=\scriptsize\sffamily\bfseries, text=purple!50] at (5.5, -1.2) {\textit{Neural Subsystem} (Perception)};
\node[font=\scriptsize\sffamily\bfseries, text=blue!50] at (7.5, 4.3) {\textit{Symbolic Subsystem} (Reasoning)};

\end{tikzpicture}
\caption{Neuro-symbolic architecture of the proposed OpenAI-POMDP medication-adherence system. The \textit{neural subsystem} (bottom) utilises the OpenAI multimodal API as the observation function ($O$), parsing high-dimensional sensory data into discrete probabilistic observations. The \textit{symbolic subsystem} (top) maintains the POMDP belief state and optimal policy $\pi^*(b)$, providing temporal memory via Bayesian filtering. Actions are translated back through the API into natural language and gestures for the Neo robot (Garcez and Lamb, 2023; Ahn et al., 2022).}
\label{fig:neuro-symbolic-arch}
\end{figure}

### 2.4.1 The Neuro-Symbolic Architecture

The Neo robot's onboard sensors (camera, microphone array, tactile sensors) capture raw multimodal data from the elderly user, transmitted to the OpenAI multimodal API serving as the **observation function** ($O$). The API processes this stream, analysing facial action units, extracting prosodic descriptors (pitch, MFCCs, zero-crossing rate) from speech (Lecture 3), and interpreting gestural semantics, to output a structured observation $o \in \Omega$. Crucially, the API provides a probability distribution over possible observations rather than a categorical label, thereby preserving the epistemic uncertainty the POMDP requires; the observation function thus feeds structured assessments continuously throughout the interaction wherein the Bayesian update incrementally refines the model of the user. Concretely, if the robot performs Verbal\_Remind and the API observes Hesitate, the belief shifts toward medium-trust, high-load states; $\pi^*(b)$ consequently selects Explain\_Benefits rather than escalating to physical assistance, as the belief indicates the user is cognitively loaded rather than non-compliant.

### 2.4.2 Formal Specification

- **State Space** ($S$): Trust $\in \{$Low, Medium, High$\}$ $\times$ Cognitive Load $\in \{$Low, High$\}$, yielding $|S| = 6$.
- **Action Space** ($A$): $\{$Verbal\_Remind, Explain\_Benefits, Offer\_Physical\_Assist, Increase\_Autonomy, Disengage$\}$. The POMDP selects abstract actions; the API translates these into culturally-calibrated language and gestures via the Neo robot.
- **Observation Space** ($\Omega$): $\{$Comply, Hesitate, Verbal\_Refuse, Ignore, Gaze\_Avert$\}$, extracted by the OpenAI API from the raw multimodal stream.
- **Observation Function** ($O$): $P(o \mid s', a)$ is estimated by the API's multimodal inference; e.g. $P(\text{Comply} \mid \text{HighTrust, LowLoad}, \text{Remind}) = 0.8$, derived from the user's facial configuration and vocal tone.
- **Transition Function** ($T$): Models trust dynamics parametrically. An unneeded Offer\_Physical\_Assist violating personal proxemics (Lecture 4) degrades trust: $P(\text{Low} \mid \text{Med}, \text{Assist}) = 0.6$; conversely, a well-timed Explain\_Benefits yields $P(\text{High} \mid \text{Med}, \text{Explain}) = 0.5$.
- **Reward Function** ($R$): Successful medication adherence yields $R = +10$; preserving user autonomy (choosing Increase\_Autonomy when trust is High) yields $R = +3$; unwanted physical assistance incurs $R = -5$, reflecting the social cost of proxemic violation. Notably, both $O$ and $R$ must be culturally parametrised per the findings in Task 1; the proxemic penalty, for instance, should be weighted more heavily for non-contact cultures.

\begin{figure}[H]
\centering
\begin{tikzpicture}
\begin{axis}[
    width=12cm, height=7cm,
    xlabel={Timestep},
    ylabel={Belief Probability $b(s)$},
    xmin=-0.3, xmax=2.7,
    ymin=0, ymax=0.65,
    xtick={0, 1, 2},
    xticklabels={$t_0$, $t_1$, $t_2$},
    ytick={0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6},
    legend style={at={(0.02,0.98)}, anchor=north west, font=\scriptsize\sffamily,
                  draw=black!30, fill=white, rounded corners=2pt},
    grid=major,
    grid style={gray!20},
    every axis label/.style={font=\small\sffamily},
    every tick label/.style={font=\scriptsize\sffamily},
]

% High Trust, Low Load
\addplot[color=blue!70, thick, mark=*, mark size=3pt] coordinates {
    (0, 0.167) (1, 0.08) (2, 0.18)
};
\addlegendentry{$b$(High Trust, Low Load)}

% High Trust, High Load
\addplot[color=blue!30, thick, mark=square*, mark size=2.5pt] coordinates {
    (0, 0.167) (1, 0.12) (2, 0.22)
};
\addlegendentry{$b$(High Trust, High Load)}

% Med Trust, Low Load
\addplot[color=orange!80, thick, mark=*, mark size=3pt] coordinates {
    (0, 0.167) (1, 0.28) (2, 0.15)
};
\addlegendentry{$b$(Med Trust, Low Load)}

% Med Trust, High Load  (THE DOMINANT STATE after Hesitate)
\addplot[color=red!70, thick, mark=triangle*, mark size=3.5pt] coordinates {
    (0, 0.167) (1, 0.40) (2, 0.20)
};
\addlegendentry{$b$(Med Trust, High Load)}

% Low Trust, Low Load
\addplot[color=gray!60, thick, mark=diamond*, mark size=2.5pt, dashed] coordinates {
    (0, 0.167) (1, 0.08) (2, 0.05)
};
\addlegendentry{$b$(Low Trust, Low Load)}

% Low Trust, High Load
\addplot[color=gray!30, thick, mark=pentagon*, mark size=2.5pt, dashed] coordinates {
    (0, 0.167) (1, 0.04) (2, 0.20)
};
\addlegendentry{$b$(Low Trust, High Load)}

% Uniform prior line
\addplot[dashed, gray!50, thin] coordinates {(-0.3, 0.167) (2.7, 0.167)};

% Annotations: actions and observations
\node[font=\tiny\sffamily, text=black!60, align=center] at (axis cs: -0.15, 0.19) {Uniform\\prior: $\frac{1}{6}$};

% Action/observation labels between timesteps
\node[font=\scriptsize\sffamily\itshape, text=green!50!black, align=center] at (axis cs: 0.5, 0.58) {$a_0$: Verbal\_Remind};
\node[font=\scriptsize\sffamily\itshape, text=orange!70!black, align=center] at (axis cs: 0.5, 0.52) {$o_1$: Hesitate};

\node[font=\scriptsize\sffamily\itshape, text=green!50!black, align=center] at (axis cs: 1.5, 0.58) {$a_1$: Explain\_Benefits};
\node[font=\scriptsize\sffamily\itshape, text=orange!70!black, align=center] at (axis cs: 1.5, 0.52) {$o_2$: Comply};

% Red delta annotations at t=1
\draw[red!70, thick, ->] (axis cs: 1.12, 0.167) -- (axis cs: 1.12, 0.39)
    node[midway, right, font=\tiny\sffamily\bfseries, text=red!70] {+0.23};

% Red delta annotation at t=2 (Med High Load drops)
\draw[red!70, thick, ->] (axis cs: 2.12, 0.40) -- (axis cs: 2.12, 0.21)
    node[midway, right, font=\tiny\sffamily\bfseries, text=red!70] {$-$0.20};

\end{axis}
\end{tikzpicture}
\caption{Belief evolution across two interaction cycles. At $t_0$, the uniform prior assigns equal probability ($\frac{1}{6}$) to all six states. After the robot performs Verbal\_Remind and the API observes Hesitate, the belief at $t_1$ concentrates on medium-trust, high-cognitive-load states (red triangle, +0.23); the policy $\pi^*(b_1)$ consequently selects Explain\_Benefits rather than escalating to physical assistance. At $t_2$, the observation of Comply redistributes belief toward higher-trust states ($-$0.20 from the dominant state), demonstrating the incremental Bayesian refinement that distinguishes the POMDP from a stateless LLM.}
\label{fig:belief-evolution}
\end{figure}

### 2.4.3 Benefits and Limitations

The model's strength lies in neuro-symbolic complementarity: the API parses unstructured multimodal reality into discrete observations, whilst the POMDP provides the temporal cognitive engine (the belief state $b$) that the stateless LLM fundamentally cannot. Unlike traditional solvers such as PBVI (Pineau, Gordon and Thrun, 2003) which struggle with high-dimensional unstructured observations, this approach delegates perceptual dimensionality-reduction to the LLM, thereby preserving the tractability of the belief update. However, the architecture introduces several limitations: 1) a fundamental mathematical friction: the POMDP relies on the Markov property with a stationary observation function $O(s', a, o)$, yet the LLM is inherently non-stationary; its outputs depend on a dynamic context window, meaning the observation function shifts based on the LLM's own internal states, and thus the belief update is technically an approximation rather than an exact sufficient statistic. The practical consequence is insidious: if the LLM's interpretation silently shifts (e.g., following an API version update), the belief state degrades without any mechanism to detect this drift; 2) API latency (200-800ms) may disrupt real-time proxemic responsiveness (Lecture 4); 3) the LLM's stochastic nature means identical inputs may yield different observation distributions, introducing unmodelled noise into the Bayesian update; and 4) the observation model may inherit training-data biases, degrading inference accuracy for elderly users if the model was predominantly trained on younger demographics (Lecture 5).

## 2.5 Ethical and Social Implications

By operationalising trust as a now-computable metric, the POMDP risks enabling exploitation: insofar as the reward function solely prioritises compliance, the optimal policy may learn to time requests when inferred cognitive load is highest. Designers must therefore encode user autonomy into the reward structure, lest assistance erode into manipulation. Sharkey (2014, pp. 69-70) frames this via the Capability Approach: the robot must expand rather than impede access to Nussbaum's central capabilities, and thus the $R = +3$ autonomy bonus is not merely a design preference but an ethical imperative encoding that dignity requires preservation of choice.

The OpenAI API introduces three additional ethical dimensions. Firstly, **hallucination risk**: LLMs generate plausible but factually incorrect outputs (Ji et al., 2023); in a medication-adherence context, misclassifying confused hesitation as willing compliance could trigger inappropriate actions with direct health consequences. Explainable AI (Lecture 5) therefore becomes non-negotiable: the POMDP must justify *why* it selected a particular action, tracing the decision through the belief state to the specific observations extracted. Secondly, **cloud-data sovereignty**: continuous multimodal processing transmitted to third-party servers risks what Sharkey and Sharkey (2012, pp. 35-36) identify as monitoring that infringes on "the right to privacy" (Figure~\ref{fig:lecture5-privacy-surveillance}); the user's most vulnerable moments are thereby streamed to servers whose data-handling policies cannot be meaningfully audited. Finally, **API latency and proxemic violation**: response delays during a time-critical approach may cause the robot to freeze or fail to yield, behaviour Lecture 4 identifies as "aggressive" (Figure~\ref{fig:lecture4-aggressive-robot}). The ethical watchword is therefore proactive regulation (Lecture 5, Figure~\ref{fig:lecture5-ethics-approaches}): designers must encode transparent, auditable constraints *ex ante* into both the reward function and the API pipeline, ensuring the robot does not merely *model* trust but actively *earns* it through explainable, privacy-preserving behaviour.

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

\begin{figure}[H]
\centering
\includegraphics[width=0.75\textwidth]{image/lecture5-ethics-approaches.png}
\caption{Lecture-5 slide contrasting ``Bottom up'' and ``Pro-active'' ethical approaches to AI regulation, underpinning the argument that designers must encode constraints \textit{ex ante} rather than learning from harm after deployment.}
\label{fig:lecture5-ethics-approaches}
\end{figure}

\begin{figure}[H]
\centering
\includegraphics[width=0.75\textwidth]{image/lecture5-biased-algorithms.png}
\caption{Lecture-5 slide identifying the biased-algorithms problem: ``AI trains on dataset that may contain a bias (e.g.\ favors young white men)'' --- relevant to the observation model's potential demographic degradation when applied to elderly users (Section 2.4).}
\label{fig:lecture5-biased-algorithms}
\end{figure}

\newpage

# References

- [ ] PEER-REVIEWED OR CONFERENCE SOURCES ONLY

## Task (1)'s

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

## Task (2)'s

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
ChatGPT & Finding relevant pages to read in the paper \textbf{(A4)} & If the paper takes too long to consume efficiently \\
\hline
ChatGPT & General conversations via web-search AI about how the topic relates to others' studies \textbf{(A4)} & Few times \\
\hline
TODO & TODO & TODO \\
\hline
\end{tabular}

- [X] I understand that the ownership and responsibility for the academic integrity of this submitted assessment falls with me, the student.
- [X] I confirm that all details provide above are an accurate description of how AI was used for this assessment.
