# defense_tower

Buildable by **15** civilisations. Generic (non-civ-specific) building of 0 A.D. 0.28.0 — see `docs/game_description/generic_buildings/README.md` for the method.

Generic stats resolved from the shared template `simulation/templates/template_structure_defensive_tower_stone` (deepest template common to all civilisation variants; variants may override, see below).

## Basic stats

- **Generic name:** Stone Tower
- **Health:** 1000 HP
- **Armor:** 29 hack / 35 pierce / 3 crush
- **Attack:** Ranged "Bow" — damage 8 pierce — range 60 m — prepare 0.4 s — repeat 3.5 s — preferred Human
- **Cost:** 100 wood, 100 stone
- **Build time:** 150 s
- **Territory influence:** radius 32 m, weight 30000
- **Garrison:** 5 slots
- **Vision:** 80 m
- **Capture points:** 500
- **Build territory:** own
- **Placement:** land
- **Build distance:** min 60 m from Tower
- **Requirements:** phase_town
- **Classes:** Structure
- **Visible classes:** Defensive Tower StoneTower

## Civilisations that can build it

- **athen** — `structures/athen/defense_tower`
- **brit** — `structures/brit/defense_tower`
- **cart** — `structures/cart/defense_tower`
- **gaul** — `structures/gaul/defense_tower`
- **germ** — `structures/germ/defense_tower`
- **han** — `structures/han/defense_tower`
- **iber** — `structures/iber/defense_tower`
- **kush** — `structures/kush/defense_tower`
- **mace** — `structures/mace/defense_tower`
- **maur** — `structures/maur/defense_tower`
- **pers** — `structures/pers/defense_tower`
- **ptol** — `structures/ptol/defense_tower`
- **rome** — `structures/rome/defense_tower`
- **sele** — `structures/sele/defense_tower`
- **spart** — `structures/spart/defense_tower`

## Civilisation-specific overrides

These civilisations override the generic stats above (only differing values are listed):

- **iber** — `structures/iber/defense_tower`
  - health 2400 HP
  - Ranged "Bow" — damage 8 pierce — range 60 m — prepare 0.4 s — repeat 3.5 s — preferred Human
  - cost 50 wood, 250 stone
  - build time 200 s
  - territory radius 38 m, weight 30000
  - garrison 8 slots
