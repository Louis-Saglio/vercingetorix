# Turn 033 — Parallel builders on the critical path

Goal served: G4b (defeat sandbox Rome).

## Hypothesis

> If the turn-032 iteration-2 configuration is restored (5/10 wins, composite
> +11.81) and the forge/arsenal foundations get up to three builders instead
> of one, then the bot wins on ≥ 8/10 seeds before the 30-minute limit,
> because the critical path is builder-bound: three forges × 120 s and the
> arsenal × 180 s are built sequentially by one builder each (~8 minutes);
> three builders each cut that to ~2.5 minutes, the rams leave ~4 minutes
> earlier, and the draw seeds that killed at ~t30.5 (turn 032) win
> comfortably.

Primary metric: fraction of seeds won before the 30-minute limit, 0 JS
errors.

Verdict thresholds (pre-registered): good if ≥ 8/10 wins, 0 JS errors, canary
PASS; bad if ≤ 2/10 or error/determinism veto; neutral otherwise. Secondary
(reported, not the verdict): attack minute, win minute, composite. In-turn
fix-and-rerun iterations allowed.

## Implementation

In `bot/simulation/ai/vercingetorix/vercingetorix.js`:

- Restores the turn-032 iteration-2 configuration (ram gate at 32, 2:1
  soldier split, post-town workers 1 stone / 2 metal / 1 food, attack at
  two rams).
- The foundation-repair branches of `manageForges` and `manageArsenal` send
  up to **three** capable builders to the pending foundation (was one).

## Experiment

Settings: seeds 301–310 (fresh), sandbox Rome (`--difficulty2 0`),
`random/mainland` 128, `conquest_civic_centers`, treasures disabled, 30
game-minute limit, biome/placement pinned. Baseline = last validated code
(HEAD, turn-029 state) run once on these seeds; treatment = parallel
builders; canary = seed 301.

## Results

**Iteration 1 (parallel builders):** regression — 1/10 wins. The rams never
train on 8/10: the arsenal cannot be placed — with 12 buildings around the
CC, the 72/88 m rings have no candidate left with 28 m clearance on this
seed batch (wood stockpiles to 2000+ with no placement possible). The
multi-builder change itself works (forges at t16 vs t18–20).

**Iteration 2 (in-turn fix):** the arsenal gets a wider ring — a third ring
of 16 candidates at 104 m (City territory covers it). Rerun below.

**Iteration 2 result:** still 1/10 — and an A/B diagnostic on the exact
turn-032-iteration-2 code (no turn-033 changes) reproduces the failure on
this batch: **0/10, no rams**. The root cause: the arsenal **foundation**
never completes on seeds 301–310 — the repair branch re-posts the repair
order every play tick, and each re-post resets the builder's approach, so a
far-away builder never arrives (REPAIR.REPAIRING 1 for 4+ minutes, found=1
forever). On the 291–300 batch the arsenal landed closer and escaped the
stall.

**Iteration 3 (in-turn fix):** the repair branches stop re-posting while any
own unit is already in a REPAIR state — the current builder finishes the
foundation undisturbed. Rerun below.

**Iteration 3 result:** the stall is fixed (one builder now repairs
continuously), but the chain is too late: the arsenal lands at minute 26–29
on this batch — the single-builder forges (3 × 120 s) and arsenal (180 s)
are the long pole.

**Iteration 4 (in-turn fix):** combine the re-post fix with **three
builders** per siege foundation (forges and arsenal) — the critical path
shrinks ~3x. Rerun below.

**Iteration 4 result:** still 1/10 — the arsenal now completes (the stall
is fixed) but the rams still starve: seed 306 shows wood 120–250 from
minute 26 with a 51-soldier army that no longer trains — the wood income
has collapsed. The cause is structural: the wood scan radius is capped at
160 m, and by minute 24–26 on this seed batch the local trees are chopped
out — the wood list empties, the gatherers idle, and the ram's 300 wood
never pools. The 291–300 batch (5/10 wins) had denser local forests.
Stop-the-turn per the rule: four iterations, not converging; the fix is a
new hypothesis (wood radius), not a small patch.

## Verdict

**Bad** (pre-registered: 1/10 ≤ 2/10). Reverted.

## Action

Revert the change (`git restore bot/`) and commit as `turn 033:
parallel-builders — bad`. No `CHANGELOG.md` entry. The negative knowledge
goes to `turns/backlog.md`: the repair re-post stall (fixed and
understood), the multi-builder (works), and the wood-depletion finding.

## Next

Turn 034: widen the wood/food scan radius (160 → 320 m, or grow it when
the local list empties) so the wood income survives into the late game,
then re-test the assault. See `turns/backlog.md`.
