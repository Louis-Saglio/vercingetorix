# Turn 034 — Wood radius 320 m

Goal served: G4b (defeat sandbox Rome).

## Hypothesis

> If the wood/food scan radius widens from 160 m to 320 m (on the restored
> turn-032 assault configuration with the turn-033 repair re-post fix), then
> the bot wins on ≥ 8/10 seeds before the 30-minute limit, because turn 033
> isolated the late-game killer: the 160 m radius empties by minute 24–26 on
> some batches, the wood income collapses and the rams starve. A 320 m radius
> keeps the gatherers supplied for the whole match; the cost is one longer
> walk per tree ring, paid once per depletion.

Primary metric: fraction of seeds won before the 30-minute limit, 0 JS
errors.

Verdict thresholds (pre-registered): good if ≥ 8/10 wins, 0 JS errors, canary
PASS; bad if ≤ 2/10 or error/determinism veto; neutral otherwise. Secondary
(reported, not the verdict): attack minute, win minute, composite. In-turn
fix-and-rerun iterations allowed.

## Implementation

In `bot/simulation/ai/vercingetorix/vercingetorix.js`:

- `maxDistSq` 160² → 320² (the wood/food caches are auto-maintained; the
  per-play-tick distance filter over a few thousand trees stays within the
  performance budget).
- Restores the turn-032 assault configuration (ram gate at 32, 2:1 soldier
  split, post-town workers 1 stone / 2 metal / 1 food, attack at two rams)
  and the turn-033 repair re-post fix (skip re-posts while someone is
  REPAIRING) — both documented known-good machinery from those turns.

## Experiment

Settings: seeds 301–310 (the turn-033 batch — the depletion batch),
sandbox Rome (`--difficulty2 0`), `random/mainland` 128,
`conquest_civic_centers`, treasures disabled, 30 game-minute limit,
biome/placement pinned. Baseline = the stored turn-033 baseline (last
validated code on these seeds — reused); treatment = 320 m radius; canary =
stored turn-033 canary.

## Results

**Iteration 1 (320 m radius):** 0/10 — the radius fix delivers (wood 1325–
2035 at t26–28), but the rams still miss the window: on this batch the
**forges are the long pole** (single builder, 120 s each, placed slowly on
the crowded ring) — the third forge completes at t25–26, so the city posts
t25–26, the arsenal lands t27–28 and finishes after t30.

**Iteration 2 (in-turn fix):** three builders per forge/arsenal foundation
(the turn-033 multi-builder, now combined with the re-post fix and the
320 m radius). Rerun below.

**Iteration 2 result:** still 1/10 — city lands earlier (t17–23 on several
seeds, the multi-builder works) and seed 306 shows wood 1325+, arsenal
built, metal 2710, melee 50 — every precondition met — yet the rams still
do not train on this batch. The batch-level difference between 291–300
(5/10 wins, rams train) and 301–310 (1/10, rams 0–2) remains unexplained
by the economy levers. Stop-the-turn: two iterations, no movement, cause
not understood.

## Verdict

**Bad** (pre-registered: 1/10 ≤ 2/10). Reverted.

## Action

Revert the change (`git restore bot/`) and commit as `turn 034:
wood-radius — bad`. No `CHANGELOG.md` entry. The knowledge goes to
`turns/backlog.md`.

## Next

Turn 035: a direct A/B diagnosis — run the winning seed 293 and the
failing seed 306 with full per-minute dumps and the sim-side train-command
logging (Commands.js override), and diff where the ram chain diverges.
See `turns/backlog.md`.
