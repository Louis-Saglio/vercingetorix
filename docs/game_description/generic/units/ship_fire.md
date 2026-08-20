# ship_fire

Trained by **4** civilisations. Generic (non-civ-specific) unit of 0 A.D. 0.28.0 — see `docs/game_description/generic/units/README.md` for the method.

Generic stats resolved from the shared template `simulation/templates/template_unit_ship_fire` (deepest template common to all civilisation variants; variants may override, see below).

## Basic stats

- **Generic name:** Fire Ship
- **Health:** 800 HP
- **Armor:** 5 hack / 1 pierce / 3 crush
- **Attack:** Melee "Flames" — range 15 m — prepare 0.1 s — repeat 0.8 s — bonus 3× vs Ship Building — preferred Ship
- **Speed:** walk 16 m/s, run 26.72 m/s
- **Vision:** 80 m
- **Cost:** 100 wood, 50 metal
- **Build time:** 18 s
- **Population:** 1
- **Classes:** Unit ConquestCritical
- **Visible classes:** Ship Warship Fireship Melee

## Civilisations that can train it

- **brit** — `units/brit/ship_fire` (crannog, dock)
- **gaul** — `units/gaul/ship_fire` (dock)
- **germ** — `units/germ/ship_fire` (dock)
- **iber** — `units/iber/ship_fire` (dock)
