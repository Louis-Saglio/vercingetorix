# Turn 011 — Save food/wood for Town research

Goal served: G3 (defeat sandbox Rome, via the siege path).

## Hypothesis

> If I make the bot hold soldier training until Town Phase is researched (so the
> 500 food / 500 wood can accumulate instead of being spent on soldiers), then
> the bot reaches Town Phase on most seeds, because the resource-savings fix
> removes the failure mode from turn 010.

Primary metric: fraction of seeds where the bot reaches Town Phase by the
20-minute limit (0 JS errors).

Verdict thresholds (pre-registered): good if ≥ 8/10 seeds reach Town Phase with
0 JS errors and canary PASS; bad if ≤ 2/10 or error/determinism veto; neutral
otherwise.

## Implementation

Re-adds turn 010's Town research and adds the resource-saving gate:

- `townResearched` serialized flag + `manageResearch(gameState, cc)` (research
  a `phase_town*` tech once food ≥ 500 and wood ≥ 500).
- In `manageSoldiers`, soldier training is gated on `this.townResearched`, so
  wood is no longer spent on soldiers before the research is paid.
- `"town"` added to the per-minute `[HARNESS]` sample.

## Experiment

Settings: seeds 101–110 (fresh), sandbox Rome (`--difficulty2 0`),
`random/mainland` 128, `conquest_civic_centers`, treasures disabled, 20
game-minute limit, biome/placement pinned. Baseline = HEAD (turn-008 code);
treatment = save-for-Town; canary = seed 101.

Results:

- Canary: **PASS**.
- Town reached: baseline **0/10**, treatment **10/10**.
- 0 JS errors in all matches.
- Composite: −2.14 (neutral) — irrelevant to the primary metric; the change
  delays the army but achieves the phase prerequisite.

## Verdict

**Good** (pre-registered single metric): 10/10 ≥ 8/10, 0 JS errors, canary
PASS. The change is kept.

## Action

Keep the change. Commit as `turn 011: save-for-town — good` and push.
`docs/CHANGELOG.md` gets an entry.

## Next

Town Phase is now reached reliably. Next: gather stone and metal so the bot can
eventually afford City Phase (750 stone + 750 metal).
