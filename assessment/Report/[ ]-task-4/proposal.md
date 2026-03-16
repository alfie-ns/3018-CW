CRAMS (Cognitive Robot for Adaptive Medical Support)

The robot watches and listens to the user's facial expressions, voice tone, gestures through the OpenAI API. Then, it figures out whether the person trusts it and whether they're cognitively overloaded. It maintains a belief about them, which updates every interaction. Based on that belief, the POMDP picks the best action, e.g. a gentle verbal reminder if trust is high,; or maybe explaining why the medication matters if the person seems hesitant to boost trust, or backing off entirely if they're refusing.

Does not just react but *anticipates* (plans accordingly to the belief about the user).

Before choosing an action, it simulates what's likely to happen; it also remembers what worked and what didn't in past interactions; it has a self-check i.e. checks if it picks actions that make things worse, it notices and changes approach.

Code-specific: a Python simulation that shows the belief updating, the action choices, the outcomes over continous interaction, etc

Wraps chatgpt (which is good at reading people but has no actual non-custom-made memory (apart from computantially in a conversation-loop list etc); no planning ability, etc) instead a POMDP will provide *memory* (which provides the memory and planning the LLM lacks).

POMDP ARCHITECTURE: OpenAI API (perception) -> structured observation (Comply, Hesitate, Verbal_Refuse, Ignore, Gaze_Avert, ...) -> POMDP updates belief & selects action (memory/reasoning/prospection) -> OpenAI API translates action into language & gesture -> user responds -> cycle repeats
