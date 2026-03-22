# MarketMind — System Architecture

## Overview

MarketMind is a client-server application with real-time bidirectional communication via WebSocket. The server runs the matching engine, AI agents, and price simulation in a single-threaded asyncio event loop. The client is a React SPA that renders the trading UI and communicates exclusively over one WebSocket connection (plus REST for non-realtime operations).

## High-Level Data Flow

```
┌─────────────────────────────────────────────────────────┐
│                        CLIENT                           │
│  React 18 + TypeScript + Vite                          │
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ Zustand   │  │ WebSocket│  │ REST     │             │
│  │ Stores    │◄─┤ Client   │  │ Client   │             │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘             │
│       │              │              │                    │
│  ┌────▼─────────────▼──────────────▼───┐               │
│  │         UI Panels (11 total)         │               │
│  │  Order Book | Chart | PnL | etc.    │               │
│  └─────────────────────────────────────┘               │
└─────────────────┬───────────────┬───────────────────────┘
                  │ WebSocket     │ REST (HTTP)
                  │ (JSON)        │ (JSON)
┌─────────────────▼───────────────▼───────────────────────┐
│                        SERVER                            │
│  Python 3.12 + FastAPI                                  │
│                                                          │
│  ┌─────────────────────────────────────────────────┐    │
│  │                 API Layer                         │    │
│  │  WebSocket Handler  |  REST Routes  |  Auth      │    │
│  └────────┬────────────────┬───────────────┬────────┘    │
│           │                │               │             │
│  ┌────────▼────────┐  ┌───▼────┐  ┌──────▼──────┐     │
│  │ Matching Engine  │  │Database│  │  Analytics   │     │
│  │                  │  │ Layer  │  │  Engine      │     │
│  │ ┌──────────────┐│  └───┬────┘  └──────┬──────┘     │
│  │ │ Order Book   ││      │              │             │
│  │ │ Price Sim    ││      │              │             │
│  │ │ Session Mgr  ││      │              │             │
│  │ └──────────────┘│  ┌───▼────┐         │             │
│  │                  │  │PostgreSQL│        │             │
│  │ ┌──────────────┐│  └────────┘         │             │
│  │ │  AI Agents   ││                     │             │
│  │ │ Rule / RL /  ││                     │             │
│  │ │ Evo / LLM   ││                     │             │
│  │ └──────────────┘│                     │             │
│  └──────────────────┘                    │             │
│                                           │             │
│  ┌────────────┐                          │             │
│  │   Redis    │◄── pub/sub (multiplayer) │             │
│  └────────────┘                          │             │
└──────────────────────────────────────────────────────────┘
```

## Component Responsibilities

### API Layer (`server/api/`)

**Owner:** Instance 4

The API layer is the boundary between client and server. It handles:

- **WebSocket endpoint** (`/ws/game/{session_id}`): Single connection per client, multiplexed via `channel` field in JSON messages. Receives player orders/cancels/modifies, broadcasts book updates/trades/PnL/alerts/news.
- **REST endpoints**: Auth (register, login, token refresh), session CRUD, analytics retrieval, leaderboards, profiles, settings, friend management.
- **Auth middleware**: JWT-based, validates tokens on both REST and WebSocket connections.
- **Message routing**: Deserializes incoming WebSocket JSON, dispatches to matching engine, serializes outbound state updates.

**Depends on:** Matching Engine (game state), Database Layer (persistence), Analytics Engine (debrief data)
**Depended on by:** Frontend (only interface to server)

### Matching Engine (`server/engine/`)

**Owner:** Instance 1

The core simulation loop. Runs in a single-threaded asyncio event loop at 50ms tick rate.

- **Order Book** (`orderbook.py`): Continuous limit order book with price-time priority (FIFO). Supports add, cancel, modify. Partial fills. Separate book per asset.
- **Matching** (`matching.py`): Matches incoming orders against resting orders. Generates trade events. Handles bot-to-bot trades.
- **Price Simulation** (`price_sim.py`): Drives fair value evolution. Implements news/event-driven (Tier 1+), regime-switching (mid-tier), and Heston stochastic vol (high-tier) processes. Uses NumPy/SciPy.
- **Session Manager** (`session.py`): Lifecycle management — session creation, countdown, active trading, time expiry, position liquidation, score handoff to analytics.

**Depends on:** AI Agents (bot orders each tick), Database Layer (session persistence)
**Depended on by:** API Layer (reads game state), Analytics Engine (post-session data)

### AI Agents (`server/agents/`)

**Owner:** Instance 2

All non-player participants in the market. Each agent receives the current book state and produces orders.

- **Rule-Based** (`rule_based.py`): Noise Trader, Informed Trader, Momentum Scalper, Adversarial MM. Parameterized difficulty (1-10 scale).
- **RL Agent** (`rl_agent.py`): SAC (Stable Baselines 3). Global model + personal shadow model. Discrete action space for v1.
- **Evolutionary** (`evolutionary.py`): Population of 100-200 agents. Continuous evolution with niching for strategy diversity.
- **LLM Agent** (`llm_agent.py`): Haiku-powered reasoning trader. Pre-generated news via Claude.

**Depends on:** Matching Engine (book state, fair value)
**Depended on by:** Matching Engine (consumes bot orders)

### Analytics Engine (`server/analytics/`)

**Owner:** Instance 5

Post-session analysis and persistent tracking.

- **Scoring** (`scoring.py`): Composite score calculation (PnL, Sharpe, spread efficiency, drawdown, inventory). Letter grade assignment. Streak tracking.
- **Debrief** (`debrief.py`): Generates debrief data — PnL curve vs fair value, inventory heatmap, trade classification (informed/noise/momentum), behavioral patterns.
- **Behavioral** (`behavioral.py`): Pattern detection across sessions ("you widen after losses", "slow to adjust after news").

**Depends on:** Database Layer (session data, historical data), Matching Engine (raw session data at session end)
**Depended on by:** API Layer (serves debrief to client)

### Database Layer (`server/db/`)

**Owner:** Instance 6 (or shared)

Persistence via Tortoise ORM (async-native) backed by PostgreSQL.

- **Models** (`models.py`): User, Session, Order, Trade, SessionAnalytics, AgentModel, Friendship, Tournament.
- **Migrations** (`migrations/`): Raw SQL migration files (no ORM-generated migrations).

**Depends on:** PostgreSQL (external)
**Depended on by:** All server modules

### Frontend (`client/`)

**Owner:** Instance 3

React 18 SPA with 11 draggable panels, real-time WebSocket updates, and Zustand state management.

- **Components** (`src/components/`): Reusable UI elements
- **Panels** (`src/panels/`): The 11 game panels (order book ladder, depth chart, price chart, T&S tape, PnL curve, inventory gauge, risk dashboard, order entry, asset selector, news feed, alert log)
- **Hooks** (`src/hooks/`): `useWebSocket`, `useGameState`, `useKeyBindings`, etc.
- **Stores** (`src/stores/`): Zustand stores for game state, user settings, session config
- **Types** (`src/types/`): All TypeScript interfaces matching server contracts

**Depends on:** API Layer (WebSocket + REST)
**Depended on by:** Nothing (leaf node)

## Session Lifecycle

```
1. Client: POST /api/sessions (mode, assets, buy_in, duration)
2. Server: Creates session, initializes order books, spawns agents
3. Server: Returns session_id
4. Client: Connects WebSocket to /ws/game/{session_id}
5. Server: Sends countdown (3...2...1...GO)
6. Server: Starts tick loop (50ms):
   a. Advance price simulation
   b. Agents observe book state → generate orders
   c. Process all orders (player + agent) through matching engine
   d. Generate trade events
   e. Broadcast state update to client (book, trades, PnL, alerts)
7. Timer expires → server stops accepting orders
8. Server: Auto-liquidates open positions at last traded price
9. Server: Hands session data to analytics engine
10. Analytics: Computes composite score, generates debrief
11. Server: Persists session results to database
12. Client: Receives session_end event, shows score reveal animation
13. Client: Can fetch debrief via REST (GET /api/sessions/{id}/debrief)
```

## Communication Protocols

### WebSocket (real-time game state)

Single connection per client. JSON messages with `type` (client→server) or `channel` (server→client) field for routing. See `docs/api/WEBSOCKET.md` for full message catalog.

### REST (non-realtime operations)

Standard JSON REST API. JWT auth via `Authorization: Bearer <token>` header. See `docs/api/REST.md` for endpoint catalog.

## Deployment

| Service | Provider | Notes |
|---------|----------|-------|
| Frontend | Vercel (free) | Static SPA, CDN |
| Backend | Railway (free/$5) | FastAPI + WebSocket |
| PostgreSQL | Neon or Supabase (free) | Managed Postgres |
| Redis | Railway (self-hosted) | Only needed for multiplayer |

## Performance Targets

| Metric | Target |
|--------|--------|
| Matching engine tick rate | 50ms (20 ticks/sec) |
| Client update latency | <100ms |
| WebSocket message format | JSON |
| Concurrent sessions (beta) | 5-10 |
