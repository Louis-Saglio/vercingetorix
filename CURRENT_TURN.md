# Current turn

- Number: — (no active turn)
- Phase: **between turns**. Turn 004 (`food-first-allocation`) closed with
  verdict **good** (2026-08-20): 75/25 food/wood quota for idle gatherers;
  mean food gathered 4718 vs 2224 baseline (+112 %), consistent on all seeds;
  canary PASS; 0 JS errors; no turn-rate regression. Validated and published.
  (Composite −0.68 "neutral" by design: the hypothesis deliberately stops
  gathering stone/metal; the turn's pre-registered single-metric thresholds
  governed.)
- Next: turn 005 = backlog top — restore turn 003's house building (same
  design, same ≥ 6/10 reach-100 threshold).
- Baseline for turn 005: turn-004 validated code (= current HEAD).
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
