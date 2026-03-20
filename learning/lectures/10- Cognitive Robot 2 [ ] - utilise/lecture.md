# Lecture 10: Learning from Demonstration (LfD)

**Module:** COMP3018/COMP5018 Human-Robot Interaction
**Lecturer:** Dr. Amir Aly
**Session Learning Outcome:** Describe the learning approach and its categories

---

## 1. CRITICAL ASSESSMENT INTELLIGENCE

### Direct Coursework Alignment (Task 4: CRAMS)

- The lecturer's formal LfD framework (S, A, Z, M, policy) maps directly onto CRAMS's POMDP tuple (S, A, O, T, Omega, R). CRAMS's observation space (Comply, Hesitate, Verbal_Refuse, etc.) is precisely the "Z" observations that LfD describes; the user is the "teacher" and the robot infers the best action from those observations.
- Inverse Reinforcement Learning (IRL) is the single most important concept from this lecture for CRAMS. Dr. Aly explicitly distinguishes IRL from standard RL: **"So effectively it's not reinforcement learning for the reason that the expert is needed. So when the expert is needed, this is a different story. This is called inverse reinforcement learning."** CRAMS's QMDP solver infers the reward structure from user behaviour rather than receiving an explicit reward signal; this is the IRL paradigm.
- The `main.py` TODO items (`talk about the LfD`, `talk about IRL`) confirm that these concepts should be woven into the Task 4 report; specifically in the Background (10%) and Method and Setup (35%) sections.
- The lecturer's emphasis on the **mapping function M** (linking world state + teacher observations + input to output) directly parallels CRAMS's observation model `build_observation_model()`, which maps user behavioural cues to structured observations the POMDP can process.
- **Transfer learning** tangent is relevant to CRAMS's future work section: transferring a learned medication adherence policy from one user profile to another (cooperative to resistant) is analogous to transfer learning between related domains.
- The **explicit vs implicit knowledge transfer** distinction maps to CRAMS: the OpenAI API provides *implicit* knowledge transfer (the robot infers user trust/load from behavioural cues rather than having direct sensor access to the user's internal state).

### What Distinguishes 70%+ Work Here

- Demonstrating that you understand the *relationship* between LfD, IRL, and POMDPs; not treating them as isolated topics but showing how they form a coherent cognitive architecture.
- Using the lecturer's own terminology: "underlying pattern", "mapping function", "policy derivation", "inverse reinforcement learning", "problem space continuity".
- Connecting the correspondence problem to the gap between raw human behaviour and structured POMDP observations.

---

## 2. The Alpha Brief: Comprehensive Directives

### Highest Priority

- **LfD is NOT reinforcement learning.** Dr. Aly repeated this distinction multiple times and tested students on it. "It is different from Reinforcement Learning, in which a policy is derived from experience. This means that there is no such expert; the agent has a 'reward' function, and it uses greedy/exploitative strategies to effectively explore the state and action space, and come up by itself (using trial and error) with an optimal policy." (Slide 6, repeated verbatim in transcript lines 136-143)
- **Inverse Reinforcement Learning (IRL)** is the correct term for learning from demonstration when the reward must be inferred. "Here we don't have a reward, but you have an expert. So you try to learn this reward in some sense." (Transcript lines 155-158). This was the subject of a direct student question and extended explanation.
- **The mapping function M** is what ties the entire LfD framework together. "Machine learning aims to learn the underlying pattern. Try to make sure that you are attentive to these technical words." (Transcript lines 288-292). Dr. Aly explicitly said using the phrase "underlying pattern" signals ML fluency.
- **Four types of LfD:** Teleoperation, Shadowing, Sensors on Teacher, External Observation. These arise from the 2x2 matrix of (Recording: direct/mapped) x (Embodiment: direct/mapped). (Slide 14)
- **Demonstration vs Imitation:** "When they are used directly, this is demonstration. When we are mapped or inferred, this is imitation." (Transcript lines 541-546)

### High Priority

- **Problem space** = task + environment + demonstrations. The agent must generalise learned behaviour to new situations similar to demonstrated ones. (Slide 9, transcript lines 216-222)
- **Batch vs interactive training:** batch = all data collected first; interactive = data arrives incrementally. (Slide 9, transcript lines 204-212)
- **Transfer learning** tangent: Dr. Aly spent significant time on this. "Instead of saying I need to train a system on X data, what if the X data doesn't exist? You use transfer learning. Look at similar area that has connections." (Transcript lines 241-246). Alzheimer's diagnosis example with 300 data points.
- **Correspondence problem:** human and robot may have different degrees of freedom. "The teacher has more or different degrees of freedom than robots." (Transcript line 456). Requires mapping function when structures differ.

### Notable

- Dr. Aly's Japan anecdote: students working 24 hours in 8-hour shifts for one month generating robot arm trajectory data; illustrates the data generation burden that LfD solves. (Transcript lines 15-21)
- "If you are in an interview and you say 'underlying pattern', I will say this guy is more familiar with common standard expressions in machine learning." (Transcript lines 291-293). Terminology matters.
- The Kinect/Xbox analogy for motion capture and direct correspondence. (Transcript lines 513-516, 612-618)
- Haptic devices: solve correspondence problem and provide haptic information, but require training and are not easy to use. (Transcript lines 623-627)

---

## 3. Exhaustive Topic Breakdown

### 3.1 Introduction: Why Learn from Demonstration?

**Slide 3: Programming robots is hard!**

- Huge number of possible tasks
- Unique environmental demands
- Tasks difficult to describe formally
- Expert engineering impractical

**Dr. Aly's verbatim explanation:** "Programming robot is hard. Huge number of possible tasks, unique environmental demands. Tasks are difficult to describe formally. And expert engineering in particular." (Transcript lines 44-46)

**Slide 4: LfD is the solution because it is:**

- Natural, expressive way to program
- No expert knowledge required
- Valuable human intuition
- Program new tasks as-needed

**Dr. Aly's verbatim:** "A natural way, for example, using learning demonstration is natural expressive way to program. No expert knowledge required. Valuable human intuition to program new tasks as needed." (Transcript lines 47-49)

**CRAMS connection:** CRAMS sidesteps the "programming is hard" problem by having the OpenAI API perceive user behaviour naturally; the POMDP then derives policy from these observations rather than requiring hand-coded behavioural rules for every possible user response.

---

### 3.2 Learning from Human Demonstrations: Principle

**Slide 5:**

- Transfer to the robot skills that took years for humans to master
- Human can quickly re-train the robot to adapt to task changes
- The human teaches by showing how to perform the task

**Dr. Aly's verbatim:** "What we're trying to do is pretty much one is that we are trying to transfer the robot skills that took years from humans to master. Human can quickly retrain the robot to adapt to task changes. And the human teaches by showing how to perform the task simply like that." (Transcript lines 56-58)

**CRAMS connection:** In CRAMS, the "demonstration" is not physical movement but *behavioural interaction*. The user's responses (Comply, Hesitate, Refuse, etc.) serve as demonstrations of how they respond to different robot actions, and the POMDP learns the optimal policy from these interaction sequences.

---

### 3.3 Learning from Demonstration (LfD): Formal Definition

**Slide 6: Core definition (quoted from slide, emphasised in red on the slide itself):**

> "Learning from Demonstration: Deriving a policy from examples provided by a teacher. The learner first observes the actions of an (often human) expert, during the training phase. The learner then uses this training set to learn a policy that tries to perform the same task demonstrated by the expert, in order to achieve the best performance."

**The critical distinction from RL (slide text, bold):**

> "It is different from Reinforcement Learning, in which a policy is derived from experience. This means that there is no such expert; the agent has a 'reward' function, and it uses greedy/exploitative strategies to effectively explore the state and action space, and come up by itself (using trial and error) with an optimal policy."

**Dr. Aly's classroom interaction on this point (transcript lines 78-143):**

He asked: "Is it similar in your understanding to reinforcement learning or not?"

Students were uncertain. He then walked through the key differentiator:

- "Think okay about the reward. What do we have in reinforcement learning?" (line 86)
- "Do we have in reinforcement learning, do we have expert or not?" (line 96)
- Key answer: "So what is a key point here is a reward. So you can try to make interaction with the environment and you learn is it good or bad by the reward. And the reward is a cookie." (lines 107-110)
- Navigation analogy: "If I go from here, that route, it will take five minutes. Another person can say, I will go to Germany, and from Germany I will take flight to Manchester..." (lines 127-130). More steps = more minus-one penalties = worse cumulative reward.
- Final verdict: "So effectively it's not reinforcement learning for the reason that the expert is needed. This is called inverse reinforcement learning." (lines 136-138)

**CRAMS connection:** CRAMS occupies an interesting middle ground. It utilises a POMDP with an explicit reward function R(s,a) (like RL), but the *user* acts as a kind of implicit expert whose behavioural responses guide belief updates (like IRL). The meta-reasoner detects when the robot's policy is failing and adapts; this is analogous to inferring reward from expert feedback rather than relying solely on a pre-defined reward.

---

### 3.4 LfD: Phases and Formal Components

**Slide 7: Two phases of LfD:**

1. **Gathering examples:** the process of recording example data to derive a policy from
2. **Deriving policies:** analysing examples to determine a policy

**Slide 8: Formal definition components:**

- **S** (States): the set of possible states of the environment
- **A** (Actions): the set of possible actions an agent can take
- **Z** (Observable states): the set of demonstrations provided by the human expert, mapped from S to Z by mapping **M** (the ultimate objective the agent is trying to learn)
- **Policy pi: Z -> A**: a selection of actions A based on the observable world states

**Dr. Aly's explanation:** "The world consists of states S. It defines the set of possible environment states. And actions A, it defines the set of possible actions that an agent can take in the environment. States Z are observable states. Z represents the set of demonstrations provided by the human expert, that are mapped from S to Z by mapping M, which represents the ultimate objective that the agent is trying to learn. The policy pi: Z -> A is a selection of actions A based on the observable world states." (Transcript lines 172-201)

**CRAMS mapping:**

| LfD Component | CRAMS Equivalent |
|---|---|
| S (world states) | 9 hidden states: Trust(High/Med/Low) x Load(Low/Med/High) |
| A (actions) | 6 robot actions: Gentle_Reminder, Explain_Importance, Back_Off, Encourage, Direct_Prompt, Simplify |
| Z (observations from teacher) | 7 behavioural cues: Comply, Hesitate, Verbal_Refuse, Ignore, Gaze_Avert, Nod, Ask_Question |
| M (mapping function) | `build_observation_model()` in pomdp.py; the parametric observation model Omega(o\|s',a) |
| Policy pi | QMDP belief-weighted action selection in `QMDPSolver.select_action()` |

---

### 3.5 LfD: Training Modes, Problem Space, and Generalisation

**Slide 9:**

- **Batch training:** policy derived *after* all training data is obtained
- **Interactive training:** policy developed incrementally as data becomes available

**Dr. Aly's explanation:** "Do you know the batch world? So you have all the data already arrived and you have it. Nothing's coming after. On the other side, you have the incoming incrementally coming data. So it's called batch training. You have already everything." (Transcript lines 204-212)

**Problem Space (three components):**

1. The **task** that the agent needs to learn
2. The **environment** in which the task is performed
3. The **demonstrations** provided by the expert

**Generalisation challenge:** "The agent should be able to generalise the learned behaviour to new situations that are similar to the demonstrated ones." (Transcript line 222)

**Dr. Aly's bedsheet/T-shirt example:** "If you learned to fold big bed sheets, you should be able to transfer this knowledge to a T-shirt. The concept is learned. So if you give it a different piece of clothes, a different texture, it should fold it with the same principle." (Transcript lines 223-228)

**Diverse demonstrations required:** "To ensure that the agent can generalise to different situations, it is essential to collect a diverse set of demonstrations that cover different variations of the task. For example, if the task is to navigate a robot, the demonstrations should cover different types of obstacles, terrains, and lighting conditions." (Transcript lines 272-273)

**CRAMS connection:** CRAMS addresses generalisation through its `compare_scenarios()` function, which runs cooperative, uncertain, and resistant user profiles side-by-side. This is the equivalent of "diverse demonstrations" covering different variations. CRAMS uses *interactive* training (online belief updates each step) rather than batch training.

---

### 3.6 Deriving a Policy: The Mapping Function

**Slide 10: Three methods for calculating the underlying function:**

#### 3.6.1 Regression-Based Methods

- Fit a function to input-output pairs using techniques such as linear regression
- The resulting function serves as the mapping function
- "You have inputs, you have outputs and you just need to link between them through a function. So simply speaking, you try to find the curve that passes by all the inputs and the outputs." (Transcript lines 297-301)

#### 3.6.2 Decision Tree-Based Methods

- Construct a tree structure that partitions the input space based on input features
- Output for each partition determined by majority vote
- Once trained, used to estimate the mapping function M for new input data

**Dr. Aly's extended navigation example (transcript lines 303-370):**

"The decision tree is like making a tree. And the tree has a lot of nodes and these nodes are used for making a decision. So should I, for example, I reached an obstacle. If I reached an obstacle, should I go to left or right? So this becomes a node. If you find your left is free, go to left. If you find your right is free, go to right. If your left and your right are not free, go back." (Lines 303-314)

He then extended this to include world observations AND teacher observations as decision nodes: "I'm trying to put both the nodes, the decision nodes, make them represent the world and the observation from the teacher. So I make decision nodes everywhere until I come to a final branch and a final action." (Lines 341-343)

**Dr. Aly's key point on unifying multiple demonstrations:** "If you build a tree representing all these actions and each node that represents a decision that each person took when they were creating the robot action, you find a unified tree and you give all this data for training." (Transcript line 365)

#### 3.6.3 Inverse Reinforcement Learning (IRL)

- No explicit reward function; the reward is *inferred* from expert behaviour
- "Here we don't have a reward, but you have an expert. So you try to learn this reward in some sense." (Transcript lines 155-157)

**Dr. Aly's obstacle-avoidance example of reward inference:** "If I am following an expert, the expert, for example, let's say I'm trying to do an action, moving the arm. And there were a lot of obstacles. So when I'm moving the robot arm, I find that the robot has slowed down or tried to avoid this object and then try to avoid this object. And there was always positive reward here or like more focus on avoiding these objects. So I will understand, implicitly infer it, that when I approach this object, I should avoid it." (Transcript lines 158-164)

**Student question (transcript lines 407-429):** "How does it infer the reward?"

Dr. Aly's answer: "I put a group of obstacles. I try to avoid the group of obstacles. This is something that we can understand that there is an obstacle in XYZ coordinates and the person tried to turn around XYZ. So this means the person tried to avoid these obstacles. So this will be a point itself that these points should be avoided." (Lines 416-422)

**CRAMS connection:** This is directly relevant. CRAMS's observation model does precisely this: when the user hesitates or averts gaze after a Direct_Prompt, the POMDP infers (via Bayesian belief update) that trust is low and cognitive load is high; it thereby "infers the reward" for backing off or simplifying rather than persisting. The `MetaReasoner` component explicitly detects declining reward trends (i.e., infers that the current policy is not aligned with the "expert's" implicit preferences) and adapts.

---

### 3.7 Knowledge Transfer: Explicit vs Implicit

**Slide 11:**

- The world state is often *not directly accessible* to the robot; it must depend on its **observations**
- The learned action policy tells the robot what action to take based on its observations
- During learning, knowledge is transferred to the robot
- Transfer may be **explicit** or **implicit**:
  - **Explicit:** the robot has direct access to the teacher's knowledge (motion, world state information)
  - **Implicit:** the robot has to infer it

**Dr. Aly's verbatim:** "The world isn't directly accessible to the robot. So it has to depend on its observations." (Transcript lines 434-435)

"Explicit way to transfer this knowledge to the robot is if the robot directly accesses the teacher knowledge. The motion, the world state information that characterise the actions being performed." (Transcript lines 442-444)

"When the robot doesn't have this explicit knowledge directly accessed, we call it implicit. Like you have to infer." (Transcript lines 447-449)

**CRAMS connection:** CRAMS operates entirely in the *implicit* regime. The robot never has direct access to the user's trust level or cognitive load (these are the hidden states S). It must infer them from observable behavioural cues (Z = Comply, Hesitate, Refuse, etc.) via Bayesian belief update. This is precisely why CRAMS uses a POMDP rather than an MDP: the partial observability means the robot must maintain a probabilistic belief over hidden states and act on that belief.

---

### 3.8 Transfer Steps and Four Types of LfD

**Slide 12: Two steps:**

1. **Recording** the teacher's actions
2. Determining the **correspondence** of this data with the robot's embodiment

Each step can be **direct** (data used without modification) or **indirect** (data must be mapped/inferred).

**Slide 13-14: The 2x2 matrix produces four types:**

| | Embodiment: Used Directly | Embodiment: Mapped/Inferred |
|---|---|---|
| **Recording: Used Directly** | **Teleoperation** | **Sensors on Teacher** |
| **Recording: Mapped/Inferred** | **Shadowing** | **External Observation** |

- **Left column** (direct embodiment): teaching data matches the robot's body; can be used directly = **Demonstration**
- **Right column** (mapped embodiment): teacher's body doesn't match the robot's body; data must be mapped = **Imitation**

**Dr. Aly's definitions:**

- **Teleoperation:** "A human directly controls a mobile robot and the robot records the control data." (Transcript line 504). Xbox Kinect example: "The camera can measure directly your articulations and how they are moving. And this is the recording; map them directly to the embodiment." (Lines 514-515)
- **Sensors on Teacher:** "The robot has direct access to the teacher action data. Sensors on teacher is like, instead of using Kinect, you have sensors on the teacher. And these sensors transfer the movement data directly." (Lines 518-521)
- **Shadowing:** "Human uses gestures to teach a humanoid robot and the robot observes the human, interpreting the movement. Here the robot doesn't have direct access to the teacher's action data." (Lines 525-528)
- **External Observation:** "The robot observes recordings of an expert performing the task." (Line 535)

**The Demonstration vs Imitation distinction:** "When they are used directly, this is demonstration. When we are mapped or inferred, this is imitation. Learning from demonstration and learning from imitation is simply related to how the robot can access the data and the embodiment versus recording." (Transcript lines 541-540)

**CRAMS connection:** CRAMS falls into the **External Observation** quadrant. The robot (via OpenAI API) *observes* the user's behavioural cues without direct sensor access to the user's body/brain state. The embodiment correspondence must be *inferred* (the mapping from raw behavioural signals to structured POMDP observations is performed by the LLM perception layer). This means CRAMS performs **imitation learning**, not demonstration learning, in Dr. Aly's taxonomy.

---

### 3.9 The Correspondence Problem

**Slides 16-17:**

The human teacher may have different degrees of freedom (DoF) than the robot. A correspondence must be established across degrees of freedom when feasible.

**Dr. Aly's verbatim:** "The teacher has more or different degrees of freedom than robots. You have two arms. You might find a robot that has only one arm. You have three degrees of freedom in each articulation. The robot might have one or two or three." (Transcript lines 456-460)

When structures match: use data without modification.
When structures differ: need a mapping function.

**Dr. Aly's iCub warning:** "If the teacher was doing a particular action with the arm and we tried to make the robot do this action, particularly without simulating it first, it can break any of the articulations and it costs a lot." (Transcript lines 466-468)

**CRAMS connection:** In CRAMS, the "correspondence problem" manifests differently: the robot must map between the high-dimensional space of human behavioural expression (facial expressions, voice tone, gestures; effectively infinite DoF) and the low-dimensional structured observation space (7 discrete categories). The OpenAI API serves as the mapping function that resolves this correspondence problem, translating rich multimodal human behaviour into the POMDP's observation vocabulary.

---

### 3.10 Sensing Interfaces for LfD

**Slides 18-20:**

#### Motion Capture (Phasespace, Vicon)

- Camera-based systems that surround the subject and track marker positions
- Used for full-body tracking

#### Motion Sensors (Slide 19)

**Pros:**
- Real-time kinematic information
- Solve the correspondence problem

**Cons:**
- Require wearing the system (not comfortable)
- No haptic information

**Dr. Aly's verbatim:** "They have real time kinematic information they provide. They solve the correspondence problem. But the cons: required to wear the system. And this is probably not comfortable, not smooth interaction, and no haptic information." (Transcript lines 605-609)

#### RGB-D Cameras and Depth Sensors (Slide 20)

- Standard RGB cameras
- Stereo cameras (Bumblebee)
- RGB-D: Microsoft Kinect (highlighted in red on slide)
- Time of flight: Swiss Ranger
- LIDAR: SICK

**Dr. Aly on Kinect:** "Kinect camera provides depth cameras. RGB provides like RGB colours and they provide you the ability to define the depth of objects or dimensions of objects. So it facilitates 3D interaction or interpretation." (Transcript lines 616-619)

#### Wearable Sensors

- Accelerometers, pressure sensors, etc.

#### Haptic Devices

**Dr. Aly's verbatim:** "Haptic devices allow you to have the feeling of when you touch an object. This is haptic information. They solve the correspondence problem, they provide haptic information, but require training and not very easy to use." (Transcript lines 623-626)

**CRAMS connection:** CRAMS's sensing interface is the OpenAI API acting on camera/microphone input from a NAO robot. This is most analogous to the **RGB-D camera** approach but with the critical addition of LLM-based semantic interpretation. Rather than tracking joint angles or depth maps, CRAMS extracts high-level behavioural semantics (trust cues, cognitive load indicators) from visual and auditory data.

---

### 3.11 Transfer Learning (Extended Tangent)

Dr. Aly spent significant time on transfer learning as an alternative when LfD data is unavailable.

**Core principle:** "Transfer learning, simply we try to transfer knowledge, but through training data. If you learn how to play ping pong, this is knowledge you created, which we can transfer and apply to squash. Because the concept is that there is a racket, you catch the racket and you play." (Transcript lines 236-240)

**Alzheimer's example:** "Let's say I would like to make diagnosis for Alzheimer. And I have very limited data set. 300 data elements. Not enough to train a system. But let's say I have another disease or disorder that has thousands of data and cognitively related to Alzheimer. Then I will go to this related disorder, train my system on the data that exists there. Then take that trained system and come back to the 300 data elements in Alzheimer and try to fine tune." (Transcript lines 253-262)

**The mechanism:** "You created a deep learning model. You come and you cut the last layer. You fine tune the model again on this few data samples and you create another layer that substitutes the previous layer. So you have adapted the model with core knowledge that just belongs to something else, to your case, and it can make miracles." (Transcript lines 264-266)

**CRAMS connection:** This is relevant to CRAMS's scalability argument. A CRAMS agent trained on cooperative user interactions could transfer its learned belief dynamics to a new resistant-user scenario by fine-tuning the transition and observation models whilst preserving the core POMDP structure. The `compare_scenarios()` function already demonstrates performance across different user profiles, which is the precursor to a transfer learning approach.

---

## 4. Lecturer's Lexicon

| Term | Dr. Aly's Definition | Context |
|---|---|---|
| **Learning from Demonstration (LfD)** | "Deriving a policy from examples provided by a teacher" | Core topic; Slide 6 |
| **Policy** | "The best approach" / "best strategy"; pi: Z -> A | RL/LfD; Slide 8 |
| **Inverse Reinforcement Learning (IRL)** | "The expert is needed. You don't have a reward but you try to infer it" | Key distinction from RL; Slide 10 |
| **Mapping function M** | Links world state + teacher observations + input to output; "the ultimate objective the agent is trying to learn" | Slide 8 |
| **Underlying pattern** | What ML aims to learn; standard expression signalling ML fluency | Transcript line 288 |
| **Problem space** | Task + environment + demonstrations | Slide 9 |
| **Batch training** | All data collected first, then policy derived | Slide 9 |
| **Interactive training** | Policy developed incrementally as data arrives | Slide 9 |
| **Correspondence problem** | Mismatch in degrees of freedom between human demonstrator and robot imitator | Slides 16-17 |
| **Teleoperation** | Human directly controls robot; robot records control data | Slide 14 |
| **Shadowing** | Robot observes human and interprets movement (no direct data access) | Slide 14 |
| **Sensors on Teacher** | Sensors on human body transfer movement data directly to robot | Slide 14 |
| **External Observation** | Robot observes recordings of expert performing task | Slide 14 |
| **Demonstration** | Direct use of recorded/embodied data | Slide 14 |
| **Imitation** | Mapped/inferred use of recorded/embodied data | Slide 14 |
| **Transfer learning** | Transferring knowledge from a related domain when target data is scarce | Extended tangent |
| **Fine tuning** | Adapting a pre-trained model to a new domain using limited data | Transfer learning context |
| **Embodiment** | The physical body/structure of the robot; its degrees of freedom | Correspondence problem |
| **Haptic information** | Tactile/touch feedback from interaction with objects | Sensing interfaces |

---

## 5. Coursework Success Blueprint (Task 4: CRAMS)

### Mapping Lecture Concepts to Report Sections

#### Introduction (10%)

- Frame CRAMS as a cognitive robot that *learns from user interaction* in the same way that LfD robots learn from human demonstrations
- Use Dr. Aly's rationale for LfD: "Programming robots is hard. Huge number of possible tasks, unique environmental demands." This justifies why CRAMS uses a POMDP (learning approach) rather than hard-coded behavioural rules

#### Background (10%)

- Position CRAMS within the LfD taxonomy: it is an **External Observation + Imitation** system
- Explain the IRL connection: CRAMS infers the user's implicit "reward" (compliance/engagement) through Bayesian belief updates, which is the inverse reinforcement learning paradigm
- Reference the formal LfD framework (S, A, Z, M, pi) and show how CRAMS's POMDP tuple extends it with probabilistic belief

#### Method and Setup (35%)

- The mapping function M in LfD corresponds to CRAMS's observation model Omega(o|s',a)
- The policy derivation in LfD corresponds to CRAMS's QMDP value iteration
- The correspondence problem is solved by the OpenAI API perception layer (mapping high-DoF human behaviour to low-dimensional structured observations)
- Knowledge transfer is implicit (the robot must infer trust and load from behavioural cues)

#### Results/Outcome (30%)

- Show how CRAMS generalises across user profiles (cooperative, uncertain, resistant); this addresses the "continuity of the problem space" challenge Dr. Aly emphasised
- The belief evolution plots demonstrate the robot learning the "underlying pattern" of user behaviour
- The meta-reasoning adaptation demonstrates the IRL principle: when the inferred reward declines, the robot adjusts its strategy

#### Conclusion (10%)

- Future work: transfer learning between user profiles (directly from Dr. Aly's transfer learning tangent)
- Future work: moving from external observation to sensors-on-teacher (wearable physiological sensors for direct trust/load measurement, eliminating the correspondence problem)

---

## 6. Hidden Curriculum Extraction

### Lecturer's Research Interests

- Dr. Aly has an **underwater robot** in his lab that he controls via teleoperation ("I have for example something like this in my lab to control my underwater robot. So I send the robot underwater and using that kind of device to ask the robot to move forward, move back." Transcript lines 631-632)
- He also has a **Baxter robot** (the big red one) and an **iCub** in his lab
- His personal experience with Kinect-based imitation: "When I was a student in my generation, I was doing Kinect, using Kinect to make imitation. So I move with Kinect and Kinect captures how the articulations moved and imitated." (Transcript lines 642-643)

### Pet Topics

- The LfD-to-IRL distinction (tested students on it; extended explanation)
- Transfer learning (spent disproportionate time; clearly enthusiastic)
- The correspondence problem and degrees of freedom

### Philosophical Position

- Dr. Aly sees machine learning as always providing *some* solution: "Machine learning always tries to provide you with some solutions. If you have data, fine, you are safe. If you don't have data, try to learn from demonstrations and generate data implicitly." (Transcript lines 269-271)
- He values practical, intuitive explanations alongside formal definitions

---

## 7. Q&A and Interactive Moments

### Key Student Question: "How does it infer the reward?" (Transcript lines 407-429)

**Context:** A student asked how the robot infers the reward in IRL.

**Dr. Aly's response:** He used the obstacle avoidance example. If a human demonstrator consistently avoids obstacles at specific XYZ coordinates, the robot infers that these locations carry negative reward (should be avoided). "It decides based on what it observes." (Line 428)

This is directly analogous to CRAMS: if a user consistently averts gaze or refuses after Direct_Prompt actions, the POMDP infers (via declining belief in high trust) that Direct_Prompt carries a negative effective reward in this context.

### RL vs LfD Distinction (Transcript lines 78-143)

Dr. Aly spent extended time testing students' understanding. Key teaching moment: "Do we have in reinforcement learning, do we have expert or not?" Students initially said yes. Dr. Aly corrected: in RL, there is no expert; there is only a reward signal. In LfD/IRL, there IS an expert but NO explicit reward.

---

## 8. Meta-Learning Intelligence

### Study Advice

- Dr. Aly explicitly recommended using standard ML terminology in interviews and academic work: "If I hear 'underlying pattern', I will say this person is familiar with common standard expressions in machine learning." (Transcript lines 291-293)
- He connects topics across modules: "For those who make machine learning, COMP3003" and mentions COMP5008 Advanced Machine Learning for transfer learning

### Terminology to Use in Your Report

From this lecture, the following terms should appear in your Task 4 report where relevant:
- "underlying pattern" (when discussing what the POMDP learns)
- "mapping function" (when discussing the observation model)
- "inverse reinforcement learning" (when positioning CRAMS theoretically)
- "policy derivation" (when discussing QMDP solver)
- "correspondence problem" (when discussing the gap between human behaviour and structured observations)
- "implicit knowledge transfer" (when discussing how CRAMS infers hidden states)

---

## 9. Summary: What This Lecture Means for CRAMS

CRAMS already implements several concepts from this lecture without explicitly naming them. The Task 4 report should make these connections explicit:

1. CRAMS performs **imitation learning via external observation** (Dr. Aly's taxonomy)
2. The POMDP belief update is a form of **inverse reinforcement learning** (inferring reward from user behaviour rather than receiving it explicitly)
3. The OpenAI API perception layer solves the **correspondence problem** between high-dimensional human behaviour and low-dimensional structured observations
4. CRAMS's multi-scenario testing addresses the **problem space continuity** challenge
5. Knowledge transfer to the robot is **implicit** (hidden states must be inferred from observations)
6. The **mapping function M** is implemented as the parametric observation model Omega(o|s',a)
7. CRAMS uses **interactive** (not batch) training; beliefs update continuously each interaction step

These connections, articulated using Dr. Aly's exact terminology, will demonstrate the deep understanding that distinguishes 70%+ work.
