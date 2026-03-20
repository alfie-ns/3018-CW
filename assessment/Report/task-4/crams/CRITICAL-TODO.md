CRAMS -- Cognitive Robot for Adaptive Medical Support

A POMDP-based cognitive robot that supports medication adherence by reading

a user's behavioural cues, maintaining a probabilistic belief about their

hidden trust level and cognitive load, and selecting contextually appropriate

actions -- all whilst remembering past interactions and self-checking its own

performance.

Cognitive architecture (maps to Vernon, 2014; Lecture 9):

    Perception:         -> OpenAI API via NAO camera/mic (simulated here)

    Attention:          -> selective focus on trust / load signals

    Action selection:   -> QMDP policy over belief state

    Memory:             -> episodic memory (session) + semantic memory (SQLite)

    Learning:           -> Bayesian belief update

    Reasoning:          -> QMDP value iteration (prospection)

    Meta-reasoning:     -> self-check for declining performance

    Prospection:        -> forward simulation before acting

POMDP tuple: (S, A, O, T, Omega, R, gamma)

    S     = hidden states (Trust x CognitiveLoad)

    A     = robot actions

    O     = observable user behaviours

    T     = transition model  P(s' | s, a)

    Omega = observation model P(o  | s', a)

    R     = reward function   R(s, a)

    gamma = discount factor

Pipeline (deployment on NAO):

    NAO mic/camera -> OpenAI API (perception) -> structured observation ->

    POMDP updates belief & selects action (memory / reasoning / prospection) ->

    OpenAI API translates action into language & gesture -> NAO speaks/gestures ->

    user responds -> cycle repeats

References:

    Kaelbling, L. P., Littman, M. L. and Cassandra, A. R. (1998)

    'Planning and acting in partially observable stochastic domains',

    Artificial Intelligence, 101(1-2), pp. 99-134.

    Littman, M. L., Cassandra, A. R. and Kaelbling, L. P. (1995)

    'Learning policies for partially observable environments: Scaling up',

    Proceedings of the 12th International Conference on Machine Learning,

    pp. 362-370.

    Vernon, D. (2014) Artificial Cognitive Systems: A Primer.

    Cambridge, MA: MIT Press.

    Atance, C. M. and O'Neill, D. K. (2001) 'Episodic future thinking',

    Trends in Cognitive Sciences, 5(12), pp. 533-539.
