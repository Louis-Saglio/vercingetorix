# tools/ — 0 A.D. data analysis scripts

Regenerators for the generated reference docs under `docs/game_description/`
(`generic/units`, `generic/buildings`, `generic/technologies`, `gauls/`).
Everything is extracted from the pinned game data
(`/home/ubuntu/0ad-reference/public/`, 0 A.D. 0.28.0) by re-implementing the
engine's template loading — nothing from memory:

- `analyze.py` — re-implements the template loader and merge semantics
  (`ps/TemplateLoader.cpp` inheritance + `simulation2/system/ParamNode.cpp`
  layer merging) and `simulation/components/Trainer.js` (`{civ}`/`{native}`
  substitution + template-existence filtering), then computes the generic
  units (trainable by 2+ civs) with their stats and per-civ trainer lists.
- `buildings.py` — same machinery for structures, driven by the `Builder`
  component lists (`simulation/components/Builder.js`); computes the generic
  buildings (buildable by 2+ civs) with stats and effective trainer lists.
- `technologies.py` — same machinery for technologies, driven by the
  `Researcher/Technologies` lists (`simulation/components/Researcher.js`,
  `{civ}`-or-generic fallback), the `civ`/`notciv` requirement gates
  (`globalscripts/Technologies.js`) and the `autoResearch` civ bonuses;
  computes the generic technologies (available to 2+ civs) with cost,
  requirements and modifications.
- `civ.py` — reuses the three analyses and keeps only what is exclusive to one
  civilisation (single-civ units/buildings/techs); generates the per-civ
  reference (`gauls/`, `romans/`, …) with stats from the fully resolved civ
  templates. Usage: `python3 civ.py <civ-code>` (known: `gaul`, `rome`).

## Usage

```bash
python3 analyze.py        # units        -> out/docs_out/*.md + out/units.json
python3 buildings.py      # buildings    -> out/buildings_out/*.md + out/buildings.json
python3 technologies.py   # technologies -> out/technologies_out/*.md + out/technologies.json
python3 civ.py gaul         # gaul-specific -> out/gauls_out/{units,buildings,technologies}/*.md
python3 civ.py rome         # rome-specific -> out/romans_out/{units,buildings,technologies}/*.md
```

Outputs land in `tools/out/` (gitignored). To refresh the repo docs, review the
output and copy it over:

```bash
cp out/docs_out/*.md ../docs/game_description/generic/units/
cp out/buildings_out/*.md ../docs/game_description/generic/buildings/
cp out/technologies_out/*.md ../docs/game_description/generic/technologies/
cp -r out/gauls_out/* ../docs/game_description/gauls/
cp -r out/romans_out/* ../docs/game_description/romans/
```

## Notes

- The scripts read `/home/ubuntu/0ad-reference/` directly (version-pinned,
  same data the harness runs against).
- Grouping criterion: a unit/building/technology is "generic" when 2+ of the
  15 civs can train/build/research it; single-civ items (heroes, civ-unique
  buildings, civ-specific techs…) are deliberately excluded from the generic
  docs and listed in the JSON dumps (`single_civ`). `civ.py` documents the
  per-civ subset of those single-civ items.
