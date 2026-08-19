# Current turn

- Number: 003 — report tool (see `turns/003-report-tool.md`).
- Phase: verdict **good**; RL machinery removed per Louis; final cleanup and
  commit + push next.

## What turn 003 turned into (summary)

- `harness report` (composite verdict scoring) implemented and validated:
  15 unit tests pass, self-comparison on the turn-002 baseline is
  all-zero/neutral.
- The live canary exposed nondeterminism, fully root-caused: **two unseeded
  gamesetup defaults** — the map biome and the player placement pattern
  (both `"random"`, resolved per run in the GUI realm's unseeded
  `Math.random`; the manifests showed `circle` vs `randomGroup` for the same
  seed). Fixed by pinning `-autostart-biome=generic/temperate` and
  `-autostart-placement=circle` in the harness. An intermediate pathfinder-
  race theory (and the RL-paced runner built for it) was refuted by the
  evidence and removed per Louis.
  Full report: `docs/ENGINE_BUG_0AD_0.28_NONDETERMINISM.md`.
- With the pins, the **unpaced canary passes** (seeds 5, 17, 19) — it is the
  per-batch determinism gate.
- Working tree uncommitted: `harness/src/report.rs` (new),
  `harness/src/main.rs` (report dispatch, biome and placement pins, `--speed`
  flag), `turns/003-report-tool.md`,
  `docs/ENGINE_BUG_0AD_0.28_NONDETERMINISM.md`, protocol/docs/changelog/
  AGENTS/USER_GUIDE updates, curated experiment data in `experiments/003/`.

Last completed turn: 002 — bot skeleton baseline (see `turns/002-bot-skeleton.md`).
