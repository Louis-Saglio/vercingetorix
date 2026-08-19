# Turn 028 — G4 reconsideration + army scaling

Goal served: G4 reconsideration rule + new G4a (army scaling).

## Hypothesis

> If the bot scales its army — `SOLDIER_TARGET` 32 → 50, `HOUSE_TARGET` 5 → 8
> with house placement on the clearance ring (the fixed offsets stall at 5) —
> on the restored siege economy, then ≥ 8/10 seeds field ≥ 50 melee soldiers
> by game-minute 22, because turn 027's end stats showed the true blocker:
> we trained 18 units while sandbox Rome trained 116 (90 infantry + 26
> civilians). Gaul cannot train extra workers (no
> `units/gaul/support_civilian_house`), so the civ scales through citizen
> soldiers — every trained soldier is both a gatherer and a fighter, and the
> army compounds.

Primary metric: fraction of seeds where melee ≥ 50 at the minute-22 sample,
0 JS errors.

Verdict thresholds (pre-registered): good if ≥ 8/10 seeds reach the metric,
0 JS errors, canary PASS; bad if ≤ 2/10 or error/determinism veto; neutral
otherwise. Secondary (reported, not the verdict): city minute, composite.
In-turn fix-and-rerun iterations allowed.

## Implementation

- `docs/GOALS.md`: G4 is split — **G4a (current): sustain a 50+ melee army by
  game-minute 22** (Good = ≥ 50 melee at the minute-22 sample; achieved when
  a 10-seed batch reaches Good on ≥ 8/10 seeds, 0 JS errors); **G4b (later):
  win vs sandbox Rome before the 30-minute limit** with the scaled army plus
  the rams.
- `bot/maps/scripts/NonVisualTrigger.js`: 30-minute limit (G4's).
- `bot/simulation/ai/vercingetorix/vercingetorix.js`:
  - `SOLDIER_TARGET` 32 → 50, `HOUSE_TARGET` 5 → 8.
  - `manageHouses` places on the forge double ring with the structure
    clearance walk instead of the 8 fixed offsets (5-house target already
    stalls on ~1–2/10 seeds; 8 needs the ring).
  - Restores the turn-027 siege chain (arsenal, rams, attack at two rams,
    all-wood post-town split, free training after the forges).

## Experiment

Settings: seeds 261–270 (fresh), sandbox Rome (`--difficulty2 0`),
`random/mainland` 128, `conquest_civic_centers`, treasures disabled, 30
game-minute limit, biome/placement pinned. Baseline = last validated code
(HEAD, 20-minute trigger) run once on these seeds; treatment = army scaling;
canary = seed 261.

## Results

**Iteration 1 (initial treatment):** 0/10 — melee stuck at 2 on 5 seeds, Town
delayed to minute 9–13 everywhere, max melee 15–20. Root cause: the house
placement walked the **forge rings (72/88 m), which sit outside Village-phase
territory pre-town** — placements are rejected until Town expands the
territory, so the 5 Village houses build slowly and the whole chain shifts.

**Iteration 2 (in-turn fix):** houses get their own ring at 56/64 m (inside
Village territory) with 26 m clearance. Rerun below.

**Iteration 2 result:** still 0/10 — Town still lands at minute 9–13, melee
max 16–21. The ring walk is too slow pre-town: rejected candidates (trees)
burn one play tick each, so each of the first 5 houses takes many ticks; the
proven fixed offsets placed them in seconds.

**Iteration 3 (in-turn fix):** houses 1–5 use the proven fixed offsets
(fast, no clearance — the Village requirement), houses 6–8 use the clearance
ring (the fixed 8 stall at 5). Rerun below.

**Iteration 3 result:** still 0/10, melee max 15–22, Town at minute 9–11, and
seeds 268/269 deadlock with 4 houses (townCan false forever — the fixed
offsets stall at 4 on those seeds and the ring never activates). Two causes:
(1) the forges gate holds training until minute 14–15, so the army has only
~7 minutes to grow — the wall for the t22 metric; (2) the 5th-house stall
needs the ring as a fallback once the fixed offsets are exhausted.

**Iteration 4 (in-turn fix):** training runs freely from Town (the army
compounds: every soldier gathers), and the house ring activates as fallback
when the fixed offsets are exhausted. Rerun below.

**Iteration 4 result:** 0/10, melee 12–17 at t22 — but the end stats expose
the thief: **five siege rams trained** (1500 wood + 750 metal) from minute
~20, while infantry starved at 1.3/min despite wood stockpiling to 680+.
The rams steal the army's wood as soon as the arsenal exists.

**Iteration 5 (in-turn fix):** no rams until the army is complete
(`soldiers ≥ SOLDIER_TARGET`) — the siege starts after G4a's army. Rerun
below.

**Iteration 5 result + A/B diagnostic:** still 0/10 (melee 12–17 at t22,
max 19). A diagnostic ran the **validated turn-023 code on the same seeds**:
it peaks at 2–16 melee with the 20-minute limit — the treatment (18–19) is
actually better, but both are ~3x short of 50. The seed batch's economy
(wood-starved on several seeds) plus the ~1.5-soldiers/min ceiling of the
current design make **50 by minute 22 unreachable**: the CC queue is empty
most of the time (q=0–2) because the wood income (~4–5/s) cannot feed 50
soldiers, the 8 houses and the structures inside 22 minutes. Stopped per the
protocol's stop clause — five iterations, not converging.

## Verdict

**Bad** (pre-registered: 0/10 ≥ 50 melee at t22, ≤ 2/10 boundary). Reverted.

## Action

Revert the change (`git restore bot/`) and commit as `turn 028:
army-scaling — bad`. No `CHANGELOG.md` entry. G4a is re-scoped in
`docs/GOALS.md` with this evidence: 50-by-t22 is beyond the current economy —
the next turn should first fix the wood economy (more gatherers earlier) or
adopt a modest G4a (e.g. ≥ 32 soldiers + 3 rams by minute 24, which the
evidence supports as the reachable stepping stone).

## Next

Turn 029: either a wood-economy turn (the ~1.5 soldiers/min ceiling: only
~4–5 wood/s post-town — the pre-town budget for 8 houses also drains it) or
re-scope G4a to the evidence-supported target. See `turns/backlog.md`.
