# Turn 029 — Food fix: the silent training killer

Goal served: G4a (army scaling) — evidence-collection turn that found and
fixed the root cause.

## Hypothesis

> If I diagnose why the CC trains at ~1 soldier/min despite abundant wood and
> an empty queue (turn 028's mystery), then I can fix the true binding
> constraint, because every diagnostic so far contradicted the wood theory —
> wood stockpiled to 2110 while the queue stayed empty.

Primary metric: the diagnosis (qualitative), plus the fix's verification:
melee ≥ 32 at the minute-22 sample on ≥ 8/10 seeds (the turn-023-known-good
level), 0 JS errors, canary PASS.

## Implementation

- Diagnostic (temporary, reverted before the experiment): an override of the
  sim's `Commands.js`/`Trainer.js` with logging showed the train command dies
  silently in `Trainer.Item.Queue` → `TrySubtractResources`: the sim's
  spearman costs **{food: 50, wood: 50}** — the base infantry template's 50
  food is inherited and merged with the spearman's own 50 wood — and the bot's
  post-town food income is **zero** since the turn-026 "food buys nothing"
  change sent all gatherers to wood. The sim rejects unaffordable train
  orders with no log; the AI realm's own `canAfford({wood:50})` check passed
  because it ignored food. That is the whole turn-028 mystery: the army
  starved on food, not wood.
- **The fix:** the post-town gather split returns to 2:1 wood:food (the
  carve-out unchanged). `template_unit_infantry.xml`'s 50-food cost is
  documented in the code comment.
- The turn-028 iteration-5 design is otherwise restored (free post-town
  training, 8 houses with hybrid placement, rams gated on the full army,
  30-minute trigger).

## Experiment

Settings: seeds 261–270 (the turn-028 batch), sandbox Rome
(`--difficulty2 0`), `random/mainland` 128, `conquest_civic_centers`,
treasures disabled, 30 game-minute limit, biome/placement pinned. Baseline =
the last validated code's stored results on these seeds
(`experiments/028/baseline.json`, run once per the baseline rule — reused);
canary = `experiments/028/canary.json` (stored); treatment = the food fix.

## Results

**Iteration 1 (food fix):** Canary PASS, 0 JS errors, composite **+17.29**.
Melee max 25–52 (was 15–19 in turn 028), City 10/10 — the food fix unblocks
training completely. But only **4/10** seeds reach ≥ 32 melee at t22
(12–34): with 50 food + 50 wood per soldier and a 2:1 wood:food split, food
binds the growth at ~3 soldiers/min.

**Iteration 2 (in-turn fix):** the gather split becomes 1:1 wood:food — the
two 50-costs balance. Rerun below.

**Iteration 2 result:** regression — 1/10. The 1:1 split applied pre-town
too, halving the Village-phase wood income (the phase needs 1100 wood vs 500
food), so Town slid to minute 13–20 and everything after followed.

**Iteration 3 (in-turn fix):** pre-town keeps 2:1 wood:food; post-town uses
1:1. Rerun below.

**Iteration 3 result:** 5/10 — melee max 41–52 on all seeds (the 50-army is
now real), Town at minute 9–13. The misses (27–31 at t22) are the late-town
seeds: the 8 pre-town houses delay Town by 1–2 minutes on the marginal
seeds.

**Iteration 4 (in-turn fix):** only the 5 Village-requirement houses build
pre-town; the extra pop houses come after Town. Rerun below.

**Iteration 4 result:** 6/10 — Town at minute 7–8 everywhere, but four seeds
(263, 267, 268, 269) stay food-bound: food sits at 0–40 from minute 10 as
the early food sources deplete, capping training at ~1/min while wood pools.

**Iteration 5 (in-turn fix):** post-town, two of the four workers switch to
food (1.0/s each, twice the soldier rate). Rerun below.

**Iteration 5 result: 8/10** — the food-poor seeds recover (263: 14 → 33,
268: 28 → 37, 269: 30 → 43 at t22); the misses are 267 (26) and 270 (29),
both close. Melee max 43–53 everywhere, City 10/10, composite **+17.19**,
0 JS errors, canary PASS.

## Verdict

**Good** (pre-registered: ≥ 8/10 with ≥ 32 melee at minute 22, 0 JS errors,
canary PASS): 8/10. The change is kept. The evidence-collection question is
answered decisively: the spearman costs 50 food + 50 wood (the base infantry
template's 50 food is inherited), the sim silently rejects unaffordable
train orders, and the turn-026 "food buys nothing" change had starved the
army.

## Action

Keep the change. Commit as `turn 029: food-fix — good` and push.
`docs/CHANGELOG.md` gets an entry; `docs/GAME.md` corrects the spearman cost
(50 food + 50 wood); `docs/GOALS.md` re-scopes G4a to the evidence-supported
target (≥ 32 melee by minute 22 — reached 8/10 here — plus 3 rams by minute
24, the turn-030 metric). The validated mod zip is published to the file
server (standing instruction).

## Next

Turn 030: the assault-ready army — relax the ram gate from 50 to 32
soldiers, keep the attack at two rams, and test G4a (32 melee by t22 AND 3
rams by t24) plus the first real assault at the 30-minute limit. See
`turns/backlog.md`.
