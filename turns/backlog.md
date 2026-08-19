# Hypothesis backlog

One line per candidate: the change, the primary metric, and the rationale.
Top of the list goes first. Fed by experiment results; never edit an entry
retroactively to match a verdict.

- G3: gather stone and metal (in addition to wood/food) so the bot can afford
  City Phase (750 stone + 750 metal); primary metric = stone/metal gathered.
- G3: research City Phase once stone ≥ 750 and metal ≥ 750; primary metric =
  City Phase reached.
- G3: build an arsenal in City Phase, then train a siege ram for crush damage
  against the CC; primary metric = win rate.
- G3: direct capture-allowed attack on the enemy CC with the 32-soldier army.
  (turn 009 — bad.)
- G3: target the enemy civic centre in the sweep. (turn 005 — bad.)
- **Prereq** — harness runner: spawn matched-pair batches (isolated HOMEs, seeds,
  timeout, stats extraction). Required before any experiment. (turn 001 — done)
- **Prereq** — bot skeleton: Vercingetorix mod that survives a full match vs sandbox
  Rome with zero JS errors. Produces the baseline numbers. (turn 002 — done)
- **Prereq** — report tool: paired baseline-vs-treatment diff applying the composite
  verdict rules (outcome + quality + survival, draws), plus the canary match check.
  (turn 003 — done; also pinned biome/placement and restored the canary gate)
- Evidence: report time-to-phase (town/city) and per-minute resource/army samples
  so the composite score has phase-timing metrics to use.
- Perf (refactor/optimization): replace the skeleton's per-tick full-map resource
  scan (`getEntities()` over all map entities in `play()`) with cached collections
  or the shared `resourceMaps`; behavior-preserving, judged by turn rate.

Turn 004 done (G1 achieved). Turn 005 bad. Turn 006 invalid. Turn 007 neutral.
Turn 008 done (G2 achieved). Turn 009 bad. Turn 010 bad. Turn 011 done
(save-for-town — good); Town Phase now reached.
