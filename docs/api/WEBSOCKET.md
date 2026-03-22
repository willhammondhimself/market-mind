# MarketMind — WebSocket Protocol Specification

**Endpoint:** `ws://host/ws/game/{session_id}` (or `wss://` for TLS)
**Auth:** JWT token sent as first message after connection or via query param `?token=JWT`
**Format:** JSON over WebSocket frames
**Direction:** Bidirectional (client ↔ server)

---

## Connection Lifecycle

1. **Client connects** to `ws://host/ws/game/{session_id}?token=JWT`
   - Token can alternatively be sent in first message (see auth below)

2. **Server validates token** and session ownership
   - Returns `session_state` message with current state
   - If countdown phase: includes countdown_seconds
   - If active phase: includes current book snapshot

3. **During countdown** (30-second period before market open)
   - Server sends `session_state` with countdown_seconds every second
   - Client may send orders (queued, not executed yet)

4. **During active trading** (main market phase)
   - Server sends `book`, `trade`, `fill`, `pnl`, `news`, `alert` messages at each tick
   - Book updates: every tick (50ms default)
   - PnL updates: every tick
   - Trades/fills: on occurrence only
   - News: on Poisson arrival (random)

5. **On session end**
   - Server sends final `score` message
   - Server closes WebSocket connection

6. **Reconnection** (career mode only)
   - Client can reconnect within 30-second grace period
   - Receives full state snapshot and resumes

**Connection closure codes:**
- `1000` — Normal closure (session ended)
- `1002` — Protocol error (invalid message format)
- `1008` — Policy violation (auth failure, rate limit)
- `1011` — Server error

---

## Authentication

### Method 1: Query Parameter

```
ws://host/ws/game/{session_id}?token=eyJhbGc...
```

### Method 2: First Message

Connect, then send auth message as first message:

```json
{
  "type": "auth",
  "token": "eyJhbGc..."
}
```

**Auth Failure Response:**
```json
{
  "channel": "error",
  "code": "AUTH_FAILED",
  "message": "Invalid or expired token"
}
```

Server closes connection with code `1008` after auth failure.

---

## Client → Server Messages

All client messages include a `type` field identifying the message type.

### Message: order

Create a new order (buy or sell limit/market).

**Fields:**
- `type` — "order" (string, required)
- `id` — Unique client message ID for matching fill confirmations (string, optional but recommended)
- `symbol` — Ticker symbol (string, required, e.g., "AAPL")
- `side` — "buy" or "sell" (string, required)
- `order_type` — "market" or "limit" (string, required)
- `quantity` — Number of shares (number, required, positive integer)
- `price` — Limit price (number, required for limit orders, ignored for market)
- `time_in_force` — "day" or "ioc" (string, optional, default="day")

**Example: Market Buy**
```json
{
  "type": "order",
  "id": "client-msg-1",
  "symbol": "AAPL",
  "side": "buy",
  "order_type": "market",
  "quantity": 100
}
```

**Example: Limit Sell**
```json
{
  "type": "order",
  "id": "client-msg-2",
  "symbol": "TSLA",
  "side": "sell",
  "order_type": "limit",
  "quantity": 50,
  "price": 245.75,
  "time_in_force": "day"
}
```

**Response:** Server will send `fill` message(s) when order executes, or `alert` if rejected.

---

### Message: cancel

Cancel an open order by order ID.

**Fields:**
- `type` — "cancel" (string, required)
- `id` — Unique client message ID (string, optional)
- `order_id` — ID of order to cancel (string, required)

**Example:**
```json
{
  "type": "cancel",
  "id": "client-msg-3",
  "order_id": "order-12345"
}
```

**Response:** Server sends `alert` confirming cancellation, or error if order not found.

---

### Message: modify

Modify price/quantity of an open order.

**Fields:**
- `type` — "modify" (string, required)
- `id` — Unique client message ID (string, optional)
- `order_id` — ID of order to modify (string, required)
- `quantity` — New quantity (number, optional, positive integer)
- `price` — New limit price (number, optional, for limit orders)

**Example:**
```json
{
  "type": "modify",
  "id": "client-msg-4",
  "order_id": "order-12345",
  "price": 250.00
}
```

**Response:** Server sends `alert` confirming modification or error.

---

### Message: cancel_all

Cancel all open orders for a symbol or all symbols.

**Fields:**
- `type` — "cancel_all" (string, required)
- `id` — Unique client message ID (string, optional)
- `symbol` — Symbol to cancel all orders for (string, optional. If omitted, cancels all symbols)

**Example: Cancel all for AAPL**
```json
{
  "type": "cancel_all",
  "id": "client-msg-5",
  "symbol": "AAPL"
}
```

**Example: Cancel all orders**
```json
{
  "type": "cancel_all",
  "id": "client-msg-6"
}
```

**Response:** Server sends one or more `alert` messages confirming cancellations.

---

### Message: heartbeat (ping)

Periodic heartbeat to keep connection alive and detect stale connections.

**Fields:**
- `type` — "ping" (string, required)
- `timestamp` — Client timestamp (number, optional, Unix milliseconds)

**Example:**
```json
{
  "type": "ping",
  "timestamp": 1710950400000
}
```

**Response:** Server responds with `pong` message (see below).

---

## Server → Client Messages

All server messages include a `channel` field identifying the message type.

### Message: session_state

Sent upon connection and during countdown phase. Contains full session state snapshot.

**Fields:**
- `channel` — "session_state" (string)
- `session_id` — Session ID (string, UUID)
- `state` — "countdown" | "active" | "ended" (string)
- `countdown_seconds` — Seconds until market opens (number, null if active/ended)
- `tick` — Current market tick (number, null during countdown)
- `timestamp` — Server timestamp (number, Unix milliseconds)
- `portfolio` — User's portfolio (object)
  - `capital` — Cash available (number)
  - `positions` — Map of symbol → quantity (object)
  - `open_orders` — Array of open orders (array)
- `market` — Market snapshot (object)
  - `symbols` — List of tradable symbols (array of strings)
  - `book` — Order book for all symbols (object, see book message format)

**Example: During Countdown**
```json
{
  "channel": "session_state",
  "session_id": "sess-abc123",
  "state": "countdown",
  "countdown_seconds": 25,
  "timestamp": 1710950400000,
  "portfolio": {
    "capital": 100000,
    "positions": {},
    "open_orders": []
  },
  "market": {
    "symbols": ["AAPL", "GOOGL", "MSFT", "TSLA"],
    "book": {}
  }
}
```

**Example: During Active (with book)**
```json
{
  "channel": "session_state",
  "session_id": "sess-abc123",
  "state": "active",
  "tick": 42,
  "countdown_seconds": null,
  "timestamp": 1710950402100,
  "portfolio": {
    "capital": 95000,
    "positions": {
      "AAPL": 100
    },
    "open_orders": [
      {
        "order_id": "order-12345",
        "symbol": "MSFT",
        "side": "buy",
        "order_type": "limit",
        "quantity": 50,
        "price": 350.00,
        "created_at": 1710950401000
      }
    ]
  },
  "market": {
    "symbols": ["AAPL", "GOOGL", "MSFT", "TSLA"],
    "book": {
      "AAPL": {
        "bids": [[150.25, 100], [150.20, 150], [150.15, 200]],
        "asks": [[150.35, 120], [150.40, 80], [150.50, 200]]
      },
      "GOOGL": {
        "bids": [[142.50, 50], [142.45, 75]],
        "asks": [[142.65, 100], [142.75, 50]]
      }
    }
  }
}
```

---

### Message: book

Order book snapshot for one or more symbols. Sent every tick during active phase.

**Fields:**
- `channel` — "book" (string)
- `tick` — Market tick (number)
- `timestamp` — Server timestamp (number, Unix milliseconds)
- `symbols` — Map of symbol → book state (object)
  - Each symbol contains:
    - `bids` — Array of [price, quantity] tuples, sorted descending by price (array)
    - `asks` — Array of [price, quantity] tuples, sorted ascending by price (array)
    - `mid` — Midpoint price (number, optional)
    - `spread` — Bid-ask spread (number, optional)

**Example:**
```json
{
  "channel": "book",
  "tick": 50,
  "timestamp": 1710950402500,
  "symbols": {
    "AAPL": {
      "bids": [[150.25, 200], [150.20, 150], [150.15, 100]],
      "asks": [[150.35, 120], [150.40, 180], [150.50, 250]],
      "mid": 150.30,
      "spread": 0.10
    },
    "TSLA": {
      "bids": [[248.50, 300], [248.40, 250]],
      "asks": [[248.75, 150], [248.90, 200]],
      "mid": 248.625,
      "spread": 0.25
    }
  }
}
```

---

### Message: trade

Market trade execution (informational, not user-specific).

**Fields:**
- `channel` — "trade" (string)
- `tick` — Market tick (number)
- `timestamp` — Server timestamp (number, Unix milliseconds)
- `symbol` — Ticker symbol (string)
- `price` — Execution price (number)
- `quantity` — Quantity traded (number)
- `side` — "buy" or "sell" (string, side of aggressive buyer)

**Example:**
```json
{
  "channel": "trade",
  "tick": 48,
  "timestamp": 1710950402400,
  "symbol": "AAPL",
  "price": 150.30,
  "quantity": 500,
  "side": "buy"
}
```

---

### Message: fill

User's order was filled (partial or full).

**Fields:**
- `channel` — "fill" (string)
- `tick` — Market tick when filled (number)
- `timestamp` — Server timestamp (number, Unix milliseconds)
- `order_id` — Order ID (string)
- `symbol` — Ticker symbol (string)
- `side` — "buy" or "sell" (string)
- `quantity` — Quantity filled (number)
- `price` — Execution price (number)
- `commission` — Trading commission (number, optional)
- `remaining_quantity` — Remaining unfilled quantity (number, 0 if fully filled)

**Example: Partial Fill**
```json
{
  "channel": "fill",
  "tick": 48,
  "timestamp": 1710950402400,
  "order_id": "order-12345",
  "symbol": "MSFT",
  "side": "buy",
  "quantity": 30,
  "price": 350.15,
  "commission": 1.05,
  "remaining_quantity": 20
}
```

**Example: Full Fill**
```json
{
  "channel": "fill",
  "tick": 49,
  "timestamp": 1710950402450,
  "order_id": "order-12345",
  "symbol": "MSFT",
  "side": "buy",
  "quantity": 20,
  "price": 350.20,
  "commission": 0.70,
  "remaining_quantity": 0
}
```

---

### Message: pnl

Portfolio profit/loss update. Sent every tick during active phase.

**Fields:**
- `channel` — "pnl" (string)
- `tick` — Market tick (number)
- `timestamp` — Server timestamp (number, Unix milliseconds)
- `capital` — Current cash balance (number)
- `gross_value` — Total portfolio value including positions (number)
- `total_pnl` — Absolute profit/loss from starting capital (number)
- `total_pnl_pct` — Percentage return (number)
- `realized_pnl` — Pnl from closed positions (number)
- `unrealized_pnl` — Pnl from open positions (number)
- `positions` — Map of symbol → position details (object)
  - `quantity` — Number of shares held (number)
  - `avg_entry_price` — Average entry price (number)
  - `current_price` — Current market price (number)
  - `position_pnl` — Pnl for this position (number)
  - `position_pnl_pct` — Pnl percentage for this position (number)

**Example:**
```json
{
  "channel": "pnl",
  "tick": 50,
  "timestamp": 1710950402500,
  "capital": 94000,
  "gross_value": 113200,
  "total_pnl": 13200,
  "total_pnl_pct": 13.2,
  "realized_pnl": 500,
  "unrealized_pnl": 12700,
  "positions": {
    "AAPL": {
      "quantity": 100,
      "avg_entry_price": 150.00,
      "current_price": 152.00,
      "position_pnl": 200,
      "position_pnl_pct": 1.33
    },
    "TSLA": {
      "quantity": 50,
      "avg_entry_price": 245.00,
      "current_price": 248.50,
      "position_pnl": 175,
      "position_pnl_pct": 1.43
    }
  }
}
```

---

### Message: news

Market news event affecting one or more symbols.

**Fields:**
- `channel` — "news" (string)
- `tick` — Market tick when news arrived (number)
- `timestamp` — Server timestamp (number, Unix milliseconds)
- `headline` — News headline (string)
- `symbols` — Symbols affected (array of strings)
- `impact_type` — "positive" | "negative" | "neutral" (string)
- `price_impact` — Expected price change percentage (number, e.g., -2.5 for -2.5%)

**Example: Positive News**
```json
{
  "channel": "news",
  "tick": 35,
  "timestamp": 1710950401750,
  "headline": "Apple announces record Q2 earnings",
  "symbols": ["AAPL"],
  "impact_type": "positive",
  "price_impact": 3.2
}
```

**Example: Sector News**
```json
{
  "channel": "news",
  "tick": 60,
  "timestamp": 1710950403000,
  "headline": "Tech sector faces regulatory headwinds",
  "symbols": ["AAPL", "GOOGL", "MSFT"],
  "impact_type": "negative",
  "price_impact": -1.8
}
```

---

### Message: alert

Alert or status message (order rejected, cancelled, etc).

**Fields:**
- `channel` — "alert" (string)
- `tick` — Current market tick (number, null during countdown)
- `timestamp` — Server timestamp (number, Unix milliseconds)
- `level` — "info" | "warning" | "error" (string)
- `code` — Alert code (string, e.g., "ORDER_REJECTED", "INSUFFICIENT_CAPITAL")
- `message` — Human-readable message (string)
- `details` — Additional context (object, optional)

**Example: Insufficient Capital**
```json
{
  "channel": "alert",
  "tick": 48,
  "timestamp": 1710950402400,
  "level": "error",
  "code": "INSUFFICIENT_CAPITAL",
  "message": "Order rejected: insufficient capital for 100 shares at $350.15",
  "details": {
    "required": 35015,
    "available": 5000,
    "symbol": "MSFT"
  }
}
```

**Example: Order Cancelled**
```json
{
  "channel": "alert",
  "tick": 49,
  "timestamp": 1710950402450,
  "level": "info",
  "code": "ORDER_CANCELLED",
  "message": "Order cancelled by user",
  "details": {
    "order_id": "order-12345",
    "symbol": "MSFT",
    "unfilled_quantity": 50
  }
}
```

**Example: During Countdown (tick = null)**
```json
{
  "channel": "alert",
  "tick": null,
  "timestamp": 1710950400500,
  "level": "info",
  "code": "ORDER_QUEUED",
  "message": "Order queued for execution at market open",
  "details": {
    "order_id": "order-xyz789",
    "symbol": "GOOGL"
  }
}
```

---

### Message: score

Final session score and leaderboard data. Sent when session ends.

**Fields:**
- `channel` — "score" (string)
- `timestamp` — Server timestamp (number, Unix milliseconds)
- `session_id` — Session ID (string, UUID)
- `stats` — Performance metrics (object)
  - `starting_capital` — Initial capital (number)
  - `final_capital` — Ending capital (number)
  - `total_return_pct` — Percentage return (number)
  - `total_profit_loss` — Absolute profit/loss (number)
  - `max_drawdown_pct` — Maximum drawdown percentage (number)
  - `sharpe_ratio` — Risk-adjusted return metric (number)
  - `win_rate_pct` — Percentage of winning trades (number)
  - `trades_completed` — Total closed trades (number)
  - `news_events_seen` — Total news events received (number)
- `rank` — Player's position on leaderboard (object, optional)
  - `tier_rank` — Rank within user's tier (number)
  - `global_rank` — Global rank (number)
  - `percentile` — Percentile (0-100) (number)

**Example:**
```json
{
  "channel": "score",
  "timestamp": 1710950450000,
  "session_id": "sess-abc123",
  "stats": {
    "starting_capital": 100000,
    "final_capital": 118500,
    "total_return_pct": 18.5,
    "total_profit_loss": 18500,
    "max_drawdown_pct": -8.2,
    "sharpe_ratio": 1.45,
    "win_rate_pct": 62.5,
    "trades_completed": 16,
    "news_events_seen": 12
  },
  "rank": {
    "tier_rank": 3,
    "global_rank": 87,
    "percentile": 85
  }
}
```

---

### Message: heartbeat (pong)

Server response to client's ping heartbeat.

**Fields:**
- `channel` — "pong" (string)
- `timestamp` — Server timestamp (number, Unix milliseconds)
- `latency_ms` — Round-trip time estimate (number, optional)

**Example:**
```json
{
  "channel": "pong",
  "timestamp": 1710950402500,
  "latency_ms": 45
}
```

---

### Message: error

Server error or protocol violation.

**Fields:**
- `channel` — "error" (string)
- `code` — Error code (string, e.g., "INVALID_MESSAGE", "AUTH_FAILED", "RATE_LIMITED")
- `message` — Error description (string)
- `details` — Additional context (object, optional)

**Example: Malformed Message**
```json
{
  "channel": "error",
  "code": "INVALID_MESSAGE",
  "message": "Message missing required 'type' field",
  "details": {
    "message": "{\"symbol\": \"AAPL\"}"
  }
}
```

**Example: Rate Limited**
```json
{
  "channel": "error",
  "code": "RATE_LIMITED",
  "message": "Too many messages sent. Limit: 100/second",
  "details": {
    "limit": 100,
    "window_seconds": 1,
    "retry_after_seconds": 2
  }
}
```

---

## Update Rates

Market data update frequencies during active trading phase:

| Message Type | Frequency | Notes |
|---|---|---|
| `book` | Every tick (50ms default) | Order book snapshot |
| `pnl` | Every tick (50ms default) | Portfolio value update |
| `trade` | On occurrence | Market trades (Poisson-distributed) |
| `fill` | On occurrence | User order executions |
| `news` | On occurrence | Poisson arrival (~1-3 per minute typical) |
| `alert` | On occurrence | Order status changes, warnings |
| `session_state` | Connection + countdown phase | ~1/second during countdown |

Server clock tick is configurable (default 50ms). Update rates scale accordingly.

---

## Message Flow Examples

### Example 1: Simple Market Buy

**Client:**
```json
{
  "type": "order",
  "id": "msg-001",
  "symbol": "AAPL",
  "side": "buy",
  "order_type": "market",
  "quantity": 100
}
```

**Server (next tick):**
```json
{
  "channel": "fill",
  "tick": 42,
  "timestamp": 1710950402300,
  "order_id": "order-12345",
  "symbol": "AAPL",
  "side": "buy",
  "quantity": 100,
  "price": 150.35,
  "commission": 5.01,
  "remaining_quantity": 0
}
```

**Server (same tick):**
```json
{
  "channel": "pnl",
  "tick": 42,
  "timestamp": 1710950402300,
  "capital": 94494.99,
  "gross_value": 110534.99,
  "total_pnl": 10534.99,
  "total_pnl_pct": 10.53,
  "realized_pnl": 0,
  "unrealized_pnl": 10534.99,
  "positions": {
    "AAPL": {
      "quantity": 100,
      "avg_entry_price": 150.35,
      "current_price": 150.35,
      "position_pnl": 0,
      "position_pnl_pct": 0
    }
  }
}
```

---

### Example 2: Limit Order with News Impact

**Client (during active trading):**
```json
{
  "type": "order",
  "id": "msg-002",
  "symbol": "GOOGL",
  "side": "sell",
  "order_type": "limit",
  "quantity": 50,
  "price": 145.00
}
```

**Server (alert confirming order queued):**
```json
{
  "channel": "alert",
  "tick": 55,
  "timestamp": 1710950402750,
  "level": "info",
  "code": "ORDER_ACCEPTED",
  "message": "Limit order created",
  "details": {
    "order_id": "order-23456",
    "symbol": "GOOGL",
    "side": "sell",
    "quantity": 50,
    "price": 145.00
  }
}
```

**Server (news arrives):**
```json
{
  "channel": "news",
  "tick": 60,
  "timestamp": 1710950403000,
  "headline": "Google announces AI breakthrough",
  "symbols": ["GOOGL"],
  "impact_type": "positive",
  "price_impact": 5.0
}
```

**Server (order fills at higher price due to news):**
```json
{
  "channel": "fill",
  "tick": 61,
  "timestamp": 1710950403050,
  "order_id": "order-23456",
  "symbol": "GOOGL",
  "side": "sell",
  "quantity": 50,
  "price": 152.25,
  "commission": 3.81,
  "remaining_quantity": 0
}
```

---

### Example 3: Reconnection (Grace Period)

**Client loses connection at tick 75**

**Client reconnects at tick 80 (within 30s window):**
```
ws://host/ws/game/sess-abc123?token=JWT
```

**Server (reconnect response with state snapshot):**
```json
{
  "channel": "session_state",
  "session_id": "sess-abc123",
  "state": "active",
  "tick": 80,
  "timestamp": 1710950404000,
  "portfolio": {
    "capital": 92000,
    "positions": {
      "AAPL": 100,
      "GOOGL": -50
    },
    "open_orders": []
  },
  "market": {
    "symbols": ["AAPL", "GOOGL", "MSFT", "TSLA"],
    "book": {
      "AAPL": {
        "bids": [[150.50, 200]],
        "asks": [[150.75, 150]]
      }
    }
  }
}
```

Client is fully synchronized and can resume trading.

---

## Best Practices

1. **Heartbeat Strategy:** Send a ping every 30 seconds during idle periods to detect stale connections.

2. **Message IDs:** Include unique `id` fields in client messages to correlate fills and alerts.

3. **Order Management:** Track `order_id` values returned in alert/fill messages for subsequent modifications/cancellations.

4. **Portfolio State:** Maintain local copy of portfolio state from pnl messages for UI display. Update on every tick.

5. **Error Recovery:** On connection loss, reconnect immediately if within grace period (30s). Otherwise, session is lost.

6. **Rate Limiting:** Do not send more than 100 order messages per second per connection. Server will send rate_limited error if exceeded.

7. **Clock Synchronization:** Use server timestamp in messages for accurate time-series data. Avoid relying on client clock.

8. **News Monitoring:** Subscribe to news messages for market-moving events. Alert user of high-impact news.

---

## Glossary

- **Tick:** Discrete time step in the simulation (default 50ms, configurable per session)
- **Order Book:** Current snapshot of bid/ask orders at each price level
- **Bid/Ask Spread:** Difference between highest bid and lowest ask price
- **PnL:** Profit/Loss, calculated as (current_value - initial_value)
- **Drawdown:** Peak-to-trough decline in portfolio value
- **Sharpe Ratio:** Risk-adjusted return metric (excess return per unit volatility)
- **Glicko-2:** Rating system used for multiplayer ranking
- **Grace Period:** 30-second window for reconnection without session loss
