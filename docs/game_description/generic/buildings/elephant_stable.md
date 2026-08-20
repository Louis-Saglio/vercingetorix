# elephant_stable

Buildable by **6** civilisations. Generic (non-civ-specific) building of 0 A.D. 0.28.0 — see `docs/game_description/generic/buildings/README.md` for the method.

Generic stats resolved from the shared template `simulation/templates/template_structure_military_elephant_stable` (deepest template common to all civilisation variants; variants may override, see below).

## Guide

The Elephant Stable is the City-phase production building for elephant units: it trains support elephants, elephant archers and champion elephants, and researches elephant technologies. Build it only if your civilisation is on the list below (6 civilisations) and you intend to field elephants — at 200 wood + 200 stone and 180 s build time it is a moderate investment with no other purpose. It has the ConquestCritical class, so losing it counts toward defeat in conquest-type victories; its 5 garrison slots and high pierce armor (35) give it some resilience.

## Basic stats

- **Generic name:** Elephant Stable
- **Health:** 3000 HP
- **Armor:** 24 hack / 35 pierce / 3 crush
- **Cost:** 200 wood, 200 stone
- **Build time:** 180 s
- **Territory influence:** radius 38 m, weight 40000
- **Garrison:** 5 slots
- **Vision:** 40 m
- **Capture points:** 500
- **Build territory:** own
- **Placement:** land
- **Requirements:** phase_city
- **Trains:** units/{civ}/support_elephant units/{civ}/elephant_archer_b units/{civ}/champion_elephant
- **Classes:** Structure ConquestCritical
- **Visible classes:** Military City ElephantStable

## Civilisations that can build it

- **cart** — `structures/cart/elephant_stable`
- **kush** — `structures/kush/elephant_stable`
- **maur** — `structures/maur/elephant_stable`
- **pers** — `structures/pers/elephant_stable`
- **ptol** — `structures/ptol/elephant_stable`
- **sele** — `structures/sele/elephant_stable`
