# Turn 020 — City Phase via three forges

Goal served: G4 (defeat sandbox Rome — the siege path needs City for the
arsenal).

## Hypothesis

> If the bot builds three forges after real Town (each carries the sim's Town
> class, 200 wood, no special limits) and posts City once stone ≥ 750, metal ≥
> 750 and the sim's `canResearch` passes, then `gameState.currentPhase()`
> reaches 3 before the 20-minute limit on ≥ 8/10 seeds, because turn 019 made
> Town real at minute 7–8, turn 017 banks 750/750 by minute 16, and the only
> missing piece is the 3-Town-structure requirement.

Primary metric: fraction of seeds where `gameState.currentPhase() >= 3`
(sim ground truth) before the 20-minute limit, 0 JS errors.

Verdict thresholds (pre-registered): good if ≥ 8/10 seeds reach City, 0 JS
errors, canary PASS; bad if ≤ 2/10 or error/determinism veto; neutral
otherwise. Secondary (reported, not the verdict): city minute, stone/metal at
minute 16, composite.

## Implementation

In `bot/simulation/ai/vercingetorix/vercingetorix.js`:

- `manageForges(gameState, cc)`: the house pattern generalized to forges —
  repair the pending foundation with a unit that can actually build forges,
  place the next forge (same 8 offsets) while `forges < 3` and wood ≥ 200.
  Serialized `forgeAttempts` counter, `FORGE_TARGET = 3`.
- `manageResearch`: after the real-Town check (`currentPhase() >= 2`), a
  serialized `cityAttempted` flag posts `phase_city*` once stone ≥ 750,
  metal ≥ 750 and `gameState.canResearch(cityTech)` pass.
- The `[HARNESS]` sample adds `forges` and `cityCan`.

## Experiment

Settings: seeds 181–190 (fresh), sandbox Rome (`--difficulty2 0`),
`random/mainland` 128, `conquest_civic_centers`, treasures disabled, 20
game-minute limit, biome/placement pinned. Baseline = HEAD (turn-019 commit);
treatment = forges + City research; canary = seed 181.

## Results

- Canary: **PASS**.
- Primary metric: **0/10** seeds reach City. 0 JS errors. Composite +0.22.
- The mechanism works end to end (real Town on 9/10 at minute 7–8; stone/metal
  banked), but the forges lose the wood race: soldier training consumes every
  spare 50 wood from minute 8 on, so wood hovers at 25–300 and the first forge
  lands at minute 12–18 (0–2 forges by minute 16). City research (needs 3
  forges + 750/750) never gets the chance inside the 20-minute limit. Seed 187
  also re-hits the 5-house placement stall (phase stays 1).
- The builder churn of the forge foundations (repair orders interrupt
  gatherers) also shaves stone/metal income: metal 710–1200 at t16 vs
  870–1200 in turn 019.

## Verdict

**Bad** (pre-registered: 0/10 ≤ 2/10). The hypothesis underestimated wood
contention: forge construction cannot compete with continuous training.
Reverted.

## Action

Revert the change (`git restore bot/simulation/ai/vercingetorix/vercingetorix.js`)
and commit as `turn 020: city-forges — bad`. No `CHANGELOG.md` entry.

## Next

Hold soldier training until the 3 forges exist (like the pre-Town gate), so
wood pools for the forges; then City research follows at 750/750. The
5-house placement stall (~1/10 seeds) stays on the backlog. See
`turns/backlog.md`.
