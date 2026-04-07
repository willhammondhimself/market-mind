# MarketMind

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/) [![FastAPI](https://img.shields.io/badge/FastAPI-0.108+-green.svg)](https://fastapi.tiangolo.com/) [![React](https://img.shields.io/badge/React-18.2+-61DAFB.svg)](https://reactjs.org/) [![SAC](https://img.shields.io/badge/RL-SAC-red.svg)]() [![LLM](https://img.shields.io/badge/LLM-Claude_Haiku-blueviolet.svg)]()

Real-time market making simulator with adaptive AI opponents.

Quote bid/ask prices on a continuous order book while AI agents — from rule-based bots to reinforcement learning agents — act as your counterparties. They adapt to your style, silently exploit your weaknesses, and get harder as you improve.

## Features

- **Continuous order book** with price-time priority matching (50ms tick rate)
- **15+ tradeable assets** with distinct price processes and difficulty levels
- **Adaptive AI agents** — rule-based, RL (SAC), evolutionary, and LLM-powered
- **Career mode** with permadeath, tier progression (Intern → Legend), and real capital stakes
- **Real-time multiplayer** (2-4 players) with Glicko-2 ranked matchmaking
- **Post-session debrief** with trade classification, behavioral analysis, and AI coaching

## Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + TypeScript + Vite + Zustand + Tailwind |
| Backend | Python 3.12 + FastAPI + WebSocket |
| Database | PostgreSQL (Tortoise ORM) |
| Charts | Lightweight Charts (TradingView) + D3.js |
| AI/ML | Stable Baselines 3 (SAC) + Anthropic SDK |

## Repo Structure

```
marketmind/
├── CLAUDE.md              # Instructions for Claude Code agents
├── docs/
│   ├── ARCHITECTURE.md    # System design
│   ├── CONTRACTS.md       # Module interface specs
│   ├── schemas/           # JSON schemas at module boundaries
│   └── api/               # REST + WebSocket specs
├── client/                # React frontend (Instance 3)
│   ├── src/types/         # TypeScript interfaces
│   └── ...
├── server/
│   ├── types.py           # Shared Python types
│   ├── engine/            # Matching engine (Instance 1)
│   ├── agents/            # AI agents (Instance 2)
│   ├── api/               # FastAPI + WebSocket (Instance 4)
│   ├── analytics/         # Scoring + debrief (Instance 5)
│   └── db/                # Database models (Instance 6)
└── MarketMind_PRD_v2_FINAL.md  # Full product spec
```

## Quick Start

**Frontend:**
```bash
cd client
npm install
npm run dev
```

**Backend:**
```bash
cd server
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn server.api.main:app --reload --port 8000
```

## Development

This repo is designed for parallel development with 3-5+ Claude Code instances. Each instance owns a module and communicates via contracts in `docs/`. See `CLAUDE.md` for agent instructions.

## License

Source-available. Viewable on GitHub but not forkable without license.
