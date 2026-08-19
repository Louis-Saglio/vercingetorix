# Turn 000 — Project setup

## Hypothesis

None. This is the establishment turn: create the project, the development protocol,
and the documentation scaffolding.

## Implementation

- Created `/home/ubuntu/vercingetorix` with git repository (`main` branch).
- Wrote `docs/PROTOCOL.md` (the turn cycle, hard rules, experiment defaults, verdict rules).
- Wrote `README.md`, `docs/CHANGELOG.md`, `docs/USER_GUIDE.md`, `docs/DEVELOPER_GUIDE.md`.
- Created `turns/` journal with this file and `turns/backlog.md`, plus `experiments/`.
- Installed `0ad` / `0ad-data` 0.28.0 system-wide and verified the headless workflow
  (see the developer guide, Environment section, for the measured facts).

## Experiment

None. Environment verification was done as a PoC before this project existed:
three headless runs confirming simulation speed (~13-21x real-time), the game-end
statistics JSON on stdout, clean exit code 0, and the 0.28 log/replay paths.

## Verdict

n/a

## Action

Committed as the initial state.

## Next

Turn 001: build the harness runner (prerequisite for every future experiment).
Then turn 002: bot skeleton baseline. See `turns/backlog.md`.
