# MarketMind — Definitive Product Requirements Document

**Version:** 2.0 — Final Specification
**Author:** Will Hammond
**Date:** March 21, 2026
**Status:** Ready for Build

> **⚠️ REMINDER:** Before building any UI, create mockups using Google's frontend design tool (Stitch / Firebase Studio). Use the `/mnt/skills/public/frontend-design/SKILL.md` skill for all UI implementation — no AI slop. Every interface should feel hand-designed, distinctive, and production-grade.

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Product Identity](#2-product-identity)
3. [Core Gameplay Loop](#3-core-gameplay-loop)
4. [Career Mode & Progression](#4-career-mode--progression)
5. [Practice Mode](#5-practice-mode)
6. [Assets & Market Simulation](#6-assets--market-simulation)
7. [News & Information System](#7-news--information-system)
8. [AI Agent Architecture](#8-ai-agent-architecture)
9. [Multiplayer System](#9-multiplayer-system)
10. [Challenge Modes](#10-challenge-modes)
11. [Analytics & Debrief](#11-analytics--debrief)
12. [AI Coaching System](#12-ai-coaching-system)
13. [Scoring, Streaks & Multipliers](#13-scoring-streaks--multipliers)
14. [UI/UX Specification](#14-uiux-specification)
15. [Audio Design](#15-audio-design)
16. [Onboarding & Tutorial](#16-onboarding--tutorial)
17. [Social & Profile System](#17-social--profile-system)
18. [Leaderboards](#18-leaderboards)
19. [Tournament System](#19-tournament-system)
20. [Monetization](#20-monetization)
21. [Technical Architecture](#21-technical-architecture)
22. [Multi-Agent Claude Code Development](#22-multi-agent-claude-code-development)
23. [Infrastructure & Deployment](#23-infrastructure--deployment)
24. [Data Model](#24-data-model)
25. [Error Handling & Edge Cases](#25-error-handling--edge-cases)
26. [Phased Roadmap](#26-phased-roadmap)
27. [Open Questions & Future Features](#27-open-questions--future-features)

---

## 1. Executive Summary

**MarketMind** is a real-time market making simulator where players quote bid/ask prices on a live continuous order book with 15+ tradeable assets while AI agents — ranging from rule-based bots to reinforcement learning agents to LLM-powered reasoners — act as counterparties. The bots adapt to the player's style over time, silently exploiting weaknesses in their quoting behavior, inventory management, and adverse selection handling. The game features a persistent career mode with permadeath, a buy-in system for capital allocation, a tier progression from Intern to Legend, and real-time multiplayer where 2–4 market makers compete for flow on the same book with career capital at stake.

**Primary purpose:** Monetizable product that Will also genuinely uses as a personal training tool.

**Target audience:** Quant interview candidates, trading club members (Student Quant Fund, Claremont network), and anyone building intuition for market microstructure.

**Launch strategy:** Private beta with 5–10 friends → Student Quant Fund → broader rollout.

**What makes MarketMind different:** Adaptive AI opponents that silently learn your weaknesses + continuous multi-asset order book + persistent career mode with permadeath + real-time multiplayer. Nobody else has all four.

---

## 2. Product Identity

- **Name:** MarketMind
- **Tagline:** TBD (not needed for beta)
- **Brand:** Standalone (not under CruxAI)
- **Landing page:** None for v1 — ship the product, share directly
- **License:** Source-available (viewable on GitHub but not forkable without license)
- **Repository:** `github.com/willhammondhimself/marketmind` (or similar)
- **Repo structure:** Monorepo — `marketmind/client/` and `marketmind/server/`

---

## 3. Core Gameplay Loop

### 3.1 Session Flow

1. **Home dashboard** → two clicks to play (pick mode → play)
2. **Pre-session config** (Quick Play with saved defaults, or Advanced Config for power users):
   - Select mode: Career / Practice / Challenge / Multiplayer
   - Select assets (from unlocked pool)
   - Set buy-in amount (career mode)
   - Set session length: 2 min / 5 min / 15 min / Endless
   - Optional: pay a small capital fee for 10-second book preview
3. **Countdown:** 3… 2… 1… GO — immediate trading
4. **Live session:** Real-time market making on continuous order book(s)
5. **Session end:** Abrupt when timer hits zero (player can also end early). All open positions auto-liquidated at last traded price
6. **Score reveal:** Letter grade animation (S/A/B/C/D/F)
7. **Post-session options:** Play Again (same config) / Change Config / View Debrief / Home

### 3.2 Trading Mechanics

**Order types (v1):** Limit orders only. Additional types (Market, IOC, FOK) added later.

**Order book:**
- Continuous limit order book with price-time priority (FIFO at each price level)
- Partial fills allowed (standard)
- Variable tick size per asset (liquid assets = tight ticks)
- Variable lot size per asset
- Variable price ranges ($10–$5,000 depending on asset type)

**Input methods (all three available, player's choice):**
- Type exact price in input field
- Click price level on the ladder
- Hotkey adjustments relative to current quote

**Keyboard shortcuts:** Fully customizable rebindable keys. Essential one-key actions:
- Tighten/widen spread by 1 tick
- Shift entire quote up/down by 1 tick
- Cancel all orders (panic button)
- Cycle between assets (for multi-asset)

**Position limits:** Soft limit with warning (visual + sound + screen shake when approaching ±50 units). No hard limit — risk management is the player's responsibility.

**Transaction fees:** Configurable per session — player can toggle fees on/off.

### 3.3 Pause & Save

- **Pause:** Allowed in practice mode only (freezes everything). No pause in career/multiplayer.
- **Save/resume:** Sessions can be saved and resumed later in solo modes only.
- **Disconnect:** Career mode = forfeit the session entirely. Practice = can reconnect.
- **Brief network glitch (1–5 sec):** Auto-reconnect with position preserved (30-second grace period).

---

## 4. Career Mode & Progression

### 4.1 Capital System

- **Starting capital:** $100,000
- **Buy-in model:** Each session, the player allocates a portion of their career capital as a buy-in. This is their maximum loss for the session. PnL is 1:1 — make $5K, capital goes up $5K.
- **Minimum buy-in:** Scales per tier (higher tiers require bigger stakes)
- **Capped downside:** You can only lose what you bought in with
- **No artificial caps** on loss — position sizing naturally limits exposure

### 4.2 Permadeath

- Capital hits $0 → **game over**
- Player can start fresh: $100,000, Tier 1 (Intern), no history
- This is a full reset — all progression lost

### 4.3 Tier System — 11 Tiers

| Tier | Title | Capital Threshold (Approx) |
|------|-------|---------------------------|
| 1 | Intern | $100K (start) |
| 2 | Analyst | $150K |
| 3 | Associate | $250K |
| 4 | Trader | $500K |
| 5 | Senior Trader | $1M |
| 6 | VP | $2M |
| 7 | Director | $4M |
| 8 | MD | $8M |
| 9 | Partner | $16M |
| 10 | Founder | $30M |
| 11 | Legend | $50M+ |

**Tier-up requirements:** Capital thresholds only (exponential curve).

**Demotion:** Yes, with grace period — 3 consecutive sessions below the threshold before demotion.

**Placement matches:** Optional. 3 quick matches. Max placement at Tier 3 (Associate). Standard career capital ($100K) at risk during placement.

### 4.4 Tier Unlocks

As players tier up, they unlock:
- **New assets** (15+ total, progressively unlocked)
- **Harder bot archetypes** (RL bots, evolutionary bots at higher tiers)
- **New price processes** (Heston, regime-switching at higher tiers)
- **Challenge modes** (individual modes unlock at specific tiers)
- **Procedurally generated assets** (at high tiers — genuinely novel, never-before-seen instruments)
- **Fake/misleading news events** (high tiers only — difficulty mechanic)
- **Multiplayer** (unlocks at a specific tier)

### 4.5 Difficulty Scaling

**What gets harder at higher tiers:**
- Increased informed trader ratio (more adverse selection)
- Faster bot reaction times
- More aggressive competing MMs (tighter spreads)
- More frequent news events
- Higher baseline volatility
- Fake/misleading news introduced

**Difficulty variation:** Random within a difficulty band per tier — no two sessions feel the same.

**Mid-session adaptation:** Yes — if you're crushing it, bots adapt in real-time (silently, no notification).

---

## 5. Practice Mode

- **Capital:** Fixed $100K every session (no career impact)
- **Bot difficulty:** Identical to career mode at the player's current tier
- **Limits:** Unlimited sessions, no caps
- **Pause:** Allowed (freezes everything)
- **Stats:** Not tracked separately — practice doesn't affect career stats
- **Blowup behavior:** Capital can go negative, settled at session end (gradual, not instant)

---

## 6. Assets & Market Simulation

### 6.1 Asset Universe

- **Total assets:** 15+ (curated base set + procedurally generated extras at high tiers)
- **Theming:** Real-world inspired ("Tech ETF", "Oil Futures", "Crypto")
- **Labels:** Themed tickers (NVT, MRD, CRX, etc.)
- **Unlocking:** Assets unlock as the player tiers up
- **Difficulty:** Individual assets have inherent difficulty levels (some are wider/jumpier)

### 6.2 Price Processes

Each asset has a consistent process type assigned (persists across sessions) — but the player is **never told** which process an asset uses. Must infer from price behavior.

| Process | Description | When Available |
|---------|-------------|----------------|
| News/event-driven | Fair value shifts on discrete information events | Tier 1+ |
| Regime-switching | Parameters change between hidden states (sudden jumps, no warning) | Mid-tier unlock |
| Heston (stochastic vol) | Volatility itself is stochastic | High-tier unlock |

**Parameter randomization:** Each asset has base parameters that vary within a range per session — familiar assets still feel different each time.

### 6.3 Volatility

- **Default:** Random per session (forces adaptation)
- **Within session:** Tied to news events + random regime switches (vol can shift even without news)
- **Bot flow:** Realistically correlated with vol (not perfectly — baseline noise always present)

### 6.4 Multi-Asset Mechanics

- **Asset selection:** Player chooses which assets to quote per session (specialize or diversify). No minimum — can trade 1 asset if desired.
- **Correlations:** Dynamic — shift over time, tied to regime-switching. No grouping labels shown. Player must infer from price action.
- **Cross-asset flow:** News for one asset moves correlated assets. Bots exploit cross-asset mispricings.
- **No correlation data shown** during session — player must discover structure from observation.
- **Correlation breakdown** revealed in debrief.

### 6.5 Index / Basket Instruments

- **Multiple indices:** One per sector/group + one broad index
- **Tradeable:** Yes — each index has its own independent order book
- **Available from Tier 1** (helps beginners hedge)
- **Arb opportunity:** Index can deviate from component prices — bots will exploit this

### 6.6 Tick Size, Price Range, Lot Size

All **vary per asset:**

| Property | Range |
|----------|-------|
| Tick size | $0.01 (liquid) to $0.25 (commodity-like) |
| Price range | $10 – $5,000 depending on asset type |
| Lot size | 1 – 100 units depending on asset type |

---

## 7. News & Information System

### 7.1 Event Types

- Earnings announcements ("NVT beats revenue estimates")
- Macro events ("Fed signals rate hold")
- Sector-specific ("Oil supply disruption in Gulf")
- Geopolitical ("Trade deal uncertainty rises")
- Company-specific ("CRX CEO steps down")

### 7.2 Generation Pipeline

- **Pre-generated:** Massive library of 1000+ events, generated once with Claude, stored as JSON files in the repo
- **Rare/complex events:** Claude generates during session setup (hybrid, not live — zero latency)
- **Model:** Haiku for speed

### 7.3 Delivery

- **Format:** Pop-up alerts that demand attention
- **Frequency:** Random Poisson arrivals (unpredictable)

### 7.4 Information Asymmetry

- **Private information:** Some news is private — only informed bots see it first. Player gets the headline later.
- **Ambiguity:** Mix of clear and ambiguous headlines. Easier at low tiers, harder at high tiers.
- **Fake news:** At higher tiers only — some headlines are misleading or have no actual impact.

### 7.5 Fair Value Impact

- **Depends on news type:** Earnings = instant price jump. Macro = gradual drift.
- **Scope depends on type:** Company news = single asset. Macro = all assets with varying magnitude.

---

## 8. AI Agent Architecture

### 8.1 Design Philosophy

**The core feature.** Layered architecture where each layer adds sophistication. All layers coexist in a single session. AI adaptation is **silent** — no notifications, no HUD, no visible stats. The player just notices things getting harder. Bots are anonymous (Agent-1, Agent-2, etc.).

### 8.2 Layer 1: Rule-Based Agents (v1.0)

Parameterized archetypes with tunable difficulty:

**Noise Trader** — Random hits/lifts, Poisson intensity, provides baseline flow.
**Informed Trader** — Knows fair value, picks off stale quotes. Aggressiveness and latency parameters.
**Momentum Scalper** — Detects trends, trades in direction of momentum.
**Adversarial Market Maker** — Quotes competing market, tightens when player widens.

Difficulty parameters scale from 1–10 per bot type, auto-adjusted based on player performance and tier.

### 8.3 Layer 2: Reinforcement Learning Agents (v1.5)

**Algorithm:** SAC (Soft Actor-Critic) — handles continuous state space, entropy bonus encourages diverse strategies.

**Observation space (maximum):**
- Full order book state
- Recent trade history
- Player's quoting history (last N quotes)
- Player's estimated inventory
- Player behavior model (learned tendencies)
- Time remaining + current PnL

**Action space:** Discrete for v1 (hit bid, lift ask, wait, specific price levels). Migrate to continuous if needed.

**Two model types:**
- **Global model** — Trained on all player data, provides baseline challenge from day one
- **Personal shadow model** — Trained specifically on YOUR play history, learns your weaknesses

**Training schedule:**
- Retrain every 5 sessions (stable learning)
- Adaptive threshold — only trains when enough new data has accumulated
- Runs locally on Will's machine (zero cost)
- Latest model only retained (no version history)

**Mixed objectives:** Some RL agents are adversarial (maximize PnL against you), some are cooperative (noise traders providing flow).

### 8.4 Layer 3: Evolutionary Agents (v2.0)

- **Population:** 100–200 agents (balanced diversity/compute)
- **Evolution:** Continuous in background (never stops)
- **Selection:** Niching — preserve diverse strategies even if suboptimal (prevents convergence to one super-bot)
- **Genome:** Encodes entry thresholds, spread preferences, inventory limits, momentum sensitivity
- **Fitness:** PnL against real players over recent sessions

### 8.5 Layer 4: LLM Agents (v2.5)

**Models:** Haiku for live agents (fastest), Sonnet for coaching/debrief.

**Applications:**
- Pre-generated news events (hybrid pipeline)
- Post-session AI coaching debrief (conversational, unlimited for BYO key)
- Reasoning trader agent (explicit strategy reasoning in context window)

### 8.6 Cross-Asset Bot Strategies

- Bots exploit cross-asset mispricings and correlations
- Some bot archetypes are dedicated cross-asset arbitrageurs
- Index arb bots keep index price in line with components

---

## 9. Multiplayer System

### 9.1 Core Design

- **Players:** 2–4 per session
- **Communication:** None — pure trading, read the tape
- **Spectating:** Post-session replay only (no live spectating)
- **Career capital:** At stake in multiplayer (real permadeath risk)

### 9.2 Matchmaking

- **Private rooms** with invite codes (direct friend challenges)
- **Ranked queue** with Glicko-2 rating
- **Direct challenges:** Yes — challenge a friend directly, no restrictions

### 9.3 Rating System

- **Algorithm:** Glicko-2 (accounts for rating uncertainty and volatility)
- **Starting rating:** Unrated — first 5 matches are placement games
- **Rating change:** Based on PnL ranking in session (1st/2nd/3rd/4th get different adjustments)

### 9.4 Session Rules

- **Assets:** Each player picks their own (asymmetric, strategic)
- **Buy-in:** Minimum set by highest-tier player in the room
- **Bots:** Configurable by host (full bots, fewer bots, or pure PvP)
- **Winner:** PnL determines capital change. Composite score determines Glicko-2 rating change.

### 9.5 Post-Multiplayer

- **Debrief:** Your own stats only (same as solo debrief). No opponent stats visible.
- **Replay:** Private — opponents cannot see your session replay.

---

## 10. Challenge Modes

All challenge modes are **the same continuous order book engine** with different parameter presets. No separate game modes to maintain.

| Mode | What Changes | Description |
|------|-------------|-------------|
| **Speed** | 3x tick rate + 1.5x bot speed | Ultra-fast quoting under pressure |
| **News Storm** | 5x news event frequency | Information overload |
| **Shark Tank** | Normal informed ratio but bots have near-perfect information | Every fill is likely adverse |
| **Thin Book** | 80% fewer bots providing liquidity | Wide natural spreads, gap risk |
| **Volatility Regime** | Sudden vol regime jumps with no warning | Detect and adapt or get crushed |
| **Nightmare** | News Storm + Shark Tank combined | The ultimate flex |

**Session length:** Host/player configures duration.

**Career capital:** Player chooses — practice stakes or career stakes per challenge.

**Combinability:** News Storm + Shark Tank can be stacked (Nightmare mode). Other combinations TBD.

**Multipliers:** No career capital multiplier for challenge modes — just bragging rights.

---

## 11. Analytics & Debrief

### 11.1 Post-Session Dashboard

**Layout:** Tabbed sections — Performance / Inventory / Trades / AI Coach

**Performance Tab (must-haves for v1):**
- PnL curve overlaid with revealed fair value
- Final PnL, Sharpe ratio, max drawdown, average spread
- Letter grade composite score
- Per-asset PnL breakdown

**Inventory Tab:**
- Inventory heatmap over time
- Time-weighted average inventory
- Inventory correlation with subsequent PnL

**Trades Tab:**
- Trade-by-trade classification (informed / noise / momentum)
- Spread efficiency vs. optimal spread comparison
- Behavioral pattern detection ("you widen after losses", "your time-to-adjust is X ms")
- Interactive: click any trade to see the full book state at that moment
- Counterparty identity shown on YOUR trades (which agent was on the other side)

**AI Coach Tab:** See §12.

**Visual style:** Identical to trading UI (consistent cream fintech brand).
**Charting:** Lightweight Charts (TradingView) for price data, D3.js for custom analytics.

### 11.2 Session-Over-Session Tracking

- Skill spider chart (spread, inventory, speed, adverse selection, etc.)
- PnL and Sharpe trend lines over time
- Win rate / session completion streaks
- On-demand only — player checks when they want
- Benchmarked against: your own history, anonymized percentile vs. tier, named comparison vs. friends

---

## 12. AI Coaching System

### 12.1 Debrief Coach

- **Model:** Claude Sonnet
- **Tone:** Encouraging but honest ("good session, but watch your inventory at 2:34")
- **Format:** Conversational — player can ask unlimited follow-up questions (BYO key) or 5 follow-ups (Pro subscribers)
- **Context:** Full session data — whatever fits in Claude's context window (per-second snapshots, trade log, news events, book states at key moments)
- **References specific moments:** "At 3:42, you widened after that 100-lot fill, but the seller was likely noise based on the price path"

### 12.2 BYO API Key Model

- **Entry:** Settings page — paste key, stored server-side (encrypted)
- **Providers:** Anthropic only for v1, expand later
- **Unlocks:** All AI features identical to Pro + usage dashboard showing API costs
- **During beta:** Will's own API key powers all AI features for all beta testers

---

## 13. Scoring, Streaks & Multipliers

### 13.1 Composite Score

Components ranked by importance:
1. **Raw PnL** (highest weight)
2. **Sharpe ratio** (risk-adjusted)
3. **Spread efficiency** (tighter = more points)
4. **Max drawdown penalty**
5. **Inventory management score** (lowest weight)

**Display:** Letter grades — S, A, B, C, D, F

### 13.2 Streak Bonuses

| Consecutive B+ Sessions | Multiplier |
|--------------------------|-----------|
| 3 | 1.1x |
| 5 | 1.25x |
| 10 | 1.5x |

**Win criteria:** Must achieve minimum composite score of B or higher (prevents sandbagging).

**Streak freeze:** One loss freezes the streak. Second consecutive loss resets to zero.

### 13.3 Multiplier Stacking

- Only streaks provide multipliers
- **No multiplier** for challenge modes (bragging rights only)
- **No multiplier** for bigger buy-ins (buy-in only determines risk)
- **Cap:** Total multiplier capped at 3x (prevents runaway compounding)

### 13.4 Score Bonuses

- Career-capital sessions: streak multiplier applies
- Challenge mode completions: bragging rights only
- Tutorial completion: small capital bonus

---

## 14. UI/UX Specification

### 14.1 Visual Style

- **Aesthetic:** Modern fintech with cream background — NOT typical dark-mode trading UI
- **Theme:** System-follows (match OS preference) — cream light mode + dark mode
- **Design approach:** Use `/mnt/skills/public/frontend-design/SKILL.md` for ALL UI. No AI slop. Distinctive typography, thoughtful spatial composition, refined color palette.
- **Profit/loss colors:** Red/green (standard trading colors)
- **Number formatting:** Comma-separated with 2 decimal places ($1,234.56) + K/M notation for large numbers ($1.2M career capital)

### 14.2 Layout

- **Drag-and-drop panels** (library: react-grid-layout or similar — Claude Code's recommendation)
- **Saveable layouts:** One saved layout per user
- **Presets:** Default layout + presets ("Beginner", "Pro", "Scalper", "Multi-Asset") + blank canvas
- **Minimum screen width:** Fluid — works at any width with panel rearrangement
- **Platform:** Desktop-only for v1 (no mobile)

### 14.3 Available Panels (11 total)

1. **Order book ladder** (vertical price levels, bid left / ask right)
2. **Depth chart** (horizontal area chart showing liquidity)
3. **Price chart** (toggleable: candlestick or line — Lightweight Charts / TradingView)
4. **Time & sales tape** (scrolling trade list — all trades, player's highlighted, counterparty shown on player's trades)
5. **PnL curve** (live, real-time — realized + unrealized shown separately)
6. **Inventory gauge** (visual meter)
7. **Risk dashboard** (per-asset PnL breakdown, portfolio-level Greeks, cross-asset risk metrics)
8. **Order entry panel**
9. **Asset selector / portfolio overview** (shows session count, win rate, avg score on hover per asset)
10. **News feed** (pop-up alerts)
11. **Alert log**

### 14.4 Always-Visible HUD Elements

- Floating PnL (realized + unrealized separately)
- Position/inventory gauge
- Spread indicator (current quoted spread)
- Session timer with progress bar
- Mini risk dashboard (delta, exposure across assets)

### 14.5 In-Session Alerts

**What triggers alerts:**
- Inventory approaching soft limit
- Session time running low (1 min warning)
- News event incoming

**Display:** Toast notifications in corner.

**Intensity:** Visual + sound + screen shake for critical alerts (inventory limit).

### 14.6 Order Book Visualization

- **Configurable per session** + **progressive** (beginners see full, advanced see less)
- Both ladder + depth chart available side by side as separate panels

### 14.7 Visual Feedback

- Screen flash / border color change on trade fills
- Score reveal with letter grade animation at session end
- Animated market visualization during loading states (price paths building)

### 14.8 Settings Panel

Accessed via gear icon (in-game). Configurable:
- Keybinding editor
- Sound volume controls (master + mute toggles per category)
- Default session length
- Default buy-in percentage
- Color theme (cream light / dark)
- Default assets to trade

No export/import — keep it simple.

---

## 15. Audio Design

### 15.1 Soundscape

- **Sound on by default** (player can mute)
- **No background music** — functional audio only
- **No ambient noise** — every sound means something

### 15.2 Sound Types

| Sound | Trigger |
|-------|---------|
| Buy fill | Player order filled on buy side |
| Sell fill | Player order filled on sell side |
| Large fill (distinct third sound) | Fill above configurable size threshold |
| Inventory warning | Approaching soft position limit |
| News alert | News event incoming |
| Time warning | 1 minute remaining |
| Session end | Timer expires |
| Countdown beeps | 3… 2… 1… GO |

### 15.3 Volume Controls

- Master volume
- Mute toggles per category (fills, alerts, system)

---

## 16. Onboarding & Tutorial

### 16.1 Flow

1. **Create account** (email + password)
2. **Adaptive quiz** (3–5 multiple choice questions, quick)
3. **Quiz sorts player into level:**
   - Beginner → full tutorial
   - Intermediate → abbreviated tutorial
   - Advanced → skip tutorial, go straight to placement matches
4. **Tutorial** (if needed): text-based walkthrough with diagrams + interactive mini-sessions. 5 minutes max.
5. **Tutorial completion reward:** Small capital bonus
6. **Placement matches** (optional): 3 matches, max placement at Tier 3
7. **Land on home dashboard**

### 16.2 Quiz Topics

- What is a bid/ask spread?
- How does an order book work?
- What is adverse selection?
- What is inventory risk?
- Basic probability (expected value, variance)

---

## 17. Social & Profile System

### 17.1 Friends

- **Add friends:** Username search only
- **Friends list info:** Online/offline + currently in session + current tier and capital
- **Direct challenges:** Yes — challenge a friend to multiplayer, no tier restrictions

### 17.2 Public Profile

- **Visible to anyone** (no privacy settings for v1)
- **Shows:** Current tier/title + career capital (exact or range)
- **Avatar:** Upload custom avatar

### 17.3 Account

- **Auth:** Email + password only (fastest to implement — JWT or session cookies, whatever ships fastest)
- **Delete account:** Yes — data removed, anonymized gameplay data retained for RL training
- **Career reset:** Allowed — fresh start at $100K, Tier 1, no history

---

## 18. Leaderboards

### 18.1 Boards

- **All-time career capital** leaderboard
- **Current Glicko-2 rating** leaderboard

### 18.2 Filters

- Global
- Friends only
- Tier-specific

### 18.3 Display

- Top 50 with search for any player
- Your own rank always visible

---

## 19. Tournament System

- **Format:** Round-robin (everyone plays everyone)
- **Size:** 8–16 players
- **Creator:** Player-created (Student Quant Fund hosts their own)
- **Rewards:** Bragging rights + leaderboard placement only
- **Capital:** Career capital at stake (same as normal multiplayer)

---

## 20. Monetization

### 20.1 Model: Freemium

**Free tier (genuinely unlimited):**
- Unlimited sessions (solo + career)
- All game modes, all assets (as unlocked)
- Full analytics and debrief (non-AI)
- Multiplayer access
- All difficulty levels and challenge modes
- Keyboard customization, layouts, everything

**Pro tier ($5–10/mo) — only paywalls AI features that cost API money:**
- Claude AI coaching debrief (conversational, 5 follow-ups)
- Claude-generated news events (live rare/complex events)
- LLM reasoning trader agent
- Session replay with playback controls
- CSV/JSON export of trade history

**BYO API Key (free alternative to Pro):**
- Paste Anthropic API key in settings (stored server-side, encrypted)
- Unlocks ALL Pro AI features
- Unlimited follow-up questions with AI coach
- Usage dashboard showing API costs
- Anthropic only for v1

### 20.2 Beta Period

- Will's own API key powers all AI features for all beta testers (5–10 people)
- $0 infrastructure budget beyond Claude Max subscription
- No landing page, no marketing

---

## 21. Technical Architecture

### 21.1 Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | React 18 + TypeScript (strict) + Vite |
| **State management** | Zustand |
| **WebSocket client** | Native WebSocket API with reconnection |
| **Price chart** | Lightweight Charts (TradingView open-source) |
| **Analytics charts** | D3.js |
| **Drag-and-drop** | react-grid-layout (or Claude Code recommendation) |
| **Styling** | Tailwind CSS + frontend-design skill |
| **Backend** | Python 3.12 + FastAPI |
| **ORM** | Tortoise ORM (async-native) |
| **Database** | PostgreSQL (free tier — Neon or Supabase) |
| **Migrations** | Raw SQL migration files |
| **Cache / pub-sub** | Redis (self-hosted on Railway for multiplayer, in-memory for solo) |
| **WebSocket server** | FastAPI WebSocket endpoints |
| **Matching engine** | Custom Python (asyncio event loop) |
| **Price simulation** | NumPy/SciPy |
| **RL training** | Stable Baselines 3 (SAC) — runs locally |
| **LLM integration** | Anthropic Python SDK |
| **Auth** | Email + password (fastest implementation — JWT or sessions) |
| **Frontend deploy** | Vercel (free tier) |
| **Backend deploy** | Railway (free tier / $5 credit) |

### 21.2 API Architecture

- **REST** for auth, config, analytics, session history, leaderboards, profiles
- **WebSocket** for live game state (order book, trades, PnL, alerts, news)
- **Single WebSocket connection** with multiple channels via message type routing (book, trades, PnL, alerts)
- **No API documentation** for now — typed interfaces are the documentation

### 21.3 WebSocket Protocol

**Message format:** JSON (simplest to build and debug)

**Client → Server:**
```json
{"type": "order", "side": "bid", "price": 100.50, "size": 10, "order_type": "limit"}
{"type": "cancel", "order_id": "abc123"}
{"type": "modify", "order_id": "abc123", "new_price": 100.51}
```

**Server → Client (channels):**
```json
{"channel": "book", "bids": [[100.50, 10], ...], "asks": [[100.52, 15], ...], "timestamp": 1711036800000}
{"channel": "trade", "price": 100.51, "size": 5, "aggressor": "buy", "is_yours": true, "counterparty": "Agent-3"}
{"channel": "pnl", "realized": 1250.00, "unrealized": -340.50, "inventory": 15}
{"channel": "alert", "type": "inventory_warning", "message": "Position approaching limit"}
{"channel": "news", "headline": "NVT beats revenue estimates", "type": "earnings", "affected_assets": ["NVT"]}
{"channel": "fill", "side": "bid", "price": 100.50, "size": 5}
```

### 21.4 Matching Engine

- **Priority:** Price-time (FIFO) — industry standard
- **Tick rate:** 50ms internal (20 updates/sec)
- **Client update rate:** <100ms latency target
- **Partial fills:** Allowed (standard)
- **Bot-to-bot trading:** Yes — bots can trade with each other, creating realistic tape
- **Async event loop:** Single-threaded asyncio — no race conditions

### 21.5 Security (v1 — ship fast)

- **Auth:** Whatever's fastest (JWT or sessions)
- **Anti-cheat:** Trust the client for v1, add server validation later
- **Data privacy:** Don't worry about it for private beta, add later
- **API keys:** Stored server-side, encrypted

---

## 22. Multi-Agent Claude Code Development

### 22.1 Architecture for Parallel Development

The codebase is designed for **3–5+ Claude Code instances** working simultaneously in different parts of the repo, communicating via well-defined interfaces and merging via PRs.

### 22.2 Module Ownership

| Module | Directory | Claude Code Instance |
|--------|-----------|---------------------|
| Matching engine / order book | `server/engine/` | Instance 1 |
| AI agents (rule-based + RL + evo) | `server/agents/` | Instance 2 |
| Frontend (React UI, panels, charts) | `client/` | Instance 3 |
| WebSocket server + REST API layer | `server/api/` | Instance 4 |
| Analytics engine + debrief system | `server/analytics/` | Instance 5 |
| Database models + migrations | `server/db/` | Instance 6 (or shared) |

### 22.3 Contract Communication

All three layers required:
1. **Shared markdown specs** in `/docs/` that all instances read
2. **JSON schema contracts** at module boundaries
3. **TypeScript/Python typed interfaces** defining the API between modules

### 22.4 Git Workflow

- **Branch per instance** (e.g., `engine/feature-x`, `frontend/panel-layout`)
- **Merge via PRs** — Will reviews and merges (human checkpoint)
- All instances can read `/docs/` and contract files on main

### 22.5 Repo Structure

```
marketmind/
├── README.md                  # Architecture overview
├── docs/
│   ├── ARCHITECTURE.md        # System design
│   ├── CONTRACTS.md           # Module interface specs
│   ├── schemas/               # JSON schemas for module boundaries
│   └── api/                   # REST + WebSocket message specs
├── client/
│   ├── README.md              # Frontend module docs
│   ├── package.json
│   ├── vite.config.ts
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── panels/            # Drag-and-drop panel components
│   │   ├── hooks/             # Custom hooks (WebSocket, game state)
│   │   ├── stores/            # Zustand stores
│   │   ├── types/             # TypeScript interfaces
│   │   └── utils/             # Helpers
│   └── public/
│       └── sounds/            # Audio files
├── server/
│   ├── README.md              # Backend module docs
│   ├── requirements.txt
│   ├── engine/
│   │   ├── README.md          # Matching engine docs
│   │   ├── orderbook.py
│   │   ├── matching.py
│   │   ├── price_sim.py       # Stochastic processes
│   │   └── session.py
│   ├── agents/
│   │   ├── README.md          # AI agent docs
│   │   ├── rule_based.py
│   │   ├── rl_agent.py
│   │   ├── evolutionary.py
│   │   └── llm_agent.py
│   ├── api/
│   │   ├── README.md          # API layer docs
│   │   ├── main.py            # FastAPI app
│   │   ├── websocket.py       # WebSocket handlers
│   │   ├── routes/            # REST endpoints
│   │   └── auth.py
│   ├── analytics/
│   │   ├── README.md          # Analytics docs
│   │   ├── debrief.py
│   │   ├── scoring.py
│   │   └── behavioral.py
│   ├── db/
│   │   ├── README.md
│   │   ├── models.py          # Tortoise ORM models
│   │   └── migrations/        # Raw SQL migration files
│   └── data/
│       └── news_events.json   # Pre-generated 1000+ news events
└── .github/
    └── workflows/             # CI if needed later
```

---

## 23. Infrastructure & Deployment

### 23.1 Hosting

| Service | Provider | Tier |
|---------|----------|------|
| Frontend | Vercel | Free |
| Backend (FastAPI + WebSocket) | Railway | Free ($5/mo credit) |
| PostgreSQL | Neon or Supabase | Free tier |
| Redis | Self-hosted on Railway | Included in Railway |

### 23.2 Budget

- **Monthly cost:** $0 beyond Claude Max subscription
- **RL training:** Local on Will's machine (free)
- **LLM API:** Will's API key during beta

### 23.3 Performance Targets

| Metric | Target |
|--------|--------|
| Order book update latency | <100ms |
| Matching engine tick rate | 50ms (20/sec) |
| WebSocket message format | JSON |
| Concurrent sessions (beta) | 5–10 |

---

## 24. Data Model

### 24.1 Core Entities

**User:** id, username, email, password_hash, avatar_url, career_capital, tier, glicko_rating, glicko_rd, glicko_vol, streak_count, created_at, settings_json, api_key_encrypted

**Session:** id, user_id, mode (career/practice/challenge/multiplayer), duration_seconds, session_length_type, buy_in_amount, price_process_types, assets_selected, difficulty_band, start_time, end_time, status (active/completed/forfeited/voided)

**Order:** id, session_id, user_or_agent_id, asset_ticker, side, price, size, order_type, status (active/filled/partial/cancelled), fill_price, fill_size, timestamp

**Trade:** id, session_id, asset_ticker, buy_order_id, sell_order_id, price, size, timestamp, aggressor_side, fair_value_at_trade, counterparty_type (informed/noise/momentum/player)

**SessionAnalytics:** session_id, final_pnl, sharpe, max_drawdown, avg_spread, adverse_selection_ratio, composite_score, letter_grade, snapshot_data_json (per-second aggregated snapshots), behavioral_patterns_json

**AgentModel:** id, user_id (null for global), agent_type, model_blob, training_session_count, last_trained_at

**Friendship:** id, user_id, friend_user_id, created_at

**Tournament:** id, creator_user_id, name, format (round_robin), max_players, status, created_at

### 24.2 Data Retention

- **Per-second session snapshots:** Keep 30 days, archive to cold storage after
- **Session summaries:** Keep forever
- **Session replay data:** Pro users only (stored as aggregated snapshots)

---

## 25. Error Handling & Edge Cases

### 25.1 Network Issues

| Scenario | Career Mode | Practice Mode |
|----------|------------|---------------|
| Brief glitch (1–5 sec) | Auto-reconnect, 30-sec grace, position preserved | Auto-reconnect, position preserved |
| Extended disconnect | Forfeit session | Can reconnect later |
| Server crash | Session voided (no capital change) | Ignored |

### 25.2 Loading States

Animated market visualization (price paths building, order book constructing) during all loading screens.

### 25.3 Session End Edge Cases

- **Blowup mid-session (career):** Capital hits $0 → session ends immediately, game over
- **Blowup mid-session (practice):** Capital can go negative, settled at session end
- **Early exit:** Player can end session early — positions mark-to-market at last traded price
- **Disconnect in multiplayer:** Forfeit — all other players continue

---

## 26. Phased Roadmap

### Phase 1: Foundation (Weeks 1–4) — "Playable v0.5"

**Goal:** Working solo career mode with rule-based bots on a single asset.

- [ ] FastAPI backend with WebSocket support
- [ ] Matching engine (price-time priority, partial fills)
- [ ] News-driven price process (simplest of the three chosen)
- [ ] Rule-based noise trader + informed trader bots
- [ ] React frontend with Vite + TypeScript: order book ladder, price chart, order entry, PnL display
- [ ] Career mode: buy-in system, capital persistence, tier progression
- [ ] Practice mode: fixed capital, same bots
- [ ] Basic composite scoring + letter grade
- [ ] Keyboard shortcuts (rebindable)
- [ ] Cream fintech UI using frontend-design skill
- [ ] Pre-generated news events (JSON library)
- [ ] Auth (email + password, basic JWT)

**Deliverable:** Play a 5-minute career session, buy in with your capital, trade one asset against bots, get a letter grade.

### Phase 2: Multi-Asset + Polish (Weeks 5–7) — "Full Trading Desk v1.0"

- [ ] 5+ assets with variable tick/lot/price
- [ ] Cross-asset correlations (dynamic, regime-switching)
- [ ] Tradeable index instruments
- [ ] All 11 draggable panels
- [ ] Depth chart, time & sales tape, risk dashboard
- [ ] Full debrief system (all 4 tabs — Performance, Inventory, Trades, placeholder for AI Coach)
- [ ] Interactive trade drill-down in debrief
- [ ] All session lengths (2/5/15/Endless)
- [ ] Streaks + multiplier system
- [ ] Sound design (fill sounds, alerts, screen shake)
- [ ] Placement matches
- [ ] Onboarding quiz + tutorial

### Phase 3: AI Intelligence (Weeks 8–11) — "Adaptive v1.5"

- [ ] RL agent training pipeline (SAC via Stable Baselines 3)
- [ ] Global model + personal shadow model
- [ ] Silent mid-session difficulty adaptation
- [ ] Regime-switching + Heston price processes
- [ ] Adversarial MM bot + momentum scalper bot
- [ ] Difficulty auto-scaling per tier
- [ ] Claude AI coaching debrief (Sonnet, conversational)
- [ ] BYO API key system
- [ ] Session-over-session tracking (spider chart, trends)
- [ ] Behavioral pattern detection

### Phase 4: Multiplayer (Weeks 12–15) — "Competitive v2.0"

- [ ] Real-time multiplayer (2–4 players)
- [ ] Multiplayer game rooms (create/join with codes)
- [ ] Ranked queue with Glicko-2
- [ ] Direct friend challenges
- [ ] Friends list + profiles
- [ ] Leaderboards (capital + rating, global + friends + tier)
- [ ] Player-created tournaments (round-robin, 8–16 players)
- [ ] Post-multiplayer debrief (private, own stats only)

### Phase 5: Deep AI + Challenges (Weeks 16–20) — "Evolution v2.5"

- [ ] Evolutionary agent population (100–200, continuous evolution, niching)
- [ ] Challenge modes (Speed, News Storm, Shark Tank, Thin Book, Vol Regime, Nightmare)
- [ ] Procedurally generated assets at high tiers
- [ ] Fake/misleading news at high tiers
- [ ] LLM reasoning trader agent
- [ ] Cross-asset arb bots
- [ ] Session replay (Pro feature)
- [ ] CSV/JSON export
- [ ] Stress testing (100+ concurrent sessions)

### Phase 6: Polish & Beta Launch (Weeks 21–24)

- [ ] Private beta with 5–10 friends
- [ ] Bug fixing, balance tuning
- [ ] Performance optimization (<100ms book updates)
- [ ] Dark mode (system-follows)
- [ ] Layout presets
- [ ] Asset hover stats in selector
- [ ] Endless mode difficulty ramp + duration multiplier
- [ ] Paid preview book feature (capital cost)

---

## 27. Open Questions & Future Features

### Deferred to Post-v1

- Achievements / cosmetics system (parked for later)
- Probability market mode (SIG-style, maybe later)
- Options / derivatives trading
- Mobile support
- Landing page / marketing site
- Community features (Discord, forums)
- PWA / native app
- Accessibility (colorblind modes, screen reader)
- GDPR compliance
- Advanced order types (Market, IOC, FOK)
- OpenAI / other API provider support for BYO key
- Settings export/import
- Async multiplayer (replay-based)
- Additional price processes (GBM, OU)

### Open Design Questions

1. Exact capital thresholds per tier — fine-tune after playtesting
2. Tier unlock mapping (which assets/modes unlock at which tier) — balance after beta feedback
3. Optimal RL observation space dimensionality — may need to reduce for training stability
4. News event library size — 1000 may need expansion after players see repeats
5. Endless mode difficulty ramp curve — exponential? logarithmic? needs testing
6. Cross-asset correlation strength ranges — too high feels forced, too low feels random
7. Tutorial capital bonus amount — enough to matter but not enough to skip early progression

---

*This document represents 290+ design decisions across 99 interview batches. It is the single source of truth for MarketMind development. Every Claude Code instance should read this before writing a single line of code.*
