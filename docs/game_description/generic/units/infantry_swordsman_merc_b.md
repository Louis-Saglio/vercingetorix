# infantry_swordsman_merc_b

Trained by **2** civilisations. Generic (non-civ-specific) unit of 0 A.D. 0.28.0 — see `docs/game_description/generic/units/README.md` for the method.

Generic stats resolved from the shared template `simulation/templates/template_unit_infantry_melee_swordsman` (deepest template common to all civilisation variants; variants may override, see below).

## Basic stats

- **Generic name:** Swordsman
- **Health:** 100 HP
- **Armor:** 3 hack / 3 pierce / 15 crush
- **Attack:** Capture — strength 2.5 — range 4 m — repeat 1 s — restricted Field Palisade Wall
- **Attack:** Melee "Sword" — damage 8 hack — range 3 m — prepare 0.375 s — repeat 0.75 s — preferred Unit+!Ship
- **Speed:** walk 9.5 m/s, run 15.86 m/s
- **Vision:** 80 m
- **Cost:** 50 food, 40 wood, 10 metal
- **Build time:** 10 s
- **Population:** 1
- **Gather:** rates: food: fruit 0.5, grain 0.25, meat 1; wood: tree 0.75, ruins 5; stone: rock 0.5, ruins 2; metal: ore 0.5, ruins 2 /s
- **Gather:** capacity: 10 food, 10 wood, 10 stone, 10 metal
- **Classes:** Unit Organic ConquestCritical Human CitizenSoldier
- **Visible classes:** Builder Citizen Worker Soldier Infantry Melee Swordsman
- **Rank:** Basic

## Civilisations that can train it

- **ptol** — `units/ptol/infantry_swordsman_merc_b` (military_colony)
- **sele** — `units/sele/infantry_swordsman_merc_b` (military_colony)

## Civilisation-specific overrides

These civilisations override the generic stats above (only differing values are listed):

- **ptol** — `units/ptol/infantry_swordsman_merc_b`
  - Capture — strength 2.5 — range 4 m — repeat 1 s — restricted Field Palisade Wall
  - Melee "Sword" — damage 8.8 hack — range 3 m — prepare 0.375 s — repeat 0.75 s — preferred Unit+!Ship
  - cost 60 metal
  - build time 7 s
- **sele** — `units/sele/infantry_swordsman_merc_b`
  - Capture — strength 2.5 — range 4 m — repeat 1 s — restricted Field Palisade Wall
  - Melee "Rhomphaia" — damage 8.8 hack — range 3 m — prepare 0.375 s — repeat 0.75 s — preferred Unit+!Ship
  - cost 60 metal
  - build time 7 s
