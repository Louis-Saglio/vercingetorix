# Current turn

- Number: — (no active turn)
- Phase: **between turns**. Turn 001 (`gather-starting-workers`) closed with
  verdict **good** (2026-08-20): the 9 starting units gather from game-minute
  1; batch mean resourcesGathered 6709 vs 0 baseline; canary PASS; no JS
  errors. Validated and published.
- Post-turn reflection items pending (separate commit before turn 002):
  harness verdict float-boundary bug (0.4×10 < 4.0 → "neutral" at exactly
  +4.00); trigger `TIME_LIMIT_MS` is 30 min while comment/protocol say 20.
- Next: turn 002 = backlog top — train civilians at the civil centre.
- Baseline for the next turn: turn 001's validated code and
  `experiments/001/baseline.json` is stale for it — the next turn runs a
  fresh baseline of the validated code on its own seeds.

Standing instructions (Louis, 2026-08-20):

- After each **validated** turn, publish the bot mod zip on the file server
  (https://files.louissaglio.fr/vercingetorix.zip).
- Each turn is exactly one commit — fold backlog and `CURRENT_TURN.md`
  bookkeeping into the turn commit.
- Bad/neutral → fix small understood causes in-turn and rerun; baseline =
  last validated experiment.
