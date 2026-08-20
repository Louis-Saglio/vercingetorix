# army_camp

Roman-specific building of 0 A.D. 0.28.0 — only the romans can build it. See `docs/game_description/romans/buildings/README.md` for the method; shared buildings are documented in `docs/game_description/generic/buildings/`.

Stats resolved from `simulation/templates/structures/rome/army_camp` (full roman template chain).

## Basic stats

- **Generic name:** Army Camp
- **Health:** 1750 HP
- **Armor:** 15 hack / 35 pierce / 3 crush
- **Attack:** Ranged "Bow" — damage 8 pierce — range 60 m — prepare 0.4 s — repeat 3.5 s — preferred Human
- **Cost:** 400 wood, 150 stone
- **Build time:** 250 s
- **Garrison:** 20 slots
- **Vision:** 90 m
- **Capture points:** 1500
- **Build territory:** neutral enemy
- **Placement:** land
- **Build distance:** min 80 m from ArmyCamp
- **Requirements:** phase_town
- **Trains:** units/{civ}/infantry_swordsman_a units/{civ}/infantry_spearman_a units/{civ}/infantry_antesignanus units/{civ}/siege_onager_packed units/{civ}/siege_ram
- **Classes:** Structure ConquestCritical CivSpecific
- **Visible classes:** Town ArmyCamp

## Built by

- **rome** — `structures/rome/army_camp`
