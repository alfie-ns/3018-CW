"""
CRAMS (Cognitive Robot for Adaptive Medical Support)

Runs a visual simulation of the POMDP-based cognitive robot interacting
with a simulated user across continuous medication adherence episodes.

Cognitive architecture (maps to Vernon, 2014):
    Perception:         -> OpenAI API (simulated here)
    Attention:          -> focus on trust / load signals
    Action selection:   -> QMDP policy over belief state
    Memory:             -> episodic memory of past interactions
    Learning:           -> Bayesian belief update
    Reasoning:          -> QMDP value iteration (prospection)
    Meta-reasoning:     -> self-check for declining performance
    Prospection:        -> forward simulation before acting

Pipeline:
    OpenAI API (perception) -> structured observation ->
    POMDP updates belief & selects action (memory / reasoning / prospection) ->
    OpenAI API translates action into language & gesture -> user responds ->
    cycle repeats
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from collections import deque
from dataclasses import dataclass
from typing import List, Optional

from pomdp import (
    STATES, ACTIONS, OBSERVATIONS, TRUST_LEVELS, LOAD_LEVELS,
    n_s, n_a, n_o,
    state_idx, state_components,
    build_transition_model, build_observation_model, build_reward_model,
    belief_update, QMDPSolver,
)


# ── Episodic Memory ──────────────────────────────────────────────────
# Stores past interaction episodes so the robot can recall what worked
# and what did not.  Implements episodic future thinking: past events
# are reconstructed to allow the agent to pre-experience the future.
#
# Reference:
#   Atance, C. M. and O'Neill, D. K. (2001) 'Episodic future thinking',
#   Trends in Cognitive Sciences, 5(12), pp. 533-539.


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


class EpisodicMemory:
    """
    Capacity-limited store of past interaction episodes.

    recall_similar() retrieves episodes whose belief state most closely
    resembles the current belief -- the robot reconstructs past situations
    to inform future action, analogous to episodic future thinking.
    """

    def __init__(self, capacity: int = 200):
        self.episodes: deque = deque(maxlen=capacity)

    def store(self, episode: Episode):
        self.episodes.append(episode)

    def recall_similar(self, belief: np.ndarray, top_k: int = 5) -> List[Episode]:
        """Retrieve episodes with most similar belief state (cosine similarity)."""
        if not self.episodes:
            return []

        sims = []
        for ep in self.episodes:
            denom = np.linalg.norm(belief) * np.linalg.norm(ep.belief_before) + 1e-10
            sims.append((np.dot(belief, ep.belief_before) / denom, ep))

        sims.sort(key=lambda x: x[0], reverse=True)
        return [ep for _, ep in sims[:top_k]]

    def action_success_rate(self, action_idx: int, window: int = 20) -> float:
        """Fraction of recent uses of action that yielded Comply or Nod."""
        recent = list(self.episodes)[-window:]
        relevant = [ep for ep in recent if ep.action == action_idx]
        if not relevant:
            return 0.5
        successes = sum(1 for ep in relevant if ep.observation in [0, 5])
        return successes / len(relevant)


# ── Meta-Reasoning ───────────────────────────────────────────────────
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
        previous = np.mean(self.reward_history[-2 * self.window:-self.window])
        return (recent - previous) < self.decline_threshold

    def get_exploration_boost(self) -> float:
        """Return exploration probability when adaptation is triggered."""
        if self.should_adapt():
            self.adaptation_log.append({
                "step": len(self.reward_history),
                "recent_mean": float(np.mean(self.reward_history[-self.window:])),
            })
            return 0.3
        return 0.0


# ── Simulated User ───────────────────────────────────────────────────
# Replaces the OpenAI API perception layer for offline testing.
# In deployment, the API would map camera/microphone input to one of
# the OBSERVATIONS categories; here the user samples from the same
# observation model directly.


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


# ── CRAMS Agent ──────────────────────────────────────────────────────


class CRAMSAgent:
    """
    Cognitive Robot for Adaptive Medical Support.

    Integrates:
        - POMDP belief tracking   (learning / perception)
        - QMDP policy             (reasoning / prospection)
        - Episodic memory         (memory)
        - Meta-reasoning          (metacognition)

    Cognitive cycle per interaction step:
        1. Receive observation from user
        2. Bayesian belief update        (learning)
        3. Recall similar past episodes  (episodic memory)
        4. QMDP action-value computation (prospection)
        5. Memory-informed bias          (episodic future thinking)
        6. Meta-reasoning check          (metacognition)
        7. Action selection              (action selection)
    """

    def __init__(self, gamma: float = 0.95):
        # build POMDP model
        self.T = build_transition_model()
        self.O = build_observation_model()
        self.R = build_reward_model()

        # prospective planner
        self.solver = QMDPSolver(self.T, self.R, gamma)

        # initial belief: uniform -- no prior assumptions about the user
        self.belief = np.ones(n_s) / n_s

        # cognitive modules
        self.memory = EpisodicMemory(capacity=200)
        self.meta = MetaReasoner(window=5, decline_threshold=-0.3)

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
        3- Meta-reasoning injects exploration if performance is declining
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

        # -- store in episodic memory --
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


# ── Simulation ───────────────────────────────────────────────────────

def run_simulation(n_steps: int = 30, initial_state: int = 4,
                   seed: int = 42, stress_step: Optional[int] = 15):
    """
    Run CRAMS and produce comprehensive visualisation.

    Parameters
    ----------
    n_steps : int
        Number of interaction rounds.
    initial_state : int
        User's starting hidden state index (default 4 = Medium trust, Medium load).
    seed : int
        Random seed for reproducibility.
    stress_step : int or None
        If set, at this step the user's load jumps to High (simulates
        an external stressor) to demonstrate adaptive behaviour.
    """
    np.random.seed(seed)

    agent = CRAMSAgent(gamma=0.95)
    user = SimulatedUser(true_state_idx=initial_state)

    print("=" * 70)
    print("  CRAMS -- Cognitive Robot for Adaptive Medical Support")
    print("  POMDP-based Medication Adherence Simulation")
    print("=" * 70)
    print(f"\n  Initial user state : {STATES[initial_state]}")
    print(f"  Simulation steps   : {n_steps}")
    if stress_step:
        print(f"  Stress event at    : step {stress_step}")
    print()

    # -- initial action (uniform belief, no observation yet) --
    action = agent.select_action(0)
    agent.action_history.append(action)

    for step in range(n_steps):
        # inject stress event
        if stress_step and step == stress_step:
            t_curr, _ = state_components(user.true_state)
            user.true_state = state_idx(t_curr, 2)  # load -> High
            print(f"  {'':6s}>>> STRESS EVENT: cognitive load increased <<<\n")

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

    # ── visualisation ────────────────────────────────────────────────
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
    for i, a in enumerate(agent.action_history[:-1]):  # exclude final pending action
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

    obs_counts = {OBSERVATIONS[o]: agent.obs_history.count(o) for o in range(n_o)}
    compliance = obs_counts.get("Comply", 0)
    compliance_rate = compliance / n_steps * 100

    print(f"  Compliance rate      : {compliance_rate:.1f}%  ({compliance}/{n_steps})")
    print(f"  Total reward         : {sum(agent.reward_history):.2f}")
    print(f"  Meta-adaptations     : {len(agent.meta.adaptation_log)}")
    print(f"  Episodes in memory   : {len(agent.memory.episodes)}")

    print(f"\n  Observation distribution:")
    for obs_name, count in sorted(obs_counts.items(), key=lambda x: -x[1]):
        bar = "#" * count
        print(f"    {obs_name:18s}: {count:2d}  {bar}")

    print(f"\n  Final belief (top 3):")
    top = np.argsort(agent.belief)[::-1][:3]
    for s in top:
        print(f"    {STATES[s]:22s} : {agent.belief[s]:.3f}")
    print()


# ── Multi-scenario comparison ────────────────────────────────────────

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
        agent = CRAMSAgent()
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
            "#2ecc71", "#3498db", "#95a5a6", "#f39c12", "#e74c3c", "#9b59b6",
        ]
        counts = [agent.action_history.count(a) for a in range(n_a)]
        ax_act.barh(range(n_a), counts, color=act_colours)
        ax_act.set_yticks(range(n_a))
        ax_act.set_yticklabels(ACTIONS, fontsize=8)
        ax_act.set_title(f"{name} -- Actions Used")

        # compliance stat
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


# ── Entry Point ──────────────────────────────────────────────────────

if __name__ == "__main__":
    # Primary simulation with stress event at step 15
    run_simulation(n_steps=30, initial_state=4, seed=42, stress_step=15)

    # Uncomment for multi-scenario comparison:
    # compare_scenarios()
