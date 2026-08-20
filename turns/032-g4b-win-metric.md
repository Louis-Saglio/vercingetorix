# Turn 032 — G4b: the win metric

Goal served: G4b (defeat sandbox Rome).

## Hypothesis

> If the turn-031 winning configuration is restored — ram gate at 32, 2:1
> wood:food soldier split post-town, two post-town food workers — then the
> bot wins (enemy CC destroyed before the 30-minute limit) on ≥ 8/10 seeds,
> because turn 031's iteration 2 won on seeds 282/285 (the project's first
> wins: attack at minute 25/27) and the assault machinery demonstrably cracks
> the sandbox base when the chain lands on time; the slow seeds are the known
> gap (City t22–27 → arsenal +180 s → rams t26–29), and the understood lever
> is a post-town worker moved from food to metal.

Primary metric: fraction of seeds won before the 30-minute limit, 0 JS
errors.

Verdict thresholds (pre-registered): good if ≥ 8/10 wins, 0 JS errors, canary
PASS; bad if ≤ 2/10 or error/determinism veto; neutral otherwise. Secondary
(reported, not the verdict): attack minute, win minute, composite. In-turn
fix-and-rerun iterations allowed.

## Implementation

In `bot/simulation/ai/vercingetorix/vercingetorix.js`:

- `RAM_ARMY_GATE = 32`; `manageRams` gates on it.
- The post-town soldier gather split returns to 2:1 wood:food (turn 031
  iteration 2 — the 1:1 split starved the forges of wood); the two post-town
  food workers stay.

## Experiment

Settings: seeds 291–300 (fresh), sandbox Rome (`--difficulty2 0`),
`random/mainland` 128, `conquest_civic_centers`, treasures disabled, 30
game-minute limit, biome/placement pinned. Baseline = last validated code
(HEAD, turn-029 state) run once on these seeds; treatment = the winning
configuration; canary = seed 291.

## Results

**Iteration 1 (winning configuration):** Canary PASS, 0 JS errors, composite
+8.19. **3/10 wins** (293, 294, 296 — attack at minute 24–27), attack fires
on 6/10, City 10/10 at minute 20–26. The slow seeds (291, 295, 299, 300:
City t24–26) never get rams out in time — the City's 750 metal binds the
timeline.

**Iteration 2 (in-turn fix):** post-town workers become 1 stone / 2 metal /
1 food (one more metal hand — City ~1 minute earlier on the slow seeds).
Rerun below.

**Iteration 2 result:** 5/10 wins (up from 3/10), composite +11.81, attack
fires on 7/10. The remaining draws split into two: 294/295/299 never get
rams out (City t20–25 but the chain stalls), and 292/297 attack at minute 26
with the kill landing just past the 30-minute limit.

**Iteration 3 (in-turn fix):** the attack triggers at 32 soldiers OR the
first ram — the army marches early (minute ~22) and occupies Rome's
defenders while the rams walk in. Rerun below.

**Iteration 3 result:** regression — 0/10 wins, composite −0.70. The army
marches at minute 18–25, the gather loop stops with it, the economy
collapses, and the rams never train (0–2) — the exact turn-027 failure mode.
The rams need the running economy; the army cannot march without them.

**Stop-the-turn decision:** the iterations went 3/10 → 5/10 → 0/10; the best
configuration is iteration 2 (5/10 wins, composite +11.81). The remaining
gap has two known causes: (a) the draw-with-attack seeds kill at ~t30.5 —
a third ram joining the assault would add 50% crush; (b) the no-attack seeds
stall the arsenal/ram chain. These are turn 033's pre-registered levers.

## Verdict

**Neutral** (5/10 at the best iteration; the final iteration regressed to
0/10). Reverted per the rules; the winning configuration is documented
above for turn 033.

## Action

Revert the change (`git restore bot/`) and commit as `turn 032:
g4b-win-metric — neutral (reverted)`. No `CHANGELOG.md` entry. The
iteration-2 configuration and the levers go to `turns/backlog.md`.

## Next

Turn 033: restore the iteration-2 configuration (ram gate 32, 2:1 split,
1 stone / 2 metal / 1 food workers, attack at 2 rams) plus the two levers —
a third ram and multiple builders on the arsenal — and pre-register wins
≥ 8/10 before the 30-minute limit. See `turns/backlog.md`.
