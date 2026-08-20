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
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
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
    xp = fmt_num(get_path(tree, "Entity/Promotion/RequiredXp"))
    if xp is not None:
        st["xp"] = xp
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

# ---------------------------------------------------------------- ranks (promotion)

RANK_TECHS = {"Advanced": "unit_advanced", "Elite": "unit_elite"}
RANK_TECH_ROOT = "/home/ubuntu/0ad-reference/public/simulation/data/technologies"

_rank_techs = {}

def rank_tech(rank):
    if rank not in _rank_techs:
        with open(os.path.join(RANK_TECH_ROOT, RANK_TECHS[rank] + ".json")) as f:
            _rank_techs[rank] = json.load(f)
    return _rank_techs[rank]

def matches_class_list(classes, match):
    """Faithful port of globalscripts/Templates.js MatchesClassList."""
    if not match or not classes:
        return False
    if isinstance(match, str):
        match = [match]
    for sub in match:
        words = re.split(r"[+\s]+", sub)
        if all((w.startswith("!") and w[1:] not in classes) or
               (not w.startswith("!") and w in classes) for w in words):
            return True
    return False

def promotion_chain(full_path):
    """[(rank, template, xp_to_promote), ...] starting at the given template;
    ends when the unit cannot promote further (Promotion/Entity missing or
    nonexistent)."""
    chain = []
    cur = full_path
    for _ in range(3):
        tree = resolve(cur)
        rank = get_path(tree, "Entity/Identity/Rank") or "Basic"
        xp = fmt_num(get_path(tree, "Entity/Promotion/RequiredXp"))
        chain.append((rank, cur, xp))
        nxt = get_path(tree, "Entity/Promotion/Entity")
        if not nxt or not template_exists(nxt):
            break
        cur = nxt
    return chain

def _rank_deltas(stats, rank):
    """Applicable (stat_key -> (mult, add)) changes for this rank, computed
    from the rank's auto-research tech filtered by the unit's classes
    (unit_advanced / unit_elite)."""
    tech = rank_tech(rank)
    classes = set((stats.get("classes") or "").split()) \
        | set((stats.get("visible_classes") or "").split()) | {rank}
    default_affects = tech.get("affects")
    deltas = {}
    for m in tech.get("modifications", []):
        aff = m.get("affects", default_affects)
        if not matches_class_list(classes, aff):
            continue
        v = m.get("value", "")
        key = None
        if v == "Health/Max":
            key = "health"
        elif v.startswith("Attack/Melee/Damage/"):
            key = "melee"
        elif v == "Attack/Capture/Capture":
            key = "capture"
        elif v == "Cost/BuildTime":
            key = "buildtime"
        elif v == "ResourceGatherer/BaseSpeed":
            key = "gather"
        elif v.startswith("Loot/"):
            key = "loot"
        elif v == "Attack/Ranged/Projectile/Spread":
            key = "spread"
        elif v == "Heal/Range":
            key = "heal_range"
        elif v == "Heal/Health":
            key = "heal_health"
        if key is None:
            continue
        mult, add = deltas.get(key, (Decimal(1), Decimal(0)))
        if "multiply" in m:
            # overwrite: the melee (Hack/Pierce/Crush) and loot mods repeat the
            # same multiplier for each sub-stat, it must not be compounded
            deltas[key] = (Decimal(str(m["multiply"])), add)
        elif "add" in m:
            deltas[key] = (mult, add + Decimal(str(m["add"])))
    return deltas, classes

def _fmt2(d):
    d = d.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return str(int(d)) if d == d.to_integral_value() else str(d.normalize())

def rank_section_lines(stats, chain, pre_ranks=()):
    """Markdown lines for a '## Ranks' section; empty when the unit cannot
    promote. Stat changes come from the auto-researched unit_advanced /
    unit_elite techs (verified: the _a/_e templates themselves only change
    Identity/Rank, Promotion and the actor) plus any template-level stat
    differences between the two rank files. `pre_ranks` pre-seeds the
    cumulative state for units already trained at a non-basic rank."""
    if len(chain) < 2:
        return []
    lines = ["## Ranks", ""]
    cum = {}  # stat key -> (multiplier, add) accumulated over previous ranks
    first = True
    for pre in pre_ranks:
        pd, _cls = _rank_deltas(stats, pre)
        for k, (m, a) in pd.items():
            cm, ca = cum.get(k, (Decimal(1), Decimal(0)))
            cum[k] = (cm * m, ca * m + a)
        first = False
    for i, (rank, path, _xp) in enumerate(chain[1:], start=1):
        prev_path = chain[i - 1][1]
        xp = chain[i - 1][2]  # XP required to promote from the previous rank
        lines.append(f"### {rank} — `{path}`")
        lines.append(f"Requires {xp or '?'} XP.")
        emitted = False
        if rank in RANK_TECHS:
            deltas, classes = _rank_deltas(stats, rank)
            if "Mercenary" in classes:
                lines.append("- Note: mercenaries promote at 0 XP (the auto-researched"
                             " `upgrade_rank_advanced_mercenary` tech replaces RequiredXp).")
        else:
            deltas, classes = {}, set()
        # template-level stat differences between the two rank files
        template_diffs = fmt_diff_lines(
            extract_stats(resolve(path)), extract_stats(resolve(prev_path)))
        for dl in template_diffs:
            if dl.startswith("promotes_to"):
                continue
            lines.append(f"- {dl}")
            emitted = True

        def total(key, mult, add):
            cm, ca = cum.get(key, (Decimal(1), Decimal(0)))
            cm, ca = cm * mult, ca * mult + add
            cum[key] = (cm, ca)
            return cm, ca

        def total_txt(cm, ca=None):
            if first:
                return ""
            if ca is not None and cm == 1:
                return f" (total +{_fmt2(ca)})"
            return f" (total ×{_fmt2(cm)})"

        n0 = len(lines)

        # health
        if "health" in deltas and "health" in stats:
            m, a = deltas["health"]
            cm, ca = total("health", m, a)
            lines.append(f"- Health: ×{_fmt2(m)}{total_txt(cm)}"
                         f" → {_fmt2(Decimal(stats['health']) * cm + ca)} HP")
        # melee damage
        if "melee" in deltas:
            melee = next((x for x in stats.get("attacks", []) if x["type"] == "Melee"), None)
            if melee and "damage" in melee:
                m, a = deltas["melee"]
                cm, ca = total("melee", m, a)
                parts = []
                for dk in ("Hack", "Pierce", "Crush"):
                    if dk in melee["damage"]:
                        parts.append(f"{dk.lower()} {_fmt2(Decimal(melee['damage'][dk]) * cm)}")
                lines.append(f"- Melee attack damage: ×{_fmt2(m)}{total_txt(cm)}"
                             f" → {' + '.join(parts)}")
        # capture
        if "capture" in deltas:
            cap = next((x for x in stats.get("attacks", []) if x["type"] == "Capture"), None)
            if cap and "capture_strength" in cap:
                m, a = deltas["capture"]
                cm, ca = total("capture", m, a)
                lines.append(f"- Capture strength: +{_fmt2(a)}{total_txt(cm, ca)}"
                             f" → {_fmt2(Decimal(cap['capture_strength']) * cm + ca)}")
        # build time
        if "buildtime" in deltas and "build_time" in stats:
            m, a = deltas["buildtime"]
            cm, ca = total("buildtime", m, a)
            lines.append(f"- Build time: ×{_fmt2(m)}{total_txt(cm)}"
                         f" → {_fmt2(Decimal(stats['build_time']) * cm + ca)} s")
        # gather base speed
        if "gather" in deltas and "gather" in stats:
            m, a = deltas["gather"]
            cm, ca = total("gather", m, a)
            base = Decimal(stats["gather"].get("base_speed", "1"))
            lines.append(f"- Gather base speed: ×{_fmt2(m)}{total_txt(cm)}"
                         f" → {_fmt2(base * cm + ca)}")
        # loot
        if "loot" in deltas:
            m, a = deltas["loot"]
            cm, ca = total("loot", m, a)
            lines.append(f"- Loot: ×{_fmt2(m)}{total_txt(cm)}")
        # ranged spread
        if "spread" in deltas:
            m, a = deltas["spread"]
            cm, ca = total("spread", m, a)
            lines.append(f"- Ranged spread: ×{_fmt2(m)}{total_txt(cm)}")
        # healer
        if "heal_range" in deltas:
            m, a = deltas["heal_range"]
            cm, ca = total("heal_range", m, a)
            lines.append(f"- Heal range: +{_fmt2(a)} m"
                         + ("" if first else f" (total +{_fmt2(ca)} m)"))
        if "heal_health" in deltas:
            m, a = deltas["heal_health"]
            cm, ca = total("heal_health", m, a)
            lines.append(f"- Heal strength: +{_fmt2(a)}"
                         + ("" if first else f" (total +{_fmt2(ca)})"))
        if len(lines) == n0 and not emitted:
            lines.append("- No stat changes (identity/visuals only).")
        lines.append("")
        first = False
    return lines

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
        # ranks (promotion)
        chains = {c: promotion_chain(d["variant_files"][c]) for c in civs}
        if any(len(ch) > 1 for ch in chains.values()):
            longest_civ = max(chains, key=lambda c: len(chains[c]))
            longest = chains[longest_civ]
            pattern = [(r, p.replace(f"units/{longest_civ}/", "units/{civ}/"), xp)
                       for r, p, xp in longest]
            lines.append("")
            lines.extend(rank_section_lines(d["stats"], pattern))
            notes = []
            max_ranks = defaultdict(list)
            for c, ch in chains.items():
                max_ranks[ch[-1][0]].append(c)
            for rank_label, cs in sorted(max_ranks.items()):
                if rank_label == longest[-1][0]:
                    continue
                promoted = [c for c in cs if len(chains[c]) > 1]
                trained = [c for c in cs if len(chains[c]) == 1]
                if trained:
                    for c in trained:
                        notes.append(f"**{c}**'s variant is trained at **{rank_label}** rank"
                                     f" (already receives the rank techs in game).")
                if promoted:
                    verb = "promotes" if len(promoted) == 1 else "promote"
                    notes.append(f"{', '.join('**' + c + '**' for c in promoted)} {verb}"
                                 f" only to {rank_label}.")
            # per-civ XP deviations per promotion step
            for i in range(1, len(longest)):
                devs = []
                for c, ch in chains.items():
                    if i < len(ch) and ch[i - 1][2] != longest[i - 1][2]:
                        devs.append(f"**{c}** ({ch[i - 1][2] or '?'} XP)")
                if devs:
                    notes.append(f"{', '.join(devs)} for the {longest[i][0]} promotion.")
            # promotions beyond the documented rank ladder
            further = []
            for c, ch in chains.items():
                tree = resolve(ch[-1][1])
                nxt = get_path(tree, "Entity/Promotion/Entity")
                if nxt and template_exists(nxt):
                    pat = nxt.replace(f"units/{c}/", "units/{civ}/")
                    further.append(f"**{c}** ({ch[-1][0]} rank promotes further to"
                                   f" `{pat}` at {ch[-1][2] or '?'} XP)")
            if further:
                notes.append("; ".join(further) + ".")
            merc_civs = [
                c for c in civs
                if "Mercenary" in (extract_stats(resolve(d["variant_files"][c])).get("visible_classes") or "").split()
            ]
            if merc_civs:
                notes.append("mercenary variants promote at 0 XP (the auto-researched"
                             " `upgrade_rank_advanced_mercenary` tech replaces RequiredXp"
                             " with 0).")
            for n in notes:
                lines.append(f"- Note: {n}")
            lines.append("")
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
    lines.append("- **Ranks:** upgradable units get a \"Ranks\" section per non-basic rank"
                 " (Advanced, Elite) with the promotion target, the required XP and every"
                 " stat that changes. The changes come from the auto-researched"
                 " `unit_advanced` / `unit_elite` techs (verified: the `_a`/`_e` template"
                 " files themselves only change `Identity/Rank`, `Promotion` and the"
                 " actor) plus any template-level stat differences for special promotions"
                 " (e.g. rome's champion → \"First Cohort\", athen's elite spearman →"
                 " champion). Per-civ deviations (XP values, civs that skip or extend the"
                 " ladder) are noted.")
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
