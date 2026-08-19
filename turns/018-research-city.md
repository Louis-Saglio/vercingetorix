# Turn 018 — Research City Phase

Goal served: G4 (defeat sandbox Rome, via the siege path: City → arsenal → ram).

## Hypothesis

> If the bot researches City Phase at the civic centre once ≥ 750 stone and
> ≥ 750 metal are banked (after Town completes), then the bot reaches City
> Phase before the 20-minute limit on ≥ 8/10 seeds, because turn 017 banks the
> 750/750 reliably by minute 16, the CC lists `phase_city_{civ}` in its
> Researcher list, and the sim accepted Town research from the AI with zero
> class-counted structures (town was paid and completed with 0 houses — the
> classCounts requirement does not block the AI path).

Primary metric: fraction of seeds where the bot reaches City Phase
(`gameState.currentPhase() >= 3`, sim ground truth) before the 20-minute limit,
0 JS errors.

Verdict thresholds (pre-registered): good if ≥ 8/10 seeds reach City Phase,
0 JS errors, canary PASS; bad if ≤ 2/10 or error/determinism veto; neutral
otherwise. Composite reported as secondary evidence.

## Implementation

In `bot/simulation/ai/vercingetorix/vercingetorix.js`:

- `manageResearch`: after Town is *completed* (`gameState.currentPhase() >= 2`,
  not merely posted), find a `phase_city*` tech in the CC's `researchableTechs`
  and post `cc.research(cityTech)` once stone ≥ 750 and metal ≥ 750; a
  serialized `cityAttempted` flag prevents re-posting.
- The `[HARNESS]` sample now reports `city` (true when
  `gameState.currentPhase() >= 3`) and `townClass` (the sim's
  `playerData.classCounts["Town"]`) — evidence for whether the "3 Town
  structures" requirement counts anything and whether City completed.

## Experiment

Settings: seeds 161–170 (fresh), sandbox Rome (`--difficulty2 0`),
`random/mainland` 128, `conquest_civic_centers`, treasures disabled, 20
game-minute limit, biome/placement pinned. Baseline = HEAD (turn-017 code);
treatment = City Phase research; canary = seed 161.

## Results

- Canary: **PASS**.
- Primary metric: **0/10** seeds reach City Phase. Composite: **+0.00**; 0 JS
  errors everywhere.
- The instrumentation exposes the root cause: `gameState.currentPhase()` stays
  **1** for the whole match on every seed, and `playerData.classCounts["Town"]`
  stays 0. A follow-up diagnostic match (seed 161) shows
  `isResearched("phase_town")` and `isResearched("phase_town_generic")` are
  false forever: **the sim never accepted the Town research either** — since
  turn 011, the bot's `townResearched` flag has been a bot-side fiction, not a
  real phase advance. The sim's `canResearch("phase_town_generic")` is false
  the whole match because the "5 Village structures" requirement is unmet:
  `classCounts["Village"]` tracks the houses exactly (0→4) and never reaches 5.
  (The 500/500 food/wood drop at town time is training spend, not the research
  cost.)
- So turns 010–017's "Town Phase reached" evidence was invalid — it measured
  the bot's flag, not the sim. The 750/750 stone/metal gathering (G3) is still
  real (resources are real, and the carve-out gates on the flag), but every
  phase-gated conclusion must be re-verified against `currentPhase()`.

## Verdict

**Bad** (pre-registered: 0/10 ≤ 2/10). The hypothesis premise — that the sim
accepted Town research with zero class-counted structures — is falsified.
Reverted.

## Action

Revert the change (`git restore bot/simulation/ai/vercingetorix/vercingetorix.js`)
and commit as `turn 018: research-city — bad`. No `CHANGELOG.md` entry for the
bot change; the commit adds a documentation fix (post-turn reflection):
`docs/DEVELOPER_GUIDE.md` now records the sim-side phase requirements and
mandates sim-truth phase evidence (`currentPhase()`/`isResearched`), and
`docs/GOALS.md` gets a note that the turn-011 "Town reached" evidence was
flawed.

## Next

Reach Town Phase **for real**: the sim requires 5 Village-class structures
(house = Village). The pre-town economy must therefore save 500 food + 875
wood (5 houses + the research) before posting, which the current 2-gatherer
pre-town economy cannot do in time — the worker/gatherer split needs
re-balancing. Then City needs 3 Town-class structures (forge/market/tavern),
then the arsenal + ram. See `turns/backlog.md`.
