# support_civilian

Trained by **15** civilisations. Generic (non-civ-specific) unit of 0 A.D. 0.28.0 — see `docs/game_description/generic_units/README.md` for the method.

Generic stats resolved from the shared template `simulation/templates/template_unit_support_civilian` (deepest template common to all civilisation variants; variants may override, see below).

## Basic stats

- **Generic name:** Civilian
- **Health:** 25 HP
- **Armor:** 1 hack / 1 pierce / 1 crush
- **Attack:** Melee "Dagger" — damage 2 hack — range 3 m — prepare 0.5 s — repeat 1 s
- **Speed:** walk 9 m/s, run 15.03 m/s
- **Vision:** 32 m
- **Cost:** 50 food
- **Build time:** 8 s
- **Population:** 1
- **Classes:** Unit Organic ConquestCritical Human
- **Visible classes:** Support Builder Civilian Worker

## Civilisations that can train it

- **athen** — `units/athen/support_civilian` (civil_centre)
- **brit** — `units/brit/support_civilian` (civil_centre, crannog)
- **cart** — `units/cart/support_civilian` (civil_centre)
- **gaul** — `units/gaul/support_civilian` (civil_centre)
- **germ** — `units/germ/support_civilian` (civil_centre, encampment)
- **han** — `units/han/support_civilian` (civil_centre)
- **iber** — `units/iber/support_civilian` (civil_centre)
- **kush** — `units/kush/support_civilian` (civil_centre)
- **mace** — `units/mace/support_civilian` (civil_centre)
- **maur** — `units/maur/support_civilian` (civil_centre)
- **pers** — `units/pers/support_civilian` (civil_centre)
- **ptol** — `units/ptol/support_civilian` (civil_centre)
- **rome** — `units/rome/support_civilian` (civil_centre)
- **sele** — `units/sele/support_civilian` (civil_centre, military_colony)
- **spart** — `units/spart/support_civilian` (civil_centre)

## Civilisation-specific overrides

These civilisations override the generic stats above (only differing values are listed):

- **spart** — `units/spart/support_civilian`
  - health 35 HP
  - armor 1 hack / 1 pierce / 1 crush
  - Melee "Dagger" — damage 3 hack — range 3 m — prepare 0.5 s — repeat 1 s
  - walk 9 m/s
  - run 15.03 m/s
  - vision 32 m
  - cost 50 food
  - build time 8 s
  - population 1
