# Changelog

## Unreleased

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
