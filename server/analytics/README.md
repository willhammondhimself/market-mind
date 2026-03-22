# Analytics Engine (`server/analytics/`)

**Owner:** Claude Code Instance 5

Post-session analysis, scoring, debrief generation, and behavioral pattern detection.

## Files

- `scoring.py` — Composite score calculation, letter grade assignment, streak tracking
- `debrief.py` — Full debrief data generation (PnL curves, inventory heatmaps, trade classification)
- `behavioral.py` — Cross-session behavioral pattern detection

## Scoring Components (by weight)

1. **Raw PnL** (highest weight)
2. **Sharpe ratio** (risk-adjusted return)
3. **Spread efficiency** (tighter = more points)
4. **Max drawdown penalty**
5. **Inventory management score** (lowest weight)

Letter grades: S > A > B > C > D > F

## Interfaces

**Consumes:** `RawSessionData` from matching engine at session end
**Provides:** `DebriefData` to API layer for client

See `docs/CONTRACTS.md` §5 for full interface spec.
