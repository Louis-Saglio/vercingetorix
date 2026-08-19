# Goals

Long-term goals that span multiple turns. Each turn grades its experiment against
the current goal's scale. When a goal is achieved, the next goal and its grading
system are defined in the closing commit.

## Current goal: G1 — Economy boot

**Statement:** Vercingetorix reliably collects wood and food and grows its unit
count exponentially from the starting units.

**Grading per match** (against the per-minute samples):

- **Excellent** — 20 citizen soldiers reached by game-minute 8, and the soldier
  count at minute 20 is at least double the count at minute 10.
- **Good** — 20 citizen soldiers reached by game-minute 12, or the doubling
  condition holds even if later than 8 minutes.
- **Pass** — 20 citizen soldiers reached by game-minute 16, or steady growth
  (soldier count at 20 > soldier count at 10) without doubling.
- **Fail** — anything else: stall, decline, fewer than 20 soldiers by minute 20,
  or JS errors.

**Goal achieved when:** a 10-seed batch against sandbox Rome scores Good or better
on ≥ 8/10 seeds with 0 JS errors. Record the batch in the closing commit and define
goal G2 (e.g. defeat sandbox Rome consistently; then medium Petra).

## Backlog of candidate goals (unrefined, for later)

- G2: defeat sandbox Rome (win ≥ 8/10 seeds on the standard batch).
- G3: defeat medium (difficulty 3) Rome.
- G4: town phase timing: reach Town Phase by minute X and City by minute Y.

## Reconsideration rule

If G1 (or any goal) resists several turns of effort, stop and reconsider: is it too
ambitious? Does it depend on another goal that should come first? Adjust the goal
here, with a note explaining why.
