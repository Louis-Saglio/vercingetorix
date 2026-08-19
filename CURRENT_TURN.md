# Current turn

- Number: 028 — G4 reconsideration + army scaling (G4a).
- Phase: five in-turn iterations + A/B diagnostic done → verdict bad (50
  soldiers by t22 unreachable: even the validated code peaks at 16 on these
  seeds) → reverted → committing (then turn 029: wood economy or re-scoped
  G4a).
- Standing instruction (Louis, 2026-08-19): keep doing turns until the
  context window is ~79% used.
- Standing instruction (Louis, 2026-08-19): each turn is exactly one commit —
  fold backlog and `CURRENT_TURN.md` bookkeeping into the turn commit; no
  separate backlog/closure commit.
- Standing instruction (Louis, 2026-08-19): bad/neutral → fix small
  understood causes in-turn and rerun; baseline = last validated experiment.

Last completed turn: 027 — concentrated-assault (bad; economy gap 18 vs 116
units → G4 split).
