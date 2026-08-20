# corral

Buildable by **15** civilisations. Generic (non-civ-specific) building of 0 A.D. 0.28.0 — see `docs/game_description/generic/buildings/README.md` for the method.

Generic stats resolved from the shared template `simulation/templates/template_structure_resource_corral` (deepest template common to all civilisation variants; variants may override, see below).

## Basic stats

- **Generic name:** Corral
- **Health:** 500 HP
- **Armor:** 1 hack / 20 pierce / 1 crush
- **Cost:** 100 wood
- **Build time:** 50 s
- **Territory influence:** radius 20 m, weight 30000
- **Garrison:** 8 slots (+1/s heal)
- **Vision:** 20 m
- **Capture points:** 500
- **Build territory:** own
- **Placement:** land
- **Requirements:** phase_village
- **Trains:** gaia/fauna_goat_trainable gaia/fauna_sheep_trainable gaia/fauna_pig_trainable gaia/fauna_cattle_cow_trainable
- **Classes:** Structure
- **Visible classes:** Resource Economic Village Corral

## Civilisations that can build it

- **athen** — `structures/athen/corral`
- **brit** — `structures/brit/corral`
- **cart** — `structures/cart/corral`
- **gaul** — `structures/gaul/corral`
- **germ** — `structures/germ/corral`
- **han** — `structures/han/corral`
- **iber** — `structures/iber/corral`
- **kush** — `structures/kush/corral`
- **mace** — `structures/mace/corral`
- **maur** — `structures/maur/corral`
- **pers** — `structures/pers/corral`
- **ptol** — `structures/ptol/corral`
- **rome** — `structures/rome/corral`
- **sele** — `structures/sele/corral`
- **spart** — `structures/spart/corral`

## Civilisation-specific overrides

These civilisations override the generic stats above (only differing values are listed):

- **cart** — `structures/cart/corral`
  - trains gaia/fauna_goat_trainable gaia/fauna_sheep_trainable gaia/fauna_pig_trainable gaia/fauna_cattle_sanga_trainable
- **han** — `structures/han/corral`
  - trains gaia/fauna_goat_trainable gaia/fauna_pig_trainable gaia/fauna_cattle_cow_trainable gaia/fauna_cattle_zebu_trainable
- **kush** — `structures/kush/corral`
  - trains gaia/fauna_goat_trainable gaia/fauna_sheep_trainable gaia/fauna_pig_trainable gaia/fauna_cattle_sanga_trainable
- **maur** — `structures/maur/corral`
  - trains gaia/fauna_goat_trainable gaia/fauna_sheep_trainable gaia/fauna_pig_trainable gaia/fauna_cattle_zebu_trainable
- **ptol** — `structures/ptol/corral`
  - trains gaia/fauna_goat_trainable gaia/fauna_sheep_trainable gaia/fauna_pig_trainable gaia/fauna_cattle_sanga_trainable
