# champion_infantry

Trained by **3** civilisations. Generic (non-civ-specific) unit of 0 A.D. 0.28.0 — see `docs/game_description/generic_units/README.md` for the method.

Generic stats resolved from the shared template `simulation/templates/template_unit_champion_infantry_spearman` (deepest template common to all civilisation variants; variants may override, see below).

## Basic stats

- **Generic name:** Champion Spearman
- **Health:** 200 HP
- **Armor:** 6 hack / 6 pierce / 20 crush
- **Attack:** Melee "Spear" — damage 10 hack + 8.5 pierce — range 4 m — prepare 0.5 s — repeat 1 s — bonus 2.5× vs Cavalry — preferred Unit+!Ship
- **Speed:** walk 9.5 m/s, run 15.86 m/s
- **Vision:** 80 m
- **Cost:** 80 food, 60 wood, 80 metal
- **Build time:** 20 s
- **Population:** 1
- **Classes:** Unit Organic ConquestCritical Human
- **Visible classes:** Soldier Champion Infantry Melee Spearman

## Civilisations that can train it

- **athen** — `units/athen/champion_infantry` (gymnasium)
- **cart** — `units/cart/champion_infantry` (temple)
- **pers** — `units/pers/champion_infantry` (barracks)

## Civilisation-specific overrides

These civilisations override the generic stats above (only differing values are listed):

- **athen** — `units/athen/champion_infantry`
  - health 200 HP
  - armor 6 hack / 6 pierce / 20 crush
  - Melee "Spear" — damage 10 hack + 8.5 pierce — range 4 m — prepare 0.5 s — repeat 1 s — bonus 2.5× vs Cavalry — preferred Unit+!Ship
  - walk 9.5 m/s
  - run 15.86 m/s
  - vision 80 m
  - cost 80 food, 60 wood, 80 metal
  - build time 15 s
  - population 1
- **cart** — `units/cart/champion_infantry`
  - health 200 HP
  - armor 6 hack / 6 pierce / 20 crush
  - Melee "Spear" — damage 10 hack + 8.5 pierce — range 4 m — prepare 0.5 s — repeat 1 s — bonus 2.5× vs Cavalry — preferred Unit+!Ship
  - walk 9.5 m/s
  - run 15.86 m/s
  - vision 80 m
  - cost 80 food, 60 wood, 80 metal
  - build time 15 s
  - population 1
- **pers** — `units/pers/champion_infantry`
  - health 120 HP
  - armor 4 hack / 5 pierce / 20 crush
  - Melee "Spear" — damage 8.5 hack + 7.225 pierce — range 4 m — prepare 0.5 s — repeat 1 s — bonus 2.5× vs Cavalry — preferred Unit+!Ship
  - walk 9.5 m/s
  - run 15.86 m/s
  - vision 80 m
  - cost 50 food, 30 wood, 50 metal
  - build time 20 s
  - population 1
