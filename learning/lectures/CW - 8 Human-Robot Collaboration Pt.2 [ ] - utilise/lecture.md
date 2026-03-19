# COMP3018 Lecture 8: Models for Human-Robot Collaboration (Part 2) – POMDP

## BRITISH AI Lecture Intelligence Extraction

**Lecturer:** Dr. Amir Aly | **Module:** COMP3018 Human-Robot Interaction | **Date:** Semester 2, 2025-2026

-----

## 1. CRITICAL ASSESSMENT INTELLIGENCE [HIGHEST PRIORITY]

### Direct Coursework Alignment – Assessment 1, Task 2 (60% of CW1, i.e. 18% of module)

This lecture is the **primary source material** for Assessment 1, Task 2 which asks you to discuss POMDP in the context of human-robot collaboration. The task has five sub-questions weighted as follows:

|Sub-question                                                                   |Weight|Core Lecture Content                                                               |
|-------------------------------------------------------------------------------|------|-----------------------------------------------------------------------------------|
|2-1: POMDP role in trust, cooperation, coordination, collaboration in HRI teams|20%   |Trust-POMDP model (Slide 22), POMDP in HRI (Slide 21), latent variable modelling   |
|2-2: Role of uncertainty in HRI and how POMDPs handle it                       |20%   |Belief states, partial observability vs MDP, tiger example, continuous belief space|
|2-3: Challenges of modelling trust and how POMDPs address them                 |15%   |Trust as latent variable, theta_t in Trust-POMDP, reward shaping around trust      |
|2-4: Develop a POMDP model for a specific HRI scenario (trust + uncertainty)   |35%   |Tiger example as template, Trust-POMDP structure, observation/action/reward design |
|2-5: Ethical and social implications of POMDPs in HRI                          |10%   |Social norms example, reward for appropriate emotional responses                   |

**Key insight:** Sub-question 2-4 is worth 35% – the largest single chunk. The lecturer’s tiger example and Trust-POMDP are your **templates** for designing your own scenario. You must show you can independently formulate a POMDP with states, actions, observations, transitions, rewards, and belief updates.

### Assessment 2 Relevance (70% Report, due 5th May)

Task 3 (Literature Review on assistive robotics): POMDP is a strong framework to reference when discussing how assistive robots handle uncertainty in real-world environments. Task 4 (Programming Project): A POMDP-based HRI system could be a strong project concept – the lecturer explicitly values this framework.

-----

## 2. THE COMPLETE ‘ALPHA’ BRIEF: Comprehensive Directives

### Triple-Star Priority (Mark Magnets)

- **Why POMDP and not MDP in HRI:** “Because MDP requires that all the states are known. Like in human robot interaction context, like speech, for example, emotions. Speech like intent, you know, emotion expressed through facial expressions and so on and so forth. That’s why we try to add this POMDP.” – This is the **foundational argument** for your entire Task 2 answer. The lecturer repeated this MDP vs POMDP distinction multiple times. Use this reasoning verbatim in 2-1 and 2-2.
- **Policy = Strategy:** “Don’t read the word, the policy worries you. Policy is how can I, how should I take the action?” and “So when we try to speak about policy, it means like I have to economize something.” – He deliberately demystified this term. Shows he values students who explain policy in plain, intuitive language rather than hiding behind jargon.
- **Belief = amount of information you have:** “Also, don’t let the world, you know, feel what this means. Belief. Belief is the amount of information you have at state whichever.” – He repeated this definition multiple times with emphasis. Critical for 2-2.
- **Trust-POMDP as the pinnacle application:** The lecturer spent significant time on the Trust-POMDP from Chen et al. (2020). He explicitly framed it as: “We need a computational model that integrates trust (latent variable) into robot decision-making.” This is the **direct answer** to sub-questions 2-1 and 2-3.
- **Latent variables are extensible:** “And if you need to use it, for example, you can sophisticate it more. And instead of the trust, for example, you can use for example latent variable. You can add another latent variable called intent. And you can add the trust and intent.” – This tells you the lecturer values seeing students who go beyond trust alone and propose multi-variable POMDP models. **Massive signal for 2-4.**
- **Social norms and reward shaping:** “So somebody, for example, somebody is sad and say I am happy that you are sad. This is out of social norms. So the reward is that you will feel what are you saying? […] This is a negative cookie. So the reward is minimized because the action was not suitable.” – This example is gold for 2-5 (ethical implications) and 2-4 (designing reward functions).

### Double-Star Priority

- **Continuous belief space problem:** “The problem is that the belief is continuous. So we don’t have values that I can iterate for state by state, it is continuous.” and “You cannot do it in this way because it is continuous.” – Understanding WHY table-based methods fail in POMDP is essential for 2-2.
- **Piecewise linear approximation:** “A policy made up of a set of trees is piecewise linear. […] Each of these segments represent a segment, piecewise linear segments.” – The lecturer’s explanation of how the continuous value function is approximated through linear segments/alpha vectors. Shows sophistication if you reference this in your model design (2-4).
- **Alpha vectors and optimal value function:** V*(b) = max_i (sum_s b(s) . alpha_i(s)). The lecturer walked through the worked example: action a1 values [0, 1], action a2 values [1.5, 0], belief [0.75, 0.25]. V(a1) = 0.25, V(a2) = 1.125, therefore a2 is optimal. Understanding this calculation demonstrates technical depth.
- **Belief update mechanism:** “I came by update my belief that you are 0.5 sad, 0.5 happy. Then I started to update my belief how? By looking at faces and by analysing your speech.” – The intuitive explanation of Bayesian belief updating, mapped directly to HRI sensor inputs.
- **Key reference:** Chen, M., Nikolaidis, S., Soh, H., et al., “Trust-Aware Decision Making for Human-Robot Collaboration: Model Learning and Planning”, ACM Trans. Hum.-Robot Interact., 9(2), 2020. – **Cite this in your coursework.** The lecturer explicitly presented this as a research exemplar.

### Single-Star Priority

- **Value iteration vs policy iteration in POMDP:** Both exist as solving techniques, but the continuous belief space makes them harder than in MDP. The lecturer noted this is “adapted from the very basic Bellman equation.”
- **Any observation without listening is uninformative:** In the tiger example, opening a door without listening provides no information. This is analogous to acting in HRI without first sensing the human’s state.
- **Cost of listening (information gathering has a penalty):** “Cost of listening action minus one. So my reward reduces by one. So I need the policy that reduces the number of listening as much as possible.” – In HRI, this maps to the cost of prolonged sensing/processing before acting.
- **Different graphical representations are equivalent:** “Don’t say ah, this is different than the model that I have seen in the lecture. You can just have different graphical representation.” – He values students who understand the underlying structure regardless of how it’s drawn.

-----

## 3. EXHAUSTIVE TOPIC BREAKDOWN

### Topic 1: MDP vs POMDP – The Fundamental Distinction

**Lecturer’s definition:** POMDP is needed when states are not fully observable. In HRI, internal human states (emotions, intent, trust) are hidden and must be inferred.

**Key quote:** “Because MDP requires that all the states are known. Like in human robot interaction context, like speech, for example, emotions.”

**Why this matters for coursework:** This is the opening argument for sub-question 2-2. The lecturer frames partial observability as the defining challenge of HRI – you cannot directly observe what a human is thinking or feeling, so you must infer it through observations (facial expressions, speech, gestures).

**Lecturer’s analogy (repeated 3x):** Entering a room and not knowing if people are happy or sad. Initial belief is 0.5/0.5, then updated by observing faces and analysing speech. This maps directly to a robot encountering a human for the first time.

**Continuous space distinction:** In MDP, you move from discrete state to discrete state (like chess). In POMDP, the belief space is continuous. “It’s not like in the MDP I have state and I’m going from… moving from state one to state two in a discrete way. No, we have continuous.”

### Topic 2: Belief State and Belief Space

**Lecturer’s definition of Belief State:** “Belief is the amount of information you have at state whichever. So if I’m at this state, what is the information I have? This is belief.” He emphasised: “It’s the amount of information you have.”

**Formal definition (slide):** Belief State = probability distribution over states. Belief Space = the entire probability space.

**Lecturer’s example:** If you have three states S1, S2, S3, and probabilities [0.5, 0.25, 0.25], that vector IS your belief state. The belief space is all possible permutations/combinations of probability distributions across those states.

**Why table-based methods fail:** “You cannot do it in this way because it is continuous. So we have to deal with this kind of curve.” The value function V(b) is a continuous curve over the belief space, not a lookup table.

**Slide content:** The solution is to approximate – discretise the POMDP belief space and solve the resulting belief-space MDP using value iteration, policy iteration, or any MDP solving technique. This reduces computational complexity.

### Topic 3: Policy Trees and Piecewise Linear Value Functions

**Core concept:** The continuous value function curve can be decomposed into linear segments. Each segment corresponds to a policy tree. Each tree represents a decision-making strategy over multiple time steps under uncertainty.

**Lecturer’s explanation:** “Imagine that this curve, continuous curve is composed of segments. One segment, one segment, one segment. […] Each of these linear curves here represent a segment, piecewise linear segments. And they are representing policy.”

**Alpha vectors:** Each alpha vector corresponds to a linear segment in the value function, representing the value of being in a certain belief state and taking a specific action. The optimal value function V*(b) for finite horizon is piecewise linear and convex in b.

**Optimal value function formula:** V*(b) = max_i (sum_s b(s) . alpha_i(s)), where b(s) is the probability of state s in belief state b, and alpha_i(s) is the value associated with state s in the i-th alpha vector.

**The “max” operation:** “I might have this route, but I might have another route, and I have another route. […] I take max because this is what will give me the maximum value.” – Selecting the best policy among all candidates.

### Topic 4: Point-Based Methods – Worked Example

**Setup:** Action a1 has value [0, 1] across states [s1, s2]. Action a2 has value [1.5, 0]. Belief state is [0.75, 0.25].

**Calculation:**

- V(a1) = 0.75 x 0 + 0.25 x 1 = 0.25
- V(a2) = 0.75 x 1.5 + 0.25 x 0 = 1.125

**Conclusion:** “Taking action a2 is expected to yield a higher cumulative reward in that belief state compared to taking action a1.”

**Lecturer’s real-world mapping:** He compared this to choosing between doing a master’s degree (0.75 belief) vs working with a bachelor’s (0.25 belief), and evaluating accumulated rewards over each route.

### Topic 5: Bellman Equation for POMDP (Value Iteration)

**Formula (from slide):** V*(b) = max_a R(b,a) + gamma * sum_o’ Pr(o’|b,a) V*(b^{a,o’})

**Components:**

- R(b, a): Immediate reward from taking action a in belief state b
- Pr(o|b, a): Probability of observation o given belief state b and action a
- b^{a,o’}: Updated belief state after taking action a and receiving observation o’
- gamma: Discount factor

**Lecturer’s emphasis:** “The best policy has the highest V* value.”

**Belief update equation (from slide 17):** b1_{a,o}(s’) = [p(o|s’,a) * sum_{s_i in S} p(s’|s_i, a) * b_0(s_i)] / p(o|a,b)

**Lecturer’s intuition:** “You use your initial belief to get an updated belief. […] So when you had the initial belief, I received information and I updated my belief.”

### Topic 6: Tiger Example (Complete Walkthrough)

This is the **template** for your own POMDP model in sub-question 2-4.

**Problem setup:**

- Two states: S0 = “tiger-left”, S1 = “tiger-right”
- Three actions: {0: listen, 1: open-left, 2: open-right}
- Two observations: hear tiger on left (TL), hear tiger on right (TR)
- Reward function: Wrong opening = -100, Correct opening = +10, Listening cost = -1

**Observation probabilities (LISTEN action):**

|            |O: TL|O: TR|
|------------|-----|-----|
|Tiger: left |0.85 |0.15 |
|Tiger: right|0.15 |0.85 |

**Observation probabilities (OPEN-LEFT or OPEN-RIGHT):** All 0.5 – “Any observation without listening is uninformative.”

**Transition probabilities (LISTEN):** Tiger doesn’t move. Tiger-left stays tiger-left (1.0), tiger-right stays tiger-right (1.0).

**Transition probabilities (OPEN-LEFT or OPEN-RIGHT):** Problem resets. All probabilities become 0.5 (you lose all information).

**Belief update process:**

1. Initial belief: b0 = [0.5, 0.5] (no information)
1. After listening and hearing tiger-left: belief updates to approximately [0.85, 0.15]
1. Continue listening to refine belief further

**Optimal policy at t=1:**

- Belief in [0.00, 0.10]: open-left (very confident tiger is right, so left door is safe)
- Belief in [0.10, 0.90]: listen (still uncertain)
- Belief in [0.90, 1.00]: open-right (very confident tiger is left, so right door is safe)

**Alpha vectors at t=1:**

- alpha^0(1) = (-100.0, 10.0) – open-left
- alpha^1(1) = (-1.0, -1.0) – listen
- alpha^0(1) = (10.0, -100.0) – open-right

**Optimal policy at t=2:** More branches in the decision tree because the agent has had more opportunities to listen and refine its belief. “As time progresses to t=2, the agent has had more opportunities to listen and thus may have a more refined belief state.”

**Lecturer’s key insight:** “The reason you see many listen states at t=2 is because each time the agent chooses to listen rather than open a door, it gets more information which updates its belief state about the location of the tiger.”

**Convergence:** “Calculate the V value using the Bellman equation and iterate at different time steps until it converges.”

**The policy in plain English:** “Roughly: listen until sure, then open.” (Slide 11)

### Topic 7: POMDP in HRI – The Real-World Application

**Slide 21 structure (POMDP for HRI):**

- **Observations:** z_t (sensors), l_t (language), g_t (gestures)
- **States:** p_t (physical states of world – objects, robots), h_t (human mental states)
- **Reward:** r_t (do what the person wants)
- **Robot Actions:** a_t (physical actions, languages, gestures)

**Lecturer’s explanation:** “You have sensors, you have language, you have gestures and all of them are connected in such a way. […] The states represent the human mental state. Human mental state means your emotions, your plans, your intents and the physical state of the world represents the objects.”

**Critical mapping to tiger example:** The tiger behind the door is analogous to the human’s hidden emotional/mental state. Listening is analogous to sensor observation (camera, microphone). The door-opening action is analogous to the robot’s response action.

**Lecturer’s analogy for HRI:** “Your emotions, you are putting it inside the room so it’s not observable for me. So I need to infer. […] Your emotions are not known for me. So I’m trying to listen. I’m trying to analyse the facial expressions to know if you are for example, happy or sad.”

### Topic 8: Trust-POMDP – Research Application

**Reference:** Chen, M., Nikolaidis, S., Soh, H., et al. (2020). “Trust-Aware Decision Making for Human-Robot Collaboration: Model Learning and Planning”, ACM Trans. Hum.-Robot Interact., 9(2).

**Model structure:**

- theta_t: Human trust (latent variable, transitions to theta_{t+1})
- a_t^H: Human action (depends on world state x_t and human trust theta_t)
- a_t^R: Robot action (depends on world state x_t and its belief over trust theta_t)
- x_t: World state (transits to x_{t+1} given human action a_t^H and robot action a_t^R)
- e_{t+1}: Robot performance (trust transitions depend on this)

**Lecturer’s emphasis:** “The trust variable is incorporated in the reward function and the Bellman equation.” (Slide text)

**Extensibility:** The lecturer explicitly stated you can add more latent variables beyond trust: “You can add another latent variable called intent. And you can add the trust and intent. It means like it will make the action considering the trust, considering the intent.” He then named naming conventions: “Trust-POMDP, intent-POMDP, emotion-POMDP, anything like this.”

**Social norms example (crucial for ethics, sub-question 2-5):** “If I am saying for example that okay, what happened? How can I help you? I sympathise with you, then the reward increases. So you have different actions to do while you are observing the person in front of you. […] I take the actions that will give me positive reward.”

**Lecturer’s core message:** “The purpose of this is like I’m letting the robot interact in the environment and interact with the human. But considering a latent variable called the trust.”

-----

## 4. LECTURER’S LEXICON

|Term                   |Lecturer’s Definition                                                                  |Context                                                  |
|-----------------------|---------------------------------------------------------------------------------------|---------------------------------------------------------|
|**Policy**             |“How should I take the action?” / Strategy for decision-making                         |Demystified deliberately – “Don’t let the word worry you”|
|**Belief**             |“The amount of information you have at state whichever”                                |Repeated 4+ times with emphasis                          |
|**Belief State**       |Probability distribution over states (e.g. [0.5, 0.25, 0.25])                          |Formal + intuitive definitions given                     |
|**Belief Space**       |The entire probability space – all possible belief distributions                       |Distinguished carefully from belief state                |
|**Alpha Vector**       |Linear segment in value function representing value of a belief-action pair            |Connected to policy trees                                |
|**Policy Tree**        |Hierarchical/tree representation of decision-making strategy under uncertainty         |Nodes = actions, branches = observations                 |
|**Piecewise Linear**   |Composed of linear segments that approximate the continuous value function             |Key property of POMDP value functions                    |
|**Value Function V(b)**|Continuous curve over belief space telling you how good each belief state is           |Cannot be table-based in POMDP                           |
|**Latent Variable**    |Unobservable variable (trust, intent, emotion) that must be inferred                   |Central to POMDP formulation in HRI                      |
|**Trust-POMDP**        |POMDP model that incorporates trust as a latent variable in the reward/Bellman equation|From Chen et al. (2020)                                  |

-----

## 5. COURSEWORK SUCCESS BLUEPRINT

### Sub-question 2-1 (20%): POMDP role in trust, cooperation, coordination, collaboration

**What the lecturer wants:** A discussion showing you understand WHY POMDP is suitable for HRI team problems. Use the Trust-POMDP as your primary example.

**Key arguments from lecture:**

- POMDP handles partial observability – human mental states (trust, intent, emotions) are hidden
- The belief mechanism allows the robot to maintain probabilistic estimates of these latent variables
- Trust-POMDP specifically incorporates trust into the reward function so the robot’s actions consider trust maintenance
- The framework is extensible to cooperation (add cooperation-related states), coordination (action dependencies between agents), and collaboration (joint reward optimisation)
- The lecturer explicitly said: “I’m trying to put all the parameters together so that when I use POMDP to find the best sequence of action or behaviour, I do, I consider the trust.”

**Lecturer’s preferred approach:** Use the graphical model representation (theta_t -> theta_{t+1}, x_t -> x_{t+1}, actions, rewards). Reference Chen et al. (2020).

### Sub-question 2-2 (20%): Role of uncertainty and how POMDPs handle it

**What the lecturer wants:** Explain the nature of uncertainty in HRI and map it to POMDP components.

**Key arguments from lecture:**

- Uncertainty in HRI comes from unobservable human states (emotions, intent, trust)
- “Your emotions are not known for me. So I’m trying to listen. I’m trying to analyse the facial expressions.”
- POMDP handles this through: belief states (probabilistic representation of uncertainty), observations (noisy sensor data), belief updates (Bayesian filtering to refine estimates)
- The tiger example demonstrates: initial uncertainty (0.5/0.5), information gathering (listening), belief refinement (0.85/0.15), and optimal action selection
- Continuous belief space means the robot handles gradations of uncertainty, not just binary known/unknown

### Sub-question 2-3 (15%): Challenges of modelling trust and POMDP solutions

**Key arguments from lecture:**

- Trust is a latent variable – cannot be directly observed or measured
- Trust changes over time based on robot performance (e_{t+1} in Trust-POMDP)
- Challenge: trust is subjective, culturally dependent, context-sensitive
- POMDP solution: treat trust as a hidden state, infer it through observations (human actions, feedback), and incorporate it into the reward function
- “If I will say how can I help you? I sympathise with you, the trust increases.”
- The Bellman equation with trust means the robot plans actions that maximise long-term trust, not just immediate task completion

### Sub-question 2-4 (35%): Develop your own POMDP model

**Template from lecture (tiger example structure):**

1. Define states (hidden + observable)
1. Define actions
1. Define observations
1. Specify transition probabilities
1. Specify observation probabilities
1. Define reward function
1. Specify initial belief
1. Show belief update process
1. Describe optimal policy

**Lecturer’s tip for sophistication:** Add multiple latent variables (trust + intent, or trust + emotion). “You can sophisticate it more.”

**Suggested scenario structure (based on lecture examples):**

- Healthcare robot assisting elderly patient
- States: patient emotional state (hidden), physical health indicators (partially observable)
- Trust as latent variable affecting patient compliance
- Observations: facial expressions, speech patterns, physiological sensors
- Actions: verbal encouragement, physical assistance, calling for help, waiting
- Rewards: positive for appropriate response, negative for social norm violation, cost for excessive sensing

### Sub-question 2-5 (10%): Ethical and social implications

**Lecturer’s signals:**

- Social norms violation example: “Somebody is sad and say I am happy that you are sad. This is out of social norms.”
- Reward function encodes what is “appropriate” – who defines this? Cultural bias?
- Trust modelling raises questions about manipulation – a robot optimising trust could learn to be deceptively reassuring
- Privacy concerns with continuous observation/sensing of human emotional states
- The cost of listening action (-1) implies a design choice about how much surveillance is acceptable

-----

## 6. HIDDEN CURRICULUM EXTRACTION

### Lecturer’s Research Interests

Dr. Aly’s research clearly centres on POMDP-based models for HRI with latent variables. He referenced the Trust-POMDP paper with detailed familiarity and enthusiasm. He values the framework’s ability to handle real-world HRI complexity.

### Pet Topics

- The connection between hidden emotional states and POMDP formulations
- The extensibility of POMDP to multiple latent variables
- Making mathematical concepts intuitive through real-life analogies

### Philosophical Position

The lecturer strongly believes in the POMDP framework as the “right” model for HRI because of inherent uncertainty in human states. He explicitly contrasted it with MDP as insufficient: “That’s why we use this in human robot interaction and not MDP.”

### What He Values in Student Work (from threshold criteria)

- 70%+: “Very well discussed in detail, supported by excellent arguments. Answers are correct and complete, especially with clear and well-justified analysis and description. There is strong evidence of investigation and research […] deep analysis and full investigation. The writings are of high standards and quality (focused and concise).”
- **“Focused and concise”** – he wants density of insight, not padding.
- **“Deep analysis and full investigation”** – go beyond the lecture, cite papers, show independent thinking.

-----

## 7. COMPUTATIONAL THINKING PATTERNS

### How the lecturer approaches POMDP problems:

1. Start with the intuitive story (hotel directions, career choices, entering a room)
1. Map the story to formal POMDP components (states, actions, observations, rewards)
1. Set up probability tables (transition, observation, reward)
1. Calculate belief updates step by step
1. Find optimal policy through value iteration
1. Interpret the result back in plain language

### His preferred problem-solving style:

- Always start from “what is the real-world situation?”
- Map to formal model
- Solve mathematically
- Interpret results practically

-----

## 8. META-LEARNING INTELLIGENCE

### Study Advice (Implicit)

- The lecturer said: “This is not detailed like one by one solving. Just to give you some kind of general, you know, brief of how can we formulate just a problem like this in real life.” – He does NOT expect you to solve POMDPs from scratch mathematically. He wants you to **understand the story** and **formulate** problems.
- “This is more or less to make you understand not the mathematical side because this is not machine learning module, but rather to understand the story how people use it.” – **This is a massive signal.** Your coursework should emphasise conceptual understanding and application design, not mathematical derivation.
- “If you are reading for example a human robot interaction paper, you have an idea of why, what does it mean POMDP and why it was used and why POMDP and not MDP.” – He wants you to be able to critically read HRI research papers and understand modelling choices.

### Key Reference to Cite

- Chen, M., Nikolaidis, S., Soh, H., et al. (2020). “Trust-Aware Decision Making for Human-Robot Collaboration: Model Learning and Planning”, ACM Trans. Hum.-Robot Interact., 9(2).

-----

## 9. WORD/CHARACTER BUDGET AWARENESS

Assessment 1, Task 2 has a **1,650-word limit** across 5 sub-questions. Rough allocation based on weights:

|Sub-question          |Weight|Suggested Words|
|----------------------|------|---------------|
|2-1 (POMDP role)      |20%   |~330 words     |
|2-2 (Uncertainty)     |20%   |~330 words     |
|2-3 (Trust challenges)|15%   |~250 words     |
|2-4 (Your own model)  |35%   |~575 words     |
|2-5 (Ethics)          |10%   |~165 words     |

**Warning:** 575 words for designing a full POMDP model is tight. Be extremely concise. Use a table for your probability specifications rather than prose – it’s more efficient and mirrors how the lecturer presented the tiger example.

**Therefore**: do loads of latex diagrams etc 

-----

## 10. TRANSCRIPT COMPLETENESS NOTE

The transcript appears to cover the full lecture content. It trails off at the end with attendance codes and brief student exchanges, but by that point the substantive material (POMDP theory, tiger example, POMDP in HRI, Trust-POMDP, extensibility to other latent variables) had been fully delivered. The slides confirm no major content was missed – the final slide (23) is simply a summary stating “Today we discussed: Introduction to POMDP. Next week: Cognitive Robotics.”

One potentially useful snippet from the very end: a student appears to ask about research findings in different countries, and the lecturer responds positively about discussing cultural tendencies – this could link to Task 1 (cultural factors in HRI) but the exchange is too fragmented to extract reliably.