# MarketMind — Claude Code Agent Instructions

## What Is This Project?

MarketMind is a real-time market making simulator. Players quote bid/ask prices on a continuous order book while AI agents act as counterparties. The game features career mode with permadeath, adaptive AI opponents, multi-asset trading, and real-time multiplayer.

**Read the full PRD before writing any code:** `MarketMind_PRD_v2_FINAL.md` (root of repo)

## Repo Structure

This is a **monorepo** with two top-level packages:

```
marketmind/
├── client/          # React 18 + TypeScript + Vite frontend
├── server/          # Python 3.12 + FastAPI backend
├── docs/            # Architecture, contracts, schemas, API specs
└── CLAUDE.md        # You are here
```

## Module Ownership

Each Claude Code instance owns one module. **Do not modify files outside your module** unless updating a shared contract (which requires a PR).

| Module | Directory | Description |
|--------|-----------|-------------|
| Matching Engine | `server/engine/` | Order book, matching, price simulation, session lifecycle |
| AI Agents | `server/agents/` | Rule-based bots, RL agents, evolutionary agents, LLM agents |
| Frontend | `client/` | React UI, panels, charts, WebSocket client, stores |
| API Layer | `server/api/` | FastAPI app, WebSocket handlers, REST routes, auth |
| Analytics | `server/analytics/` | Debrief, scoring, behavioral analysis |
| Database | `server/db/` | Tortoise ORM models, migrations |

## Contracts Are Law

Before writing code, read these files:

1. **`docs/ARCHITECTURE.md`** — System design, data flow, component relationships
2. **`docs/CONTRACTS.md`** — Module interface specifications (function signatures, data types)
3. **`docs/schemas/`** — JSON schemas for all message types at module boundaries
4. **`docs/api/`** — REST endpoint specs and WebSocket message format

If your module produces data that another module consumes, the contract in `docs/` is the source of truth. If you need to change a contract, update the doc AND coordinate via PR.

## Tech Stack

### Frontend (client/)
- React 18 + TypeScript (strict mode)
- Vite for bundling
- Zustand for state management
- Tailwind CSS for styling
- Lightweight Charts (TradingView) for price charts
- D3.js for analytics charts
- react-grid-layout for drag-and-drop panels
- Native WebSocket API with reconnection logic

### Backend (server/)
- Python 3.12 + FastAPI
- Tortoise ORM (async-native) + PostgreSQL
- Redis for pub-sub (multiplayer)
- NumPy/SciPy for price simulation
- Stable Baselines 3 (SAC) for RL training
- Anthropic Python SDK for LLM features

## Git Workflow

- **Branch naming:** `{module}/{feature}` — e.g., `engine/order-book`, `frontend/panel-layout`, `agents/noise-trader`
- **Merge via PR.** Will reviews and merges (human checkpoint).
- **All instances can read** `docs/` and contract files on `main`.
- **Never push directly to main.**

## Code Style

### Python (server/)
- Type hints on all function signatures
- Docstrings on public functions (Google style)
- `async`/`await` everywhere — no blocking calls
- Use `from __future__ import annotations` in every file
- Pydantic models for all API request/response types
- No wildcard imports

### TypeScript (client/)
- Strict mode (`"strict": true` in tsconfig)
- Functional components only (no class components)
- All props typed with interfaces (no `any`)
- Custom hooks for shared logic
- Zustand stores for global state
- No direct DOM manipulation

## Key Design Decisions

1. **Single-threaded asyncio** for the matching engine — no race conditions
2. **50ms tick rate** internal, <100ms client update latency target
3. **JSON over WebSocket** with channel-based message routing
4. **Price-time priority (FIFO)** matching — industry standard
5. **AI adaptation is silent** — no notifications when bots get harder
6. **Bot-to-bot trading is enabled** — creates realistic tape
7. **Cream fintech aesthetic** — NOT typical dark-mode trading UI (dark mode is secondary)

## Testing

- Backend: pytest with async support (`pytest-asyncio`)
- Frontend: Vitest + React Testing Library
- Write tests for module boundaries first (contract tests)
- Integration tests for the matching engine are critical

## What NOT To Do

- Don't add dependencies without documenting why in your PR
- Don't use `any` in TypeScript — find the right type
- Don't make synchronous database calls
- Don't hardcode config values — use environment variables or config objects
- Don't skip error handling on WebSocket messages
- Don't implement features not in the PRD without discussing first
