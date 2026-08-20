#!/usr/bin/env python3
"""Generic technologies of 0 A.D. 0.28.0: techs available to 2+ civilisations.

Grounds itself in the engine's tech mechanics:
- simulation/components/Researcher.js GetTechnologiesList: researcher tokens
  with {civ} resolve to <civ>-specific tech if it exists, else the "generic"
  fallback; techs the civ cannot research (requirements civ/notciv gates) are
  removed.
- globalscripts/Technologies.js DeriveTechnologyRequirements /
  InterpretTechRequirements: the civ/notciv/any/all requirement operators.
- simulation/components/TechnologyManager.js: autoResearch techs are
  auto-researched by every civ whose requirements allow it.
"""
import json
import os
import sys
from collections import defaultdict
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyze as A
from buildings import buildable_structures

CIVS = A.CIVS
TECH_ROOT = "/home/ubuntu/0ad-reference/public/simulation/data/technologies"

# ---------------------------------------------------------------- tech index

_techs = None  # name (without .json, relative to TECH_ROOT) -> parsed JSON

def tech_index():
    global _techs
    if _techs is not None:
        return _techs
    _techs = {}
    for dirpath, _dirs, files in os.walk(TECH_ROOT):
        for fn in sorted(files):
            if not fn.endswith(".json"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, fn), TECH_ROOT)[:-5]
            with open(os.path.join(dirpath, fn)) as f:
                _techs[rel] = json.load(f)
    return _techs

def has_tech(name):
    return name in tech_index()

def get_tech(name):
    return tech_index().get(name)

# ---------------------------------------------------------------- requirements civ gate

def interp_requirements(civ, op, value):
    """Mirror of globalscripts/Technologies.js InterpretTechRequirements.

    Returns False when the civ cannot research the tech, otherwise a list
    (possibly empty) of requirement objects.
    """
    if op == "civ":
        return [] if (civ is None or civ == value) else False
    if op == "notciv":
        return False if civ == value else []
    if op == "entity":
        reqs = []
        number = value.get("number", value.get("numberOfTypes", 0))
        if number > 0:
            reqs.append({"entities": [{
                "class": value["class"],
                "number": number,
                "check": "count" if "number" in value else "variants",
            }]})
        return reqs
    if op == "tech":
        return [{"techs": [value]}]
    if op == "all":
        reqs = []
        civ_permitted = None  # tri-state: None / False / True
        for sub in value:
            new_op, new_val = next(iter(sub.items()))
            result = interp_requirements(civ, new_op, new_val)
            if new_op == "civ":
                if result is not False:
                    civ_permitted = True
                elif civ_permitted is not True:
                    civ_permitted = False
            elif new_op == "notciv":
                if result is False:
                    return False
            elif new_op in ("any", "all"):
                if result is False:
                    nullres = interp_requirements(None, new_op, new_val)
                    if nullres is False or not len(nullres):
                        civ_permitted = False
                    continue
                # else fall through to the tech/entity merge below
                _merge_reqs(reqs, result)
            elif new_op in ("tech", "entity"):
                if result:
                    _merge_reqs(reqs, result)
            else:
                pass  # engine warns on unknown operators; none exist in 0.28
        if civ_permitted is False:
            return False
        return reqs
    if op == "any":
        reqs = []
        civ_permitted = False
        for sub in value:
            new_op, new_val = next(iter(sub.items()))
            result = interp_requirements(civ, new_op, new_val)
            if new_op == "civ":
                if result is not False:
                    return []
            elif new_op == "notciv":
                if result is False:
                    return False
                civ_permitted = True
            elif new_op == "any":
                if result is False:
                    nullres = interp_requirements(None, new_op, new_val)
                    if nullres is False or not len(nullres):
                        continue
                    return False
                _merge_reqs(reqs, result)
            elif new_op == "all":
                if result is False:
                    continue
                civ_permitted = True
                _merge_reqs(reqs, result)
            elif new_op in ("tech", "entity"):
                if result:
                    _merge_reqs(reqs, result)
            else:
                pass
        if not civ_permitted and not len(reqs):
            return False
        return reqs
    return []

def _merge_reqs(reqs, result):
    """JS 'all' merge: cross-product of requirement groups."""
    if not result:
        return
    if not reqs:
        reqs.extend(result)
        return
    merged = []
    for curr in reqs:
        for res in result:
            new_req = dict(curr)
            for subtype, vals in res.items():
                new_req[subtype] = list(new_req.get(subtype, [])) + list(vals)
            merged.append(new_req)
    reqs[:] = merged

def civ_gate_ok(civ, template):
    """True unless the tech's requirements forbid this civ."""
    reqs = template.get("requirements")
    if not reqs:
        return True
    op, val = next(iter(reqs.items()))
    return interp_requirements(civ, op, val) is not False

# ---------------------------------------------------------------- per-civ collection

def researcher_tokens(tree):
    sec = A.child(A.child(tree, "Entity"), "Researcher")
    if sec is None:
        return []
    techs = A.child(sec, "Technologies")
    if techs is None:
        return []
    return (A.value(techs) or "").split()

def collect_per_civ():
    """tech -> {civ: [structure sources]}; plus civ-gated-out info."""
    sources = defaultdict(lambda: defaultdict(list))   # tech -> civ -> [structs]
    gated_out = defaultdict(list)                      # tech -> civs forbidden by requirements
    for civ in CIVS:
        for s in sorted(buildable_structures(civ)):
            tree = A.resolve(s)
            for tok in researcher_tokens(tree):
                if "{civ}" in tok:
                    civ_tech = tok.replace("{civ}", civ)
                    final = civ_tech if has_tech(civ_tech) else tok.replace("{civ}", "generic")
                else:
                    final = tok
                if not has_tech(final):
                    continue  # placeholder or missing tech: not researchable
                tpl = get_tech(final)
                if not civ_gate_ok(civ, tpl):
                    gated_out[final].append(civ)
                    continue
                sources[final][civ].append(s)
    # auto-research techs (not tied to a building's researcher list)
    for name, tpl in tech_index().items():
        if not tpl.get("autoResearch"):
            continue
        for civ in CIVS:
            if civ in sources.get(name, {}):
                continue
            if civ_gate_ok(civ, tpl):
                sources[name][civ].append(None)  # None = auto-researched
            else:
                gated_out[name].append(civ)
    return sources, gated_out

# ---------------------------------------------------------------- formatting

def fmt_num(x):
    d = Decimal(str(x))
    return str(int(d)) if d == d.to_integral_value() else str(d.normalize())

def fmt_mod(m):
    if "replace" in m:
        head = f"= {m['replace']}"
    elif "multiply" in m:
        head = f"×{m['multiply']}"
    elif "add" in m:
        head = f"+{m['add']}"
    elif "tokens" in m:
        head = f"tokens {m['tokens']}"
    else:
        head = "?"
    s = f"{head} {m['value']}"
    aff = m.get("affects")
    if aff:
        s += " — " + (aff if isinstance(aff, str) else " ".join(aff))
    return s

def fmt_requirements(tpl):
    reqs = tpl.get("requirements")
    if not reqs:
        return None
    return json.dumps(reqs, separators=(",", ": "))

def fmt_stats_lines(tpl):
    lines = []
    if tpl.get("genericName"):
        lines.append(f"- **Name:** {tpl['genericName']}")
    if tpl.get("autoResearch"):
        lines.append("- **Auto-researched:** yes")
    if "top" in tpl and "bottom" in tpl:
        lines.append(f"- **Pair tech:** choose {tpl['top']} or {tpl['bottom']}")
    cost = tpl.get("cost", {})
    if cost:
        parts = [f"{fmt_num(v)} {k}" for k, v in cost.items()]
        lines.append(f"- **Cost:** {', '.join(parts)}")
    if tpl.get("researchTime"):
        lines.append(f"- **Research time:** {fmt_num(tpl['researchTime'])} s")
    reqs = fmt_requirements(tpl)
    if reqs:
        line = f"- **Requirements:** `{reqs}`"
        if tpl.get("requirementsTooltip"):
            line += f" — {tpl['requirementsTooltip']}"
        lines.append(line)
    if tpl.get("supersedes"):
        lines.append(f"- **Supersedes:** {tpl['supersedes']}")
    if tpl.get("replaces"):
        lines.append(f"- **Replaces:** {' '.join(tpl['replaces'])}")
    if tpl.get("tooltip"):
        lines.append(f"- **Effect:** {tpl['tooltip']}")
    mods = tpl.get("modifications", [])
    if mods:
        lines.append("- **Modifications:**")
        for m in mods:
            lines.append(f"  - {fmt_mod(m)}")
    aff = tpl.get("affects")
    if aff:
        lines.append(f"- **Affects:** {aff if isinstance(aff, str) else ' '.join(aff)}")
    return lines

# ---------------------------------------------------------------- output

def generate_markdown(data, outdir):
    os.makedirs(outdir, exist_ok=True)
    files = []
    for name, d in sorted(data["generic"].items()):
        civs = d["civs"]
        tpl = get_tech(name)
        lines = []
        lines.append(f"# {name}\n")
        lines.append(f"Available to **{len(civs)}** civilisations. Generic (non-civ-specific)"
                     f" technology of 0 A.D. 0.28.0 — see"
                     f" `docs/game_description/generic_technologies/README.md` for the method.")
        lines.append(f"\nData file: `simulation/data/technologies/{name}.json`.\n")
        lines.append("## Basic stats\n")
        lines.extend(fmt_stats_lines(tpl))
        lines.append("\n## Civilisations\n")
        for c in civs:
            srcs = [s for s in d["sources"].get(c, []) if s]
            if d["sources"].get(c) and all(s is None for s in d["sources"][c]):
                lines.append(f"- **{c}** — auto-researched")
            else:
                short = ", ".join(sorted(s.split("/")[-1] for s in srcs))
                lines.append(f"- **{c}** — {short}")
        notes = []
        if name.endswith("_generic"):
            base = name[: -len("_generic")]
            civ_variants = sorted(c for c in CIVS if has_tech(f"{base}_{c}"))
            if civ_variants:
                notes.append(", ".join(f"**{c}**" for c in civ_variants)
                              + f" research{'es' if len(civ_variants) == 1 else ''} the civ-specific"
                              + f" variant{'s' if len(civ_variants) > 1 else ''} instead"
                              + f" (`{base}_<civ>`)")
        if d["gated_out"]:
            g = ", ".join(f"**{c}**" for c in sorted(set(d["gated_out"])))
            notes.append(f"{g} cannot research this (forbidden by the tech's requirements)")
        if notes:
            lines.append("\n## Notes\n")
            for n in notes:
                lines.append(f"- {n}")
        path = os.path.join(outdir, name.replace("/", "__") + ".md")
        with open(path, "w") as f:
            f.write("\n".join(lines) + "\n")
        files.append(path)
    return files

def generate_readme(data):
    outdir = os.path.join(A.OUT_DIR, "technologies_out")
    lines = []
    lines.append("# Generic technologies of 0 A.D. 0.28.0\n")
    lines.append("One file per **generic technology**: a tech available to **more than one**"
                 " civilisation — either researchable from one of the civ's buildings"
                 " (`Researcher/Technologies` lists) or auto-researched (`autoResearch: true`,"
                 " e.g. the civ bonus techs in `civbonuses/`). Techs available to a single"
                 " civilisation (civ-specific phase techs, pair choices, unique bonuses) are"
                 " deliberately excluded.\n")
    lines.append("All data was extracted from the game files, not from memory:"
                 " `/home/ubuntu/0ad-reference/public/simulation/data/technologies/`"
                 " (0 A.D. 0.28.0, the version the harness runs).\n")
    lines.append("## Method\n")
    lines.append("- **Researcher lists:** each building's `Researcher/Technologies` token list is"
                 " resolved exactly like `Researcher.js` `GetTechnologiesList`: a `{civ}` token"
                 " resolves to the `<civ>`-specific tech if its file exists, otherwise to the"
                 " `generic` fallback (e.g. `phase_town_{civ}` → `phase_town_athen` for athen,"
                 " `phase_town_generic` for the other civs). Tokens whose tech file does not"
                 " exist are dropped.")
    lines.append("- **Civ gates:** techs carry `requirements` operators `civ`, `notciv`, `all`,"
                 " `any` (`globalscripts/Technologies.js` `InterpretTechRequirements`); a civ"
                 " is excluded when those forbid it (e.g. `unlock_civilians_house_generic` has"
                 " `notciv: kush`, the `civbonuses/` techs are gated to their civs).")
    lines.append("- **Buildings:** the set of buildings a civ owns is the buildable-structure"
                 " closure of `generic_buildings/` (builder lists with `{civ}` substitution and"
                 " template existence).")
    lines.append("- **Auto-research:** techs with `autoResearch: true` are researched"
                 " automatically by every civ whose requirements allow it"
                 " (`TechnologyManager.UpdateAutoResearch`); they appear with"
                 " \"auto-researched\" instead of a building.")
    lines.append("- **Stats:** cost, research time, requirements, supersedes/replaces, tooltip"
                 " and the full `modifications` list (value + operation + affected classes) are"
                 " read from the tech JSON. Per-civ `specificName` and `description` are"
                 " flavour text and not listed.\n")
    lines.append("## Index\n")
    lines.append("| Technology | Civilisations | Type |")
    lines.append("|---|---|---|")
    for name, d in sorted(data["generic"].items()):
        tpl = get_tech(name)
        if tpl.get("autoResearch"):
            kind = "auto"
        elif "top" in tpl:
            kind = "pair"
        else:
            kind = "researchable"
        lines.append(f"| [{name}]({name.replace('/', '__')}.md) | {len(d['civs'])} | {kind} |")
    lines.append("")
    lines.append("Also see `docs/GAME.md` → \"Simulation templates and data organisation\" for"
                 " how the template system works (inheritance, merging, civ substitution,"
                 " researcher lists).")
    path = os.path.join(outdir, "README.md")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return path

def main():
    sources, gated_out = collect_per_civ()

    generic = {t: sorted(cs) for t, cs in sources.items() if len(cs) >= 2}
    single = {t: sorted(cs) for t, cs in sources.items() if len(cs) == 1}

    out = {}
    for name in sorted(generic):
        out[name] = {
            "civs": generic[name],
            "sources": {c: sources[name][c] for c in generic[name]},
            "gated_out": sorted(set(gated_out.get(name, []))),
        }

    data = {
        "generic": out,
        "single_civ": {t: cs for t, cs in sorted(single.items())},
        "total_available_techs": len(sources),
        "generic_count": len(generic),
        "single_civ_count": len(single),
    }
    os.makedirs(A.OUT_DIR, exist_ok=True)
    with open(os.path.join(A.OUT_DIR, "technologies.json"), "w") as f:
        json.dump(data, f, indent=1, sort_keys=True)

    print("total techs available to >=1 civ:", len(sources))
    print("generic (>=2 civs):", len(generic))
    print("single-civ:", len(single))
    print()
    for t, d in sorted(out.items()):
        print(t, "->", ", ".join(d["civs"]))
    print()
    files = generate_markdown(data, os.path.join(A.OUT_DIR, "technologies_out"))
    readme = generate_readme(data)
    print("wrote", len(files), "markdown files + README")

if __name__ == "__main__":
    main()
