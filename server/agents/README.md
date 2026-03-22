# AI Agents (`server/agents/`)

**Owner:** Claude Code Instance 2

All non-player market participants. These are the counterparties that make the game challenging.

## Files

- `base.py` — Abstract `BaseAgent` class (all agents implement this)
- `rule_based.py` — Noise Trader, Informed Trader, Momentum Scalper, Adversarial MM
- `rl_agent.py` — SAC reinforcement learning agent (Stable Baselines 3)
- `evolutionary.py` — Evolutionary population with niching
- `llm_agent.py` — Claude Haiku-powered reasoning trader

## Agent Types (v1 — Rule-Based)

| Agent | Behavior | Difficulty Params |
|-------|----------|-------------------|
| Noise Trader | Random hits/lifts, Poisson intensity | arrival_rate, size_range |
| Informed Trader | Knows fair value, picks off stale quotes | aggressiveness, latency |
| Momentum Scalper | Detects trends, trades in direction | sensitivity, hold_time |
| Adversarial MM | Quotes competing market, tightens when player widens | spread_target, reaction_speed |

## Key Design Decisions

- **All agents implement `BaseAgent.on_tick()`** — uniform interface for the engine.
- **Difficulty scales 1-10** per agent type, auto-adjusted per tier.
- **AI adaptation is SILENT** — no UI notification when bots get harder.
- **Agents are anonymous** — players see "Agent-1", "Agent-2", etc.
- **Fair value access**: Only informed agents see `observation.fair_value`. Others must infer.

## Interfaces

**Implements:** `BaseAgent` (on_tick, on_session_start, on_session_end)
**Consumes:** `AgentObservation` from the matching engine each tick
**Produces:** `list[AgentAction]` each tick

See `docs/CONTRACTS.md` §4 for full interface spec.
