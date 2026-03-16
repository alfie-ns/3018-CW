"""
pomdp.py -- POMDP Engine for CRAMS
Cognitive Robot for Adaptive Medical Support

Formulates medication adherence as a Partially Observable Markov Decision
Process. The robot cannot directly observe trust or cognitive load; it infers
these from behavioural cues (observations) and selects actions that maximise
long-term adherence whilst maintaining trust.

POMDP tuple: (S, A, O, T, Omega, R, gamma)
    S     = hidden states (Trust x CognitiveLoad)
    A     = robot actions
    O     = observable user behaviours
    T     = transition model  P(s' | s, a)
    Omega = observation model P(o  | s', a)
    R     = reward function   R(s, a)
    gamma = discount factor

Reference:
    Kaelbling, L. P., Littman, M. L. and Cassandra, A. R. (1998)
    'Planning and acting in partially observable stochastic domains',
    Artificial Intelligence, 101(1-2), pp. 99-134.
"""

import numpy as np
from typing import Tuple

# ── State Space --
# 2-D hidden state: (Trust, CognitiveLoad), each with 3 levels -> 9 states.
# The robot never observes these directly; it maintains a belief distribution.

TRUST_LEVELS = ["High", "Medium", "Low"]
LOAD_LEVELS = ["Low", "Medium", "High"]

STATES = [f"T:{t}_L:{c}" for t in TRUST_LEVELS for c in LOAD_LEVELS]
# Index 0 = (High trust, Low load)  -- best case
# Index 8 = (Low trust, High load)  -- worst case

# ── Action Space --
# Actions the cognitive robot can take during a medication adherence episode.

ACTIONS = [
    "Gentle_Reminder",       # simple, non-intrusive prompt
    "Explain_Importance",    # explain why medication matters (trust-building)
    "Back_Off",              # withdraw, give space (load-reducing)
    "Encourage",             # positive reinforcement
    "Direct_Prompt",         # assertive, clear instruction
    "Simplify",              # break task into smaller steps (load-reducing)
]

# ── Observation Space --
# Structured observations derived from multimodal perception (face, voice,
# gesture). In deployment, the OpenAI API maps raw sensory data to these
# discrete categories; herein the simulated user generates them directly.

OBSERVATIONS = [
    "Comply",            # user takes medication
    "Hesitate",          # user pauses, seems unsure
    "Verbal_Refuse",     # user explicitly says no
    "Ignore",            # no response at all
    "Gaze_Avert",        # user looks away (discomfort / avoidance)
    "Nod",               # acknowledgement without full compliance
    "Ask_Question",      # user seeks clarification
]

n_s = len(STATES)   # 9
n_a = len(ACTIONS)  # 6
n_o = len(OBSERVATIONS)  # 7


# ── Index helpers --

def state_idx(trust: int, load: int) -> int:
    """Flat index from (trust_level_idx, load_level_idx)."""
    return trust * len(LOAD_LEVELS) + load


def state_components(idx: int) -> Tuple[int, int]:
    """Return (trust_idx, load_idx) from flat state index."""
    return divmod(idx, len(LOAD_LEVELS))


# ── Transition Model T[a][s][s'] ─────────────────────────────────────
# Trust and load evolve independently given the robot's action.
# Shift probabilities: [P(improve), P(same), P(worsen)]
#   improve = trust rises or load falls (index moves towards 0)
#   worsen  = trust falls or load rises (index moves towards max)

_TRUST_SHIFT = {
    #                       improve  same  worsen
    "Gentle_Reminder":      [0.20,   0.70, 0.10],
    "Explain_Importance":   [0.40,   0.50, 0.10],
    "Back_Off":             [0.15,   0.55, 0.30],
    "Encourage":            [0.35,   0.50, 0.15],
    "Direct_Prompt":        [0.10,   0.40, 0.50],
    "Simplify":             [0.25,   0.55, 0.20],
}

_LOAD_SHIFT = {
    #                       decrease same  increase
    "Gentle_Reminder":      [0.15,   0.65, 0.20],
    "Explain_Importance":   [0.10,   0.50, 0.40],
    "Back_Off":             [0.55,   0.35, 0.10],
    "Encourage":            [0.20,   0.60, 0.20],
    "Direct_Prompt":        [0.10,   0.40, 0.50],
    "Simplify":             [0.50,   0.40, 0.10],
}


def _dim_transition(current: int, n_levels: int, shift: list) -> np.ndarray:
    """
    Transition probabilities for one dimension with boundary clamping.
    Probability mass that would exceed [0, n_levels-1] is absorbed by
    the boundary state.
    """
    p = np.zeros(n_levels)
    p_improve, p_same, p_worsen = shift

    if current > 0:
        p[current - 1] += p_improve
    else:
        p[current] += p_improve       # already at best -> stay

    p[current] += p_same

    if current < n_levels - 1:
        p[current + 1] += p_worsen
    else:
        p[current] += p_worsen        # already at worst -> stay

    return p


def build_transition_model() -> np.ndarray:
    """
    Construct T[a][s][s'] = P(s' | s, a).

    Trust and load transition independently, therefore
        P(s' | s, a) = P(t' | t, a) * P(l' | l, a)
    """
    T = np.zeros((n_a, n_s, n_s))

    for a_idx, action in enumerate(ACTIONS):
        for s in range(n_s):
            t, l = state_components(s)
            p_trust = _dim_transition(t, 3, _TRUST_SHIFT[action])
            p_load = _dim_transition(l, 3, _LOAD_SHIFT[action])

            for t_new in range(3):
                for l_new in range(3):
                    T[a_idx, s, state_idx(t_new, l_new)] = (
                        p_trust[t_new] * p_load[l_new]
                    )
    return T


# ── Observation Model Omega[a][s'][o] ────────────────────────────────

def _base_obs_probs(trust: int, load: int) -> np.ndarray:
    """
    Base observation distribution as a parametric function of state.

    Trust  drives compliance vs refusal (higher trust -> more compliance).
    Load   shifts distribution towards hesitation / avoidance.

    Returns unnormalised weights for each observation.
    """
    tf = (2 - trust) / 2.0   # 1.0 = High trust, 0.0 = Low trust
    lf = load / 2.0           # 0.0 = Low load,   1.0 = High load

    return np.array([
        0.10 + 0.45 * tf * (1 - 0.5 * lf),          # Comply
        0.10 + 0.15 * lf,                             # Hesitate
        0.05 + 0.30 * (1 - tf),                       # Verbal_Refuse
        0.05 + 0.20 * (1 - tf) * (1 + lf) / 2,       # Ignore
        0.05 + 0.15 * ((1 - tf) + lf) / 2,            # Gaze_Avert
        0.05 + 0.15 * tf * (1 - lf / 2),              # Nod
        0.05 + 0.10 * tf * (1 - lf),                  # Ask_Question
    ])


# Multiplicative action modifiers -- each action shifts observation
# likelihoods relative to the base distribution.
_ACTION_OBS_MOD = {
    "Gentle_Reminder":    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    "Explain_Importance": [0.9, 1.0, 0.8, 0.9, 0.9, 1.2, 1.5],
    "Back_Off":           [0.5, 0.8, 0.7, 1.5, 1.3, 0.8, 0.7],
    "Encourage":          [1.1, 0.9, 0.8, 0.9, 0.8, 1.3, 1.1],
    "Direct_Prompt":      [1.3, 0.9, 1.4, 1.0, 1.1, 0.8, 0.7],
    "Simplify":           [1.1, 0.8, 0.9, 0.9, 0.8, 1.1, 1.3],
}


def build_observation_model() -> np.ndarray:
    """
    Construct Omega[a][s'][o] = P(o | s', a).

    Base distribution is state-driven; action provides a secondary
    multiplicative modulation. All rows are clamped and normalised.
    """
    O = np.zeros((n_a, n_s, n_o))

    for a_idx, action in enumerate(ACTIONS):
        mod = np.array(_ACTION_OBS_MOD[action])
        for s in range(n_s):
            t, l = state_components(s)
            probs = _base_obs_probs(t, l) * mod
            probs = np.maximum(probs, 1e-3)
            probs /= probs.sum()
            O[a_idx, s] = probs

    return O


# ── Reward Function R[s][a] ──────────────────────────────────────────

def build_reward_model() -> np.ndarray:
    """
    R[s][a] = immediate expected reward for action a in state s.

    Rewards encode the clinical goal: maximise medicL interventjon adherence
    (which correlates with high trust, low load) whilst penalising
    actions that are inappropriate for the current state.
    """
    R = np.zeros((n_s, n_a))

    for s in range(n_s):
        t, l = state_components(s)

        for a_idx, action in enumerate(ACTIONS):
            # -- intrinsic state value --
            trust_r = (2 - t) * 2.0       # High=4, Med=2, Low=0
            load_p = l * (-1.0)            # Low=0, Med=-1, High=-2
            r = trust_r + load_p

            # -- context-sensitive action penalties / bonuses --
            if action == "Direct_Prompt" and t == 2:
                r -= 3.0   # assertive prompt when trust is low -> damages rapport
            if action == "Explain_Importance" and l == 2:
                r -= 2.0   # lengthy explanation when cognitively overloaded -> counterproductive
            if action == "Withdrawal" and t == 0 and l == 0:
                r -= 1.0   # backing off when everything is fine -> missed opportunity
            if action == "Simplify" and l == 2:
                r += 2.0   # simplifying under high load -> appropriate support
            if action == "Encourage" and t == 1:
                r += 1.5   # encouragement for uncertain user -> trust-building
            if action == "Gentle_Reminder" and t == 0:
                r += 1.0   # gentle approach with trusting user -> natural

            R[s, a_idx] = r

    return R


# ── Belief Update ────────────────────────────────────────────────────

def belief_update(belief: np.ndarray, action: int, obs: int,
                  T: np.ndarray, O: np.ndarray) -> np.ndarray:
    """
    Bayesian belief update (the SE update / discrete Bayes filter):

        b'(s') = eta * Omega(o | s', a) * SUM_s T(s' | s, a) * b(s)

    This is the cognitive core: the robot revises its internal model of
    the user after every interaction, analogous to Bayesian theory of mind.
    """
    # prediction step
    b_pred = T[action].T @ belief

    # correction step (incorporate observation likelihood)
    b_new = O[action, :, obs] * b_pred

    # normalise
    total = b_new.sum()
    if total > 1e-12:
        b_new /= total
    else:
        b_new = np.ones(n_s) / n_s   # degenerate -> reset to uniform

    return b_new


# ── QMDP Solver ──────────────────────────────────────────────────────

class QMDPSolver:
    """
    QMDP approximation for POMDP action selection.

    1- Solve the underlying fully-observable MDP via value iteration
       to obtain Q(s, a).
    2- At decision time, weight Q-values by the current belief:
           a* = argmax_a  SUM_s  b(s) * Q(s, a)

    This realises prospection: the robot anticipates future outcomes
    across multiple time-steps before committing to an action, rather
    than reacting to immediate sensory signals alone.

    Reference:
        Littman, M. L., Cassandra, A. R. and Kaelbling, L. P. (1995)
        'Learning policies for partially observable environments: Scaling up',
        Proceedings of the 12th International Conference on Machine Learning,
        pp. 362-370.
    """

    def __init__(self, T: np.ndarray, R: np.ndarray,
                 gamma: float = 0.95, n_iterations: int = 200):
        self.T = T
        self.R = R
        self.gamma = gamma
        self.Q = self._value_iteration(n_iterations)

    def _value_iteration(self, n_iter: int) -> np.ndarray:
        """Standard Bellman backup: Q(s,a) = R(s,a) + gamma * E[V(s') | s,a]."""
        V = np.zeros(n_s)
        Q = np.zeros((n_s, n_a))

        for _ in range(n_iter):
            for a in range(n_a):
                Q[:, a] = self.R[:, a] + self.gamma * (self.T[a] @ V)
            V = Q.max(axis=1)

        return Q

    def select_action(self, belief: np.ndarray) -> int:
        """Belief-weighted action selection (QMDP policy)."""
        return int(np.argmax(belief @ self.Q))

    def action_values(self, belief: np.ndarray) -> np.ndarray:
        """Belief-weighted Q-values for all actions."""
        return belief @ self.Q
