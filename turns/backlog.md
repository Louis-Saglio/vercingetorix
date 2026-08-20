# Hypothesis backlog

One line per candidate: the change, the primary metric, and the rationale.
Top of the list goes first. Fed by experiment results; never edit an entry
retroactively to match a verdict.

1. **Parallel training: research Fertility Festival, then train from
   houses** — primary metric: time to 100 population (G1 batch median, to
   beat: **13 game-min**). Rationale: the civil centre's single 8 s queue is
   now the rate limiter (≥ 10.7 min for 80+ workers; turn 005 evidence).
   Houses train `support_civilian_house` after `unlock_civilians_house_generic`
   (250 food / 100 wood / 100 metal / 60 s — requirements verified in
   `units/gaul/support_civilian_house.xml`); this reintroduces a small metal
   need. Target: median ≤ 11 min.
2. **Parallel house construction** (place the next house while one is
   building, when wood allows) — primary metric: time to 100 population.
   Rationale: one-house-in-flight paces the cap lift at ~20–30 s per house;
   the cap trailed usage by design in turn 005 (headroom gate) but earlier
   headroom means earlier training room.
3. **Build a storehouse/farmstead near dense woodlines** — primary metric:
   wood income per game-minute. Rationale: travel time dominates late-game
   gathering as near-CC supplies deplete (`resources_and_gathering.md` —
   dropsite distance drives effective rates).
