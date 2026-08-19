# Turn 023 — Double-ring forge placement

Goal served: G4 (defeat sandbox Rome — City is the siege-path prerequisite).

## Hypothesis

> If the forge placement ring doubles (16 candidates at 72 m plus 16 at 88 m,
> same ≥ 28 m structure clearance), then the bot reaches City Phase before the
> match limit on ≥ 8/10 seeds, because turn 022 showed the single 72 m ring
> delivers 3 forges on only 5/10 seeds — the other five exhaust the ring on
> terrain/trees — and the city mechanism itself works on every seed that gets
> its forges (5/5 at minute 17–19).

Primary metric: fraction of seeds where `gameState.currentPhase() >= 3`
(sim ground truth) before the match limit, 0 JS errors.

Verdict thresholds (pre-registered): good if ≥ 8/10 seeds reach City, 0 JS
errors, canary PASS; bad if ≤ 2/10 or error/determinism veto; neutral
otherwise. Secondary (reported, not the verdict): city minute, forge count at
minute 16, composite.

## Implementation

In `bot/simulation/ai/vercingetorix/vercingetorix.js`:

- The turn-022 design is restored (reverted as the neutral verdict requires):
  3-forge target, training held while `forges < 3`, City research at 750/750
  via `canResearch` (fixed branch — no early return), sample fields.
- **New change:** `FORGE_OFFSETS` becomes 32 candidates — 16 at 72 m and 16
  at 88 m from the CC. The ring walk and clearance check are unchanged.

## Experiment

Settings: seeds 211–220 (fresh), sandbox Rome (`--difficulty2 0`),
`random/mainland` 128, `conquest_civic_centers`, treasures disabled, 20
game-minute limit (the G4 25-minute limit applies from the attack turn on),
biome/placement pinned. Baseline = HEAD (turn-022 commit); treatment =
double-ring placement; canary = seed 211.

## Results

- Canary: **PASS**.
- Primary metric: **9/10** seeds reach City, at minute 18–19. 0 JS errors.
  Composite −4.80 (reported; the army is deliberately small until the forges
  are up).
- The double ring fixes placement: forges = 3 by minute 16 on 9/10 seeds (the
  single ring managed 5/10). Seed 216 fails earlier: Town only at minute 14
  (slow house placement) and only 2 forges by minute 16 — the known house
  placement stall variant.

## Verdict

**Good** (pre-registered: ≥ 8/10 City, 0 JS errors, canary PASS): 9/10. The
change is kept.

## Action

Keep the change. Commit as `turn 023: forge-double-ring — good` and push.
`docs/CHANGELOG.md` gets an entry.

## Next

The siege endgame: build the arsenal in City (300 wood), train a siege ram
(300 wood + 150 metal, 150 crush per hit, restricted to structures), and
attack the enemy CC with ram + army under the 25-minute G4 limit (turn 024 —
the trigger's time limit moves from 20 to 25 minutes as part of that change).
See `turns/backlog.md`.
