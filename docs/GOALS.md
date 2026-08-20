# Goals

Long-term goals that span multiple turns. Each turn grades its experiment against
the current goal's scale. When a goal is achieved, the next goal and its grading
system are defined in the closing commit.

## Current goal: G1 — Reach 100 population as fast as possible

**Statement:** Vercingetorix grows its population to **100** as fast as
possible. Purely economic goal: no combat, no phases beyond what the growth
requires. Population costs 1 per unit for the units the bot can mass (see
`docs/game_description/mechaniques/population_and_entity_limits.md`), so 100
population means ~100 units — and, since the civil centre provides only 20
population and each house 5, at least **16 houses**. The opponent is sandbox
Rome (Petra, difficulty 0), which does not interfere.

**Primary metric:** time to 100 population, in game-minutes, read from the
per-minute `[HARNESS]` samples (`pop` field). Lower is better; the batch
metric is the median over seeds.

**Grading per match:** no time band. A match yields its time-to-100; it is
**Fail** only if 100 is never reached before the match limit, the bot is
defeated, or there are JS errors.

**Goal achieved when:** the time cannot be pushed lower — operationally,
when **5 consecutive turns** fail to beat the best batch median achieved so
far. The backlog is then free to move to the next goal.

## Backlog goal: G2 — Reach City phase and 300 population as fast as possible

**Statement:** Vercingetorix researches the **City phase** (`currentPhase()
>= 3` — the sim's truth, not a bot flag) **and** grows its population to
**300** (the per-player population cap used in experiments), as fast as possible. This is the
economic ceiling of the game: City requires Town first, the 750 stone / 750
metal research cost and 3 Town-class structures; 300 population requires
the houses to support it (civil centre 20 + 5 per house) on top of the
units themselves. See
`docs/game_description/mechaniques/technologies_and_modifiers.md` (phases)
and `population_and_entity_limits.md`. Same opponent: sandbox Rome.

**Primary metric:** time until both conditions hold, in game-minutes, from
the `[HARNESS]` samples (`pop` field) and `currentPhase()` (add it to the
samples when this goal becomes active). Batch metric: median over seeds.

**Grading per match:** no time band. **Fail** only if the match limit is
reached first, the bot is defeated, or there are JS errors.

**Goal achieved when:** **5 consecutive turns** fail to beat the best batch
median achieved so far.


## Reconsideration rule

If a goal resists several turns of effort, stop and reconsider: is it too
ambitious? Does it depend on another goal that should come first? Adjust the goal
here, with a note explaining why.
