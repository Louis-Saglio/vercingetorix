# Turn 013 — Grow the army to 40 with 6 houses

Goal served: G3 (defeat sandbox Rome, via a larger capture force).

## Hypothesis

> If I raise the soldier target from 32 to 40 and the house target from 4 to 6
> (with 12 offset candidates so the extra houses can actually be placed), then
> the bot reaches 40 melee soldiers by game-minute 16, because the larger target
> and extra housing let the army keep growing beyond the previous 32-soldier
> ceiling.

Primary metric: fraction of seeds that reach ≥ 40 melee soldiers by game-minute
16 (0 JS errors).

Verdict thresholds (pre-registered): good if ≥ 8/10 seeds, 0 JS errors, canary
PASS; bad if ≤ 2/10 or error/determinism veto; neutral otherwise.

## Implementation

In `bot/simulation/ai/vercingetorix/vercingetorix.js`:

- `SOLDIER_TARGET` 32 → 40 (and `ATTACK_THRESHOLD` follows it).
- `HOUSE_TARGET` 4 → 6.
- `HOUSE_OFFSETS` 8 → 12 candidates (adds four at ~24 tiles) so six houses can
  actually be placed.

## Experiment

Settings: seeds 121–130 (fresh), sandbox Rome (`--difficulty2 0`),
`random/mainland` 128, `conquest_civic_centers`, treasures disabled, 20
game-minute limit, biome/placement pinned. Baseline = HEAD (turn-011 code);
treatment = grow-to-40; canary = seed 121.

Results:

- Canary: **PASS**.
- Primary metric: reached ≥40 melee by minute 16 on **3/10** seeds (baseline
  0/10).
- 0 JS errors.
- Composite: +0.59 (neutral).

## Verdict

**Neutral** (3/10). The change reaches 40 soldiers only intermittently — the
six-house placement still fails on most seeds, so the larger target is not
reliable. The result is deterministic and far below the ≥8/10 good bar, so I
reverted rather than spending a doubled-N repeat on a foregone conclusion.

## Action

Revert the change (`git restore bot/simulation/ai/vercingetorix/vercingetorix.js`)
and commit as `turn 013: grow-to-40 — neutral`. No `CHANGELOG.md` entry.

## Next

G3 has now resisted five turns (005, 009, 010, 012, 013). Reconsider G3: the
citizen-soldier/siege paths both need capabilities the current bot does not
have. See `turns/backlog.md`.
