# Database Layer (`server/db/`)

**Owner:** Claude Code Instance 6 (or shared)

Persistence via Tortoise ORM (async-native) backed by PostgreSQL.

## Files

- `models.py` — Tortoise ORM model definitions
- `migrations/` — Raw SQL migration files

## Core Entities

| Model | Key Fields |
|-------|-----------|
| User | username, email, career_capital, tier, glicko_rating, streak_count, settings_json, api_key_encrypted |
| Session | user_id, mode, duration, buy_in, assets, difficulty, status, timestamps |
| Order | session_id, owner_id, asset, side, price, size, status, fill info |
| Trade | session_id, asset, buy/sell_order_id, price, size, counterparty_type |
| SessionAnalytics | session_id, pnl, sharpe, drawdown, composite_score, letter_grade, snapshot_data_json |
| AgentModel | user_id (null for global), agent_type, model_blob, training_count |
| Friendship | user_id, friend_user_id |
| Tournament | creator_id, name, format, max_players, status |

## Conventions

- All timestamps: UTC unix milliseconds
- Monetary values: floats (sufficient for a game)
- JSON blobs: `JSONField` for flexible nested data
- Migrations: Raw SQL files (not ORM-generated)
- No cascading deletes — handle in application code

See `docs/CONTRACTS.md` §6 for full entity specs.
