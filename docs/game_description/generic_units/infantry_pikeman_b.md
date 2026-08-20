# infantry_pikeman_b

Trained by **5** civilisations. Generic (non-civ-specific) unit of 0 A.D. 0.28.0 — see `docs/game_description/generic_units/README.md` for the method.

Generic stats resolved from the shared template `simulation/templates/template_unit_infantry_melee_pikeman` (deepest template common to all civilisation variants; variants may override, see below).

## Basic stats

- **Generic name:** Pikeman
- **Health:** 100 HP
- **Armor:** 5 hack / 5 pierce / 15 crush
- **Attack:** Melee "Pike" — damage 4 hack + 7.5 pierce — range 8 m — prepare 1 s — repeat 2 s — bonus 2.5× vs Cavalry — preferred Human
- **Speed:** walk 8.55 m/s, run 14.28 m/s
- **Vision:** 80 m
- **Cost:** 50 food, 50 wood
- **Build time:** 10 s
- **Population:** 1
- **Classes:** Unit Organic ConquestCritical Human CitizenSoldier
- **Visible classes:** Builder Citizen Worker Soldier Infantry Melee Pikeman
- **Rank:** Basic

## Civilisations that can train it

- **han** — `units/han/infantry_pikeman_b` (barracks)
- **kush** — `units/kush/infantry_pikeman_b` (barracks)
- **mace** — `units/mace/infantry_pikeman_b` (barracks, civil_centre)
- **ptol** — `units/ptol/infantry_pikeman_b` (barracks, civil_centre)
- **sele** — `units/sele/infantry_pikeman_b` (barracks)

## Civilisation-specific overrides

These civilisations override the generic stats above (only differing values are listed):

- **han** — `units/han/infantry_pikeman_b`
  - health 100 HP
  - armor 3 hack / 3 pierce / 15 crush
  - Melee "Ji" — damage 10 hack + 3.5 pierce — range 8 m — prepare 1 s — repeat 2 s — bonus 2.5× vs Cavalry — preferred Human
  - walk 8.55 m/s
  - run 14.28 m/s
  - vision 80 m
  - cost 50 food, 50 wood
  - build time 10 s
  - population 1
