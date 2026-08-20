#!/usr/bin/env python3
"""Gaul-specific units, buildings and technologies of 0 A.D. 0.28.0.

Reuses the three analyses (analyze.py, buildings.py, technologies.py) and keeps
only what is exclusive to the gaul civilisation (trained/buildable/researchable
by gaul and by no other civ). Stats come from the fully resolved gaul template.
"""
import json
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyze as A
from buildings import buildable_structures, extract_building_stats, fmt_stats_lines as fmt_building_stats
from technologies import (collect_per_civ as collect_techs, get_tech, has_tech,
                          fmt_stats_lines as fmt_tech_stats)

CIVS = A.CIVS
GAUL = "gaul"

# ---------------------------------------------------------------- collect gaul-only items

def single_civ_types(per_civ):
    """Map type name -> {civ: full path}, keeping only types owned by exactly one civ."""
    type_civs = defaultdict(dict)
    for civ, items in per_civ.items():
        for full in items:
            type_civs[full.split("/")[-1]][civ] = full
    return {t: cs for t, cs in type_civs.items() if len(cs) == 1}

def gaul_units():
    per_civ = {}
    sources = {}
    for civ in CIVS:
        units, _structs = A.closure(civ)
        per_civ[civ] = units
        if civ == GAUL:
            sources = A.training_sources(civ, _structs)
    single = single_civ_types(per_civ)
    out = {}
    for typ, cs in single.items():
        if GAUL in cs:
            out[typ] = {"template": cs[GAUL], "sources": sources.get(cs[GAUL], [])}
    return out

def gaul_buildings():
    per_civ = {}
    for civ in CIVS:
        per_civ[civ] = buildable_structures(civ)
    single = single_civ_types(per_civ)
    return {t: cs[GAUL] for t, cs in single.items() if GAUL in cs}

def gaul_techs():
    sources, gated = collect_techs()
    out = {}
    for name, civs in sources.items():
        if list(civs.keys()) == [GAUL]:
            out[name] = civs[GAUL]
    return out

# ---------------------------------------------------------------- markdown

def clean_source(s):
    if s is None:
        return None
    if s.startswith("skirmish/"):
        return None
    return s.split("/")[-1]

def unit_doc(typ, info, outdir):
    tpl = info["template"]
    stats = A.extract_stats(A.resolve(tpl))
    lines = []
    lines.append(f"# {typ}\n")
    lines.append("Gaul-specific unit of 0 A.D. 0.28.0 — only the gauls can train it."
                 " See `docs/game_description/gauls/units/README.md` for the method;"
                 " shared units are documented in `docs/game_description/generic/units/`.")
    lines.append(f"\nStats resolved from `simulation/templates/{tpl}`"
                 f" (full gaul template chain).\n")
    lines.append("## Basic stats\n")
    lines.extend(A.fmt_stats_lines(stats))
    lines.append("\n## Trained by\n")
    srcs = [s for s in (clean_source(x) for x in info["sources"]) if s]
    src_txt = ", ".join(sorted(srcs)) if srcs else "?"
    lines.append(f"- **gaul** — `{tpl}` ({src_txt})")
    path = os.path.join(outdir, typ + ".md")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return path

def building_doc(typ, tpl, outdir):
    stats = extract_building_stats(A.resolve(tpl))
    lines = []
    lines.append(f"# {typ}\n")
    lines.append("Gaul-specific building of 0 A.D. 0.28.0 — only the gauls can build it."
                 " See `docs/game_description/gauls/buildings/README.md` for the method;"
                 " shared buildings are documented in"
                 " `docs/game_description/generic/buildings/`.")
    lines.append(f"\nStats resolved from `simulation/templates/{tpl}`"
                 f" (full gaul template chain).\n")
    lines.append("## Basic stats\n")
    lines.extend(fmt_building_stats(stats))
    lines.append("\n## Built by\n")
    lines.append(f"- **gaul** — `{tpl}`")
    path = os.path.join(outdir, typ + ".md")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return path

def tech_doc(name, sources, outdir):
    tpl = get_tech(name)
    lines = []
    lines.append(f"# {name}\n")
    lines.append("Gaul-specific technology of 0 A.D. 0.28.0 — only the gauls can get it."
                 " See `docs/game_description/gauls/technologies/README.md` for the method;"
                 " shared technologies are documented in"
                 " `docs/game_description/generic/technologies/`.")
    lines.append(f"\nData file: `simulation/data/technologies/{name}.json`.\n")
    lines.append("## Basic stats\n")
    lines.extend(fmt_tech_stats(tpl))
    lines.append("\n## Gaul\n")
    if all(s is None for s in sources):
        lines.append("- auto-researched")
    else:
        srcs = [s for s in (clean_source(x) for x in sources) if s]
        lines.append(f"- {', '.join(sorted(srcs))}")
    path = os.path.join(outdir, name.replace("/", "__") + ".md")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return path

def write_readme(outdir, title, intro, index_rows, extra=""):
    lines = [f"# {title}\n", intro + "\n"]
    lines.append("## Index\n")
    lines.append("| Name | Type |")
    lines.append("|---|---|")
    lines.extend(f"| [{n}]({n}) | {k} |" for n, k in index_rows)
    lines.append("")
    if extra:
        lines.append(extra)
    path = os.path.join(outdir, "README.md")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return path

def main():
    out_root = os.path.join(A.OUT_DIR, "gauls_out")
    units_dir = os.path.join(out_root, "units")
    buildings_dir = os.path.join(out_root, "buildings")
    techs_dir = os.path.join(out_root, "technologies")
    for d in (units_dir, buildings_dir, techs_dir):
        os.makedirs(d, exist_ok=True)

    units = gaul_units()
    for typ, info in sorted(units.items()):
        unit_doc(typ, info, units_dir)
    write_readme(
        units_dir,
        "Gaul-specific units of 0 A.D. 0.28.0",
        "One file per unit that **only the gauls** can train (single-civ units"
        " of the `generic/units/` analysis). Stats are the fully resolved gaul"
        " templates; the shared units are documented in"
        " `docs/game_description/generic/units/`.",
        [(n, "unit") for n in sorted(units)])

    buildings = gaul_buildings()
    for typ, tpl in sorted(buildings.items()):
        building_doc(typ, tpl, buildings_dir)
    write_readme(
        buildings_dir,
        "Gaul-specific buildings of 0 A.D. 0.28.0",
        "One file per building that **only the gauls** can build (single-civ"
        " structures of the `generic/buildings/` analysis). Stats are the fully"
        " resolved gaul templates; the shared buildings are documented in"
        " `docs/game_description/generic/buildings/`.",
        [(n, "building") for n in sorted(buildings)],
        "Note: `structures/gaul/tavern.xml` exists but no builder list references"
        " it — the tavern is **not buildable** in 0.28 (vestigial, like the"
        " archery range).")

    techs = gaul_techs()
    for name, sources in sorted(techs.items()):
        tech_doc(name, sources, techs_dir)
    write_readme(
        techs_dir,
        "Gaul-specific technologies of 0 A.D. 0.28.0",
        "One file per technology that **only the gauls** can get (single-civ"
        " techs of the `generic/technologies/` analysis). Shared technologies are"
        " documented in `docs/game_description/generic/technologies/`.",
        [(n, "auto-researched" if get_tech(n).get("autoResearch") else "researchable")
         for n in sorted(techs)])

    print("gaul units:", sorted(units))
    print("gaul buildings:", sorted(buildings))
    print("gaul techs:", sorted(techs))

if __name__ == "__main__":
    main()
