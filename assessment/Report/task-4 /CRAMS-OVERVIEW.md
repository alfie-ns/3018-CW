# CRAMS -- Cognitive Robot for Adaptive Medical Support

## What It Is

A POMDP-based cognitive robot that supports medication adherence by reading a user's behavioural cues (facial expressions, voice tone, gestures), maintaining a probabilistic belief about their hidden trust level and cognitive load, and selecting contextually appropriate actions -- all whilst remembering past interactions and self-checking its own performance.

The novel contribution: wrapping an LLM (which perceives but cannot plan or remember) inside a POMDP (which plans and remembers but cannot perceive naturally). Each fills the gap the other lacks.

## Architecture

```
OpenAI API (perception)
    |
    v
Structured Observation (Comply, Hesitate, Verbal_Refuse, Ignore, Gaze_Avert, Nod, Ask_Question)
    |
    v
POMDP Belief Update (Bayesian inference)
    |
    v
Episodic Memory Retrieval (recall similar past situations)
    |
    v
QMDP Action Selection (prospective planning via value iteration)
    |
    v
Meta-Reasoning Check (detect declining performance, inject exploration)
    |
    v
Selected Action (Gentle_Reminder, Explain_Importance, Back_Off, Encourage, Direct_Prompt, Simplify)
    |
    v
OpenAI API translates action into natural language & gesture
    |
    v
User responds -> cycle repeats
```

## POMDP Formulation

| Component | Definition |
|---|---|
| **States (S)** | 9 hidden states: (Trust: High/Medium/Low) x (CognitiveLoad: Low/Medium/High) |
| **Actions (A)** | 6 robot actions: Gentle_Reminder, Explain_Importance, Back_Off, Encourage, Direct_Prompt, Simplify |
| **Observations (O)** | 7 behavioural cues: Comply, Hesitate, Verbal_Refuse, Ignore, Gaze_Avert, Nod, Ask_Question |
| **Transition T(s'\|s,a)** | Trust and load shift independently per action; boundary-clamped probabilities |
| **Observation Omega(o\|s',a)** | Parametric function of trust/load with multiplicative action modulation |
| **Reward R(s,a)** | State value (high trust, low load = good) + context-sensitive action bonuses/penalties |
| **Solver** | QMDP approximation -- value iteration on underlying MDP, belief-weighted action selection |

## Mapping to Lecture 9: Core Cognitive Abilities

Dr. Aly (Lecture 9) identifies seven core cognitive abilities plus prospection. CRAMS implements all of them:

| Cognitive Ability | CRAMS Implementation | Code Location |
|---|---|---|
| **Perception** | Multimodal observation via OpenAI API (simulated in offline mode) | `pomdp.py:build_observation_model()` |
| **Attention** | Selective focus on trust-relevant and load-relevant signals only | State space design (9 states from 2 dimensions) |
| **Action Selection** | QMDP belief-weighted policy selects action with highest expected long-term value | `pomdp.py:QMDPSolver.select_action()` |
| **Memory** | Episodic memory stores past interactions; cosine-similarity retrieval recalls what worked in similar belief states | `main.py:EpisodicMemory` |
| **Learning** | Bayesian belief update revises internal model after every observation | `pomdp.py:belief_update()` |
| **Reasoning** | Value iteration computes multi-step expected outcomes for each action | `pomdp.py:QMDPSolver._value_iteration()` |
| **Meta-Reasoning** | Self-monitoring detects declining reward trends and triggers exploration to escape ineffective action loops | `main.py:MetaReasoner` |
| **Prospection** | Forward simulation via value iteration -- the robot anticipates outcomes *before* acting, not merely reacting to sensory input | QMDP solver (Bellman backup over future states) |

### Episodic Future Thinking

The `EpisodicMemory.recall_similar()` method implements episodic future thinking (Atance and O'Neill, 2001): past events are reconstructed (retrieved by belief similarity) to allow the agent to pre-experience the future. If a similar belief state previously led to a successful action, that action receives a bonus; if it led to failure, it is suppressed.

### Metacognition

The `MetaReasoner` compares recent reward windows to detect performance decline -- reasoning about reasoning (Vernon, 2014). When triggered, it injects epsilon-greedy exploration weighted by historical action success rates, thereby preventing the robot from persisting with a failing strategy.

## Visualisation Output (5 panels)

1. **Trust Belief Evolution** -- stacked area chart showing how the robot's belief about user trust changes over time
2. **Cognitive Load Belief Evolution** -- same for cognitive load dimension
3. **Action Timeline** -- horizontal bar chart showing which action was selected at each step, with meta-reasoning adaptation triggers marked in red
4. **Cumulative Adherence Performance** -- cumulative reward curve; kinks indicate disruptions (e.g. stress events) and subsequent recovery
5. **True vs. MAP Belief** -- overlay of the user's actual hidden state against the robot's best guess, demonstrating inference under partial observability

## Simulation Features

- **Stress event injection**: at a configurable step, the user's cognitive load spikes to High, simulating an external stressor; the robot must detect and adapt
- **Multi-scenario comparison**: `compare_scenarios()` runs cooperative, uncertain, and resistant user profiles side-by-side to demonstrate generalisation
- **Reproducible**: seeded randomness for consistent demo results

## File Structure

```
crams/
  pomdp.py          -- POMDP engine (states, actions, observations, T, O, R, belief update, QMDP solver)
  main.py            -- CRAMS agent (episodic memory, meta-reasoning, simulated user, visualisation)
```

## Running

```bash
cd crams
python3 main.py
```

Produces console output (step-by-step interaction log + summary statistics) and saves `crams_simulation.png`.

For multi-scenario comparison, uncomment the last line in `main.py`:
```python
compare_scenarios()
```

## Key References

- Kaelbling, L. P., Littman, M. L. and Cassandra, A. R. (1998) 'Planning and acting in partially observable stochastic domains', *Artificial Intelligence*, 101(1-2), pp. 99-134.
- Littman, M. L., Cassandra, A. R. and Kaelbling, L. P. (1995) 'Learning policies for partially observable environments: Scaling up', *Proceedings of the 12th International Conference on Machine Learning*, pp. 362-370.
- Atance, C. M. and O'Neill, D. K. (2001) 'Episodic future thinking', *Trends in Cognitive Sciences*, 5(12), pp. 533-539.
- Vernon, D. (2014) *Artificial Cognitive Systems: A Primer*. Cambridge, MA: MIT Press.
- Cangelosi, A. and Asada, M. (in press) *Cognitive Robotics*, Chapter 1. MIT Press.
- Sandini, G., Sciutti, A. and Vernon, D. (2021) 'Cognitive Robotics', in Ang, M., Khatib, O. and Siciliano, B. (eds.) *Encyclopedia of Robotics*. Springer.

## Assessment Mapping (Task 4 -- 60% of Assessment 2)

| Marking Criterion | What CRAMS Demonstrates |
|---|---|
| **Introduction (10%)** | Novel contribution: LLM + POMDP hybrid for medication adherence |
| **Background (10%)** | Grounded in cognitive robotics theory (Lecture 9), POMDP literature, trust modelling |
| **Method and Setup (35%)** | Full POMDP formulation; parametric observation model; QMDP solver; episodic memory; meta-reasoning; stress-event testing |
| **Results/Outcome (30%)** | 5-panel visualisation; compliance rates; belief convergence; adaptive strategy shifts; multi-scenario comparison |
| **Conclusion (10%)** | Limitations (QMDP approximation, simulated user) and future work (real OpenAI API integration, real robot deployment) |
| **References (5%)** | Peer-reviewed sources throughout |
