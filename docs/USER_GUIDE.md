# Vercingetorix — User Guide

## What it is

Vercingetorix is an AI bot for the 0 A.D. real-time strategy game. It is developed on
this VPS by an agent that runs headless matches, measures results, and keeps only the
changes that are proven to help. This guide is for Louis, the project owner.

## How the development loop works

Everything happens in **turns** (see [PROTOCOL.md](PROTOCOL.md)):

1. The agent writes a hypothesis about what to improve.
2. Implements it.
3. Runs an experiment: a batch of Vercingetorix-vs-Petra matches, plus a
   canary re-run proving the bot reproduces itself identically.
4. Decides good / bad / neutral.
5. Keeps, reverts, or gathers more evidence.
6. Commits and starts the next turn.

## Where to look

- `turns/` — one journal file per turn: hypothesis, experiment, verdict, action.
- `experiments/NNN/` — raw match results and the baseline-vs-treatment report.
- `CURRENT_TURN.md` — what the agent is doing right now.
- `git log` — one commit per turn.

## Running a match yourself

One headless match, Vercingetorix (player 1) vs Petra (player 2) on Alpine Lakes:

```bash
pyrogenesis -autostart="random/alpine_lakes" -autostart-seed=42 \
  -autostart-biome=generic/temperate -autostart-placement=circle \
  -autostart-nonvisual -autostart-players=2 -autostart-size=128 \
  -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:3 \
  -autostart-civ=1:athen -autostart-civ=2:mace -autostart-player=-1 \
  -mod=vercingetorix -unique-logs -nosound
```

At the end it prints one JSON block per player with the full match statistics and exits.

## Playing against Vercingetorix yourself

1. Copy the mod: `cp -r bot ~/.local/share/0ad/mods/vercingetorix`
   (the folder must contain `mod.json`; see the developer guide for the layout).
2. Start 0 A.D., open Game Setup, pick "Vercingetorix" as an opponent AI.

## Common issues

- **`pyrogenesis: command not found`** — install it: `sudo apt install 0ad`.
  The binary is `/usr/games/pyrogenesis`; some shells need the full path.
- **A match never ends** — matches are capped at 20 wall-clock minutes by the
  protocol; the runner counts that as a loss.
- **"Disk full" while experimenting** — never put match home directories on `/tmp`
  (it is a small tmpfs); use disk-backed paths.
