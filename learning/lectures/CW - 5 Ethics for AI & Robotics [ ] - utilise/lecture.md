# COMP3018 Lecture 5: Ethics for AI and Robotics -- BRITISH AI Intelligence Extraction

**Module:** COMP3018 Human-Robot Interaction
**Lecturer:** Dr. Amir Aly
**Topic:** Ethics for AI and Robotics
**Extraction Date:** 06/03/2026
**Sources:** Transcript (primary authority) + Slides (structural reference) + Assessment Brief (targeting)

---

## 1. CRITICAL ASSESSMENT INTELLIGENCE [HIGHEST PRIORITY]

### How This Lecture Maps to Each Coursework Task

**TASK 1 -- Cultural Differences and HRI Design (40% of Assessment 1, i.e. 12% of module)**

This lecture is DIRECTLY relevant to Task 1. Dr. Aly explicitly raised cultural divergence in robot acceptance during the nanny robot discussion:

> "So now we have cultural issues here in Japan. They are fine to leave people more robots or probably less sensitive to risks that might appear from robots to some extent than Wisto [the West]."

* This verbatim quote supports Q1 (Kaplan 2004 cultural factors) and Q3 (suggesting traits for East vs. West acceptance). Dr. Aly himself articulates the East-West divide in comfort with autonomous robots -- use this as a framing device when discussing cultural acceptance factors.
* The entire nanny robot discussion reveals Dr. Aly's own position: autonomy, trust, and cultural context determine acceptance. He values students who can articulate WHY cultures differ, not just THAT they differ.
* For Q2 (Africa), note that Dr. Aly said "we have here backgrounds, different backgrounds and different countries. So probably it's opportunity to listen different opinions." He VALUES diverse cultural perspectives and wants you to reason from genuine cultural understanding, not surface-level generalisations.

**TASK 2 -- POMDP Models for HRI (60% of Assessment 1, i.e. 18% of module)**

The ethics lecture connects to POMDP modelling in several critical ways:

* **Trust and uncertainty** are central to both this lecture AND the POMDP task. Dr. Aly's autonomous car dilemma is fundamentally a decision-under-uncertainty problem -- exactly what POMDPs model. When he says "a lot of confusion that might happen might affect the certainty of the decision made", he is describing the core POMDP challenge of partial observability.
* **Q2 (uncertainty in human-robot collaboration):** The hacking concern Dr. Aly raises -- "technology can be hacked. So what the robot is watching or saying okay can be at any moment influenced by external... ways or algorithms" -- is a source of uncertainty that a POMDP must account for. Environmental state can change unpredictably.
* **Q3 (trust modelling challenges):** Dr. Aly's nanny robot discussion reveals trust is not binary -- it depends on supervision level, capability awareness, and cultural background. One student said: "If I'm fully aware of what the robot is capable of doing and what it can't do... then I'm completely comfortable." This maps directly to how belief states about robot capability affect trust in a POMDP framework.
* **Q4 (develop a POMDP model):** The autonomous car scenario Dr. Aly spent the most time on is a PERFECT candidate for your POMDP model. The states (pedestrian positions), observations (sensor readings, partial), actions (swerve left/right/brake), and the ethical reward function (minimise harm, but whose harm?) are all rich POMDP territory. Dr. Aly clearly finds this scenario intellectually compelling -- he returned to it multiple times.
* **Q5 (ethical/social implications of POMDPs):** This ENTIRE lecture is your ammunition for Q5. The question of who is responsible when a POMDP-based system makes a harmful decision, the black-box problem, bias in training data -- all directly from Dr. Aly's mouth.

**TASK 3 -- Literature Review: Assistive Robotics (40% of Assessment 2, i.e. 28% of module)**

The essay requires discussion of ethical issues. This lecture gives you Dr. Aly's exact ethical framework:

* **Ethical challenges section (required in Discussion, 20% of task mark):** Dr. Aly's hierarchy of concerns maps your essay structure: privacy/surveillance, autonomy/agency, bias/fairness, transparency/explainability, responsibility/accountability, job displacement.
* **The PARO robot (healthcare slide, slide 7):** Dr. Aly showed the PARO therapeutic seal robot under "Health Care" -- this is a direct assistive robotics example. His concern about children becoming "too attached to an educational robot" applies to therapeutic robots too: "This also can happen and can have impact that it's attached to an educational robot and then is not able to probably it's like using mobile phone too much."
* **For your essay's ethical issues section** , Dr. Aly explicitly values PROACTIVE ethics over reactive: "The approach we did is like to think about proactively. So in science, we try to put in advance the regulations and some certifications and put some standards." Frame your ethical discussion around proactive design, not just listing problems.
* **Assistive robotics specific concerns from this lecture:** surgery robots ("to which extent you'll feel comfortable to be operated by a robot"), care robots giving wrong medication, nanny robots and child safety, loss of human agency, data privacy in health contexts.

**TASK 4 -- Programming Project (60% of Assessment 2, i.e. 42% of module)**

* Any project you propose MUST address ethical considerations. Dr. Aly's lecture gives you the vocabulary and framework he expects. He will be looking for awareness of: autonomy levels, data privacy, bias mitigation, explainability, and user trust.
* His pre-lecture chat reveals he offers project topics: "I put some of my mine as well, so if you are interested" -- some focused on robotics, others on "healthcare and AI." He mentioned collaborative teams with potential for publication. He told the story of an undergraduate who published in eClinical Medicine: "This is a journal eClinical Medicine. So this was led by undergraduate students and in clinical medicine, this is the highest of any other journal." His message: "don't feel afraid if you find ambitious project. So it is possible to do it."
* For the project report's Introduction and Conclusion sections (10% each), ethical framing using this lecture's content will demonstrate module coherence.

---

## 2. THE ALPHA BRIEF: Complete Critical Intelligence

### Direct Assessment Signals

* [!!!] Dr. Aly values AMBITIOUS students who take on challenging projects -- the eClinical Medicine story was clearly a point of pride. He wants to see intellectual courage: "he didn't fear to work on a topic, you know, trying to accomplish something."
* [!!!] He explicitly said he offers his OWN project topics -- approach him about this for Task 4. Some involve collaborating teams aiming for publication.
* [!!!] Cultural sensitivity is not just a topic for Dr. Aly -- it's a personal lens. He studied at the Sorbonne, has led panel discussions at robotics conferences, and draws on cross-cultural experience. Superficial cultural analysis will not impress him.
* [!!!] He values the PROACTIVE approach to ethics over the bottom-up (reactive) approach. Frame all ethical discussions around anticipation and design-stage thinking.
* [!!!] The autonomous car dilemma is clearly his favourite teaching example -- he spent more time on it than any other single point. He returned to it repeatedly and used it to generate student discussion. Understanding it deeply signals engagement with his thinking.

### Lecturer's Emphasis Patterns (Repetition Count)

* **Autonomy levels / how autonomous should machines be** -- raised 5+ times across the lecture (nanny robot, surgery robot, autonomous car, factory machines, general framework). This is clearly a core concept for Dr. Aly.
* **Trust** -- referenced in nanny robot discussion, surgery discussion, autonomous car discussion, clinician-AI trust. Central to his thinking about HRI.
* **Proactive vs. reactive regulation** -- explicitly contrasted twice, with the VW scandal as the cautionary tale of reactive ethics.
* **"Who is responsible?"** -- asked repeatedly about autonomous car, AI decisions, hacking scenarios. This is the ethical question he most wants students to grapple with.
* **Bias and fairness** -- discussed with the concrete example of facial recognition bias and directly linked to data preparation practices.
* **Black box / explainability** -- introduced "explainable AI" as the response to non-transparent algorithms. Connected it to healthcare trust.

### Warnings and Pitfalls

* [!] Do NOT treat ethics as abstract philosophy disconnected from engineering practice. Dr. Aly moved from meta-ethics to applied ethics quickly and always grounds discussion in real scenarios.
* [!] Do NOT underestimate the approval/regulation process. Dr. Aly was surprised himself: "when I grew up and I started to be for example involved in research, I understood... It's not like as I was thinking, there is actually restrictions." He now respects the rigour -- so should your writing.
* [!] Do NOT ignore the data pipeline when discussing bias. Dr. Aly told his PhD student: "don't try to give, for example, try to make some balance between data. If you give data, for example for one category... 1 million data point and the other category 100, certainly there will be some bias. So try to balance your data when you are preparing." This is practical, not theoretical.

---

## 3. EXHAUSTIVE TOPIC BREAKDOWN

### Topic A: Technology Pervasiveness (Slides 3-10)

**Lecturer's framing:** AI is already embedded everywhere -- pocket (phones), office, finance, transport, healthcare, military, data, "all things everywhere." Dr. Aly uses this to establish stakes: "your mobile phone for example, is an AI tool that can be a spying tool, for example, without, you know, your PC can be a spying tool without, you know, the cameras of your PC can be running and operating and recording without, you know."

**Assessment utility:** This framing is useful for Task 3's Introduction section -- establishing why ethical considerations in assistive robotics are urgent and inescapable.

### Topic B: Issues Raised by Technology (Slides 11-16)

**B1. Definition Problems**

The slide notes: regulation is hard because new technologies (robots, AI, algorithms, IoT, cyber-physical systems) don't fit existing legal categories. Dr. Aly asks: "How autonomous, intelligent, etc.?"

**B2. Privacy, Security, Surveillance**

Dr. Aly's key point: "AI records what you do and transfers data... to whom? To companies? Third party?" He gave the Facebook terms-of-service example: "very long... you might be speaking about third party and transferring data to whichever third party we don't verify. Because even if you don't agree, it will not open the application for you."

He also raised recommendation systems tracking location as an example of passive surveillance: "how the technology observes that you are in this area, they are observing or for example, they learn from your preference and they give you some more customized products."

**Assessment utility (Task 3):** When discussing assistive robotics ethical issues, privacy is paramount -- assistive robots operate in intimate settings (homes, hospitals). Dr. Aly's hacking concern is directly relevant: "what if the robots get hacked?"

**B3. Replacement, Autonomy, Loss of Agency**

The slide lists: Robot/AI-human teams, degrees of autonomy, distributed agency.

Dr. Aly's nuanced position: autonomy level should match risk. He used a spectrum: "Peppa, okay, autonomous take action completely. Because I know like Peppa will not make, you know, huge harm maybe. But if I have cooker hand [Kuka arm?], for example, that can one hit from the coca hand can destroy the wall... So probably I would prefer to have some kind of control."

**Key distinction he draws:** The definition of what SHOULD be autonomous vs. what should NOT be autonomous "is part of the ethics framework."

**Assessment utility (Task 2, Q4):** When building your POMDP model, the autonomy level directly determines what actions are available to the agent vs. what requires human approval. Dr. Aly's Pepper vs. industrial arm distinction is a concrete way to justify action space design in your POMDP.

**B4. Autonomous Driving -- The Core Ethical Dilemma**

Dr. Aly's extended scenario (he spent approximately 10 minutes on this):

The setup: Autonomous car, person crosses street incorrectly, others waiting correctly on the pavement. Three options:

1. Crash into the person crossing wrongly
2. Swerve and crash into innocent bystanders
3. Crash into wall and kill the driver

He then escalated: "what if, for example, the situation become harder and instead of having one person crossing wrongly and one person waiting in the safe area, we have multiple persons crossing wrongly or multiple persons waiting in the safe area."

His critical question: "the risk of the AI algorithm, what it calculates it, it multiplies by the number of people who might be hurted. But then, okay... would it say, okay, I crashed the person... who passed the street wrongly because it is his mistake?"

Then the responsibility question: "Most importantly, if AI took wrong decision, I would be responsible for this... who would be responsible for the act done by AI who should be criminalized if there is an A crime?"

He references the SAE 6 Levels of self-driving autonomy (slide 16):

* Level 0: monitoring, warnings
* Level 1: adaptive cruise control, automated parking
* Level 2: automated driving, but driver must be alert and take over
* Level 5: no human intervention needed

His summary: "even if the car can be used, there's always risk of something to happen. So that's actually the ethics here is about to put the framework that can consider for all this."

**Assessment utility (Task 2, Q4-Q5):** This is your best example for the POMDP ethical implications question. The autonomous car maps perfectly: states are partially observable (pedestrian intentions unknown), actions have irreversible consequences, and the reward function encodes ethical values. Ask: whose utility function does the POMDP optimise?

**B5. Moral and Legal Responsibility (Slide 15)**

Dr. Aly's examples of scenarios needing ethical frameworks:

* Autonomous car drives into group of children
* AI causes crashes in financial markets
* Machines harm workers in a factory
* Care robot gives the wrong medication
* Killer robot kills civilians
* A child gets too attached to an educational robot

His key rhetorical: "we don't have prisons for algorithms, for example. So what would be happening in this case?"

**Assessment utility (Task 3):** For the assistive robotics essay, the "care robot gives wrong medication" example is directly on-topic. Use it as a concrete case study when discussing challenges.

### Topic C: Societal Implications of AI (Slides 17-21)

**C1. The Future of Work**

Dr. Aly referenced Elon Musk's claims about AI replacing jobs. He then shared his own experience: "I recall colleagues in the Faculty of Arts who work in illustrations. They were so worried... I ask one guy, can you make illustration for me? And he tells me, or she tells me, come after several days. But with AI tools you can generate illustration 5 minutes."

His nuanced view: "it killed many jobs, but it created too many other jobs because like AI needs maintenance, AI machines need maintenance, needs, coding needs." He referenced a European Union report supporting this.

His deeper point: "this doesn't mean that our study or our relationship with AI ends or depend only on what we are studying here. Because AI after five years would be largely different from the AI of today."

**Assessment utility (Task 3):** If discussing impact of assistive robotics, job displacement in care work is a relevant societal concern.

**C2. Biased Algorithms**

Slide: "Problem in machine learning: AI trains on dataset that may contain a bias (e.g. favors young white men)"

Dr. Aly's expanded explanation: facial recognition system had "unintentionally majority of white people... So this created bias in judgment." He gave practical advice: "try to balance your data when you are preparing."

He introduced the concept of  **Fairness in AI** : "bias. This is something called bias. And the fairness API, you probably heard about it. Fairness in AI is affected by bias. So they are all related to each other. So to have fairness in judgment in anything, we have to avoid bias."

His position on whether bias is avoidable: "Is bias, for example affordable [avoidable]? This exists, but we can try to take... measures... to consider the data construction of data that we are dealing with and try to avoid it and try to analyze bias, for example to mitigate the effect of bias if happened."

**Assessment utility (Task 3 and Task 4):** Any assistive robotics system you discuss or build must address potential bias. Dr. Aly's pipeline approach (mitigate from data preparation stage) is the framework he expects.

**C3. Non-Transparent Algorithms / Explainability**

Slide: "Decision AI/algorithm black box, I am affected by its decision but do not know how it came to its decision." References Wachter et al. (2017) on "Right to Explanation of Automated Decision Making."

Dr. Aly introduced  **Explainable AI (XAI)** : "It's like a trying to have an interpretation for why the algorithms came to this decision or how it came to this decision."

His healthcare example for why this matters: "A clinician will not understand this... Should the clinician trust what you are giving us judgment? Should the clinician try to have search for? Because if the person trusts what we are giving and if it's wrong, it's responsibility on the clinician or might be wasting resources."

**Assessment utility (Task 3):** Explainability is CRITICAL for assistive robotics in healthcare contexts. A care robot that recommends medication changes must be interpretable to clinicians. Reference Wachter et al. (2017) -- Dr. Aly put it on his slides so he clearly values it.
**Assessment utility (Task 4):** If your project involves any ML component, address explainability. Dr. Aly will notice.

### Topic D: Ethics -- Definitions and Branches (Slides 22-24)

Dr. Aly's definition: "Ethics is a branch of philosophy that deals with the moral principles and the values that guide human knowledge... concerned with what's right and what's wrong, good and bad and what ought to be done."

Three branches:

1. **Meta-ethics:** "Studying where our ethics come from. Are they derived from human nature, society, religion, cultural norms or something universal and objective."
2. **Normative ethics:** "Generating moral standards for right versus wrong... the consequences of our behaviors on others."
3. **Applied ethics:** "Examining specific controversial issues. Nuclear war, animal rights, etc."

He connected applied ethics to research practice: "in any funding that we apply to... you find always... this research will be conducted in any human samples or anything related to tissues, human tissues or animal tissues or... involving animals. If yes, certainly there will be very specific procedures."

**Assessment utility (Task 1):** The meta-ethics branch is directly relevant -- cultural factors in robot acceptance ARE meta-ethical (where do our ethical attitudes to robots come from? Society, religion, cultural norms). Frame your Kaplan (2004) discussion using Dr. Aly's own meta-ethics framing.

### Topic E: Approaches to Ethics in AI (Slides 25-31)

**Two approaches:**

1. **Bottom-up approach:** Experience/Practices --> Ethical & Legal Theory and Principles. Start from what happens in practice, then derive rules.
2. **Pro-active approach:** Put regulations and frameworks in place BEFORE problems occur. Work through standards (IEEE), certification, governmental and non-governmental actors.

Dr. Aly's clear preference is the proactive approach. He used the VW emissions scandal (slide 28) as an example of what happens when you rely only on the bottom-up: "So it can lead to situation like that."

His key statement: "you don't need to let the experience happen first. So we need to put in advance some proactive expectations for what could be the problems."

He mentioned:

* IEEE standards
* Certification processes
* Non-governmental actors (showed Responsible Robotics organisation, slide 30)
* Need for multi-level approval (university, NHS)

Final slide message: "Policy needed. Everyone affected, need for vision and policy NOW."

**Assessment utility (Task 3):** Structure your Discussion section around the proactive approach -- don't just list ethical problems, propose how assistive robotics should anticipate and design against them. This is what Dr. Aly means by "deep analysis and full investigation" in the 70%+ threshold criteria.

---

## 4. LECTURER'S LEXICON

| Term                           | Dr. Aly's Definition/Usage                                                                            | Assessment Relevance                                      |
| ------------------------------ | ----------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| **Ethics**               | "branch of philosophy that deals with the moral principles and the values that guide human knowledge" | Use his framing in any ethics discussion                  |
| **Meta-ethics**          | "Studying where our ethics come from" -- human nature, society, religion, cultural norms              | Task 1: cultural factors ARE meta-ethical                 |
| **Normative ethics**     | "Generating moral standards for right versus wrong"                                                   | Task 2 Q5: POMDP reward functions encode normative ethics |
| **Applied ethics**       | "Examining specific controversial issues"                                                             | Task 3: assistive robotics ethical issues                 |
| **Explainable AI (XAI)** | "trying to have an interpretation for why the algorithms came to this decision"                       | Task 3 and Task 4: critical for healthcare robots         |
| **Fairness in AI**       | Related to bias -- "to have fairness in judgment in anything, we have to avoid bias"                  | Task 3: assistive robotics must be fair                   |
| **Bias**                 | Training data imbalance leading to discriminatory outcomes                                            | Task 4: data preparation consideration                    |
| **Proactive approach**   | Anticipating ethical problems BEFORE they occur, setting standards in advance                         | Use this framing everywhere                               |
| **Bottom-up approach**   | Deriving ethical principles from experience after the fact                                            | Contrast with proactive; Dr. Aly prefers proactive        |
| **SAE Levels (0-5)**     | Classification of self-driving autonomy from monitoring only to fully autonomous                      | Task 2: degrees of autonomy in POMDP context              |
| **Moral agent**          | Whether AI/robot can be held morally responsible for actions                                          | Task 2 Q5, Task 3 Discussion                              |

---

## 5. COURSEWORK SUCCESS BLUEPRINT

### Task-by-Task Strategy Using This Lecture

**Task 1 (Cultural Differences) -- What Dr. Aly Wants to See:**

* Use the meta-ethics framework (where do attitudes to robots come from?) to analyse cultural factors
* Reference East-West divide he explicitly raised (Japan vs. West comfort with robot autonomy)
* For Africa (Q2), he wants genuine reasoning from cultural understanding, not stereotypes -- he invited diverse perspectives in class
* For Q3 (design traits), think about autonomy levels -- he spent the most time on this. Different cultures will accept different autonomy levels
* For Q4 (Kahn et al. design patterns), link cultural ethics to specific design decisions about robot behaviour

**Task 2 (POMDP) -- Ethical Angle from This Lecture:**

* Q4 scenario: Consider using the autonomous car dilemma or an assistive care robot as your POMDP scenario. Dr. Aly clearly loves these examples
* Q5 is worth 10% of Task 2 -- use EVERYTHING from this lecture. Discuss: responsibility for POMDP decisions, transparency of POMDP policy, bias in observation/transition models, cultural variation in reward function design
* Trust modelling (Q3, 15%): Dr. Aly's nanny robot discussion shows trust depends on capability awareness, supervision, cultural background, and malfunction risk. Model these as belief state variables

**Task 3 (Assistive Robotics Essay) -- Direct Lecture Content to Include:**

* **Introduction (10%):** AI pervasiveness + urgency of ethical frameworks for assistive robotics
* **Applications (30%):** Surgery robots, care robots (medication), therapeutic robots (PARO), nanny/educational robots -- all from this lecture
* **Discussion (20%):** Structure around proactive ethics framework: privacy/data, autonomy levels, bias/fairness, explainability, responsibility, job displacement in care work. Reference Wachter et al. (2017) for explainability
* **Conclusion (10%):** Echo Dr. Aly's "Policy needed... need for vision and policy NOW" -- argue for proactive ethical design in assistive robotics
* **References (10%):** Wachter et al. (2017) from the slides; Frey & Osborne on future of employment (shown on slide 18); Responsible Robotics organisation

**Task 4 (Programming Project) -- Ethical Design Integration:**

* Whatever project you propose, include an ethics section addressing: data privacy, autonomy level justification, bias mitigation, explainability
* Dr. Aly's proactive framework: show you've anticipated ethical concerns in your design, not just noted them afterwards
* Consider approaching Dr. Aly about his own project topics -- he explicitly offered these and values ambitious students

---

## 6. HIDDEN CURRICULUM EXTRACTION

### Lecturer's Research Interests and Perspectives

* Dr. Aly works in **healthcare AI/robotics** -- he mentioned NHS approvals, clinician trust, eClinical Medicine publication. Healthcare is clearly where his research lives. Framing your work with healthcare applications will align with his interests.
* He has **personal experience with ethical debates** -- studied at the Sorbonne, led panel discussions at robotics conferences. He told the story of his younger self saying "In science or in AI there is nothing called ethics" and his professor correcting him. He later realised restrictions are real and necessary. He respects students who take ethics seriously, not cynically.
* He works with **Pepper (NAO/Pepper platform)** -- mentioned moving "Peppa" around campus and used it as an example of low-risk autonomy.
* He has **PhD students** working on bias and data preparation -- this is an active research concern for him, not just textbook material.

### Pet Topics and Enthusiasm Indicators

* **The autonomous car trolley problem** -- he spent the longest single stretch on this. He loves the ethical complexity and used it to generate the most class discussion.
* **Cultural differences in robot acceptance** -- raised organically during the nanny robot discussion. Japan vs. West is a lens he naturally applies.
* **The tension between regulation and innovation** -- his personal arc (from "ethics doesn't matter" to respecting NHS approval processes) is clearly formative.
* **Ambitious student projects leading to publication** -- the eClinical Medicine story was told with clear pride. He wants students to aim high.

### What He Values in Writing (from threshold criteria + lecture behaviour)

* **70%+ threshold:** "very well discussed in detail, supported by excellent arguments... clear and well-justified analysis... strong evidence of investigation and research (e.g., deep analysis and full investigation)... high standards and quality (focused and concise)."
* He asked LOTS of questions in the lecture and valued student participation. He wants YOUR reasoning, not regurgitation.
* He consistently used concrete examples (VW scandal, Facebook terms, facial recognition bias, eClinical Medicine) -- he values specificity over abstraction.

---

## 7. COMPLETE Q&A AND INTERACTIVE MOMENTS

### Nanny Robot Discussion (Major Interactive Segment)

**Dr. Aly's question:** "Would you let your child, for example, with a nanny robot, if you are busy?"

**Student responses (capturing diversity of opinion -- Dr. Aly valued all of these):**

1. One student: Under supervision, fine. Without supervision, no.
2. Another student: "If I'm fully aware of what the robot is capable of doing and what it can't do, for example, I know that it cannot harm the child, then I'm completely comfortable with... leaving the robot completely on its..." -- emphasised capability awareness as the trust determinant.
3. Another student: "as long as it has gone through all the safeguards and like the security to make sure nothing happens" -- plus monitoring capability.
4. Another student raised the key counter-argument: "there's always a chance that it will malfunction... it also depends on how young a child is... if it was like a robot and it's like your 14 year old teenager, that's different because they can still handle themselves. But if we're comparing it to like a one year old or a two year old, I could never like never without supervision."

**Dr. Aly's synthesis:** Added the cultural dimension (Japan vs. West) and the hacking dimension (externally compromised robot).

### Autonomous Car Discussion

**Student contribution:** "if the AI made the decision to crash the car, you'd think who would want to buy an AI or buy something that would choose to kill you over?"

**Another student:** "People are more crucial call [critical] and less forgiving when the AI makes a mistake... even if human driver would have done the same mistake." -- Dr. Aly agreed with this point.

**Student on human vs. robot decision-making:** "for human, there's a lot of feeling and emotion on the decision that we make... as a robot, I think since it's rule based, you might think that I'm on the right track and I'll follow these rules so there's no feelings involved."

**Dr. Aly's response:** Escalated the scenario -- what about 5 vs. 1? "AI also is responsible for not hurting people or reducing human loss in this way. So a lot of confusion that might happen might affect the certainty of the decision made."

### Job Displacement Discussion

**Student:** "it's not already happening. Hasn't Amazon done a bunch of like layouts [layoffs] because of AI?"

**Dr. Aly's response:** Shared the EU report finding and his own nuanced view: AI is a "job killer" but also "redefined the job market" and "created too many other jobs."

---

## 8. KEY REFERENCES MENTIONED/SHOWN

* **Wachter et al. (2017)** -- "Right to Explanation of Automated Decision Making" -- on slide 21, directly relevant to XAI discussion
* **Frey & Osborne** -- "The future of employment: How susceptible are jobs to computerisation?" -- shown on slide 18 (Technological Forecasting & Social Change journal)
* **European Economic and Social Committee opinion on AI** -- shown on slide 18, about consequences of AI on employment and society
* **Society of Automotive Engineers (SAE)** -- 6 levels of self-driving classification
* **IEEE** -- mentioned as standards body for proactive ethics in AI/robotics
* **Responsible Robotics** -- non-governmental organisation shown on slide 30, "Accountable Innovation for the Humans Behind the Robots"
* **VW emissions scandal** -- used as cautionary example of reactive (bottom-up) ethics failure

---

## 9. META-LEARNING INTELLIGENCE

### Dr. Aly's Approach to the Module

* He structures lectures around **discussion and student engagement** -- not just content delivery. He asked multiple open questions and valued all responses. Your coursework should demonstrate this kind of dialogic thinking (consider multiple perspectives, don't just state one position).
* He draws heavily on **personal anecdotes** (Sorbonne, Pepper on campus, eClinical Medicine publication, PhD student supervision). This suggests he values authentic, personal engagement with material over formal academic distance.
* He explicitly encouraged students to take on **ambitious projects** and offered his own topics for Task 4. Taking him up on this shows initiative.

### Study Advice Embedded in Lecture

* "AI after five years would be largely different from the AI of today. So we need always to adapt ourselves" -- he values students who demonstrate awareness of the field's rapid evolution.
* "don't feel afraid if you find ambitious project. So it is possible to do it" -- direct encouragement for Task 4.

---

## 10. VERBATIM QUOTE BANK (Organised by Assessment Utility)

### For Task 1 (Cultural Differences)

> "So now we have cultural issues here in Japan. They are fine to leave people more robots or probably less sensitive to risks that might appear from robots to some extent than Wisto [the West]."

### For Task 2 (POMDP -- Trust and Uncertainty)

> "a lot of confusion that might happen might affect the certainty of the decision made"

> "technology can be hacked. So what the robot is watching or saying okay can be at any moment influenced by external... ways or algorithms that can change this. So you never know."

> "Most importantly, if AI took wrong decision, I would be responsible for this... who would be responsible for the act done by AI who should be criminalized if there is an A crime?"

> "we don't have prisons for algorithms, for example. So what would be happening in this case?"

### For Task 3 (Assistive Robotics Ethics)

> "your mobile phone for example, is an AI tool that can be a spying tool, for example, without, you know"

> "Should the clinician trust what you are giving us judgment? Should the clinician try to have search for? Because if the person trusts what we are giving and if it's wrong, it's responsibility on the clinician or might be wasting resources."

> "you don't need to let the experience happen first. So we need to put in advance some proactive expectations for what could be the problems."

> "AI is like, is like something if you don't control, will get out of control."

> "don't try to give, for example, try to make some balance between data. If you give data, for example for one category... 1 million data point and the other category 100, certainly there will be some bias."

> "Is bias, for example affordable [avoidable]? This exists, but we can try to take... measures... to consider the data construction of data that we are dealing with and try to avoid it and try to analyze bias."

### For Task 4 (Project Ethics Section)

> "don't feel afraid if you find ambitious project. So it is possible to do it."

> "In science, we try to put in advance the regulations and some certifications and put some standards... not to leave everything to work without any framework."

> "the definition of what should be autonomous, what should not be autonomous. This is part of the ethics framework."

### On the Lecturer's Own Ethical Journey

> "In science or in AI there is nothing called ethics... And he told me not like. Not exactly like that. And when I grew up and I started to be for example involved in research, I understood... It's not like as I was thinking, there is actually restrictions."

---

**END OF EXTRACTION -- Cross-check with Gemini for gap identification.**
