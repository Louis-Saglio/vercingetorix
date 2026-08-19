# Hypothesis backlog

One line per candidate: the change, the primary metric, and the rationale.
Top of the list goes first. Fed by experiment results; never edit an entry
retroactively to match a verdict.

- **Prereq** — harness runner: spawn matched-pair batches (isolated HOMEs, seeds,
  timeout, stats extraction). Required before any experiment. (turn 001 — done)
- **Prereq** — bot skeleton: Vercingetorix mod that survives a full match vs sandbox
  Rome with zero JS errors. Produces the baseline numbers. (turn 002 — in progress)
- **Prereq** — report tool: paired baseline-vs-treatment diff applying the composite
  verdict rules (outcome + quality + survival, draws), plus the canary match check.
  (turn 003 — done; also pinned biome/placement and restored the canary gate)
- Evidence: report time-to-phase (town/city) and per-minute resource/army samples
  so the composite score has phase-timing metrics to use.
- Perf (refactor/optimization): replace the skeleton's per-tick full-map resource
  scan (`getEntities()` over all map entities in `play()`) with cached collections
  or the shared `resourceMaps`; behavior-preserving, judged by turn rate.

Real hypotheses start at turn 004 and are derived from the baseline results of turn 002.
