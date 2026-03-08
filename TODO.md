# COMP3018 Set Exercises -- TODO Reminders

**Deadline: 12th March 2026 (15:00)**
**Feedback: 31st March 2026 (15:00)**

-----

## General Notes

- [X] Talk about further AI theory
- [ ] Ensure to balance this with 2006, allocate good amount to spend on **actually typing this**
- [ ] Use the words 'classify', 'classification', etc somewhere
- [ ] 'may be inclined to classify...'???
- [ ] MATLAB code snippets?

-----

## STEP ZERO: Read the Papers (Before Writing Anything)

- [X] **Read Kaplan (2004)** -- "Who is afraid of the humanoid?" -- extract: Frankenstein Complex, animism/Shinto, industrial normalisation in Japan
- [X] **Read Kahn et al. (2008)** -- "Design patterns for sociality in HRI" -- list out every named design pattern (Initial Introduction, Reciprocal Turn-Taking, etc.)
- [X] Find **2-3 papers on technology/robot acceptance in African contexts** -- look for Hofstede's dimensions applied to Sub-Saharan Africa, Ubuntu philosophy + technology
- [X] Find **2-3 foundational POMDP-HRI papers** -- Nikolaidis et al., Javdani et al., or Chen et al. on trust modelling
- [X] Find **1-2 papers on ethical implications of adaptive/persuasive robots** -- for Task 2-5

-----

## Task 1: Cultural Differences & HRI Design (1,750 words max)

### Part 1-1: Summarise Kaplan (20% = ~350 words)

- [X] Cover BOTH theological/philosophical AND industrial dimensions
- [X] West: Frankenstein Complex, Judaeo-Christian creation anxiety, Terminator trope
- [X] East: Shinto animism (kami in all things), Buddhism (no born/made divide), post-war manufacturing normalisation
- [X] Anchor every claim to Kaplan's actual text with page numbers

### Part 1-2: Propose African Factors (20% = ~350 words)

- [X] Need **at least two distinct cultural factors** with peer-reviewed backing
- [X] Ubuntu philosophy ("I am because we are") -- communal personhood
- [X] Hofstede's power distance / collectivism dimensions for sub-Saharan Africa
- [X] Oral tradition / storytelling as interaction paradigm
- [X] **DO NOT just speculate -- every factor needs a citation**

### Part 1-3: Design Traits for East/West/Africa (30% = ~525 words)

- [X] Concrete, specific traits (appearance AND behaviour)
- [X] Consider a LaTeX table mapping regions to traits
- [X] East: humanoid acceptance, emotional expressivity, social role integration
- [X] West: functional/tool-like, transparency, user control emphasis
- [X] Africa: communal interaction, elder-respectful, storytelling-capable
- [X] Each trait must link back to the cultural factor from 1-1/1-2

### Part 1-4: Adapt Kahn et al. (2008) Patterns (30% = ~525 words)

- [X] Select 3-4 specific named design patterns from Kahn et al.
- [X] Show concretely HOW each pattern changes per region
- [X] **LaTeX table or diagram here would be strong**
- [X] Link modifications back to cultural factors (closed argumentative loop)

-----

## Task 2: POMDPs in HRI (1,650 words max)

### Part 2-1: POMDP Role in Trust/Cooperation/Collaboration (20% = ~330 words)

- [X] Define POMDP tuple formally: (S, A, T, R, Omega, O, gamma)
- [X] Bridge from MDP (COMP3003) to POMDP -- show the examiner you're building on prior knowledge
- [X] Explain WHY partial observability matters for HRI (human mental states are hidden)
- [X] Cite foundational POMDP-HRI papers

### Part 2-2: Uncertainty in Collaboration (20% = ~330 words)

- [X] Belief states b(s) -- probability distribution over hidden states
- [X] How robot uses observations to update beliefs (Bayesian filtering)
- [X] Concrete example of uncertainty in HRI context
- [X] Link to decision-making under uncertainty

### Part 2-3: Challenges of Modelling Trust (15% = ~250 words)

- [X] Trust as latent variable -- cannot be directly measured
- [X] Trust is dynamic (builds/erodes over time)
- [X] Computational cost of POMDP solving (curse of dimensionality)
- [ ] Subjectivity of trust across individuals

### Part 2-4: Develop a Specific POMDP Model (35% = ~575 words) **THIS IS THE CENTREPIECE**

- [X] Choose a concrete scenario (e.g., assistive medication robot for elderly users)
- [X] **Formally specify the full POMDP tuple with actual values**
- [X] S = {trust levels x task states}, A = {robot actions}, O = {observable user behaviours}
- [X] **TikZ diagram: POMDP graphical model showing hidden states -> observations -> actions**
- [X] Explain transition dynamics (how trust changes based on robot actions)
- [X] State benefits AND limitations explicitly
- [X] This section alone is worth 35% -- give it the most love

### Part 2-5: Ethical/Social Implications (10% = ~165 words)

- [X] Manipulation risk (robot optimising for compliance, not wellbeing)
- [X] Privacy (inferring mental states from observations)
- [X] Autonomy erosion (human deferring to robot decisions)
- [X] Keep concise -- 10% weighting means don't overwrite

-----

## COMP3003 Feedback to Apply (Non-Negotiables)

- [X] **Every analytical claim references other studies** (the #1 feedback point)
- [X] **Complete every answer fully** -- no trailing off (V*(S5) mistake)
- [X] Use first-principles exposition style (your strength -- keep it)
- [X] Harvard referencing throughout
- [X] Peer-reviewed papers ONLY (journals and conference papers)
- [X] Include AI Declaration appendix (A2 + A4 only)

-----

## Quality Checks Before Submission

- [ ] Word count Task 1: <= 1,750
- [ ] Word count Task 2: <= 1,650
- [X] All sub-questions explicitly answered (not implicit)
- [X] Every discussion claim backed by literature
- [ ] LaTeX compiles cleanly
- [ ] TikZ diagrams render correctly
- [ ] Check against Gemini for critique
- [X] References are all Harvard style
- [ ] PDF format for submission
- [X] AI Declaration appendix included and signed
