"""
    LECTURE 10 (LfD / IRL) -- WEAVE INTO REPORT
    ==============================================
    This is the theoretical layer that elevates the report from
    "I built a POMDP" to "I understand where CRAMS sits within
    cognitive robotics theory." Use Dr. Aly's exact terminology.

    REPORT SECTION: Introduction (10%)
    - [ ] TODO: Frame the *problem* using Dr. Aly's LfD rationale:
          "Programming robots is hard; huge number of possible tasks,
          unique environmental demands, tasks difficult to describe
          formally." This justifies why CRAMS uses a learning approach
          (POMDP) rather than hand-coded behavioural rules
    - [ ] TODO: State that CRAMS performs **implicit knowledge transfer**:
          the robot never directly observes the user's trust or cognitive
          load; it must infer them from behavioural cues

    REPORT SECTION: Background (10%)
    - [ ] TODO: Position CRAMS within the LfD taxonomy: it is an
          **External Observation / Imitation** system (Slide 14 of
          Lecture 10); the robot observes the user without direct sensor
          access to internal states, and embodiment correspondence is
          inferred
    - [ ] TODO: Explicitly name **Inverse Reinforcement Learning (IRL)**
          as the theoretical paradigm: CRAMS infers the user's implicit
          "reward" (compliance/engagement) from behavioural cues rather
          than receiving an explicit reward signal. Quote Dr. Aly:
          "You don't have a reward, but you have an expert. So you try
          to learn this reward in some sense."
    - [ ] TODO: Draw the formal parallel: LfD's (S, A, Z, M, pi) maps
          to CRAMS's POMDP tuple (S, A, O, T, Omega, R, gamma);
          Z = O, M = Omega, pi = QMDP policy

    REPORT SECTION: Method and Setup (35%)
    - [ ] TODO: Describe the OpenAI API perception layer as the
          **mapping function M** that solves the **correspondence
          problem** (high-dimensional human behaviour to 7 discrete
          observations)
    - [ ] TODO: Explain QMDP value iteration as the **policy derivation**
          mechanism (Dr. Aly's term)
    - [ ] TODO: Note that CRAMS uses **interactive** (not batch) training;
          beliefs update continuously each step, which aligns with the
          incremental policy development mode from Slide 9
    - [ ] TODO: Frame the observation model Omega(o|s',a) as learning
          the **underlying pattern** (Dr. Aly's preferred ML expression)
          behind user behavioural responses

    REPORT SECTION: Results/Outcome (30%)
    - [ ] TODO: Frame multi-scenario comparison (cooperative, uncertain,
          resistant) as addressing **problem space continuity**: the agent
          generalises learned behaviour to new situations similar to
          demonstrated ones (Slide 9)
    - [ ] TODO: Present belief evolution plots as evidence the robot
          learns the **underlying pattern** of user behaviour
    - [ ] TODO: Frame MetaReasoner adaptation as the **IRL mechanism**:
          when inferred reward declines, the robot adjusts strategy,
          exactly as Dr. Aly described with the obstacle-avoidance
          reward inference example

    REPORT SECTION: Conclusion (10%)
    - [ ] TODO: Future work: **transfer learning** between user profiles
          (directly from Dr. Aly's Lecture 10 tangent); a CRAMS agent
          trained on cooperative users could fine-tune to resistant users,
          analogous to his Alzheimer's/related-disorder example
    - [ ] TODO: Future work: moving from External Observation to Sensors
          on Teacher (wearable physiological sensors for direct trust/load
          measurement), thereby shifting from **imitation** to
          **demonstration** in Dr. Aly's taxonomy and eliminating the
          correspondence problem
    - [ ] TODO: Limitation: acknowledge CRAMS currently uses a pre-defined
          reward function R(s,a) rather than pure IRL; the reward is
          designed, not fully inferred. The meta-reasoner partially
          addresses this gap

    CODE DOCUMENTATION
    - [ ] TODO: Add a comment block in the POMDP engine (Section 1)
          explaining CRAMS's position in the LfD taxonomy (External
          Observation / Imitation)
    - [ ] TODO: Add a comment block at MetaReasoner explaining the IRL
          connection (inferring reward from declining performance trends)

    KEY TERMINOLOGY CHECKLIST (use each at least once in report)
    - [ ] "underlying pattern"
    - [ ] "mapping function"
    - [ ] "inverse reinforcement learning"
    - [ ] "policy derivation"
    - [ ] "correspondence problem"
    - [ ] "implicit knowledge transfer"
    - [ ] "problem space continuity"
    - [ ] "external observation"

    - [ ] TODO: talk about the LfD (learn-from-demonstration)
    - [ ] TODO: talk about IRL (inverse reinforcement learning)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from collections import deque
from dataclasses import dataclass
from typing import List, Optional, Tuple
import sqlite3
import json
import time
import os
import uuid


# --------------------------------------------------------------------
#  SECTION 1 -- POMDP ENGINE
# --------------------------------------------------------------------

# ── State Space ──
# 2-D hidden state: (Trust, CognitiveLoad), each with 3 levels -> 9 states.
# The robot never observes these directly; it maintains a belief distribution.

TRUST_LEVELS = ["High", "Medium", "Low"]
LOAD_LEVELS = ["Low", "Medium", "High"]

STATES = [f"T:{t}_L:{c}" for t in TRUST_LEVELS for c in LOAD_LEVELS]
# Index 0 = (High trust, Low load)  -- best case
# Index 8 = (Low trust, High load)  -- worst case

# ── Action Space ──
# Actions the cognitive robot can take during a medication adherence episode.

ACTIONS = [
    "Gentle_Reminder",       # simple, non-intrusive prompt
    "Explain_Importance",    # explain why medication matters (trust-building)
    "Back_Off",              # withdraw, give space (load-reducing)
    "Encourage",             # positive reinforcement
    "Direct_Prompt",         # assertive, clear instruction
    "Simplify",              # break task into smaller steps (load-reducing)
]

# ── Observation Space ──
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

n_s = len(STATES)         # 9
n_a = len(ACTIONS)        # 6
n_o = len(OBSERVATIONS)   # 7

# ── Personality Presets ────────────────────────────────────────────
# Each personality tunes the ratio between reward (behaviour the robot
# encourages) and penalty (behaviour it discourages).  A cautious robot
# weighs penalties higher, producing patient-respecting, conservative
# action selection; an assertive robot weighs bonuses higher, pushing
# harder for medication compliance at the risk of damaging rapport.
#
# Keys:
#   bonus_w   -- multiplier on context-sensitive bonuses in R(s,a)
#   penalty_w -- multiplier on context-sensitive penalties in R(s,a)
#   load_w    -- multiplier on intrinsic load penalty (higher = more
#                sensitive to cognitive overload)
#   trust_w   -- multiplier on intrinsic trust reward

PERSONALITIES={
    "cautious":{
        "bonus_w":0.8,"penalty_w":1.5,"load_w":1.5,"trust_w":1.0,
        "desc":"Patient-first: penalises mismatched actions heavily, "
               "backs off readily under high load",
    },
    "balanced":{
        "bonus_w":1.0,"penalty_w":1.0,"load_w":1.0,"trust_w":1.0,
        "desc":"Default: equal weighting of encouragement and discouragement",
    },
    "assertive":{
        "bonus_w":1.3,"penalty_w":0.7,"load_w":0.8,"trust_w":1.3,
        "desc":"Goal-driven: pursues compliance aggressively, tolerates "
               "higher load before backing off",
    },
}


# ── Index helpers ──

def state_idx(trust: int, load: int) -> int:
    """Flat index from (trust_level_idx, load_level_idx)."""
    return trust * len(LOAD_LEVELS) + load


def state_components(idx: int) -> Tuple[int, int]:
    """Return (trust_idx, load_idx) from flat state index."""
    return divmod(idx, len(LOAD_LEVELS))


# ── Transition Model T[a][s][s'] ──
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


# ── Observation Model Omega[a][s'][o] ───────────────────────────────

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


# ── Reward Function R[s][a] ──
#
# Design rationale (anti-pestering):
#   The reward is NOT a simple "+100 for compliance, -10 for annoyance"
#   structure.  That ratio (10:1) would teach the robot that pestering
#   is net-positive, because the upside of compliance dwarfs the penalty.
#   Instead, reward is a function of the *hidden state* (trust x load),
#   meaning the robot must maintain trust as a necessary precondition for
#   compliance.  Context-sensitive penalties further punish actions that
#   are mismatched to the current state, ensuring the robot cannot brute-
#   force adherence through relentless prompting.
#
#   An additional REPETITION_PENALTY (applied at action-selection time,
#   not within R itself) discounts recently-repeated actions, preventing
#   the POMDP from converging on a single strategy.

def build_reward_model(personality: str="balanced") -> np.ndarray:
    """
    R[s][a] = immediate expected reward for action a in state s.

    Rewards encode the clinical goal: maximise medication adherence
    (which correlates with high trust, low load) whilst penalising
    actions that are inappropriate for the current state.

    The personality parameter scales the ratio between encouragement
    and discouragement, producing distinct robot attitudes from the
    same underlying reward structure.
    """
    p=PERSONALITIES[personality]
    tw,lw=p["trust_w"],p["load_w"]
    bw,pw=p["bonus_w"],p["penalty_w"]

    R=np.zeros((n_s,n_a))

    for s in range(n_s):
        t,l=state_components(s)

        for a_idx,action in enumerate(ACTIONS):
            # -- intrinsic state value (scaled by personality) --
            trust_r=(2-t)*2.0*tw       # High=4*tw, Med=2*tw, Low=0
            load_p=l*(-1.0)*lw         # Low=0, Med=-1*lw, High=-2*lw
            r=trust_r+load_p

            # -- context-sensitive action penalties (scaled by pw) --
            penalty=0.0

            if action=="Direct_Prompt" and t==2:
                penalty+=3.0   # assertive prompt when trust is low -> damages rapport
            if action=="Explain_Importance" and l==2:
                penalty+=2.0   # lengthy explanation when cognitively overloaded
            if action=="Simplify" and l==0:
                penalty+=2.5   # oversimplifying for capable user -> patronising
            if action=="Simplify" and l==1:
                penalty+=0.5   # premature simplification at medium load
            if action=="Direct_Prompt" and l==2:
                penalty+=1.5   # assertive pressure on strained user -> overwhelm
            if action=="Encourage" and t==2:
                penalty+=1.5   # positive reinforcement from untrusted source
            if action=="Gentle_Reminder" and t==2:
                penalty+=1.0   # gentle nudge ineffective without trust
            if action=="Back_Off" and t==0 and l==0:
                penalty+=1.0   # backing off when everything is fine
            if action=="Back_Off" and t<=1 and l<=1:
                penalty+=1.0   # withdrawing from engaged, manageable user

            # -- context-sensitive action bonuses (scaled by bw) --
            bonus=0.0

            if action=="Gentle_Reminder" and t==0 and l<=1:
                bonus+=3.0   # gentle nudge for cooperative, unloaded user
            if action=="Simplify" and l==2:
                bonus+=2.5   # appropriate cognitive support under high load
            if action=="Back_Off" and l==2:
                bonus+=2.5   # pressure relief when overwhelmed
            if action=="Encourage" and t==1:
                bonus+=2.0   # rapport-building at the trust tipping point
            if action=="Back_Off" and t==2 and l>=1:
                bonus+=2.0   # respecting autonomy when trust is absent
            if action=="Explain_Importance" and t>=1 and l<=1:
                bonus+=1.5   # educational approach when user can listen
            if action=="Direct_Prompt" and t==0 and l==0:
                bonus+=1.5   # clear instruction welcomed by cooperative user

            R[s,a_idx]=r - penalty*pw + bonus*bw

    return R


# ── Belief Update ──

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


# ── QMDP Solver ──

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


# ---------------------------------------------------------------------
#  SECTION 2 -- COGNITIVE MODULES
# ---------------------------------------------------------------------

# ── Anti-Pestering Configuration ────────────────────────────────────
# Q-value penalty applied when the robot repeats the same action within
# a short window.  Without this, the POMDP can converge on a single
# high-reward action and use it relentlessly, which in a medical context
# amounts to pestering the patient.  The penalty forces action diversity,
# ensuring the robot adapts its approach rather than hammering one strategy.
REPETITION_PENALTY = 1.5
REPETITION_WINDOW  = 3      # look-back horizon (last N actions)
REPETITION_THRESH  = 2      # trigger penalty when count >= this


# ── Persistent Storage (SQLite) ─────────────────────────────────────
# Lecture 9 (Vernon, 2014) distinguishes episodic memory (specific past
# events) from semantic memory (generalised knowledge about the world).
# In-memory structures serve the current session; SQLite ensures both
# memory types survive between sessions, enabling longitudinal adaptation
# to a specific user.
#
# Schema:
#   episodes        -- individual interaction records (episodic memory)
#   semantic_memory -- accumulated user knowledge (semantic memory)
#   sessions        -- session-level metadata for audit and analysis

class PersistentStore:
    """SQLite backend for cross-session cognitive memory."""

    def __init__(self, db_path: str = "crams_memory.db"):
        self.db_path = db_path
        self.session_id = str(uuid.uuid4())[:8]
        self.conn = sqlite3.connect(db_path)
        self._create_tables()

    def _create_tables(self):
        c = self.conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS episodes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                step INTEGER NOT NULL,
                belief_before BLOB NOT NULL,
                action INTEGER NOT NULL,
                observation INTEGER NOT NULL,
                belief_after BLOB NOT NULL,
                reward REAL NOT NULL,
                timestamp REAL NOT NULL
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS semantic_memory (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                confidence REAL DEFAULT 0.5,
                updated_at REAL NOT NULL
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                started_at REAL NOT NULL,
                total_steps INTEGER DEFAULT 0,
                total_reward REAL DEFAULT 0.0,
                compliance_rate REAL DEFAULT 0.0
            )
        """)
        c.execute(
            "INSERT INTO sessions (session_id, started_at) VALUES (?, ?)",
            (self.session_id, time.time()),
        )
        self.conn.commit()

    def save_episode(self, episode):
        """Persist a single interaction episode."""
        c = self.conn.cursor()
        c.execute(
            "INSERT INTO episodes (session_id, step, belief_before, action, "
            "observation, belief_after, reward, timestamp) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (self.session_id, episode.step,
             episode.belief_before.tobytes(), episode.action,
             episode.observation, episode.belief_after.tobytes(),
             episode.reward, time.time()),
        )
        self.conn.commit()

    def load_past_episodes(self, limit: int = 100):
        """Retrieve episodes from previous sessions for long-term recall."""
        c = self.conn.cursor()
        c.execute(
            "SELECT step, belief_before, action, observation, "
            "belief_after, reward FROM episodes "
            "WHERE session_id != ? ORDER BY id DESC LIMIT ?",
            (self.session_id, limit),
        )
        episodes = []
        for row in c.fetchall():
            episodes.append(Episode(
                step=row[0],
                belief_before=np.frombuffer(row[1], dtype=np.float64).copy(),
                action=row[2],
                observation=row[3],
                belief_after=np.frombuffer(row[4], dtype=np.float64).copy(),
                reward=row[5],
            ))
        return episodes

    def update_semantic(self, key: str, value: str, confidence: float = 0.5):
        """Store or update a semantic memory entry."""
        c = self.conn.cursor()
        c.execute(
            "INSERT OR REPLACE INTO semantic_memory "
            "(key, value, confidence, updated_at) VALUES (?, ?, ?, ?)",
            (key, value, confidence, time.time()),
        )
        self.conn.commit()

    def get_semantic(self, key: str):
        """Retrieve a single semantic memory entry (or None)."""
        c = self.conn.cursor()
        c.execute("SELECT value FROM semantic_memory WHERE key = ?", (key,))
        row = c.fetchone()
        return row[0] if row else None

    def get_all_semantic(self) -> dict:
        """Retrieve every semantic memory entry."""
        c = self.conn.cursor()
        c.execute("SELECT key, value, confidence FROM semantic_memory")
        return {
            row[0]: {"value": row[1], "confidence": row[2]}
            for row in c.fetchall()
        }

    def finalise_session(self, total_steps: int, total_reward: float,
                         compliance_rate: float):
        """Update session record with final statistics."""
        c = self.conn.cursor()
        c.execute(
            "UPDATE sessions SET total_steps = ?, total_reward = ?, "
            "compliance_rate = ? WHERE session_id = ?",
            (total_steps, total_reward, compliance_rate, self.session_id),
        )
        self.conn.commit()

    def close(self):
        self.conn.close()


# ── Episode Dataclass ───────────────────────────────────────────────

@dataclass
class Episode:
    """Single interaction record in episodic memory."""
    step: int
    belief_before: np.ndarray
    action: int
    observation: int
    belief_after: np.ndarray
    reward: float

    @property
    def action_name(self) -> str:
        return ACTIONS[self.action]

    @property
    def obs_name(self) -> str:
        return OBSERVATIONS[self.observation]


# ── Episodic Memory ──
# Stores past interaction episodes so the robot can recall what worked
# and what did not.  Implements episodic future thinking: past events
# are reconstructed to allow the agent to pre-experience the future.
#
# When backed by a PersistentStore (SQLite), episodes survive between
# sessions, enabling longitudinal learning across multiple interactions
# with the same user.
#
# Reference:
#   Atance, C. M. and O'Neill, D. K. (2001) 'Episodic future thinking',
#   Trends in Cognitive Sciences, 5(12), pp. 533-539.

class EpisodicMemory:
    """
    Capacity-limited store of past interaction episodes.

    recall_similar() retrieves episodes whose belief state most closely
    resembles the current belief -- the robot reconstructs past situations
    to inform future action, analogous to episodic future thinking.
    """

    def __init__(self, capacity: int = 200,
                 db: Optional[PersistentStore] = None):
        self.episodes: deque = deque(maxlen=capacity)
        self.db = db

        # load episodes from previous sessions (long-term episodic memory)
        self.long_term: List[Episode] = []
        if db:
            self.long_term = db.load_past_episodes(limit=100)

    def store(self, episode: Episode):
        """Append to current-session memory and persist to SQLite."""
        self.episodes.append(episode)
        if self.db:
            self.db.save_episode(episode)

    def recall_similar(self, belief: np.ndarray,
                       top_k: int = 5) -> List[Episode]:
        """
        Retrieve episodes with most similar belief state (cosine similarity).

        Searches both current-session episodes and long-term memory from
        previous sessions, with a slight recency bias towards the current
        session so that recent experience is weighted more heavily.
        """
        current = list(self.episodes)
        all_episodes = current + self.long_term
        if not all_episodes:
            return []

        current_set = set(id(ep) for ep in current)
        sims = []
        for ep in all_episodes:
            denom = (np.linalg.norm(belief)
                     * np.linalg.norm(ep.belief_before) + 1e-10)
            sim = np.dot(belief, ep.belief_before) / denom
            # slight recency bias for current-session episodes
            if id(ep) in current_set:
                sim *= 1.05
            sims.append((sim, ep))

        sims.sort(key=lambda x: x[0], reverse=True)
        return [ep for _, ep in sims[:top_k]]

    def action_success_rate(self, action_idx: int,
                            window: int = 20) -> float:
        """Fraction of recent uses of action that yielded Comply or Nod."""
        recent = list(self.episodes)[-window:]
        relevant = [ep for ep in recent if ep.action == action_idx]
        if not relevant:
            return 0.5
        successes = sum(1 for ep in relevant if ep.observation in [0, 5])
        return successes / len(relevant)


# ── Semantic Memory ──
# Whilst episodic memory stores specific interaction events, semantic
# memory stores generalised knowledge that persists across sessions:
#   - User's baseline trust level
#   - Which actions historically work best for this user
#   - Final belief from previous session (used as prior for next)
#
# This maps to the distinction Aly draws in Lecture 9 between episodic
# memory (past experience reconstruction) and semantic memory (knowledge
# of the world).
#
# Reference:
#   Vernon, D. (2014) Artificial Cognitive Systems: A Primer.
#   Cambridge, MA: MIT Press.  (slides 24, 28)

class SemanticMemory:
    """Cross-session knowledge about the user and the world."""

    def __init__(self, db: Optional[PersistentStore] = None):
        self.db = db
        self._cache: dict = {}
        if db:
            self._cache = db.get_all_semantic()

    def store(self, key: str, value: str, confidence: float = 0.5):
        """Store a semantic fact."""
        self._cache[key] = {"value": value, "confidence": confidence}
        if self.db:
            self.db.update_semantic(key, value, confidence)

    def recall(self, key: str) -> Optional[str]:
        """Recall a semantic fact (or None)."""
        entry = self._cache.get(key)
        return entry["value"] if entry else None

    def get_prior_belief(self) -> Optional[np.ndarray]:
        """
        Retrieve a prior belief from semantic memory for session init.

        If past sessions exist, the final belief from the most recent
        session serves as a prior for the next, rather than starting
        from uniform.  This enables cross-session adaptation.
        """
        prior_str = self.recall("last_session_final_belief")
        if prior_str:
            try:
                arr = np.array(json.loads(prior_str))
                if len(arr) == n_s and arr.sum() > 0:
                    return arr / arr.sum()
            except (json.JSONDecodeError, ValueError):
                pass
        return None

    def update_from_session(self, agent):
        """
        Distil session-level knowledge into persistent semantic facts.

        Called at the end of a session to record what the robot learned:
        final belief state, best-performing action, compliance rate, etc.
        """
        if not agent.action_history:
            return

        # store final belief as prior for next session
        self.store(
            "last_session_final_belief",
            json.dumps(agent.belief.tolist()),
            confidence=0.7,
        )

        # identify best-performing action across the session
        if agent.reward_history:
            action_rewards: dict = {}
            for i, a in enumerate(agent.action_history[:-1]):
                if i < len(agent.reward_history):
                    action_rewards.setdefault(a, []).append(
                        agent.reward_history[i]
                    )
            if action_rewards:
                best = max(action_rewards,
                           key=lambda a: np.mean(action_rewards[a]))
                self.store(
                    "best_performing_action",
                    ACTIONS[best],
                    confidence=min(
                        0.9, 0.5 + len(agent.reward_history) * 0.01
                    ),
                )

        # store compliance rate
        if agent.obs_history:
            rate = agent.obs_history.count(0) / len(agent.obs_history)
            self.store("last_compliance_rate", f"{rate:.3f}", confidence=0.8)


# ── Meta-Reasoning ──
# The robot monitors its own performance and triggers strategy adaptation
# when reward trends decline -- reasoning about reasoning.
#
# Reference:
#   Vernon, D. (2014) Artificial Cognitive Systems: A Primer.
#   Cambridge, MA: MIT Press.

class MetaReasoner:
    """
    Metacognition module: detects when the robot's current policy is
    producing declining outcomes and injects exploration to escape
    ineffective action loops.
    """

    def __init__(self, window: int = 5, decline_threshold: float = -0.3):
        self.window = window
        self.decline_threshold = decline_threshold
        self.reward_history: List[float] = []
        self.adaptation_log: List[dict] = []

    def record(self, reward: float):
        self.reward_history.append(reward)

    def should_adapt(self) -> bool:
        """Compare recent reward window to previous window."""
        if len(self.reward_history) < 2 * self.window:
            return False
        recent = np.mean(self.reward_history[-self.window:])
        previous = np.mean(
            self.reward_history[-2 * self.window:-self.window]
        )
        return (recent - previous) < self.decline_threshold

    def get_exploration_boost(self) -> float:
        """Return exploration probability when adaptation is triggered."""
        if self.should_adapt():
            self.adaptation_log.append({
                "step": len(self.reward_history),
                "recent_mean": float(
                    np.mean(self.reward_history[-self.window:])
                ),
            })
            return 0.3
        return 0.0


# ---------------------------------------------------------------------
#  SECTION 3 -- SIMULATED USER
# ---------------------------------------------------------------------
# Replaces the OpenAI API perception layer for offline testing.
# In deployment on the NAO, the API would map camera/microphone input
# to one of the OBSERVATIONS categories; here the user samples from the
# same observation model directly.

class SimulatedUser:
    """Probabilistic user with a hidden true state that evolves over time."""

    def __init__(self, true_state_idx: int = 4):
        self.true_state = true_state_idx
        self.history: List[int] = [true_state_idx]

    def respond(self, action_idx: int, O: np.ndarray) -> int:
        """Sample observation from P(o | true_state, action)."""
        probs = O[action_idx, self.true_state]
        return int(np.random.choice(n_o, p=probs))

    def evolve(self, action_idx: int, T: np.ndarray):
        """True state transitions according to T(s' | s, a)."""
        probs = T[action_idx, self.true_state]
        self.true_state = int(np.random.choice(n_s, p=probs))
        self.history.append(self.true_state)


# ---------------------------------------------------------------------
#  SECTION 4 -- CRAMS AGENT
# ---------------------------------------------------------------------

class CRAMSAgent:
    """
    Cognitive Robot for Adaptive Medical Support.

    Integrates:
        - POMDP belief tracking   (learning / perception)
        - QMDP policy             (reasoning / prospection)
        - Episodic memory         (short-term, session-scoped)
        - Semantic memory         (long-term, cross-session via SQLite)
        - Meta-reasoning          (metacognition)
        - Anti-pestering guard    (repetition penalty)

    Cognitive cycle per interaction step:
        1. Receive observation from user
        2. Bayesian belief update            (learning)
        3. Recall similar past episodes      (episodic memory)
        4. QMDP action-value computation     (prospection)
        5. Memory-informed bias              (episodic future thinking)
        6. Repetition penalty                (anti-pestering)
        7. Meta-reasoning check              (metacognition)
        8. Action selection                  (action selection)
    """

    def __init__(self, gamma: float=0.95,
                 db_path: Optional[str]="crams_memory.db",
                 personality: str="balanced"):
        self.personality=personality
        # build POMDP model
        self.T=build_transition_model()
        self.O=build_observation_model()
        self.R=build_reward_model(personality)

        # prospective planner
        self.solver=QMDPSolver(self.T,self.R,gamma)

        # persistent storage (SQLite)
        self.db = PersistentStore(db_path) if db_path else None

        # semantic memory: cross-session knowledge (Vernon, 2014)
        self.semantic = SemanticMemory(self.db)

        # initial belief: use semantic prior if available, else uniform
        prior = self.semantic.get_prior_belief()
        if prior is not None:
            self.belief = prior
        else:
            self.belief = np.ones(n_s) / n_s

        # episodic memory: session + long-term recall
        self.memory = EpisodicMemory(capacity=200, db=self.db)
        self.meta = MetaReasoner(window=4, decline_threshold=-0.2)

        # history for visualisation
        self.belief_history: List[np.ndarray] = [self.belief.copy()]
        self.action_history: List[int] = []
        self.obs_history: List[int] = []
        self.reward_history: List[float] = []

    def select_action(self, step: int) -> int:
        """
        Full cognitive pipeline for action selection.

        1- QMDP computes prospective action values (forward planning)
        2- Episodic memory biases towards historically successful actions
        3- Repetition penalty discourages pestering (anti-pestering guard)
        4- Meta-reasoning injects exploration if performance is declining
        """
        # -- prospective planning --
        q_values = self.solver.action_values(self.belief).copy()

        # -- episodic memory bias --
        similar = self.memory.recall_similar(self.belief, top_k=5)
        if similar:
            bonus = np.zeros(n_a)
            for ep in similar:
                bonus[ep.action] += ep.reward * 0.1
            q_values += bonus

        # -- anti-pestering: penalise recently repeated actions --
        # If the robot uses the same action multiple times in recent
        # steps, it receives a Q-value penalty.  This prevents the
        # failure mode where maximising compliance reward leads to
        # relentless prompting of the patient.
        if len(self.action_history) >= REPETITION_THRESH:
            recent = self.action_history[-REPETITION_WINDOW:]
            for a_idx in range(n_a):
                count = recent.count(a_idx)
                if count >= REPETITION_THRESH:
                    q_values[a_idx] -= REPETITION_PENALTY * (count - 1)

        # -- meta-reasoning: exploration on performance decline --
        exploration = self.meta.get_exploration_boost()
        if exploration > 0 and np.random.random() < exploration:
            weights = np.array([
                max(self.memory.action_success_rate(a), 0.1)
                for a in range(n_a)
            ])
            weights /= weights.sum()
            return int(np.random.choice(n_a, p=weights))

        return int(np.argmax(q_values))

    def step(self, observation: int, step_num: int) -> int:
        """
        Process one interaction cycle:
            receive observation -> update belief -> store episode ->
            meta-check -> select next action
        """
        old_belief = self.belief.copy()
        prev_action = self.action_history[-1]

        # -- Bayesian belief update (learning) --
        self.belief = belief_update(
            self.belief, prev_action, observation, self.T, self.O
        )
        self.belief_history.append(self.belief.copy())
        self.obs_history.append(observation)

        # -- expected reward under previous belief --
        reward = float(self.R[:, prev_action] @ old_belief)
        self.reward_history.append(reward)
        self.meta.record(reward)

        # -- store in episodic memory (persists to SQLite if db exists) --
        self.memory.store(Episode(
            step=step_num,
            belief_before=old_belief,
            action=prev_action,
            observation=observation,
            belief_after=self.belief.copy(),
            reward=reward,
        ))

        # -- select next action --
        action = self.select_action(step_num)
        self.action_history.append(action)
        return action

    def finalise(self, n_steps: int):
        """
        End-of-session housekeeping: persist semantic knowledge and
        update the session record in SQLite.
        """
        self.semantic.update_from_session(self)

        if self.db:
            compliance = (self.obs_history.count(0) / n_steps * 100
                          if n_steps > 0 else 0.0)
            self.db.finalise_session(
                total_steps=n_steps,
                total_reward=sum(self.reward_history),
                compliance_rate=compliance,
            )
            self.db.close()


# =====================================================================
#  SECTION 5 -- SIMULATION & VISUALISATION
# =====================================================================

def run_simulation(n_steps: int=30, initial_state: int=4,
                   seed: int=42, stress_step: Optional[int]=15,
                   db_path: Optional[str]="crams_memory.db",
                   personality: str="balanced"):
    """
    Run CRAMS and produce comprehensive visualisation.

    Parameters
    ----------
    n_steps : int
        Number of interaction rounds.
    initial_state : int
        User's starting hidden state index (default 4 = Medium trust,
        Medium load).
    seed : int
        Random seed for reproducibility.
    stress_step : int or None
        If set, at this step the user's load jumps to High (simulates
        an external stressor) to demonstrate adaptive behaviour.
    db_path : str or None
        Path to SQLite database for persistent memory. None disables
        persistence (pure in-memory simulation).
    personality : str
        Robot personality preset: "cautious", "balanced", or "assertive".
        Controls the ratio between reward bonuses and penalties.
    """
    np.random.seed(seed)

    agent=CRAMSAgent(gamma=0.95,db_path=db_path,personality=personality)
    user = SimulatedUser(true_state_idx=initial_state)

    pdesc=PERSONALITIES[personality]["desc"]
    print("="*70)
    print("  CRAMS -- Cognitive Robot for Adaptive Medical Support")
    print("  POMDP-based Medication Adherence Simulation")
    print("="*70)
    print(f"\n  Personality        : {personality} -- {pdesc}")
    print(f"  Initial user state : {STATES[initial_state]}")
    print(f"  Simulation steps   : {n_steps}")
    if stress_step:
        print(f"  Stress event at    : step {stress_step}")
    if db_path:
        print(f"  Persistent memory  : {db_path}")
    print()

    # -- initial action (belief prior, no observation yet) --
    action = agent.select_action(0)
    agent.action_history.append(action)

    for step in range(n_steps):
        # inject stress event
        if stress_step and step == stress_step:
            t_curr, _ = state_components(user.true_state)
            user.true_state = state_idx(t_curr, 2)  # load -> High
            print(
                f"  {'':6s}>>> STRESS EVENT: cognitive load increased <<<\n"
            )

        # user responds to robot's action
        obs = user.respond(action, agent.O)

        # user's true state evolves
        user.evolve(action, agent.T)

        # robot processes observation, selects next action
        action = agent.step(obs, step)

        # console log
        t, l = state_components(user.true_state)
        adapting = agent.meta.should_adapt()
        flag = " [META-ADAPT]" if adapting else ""
        print(
            f"  Step {step + 1:2d} | "
            f"Act: {ACTIONS[agent.action_history[-2]]:20s} | "
            f"Obs: {OBSERVATIONS[obs]:15s} | "
            f"True: T={TRUST_LEVELS[t]}, L={LOAD_LEVELS[l]}{flag}"
        )

    # -- finalise session (persist semantic knowledge to SQLite) --
    agent.finalise(n_steps)

    # -- visualisation --
    _plot_results(agent, user, n_steps, stress_step)
    _print_summary(agent, n_steps)


def _plot_results(agent: CRAMSAgent, user: SimulatedUser,
                  n_steps: int, stress_step: Optional[int]):
    """Generate the 5-panel results figure."""
    fig = plt.figure(figsize=(16, 12))
    fig.suptitle(
        "CRAMS: Cognitive Robot for Adaptive Medical Support",
        fontsize=14, fontweight="bold", y=0.98,
    )
    gs = GridSpec(3, 2, figure=fig, hspace=0.38, wspace=0.28)
    belief_arr = np.array(agent.belief_history)
    steps = np.arange(len(belief_arr))

    # ---- panel 1: trust belief evolution ----
    ax1 = fig.add_subplot(gs[0, 0])
    trust_b = np.zeros((len(belief_arr), 3))
    for i, b in enumerate(belief_arr):
        for s in range(n_s):
            t, _ = state_components(s)
            trust_b[i, t] += b[s]
    ax1.stackplot(
        steps, trust_b.T,
        labels=["High Trust", "Medium Trust", "Low Trust"],
        colors=["#2ecc71", "#f39c12", "#e74c3c"], alpha=0.85,
    )
    if stress_step:
        ax1.axvline(stress_step, color="k", ls="--", lw=1, alpha=0.5)
    ax1.set_ylabel("Belief Probability")
    ax1.set_title("Trust Belief Evolution")
    ax1.legend(loc="upper right", fontsize=8)
    ax1.set_xlim(0, len(belief_arr) - 1)
    ax1.set_ylim(0, 1)

    # ---- panel 2: load belief evolution ----
    ax2 = fig.add_subplot(gs[0, 1])
    load_b = np.zeros((len(belief_arr), 3))
    for i, b in enumerate(belief_arr):
        for s in range(n_s):
            _, l = state_components(s)
            load_b[i, l] += b[s]
    ax2.stackplot(
        steps, load_b.T,
        labels=["Low Load", "Medium Load", "High Load"],
        colors=["#3498db", "#9b59b6", "#e74c3c"], alpha=0.85,
    )
    if stress_step:
        ax2.axvline(stress_step, color="k", ls="--", lw=1, alpha=0.5)
    ax2.set_ylabel("Belief Probability")
    ax2.set_title("Cognitive Load Belief Evolution")
    ax2.legend(loc="upper right", fontsize=8)
    ax2.set_xlim(0, len(belief_arr) - 1)
    ax2.set_ylim(0, 1)

    # ---- panel 3: action timeline ----
    ax3 = fig.add_subplot(gs[1, :])
    action_colours = [
        "#2ecc71", "#3498db", "#95a5a6", "#f39c12", "#e74c3c", "#9b59b6",
    ]
    for i, a in enumerate(agent.action_history[:-1]):
        ax3.barh(a, 1, left=i, color=action_colours[a],
                 edgecolor="white", linewidth=0.5)
    ax3.set_yticks(range(n_a))
    ax3.set_yticklabels(ACTIONS, fontsize=9)
    ax3.set_xlabel("Interaction Step")
    ax3.set_title("Action Selections Over Time")
    if stress_step:
        ax3.axvline(stress_step, color="k", ls="--", lw=1.5, alpha=0.6)
        ax3.annotate("Stress\nEvent", xy=(stress_step, n_a - 0.3),
                     fontsize=8, ha="center", color="k")
    for entry in agent.meta.adaptation_log:
        ax3.axvline(entry["step"], color="red", ls=":", lw=1.5, alpha=0.7)

    # ---- panel 4: cumulative reward ----
    ax4 = fig.add_subplot(gs[2, 0])
    cum_r = np.cumsum(agent.reward_history)
    ax4.plot(cum_r, color="#2c3e50", linewidth=2)
    ax4.fill_between(range(len(cum_r)), cum_r, alpha=0.12, color="#2c3e50")
    if stress_step:
        ax4.axvline(stress_step, color="k", ls="--", lw=1, alpha=0.5)
    ax4.set_xlabel("Interaction Step")
    ax4.set_ylabel("Cumulative Reward")
    ax4.set_title("Cumulative Adherence Performance")

    # ---- panel 5: true state vs MAP belief ----
    ax5 = fig.add_subplot(gs[2, 1])
    n = min(len(user.history), len(agent.belief_history))
    true_s = user.history[:n]
    map_s = [int(np.argmax(b)) for b in agent.belief_history[:n]]
    ax5.plot(true_s, "o-", label="True State", color="#e74c3c",
             markersize=4, alpha=0.7)
    ax5.plot(map_s, "s-", label="MAP Belief", color="#3498db",
             markersize=4, alpha=0.7)
    if stress_step:
        ax5.axvline(stress_step, color="k", ls="--", lw=1, alpha=0.5)
    ax5.set_xlabel("Interaction Step")
    ax5.set_ylabel("State Index")
    ax5.set_title("True vs. Believed User State")
    ax5.legend(fontsize=8)

    plt.savefig("crams_simulation.png", dpi=150, bbox_inches="tight")
    print(f"\n  [Figure saved to crams_simulation.png]")
    plt.show()


def _print_summary(agent: CRAMSAgent, n_steps: int):
    """Print summary statistics to console."""
    print(f"\n{'=' * 70}")
    print("  Simulation Summary")
    print(f"{'=' * 70}")

    obs_counts = {
        OBSERVATIONS[o]: agent.obs_history.count(o) for o in range(n_o)
    }
    compliance = obs_counts.get("Comply", 0)
    compliance_rate = compliance / n_steps * 100

    print(f"  Compliance rate      : {compliance_rate:.1f}%"
          f"  ({compliance}/{n_steps})")
    print(f"  Total reward         : {sum(agent.reward_history):.2f}")
    print(f"  Meta-adaptations     : {len(agent.meta.adaptation_log)}")
    print(f"  Episodes in memory   : {len(agent.memory.episodes)}")
    print(f"  Long-term episodes   : {len(agent.memory.long_term)}")

    print(f"\n  Observation distribution:")
    for obs_name, count in sorted(obs_counts.items(), key=lambda x: -x[1]):
        bar = "#" * count
        print(f"    {obs_name:18s}: {count:2d}  {bar}")

    print(f"\n  Final belief (top 3):")
    top = np.argsort(agent.belief)[::-1][:3]
    for s in top:
        print(f"    {STATES[s]:22s} : {agent.belief[s]:.3f}")
    print()


# ── Multi-scenario comparison ──

def compare_scenarios(n_steps: int = 30):
    """
    Run three user profiles and compare CRAMS adaptation.
    Produces a side-by-side figure suitable for the report.
    """
    scenarios = [
        ("Cooperative (High Trust, Low Load)",  0, 42),
        ("Uncertain (Medium Trust, Med Load)",  4, 42),
        ("Resistant (Low Trust, High Load)",    8, 42),
    ]

    fig, axes = plt.subplots(len(scenarios), 2, figsize=(14, 10))
    fig.suptitle(
        "CRAMS: Adaptation Across User Profiles",
        fontsize=14, fontweight="bold",
    )

    for row, (name, init, seed) in enumerate(scenarios):
        np.random.seed(seed)
        agent = CRAMSAgent(db_path=None)  # no persistence for comparison
        user = SimulatedUser(init)

        action = agent.select_action(0)
        agent.action_history.append(action)

        for step in range(n_steps):
            obs = user.respond(action, agent.O)
            user.evolve(action, agent.T)
            action = agent.step(obs, step)

        # trust belief
        belief_arr = np.array(agent.belief_history)
        trust_b = np.zeros((len(belief_arr), 3))
        for i, b in enumerate(belief_arr):
            for s in range(n_s):
                t, _ = state_components(s)
                trust_b[i, t] += b[s]

        ax_trust = axes[row, 0]
        ax_trust.stackplot(
            range(len(belief_arr)), trust_b.T,
            colors=["#2ecc71", "#f39c12", "#e74c3c"], alpha=0.85,
        )
        ax_trust.set_ylabel("Belief")
        ax_trust.set_title(f"{name} -- Trust Belief")
        ax_trust.set_ylim(0, 1)

        # action distribution
        ax_act = axes[row, 1]
        act_colours = [
            "#2ecc71", "#3498db", "#95a5a6",
            "#f39c12", "#e74c3c", "#9b59b6",
        ]
        counts = [agent.action_history.count(a) for a in range(n_a)]
        ax_act.barh(range(n_a), counts, color=act_colours)
        ax_act.set_yticks(range(n_a))
        ax_act.set_yticklabels(ACTIONS, fontsize=8)
        ax_act.set_title(f"{name} -- Actions Used")

        compliance = agent.obs_history.count(0) / n_steps * 100
        ax_act.text(
            0.95, 0.05, f"Comply: {compliance:.0f}%",
            transform=ax_act.transAxes, ha="right", fontsize=9,
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
        )

    axes[-1, 0].set_xlabel("Interaction Step")
    axes[-1, 1].set_xlabel("Count")
    plt.tight_layout()
    plt.savefig("crams_comparison.png", dpi=150, bbox_inches="tight")
    print("  [Comparison figure saved to crams_comparison.png]")
    plt.show()


# ── Entry Point ──

if __name__=="__main__":
    # Primary simulation with stress event at step 15
    run_simulation(n_steps=30,initial_state=4,seed=42,stress_step=15,
                   personality="balanced")

    # Try different personalities to see how reward ratios shape behaviour:
    # run_simulation(n_steps=30,initial_state=4,seed=42,stress_step=15,
    #                personality="cautious")
    # run_simulation(n_steps=30,initial_state=4,seed=42,stress_step=15,
    #                personality="assertive")

    # Uncomment for multi-scenario comparison:
    # compare_scenarios()
