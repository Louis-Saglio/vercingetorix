# Hypothesis backlog

One line per candidate: the change, the primary metric, and the rationale.
Top of the list goes first. Fed by experiment results; never edit an entry
retroactively to match a verdict.

- G4: reach Town Phase **for real** (sim truth): build 5 Village-class houses
  and rebalance the pre-town gatherer split so 500 food + 875 wood accumulate
  in time; primary metric = `currentPhase() >= 2` before minute 12. Turn 018
  discovery: since turn 011 the bot's `townResearched` flag was fiction — the
  sim never accepted the research (requires 5 Village structures, the bot had
  0–4 houses at post time). All phase evidence must use
  `gameState.currentPhase()`/`isResearched`. **Done turn 019 (good): 9/10
  real Town at minute 7–8.**
- G4: research City Phase once `currentPhase() >= 2`, stone ≥ 750, metal ≥
  750 AND 3 Town-class structures exist. **Done turn 023 (good): 9/10 City at
  minute 18–19** — training held until 3 forges, forges placed on a double
  ring (72 m + 88 m, 32 candidates, 28 m clearance).
- G4: build the arsenal in City (300 wood), train a siege ram (300 wood +
  150 metal), and attack the enemy CC with army + ram; primary metric = wins
  before the 25-minute limit. Turn 024 (bad): two failure modes — (a)
  `manageRams` trains on the arsenal *foundation* (foundations carry the
  Arsenal class → JS errors, veto); filter foundations out. (b) metal
  starvation: City research spends the banked 750 metal, and only ~0.4/s
  regathers, so the ram's 150 metal arrives after the limit — **gate City on
  metal ≥ 900 (750 + 150)** so the ram metal is pre-banked. Requires the
  NonVisualTrigger limit 20 → 25 minutes (part of the change).
- G4: more/better house placement: 5-house target stalls on ~1/10 seeds when
  all 8 offsets are invalid (turn 019 seed 173); primary metric = 5 houses on
  10/10 seeds.
- G4: build an arsenal in City Phase, then train a siege ram for crush damage
  against the CC; primary metric = win rate vs sandbox Rome.
- G4: direct capture-allowed attack on the enemy CC. (turns 005/009 — bad.)
- **Prereq** — harness runner (turn 001 — done).
- **Prereq** — bot skeleton (turn 002 — done).
- **Prereq** — report tool (turn 003 — done; pinned biome/placement, canary gate).
- Evidence: report time-to-phase (town/city) and per-minute resource/army
  samples so the composite score has phase-timing metrics to use.
- Perf: cached resource collections (turn 014 — done).

Turns 004–017: G1 achieved (004), G2 achieved (008), Town research (011 good),
perf refactor (014 good), G3 reconsidered (015) and achieved (017 good —
workers on stone/metal from minute 0 + post-town carve-out). G4 is now active.
