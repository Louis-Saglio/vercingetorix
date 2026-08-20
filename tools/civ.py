#!/usr/bin/env python3
"""Civ-specific units, buildings and technologies of 0 A.D. 0.28.0.

Usage: python3 civ.py <civ-code>

Reuses the three analyses (analyze.py, buildings.py, technologies.py) and keeps
only what is exclusive to the given civilisation (trained/buildable/
researchable by that civ and by no other civ). Stats come from the fully
resolved civ template.
"""
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyze as A
from buildings import buildable_structures, extract_building_stats, fmt_stats_lines as fmt_building_stats
from technologies import (collect_per_civ as collect_techs, get_tech, has_tech,
                          fmt_stats_lines as fmt_tech_stats)
from auras import (collect_per_civ as collect_auras, get_aura, has_aura,
                   fmt_aura_lines, short_carrier)

CIVS = A.CIVS

# civ code -> (folder name, adjective, plural reference)
CIV_INFO = {
    "gaul": ("gauls", "Gaul", "the gauls"),
    "rome": ("romans", "Roman", "the romans"),
}

# ---------------------------------------------------------------- collect civ-only items

def single_civ_types(per_civ):
    """Map type name -> {civ: full path}, keeping only types owned by exactly one civ."""
    type_civs = defaultdict(dict)
    for civ, items in per_civ.items():
        for full in items:
            type_civs[full.split("/")[-1]][civ] = full
    return {t: cs for t, cs in type_civs.items() if len(cs) == 1}

def civ_units(civ):
    per_civ = {}
    sources = {}
    for c in CIVS:
        units, _structs = A.closure(c)
        per_civ[c] = units
        if c == civ:
            sources = A.training_sources(c, _structs)
    single = single_civ_types(per_civ)
    out = {}
    for typ, cs in single.items():
        if civ in cs:
            out[typ] = {"template": cs[civ], "sources": sources.get(cs[civ], [])}
    return out

def civ_buildings(civ):
    per_civ = {}
    for c in CIVS:
        per_civ[c] = buildable_structures(c)
    single = single_civ_types(per_civ)
    return {t: cs[civ] for t, cs in single.items() if civ in cs}

def civ_techs(civ):
    sources, gated = collect_techs()
    out = {}
    for name, civs in sources.items():
        if list(civs.keys()) == [civ]:
            out[name] = civs[civ]
    return out

def civ_auras(civ):
    carriers, gaia = collect_auras()
    out = {}
    for name, civs in carriers.items():
        if list(civs.keys()) == [civ]:
            out[name] = civs[civ]
    return out

# ---------------------------------------------------------------- markdown

def clean_source(s):
    if s is None:
        return None
    if s.startswith("skirmish/"):
        return None
    return s.split("/")[-1]

def unit_doc(typ, info, outdir, folder, adjective, people, civ):
    tpl = info["template"]
    stats = A.extract_stats(A.resolve(tpl))
    lines = []
    lines.append(f"# {typ}\n")
    lines.append(f"{adjective}-specific unit of 0 A.D. 0.28.0 — only {people} can train"
                 f" it. See `docs/game_description/{folder}/units/README.md` for the"
                 f" method; shared units are documented in"
                 f" `docs/game_description/generic/units/`.")
    lines.append(f"\nStats resolved from `simulation/templates/{tpl}`"
                 f" (full {adjective.lower()} template chain).\n")
    lines.append("## Basic stats\n")
    lines.extend(A.fmt_stats_lines(stats))
    chain = A.promotion_chain(tpl)
    lines.append("")
    pre_ranks = []
    if chain and chain[0][0] == "Elite":
        pre_ranks = ["Advanced", "Elite"]
    elif chain and chain[0][0] == "Advanced":
        pre_ranks = ["Advanced"]
    lines.extend(A.rank_section_lines(stats, chain, pre_ranks))
    if chain and chain[0][0] != "Basic":
        lines.append(f"Note: this unit is already **{chain[0][0]}** rank — in game it also"
                     f" receives the auto-researched"
                     f" `unit_{chain[0][0].lower()}` tech modifications (see the Ranks"
                     f" sections in `docs/game_description/generic/units/`).")
        lines.append("")
    lines.append("## Trained by\n")
    srcs = [s for s in (clean_source(x) for x in info["sources"]) if s]
    src_txt = ", ".join(sorted(srcs)) if srcs else "?"
    lines.append(f"- **{civ}** — `{tpl}` ({src_txt})")
    path = os.path.join(outdir, typ + ".md")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return path

def building_doc(typ, tpl, outdir, folder, adjective, people, civ):
    stats = extract_building_stats(A.resolve(tpl))
    # keep only trainer entries whose unit template exists for this civ
    # (Trainer.js silently drops the others, e.g. army_camp lists
    # infantry_axeman_a but rome has no such file)
    if "trains" in stats:
        eff = []
        for tok in stats["trains"]:
            t = A.substitute(tok, civ, civ)
            if t and A.template_exists(t):
                eff.append(tok)
        stats["trains"] = eff
    lines = []
    lines.append(f"# {typ}\n")
    lines.append(f"{adjective}-specific building of 0 A.D. 0.28.0 — only {people} can"
                 f" build it. See `docs/game_description/{folder}/buildings/README.md`"
                 f" for the method; shared buildings are documented in"
                 f" `docs/game_description/generic/buildings/`.")
    lines.append(f"\nStats resolved from `simulation/templates/{tpl}`"
                 f" (full {adjective.lower()} template chain).")
    if typ.startswith("wallset"):
        lines.append("\nNote: this is a **wall set**, not a single building — it defines"
                     " the wall segments placed with the wall tool. Segment stats come"
                     " from `template_structure_defensive_wall_*`.")
    lines.append("\n## Basic stats\n")
    lines.extend(fmt_building_stats(stats))
    lines.append("\n## Built by\n")
    lines.append(f"- **{civ}** — `{tpl}`")
    path = os.path.join(outdir, typ + ".md")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return path

def tech_doc(name, sources, outdir, folder, adjective, people):
    tpl = get_tech(name)
    lines = []
    lines.append(f"# {name}\n")
    lines.append(f"{adjective}-specific technology of 0 A.D. 0.28.0 — only {people} can"
                 f" get it. See `docs/game_description/{folder}/technologies/README.md`"
                 f" for the method; shared technologies are documented in"
                 f" `docs/game_description/generic/technologies/`.")
    lines.append(f"\nData file: `simulation/data/technologies/{name}.json`.\n")
    lines.append("## Basic stats\n")
    lines.extend(fmt_tech_stats(tpl))
    lines.append(f"\n## {adjective}\n")
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

def aura_doc(name, carriers_list, outdir, folder, adjective, people, civ):
    a = get_aura(name)
    lines = []
    lines.append(f"# {name}\n")
    lines.append(f"{adjective}-specific aura of 0 A.D. 0.28.0 — only {people} can have"
                 f" it. See `docs/game_description/{folder}/auras/README.md` for the"
                 f" method; shared auras are documented in"
                 f" `docs/game_description/generic/auras/`.")
    lines.append(f"\nData file: `simulation/data/auras/{name}.json`.\n")
    lines.append("## Basic stats\n")
    lines.extend(fmt_aura_lines(a))
    lines.append(f"\n## {adjective}\n")
    for c in sorted(set(carriers_list)):
        lines.append(f"- attached by {short_carrier(c)}")
    path = os.path.join(outdir, name.replace("/", "__") + ".md")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return path

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in CIV_INFO:
        print("usage: python3 civ.py <civ-code>  (known: " + ", ".join(sorted(CIV_INFO)) + ")")
        sys.exit(1)
    civ = sys.argv[1]
    folder, adjective, people = CIV_INFO[civ]

    out_root = os.path.join(A.OUT_DIR, f"{folder}_out")
    units_dir = os.path.join(out_root, "units")
    buildings_dir = os.path.join(out_root, "buildings")
    techs_dir = os.path.join(out_root, "technologies")
    auras_dir = os.path.join(out_root, "auras")
    for d in (units_dir, buildings_dir, techs_dir, auras_dir):
        os.makedirs(d, exist_ok=True)

    units = civ_units(civ)
    for typ, info in sorted(units.items()):
        unit_doc(typ, info, units_dir, folder, adjective, people, civ)
    write_readme(
        units_dir,
        f"{adjective}-specific units of 0 A.D. 0.28.0",
        f"One file per unit that **only {people}** can train (single-civ units"
        f" of the `generic/units/` analysis). Stats are the fully resolved"
        f" {adjective.lower()} templates; the shared units are documented in"
        f" `docs/game_description/generic/units/`.",
        [(n, "unit") for n in sorted(units)])

    buildings = civ_buildings(civ)
    for typ, tpl in sorted(buildings.items()):
        building_doc(typ, tpl, buildings_dir, folder, adjective, people, civ)
    extra = ""
    if civ == "gaul":
        extra = ("Note: `structures/gaul/tavern.xml` exists but no builder list references"
                 " it — the tavern is **not buildable** in 0.28 (vestigial, like the"
                 " archery range).")
    write_readme(
        buildings_dir,
        f"{adjective}-specific buildings of 0 A.D. 0.28.0",
        f"One file per building that **only {people}** can build (single-civ"
        f" structures of the `generic/buildings/` analysis). Stats are the fully"
        f" resolved {adjective.lower()} templates; the shared buildings are"
        f" documented in `docs/game_description/generic/buildings/`.",
        [(n, "building") for n in sorted(buildings)],
        extra)

    techs = civ_techs(civ)
    for name, sources in sorted(techs.items()):
        tech_doc(name, sources, techs_dir, folder, adjective, people)
    write_readme(
        techs_dir,
        f"{adjective}-specific technologies of 0 A.D. 0.28.0",
        f"One file per technology that **only {people}** can get (single-civ"
        f" techs of the `generic/technologies/` analysis). Shared technologies are"
        f" documented in `docs/game_description/generic/technologies/`.",
        [(n, "auto-researched" if get_tech(n).get("autoResearch") else "researchable")
         for n in sorted(techs)])

    auras = civ_auras(civ)
    for name, carriers_list in sorted(auras.items()):
        aura_doc(name, carriers_list, auras_dir, folder, adjective, people, civ)
    write_readme(
        auras_dir,
        f"{adjective}-specific auras of 0 A.D. 0.28.0",
        f"One file per aura that **only {people}** can have (single-civ auras of"
        f" the `generic/auras/` analysis): the {adjective.lower()} teambonus (the"
        f" `special/players/{civ}.xml` player aura), hero auras and auras attached"
        f" to {adjective.lower()}-unique entities. Shared auras are documented in"
        f" `docs/game_description/generic/auras/`.",
        [(n, get_aura(n).get("type", "?")) for n in sorted(auras)])

    print(f"{civ} units:", sorted(units))
    print(f"{civ} buildings:", sorted(buildings))
    print(f"{civ} techs:", sorted(techs))
    print(f"{civ} auras:", sorted(auras))

if __name__ == "__main__":
    main()
