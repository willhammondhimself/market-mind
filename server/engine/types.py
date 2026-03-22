"""Engine-specific types. Re-exports shared types for convenience."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Awaitable, Callable

from server.types import (
    AgentAction,
    AgentObservation,
    BookState,
    GameMode,
    NewsEvent,
    OrderRecord,
    OrderRequest,
    OrderResult,
    OrderSide,
    RawSessionData,
    SessionConfig,
    SessionResult,
    SessionState,
    SessionStatus,
    TradeRecord,
)

# Re-export for convenience
__all__ = [
    "AgentAction",
    "AgentObservation",
    "BookState",
    "GameMode",
    "NewsEvent",
    "OrderRecord",
    "OrderRequest",
    "OrderResult",
    "OrderSide",
    "RawSessionData",
    "SessionConfig",
    "SessionResult",
    "SessionState",
    "SessionStatus",
    "TradeRecord",
    "GameEvent",
    "InternalOrder",
    "AssetConfig",
]


@dataclass
class GameEvent:
    """Event emitted by the engine for the API layer to broadcast."""
    event_type: str  # "book_update", "trade", "fill", "pnl", "news", "alert", "session_state", "score"
    data: dict
    session_id: str
    timestamp: int


@dataclass
class InternalOrder:
    """Internal order representation within the matching engine."""
    order_id: str
    owner_id: str
    asset: str
    side: OrderSide
    price: float
    size: int
    remaining_size: int
    timestamp: int
    is_player: bool = False


@dataclass
class AssetConfig:
    """Configuration for a tradeable asset."""
    ticker: str
    name: str
    tick_size: float
    lot_size: int
    price_range: tuple[float, float]
    initial_price: float
    volatility_base: float
    difficulty: int  # 1-10
    tier_unlock: int
    price_process: str  # "news_driven", "regime_switching", "heston"
