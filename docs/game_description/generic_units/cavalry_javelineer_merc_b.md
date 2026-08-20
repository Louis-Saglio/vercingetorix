# cavalry_javelineer_merc_b

Trained by **2** civilisations. Generic (non-civ-specific) unit of 0 A.D. 0.28.0 — see `docs/game_description/generic_units/README.md` for the method.

Generic stats resolved from the shared template `simulation/templates/template_unit_cavalry_ranged_javelineer` (deepest template common to all civilisation variants; variants may override, see below).

## Basic stats

- **Generic name:** Cavalry Javelineer
- **Health:** 100 HP
- **Armor:** 2 hack / 1 pierce / 15 crush
- **Attack:** Ranged "Javelin" — damage 18 pierce — range 30 m — prepare 0.4 s — repeat 1.5 s — preferred Human
- **Speed:** walk 16.2 m/s, run 22.68 m/s
- **Vision:** 80 m
- **Cost:** 100 food, 50 wood
- **Build time:** 15 s
- **Population:** 1
- **Classes:** Unit Organic ConquestCritical Human FastMoving CitizenSoldier
- **Visible classes:** Citizen Soldier Cavalry Ranged Javelineer
- **Rank:** Basic

## Civilisations that can train it

- **kush** — `units/kush/cavalry_javelineer_merc_b` (camp_blemmye)
- **ptol** — `units/ptol/cavalry_javelineer_merc_b` (military_colony)

## Civilisation-specific overrides

These civilisations override the generic stats above (only differing values are listed):

- **kush** — `units/kush/cavalry_javelineer_merc_b`
  - Ranged "Javelin" — damage 19.8 pierce — range 30 m — prepare 0.4 s — repeat 1.5 s — preferred Human
  - cost 20 food, 90 metal
  - build time 10.5 s
- **ptol** — `units/ptol/cavalry_javelineer_merc_b`
  - Ranged "Javelin" — damage 19.8 pierce — range 30 m — prepare 0.4 s — repeat 1.5 s — preferred Human
  - cost 20 food, 90 metal
  - build time 10.5 s
