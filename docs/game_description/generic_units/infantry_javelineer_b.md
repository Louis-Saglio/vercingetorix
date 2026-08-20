# infantry_javelineer_b

Trained by **11** civilisations. Generic (non-civ-specific) unit of 0 A.D. 0.28.0 — see `docs/game_description/generic_units/README.md` for the method.

Generic stats resolved from the shared template `simulation/templates/template_unit_infantry_ranged_javelineer` (deepest template common to all civilisation variants; variants may override, see below).

## Basic stats

- **Generic name:** Infantry Javelineer
- **Health:** 50 HP
- **Armor:** 1 hack / 1 pierce / 10 crush
- **Attack:** Ranged "Javelin" — damage 16 pierce — range 30 m — prepare 0.4 s — repeat 1.5 s — preferred Human
- **Speed:** walk 11.4 m/s, run 19.04 m/s
- **Vision:** 80 m
- **Cost:** 50 food, 50 wood
- **Build time:** 10 s
- **Population:** 1
- **Classes:** Unit Organic ConquestCritical Human CitizenSoldier
- **Visible classes:** Builder Citizen Worker Soldier Infantry Ranged Javelineer
- **Rank:** Basic

## Civilisations that can train it

- **athen** — `units/athen/infantry_javelineer_b` (barracks)
- **brit** — `units/brit/infantry_javelineer_b` (barracks)
- **gaul** — `units/gaul/infantry_javelineer_b` (barracks, civil_centre)
- **germ** — `units/germ/infantry_javelineer_b` (barracks)
- **iber** — `units/iber/infantry_javelineer_b` (barracks, civil_centre)
- **mace** — `units/mace/infantry_javelineer_b` (barracks, civil_centre)
- **pers** — `units/pers/infantry_javelineer_b` (barracks)
- **ptol** — `units/ptol/infantry_javelineer_b` (barracks)
- **rome** — `units/rome/infantry_javelineer_b` (barracks, civil_centre)
- **sele** — `units/sele/infantry_javelineer_b` (barracks, civil_centre)
- **spart** — `units/spart/infantry_javelineer_b` (barracks, civil_centre)

## Civilisation-specific overrides

These civilisations override the generic stats above (only differing values are listed):

- **athen** — `units/athen/infantry_javelineer_b`
  - Ranged "Javelin" — damage 17.6 pierce — range 30 m — prepare 0.4 s — repeat 1.5 s — preferred Human
  - cost 60 metal
  - build time 7 s
- **ptol** — `units/ptol/infantry_javelineer_b`
  - Ranged "Javelin" — damage 17.6 pierce — range 30 m — prepare 0.4 s — repeat 1.5 s — preferred Human
  - cost 60 metal
  - build time 7 s
