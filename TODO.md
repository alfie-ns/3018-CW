# COMP3018 Set Exercises -- TODO Reminders

**Deadline: 12th March 2026 (15:00)**
**Feedback: 31st March 2026 (15:00)**

-----

## General Notes

- [ ] Talk about further AI theory
- [ ] Ensure to balance this with 2006, allocate good amount to spend on **actually typing this**
- [ ] Use the words 'classify', 'classification', etc somewhere
- [ ] 'may be inclined to classify...'???
- [ ] MATLAB code snippets?

-----

## STEP ZERO: Read the Papers (Before Writing Anything)

- [ ] **Read Kaplan (2004)** -- "Who is afraid of the humanoid?" -- extract: Frankenstein Complex, animism/Shinto, industrial normalisation in Japan
- [ ] **Read Kahn et al. (2008)** -- "Design patterns for sociality in HRI" -- list out every named design pattern (Initial Introduction, Reciprocal Turn-Taking, etc.)
- [ ] Find **2-3 papers on technology/robot acceptance in African contexts** -- look for Hofstede's dimensions applied to Sub-Saharan Africa, Ubuntu philosophy + technology
- [ ] Find **2-3 foundational POMDP-HRI papers** -- Nikolaidis et al., Javdani et al., or Chen et al. on trust modelling
- [ ] Find **1-2 papers on ethical implications of adaptive/persuasive robots** -- for Task 2-5

-----

## Task 1: Cultural Differences & HRI Design (1,750 words max)

### Part 1-1: Summarise Kaplan (20% = ~350 words)

- [ ] Cover BOTH theological/philosophical AND industrial dimensions
- [ ] West: Frankenstein Complex, Judaeo-Christian creation anxiety, Terminator trope
- [ ] East: Shinto animism (kami in all things), Buddhism (no born/made divide), post-war manufacturing normalisation
- [ ] Anchor every claim to Kaplan's actual text with page numbers

### Part 1-2: Propose African Factors (20% = ~350 words)

- [ ] Need **at least two distinct cultural factors** with peer-reviewed backing
- [ ] Ubuntu philosophy ("I am because we are") -- communal personhood
- [ ] Hofstede's power distance / collectivism dimensions for sub-Saharan Africa
- [ ] Oral tradition / storytelling as interaction paradigm
- [ ] **DO NOT just speculate -- every factor needs a citation**

### Part 1-3: Design Traits for East/West/Africa (30% = ~525 words)

- [ ] Concrete, specific traits (appearance AND behaviour)
- [ ] Consider a LaTeX table mapping regions to traits
- [ ] East: humanoid acceptance, emotional expressivity, social role integration
- [ ] West: functional/tool-like, transparency, user control emphasis
- [ ] Africa: communal interaction, elder-respectful, storytelling-capable
- [ ] Each trait must link back to the cultural factor from 1-1/1-2

### Part 1-4: Adapt Kahn et al. (2008) Patterns (30% = ~525 words)

- [ ] Select 3-4 specific named design patterns from Kahn et al.
- [ ] Show concretely HOW each pattern changes per region
- [ ] **LaTeX table or diagram here would be strong**
- [ ] Link modifications back to cultural factors (closed argumentative loop)

-----

## Task 2: POMDPs in HRI (1,650 words max)

### Part 2-1: POMDP Role in Trust/Cooperation/Collaboration (20% = ~330 words)

- [ ] Define POMDP tuple formally: (S, A, T, R, Omega, O, gamma)
- [ ] Bridge from MDP (COMP3003) to POMDP -- show the examiner you're building on prior knowledge
- [ ] Explain WHY partial observability matters for HRI (human mental states are hidden)
- [ ] Cite foundational POMDP-HRI papers

### Part 2-2: Uncertainty in Collaboration (20% = ~330 words)

- [ ] Belief states b(s) -- probability distribution over hidden states
- [ ] How robot uses observations to update beliefs (Bayesian filtering)
- [ ] Concrete example of uncertainty in HRI context
- [ ] Link to decision-making under uncertainty

### Part 2-3: Challenges of Modelling Trust (15% = ~250 words)

- [ ] Trust as latent variable -- cannot be directly measured
- [ ] Trust is dynamic (builds/erodes over time)
- [ ] Computational cost of POMDP solving (curse of dimensionality)
- [ ] Subjectivity of trust across individuals

### Part 2-4: Develop a Specific POMDP Model (35% = ~575 words) **THIS IS THE CENTREPIECE**

- [ ] Choose a concrete scenario (e.g., assistive medication robot for elderly users)
- [ ] **Formally specify the full POMDP tuple with actual values**
- [ ] S = {trust levels x task states}, A = {robot actions}, O = {observable user behaviours}
- [ ] **TikZ diagram: POMDP graphical model showing hidden states -> observations -> actions**
- [ ] Explain transition dynamics (how trust changes based on robot actions)
- [ ] State benefits AND limitations explicitly
- [ ] This section alone is worth 35% -- give it the most love

### Part 2-5: Ethical/Social Implications (10% = ~165 words)

- [ ] Manipulation risk (robot optimising for compliance, not wellbeing)
- [ ] Privacy (inferring mental states from observations)
- [ ] Autonomy erosion (human deferring to robot decisions)
- [ ] Keep concise -- 10% weighting means don't overwrite

-----

## COMP3003 Feedback to Apply (Non-Negotiables)

- [ ] **Every analytical claim references other studies** (the #1 feedback point)
- [ ] **Complete every answer fully** -- no trailing off (V*(S5) mistake)
- [ ] Use first-principles exposition style (your strength -- keep it)
- [ ] Harvard referencing throughout
- [ ] Peer-reviewed papers ONLY (journals and conference papers)
- [ ] Include AI Declaration appendix (A2 + A4 only)

-----

## Quality Checks Before Submission

- [ ] Word count Task 1: <= 1,750
- [ ] Word count Task 2: <= 1,650
- [ ] All sub-questions explicitly answered (not implicit)
- [ ] Every discussion claim backed by literature
- [ ] LaTeX compiles cleanly
- [ ] TikZ diagrams render correctly
- [ ] Check against Gemini for critique
- [ ] References are all Harvard style
- [ ] PDF format for submission
- [ ] AI Declaration appendix included and signed
