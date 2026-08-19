# Hypothesis backlog

One line per candidate: the change, the primary metric, and the rationale.
Top of the list goes first. Fed by experiment results; never edit an entry
retroactively to match a verdict.

- G2: grow the army and its housing together — raise `SOLDIER_TARGET` and
  `HOUSE_TARGET` so the population cap can actually hold the target, then
  attack; primary metric = win rate vs sandbox Rome (G2). (turn 006 was
  invalid: raising only `SOLDIER_TARGET` to 32 stalls at 28 melee / pop 35 /
  3 houses and never attacks.)
- G2: advance to Town Phase and build siege (rams) for crush damage against the
  CC; primary metric = win rate vs sandbox Rome.
- G2: target the enemy civic centre in the sweep; primary metric = time to
  destroy the enemy CC. (turn 005 — bad: a lone spearman capture is out-paced
  by the CC garrison, and it discards the baseline sweep's incidental kills.)
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

Turn 004 done (grow-to-20-before-attack — good); G1 achieved. Turn 005 done
(target-enemy-civic-centre — bad). Turn 006 done (bigger-army — invalid);
G2 still open.
