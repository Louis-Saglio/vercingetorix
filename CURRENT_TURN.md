# Current turn

- Number: — (no active turn)
- Phase: **between turns**. Turn 002 (`train-civilians`) closed with verdict
  **good** (2026-08-20): the civil centre trains workers continuously;
  20/20 population in 10/10 matches (median ≤ 2 game-min) vs never on the
  turn-001 baseline; composite +15.12; canary PASS; 0 JS errors. Validated
  and published.
- Next: turn 003 = backlog top — build houses when population headroom runs
  low (the binding constraint: economy idles at 20/20 from minute ~2).
- Reminder: experiments now run to the 20-game-minute limit.
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
