# Goals

Long-term goals that span multiple turns. Each turn grades its experiment against
the current goal's scale. When a goal is achieved, the next goal and its grading
system are defined in the closing commit.

## Current goal: G2 — Defeat sandbox Rome

**Statement:** Vercingetorix reliably defeats sandbox Rome by destroying its
civic centre under `conquest_civic_centers` before the 20-game-minute limit.

**Grading per match** (win = enemy CC destroyed before the limit; draw = time
limit with both CCs standing; loss = our CC destroyed):

- **Good** — win (enemy CC destroyed), with 0 JS errors.
- **Pass** — draw at the limit, but the bot had the better of the fighting
  (`enemyUnitsKilled > unitsLost`).
- **Fail** — loss, or a draw with `enemyUnitsKilled ≤ unitsLost`, or JS errors.

**Goal achieved when:** a 10-seed batch against sandbox Rome wins ≥ 8/10 seeds
with 0 JS errors. Record the batch in the closing commit and define goal G3
(defeat medium (difficulty 3) Rome).

## Completed goals

### G1 — Economy boot (achieved turn 004)

Vercingetorix reliably collects wood and food and grows its unit count from the
starting units.

Grading (historical): **Excellent** — 20 citizen soldiers reached by game-minute
8 and the soldier count at minute 20 is at least double the count at minute 10;
**Good** — 20 by minute 12, or the doubling condition; **Pass** — 20 by minute
16, or steady growth (minute-20 count > minute-10 count) without doubling;
**Fail** — otherwise.

**Closing batch:** turn 004, seeds 21–30 vs sandbox Rome — **10/10 Good, 0 JS
errors** (baseline was 9 Fail / 1 Pass). The validated change: attack at
`SOLDIER_TARGET` (20) instead of at 15, so the bot reaches 20 citizen soldiers
before the first attack.

## Backlog of candidate goals (unrefined, for later)

- G3: defeat medium (difficulty 3) Rome.
- G4: town phase timing: reach Town Phase by minute X and City by minute Y.

## Reconsideration rule

If G2 (or any goal) resists several turns of effort, stop and reconsider: is it too
ambitious? Does it depend on another goal that should come first? Adjust the goal
here, with a note explaining why.
