# Turn 004 — Reach the 20-soldier target before attacking

Goal served: G1 (economy boot) — **achieved** this turn (see Action).

## Hypothesis

> If I raise the bot's attack threshold from 15 to the 20-soldier target, then
> the mean peak melee count in the first 8 game-minutes rises by ≥10% versus
> the baseline, because the premature attack at 15 is what currently prevents
> the army from ever reaching 20.

Primary metric: mean over the 10 seeds of the maximum `melee` count in the
bot's per-minute `[HARNESS]` samples with `t` in 1..8.

Verdict thresholds (single-metric, `PROTOCOL.md`): good if the treatment mean
improves ≥10% relative to baseline; bad if it worsens ≥10%; neutral otherwise
(escalate on neutral). The error veto (any pair increases JS errors → bad) and
the determinism canary both apply.

## Implementation

One-line change in `bot/simulation/ai/vercingetorix/vercingetorix.js`:

- `const ATTACK_THRESHOLD = 15;` → `const ATTACK_THRESHOLD = SOLDIER_TARGET;`

The skeleton's own plan is "grow to `SOLDIER_TARGET` (20), then attack"; the
threshold was 15, below the target, so the army was sacrificed before it ever
reached 20. Aligning the two makes the bot reach 20 citizen soldiers before the
first attack. Instrumentation is the existing per-minute `[HARNESS]` `melee`
sample — no new collection is needed.

## Experiment

Settings: seeds 21–30 (fresh, never reused), sandbox Rome (`--difficulty2 0`,
per G1), `random/mainland` 128, `conquest_civic_centers`, treasures disabled,
20 game-minute limit, biome/placement pinned (canary gate). Baseline = HEAD
(committed turn-003 code) run on the turn's seed set; treatment = the one-line
change; canary = seed 21 repeated with the baseline code.

Commands (run from `harness/`):

- baseline: `./target/release/harness --tag baseline --seeds 21,...,30 --out ../experiments/004 --ai1 vercingetorix --ai2 petra --difficulty2 0 --mod vercingetorix --mod-dir ../bot`
- canary: same with `--tag canary --seeds 21`
- treatment (after the edit): same with `--tag treatment --seeds 21,...,30`
- report: `./target/release/harness report --baseline ../experiments/004/baseline.json --treatment ../experiments/004/treatment.json --canary ../experiments/004/canary.json --out ../experiments/004`

Results:

- Canary: **PASS** (seed 21 reproduced identically).
- Composite score: total **+9.00** (≥ +4), error veto false → good.
- Primary metric (mean peak `melee`, game-minutes 1–8):
  baseline **15.7** → treatment **20.7** = **+31.8%** (≥ +10%) → good.
- Error veto: none (all 20 matches 0 JS errors).
- G1 grade distribution (per-minute samples): baseline 9 Fail / 1 Pass;
  treatment **10 Good / 0 others** (every seed reaches ≥20 melee by minute 8;
  minute-10 melee 19–22). Full per-match numbers in `experiments/004/`.

## Verdict

**Good.** Primary metric improved +31.8% (≥10%), composite +9.00 (≥+4), canary
PASS, 0 JS errors. No error/determinism veto. The change is kept.

## Action

Keep the change. Commit as `turn 004: grow-to-20-before-attack — good` and push.

This batch also **achieves G1** (economy boot): 10/10 seeds Good or better with
0 JS errors, against sandbox Rome — the criterion is ≥8/10. `GOALS.md` is
updated in the same commit to record the closing batch and define G2 (defeat
sandbox Rome).

## Next

Goal G2: defeat sandbox Rome (win ≥8/10 seeds, 0 JS errors). Candidates: raise
the soldier target so the army keeps growing past 20 instead of plateauing,
then attack later/harder; or add siege / civic-centre targeting. The two
standing backlog items (phase-timing evidence, perf scan optimization) remain
available but are not G2 blockers.
