# MarketMind — Module Interface Contracts

This document defines the typed interfaces at every module boundary. All modules MUST conform to these contracts. If you need to change a contract, update this document in a PR and coordinate with affected module owners.

Corresponding JSON schemas are in `docs/schemas/`. TypeScript types are in `client/src/types/`. Python types are defined in each module's type stubs.

---

## 1. API Layer ↔ Frontend (WebSocket Messages)

### Client → Server

All messages are JSON with a `type` field.

#### `order` — Place a new order
```python
class OrderMessage:
    type: Literal["order"]           # always "order"
    asset: str                       # ticker, e.g. "NVT"
    side: Literal["bid", "ask"]
    price: float                     # must be on valid tick
    size: int                        # positive integer
    order_type: Literal["limit"]     # v1: limit only
```

#### `cancel` — Cancel an existing order
```python
class CancelMessage:
    type: Literal["cancel"]
    order_id: str                    # UUID of order to cancel
```

#### `modify` — Modify an existing order
```python
class ModifyMessage:
    type: Literal["modify"]
    order_id: str
    new_price: float | None          # null = keep current
    new_size: int | None             # null = keep current
```

#### `cancel_all` — Cancel all player orders (panic button)
```python
class CancelAllMessage:
    type: Literal["cancel_all"]
    asset: str | None                # null = all assets
```

### Server → Client

All messages are JSON with a `channel` field.

#### `book` — Order book snapshot
```python
class BookUpdate:
    channel: Literal["book"]
    asset: str
    bids: list[tuple[float, int]]    # [[price, size], ...] best first
    asks: list[tuple[float, int]]    # [[price, size], ...] best first
    timestamp: int                   # unix ms
```

#### `trade` — Trade occurred
```python
class TradeUpdate:
    channel: Literal["trade"]
    asset: str
    price: float
    size: int
    aggressor_side: Literal["buy", "sell"]
    is_yours: bool                   # was the player involved?
    counterparty: str | None         # "Agent-3" if is_yours, else null
    timestamp: int
```

#### `fill` — Player order filled
```python
class FillUpdate:
    channel: Literal["fill"]
    asset: str
    order_id: str
    side: Literal["bid", "ask"]
    price: float
    size: int
    remaining_size: int              # 0 if fully filled
    timestamp: int
```

#### `pnl` — Player P&L update
```python
class PnLUpdate:
    channel: Literal["pnl"]
    realized: float
    unrealized: float
    inventory: dict[str, int]        # {"NVT": 15, "MRD": -5}
    total_pnl: float
    timestamp: int
```

#### `news` — News event
```python
class NewsUpdate:
    channel: Literal["news"]
    headline: str
    news_type: Literal["earnings", "macro", "sector", "geopolitical", "company"]
    affected_assets: list[str]       # tickers
    timestamp: int
```

#### `alert` — System alert
```python
class AlertUpdate:
    channel: Literal["alert"]
    alert_type: Literal["inventory_warning", "time_warning", "session_end", "countdown"]
    message: str
    severity: Literal["info", "warning", "critical"]
    timestamp: int
```

#### `session_state` — Session lifecycle events
```python
class SessionStateUpdate:
    channel: Literal["session_state"]
    state: Literal["countdown", "active", "ending", "ended"]
    countdown_value: int | None      # 3, 2, 1 during countdown
    time_remaining_ms: int | None    # ms remaining during active
    timestamp: int
```

#### `score` — Session end score reveal
```python
class ScoreUpdate:
    channel: Literal["score"]
    letter_grade: Literal["S", "A", "B", "C", "D", "F"]
    composite_score: float
    pnl: float
    sharpe: float
    max_drawdown: float
    avg_spread: float
    capital_change: float            # +/- career capital
    new_capital: float               # updated career capital
    streak_count: int
    multiplier: float
```

---

## 2. API Layer ↔ Frontend (REST Endpoints)

### Auth
| Method | Path | Request | Response |
|--------|------|---------|----------|
| POST | `/api/auth/register` | `{username, email, password}` | `{user_id, token}` |
| POST | `/api/auth/login` | `{email, password}` | `{user_id, token, refresh_token}` |
| POST | `/api/auth/refresh` | `{refresh_token}` | `{token}` |

### Sessions
| Method | Path | Request | Response |
|--------|------|---------|----------|
| POST | `/api/sessions` | `SessionConfig` | `{session_id}` |
| GET | `/api/sessions/{id}` | — | `SessionSummary` |
| GET | `/api/sessions/{id}/debrief` | — | `DebriefData` |
| GET | `/api/sessions/history` | `?page=&limit=` | `SessionSummary[]` |

### User Profile
| Method | Path | Request | Response |
|--------|------|---------|----------|
| GET | `/api/users/me` | — | `UserProfile` |
| PATCH | `/api/users/me` | partial `UserProfile` | `UserProfile` |
| GET | `/api/users/{id}` | — | `PublicProfile` |
| POST | `/api/users/me/settings` | `UserSettings` | `UserSettings` |

### Social
| Method | Path | Request | Response |
|--------|------|---------|----------|
| GET | `/api/friends` | — | `Friend[]` |
| POST | `/api/friends/{user_id}` | — | `{status}` |
| DELETE | `/api/friends/{user_id}` | — | `{status}` |

### Leaderboards
| Method | Path | Request | Response |
|--------|------|---------|----------|
| GET | `/api/leaderboards/capital` | `?scope=&tier=` | `LeaderboardEntry[]` |
| GET | `/api/leaderboards/rating` | `?scope=&tier=` | `LeaderboardEntry[]` |

---

## 3. API Layer ↔ Matching Engine

The API layer calls into the matching engine to process player actions and read game state.

```python
# --- Engine provides to API ---

class GameEngine:
    async def create_session(self, config: SessionConfig) -> str:
        """Create a new game session. Returns session_id."""

    async def submit_order(self, session_id: str, order: OrderRequest) -> OrderResult:
        """Submit a player order. Returns fill info or rejection."""

    async def cancel_order(self, session_id: str, order_id: str) -> bool:
        """Cancel an order. Returns success."""

    async def modify_order(self, session_id: str, order_id: str, new_price: float | None, new_size: int | None) -> OrderResult:
        """Modify an order. Returns updated order info."""

    async def cancel_all_orders(self, session_id: str, player_id: str, asset: str | None) -> int:
        """Cancel all player orders. Returns count cancelled."""

    async def get_book_state(self, session_id: str, asset: str) -> BookState:
        """Get current order book state for an asset."""

    async def get_session_state(self, session_id: str) -> SessionState:
        """Get current session state (time remaining, active status)."""

    async def end_session(self, session_id: str) -> SessionResult:
        """Force end a session. Liquidates positions, returns results."""

    def subscribe_events(self, session_id: str, callback: Callable[[GameEvent], Awaitable[None]]) -> None:
        """Register callback for real-time game events (trades, book changes, alerts)."""
```

---

## 4. Matching Engine ↔ AI Agents

Each tick (50ms), the engine asks all agents for their actions, then processes them.

```python
# --- Agent interface (all agents implement this) ---

class BaseAgent(ABC):
    agent_id: str                     # "Agent-1", "Agent-2", etc.
    agent_type: str                   # "noise", "informed", "momentum", "adversarial_mm", "rl", "evo", "llm"

    @abstractmethod
    async def on_tick(self, observation: AgentObservation) -> list[AgentAction]:
        """Called each tick. Returns zero or more actions."""

    @abstractmethod
    async def on_session_start(self, config: SessionConfig) -> None:
        """Called when session starts. Agent can initialize state."""

    @abstractmethod
    async def on_session_end(self, result: SessionResult) -> None:
        """Called when session ends. Agent can update models."""


class AgentObservation:
    tick: int
    timestamp: int
    assets: dict[str, AssetObservation]  # per-asset state
    time_remaining_ms: int
    player_estimated_inventory: dict[str, int]  # engine's estimate


class AssetObservation:
    fair_value: float                 # only for informed agents
    bids: list[tuple[float, int]]
    asks: list[tuple[float, int]]
    last_trades: list[TradeInfo]      # recent trades
    current_price: float
    volatility: float
    news_events: list[NewsEvent]      # recent news


class AgentAction:
    action_type: Literal["place_order", "cancel_order", "modify_order"]
    asset: str
    side: Literal["bid", "ask"] | None
    price: float | None
    size: int | None
    order_id: str | None              # for cancel/modify
```

---

## 5. Matching Engine ↔ Analytics Engine

At session end, the engine hands raw session data to analytics for processing.

```python
# --- Engine provides to Analytics ---

class RawSessionData:
    session_id: str
    player_id: str
    mode: Literal["career", "practice", "challenge", "multiplayer"]
    duration_seconds: int
    buy_in: float
    assets: list[str]
    difficulty_band: int

    # Time series (per-tick snapshots)
    snapshots: list[TickSnapshot]

    # All trades
    trades: list[TradeRecord]

    # All orders placed/cancelled/modified
    orders: list[OrderRecord]

    # News events that occurred
    news_events: list[NewsEventRecord]

    # Fair value path per asset (revealed post-session)
    fair_value_paths: dict[str, list[tuple[int, float]]]  # asset -> [(timestamp, value)]


class TickSnapshot:
    tick: int
    timestamp: int
    player_inventory: dict[str, int]
    player_realized_pnl: float
    player_unrealized_pnl: float
    book_state: dict[str, BookState]   # per asset
    player_active_orders: list[OrderRecord]


# --- Analytics provides to API ---

class DebriefData:
    session_id: str
    letter_grade: str
    composite_score: float
    component_scores: dict[str, float]  # pnl, sharpe, spread, drawdown, inventory

    # Performance tab
    pnl_curve: list[tuple[int, float]]               # [(timestamp, total_pnl)]
    fair_value_overlay: dict[str, list[tuple[int, float]]]
    per_asset_pnl: dict[str, float]

    # Inventory tab
    inventory_heatmap: dict[str, list[tuple[int, int]]]  # asset -> [(timestamp, position)]
    time_weighted_avg_inventory: dict[str, float]

    # Trades tab
    classified_trades: list[ClassifiedTrade]
    spread_efficiency: float
    optimal_spread: float
    behavioral_patterns: list[str]

    # Session-over-session (if available)
    skill_spider: dict[str, float] | None
    historical_pnl: list[tuple[str, float]] | None     # [(session_id, pnl)]


class ClassifiedTrade:
    trade_id: str
    timestamp: int
    asset: str
    side: str
    price: float
    size: int
    counterparty_type: Literal["informed", "noise", "momentum", "player"]
    counterparty_id: str
    pnl_impact: float
    book_state_at_trade: BookState     # for interactive drill-down
```

---

## 6. Database Layer ↔ All Server Modules

All modules interact with the database through Tortoise ORM models. See `server/db/models.py` for the full model definitions. Key entities:

- **User**: Auth, career capital, tier, rating, settings
- **Session**: Config, results, timestamps, status
- **Order**: All orders (player + agent), status tracking
- **Trade**: All executed trades with classification
- **SessionAnalytics**: Computed metrics, debrief data (JSON blob for snapshots)
- **AgentModel**: Serialized RL/evo model weights
- **Friendship**: Social graph
- **Tournament**: Tournament config and results

### Database conventions:
- All timestamps are UTC unix milliseconds
- All monetary values are floats (sufficient precision for a game)
- JSON blobs use `JSONField` for flexible nested data (snapshots, patterns, settings)
- Soft deletes where appropriate (users)
- No cascading deletes — handle in application code
