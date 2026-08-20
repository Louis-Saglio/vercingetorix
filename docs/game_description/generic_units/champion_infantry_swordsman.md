# champion_infantry_swordsman

Trained by **7** civilisations. Generic (non-civ-specific) unit of 0 A.D. 0.28.0 — see `docs/game_description/generic_units/README.md` for the method.

Generic stats resolved from the shared template `simulation/templates/template_unit_champion_infantry_swordsman` (deepest template common to all civilisation variants; variants may override, see below).

## Basic stats

- **Generic name:** Champion Swordsman
- **Health:** 200 HP
- **Armor:** 6 hack / 6 pierce / 20 crush
- **Attack:** Melee "Sword" — damage 16 hack — range 3 m — prepare 0.375 s — repeat 0.75 s — preferred Unit+!Ship
- **Speed:** walk 9.5 m/s, run 15.86 m/s
- **Vision:** 80 m
- **Cost:** 80 food, 60 wood, 80 metal
- **Build time:** 20 s
- **Population:** 1
- **Classes:** Unit Organic ConquestCritical Human
- **Visible classes:** Soldier Champion Infantry Melee Swordsman

## Civilisations that can train it

- **brit** — `units/brit/champion_infantry_swordsman` (barracks)
- **gaul** — `units/gaul/champion_infantry_swordsman` (barracks)
- **iber** — `units/iber/champion_infantry_swordsman` (barracks)
- **mace** — `units/mace/champion_infantry_swordsman` (barracks)
- **rome** — `units/rome/champion_infantry_swordsman` (barracks)
- **sele** — `units/sele/champion_infantry_swordsman` (barracks)
- **spart** — `units/spart/champion_infantry_swordsman` (barracks)

## Civilisation-specific overrides

These civilisations override the generic stats above (only differing values are listed):

- **mace** — `units/mace/champion_infantry_swordsman`
  - Melee "Rhomphaia" — damage 10 hack — range 5 m — prepare 0.5 s — repeat 1 s — preferred Unit+!Ship
- **spart** — `units/spart/champion_infantry_swordsman`
  - health 100 HP
  - armor 5 hack / 5 pierce / 15 crush
  - Melee "Sword" — damage 9.5 hack — range 3 m — prepare 0.375 s — repeat 0.75 s — preferred Unit+!Ship
  - cost 50 food, 40 wood, 35 metal
  - build time 10 s
