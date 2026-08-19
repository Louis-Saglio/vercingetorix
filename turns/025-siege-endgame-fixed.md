# Turn 025 — Siege endgame, fixed

Goal served: G4 (defeat sandbox Rome).

## Hypothesis

> If the turn-024 siege endgame is restored with its two understood failure
> modes fixed — (1) `manageRams` never trains on a foundation (foundations
> carry the Arsenal class but have no Trainer), (2) soldier training is held
> until the arsenal is built so wood pools for it instead of dripping into
> soldiers, and (3) the attack triggers on the first ram instead of 32
> soldiers — then the bot wins (enemy CC destroyed) on ≥ 8/10 seeds before
> the 25-minute limit, because the ram reaches the enemy CC escorted by the
> soldiers, and the 32-soldier gate was itself unreachable by minute 25 in
> turn 024 (melee was 23 at t24).

Primary metric: fraction of seeds won (enemy CC destroyed before the limit),
0 JS errors.

Verdict thresholds (pre-registered): good if ≥ 8/10 wins, 0 JS errors, canary
PASS; bad if ≤ 2/10 or error/determinism veto; neutral otherwise. Secondary
(reported, not the verdict): win minute, city minute, ram minute, composite.
In-turn fix-and-rerun iterations are expected per the updated protocol.

## Implementation

In `bot/maps/scripts/NonVisualTrigger.js` (25-minute limit) and
`bot/simulation/ai/vercingetorix/vercingetorix.js`:

- Restores turn 024's siege endgame (arsenal on the double ring, rams
  trained at the arsenal, rams attack the nearest enemy CC, sample fields).
- Fix 1: `manageRams` skips foundations when picking the arsenal.
- Fix 2: training is held while `arsenals == 0` (like the forge gate), so
  wood pools for the 300-wood arsenal.
- Fix 3: the attack triggers at `rams ≥ 1` (the ram is the win condition);
  the soldier sweep still escorts from that moment.

## Experiment

Settings: seeds 231–240 (fresh), sandbox Rome (`--difficulty2 0`),
`random/mainland` 128, `conquest_civic_centers`, treasures disabled, 25
game-minute limit, biome/placement pinned. Baseline = last validated
experiment's code (HEAD, turn-023 state, 20-minute trigger) run once on
these seeds; treatment = fixed siege endgame; canary = seed 231.

## Results

**Iteration 1 (initial treatment):** Canary PASS, 0 JS errors (foundation fix
works), City 10/10 at minute 18–20, arsenal 10/10 at 19–21 — but **0/10 wins
and 0 rams**: training resumes as soon as the arsenal is built and drains
every spare 50 wood, so the 300-wood ram gate never passes (wood oscillates
at 5–205 from minute 21 on; metal reaches 150 at minute 22–24 but wood is the
binding constraint).

**Iteration 2 (in-turn fixes):** training now holds until the first ram
exists (wood pools for it), and the workers split 1 stone / 3 metal (metal is
the critical-path resource: City research then the ram). Rerun below.

**Iteration 2 result:** **regression** — 0/10 wins and City never reached on
any seed: with one stone worker, stone becomes the binding constraint and the
750 stone for City research never arrives. The metal speed-up was bought with
the stone margin that did not exist. Composite −6.47, 0 JS errors, canary
PASS.

**Stop-the-turn decision:** the iterations are not converging — each fix
surfaces a new binding constraint (wood contention → stone collapse). The
real problem is structural: the optimized critical path is city t18–20 →
arsenal t19–21 → ram t21.5–22 (with the wood fix) → march ~2.5–3 min → CC
kill ~1–1.5 min, i.e. wins land at t25.5–27 — **outside the 25-minute
limit**. That needs a designed next turn, not more small patches.

## Verdict

**Bad** (pre-registered: 0/10 wins ≤ 2/10 across both iterations). Reverted.

## Action

Revert the change (`git restore bot/`) and commit as `turn 025:
siege-endgame-fixed — bad`. No `CHANGELOG.md` entry. The negative knowledge
and the next-turn plan go to `turns/backlog.md`.

## Next

Turn 026: keep 2+2 workers, hold training until the first ram (the fix that
iteration 1's evidence demanded, never tested in isolation), attack on the
first ram — and raise the G4 match limit 25 → 30 game-minutes on the
evidence above (the goal-adjustment rule; the timeline is 25.5–27 minutes
even optimized). See `turns/backlog.md`.
