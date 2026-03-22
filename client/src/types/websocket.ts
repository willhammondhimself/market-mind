// ===== Client → Server Messages =====

export interface OrderMessage {
  type: 'order';
  asset: string;
  side: 'bid' | 'ask';
  price: number;
  size: number;
  order_type: 'limit';
}

export interface CancelMessage {
  type: 'cancel';
  order_id: string;
}

export interface ModifyMessage {
  type: 'modify';
  order_id: string;
  new_price: number | null;
  new_size: number | null;
}

export interface CancelAllMessage {
  type: 'cancel_all';
  asset: string | null;
}

export interface PingMessage {
  type: 'ping';
}

export type ClientMessage = OrderMessage | CancelMessage | ModifyMessage | CancelAllMessage | PingMessage;

// ===== Server → Client Messages =====

export interface BookUpdate {
  channel: 'book';
  asset: string;
  bids: [number, number][];  // [price, size]
  asks: [number, number][];
  timestamp: number;
}

export interface TradeUpdate {
  channel: 'trade';
  asset: string;
  price: number;
  size: number;
  aggressor_side: 'buy' | 'sell';
  is_yours: boolean;
  counterparty: string | null;
  timestamp: number;
}

export interface FillUpdate {
  channel: 'fill';
  asset: string;
  order_id: string;
  side: 'bid' | 'ask';
  price: number;
  size: number;
  remaining_size: number;
  timestamp: number;
}

export interface PnLUpdate {
  channel: 'pnl';
  realized: number;
  unrealized: number;
  inventory: Record<string, number>;
  total_pnl: number;
  timestamp: number;
}

export interface NewsUpdate {
  channel: 'news';
  headline: string;
  news_type: 'earnings' | 'macro' | 'sector' | 'geopolitical' | 'company';
  affected_assets: string[];
  timestamp: number;
}

export interface AlertUpdate {
  channel: 'alert';
  alert_type: 'inventory_warning' | 'time_warning' | 'session_end' | 'countdown';
  message: string;
  severity: 'info' | 'warning' | 'critical';
  timestamp: number;
}

export interface SessionStateUpdate {
  channel: 'session_state';
  state: 'countdown' | 'active' | 'ending' | 'ended';
  countdown_value: number | null;
  time_remaining_ms: number | null;
  timestamp: number;
}

export interface ScoreUpdate {
  channel: 'score';
  letter_grade: 'S' | 'A' | 'B' | 'C' | 'D' | 'F';
  composite_score: number;
  pnl: number;
  sharpe: number;
  max_drawdown: number;
  avg_spread: number;
  capital_change: number;
  new_capital: number;
  streak_count: number;
  multiplier: number;
}

export interface PongMessage {
  channel: 'pong';
}

export interface ErrorMessage {
  channel: 'error';
  code: string;
  message: string;
}

export type ServerMessage =
  | BookUpdate
  | TradeUpdate
  | FillUpdate
  | PnLUpdate
  | NewsUpdate
  | AlertUpdate
  | SessionStateUpdate
  | ScoreUpdate
  | PongMessage
  | ErrorMessage;
