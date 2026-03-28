# COMP3018 Lecture 11: Cognitive Architectures – BRITISH AI Intelligence Extraction

**Lecturer:** Dr. Amir Aly
**Module:** COMP3018 Human-Robot Interaction
**Date extracted:** 27 March 2026
**Assessment alignment:** Assessment 2 (70%) – Task 3 (Literature Review, 40%) & Task 4 (Programming Project, 60%)

-----

## 1. CRITICAL ASSESSMENT INTELLIGENCE

### Direct Coursework Alignment

#### Task 4 (Programming Project – CRAMS) – PRIMARY TARGET OF THIS LECTURE

This lecture is **foundational architecture knowledge** for your CRAMS project. Dr. Aly is explicitly laying out the cognitive framework vocabulary and structure that your project must demonstrate awareness of.

- **Your CRAMS architecture maps directly onto the cognitivist paradigm.** Your POMDP with fixed rules + knowledge (medication adherence domain) = Cognitive Architecture + Knowledge = Cognitive Model. Dr. Aly literally gave this equation: “Cognitive architecture plus knowledge means cognitive model. This means cognitive architecture is a framework. You bring your knowledge and put it inside the cognitive architecture.”
- **The Lehman (1998) BEHAVIOR = ARCHITECTURE x CONTENT formulation is critical for your report.** Dr. Aly spent significant time explaining why multiplication (not addition) matters: “The behavior of function to move the chess is not depending separately on architecture, on the rules and separately on the position on the board, but on both together. When you have this kind of relationship, both together and not separately, you use the multiplication.” – Your CRAMS report should frame POMDP belief state as the “content” and POMDP transition/observation/reward matrices as the “architecture,” and argue that behaviour emerges from their interaction (multiplication), not from either alone.
- **All 8 core cognitive abilities are your design vocabulary.** Dr. Aly listed: Perception, Attention, Action Selection, Memory, Learning, Reasoning, Meta-reasoning, Prospection. Your CRAMS project should explicitly map its components to these abilities in the report.
- **Prospection is Dr. Aly’s pet topic and is NOT in the main reference paper.** He noted: “The prospection is not included in this reference, unfortunately.” This means if you include prospection in your CRAMS design (which you already do via POMDP belief-based future simulation), you demonstrate knowledge BEYOND the standard literature – exactly what gets 70%+ marks.
- **Dr. Aly explicitly flagged the difficulty of prospection for robots:** “Do you understand how difficult it is just a simple thing like this. How can robots simulate an event and think about your reaction and for example, predicting potential outcomes. So that should the robot go this way or not go this way?” – Your CRAMS project literally does this via POMDP belief updates and action selection. Frame it as computational prospection in your report.
- **Theory of Mind connection:** “Theory of mind in general is like… it can understand, for example, human emotion by inferring them from facial expressions or from speech… I inferred your intent.” – Your CRAMS system infers patient internal state (compliant/hesitant/refusing) from observations. This IS computational Theory of Mind. Use this terminology.

#### Task 3 (Literature Review – Assistive Robotics)

- **Cognitive architectures provide the theoretical backbone for assistive robots.** When writing about assistive robotics, you can discuss how cognitive architectures enable robots to adapt to patient needs over time, which connects to the “develop autonomously so that the performance improves over time” requirement Dr. Aly emphasised.
- **The emergent vs. cognitivist distinction matters for assistive robotics discussion.** Assistive robots that need to adapt to individual patients over long-term use lean toward emergent/hybrid architectures. This is a sophisticated point for your literature review.
- **Transfer learning example is directly relevant:** “Like for example, transfer learning… for X disorder or X disease, I don’t need to have a lot of data to be able to diagnose or detect it.” – Cite this as a challenge/opportunity in assistive robotics: limited clinical data per condition can be overcome via transfer learning.

### Implicit Marking Scheme Signals

- Dr. Aly values students who can **connect concepts across the module**: “Now we are at the end of the module, so you probably had… We spoke about the word context before.” He expects you to weave earlier lecture material (FACS, emotion recognition, speech analysis) into your cognitive architecture discussion.
- He explicitly tested whether students remembered **FACS (Facial Action Coding System)** from earlier lectures: “Can you remind me the name that studies the actions of the face that can encode emotions?” – This signals he expects cross-referencing in assessments.
- **Conceptual understanding over mathematical rigour** (confirmed from earlier extraction): He used the chess analogy, the orange/symbol grounding analogy, the child development analogy – all to build intuition. Your report should demonstrate this kind of intuitive understanding.

-----

## 2. THE COMPLETE ALPHA BRIEF

### Triple Star (Highest Priority for Coursework)

- ***“Cognitive architecture plus knowledge means cognitive model.”*** – Use this exact framing for your CRAMS report. Your POMDP structure = architecture; medication adherence domain knowledge = knowledge; the running system = cognitive model. (Repeated/emphasised across multiple slides)
- ***BEHAVIOR = ARCHITECTURE x CONTENT (Lehman et al. 1998)*** – “The effect of the architecture on behavior is not simply additive to the effect of the content.” Frame your CRAMS action selection as multiplicative interaction between POMDP structure and current belief state. Dr. Aly spent ~5 minutes on the chess analogy to drive this home.
- ***8 Core Cognitive Abilities:*** Perception, Attention, Action Selection, Memory, Learning, Reasoning, Meta-reasoning, Prospection. Your CRAMS report MUST map its components to these. Reference: Kotseruba and Tsotsos (2020) “40 years of cognitive architectures” – Dr. Aly called this “one of the very, very important papers.”
- ***Prospection = your CRAMS differentiator.*** “Prospection is like simulating future scenario. You’re predicting the goal.” Your POMDP belief update literally does this. Dr. Aly noted it is NOT covered in Kotseruba and Tsotsos (2020), so demonstrating it shows independent thinking.
- ***Three paradigms of cognitive architecture:*** Cognitivist, Emergent, Hybrid. Know which your CRAMS falls into (cognitivist/hybrid) and justify why in your report.

### Double Star (High Priority)

- **Theory of Mind connection to prospection:** “Theory of mind… it can understand, for example, human emotion by inferring them from facial expressions or from speech… I inferred your intent.” Your CRAMS perception module (OpenAI API reading user state) implements computational Theory of Mind.
- **Emergent approach – Dr. Aly’s personal research preference:** “For the emergence, which I personally like a lot, that’s focused on development.” His PhD student is working on language development through environmental interaction. If you can frame any learning/adaptation element of CRAMS as having emergent properties, this aligns with his research interests.
- **Memory types taxonomy (from GMU BICA architecture):** Episodic memory (long-term, stores past episodes), Semantic memory (knowledge, facts, concepts), Procedural memory (sensory/motor information), Working memory (short-term, decision-making), Cognitive map (spatial reasoning, planning, navigation). Map your CRAMS memory component to this taxonomy.
- **Piaget vs. Vygotsky – complementary, not opposing:** Individual development vs. social development. Dr. Aly stressed: “I’m not telling you try to choose… they are not opponents… they are complementary.” This matters for Task 3 if discussing how assistive robots learn/adapt.
- **Symbol grounding problem:** Dr. Aly explained at length how symbols gain meaning through connection to real-world percepts. GOFAI = “Good Old Fashioned Artificial Intelligence” = symbolic AI. Relevant context for understanding cognitive architecture history.

### Single Star (Notable)

- **Cognitive architectures are frameworks, not plug-and-play:** “It is just something like a framework you download from anywhere. It’s not something that’s plug and play. You have to give it knowledge about what you need to do.”
- **Developmental aspect:** “When we speak about cognitive agents, cognitive architecture should also be able to develop autonomously so that the performance improves over time.” Consider whether CRAMS has any developmental capacity.
- **Context understanding requires multimodal perception:** Dr. Aly walked through how a robot in the classroom would collect visual data (facial expressions, mouth open = laughing), audio data (voices), static images (objects), dynamic video (people moving) to understand context.
- **ACT-R mentioned as example cognitive architecture** – one of the most famous existing frameworks. Worth mentioning in your report as a comparison point.
- **Dozens of cognitive architectures exist:** “Too many. Too many tens and tens and tens of cognitive architectures. Certainly the more famous you’ll be, the more tasks you can work independently.”
- **Next lecture (Lecture 12) will cover more practicalities about specific cognitive architectures** and then transition to coursework support.

-----

## 3. EXHAUSTIVE TOPIC BREAKDOWN

### 3.1 What is a Cognitive Agent?

**Slide definition:** “The chief characteristic of a cognitive agent is the ability to act effectively in a world that is uncertain, under-specified, dynamic, possibly cooperating with other cognitive agents.”

**Lecturer expansion:** “To achieve goals adaptively and robustly in these circumstances, we require complex system. It’s complex system that can construct model of the way the world works, use them to guide actions prospectively and update them dynamically.”

**Three requirements of the complex system (from slide 3):**

1. Construct models of the way the world works
1. Use them to guide actions prospectively
1. Update them dynamically as the system continually learns through its interactions

**CRAMS mapping:** Your POMDP belief state = constructed model; action selection policy = guiding actions prospectively; belief updates from observations = dynamic updating through interaction.

### 3.2 What is a Cognitive Architecture?

**Slide definition:** “A cognitive architecture is a software framework that integrates all the elements required for a system to exhibit characteristic attributes of a cognitive agent.”

**Lecturer expansion:** “To design a cognitive architecture requires the specification of the formalism for all processes and knowledge representation used by… So you need to understand the formalism of all processes.”

**Key analogy (repeated):** “It is just something like a framework you download from anywhere. It’s not something that’s plug and play. You have to give it knowledge about what you need to do.”

**Dr. Aly’s emphasis on understanding formalism:** “If I say I will use ACT-R… I have to understand how it is used, which language it is, all the formalism, the structure, the rules… so that I can use to update them with my own rules and give it my knowledge.”

### 3.3 How Does a Cognitive Architecture Work?

**Core cognitive abilities (slide 5):** Perception, Attention, Action Selection, Memory, Learning, Reasoning, Meta-reasoning, Prospection.

**Key properties:**

- Integrates core cognitive abilities so they can be **dynamically coordinated**
- Allows agents to exhibit **flexible context-sensitive behaviour**
- **Prospectively selecting and controlling** actions required to achieve goals
- Should be able to **develop autonomously** so performance improves over time with experience

**Lecturer on context-sensitivity:** “Flexible context sensitive means like understanding the context. How do you understand the context?” – Then he walked through a classroom scenario where the robot collects visual, auditory, and environmental signals to build context understanding.

**FACS callback:** “When I say about, for example, understand the facial expressions, I was saying there is a specific coding for this… Facial Action Coding System. So the FACS coding tells you what units of the face moves for humans.” – He tested students on this and they struggled to remember it. Signal: he expects cross-referencing of earlier material.

### 3.4 Three Paradigms of Cognitive Architecture

**Slide 6 diagram:** Cognitive Science branches into Cognitivist Systems, Hybrid Systems, Emergent Systems.

#### 3.4.1 Cognitivist Cognitive Architecture

**Definition:** Attempts to create Unified Theories of Cognition (UTC).

**Why “unified theories” (plural)?** Dr. Aly: “There are actually unified theories of cognition… theories, because we understand that there are a lot of theories related to attention, related to memory, problem solving, decision making, learning. A lot of theories exist. And unified because… the most famous, the less disputed.”

**Key properties (slide 8, Ritter and Young 2001):**

- Encapsulation of scientific hypothesis about aspects of human cognition that are:
  - **Relatively constant over time** (not emergent/developmental)
  - **Relatively independent of task** (general-purpose framework)

**Lecturer clarification:** “It’s not something that depends on emergence, it’s not something that depend on absolute development… don’t expect it to have it like, for example, to develop similar to a child growing up from age 2 to age 10. But it have some kind of basic building blocks that are relatively constant over time.”

**The key equation (slide 9):**

```
Cognitive Architecture + Knowledge = Cognitive Model
```

**Lehman et al. (1998) alternative:**

```
BEHAVIOR = ARCHITECTURE x CONTENT
```

**Lecturer’s chess analogy for multiplication vs. addition:** “This architecture is a rule about the chess game, chess engine, and the content is about the board position… the behavior here is not separately depend… on the rules and separately on the position on the board, but on both together. When you have this kind of relationship, both together and not separately, you use the multiplication.”

**Knowledge is typically:**

- Determined by the designer (explicitly or implicitly)
- Adapted and augmented by machine learning techniques

**Transfer learning example:** “Like ping pong and tennis. You don’t need to have a lot of information about ping pong… if I have a lot of information about tennis, I train the system of tennis. And if I have very tiny amount of information about ping pong, I just refine the trained system.”

**Overall structure of a cognitivist system (slide 11, GMU BICA Architecture, Samsonovich 2010):**

- Essential modules
- Essential relations between modules
- Essential algorithmic and representational details in each module

**Memory types in the GMU BICA Architecture:**

- **Episodic memory:** Long-term; encodes, stores, and retrieves specific episodes of the agent’s past experiences. Dr. Aly: “Very important memory for human-robot interaction, is very good for the prospection of the future.”
- **Semantic memory:** Knowledge, facts, and concepts. “Like a shelf. You put knowledge on the shelf, you encode them, you give them a code, you put them on the shelf in your brain and they get your knowledge back from the shelf.”
- **Procedural memory:** Sensory information.
- **Working memory:** Short-term; used in tasks like decision-making.
- **Cognitive map:** Models spatial reasoning, planning, and navigation.

**Lecturer emphasis:** “You will see or should see in our next lecture. Memory is kind of memories, semantic, episodic… These are the very, very, very basic building blocks.” (Triple “very” = strong emphasis)

#### 3.4.2 Emergent Cognitive Architecture

**Focus:** Development – from primitive state to fully cognitive state, over the system’s lifetime.

**Two views of development:**

1. **Individual (Piaget):** Personal experience, biological maturation, touching/interacting with environment
1. **Social (Vygotsky):** Social factors shape cognitive development; children learn from each other

**Lecturer emphasis:** “I’m not telling you try to choose… they are not opponents, but they are complementary.”

**Baby/cup analogy:** “If you give a baby a cup with a handle, certainly the baby will try and figure out beginning touch the cup, but at some point it will be able to put the hand around the handle, inside the handle, for example, and catch it better.”

**Dr. Aly’s personal research connection:** “For the emergence, which I personally like a lot… how you have very basic level of knowledge and how this emerges to having higher level of knowledge.” His PhD student works on children learning word meanings through environmental interaction, then learning grammar. “Can we have this capability in the robot?”

**Phylogenetic configuration:**

- Basis for ontogenesis (growth and development)
- Innate skills and core knowledge (cf. E. Spelke)
- Structure to embed: Perception, Action, Adaptation, Anticipation, Motivation… and development of all these

**Innate skills example – language faculty:** “Children can receive… the signal. I said this is an apple. They received… what I said… What is the innate skill here is that they can cut. They can understand that there is acoustic feature here and acoustic feature here… But they don’t understand which one belongs to which words.”

**Key philosophical stance – rejects dualism and functionalism:**

- No separation between mind and body
- Physical platform and what it perceives = one system, not separate
- “It rejects dualism and functionalism. So that creates cognitive mechanisms independently of the physical. So what this means – physical platform and what it perceives, etc., is one system, not separate systems.”

#### 3.4.3 Hybrid Cognitive Architecture

**Slide 16 definition:** “Hybrid cognitive architectures aim to combine the symbolic, rule-based processing of cognitivist architectures with the parallel, distributed processing of emergent architectures.”

**Lecturer expansion:** “It takes some kind of basic, one basic thing from knowledge, for example from cognitive approach. And it tries to take also a processing architecture from the emergent and put them together.”

**Examples of hybridisation:**

- Symbolic representations for abstract concepts/rules + neural networks for flexible/adaptive behaviour
- Cognitive storage from cognitivist approach + adaptation mechanisms like reinforcement learning or evolutionary algorithms from emergent approach

**Decision framework Dr. Aly gave (for choosing paradigm):**

- “If we don’t need our robot or our knowledge to be developed, we look at cognitivist.”
- “If we’d like it to be developed, we look at emergent.”
- Then within each paradigm, there are “plenty” of specific architectures to choose from.
- Compared this to choosing RL paradigms in COMP3003: model-free vs model-based, etc.

### 3.5 Core Cognitive Abilities (Detailed Breakdown, slides 17-25)

**Key reference:** Kotseruba and Tsotsos (2020) “40 years of cognitive architectures: core cognitive abilities and practical applications.” Artificial Intelligence Review, Vol. 53, No. 1, pp. 17-94.

Dr. Aly: “This is one of the very, very important papers.”

**Note:** Prospection (#8) is NOT included in this reference. Dr. Aly adds it from other sources (Vernon 2014, von Hofsten 2009).

#### 1. Perception

- Uses many sensory modalities: vision, audition, haptic (tactile and kinesthetic)
- Transforms raw input into the system’s internal representation

#### 2. Attention

- Reduces information to process by selecting relevant and filtering irrelevant
- **Selective mechanisms:** Choose one entity from many (e.g., gaze, viewpoint)
- **Restrictive mechanisms:** Choose some entities from many; priming what/where to look
- **Suppressive mechanisms:** Suppress irrelevant features, objects, locations

**Lecturer’s gaze example:** “I will look at your gaze only because I’m interested in the gaze. I’m selected… I don’t care what you do with your hands. But I will look to your eyes.”

#### 3. Action Selection

- Determines what the agent should do next
- **Planning:** Determines sequence of steps to reach a goal prior to execution
- **Dynamic action selection:** Selection based on knowledge at the time, typically using winner-take-all, probabilistic, or pre-defined order selection mechanisms

#### 4. Memory (Kotseruba and Tsotsos identify six types)

- **Short-term sensory memory:** Recent percepts
- **Short-term working memory:** Information relevant to current task
- **Long-term episodic memory:** Key to anticipation; autobiographical
- **Long-term semantic memory:** General knowledge about the world
- **Long-term procedural memory:** Motor skills
- **Long-term global memory:** For architectures that don’t draw a type-duration distinction

**Lecturer on memory and CRAMS relevance:** “If you are having a robot and you’d like to create cognitive architecture more systematic… which knowledge to put in which memory. That’s what you need to do.”

#### 5. Learning

- Ability to improve performance over time through acquisition of knowledge or skill
- **Declarative learning:** Explicit knowledge acquisition (supervised, unsupervised, reinforcement learning)
- **Non-declarative learning:** Perceptual, procedural, associative, non-associative learning

**Examples given by Dr. Aly:**

- Declarative: “If the goal is to travel, and you’re in a car, then press the gas pedal”
- Non-declarative: “Learning to ride a bike, developing motor skills for a sport, or learning to associate a certain smell with a particular emotion”

#### 6. Reasoning

- Ability to logically and systematically process knowledge to infer conclusions
- Focuses on practical objective of finding the **next best action to perform**
- Three classical forms: **deduction, induction, abduction**

**Abduction:** Best possible explanation for observations (water on floor -> water was spilled)
**Deduction:** Conclusion from premises (all cats are mammals + Fluffy is a cat -> Fluffy is a mammal)
**Induction:** Generalisation from specific instances (every cat I’ve seen is black and white -> all cats are black and white – may not be true)

#### 7. Metacognition

- Ability to **monitor** internal cognitive processes, **reason about** them, and **adapt** them
- Needed for social cognition / Theory of Mind / perspective-taking
- “The ability to infer the cognitive states of other agents with which it is interacting”

**Lecturer’s exam analogy:** “In an exam you say ah, why did I make answer A but I could have made answer B and start blaming yourself. So we always just do this. Metacognition… unconsciously.”

#### 8. Prospection (NOT in Kotseruba and Tsotsos 2020)

- Capacity to **anticipate the future** – “one of the hallmark attributes of cognition” (Vernon 2014)
- Lies at the heart of other core characteristics: autonomy, perception, action, learning, adaptation
- Central to action since **actions are goal-directed and guided by prospective information** (von Hofsten 2009)
- **Internal simulation** plays a key role

**Lecturer’s extended emphasis:** “How can robots simulate an event and think about your reaction and for example, predicting potential outcomes… this is very difficult. Very, very difficult. How can the robot have this perspective? How can the robot be simulating this, the experience?… There is active research in this area.”

### 3.6 Symbol Grounding Problem (Extended Aside)

Dr. Aly gave an extensive explanation of the symbol grounding problem:

- **Symbol:** Any concept or representation that doesn’t have a clear reference to the world. Words are symbols.
- **Grounding:** Connecting a symbol to real-world percepts/features (shape, colour, haptic properties)
- **GOFAI:** “Good Old Fashioned Artificial Intelligence” – symbolic AI based on symbol manipulation and building connections between symbols

**Orange analogy (extended):** A newborn agent hears “this is an orange” – receives acoustic signal, can segment it (innate skill), but doesn’t know what the words mean. They are symbols. Through interaction with the real-world object (circular, orange colour, specific texture), the symbol gets grounded to physical features. Then the word “orange” associates with those features.

**Cross-linguistic extension:** If you already know English and encounter a Japanese word, you can open the dictionary and link the new symbol to the English word, which is already grounded.

-----

## 4. LECTURER’S LEXICON

|Term                          |Definition (Dr. Aly’s usage)                                                                  |CRAMS relevance                                                                 |
|------------------------------|----------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------|
|**Cognitive architecture**    |Software framework integrating all elements for a system to exhibit cognitive agent attributes|The theoretical framing for your entire project                                 |
|**Cognitive model**           |Cognitive architecture + domain knowledge                                                     |Your CRAMS system once POMDP is populated with medication adherence knowledge   |
|**Cognitivist**               |Fixed framework with embedded knowledge; relatively constant over time, task-independent      |Your POMDP structure with fixed matrices                                        |
|**Emergent**                  |Developmental approach; from primitive to fully cognitive through experience                  |Not your primary paradigm, but adaptation elements could qualify                |
|**Hybrid**                    |Combines symbolic (cognitivist) with parallel/distributed processing (emergent)               |If you argue CRAMS uses both POMDP rules AND LLM neural processing = hybrid     |
|**Prospection**               |Simulating future scenarios and predicting potential outcomes                                 |Your POMDP belief-based action selection IS computational prospection           |
|**Theory of Mind**            |Inferring cognitive/emotional states of other agents                                          |Your observation model (perceiving patient state) = computational ToM           |
|**FACS**                      |Facial Action Coding System – encoding facial muscle movements for emotion recognition        |Earlier lecture content; mention in context understanding discussion            |
|**Symbol grounding**          |Connecting abstract representations to real-world percepts                                    |Background knowledge for understanding symbolic vs. subsymbolic approaches      |
|**GOFAI**                     |Good Old Fashioned AI – symbolic AI approach                                                  |Historical context                                                              |
|**UTC**                       |Unified Theories of Cognition (Allen Newell)                                                  |Theoretical foundation of cognitivist architectures                             |
|**Ontogenesis**               |Growth and development of an individual system over its lifetime                              |Emergent architecture concept                                                   |
|**Phylogenetic configuration**|Innate/inherited system configuration – basis for ontogenesis                                 |What the emergent architecture starts with                                      |
|**Dualism**                   |Separation of mind and body (rejected by emergent approach)                                   |Know this to contrast with embodied cognition                                   |
|**Functionalism**             |Treating cognitive mechanisms independently of physical platform (rejected by emergent)       |Contrasts with embodied approach                                                |
|**Declarative learning**      |Explicit knowledge acquisition (supervised, unsupervised, RL)                                 |Your POMDP updates                                                              |
|**Non-declarative learning**  |Procedural, associative, perceptual learning (riding a bike, etc.)                            |Less relevant to CRAMS                                                          |
|**Abduction**                 |Reasoning to best explanation from observations                                               |Your robot observing patient behaviour and inferring internal state             |
|**Metacognition**             |Monitoring and reasoning about own cognitive processes                                        |Advanced CRAMS extension: robot reflecting on why it chose a particular strategy|

-----

## 5. COURSEWORK SUCCESS BLUEPRINT

### Task 4 (CRAMS Project) – How This Lecture Feeds Your Report

#### Introduction section (10% of task mark)

- Frame CRAMS as a cognitive architecture for medication adherence support
- Reference the definition: “A cognitive architecture is a software framework that integrates all the elements required for a system to exhibit characteristic attributes of a cognitive agent”
- State that your system operates in an “uncertain, under-specified, dynamic” environment (Dr. Aly’s exact framing of cognitive agent characteristics)

#### Background section (10% of task mark)

- Cite Kotseruba and Tsotsos (2020) as the landmark survey
- Discuss the three paradigms (cognitivist, emergent, hybrid) and justify where CRAMS sits
- Reference Lehman et al. (1998) BEHAVIOR = ARCHITECTURE x CONTENT
- Note that prospection is a hallmark attribute of cognition (Vernon 2014) not covered in the main survey

#### Method and Setup section (35% of task mark) – HIGHEST WEIGHTED

- **Map every CRAMS component to the 8 core cognitive abilities:**
  - Perception: OpenAI API vision module reading user facial expressions/behaviour
  - Attention: Selective focus on medication-relevant cues (compliance signals)
  - Action Selection: POMDP policy determining next robot action (dynamic action selection, probabilistic)
  - Memory: Belief state = working memory; POMDP model parameters = semantic memory; interaction history = episodic memory
  - Learning: Belief updates from observations (declarative learning via Bayesian updating)
  - Reasoning: POMDP reasoning over actions – abductive reasoning (observing behaviour, inferring hidden state)
  - Meta-reasoning: Could frame as the system evaluating whether its current strategy is working
  - **Prospection:** POMDP belief projection = simulating future scenarios to select best action. THIS IS YOUR DIFFERENTIATOR.
- Reference the “cognitive architecture + knowledge = cognitive model” equation explicitly

#### Results/Outcome section (30% of task mark)

- Show the system exhibits “flexible context-sensitive behaviour” – different responses to different patient states
- Demonstrate the multiplicative relationship: same architecture (POMDP) with different content (patient states) produces different behaviours
- Show prospection in action: the system anticipating likely outcomes and choosing accordingly

#### Conclusion (10% of task mark)

- Discuss whether CRAMS is purely cognitivist or has hybrid properties (OpenAI API = neural network component within a symbolic POMDP framework = arguably hybrid)
- Future work: adding developmental/emergent capabilities (learning new strategies over time)

### Task 3 (Literature Review – Assistive Robotics) – How This Lecture Adds Depth

- **Use cognitive architecture vocabulary** when discussing how assistive robots process information and adapt to users
- **Cite the memory taxonomy** when discussing how assistive robots store and retrieve patient data
- **Prospection as a key challenge:** “How can robots simulate an event and think about your reaction and predicting potential outcomes… this is very difficult” – frame this as an open research challenge in assistive robotics
- **Theory of Mind** as essential for assistive robots that need to understand patient emotional states and intentions
- **Transfer learning relevance:** Dr. Aly’s point about using tennis knowledge for ping pong maps to using general health domain data to assist with specific conditions

-----

## 6. HIDDEN CURRICULUM EXTRACTION

### Dr. Aly’s Research Interests (Marking Influence)

- **Emergent cognitive development** is his personal research passion: “For the emergence, which I personally like a lot.” His lab in Japan was called “Immersion Robotics” [likely “Emergent Robotics” – transcript garbled]. His PhD student works on language development through environmental interaction.
- **Prospection and Theory of Mind** are areas he cares deeply about – he spent disproportionate time on these relative to slide content.
- **Cross-module integration** – he expects students to remember FACS, emotion recognition, speech processing from earlier lectures and connect them to cognitive architecture concepts.

### Pet Topics

- **Child development as metaphor for robot learning** – used extensively (baby with cup, child learning language, nursery social learning)
- **Symbol grounding** – went on a long tangent explaining it in detail, indicating it’s important to him
- **The difficulty of implementing prospection in robots** – “very difficult. Very, very difficult” – he wants students to appreciate the challenge, not just describe it glibly

### Philosophical Positions

- **Complementarity over competition:** Repeatedly stressed Piaget and Vygotsky are complementary, not opposing. Individual and social development both matter. Apply this thinking to your report – don’t pick one approach and dismiss others.
- **Anti-plug-and-play:** Cognitive architectures require deep understanding of formalism before use. He expects students to show they understand WHY their approach works, not just that it runs.
- **Embodiment matters (for emergent):** Rejection of dualism and functionalism in emergent approaches. The physical body and cognitive mechanisms are one system.

-----

## 7. Q&A AND INTERACTIVE MOMENTS

**Q: What signals should a robot collect from the environment?**
Student answer: “What can see.”
Dr. Aly: “Yes, very good. What can see? For example, so I observe there are students or for example, let’s say I have to prove some students are silent, some students are laughing.”

**Q: What is the coding system for facial expressions?**
Students struggled. One said “Emotional coding.” Another said “Fax coding” [phonetic].
Dr. Aly: “Facial Action Coding System. So the FACS coding tells you what units of the face moves for humans.”
**Signal:** He was testing recall from earlier lectures. He expects this cross-referencing.

**Q: Why “theories” (plural) and why “unified”?**
Student: “Does this go back to how there were many definitions of cognition as well?”
Dr. Aly confirmed and expanded: because there are many theories of attention, memory, problem-solving etc., and “unified” means putting the most established/less disputed ones together.

**Q (student asking about project topics):**
Dr. Aly indicated he would update the project list, that most existing topics already have teams, and he is open to students proposing topics in his areas of interest. He specifically mentioned being “more than happy to chat” about healthcare-related topics or other areas of interest to him.

-----

## 8. COMPUTATIONAL THINKING PATTERNS

### Dr. Aly’s Problem-Solving Approach

- **Layer by layer:** He builds understanding from definitions (what is a cognitive agent?) -> architecture (what is a cognitive architecture?) -> types (cognitivist/emergent/hybrid) -> components (8 core abilities) -> specific details of each component
- **Analogy-first:** Chess for architecture x content, orange for symbol grounding, baby for development, shelf for memory encoding
- **Always connects theory to robotics implementation:** Every abstract concept gets a “how would this work in a robot?” treatment

### Design Decision Framework He Modelled

1. What does your robot need to do? (task analysis)
1. Does it need to develop/learn over time? -> If no: cognitivist. If yes: emergent. If both: hybrid.
1. Within chosen paradigm, which specific architecture? (compare available options)
1. Understand the formalism, rules, structure of chosen architecture
1. Add your domain knowledge to the framework
1. The combination produces your cognitive model

-----

## 9. META-LEARNING INTELLIGENCE

### Key References Mentioned

1. **Kotseruba and Tsotsos (2020)** – “40 years of cognitive architectures: core cognitive abilities and practical applications.” Artificial Intelligence Review, Vol. 53, No. 1, pp. 17-94. – Called “one of the very, very important papers.” USE THIS.
1. **Lehman et al. (1998)** – BEHAVIOR = ARCHITECTURE x CONTENT formulation
1. **Vernon (2014)** – Prospection as hallmark attribute of cognition
1. **von Hofsten (2009)** – Actions are goal-directed and guided by prospective information
1. **GMU BICA Architecture (Samsonovich 2010)** – Example of cognitivist architecture with memory modules
1. **Ritter and Young (2001)** – Cognitivist architecture definition (constant over time, independent of task)
1. **Langley (2005, 2006), Langley et al. (2009)** – Cited on slide 11 for cognitive system structure
1. **Sun (2007)** – Cited on slide 11 diagram
1. **Jean Piaget (1896-1980)** – Individual development theory
1. **Lev Vygotsky (1896-1934)** – Social development theory
1. **E. Spelke** – Core knowledge (referenced on slide 14)

### Study Advice (Implicit)

- **Lecture 12 will be shorter** and cover more specific/practical cognitive architectures + transition to coursework support
- Dr. Aly said: “Near to… we will have a session today probably we can speak about how we will work on the next period.” – Coursework support sessions are imminent. Bring your CRAMS proposal to get approval.

-----

## 10. WARNINGS AND PITFALLS REGISTER

- **Do NOT treat cognitive architecture types as opposites:** “I’m not telling you try to choose… they are not opponents.” Apply nuance in your report.
- **Do NOT assume cognitive architectures are plug-and-play:** “You have to understand the formalism, the rules… you have to give it knowledge.” Show understanding of the underlying mechanics, not just surface-level description.
- **Do NOT ignore prospection:** It is Dr. Aly’s addition beyond the standard reference, and he clearly values it highly. Missing it from your CRAMS report would be a significant omission.
- **Do NOT forget earlier module content:** He explicitly tested FACS recall. Your report should demonstrate integration across the whole module, not just the most recent lectures.
- **Do NOT mistake cognitivist for static/simple:** It has basic building blocks that are “relatively constant over time” but can still have machine learning augmentation. The distinction is about the degree and nature of development, not the presence/absence of any learning.

-----

## CRAMS-SPECIFIC ACTION ITEMS FROM THIS LECTURE

1. **Frame CRAMS as a hybrid cognitive architecture** in your report: POMDP symbolic structure (cognitivist) + OpenAI neural network processing (emergent/connectionist) = hybrid. This is a sophisticated classification that demonstrates lecture understanding.
1. **Create a mapping table** in your report: CRAMS Component -> Core Cognitive Ability -> Implementation Detail. Cover all 8 abilities.
1. **Emphasise prospection** as the novel contribution: Your POMDP belief projection literally implements computational prospection. Reference Vernon (2014) and note this is absent from Kotseruba and Tsotsos (2020).
1. **Use the Lehman (1998) equation** in your Method section: BEHAVIOR = ARCHITECTURE x CONTENT. Your POMDP structure = architecture, current belief state/observations = content, robot’s medication support action = behaviour. The multiplicative relationship means the same observation produces different actions depending on belief state, and vice versa.
1. **Reference Theory of Mind** when describing your perception/observation module. The robot inferring patient internal state from external signals IS computational Theory of Mind.
1. **Wait for Lecture 12** before finalising design – Dr. Aly said more practicalities about specific architectures coming next, plus coursework support transition.

-----

*Cross-check this extraction with Gemini for critique and gap identification.*