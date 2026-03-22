# Matching Engine (`server/engine/`)

**Owner:** Claude Code Instance 1

The core simulation engine. Manages order books, matching, price processes, and session lifecycle.

## Files

- `orderbook.py` — Continuous limit order book (price-time priority FIFO, partial fills)
- `matching.py` — Order matching logic, trade generation, bot-to-bot trading
- `price_sim.py` — Fair value simulation (news-driven, regime-switching, Heston)
- `session.py` — Session lifecycle (create, countdown, active, end, liquidate)

## Key Design Decisions

- **Single-threaded asyncio** — No race conditions. One event loop runs the entire tick.
- **50ms tick rate** (20 ticks/sec) — Each tick: advance price sim → collect agent orders → match → broadcast.
- **Separate book per asset** — Each asset has its own independent order book.
- **Bot-to-bot trading enabled** — Creates realistic tape and price discovery.

## Interfaces

**Provides to API Layer:**
- `GameEngine` class with async methods for session management and order processing
- Event subscription for real-time game state broadcasts

**Consumes from AI Agents:**
- Calls `agent.on_tick(observation)` each tick, processes returned actions

**Provides to Analytics:**
- `RawSessionData` at session end (all snapshots, trades, orders, fair values)

See `docs/CONTRACTS.md` §3–§5 for full interface specs.
