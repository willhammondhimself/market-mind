import type { LetterGrade } from './game';

export interface DebriefData {
  session_id: string;
  letter_grade: LetterGrade;
  composite_score: number;
  component_scores: ComponentScores;

  // Performance tab
  pnl_curve: [number, number][];          // [timestamp, total_pnl]
  fair_value_overlay: Record<string, [number, number][]>;
  per_asset_pnl: Record<string, number>;

  // Inventory tab
  inventory_heatmap: Record<string, [number, number][]>;  // asset -> [timestamp, position]
  time_weighted_avg_inventory: Record<string, number>;

  // Trades tab
  classified_trades: ClassifiedTrade[];
  spread_efficiency: number;
  optimal_spread: number;
  behavioral_patterns: string[];

  // Session-over-session (if available)
  skill_spider: SkillSpider | null;
  historical_pnl: [string, number][] | null;  // [session_id, pnl]
}

export interface ComponentScores {
  pnl: number;
  sharpe: number;
  spread_efficiency: number;
  max_drawdown: number;
  inventory_management: number;
}

export interface ClassifiedTrade {
  trade_id: string;
  timestamp: number;
  asset: string;
  side: 'bid' | 'ask';
  price: number;
  size: number;
  counterparty_type: 'informed' | 'noise' | 'momentum' | 'player';
  counterparty_id: string;
  pnl_impact: number;
}

export interface SkillSpider {
  spread_management: number;
  inventory_control: number;
  speed: number;
  adverse_selection: number;
  news_reaction: number;
  risk_management: number;
}

export interface SessionTrend {
  session_id: string;
  date: string;
  pnl: number;
  sharpe: number;
  letter_grade: LetterGrade;
  composite_score: number;
}
