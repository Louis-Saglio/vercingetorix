# Turn 016 — Targeted stone/metal gathering after Town

Goal served: G3 (gather 750 stone + 750 metal by game-minute 16).

## Hypothesis

> If I assign a fixed share of the army to stone and metal — but only after Town
> Phase is researched, and with a full-map stone/metal scan (no 160 m cap) — and
> defer the attack until 750 stone + 750 metal are banked, then the bot reaches
> ≥ 750 stone AND ≥ 750 metal by game-minute 16 on ≥ 8/10 seeds, because turn
> 012 failed from two identified causes: the 4-way split applied *before* Town,
> so the only two pre-town gatherers starved wood and Town was never reached;
> and the 160 m scan radius never saw a stone mine (mines are placed ≥ 20 tiles
> from player territory), so no stone was gathered at all.

Primary metric: fraction of seeds whose minute-16 `[HARNESS]` sample shows
stock ≥ 750 stone AND ≥ 750 metal (the bot starts at 300/300, so this means
≥ 450 net gathered of each — enough to afford City Phase), 0 JS errors.

Verdict thresholds (pre-registered): good if ≥ 8/10 seeds reach the primary
metric, 0 JS errors, canary PASS, and the composite score is not strongly
negative (> −4, i.e. no economy collapse like turn 012's −18.33); bad if
≤ 2/10 or error/determinism veto; neutral otherwise.

## Implementation

In `bot/simulation/ai/vercingetorix/vercingetorix.js`:

- Two new auto-maintained caches (`resource-stone`, `resource-metal`) with
  **no radius cap** — mines are few dozen entities, so the full-map scan is
  cheap and finds the mines the 160 m wood/food cap missed.
- `manageSoldiers`: once `townResearched`, idle gatherers with
  `id % 16 < 3` gather stone and `id % 16 < 5` gather metal (≈ 6 + 4 of the
  32-soldier army); the rest keep the pre-town 2:1 wood:food split. The split
  only changes *after* Town, so the pre-town wood/food accumulation is
  untouched.
- The attack trigger now also requires `stone ≥ 750 && metal ≥ 750`, so the
  army keeps gathering instead of marching off at 32 soldiers.
- The per-minute `[HARNESS]` sample now reports `stone` and `metal` (evidence
  for the primary metric).

## Experiment

Settings: seeds 141–150 (fresh), sandbox Rome (`--difficulty2 0`),
`random/mainland` 128, `conquest_civic_centers`, treasures disabled, 20
game-minute limit, biome/placement pinned. Baseline = HEAD (turn-015 code);
treatment = targeted stone/metal gathering; canary = seed 141.

## Results

- Canary: **PASS**.
- Primary metric: **2/10** seeds reach ≥ 750 stone AND ≥ 750 metal at the
  minute-16 sample (seeds 142, 146). G3 Pass tier (≥ 500 of each): **8/10** —
  misses are 145 (740/440) and 150 (480/660).
- 0 JS errors in all matches, both arms.
- Composite: **−2.56** → neutral band; no economy collapse (turn 012 was
  −18.33). Wood/food survive the carve-out.
- Per-seed t16 (treatment): 141 770/530, 142 1420/960, 143 550/810,
  144 700/1130, 145 740/440, 146 1050/840, 147 920/600, 148 850/710,
  149 710/790, 150 480/660.

The mechanics work — stone is found (full-map scan) and both resources rise on
every seed. The shortfall is timing: town lands at minute 8–9, the army grows
slowly afterwards (stone/metal hands only exist post-town), and the 6+4 share
of a 32-target army under-delivers in the t16 window. Measured per-gatherer
income: ≈ 0.17/s stone (mines far out), ≈ 0.2/s metal. Seed 150 also shows the
carve-out biting the early small army: only ~8 wood gatherers → army stuck at
18 by t16.

## Verdict

**Bad** (pre-registered: good ≥ 8/10, bad ≤ 2/10): 2/10 on the primary metric.
Reverted.

## Action

Revert the change (`git restore bot/simulation/ai/vercingetorix/vercingetorix.js`)
and commit as `turn 016: stone-metal-after-town — bad`. No `CHANGELOG.md` entry.

## Next

The binding constraint is early hands, not shares: the four starting support
workers sit idle all game (the bot only commands Melee entities). Next
hypothesis: put the starting workers on stone/metal from minute 0 (they gather
faster than citizen soldiers), keep the post-town carve-out for the army, and
tune shares so a mid-size army still grows. See `turns/backlog.md`.
