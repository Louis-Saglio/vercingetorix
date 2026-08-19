# Vercingetorix

Vercingetorix is a rule-based AI bot for [0 A.D.](https://play0ad.com/), written as an
in-engine JavaScript mod, developed and trained entirely in headless matches on this VPS.

It is developed by an autonomous agent following a strict, evidence-driven cycle:
hypothesis → implementation → experiment → verdict → action, one change per turn.
See [PROTOCOL.md](PROTOCOL.md).

## Quick start

- **Run one headless match** (bot vs Petra): see [User Guide](docs/USER_GUIDE.md).
- **Play against it**: copy the mod into `~/.local/share/0ad/mods/vercingetorix` and
  select it in the game setup.
- **Follow development**: read `turns/` (journal) and `experiments/` (raw results).

## Documentation

- [Changelog](CHANGELOG.md)
- [User Guide](docs/USER_GUIDE.md)
- [Developer Guide](docs/DEVELOPER_GUIDE.md)
