# Vercingetorix Development Protocol

**Goal:** improve Vercingetorix — a rule-based 0 A.D. AI bot written as an in-engine
JavaScript mod — until it reliably beats Petra at increasing difficulty levels,
using evidence-driven development cycles.

All work happens in **turns**. One turn = one hypothesis, tested by one experiment,
closed by one verdict and exactly one commit.

## Turn types

- **Improvement turn** (default): a hypothesis about making the bot better.
- **Evidence-collection turn**: the hypothesis is "if I collect data D, then I will
  understand Y well enough to formulate a bot improvement". No bot behavior change
  is claimed. The deliverable is the collected evidence plus what it teaches, written
  in the turn record. Verdict = did the evidence answer the question (yes/no).
  Evidence may be logs in the bot or anywhere in the simulation — any code that helps
  see what is going on, including in the engine's own scripts if needed.
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
2. **Implement** — make the minimal code change for X. Bot logic changes only;
   nothing else rides along.
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
6. **Commit** — every turn ends with one commit, regardless of verdict:
   `turn NNN: <slug> — <verdict>` with the journal summary as the body.
7. **Post-turn reflection** — before launching the next turn, ask: did anything in
   this turn reveal a problem or a missing capability in the harness or in this
   protocol itself? If yes, make those improvements **now**, in a separate commit
   (not inside a turn commit), then launch the next turn. Examples: a metric the
   harness does not extract, a verdict rule that misjudged an obvious result, an
   experiment default that got in the way.
8. **Next turn** — take the top item from `turns/backlog.md`, or derive a new
   hypothesis from the last results (including from evidence-collection turns).

## Hard rules

1. **One change per turn.** If a change needs several parts, split it into several turns.
2. **Hypothesis before code.** Never adjust the metric or the thresholds after seeing
   results — that would make the verdict meaningless. A badly designed experiment is
   marked invalid, not re-interpreted.
3. **Determinism gate.** Every commit must reproduce identically (same seed twice →
   identical results). A change that breaks determinism is **bad** regardless of metrics.
4. **Error veto.** A change that increases the bot's JS error count is **bad**
   regardless of metrics.
5. **Minimal diffs.** No refactoring, no formatting, no unrelated fixes inside a turn
   (refactors are their own turn type).
6. **Baseline = last commit.** Never compare against a stale baseline.
7. **Only validated improvements persist.** Reverted turns leave no trace in the code,
   only in the journal.

## Experiment specification (defaults)

- **Bot:** Vercingetorix, player 1, civ `gaul`.
- **Opponent:** Petra, player 2, civ `rome`, difficulty 3. Raise the difficulty when
  the bot's win rate is ≥ 80% over the last 10 turns at the current level.
- **Map:** `random/mainland`, size 128.
- **Seeds:** every turn draws its own seed set (default 10 seeds) and records it in
  the turn file. Baseline and treatment always share the turn's seed set (paired
  comparison). Seed sets are never reused across turns — this is the anti-overfitting
  measure.
- **Canary match:** every batch additionally runs one match that repeats the baseline
  exactly (same civ, same seed as an existing baseline match). Its result must be
  identical to the original baseline run; if not, the batch is invalid and the
  harness has a bug to fix before any verdict.
- **Match limit:** a match that has not ended after 20 minutes of wall clock is
  stopped and recorded as a **draw** (not a loss). Draws are then judged by the
  quality metrics, not by outcome alone.
- **Runner command** (the harness implements exactly this, with an isolated HOME per
  match):

  ```
  pyrogenesis -autostart="random/mainland" -autostart-seed=SEED \
    -autostart-nonvisual -autostart-players=2 -autostart-size=128 \
    -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:3 \
    -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 \
    -mod=vercingetorix -unique-logs -nosound
  ```

- **Standard battery** (recorded for every match): outcome (win/draw/loss), duration,
  resourcesGathered, resourcesUsed, unitsTrained, unitsLost, enemyUnitsKilled,
  buildingsConstructed, enemyBuildingsDestroyed, population peak, % map explored,
  time to each phase (from bot reporting), bot JS error count, determinism check.

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

## Turn records

- Every turn gets `turns/NNN-slug.md` with fixed sections: Hypothesis, Implementation,
  Experiment, Verdict, Action, Next.
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
