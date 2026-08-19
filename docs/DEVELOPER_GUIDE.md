# Vercingetorix — Developer Guide

For the agents maintaining this project. Read this before touching anything.

## Architecture

```
vercingetorix/
├── PROTOCOL.md          # the development loop (canonical rules) — read first
├── CURRENT_TURN.md      # active turn + phase — the recovery entry point
├── turns/               # journal: NNN-slug.md per turn, backlog.md
├── experiments/NNN/     # raw results per turn: baseline.json, treatment.json, report.md
├── bot/                 # the 0 A.D. mod containing the Vercingetorix AI (JS)
├── harness/             # Rust match runner + report tool
└── docs/                # this guide + user guide
```

Data flow of an experiment:

```
harness run-batch ──spawns──▶ pyrogenesis (headless match)
                                   │  stdout: "Turn N (200)..." progress,
                                   │  end-of-game per-player statistics JSON,
                                   │  exit code (0 = finished)
                                   └─▶ match dir: stdout, logs, replay
harness report ──▶ experiments/NNN/{baseline,treatment}.json + report.md
```

## Environment (verified on this VPS, 2026-08)

- **Engine:** Pyrogenesis 0.28.0, installed system-wide via apt (`0ad` + `0ad-data`).
  Binary: `/usr/games/pyrogenesis`. Upstream online docs may lag behind this version.
- **Headless mode:** `-autostart-nonvisual` runs with no display, no GPU, no sound.
  The main loop feeds the turn manager one fixed 200 ms step per iteration, unpaced —
  the sim runs as fast as the CPU computes.
- **Speed:** measured ~65 turns/s solo (≈13x real-time), ~107 turns/s with
  `-autostart-speed=20` in observer mode (≈21.5x), ~200 turns/s when sharing 4 cores.
  Planning number: **~20x real-time per core**. `-autostart-speed` mostly does not
  matter in nonvisual mode (its rate is applied on the GUI frame path, not the
  nonvisual loop); treat it as optional.
- **Game end:** when the match finishes, the engine prints one JSON block per player
  (`playerID`, `playerState` "won"/"defeated", full `statistics` — see
  `StatisticsTracker.GetStatisticsJSON`), writes replay metadata, and exits with code 0.
  This is the primary data channel; parse stdout.
- **Logs:** `~/.local/state/0ad/log/` (0.28 moved them here from `~/.config/0ad/logs`).
  `mainlog_<epoch>_<pid>.html` and `interestinglog_<epoch>_<pid>.html` with
  `-unique-logs`. Bot `warn()`/`error()` calls land in the interesting log — this is
  the channel for bot-side `[HARNESS]` reporting lines.
- **Replays:** `~/.local/share/0ad/replays/0.28.0/<ts>_<seq>/`. The first line is the
  full match manifest (map, seed, PlayerData, victory conditions, mods). In AI-only
  nonvisual matches the replay contains **no per-turn command lines** — do not rely on
  it for timelines; use bot-side reporting instead.
- **User data isolation:** point `HOME` at a fresh dir per match. Never use `/tmp` for
  match homes or large extractions — it is a 3.8 GB tmpfs. Use disk-backed paths.
- **Reference data (version-pinned to the running engine):** `/home/ubuntu/0ad-reference/`
  — `public/` and `mod/` are the installed game data unpacked (0.28.0), and
  `source/` is a shallow clone of the engine source at tag `v0.28.0`
  (gitea.wildfiregames.com, commit a2cae4d6). Consult these before trusting any
  memory of how the game works — see also `docs/GAME.md` for the distilled rules.
- **Hardware:** 4 vCPU (virtual Haswell), 7.6 GiB RAM. Keep match parallelism ≤ 4;
  2-3 is comfortable.

## Bot mod

The bot is an in-engine JS AI, the standard 0 A.D. architecture (Petra is the reference
implementation):

- Mod folder: `bot/` with a `mod.json` (`name: "vercingetorix"`, depends on `0ad`).
- AI folder inside the mod: `simulation/ai/vercingetorix/` with a `data.json`
  (`"moduleName"`, `"constructor"`, `"useShared": true`) — the folder name is the AI id
  used in `-autostart-ai=1:vercingetorix`.
- Lifecycle (from `common-api/baseAI.js`, loaded with `Engine.IncludeModule("common-api")`):
  - `constructor(settings)` — once per player.
  - `Init(state, playerID, sharedAI)` — once; base class sets up `this.gameState` and
    calls your `CustomInit(gameState)`.
  - `HandleMessage(state, playerID, sharedAI)` — every sim turn; base class fills
    `this.events` and calls your `OnUpdate(sharedAI)`.
  - `Serialize()`/`Deserialize(data)` — must be implemented; savegames and determinism
    depend on it.
  - `this.chat(msg)` posts to the game log.
- The bot sees: `gameState` (own entities, players, map), `this.events` (attacks,
  construction finished, trainings, renames, defeats), and the shared
  territory/accessibility maps.
- The bot acts by posting commands (`Engine.PostCommand`) — the same JSON commands the
  GUI uses; `common-api/entity.js` wraps the common ones (`moveTo`, `gather`, `attack`,
  ...). Training/building/research go through the entity's `ProductionQueue`,
  `Builder`, `Researcher` components.
- Determinism is a hard requirement: same seed → identical behavior, always. See
  [PROTOCOL.md](../PROTOCOL.md) → Hard rules.

## Harness (Rust)

The harness is a small Rust CLI (Cargo toolchain is installed on this VPS) implementing
the runner command from `PROTOCOL.md` → Experiment specification:

- `harness --tag NAME --seeds 1,2,3 --out DIR [--ai1 ID] [--ai2 ID] [--difficulty2 N]
  [--civ1 C] [--civ2 C] [--map random/alpine_lakes] [--size 128] [--timeout 1200]
  [--mod NAME] [--mod-dir PATH]`
  — spawns one `pyrogenesis` per match with an isolated `HOME`, enforces the wall-clock
  cap via `timeout`, extracts per-player stats JSON + `[HARNESS]` lines + JS error count
  into one JSON per match plus a batch aggregate.
- `--mod-dir PATH` copies the bot mod into `<home>/.local/share/0ad/mods/<name>` before
  spawning (the mod name comes from the mod's `mod.json`), so `--mod NAME` resolves
  inside each isolated home.

Do not add features to the harness that a turn does not need.

## Commands

- One match: see `docs/USER_GUIDE.md` → Running a match yourself.
- Reference extraction of the public mod: already done at `/home/ubuntu/0ad-poc/public/`.
- Determinism check: run the same seed twice, diff the stats JSON blocks — must be byte-identical.

## Conventions

- One commit per turn, message `turn NNN: <slug> — <verdict>`, body = journal summary.
- Turn files use the fixed section template in `PROTOCOL.md`.
- Update `CHANGELOG.md` only for changes that survive validation (good verdicts) and
  for protocol/tooling changes.
- Update `CURRENT_TURN.md` at every phase change of the active turn.
