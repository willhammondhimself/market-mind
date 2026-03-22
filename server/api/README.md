# API Layer (`server/api/`)

**Owner:** Claude Code Instance 4

The boundary between frontend and backend. Handles all client communication via WebSocket and REST.

## Files

- `main.py` — FastAPI application, CORS, startup/shutdown
- `websocket.py` — WebSocket connection handler, message routing
- `auth.py` — JWT auth, password hashing, token validation
- `routes/` — REST endpoint handlers (auth, sessions, users, social, leaderboards, multiplayer)

## Key Design Decisions

- **Single WebSocket connection** per client, multiplexed via `channel`/`type` fields.
- **JSON** message format (simplest to build and debug).
- **JWT auth** on both REST (`Authorization: Bearer`) and WebSocket (`?token=` query param).
- **Pydantic models** for all request/response validation.

## Endpoints

See `docs/api/REST.md` for full REST specification.
See `docs/api/WEBSOCKET.md` for full WebSocket protocol.

## Interfaces

**Depends on:**
- Matching Engine (`GameEngine` class) for game state and order processing
- Database Layer (Tortoise ORM models) for persistence
- Analytics Engine (`DebriefData`) for debrief endpoints

See `docs/CONTRACTS.md` §1–§3 for full interface specs.
