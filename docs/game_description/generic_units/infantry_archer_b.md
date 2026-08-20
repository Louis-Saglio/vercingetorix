# infantry_archer_b

Trained by **8** civilisations. Generic (non-civ-specific) unit of 0 A.D. 0.28.0 — see `docs/game_description/generic_units/README.md` for the method.

Generic stats resolved from the shared template `simulation/templates/template_unit_infantry_ranged_archer` (deepest template common to all civilisation variants; variants may override, see below).

## Basic stats

- **Generic name:** Archer
- **Health:** 50 HP
- **Armor:** 1 hack / 1 pierce / 10 crush
- **Attack:** Ranged "Bow" — damage 7.2 pierce — range 60 m — prepare 0.8 s — repeat 1.25 s — preferred Human
- **Speed:** walk 10.3 m/s, run 17.2 m/s
- **Vision:** 80 m
- **Cost:** 50 food, 50 wood
- **Build time:** 10 s
- **Population:** 1
- **Classes:** Unit Organic ConquestCritical Human CitizenSoldier
- **Visible classes:** Builder Citizen Worker Soldier Infantry Ranged Archer
- **Rank:** Basic

## Civilisations that can train it

- **athen** — `units/athen/infantry_archer_b` (barracks)
- **cart** — `units/cart/infantry_archer_b` (barracks, civil_centre)
- **han** — `units/han/infantry_archer_b` (barracks)
- **kush** — `units/kush/infantry_archer_b` (barracks, civil_centre)
- **mace** — `units/mace/infantry_archer_b` (barracks)
- **maur** — `units/maur/infantry_archer_b` (barracks, civil_centre)
- **pers** — `units/pers/infantry_archer_b` (barracks, civil_centre)
- **ptol** — `units/ptol/infantry_archer_b` (barracks)

## Civilisation-specific overrides

These civilisations override the generic stats above (only differing values are listed):

- **athen** — `units/athen/infantry_archer_b`
  - Ranged "Bow" — damage 7.92 pierce — range 60 m — prepare 0.8 s — repeat 1.25 s — preferred Human
  - cost 60 metal
  - build time 7 s
- **mace** — `units/mace/infantry_archer_b`
  - Ranged "Bow" — damage 7.92 pierce — range 60 m — prepare 0.8 s — repeat 1.25 s — preferred Human
  - cost 60 metal
  - build time 7 s
- **ptol** — `units/ptol/infantry_archer_b`
  - Ranged "Bow" — damage 7.92 pierce — range 60 m — prepare 0.8 s — repeat 1.25 s — preferred Human
  - cost 60 metal
  - build time 7 s
