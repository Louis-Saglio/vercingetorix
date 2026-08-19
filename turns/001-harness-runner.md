# Turn 001 — Harness runner

## Hypothesis

Prerequisite turn (no bot change): the experiment loop cannot run without a runner.

Acceptance criteria, stated as a hypothesis:

> If the harness can spawn the exact protocol match command with isolated HOMEs,
> enforce the 20-minute cap, and extract per-player statistics JSON from stdout,
> then a petra-vs-petra batch of the same 2 seeds run twice will produce identical
> result sets on every deterministic field (player stats blocks, turn count, exit
> status, harness lines, JS error count), proving the runner is trustworthy.

Primary metric for verification: equality of the two runs on all fields except
wall-clock duration (inherently non-deterministic by design).

## Implementation

- Rust CLI `harness/` (Cargo), single flag-only binary.
- Std library + `serde_json` only. Sequential execution in v1 (parallelism deferred).
- Per match: isolated `HOME`, `timeout 1200` wrapper, captures stdout/stderr,
  extracts statistics JSON blocks, counts `[HARNESS]` lines from stdout and JS errors
  from the interesting log, records exit code, wall time, and turn count.
- Output: `experiments/001/<tag>/<seed>.json` per match + `experiments/001/<tag>.json`
  aggregate.

## Experiment

- Run `harness --tag control-a --seeds 42,777 --ai1 petra --ai2 petra` and the same
  command with `--tag control-b`, twice with the same working tree.
- Compare the two aggregates on all fields except `wall_seconds`.

## Verdict

Passed. The two batches are identical on every deterministic field (per-player
statistics blocks, turn counts, exit statuses, harness lines, JS error counts);
only wall-clock duration differs, as expected by design.

## Action

Committed as `turn 001: harness-runner — good`.

Observed match throughput: ~14000 turns in ~45 s solo (~300 turns/s, ~60x
real-time) — far above the planning number, so batch sizes can grow later if
needed.

## Next

Turn 002: bot skeleton baseline.
