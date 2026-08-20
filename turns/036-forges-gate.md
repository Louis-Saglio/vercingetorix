# Turn 036 — Forges gate

Goal served: G4b (defeat sandbox Rome).

## Hypothesis

> If soldier training is held until the three forges are built (turn 023's
> gate), on the restored assault configuration (ram gate 32, 2:1 soldier
> split, workers 1 stone / 2 metal / 1 food, attack at two rams), then the
> bot wins on ≥ 8/10 seeds before the 30-minute limit, because turn 035's
> A/B diagnosis showed the batch difference is forge timing: on the failing
> seeds the training eats the wood, the forges complete at minute 24–25,
> and the whole siege chain misses the window. With the gate, wood pools
> for the forges first (complete by ~minute 14), the city lands at 19–21
> like the winning batch, and the rams follow in time — while the turn-029
> food fix keeps the army growing fast afterwards.

Primary metric: fraction of seeds won before the 30-minute limit, 0 JS
errors.

Verdict thresholds (pre-registered): good if ≥ 8/10 wins, 0 JS errors, canary
PASS; bad if ≤ 2/10 or error/determinism veto; neutral otherwise. Secondary
(reported, not the verdict): attack minute, win minute, composite. In-turn
fix-and-rerun iterations allowed.

## Implementation

In `bot/maps/scripts/NonVisualTrigger.js` (30-minute limit) and
`bot/simulation/ai/vercingetorix/vercingetorix.js`:

- Restores the turn-032 assault configuration (reverted as its neutral
  verdict required): `RAM_ARMY_GATE = 32`, 2:1 post-town soldier split,
  post-town workers 1 stone / 2 metal / 1 food.
- The training gate adds `forges >= FORGE_TARGET` (turn 023's gate — the
  turn-035-diagnosed fix).

## Experiment

Settings: seeds 301–310 (the failing batch), sandbox Rome
(`--difficulty2 0`), `random/mainland` 128, `conquest_civic_centers`,
treasures disabled, 30 game-minute limit, biome/placement pinned. Baseline =
the stored turn-033 baseline (last validated code on these seeds — reused);
canary = stored turn-033 canary; treatment = the forges gate.

## Results

**Iteration 1 (forges gate):** 0/10 — the forges finish early (3 by minute
18–20) and the city lands at 22–25, but the army pays: training starts at
minute 14–18 and grows at ~3/min (melee 31 by minute 28 on the best seed),
so the 32-soldier ram gate barely passes and no rams train. The gate fixed
the forges and starved the army — the missing piece is the wood to feed
both.

**Iteration 2 (in-turn fix):** add the 320 m wood radius (turn 034's fix) —
the extra wood feeds the forges AND the army. Rerun below.

**Iteration 2 result:** identical 0/10 — the radius does not move the army
growth; the binding constraints on this batch are the hand count while the
army is small and the food/wood walking distances, not the tree supply. The
economy structure itself is at its ceiling. Stop-the-turn.

## Verdict

**Bad** (pre-registered: 0/10 ≤ 2/10). Reverted.

## Action

Revert the change (`git restore bot/`) and commit as `turn 036:
forges-gate — bad`. No `CHANGELOG.md` entry. G4b is reconsidered in this
commit (it resists turns 024–036): the siege chain wins when the economy
lands it (5/10 on seeds 291–300) but is batch-dependent — the next goal is
a **robust economy** (farmstead + fields for renewable food, more gatherer
hands) before the win goal returns.

## Next

Turn 037: build a farmstead and fields (the renewable food engine — the
finite early food is the batch-dependence), the first step of the robust
economy. See `turns/backlog.md`.
