# Turn 035 — A/B diagnosis: seed 293 vs 306

Goal served: G4b — evidence-collection turn (the 301–310 batch mystery).

## Hypothesis

> If I run the winning seed 293 and the failing seed 306 under the identical
> turn-032 assault configuration with sim-side train-command logging, then
> the per-minute dumps will show exactly where the ram chain diverges,
> because turns 033–034 exhausted the economy levers (wood radius, builders,
> repair stall) and the divergence must be something seed-specific in the
> siege chain itself.

Primary metric: the diagnosis (qualitative — the deliverable is the
understanding, written below).

## Implementation

- Restores the turn-032 assault configuration (ram gate 32, 2:1 split,
  workers 1 stone / 2 metal / 1 food, attack at two rams, 30-minute trigger).
- A `bot/simulation/helpers/Commands.js` override logs every train command's
  arrival, CanTrain failures and AddItem failures.

## Experiment

Seeds 293 and 306, sandbox Rome (`--difficulty2 0`), `random/mainland` 128,
`conquest_civic_centers`, treasures disabled, 30 game-minute limit,
biome/placement pinned. Diagnostic runs (no baseline pairing).

## Results

The A/B is decisive. Seed 293 (wins): City completes at minute 22, arsenal
built by 26, ram 1 at 26, 2 rams at 28, attack, win. Seed 306 (draw): City
posts only at minute 24–25 (completes 26), the arsenal foundation lands at
26 and finishes after 30 — one ram trains at ~29–30, too late. The
divergence is **forge timing**: on 306 the wood sits at 20–100 from minute
18 to 20 (soldier training consumes it), so the forges — which need 200
wood each and one placement tick per failed candidate — only complete at
minute 24–25. Everything downstream shifts by the same 3–4 minutes. The
sim-side log confirms no dropped ram commands; the rams simply never get an
arsenal in time.

## Verdict

**Good** (evidence-collection): the question is answered — the batch
difference is the forges competing with training for wood, and the known
fix is turn 023's forges gate (hold training until the 3 forges exist),
now compatible with the turn-029 food fix. The diagnosis is the deliverable;
no code is kept.

## Action

Commit as `turn 035: ab-diagnosis — good` and push. No `CHANGELOG.md`
entry. The next-turn plan goes to `turns/backlog.md`.

## Next

Turn 036: restore the assault configuration plus the **forges gate** (hold
soldier training until the 3 forges are built, then train freely) — the
failing batch's city should land at minute 19–21 like the winning batch,
and the rams follow in time. See `turns/backlog.md`.
