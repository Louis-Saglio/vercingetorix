# Turn 030 — Assault-ready army

Goal served: G4a (the assault-ready army), feeding G4b (the win).

## Hypothesis

> If the ram gate drops from 50 to 32 soldiers (the rams no longer wait for
> the full army), then ≥ 8/10 seeds reach the re-scoped G4a state — ≥ 32
> melee at minute 22 AND ≥ 3 rams by minute 24 — because turn 029 reaches 32
> soldiers by t22 on 8/10 seeds, and the rams (300 wood + 150 metal each)
> are affordable with the fixed food/wood economy. The attack then fires on
> two rams with 32–53 soldiers behind it — the first real assault test since
> turn 027's 18-unit force was annihilated.

Primary metric: fraction of seeds with ≥ 32 melee at the minute-22 sample
AND ≥ 3 rams at the minute-24 sample, 0 JS errors.

Verdict thresholds (pre-registered): good if ≥ 8/10 seeds reach the metric,
0 JS errors, canary PASS; bad if ≤ 2/10 or error/determinism veto; neutral
otherwise. Secondary (reported, not the verdict): wins before the 30-minute
limit, composite. In-turn fix-and-rerun iterations allowed.

## Implementation

In `bot/simulation/ai/vercingetorix/vercingetorix.js`:

- `manageRams` gates on 32 melee soldiers instead of `SOLDIER_TARGET` (50):
  `RAM_ARMY_GATE = 32` constant.

## Experiment

Settings: seeds 271–280 (fresh), sandbox Rome (`--difficulty2 0`),
`random/mainland` 128, `conquest_civic_centers`, treasures disabled, 30
game-minute limit, biome/placement pinned. Baseline = last validated code
(HEAD, turn-029 state) run once on these seeds; treatment = ram gate at 32;
canary = seed 271.

## Results

- Canary: **PASS**. 0 JS errors. Composite +0.50.
- Primary metric: **0/10** — melee at t22 is strong (25–47), but **no rams
  train by t24 anywhere**. The timeline is the wall: City lands at minute
  20–29 (the post-town food workers slowed the stone/metal income), the
  arsenal builds in 180 s after that (t23–32), and three rams cost 900 wood
  + 450 metal — the metal alone regathers at ~1.4/s, so 3 rams need ~5 more
  minutes post-City. "3 rams by minute 24" was structurally unreachable, not
  a code failure.

## Verdict

**Bad** (pre-registered: 0/10 ≤ 2/10). Reverted. The ram gate at 32 is
directionally right (the baseline never trains rams at all under the 50
gate); the metric was wrong.

## Action

Revert the change (`git restore bot/`) and commit as `turn 030:
assault-ready-army — bad`. No `CHANGELOG.md` entry. G4a's target is corrected
in `docs/GOALS.md` with this timeline evidence: ≥ 32 melee by minute 22 AND
≥ 2 rams by minute 26 AND the attack fires (assault-ready), replacing the
unreachable "3 rams by minute 24".

## Next

Turn 031: re-test the ram gate at 32 with the corrected G4a metric
(≥ 32 melee at t22, ≥ 2 rams at t26, attack fired) — and watch the first
real assault with a 32–53-soldier army. See `turns/backlog.md`.
