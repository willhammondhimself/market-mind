import type { SessionLength } from './game';

export type TierTitle = 'Intern' | 'Analyst' | 'Associate' | 'Trader' | 'Senior Trader' | 'VP' | 'Director' | 'MD' | 'Partner' | 'Founder' | 'Legend';

export interface UserProfile {
  user_id: string;
  username: string;
  email: string;
  avatar_url: string | null;
  career_capital: number;
  tier: number;              // 1-11
  tier_title: TierTitle;
  glicko_rating: number;
  glicko_rd: number;
  streak_count: number;
  created_at: string;        // ISO 8601
}

export interface PublicProfile {
  user_id: string;
  username: string;
  avatar_url: string | null;
  tier: number;
  tier_title: TierTitle;
  career_capital: number;    // exact or range
  glicko_rating: number;
}

export interface Friend {
  user_id: string;
  username: string;
  avatar_url: string | null;
  tier: number;
  tier_title: TierTitle;
  career_capital: number;
  online: boolean;
  in_session: boolean;
}

export interface LeaderboardEntry {
  rank: number;
  user_id: string;
  username: string;
  avatar_url: string | null;
  tier: number;
  tier_title: TierTitle;
  value: number;             // capital or rating depending on board
  is_self: boolean;
}

export interface UserSettings {
  keybindings: Record<string, string>;  // action → key
  default_session_length: SessionLength;
  default_buy_in_pct: number;
  default_assets: string[];
  theme: 'light' | 'dark' | 'system';
  sound_master_volume: number;        // 0-100
  sound_fills_enabled: boolean;
  sound_alerts_enabled: boolean;
  sound_system_enabled: boolean;
}

export interface AuthTokens {
  token: string;
  refresh_token: string;
  user_id: string;
}
