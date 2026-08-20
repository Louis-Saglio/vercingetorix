# Current turn

- Number: — (no active turn)
- Phase: turn 007 (`parallel-house-construction`) closed with verdict
  **neutral** (2026-08-20): median time-to-100 12.5 vs 12.5 paired baseline;
  the change works (fewer at-cap minutes) but food income — not the
  population cap — is the binding constraint. Reverted. Next: turn 008,
  food-gatherer share (backlog top).

Standing instructions (Louis, 2026-08-20):

- After each **validated** turn, publish the bot mod zip on the file server
  (https://files.louissaglio.fr/vercingetorix.zip).
- Each turn is exactly one commit — fold backlog and `CURRENT_TURN.md`
  bookkeeping into the turn commit.
- Bad/neutral → fix small understood causes in-turn and rerun; baseline =
  last validated experiment.
- 2026-08-20: Louis asked to resume defining and implementing turns
  (overrides the earlier "stop after turn 006" instruction).

State for the next session: baseline = turn-006 validated code (HEAD); G1
best batch median to beat: **11 game-min**; consecutive turns without
beating it: **1**; backlog top = raise the food-gatherer share.
