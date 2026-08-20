# Current turn

- Number: — (no active turn)
- Phase: **STOPPED**. Turn 008 (`food-share-90`) closed with verdict
  **neutral** (2026-08-20): median time-to-100 13.0 vs 12.0 paired baseline
  (worse on 7 of 10 seeds) — food income is walk-distance-bound, not
  share-bound; reverted. Louis's instruction: stop after turn 008.

Standing instructions (Louis, 2026-08-20):

- **Stop after turn 008 — do not start new turns automatically.** Resume
  only on Louis's explicit request.
- After each **validated** turn, publish the bot mod zip on the file server
  (https://files.louissaglio.fr/vercingetorix.zip).
- Each turn is exactly one commit — fold backlog and `CURRENT_TURN.md`
  bookkeeping into the turn commit.
- Bad/neutral → fix small understood causes in-turn and rerun; baseline =
  last validated experiment.

State for the next session: baseline = turn-006 validated code (HEAD); G1
best batch median to beat: **11 game-min**; consecutive turns without
beating it: **2**; backlog top = farm fields next to the civil centre
(food rate is walk-distance-bound).
