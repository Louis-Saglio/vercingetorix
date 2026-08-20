#!/usr/bin/env python3
"""Generic buildings of 0 A.D. 0.28.0: structure types buildable by 2+ civs,
with basic stats resolved from the shared template chain (same loader/merge
reimplementation as analyze.py, which this script imports)."""
import json
import os
import sys
from collections import defaultdict
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyze as A

CIVS = A.CIVS

# ---------------------------------------------------------------- buildability closure

def buildable_structures(civ):
    """Structures civ can build: closure over Builder lists of its units."""
    data = A.civ_data(civ)
    units = set()
    structs = set()
    for ent in data.get("StartEntities", []):
        tpl = ent["Template"]
        if tpl.startswith("units/"):
            units.add(tpl)
    for ws in data.get("WallSets", []):
        structs.add(ws)
    while True:
        nu, ns = set(units), set(structs)
        for u in units:
            tree = A.resolve(u)
            for tok in A.tokens_of(tree, "Builder"):
                t = A.substitute(tok, civ, "")
                if t and t.startswith("structures/") and A.template_exists(t):
                    ns.add(t)
        for s in structs:
            tree = A.resolve(s)
            native = A.structure_native(tree)
            for tok in A.tokens_of(tree, "Trainer"):
                t = A.substitute(tok, civ, native)
                if t and t.startswith("units/") and A.template_exists(t):
                    nu.add(t)
        if nu == units and ns == structs:
            break
        units, structs = nu, ns
    return structs

# ---------------------------------------------------------------- building stats

def extract_building_stats(tree):
    st = {}
    hp = A.fmt_num(A.get_path(tree, "Entity/Health/Max"))
    if hp is not None:
        st["health"] = hp
    armor = {}
    for dk in ("Hack", "Pierce", "Crush"):
        v = A.fmt_num(A.get_path(tree, f"Entity/Resistance/Entity/Damage/{dk}"))
        if v is not None:
            armor[dk] = v
    if armor:
        st["armor"] = armor
    attacks = A.extract_attacks(tree)
    if attacks:
        st["attacks"] = attacks
    res = {}
    for rk in ("food", "wood", "stone", "metal"):
        v = A.fmt_num(A.get_path(tree, f"Entity/Cost/Resources/{rk}"))
        if v is not None:
            res[rk] = v
    if res:
        st["cost_resources"] = res
    bt = A.fmt_num(A.get_path(tree, "Entity/Cost/BuildTime"))
    if bt is not None:
        st["build_time"] = bt
    pop = A.fmt_num(A.get_path(tree, "Entity/Population/Bonus"))
    if pop is not None:
        st["population_bonus"] = pop
    ter = {}
    for k in ("Radius", "Weight"):
        v = A.fmt_num(A.get_path(tree, f"Entity/TerritoryInfluence/{k}"))
        if v is not None:
            ter[k] = v
    root = A.get_path(tree, "Entity/TerritoryInfluence/Root")
    if root is not None:
        ter["Root"] = root
    if ter:
        st["territory"] = ter
    gar = A.fmt_num(A.get_path(tree, "Entity/GarrisonHolder/Max"))
    if gar is not None:
        st["garrison_max"] = gar
    heal = A.fmt_num(A.get_path(tree, "Entity/GarrisonHolder/BuffHeal"))
    if heal is not None and Decimal(heal) != 0:
        st["garrison_heal"] = heal
    vision = A.fmt_num(A.get_path(tree, "Entity/Vision/Range"))
    if vision is not None:
        st["vision"] = vision
    cap = A.fmt_num(A.get_path(tree, "Entity/Capturable/CapturePoints"))
    if cap is not None:
        st["capture_points"] = cap
    terr_req = A.get_path(tree, "Entity/BuildRestrictions/Territory")
    if terr_req:
        st["build_territory"] = terr_req
    place = A.get_path(tree, "Entity/BuildRestrictions/PlacementType")
    if place:
        st["placement"] = place
    dist_class = A.get_path(tree, "Entity/BuildRestrictions/Distance/FromClass")
    dist_min = A.fmt_num(A.get_path(tree, "Entity/BuildRestrictions/Distance/MinDistance"))
    if dist_class and dist_min:
        st["build_distance"] = f"min {dist_min} m from {dist_class}"
    techs = None
    idn = A.child(A.child(tree, "Entity"), "Identity")
    if idn is not None:
        reqs = A.child(idn, "Requirements")
        if reqs is not None:
            techs = A.value(A.child(reqs, "Techs"))
    if techs:
        st["requirements"] = techs
    classes = A.value(A.child(A.child(A.child(tree, "Entity"), "Identity"), "Classes"))
    if classes:
        st["classes"] = classes
    vclasses = A.value(A.child(A.child(A.child(tree, "Entity"), "Identity"), "VisibleClasses"))
    if vclasses:
        st["visible_classes"] = vclasses
    gname = A.value(A.child(A.child(A.child(tree, "Entity"), "Identity"), "GenericName"))
    if gname:
        st["generic_name"] = gname
    train = A.tokens_of(tree, "Trainer")
    if train:
        st["trains"] = train
    return st

DIFF_KEYS = ("health", "armor", "attacks", "cost_resources", "build_time",
             "population_bonus", "territory", "garrison_max", "garrison_heal",
             "vision", "capture_points", "trains")

def stats_signature(st):
    def norm(v):
        if isinstance(v, dict):
            return tuple(sorted((k, norm(x)) for k, x in v.items()))
        if isinstance(v, list):
            return tuple(norm(x) for x in v)
        return v
    return norm({k: st[k] for k in DIFF_KEYS if k in st})

# ---------------------------------------------------------------- markdown

def fmt_resources(res):
    out = []
    for k in ("food", "wood", "stone", "metal"):
        if k in res and Decimal(res[k]) != 0:
            out.append(f"{res[k]} {k}")
    return ", ".join(out)

def fmt_stats_lines(st):
    lines = []
    if "generic_name" in st:
        lines.append(f"- **Generic name:** {st['generic_name']}")
    if "health" in st:
        lines.append(f"- **Health:** {st['health']} HP")
    if "armor" in st:
        lines.append("- **Armor:** " + " / ".join(
            f"{st['armor'][k]} {k.lower()}" for k in ("Hack", "Pierce", "Crush") if k in st["armor"]))
    if "attacks" in st:
        for a in st["attacks"]:
            lines.append(f"- **Attack:** {A.fmt_attack(a)}")
    if "cost_resources" in st:
        cost = fmt_resources(st["cost_resources"])
        if cost:
            lines.append(f"- **Cost:** {cost}")
    if "build_time" in st:
        lines.append(f"- **Build time:** {st['build_time']} s")
    if "population_bonus" in st:
        lines.append(f"- **Population bonus:** +{st['population_bonus']}")
    if "territory" in st:
        t = st["territory"]
        bits = [f"radius {t['Radius']} m" if "Radius" in t else None,
                f"weight {t['Weight']}" if "Weight" in t else None,
                "territory root" if t.get("Root") == "true" else None]
        bits = [b for b in bits if b]
        if bits:
            lines.append(f"- **Territory influence:** " + ", ".join(bits))
    if "garrison_max" in st:
        lines.append(f"- **Garrison:** {st['garrison_max']} slots"
                     + (f" (+{st['garrison_heal']}/s heal)" if "garrison_heal" in st else ""))
    if "vision" in st:
        lines.append(f"- **Vision:** {st['vision']} m")
    if "capture_points" in st:
        lines.append(f"- **Capture points:** {st['capture_points']}")
    if "build_territory" in st:
        lines.append(f"- **Build territory:** {st['build_territory']}")
    if "placement" in st:
        lines.append(f"- **Placement:** {st['placement']}")
    if "build_distance" in st:
        lines.append(f"- **Build distance:** {st['build_distance']}")
    if "requirements" in st:
        lines.append(f"- **Requirements:** {st['requirements']}")
    if "trains" in st:
        lines.append(f"- **Trains:** {' '.join(st['trains'])}")
    if "classes" in st:
        lines.append(f"- **Classes:** {st['classes']}")
    if "visible_classes" in st:
        lines.append(f"- **Visible classes:** {st['visible_classes']}")
    return lines

def fmt_diff_lines(vstats, base, civ=None):
    out = []
    for key in DIFF_KEYS:
        if key not in vstats:
            continue
        if key in base and vstats[key] == base[key]:
            continue
        v = vstats[key]
        if key == "health":
            out.append(f"health {v} HP")
        elif key == "armor":
            out.append("armor " + " / ".join(f"{v[k]} {k.lower()}" for k in ("Hack", "Pierce", "Crush") if k in v))
        elif key == "attacks":
            for a in v:
                out.append(A.fmt_attack(a))
        elif key == "cost_resources":
            c = fmt_resources(v)
            if c:
                out.append(f"cost {c}")
        elif key == "build_time":
            out.append(f"build time {v} s")
        elif key == "population_bonus":
            out.append(f"population +{v}")
        elif key == "territory":
            bits = [f"radius {v['Radius']} m" if "Radius" in v else None,
                    f"weight {v['Weight']}" if "Weight" in v else None,
                    "territory root" if v.get("Root") == "true" else None]
            bits = [b for b in bits if b]
            if bits:
                out.append("territory " + ", ".join(bits))
        elif key == "garrison_max":
            out.append(f"garrison {v} slots")
        elif key == "garrison_heal":
            out.append(f"garrison heal +{v}/s")
        elif key == "vision":
            out.append(f"vision {v} m")
        elif key == "capture_points":
            out.append(f"capture points {v}")
        elif key == "trains":
            if civ is not None:
                eff = []
                for tok in v:
                    t = A.substitute(tok, civ, civ)
                    if t and A.template_exists(t):
                        eff.append(tok)
                out.append(f"trains {' '.join(eff)}")
            else:
                out.append(f"trains {' '.join(v)}")
    return out

def generate(data, outdir):
    os.makedirs(outdir, exist_ok=True)
    files = []
    for typ, d in sorted(data["generic"].items()):
        civs = d["civs"]
        lines = []
        lines.append(f"# {typ}\n")
        lines.append(f"Buildable by **{len(civs)}** civilisations. Generic (non-civ-specific)"
                     f" building of 0 A.D. 0.28.0 — see"
                     f" `docs/game_description/generic/buildings/README.md` for the method.")
        lines.append(f"\nGeneric stats resolved from the shared template"
                     f" `simulation/templates/{d['lca']}` (deepest template common to all"
                     f" civilisation variants; variants may override, see below).")
        if d["lca"] == "template_structure":
            lines.append("\nNote: the civilisation variants of this building share no"
                         " concrete common template — the values below are the abstract"
                         " `template_structure` base; see the overrides for the actual stats.")
        if d["lca"] == "template_wallset":
            lines.append("\nNote: this is a **wall set**, not a single building — it defines"
                         " the wall segments (short/medium/long/tower/gate) placed with the"
                         " wall tool. Segment stats come from"
                         " `template_structure_defensive_wall_*`.")
        lines.append("\n## Basic stats\n")
        lines.extend(fmt_stats_lines(d["stats"]))
        lines.append("\n## Civilisations that can build it\n")
        for c in civs:
            lines.append(f"- **{c}** — `{d['variant_files'][c]}`")
        if d["diffs"]:
            lines.append("\n## Civilisation-specific overrides\n")
            lines.append("These civilisations override the generic stats above (only"
                         " differing values are listed):\n")
            for c in sorted(d["diffs"]):
                lines.append(f"- **{c}** — `{d['variant_files'][c]}`")
                for dl in fmt_diff_lines(d["diffs"][c], d["stats"], civ=c):
                    lines.append(f"  - {dl}")
        path = os.path.join(outdir, typ + ".md")
        with open(path, "w") as f:
            f.write("\n".join(lines) + "\n")
        files.append(path)
    return files

def generate_readme(data):
    """Index README.md for the generated building docs (same directory as the files)."""
    outdir = os.path.join(A.OUT_DIR, "buildings_out")
    lines = []
    lines.append("# Generic buildings of 0 A.D. 0.28.0\n")
    lines.append("One file per **generic building**: a structure type that civilisations can"
                 " **build** in a skirmish game and that is buildable by **more than one**"
                 " civilisation (structures buildable by a single civilisation — civ-unique"
                 " temples, halls, embassies, monuments… — are deliberately excluded).\n")
    lines.append("All data was extracted from the game files, not from memory:"
                 " `/home/ubuntu/0ad-reference/public/simulation/templates/` (0 A.D. 0.28.0,"
                 " the version the harness runs). Template paths below are relative to that"
                 " root.\n")
    lines.append("## Method\n")
    lines.append("- **Buildability:** builder units carry a `Builder` component listing the"
                 " structure templates they can build, with `{civ}` replaced by the owner's"
                 " civ code (`simulation/components/Builder.js`, same mechanics as the"
                 " training `Trainer` lists). An entry is only buildable if the referenced"
                 " template exists; entries pointing to a missing file are silently dropped.")
    lines.append("- **Which civs:** for each of the 15 civs, the analysis resolves every unit"
                 " the civ can train (see `generic/units/`), collects the resolved `Builder`"
                 " lists, and keeps entries whose file exists. The union over civs gives 56"
                 " buildable structure types: **23 buildable by 2+ civs** (documented here)"
                 " and 33 buildable by a single civ (excluded).")
    lines.append("- **Vestigial templates:** `structures/<civ>/range.xml` exists for"
                 " athen/mace/pers/sele/han but no `Builder` list references `range` — the"
                 " archery range is **not buildable** in 0.28 (archers train from the"
                 " barracks). Likewise `structures/pers/apartment_block.xml` and the sele"
                 " academy are unreferenced.")
    lines.append("- **Stats:** each structure file inherits from a shared template chain"
                 " (`parent` attribute, `A|B` = \"B as base, then A on top\"). The generic"
                 " stats shown are the full merge of the deepest template common to all civ"
                 " variants (engine `CParamNode` merge semantics). When a civ variant"
                 " overrides the generic stats, the file lists the differing values. Armor"
                 " is `Resistance/Entity/Damage`; \"trains\" lists are the `Trainer` entries"
                 " (with `{civ}`/`{native}` placeholders; per-civ override lists only show"
                 " entries whose unit template exists for that civ).")
    lines.append("- **Wall sets:** `wallset_palisade`/`wallset_stone` are wall sets, not single"
                 " buildings — they define the wall segments placed with the wall tool"
                 " (stats in `template_structure_defensive_wall_*`).\n")
    lines.append("## Index\n")
    lines.append("| Building | Civilisations | Generic stats template |")
    lines.append("|---|---|---|")
    for typ, d in sorted(data["generic"].items()):
        lines.append(f"| [{typ}]({typ}.md) | {len(d['civs'])} | `{d['lca']}` |")
    lines.append("")
    lines.append("Also see `docs/GAME.md` → \"Simulation templates and data organisation\""
                 " for how the template system works (inheritance, merging, civ"
                 " substitution, builder/trainer lists).")
    path = os.path.join(outdir, "README.md")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return path

def main():
    per_civ = {}
    for civ in CIVS:
        per_civ[civ] = buildable_structures(civ)

    type_civs = defaultdict(dict)
    for civ in CIVS:
        for full in per_civ[civ]:
            typ = full.split("/")[-1]
            type_civs[typ][civ] = full

    generic = {t: sorted(cs) for t, cs in type_civs.items() if len(cs) >= 2}
    single = {t: sorted(cs) for t, cs in type_civs.items() if len(cs) == 1}

    out = {}
    for typ in sorted(generic):
        civs = generic[typ]
        variant_files = [type_civs[typ][c] for c in civs]
        chains = [A.chain_of(f, set()) for f in variant_files]
        common = set.intersection(*chains)
        lca = max(common, key=lambda t: len(A.chain_of(t, set())))
        if lca == "template_structure":
            counts = defaultdict(int)
            for ch in chains:
                for t in ch:
                    counts[t] += 1
            candidates = [t for t in counts if t != "template_structure" and counts[t] >= 2]
            if candidates:
                lca = max(candidates, key=lambda t: (counts[t], len(A.chain_of(t, set()))))
        stats = extract_building_stats(A.resolve(lca))
        diffs = {}
        for c in civs:
            vstats = extract_building_stats(A.resolve(type_civs[typ][c]))
            if stats_signature(vstats) != stats_signature(stats):
                diffs[c] = vstats
        out[typ] = {
            "civs": civs,
            "lca": lca,
            "stats": stats,
            "diffs": diffs,
            "variant_files": {c: type_civs[typ][c] for c in civs},
        }

    data = {
        "generic": out,
        "single_civ": {t: cs for t, cs in sorted(single.items())},
        "total_buildable_types": len(type_civs),
        "generic_count": len(generic),
        "single_civ_count": len(single),
    }
    os.makedirs(A.OUT_DIR, exist_ok=True)
    with open(os.path.join(A.OUT_DIR, "buildings.json"), "w") as f:
        json.dump(data, f, indent=1, sort_keys=True)

    print("total buildable structure types:", len(type_civs))
    print("generic (>=2 civs):", len(generic))
    print("single-civ:", len(single))
    print()
    for t, d in sorted(out.items()):
        print(t, "->", ", ".join(d["civs"]), "| lca:", d["lca"])
    print()
    files = generate(data, os.path.join(A.OUT_DIR, "buildings_out"))
    readme = generate_readme(data)
    print("wrote", len(files), "markdown files + README")

if __name__ == "__main__":
    main()
