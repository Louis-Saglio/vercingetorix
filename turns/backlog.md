# Hypothesis backlog

One line per candidate: the change, the primary metric, and the rationale.
Top of the list goes first. Fed by experiment results; never edit an entry
retroactively to match a verdict.

1. **Train civilians at the civil centre continuously** (while food ≥ 50 and
   population room exists) — primary metric: population over time / time to
   reach the 20-pop cap, batch median. Rationale: turn 001 gives income;
   training is the only way to raise population (G1) and each extra civilian
   compounds income. (`support_civilian`: 50 food, 8 s, 1 pop, trained at the
   civil centre.)
2. **Build houses whenever population headroom runs low** — primary metric:
   time to 100 population (G1's metric). Rationale: the civil centre caps at
   20; each gaul house adds 5 for 75 wood, so ≥ 16 houses are required for
   100. Training without housing deadlocks at the cap (training reservations
   block silently, `population_and_entity_limits.md`).
3. **Allocate gatherers by need (food and wood first)** instead of pure
   nearest-supply — primary metric: food income per game-minute in the
   `[HARNESS]` samples. Rationale: turn 001 showed need-blind allocation
   (0 stone/0 metal on several seeds while food is the bottleneck for
   training; wood for houses).
