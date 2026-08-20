# Current turn

- Number: — (no active turn)
- Phase: **fresh start**. All pre-`game_description` turns and experiments
  were deleted (2026-08-20, Louis's decision: they predated the game
  reference and did not progress correctly). The bot is the do-nothing
  baseline with observability kept. The next turn is a new turn 001,
  designed from `docs/game_description/`.

Standing instructions (Louis, 2026-08-20):

- After each **validated** turn, publish the bot mod zip on the file server
  (https://files.louissaglio.fr/vercingetorix.zip).
- Each turn is exactly one commit — fold backlog and `CURRENT_TURN.md`
  bookkeeping into the turn commit.
- Bad/neutral → fix small understood causes in-turn and rerun; baseline =
  last validated experiment.
