CRAMS (Cognitive Robot for Adaptive Medical Support)

The robot watches and listens to the user's facial expressions, voice tone, gestures through the OpenAI API. Then, it figures out whether the person trusts it and whether they're cognitively overloaded. It maintains a belief about them, which updates every interaction. Based on that belief, the POMDP picks the best action, e.g. a verbal reminder if trust is high,; or maybe explaining why the medication matters if the person seems hesitant to boost trust, or backing off entirely if they're refusing.

Does not just react but *anticipates* (plans accordingly to the belief about the user).

Before choosing an action, it simulates what's likely to happen; it also remembers what worked and what didn't in past interactions; it has a self-check i.e. checks if it picks actions that make things worse, it will notice and change its approach.

Code-specific: a Python simulation that shows the belief updating, the action choices, the outcomes over continous interaction, etc

Wraps chatgpt (which is good at reading people but has no actual non-custom-made memory (apart from computantially created in a conversation-loop list etc); no planning ability, etc) a POMDP will instead provide *memory* (which provides the memory and planning the LLM lacks).

POMDP ARCHITECTURE: OpenAI API (perception) \to structured observation (Comply, Hesitate, Verbal_Refuse, Ignore, Gaze_Avert, ...) \to POMDP updates belief & selects action (memory/reasoning/prospection) \to OpenAI API translates action into language & gesture \to user responds \to cycle repeats

Lfd because it learns from the user's behaviour, not from a predefined reward function. It infers what the user wants and how they feel based on their cues, and it learns to adapt its behaviour accordingly.
