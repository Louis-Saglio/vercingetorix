# infantry_slinger_b

Trained by **7** civilisations. Generic (non-civ-specific) unit of 0 A.D. 0.28.0 — see `docs/game_description/generic/units/README.md` for the method.

Generic stats resolved from the shared template `simulation/templates/template_unit_infantry_ranged_slinger` (deepest template common to all civilisation variants; variants may override, see below).

## Basic stats

- **Generic name:** Slinger
- **Health:** 50 HP
- **Armor:** 1 hack / 1 pierce / 10 crush
- **Attack:** Capture — strength 2.5 — range 4 m — repeat 1 s — restricted Field Palisade Wall
- **Attack:** Ranged "Sling" — damage 11.5 pierce + 1.1 crush — range 45 m — prepare 0.4 s — repeat 1.5 s — preferred Human
- **Speed:** walk 10.8 m/s, run 18.04 m/s
- **Vision:** 80 m
- **Cost:** 50 food, 20 wood, 30 stone
- **Build time:** 10 s
- **Population:** 1
- **Gather:** rates: food: fruit 0.5, grain 0.25, meat 1; wood: tree 0.75, ruins 5; stone: rock 0.5, ruins 2; metal: ore 0.5, ruins 2 /s
- **Gather:** capacity: 10 food, 10 wood, 10 stone, 10 metal
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

## Ranks

### Advanced — `units/{civ}/infantry_slinger_a`
Requires 100 XP.
- Health: ×1.25 → 62.5 HP
- Capture strength: +0.7 → 3.2
- Build time: ×1.2 → 12 s
- Gather base speed: ×0.7 → 0.7
- Loot: ×1.2
- Ranged spread: ×0.8

### Elite — `units/{civ}/infantry_slinger_e`
Requires 100 XP.
- Health: ×1.25 (total ×1.56) → 78.13 HP
- Capture strength: +0.8 (total +1.5) → 4
- Build time: ×1.2 (total ×1.44) → 14.4 s
- Gather base speed: ×0.7 (total ×0.49) → 0.49
- Loot: ×1.2 (total ×1.44)
- Ranged spread: ×0.8 (total ×0.64)

- Note: mercenary variants promote at 0 XP (the auto-researched `upgrade_rank_advanced_mercenary` tech replaces RequiredXp with 0).


## Civilisation-specific overrides

These civilisations override the generic stats above (only differing values are listed):

- **mace** — `units/mace/infantry_slinger_b`
  - Capture — strength 2.5 — range 4 m — repeat 1 s — restricted Field Palisade Wall
  - Ranged "Sling" — damage 12.65 pierce + 1.21 crush — range 45 m — prepare 0.4 s — repeat 1.5 s — preferred Human
  - cost 60 metal
  - build time 7 s
