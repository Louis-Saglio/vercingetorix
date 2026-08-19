# Turn 015 — Reconsider G3

Goal served: protocol reconsideration rule (GOALS.md).

## Hypothesis

> If I re-analyze the five G3 turns (005, 009, 010, 012, 013), then I can
> decompose the blocked "defeat sandbox Rome" goal into a smaller, achievable
> prerequisite, because every failure shares the same root cause: the bot lacks
> the economic/siege capability to take a civic centre.

Primary metric: a clear, testable replacement goal with an objective grading
scale (qualitative — this is a goal-adjustment turn, not a bot experiment).

## Implementation

`docs/GOALS.md`: G3 is redefined as a resource prerequisite (gather 750 stone
and 750 metal by game-minute 16); the "defeat sandbox Rome" win goal moves to
the backlog as G4. `turns/backlog.md` is updated to match.

## Experiment

Re-analysis of existing results only (no new matches):

- Capture path: 32 spearmen sustain only ~22 capturers, too slow (turns 005, 009).
- Siege path: Town is now reachable (turn 011), but City needs 750 stone + 750
  metal; turn 012 gathered no stone and crippled the economy with a naive split.
- Bigger-army path: 40 soldiers is only intermittently reachable (turn 013).

The common prerequisite is reliable stone/metal income.

## Verdict

**Good** (reconsideration delivered): the blocked goal is split into a concrete,
testable prerequisite and the original win goal is preserved in the backlog.

## Action

Keep the goal adjustment. Commit as `turn 015: reconsider-g3 — good` and push.
`docs/CHANGELOG.md` gets an entry.

## Next

Pursue the new G3: gather 750 stone + 750 metal. This batch (turns 010–015) is
complete.
