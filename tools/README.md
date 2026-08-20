# tools/ — 0 A.D. data analysis scripts

Regenerators for the generated reference docs
(`docs/game_description/generic_units/`, `docs/game_description/generic_buildings/`).
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

## Usage

```bash
python3 analyze.py      # units    -> out/docs_out/*.md + out/units.json
python3 buildings.py    # buildings -> out/buildings_out/*.md + out/buildings.json
```

Outputs land in `tools/out/` (gitignored). To refresh the repo docs, review the
output and copy it over:

```bash
cp out/docs_out/*.md ../docs/game_description/generic_units/
cp out/buildings_out/*.md ../docs/game_description/generic_buildings/
```

## Notes

- The scripts read `/home/ubuntu/0ad-reference/` directly (version-pinned,
  same data the harness runs against).
- Grouping criterion: a unit/building is "generic" when 2+ of the 15 civs can
  train/build it; single-civ types (heroes, civ-unique buildings…) are
  deliberately excluded and listed in the JSON dumps (`single_civ`).
