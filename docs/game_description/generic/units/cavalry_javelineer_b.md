# cavalry_javelineer_b

Trained by **13** civilisations. Generic (non-civ-specific) unit of 0 A.D. 0.28.0 — see `docs/game_description/generic/units/README.md` for the method.

Generic stats resolved from the shared template `simulation/templates/template_unit_cavalry_ranged_javelineer` (deepest template common to all civilisation variants; variants may override, see below).

## Basic stats

- **Generic name:** Cavalry Javelineer
- **Health:** 100 HP
- **Armor:** 2 hack / 1 pierce / 15 crush
- **Attack:** Capture — strength 1.75 — range 4 m — repeat 1 s — restricted Field Palisade Wall
- **Attack:** Ranged "Javelin" — damage 18 pierce — range 30 m — prepare 0.4 s — repeat 1.5 s — preferred Human
- **Speed:** walk 16.2 m/s, run 22.68 m/s
- **Vision:** 80 m
- **Cost:** 100 food, 50 wood
- **Build time:** 15 s
- **Population:** 1
- **Gather:** rates: food: meat 5 /s
- **Gather:** capacity: 20 food
- **Classes:** Unit Organic ConquestCritical Human FastMoving CitizenSoldier
- **Visible classes:** Citizen Soldier Cavalry Ranged Javelineer
- **Rank:** Basic

## Civilisations that can train it

- **athen** — `units/athen/cavalry_javelineer_b` (civil_centre, stable)
- **brit** — `units/brit/cavalry_javelineer_b` (civil_centre, crannog, stable)
- **cart** — `units/cart/cavalry_javelineer_b` (civil_centre, stable)
- **gaul** — `units/gaul/cavalry_javelineer_b` (civil_centre, stable)
- **germ** — `units/germ/cavalry_javelineer_b` (civil_centre, stable)
- **iber** — `units/iber/cavalry_javelineer_b` (civil_centre, stable)
- **kush** — `units/kush/cavalry_javelineer_b` (civil_centre, stable)
- **mace** — `units/mace/cavalry_javelineer_b` (stable)
- **maur** — `units/maur/cavalry_javelineer_b` (civil_centre, stable)
- **pers** — `units/pers/cavalry_javelineer_b` (civil_centre, stable)
- **rome** — `units/rome/cavalry_javelineer_b` (stable)
- **sele** — `units/sele/cavalry_javelineer_b` (civil_centre, stable)
- **spart** — `units/spart/cavalry_javelineer_b` (civil_centre, stable)

## Civilisation-specific overrides

These civilisations override the generic stats above (only differing values are listed):

- **cart** — `units/cart/cavalry_javelineer_b`
  - walk 17.82 m/s
  - run 24.95 m/s
- **mace** — `units/mace/cavalry_javelineer_b`
  - Capture — strength 1.75 — range 4 m — repeat 1 s — restricted Field Palisade Wall
  - Ranged "Javelin" — damage 19.8 pierce — range 30 m — prepare 0.4 s — repeat 1.5 s — preferred Human
  - cost 20 food, 90 metal
  - build time 10.5 s
