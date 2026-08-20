# Current turn

- Number: — (no active turn)
- Phase: **between turns**. Turn 005 (`build-houses-redux`) closed with
  verdict **good** (2026-08-20): house building restored on top of food-first
  allocation — **100 pop reached in 10/10 matches, median 13 game-min**
  (G1's first non-Fail batch; best median to beat: 13). Composite +14.79,
  canary PASS, 0 JS errors. Validated and published. Turn 003's journal
  erratum recorded (reverted code had not been committed; re-written here).
- Performance watch: treatment wall ~30 s vs baseline ~17 s per 6000-turn
  match — entity-count-driven sim cost, not AI decision cost; monitored per
  rule 9, no action yet.
- Next: turn 006 = backlog top — parallel training via houses (Fertility
  Festival tech + house training), target median ≤ 11 min.
- Baseline for turn 006: turn-005 validated code (= current HEAD).
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
