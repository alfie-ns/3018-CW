# COMP3018 Lecture 9: Introduction to Cognitive Robotics

## BRITISH AI Lecture Intelligence Extraction

### Lecturer: Dr. Amir Aly | Date Extracted: 13 March 2026

-----

## 1. CRITICAL ASSESSMENT INTELLIGENCE [HIGHEST PRIORITY]

### Direct Coursework Alignment: Assessment 2 (70% Report, Due 5th May 2026)

**Task 3 – Literature Review (40% of Assessment 2): Assistive Robotics Essay (1,800 words)**

This lecture provides foundational vocabulary and conceptual framing for assistive robotics within a cognitive framework. Key mappings:

- The literature review must cover “impact, challenges, future applications, and ethical issues” of assistive robotics. Cognitive robotics is the theoretical backbone that makes assistive robots *actually useful* – Aly explicitly stated: “cognition allows robots to work autonomously in everyday environments” and “enables effective interaction with humans.” Your essay should frame assistive robotics as requiring cognitive capabilities (not just social behaviour) to be genuinely effective.
- Aly’s distinction between social robotics and cognitive robotics is a mark-earning framing device. He said: “people who work in cognitive robotics certainly can work on social robotics… we need the intelligence to be deployed over social layer of behavior, not vice versa.” This hierarchy (cognition > social layer) should inform how you discuss the *limitations* of current assistive robots in your literature review – many are socially reactive but not cognitively capable.
- The concept of **embodied cognition** (“intelligence means body”) directly connects to assistive robotics challenges: robots assisting elderly/disabled users need physical embodiment to sense and interact, not just process language.
- **Episodic memory** and **semantic memory** concepts are directly relevant to assistive robots that need to remember user preferences (episodic) and understand their environment (semantic).
- **Theory of mind** – Aly discussed this as the ability to “put myself in your place” and “infer your goals.” For assistive robotics, this is the gold standard: a robot that can anticipate a user’s needs without being explicitly told. Cite this as a future direction/challenge.

**Task 4 – Programming Project (60% of Assessment 2): Novel HRI Project (2,000 words + code + 5-min video)**

This is where Lecture 9 is *most* valuable. The project requires “a novel intellectual contribution that addresses a problem of interest” and “the focus should be… related to a core topic(s) we have covered in class.”

- Aly explicitly *invited* cognitive robotics projects: “I have never seen up to now a project like somebody would like to work on affordances learning, for example. So it’s like invitation for challenging minds would like to make something like excellent like this.” This is a direct signal that a cognitive robotics project would impress him and is considered higher-tier work.
- He also immediately tempered this with: “But we… bear in mind also the time constraints.” So the project must be scoped realistically within the timeframe.
- The project must be approved: “you have to approve the idea… first… so that we can understand if it is doable. Not doable… it has enough complexity.”
- For non-robot users: “for those who will not use robots, they have to come to speak to me.” – This suggests simulation-based or API-based approaches may be acceptable but need explicit approval.

### Implicit Marking Scheme Signals

- Aly values **sophistication** – he repeatedly used this word: “sophisticate a certain behavior”, “more sophisticated research than working on the very social layer.” A project that operates at the cognitive level rather than just the social level will score higher.
- He values **interdisciplinary grounding** – connecting to psychology, cognitive science, developmental theories. A project that references cognitive science literature (not just engineering) aligns with his worldview.
- He values **formal specification** – definitions, building blocks, architectures. Your project report should have clear formal components (state spaces, architecture diagrams).
- The threshold criteria for 70%+ states: “very well discussed in detail, supported by excellent arguments… clear and well-justified analysis… deep analysis and full investigation… high standards and quality (focused and concise).”

-----

## 2. THE COMPLETE ‘ALPHA’ BRIEF: Comprehensive Directives

### Triple-Star Directives (Mark-Critical)

- **[***] PROJECT INVITATION**: “I have never seen up to now a project like somebody would like to work on affordances learning… it’s like invitation for challenging minds would like to make something like excellent like this.” – Aly is explicitly signalling that cognitive robotics projects are rare and would be viewed favourably. This is your competitive advantage.
- **[***] COGNITIVE > SOCIAL HIERARCHY**: “people who work in cognitive robotics certainly can work on social robotics… we need the intelligence to be deployed over social layer of behavior, not vice versa.” – Frame your project as deploying cognitive intelligence *over* social behaviour, not the other way round. This mirrors Aly’s own career trajectory and philosophical position.
- **[***] EMBODIED COGNITION**: “intelligence means body” – Aly stated this is his core belief (“I was always saying that intelligence means body”). If your project involves a physical robot or simulated embodiment, explicitly connect to this concept. This is Aly’s research identity.
- **[***] COGNITIVE ARCHITECTURE AS BUILDING BLOCKS**: The core cognitive abilities (perception, attention, action selection, memory, learning, reasoning, metacognition, prospection) are the “basic building blocks” that appear in “all the systems that we will discuss in the next two lectures.” Your project should explicitly map its components to these building blocks.

### Double-Star Directives (High Value)

- **[**] PROSPECTION IS THE KEY DIFFERENTIATOR**: “a key feature of cognitive robotics is a focus on prospection to augment the immediate sensory motor experience.” Prospection (anticipating outcomes) is what separates cognitive robots from reactive ones. If your POMDP-based system anticipates user behaviour, you are implementing prospection – use this exact term.
- **[**] EPISODIC vs SEMANTIC MEMORY**: “please distinguish or remember these two because we will see these two memories in many of the cognitive architectures models.” Aly explicitly asked students to remember this distinction. Episodic = past experience memories; Semantic = knowledge about the world (spatial relationships, facts). Both appear in cognitive architectures. If your project has memory components, label them as episodic or semantic.
- **[**] THEORY OF MIND**: “from what’s called… theory of mind, try to put myself in your place. And from that I try to infer your goals.” – This is directly relevant to your POMDP trust model: the robot inferring the user’s latent state (trust, cognitive load) is a form of theory of mind. Explicitly name it as such.
- **[**] METACOGNITION**: “meta cognition… you think about why did you do this in that situation… you take an action and then you reflect about the action you have taken.” If your system has any self-evaluation or policy-reflection component, frame it as metacognition.
- **[**] 42 DEFINITIONS OF COGNITION**: Aly highlighted that there is no single definition, but the common thread across all 42 is: “we anticipate, we learn, we adapt, and we intersect this with perception and action to create autonomy.” Use this synthesis in your report.

### Single-Star Directives (Notable)

- [*] **Affordances learning** was mentioned as an example of a never-attempted project topic. If you can incorporate any element of affordance reasoning (how the robot determines how to interact with objects based on their properties), this would stand out.
- [*] **Agent** is a technical term meaning “robot or human” – use this terminology in your report. Aly explicitly tested students on this definition.
- [*] **Goal-directed action** vs metaphoric gesture – Aly distinguished between purposeful actions (grasping a cup) and non-referential gestures (waving hands while speaking). Cognitive robots perform goal-directed actions. Frame your robot’s actions as goal-directed.
- [*] **Direct vs indirect interaction** – Direct: robot assists customer face-to-face; Indirect: robot stacks shelves while customers shop, but actions still affect each other through the shared environment. Consider which your project implements.
- [*] **Attention types**: Suppressive (ignoring irrelevant stimuli), Restrictive (limiting where to look), Selective (choosing specific features/objects). If your system filters observations, frame this as attention.

-----

## 3. EXHAUSTIVE TOPIC BREAKDOWN

### 3.1 What is Cognitive Robotics? (Slides 3-6)

**Aly’s Definition (via Cangelosi and Asada):**
Cognitive robotics is the intersection of three domains: Robotics, Artificial Intelligence, and Cognitive & Biological Sciences. The intersection of just Robotics and AI gives “Intelligent Robotics” or “AI Robotics” (Murphy, 2017). Adding Cognitive & Biological Sciences gives Cognitive Robotics.

Aly’s verbatim framing: “So we just don’t speak about robotics in general from the engineering perspective, but artificial intelligence from the functions like computer vision or speech processing, etc. We speak also about cognitive and biological science.”

**Cangelosi & Asada formal definition (Slide 5):** Cognitive Robotics combines insights and methods from robotics, AI, and cognitive and biological sciences to design an integrated cognitive system combining sensorimotor behaviour, higher-level functions, and social capabilities of an intelligent robot.

Aly’s unpacking: “you involve the sensory motor behavior… higher level functions is all about the cognitive functions that we are trying to model from what we have in infants and robots and social capabilities.”

**Cognitive Robotics Emphasises (Slide 6):**

- Bio-inspired, human-like and animal-like behaviour and intelligence
- System-level integration of cognitive abilities: sensorimotor skills, knowledge representation & reasoning, social interaction
- Interdisciplinary approach: cognitive (neuro)science, cognitive psychology, biology

**Key Lecturer Insight – His Career Trajectory:**
“When I was young, I finished my PhD in Social Robotics and then I said no, I need to work in more sophisticated research than working on the very social layer of research in robotics… I was believing… I should work in cognitive robotics, developmental robotics. So as a postdoc. So it took me some time and that actually what took me to Japan to stay several years there to work on cognitive and developmental like language development.”

This is critical hidden curriculum: Aly personally views cognitive robotics as *more sophisticated* than social robotics. A project pitched at the cognitive level will resonate with his worldview.

### 3.2 Development of Cognitive Robotics (Slide 7)

Timeline of key platforms:

- **1950**: Tortoises (Walter, 1953 – “The Living Brain”)
- **1966**: Shakey (MIT) – Aly: “if you search YouTube for robots, you’ll find Shaky from MIT”
- **1986**: Vehicles (Braitenberg)
- **1992**: Darwin
- **1999**: Khepera
- **2007**: CB2; Pfeifer & Bongard “How the Body Shapes the Way We Think”
- **2008**: iCub
- **2015**: Octopus; Cangelosi & Schlesinger “Developmental Robotics: From Babies to Robots”

**iCub as the informal standard**: “the informal standard is that iCub… is the one that is used mostly in research related to cognitive robotics.” Aly noted it has “sophisticated fingers” for grasping but its face is “difficult to be used for social robotics despite the fact that they have some lids.”

**Key reference**: Cangelosi and Schlesinger’s book “Developmental Robotics: From Babies to Robots” – Aly highlighted this as the foundational text. The “Kangaroosi” in the transcript is likely **Cangelosi** (transcription error).

### 3.3 Why is Cognition Useful in Robotics? (Slides 10-11)

Two core reasons:

1. “It allows robots to work autonomously in everyday environments”
1. “It enables effective interaction with humans”

**Cognitive robot characteristics (Slide 11):**

- Capable of **flexible context-sensitive goal-directed action**
- Anticipates: (a) the need to act, (b) the outcome of the action
- Action guided by **prospection** (not just sensory-motor reaction)
- Can adapt to changing circumstances by adjusting existing or creating new action policies
- Achieves this by dynamically recruiting **core cognitive abilities**: perception, attention, action selection, memory, learning, reasoning, metacognition, prospection

Aly’s explanation of prospection: “you don’t depend on sensory motor information… you try to expect the outcome of the action… and consider it in your planning, like reinforcement learning. So learn from the action and plan or use it to plan for future action.”

Aly’s explanation of goal-directed action: “Goal directed is like you are making an action for a specific goal. Like grasping an object to make something flexible, context sensitive. So it’s like it can certainly learn from the context.”

He contrasted this with **metaphoric gestures** (non-goal-directed): “when I have like moving my hands like this, I’m speaking. What kind of gestures is this? Metaphoric.” – This connects back to the gesture taxonomy from earlier lectures.

### 3.4 What is Cognition? (Slides 12-18)

**The 42 Definitions Problem (Slide 13):**
The European Network for Advancement of Artificial Cognitive Systems (euCognition) collected 42 definitions of cognition. Aly highlighted several:

- **Mike Denham**: “the ability to relate perception to action in a meaningful way, determined by experience, learning and the memory”
- **Horst Bischof**: “a cognitive system possesses the ability of self-reflection, or at least self-awareness”
- **Majid Mermehdi**: “gaining knowledge through the senses”
- **Christian Bauckhage**: “the ability to ground perceptions into concepts together with the ability to manipulate concepts in order to proceed toward the goals”

Aly’s synthesis of all 42 (Slide 14): “in most of them, we can see that cognition has… basic stages and cycles, like we anticipate, we learn, we adapt, and we intersect this with perception and action to create autonomy.”

This maps to the Vernon (2014) cycle diagram: **Anticipate -> Learn -> Adapt**, intersecting with **Perception <-> Action** to create **Autonomy**.

**Core Abilities of a Cognitive System (Slide 15):**
Perception, Attention, Action Selection, Memory, Learning, Reasoning, Meta-reasoning… and **Prospection**.

**Prospection Umbrella (Slide 16):**
Under prospection sit: Anticipation, Prediction, Intention, Planning, Simulation, Episodic Future Thinking.

**Episodic Future Thinking (Slide 17):**
Aly: “The past events are reconstructed to allow the agent to re-experience the future… you remember a problem, similar problem happened… and how you have reacted and how your reaction generated a specific… reaction from others… So you start rebuilding the situation in your mind… to think about what happened and then expecting that probably when I did this in the past, the reaction of the person was good or not good.”

References on slide:

- Atance & O’Neill (2001), “Episodic future thinking,” Trends in Cognitive Sciences
- Schacter & Addis (2007), “The cognitive neuroscience of constructive memory,” Phil. Trans. Royal Society B

**Metacognition:**
Aly: “What is the difference when I say meta? … So why did you reason?… you think about the reasoning that you have reasoned and why did you reason in that way? Okay, two times thinking.”

He distinguished cognition (connecting building blocks) from metacognition (the layer above – reflecting on why you made the cognitive decisions you did).

### 3.5 Detailed Definition of Cognitive Robotics (Slide 18)

Source: Sandini, G., Sciutti, A., and Vernon, D. (2021) “Cognitive Robotics.” In Encyclopedia of Robotics. Springer.

Key elements of the detailed definition:

- Word “cognition” from Latin *cognosco* = *con* (related to) + *gnosco* (to know)
- Cognitive robotics = branch where **knowledge** plays central role in supporting action selection, execution, and understanding
- Robots that can: learn from experience and from others, commit knowledge to memory, retrieve as context requires, flexibly use knowledge for goal pursuit while anticipating outcomes
- Can reason about own actions and actions of interaction partners, modify behaviour for long-term effectiveness
- “In short, cognitive robots are capable of flexible, context-sensitive action, knowing what they are doing and why they are doing it.”

Key names mentioned: Sandini (IIT – the institute that created iCub), Sciutti (IIT), Vernon (Carnegie Mellon).

### 3.6 How Do Cognitive Robots Work? (Slides 20-29)

**Operational Cycle (Slide 20):**
Cognitive robots achieve goals by: Perceiving -> Paying attention -> Anticipating -> Planning -> Anticipating outcome during execution -> Learning from interaction -> Adapting to change.

**Perception (Slide 21):**
Uses many sensory modalities: vision, audition, haptic (tactile and kinesthetic).

Aly’s extended example on haptic and cognitive representation: “even I close my eye, what is the tissue… of this object… I can build some kind of cognitive representation without vision… I can feel that there is a chair here… I can build cognitive representation for what I feel… without having vision.” He then noted that people who are blind have difficulty creating certain cognitive representations because “the ability to update the cognitive representation is not the same.”

**Attention (Slide 22):**
Three types (Kotseruba and Tsotsos, 2020):

- **Selective**: selecting a given feature or object
- **Restrictive**: restricting what to look for or where to look for it
- **Suppressive**: suppressing features, objects, or locations deemed not relevant

Aly’s example of restrictive attention: “I will look for example for reaction of students to what I’m teaching… and I will try to make this for the UG group, not the… postgraduate.”

**Anticipation/Prospection (Slide 23):**
Also referred to as prospection. Associated with achieving a goal. Four modes of operation: simulation, prediction, intention, planning. (Szpunar et al., 2014)

**Planning (Slide 24):**
Affected by reasoning about current state of world or anticipated future states. Exploits **episodic memory** (past experience) and **semantic memory** (knowledge of the world).

Aly explicitly flagged: “please distinguish or remember these two because we will see these two memories in many of the cognitive architectures models that we will be highlighting.”

- **Episodic memory**: “exploits memories of past experience. If you’re thinking about the past and you’d like to exploit the experiences, what happened? What was the context?”
- **Semantic memory**: “knowledge about the world… the spatial relationship between objects… they are beside each other… part of the spatial mapping or spatial concept”

Cognitive architectures “try to find the representation, suitable representation for each building block” and propose “how can it communicate the information with other… components.”

**Anticipating Outcomes (Slide 25):**
Can refer to actions of the robot itself OR actions of other agents (people and other robots).

**Agent** = robot or human. Aly tested students: “When I say agent, what do I mean by agent? … Agent means robot or human.” He referenced the HAI (Human-Agent Interaction) conference.

**Learning (Slide 26):**
Learning from actions means future actions can be more effective or efficient. Often based on reasoning. Sometimes referred to as metacognition or meta-reasoning (focus on improving the cognitive/reasoning process itself).

**Adapting (Slide 27):**
Adaptation through learning produces a **new** action policy rather than an **improved** action policy. This is a subtle but important distinction.

**Summary Slide (28):**
“Cognition is the process by which an autonomous system perceives its environment, learns from experience, anticipates the outcome of events, acts to pursue goals, and adapts to changing circumstances.” Orchestrating all this requires a **cognitive architecture**.

**Prospection and Theory of Mind (Slide 29):**

- Key feature: prospection to augment immediate sensory-motor experience
- Cognitive robots carry out tasks by anticipating effects of own actions AND actions of people around them
- **Theory of mind**: “being able to view the world from another person’s perspective, a cognitive robot can anticipate that person’s intended actions and needs”
- Applies to both **direct interaction** (assisting customer in supermarket) and **indirect interaction** (robot stacking shelves while customers shop)

Aly on theory of mind: “I’m speaking to you and you’re saying I will do this… And from what you’re saying, I can anticipate that you aim to do this or do that at the end… try to put myself in your place. And from that I try to infer your goals.”

### 3.7 Embodied Cognition and Final Thought (Slide 30)

Two reasons people study cognitive robotics:

1. They want to build smart robots
1. They want to understand cognition -> **Embodied Cognition**

Aly: “intelligence means body… if we are building our own intelligence through our… abilities to touch and interact with the environment, the robot should have this capability to sense, to be able to create knowledge.”

On using robots to model cognition: “people in psychology can put theories, if you’d like to see or to model these theories… experimentally. You need a robot… you can observe, but you cannot enter inside the child. However, with a robot, you can see how, for example, through developmental interaction, how a robot… can sophisticate an action.”

-----

## 4. LECTURER’S LEXICON

|Term                        |Aly’s Definition/Usage                                                                                      |Context                               |
|----------------------------|------------------------------------------------------------------------------------------------------------|--------------------------------------|
|**Cognitive robotics**      |Intersection of Robotics, AI, and Cognitive & Biological Sciences                                           |Core lecture topic                    |
|**Sensorimotor behaviour**  |“behavior that’s related to sensors and the motors… I observe something from my sensor and I make an action”|Building block                        |
|**Prospection**             |Anticipating the outcome of actions; not depending only on sensory-motor information                        |Key differentiator of cognitive robots|
|**Episodic memory**         |Memories of past experience – what happened, what was the context                                           |Appears in cognitive architectures    |
|**Semantic memory**         |Knowledge about the world – spatial relationships, facts                                                    |Appears in cognitive architectures    |
|**Metacognition**           |“reasoning behind the reasoning” – reflecting on why you reasoned a certain way                             |Higher cognitive function             |
|**Episodic future thinking**|Past events reconstructed to allow agent to pre-experience the future                                       |Under prospection umbrella            |
|**Cognitive architecture**  |System that puts all building blocks together and supports communication between them                       |Orchestrating framework               |
|**Agent**                   |Robot or human (technical term in HRI)                                                                      |Standard terminology                  |
|**Goal-directed action**    |Action aimed at achieving a specific goal (vs. metaphoric gesture)                                          |Cognitive robot characteristic        |
|**Affordances learning**    |Learning how to interact with objects based on their properties (e.g. how to grasp)                         |Advanced cognitive behaviour          |
|**Embodied cognition**      |Intelligence requires a body; cognition is shaped by physical interaction with environment                  |Aly’s core belief                     |
|**Theory of mind**          |Ability to view world from another’s perspective, infer their goals                                         |High-level cognitive function         |
|**Self-awareness**          |Being aware of yourself, your emotions, your intents                                                        |Advanced definition of cognition      |
|**Suppressive attention**   |Ignoring irrelevant stimuli                                                                                 |Attention type                        |
|**Restrictive attention**   |Limiting where or what to look at                                                                           |Attention type                        |
|**Selective attention**     |Choosing specific features or objects to attend to                                                          |Attention type                        |

-----

## 5. COURSEWORK SUCCESS BLUEPRINT

### Task 3: Literature Review – How to Leverage Lecture 9

Your essay on assistive robotics should use cognitive robotics as a **framing device**:

1. **Introduction**: Frame assistive robotics as requiring cognitive capabilities for genuine effectiveness. Use Aly’s hierarchy: cognitive intelligence deployed over the social layer.
1. **Literature review**: Cite Cangelosi & Asada’s definition. Reference the core cognitive abilities as requirements for assistive robots. Use Vernon (2014) for the cognition cycle.
1. **Applications**: For each assistive application, identify which cognitive building blocks are required (e.g., medication reminders need episodic memory + prospection + theory of mind).
1. **Discussion/Challenges**: Frame challenges through the lens of what cognitive capabilities are still missing – e.g., most assistive robots lack genuine prospection, theory of mind, or metacognition. Reference the 42-definitions problem to argue the field still lacks consensus on what cognition even *is*.
1. **Ethical issues**: Connect to embodied cognition – if intelligence requires a body, what are the implications of assistive robots entering intimate spaces?

### Task 4: Programming Project – How to Leverage Lecture 9

Your project should be explicitly framed as a **cognitive robotics** project. The POMDP system from your set exercises already implements several cognitive building blocks – make this mapping explicit:

- Belief state update = **episodic memory** (learning from past interactions)
- POMDP planning = **prospection** (anticipating outcomes before acting)
- Trust inference = **theory of mind** (inferring the user’s latent mental state)
- Observation processing via OpenAI API = **perception** (multimodal sensory processing)
- Action selection via policy = **action selection** (goal-directed)
- Belief-based filtering of irrelevant observations = **attention** (suppressive/selective)
- Policy evaluation/improvement = **metacognition** (reasoning about the reasoning process)

-----

## 6. HIDDEN CURRICULUM EXTRACTION

### Aly’s Research Identity

- He did his PhD in Social Robotics, then deliberately moved to cognitive/developmental robotics for his postdoc in Japan. He views this as an upgrade in sophistication. A project that operates at the cognitive level will resonate with his personal trajectory.
- He was at a lab with iCub (“in my lab, most of you have seen it”).
- His interest is in **understanding cognition through robots** (embodied cognition approach), not just building useful robots.
- He references developmental robotics frequently – how infants develop language, motor skills, etc. – suggesting he values bio-inspired, developmental approaches.

### Pet Topics

- **Embodied cognition**: “I was always saying that intelligence means body”
- **Cognitive architectures**: Will be covered in upcoming lectures; he clearly values systematic, structured approaches to building cognitive systems
- **Prospection**: Repeatedly emphasised as the key differentiator
- **Developmental robotics**: References to infant development, language acquisition, Cangelosi & Schlesinger

### Philosophical Position

- Cognition > social behaviour (explicit hierarchy)
- Understanding cognition through robotics (not just engineering utility)
- Bio-inspired approaches valued over purely engineering approaches
- Formal definitions and building blocks matter – he spent significant time on definitional rigour

-----

## 7. KEY REFERENCES FROM THIS LECTURE

- Murphy, R. R. (2019) *Introduction to AI Robotics*. Cambridge, MA: MIT Press.
- Cangelosi, A. and Asada, M. (in press) *Cognitive Robotics*, Chapter 1. MIT Press.
- Cangelosi, A. and Schlesinger, M. (2015) *Developmental Robotics: From Babies to Robots*. MIT Press.
- Vernon, D. (2014) *Artificial Cognitive Systems – A Primer*. MIT Press.
- Sandini, G., Sciutti, A. and Vernon, D. (2021) “Cognitive Robotics.” In Ang, M., Khatib, O. and Siciliano, B. (Eds.), *Encyclopedia of Robotics*. Springer.
- Pfeifer, R. and Bongard, J. (2007) *How the Body Shapes the Way We Think*. MIT Press.
- Atance, C. M. and O’Neill, D. K. (2001) “Episodic future thinking,” *Trends in Cognitive Sciences*, 5(12), pp. 533-539.
- Schacter, D. L. and Addis, D. R. (2007) “The cognitive neuroscience of constructive memory,” *Phil. Trans. Royal Society B*, 362, pp. 773-786.
- Kotseruba, I. and Tsotsos, J. K. (2020) [Reference for attention types – selective, restrictive, suppressive]
- Szpunar, K. K. et al. (2014) [Reference for four modes of anticipation – simulation, prediction, intention, planning]
- Walter, W. G. (1953) *The Living Brain*.

-----

## 8. INTEGRATING COGNITIVE ROBOTICS INTO YOUR ASSESSMENT 2 PROJECT

### The Strategic Opportunity

Aly said nobody has ever done a cognitive robotics project before. He described this as “invitation for challenging minds.” Your existing POMDP-based medication adherence assistant from the set exercises is already operating at the cognitive level – you just need to **reframe and extend it** using the vocabulary and architecture from this lecture. This is where you differentiate yourself from every other student who will do a purely social robotics project.

### Your Existing System Already Maps to Cognitive Building Blocks

Here is how your set exercises POMDP model maps to the cognitive architecture building blocks Aly presented:

|Cognitive Building Block|Your System Component                                                       |How to Strengthen                                                                                                                                                                                                                    |
|------------------------|----------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|**Perception**          |OpenAI API processing facial AUs, prosodic features, gestures               |Frame as multimodal cognitive perception (vision + audition + haptic from tactile sensors)                                                                                                                                           |
|**Attention**           |Observation filtering – the API focuses on relevant behavioural cues        |Explicitly implement suppressive/selective attention: e.g., ignore irrelevant environmental noise, focus on medication-relevant user behaviours                                                                                      |
|**Action Selection**    |POMDP policy $\pi^*(b)$ selecting from action space                         |Already goal-directed. Frame as satisfying the “flexible context-sensitive goal-directed action” criterion                                                                                                                           |
|**Memory (Episodic)**   |Belief state $b(s)$ carries forward history of interactions                 |Extend: store specific past interaction episodes (e.g., “last Tuesday, user refused medication after verbal remind but accepted after explain_benefits”)                                                                             |
|**Memory (Semantic)**   |Knowledge of medication schedules, user profile, cultural parameters        |Extend: add spatial/contextual knowledge (user’s routine, room layout, time-of-day patterns)                                                                                                                                         |
|**Learning**            |Belief update via Bayesian filtering                                        |Extend: could add simple policy learning – adapting transition probabilities based on accumulated experience                                                                                                                         |
|**Reasoning**           |POMDP planning over belief space                                            |Frame as “reasoning about current state of the world or anticipated future states” (Aly’s exact words for planning)                                                                                                                  |
|**Metacognition**       |*Currently missing*                                                         |**ADD THIS**: Have the system evaluate *why* a particular action was selected and whether the reasoning was sound. E.g., if trust degrades after three consecutive Explain_Benefits, the metacognitive layer triggers a policy review|
|**Prospection**         |POMDP inherently anticipates outcomes – it plans over expected future states|Make this explicit in your report. The POMDP’s value function is literally prospection: computing expected future reward                                                                                                             |
|**Theory of Mind**      |Inferring user’s trust and cognitive load from observations                 |Frame explicitly as theory of mind: “the robot infers the user’s latent mental state to anticipate their needs”                                                                                                                      |

### Concrete Extension: Adding a Cognitive Architecture Layer

Your set exercises model had the POMDP + OpenAI API. For the report project, wrap this in an explicit **cognitive architecture** that Aly can recognise:

```
COGNITIVE ARCHITECTURE
|
|-- PERCEPTION MODULE (OpenAI API: multimodal observation extraction)
|   |-- Vision: facial action units, gaze direction
|   |-- Audition: prosodic features, speech content
|   |-- Haptic: tactile sensor data (if user touches robot)
|
|-- ATTENTION MODULE (Observation filtering)
|   |-- Selective: focus on medication-relevant behaviours
|   |-- Suppressive: ignore environmental distractors
|
|-- MEMORY SYSTEM
|   |-- Episodic Memory: past interaction outcomes stored as (state, action, observation, reward) tuples
|   |-- Semantic Memory: user profile, medication schedule, cultural parameters, spatial context
|
|-- REASONING/PLANNING MODULE (POMDP solver)
|   |-- Belief state b(s) maintained via Bayesian update
|   |-- Policy pi*(b) computed via value iteration or point-based solver
|   |-- Prospection: forward simulation of expected outcomes
|
|-- ACTION EXECUTION MODULE
|   |-- Abstract action -> OpenAI API -> culturally-calibrated language/gesture
|   |-- Goal-directed: each action targets medication adherence
|
|-- METACOGNITION MODULE [NEW]
|   |-- Monitors reasoning performance (e.g., tracks if belief updates are leading to improved outcomes)
|   |-- Triggers policy review if repeated actions produce negative outcomes
|   |-- Logs "reasoning about the reasoning" for self-improvement
|
|-- THEORY OF MIND MODULE
|   |-- Infers user's trust level and cognitive load
|   |-- Anticipates user's intended actions and needs
|   |-- Enables perspective-taking for proactive assistance
```

### How to Frame This in the Report

Your 2,000-word report for Task 4 should:

1. **Introduction (10%)**: Position the project as a cognitive robotics approach to assistive medication adherence. Cite Cangelosi & Asada’s definition. State that most assistive robots operate at the social layer; your system deploys cognitive intelligence *over* the social layer (Aly’s hierarchy). This framing alone distinguishes your work.
1. **Background (10%)**: Briefly cover: cognitive robotics building blocks (perception through prospection – cite Vernon 2014), POMDPs as a planning mechanism for cognitive agents, and the neuro-symbolic paradigm (LLM perception + POMDP reasoning).
1. **Method and Setup (35%)**: This is the bulk. Present your cognitive architecture diagram. For each module, explain: (a) what cognitive building block it implements, (b) how it’s implemented technically, (c) why it’s necessary for the assistive task. Include formal POMDP specification. Show code architecture. The key differentiator from your set exercises is: you’re now *building and demonstrating it*, not just specifying it.
1. **Results/Outcome/System Analysis (30%)**: Run the system (even in simulation). Show belief state evolution over interaction episodes. Demonstrate how prospection improves action selection vs. a reactive baseline. Show metacognition detecting suboptimal reasoning patterns.
1. **Conclusion (10%)**: Reflect on which cognitive building blocks were most effective, which were hardest to implement, and what would be needed for genuine embodied cognition (connecting to Aly’s core belief).

### Scoping Advice (Don’t Shoot Yourself in the Foot)

Aly warned: “we… bear in mind also the time constraints.” Your POMDP model from the set exercises is already complex. For the project:

- **Do**: Implement a working simulation (even without a physical robot – but get approval). A Python simulation with a simple GUI showing the robot’s belief state, action selection, and user response would be sufficient.
- **Do**: Frame everything in cognitive robotics terminology from this lecture.
- **Do**: Add the metacognition layer – it’s novel, directly from this lecture, and relatively simple to implement (a monitoring function that tracks action-outcome patterns and flags when the policy is underperforming).
- **Do**: Include episodic memory – store past interactions and show how they influence future decisions.
- **Don’t**: Try to implement full affordances learning, developmental learning, or language acquisition. These are too ambitious for the timeframe.
- **Don’t**: Forget the 5-minute video requirement. Plan your demo around showing the cognitive architecture in action, walking through a scenario where the robot perceives, attends, reasons, acts, learns, and adapts.

### Connecting to Your Set Exercises

Your set exercises already established the POMDP formalism, the neuro-symbolic architecture, and the medication adherence scenario. The report project should be framed as the **implementation and extension** of that theoretical model, now explicitly situated within a cognitive robotics architecture. Key additions:

- Explicit cognitive architecture wrapping the POMDP
- Working code (simulation)
- Metacognition module (new from Lecture 9)
- Episodic/semantic memory distinction (new from Lecture 9)
- Framing in embodied cognition terms (new from Lecture 9)
- Theory of mind labelling (reinforced from Lecture 9)
- Prospection terminology applied to POMDP planning (new from Lecture 9)

### What to Discuss with Aly for Approval

Before committing, you need to speak to Aly about:

1. Whether a simulation-based project (without physical robot) is acceptable
1. Whether extending the POMDP model from your set exercises into a full cognitive architecture implementation is considered sufficiently novel for the project
1. Whether using the Neo/Pepper platform in simulation (e.g., via Webots or Choregraphe) would satisfy the embodiment requirement
1. The scope – is the cognitive architecture + POMDP + metacognition enough, or does he expect more?

-----

## 9. WARNINGS AND PITFALLS REGISTER

- **Don’t conflate social and cognitive robotics**: Aly views them as distinct levels. Social is the outer layer; cognitive is the inner intelligence. Your project should clearly distinguish which level it operates at.
- **Don’t skip the definitional rigour**: Aly spent nearly half the lecture on definitions. Your report should define cognitive robotics, cognition, and your key terms precisely.
- **Don’t assume the reader knows the basics**: The assessment criteria state this. Define everything.
- **Transcription note**: “Kangalusi” / “Kangaroosi” in the transcript = **Cangelosi** (Angelo Cangelosi). The transcript also has “Shaky” = **Shakey**. Attribute correctly.
- **Don’t present cognitive robotics as solved**: Aly emphasised there are 42 definitions and “still we find a lot of challenges like social robotics.” Your discussion should acknowledge ongoing challenges.

-----

## 10. META-LEARNING: WHAT’S COMING NEXT

Aly stated: “we will be next time speaking about different parts related to cognitive” and “you will see in all the systems that we will discuss in the next two lectures.” This means:

- **Upcoming lectures will cover specific cognitive architectures** – these will be directly relevant to your project. Wait for these before finalising your architecture design.
- The building blocks from this lecture (perception, attention, memory, learning, reasoning, metacognition, prospection) will reappear as components of actual architectures.
- Expect to see episodic and semantic memory implementations in real cognitive architectures.

-----

*Final step: Cross-check this extraction with Gemini for critique and gap identification.*