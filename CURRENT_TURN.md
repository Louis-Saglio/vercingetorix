# Current turn

- Number: — (no active turn)
- Phase: **STOPPED**. Turn 006 (`parallel-training`) closed with verdict
  **good** (2026-08-20): Fertility Festival researched at minute ~2, houses
  train civilians in parallel — median time-to-100 **11 game-min** vs 13
  baseline (10/10 both sides, canary PASS, 0 JS errors). Validated and
  published.

Standing instructions (Louis, 2026-08-20):

- **Stop after turn 006 — do not start new turns automatically.** Resume
  only on Louis's explicit request.
- After each **validated** turn, publish the bot mod zip on the file server
  (https://files.louissaglio.fr/vercingetorix.zip).
- Each turn is exactly one commit — fold backlog and `CURRENT_TURN.md`
  bookkeeping into the turn commit.
- Bad/neutral → fix small understood causes in-turn and rerun; baseline =
  last validated experiment.

State for the next session: baseline = turn-006 validated code (HEAD); G1
best batch median to beat: **11 game-min**; backlog top = parallel house
construction.
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
