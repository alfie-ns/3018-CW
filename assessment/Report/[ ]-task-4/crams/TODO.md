# CRAMS -- Build Order

- [ ] personalise to learn the how and when the user takes medication


## Pre-req

* [ ] GET APPROVAL FROM ALY
* [ ] Wait for Lectures 10/11 on cognitive architectures before finalising

## Phase 1: Brain (POMDP engine)

* [ ] Fill transition matrices T[a][s][s'] for all 5 actions x 6 states
* [ ] Fill observation matrices O[a][s'][o] for all 5 actions x 6 states x 5 observations
* [ ] Fill reward matrix R[s][a] using set exercises values (+10, +3, -5, -1)
* [ ] Run main.py, verify belief converges sensibly over 20 cycles

## Phase 2: Metacognition

* [ ] Track last N action-outcome pairs
* [ ] Flag when repeated actions produce negative outcomes
* [ ] Trigger policy adjustment when flagged

## Phase 3: OpenAI API integration

* [ ] Perception prompt: raw user data -> one of 5 observations
* [ ] Speech prompt: abstract action -> natural language/gesture for elderly user
* [ ] Wire into main loop replacing SimulatedUser

## Phase 4: GUI

* [ ] Belief state bar chart updating each cycle
* [ ] Action selection display
* [ ] Observation log
* [ ] Metacognition alerts

## Phase 5: Report (2,000 words)

* [ ] Introduction -- cognitive robotics framing (10%)
* [ ] Background -- POMDP + neuro-symbolic paradigm (10%)
* [ ] Method and setup -- cognitive architecture diagram + formal spec + code (35%)
* [ ] Results -- belief evolution plots, prospection vs reactive baseline (30%)
* [ ] Conclusion (10%)
* [ ] References -- peer-reviewed/conference only (5%)

## Phase 6: Video (5 min)

* [ ] Walk through one full scenario: perceive -> attend -> reason -> act -> learn -> adapt
* [ ] Show GUI with belief updating live

## Context
