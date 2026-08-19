# Hypothesis backlog

One line per candidate: the change, the primary metric, and the rationale.
Top of the list goes first. Fed by experiment results; never edit an entry
retroactively to match a verdict.

- G3 (reconsider): the capture path is refuted at 32 soldiers, and the siege
  path's first step (Town research) fails because the bot spends all resources
  on soldiers instead of saving for phase techs. Next: make the bot save
  food/wood for Town research before massing soldiers, or pick another path.
- G3: save food/wood for `phase_town_generic` before massing soldiers; primary
  metric = Town phase reached. (turn 010 — bad: "research when spare" fired on
  only 1/10 seeds.)
- G3: advance to Town Phase, then City Phase, build an arsenal, and train a
  siege ram for crush damage against the CC; primary metric = win rate.
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
Turn 008 done (G2 achieved). Turn 009 bad. Turn 010 bad; G3 still open.
