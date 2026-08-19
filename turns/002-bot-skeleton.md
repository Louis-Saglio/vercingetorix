# Turn 002 — Bot skeleton baseline

## Hypothesis

Prerequisite turn (no improvement claim): every future turn needs a bot that plays.

Acceptance criteria, stated as a hypothesis:

> If the bot is a minimal scripted mod (grow citizen soldiers, rush, sweep) that
> completes a full match against sandbox Rome, then a 10-seed batch against sandbox
> Rome will finish with 0 JS errors and every match reaching a verdict (win or
> draw), giving the baseline numbers every future turn is compared against.

Primary metric for verification: 0 JS errors, 0 matches without a verdict
(no timeouts other than recorded draws).

## Implementation

- Bot mod in `bot/`: `mod.json` (depends on `0ad=0.28.0` — the public mod carries
  the autostart scripts), `simulation/ai/vercingetorix/data.json`,
  `simulation/ai/vercingetorix/vercingetorix.js` (ES module, 0.28 style), and
  `maps/scripts/NonVisualTrigger.js` (game-time limit + stats printing).
- 0.28 has no dedicated worker units: citizen soldiers gather and fight. The
  skeleton trains infantry spearmen (gaul) up to 20, keeps idle ones gathering
  (2/3 wood, 1/3 food, within 40 tiles of the CC), builds houses when population
  nears the CC's 20 cap, then attacks at 15+ and sweeps the nearest enemy entity
  until Conquest ends the game.
- Harness gains `--mod-dir PATH`: copies the bot mod into
  `~/.local/share/0ad/mods/<name>` under each match HOME before spawning.
- Design change from the first attempt: the initial version trained
  "support_female_citizen", which does not exist as a trainable unit in 0.28 —
  caught by Louis's review and the game data.

### 0.28 gotchas discovered and fixed (each cost a failed run)

1. `-mod=NAME` disables the public mod; autostart needs `-mod=public -mod=NAME`.
2. Trainer tokens use `units/{civ}/...` (slash), not the older underscore form.
3. `print()` in the AI realm does not append newlines — harness lines merged.
4. Trees have no Identity classes; resources are found via `getResourceType()`
   (ResourceSupply/Type "wood.tree").
5. `EntityCollection.values()` returns an iterator, not an array.
6. `GameState.getTemplate()` returns a wrapper; read fields via `.get("path")`.
7. Positions are in meters (4 m/tile) — all offsets and radii must scale.
8. The CC gives 20 population; laborers ("Civilian Worker", no `Unit` class —
   invisible to `findBuilder`) build houses; `construct()` only places the
   foundation (`autorepair:false`) — the actual building needs a separate
   `repair` order.
9. Entities mid-destruction have no position — guard before distance math.

## Experiment

- Match limit: 20 minutes of **game time**, enforced by the mod's trigger
  (`bot/maps/scripts/NonVisualTrigger.js`); the harness wall-clock timeout is a
  safety net only.
- Smoke: `harness --tag smoke --seeds 42 --ai1 vercingetorix --ai2 petra
  --difficulty2 0 --mod vercingetorix --mod-dir bot` (map/civs are the new
  defaults: mainland, gaul vs rome).
- Baseline: same with `--tag baseline --seeds 1,2,3,4,5,6,7,8,9,10`.
- Results: baseline 10/10 finished at the limit, 0 JS errors; per-match numbers
  in `experiments/002/baseline.json` (trained 14-61, houses 1-2, attacks on all
  seeds). Graded against goal G1: mostly Fail/Pass — the skeleton is a starting
  point, not a goal achievement.

## Verdict

Passed (prereq fulfilled). The 10-seed baseline batch: 10/10 matches reach a
verdict at the 20-game-minute limit (all time-limit draws — the skeleton does
not beat sandbox Rome yet), 0 JS errors, exit 0 every match, houses and training
work on every seed. The batch JSON is committed as the reference baseline for all
future turns.

Open question recorded for a future evidence turn: `unitsLost` stays 0 while the
live melee count drops mid-fight — some soldiers leave the `Melee` filter without
being counted as lost. Needs investigation (promotion? capture? state handling).

## Action

Commit as `turn 002: bot-skeleton — good`; then STOP per Louis's instruction
(no turn 003 without his go-ahead).

## Next

Turn 003 (on Louis's go-ahead): report tool implementing the composite verdict
score, canary match, and draw semantics. Then real hypotheses against this
baseline, graded on goal G1 (economy boot).
