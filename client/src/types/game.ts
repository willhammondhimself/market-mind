import type { TradeUpdate, NewsUpdate } from './websocket';

export type GameMode = 'career' | 'practice' | 'challenge' | 'multiplayer';
export type SessionLength = '2min' | '5min' | '15min' | 'endless';
export type ChallengeMode = 'speed' | 'news_storm' | 'shark_tank' | 'thin_book' | 'volatility_regime' | 'nightmare';
export type LetterGrade = 'S' | 'A' | 'B' | 'C' | 'D' | 'F';
export type OrderSide = 'bid' | 'ask';

export interface SessionConfig {
  mode: GameMode;
  assets: string[];
  session_length: SessionLength;
  buy_in_amount: number;
  challenge_modes?: ChallengeMode[];
  preview_book?: boolean;
}

export interface SessionSummary {
  session_id: string;
  mode: GameMode;
  letter_grade: LetterGrade;
  composite_score: number;
  final_pnl: number;
  capital_change: number;
  duration_seconds: number;
  assets_traded: string[];
  created_at: string;  // ISO 8601
}

export interface ActiveOrder {
  order_id: string;
  asset: string;
  side: OrderSide;
  price: number;
  size: number;
  filled_size: number;
  timestamp: number;
}

export interface AssetConfig {
  ticker: string;
  name: string;
  tick_size: number;
  lot_size: number;
  price_range: [number, number];  // [min, max]
  difficulty: number;             // 1-10
  tier_unlock: number;            // minimum tier to access
}

export interface OrderBookState {
  asset: string;
  bids: [number, number][];
  asks: [number, number][];
  spread: number;
  mid_price: number;
}

export interface GameState {
  session_id: string;
  status: 'countdown' | 'active' | 'ending' | 'ended';
  time_remaining_ms: number;
  books: Record<string, OrderBookState>;
  inventory: Record<string, number>;
  realized_pnl: number;
  unrealized_pnl: number;
  total_pnl: number;
  active_orders: ActiveOrder[];
  recent_trades: TradeUpdate[];
  recent_news: NewsUpdate[];
}
