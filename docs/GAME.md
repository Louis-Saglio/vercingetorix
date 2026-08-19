# 0 A.D. 0.28.0 — Game knowledge

Ground truth for bot development, distilled from the installed game data
(`/home/ubuntu/0ad-reference/public/`) and engine source (`.../source/`), not from
memory. Verify anything suspicious against those paths; they are pinned to the
running engine version.

## Objective of a match

The default victory condition is **Conquest**: "Defeat opponents by killing all
their units and destroying all their structures" (`simulation/data/settings/victory_conditions/conquest.json`).
Other conditions exist (wonder, capture the relic, regicide, conquest_structures,
conquest_units, conquest_civic_centers) but the harness always plays Conquest.

## Civilisations

15 civs: `athen brit cart gaul germ han iber kush mace maur pers ptol rome sele spart`
(`simulation/data/civs/*.json`). The bot plays **gaul**; the opponent plays **rome**.
Each civ has its own building set, unit roster, and techs. Data per civ lives in
`simulation/data/civs/<civ>.json`.

## Resources and economy

Four resources: **food, wood, stone, metal**. Match start: 300 of each (from the
autostart manifest), population cap 300.

The defining fact of 0.28: **there are no dedicated worker units.** Citizen
soldiers both gather and fight — every trainable infantry/cavalry unit has the
`Worker` class (`template_unit_infantry.xml`: classes `Human CitizenSoldier`,
visible classes `Citizen Worker Soldier Infantry`). The economy is the army and
the army is the economy. A unit that is not fighting or training should be
gathering or building. (A `support_civilian` template exists but no structure
trains it; it is not part of normal play.)

- **Dropsites:** storehouse (wood/stone/metal), farmstead (food). Units carry
  resources back to the nearest dropsite.
- **Food:** berry bushes and hunt early; **fields** (built near a farmstead, need
  food to seed) are the steady source; corrals raise animals.
- **Trade:** market — barter resources, or set trade routes between markets/docks.
- Buildings cost resources; units cost food/wood (spearman: 50 wood + food, see
  `template_unit_infantry_melee_spearman.xml`).

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
Gaul specifics include `assembly`, `tavern`, `rotarymill`
(`simulation/templates/structures/gaul/`).

All construction requires being inside your territory, and buildings can only be
placed where builders can reach.

## Phases (ages)

Three phases: **Village → Town → City**, advanced by researching the phase techs at
the CC (`simulation/data/technologies/phase_town.json`, `phase_city.json`). Town
and City unlock better units, buildings, and techs. The time a bot reaches each
phase is a core quality metric (reported by the bot via research events).

## Territory and map

- Territory comes from the CC (and some other buildings); buildings must be built
  inside it. Territory control % is a tracked statistic.
- The harness map is `random/mainland` (a balanced land map), size 128 tiles,
  circular. Seed determines the layout; same seed = same map.

## Simulation facts (for bot code)

- **Turns:** fixed 200 ms of sim time each; AIs get `HandleMessage` every turn.
  Headless games run the turns as fast as the CPU allows (~60-300x real time here).
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

## Where to look

- Units/buildings: `/home/ubuntu/0ad-reference/public/simulation/templates/`
- Civ definitions: `.../simulation/data/civs/*.json`
- Technologies: `.../simulation/data/technologies/`
- Victory conditions: `.../simulation/data/settings/victory_conditions/`
- Engine internals: `/home/ubuntu/0ad-reference/source/`
- Reference bot: `.../public/simulation/ai/petra/` and `.../common-api/`
