# MarketMind — Frontend

React 18 + TypeScript + Vite trading UI.

## Owner

**Claude Code Instance 3** — All frontend code lives here.

## Setup

```bash
npm install
npm run dev     # starts on http://localhost:3000
```

The dev server proxies `/api` and `/ws` to the backend at `localhost:8000`.

## Architecture

- **`src/components/`** — Reusable UI components (buttons, inputs, modals)
- **`src/panels/`** — The 11 draggable game panels (order book, chart, PnL, etc.)
- **`src/hooks/`** — Custom hooks (`useWebSocket`, `useGameState`, `useKeyBindings`)
- **`src/stores/`** — Zustand stores (game state, user settings, session config)
- **`src/types/`** — TypeScript interfaces matching server contracts
- **`src/utils/`** — Helper functions (formatting, calculations)
- **`public/sounds/`** — Audio files for fills, alerts, countdown

## Key Libraries

| Library | Purpose |
|---------|---------|
| Zustand | Global state management |
| Lightweight Charts | Price chart (TradingView open-source) |
| D3.js | Analytics/debrief charts |
| react-grid-layout | Drag-and-drop panel layout |
| Tailwind CSS | Styling |

## Design System

- **Light mode**: Cream background (`#FFFDF7`) — NOT typical dark trading UI
- **Dark mode**: System-follows via `prefers-color-scheme`
- **Profit/Loss**: Green (#16A34A) / Red (#DC2626)
- **Font**: Inter (UI) + JetBrains Mono (numbers/prices)

## Contracts

All TypeScript types in `src/types/` must match `docs/CONTRACTS.md`. If you need to change a type, update the contract doc in a PR first.
