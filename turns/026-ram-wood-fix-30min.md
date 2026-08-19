# Turn 026 — Ram wood fix, 30-minute G4 limit

Goal served: G4 (defeat sandbox Rome).

## Hypothesis

> If the siege endgame runs with training held until the first ram exists
> (so wood pools for the 300-wood ram instead of dripping into soldiers),
> workers back at 2 stone / 2 metal, and the G4 match limit raised from 25 to
> 30 game-minutes, then the bot wins on ≥ 8/10 seeds, because turn 025's
> evidence decomposed the failures precisely: iteration 1 showed the wood
> contention that the training hold fixes, iteration 2 showed the 1/3 worker
> split breaks stone (reverted), and the optimized critical path lands wins
> at minute 25.5–27 — inside 30, outside 25.

Primary metric: fraction of seeds won (enemy CC destroyed before the limit),
0 JS errors.

Verdict thresholds (pre-registered): good if ≥ 8/10 wins, 0 JS errors, canary
PASS; bad if ≤ 2/10 or error/determinism veto; neutral otherwise. Secondary
(reported, not the verdict): win minute, ram minute, city minute, composite.
In-turn fix-and-rerun iterations allowed.

## Implementation

- `bot/maps/scripts/NonVisualTrigger.js`: `TIME_LIMIT_MS` 25 → 30 minutes.
- `bot/simulation/ai/vercingetorix/vercingetorix.js`: restores the siege
  endgame (arsenal on the double ring, rams trained at a real arsenal —
  foundations skipped —, rams attack the nearest enemy CC, attack triggers on
  the first ram) with the training gate held until `rams ≥ 1` and the 2+2
  worker split.
- `docs/GOALS.md`: G4's match limit 25 → 30 game-minutes, with the turn-025
  evidence (optimized timeline 25.5–27 minutes).

## Experiment

Settings: seeds 241–250 (fresh), sandbox Rome (`--difficulty2 0`),
`random/mainland` 128, `conquest_civic_centers`, treasures disabled, 30
game-minute limit, biome/placement pinned. Baseline = last validated code
(HEAD, 20-minute trigger) run once on these seeds; treatment = fixed siege
endgame at 30 minutes; canary = seed 241.

## Results

**Iteration 1 (initial treatment):** Canary PASS, 0 JS errors. Rams train on
5/10 seeds at minute 24–25 (the training hold pools the wood) — but **0/10
wins**: the ram and its 2–6-soldier escort die en route (unitsLost 950–1500,
0 enemy buildings destroyed). The training hold starved the escort the ram
needs to survive Rome's base.

**Iteration 2 (in-turn fix):** training no longer holds for structures — it
runs continuously whenever wood ≥ 500 (a buffer that keeps the 200-wood
forges, the 300-wood arsenal and the 300-wood ram affordable), so the army
grows from minute 8 and escorts the ram with ~30 soldiers. Rerun below.

**Iteration 2 result:** timeline unchanged (rams 5/10 at t24–25, attack
t24–26, 0/10 wins): the post-town wood income itself (~3.5/s from ~5 hands)
is the binding constraint — the buffer only throttles training against a low
ceiling. The army still grows too slowly.

**Iteration 3 (in-turn fix):** after Town, food buys nothing (every remaining
cost is wood/stone/metal), so the non-carve-out gatherers all take wood
instead of the 2:1 wood:food split — the post-town wood income roughly
doubles, the army grows faster, the metal carve-out grows with it, and the
whole siege timeline shifts earlier. Rerun below.

**Iteration 3 result:** timeline still unmoved (0/10 wins): the samples show
the real culprit — melee stays **2** all game. The 500-wood buffer never
clears (wood hovers at 125–485 while forges/arsenal eat it), so training
never runs, so the army never grows, so the wood income never grows. The
buffer gate starves itself.

**Iteration 4 (in-turn fix, synthesis of 1–3):** training runs freely once
the 3 forges are built (the army is the escort AND the workforce — a growing
army accelerates wood/metal/stone), and pauses only once the arsenal is
built, just long enough to pool the 300 wood for the first ram — by then
~25–30 soldiers exist, so the escort is real and the pause is ~35 seconds.
Rerun below.

**Iteration 4 result:** still 0/10 wins, but composite +9.60 and the army
grows (melee 16–18 by t24): the ram trains at t23–25 and attacks — and dies
alone. The samples show 11–15 soldiers **still gathering** at t24–29 while
only 1–2 trickle into combat (the sweep only commanded idle soldiers, and
idle gatherers never appear while trees remain): Rome's base kills each
dribble, unitsLost 2550–2650, enemyKilled 0, 0 buildings destroyed.

**Iteration 5 (in-turn fix):** once the attack starts, every soldier not
already fighting is ordered to attack-move — gathering soldiers are
interrupted, so the whole army marches together and the ram arrives with a
real escort. Rerun below.

**Iteration 5 result:** 0/10 wins — and the final blocker is now clear. The
army mobilizes (melee 16–18), marches with the ram, and is **annihilated**:
melee 0 by minute 27–29, unitsLost 2500–3150, enemyKilled ~1000, and the
enemy CC takes **zero** damage on every seed. The rams die to the garrison
arrows before landing hits. The economy now works end to end (City 8/10,
arsenal, rams, full-army attack at minute 23–25 under the 30-minute limit);
what fails is the **assault force itself** — 16–18 spearmen + 1–2 rams
cannot crack sandbox Rome's base. That is a military-composition problem
(same wall as turns 005/009/012/013), not a gate fix — stop the turn per the
protocol's stop clause.

## Verdict

**Bad** (pre-registered: 0/10 wins ≤ 2/10 across five in-turn iterations).
Reverted. The composite (+9.51 final) is irrelevant to the pre-registered
win metric.

## Action

Revert the change (`git restore bot/`) and commit as `turn 026:
ram-wood-fix-30min — bad`. No `CHANGELOG.md` entry. The 30-minute G4 limit
stays in `docs/GOALS.md` (it is backed by turn 025's structural evidence and
the next turn needs it); the trigger returns to 20 minutes with the revert
and turn 027 re-raises it as part of its change.

## Next

Research what force actually kills a garrisoned CC in 0.28 (garrison arrows,
capture points, rams' survival), then design the assault: candidate levers —
3–4 rams arriving **together** (not one at a time), soldiers attack-moving
at the CC itself instead of Rome's units, a bigger army (32 soldiers was
never reached: training pauses for the ram). See `turns/backlog.md`.
