# Hypothesis backlog

One line per candidate: the change, the primary metric, and the rationale.
Top of the list goes first. Fed by experiment results; never edit an entry
retroactively to match a verdict.

- **Prereq** — harness runner: spawn matched-pair batches (isolated HOMEs, seeds,
  timeout, stats extraction). Required before any experiment. (turn 001)
- **Prereq** — bot skeleton: Vercingetorix mod that survives a full match vs sandbox
  Petra with zero JS errors. Produces the baseline numbers. (turn 002)
- **Prereq** — report tool: paired baseline-vs-treatment diff applying the verdict
  rules. (turn 003)

Real hypotheses start at turn 004 and are derived from the baseline results of turn 002.
