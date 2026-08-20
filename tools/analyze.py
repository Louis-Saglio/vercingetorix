#!/usr/bin/env python3
"""Analyse the 0 A.D. 0.28.0 simulation templates and extract the generic,
trainable units shared by multiple civilisations.

Faithful reimplementation of the engine's template loading:
- ps/TemplateLoader.cpp LoadTemplateFile: search order special/filter -> mixins -> root,
  'A|B' parent = load B first, then apply A on top.
- simulation2/system/ParamNode.cpp ApplyLayer: disable/replace/op/merge/filtered
  attributes, datatype="tokens" list merging with '-token' removal.
- simulation/components/Trainer.js CalculateEntitiesMap: '{civ}' -> owner civ,
  '{native}' -> entity's own civ code, entry dropped if the template does not exist.
"""
import json
import os
import re
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from xml.etree import ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "out")

ROOT = "/home/ubuntu/0ad-reference/public/simulation/templates"
CIVS_DIR = "/home/ubuntu/0ad-reference/public/simulation/data/civs"
CIVS = ["athen", "brit", "cart", "gaul", "germ", "han", "iber", "kush",
        "mace", "maur", "pers", "ptol", "rome", "sele", "spart"]

SPECIAL_ATTRS = {"replace", "op", "merge", "filtered"}

# ---------------------------------------------------------------- template loading

_cache = {}      # name -> merged tree
_et_cache = {}   # path -> ElementTree root

def find_xml(name):
    for d in ("special/filter", "mixins", ""):
        p = os.path.join(ROOT, d, name + ".xml")
        if os.path.exists(p):
            return p
    return None

def parse(path):
    if path not in _et_cache:
        _et_cache[path] = ET.parse(path).getroot()
    return _et_cache[path]

def apply_layer(elem, node):
    """Apply one XML element as a layer onto the merged tree (CParamNode::ApplyLayer).

    Tree representation: a node is a dict; element children are direct keys,
    the element text value is '_v', XML attributes are '@name' keys.
    """
    name = elem.tag
    text = elem.text or ""
    attrs = dict(elem.attrib)

    if "disable" in attrs:
        node.pop(name, None)
        return
    replacing = "replace" in attrs
    if replacing:
        node.pop(name, None)
    filtering = "filtered" in attrs
    if "merge" in attrs:
        if name not in node:
            return
        merging = True
    else:
        merging = False
    op = attrs.get("op")
    if op not in (None, "add", "mul", "mul_round"):
        op = None  # engine logs a warning and continues

    child = node.setdefault(name, {})
    has_set_value = False

    if attrs.get("datatype") == "tokens":
        old = []
        if not replacing:
            old = (child.get("_v", "") or "").split()
        for t in text.split():
            if t.startswith("-"):
                if t[1:] in old:
                    old.remove(t[1:])
            else:
                if t not in old:
                    old.append(t)
        child["_v"] = " ".join(old)
        has_set_value = True

    if op:
        oldval = Decimal((child.get("_v", "") or "0").strip() or "0")
        try:
            mod = Decimal(text.strip() or "0")
        except InvalidOperation:
            mod = Decimal(0)
        if op == "add":
            child["_v"] = str(oldval + mod)
        elif op == "mul":
            child["_v"] = str(oldval * mod)
        elif op == "mul_round":
            child["_v"] = str(int((oldval * mod).to_integral_value()))
        has_set_value = True

    if not has_set_value and not merging:
        child["_v"] = text

    for sub in elem:
        apply_layer(sub, child)

    if filtering:
        keep = {sub.tag for sub in elem}
        kept = {k: v for k, v in child.items() if k in keep}
        v_ = child.get("_v")
        child.clear()
        if v_:
            child["_v"] = v_
        child.update(kept)

    for k, v in attrs.items():
        if k in SPECIAL_ATTRS:
            continue
        child.setdefault("@" + k, {})["_v"] = v

def load_layer(name, node, depth):
    if depth > 100:
        raise RecursionError("template inheritance too deep: " + name)
    if "|" in name:
        a, b = name.split("|", 1)
        load_layer(b, node, depth + 1)
        load_layer(a, node, depth + 1)
        return
    path = find_xml(name)
    if not path:
        return
    root = parse(path)
    parent = root.get("parent")
    if parent:
        load_layer(parent, node, depth + 1)
    apply_layer(root, node)

def resolve(name):
    if name not in _cache:
        node = {}
        load_layer(name, node, 0)
        _cache[name] = node
    return _cache[name]

def template_exists(name):
    return find_xml(name) is not None

# ---------------------------------------------------------------- tree access

def child(node, key):
    if node is None:
        return None
    return node.get(key)

def value(node):
    return None if node is None else (node.get("_v") or None)

def get_path(tree, path):
    cur = tree
    for part in path.split("/"):
        cur = child(cur, part)
        if cur is None:
            return None
    return value(cur)

def tokens_of(tree, section):
    """Resolved token list of <section><Entities datatype=tokens>."""
    sec = child(child(tree, "Entity"), section)
    if sec is None:
        return []
    ent = child(sec, "Entities")
    if ent is None:
        return []
    return (value(ent) or "").split()

# ---------------------------------------------------------------- civ data

def civ_data(code):
    with open(os.path.join(CIVS_DIR, code + ".json")) as f:
        return json.load(f)

# ---------------------------------------------------------------- per-civ closure

def substitute(tok, owner, native):
    tok = tok.replace("{civ}", owner).replace("{native}", native)
    if "{" in tok or "}" in tok:
        return None
    return tok

def structure_native(tree):
    """Identity/Civ of the resolved structure template ('' if unset)."""
    v = get_path(tree, "Entity/Identity/Civ")
    return v if v else ""

def closure(civ):
    data = civ_data(civ)
    units = set()
    structs = set()
    skirmish_map = data.get("SkirmishReplacements", {})

    def repl(tpl):
        # SkirmishReplacer: exact template-name match against SkirmishReplacements
        key = "skirmish/" + tpl.split("/", 1)[1] if tpl.startswith("skirmish/") else None
        if key in skirmish_map:
            return skirmish_map[key]
        return tpl

    for ent in data.get("StartEntities", []):
        tpl = repl(ent["Template"])
        if tpl.startswith("structures/"):
            structs.add(tpl)
        elif tpl.startswith("units/"):
            units.add(tpl)
    for ws in data.get("WallSets", []):
        structs.add(ws)

    # generic skirmish structures any player may end up owning (map-placed defaults)
    skirmish_structs = [
        "skirmish/structures/" + f[:-4]
        for f in sorted(os.listdir(os.path.join(ROOT, "skirmish", "structures")))
        if f.endswith(".xml")
    ]
    for s in skirmish_structs:
        if template_exists(s):
            structs.add(s)

    while True:
        nu, ns = set(units), set(structs)
        for s in structs:
            tree = resolve(s)
            native = structure_native(tree)
            for tok in tokens_of(tree, "Trainer"):
                t = substitute(tok, civ, native)
                if t and t.startswith("units/") and template_exists(t):
                    nu.add(t)
        for u in units:
            tree = resolve(u)
            native = ""  # builder lists use {civ} only; {native} would need unit Identity/Civ
            for tok in tokens_of(tree, "Builder"):
                t = substitute(tok, civ, native)
                if t and t.startswith("structures/") and template_exists(t):
                    ns.add(t)
        if nu == units and ns == structs:
            break
        units, structs = nu, ns
    return units, structs

def training_sources(civ, structs):
    """{unit_token: [structure names]} for a civ's owned structures."""
    out = defaultdict(list)
    for s in sorted(structs):
        tree = resolve(s)
        native = structure_native(tree)
        for tok in tokens_of(tree, "Trainer"):
            t = substitute(tok, civ, native)
            if t and t.startswith("units/") and template_exists(t):
                out[t].append(s)
    return dict(out)

# ---------------------------------------------------------------- inheritance chains

def chain_of(name, acc):
    """Set of templates in the inheritance closure of `name` (pipes expanded)."""
    if name in acc:
        return acc
    if "|" in name:
        a, b = name.split("|", 1)
        acc.add(a)
        chain_of(b, acc)
        return acc
    acc.add(name)
    path = find_xml(name)
    if path:
        parent = parse(path).get("parent")
        if parent:
            chain_of(parent, acc)
    return acc

# ---------------------------------------------------------------- stat extraction

DIFF_KEYS = ("health", "health_regen", "armor", "attacks", "walk_speed",
             "run_speed", "vision", "cost_resources", "build_time", "population",
             "gather")

def fmt_num(s):
    if s is None:
        return None
    d = Decimal(s)
    if d == d.to_integral_value():
        return str(int(d))
    return str(d.normalize())

def extract_attacks(tree):
    atk_node = child(child(tree, "Entity"), "Attack")
    attacks = []
    if atk_node is not None:
        for kind, node in sorted(atk_node.items()):
            if kind.startswith("@") or kind == "_v":
                continue
            if kind not in ("Melee", "Ranged", "Charge", "Capture"):
                continue  # skip Slaughter (not a requested stat)
            a = {}
            a["type"] = kind
            name = value(child(node, "AttackName"))
            if name:
                a["name"] = name
            dmg = child(node, "Damage")
            if dmg is not None:
                parts = {}
                for dk in ("Hack", "Pierce", "Crush"):
                    dv = fmt_num(value(child(dmg, dk)))
                    if dv is not None:
                        parts[dk] = dv
                if parts:
                    a["damage"] = parts
            if kind == "Capture":
                cap = fmt_num(value(child(node, "Capture")))
                if cap is not None:
                    a["capture_strength"] = cap
            for k in ("MaxRange", "MinRange", "PrepareTime", "RepeatTime"):
                v = fmt_num(value(child(node, k)))
                if v is not None:
                    a[k] = v
            bonus_node = child(node, "Bonuses")
            if bonus_node is not None:
                bonuses = []
                for bn, bnode in sorted(bonus_node.items()):
                    if bn.startswith("@") or bn == "_v":
                        continue
                    classes = value(child(bnode, "Classes"))
                    mult = fmt_num(value(child(bnode, "Multiplier")))
                    if classes and mult:
                        bonuses.append({"classes": classes, "multiplier": mult})
                if bonuses:
                    a["bonuses"] = bonuses
            pref = value(child(node, "PreferredClasses"))
            if pref:
                a["preferred"] = pref
            restr = value(child(node, "RestrictedClasses"))
            if restr:
                a["restricted"] = restr
            attacks.append(a)
    return attacks

def extract_stats(tree):
    e = child(tree, "Entity")
    st = {}
    hp = fmt_num(get_path(tree, "Entity/Health/Max"))
    if hp is not None:
        st["health"] = hp
    regen = fmt_num(get_path(tree, "Entity/Health/RegenRate"))
    if regen is not None:
        st["health_regen"] = regen
    armor = {}
    for dk in ("Hack", "Pierce", "Crush"):
        v = fmt_num(get_path(tree, f"Entity/Resistance/Entity/Damage/{dk}"))
        if v is not None:
            armor[dk] = v
    if armor:
        st["armor"] = armor
    attacks = extract_attacks(tree)
    if attacks:
        st["attacks"] = attacks
    walk = fmt_num(get_path(tree, "Entity/UnitMotion/WalkSpeed"))
    if walk is not None:
        st["walk_speed"] = walk
    mult = fmt_num(get_path(tree, "Entity/UnitMotion/RunMultiplier"))
    if mult is not None and walk is not None:
        run = Decimal(walk) * Decimal(mult)
        run = run.quantize(Decimal("0.01"))
        st["run_speed"] = str(run.normalize())
    vision = fmt_num(get_path(tree, "Entity/Vision/Range"))
    if vision is not None:
        st["vision"] = vision
    res = {}
    for rk in ("food", "wood", "stone", "metal"):
        v = fmt_num(get_path(tree, f"Entity/Cost/Resources/{rk}"))
        if v is not None:
            res[rk] = v
    if res:
        st["cost_resources"] = res
    bt = fmt_num(get_path(tree, "Entity/Cost/BuildTime"))
    if bt is not None:
        st["build_time"] = bt
    pop = fmt_num(get_path(tree, "Entity/Cost/Population"))
    if pop is not None:
        st["population"] = pop
    classes = value(child(child(e, "Identity"), "Classes"))
    if classes:
        st["classes"] = classes
    vclasses = value(child(child(e, "Identity"), "VisibleClasses"))
    if vclasses:
        st["visible_classes"] = vclasses
    gname = value(child(child(e, "Identity"), "GenericName"))
    if gname:
        st["generic_name"] = gname
    rank = value(child(child(e, "Identity"), "Rank"))
    if rank:
        st["rank"] = rank
    promo = value(child(child(e, "Promotion"), "Entity"))
    if promo:
        st["promotes_to"] = promo
    rg = child(e, "ResourceGatherer")
    if rg is not None:
        gather = {}
        base = fmt_num(value(child(rg, "BaseSpeed")))
        if base is not None and Decimal(base) != 1:
            gather["base_speed"] = base
        rates_node = child(rg, "Rates")
        if rates_node is not None:
            rates = {}
            for k, v in sorted(rates_node.items()):
                if k.startswith("@") or k == "_v":
                    continue
                rv = fmt_num(value(v))
                if rv is not None:
                    rates[k] = rv
            if rates:
                gather["rates"] = rates
        cap_node = child(rg, "Capacities")
        if cap_node is not None:
            caps = {}
            for k, v in sorted(cap_node.items()):
                if k.startswith("@") or k == "_v":
                    continue
                cv = fmt_num(value(v))
                if cv is not None:
                    caps[k] = cv
            if caps:
                gather["capacities"] = caps
        if gather:
            st["gather"] = gather
    return st

def stats_signature(st):
    """Comparable signature for per-civ diffing (combat/econ keys only)."""
    def norm(v):
        if isinstance(v, dict):
            return tuple(sorted((k, norm(x)) for k, x in v.items()))
        if isinstance(v, list):
            return tuple(sorted(norm(x) for x in v))
        return v
    return norm({k: st[k] for k in DIFF_KEYS if k in st})

# ---------------------------------------------------------------- main

def main():
    # per-civ closures
    per_civ_units = {}
    per_civ_structs = {}
    per_civ_sources = {}
    for civ in CIVS:
        units, structs = closure(civ)
        per_civ_units[civ] = units
        per_civ_structs[civ] = structs
        per_civ_sources[civ] = training_sources(civ, structs)

    # token type name -> {civ: full template path}
    type_civs = defaultdict(dict)
    type_sources = defaultdict(dict)  # type -> {civ: [structs]}
    for civ in CIVS:
        for full in per_civ_units[civ]:
            typ = full.split("/")[-1]
            type_civs[typ][civ] = full
            type_sources[typ][civ] = per_civ_sources[civ].get(full, [])

    generic = {t: sorted(cs) for t, cs in type_civs.items() if len(cs) >= 2}
    single = {t: sorted(cs) for t, cs in type_civs.items() if len(cs) == 1}

    out = {}
    for tok in sorted(generic):
        civs = generic[tok]
        variant_files = [type_civs[tok][c] for c in civs]
        chains = [chain_of(f, set()) for f in variant_files]
        common = set.intersection(*chains)
        # deepest common ancestor
        lca = max(common, key=lambda t: len(chain_of(t, set())))
        # if all variants only share the abstract root, fall back to the deepest
        # template used by at least two variant chains
        if lca == "template_unit":
            counts = defaultdict(int)
            for ch in chains:
                for t in ch:
                    counts[t] += 1
            candidates = [t for t in counts if t != "template_unit" and counts[t] >= 2]
            if candidates:
                lca = max(candidates, key=lambda t: (counts[t], len(chain_of(t, set()))))
        stats = extract_stats(resolve(lca))
        # per-civ stat diffs vs generic
        diffs = {}
        for c in civs:
            vstats = extract_stats(resolve(type_civs[tok][c]))
            if stats_signature(vstats) != stats_signature(stats):
                diffs[c] = vstats
        out[tok] = {
            "civs": civs,
            "lca": lca,
            "stats": stats,
            "diffs": diffs,
            "sources": {c: type_sources[tok][c] for c in civs},
            "variant_files": {c: type_civs[tok][c] for c in civs},
        }

    data = {
        "generic": out,
        "single_civ": {t: cs for t, cs in sorted(single.items())},
        "total_trainer_types": len(type_civs),
        "generic_count": len(generic),
        "single_civ_count": len(single),
    }
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "units.json"), "w") as f:
        json.dump(data, f, indent=1, sort_keys=True)

    print("total trainable unit types:", len(type_civs))
    print("generic (>=2 civs):", len(generic))
    print("single-civ:", len(single))
    print()
    for t, d in sorted(out.items()):
        print(t, "->", ", ".join(d["civs"]), "| lca:", d["lca"])
    print()
    files = generate_markdown(data, os.path.join(OUT_DIR, "docs_out"))
    readme = generate_readme(data)
    print("wrote", len(files), "markdown files + README")

# ---------------------------------------------------------------- markdown output

SECONDS_KEYS = {"PrepareTime": "prepare", "RepeatTime": "repeat"}

def sec(ms):
    d = Decimal(ms) / 1000
    s = str(d.normalize())
    return s + " s"

def fmt_damage(d):
    out = []
    for k in ("Hack", "Pierce", "Crush"):
        if k in d and Decimal(d[k]) != 0:
            out.append(f"{d[k]} {k.lower()}")
    return " + ".join(out)

def fmt_bonuses(bonuses):
    return "; ".join(f"{b['multiplier']}× vs {b['classes']}" for b in bonuses)

def fmt_attack(a):
    parts = [a["type"]]
    if a.get("name") and a["name"] != a["type"]:
        parts.append(f'"{a["name"]}"')
    line = " ".join(parts)
    bits = []
    if "capture_strength" in a:
        bits.append(f"strength {a['capture_strength']}")
    if "damage" in a:
        bits.append(f"damage {fmt_damage(a['damage'])}")
    if "MaxRange" in a:
        bits.append(f"range {a['MaxRange']} m")
    for k, label in SECONDS_KEYS.items():
        if k in a:
            bits.append(f"{label} {sec(a[k])}")
    if "bonuses" in a:
        bits.append(f"bonus {fmt_bonuses(a['bonuses'])}")
    if "preferred" in a:
        bits.append(f"preferred {a['preferred']}")
    if "restricted" in a:
        bits.append(f"restricted {a['restricted']}")
    return (line + " — " + " — ".join(bits)) if bits else line

def fmt_resources(res):
    out = []
    for k in ("food", "wood", "stone", "metal"):
        if k in res and Decimal(res[k]) != 0:
            out.append(f"{res[k]} {k}")
    return ", ".join(out)

def fmt_gather(g):
    """Compact rendering of ResourceGatherer data (rates grouped by resource type)."""
    out = []
    if "base_speed" in g:
        out.append(f"base speed ×{g['base_speed']}")
    rates = g.get("rates", {})
    if rates:
        grouped = {}
        for k, v in sorted(rates.items()):
            generic, _, specific = k.partition(".")
            grouped.setdefault(generic, []).append((specific, v))
        for generic in grouped:
            grouped[generic].sort(key=lambda e: (e[0] == "ruins", e[0]))
        parts = []
        for generic in ("food", "wood", "stone", "metal", "treasure"):
            if generic not in grouped:
                continue
            entries = grouped.pop(generic)
            if len(entries) == 1 and entries[0][0] == "":
                parts.append(f"{generic} {entries[0][1]}")
            else:
                parts.append(generic + ": " + ", ".join(f"{s} {v}" for s, v in entries))
        for generic in sorted(grouped):
            entries = grouped[generic]
            parts.append(generic + ": " + ", ".join(f"{s} {v}" for s, v in entries))
        out.append("rates: " + "; ".join(parts) + " /s")
    caps = g.get("capacities", {})
    if caps:
        ordered = [f"{caps[k]} {k}" for k in ("food", "wood", "stone", "metal") if k in caps]
        ordered += [f"{v} {k}" for k, v in sorted(caps.items()) if k not in ("food", "wood", "stone", "metal")]
        out.append("capacity: " + ", ".join(ordered))
    return out

def fmt_stats_lines(st):
    lines = []
    if "generic_name" in st:
        lines.append(f"- **Generic name:** {st['generic_name']}")
    if "health" in st:
        regen = st.get("health_regen")
        lines.append(f"- **Health:** {st['health']} HP"
                     + (f" (+{regen}/s regen)" if regen and Decimal(regen) != 0 else ""))
    elif "health_regen" in st:
        lines.append(f"- **Health regen:** {st['health_regen']}/s")
    if "armor" in st:
        parts = []
        for k in ("Hack", "Pierce", "Crush"):
            if k in st["armor"]:
                parts.append(f"{st['armor'][k]} {k.lower()}")
        lines.append("- **Armor:** " + " / ".join(parts))
    if "attacks" in st:
        for a in st["attacks"]:
            lines.append(f"- **Attack:** {fmt_attack(a)}")
    if "walk_speed" in st:
        lines.append(f"- **Speed:** walk {st['walk_speed']} m/s"
                     + (f", run {st['run_speed']} m/s" if "run_speed" in st else ""))
    if "vision" in st:
        lines.append(f"- **Vision:** {st['vision']} m")
    if "cost_resources" in st:
        cost = fmt_resources(st["cost_resources"])
        if cost:
            lines.append(f"- **Cost:** {cost}")
    if "build_time" in st:
        lines.append(f"- **Build time:** {st['build_time']} s")
    if "population" in st:
        lines.append(f"- **Population:** {st['population']}")
    if "gather" in st:
        for gline in fmt_gather(st["gather"]):
            lines.append(f"- **Gather:** {gline}")
    if "classes" in st:
        lines.append(f"- **Classes:** {st['classes']}")
    if "visible_classes" in st:
        lines.append(f"- **Visible classes:** {st['visible_classes']}")
    if "rank" in st:
        lines.append(f"- **Rank:** {st['rank']}")
    return lines

def fmt_diff_lines(vstats, base):
    """Compact lines for the stats that a civ variant overrides."""
    out = []
    for key in DIFF_KEYS:
        if key not in vstats:
            continue
        if key in base and vstats[key] == base[key]:
            continue
        v = vstats[key]
        if key == "health":
            out.append(f"health {v} HP")
        elif key == "health_regen":
            if Decimal(v) != 0:
                out.append(f"health regen {v}/s")
        elif key == "armor":
            parts = []
            for dk in ("Hack", "Pierce", "Crush"):
                if dk in v:
                    parts.append(f"{v[dk]} {dk.lower()}")
            out.append("armor " + " / ".join(parts))
        elif key == "attacks":
            for a in v:
                out.append(fmt_attack(a))
        elif key == "walk_speed":
            out.append(f"walk {v} m/s")
        elif key == "run_speed":
            out.append(f"run {v} m/s")
        elif key == "vision":
            out.append(f"vision {v} m")
        elif key == "cost_resources":
            c = fmt_resources(v)
            if c:
                out.append(f"cost {c}")
        elif key == "build_time":
            out.append(f"build time {v} s")
        elif key == "population":
            out.append(f"population {v}")
        elif key == "gather":
            out.extend(fmt_gather(v))
    return out

def clean_source(s):
    if s.startswith("skirmish/"):
        return None
    return s.split("/")[-1]

def generate_markdown(data, outdir):
    os.makedirs(outdir, exist_ok=True)
    files = []
    for tok, d in sorted(data["generic"].items()):
        civs = d["civs"]
        lines = []
        lines.append(f"# {tok}\n")
        lines.append(f"Trained by **{len(civs)}** civilisations. Generic (non-civ-specific) unit"
                     f" of 0 A.D. 0.28.0 — see `docs/game_description/generic/units/README.md`"
                     f" for the method.")
        lines.append(f"\nGeneric stats resolved from the shared template"
                     f" `simulation/templates/{d['lca']}` (deepest template common to all"
                     f" civilisation variants; variants may override, see below).")
        if d["lca"] == "template_unit":
            lines.append("\nNote: the civilisation variants of this unit share no"
                         " concrete common template — the values below are the abstract"
                         " `template_unit` base; see the overrides for the actual stats.")
        lines.append("\n## Basic stats\n")
        lines.extend(fmt_stats_lines(d["stats"]))
        lines.append("\n## Civilisations that can train it\n")
        for c in civs:
            srcs = [s for s in (clean_source(x) for x in d["sources"][c]) if s]
            src_txt = ", ".join(srcs) if srcs else "?"
            lines.append(f"- **{c}** — `{d['variant_files'][c]}` ({src_txt})")
        if d["diffs"]:
            lines.append("\n## Civilisation-specific overrides\n")
            lines.append("These civilisations override the generic stats above (only"
                         " differing values are listed):\n")
            for c in sorted(d["diffs"]):
                diff_lines = fmt_diff_lines(d["diffs"][c], d["stats"])
                lines.append(f"- **{c}** — `{d['variant_files'][c]}`")
                for dl in diff_lines:
                    lines.append(f"  - {dl}")
        path = os.path.join(outdir, tok + ".md")
        with open(path, "w") as f:
            f.write("\n".join(lines) + "\n")
        files.append(path)
    return files

def generate_readme(data):
    """Index README.md for the generated unit docs (same directory as the files)."""
    outdir = os.path.join(OUT_DIR, "docs_out")
    lines = []
    lines.append("# Generic units of 0 A.D. 0.28.0\n")
    lines.append("One file per **generic unit**: a unit type trainable in a skirmish game by"
                 " **more than one** civilisation (unit types trainable by a single"
                 " civilisation — heroes, civ-specific champions, unique mercenaries — are"
                 " deliberately excluded).\n")
    lines.append("All data was extracted from the game files, not from memory:"
                 " `/home/ubuntu/0ad-reference/public/simulation/templates/` (0 A.D. 0.28.0,"
                 " the version the harness runs). Template paths below are relative to that"
                 " root.\n")
    lines.append("## Method\n")
    lines.append("- **Training data:** each civilisation's buildings carry a `Trainer` component"
                 " listing the entity templates it can train, with `{civ}` replaced by the"
                 " owner's civ code and `{native}` by the building's own civ code"
                 " (`simulation/components/Trainer.js`). An entry is only trainable if the"
                 " referenced template exists (`TemplateExists`); entries pointing to a"
                 " missing file are silently dropped.")
    lines.append("- **Which civs:** for each of the 15 civs, the analysis resolves every"
                 " structure the civ can own (its `structures/<civ>/*.xml`, the starting"
                 " entities from `simulation/data/civs/<civ>.json`, and the generic"
                 " `skirmish/structures/default_*`), collects the resolved `Trainer` lists,"
                 " and keeps entries whose file exists. The union over civs gives 133"
                 " trainable unit types: **36 trained by 2+ civs** (documented here) and 97"
                 " trained by a single civ (excluded).")
    lines.append("- **Stats:** each unit file inherits from a shared template chain"
                 " (`parent` attribute, `A|B` = \"B as base, then A on top\"). The generic"
                 " stats shown are the full merge of the deepest template common to all civ"
                 " variants (the engine's `CParamNode` merge semantics: child overrides,"
                 " token lists merged, `disable`/`replace`/`op` attributes honoured). When"
                 " a civ variant overrides the generic stats, the file lists the differing"
                 " values. Armor is the `Resistance/Entity/Damage` values (hack/pierce/"
                 "crush); speeds are `UnitMotion` walk/run; prepare/repeat times are in"
                 " seconds (templates store milliseconds).")
    lines.append("- **Capture & gathering:** the `Capture` attack line shows the capture"
                 " strength, range, repeat time and restricted classes (from the"
                 " `Attack/Capture` section). \"Gather\" lines show the"
                 " `ResourceGatherer` data: base speed multiplier, the rates per"
                 " resource subtype (e.g. `food.fruit`; the engine looks up the"
                 " specific subtype first, then the generic resource type —"
                 " `ResourceGatherer.js` `GetTargetGatherRate`), and the carrying"
                 " capacities.")
    lines.append("- **Excluded from these files:** the `Slaughter` attack (used to kill"
                 " corralled animals) and promotion targets (units trained directly"
                 " only).\n")
    lines.append("## Index\n")
    lines.append("| Unit | Civilisations | Generic stats template |")
    lines.append("|---|---|---|")
    for tok, d in sorted(data["generic"].items()):
        lines.append(f"| [{tok}]({tok}.md) | {len(d['civs'])} | `{d['lca']}` |")
    lines.append("")
    lines.append("Also see `docs/GAME.md` → \"Simulation templates and data organisation\" for"
                 " how the template system works (inheritance, merging, civ substitution,"
                 " trainer lists).")
    path = os.path.join(outdir, "README.md")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return path

if __name__ == "__main__":
    main()
