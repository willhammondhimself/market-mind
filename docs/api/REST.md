# MarketMind — REST API Specification

**Base URL:** `/api`
**Auth:** JWT Bearer token in `Authorization` header
**Content-Type:** `application/json`

---

## Auth Endpoints

### POST /api/auth/register

Create a new user account.

**Auth Required:** No

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**Response (201 Created):**
```json
{
  "user_id": "string (UUID)",
  "username": "string",
  "email": "string",
  "token": "string (JWT)",
  "created_at": "string (ISO 8601)"
}
```

**Error Responses:**
- `400 Bad Request` — Validation error (missing fields, invalid email format)
- `409 Conflict` — Username or email already exists

---

### POST /api/auth/login

Authenticate user and get access token.

**Auth Required:** No

**Request Body:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Response (200 OK):**
```json
{
  "user_id": "string (UUID)",
  "token": "string (JWT, expires in 24h)",
  "refresh_token": "string (JWT, expires in 30d)",
  "expires_in": "number (seconds)"
}
```

**Error Responses:**
- `400 Bad Request` — Validation error
- `401 Unauthorized` — Invalid credentials

---

### POST /api/auth/refresh

Obtain a new access token using a refresh token.

**Auth Required:** No

**Request Body:**
```json
{
  "refresh_token": "string"
}
```

**Response (200 OK):**
```json
{
  "token": "string (JWT, expires in 24h)",
  "expires_in": "number (seconds)"
}
```

**Error Responses:**
- `400 Bad Request` — Missing refresh_token
- `401 Unauthorized` — Invalid or expired refresh_token

---

## Sessions Endpoints

### POST /api/sessions

Create a new game session.

**Auth Required:** Yes (JWT Bearer)

**Request Body:**
```json
{
  "mode": "string (career | sandbox | tutorial)",
  "difficulty": "number (1-11, tier level)",
  "starting_capital": "number (optional, overrides tier default)",
  "duration": "number (optional, session length in minutes)"
}
```

**Response (201 Created):**
```json
{
  "session_id": "string (UUID)",
  "user_id": "string (UUID)",
  "mode": "string",
  "difficulty": "number",
  "starting_capital": "number",
  "started_at": "string (ISO 8601)",
  "state": "string (countdown | active | ended)",
  "countdown_seconds": "number (null if not in countdown)"
}
```

**Error Responses:**
- `401 Unauthorized` — Invalid or missing token
- `400 Bad Request` — Invalid session config
- `429 Too Many Requests` — Session limit exceeded

---

### GET /api/sessions/:id

Get session summary (non-debrief data).

**Auth Required:** Yes (JWT Bearer)

**Response (200 OK):**
```json
{
  "session_id": "string (UUID)",
  "user_id": "string (UUID)",
  "mode": "string",
  "difficulty": "number",
  "starting_capital": "number",
  "current_capital": "number",
  "state": "string (countdown | active | ended)",
  "started_at": "string (ISO 8601)",
  "ended_at": "string (ISO 8601, null if ongoing)",
  "tick_count": "number",
  "final_score": "number (null if ongoing)"
}
```

**Error Responses:**
- `401 Unauthorized` — Invalid token
- `403 Forbidden` — Session not owned by user
- `404 Not Found` — Session does not exist

---

### GET /api/sessions/:id/debrief

Get full debrief data with trades, analytics, and performance summary.

**Auth Required:** Yes (JWT Bearer)

**Response (200 OK):**
```json
{
  "session_id": "string (UUID)",
  "user_id": "string (UUID)",
  "mode": "string",
  "difficulty": "number",
  "starting_capital": "number",
  "final_capital": "number",
  "total_return_pct": "number",
  "total_profit_loss": "number",
  "max_drawdown_pct": "number",
  "sharpe_ratio": "number",
  "win_rate_pct": "number",
  "trades": [
    {
      "trade_id": "string",
      "symbol": "string",
      "side": "string (buy | sell)",
      "entry_price": "number",
      "entry_tick": "number",
      "exit_price": "number",
      "exit_tick": "number",
      "quantity": "number",
      "profit_loss": "number",
      "profit_loss_pct": "number"
    }
  ],
  "news_events": [
    {
      "tick": "number",
      "symbol": "string",
      "headline": "string",
      "impact_type": "string (positive | negative | neutral)",
      "price_change_pct": "number"
    }
  ],
  "started_at": "string (ISO 8601)",
  "ended_at": "string (ISO 8601)",
  "duration_seconds": "number"
}
```

**Error Responses:**
- `401 Unauthorized` — Invalid token
- `403 Forbidden` — Session not owned by user
- `404 Not Found` — Session does not exist

---

### GET /api/sessions/history

Get paginated session history for authenticated user.

**Auth Required:** Yes (JWT Bearer)

**Query Parameters:**
- `page` (integer, default=1) — Page number
- `limit` (integer, default=20, max=100) — Results per page

**Response (200 OK):**
```json
{
  "sessions": [
    {
      "session_id": "string (UUID)",
      "mode": "string",
      "difficulty": "number",
      "starting_capital": "number",
      "final_capital": "number",
      "total_return_pct": "number",
      "started_at": "string (ISO 8601)",
      "ended_at": "string (ISO 8601)",
      "duration_seconds": "number"
    }
  ],
  "pagination": {
    "page": "number",
    "limit": "number",
    "total": "number",
    "pages": "number"
  }
}
```

**Error Responses:**
- `401 Unauthorized` — Invalid token
- `400 Bad Request` — Invalid pagination params

---

### POST /api/sessions/:id/end

Force end an active session early.

**Auth Required:** Yes (JWT Bearer)

**Response (200 OK):**
```json
{
  "session_id": "string (UUID)",
  "state": "string (ended)",
  "ended_at": "string (ISO 8601)",
  "final_capital": "number",
  "total_return_pct": "number"
}
```

**Error Responses:**
- `401 Unauthorized` — Invalid token
- `403 Forbidden` — Session not owned by user
- `404 Not Found` — Session does not exist
- `409 Conflict` — Session already ended

---

## Users Endpoints

### GET /api/users/me

Get authenticated user's profile.

**Auth Required:** Yes (JWT Bearer)

**Response (200 OK):**
```json
{
  "user_id": "string (UUID)",
  "username": "string",
  "email": "string",
  "display_name": "string (optional)",
  "tier": "number (1-11)",
  "career_capital": "number",
  "total_sessions": "number",
  "glicko2_rating": "number",
  "glicko2_rd": "number",
  "created_at": "string (ISO 8601)",
  "updated_at": "string (ISO 8601)"
}
```

**Error Responses:**
- `401 Unauthorized` — Invalid or missing token

---

### PATCH /api/users/me

Update authenticated user's profile.

**Auth Required:** Yes (JWT Bearer)

**Request Body:**
```json
{
  "username": "string (optional)",
  "email": "string (optional)",
  "display_name": "string (optional)",
  "password": "string (optional, current password required in separate field)"
}
```

**Response (200 OK):**
```json
{
  "user_id": "string (UUID)",
  "username": "string",
  "email": "string",
  "display_name": "string",
  "updated_at": "string (ISO 8601)"
}
```

**Error Responses:**
- `401 Unauthorized` — Invalid token
- `400 Bad Request` — Validation error
- `409 Conflict` — Username or email already exists

---

### GET /api/users/:id

Get public profile for another user.

**Auth Required:** Yes (JWT Bearer)

**Response (200 OK):**
```json
{
  "user_id": "string (UUID)",
  "username": "string",
  "display_name": "string",
  "tier": "number (1-11)",
  "glicko2_rating": "number",
  "total_sessions": "number",
  "created_at": "string (ISO 8601)"
}
```

**Error Responses:**
- `401 Unauthorized` — Invalid token
- `404 Not Found` — User does not exist

---

### POST /api/users/me/settings

Update user settings (keybindings, defaults, theme).

**Auth Required:** Yes (JWT Bearer)

**Request Body:**
```json
{
  "theme": "string (light | dark | system)",
  "keybindings": {
    "buy": "string (keyboard key)",
    "sell": "string (keyboard key)",
    "cancel_all": "string (keyboard key)"
  },
  "defaults": {
    "order_size": "number",
    "order_type": "string (market | limit)"
  },
  "notifications": {
    "email_alerts": "boolean",
    "sound_alerts": "boolean"
  }
}
```

**Response (200 OK):**
```json
{
  "user_id": "string (UUID)",
  "settings": {
    "theme": "string",
    "keybindings": "object",
    "defaults": "object",
    "notifications": "object"
  },
  "updated_at": "string (ISO 8601)"
}
```

**Error Responses:**
- `401 Unauthorized` — Invalid token
- `400 Bad Request` — Invalid settings format

---

### POST /api/users/me/api-key

Set or update BYO API key (encrypted server-side).

**Auth Required:** Yes (JWT Bearer)

**Request Body:**
```json
{
  "api_key": "string",
  "provider": "string (openai | anthropic | other)"
}
```

**Response (200 OK):**
```json
{
  "user_id": "string (UUID)",
  "provider": "string",
  "key_fingerprint": "string (last 8 chars only, for verification)",
  "set_at": "string (ISO 8601)"
}
```

**Error Responses:**
- `401 Unauthorized` — Invalid token
- `400 Bad Request` — Invalid API key format

---

### POST /api/users/me/reset-career

Reset user's career progression back to Tier 1 with $100K capital.

**Auth Required:** Yes (JWT Bearer)

**Response (200 OK):**
```json
{
  "user_id": "string (UUID)",
  "tier": "number (1)",
  "career_capital": "number (100000)",
  "reset_at": "string (ISO 8601)"
}
```

**Error Responses:**
- `401 Unauthorized` — Invalid token

---

### DELETE /api/users/me

Delete user account (permanently removes all data after grace period).

**Auth Required:** Yes (JWT Bearer)

**Response (204 No Content)**

**Error Responses:**
- `401 Unauthorized` — Invalid token
- `400 Bad Request` — Account has pending actions

---

## Social Endpoints

### GET /api/friends

List all friends for authenticated user.

**Auth Required:** Yes (JWT Bearer)

**Response (200 OK):**
```json
{
  "friends": [
    {
      "user_id": "string (UUID)",
      "username": "string",
      "display_name": "string",
      "tier": "number (1-11)",
      "glicko2_rating": "number",
      "added_at": "string (ISO 8601)"
    }
  ],
  "count": "number"
}
```

**Error Responses:**
- `401 Unauthorized` — Invalid token

---

### POST /api/friends/:user_id

Add another user as a friend.

**Auth Required:** Yes (JWT Bearer)

**Response (201 Created):**
```json
{
  "friend_id": "string (UUID)",
  "username": "string",
  "added_at": "string (ISO 8601)"
}
```

**Error Responses:**
- `401 Unauthorized` — Invalid token
- `404 Not Found` — User does not exist
- `409 Conflict` — Already friends or cannot add self

---

### DELETE /api/friends/:user_id

Remove a user from friends list.

**Auth Required:** Yes (JWT Bearer)

**Response (204 No Content)**

**Error Responses:**
- `401 Unauthorized` — Invalid token
- `404 Not Found` — User not in friends list

---

## Leaderboards Endpoints

### GET /api/leaderboards/capital

Get capital leaderboard with filtering options.

**Auth Required:** Yes (JWT Bearer)

**Query Parameters:**
- `scope` (string, default=global) — global | friends | tier
- `tier` (integer, 1-11, optional) — Filter by tier
- `limit` (integer, default=50, max=500) — Number of results

**Response (200 OK):**
```json
{
  "leaderboard": [
    {
      "rank": "number",
      "user_id": "string (UUID)",
      "username": "string",
      "tier": "number",
      "career_capital": "number",
      "sessions_completed": "number"
    }
  ],
  "metadata": {
    "scope": "string",
    "tier": "number (optional)",
    "updated_at": "string (ISO 8601)",
    "your_rank": "number (optional)"
  }
}
```

**Error Responses:**
- `401 Unauthorized` — Invalid token
- `400 Bad Request` — Invalid scope or tier

---

### GET /api/leaderboards/rating

Get Glicko-2 rating leaderboard with same filtering options.

**Auth Required:** Yes (JWT Bearer)

**Query Parameters:**
- `scope` (string, default=global) — global | friends | tier
- `tier` (integer, 1-11, optional) — Filter by tier
- `limit` (integer, default=50, max=500) — Number of results

**Response (200 OK):**
```json
{
  "leaderboard": [
    {
      "rank": "number",
      "user_id": "string (UUID)",
      "username": "string",
      "tier": "number",
      "glicko2_rating": "number",
      "glicko2_rd": "number",
      "matches_played": "number"
    }
  ],
  "metadata": {
    "scope": "string",
    "tier": "number (optional)",
    "updated_at": "string (ISO 8601)",
    "your_rank": "number (optional)"
  }
}
```

**Error Responses:**
- `401 Unauthorized` — Invalid token
- `400 Bad Request` — Invalid scope or tier

---

## Multiplayer Endpoints

### POST /api/rooms

Create a new multiplayer game room with an invite code.

**Auth Required:** Yes (JWT Bearer)

**Request Body:**
```json
{
  "mode": "string (casual | ranked)",
  "max_players": "number (2-8, default=2)",
  "difficulty": "number (1-11)"
}
```

**Response (201 Created):**
```json
{
  "room_id": "string (UUID)",
  "invite_code": "string (6-8 alphanumeric)",
  "created_by": "string (UUID)",
  "mode": "string",
  "difficulty": "number",
  "max_players": "number",
  "current_players": "number (1)",
  "created_at": "string (ISO 8601)"
}
```

**Error Responses:**
- `401 Unauthorized` — Invalid token
- `400 Bad Request` — Invalid room config

---

### GET /api/rooms/:code

Get room information by invite code.

**Auth Required:** Yes (JWT Bearer)

**Response (200 OK):**
```json
{
  "room_id": "string (UUID)",
  "invite_code": "string",
  "mode": "string",
  "difficulty": "number",
  "max_players": "number",
  "current_players": "number",
  "players": [
    {
      "user_id": "string (UUID)",
      "username": "string",
      "ready": "boolean"
    }
  ],
  "created_at": "string (ISO 8601)",
  "game_state": "string (waiting | starting | active | ended)"
}
```

**Error Responses:**
- `401 Unauthorized` — Invalid token
- `404 Not Found` — Room does not exist

---

### POST /api/rooms/:code/join

Join an existing multiplayer room.

**Auth Required:** Yes (JWT Bearer)

**Response (200 OK):**
```json
{
  "room_id": "string (UUID)",
  "invite_code": "string",
  "joined_at": "string (ISO 8601)",
  "current_players": "number"
}
```

**Error Responses:**
- `401 Unauthorized` — Invalid token
- `404 Not Found` — Room does not exist
- `409 Conflict` — Room is full or game already started

---

### POST /api/matchmaking/queue

Enter the ranked matchmaking queue.

**Auth Required:** Yes (JWT Bearer)

**Request Body:**
```json
{
  "difficulty": "number (1-11, optional, uses user tier if omitted)"
}
```

**Response (202 Accepted):**
```json
{
  "queue_id": "string (UUID)",
  "position": "number",
  "estimated_wait_seconds": "number"
}
```

**Error Responses:**
- `401 Unauthorized` — Invalid token
- `409 Conflict` — Already in queue

---

### DELETE /api/matchmaking/queue

Leave the ranked matchmaking queue.

**Auth Required:** Yes (JWT Bearer)

**Response (204 No Content)**

**Error Responses:**
- `401 Unauthorized` — Invalid token
- `404 Not Found` — Not in queue

---

## Error Response Format

All error responses follow this standard format:

```json
{
  "error": {
    "code": "string (UPPERCASE_ERROR_CODE)",
    "message": "string",
    "details": "object (optional, context-specific)"
  }
}
```

**Common Error Codes:**
- `INVALID_REQUEST` — Malformed request
- `UNAUTHORIZED` — Missing or invalid authentication
- `FORBIDDEN` — Authenticated but not authorized for resource
- `NOT_FOUND` — Resource does not exist
- `CONFLICT` — Request conflicts with current state
- `VALIDATION_ERROR` — Request validation failed
- `RATE_LIMITED` — Too many requests
- `INTERNAL_ERROR` — Server error

---

## Authentication

All endpoints marked "Auth Required: Yes" expect the JWT token in the Authorization header:

```
Authorization: Bearer <jwt_token>
```

Tokens expire in 24 hours. Use the refresh endpoint to obtain a new token.

---

## Rate Limiting

Rate limits applied per user per endpoint:
- Auth endpoints: 10 requests/minute
- Public endpoints: 60 requests/minute
- Game endpoints: 300 requests/minute

Rate limit information returned in response headers:
- `X-RateLimit-Limit` — Request limit
- `X-RateLimit-Remaining` — Requests remaining
- `X-RateLimit-Reset` — Unix timestamp of reset time
