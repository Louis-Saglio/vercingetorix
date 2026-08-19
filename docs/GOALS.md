# Goals

Long-term goals that span multiple turns. Each turn grades its experiment against
the current goal's scale. When a goal is achieved, the next goal and its grading
system are defined in the closing commit.

## Current goal: G4 — Defeat sandbox Rome

**Statement:** Vercingetorix destroys the enemy civic centre (the
`conquest_civic_centers` victory condition) against sandbox Rome (Petra,
difficulty 0), which does not expand or attack, before the **25-game-minute**
match limit (raised from 20 on turn 022's evidence: City Phase lands at
minute 17–19 on the seeds where the forge prerequisites build, so the
arsenal → ram → march → CC kill cannot fit inside 20 minutes).

**Grading per match:**

- **Good** — win: the enemy CC is destroyed before the limit.
- **Fail** — otherwise (draw at the limit, own CC lost), or JS errors.

**Goal achieved when:** a 10-seed batch against sandbox Rome wins on ≥ 8/10
seeds with 0 JS errors and canary PASS. Record the batch in the closing commit
and move on to G5.

## Completed goals

### G1 — Economy boot (achieved turn 004)

20 citizen soldiers by game-minute 8/12/16 and growth (see turn 004). Closing
batch: seeds 21–30, 10/10 Good, 0 JS errors.

### G2 — Sustain a 32+ citizen-soldier army (achieved turn 008)

32 melee soldiers by game-minute 12. Closing batch: seeds 71–80, 8/10 Good,
0 JS errors.

### G3 — Gather 750 stone and 750 metal (achieved turn 017)

≥ 750 stone AND ≥ 750 metal in stock by game-minute 16 (the City Phase cost;
the bot starts at 300/300, so this is ≥ 450 net gathered of each), without
collapsing the wood/food economy. Closing batch: turn 017's treatment, seeds
151–160 vs sandbox Rome, 10/10 Good, 0 JS errors, canary PASS. Mechanism: the
four starting support workers gather stone/metal from minute 0, plus a
post-town army carve-out (id % 16: 3/16 stone, 2/16 metal), attack deferred
until 750/750 are banked.

## Backlog of candidate goals (unrefined, for later)

- G5: defeat medium (difficulty 3) Rome.
- G6: town phase timing: reach Town Phase by minute X and City by minute Y.

## Reconsideration rule

If a goal resists several turns of effort, stop and reconsider: is it too
ambitious? Does it depend on another goal that should come first? Adjust the goal
here, with a note explaining why.

## Reconsideration note (turn 015)

"Defeat sandbox Rome" (formerly G3) resisted five turns (005, 009, 010, 012,
013). It was split: the resource prerequisite became G3 (achieved turn 017) and
the win goal is now G4.

## Evidence correction (turn 018)

Turn 011's "Town Phase reached 10/10" measured the bot's own `townResearched`
flag, which the bot sets when it *posts* the research — not sim truth. The sim
rejects the Town research because it requires 5 Village-class structures and
the bot has 0–4 houses at post time (`classCounts["Village"]` tracks the
houses exactly). `gameState.currentPhase()` stays 1 all match. G3's
stone/metal gathering is unaffected (real resources, gated on the bot flag),
but all phase-gated claims must use `currentPhase()`/`isResearched` from now
on.
