"""
MarketMind — Shared Server Types

All server modules import from this file to ensure type consistency
across module boundaries. These types match the contracts in docs/CONTRACTS.md.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Literal


# ===== Enums =====

class GameMode(str, Enum):
    CAREER = "career"
    PRACTICE = "practice"
    CHALLENGE = "challenge"
    MULTIPLAYER = "multiplayer"


class OrderSide(str, Enum):
    BID = "bid"
    ASK = "ask"


class OrderStatus(str, Enum):
    ACTIVE = "active"
    FILLED = "filled"
    PARTIAL = "partial"
    CANCELLED = "cancelled"


class SessionStatus(str, Enum):
    COUNTDOWN = "countdown"
    ACTIVE = "active"
    ENDING = "ending"
    ENDED = "ended"
    FORFEITED = "forfeited"
    VOIDED = "voided"


class AgentType(str, Enum):
    NOISE = "noise"
    INFORMED = "informed"
    MOMENTUM = "momentum"
    ADVERSARIAL_MM = "adversarial_mm"
    RL = "rl"
    EVOLUTIONARY = "evo"
    LLM = "llm"


class NewsType(str, Enum):
    EARNINGS = "earnings"
    MACRO = "macro"
    SECTOR = "sector"
    GEOPOLITICAL = "geopolitical"
    COMPANY = "company"


class AlertType(str, Enum):
    INVENTORY_WARNING = "inventory_warning"
    TIME_WARNING = "time_warning"
    SESSION_END = "session_end"
    COUNTDOWN = "countdown"


class Severity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class LetterGrade(str, Enum):
    S = "S"
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    F = "F"


class SessionLength(str, Enum):
    TWO_MIN = "2min"
    FIVE_MIN = "5min"
    FIFTEEN_MIN = "15min"
    ENDLESS = "endless"


class ChallengeMode(str, Enum):
    SPEED = "speed"
    NEWS_STORM = "news_storm"
    SHARK_TANK = "shark_tank"
    THIN_BOOK = "thin_book"
    VOLATILITY_REGIME = "volatility_regime"
    NIGHTMARE = "nightmare"


class TierTitle(str, Enum):
    INTERN = "Intern"
    ANALYST = "Analyst"
    ASSOCIATE = "Associate"
    TRADER = "Trader"
    SENIOR_TRADER = "Senior Trader"
    VP = "VP"
    DIRECTOR = "Director"
    MD = "MD"
    PARTNER = "Partner"
    FOUNDER = "Founder"
    LEGEND = "Legend"


# ===== Session Config =====

@dataclass
class SessionConfig:
    mode: GameMode
    assets: list[str]
    session_length: SessionLength
    buy_in_amount: float = 0.0
    challenge_modes: list[ChallengeMode] = field(default_factory=list)
    preview_book: bool = False
    player_id: str = ""


# ===== Order Book Types =====

@dataclass
class PriceLevel:
    price: float
    size: int


@dataclass
class BookState:
    asset: str
    bids: list[tuple[float, int]]   # [(price, size)] best first
    asks: list[tuple[float, int]]   # [(price, size)] best first
    timestamp: int = 0


# ===== Order Types =====

@dataclass
class OrderRequest:
    player_id: str
    asset: str
    side: OrderSide
    price: float
    size: int
    order_type: Literal["limit"] = "limit"


@dataclass
class OrderResult:
    order_id: str
    status: OrderStatus
    filled_size: int = 0
    fill_price: float = 0.0
    remaining_size: int = 0
    error: str | None = None


@dataclass
class OrderRecord:
    order_id: str
    session_id: str
    owner_id: str                   # player_id or agent_id
    asset: str
    side: OrderSide
    price: float
    size: int
    order_type: str
    status: OrderStatus
    fill_price: float = 0.0
    fill_size: int = 0
    timestamp: int = 0


# ===== Trade Types =====

@dataclass
class TradeRecord:
    trade_id: str
    session_id: str
    asset: str
    buy_order_id: str
    sell_order_id: str
    price: float
    size: int
    timestamp: int
    aggressor_side: Literal["buy", "sell"]
    fair_value_at_trade: float = 0.0
    counterparty_type: Literal["informed", "noise", "momentum", "player"] = "noise"


@dataclass
class TradeInfo:
    """Lightweight trade info for agent observations."""
    price: float
    size: int
    aggressor_side: Literal["buy", "sell"]
    timestamp: int


# ===== News Types =====

@dataclass
class NewsEvent:
    headline: str
    news_type: NewsType
    affected_assets: list[str]
    fair_value_impact: dict[str, float]   # asset -> delta
    timestamp: int = 0
    is_fake: bool = False


@dataclass
class NewsEventRecord:
    headline: str
    news_type: NewsType
    affected_assets: list[str]
    timestamp: int
    is_fake: bool = False


# ===== Agent Types =====

@dataclass
class AssetObservation:
    fair_value: float               # only meaningful for informed agents
    bids: list[tuple[float, int]]
    asks: list[tuple[float, int]]
    last_trades: list[TradeInfo]
    current_price: float
    volatility: float
    news_events: list[NewsEvent]


@dataclass
class AgentObservation:
    tick: int
    timestamp: int
    assets: dict[str, AssetObservation]
    time_remaining_ms: int
    player_estimated_inventory: dict[str, int]


@dataclass
class AgentAction:
    action_type: Literal["place_order", "cancel_order", "modify_order"]
    asset: str
    side: OrderSide | None = None
    price: float | None = None
    size: int | None = None
    order_id: str | None = None


# ===== Session Result Types =====

@dataclass
class SessionState:
    session_id: str
    status: SessionStatus
    time_remaining_ms: int
    tick: int
    assets: list[str]


@dataclass
class SessionResult:
    session_id: str
    player_id: str
    mode: GameMode
    final_pnl: float
    duration_seconds: int
    assets_traded: list[str]


# ===== Analytics Types =====

@dataclass
class TickSnapshot:
    tick: int
    timestamp: int
    player_inventory: dict[str, int]
    player_realized_pnl: float
    player_unrealized_pnl: float
    book_state: dict[str, BookState]
    player_active_orders: list[OrderRecord]


@dataclass
class RawSessionData:
    session_id: str
    player_id: str
    mode: GameMode
    duration_seconds: int
    buy_in: float
    assets: list[str]
    difficulty_band: int
    snapshots: list[TickSnapshot]
    trades: list[TradeRecord]
    orders: list[OrderRecord]
    news_events: list[NewsEventRecord]
    fair_value_paths: dict[str, list[tuple[int, float]]]


@dataclass
class ComponentScores:
    pnl: float
    sharpe: float
    spread_efficiency: float
    max_drawdown: float
    inventory_management: float


@dataclass
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


@dataclass
class DebriefData:
    session_id: str
    letter_grade: LetterGrade
    composite_score: float
    component_scores: ComponentScores
    pnl_curve: list[tuple[int, float]]
    fair_value_overlay: dict[str, list[tuple[int, float]]]
    per_asset_pnl: dict[str, float]
    inventory_heatmap: dict[str, list[tuple[int, int]]]
    time_weighted_avg_inventory: dict[str, float]
    classified_trades: list[ClassifiedTrade]
    spread_efficiency: float
    optimal_spread: float
    behavioral_patterns: list[str]
    skill_spider: dict[str, float] | None = None
    historical_pnl: list[tuple[str, float]] | None = None


# ===== Tier Constants =====

TIER_THRESHOLDS: dict[int, tuple[str, float]] = {
    1:  ("Intern",        100_000),
    2:  ("Analyst",       150_000),
    3:  ("Associate",     250_000),
    4:  ("Trader",        500_000),
    5:  ("Senior Trader", 1_000_000),
    6:  ("VP",            2_000_000),
    7:  ("Director",      4_000_000),
    8:  ("MD",            8_000_000),
    9:  ("Partner",       16_000_000),
    10: ("Founder",       30_000_000),
    11: ("Legend",         50_000_000),
}


def get_tier_for_capital(capital: float) -> tuple[int, str]:
    """Returns (tier_number, tier_title) for a given capital amount."""
    for tier in range(11, 0, -1):
        title, threshold = TIER_THRESHOLDS[tier]
        if capital >= threshold:
            return tier, title
    return 1, "Intern"


# ===== Streak Constants =====

STREAK_MULTIPLIERS: dict[int, float] = {
    3: 1.1,
    5: 1.25,
    10: 1.5,
}
MAX_MULTIPLIER = 3.0


def get_streak_multiplier(streak_count: int) -> float:
    """Returns the multiplier for a given streak count."""
    multiplier = 1.0
    for threshold, mult in sorted(STREAK_MULTIPLIERS.items()):
        if streak_count >= threshold:
            multiplier = mult
    return min(multiplier, MAX_MULTIPLIER)
