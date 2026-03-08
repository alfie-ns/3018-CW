---
title: "Test TikZ Figures — Belief Evolution Variants"
subtitle: "Draft visualisations for COMP3018 Set Exercises"
---

<!--
  Compile with: pandoc test-tex-figures.md -o test-tex-figures.pdf --pdf-engine=xelatex
  These are simplified, humanistic-style belief diagrams inspired by
  the non-monotonic posterior figure. They prioritise clarity and
  hand-drawn-like annotation over visual complexity.
-->

\usepackage{tikz, pgfplots, amsmath, xcolor}
\usetikzlibrary{positioning, arrows.meta, calc}
\pgfplotsset{compat=1.18}

\definecolor{trustblue}{HTML}{2E5FA1}
\definecolor{loadred}{HTML}{C0392B}
\definecolor{annotatered}{HTML}{E74C3C}
\definecolor{softgray}{HTML}{888888}

<!-- ============================================================ -->
<!-- FIGURE 1: Simplified Belief Evolution (3-state, 2 timesteps)  -->
<!-- Style: matches the attached non-monotonic posterior image      -->
<!-- ============================================================ -->

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
\caption{Simplified belief evolution (3 trust states). The medium-trust state exhibits non-monotonic behaviour: rising sharply after observing Hesitate ($t_1$), then falling after Comply ($t_2$). Red annotations show deviations from the prior, mirroring the style of classical non-monotonic posterior plots.}
\label{fig:test-belief-simple}
\end{figure}

\vspace{1em}

<!-- ============================================================ -->
<!-- FIGURE 2: Trust Trajectory — Single State Over Many Steps     -->
<!-- Minimal line graph with deviation bands                        -->
<!-- ============================================================ -->

\begin{figure}[H]
\centering
\begin{tikzpicture}
\begin{axis}[
    width=11cm, height=5.5cm,
    xlabel={Interaction Cycle},
    ylabel={$b(\text{High Trust})$},
    xmin=0, xmax=6,
    ymin=0, ymax=1.0,
    xtick={0,1,2,3,4,5,6},
    xticklabels={$t_0$,$t_1$,$t_2$,$t_3$,$t_4$,$t_5$,$t_6$},
    every axis label/.style={font=\small\sffamily},
    every tick label/.style={font=\scriptsize\sffamily},
    grid=none,
    axis lines=left,
    axis line style={->, thick},
]

% Prior reference line
\addplot[dashed, softgray, thin] coordinates {(0, 0.167) (6, 0.167)};
\node[font=\tiny\sffamily, text=softgray, anchor=east] at (axis cs: 0.9, 0.21) {Prior: $\frac{1}{6}$};

% Trust trajectory — non-monotonic, gradually rising
\addplot[color=trustblue, very thick, mark=*, mark size=3.5pt] coordinates {
    (0, 0.167) (1, 0.08) (2, 0.18) (3, 0.35) (4, 0.29) (5, 0.55) (6, 0.72)
};

% Observation annotations
\node[font=\tiny\sffamily\itshape, text=loadred, align=center, rotate=0] at (axis cs: 1, 0.02) {Hesitate};
\node[font=\tiny\sffamily\itshape, text=trustblue, align=center] at (axis cs: 2, 0.25) {Comply};
\node[font=\tiny\sffamily\itshape, text=trustblue, align=center] at (axis cs: 3, 0.42) {Comply};
\node[font=\tiny\sffamily\itshape, text=loadred, align=center] at (axis cs: 4, 0.22) {Gaze\\Avert};
\node[font=\tiny\sffamily\itshape, text=trustblue, align=center] at (axis cs: 5, 0.62) {Comply};
\node[font=\tiny\sffamily\itshape, text=trustblue, align=center] at (axis cs: 6, 0.79) {Comply};

% Key dip annotation
\draw[annotatered, thick, ->] (axis cs: 3.85, 0.35) -- (axis cs: 3.85, 0.295)
    node[midway, left, font=\tiny\sffamily\bfseries, text=annotatered] {$-$0.06};

\end{axis}
\end{tikzpicture}
\caption{Trust trajectory across six interaction cycles for $b(\text{High Trust})$. Despite the overall upward trend, the posterior dips at $t_1$ (Hesitate) and $t_4$ (Gaze Avert), illustrating non-monotonic convergence: individual observations can temporarily decrease trust even as the long-run trajectory rises. Each label indicates the observation received at that timestep.}
\label{fig:test-trust-trajectory}
\end{figure}

\vspace{1em}

<!-- ============================================================ -->
<!-- FIGURE 3: Action Selection Threshold Diagram                  -->
<!-- Shows belief crossing a policy threshold — clean, minimal     -->
<!-- ============================================================ -->

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
\caption{Action selection governed by belief thresholds. When $b(\text{Med Trust, High Load})$ exceeds the escalation threshold $\tau = 0.45$ (at $t_2$), the policy switches from Verbal\_Remind to Explain\_Benefits and then Offer\_Physical\_Assist. As trust recovers and the belief drops below $\tau$ (from $t_3$), the robot de-escalates. This demonstrates how the POMDP's policy boundaries produce qualitatively different behaviour from a threshold-free LLM approach.}
\label{fig:test-action-threshold}
\end{figure}

\vspace{1em}

<!-- ============================================================ -->
<!-- FIGURE 4: Observation Surprise — Entropy of Belief Over Time  -->
<!-- Minimalist, one clean line with annotation callouts            -->
<!-- ============================================================ -->

\begin{figure}[H]
\centering
\begin{tikzpicture}
\begin{axis}[
    width=11cm, height=5.5cm,
    xlabel={Interaction Cycle},
    ylabel={Entropy $H(b)$},
    xmin=-0.3, xmax=5.5,
    ymin=0, ymax=3.0,
    xtick={0,1,2,3,4,5},
    xticklabels={$t_0$,$t_1$,$t_2$,$t_3$,$t_4$,$t_5$},
    every axis label/.style={font=\small\sffamily},
    every tick label/.style={font=\scriptsize\sffamily},
    grid=none,
    axis lines=left,
    axis line style={->, thick},
]

% Maximum entropy reference
\addplot[dashed, softgray, thin] coordinates {(-0.3, 2.585) (5.5, 2.585)};
\node[font=\tiny\sffamily, text=softgray, anchor=west] at (axis cs: 4.4, 2.72) {$H_{\max} = \ln 6$};

% Entropy trajectory
\addplot[color=trustblue, very thick, mark=*, mark size=3.5pt] coordinates {
    (0, 2.585) (1, 1.70) (2, 1.45) (3, 1.80) (4, 1.20) (5, 0.75)
};

% Surprise spike annotation
\draw[annotatered, thick, ->] (axis cs: 2.85, 1.45) -- (axis cs: 2.85, 1.78)
    node[midway, right, font=\tiny\sffamily\bfseries, text=annotatered] {+0.35};
\node[font=\tiny\sffamily\itshape, text=loadred, anchor=south] at (axis cs: 3, 1.90) {Surprise!};
\node[font=\tiny\sffamily, text=softgray, align=center] at (axis cs: 3, 2.20) {Unexpected\\Gaze Avert};

% Convergence region
\draw[trustblue!30, thick, dashed, rounded corners=3pt] (axis cs: 3.7, 0.55) rectangle (axis cs: 5.3, 1.35);
\node[font=\tiny\sffamily\itshape, text=trustblue!70] at (axis cs: 4.5, 0.48) {Converging};

\end{axis}
\end{tikzpicture}
\caption{Entropy of the belief distribution over time. Starting from maximum entropy ($H_{\max} = \ln 6 \approx 2.58$ at the uniform prior), the robot's uncertainty decreases as observations narrow the belief. At $t_3$, an unexpected Gaze Avert \textit{increases} entropy (+0.35), representing genuine surprise --- the robot becomes less certain. This non-monotonic entropy decrease mirrors the non-monotonic posterior behaviour: evidence does not always reduce uncertainty.}
\label{fig:test-entropy}
\end{figure}
