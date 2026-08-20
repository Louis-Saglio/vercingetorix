# military_colony

Buildable by **2** civilisations. Generic (non-civ-specific) building of 0 A.D. 0.28.0 — see `docs/game_description/generic/buildings/README.md` for the method.

Generic stats resolved from the shared template `simulation/templates/template_structure_civic_civil_centre_military_colony` (deepest template common to all civilisation variants; variants may override, see below).

## Basic stats

- **Generic name:** Military Colony
- **Health:** 2000 HP
- **Armor:** 29 hack / 35 pierce / 3 crush
- **Attack:** Ranged "Bow" — damage 8 pierce — range 60 m — prepare 0.4 s — repeat 4 s — preferred Human
- **Cost:** 200 wood, 200 stone, 150 metal
- **Build time:** 300 s
- **Population bonus:** +20
- **Territory influence:** radius 75 m, weight 10000, territory root
- **Garrison:** 20 slots (+1/s heal)
- **Vision:** 90 m
- **Capture points:** 2500
- **Build territory:** own neutral
- **Placement:** land
- **Build distance:** min 120 m from CivilCentre
- **Requirements:** phase_town
- **Trains:** units/{native}/support_civilian
- **Classes:** Structure ConquestCritical CivCentre
- **Visible classes:** Civic Defensive CivilCentre Colony

## Civilisations that can build it

- **ptol** — `structures/ptol/military_colony`
- **sele** — `structures/sele/military_colony`

## Civilisation-specific overrides

These civilisations override the generic stats above (only differing values are listed):

- **ptol** — `structures/ptol/military_colony`
  - trains units/{civ}/infantry_spearman_merc_b units/{civ}/infantry_swordsman_merc_b units/{civ}/cavalry_spearman_merc_b units/{civ}/cavalry_javelineer_merc_b
- **sele** — `structures/sele/military_colony`
  - trains units/{native}/support_civilian units/{civ}/infantry_swordsman_merc_b units/{civ}/infantry_archer_merc_b units/{civ}/cavalry_spearman_merc_b
