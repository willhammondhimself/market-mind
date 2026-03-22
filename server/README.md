# MarketMind — Backend

Python 3.12 + FastAPI server with WebSocket support.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # edit with your values
uvicorn server.api.main:app --reload --port 8000
```

## Module Overview

| Module | Directory | Owner | Description |
|--------|-----------|-------|-------------|
| Matching Engine | `engine/` | Instance 1 | Order book, matching, price sim, session lifecycle |
| AI Agents | `agents/` | Instance 2 | Rule-based, RL, evolutionary, LLM agents |
| API Layer | `api/` | Instance 4 | FastAPI, WebSocket handlers, REST routes, auth |
| Analytics | `analytics/` | Instance 5 | Scoring, debrief, behavioral analysis |
| Database | `db/` | Instance 6 | Tortoise ORM models, migrations |

## Shared Types

All modules import from `server/types.py` for shared type definitions. This ensures consistency across module boundaries.

## Contracts

All interfaces between modules are defined in `docs/CONTRACTS.md`. Read it before writing code.
