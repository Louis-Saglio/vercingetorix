# AGENTS.md — Vercingetorix

Agent instructions for this repository. Read before acting.

## Read first

- `docs/PROTOCOL.md` — the development loop. All work happens in turns:
  hypothesis → implement → experiment → verdict → action → commit + push.
  No work outside the protocol.
- `CURRENT_TURN.md` — the active turn and its phase; the recovery entry point
  after any session break. If it says STOPPED, do not start new turns.
- `docs/GOALS.md` — the current long-term goal and its grading scale.
- `docs/GAME.md` — the game mechanics reference. Grounded in the installed
  0 A.D. 0.28.0 data. **Grow this file every time game files are explored;
  everything in it must stay correct.**
- `docs/DEVELOPER_GUIDE.md` — environment, architecture, the AI API reference
  (verified), and maintenance.
- `docs/USER_GUIDE.md` — for Louis.
- `docs/CHANGELOG.md` — curated change history (append-only).
- `turns/backlog.md` — candidate hypotheses.

## Hard facts

- The repo is public on GitHub: https://github.com/Louis-Saglio/vercingetorix.
  **Push after every commit** (`git push`).
- Engine, game data and source are version-pinned in `/home/ubuntu/0ad-reference/`
  (0.28.0); the harness runs `/usr/games/pyrogenesis` headless.
- Experiments: gaul (bot) vs rome (Petra), `random/mainland` 128, victory
  `conquest_civic_centers`, treasures disabled, 20 game-minutes limit (tunable),
  per-turn seed rotation with paired baseline/treatment and a canary match
  (same seed twice must be identical — the determinism gate). Biome and
  player placement are pinned (`generic/temperate`, `circle` — the gamesetup
  defaults are unseeded `"random"` for both; see
  `docs/ENGINE_BUG_0AD_0.28_NONDETERMINISM.md`).
- Never run matches with HOMEs on `/tmp` (small tmpfs); the harness isolates
  HOMEs under `experiments/<turn>/homes/`.
- Louis's standing instructions override the protocol (e.g. "stop after turn N",
  "don't start turns automatically"). Record such instructions in
  `CURRENT_TURN.md`.
- **AI performance is a hard constraint**: the bot must not slow down the
  simulation. No full-map scans per tick; prefer cached collections and the
  shared resource maps. See `docs/PROTOCOL.md` rule 9 and
  `docs/DEVELOPER_GUIDE.md` → Performance guidance.
