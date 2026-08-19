# Hypothesis backlog

One line per candidate: the change, the primary metric, and the rationale.
Top of the list goes first. Fed by experiment results; never edit an entry
retroactively to match a verdict.

- G2 (reconsider): three G2 turns produced no wins (005 bad, 006 invalid, 007
  neutral). Consider decomposing G2 into a "sustain a 32+ soldier army"
  prerequisite before re-attempting CC capture, or pivot to the siege path
  (Town → City phase → arsenal → rams).
- G2: grow the army and its housing together — raise `SOLDIER_TARGET` and
  `HOUSE_TARGET` so the cap can hold the target, then attack. (turn 007 tested
  `SOLDIER_TARGET=27` with the old sweep — neutral, 0 wins: a bigger army alone
  never focuses the CC.)
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
(target-enemy-civic-centre — bad). Turn 006 done (bigger-army — invalid).
Turn 007 done (reachable-bigger-army — neutral); G2 still open.
