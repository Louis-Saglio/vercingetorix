# Turn 010 — Research Town Phase

Goal served: G3 (defeat sandbox Rome, via the siege path).

## Hypothesis

> If I make the bot research Town Phase (`phase_town_generic`) once it has the
> 500 food / 500 wood, then the bot reaches Town Phase in the experiment,
> because the change adds the first prerequisite of the siege path (Town →
> City → arsenal → ram) that the baseline never touches.

Primary metric: fraction of seeds where the bot reaches Town Phase by the
20-minute limit (0 JS errors).

Verdict thresholds (pre-registered): good if ≥ 8/10 seeds reach Town Phase with
0 JS errors and canary PASS; bad if ≤ 2/10 or error/determinism veto; neutral
otherwise.

## Implementation

In `bot/simulation/ai/vercingetorix/vercingetorix.js`:

- Added a serialized `townResearched` flag.
- Added `manageResearch(gameState, cc)`: once per game, if the CC can still
  research a `phase_town*` tech and the bot has ≥ 500 food and ≥ 500 wood,
  issue `cc.research(townTech)`.
- Called `manageResearch` from `play()` before house/soldier management.
- Added `"town"` to the per-minute `[HARNESS]` sample (evidence collection).

## Experiment

Settings: seeds 91–100 (fresh), sandbox Rome (`--difficulty2 0`),
`random/mainland` 128, `conquest_civic_centers`, treasures disabled, 20
game-minute limit, biome/placement pinned. Baseline = HEAD (turn-008 code);
treatment = Town research; canary = seed 91.

Results:

- Canary: **PASS**.
- Town reached: baseline **0/10**, treatment **1/10** (only seed 91).
- 0 JS errors in all matches.
- Composite: 0.00 (neutral) — irrelevant to the primary metric.

## Verdict

**Bad.** 1/10 ≤ 2/10. The bot almost never has 500 spare food AND 500 spare wood
because it spends wood on soldiers/houses every tick, so the research trigger
rarely fires. The siege path's first step needs a resource-saving strategy, not
just a "research when spare" check.

## Action

Revert the change (`git restore bot/simulation/ai/vercingetorix/vercingetorix.js`)
and commit as `turn 010: research-town-phase — bad`. No `CHANGELOG.md` entry.

## Next

The siege path needs the bot to save resources for phase research instead of
spending everything on soldiers. Reconsider the economy priority (or pick a
different path) before continuing. See `turns/backlog.md`.
