# infantry_slinger_b

Trained by **7** civilisations. Generic (non-civ-specific) unit of 0 A.D. 0.28.0 — see `docs/game_description/generic_units/README.md` for the method.

Generic stats resolved from the shared template `simulation/templates/template_unit_infantry_ranged_slinger` (deepest template common to all civilisation variants; variants may override, see below).

## Basic stats

- **Generic name:** Slinger
- **Health:** 50 HP
- **Armor:** 1 hack / 1 pierce / 10 crush
- **Attack:** Ranged "Sling" — damage 11.5 pierce + 1.1 crush — range 45 m — prepare 0.4 s — repeat 1.5 s — preferred Human
- **Speed:** walk 10.8 m/s, run 18.04 m/s
- **Vision:** 80 m
- **Cost:** 50 food, 20 wood, 30 stone
- **Build time:** 10 s
- **Population:** 1
- **Classes:** Unit Organic ConquestCritical Human CitizenSoldier
- **Visible classes:** Builder Citizen Worker Soldier Infantry Ranged Slinger
- **Rank:** Basic

## Civilisations that can train it

- **athen** — `units/athen/infantry_slinger_b` (barracks, civil_centre)
- **brit** — `units/brit/infantry_slinger_b` (barracks, civil_centre, crannog)
- **gaul** — `units/gaul/infantry_slinger_b` (barracks)
- **germ** — `units/germ/infantry_slinger_b` (barracks, civil_centre, encampment)
- **iber** — `units/iber/infantry_slinger_b` (barracks)
- **mace** — `units/mace/infantry_slinger_b` (barracks)
- **ptol** — `units/ptol/infantry_slinger_b` (barracks, civil_centre)

## Civilisation-specific overrides

These civilisations override the generic stats above (only differing values are listed):

- **mace** — `units/mace/infantry_slinger_b`
  - Ranged "Sling" — damage 12.65 pierce + 1.21 crush — range 45 m — prepare 0.4 s — repeat 1.5 s — preferred Human
  - cost 60 metal
  - build time 7 s
