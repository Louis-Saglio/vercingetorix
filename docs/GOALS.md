# Goals

Long-term goals that span multiple turns. Each turn grades its experiment against
the current goal's scale. When a goal is achieved, the next goal and its grading
system are defined in the closing commit.

## Current goal: G3 — Defeat sandbox Rome

**Statement:** Vercingetorix reliably defeats sandbox Rome by capturing or
destroying its civic centre under `conquest_civic_centers` before the 20-minute
game limit.

**Grading per match** (win = enemy CC captured/destroyed before the limit;
draw = time limit with both CCs standing; loss = our CC destroyed):

- **Good** — win, with 0 JS errors.
- **Pass** — draw at the limit (survived, no loss).
- **Fail** — loss, or JS errors.

**Goal achieved when:** a 10-seed batch against sandbox Rome wins ≥ 8/10 seeds
with 0 JS errors. Record the batch in the closing commit and define G4 (defeat
medium, difficulty 3, Rome).

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
errors**. The validated change: attack at `SOLDIER_TARGET` (20) instead of at 15.

### G2 — Sustain a 32+ citizen-soldier army (achieved turn 008)

Vercingetorix fields and sustains a 32+ citizen-soldier army early enough to
attempt a civic-centre capture.

Grading (historical): **Good** — 32 melee soldiers reached by game-minute 12;
**Pass** — 28 by minute 12, or 32 by minute 16; **Fail** — otherwise or JS errors.

**Closing batch:** turn 008, seeds 71–80 vs sandbox Rome — **8/10 Good, 0 JS
errors** (9/10 reached 28 by minute 12). The validated change: raise
`SOLDIER_TARGET` to 32 and expand `HOUSE_OFFSETS` to 8 candidates so the bot
can actually build its 4 houses.

## Backlog of candidate goals (unrefined, for later)

- G4: defeat medium (difficulty 3) Rome.
- G5: town phase timing: reach Town Phase by minute X and City by minute Y.

## Reconsideration rule

If a goal resists several turns of effort, stop and reconsider: is it too
ambitious? Does it depend on another goal that should come first? Adjust the goal
here, with a note explaining why.
