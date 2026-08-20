# 0 A.D. 0.28.0 — Game knowledge

Ground truth for bot development, distilled from the installed game data
(`/home/ubuntu/0ad-reference/public/`) and engine source (`.../source/`), not from
memory. Verify anything suspicious against those paths; they are pinned to the
running engine version.

The full game reference lives in `docs/game_description/` (see its README):
per-mechanic deep dives in `mechaniques/` and per-entity data in `generic/`,
`gauls/`, `romans/` — all verified against the source with inline citations.

## Objective of a match

The default victory condition is **Conquest**: "Defeat opponents by killing all
their units and destroying all their structures" (`simulation/data/settings/victory_conditions/conquest.json`).
Other conditions exist (wonder, capture the relic, regicide, conquest_structures,
conquest_units, conquest_civic_centers). **The harness plays
`conquest_civic_centers`**: "Defeat opponents by destroying all their fully built
civic centers" — a game ends when the enemy CCs fall (foundations do not count).

## Civilisations

15 civs: `athen brit cart gaul germ han iber kush mace maur pers ptol rome sele spart`
(`simulation/data/civs/*.json`). The bot plays **gaul**; the opponent plays **rome**.
Each civ has its own building set, unit roster, and techs. Data per civ lives in
`simulation/data/civs/<civ>.json`.

## Resources and economy

Four resources: **food, wood, stone, metal**. Match start: 300 of each (from the
autostart manifest), population cap **300 per player** (gamesettings default,
pinned by the bot mod's autostart override). Experiments play on a **Small**
map (`random/mainland`, 192 tiles).

The economy runs on two kinds of workers:

- **Dedicated worker citizens** — the support civilian (e.g. "Gallic Laborer" /
  Ambactos). Every civ starts with 4. They gather (ResourceGatherer rates on
  `template_unit_support_civilian.xml`) and they **build all structures** (the
  full builder mixin list, `templates/mixins/builder.xml`). They cannot fight.
  The base civic-centre template trains them (`units/{native}/support_civilian`),
  but civ-specific CC trainer lists (gaul, athen) list only military units — so
  for those civs the starting 4 are the only ones.
- **Citizen soldiers** — every trainable military unit also has the `Worker`
  class (`template_unit_infantry.xml`: classes `Human CitizenSoldier`, visible
  classes `Citizen Worker Soldier Infantry`) and gathers when not fighting.

So the army is also the workforce, but dedicated laborers exist and are the
builders.

- **Dropsites:** storehouse (wood/stone/metal), farmstead (food). Units carry
  resources back to the nearest dropsite.
- **Food:** berry bushes and hunt early; **fields** (built near a farmstead, need
  food to seed) are the steady source; corrals raise animals.
- **Trade:** market — barter resources, or set trade routes between markets/docks.
- Buildings cost resources; **spearmen cost 50 food + 50 wood** (the base
  infantry template's 50 food is inherited and merged with the spearman's own
  50 wood — see `docs/game_description/generic/units/infantry_spearman_b.md`);
  houses cost 75 wood.
- **Treasures:** treasure chests (gaia entities) are scattered on the map; units
  can gather them for instant resources. Disabled in the experiments
  (`DisableTreasures` gamesetting, forced by the bot mod's autostart override).
- **Construction is two steps:** a `construct` command only *places* the
  foundation (the API helper posts `autorepair:false`); the actual building is a
  separate `repair` order on the foundation. Foundations carry the class of the
  final building plus `Foundation`.

## Units

Core trainable units (gaul civil centre): `infantry_spearman_b`,
`infantry_javelineer_b`, `cavalry_javelineer_b`; barracks/stable/range add more
(`structures/gaul/civil_centre.xml` Trainer list).

- **Roles:** melee infantry, ranged infantry, cavalry, champions (elite, from
  fortress), siege (rams/catapults), heroes, ships.
- **Counters via attack bonuses:** each unit's Attack section declares bonus
  multipliers against classes. Example: spearmen have **2.5x vs Cavalry**
  (`template_unit_infantry_melee_spearman.xml` → `BonusCavMelee`). Javelineers and
  slingers have their own bonuses — check the template before assuming a counter.
- **Promotion:** units promote by rank, e.g. `infantry_spearman_b` →
  `infantry_spearman_a` (better stats).
- **Armor:** three damage types — hack, pierce, crush; armor per type on the
  template. Ranged attacks are pierce, most melee is hack, siege is crush.
- **Capture:** structures are capturable (`Capturable` on `template_structure.xml`)
  — units can take enemy buildings instead of destroying them.

## Buildings

Civil centre (CC): the heart of the base — trains the core citizen soldiers,
researches phase techs, projects territory. Houses raise population cap. Barracks /
stable / range train the military units. Farmstead + fields produce food; corral
animals; storehouse drops wood/stone/metal; market trades. Towers/fortress defend.
Gaul's buildable set is the standard one plus the city-phase `assembly`
(`simulation/templates/structures/gaul/`); that folder also contains vestigial
templates no Builder list references (`tavern.xml`, `rotarymill.xml`,
`range.xml`).

All construction requires being inside your territory, and buildings can only be
placed where builders can reach.

## Phases (ages)

Three phases: **Village → Town → City**, advanced by researching the phase techs at
the CC (`simulation/data/technologies/phase_town.json`, `phase_city.json`). Town
and City unlock better units, buildings, and techs. The time a bot reaches each
phase is a core quality metric (reported by the bot via research events).

**Phase requirements (verified 0.28):** Town requires **5
Village-class structures** (`classCounts["Village"] ≥ 5` — houses carry the
Village class); City requires **3 Town-class structures** (forge, market and
temple carry the Town class) plus the 750 stone /
750 metal cost. Town costs 500 food + 500 wood. **The sim silently rejects
phase research whose requirements are unmet** — no resources are paid, nothing
is logged, and the bot's own flags keep lying. Ground truth is
`gameState.currentPhase()` / `isResearched()`. Details:
`docs/game_description/mechaniques/technologies_and_modifiers.md`.

## Territory and map

- Territory comes from the CC (and some other buildings); buildings must be built
  inside it. Territory control % is a tracked statistic.
- The harness map is `random/mainland` (a balanced land map), size 192 tiles ("Small"),
  circular. Seed determines the layout; same seed = same map.

## Simulation facts (for bot code)

- **Turns:** fixed 200 ms of sim time each; AIs get `HandleMessage` every turn.
  Headless games run the turns as fast as the CPU allows (~60-300x real time here).
- **Positions are in meters, 4 m per tile.** Every offset, radius, and range in
  bot code must be scaled by 4 (e.g. 40 tiles = 160 m).
- **Population:** the CC provides 20, each house 5 (`template_structure_civic_*`);
  the cap is the sum of the player's Population bonuses, and training stalls when
  it is reached.
- **Determinism:** same seed, same commands → identical outcome. This is a hard
  requirement for every bot change (savegames and replays depend on it).
- **AI events** (via `this.events` in the bot): attacks, construction finished,
  trainings finished, research finished, entity renamed, player defeated, etc.
- **Statistics:** the engine tracks per-player `StatisticsTracker` metrics
  (resources gathered/used, units trained/lost/killed, buildings, % map explored,
  % territory) and prints them at game end — the harness's data source.
- **Petra difficulty** (the opponent): sandbox −58% gather/trade rate, very easy
  −44%, easy −25%, medium ±0%, hard +25%, very hard +56%; sandbox does not expand
  or attack.

## Simulation templates and data organisation

All paths relative to `/home/ubuntu/0ad-reference/public/` (data) and
`/home/ubuntu/0ad-reference/source/source/` (engine C++/JS). Everything below
was verified against those files.

### Directory layout (`simulation/`)

- `templates/` — every entity is an XML template (the engine compiles them to
  the `.cached.xmb` files sitting next to each `.xml`):
  - Root `template_unit_*.xml` / `template_structure_*.xml` / `template_*.xml` —
    generic base definitions shared by all civs. The template loader never
    registers `template_*` files as placeable entities
    (`ps/TemplateLoader.cpp` `AddToTemplates`).
  - `templates/units/<civ>/` — one file per civ unit. A civ unit file usually
    only sets Identity (names) + VisualActor; stats come from its `parent`
    chain into the root `template_unit_*` templates.
  - `templates/units/` root — only 12 non-civ files (`merc_*`, `samnite_*`,
    `theb_*`, `thesp_*`, `viking_longship`, `noldor_warship`, `plane`). None is
    trainable in skirmish: they are spawned by scenario maps (the mercs,
    samnites, thebans…), `plane` is the `createPlane` cheat, and
    `theb_siege_fireraiser` / `viking_longship` are referenced nowhere outside
    l10n/art. `templates/units/pirates/` is a scenario-only pseudo-civ.
  - `templates/structures/<civ>/` — civ buildings; `structures/` root — generic
    placed buildings (shrines, tents, fences, `merc_camp_egyptian`…).
  - `templates/mixins/` — shared behaviour packages applied as parent overlays:
    `builder.xml` (the full `structures/{civ}/...` build list), `gather_*`
    (gather rates), `hoplite`, `longsword`, `shrine`…
  - `templates/special/filter/` — runtime filters searched **first** by the
    loader (before mixins, before root).
  - `templates/gaia/` — fauna, trees, ruins, treasures.
  - `templates/skirmish/` — gamesetup defaults: `skirmish/units/default_*`
    (starting units) and `skirmish/structures/default_*` (buildings). Entities
    spawned from them are replaced per civ by the `SkirmishReplacer` component
    using `data/civs/<civ>.json` → `SkirmishReplacements`.
- `data/civs/<civ>.json` — `StartEntities` (the starting units/buildings),
  `SkirmishReplacements`, `WallSets`, `CivBonuses`, `AINames`.
- `data/technologies/` — techs (JSON), incl. the phase techs. Techs available to a
  civ come from the buildings' `Researcher/Technologies` lists: a `{civ}` token
  resolves to the `<civ>`-specific tech if its file exists, else to the
  `generic` fallback (e.g. `phase_town_{civ}` → `phase_town_athen` for athen,
  `phase_town_generic` for the 13 other civs); a tech is then removed if its
  own `requirements` operators (`civ`, `notciv`, `all`, `any` — see
  `globalscripts/Technologies.js` `InterpretTechRequirements`) forbid the civ.
  Techs with `autoResearch: true` (e.g. `phase_village`, the
  `data/technologies/civbonuses/*` civ bonus techs) are auto-researched by
  every civ whose requirements allow it (`TechnologyManager.js`). Pair techs
  (`top`/`bottom` fields) present a two-way choice; the phase techs use
  `supersedes`/`replaces` to chain Village→Town→City under the logical names
  `phase_village`/`phase_town`/`phase_city`.
- `data/auras/` — auras (JSON): `type` (`range`, `garrison`, `garrisonedUnits`,
  `formation`, `global`), `radius`, `affects` (classes), `affectedPlayers`,
  `stackable`, `requiredTechnology` and `modifications` (same format as tech
  modifications). Auras are attached to entities by the `Auras` component (a
  token list in the entity template, `simulation/components/Auras.js`):
  the root unit/structure templates carry the shared ones (e.g.
  `template_unit_infantry` → `units/ram_garrison`; the temple →
  `structures/temple_heal`), hero/champion/catafalque units carry their own,
  and the **player template** `special/players/<civ>.xml` carries the civ's
  teambonus (`teambonuses/<civ>_player_teambonus`, a `global` aura with
  `affectedPlayers: MutualAlly`). The corral food-trickle auras are attached
  to **gaia domestic animals** (`gaia/fauna_*` → `structures/corral_garrison_*`),
  so they work for everyone when the animals are garrisoned in the corral.
  Unreachable in skirmish: the catafalque auras (catafalques are in no
  builder/trainer list), `structures/farmstead_60`/`structures/loyalty_regen`
  (decorative mills / Ishtar gate) and a few orphan auras (`units/centurion`,
  the Craterus/Pyrrhus hero auras).
- `data/settings/` — victory conditions and other settings.
- `components/` — JS implementations of the simulation components; each file
  declares its own XML schema (`Trainer.js`, `Resistance.js`, `Attack.js`, …).

### Template inheritance and merging

- A template declares `parent="..."`. The loader
  (`ps/TemplateLoader.cpp` `LoadTemplateFile`) resolves a name by searching
  `special/filter/<name>.xml` → `mixins/<name>.xml` → `<name>.xml`; a
  `A|B` parent means "load B as base, then apply A on top" (e.g.
  `hoplite|template_unit_infantry_melee_spearman`). Inheritance depth is capped
  at 100.
- Child layers merge onto the parent layer with `CParamNode::ApplyLayer`
  (`simulation2/system/ParamNode.cpp`) semantics: leaf values override;
  `datatype="tokens"` lists **merge** (new tokens appended, a token prefixed
  with `-` removes an inherited token); special attributes: `disable=""`
  removes the component, `replace=""` wipes the node before applying,
  `op="add|mul|mul_round"` applies arithmetic on the inherited value (e.g.
  cavalry `WalkSpeed op="mul"` = 2× the base 9 m/s), `merge=""` only applies
  when the parent has the node, `filtered=""` keeps only the listed children.

### Civ substitution and who trains what

- `Trainer/Entities` lists use `units/{civ}/X`: `{civ}` is replaced by the
  **owner's** civ code and `{native}` by the **building's** `Identity/Civ`
  (matters only for captured buildings, e.g. `merc_camp_egyptian` has
  `Identity/Civ=ptol`). `Trainer.js` `CalculateEntitiesMap` then **drops any
  entry whose template file does not exist** — so a civ trains a listed unit
  type only if it has `units/<civ>/<type>.xml`. Example: every barracks lists
  `champion_infantry_spearman`, but only mace has the file, so only mace trains
  it.
- Generic trainer lists (inherited by the civ buildings):
  civil centre → `support_civilian` + core citizens; barracks → melee/ranged
  infantry (b ranks + champions); stable → cavalry + cavalry champions + chariots;
  range → javelineer/slinger/archer/crossbow + their champions; dock → all ships;
  fortress → champion/hero/siege lists come from the civ-specific fortress file;
  temple → `support_healer_b`; market → `support_trader`; house →
  `support_civilian_house`; arsenal → siege; kennel → `war_dog`; elephant stable
  → `champion_elephant`.
- Promotions (`Promotion/Entity`, `units/{civ}/..._a`) and `RequiredXp` (100
  base) produce the `_a`/`_e` ranks — promoted units are **not** in trainer
  lists. The rank ladder is `Basic → Advanced → Elite`; the `_a`/`_e` template
  files themselves only change `Identity/Rank`, `Promotion` and the actor.
  **All rank stat changes come from two auto-researched techs**: `unit_advanced`
  (affects classes `Advanced Unit` and `Elite Unit`: +25% health, +20% build
  time, +0.7 capture strength, +20% loot, −30% gather speed, +10% melee
  damage, −20% ranged spread, healer +5 strength/+3 range) and `unit_elite`
  (the same again for `Elite Unit`). `GetIdentityClasses`
  (`globalscripts/Templates.js`) appends the `Rank` to the unit's classes,
  which is how the techs target the ranks. Mercenaries promote at 0 XP
  (`upgrade_rank_advanced_mercenary` replaces `RequiredXp`). Special
  promotions exist beyond the ladder: rome's champion swordsman →
  `champion_infantry_swordsman_first` (3000 XP, stats unchanged), athen's
  elite spearman → `champion_infantry` (250 XP), rome's elite spearman →
  `infantry_spearman_conscript` (2000 XP); spart's champion swordsman is
  trained directly at Elite rank.
- Buildability is symmetric: units carry `Builder/Entities` with
  `structures/{civ}/...` (`mixins/builder.xml`) — a civ can only build
  structures it has a file for. Vestigial templates exist: the archery range
  (`structures/{civ}/range.xml` for athen/mace/pers/sele/han) is **not in any
  Builder list** in 0.28, so it cannot be built at all (archers train from the
  barracks); `structures/pers/apartment_block.xml` and the sele academy are
  likewise unreferenced.

### Generic units inventory (0.28.0)

Across the 15 civs there are **133 trainable unit types**: **36 are trained by
2+ civs** (the generic units, one file each in
`docs/game_description/generic/units/`, with stats resolved from the deepest
shared template and the per-civ trainer lists), and **97 are trained by a
single civ** (46 heroes, civ-specific champions/mercenaries/conscripts…).
Stats in those files come from re-implementing the loader+merge semantics
above on the actual templates, not from memory.

### Generic buildings inventory (0.28.0)

Across the 15 civs there are **56 buildable structure types**: **23 are
buildable by 2+ civs** (the generic buildings, one file each in
`docs/game_description/generic/buildings/`, with stats resolved the same way
plus per-civ trainer lists), and **33 are buildable by a single civ**
(civ-unique temples, halls, embassies, monuments…). Wall sets
(`wallset_palisade`, `wallset_stone`) are documented as wall sets, not single
buildings — they define the segments placed with the wall tool.

### Generic technologies inventory (0.28.0)

Of the 198 tech JSON files (`data/technologies/` + `civbonuses/`), **160 are
available to at least one civ** (researchable from a building or
auto-researched): **95 are available to 2+ civs** (the generic technologies,
one file each in `docs/game_description/generic/technologies/`), and **65 to a
single civ** (civ-specific phase techs, pair choices, unique bonuses). 17 are
not reachable by anyone (logical phase names `phase_town`/`phase_city`,
pair-choice techs of single-civ pairs, and leftovers such as
`unlock_females_house` or `ship_capture_resistance`).

### Generic auras inventory (0.28.0)

Of the 151 aura JSON files, **9 auras are available to 2+ civs** (the generic
auras, one file each in `docs/game_description/generic/auras/`), **105 are
single-civ** (the 15 teambonuses, hero auras, civ-unique auras — documented
per civ in `gauls/auras/`, `romans/auras/`, …), **3 are gaia-carried** (the
corral food trickles) and the rest are unreachable in skirmish (catafalques,
decorative buildings, orphans).

## Where to look

In-repo references (read these first; see `docs/game_description/README.md`
for the full index):

- Game mechanics, one verified file per mechanic (combat formula,
  construction, training, population, capture, territory, technologies,
  auras, vision, garrisoning, trade, victory, orders/sim time…):
  `docs/game_description/mechaniques/`
- Generic units reference (stats + Guide + per-civ trainer lists):
  `docs/game_description/generic/units/`
- Generic buildings reference (stats + Guide + per-civ builder lists):
  `docs/game_description/generic/buildings/`
- Generic technologies reference (stats + per-civ researcher lists):
  `docs/game_description/generic/technologies/`
- Generic auras reference (stats + per-civ carriers):
  `docs/game_description/generic/auras/`
- Civ-specific references (units/buildings/technologies/auras exclusive to one
  civ): `docs/game_description/gauls/`, `docs/game_description/romans/`

Ground truth (verify anything suspicious here; pinned to the running engine):

- Units/buildings: `/home/ubuntu/0ad-reference/public/simulation/templates/`
- Civ definitions: `.../simulation/data/civs/*.json`
- Technologies: `.../simulation/data/technologies/`
- Mechanics: `.../simulation/components/*.js`, `.../simulation/helpers/*.js`
- Victory conditions: `.../simulation/data/settings/victory_conditions/`
- Simulation components: `.../simulation/components/*.js`
- Engine internals: `/home/ubuntu/0ad-reference/source/source/`
- Reference bot: `.../public/simulation/ai/petra/` and `.../common-api/`
