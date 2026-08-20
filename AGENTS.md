# AGENTS.md — Vercingetorix

Agent instructions for this repository. Read before acting.

## Read first
- `docs/GOALS.md` — the goals the bot needs to achieve in increasing difficulty order.
- `docs/game_description/` — the full game reference: `mechaniques/` (one
  file per game mechanic, verified against the source with citations) and
  per-entity data (`generic/`, `gauls/`, `romans/`: units, buildings,
  technologies, auras, each with a bot-oriented Guide section). Consult it
  before writing bot logic; keep it correct when the game data is re-explored.
- `docs/DEVELOPER_GUIDE.md` — environment, architecture, the AI API reference
  (verified), and maintenance.

## Hard facts

- The repo is public on GitHub: https://github.com/Louis-Saglio/vercingetorix.
  **Push after every commit** (`git push`).
- Engine, game data and source are version-pinned in `/home/ubuntu/0ad-reference/`
  (0.28.0); the harness runs `/usr/games/pyrogenesis` headless.
- Experiments: gaul (bot) vs rome (Petra), `random/mainland` 192 ("Small"),
  victory `conquest_civic_centers`, treasures disabled, population cap 300
  per player (both pinned by the bot mod's autostart override), 20
  game-minutes limit (tunable),
  per-turn seed rotation with paired baseline/treatment and a canary match
  (same seed twice must be identical — the determinism gate). Biome and
  player placement are pinned (`generic/temperate`, `circle` — the gamesetup
  defaults are unseeded `"random"` for both; see
  `docs/ENGINE_BUG_0AD_0.28_NONDETERMINISM.md`).
- Never run matches with HOMEs on `/tmp` (small tmpfs); the harness isolates
  HOMEs under `experiments/<turn>/homes/`.
- **AI performance is a hard constraint**: the bot must not slow down the
  simulation. No full-map scans per tick; prefer cached collections and the
  shared resource maps.
