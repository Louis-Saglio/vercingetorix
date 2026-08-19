# Turn 014 — Cache resource collections (perf refactor)

Goal served: none directly — performance budget (protocol hard rule 9).

## Hypothesis

> If I replace the per-play-tick full-map `getEntities()` resource scan with
> auto-maintained `updatingGlobalCollection` caches for wood and food, then
> same-seed matches stay bit-identical and the turn rate does not drop, because
> the change only swaps how resource lists are produced, not which entities are
> gathered.

Primary metric: behavior preservation — treatment matches equal baseline matches
on all deterministic fields (canary-style check), 0 JS errors, and mean wall
time not materially worse.

## Implementation

In `bot/simulation/ai/vercingetorix/vercingetorix.js` `play()`:

- Replaced the `gameState.getEntities().values()` full-map scan with two
  `gameState.updatingGlobalCollection(...)` caches (`resource-wood`,
  `resource-food`) whose filters select by `getResourceType()`.
- Ownership, position, and 160 m distance filters are unchanged.

## Experiment

Settings: seeds 131–140 (fresh), sandbox Rome (`--difficulty2 0`),
`random/mainland` 128, `conquest_civic_centers`, treasures disabled, 20
game-minute limit, biome/placement pinned. Baseline = HEAD (turn-011 code);
treatment = cached resource collections.

Results:

- Behavior preservation: `harness report --baseline baseline.json --canary
  treatment.json` → **canary PASS** (all 10 seeds bit-identical on deterministic
  fields).
- 0 JS errors.
- Mean wall time: baseline 16.0 s → treatment 15.5 s (no regression).

## Verdict

**Good** (refactor). Behavior preserved bit-for-bit, no new JS errors, turn rate
not worse. The change is kept.

## Action

Keep the change. Commit as `turn 014: perf-cached-resources — good` and push.
`docs/CHANGELOG.md` gets an entry.

## Next

G3 still needs reconsideration after five failed attempts. See `turns/backlog.md`.
