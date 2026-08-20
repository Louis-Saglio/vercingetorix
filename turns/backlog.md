# Hypothesis backlog

One line per candidate: the change, the primary metric, and the rationale.
Top of the list goes first. Fed by experiment results; never edit an entry
retroactively to match a verdict.

1. **Restore house building** (turn 003's reverted code, from its commit) —
   primary metric: time to 100 population; same experiment design and the
   same ≥ 6/10 threshold as turn 003. Rationale: the mechanism is proven
   (limit rose in 10/10, composite +14.90); it was reverted only because the
   food prerequisite was missing. Turn 004 fixed that (+112 % food income);
   100 pop in 20 min should now be reachable.
2. **Parallel training: research Fertility Festival, then train from
   houses** — primary metric: time to 100 population. Rationale: G1's 90+
   workers through the civil centre's single 8 s queue cost ≥ 12 min serial;
   houses train `support_civilian_house` but only after
   `unlock_civilians_house_generic` (250 food / 100 wood / 100 metal / 60 s —
   verified in `units/gaul/support_civilian_house.xml` requirements), so this
   also reintroduces a small metal need.
