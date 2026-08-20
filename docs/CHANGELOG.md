# Changelog

## Unreleased

- Experiments: map size changed from Tiny (128) to **Small (192)** (harness
  default `--size`, `random/mainland`), and the **300 per-player population
  cap** is now pinned by the bot mod's autostart override
  (`settings.population.setPopCapType("player") + setPopCap(300)`, next to
  the existing DisableTreasures pin). Verified in a smoke match: replay
  metadata shows `"PopulationCapType":"player","PopulationCap":300`, map 192,
  0 JS errors. Docs updated (PROTOCOL, GAME, GOALS, USER_GUIDE,
  DEVELOPER_GUIDE, AGENTS.md).

- Goals: `docs/GOALS.md` reset — all pre-`game_description` goals (G1–G4,
  their history and reconsideration notes) deleted. New first goal: **G1 —
  reach 100 population as fast as possible** (purely economic; primary
  metric = time to 100 pop from the `[HARNESS]` samples, batch median; no
  time band — the goal is achieved when 5 consecutive turns fail to beat
  the best time achieved so far). Backlog goal **G2 — reach City phase and
  300 population as fast as possible** (same convergence rule).

- Reset: all pre-`game_description` turns and experiments deleted (they
  predated the game reference and did not progress correctly). `turns/` keeps
  only an emptied `backlog.md`; `CURRENT_TURN.md` marks a fresh start (next
  turn is a new turn 001 designed from `docs/game_description/`).
  `docs/ENGINE_BUG_0AD_0.28_NONDETERMINISM.md` still cites
  `experiments/003/` probe files — those are gone with the reset; the bug
  analysis itself stands.
- Bot: `vercingetorix.js` is again a do-nothing baseline (no orders issued).
  The observability used by the harness is kept: per-minute `[HARNESS]`
  sample lines (time, resources, pop, unit-state histogram — the report
  tool reads `pop`) and the final `end` event. The infrastructure mod files
  (autostart override, NonVisualTrigger time limit + statistics dump) are
  unchanged.
- Docs: `docs/GAME.md` citations that pointed at deleted turn journals now
  point at the `game_description` references.

- Documentation: `docs/game_description/` is now indexed and referenced from
  every entry point — new top-level `docs/game_description/README.md` (layout,
  how to use it when writing bot code, regeneration warning), and pointers in
  the root `README.md`, `AGENTS.md` (Read first), `docs/GAME.md` (Where to
  look, restructured docs-first) and `docs/DEVELOPER_GUIDE.md` (Bot mod).
  `tools/README.md` warns that regenerating entity docs overwrites the
  handwritten Guide sections.

- Documentation: Guide sections revised after review — ConquestCritical /
  defeat-condition references removed from all guides; costs are now framed by
  resource scarcity (food/wood abundant → easy to mass; stone/metal scarce →
  premium, hard to mass); the spearman guide notes it is the basic melee
  infantry of 13/15 civs (all but mace/ptol); the pikeman guide reframed as a
  frontline holder (armor 5/5, 8 m reach for multi-rank fighting, slow, low
  damage rate); the archer/slinger/javelineer guides now state the
  range↔damage tradeoff (60 m/7.2, 45 m/11.5, 30 m/16), the walk-speed
  ordering (javelineer fastest → best gatherer/harasser), and the slinger's
  stone cost as a massing constraint.

- Documentation: every unit and building file in `docs/game_description/`
  (generic + gauls + romans, 82 files) now opens with a "Guide" section: what
  the entity is for and its role in the game, from a bot's perspective,
  grounded in the file's documented stats and the source templates.

- Documentation: added `docs/game_description/mechaniques/` — one file per game
  mechanic (17 files + index), all verified against the 0.28.0 sources with
  inline `path:line` citations: resources/gathering, construction, training
  queues, population/entity limits, combat/damage formula, capture,
  promotion/XP, territory, technologies/modifiers, auras, vision/fog of war,
  garrisoning, healing/repair, trade/barter, loot/treasures,
  victory/diplomacy, orders/simulation time. Aimed at an agent implementing a
  bot. `docs/GAME.md` points to it.
- Documentation: the two analysis scripts that generated the
  `docs/game_description/` references are now versioned in `tools/`
  (`analyze.py` for generic units, `buildings.py` for generic buildings, with
  a short usage README); their output goes to `tools/out/` (gitignored).
- Documentation: added aura references — `docs/game_description/generic/auras/`
  (9 generic auras: ram_garrison, hero_garrison, temple_heal, arsenal_repair,
  theater, wall_garrisoned, wonder_population_cap, xp_trickle, celtic_healer)
  plus the per-civ aura folders in `gauls/` (teambonus, carnyx, the 3 hero
  auras) and `romans/` (teambonus, eternal_fire, centurion auras, the 4 hero
  auras). Auras are collected from the `Auras` component lists of the units/
  structures a civ can own plus its `special/players/<civ>.xml` player
  template (the teambonus); gaia-carried corral auras and unreachable auras
  (catafalques, decorative buildings, orphans) are documented in the READMEs.
  Generated by the new versioned `tools/auras.py`; `tools/civ.py` extended.
  `docs/GAME.md` gained the aura mechanics and inventory (151 files: 9 generic,
  105 single-civ, 3 gaia-only, the rest unreachable).
- Documentation: every upgradable unit file (generic + gauls + romans) now has
  a "Ranks" section per non-basic rank (Advanced, Elite) with the promotion
  target, required XP and every stat that changes for that rank. The changes
  are computed from the auto-researched `unit_advanced`/`unit_elite` techs
  (verified: the `_a`/`_e` templates only change identity/rank/promotion),
  with per-civ notes for XP deviations (rome's elite promotion: 2000 XP),
  mercenaries (0 XP via `upgrade_rank_advanced_mercenary`), civs skipping or
  extending the ladder (spart's champion is trained at Elite; athen's elite
  spearman promotes to `champion_infantry`; rome's champion promotes to the
  "First Cohort" variant). `docs/GAME.md` documents the rank mechanics.
- Documentation: added `docs/game_description/romans/` — the rome-specific
  counterpart of `gauls/` (units exclusive to rome: champion centurion, 3
  heroes, antesignanus, the directly-trained `_a` ranks, onager/scorpio;
  buildings: army_camp, temple_vesta, wallset_siege; technologies:
  civbonuses/rome_siege, roman_reforms, roman_roads). `tools/gaul.py` is
  generalised into `tools/civ.py <civ-code>` (gauls output verified unchanged);
  civ building docs now show effective trainer lists only (the army_camp lists
  `infantry_axeman_a`/`infantry_pikeman_a` but rome has no such files, so
  `Trainer.js` drops them).
- Documentation: `docs/game_description/` re-organised — the three generic
  references now live under `docs/game_description/generic/` (`units/`,
  `buildings/`, `technologies/`, prefix dropped), and a new
  `docs/game_description/gauls/` reference documents what is exclusive to gaul
  (units: champion_fanatic, champion_infantry_trumpeter, hero_brennus,
  hero_vercingetorix, hero_viridomarus; buildings: assembly; technologies:
  civbonuses/gaul_cavalry, gather_farming_harvester). Generated by the new
  `tools/gaul.py`. `docs/GAME.md` corrections: the gaul tavern (and
  `rotarymill`, `range`) templates are vestigial — no Builder list references
  them; forge, market and temple are the Town-class buildings gaul uses for
  City phase.
- Documentation: the generic units files (`docs/game_description/generic/units/`)
  now include the **capture attack** (strength, range, repeat time, restricted
  classes) and the **gather data** (ResourceGatherer rates per resource
  subtype, carrying capacities, base speed) for every unit, with per-civ
  overrides where they differ (e.g. cavalry only gathers meat — rate 5, cap 20;
  spartan helots have boosted stats; spart's champion swordsman is the only
  champion that gathers). `tools/analyze.py` updated accordingly.
- Documentation: added `docs/game_description/generic/technologies/` — one
  markdown file per generic 0 A.D. technology (available to 2+ civs; 95 techs),
  with cost, research time, requirements, modifications and the per-civ
  researcher lists (including `{civ}`→generic fallback and the
  `civ`/`notciv` requirement gates). Generated by the new versioned script
  `tools/technologies.py` (same loader/merge reimplementation). `docs/GAME.md`
  gained the tech mechanics paragraph (Researcher lists, auto-research civ
  bonuses, pair techs, phase tech chaining) and the tech inventory (198 files:
  160 available, 95 generic, 65 single-civ, 17 unreachable — e.g.
  `unlock_females_house`, `ship_capture_resistance`).
- Documentation: added `docs/game_description/generic/units/` — one markdown
  file per generic 0 A.D. unit (trainable in skirmish by 2+ civs; 36 units),
  with basic stats resolved from the shared template chain and the list of
  civilisations that train each unit (plus per-civ stat overrides). Added
  `docs/game_description/generic/buildings/` — the same for generic buildings
  (buildable by 2+ civs; 23 structures, with stats, per-civ overrides and
  effective trainer lists). All values extracted from `/home/ubuntu/0ad-reference/`
  (0.28.0) by re-implementing the engine's template loader/merge semantics
  (`TemplateLoader.cpp`, `ParamNode.cpp`, `Trainer.js`, `Builder.js`) — nothing
  from memory. `docs/GAME.md` gained a "Simulation templates and data
  organisation" section documenting the template layout, inheritance/merge
  rules, `{civ}`/`{native}` substitution, trainer/builder lists, and the
  inventory (133 trainable unit types: 36 generic, 97 single-civ; 56 buildable
  structures: 23 generic, 33 single-civ; the archery range is not buildable in
  0.28 — no Builder list references it).
- Turn 029 (G4a progress, good): the silent training killer found and fixed —
  the spearman costs 50 food + 50 wood (the base infantry template's 50 food
  is inherited), the sim silently rejects unaffordable train orders, and the
  turn-026 "food buys nothing" gather split had starved the army. Now: 2:1
  wood:food pre-town, 1:1 post-town, two workers on food post-town, 5 houses
  pre-town. ≥ 32 melee at minute 22 on 8/10 seeds (max 43–53), City 10/10,
  composite +17.19, 0 JS errors, canary PASS. G4a re-scoped to the
  evidence-supported target (32 melee + 3 rams).
- Workflow (Louis, 2026-08-20): after each validated turn, the bot mod is
  published as a zip on the file server — https://files.louissaglio.fr/vercingetorix.zip
  (mod folder `vercingetorix/` at the archive root; the current zip carries
  the turn-023 validated state). Codified in `docs/PROTOCOL.md` step 6.
- Protocol update (Louis's feedback, post-turn 024): bad/neutral verdicts may
  be fixed **in the same turn** when the cause is understood and the fix is
  small (iterate the treatment against the same baseline; stop the turn when
  it stops converging), and the baseline is defined as the **last validated
  experiment** — run once per turn, reused across in-turn iterations.
- Turn 023 (G4 progress): forge placement now walks a double ring (16
  candidates at 72 m + 16 at 88 m, ≥ 28 m structure clearance); 9/10 seeds
  reach real City Phase at minute 18–19 (single ring: 5/10), 0 JS errors,
  canary PASS.
- Turn 022 (G4 evidence): G4's match limit raised 20 → 25 game-minutes —
  City Phase lands at minute 17–19 even on the seeds where the forges build,
  leaving no time for the arsenal/ram/attack inside 20 minutes. (The forge
  placement ring itself was neutral, 5/10, and reverted.)
- Turn 019 (G4 progress): Town Phase is now researched **for real** — the bot
  commands all citizen soldiers (the javelineers/cavalry were idle since turn
  002), builds 5 Village-class houses, and posts Town only when the sim's
  `canResearch` passes. 9/10 seeds reach `currentPhase()==2` at minute 7–8
  (first run invalid: the foundation-repair loop could pick the non-building
  cavalry and stall; fixed to pick a real builder). Stone/metal 750/750 by
  minute 16 unaffected.
- Turn 018 (evidence correction, protocol/tooling): the sim silently rejects
  phase research whose requirements are unmet — Town needs 5 Village-class
  structures, City needs 3 Town-class structures. Turn 011's "Town reached
  10/10" measured the bot's own flag, not the sim: `currentPhase()` stayed 1
  all match. DEVELOPER_GUIDE now mandates sim-truth phase evidence.
- Turn 017 (goal G3 achieved): the four starting support workers now gather
  stone/metal from minute 0 (two each) and the army keeps a post-town carve-out
  for them; attack waits until 750 stone + 750 metal are banked. 10/10 seeds
  reach ≥750/750 by game-minute 16 (turn 016: 2/10), 0 JS errors, canary PASS,
  composite −2.34 (resourcesGathered up on every seed). Closes G3 and opens G4
  (defeat sandbox Rome).
- Turn 015 (goal reconsideration): split the blocked "defeat sandbox Rome" goal
  into a stone/metal resource prerequisite (new G3) and moved the win goal to
  G4.
- Turn 014 (perf): replaced the bot's full-map resource scan with auto-maintained
  cached collections; behavior-preserving (canary PASS), 0 JS errors, no
  turn-rate regression.
- Turn 011 (G3 progress): the bot now saves food/wood and researches Town Phase
  before massing soldiers; 10/10 seeds reach Town (baseline 0/10), 0 JS errors,
  canary PASS.
- Turn 008 (goal G2 achieved): the bot now grows to a 32-soldier army before
  attacking — `SOLDIER_TARGET` raised to 32 and `HOUSE_OFFSETS` expanded to 8
  candidates so it can actually build its 4 houses. 8/10 seeds reach ≥32 melee
  by game-minute 12 (baseline 0/10), 0 JS errors, canary PASS. Closes G2 and
  opens G3 (defeat sandbox Rome).
- Turn 004 (goal G1 achieved): the bot now attacks only at its 20-soldier
  target instead of at 15, so it boots its economy instead of sacrificing the
  army early. Baseline-vs-treatment (seeds 21–30, sandbox Rome): mean peak
  melee in the first 8 game-minutes 15.7 → 20.7 (+31.8%), G1 grade distribution
  9 Fail/1 Pass → 10/10 Good, canary PASS, composite +9.00 → good. Closes G1
  and opens G2 (defeat sandbox Rome).
- The determinism gate is the per-batch canary: same seed twice must be
  bit-identical. This only holds because experiments now pin the biome to
  `generic/temperate` and the player placement to `circle` — both gamesetup
  defaults are `"random"`, drawn from the unseeded GUI `Math.random` per run,
  so unpinned no map ever reproduces (root cause in
  `docs/ENGINE_BUG_0AD_0.28_NONDETERMINISM.md`).
- Added `harness report`: paired baseline-vs-treatment scoring per the
  protocol's verdict rules (outcome + quality + survival components, draw
  semantics, JS-error veto, canary identity check), writing `report.md` plus
  a compact summary.
- Experiments now play `conquest_civic_centers` (destroy the enemy civic centres)
  with treasures disabled (forced by the bot mod's autostart override); the
  harness gained a `--victory` flag.
- Documented the verified 0.28 AI API in the developer guide, corrected the game
  reference (0.28 has dedicated worker citizens — the support civilians that
  start the game, gather, and build), and enriched it with the construction
  two-step, population bonuses, treasures, and the meter-based position scale.
- Moved `PROTOCOL.md`, `GOALS.md`, `CHANGELOG.md` into `docs/` and added a root
  `AGENTS.md` pointing at the canonical documents; added the goal-reconsideration
  rule (adjust a goal rather than grind if it resists several turns).
- Published the repository to GitHub (https://github.com/Louis-Saglio/vercingetorix);
  every commit is pushed after it lands.
- Protocol v3 per Louis's review: long-term goals with per-goal grading scales
  (`GOALS.md`, current goal G1 — economy boot), experiments limited to 20 minutes of
  **game time** via a mod trigger (tunable per turn), mandatory per-game-minute
  telemetry with early abort of failing runs, mandatory instrumentation with every
  hypothesis implementation, reusable evidence-exploration tools, and the
  evidence-turn deliverable definition (collection code + the understanding gained).
- Reworked the development protocol per Louis's review: post-turn reflection step
  (harness/protocol improvements get their own commits), evidence-collection and
  refactor turn types, a composite verdict score (outcome + quality metrics +
  survival time, so a longer defeat can count as progress), timeouts recorded as
  draws, gaul-vs-rome on mainland, per-turn seed rotation with a canary match for
  deterministic comparison.
- Added the experiment harness (`harness/`): spawns headless matches with isolated
  HOMEs, extracts per-player end-of-game statistics, and writes per-match and batch
  JSON results. Verified deterministic across repeated runs.
- Established the turn-based development protocol (`PROTOCOL.md`), the turn journal
  (`turns/`), and the project scaffolding.
- Verified on this VPS that 0 A.D. 0.28.0 runs fully headless (`-autostart-nonvisual`),
  prints per-player end-of-game statistics JSON to stdout, and simulates at roughly
  13-21x real-time on this hardware (measured ~300 turns/s solo in practice).
