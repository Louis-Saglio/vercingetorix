# Turn 017 — Starting workers on stone/metal from minute 0

Goal served: G3 (gather 750 stone + 750 metal by game-minute 16).

## Hypothesis

> If I put the four starting support workers on stone and metal from minute 0
> (two each — they are idle all game, the bot never commands them), on top of
> the turn-016 post-town army carve-out, then the bot reaches ≥ 750 stone AND
> ≥ 750 metal by game-minute 16 on ≥ 8/10 seeds, because turn 016 showed the
> binding constraint is early hands: gathering only starts after Town (minute
> 8–9) and the army grows too slowly to make up the time. Workers add ~16
> minutes of gathering at 0.35/s per resource, before the army exists.

Primary metric: fraction of seeds whose minute-16 `[HARNESS]` sample shows
stock ≥ 750 stone AND ≥ 750 metal, 0 JS errors.

Verdict thresholds (pre-registered): good if ≥ 8/10 seeds reach the primary
metric, 0 JS errors, canary PASS, composite > −4; bad if ≤ 2/10 or
error/determinism veto; neutral otherwise.

## Implementation

In `bot/simulation/ai/vercingetorix/vercingetorix.js`:

- The turn-016 gathering design is restored (it was reverted as the bad
  verdict requires): full-map stone/metal caches, post-town army carve-out
  (`id % 16 < 3` stone, `< 5` metal), attack gated on 750/750, `stone`/`metal`
  in the `[HARNESS]` sample. This is the known-working post-town mechanism
  from turn 016's evidence, not a new hypothesis.
- **New change:** `manageWorkers` commands idle Support-class entities (the
  four starting laborers — distinct from citizen soldiers, which are also
  Worker-class) to gather stone (even id) or metal (odd id), from minute 0.
  It runs before `manageHouses`, so house-building takes whichever soldier is
  idle and the workers stay on the mines.

## Experiment

Settings: seeds 151–160 (fresh), sandbox Rome (`--difficulty2 0`),
`random/mainland` 128, `conquest_civic_centers`, treasures disabled, 20
game-minute limit, biome/placement pinned. Baseline = HEAD (turn-016 commit);
treatment = worker stone/metal gathering + restored carve-out; canary = seed
151.

## Results

- Canary: **PASS**.
- Primary metric: **10/10** seeds reach ≥ 750 stone AND ≥ 750 metal at the
  minute-16 sample (G3 Good tier); all 10 also pass the ≥ 500/500 tier.
- 0 JS errors in all matches, both arms.
- Composite: **−2.34** (neutral band, > −4 as pre-registered). The negative
  part is the deferred attack: `enemyUnitsKilled` drops (army hasn't marched
  yet) and `unitsTrained` is slightly lower on a few seeds. `resourcesGathered`
  is **up on every seed** (+4% to +12%) and melee reaches 30+ by minute 16 on
  8/10 seeds — the wood/food economy is not collapsed, it is converted into
  stone/metal income.
- Per-seed t16 (treatment): 151 1070/1280, 152 1730/1171, 153 1480/1010,
  154 1280/1240, 155 1280/1280, 156 1430/1010, 157 1810/1700, 158 1330/1150,
  159 1800/970, 160 2330/990 (stone/metal stock).

The workers close the gap turn 016 identified: four hands on stone/metal from
minute 0 (~0.35/s each, pure economy all match) plus the post-town army
carve-out clears 750/750 with margin on every seed.

## Verdict

**Good** (pre-registered: ≥ 8/10, 0 JS errors, canary PASS, composite > −4):
10/10 on the primary metric. The change is kept.

## Action

Keep the change. Commit as `turn 017: workers-stone-metal — good` and push.
`docs/CHANGELOG.md` gets an entry. **G3 is closed in this commit**: this batch
is the goal's closing batch (Good on 10/10 seeds, 0 JS errors, canary PASS —
criterion: ≥ 8/10), so `docs/GOALS.md` promotes G4 (defeat sandbox Rome) to
the current goal with its grading scale.

## Next

G4: defeat sandbox Rome. The path on the backlog: research City Phase once
750/750 are banked (City needs 750 stone + 750 metal and 3 Town structures),
then an arsenal + siege ram for the CC. The attack now waits for 750/750, so
the bot already banks the resources; the next turn adds the City research.
