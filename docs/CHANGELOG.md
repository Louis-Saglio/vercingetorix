# Changelog

## Unreleased

- Turn 008 (goal G2 achieved): the bot now grows to a 32-soldier army before
  attacking — `SOLDIER_TARGET` raised to 32 and `HOUSE_OFFSETS` expanded to 8
  candidates so it can actually build its 4 houses. 8/10 seeds reach ≥32 melee
  by game-minute 12 (baseline 0/10), 0 JS errors, canary PASS. Closes G2 and
  opens G3 (defeat sandbox Rome).
- Turn 004 (goal G1 achieved): the bot now attacks only at its 20-soldier
  target instead of at 15, so it boots its economy instead of sacrificing the
  army early. Baseline-vs-treatment (seeds 21–30, sandbox Rome): mean peak
  melee in the first 8 game-minutes 15.7 → 20.7 (+31.8%), G1 grade distribution
  9 Fail/1 Pass → 10/10 Good, canary PASS, composite +9.00 → good. Closes G1
  and opens G2 (defeat sandbox Rome).
- The determinism gate is the per-batch canary: same seed twice must be
  bit-identical. This only holds because experiments now pin the biome to
  `generic/temperate` and the player placement to `circle` — both gamesetup
  defaults are `"random"`, drawn from the unseeded GUI `Math.random` per run,
  so unpinned no map ever reproduces (root cause in
  `docs/ENGINE_BUG_0AD_0.28_NONDETERMINISM.md`).
- Added `harness report`: paired baseline-vs-treatment scoring per the
  protocol's verdict rules (outcome + quality + survival components, draw
  semantics, JS-error veto, canary identity check), writing `report.md` plus
  a compact summary.
- Experiments now play `conquest_civic_centers` (destroy the enemy civic centres)
  with treasures disabled (forced by the bot mod's autostart override); the
  harness gained a `--victory` flag.
- Documented the verified 0.28 AI API in the developer guide, corrected the game
  reference (0.28 has dedicated worker citizens — the support civilians that
  start the game, gather, and build), and enriched it with the construction
  two-step, population bonuses, treasures, and the meter-based position scale.
- Moved `PROTOCOL.md`, `GOALS.md`, `CHANGELOG.md` into `docs/` and added a root
  `AGENTS.md` pointing at the canonical documents; added the goal-reconsideration
  rule (adjust a goal rather than grind if it resists several turns).
- Published the repository to GitHub (https://github.com/Louis-Saglio/vercingetorix);
  every commit is pushed after it lands.
- Protocol v3 per Louis's review: long-term goals with per-goal grading scales
  (`GOALS.md`, current goal G1 — economy boot), experiments limited to 20 minutes of
  **game time** via a mod trigger (tunable per turn), mandatory per-game-minute
  telemetry with early abort of failing runs, mandatory instrumentation with every
  hypothesis implementation, reusable evidence-exploration tools, and the
  evidence-turn deliverable definition (collection code + the understanding gained).
- Reworked the development protocol per Louis's review: post-turn reflection step
  (harness/protocol improvements get their own commits), evidence-collection and
  refactor turn types, a composite verdict score (outcome + quality metrics +
  survival time, so a longer defeat can count as progress), timeouts recorded as
  draws, gaul-vs-rome on mainland, per-turn seed rotation with a canary match for
  deterministic comparison.
- Added the experiment harness (`harness/`): spawns headless matches with isolated
  HOMEs, extracts per-player end-of-game statistics, and writes per-match and batch
  JSON results. Verified deterministic across repeated runs.
- Established the turn-based development protocol (`PROTOCOL.md`), the turn journal
  (`turns/`), and the project scaffolding.
- Verified on this VPS that 0 A.D. 0.28.0 runs fully headless (`-autostart-nonvisual`),
  prints per-player end-of-game statistics JSON to stdout, and simulates at roughly
  13-21x real-time on this hardware (measured ~300 turns/s solo in practice).
