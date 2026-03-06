# COMP3018 Lecture 7 Part 1: Models for Human-Robot Collaboration -- POMDP Intelligence Extraction

**Prompt:** BRITISH AI Lecture Intelligence System (v3.0) -- Maximum Extraction Protocol applied to Lecture 7 Part 1: Introduction to POMDP, COMP3018 Human-Robot Interaction, Dr. Amir Aly

**Lecture:** Lecture 7: Models for Human-Robot Collaboration (Part-1)
**Lecturer:** Dr. Amir Aly
**Module:** COMP3018/COMP5018: Human-Robot Interaction
**Date Extracted:** 06/03/2026
**Source Materials:** PDF slides (19 pages) + Full lecture transcript

---

## 1. CRITICAL ASSESSMENT INTELLIGENCE [HIGHEST PRIORITY]

### Direct Coursework Alignment -- Assessment 1, Task 2 (60% of Set Exercise, 30% of module)

Task 2 is titled **"Models for HRI"** and is worth **60% of Assessment 1**. It has 5 sub-questions, all about POMDP. Here is the exact mapping of this lecture's content to each sub-question:

**Task 2-1 (20%): "Discuss the efficient role that POMDP plays in modelling and solving problems related to trust, cooperation, coordination, and collaboration in human-robot teams."**

- This lecture provides the **foundational understanding** of what POMDP is and WHY it is used in HRI
- KEY QUOTE from Dr. Aly: "That's why in human robot interaction, a very common model to use is that POMDP, because we are dealing with emotions, we are dealing with intents, we are dealing with goals that we need to infer because they are unclear."
- The lecturer explicitly frames POMDP as a **collaboration model**: "We'd like to create models that can allow collaboration. But what kind of models that we can involve?"
- He frames the entire lecture around the robot-human interaction paradigm: observing reactions, adapting behaviour, learning from rewards -- this IS the cooperation/collaboration mechanism

**Task 2-2 (20%): "Analyze the role of uncertainty in human-robot collaboration and how POMDPs can be used to make decisions in uncertain environments."**

- The lecturer EXPLICITLY identifies two cases of uncertainty (slide 5):
  - **Case #1:** Uncertainty about the action outcome
  - **Case #2:** Uncertainty about the world state due to imperfect (partial) information
- KEY QUOTE: "Your emotions for me are partial information." -- this is the uncertainty the POMDP handles
- KEY QUOTE: "Partially observable. Why? Because action outcome, I'm not sure what action outcome could be or the world state due to imperfect or partial information."
- The belief state mechanism IS the POMDP's answer to uncertainty -- the entire belief update derivation shows how decisions are made under uncertainty

**Task 2-3 (15%): "Discuss the challenges of modelling trust in human-robot collaboration and how POMDPs can help address them."**

- Trust is not directly covered in depth in this lecture, but the FRAMEWORK is here: trust is an **intrinsically unobservable** internal state that must be **inferred** -- exactly what POMDP does
- KEY QUOTE: "Your presence is directly, can be understood directly or measured directly because you occupy some vacuum, some part of the vacuum. So you understand you are present, but your intents are intrinsically unobservable. So I need to infer them."
- Trust would be modelled as a **hidden state** in the POMDP, inferred through observations (facial expressions, speech, behaviour) -- you need literature to extend this

**Task 2-4 (35%): "Develop a POMDP model for a specific scenario in human-robot collaboration and explain how it takes into account trust and uncertainty."**

- THIS IS THE BIGGEST MARK CHUNK. This lecture gives you the **formal POMDP tuple** to build your model with:
  - S: set of states (e.g., trust levels: high, medium, low)
  - A: set of actions (robot's possible behaviours)
  - Pr(s'|s,a): transition model
  - R(s,a,s'): reward model
  - gamma: discount factor
  - s_0: start state
  - E: set of possible evidence (observations)
  - Pr(e|s): observation probability
- The lecturer's own example of the "chemical engineering expert" IS a walkthrough of how belief updates work in practice -- use this logic structure for your own scenario

**Task 2-5 (10%): "Discuss the ethical and social implications of using POMDPs in human-robot collaboration."**

- Not covered in this lecture. Requires independent reading. But the inference of hidden emotional states raises obvious ethical questions about privacy, consent, and emotional manipulation.

### Threshold Criteria Mapping

From the assessment brief, to achieve 70%+:

- "very well discussed in detail, supported by excellent arguments"
- "correct and complete, especially with clear and well-justified analysis and description"
- "strong evidence of investigation and research"
- "deep analysis and full investigation"
- "writings are of high standards and quality (focused and concise)"

Dr. Aly's KEY STATEMENT about assessment expectations: "Your POMDP as well question and the coursework is very simple. Depends on your general understanding. It's not like a machine learning. When you come to machine learning, we will deal more about the algorithmic side of it."

This tells you: **the coursework is NOT about algorithmic depth -- it is about UNDERSTANDING and APPLICATION.** Don't get bogged down in the maths; demonstrate you understand WHY POMDP works for HRI and can APPLY it to a scenario.

---

## 2. The Complete 'Alpha' Brief: Comprehensive Directives

- [!!!] **POMDP is the standard model for HRI collaboration problems** -- Dr. Aly frames the ENTIRE lecture around this: "a very common model to use is that POMDP, because we are dealing with emotions, we are dealing with intents, we are dealing with goals that we need to infer because they are unclear" -- USE THIS AS YOUR ANCHOR ARGUMENT IN THE COURSEWORK
- [!!!] **The coursework expects UNDERSTANDING, not algorithmic depth** -- "Your POMDP as well question and the coursework is very simple. Depends on your general understanding. It's not like a machine learning." -- Do NOT over-engineer the maths in your report; focus on conceptual clarity and application
- [!!!] **"Infer" is the keyword of this entire lecture** -- Dr. Aly says: "Get used to this word a lot. Infer. Inferred means something not directly observable, but you try to infer it through other cues, other signals like facial expressions, like speech prosody" -- Use "infer" extensively in your coursework to show you speak the lecturer's language
- [!!] **Two types of POMDP uncertainty** -- (1) action outcome uncertainty, (2) world state uncertainty due to partial information. Quote these explicitly in Task 2-2
- [!!] **Belief = posterior distribution over states** -- This is the CORE concept. Dr. Aly spent significant time on this: "the belief is a posterior distribution... Not familiar with the B yet? ...So the posterior is like I'm trying to tell you what is the probability of event A given conditional on given event B"
- [!!] **POMDP is non-Markovian in policy but Markovian in belief update** -- This is the MOST CONFUSING PART according to Dr. Aly himself: "the POMDP can be considered as Markovian model, but non Markovian policy. And this is the most confusing part, that belief is history dependent. Yes, depends on history for computation. But once you computed it, when you update it is Markovian."
- [!!] **MDP vs POMDP distinction** -- MDP: fully observable states, policy maps state to action (pi: S -> A). POMDP: partially observable, policy maps initial belief x history to action (pi: B_0 x H_t -> A_t). This is a KEY differentiator for the coursework
- [!] **Discount factor explained with career planning analogy** -- gamma close to 0 = focus on immediate reward; gamma close to 1 = focus on long-term benefit. Use this when explaining your POMDP model design choices
- [!] **Policy = approach/strategy** -- Dr. Aly defines it very practically: "The policy is the way approach that you take to do the action." The career/navigation analogies make this concrete
- [!] **Belief state MDP equivalence** -- POMDPs can be viewed as belief state MDPs: fully observable over a continuous belief space. This is conceptually powerful for the coursework: you can argue POMDP "converts" a partially observable problem into a fully observable one over beliefs

---

## 3. Exhaustive Topic Breakdown with Complete Quotation

### Topic 1: WHY POMDP for Human-Robot Interaction (Motivating Framework)

**Lecturer's Framing (Full Narrative):**

Dr. Aly opens by setting the scene of robot-human collaboration. He acts it out physically in the lecture:

"We have a robot interacting with a human, right? ...I'm a human now, let's say... I'm coming to you. I'm from different background, different culture... I don't speak English or something like this... And then I'm coming to interact with you. I might say something. And then I observe that some of you got, for example, happy or unhappy. Then I observe. I observe in you. And then your reaction for me is a motivation or a signal for me to adapt as a behavior."

"If I see something that made you happy, I can next time stress on it to make you more happy. Or if I found something that made you sad, I can try to understand it, to change it."

He then explicitly connects this to RL: "So this is similar to reinforcement learning. We are observing there is a reward. This reward is your reaction, happy, not happy. That makes me adapt to the behavior."

**Assessment Application:** This narrative IS your introduction paragraph for Task 2-1. The robot observes human reactions (observations), interprets them (belief update), and adapts behaviour (policy) to maximise positive interaction (reward). This is collaboration modelled through POMDP.

### Topic 2: MDP Recall -- The Foundation

**Lecturer's Definition:**
"Problems involving an agent interacting with an environment which provides numeric reward signal."

**Cookie Analogy (Full Quote):**
"If I made you happy, I got a positive one cookie. They give me the cookie. So I know that, okay, this is the behavior. If I make it again, I will be the cookie. If you become sad, I will take the negative, the non cookie. So I will understand that I should, if there is a problem, I should avoid so that I can get the cookie."

**Policy Definition (Full Quote with Navigation Example):**
"In machine learning, the policy is the way approach that you take to do the action. So if I'm saying your policy, I'm trying to learn that policy to go from Smeaton from my place to outside. The shortest way, best policy or best approach is to go one step forward and turn around and then walk, walk, walk, walk until I go to the door. This is one policy. Another policy is I go 100 times ago and come from this screen to this screen... Best policy is the shortest one that takes you to the objective in less number of steps."

**Reward Mechanism (Full Quote):**
"So each step you do makes you lose a reward, so it becomes minus one. So the less number of steps, the less number of rewards you have. So if I went from here to there, for example, in 10 steps, okay, I become minus 10, my reward. However, if I went there 100 times and then went out, my reward would be minus 100. So minus 10 is larger than minus 100."

**Smeaton Tower Extended Analogy:** "One guy can go to Smeaton directly. Another guy can go to Exeter and then to Smeaton Tower... Another guy can go to Japan and then go to London again, and then go to Plymouth and then go to Smeaton directly. So different approaches, different strategies. Each strategy has its own route."

**MDP Formal Tuple (from slides):**
Defined by (S, A, R, P, gamma) where:

- S: set of possible states
- A: set of possible actions
- R: distribution of reward given (state, action) pair
- P: transition probability -- distribution over next state given (state, action) pair
- gamma: discount factor, where 0 <= gamma < 1 (for scaling rewards)

**Markov Property (Lecturer's Emphasis):**

Dr. Aly asks the class directly: "Why Markov's called Markov? ...That was a very important slide, guys, because of the Markov property."

Definition: "A state ST is Markov if and only if the next state depends only on the present state, it doesn't need the history. Which means the present state captures all relevant information from the history."

Formally: P[S_{t+1} | S_t] = P[S_{t+1} | S_1, ..., S_t]

"So you don't need to make something like this. Just say S_t. S_t encodes all the information about the past."

**Graphical explanation:** "S2 depends on S1 only. But I don't need to say S1 and S0. You don't find a connection between S0 and S2, only connection from state to state."

### Topic 3: Discount Factor (gamma) -- Extended Explanation

**The Career Planning Analogy (Full Quote):**

"Let's say you're thinking about your next step, next future step. So you might say, ah, I will try to make a plan for my 5 years career... If I do masters, I might get specialized. My salary can jump by a few hundreds of pounds. And then if I do go, I have two routes. If I work in academia, I can have this benefit. If I work in industry, I can have that benefit..."

"So this is a discount factor. The discount factor, if it's equal to zero, it's a factor from zero and one. It's telling the robot focus on the immediate reward or the near reward, the reward that happening in the next months or next days or one year or something. However, when you say reward equal to one, it means like look at the rewards that are coming on the long term."

**Summary:** gamma = 0 means myopic/short-term focus. gamma close to 1 means long-term planning. This is a design parameter YOU choose when building the model.

### Topic 4: MDP vs POMDP -- The Core Distinction

**Lecturer's Definition of the Difference:**

"A partially observable Markov decision process is really just an MDP... they are similar in everything. The only difference is in whether or not we can observe the current state of the process."

**The Observable vs Unobservable Distinction (KEY QUOTE -- use in coursework):**

"Fully observable, it means like you are for me, fully observable as humans... I understand that you are sitting on the chairs and you are doing whichever action you are doing. This is understandable to me as MDP. Fully observable."

"Partially observable is what? Your emotions, your intents, your goals. So I'm not speaking about your presence, I'm speaking about something that I need. Your presence is directly, can be understood directly or measured directly because you occupy some vacuum, some part of the vacuum. So you understand you are present, but your intents are intrinsically unobservable. So I need to infer them, infer them through your, for example, facial expressions, your speech prosody, so on and so forth."

**The HRI Connection (KEY QUOTE):**
"That's why in human robot interaction, a very common model to use is that POMDP, because we are dealing with emotions, we are dealing with intents, we are dealing with goals that we need to infer because they are unclear. The same way that you are able to understand each other, you are able X person can understand that Y person is tired, one person is ill or whatever by inferring this."

### Topic 5: POMDP Uncertainty -- Two Cases

**Slide 5 (boxed, emphasised):**

**POMDP: UNCERTAINTY**

- Case #1: Uncertainty about the action outcome
- Case #2: Uncertainty about the world state due to imperfect (partial) information

**Lecturer's Explanation:**
"So might say ah, like uncertainty here. If I do this action, this person might react this way or that way. You don't know. So action, you don't know what action can make, what reaction or lead to what reaction. You don't know."

"Your emotions for me are partial information."

### Topic 6: POMDP Graphical Model -- The "Umbrella" of Connections

**Key Structural Difference from MDP:**

In MDP graphical model: states -> states, actions -> states, states -> rewards. No observations node.

In POMDP graphical model: adds **observation nodes (o_1, o_2, ...)** and crucially, there are connections from ALL previous actions and observations to future actions (the "umbrella" of arcs at the top of the graph).

**Lecturer's Explanation:**
"The difference is in the umbrella that we have here. Umbrella of connections between an action to an action... From action A0 to A1 and from A1 to A2 and from observation, each observation, to the action after."

"So we have here no observation [in MDP] because it's intrinsically observable. It's totally observable... But because here [POMDP] it is intrinsically unobservable, the observation counts because the observation is like I'm trying to infer your emotions."

**History Dependency:**
"The decision making process at any time point in POMDP takes into account the entire history."

Then Dr. Aly asks the critical question: "Is it Markov or not Markov? ...Not Markov property. Because it depends on history."

### Topic 7: POMDP Formal Tuple

**Extended from MDP, the POMDP is defined by:**

- S: set of states
- A: set of actions
- Pr(s'|s,a): transition model
- R(s,a,s'): reward model
- gamma: discount factor
- s_0: start state
- **E: set of possible evidence (observations)** -- NEW
- **Pr(e|s): observation probability** -- NEW

**Lecturer's Connection to Bayes:**
"In Bayes theorem, remember here I was saying this is the evidence, the denominator. To translate it to the language of our model, we say E set of possible evidence observations. So observations is the denominator of the Bayes theorem."

### Topic 8: Belief -- The Central Concept

**Lecturer's Definition:**
"The belief is a posterior distribution... Belief is like the amount of information you have about something. So when you say, for example, like my belief about the current situation is this -- this is according to what you think about the current situation."

**Formal Definition:**

- Belief b_t(s) = Pr(s_t) -- Distribution over states at time t
- In POMDP: b_t(s) = Pr(s_t | h_t, b_0) -- Belief about underlying state based on history h_t and initial belief b_0

**Bayes' Theorem Connection (The Tube Analogy -- Full Quote):**

"Let's say I have a tube and you are looking from here, from this side and here B. So if you are looking from this side... I have put different kind of balls. Basketball, football, volleyball and handball. So I can tell you if you are looking from the A side, from external, what is the probability, the posterior probability that the output from this tube is a basketball?"

"Now if you look at the likelihood, you look from the other side. So you start translating it by saying given, given I put in the tube, for example, group of basketballs, what is the likelihood... what is the probability that the output you will have a basketball?"

### Topic 9: POMDP Policies -- Non-Markovian vs Markovian

**MDP Policy:** pi: S -> A (Markovian -- action determined solely by current state)

**POMDP Policy:** pi: B_0 x H_t -> A_t (Non-Markovian -- depends on initial belief AND history)

Where:

- B_0 is the space of initial beliefs b_0 = Pr(s_0)
- H_t is the space of histories h_t = <a_0, o_1, a_1, o_2, ..., a_{t-1}, o_t>

**Lecturer's Explanation:**
"In order to represent it, I need to replace the state by other thing. What is this other thing? Simply the history and the initial belief. So in POMDP policies we replace the state by initial belief B... and the history and this what maps to the action."

**Policy Trees:**
A policy tree is a decision-making approach representing the sequential decision-making process under uncertainty. Composed of nodes -- actions branch into observations, which branch into further actions.

"Like I move from one action, I can have observation O1 or O2 and O1 can take me to the same action or action one or action two. And then through different observations you can make a journey over actions."

Multiple trees map to different belief regions: B = B_1 U B_2 U B_3, where each initial belief region selects a different policy tree.

### Topic 10: Belief Update -- THE EQUATION (Taught for Coursework Application)

**The Belief Update Rule:**

Starting point: b_{t+1}(s_{t+1}) = Pr(s_{t+1} | h_{t+1}, b_0)

Step-by-step derivation (as Dr. Aly walked through):

1. **Replace history:** h_{t+1} = o_{t+1}, a_t, h_t (history at t+1 is old history + action + observation)
2. **Substitute:** b_{t+1}(s_{t+1}) = Pr(s_{t+1} | o_{t+1}, a_t, h_t, b_0)
3. **Recognise equivalence:** b_t = b_0, h_t (current belief encodes initial belief and history)
   So: = Pr(s_{t+1} | o_{t+1}, a_t, b_t)
4. **Apply Bayes' theorem:** = Pr(s_{t+1}, o_{t+1} | a_t, b_t) / Pr(o_{t+1} | a_t, b_t)
5. **Apply chain rule:** = Pr(o_{t+1} | s_{t+1}, a_t) * Pr(s_{t+1} | a_t, b_t) / Pr(o_{t+1} | a_t, b_t)
6. **Apply belief definition (marginalise over s_t):**

**FINAL BELIEF UPDATE EQUATION:**

b_{t+1}(s_{t+1}) is proportional to Pr(o_{t+1} | s_{t+1}, a_t) * SUM over s_t [ Pr(s_{t+1} | s_t, a_t) * b_t(s_t) ]

**What each term means (for your coursework model):**

| Term                       | Meaning                         | In HRI Context                                                                                            |
| -------------------------- | ------------------------------- | --------------------------------------------------------------------------------------------------------- |
| b_{t+1}(s_{t+1})           | Updated belief about next state | Robot's updated belief about human's trust/emotion                                                        |
| Pr(o_{t+1}\| s_{t+1}, a_t) | Observation probability         | Probability of seeing a facial expression given the human's actual emotional state and the robot's action |
| Pr(s_{t+1}\| s_t, a_t)     | Transition probability          | Probability human moves from one trust level to another given robot's action                              |
| b_t(s_t)                   | Current belief                  | Robot's current estimate of human's trust/emotion distribution                                            |
| SUM over s_t               | Marginalisation                 | Consider ALL possible current states the human could be in                                                |

**The Chemical Engineer Analogy (Full Walkthrough):**

Dr. Aly gives an extended narrative example of belief updating:

"I came here to interact with somebody in chemical engineering and I had my belief about him 8 over 10 that he's expert. Then I observed how he was working with chemical compound... I had my observation about him and then when I entered I was at T high. Then I found him making some kind of mess at time t+1. And he made for example in some kind of sophisticated experiment he made very nice step or not nice steps that can give me idea about his performance."

"So I updated my belief at T+1 that is consequent to my previous belief. So instead of giving him 8 over 10, I give him 6 over 10, 5 over 10."

**This is EXACTLY how you should explain your POMDP model in Task 2-4: start with an initial belief, show how an observation triggers a belief update, and explain how the new belief influences the next action.**

### Topic 11: The Markovian Resolution -- CRITICAL CONCEPTUAL POINT

**The "Most Confusing Part" (Dr. Aly's own words):**

"The POMDP can be considered as Markovian model, but non Markovian policy. And this is the most confusing part, that belief is history dependent. Yes, depends on history for computation. But once you computed it, when you update it is Markovian."

**Breakdown:**

- Initial belief definition: b_t(s) = Pr(s_t | h_t, b_0) -- NEEDS HISTORY -> Non-Markovian
- Belief UPDATE: b_{t+1} depends only on b_t, a_t, o_{t+1} -- NO HISTORY -> Markovian

"So you need history to just make calculation of the belief at the very beginning part. But after that when you update your belief, you will not need any information at the beginning."

**Dr. Aly's verification from the equations:** "Here you used history. Here you used history right here. Did you use history as a final explanation? There's no history. So this means what? When it updates the POMDP initially it has history. Just for the initial definition. But with a belief updates it doesn't have history."

**Consequence:** POMDP can be viewed as a **Belief State MDP** -- fully observable over continuous belief space.

"If we try to formulate the difference between MDP and POMDP, we can consider it as continuous space, belief MDP. So at the beginning it's not Markovian. But when we update the belief, we don't depend on H anymore in history, we depend only on the state value itself."

### Topic 12: Policy Evaluation (Brief Introduction -- Continued Next Lecture)

**Value of a POMDP policy pi:**
V^pi(b) = E[ SUM_t gamma^t * R(b_t, pi(b_t)) ]

This is the expected sum of discounted rewards following policy pi starting from belief b.

**Bellman Equation for POMDP:**
V^pi(b) = R(b, pi(b)) + gamma * SUM_{o'} Pr(o'|b,a) * V^pi(b^{a,o'}) for all b

**Lecturer's Navigation Analogy for Policy Evaluation:**
"The policy that takes me to the door. I will calculate each step I do, I take minus one, so from here to here minus 10. And then if I consider I go this way and that way I will have minus 100... So sum of rewards -- always it's about rewards."

**Career Analogy for Policy Evaluation:**
"Your policy is to make masters... and from the master become regional manager or make academia... you have different policies. And each policy you have rewards you can calculate. And then you can choose which policy should I take."

---

## 4. Complete Lecturer's Lexicon

| Term                              | Dr. Aly's Definition/Usage                                                                                                                                    | Context                                                       |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| **Infer**                   | "Something not directly observable, but you try to infer it through other cues, other signals like facial expressions, like speech prosody"                   | The CORE verb of POMDP -- used repeatedly                     |
| **Belief**                  | "A posterior distribution over states"; "the amount of information you have about something"                                                                  | Central to POMDP; replaces direct state observation           |
| **Policy**                  | "The way approach that you take to do the action"                                                                                                             | Strategy for choosing actions; evaluated by total reward      |
| **Sample**                  | "When I say sample, it means like you put your hand inside something and take a sample... like I'm taking an image just to understand how the environment is" | Taking an observation from the environment                    |
| **State**                   | "State of the world"; physical position in MDP, emotional/internal state in POMDP                                                                             | What the agent knows/infers about the environment             |
| **Observation**             | Sensor data (camera, facial expression reading) that provides partial information about hidden state                                                          | New in POMDP vs MDP                                           |
| **Discount factor (gamma)** | "A factor between 0 and 1... should I focus on the direct benefit or should I focus on the long term benefit?"                                                | Design parameter; 0 = myopic, close to 1 = long-term          |
| **Markov property**         | "The future is independent of the past given the present"; "the present state captures all relevant information from the history"                             | MDP has it; POMDP policy does NOT (but belief update does)    |
| **Belief state MDP**        | POMDP recast as fully observable MDP over continuous belief space                                                                                             | The resolution of the Markov/non-Markov tension               |
| **Policy tree**             | "A decision-making approach representing the sequential decision-making process under uncertainty"                                                            | Graphical representation of POMDP policy                      |
| **History**                 | h_t = <a_0, o_1, a_1, o_2, ..., a_{t-1}, o_t> -- sequence of all past actions and observations                                                                | Needed for initial belief computation; NOT needed for updates |

---

## 5. Coursework Success Blueprint [ESSENTIAL SECTION]

### How to Build Your Task 2-4 POMDP Model (35% of Task 2)

This is worth the MOST marks. Dr. Aly's lecture gives you the complete toolkit. Here is how to apply it:

**Step 1: Define your POMDP tuple for your chosen scenario**

Use the formal elements from slide 9:

- **S** = {your hidden states, e.g., trust levels: high_trust, medium_trust, low_trust}
- **A** = {robot actions, e.g., explain_action, ask_permission, act_autonomously}
- **Pr(s'|s,a)** = transition probabilities (how trust changes given current trust and robot action)
- **R(s,a,s')** = rewards (positive for maintaining/increasing trust, negative for losing trust)
- **gamma** = discount factor (justify your choice using Dr. Aly's career analogy)
- **s_0** = initial state distribution
- **E** = {observations, e.g., positive_feedback, negative_feedback, neutral}
- **Pr(e|s)** = observation model (probability of seeing positive feedback when trust is high, etc.)

**Step 2: Walk through a belief update example**

Use the final equation:
b_{t+1}(s_{t+1}) proportional to Pr(o_{t+1}|s_{t+1}, a_t) * SUM_{s_t} Pr(s_{t+1}|s_t, a_t) * b_t(s_t)

Give concrete numbers. E.g.:

- Initial belief: b_0 = [0.3, 0.5, 0.2] over [high, medium, low] trust
- Robot takes action "explain_action"
- Observes "positive_feedback"
- Compute updated belief b_1

**Step 3: Explain policy evaluation**

Show that the robot can evaluate different strategies (policies) by computing expected cumulative reward, choosing the policy that maximises long-term collaboration quality.

**Step 4: Discuss benefits and limitations**

Benefits: handles uncertainty in human states, principled Bayesian reasoning, can model trust dynamics
Limitations: computational complexity (continuous belief space), need accurate transition/observation models, curse of dimensionality

### Lecturer's Preferred Approach

Dr. Aly values:

- **Practical understanding over algorithmic rigour** -- "Your POMDP question in the coursework is very simple. Depends on your general understanding."
- **Real-world grounding** -- Every concept was explained with a human-interaction analogy
- **Correct use of terminology** -- "infer", "belief", "posterior distribution", "observation"
- **Clear distinction between MDP and POMDP** -- He spent significant time ensuring students understood this

### First-Class Indicators

To hit 72%+, your Task 2 should:

1. Use the POMDP formal tuple correctly and completely
2. Demonstrate understanding of WHY POMDP suits HRI (emotions/intents are hidden states)
3. Include a concrete worked belief update example with actual numbers
4. Reference the Markovian/non-Markovian distinction (shows deep understanding)
5. Use peer-reviewed literature to support claims about trust modelling
6. Be "focused and concise" (assessment brief language for 70%+)

---

## 6. Hidden Curriculum Extraction

### Lecturer's Research Interests

- Dr. Aly is clearly invested in **affective computing / emotion recognition** in HRI -- his examples consistently return to inferring emotions from facial expressions and speech prosody
- He values the **Bayesian/probabilistic** framing of HRI problems

### Pet Topics

- The concept of **inference** -- he returns to it repeatedly and explicitly tells students to "get used to this word"
- The MDP/POMDP distinction -- significant lecture time devoted to ensuring clarity
- Practical, human-relatable analogies (cookies, career planning, chemical engineer, navigating to Smeaton Tower)

### Philosophical Position

- Dr. Aly sees HRI as fundamentally a **partially observable problem** -- humans cannot be fully observed, and the interesting aspects (emotions, trust, intent) are always hidden
- He positions POMDP not as pure ML but as a **modelling framework** for understanding collaboration

### What He Values in Student Work

- Understanding over memorisation
- Ability to translate formal concepts into practical scenarios
- Correct terminology usage

---

## 7. Q&A and Interactive Moments

**Student answer about discount factor:** A student offers: "Isn't it where like the further the state is, the less the reward matters?" -- Dr. Aly responds positively and expands with the career planning analogy.

**Student confirms Markov property understanding:** When Dr. Aly asks "Is it Markov or not Markov?" students correctly answer "Not Markov property" -- he confirms: "Not Markov property. Because it depends on history. Okay, let's put this on the shelf a little."

**Student unfamiliarity with Bayes:** Dr. Aly asks "Not familiar with the B yet?" and gets confirmation students haven't covered it -- he then provides the full tube analogy explanation. This suggests **he expects you to understand Bayes' theorem for the coursework but knows you may not have formal training in it.**

---

## 8. Equations Taught for Coursework Application

### The Complete Equation Chain (How to Use Each One)

**Equation 1: Markov Property**
P[S_{t+1} | S_t] = P[S_{t+1} | S_1, ..., S_t]

*Coursework use:* Explain why standard MDP won't work for trust modelling -- trust isn't directly observable, so the Markov property over states doesn't hold for the observed data.

**Equation 2: MDP Tuple**
MDP = (S, A, R, P, gamma)

*Coursework use:* Present this as the baseline, then show how POMDP extends it.

**Equation 3: POMDP Tuple**
POMDP = (S, A, Pr(s'|s,a), R(s,a,s'), gamma, s_0, E, Pr(e|s))

*Coursework use:* This IS your model definition for Task 2-4. Define each element concretely for your scenario.

**Equation 4: MDP Policy**
pi: S -> A (Markovian)

*Coursework use:* Contrast with POMDP policy to explain why simple state-to-action mapping fails when states are hidden.

**Equation 5: POMDP Policy**
pi: B_0 x H_t -> A_t (Non-Markovian)

Where h_t = <a_0, o_1, a_1, o_2, ..., a_{t-1}, o_t>

*Coursework use:* Show that the robot must maintain a history of all interactions to decide what to do next.

**Equation 6: Belief Definition**
b_t(s) = Pr(s_t | h_t, b_0)

*Coursework use:* Define what the robot "believes" about the human's state at any time.

**Equation 7: Belief Update (THE KEY EQUATION)**

b_{t+1}(s_{t+1}) = [ Pr(o_{t+1} | s_{t+1}, a_t) * SUM_{s_t} Pr(s_{t+1} | s_t, a_t) * b_t(s_t) ] / Pr(o_{t+1} | a_t, b_t)

Or proportionally:

b_{t+1}(s_{t+1}) proportional to Pr(o_{t+1} | s_{t+1}, a_t) * SUM_{s_t} Pr(s_{t+1} | s_t, a_t) * b_t(s_t)

*Coursework use:* This is how the robot updates its understanding of the human's trust after each interaction. Walk through a numerical example.

**Breaking it down for your scenario (e.g., trust modelling):**

Suppose S = {high_trust, low_trust}, A = {explain, command}, E = {comply, resist}

To compute b_1(high_trust) after robot takes action "command" and observes "resist":

b_1(high_trust) proportional to Pr(resist | high_trust, command) * [ Pr(high_trust | high_trust, command) * b_0(high_trust) + Pr(high_trust | low_trust, command) * b_0(low_trust) ]

You'd fill in:

- Pr(resist | high_trust, command) = maybe 0.2 (high-trust human less likely to resist even commands)
- Pr(high_trust | high_trust, command) = maybe 0.6 (commanding slightly erodes trust)
- Pr(high_trust | low_trust, command) = maybe 0.1 (commanding rarely builds trust when it's low)
- b_0(high_trust) = 0.5, b_0(low_trust) = 0.5

Then: b_1(high_trust) proportional to 0.2 * [0.6 * 0.5 + 0.1 * 0.5] = 0.2 * 0.35 = 0.07

Similarly compute b_1(low_trust), then normalise so they sum to 1. This shows the robot's belief shifts toward low_trust after observing resistance to a command.

**Equation 8: Belief State MDP Transitions**
Pr(b_{t+1} | b_t, a_t) = Pr(o_{t+1} | b_t, a_t) if b_t, a_t, o_{t+1} -> b_{t+1}, else 0

*Coursework use:* Argue that POMDP can be recast as a fully observable MDP over beliefs.

**Equation 9: Belief State MDP Rewards**
R(b, a) = SUM_s b(s) * R(s, a)

*Coursework use:* Expected reward is weighted by belief -- the robot considers all possible human states weighted by how likely each is.

**Equation 10: Value Function**
V^pi(b) = E[ SUM_t gamma^t * R(b_t, pi(b_t)) ]

*Coursework use:* This is how you evaluate whether one robot strategy is better than another.

**Equation 11: Bellman Equation for POMDP**
V^pi(b) = R(b, pi(b)) + gamma * SUM_{o'} Pr(o'|b,a) * V^pi(b^{a,o'})

*Coursework use:* Show the recursive structure of optimal decision-making -- current reward plus discounted future value across all possible observations.

---

## 9. Meta-Learning Intelligence

### Study Advice (Implicit)

- Dr. Aly expects you to understand MDP before POMDP -- he labels the MDP slides as "RECALL"
- He acknowledges undergrads know RL from COMP3003 but notes "postgraduates are not familiar yet"
- He explicitly tells you the coursework "depends on your general understanding" not algorithmic depth

### What Comes Next

- "Next week we will continue discussing the POMDP" -- expect more on policy evaluation, possibly solving methods
- "We will go quickly through this part next time" -- referring to policy evaluation (Bellman equations)

### Key Differentiation from COMP3003

- "We are not dealing with algorithmic machine learning" in this module
- "When you come to machine learning, we will deal more about the algorithmic side of it"
- The POMDP here is a MODELLING FRAMEWORK for HRI, not an algorithm to implement

---

## 10. Warnings and Pitfalls

- **Do NOT treat the coursework as a machine learning implementation task** -- Dr. Aly explicitly says it's about understanding, not algorithms
- **Do NOT confuse MDP observability with POMDP** -- The entire lecture hammers this distinction
- **Do NOT say POMDP is non-Markovian without qualification** -- It is non-Markovian in POLICY but Markovian in BELIEF UPDATE. This nuance matters.
- **Do NOT neglect Bayes' theorem** -- The belief update IS Bayes' theorem applied. If you can't explain Bayes, you can't explain POMDP.
- **Do NOT forget that this is Part 1** -- Policy evaluation and solving methods continue next lecture. Your coursework will need content from BOTH parts.

---

*Check critiques with Gemini.*
