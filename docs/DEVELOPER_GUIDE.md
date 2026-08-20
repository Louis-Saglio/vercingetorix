# Vercingetorix — Developer Guide

For the agents maintaining this project. Read this before touching anything.

## Architecture

```
vercingetorix/
├── PROTOCOL.md          # the development loop (canonical rules) — read first
├── GOALS.md             # current long-term goal + grading scale
├── CHANGELOG.md         # curated change history
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
  [PROTOCOL.md](PROTOCOL.md) → Hard rules.

Before writing bot logic against a game rule or an entity's stats, consult
[game_description](game_description/README.md): `mechaniques/` explains how the
simulation works (verified against the source), and `generic/` + `gauls/` +
`romans/` give per-entity stats and bot-oriented guides.

## AI API reference (verified against 0.28.0)

The bot runs in the AI realm, a separate JS realm from the simulation. It has
**no** direct `Engine.QueryInterface` on the sim; everything goes through the
`common-api` wrappers (`gameState`, `Entity`, collections) and
`Engine.PostCommand`.

- **Registration:** `simulation/ai/<name>/data.json` with `"filename"` (the ES
  module file) and `"constructor"` (the exported function). `"useShared": true`
  loads `common-api`. The folder name is the AI id for `-autostart-ai=1:<name>`.
- **Lifecycle:** `constructor(settings)` → `Init(state, playerID, sharedAI)` (base
  class sets `this.gameState`, `this.territoryMap` — raw map data, not an InfoMap
  — then calls `CustomInit(gameState)`) → `HandleMessage(state, playerID, sharedAI)`
  every turn (base class fills `this.events`, calls `OnUpdate(sharedAI)`; it also
  **reassigns `this.territoryMap` every turn** — never store wrappers in it).
  `Serialize()`/`Deserialize(data)` for savegames.
- **Events** (`this.events`, from `state.events` in `shared.js`): `Create`,
  `EntityRenamed`, `TrainingFinished`, `ConstructionFinished`, `AIMetadata`,
  `Destroy`, plus `PlayerDefeated`/`TributeExchanged` from `AIInterface.js`
  handlers.
- **Collections:** `EntityCollection.filter(f)` is eager; `.length` works;
  **`.values()` returns an iterator** — no `.slice()`, no indexing; use `for..of`
  or `.next().value`.
- **Templates:** `gameState.getTemplate(name)` returns a `Template` wrapper —
  read fields with `.get("Cost/Resources/wood")`, not `.Cost...`. Raw data is in
  `._template`. `gameState.applyCiv("units/{civ}/...")` resolves `{civ}`;
  **trainer tokens use a slash** (`units/{civ}/infantry_spearman_b`), the older
  underscore form is wrong.
- **Entities:** `ent.position()` — **`[x, z]` 2-element array** in meters (from
  `AIProxy.js`: `position = [msg.x, msg.z]`; there is no y/height element), may
  be `undefined` mid-destruction — guard it), `ent.owner()`, `ent.id()`, `ent.hasClass(c)` (Classes +
  VisibleClasses merged), `ent.getResourceType()` ("wood"/"food"/... from
  ResourceSupply/Type — trees have **no Identity classes**), `ent.buildableEntities(civ)`,
  `ent.trainingQueue()`, `ent.unitAIState()` (e.g. `"INDIVIDUAL.IDLE"`,
  `"INDIVIDUAL.GATHER.GATHERING"`; `undefined` for structures).
- **Actions:** `ent.train(civ, template, count)`, `ent.construct(template, x, z,
  angle)` — **places the foundation only** (posts `autorepair:false`); follow with
  `ent.repair(foundationEntity)` to actually build it. `ent.gather(target)`,
  `ent.attack(targetId)`, `ent.attackMove(x, z, targetClasses)`.
- **Reporting:** `print(...)` does **not** append newlines; the bot's `hlog`
  helper appends `"\n"`. `[HARNESS]` lines go to stdout and are extracted by the
  harness. `this.chat(msg)` posts to the game chat.
- **AIs see everything** (full map knowledge, enemy stats); gaia entities have
  owner 0. `gameState.getPopulation()` / `getPopulationLimit()`; CC gives 20 pop,
  houses 5.
- **Phase research is sim-gated, not bot-gated.** Posting `cc.research("phase_town*")`
  does not advance the phase unless the sim's requirements are met: Town needs
  **5 Village-class structures** (houses are Village; `playerData.classCounts["Village"]`
  counts them), City needs **3 Town-class structures** (forge, market, tavern have
  class Town) plus the resources. The sim silently rejects unmet research —
  nothing is paid, nothing is logged. **Ground truth is
  `gameState.currentPhase()` / `gameState.isResearched(tech)`, never a bot-side
  flag.** (Turn 011–017 ran on a bot flag that the sim had rejected since turn
  011; caught in turn 018 by logging `currentPhase()`.)
- **Mod loading:** any `-mod=` flag disables the public mod — the harness always
  passes `-mod=public -mod=<botmod>`. Mod files override public files at the same
  path (the bot mod overrides `maps/scripts/NonVisualTrigger.js` and
  `autostart/cmd_line_args.js` this way).

## Harness (Rust)

The harness is a small Rust CLI (Cargo toolchain is installed on this VPS) implementing
the runner command from `PROTOCOL.md` → Experiment specification:

- `harness --tag NAME --seeds 1,2,3 --out DIR [--ai1 ID] [--ai2 ID] [--difficulty2 N]
  [--civ1 C] [--civ2 C] [--map random/alpine_lakes] [--size 192] [--timeout 1200]
  [--speed N] [--mod NAME] [--mod-dir PATH]`
  — spawns one `pyrogenesis` per match with an isolated `HOME`, enforces the wall-clock
  cap via `timeout`, extracts per-player stats JSON + `[HARNESS]` lines + JS error count
  into one JSON per match plus a batch aggregate. Always passes
  `-autostart-biome=generic/temperate` and `-autostart-placement=circle` (the
  autostart defaults are `"random"` for both, drawn from the GUI realm's
  unseeded `Math.random` per run — unpinned, no run reproduces at all).
- `--mod-dir PATH` copies the bot mod into `<home>/.local/share/0ad/mods/<name>` before
  spawning (the mod name comes from the mod's `mod.json`), so `--mod NAME` resolves
  inside each isolated home.
- `harness report --baseline B.json [--treatment T.json] [--canary C.json] [--out DIR]`
  — the protocol's verdict machinery: paired composite score (outcome + quality +
  survival, draw semantics), JS-error veto, canary identity check, writes `report.md`
  and a compact summary. See `PROTOCOL.md` → Verdict rules.

Do not add features to the harness that a turn does not need.

## Commands

- One match: see `docs/USER_GUIDE.md` → Running a match yourself.
- Reference extraction of the public mod: already done at `/home/ubuntu/0ad-poc/public/`.
- Determinism check: the per-batch canary — same seed twice, stats JSON blocks
  must be byte-identical. Holds because the harness pins biome and player
  placement (`docs/ENGINE_BUG_0AD_0.28_NONDETERMINISM.md`).

## Performance guidance

The AI must not slow the simulation down (protocol hard rule 9). Known costs and
the cheap alternatives, all verified in 0.28:

- **Full-map scans are the main hazard.** `gameState.getEntities()` holds every
  entity (thousands of trees on mainland). Iterating it every play tick to build
  resource lists is expensive — the skeleton currently does exactly this and it is
  the first optimization candidate. Alternatives: `updatingCollection(name,
  filter, base)` (auto-maintained caches), the shared resource maps
  (`sharedAI.resourceMaps`, density InfoMaps per type), or filtering once and
  caching per tick.
- **Collections are cheap, filters are eager.** `.filter()` walks the source
  every call; `updatingCollection`/`updatingGlobalCollection` keep results
  maintained across turns — prefer them for anything queried repeatedly.
- **`Template.get(path)` caches lookups** per template — safe to call repeatedly.
- **Distance math is O(n) over the filtered set** — keep sets small (radius caps)
  and reuse results within a tick.
- **The 8-turn play throttle already bounds decision cost**; keep heavy work
  inside `play()` and keep per-turn work (reporting, event collection) trivial.
- **Measuring:** the match result records `turns` and `wall_seconds`; the turn
  rate must stay close to the baseline (~300-900 turns/s on this VPS). A material
  drop means the bot is burning CPU.

## Conventions

- One commit per turn, message `turn NNN: <slug> — <verdict>`, body = journal summary.
  The single commit includes the turn record, `turns/backlog.md`, `CURRENT_TURN.md`,
  and any `docs/` updates and experiment results — no separate backlog/closure commit.
- **Push after every commit** to https://github.com/Louis-Saglio/vercingetorix
  (remote `origin`, branch `main`).
- The bot mod ships `bot/maps/scripts/NonVisualTrigger.js`, which overrides the
  engine's script: it ends the match at the game-time limit (default 20 game-min)
  by marking all active players won, which prints the statistics and quits cleanly.
  The report tool reads "all players won at the limit" as a draw.
- Turn files use the fixed section template in `PROTOCOL.md`.
- Update `CHANGELOG.md` only for changes that survive validation (good verdicts) and
  for protocol/tooling changes.
- Update `CURRENT_TURN.md` at every phase change of the active turn.
- Maintain reusable evidence-exploration tools; never parse raw experiment JSON by
  hand in agent context.
