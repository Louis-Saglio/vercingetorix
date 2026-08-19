# Current turn

- Number: none active — turn 024 closed (bad, reverted). Protocol updated with
  Louis's feedback (see below). Next: turn 025 under G4, resuming per the
  standing context-window instruction.

Standing instructions (Louis, 2026-08-19):

- Keep doing turns without stopping for go-ahead until the context window is
  ~79% used.
- Each turn is exactly one commit — fold backlog and `CURRENT_TURN.md`
  bookkeeping into the turn commit; no separate backlog/closure commit.
- **Bad/neutral verdicts: if the cause is understood and the fix is small,
  fix it in the same turn and rerun the experiment (iterate as needed; stop
  the turn if it stops converging).**
- **Baseline = results of the last validated experiment** (run once per turn
  on the turn's seeds, reused across in-turn iterations).
- These two rules are codified in `docs/PROTOCOL.md` (committed 2026-08-19).

Last completed turn: 024 — arsenal-ram-attack (bad; foundation-train JS
errors + metal starvation).
