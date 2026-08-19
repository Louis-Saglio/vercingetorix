# Turn 019 — Real Town Phase

Goal served: G4 (defeat sandbox Rome — the siege path starts with a *real*
Town Phase; turn 018 proved the sim has never accepted the research).

## Hypothesis

> If the bot commands all CitizenSoldier-class starting units (the two
> spearmen plus the two javelineers and the cavalry javelineer that have sat
> idle since turn 002), builds 5 houses (each carries the sim's Village
> class), and posts Town only when the sim's own `canResearch` says the
> requirements are met, then `gameState.currentPhase()` reaches 2 before
> game-minute 16 on ≥ 8/10 seeds, because turn 018 showed the real blockers:
> the pre-town economy had only two hands (875 wood + 500 food needed for 5
> houses + the research) and the Village class count never reached the
> required 5 (it tracks houses exactly).

Primary metric: fraction of seeds where `gameState.currentPhase() >= 2`
(sim ground truth, reported in the per-minute sample) before the 20-minute
limit, 0 JS errors.

Verdict thresholds (pre-registered): good if ≥ 8/10 seeds reach Town, 0 JS
errors, canary PASS; bad if ≤ 2/10 or error/determinism veto; neutral
otherwise. Secondary (reported, not the verdict): town minute, stone/metal
stock at minute 16 (G3 regression check).

## Implementation

In `bot/simulation/ai/vercingetorix/vercingetorix.js`:

- The gather loop now commands `byClass("CitizenSoldier")` instead of
  `byClass("Melee")` — the two starting javelineers and the cavalry javelineer
  join the pre-town wood/food economy (they gather like any citizen soldier).
  The attack sweep still uses the Melee collection, unchanged.
- `HOUSE_TARGET` 4 → 5, and `manageHouses` drops the pop-cap condition: houses
  are built whenever wood allows, from minute 0, because the sim counts them
  as the Village structures Town requires.
- `manageResearch` posts Town only when `gameState.canResearch(townTech)` is
  true (the sim's requirement check: 5 Village structures) in addition to the
  500 food / 500 wood gate.
- The `[HARNESS]` sample now reports `phase` (`currentPhase()`),
  `villageClass`, and `townCan` — the sim-truth evidence turn 018 taught us to
  collect.

## Experiment

Settings: seeds 171–180 (fresh), sandbox Rome (`--difficulty2 0`),
`random/mainland` 128, `conquest_civic_centers`, treasures disabled, 20
game-minute limit, biome/placement pinned. Baseline = HEAD (turn-018 commit);
treatment = real-Town plan; canary = seed 171.

## Results

**First run — INVALID.** Canary PASS, but the treatment stalled on every seed:
`houses=1, found=1` from minute 2 to 16, `villageClass=0`, `townCan=False`,
melee stuck at 2 (training gated), composite −16.06. Root cause: an
implementation bug, not the idea — the foundation-repair loop picked "any
idle unit", which was the cavalry javelineer (no Builder mixin, so the repair
order silently does nothing), so the second house foundation never completed
and the whole chain (5 Village houses → Town research → training) blocked.
The new pop-cap-free house timing exposed this for the first time.

**Fix:** the repair branch now picks the first unit that can actually build
the house template (`buildableEntities` contains it), busy or not. The
baseline and canary batches are unaffected and stay valid; the treatment is
rerun on the same seeds.

**Rerun results:**

- Canary: **PASS** (unchanged — the canary checks the harness, not the bot fix).
- Primary metric: **9/10** seeds reach real Town (`currentPhase() >= 2`), at
  game-minute 7–8, with `villageClass=5` at post time — the sim's requirement
  satisfied for real. 0 JS errors everywhere.
- Seed 173 fails differently: houses stall at 3 with no foundation — all 8
  house offsets are invalid on that seed, so the 5th and 4th houses never
  place. A placement-density issue for the 5-house target, not the phase
  gate.
- Composite: **−5.18** (reported, not verdict-relevant per pre-registration):
  the treatment spends wood/food on houses + research and starts training ~2
  minutes later (melee 17–30 at t16 vs 32 baseline). Stone/metal at t16:
  ≥ 750/750 on all 10 seeds — G3 not regressed.

## Verdict

**Good** (pre-registered: ≥ 8/10 real Town, 0 JS errors, canary PASS): 9/10.
The first run was invalid (implementation bug: the foundation-repair loop
could pick the non-building cavalry javelineer and stall forever); the fix —
repair by the first unit that can actually build the house — is part of this
turn's change and is kept.

## Action

Keep the change. Commit as `turn 019: real-town — good` and push.
`docs/CHANGELOG.md` gets an entry; `docs/GAME.md` gains the verified phase
requirements (5 Village structures for Town — houses count; 3 Town structures
for City — forge/market/tavern count; the sim silently rejects unmet phase
research).

## Next

City Phase: the bot now banks 750/750 by minute 16 with real Town under it.
City additionally needs 3 Town-class structures — forge, market or tavern
(costs and buildability to verify). Also: the 5-house placement fails on ~1/10
seeds (offset list exhaustion) — more/better house offsets are a candidate
improvement. See `turns/backlog.md`.
