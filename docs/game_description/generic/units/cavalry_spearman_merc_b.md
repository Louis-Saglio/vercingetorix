# cavalry_spearman_merc_b

Trained by **2** civilisations. Generic (non-civ-specific) unit of 0 A.D. 0.28.0 — see `docs/game_description/generic/units/README.md` for the method.

Generic stats resolved from the shared template `simulation/templates/template_unit_cavalry_melee_spearman` (deepest template common to all civilisation variants; variants may override, see below).

## Basic stats

- **Generic name:** Cavalry Spearman
- **Health:** 160 HP
- **Armor:** 3 hack / 3 pierce / 15 crush
- **Attack:** Capture — strength 1.75 — range 4 m — repeat 1 s — restricted Field Palisade Wall
- **Attack:** Melee "Spear" — damage 6 hack + 5.5 pierce — range 4 m — prepare 0.625 s — repeat 1.25 s — bonus 1.75× vs Cavalry — preferred Unit+!Ship
- **Speed:** walk 18 m/s, run 25.2 m/s
- **Vision:** 80 m
- **Cost:** 100 food, 50 wood
- **Build time:** 15 s
- **Population:** 1
- **Gather:** rates: food: meat 5 /s
- **Gather:** capacity: 20 food
- **Classes:** Unit Organic ConquestCritical Human FastMoving CitizenSoldier
- **Visible classes:** Citizen Soldier Cavalry Melee Spearman
- **Rank:** Basic

## Civilisations that can train it

- **ptol** — `units/ptol/cavalry_spearman_merc_b` (military_colony)
- **sele** — `units/sele/cavalry_spearman_merc_b` (military_colony)

## Civilisation-specific overrides

These civilisations override the generic stats above (only differing values are listed):

- **ptol** — `units/ptol/cavalry_spearman_merc_b`
  - Capture — strength 1.75 — range 4 m — repeat 1 s — restricted Field Palisade Wall
  - Melee "Spear" — damage 6.6 hack + 6.05 pierce — range 4 m — prepare 0.625 s — repeat 1.25 s — bonus 1.75× vs Cavalry — preferred Unit+!Ship
  - cost 20 food, 90 metal
  - build time 10.5 s
- **sele** — `units/sele/cavalry_spearman_merc_b`
  - Capture — strength 1.75 — range 4 m — repeat 1 s — restricted Field Palisade Wall
  - Melee "Spear" — damage 6.6 hack + 6.05 pierce — range 4 m — prepare 0.625 s — repeat 1.25 s — bonus 1.75× vs Cavalry — preferred Unit+!Ship
  - cost 20 food, 90 metal
  - build time 10.5 s
