#!/usr/bin/env python3
"""Generic auras of 0 A.D. 0.28.0: auras available to 2+ civilisations.

An aura is attached to an entity by the `Auras` component (a `datatype=tokens`
list in the entity template, `simulation/components/Auras.js`); the aura JSON
(`simulation/data/auras/*.json`) defines its type (range/garrison/global/…),
radius, affected classes/players and the value modifications. For each civ we
collect the aura tokens carried by every template the civ can own: its
trainable units, its buildable structures, and its player template
(`special/players/<civ>.xml`, which carries the civ's teambonus aura).
"""
import json
import os
import sys
from collections import defaultdict
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyze as A
from buildings import buildable_structures
from technologies import fmt_mod

CIVS = A.CIVS
AURA_ROOT = "/home/ubuntu/0ad-reference/public/simulation/data/auras"
TEMPLATE_ROOT = "/home/ubuntu/0ad-reference/public/simulation/templates"

# ---------------------------------------------------------------- aura index

_auras = None

def aura_index():
    global _auras
    if _auras is not None:
        return _auras
    _auras = {}
    for dirpath, _dirs, files in os.walk(AURA_ROOT):
        for fn in sorted(files):
            if not fn.endswith(".json"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, fn), AURA_ROOT)[:-5]
            with open(os.path.join(dirpath, fn)) as f:
                _auras[rel] = json.load(f)
    return _auras

def has_aura(name):
    return name in aura_index()

def get_aura(name):
    return aura_index().get(name)

# ---------------------------------------------------------------- token collection

def own_aura_tokens(tree):
    """Aura tokens declared by this template file itself (not inherited)."""
    sec = A.child(A.child(tree, "Entity"), "Auras")
    if sec is None:
        return []
    return (A.value(sec) or "").split()

def template_own_auras(name):
    """Aura tokens declared by the named template file itself."""
    path = A.find_xml(name)
    if not path:
        return []
    root = A.parse(path)
    sec = None
    for sub in root:
        if sub.tag == "Auras":
            sec = sub
            break
    if sec is None:
        return []
    return ((sec.text or "").split())

def collect_per_civ():
    """aura -> {civ: [carrier templates]}; plus auras attached only to gaia
    templates (shared by everyone in practice, carrier = the gaia entity)."""
    carriers = defaultdict(lambda: defaultdict(list))  # aura -> civ -> [templates]
    gaia_carriers = defaultdict(list)                  # aura -> [gaia templates]
    for civ in CIVS:
        owned = set()
        units, _structs = A.closure(civ)
        for u in units:
            owned.add(u)
        for s in buildable_structures(civ):
            owned.add(s)
        owned.add(f"special/players/{civ}")
        for tpl in sorted(owned):
            for name in A.chain_of(tpl, set()):
                for tok in template_own_auras(name):
                    if not has_aura(tok):
                        continue
                    carriers[tok][civ].append(name)
    # gaia attachments (domestic fauna carry the corral auras, usable by everyone)
    gaia_dir = os.path.join(TEMPLATE_ROOT, "gaia")
    if os.path.isdir(gaia_dir):
        for fn in sorted(os.listdir(gaia_dir)):
            if not fn.endswith(".xml"):
                continue
            name = "gaia/" + fn[:-4]
            for tok in template_own_auras(name):
                if has_aura(tok) and name not in gaia_carriers[tok]:
                    gaia_carriers[tok].append(name)
    return carriers, gaia_carriers

# ---------------------------------------------------------------- formatting

def fmt_aura_lines(a):
    lines = []
    if a.get("auraName"):
        lines.append(f"- **Name:** {a['auraName']}")
    typ = a.get("type", "?")
    if a.get("stackable"):
        typ += " (stackable)"
    lines.append(f"- **Type:** {typ}")
    if a.get("radius"):
        lines.append(f"- **Radius:** {a['radius']} m")
    aff = a.get("affects")
    if aff:
        lines.append(f"- **Affects:** {aff if isinstance(aff, str) else ' '.join(aff)}")
    ap = a.get("affectedPlayers")
    if ap:
        lines.append(f"- **Affected players:** {', '.join(ap)}")
    if a.get("requiredTechnology"):
        lines.append(f"- **Required technology:** {a['requiredTechnology']}")
    if a.get("auraDescription"):
        lines.append(f"- **Description:** {a['auraDescription']}")
    mods = a.get("modifications", [])
    if mods:
        lines.append("- **Modifications:**")
        for m in mods:
            lines.append(f"  - {fmt_mod(m)}")
    return lines

def short_carrier(name):
    """Compact carrier description for a template that declares the aura."""
    if name.startswith("template_unit_infantry"):
        return f"`{name}` (all infantry)"
    if name.startswith("template_unit_cavalry"):
        return f"`{name}` (all cavalry)"
    if name.startswith("template_unit_hero"):
        return f"`{name}` (all heroes)"
    if name.startswith("template_unit_champion"):
        return f"`{name}` (all champion infantry)"
    if name.startswith("template_unit_"):
        return f"`{name}`"
    if name.startswith("template_structure_"):
        return f"`{name}` (all civs' {name.split('_', 2)[-1].replace('_', ' ')})"
    if name.startswith("special/players/"):
        return "`special/players/<civ>.xml` (the player's teambonus)"
    return f"`{name}`"

def generate_markdown(data, outdir):
    os.makedirs(outdir, exist_ok=True)
    files = []
    for name, d in sorted(data["generic"].items()):
        civs = d["civs"]
        a = get_aura(name)
        lines = []
        lines.append(f"# {name}\n")
        lines.append(f"Available to **{len(civs)}** civilisations. Generic aura of"
                     f" 0 A.D. 0.28.0 — see `docs/game_description/generic/auras/README.md`"
                     f" for the method.")
        lines.append(f"\nData file: `simulation/data/auras/{name}.json`.\n")
        lines.append("## Basic stats\n")
        lines.extend(fmt_aura_lines(a))
        lines.append("\n## Civilisations\n")
        for c in civs:
            carr = d["carriers"].get(c, [])
            parts = ", ".join(short_carrier(x) for x in sorted(set(carr)))
            lines.append(f"- **{c}** — {parts}")
        if d["gaia"]:
            lines.append("\n## Notes\n")
            lines.append("- Also attached to gaia domestic animals"
                         f" ({', '.join('`' + g + '`' for g in d['gaia'])}) — garrisoning"
                         " them in the corral applies this aura.")
        path = os.path.join(outdir, name.replace("/", "__") + ".md")
        with open(path, "w") as f:
            f.write("\n".join(lines) + "\n")
        files.append(path)
    return files

def generate_readme(data):
    outdir = os.path.join(A.OUT_DIR, "auras_out")
    lines = []
    lines.append("# Generic auras of 0 A.D. 0.28.0\n")
    lines.append("One file per **generic aura**: an aura attached to entities that **2+"
                 " civilisations** can own (their trainable units, buildable structures"
                 " and their player template). Auras carried only by one civilisation's"
                 " entities are documented in the per-civ folders (`gauls/auras/`,"
                 " `romans/auras/`).\n")
    lines.append("All data was extracted from the game files, not from memory:"
                 " `/home/ubuntu/0ad-reference/public/simulation/data/auras/` and"
                 " `/home/ubuntu/0ad-reference/public/simulation/templates/` (0 A.D."
                 " 0.28.0, the version the harness runs).\n")
    lines.append("## Method\n")
    lines.append("- **Attachment:** entities carry aura names in an `Auras` token list"
                 " (`simulation/components/Auras.js`); the aura JSON defines type"
                 " (`range`/`garrison`/`garrisonedUnits`/`formation`/`global`), radius,"
                 " affected classes/players, `stackable`, `requiredTechnology` and the"
                 " `modifications` (same format as tech modifications).")
    lines.append("- **Which civs:** for each of the 15 civs, the analysis walks the full"
                 " inheritance chain of every unit/structure the civ can own plus its"
                 " `special/players/<civ>.xml` player template, and collects the aura"
                 " tokens declared by each template in the chain (token lists merge"
                 " along the chain). The carriers listed per civ are the templates that"
                 " declare the aura.")
    lines.append("- **Gaia-carried auras:** the corral food-trickle auras are attached"
                 " to gaia domestic animals (garrisoned in the corral), so they are"
                 " documented here as shared auras with a note.")
    unreachable = sorted(set(aura_index()) - set(data["generic"]) - set(data["single_civ"]) - set(data["gaia_only"]))
    lines.append("- **Unreachable auras:** " + ", ".join(f"`{u}`" for u in unreachable)
                 + " are attached to entities no civilisation can obtain in a skirmish"
                 " (the catafalque auras — catafalques are not in any builder/trainer"
                 " list; `structures/farmstead_60`/`structures/loyalty_regen` —"
                 " decorative mills and the Ishtar gate; `units/centurion` and the"
                 " mace heroes Craterus/Pyrrhus — unreferenced).\n")
    lines.append("## Index\n")
    lines.append("| Aura | Civilisations | Type |")
    lines.append("|---|---|---|")
    for name, d in sorted(data["generic"].items()):
        typ = get_aura(name).get("type", "?")
        lines.append(f"| [{name}]({name.replace('/', '__')}.md) | {len(d['civs'])} | {typ} |")
    lines.append("")
    lines.append("Also see `docs/GAME.md` → \"Simulation templates and data organisation\""
                 " for how the template system works.")
    path = os.path.join(outdir, "README.md")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return path

def main():
    carriers, gaia_carriers = collect_per_civ()

    generic = {t: sorted(cs) for t, cs in carriers.items() if len(cs) >= 2}
    single = {t: sorted(cs) for t, cs in carriers.items() if len(cs) == 1}

    out = {}
    for name in sorted(generic):
        out[name] = {
            "civs": generic[name],
            "carriers": {c: carriers[name][c] for c in generic[name]},
            "gaia": gaia_carriers.get(name, []),
        }

    data = {
        "generic": out,
        "single_civ": {t: cs for t, cs in sorted(single.items())},
        "gaia_only": {t: cs for t, cs in sorted(gaia_carriers.items())},
        "unreachable": sorted(set(aura_index()) - set(carriers) - set(gaia_carriers)),
        "generic_count": len(generic),
        "single_civ_count": len(single),
    }
    os.makedirs(A.OUT_DIR, exist_ok=True)
    with open(os.path.join(A.OUT_DIR, "auras.json"), "w") as f:
        json.dump(data, f, indent=1, sort_keys=True)

    print("generic (>=2 civs):", len(generic))
    print("single-civ:", len(single))
    print("gaia-only:", len(gaia_carriers))
    print()
    for t, d in sorted(out.items()):
        print(t, "->", ", ".join(d["civs"]))
    print()
    files = generate_markdown(data, os.path.join(A.OUT_DIR, "auras_out"))
    readme = generate_readme(data)
    print("wrote", len(files), "markdown files + README")

if __name__ == "__main__":
    main()
