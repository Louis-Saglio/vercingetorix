# Current turn

- Number: — (no active turn)
- Phase: **between turns**. Turn 003 (`build-houses`) closed with verdict
  **neutral** (2026-08-20): housing works (pop limit rose 10/10, composite
  +14.90, canary PASS, 0 JS errors after one in-turn veto fix) but 100 pop
  was reached 0/10 — food income, not housing, is the binding constraint.
  Code reverted per rule 7 (preserved in the turn commit); no zip published.
- Next: turn 004 = backlog top — allocate gatherers by need (food first).
- Baseline for turn 004: turn-002 validated code (= current HEAD).
- Reminder: experiments run to the 20-game-minute limit.
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
