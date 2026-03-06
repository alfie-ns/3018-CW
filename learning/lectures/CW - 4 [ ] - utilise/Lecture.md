# COMP3018 Lecture 4: Spatial Interaction -- Complete Intelligence Extraction

**Module:** COMP3018/COMP5018 Human-Robot Interaction
**Lecturer:** Dr. Amir Aly
**Topic:** Spatial Interaction
**Source:** Lecture slides (PDF) + Lecture transcript (primary source)
**Extraction Date:** 06/03/2026

---

## 1. CRITICAL ASSESSMENT INTELLIGENCE [HIGHEST PRIORITY]

### Direct Coursework Mapping

**Assessment 1 (30% -- Set Exercises, due 12th March 2026):**

* **Task 1: Cultural Differences and HRI Design (40% of A1)**
  * This lecture is DIRECTLY relevant to Task 1. Dr. Aly spent significant time discussing how proxemics vary across cultures. His exact words: "Every country and each culture has their own concept of proxemics." He gave specific examples contrasting Mediterranean, Northern European, and Japanese cultures -- this is precisely the kind of cultural factor analysis Task 1 demands.
  * His statement: "A robot in Japan dealing with Japanese people will not do the same behaviour like robot in Spain with Spanish people, robot in France with French people" -- this maps directly to Task 1, Q3 (suggesting how cultural factors determine robot traits for East/West/Africa).
  * The Joggobot example (Bartneck et al., 2020) from the slides -- a drone companion for joggers where "joggers don't like being chased" -- is a concrete example of how cultural/personal preferences shape robot design, directly useful for Task 1 Q3-Q4.
  * His discussion of proxemic zones (intimate 0-0.5m, social 1.2-3.7m, public 3.7m+) being culturally dependent is a concrete framework you can apply when discussing Kahn et al.'s (2008) design patterns for sociality (Task 1, Q4).
* **Task 2: Models for HRI / POMDP (60% of A1)**
  * Less directly relevant, but the concept of **uncertainty in spatial positioning** (the robot not knowing people's intentions, facing direction, whether they're conversing or just standing close) connects to POMDP's handling of uncertainty. Dr. Aly's critique: "Most mapping techniques consider people as obstacles. They don't provide information about the direction people are facing... what they are doing, are they conversing or just standing close together" -- this is a partially observable environment, which is literally what POMDPs model.

**Assessment 2 (70% -- Report, due 5th May 2026):**

* **Task 3: Literature Review on Assistive Robotics (40% of A2)**
  * Spatial interaction is foundational for assistive robots. Navigation, localisation, SLAM, and socially-aware path planning are all critical for assistive robotics applications. Dr. Aly's discussion of how robots must maintain social distance, avoid personal space, and understand group formations (F-formations) is directly relevant to challenges assistive robots face.
  * His key point: "What matters is the social impact of movement, not its functional efficiency" (slide 20) -- this is a brilliant line to reference when discussing challenges in assistive robotics. An assistive robot that is functionally efficient but socially inappropriate will fail.
* **Task 4: Programming Project (60% of A2)**
  * If your project involves a mobile robot or any form of navigation/spatial awareness, this lecture provides the theoretical grounding. The F-formation concept (o-space, p-space, r-space) gives you a framework for implementing socially-aware robot behaviour.
  * Dr. Aly's critique about human-aware maps vs. obstacle-based maps is a gap you could address as a "novel intellectual contribution" for Task 4.

### Marking Criteria Cross-Reference

For 70%+ (first-class), the brief states: "very well discussed in detail, supported by excellent arguments... clear and well-justified analysis... strong evidence of investigation and research... deep analysis and full investigation... writings are of high standards and quality (focused and concise)."

This lecture gives you ammunition for "deep analysis" -- particularly the critique about mapping techniques treating people as obstacles. Using Dr. Aly's own critical framework in your answers signals you've engaged deeply with the material.

---

## 2. THE COMPLETE 'ALPHA' BRIEF: Comprehensive Directives

* [***] **Cultural variation in proxemics is a CORE theme.** Dr. Aly returned to this repeatedly (at least 5 times across the lecture). He gave extended examples: Spain/Mediterranean (close contact acceptable, hand on shoulder with strangers), Northern Europe (more distance), Japan (no handshaking, touching is impolite). Verbatim: "In Japan it's very considered impolite, for example, if you break the personal distance or space and try to touch somebody by any means. So even don't shake hands. Japanese people, they don't shake hands."
* [***] **"What matters is the social impact of movement, not its functional efficiency"** (slide 20). This is a philosophical position Dr. Aly holds -- the robot's SOCIAL behaviour trumps optimal pathfinding. This is a first-class thinking point.
* [***] **Critical analysis point: mapping techniques treat people as obstacles.** Verbatim: "This is an important critique that most mapping techniques consider people as obstacles... But most of the techniques, the direction of people they are facing... what they are doing, are they conversing or just standing close together... HRI maps need more human-aware representation." He explicitly flagged this as "an important critique" -- lecturer pet topic alert.
* [***]  **Robots must NEVER pass through a group's o-space** , even if there is physical room. Verbatim: "Even if there is enough space to pass between people, the robot should avoid." This is about social norms, not physical constraints.
* [**] **Proxemics depends on BOTH age and culture** -- mentioned twice (slides and verbally). Not just culture.
* [**] **Three types of spatial arrangement matter:** face-to-face, L-shape, side-by-side. Each has different social meaning: "People who sit next to each other are more cooperative. People who sit opposite to each other are more competitive. And during conversation people usually position themselves at an angle."
* [**] **Cloud robotics tangent** -- Dr. Aly discussed robots sharing knowledge via the cloud so a robot travelling from Japan to Spain could adapt its proxemic behaviour. Verbatim: "The robot in Japan will know and say that I can approach people until some limits... if the robot of Japan travelled to Spain, the robot can adapt or vice versa." This is a forward-looking point about scalable cultural adaptation -- useful for Task 1 Q3-Q4 and Task 3's "future applications" section.
* [**] **Robot appearing aggressive** if it doesn't yield. Verbatim: "A robot that doesn't do this may appear aggressive." Slide 18 also notes: "Is this culturally dependent?" -- the lecturer is prompting you to think about whether yielding behaviour varies by culture.
* [*] **Walters et al. (2005)** cited on slide 20 -- study found people prefer personal or social distance from robots, but some prefer closer. Individual variation exists even within cultures.
* [*] **Lecture pacing note:** Dr. Aly said "These lectures finish quickly unlike machine learning" and referenced his COMP3003 students having "suffered with me in long lectures, but they all did well." This suggests HRI content is more conceptual/lighter than ML, but don't underestimate it.
* [*] **Next lecture is Ethics for Robotics and AI** -- he mentioned it might be combined with another topic: "Because ethics is not big slides, not large number of slides. So we can also add two of them together." Ethics is directly relevant to Task 2 Q5 (ethical implications of POMDPs) and Task 3 (ethical issues in assistive robotics).

---

## 3. EXHAUSTIVE TOPIC BREAKDOWN WITH COMPLETE QUOTATION

### TOPIC A: Proxemics (Slides 3-8)

**Lecturer's Definition (verbatim):** "Proxemics is a study of how people take up space in relation to others and how spatial positioning influences attitude, behaviour and interpersonal interaction."

**Extended Explanation:** "When I speak about spatial interaction, I speak certainly about something related to space... The robots actually supposed to coexist with human inhabitants in a place, they should be among us. So how should they move?"

**The Bus Analogy (verbatim, extended):** "Imagine like you have this bus and the bus is empty, exactly the same thing. And instead of choosing where to sit down, you go to sit down with that person. Why? The bus is empty. The person, as a normal reaction would say, why you're sitting down beside me, there is enough space."

**The Office/Table Analogy (verbatim):** "Also if you have this table or like this setup here, where will you come to sit down? Where you come sit down in part one here or part two, or where? Simply you will choose this area where you have more free space. This intuitively what we do."

**Cultural Variation -- Japan (verbatim, extensive):** "In Japan it's very considered impolite, for example, if you break the personal distance or space and try to touch somebody by any means. So even don't shake hands. Japanese people, they don't shake hands. So you might find very... if you go to Japan, might find that you try to shake hand. But people understand that westerners are shaking hands. This is normal. But you might expand your hand. But you find the other person is not replying to you and not taking your hand back to shake hands. So you might find that this is... why they don't like me or something. No, it's like that."

**Cultural Variation -- Mediterranean (verbatim):** "In Spain, for example, or Mediterranean countries, you find the people can approach you very closely, for example, and put their shoulder on your hands... on your shoulders, for example, despite they might not know you. Naturally it's like that."

**Cultural Variation -- Northern Europe (verbatim):** "If you go to north of Europe sometimes, you might still, for example, not being very normal to do... the people probably can have some more distance."

**The Four Distance Zones (Bartneck et al., 2020):**

* **Intimate:** 0-0.5m (between close persons)
* **Personal:** Part of personal space (grouped with intimate)
* **Social:** 1.2-3.7m (e.g., "distance between us here, this one meter")
* **Public:** 3.7m to infinity

**Lecturer's clarification on zones:** "So social distance, like for example, it can be like distance between us here, okay, this one metre. But if I am a little bit zero, between 0.5, like very close."

**Depends on:** Age and culture (stated twice). "These are social norms. So probably, you know, like robots, if they can be connected across a unified cloud, hopefully one day... they can share."

**Placement matters, not just distance (slide 8):**

* Side-by-side = cooperative
* Opposite = competitive
* At an angle = typical conversation positioning

**Lecturer's explanation:** "So if you are sitting in front of me, it's different than if you're sitting beside."

---

### TOPIC B: Group Spatial Interaction Dynamics -- F-Formations (Slides 9-10)

**Lecturer's Definition:** The F-formation (facing-formation) describes how people arrange themselves spatially during group interaction.

**Three spatial regions (verbatim definitions + lecturer's elaboration):**

**o-space:** "The space between people to which they have equal, direct, exclusive access. Like this area... where you are, I was speaking about two persons, like one person here and one person here speaking to each other. And I come to violate their own space. This can stop the interaction."

**p-space:** "This area around... the space occupied by people themselves."

**r-space:** "The space surrounding the people."

**Three formation types (from slide diagram):** Face-to-face, L-shape, Side-by-side.

**Critical robot behaviour rule (verbatim):** "Simply, robots need to be aware of these spaces so that they don't invade... And even there is enough space to pass between people, even if there is enough space to pass between people, the robot should avoid."

**Lecturer's walkthrough of why (verbatim):** "So if I will be passing finding two persons speaking like this, I should avoid the o-space and p-space. O-space because it will interrupt the discussion. P-space because I will collide with them. So I would like to avoid... if I don't, for example, go a little bit further, I can collide with one of the persons. And the outer space is the area where I should be moving around."

---

### TOPIC C: Localisation and Navigation (Slides 11-17)

**Localisation -- Lecturer's Definition (verbatim):** "Localisation is determining a mobile robot's position and possibly orientation."

**Odometry (verbatim):** "The odometry determines position by sensing rotation of wheels. So I can leave the robot that has wheels and it can go, go, go... through the rotation of wheels. I can have odometry. So I can sense the place of the robot with respect to rotation of wheels. And certainly during... as long as I can determine the position, I can compute distance travelled and change orientation."

**SLAM (verbatim):** "SLAM, which is another concept, is Simultaneous Localisation and Mapping. So this constructs a map as a robot moves and localises. So I construct a map and I use odometry to localise myself inside this place."

**SLAM walkthrough (verbatim, extended):** "So I know like... you can here have... we will see a video for this map for the place. So I constructed by laser sensor, construct a map like this. And in this map I can identify... the robot can identify itself saying I am, for example, in this blue point or in the red point in the location. And effectively you look at the robot, you find that it is in the blue point. So it detects itself with respect in the map. Where do I locate in the map? And it locates itself in the map."

**Type of Space Identification:** "Also identify type of space the robot is in. So for example, if the robot is in classroom, living room, bathroom... all this actually localisation can tell us where the robot is with respect to a specific landmark."

**Sensors for Localisation (from slides + transcript):**

* Short range: 2D RGB cameras, Depth/RGBD cameras (e.g., Kinect)
* Long range: Laser range finders (LIDAR -- light detection and ranging)
* Can detect and track: People, Body parts (arms, legs, hands, head)
* Environmental sensors can be mounted around the interaction environment

**Lecturer's practical note (verbatim):** "Some of your colleagues, for example, when they were making the project with Nao robot, they were using camera. I provide them camera or sometimes they provide themselves camera and say, okay, I'm making experiment with the robot and I show card game."

**Navigation -- Lecturer's Definition (verbatim):** "Moving to a goal location through a possibly crowded environment."

**Navigation involves:**

1. Obstacle (collision) avoidance
2. Path planning -- move from waypoint to waypoint
3. Avoid obstacles
4. **Maintain social distance** (highlighted in red on slides)

**Navigation walkthrough (verbatim):** "So if, for example, we have to start from here and we have an obstacle, person here, we have to turn around until we reach the goal... So move from waypoint to waypoint, avoid obstacles and maintain social distance. So this means like you don't pass close to the person. Give the person the social distance. So I want to pass like this, but a little bit... I come a little bit from here and pass."

**Extended navigation explanation (verbatim):** "And if the person is here, certainly, for example, you cannot secure enough social distance because like if you will pass from here or from here, it will be small distance. So what you should do is like to turn around, come from here and come here."

---

### TOPIC D: Socially Appropriate Positioning (Slides 18-20)

**Yielding behaviour (verbatim):** "Normally humans yield to each other when approaching. So to avoid entering each other's personal space. And also using nonverbal signals."

**Aggression implication (verbatim):** "A robot that doesn't do this may appear aggressive. So the robot should not enter in personal space or else it will be aggressive behaviour."

**Critical Critique -- People as Obstacles (verbatim, FULL):** "This is an important critique... most mapping techniques consider people as obstacles. And they should avoid. But most of the techniques, the direction of people they are facing... are they speaking like this while the robot is approaching from here or they are facing the robot. Where is the direction of the people and what they are doing? Are they conversing or just standing close together? So HRI maps need more human-aware representation. So they consider humans as obstacles. But we need to know more details in the current techniques. We need to know more details about the behaviour, what they are doing."

**Slide annotation question:** "Is this culturally dependent?" -- appears as a margin note on slide 18 regarding yielding behaviour. This is Dr. Aly prompting critical thinking about whether even yielding norms vary by culture.

**How close do people prefer? (verbatim):** "Most of people prefer the personal or social distance... the spacing and the proximity can be different from culture to culture and person to person."

**Key philosophical position (slide 20):** "What matters is the social impact of movement, not its functional efficiency." Plus note: "When a robot points to something or makes a gesture, it must not invade the human's personal space."

**Research reference:** Walters et al. (2005) -- found people prefer personal or social distance from robots, but some prefer closer.

---

## 4. COMPLETE LECTURER'S LEXICON

| Term                           | Definition (Lecturer's Words)                                                                                                                        | Context                                                     |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| **Proxemics**            | "A study of how people take up space in relation to others and how spatial positioning influences attitude, behaviour and interpersonal interaction" | Core concept of the entire lecture                          |
| **Intimate distance**    | 0-0.5m, "between two close persons"                                                                                                                  | Part of Bartneck et al. (2020) four-zone model              |
| **Personal distance**    | Grouped with intimate as "personal space"                                                                                                            | Lecturer treated intimate + personal as closely related     |
| **Social distance**      | 1.2-3.7m, "like distance between us here"                                                                                                            | The typical interaction distance                            |
| **Public distance**      | 3.7m to infinity                                                                                                                                     | Beyond social interaction range                             |
| **F-formation**          | "Facing-formation" -- spatial arrangement of people in group interaction                                                                             | Three types: face-to-face, L-shape, side-by-side            |
| **o-space**              | "The space between people to which they have equal, direct, exclusive access"                                                                        | The shared interaction zone -- NEVER to be invaded by robot |
| **p-space**              | "The space occupied by people themselves"                                                                                                            | Physical space of the people -- collision zone              |
| **r-space**              | "The space surrounding the people"                                                                                                                   | Outer zone -- where robot should navigate                   |
| **Odometry**             | "Determines position by sensing rotation of wheels"                                                                                                  | Basic localisation method                                   |
| **SLAM**                 | "Simultaneous Localisation and Mapping -- constructs a map as a robot moves and localises"                                                           | Advanced localisation                                       |
| **LIDAR**                | "Laser range finders -- light detection and ranging"                                                                                                 | Long range sensor type                                      |
| **Navigation**           | "Moving to a goal location through a possibly crowded environment"                                                                                   | Involves path planning + social distance maintenance        |
| **Cloud robotics**       | Robots connected via cloud sharing knowledge (e.g., cultural norms) across locations                                                                 | Lecturer's forward-looking tangent                          |
| **High-contact culture** | Cultures where close physical proximity/touch is normal (e.g., Spain, Mediterranean)                                                                 | Slide 7                                                     |
| **Low-contact culture**  | Cultures where physical distance is maintained (e.g., Japan, Northern Europe)                                                                        | Slide 7                                                     |

---

## 5. COURSEWORK SUCCESS BLUEPRINT

### Assessment 1 -- Task 1 (Cultural Differences and HRI Design) [DUE 12 MARCH]

**Q1 (Kaplan 2004 -- cultural factors, 20%):** Use proxemics as a framework. Dr. Aly's lecture provides the real-world grounding for Kaplan's theoretical cultural factors. His Japan vs. Spain vs. Northern Europe examples are exactly the kind of East-West contrast Kaplan discusses.

**Q2 (Cultural factors in Africa, 20%):** Apply the proxemics framework. Consider what Dr. Aly said about high-contact vs. low-contact cultures and extend to African contexts. His point that "every country and each culture has their own concept of proxemics" legitimises proposing novel cultural factors.

**Q3 (Traits for robot acceptance, 30%):** Dr. Aly's specific examples give you concrete traits: a robot for Japan should maintain greater distance, never initiate physical contact, bow rather than extend hand. A robot for Spain/Mediterranean can operate at closer range, potentially use touch-based interaction. His cloud robotics discussion suggests adaptive proxemic profiles as a design trait.

**Q4 (Adapting Kahn et al. 2008 design patterns, 30%):** The F-formation framework maps directly to Kahn et al.'s sociality patterns. Different cultures may have different expected formations -- this is your "novel" connection. Dr. Aly's point about "what matters is the social impact of movement, not its functional efficiency" should inform how you discuss adapting design patterns for different cultural contexts.

### Assessment 2 -- Task 3 (Assistive Robotics Literature Review) [DUE 5 MAY]

**Applications section (30%):** Navigation and spatial awareness are fundamental to assistive robots operating in homes, hospitals, care facilities. SLAM, odometry, and socially-aware path planning are all directly applicable.

**Challenges section (within Discussion, 20%):** Dr. Aly's critique that "HRI maps need more human-aware representation" is a challenge for assistive robotics -- the robot needs to understand not just WHERE people are but WHAT they are doing and HOW they want to be approached.

**Ethical issues:** The aggression perception issue -- "a robot that doesn't do this may appear aggressive" -- has ethical implications for vulnerable users of assistive robots. Cultural sensitivity in proxemics is an ethical design consideration.

### Assessment 2 -- Task 4 (Programming Project) [DUE 5 MAY]

**Potential project ideas grounded in this lecture:**

* Implementing culturally-adaptive proxemic zones in a robot navigation system (directly addresses the cloud robotics vision Dr. Aly described)
* F-formation detection and socially-aware navigation -- making a robot that detects group formations and routes around them appropriately
* Human-aware mapping that goes beyond treating people as obstacles (this addresses Dr. Aly's explicit critique -- strong "novel intellectual contribution")
* Comparing robot approach strategies at different distances and measuring user comfort (replicating/extending Walters et al., 2005)

**Method and setup (35% of Task 4):** The sensor setup Dr. Aly described (Kinect, RGBD cameras, LIDAR) gives you a practical framework for your experimental setup. He even showed his own lab setup with multiple Kinects and cameras mounted around the interaction environment.

---

## 6. HIDDEN CURRICULUM EXTRACTION

### Lecturer's Research Interests

* Dr. Aly showed images from what appears to be his own lab (Nao robot with Kinect sensors and multiple cameras). He has hands-on experience with spatial interaction experiments. He values PRACTICAL implementation alongside theory.
* His extended discussion of cloud robotics for sharing cultural norms suggests interest in scalable, adaptive systems.

### Pet Topics

* **Cultural variation in proxemics** -- returned to this theme repeatedly (5+ times). This is clearly something he cares deeply about and will likely reward detailed discussion of in coursework.
* **The critique that current mapping treats people as obstacles** -- he explicitly flagged this as "an important critique" and spent time elaborating. This suggests it's something he'd love to see students engage with critically.
* **Social norms over functional efficiency** -- the philosophical position that a robot's social appropriateness matters more than optimal path planning.

### Philosophical Positions

* Robots should be designed around HUMAN social norms, not the other way around
* Cultural sensitivity is non-negotiable in HRI design
* The gap between current mapping/navigation techniques and what HRI actually requires is significant and worth researching

### Industry/Real-World Perspectives

* The Joggobot example (Bartneck et al., 2020) -- drones as jogging companions
* Cloud robotics as a mechanism for cultural knowledge sharing
* Student projects with Nao robot -- he provides practical equipment and expects practical engagement

---

## 7. Q&A AND INTERACTIVE MOMENTS

**Student asking about lecture length:** Dr. Aly compared HRI to ML: "These lectures finish quickly unlike machine learning. This time these guys suffered with me in long lectures, but they all did well. So your turn next semester." -- Signals that HRI is more conceptual/less dense than ML, but he expects similar effort.

**Moment of checking student engagement:** "It's okay, it's... Are you okay? Yeah, because you are typing with your hand. I just don't... I observed you are not following, so I just follow." -- Dr. Aly actively monitors engagement. He notices when students aren't following. This tells you he values active participation.

**End of lecture -- no questions from students.** He said: "Do you have questions so far for today? Okay, this is like... We are progressing well, so I will give you the code." -- "I will give you the code" suggests practical coding materials will be shared, relevant to Task 4.

---

## 8. COMPUTATIONAL THINKING PATTERNS

* Dr. Aly thinks in terms of **spatial models first, then implementation.** He introduced concepts (proxemics, F-formations) before discussing how to implement them (sensors, SLAM, navigation).
* His approach to navigation is: detect people -> understand their spatial arrangement -> plan path that respects social norms -> execute. Not just: detect obstacles -> avoid.
* He values the **layered approach:** odometry for basic positioning, SLAM for mapping, then social awareness on top.

---

## 9. META-LEARNING INTELLIGENCE

### Readings Recommended (Slide 22)

1. **Bartneck, C. and Belpaeme, T., et al. (2020)** --  *Human-Robot Interaction* , Cambridge University Press. (This is the textbook -- referenced multiple times in slides for proxemic zones)
2. **Graziano, M. (2018)** -- "The Unconscious Rules of Personal Space",  *The Atlantic* . (A more accessible/popular science reading on proxemics)

### Key References from Lecture Content

* **Bartneck et al. (2020)** -- Joggobot, proxemic zones, F-formations
* **Walters et al. (2005)** -- Study on preferred human-robot distances
* **Kaplan (2004)** -- Referenced in Assessment 1 (cultural differences in robot acceptance)
* **Kahn et al. (2008)** -- Referenced in Assessment 1 (design patterns for sociality)

### Study Advice

* Dr. Aly's mention of "I will give you the code" at the end suggests practical materials are forthcoming -- collect and study these for Task 4.
* The ethics lecture next week will be combined with another topic due to its shorter length -- pay close attention as ethics feeds into both Assessment 1 (Task 2, Q5) and Assessment 2 (Task 3).

---

## 10. TRANSCRIPT PROCESSING NOTES

* "Special interaction" at the start was the lecturer testing students -- he corrected to "spatial interaction." Verbatim: "When I say special, what does it mean? What does it mean? Special environment. Yeah, Space not special. Okay, Spatial interaction."
* "Audiometry" appears multiple times in the transcript -- this is a transcription error for  **odometry** .
* "Parthenay" in the transcript -- this is a transcription error for **Bartneck** (the textbook author).
* "Jean Pepper" -- likely a transcription error, possibly referring to turning around the **p-space** perimeter.
* "The naval" -- likely a transcription error for **the Nao** (robot).
* Lecturer occasionally mixes up body parts when giving examples (e.g., "put their shoulder on your hands" -- meant "hand on your shoulders").

---

*Now cross-check this extraction with Gemini for any gaps or alternative interpretations.*
