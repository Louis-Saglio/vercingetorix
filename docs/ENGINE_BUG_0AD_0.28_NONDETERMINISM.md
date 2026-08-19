# Engine bug report — 0 A.D. 0.28.0: same-seed headless matches did not reproduce (unseeded gamesetup defaults)

- **Engine:** Pyrogenesis 0.28.0 (apt package `0ad` 0.28.0-3), source pinned at
  `/home/ubuntu/0ad-reference/source` (tag `v0.28.0`, commit `a2cae4d6`,
  gitea.wildfiregames.com).
- **Status:** root-caused and worked around in the project harness. No
  engine rebuild needed. This file is the project's record and the basis for
  a future upstream report.

## Summary

Two headless matches started with identical settings and the same seed did
not reproduce. The cause is **two gamesetup fields that default to
`"random"` and are resolved per run with the GUI realm's unseeded
`Math.random`** — the map's **biome** and the **player placement pattern**.
Both feed the random map generator, so the map itself differs between runs
despite `-autostart-seed`. Pinning both fields makes same-seed runs
bit-identical (the project's unpaced canary passes repeatedly).

An earlier diagnosis in this file blamed an async pathfinder race. That
theory is **refuted** by the evidence and removed: with biome and placement
pinned, unpaced same-seed runs reproduce bit-identically, which the race
theory would forbid.

## Root causes (evidence)

### 1. Unseeded biome

`autostart/cmd_line_args.js` does
`settings.biome.setBiome(cmdLineArgs['autostart-biome'] || "random")`. With
the flag absent, the gamesetup resolves `"random"` to a concrete biome per
run in the GUI realm (unseeded). Replay manifests of same-seed runs showed
`Biome: generic/sahara`, `generic/nubia`, `generic/autumn`,
`generic/temperate` — different maps, obviously different results.

### 2. Unseeded player placement

The same default applies to the placement pattern
(`settings.playerPlacement.setValue(cmdLineArgs['autostart-placement'])`,
gamesetup default `"random"` — the GUI's placement dropdown ships a `random`
option that "select[s] a random player placement pattern when starting the
game"). Two probe runs of seed 17 with the biome already pinned had
`"PlayerPlacement": "circle"` vs `"randomGroup"` in their replay manifests,
and their first-step game states showed completely different maps (civil
centre at `[228, 424]` vs `[188, 132]`; tree counts differing by tens). The
mainland script places the bases from `mapSettings.PlayerPlacement`
(`playerPlacementByPattern`), so this single input changes the whole map.

### Verification of the fix

With `-autostart-biome=generic/temperate -autostart-placement=circle` in the
harness command, the project's unpaced canary (same seed twice, every
deterministic field compared) passes: seeds 5 and 17 (and one more run on
seed 19 at the time of writing). The earlier "intermittent divergence" was
simply runs drawing different biome/placement combinations — runs whose
draws coincided were identical.

## Why this is easy to miss (and not reported)

- In normal GUI play, `"random"` biome/placement are *intended* UX: the user
  picks Random and gets a surprise map. The gamesetup resolves them with the
  unseeded GUI `Math.random` — by design.
- Replays are unaffected: the replay manifest records the *resolved* concrete
  values (e.g. `Biome: generic/temperate`, `PlayerPlacement: circle`), so
  replay playback re-uses them and stays consistent.
- The trap is the combination `-autostart-seed=N` + unset biome/placement:
  the seed suggests the whole map is determined, but two unseeded fields
  still vary. Worth an upstream note: in autostart mode the gamesetup
  defaults should resolve `"random"` from the seeded RNG, or the seed should
  be documented as not covering biome/placement.

## Project workaround (adopted, no rebuild)

- The harness always passes `-autostart-biome=generic/temperate` and
  `-autostart-placement=circle`.
- The per-batch **canary** (same seed twice, unpaced) is the determinism
  gate and now passes reliably (seeds 5, 17, 19 verified).

## Evidence artifacts

- The decisive probe evidence: `experiments/003/probe-manifests.txt` (two
  same-seed runs, identical `Seed`/`AISeed`/`Biome`, different
  `PlayerPlacement`).
- The pinned-settings canary pairs (same seed twice, bit-identical):
  `experiments/003/up5a.json` + `up5b.json`, `up17a.json` + `up17b.json`,
  `up19a.json` + `up19b.json`, with the canary reports in `up5/`, `up17/`,
  `up19/`.
- Turn journal: `turns/003-report-tool.md`.
