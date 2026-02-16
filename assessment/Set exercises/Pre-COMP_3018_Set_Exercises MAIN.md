---
title: "COMP3018: Set Exercises Human-Robot Interaction (HRI)"
subtitle: "Cultural Differences and Probabilistic Modelling in Human-Robot Interaction"
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
# Words-To-Use:

- [ ] INTEGRATE ROBOTIC DIAGRAM
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

# 1- Task (1): Cultural Differences and HRI Design (1750*1.1-word)

Kaplan's 2004 identification of East-West fundamental societal divergence is rooted in the observation that "**culture affects the way technology is perceived** and, in a reciprocal manner, **technological evolution shapes culture in particular ways**" (Kaplan, 2004, p. 465); i.e., the cultural, theological, and literary narratives of each region shape the societal meta-layer (the thing behind the thing) that underpins robotic acceptance.

**Western Society (The Frankenstein Syndrome).** Western culture's creation of human-like entities has chronically been regarded suspiciously: Kaplan (2004) identifies this as the "Frankenstein Syndrome": a culturally-filtered conviction wherein "any artificially created humanoid will necessarily turn against its creator" (p. 475). This anxiety is indeed traceable to the Judeo-Christian tradition, which posits "no place for hybrids" between divine creator and human creation (Kaplan, 2004, p. 470). The Western cultural narrative is therefore framed in humanoid robots as "something else, something that should not exist" (p. 476) — a transgression against the natural order. Consequently, Western societies have historically channelled robotic development toward industrial, non-anthropomorphic applications wherein the machine remains a visible *tool* rather than a would-be social entity. Kaplan further notes the concept of "narcissistic shields" (p. 478), whereby Westerners utilise psychological distancing to manage the discomfort of encountering machines that blur the boundary between human and artefact.

## 1.1 Cultural Differences in HRI Acceptance

# References

## Task (1)'s

- Kaplan, F. (2004) 'Who is afraid of the humanoid? Investigating cultural differences in the acceptance of robots', *International Journal of Humanoid Robotics*, 1(3), pp. 1-16. Available at: [https://www.researchgate.net/publication/220065746_Who_is_Afraid_of_the_Humanoid_Investigating_Cultural_Differences_in_the_Acceptance_of_Robots](https://www.researchgate.net/publication/220065746_Who_is_Afraid_of_the_Humanoid_Investigating_Cultural_Differences_in_the_Acceptance_of_Robots) (Accessed: 13 February 2026).

## Task (2)'s

# Appendices

## Appendix A: ...

## Appendix B: 5-Minute Video Demo

- YouTube link: [test](test)

## Appendix C: AI Declaration

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
