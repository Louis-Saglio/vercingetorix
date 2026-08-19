# Vercingetorix Development Protocol

**Goal:** improve Vercingetorix — a rule-based 0 A.D. AI bot written as an in-engine
JavaScript mod — until it reliably beats Petra at increasing difficulty levels,
using evidence-driven development cycles.

All work happens in **turns**. One turn = one hypothesis, tested by one experiment,
closed by one verdict and exactly one commit (pushed to GitHub).

## Long-term goals and grading

Development is organized around **goals** that span many turns. `GOALS.md` holds the
current goal, its grading scale, and its status. Each turn states which goal it
serves and grades its experiment against the goal's scale — a turn can be
goal-positive even when its verdict is neutral. When a goal is achieved, define the
next goal and its grading system in the same commit that closes the goal.

**If a goal resists several turns of effort, reconsider it before grinding further:**
maybe it is too ambitious, or not achievable before some other goal. Adjust the
goal (split it, reorder it, or replace it) in `GOALS.md` with a note explaining
why — that is a legitimate outcome of evidence, not a failure.

## Turn types

- **Improvement turn** (default): a hypothesis about making the bot better.
- **Evidence-collection turn**: the hypothesis is "if I collect data D, then I will
  understand Y well enough to formulate a bot improvement". The deliverable is a
  commit containing **both** (a) the code that improves evidence collection during
  experiments, and (b) the understanding gained after re-running the experiment with
  the new evidence system — written in the turn record so every future experiment
  benefits from it. Verdict = did the evidence answer the question (yes/no).
  Evidence may be logs in the bot or anywhere in the simulation.
- **Refactor turn**: the hypothesis is "if I restructure R, the code becomes easier to
  change safely, with identical behavior". The verdict is a behavior-preservation
  check: same seed → identical outcomes and statistics as before the refactor, and no
  new JS errors. Use refactor turns when the code is getting messy or when a
  structural change is needed to enable real improvements — never let structure rot.

## The turn

1. **Hypothesis** — written in the turn file *before any code changes*:

   > If I change X, then metric M improves, because Z.

   The hypothesis must name the change (X), the primary metric (M), the experiment
   that tests it, and the verdict thresholds.
2. **Implement** — make the minimal code change for X. **Every implementation adds
   evidence collection for its own effect**: instrumentation that shows, during the
   experiment, whether the change did what it was supposed to (samples, logs, states
   of the affected subsystem). A change that cannot be observed is not implemented.
3. **Experiment** — run the baseline (last commit) and the treatment (working tree)
   on the same seed set; record every match result in `experiments/NNN/`.
4. **Verdict** — apply the decision rules below to the primary metric.
   Possible verdicts: **good**, **bad**, **neutral**, **invalid**.
5. **Action**:
   - **good** → validate: keep the change.
   - **bad** → revert the change.
   - **neutral** → collect more evidence: repeat the batch once (doubled N).
     Still neutral after that → revert and record the negative knowledge.
   - **invalid** (the experiment design or the implementation was wrong, not the
     idea) → fix the experiment, rerun it against the original code, and state
     plainly in the journal what went wrong.
6. **Commit and push** — every turn ends with exactly one commit, regardless of
   verdict: `turn NNN: <slug> — <verdict>` with the journal summary as the body,
   followed by `git push` to the GitHub remote (repo:
   https://github.com/Louis-Saglio/vercingetorix). This single commit includes all
   of the turn's bookkeeping — the turn record, `turns/backlog.md`, `CURRENT_TURN.md`,
   and any `docs/CHANGELOG.md` / `docs/GOALS.md` updates and experiment results. Do
   **not** make a separate backlog/closure commit after the turn commit.
7. **Post-turn reflection** — before launching the next turn, ask: did anything in
   this turn reveal a problem or a missing capability in the harness or in this
   protocol itself? If yes, make those improvements **now**, in a separate commit
   (pushed), then launch the next turn. Examples: a metric the harness does not
   extract, a verdict rule that misjudged an obvious result, an experiment default
   that got in the way, a missing evidence-exploration tool.
8. **Next turn** — take the top item from `turns/backlog.md`, or derive a new
   hypothesis from the last results (including from evidence-collection turns).

## Hard rules

1. **One change per turn.** If a change needs several parts, split it into several turns.
2. **Hypothesis before code.** Never adjust the metric or the thresholds after seeing
   results — that would make the verdict meaningless. A badly designed experiment is
   marked invalid, not re-interpreted.
3. **Determinism gate.** Every commit must reproduce identically: the per-batch
   canary (same seed twice) must be identical. A change that breaks
   determinism is **bad** regardless of metrics. The settings pins are part
   of this: biome and player placement MUST stay fixed — their gamesetup
   defaults are unseeded `"random"` (see
   `docs/ENGINE_BUG_0AD_0.28_NONDETERMINISM.md`).
4. **Error veto.** A change that increases the bot's JS error count is **bad**
   regardless of metrics.
5. **Minimal diffs.** No refactoring, no formatting, no unrelated fixes inside a turn
   (refactors are their own turn type).
6. **Baseline = last commit.** Never compare against a stale baseline.
7. **Only validated improvements persist.** Reverted turns leave no trace in the code,
   only in the journal.
8. **Telemetry is mandatory.** The bot emits a `[HARNESS]` sample line every game
   minute (unit counts, resources, states — whatever the current goal grades). These
   samples are how the agent checks mid-experiment whether a run is going well or
   should be aborted early to avoid wasting time. Kill clearly-failing runs.
9. **Performance budget.** The AI must not slow down the simulation. No full-map
   entity scans per play tick, no re-allocating large collections every tick, no
   quadratic work over entities. Prefer cached collections, the shared resource
   maps, and the existing turn throttle. If in doubt, measure: the turn rate
   (turns per wall-second in the match result) must not drop materially versus the
   baseline. Optimizations that preserve behavior get their own commit; a
   performance regression in a turn counts against the verdict like a metric
   regression.

## Experiment specification (defaults)

- **Bot:** Vercingetorix, player 1, civ `gaul`.
- **Opponent:** Petra, player 2, civ `rome`, difficulty 3. Raise the difficulty when
  the bot's win rate is ≥ 80% over the last 10 turns at the current level.
- **Map:** `random/mainland`, size 128.
- **Victory condition:** `conquest_civic_centers` (destroy all enemy civic
  centres). **Treasures are disabled** (forced by the bot mod's autostart
  override) so random treasure windfalls cannot influence results.
- **Seeds:** every turn draws its own seed set (default 10 seeds) and records it in
  the turn file. Baseline and treatment always share the turn's seed set (paired
  comparison). Seed sets are never reused across turns — this is the anti-overfitting
  measure.
- **Canary match:** every batch additionally runs one match that repeats the baseline
  exactly (same civ, same seed as an existing baseline match). Its result must be
  identical to the original baseline run; if not, the batch is invalid and the
  harness has a bug to fix before any verdict. The canary only passes because
  the harness pins the biome and the player placement (see rule 3).
- **Match limit:** 20 minutes of **game time** (default, tunable per turn — see
  below). The bot mod ships a trigger (`bot/maps/scripts/NonVisualTrigger.js`) that
  ends the match at the limit, marking all active players won and printing the full
  per-player statistics; the report tool reads that combination as a **draw**. The
  harness's wall-clock timeout is only a safety net (set it generously, e.g. 3-4x the
  expected wall time).
- **Timeout flexibility:** a turn may set a shorter or longer game-time limit.
  Shorter limits iterate faster but do not grade long-term value; longer limits cost
  wall time. Choose per goal — the turn file records the choice and why.
- **Runner command** (the harness implements exactly this, with an isolated HOME per
  match):

  ```
  pyrogenesis -autostart="random/mainland" -autostart-seed=SEED \
    -autostart-biome=generic/temperate -autostart-placement=circle \
    -autostart-nonvisual -autostart-players=2 -autostart-size=128 \
    -autostart-victory=conquest_civic_centers \
    -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:3 \
    -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 \
    -mod=public -mod=vercingetorix -unique-logs -nosound
  ```

  The biome and the player placement pattern are pinned: with the autostart
  defaults (`"random"` each) the gamesetup draws both from the GUI realm's
  unseeded `Math.random` per run, so no experiment reproduces at all.

- **Standard battery** (recorded for every match): outcome (win/draw/loss), duration,
  resourcesGathered, resourcesUsed, unitsTrained, unitsLost, enemyUnitsKilled,
  buildingsConstructed, enemyBuildingsDestroyed, population peak, % map explored,
  time to each phase (from bot reporting), the per-minute `[HARNESS]` samples,
  bot JS error count, determinism check.

## Verdict rules

The goal is not to win every match but to **improve over the baseline**. The default
primary metric is a composite score, computed per matched pair (same seed, baseline
vs treatment) and summed over the batch:

- **Outcome component** (per pair): win = +3, draw = +1, loss = 0, minus the
  baseline's value. (A loss where the baseline won scores −3; a win where the
  baseline lost scores +3.)
- **Quality component** (per pair, always computed): for each battery metric that
  exists on both sides — resourcesGathered, resourcesUsed, enemyUnitsKilled,
  unitsTrained, population peak, and phase timings when reported — compute the
  relative delta `(treatment − baseline) / max(1, baseline)`, clamp it to [−1, 1],
  and weight it 0.4. Sum the weighted deltas.
- **Survival component** (per pair, only for loss–loss and draw–draw pairs): relative
  duration delta clamped to [−1, 1], weighted 0.4. If the baseline was a defeat and
  the treatment is also a defeat, lasting longer **is** an improvement — this
  component captures it. Same for draws.

Batch verdict over N = 10 pairs (sum of pair deltas):

| Verdict | Condition | Action |
|---|---|---|
| good | total ≥ +4, no error/determinism veto | validate: keep the change |
| bad | total ≤ −4, or error/determinism veto | revert |
| neutral | otherwise | repeat the batch once (N = 20 pairs total); still neutral → revert and record |

For a single-metric hypothesis (e.g. "time to reach Town Phase"): **good** if the
mean improves ≥ 10% relative to baseline, **bad** if it worsens ≥ 10%, **neutral**
otherwise, with the same escalation.

If a verdict is ever genuinely unclear under these rules, the turn is **invalid**:
stop, write down why in the journal, and ask Louis before proceeding.

## Evidence tools

Do not parse raw experiment JSON by hand in the agent's context — that burns tokens.
Maintain reusable exploration tools (the harness `report` subcommand and friends)
that produce compact summaries: per-match outcome and metric tables, sample curves
reduced to min/mean/max, and baseline-vs-treatment diffs. When a new kind of evidence
is collected, extend the tools in the same commit that introduces the collection.

## Turn records

- Every turn gets `turns/NNN-slug.md` with fixed sections: Hypothesis, Implementation,
  Experiment, Verdict, Action, Next. The file states the goal it serves and the
  grading result.
- `turns/backlog.md` holds candidate hypotheses — one line each, with the metric and
  the rationale.
- `CURRENT_TURN.md` always points at the active turn and its current phase. Update it
  at every phase change.
- Raw experiment results live in `experiments/NNN/` (`baseline.json`, `treatment.json`,
  `report.md`).

## Recovery (new session / after context loss)

1. Read `CURRENT_TURN.md`.
2. Read the active turn file and its experiment results.
3. Run `git status` and `git log --oneline -5`.
4. Resume at the phase indicated. Never restart a finished phase.

## References

- Engine facts verified on this VPS: `docs/DEVELOPER_GUIDE.md` → Environment.
- Game rules and how to play 0 A.D. 0.28: `docs/GAME.md` — read it before writing bot
  logic; it is grounded in the installed game data, not in memory.
- Installed game data and engine source, pinned to the running version:
  `/home/ubuntu/0ad-reference/`.
- Bot architecture (JS AI mod): `docs/DEVELOPER_GUIDE.md` → Bot mod.
