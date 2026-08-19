# Vercingetorix Development Protocol

**Goal:** improve Vercingetorix — a rule-based 0 A.D. AI bot written as an in-engine
JavaScript mod — until it reliably beats Petra at increasing difficulty levels,
using evidence-driven development cycles.

All work happens in **turns**. One turn = one hypothesis, tested by one experiment,
closed by one verdict and exactly one commit.

## The turn

A turn has five phases, always in this order:

1. **Hypothesis** — written in the turn file *before any code changes*:

   > If I change X, then metric M improves, because Z.

   The hypothesis must name the change (X), the primary metric (M), the experiment
   that tests it, and the verdict thresholds.
2. **Implement** — make the minimal code change for X. Bot logic changes only;
   nothing else rides along.
3. **Experiment** — run the baseline (last commit) and the treatment (working tree)
   on the same seeds; record every match result in `experiments/NNN/`.
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

   ```
   turn NNN: <slug> — <verdict>
   ```

   The commit body is the journal summary. Then launch the next turn: take the top
   item from `turns/backlog.md`, or derive a new hypothesis from the last results.

## Hard rules

1. **One change per turn.** If a change needs several parts, split it into several turns.
2. **Hypothesis before code.** Never adjust the metric or the thresholds after seeing
   results — that would make the verdict meaningless. A badly designed experiment is
   marked invalid, not re-interpreted.
3. **Determinism gate.** Every commit must reproduce identically (same seed twice →
   identical results). A change that breaks determinism is **bad** regardless of metrics.
4. **Error veto.** A change that increases the bot's JS error count is **bad**
   regardless of metrics.
5. **Minimal diffs.** No refactoring, no formatting, no unrelated fixes inside a turn.
6. **Baseline = last commit.** Never compare against a stale baseline.
7. **Only validated improvements persist.** Reverted turns leave no trace in the code,
   only in the journal.

## Experiment specification (defaults)

- **Bot:** Vercingetorix, player 1, civ `athen`.
- **Opponent:** Petra, player 2, civ `mace`, difficulty 3. Raise the difficulty when
  the bot's win rate is ≥ 80% over the last 10 turns at the current level.
- **Map:** `random/alpine_lakes`, size 128. Extend the map pool only by explicit
  decision recorded in a turn.
- **Seeds:** 1..10, i.e. N = 10 pairs per batch. Baseline and treatment use the *same*
  seeds (paired comparison — identical maps for both sides of the comparison).
- **Match limit:** a match that has not ended after 20 minutes of wall clock counts
  as a loss for the bot.
- **Runner command** (the harness implements exactly this, with an isolated HOME per
  match):

  ```
  pyrogenesis -autostart="random/alpine_lakes" -autostart-seed=SEED \
    -autostart-nonvisual -autostart-players=2 -autostart-size=128 \
    -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:3 \
    -autostart-civ=1:athen -autostart-civ=2:mace -autostart-player=-1 \
    -mod=vercingetorix -unique-logs -nosound
  ```

- **Standard battery** (recorded for every match, used for context even when not the
  primary metric): outcome, duration, resourcesGathered, resourcesUsed, unitsTrained,
  unitsLost, enemyUnitsKilled, buildingsConstructed, enemyBuildingsDestroyed,
  population peak, % map explored, bot JS error count, determinism check.

## Verdict rules

For a win-rate primary metric over N = 10 pairs:

| Verdict | Condition | Action |
|---|---|---|
| good | treatment wins ≥ baseline + 2, no error/determinism veto | validate: keep the change |
| bad | treatment wins ≤ baseline − 2, or error/determinism veto | revert |
| neutral | anything else | repeat the batch once (N = 20 pairs total); still neutral → revert and record |

For a continuous primary metric (e.g. average time to reach Town Phase): **good** if the
mean improves ≥ 10% relative to baseline, **bad** if it worsens ≥ 10%, **neutral**
otherwise, with the same escalation as above.

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
- Bot architecture (JS AI mod): `docs/DEVELOPER_GUIDE.md` → Bot mod.
