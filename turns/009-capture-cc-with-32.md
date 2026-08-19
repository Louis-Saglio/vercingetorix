# Turn 009 — Capture the enemy CC with the 32-soldier army

Goal served: G3 (defeat sandbox Rome).

## Hypothesis

> If I make the 32-soldier army directly attack (capture) the enemy civic
> centre instead of sweeping the nearest enemy entity, then the bot wins more
> seeds against sandbox Rome, because 32 spearmen can sustain a capture rate
> that outpaces the CC's 30/s regen and its garrison arrows — the failure mode
> of turn 005 (20 spearmen) is gone.

Primary metric: wins out of 10 seeds (enemy CC captured/destroyed before the
limit).

Verdict thresholds (pre-registered): good if ≥ 3/10 wins with 0 JS errors and
canary PASS; bad if 0/10 wins, or error/determinism veto; neutral if 1–2/10.

## Implementation

Two edits in `bot/simulation/ai/vercingetorix/vercingetorix.js` (one change:
direct capture-allowed attack on the enemy CC):

- Added `enemyCivCentre(gameState)`: the first enemy-owned entity with class
  `CivCentre`.
- The sweep now issues `soldier.attack(cc.id())` (capture allowed) at the enemy
  CC; if no CC exists, it falls back to the old nearest-enemy `attackMove`.

This re-applies turn 005's idea on top of the turn-008 32-soldier army.

## Experiment

Settings: seeds 81–90 (fresh), sandbox Rome (`--difficulty2 0`),
`random/mainland` 128, `conquest_civic_centers`, treasures disabled, 20
game-minute limit, biome/placement pinned. Baseline = HEAD (turn-008 code);
treatment = the CC-capture sweep; canary = seed 81.

Results:

- Canary: **PASS**.
- Win rate: **0/10 in both arms** (all time-limit draws; enemy CC never
  captured or destroyed).
- Composite: **−4.24** → bad; treatment `enemyUnitsKilledValue` drops to ~0
  because capture kills nothing.
- Why it still fails: the army reaches 32 (the 4-house fix from turn 008
  works), but the first assault on the garrisoned CC costs ~10 soldiers almost
  immediately (melee drops 32 → ~22 within two minutes). The bot then sustains
  ~22 capturers, a net ~25 capture/s against 30/s regen, which is not enough
  to fill 2500 points before replacements die en route.

## Verdict

**Bad.** 0/10 wins (pre-registered bad threshold), composite −4.24, no
error/determinism veto but no objective progress. The idea is refuted at this
army size: even 32 spearmen cannot out-capture a garrisoned CC.

## Action

Revert the change (`git restore bot/simulation/ai/vercingetorix/vercingetorix.js`)
and commit as `turn 009: capture-cc-with-32 — bad`. No `CHANGELOG.md` entry.

## Next

G3 resists the capture path with citizen soldiers: the CC's garrison out-paces
capture even at 32 soldiers. Reconsider G3 — the remaining realistic path is
crush-damage siege (Town → City → arsenal → rams), which is a longer chain.
See `turns/backlog.md`.
