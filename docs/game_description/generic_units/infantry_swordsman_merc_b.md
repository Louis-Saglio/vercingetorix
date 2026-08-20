# infantry_swordsman_merc_b

Trained by **2** civilisations. Generic (non-civ-specific) unit of 0 A.D. 0.28.0 — see `docs/game_description/generic_units/README.md` for the method.

Generic stats resolved from the shared template `simulation/templates/template_unit_infantry_melee_swordsman` (deepest template common to all civilisation variants; variants may override, see below).

## Basic stats

- **Generic name:** Swordsman
- **Health:** 100 HP
- **Armor:** 3 hack / 3 pierce / 15 crush
- **Attack:** Melee "Sword" — damage 8 hack — range 3 m — prepare 0.375 s — repeat 0.75 s — preferred Unit+!Ship
- **Speed:** walk 9.5 m/s, run 15.86 m/s
- **Vision:** 80 m
- **Cost:** 50 food, 40 wood, 10 metal
- **Build time:** 10 s
- **Population:** 1
- **Classes:** Unit Organic ConquestCritical Human CitizenSoldier
- **Visible classes:** Builder Citizen Worker Soldier Infantry Melee Swordsman
- **Rank:** Basic

## Civilisations that can train it

- **ptol** — `units/ptol/infantry_swordsman_merc_b` (military_colony)
- **sele** — `units/sele/infantry_swordsman_merc_b` (military_colony)

## Civilisation-specific overrides

These civilisations override the generic stats above (only differing values are listed):

- **ptol** — `units/ptol/infantry_swordsman_merc_b`
  - health 100 HP
  - armor 3 hack / 3 pierce / 15 crush
  - Melee "Sword" — damage 8.8 hack — range 3 m — prepare 0.375 s — repeat 0.75 s — preferred Unit+!Ship
  - walk 9.5 m/s
  - run 15.86 m/s
  - vision 80 m
  - cost 60 metal
  - build time 7 s
  - population 1
- **sele** — `units/sele/infantry_swordsman_merc_b`
  - health 100 HP
  - armor 3 hack / 3 pierce / 15 crush
  - Melee "Rhomphaia" — damage 8.8 hack — range 3 m — prepare 0.375 s — repeat 0.75 s — preferred Unit+!Ship
  - walk 9.5 m/s
  - run 15.86 m/s
  - vision 80 m
  - cost 60 metal
  - build time 7 s
  - population 1
