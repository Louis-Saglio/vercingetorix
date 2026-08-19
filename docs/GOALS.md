# Goals

Long-term goals that span multiple turns. Each turn grades its experiment against
the current goal's scale. When a goal is achieved, the next goal and its grading
system are defined in the closing commit.

## Current goal: G3 — Gather 750 stone and 750 metal

**Statement:** Vercingetorix gathers the 750 stone and 750 metal that City Phase
requires, without collapsing its wood/food economy. This is the prerequisite for
the siege path (City → arsenal → ram) that eventually defeats sandbox Rome.

**Grading per match** (against the per-minute `[HARNESS]` samples):

- **Good** — ≥ 750 stone AND ≥ 750 metal gathered by game-minute 16.
- **Pass** — ≥ 500 of each by game-minute 16.
- **Fail** — otherwise, or JS errors.

**Goal achieved when:** a 10-seed batch against sandbox Rome reaches Good on
≥ 8/10 seeds with 0 JS errors. Record the batch in the closing commit and move
on to G4.

## Completed goals

### G1 — Economy boot (achieved turn 004)

20 citizen soldiers by game-minute 8/12/16 and growth (see turn 004). Closing
batch: seeds 21–30, 10/10 Good, 0 JS errors.

### G2 — Sustain a 32+ citizen-soldier army (achieved turn 008)

32 melee soldiers by game-minute 12. Closing batch: seeds 71–80, 8/10 Good,
0 JS errors.

## Backlog of candidate goals (unrefined, for later)

- G4: defeat sandbox Rome (win ≥ 8/10 seeds on the standard batch).
- G5: defeat medium (difficulty 3) Rome.
- G6: town phase timing: reach Town Phase by minute X and City by minute Y.

## Reconsideration rule

If a goal resists several turns of effort, stop and reconsider: is it too
ambitious? Does it depend on another goal that should come first? Adjust the goal
here, with a note explaining why.

## Reconsideration note (turn 015)

"Defeat sandbox Rome" (formerly G3) resisted five turns (005, 009, 010, 012,
013). It was split: the current G3 is the stone/metal resource prerequisite, and
the win goal is now G4.
