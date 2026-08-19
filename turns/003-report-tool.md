# Turn 003 — Report tool (composite verdict + canary)

Goal served: none directly — prerequisite tooling. The composite score is the
mechanism every future turn uses to grade hypotheses (and G1 uses it for its
per-match grading data).

## Hypothesis

Prerequisite turn (acceptance criteria, framed as a hypothesis — same pattern
as turn 002):

> If I add a `report` subcommand to the harness that implements the protocol's
> verdict rules — paired outcome component (win +3 / draw +1 / loss 0, delta vs
> baseline), quality component (0.4-weighted clamped relative deltas for
> resourcesGathered, resourcesUsed, enemyUnitsKilled, unitsTrained, population
> peak), survival component (0.4-weighted clamped duration delta, only on
> loss–loss and draw–draw pairs), draw semantics (all active players marked won
> at the game-time limit → draw), the JS-error veto, and the canary identity
> check — then (a) comparing the committed turn-002 baseline against itself
> yields exactly 0 on every component and a neutral verdict, (b) the synthetic
> unit tests reproduce every deliberate difference (outcome flips, metric
> clamping, veto, canary mismatch), and (c) a live canary re-run of one seed
> passes the identity check, proving the verdict machinery correct before any
> real hypothesis depends on it.

Primary metric: tool correctness — all unit tests pass, self-comparison is
all-zero, live canary passes. No bot metric (no bot change this turn).

## Implementation

`harness` gains a `report` subcommand (new module `harness/src/report.rs`,
pure scoring logic + thin IO entry):

```
harness report --baseline PATH [--treatment PATH] [--canary PATH] [--out DIR]
```

- `--baseline` required; `--treatment` and `--canary` optional. Writes
  `report.md` into `--out` (default current dir) and prints a compact summary.
- Pairs matches by seed; baseline and treatment must have identical seed sets
  (else error). Canary seeds must exist in the baseline.
- Draw semantics: exactly one player "won" and the other "defeated" → win/loss
  from player 1's (the bot's) perspective; all players "won" or all
  "defeated" → draw; anything else is a hard error, not a guess.
- Quality scalarizations (justified by the 0.28 engine source
  `StatisticsTracker.js` and the data in `experiments/002/`):
  - resourcesGathered → sum of food + wood + metal + stone (`vegetarianFood` is
    a subset of food — the GUI counters skip it to avoid double counting).
  - resourcesUsed → sum of food + wood + metal + stone.
  - enemyUnitsKilled → `enemyUnitsKilledValue` (the per-class counters overlap
    — one unit lands in several class buckets — and `total` is broken in 0.28:
    it is initialized but never incremented for lost/killed).
  - unitsTrained → `unitsTrained.total` (explicitly incremented per source).
  - population peak → max of the `pop` numerator across the bot's per-minute
    `[HARNESS]` samples. A metric missing on either side is skipped.
  - Phase timings: not implemented — the bot does not report phases yet; they
    join the tool in the same turn that introduces the reporting (protocol:
    extend evidence tools with the collection).
- Verdict: batch total ≥ +4 → good; ≤ −4 → bad; else neutral. Any pair with
  treatment js_errors > baseline js_errors → bad (error veto). Canary mismatch
  → invalid.
- Canary identity: the canary match must equal the baseline match with the same
  seed on `command` (settings template), `exit`, `turns`, `players` (stats
  blocks), `harness_lines`, and `js_errors`. `wall_seconds` and `stderr` are
  excluded (wall-clock noise and pid/timestamp-specific paths).

## Experiment

1. **Synthetic:** `cargo test` — 15/15 pass; clippy pedantic clean.
2. **Self-comparison:** baseline vs baseline → every component 0, verdict
   neutral, all 10 pairs classified as draws (correct — turn 002's matches all
   hit the time limit). ✓
3. **Live canary:** FAILED, and the diagnosis is the turn's main finding:

   - Same seed + identical settings did not reproduce. First cause found in the
     replay manifests: `random/mainland` drew an **unseeded random biome** per
     run (the autostart default is `"random"`, picked in the GUI realm) — fixed
     by pinning `-autostart-biome=generic/temperate` in the harness command.
   - With the biome pinned, runs were still only *sometimes* identical
     (2/4 identical at seed 5). A vercingetorix-vs-vercingetorix batch (no
     Petra, both AIs deterministic pure functions of the sim state) diverged at
     game-minute 1 the same way → the nondeterminism is in the **engine**, not
     the bots.
   - **Wrong theory, recorded for honesty:** source reading pointed at an
     upstream 0.28.0 data race in `CCmpPathfinder`'s async path batching
     (futures vs `PrepareForComputation`), and an RL-paced runner
     (`-rl-interface`, one turn per `POST /step`) was built to sidestep it.
     That theory is **refuted**: the RL-paced checks were themselves
     intermittent (seed 5 passed, seed 17 failed), and once the real cause
     was pinned, *unpaced* runs reproduce bit-identically — which the race
     theory would forbid. The RL machinery was removed before the commit
     (Louis's direction).
   - **Bot exonerated (Louis's hypothesis tested):** four petra-vs-petra
     matches of seed 5 with identical settings (Seed 5, AISeed 0, biome
     pinned — verified in the replay manifests) also diverged: 2/4 identical
     pairs, and one run even flipped the whole outcome (player 1 conquered at
     turn 5115 vs time-limit draws at 6000 in the others). Vercingetorix is
     not in these matches at all.
   - **Real second cause: unseeded player placement.** With the biome
     pinned, same-seed probe runs still produced different maps, and their
     replay manifests showed `"PlayerPlacement": "circle"` vs
     `"randomGroup"` — the gamesetup default is `"random"`, resolved per run
     in the unseeded GUI realm, and the mainland script places the bases
     from it. Pinned `-autostart-placement=circle` in the harness command.
     This explains all the intermittency: runs whose biome+placement draws
     coincided were identical; the rest diverged.
   - **Acceptance results (final):** with both pins, the **unpaced canary
     PASSES** — seeds 5, 17, 19 (same seed twice, every deterministic field
     identical). The canary is the per-batch gate. (The interim RL-paced
     `determinism` subcommand also passed post-pin on seeds 5, 17, 17 before
     being removed per Louis's direction.)

   The canary did exactly its job: it exposed two unseeded gamesetup inputs
   that broke reproduction, and the fix is two pinned flags. Full story in
   `docs/ENGINE_BUG_0AD_0.28_NONDETERMINISM.md`.

## Verdict

**Good** (prereq fulfilled). Acceptance criteria: (a) self-comparison
all-zero/neutral ✓, (b) 15/15 synthetic tests ✓, (c) live identity check —
the unpaced canary now passes on three seeds with the settings pinned ✓.
The turn also delivered: biome + placement pinning, the canary gate, and
the protocol/docs updates describing all of it.

## Action

Commit as `turn 003: report-tool — good` (report tool + settings pins +
canary determinism gate + docs), then push.

## Next

Real hypotheses against the turn-002 baseline, graded on goal G1 (economy
boot) — first candidates in `turns/backlog.md`.

