"""
tree_expand.py
==============
Turns a problem carrying a constraint tree into the shape the writers expect.

    from tree_expand import expand_tree
    problems = [expand_tree(p) for p in PROBLEMS]
"""
import re
from collections import deque
from pathlib import Path

from compile import Constraint, Or, Xone, compile_operand

_ASSERTION = re.compile(
    r"fof\(\s*((?:res|bt|bg)_[a-z0-9_]+)\s*,\s*axiom,\s*"
    r"(?:kge_leq\(\s*([a-z0-9_]+)\s*,\s*([a-z0-9_]+)\s*\)"
    r"|kge_concept\(\s*([a-z0-9_]+)\s*\)"
    r"|([a-z0-9_]+)\s*!=\s*([a-z0-9_]+))\s*\)\s*\.",
    re.S)


def _parse_assertions(text):
    """Yield (label, kind, args) for every matching assertion, file order.

    kind is one of leq, concept, dist.  Anything the pattern does not
    match (quantified disjointness, definitions) is left to the axiom
    module includes on the TPTP side and to the writer's axiom template on
    the SMT side; only ground resource and background facts are inlined.
    """
    for m in _ASSERTION.finditer(text):
        label = m.group(1)
        if m.group(2):
            yield label, "leq", (m.group(2), m.group(3))
        elif m.group(4):
            yield label, "concept", (m.group(4),)
        else:
            yield label, "dist", (m.group(5), m.group(6))


def _betweenness(constants, leq_edges):
    """Constants plus every concept on a directed path between two of them.

    Edges are (below, above).  A concept m is kept when it is above some
    constant a and below some constant b: the chain a <= m <= b is then a
    derivation the query can make, and dropping m drops it.
    """
    up: dict = {}
    down: dict = {}
    for a, b in leq_edges:
        up.setdefault(a, set()).add(b)
        down.setdefault(b, set()).add(a)

    def reach(start, adj):
        seen = {start}
        queue = deque([start])
        while queue:
            for nxt in adj.get(queue.popleft(), ()):
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
        return seen

    ups = {c: reach(c, up) for c in constants}
    downs = {c: reach(c, down) for c in constants}
    keep = set(constants)
    for a in constants:
        for b in constants:
            if a is not b:
                keep |= ups[a] & downs[b]
    return keep


def assertions_for(constants, includes,
                   axioms_dir: Path = Path("problems/axioms")):
    """The included assertions the SMT side needs, and the extra constants.

    Returns (resource_block, background_block, extras): the two blocks as
    strings of named asserts, either possibly empty, and the closure
    concepts that appear in them beyond the given constants, which the
    caller must declare.

    Duplicate premise names across the included files abort: :named must
    be unique in one SMT query, and two files defining one name is a build
    bug the TPTP side would also mislabel.
    """
    entries = []
    seen: dict = {}
    for name in includes:
        path = axioms_dir / name
        if not path.exists() or name.startswith("KGE"):
            continue
        for label, kind, args in _parse_assertions(
                path.read_text(encoding="utf-8")):
            if label in seen:
                if seen[label] != (kind, args):
                    raise ValueError(
                        f"premise name {label} defined twice with different "
                        f"content across {includes}")
                continue
            seen[label] = (kind, args)
            entries.append((label, kind, args))

    leq_edges = [args for _, kind, args in entries if kind == "leq"]
    keep = _betweenness(list(constants), leq_edges)

    res, bg, extras = [], [], []
    for label, kind, args in entries:
        if any(a not in keep for a in args):
            continue
        if kind == "leq":
            body = f"(kge_leq {args[0]} {args[1]})"
        elif kind == "concept":
            body = f"(kge_concept {args[0]})"
        else:
            body = f"(not (= {args[0]} {args[1]}))"
        line = f"(assert (! {body} :named {label}))"
        (res if label.startswith("res_") else bg).append(line)
        for a in args:
            if a not in constants and a not in extras:
                extras.append(a)
    return "\n".join(res), "\n".join(bg), sorted(extras)


def constants_of_tree(items) -> list:
    """The concepts the tree names, in the order it names them."""
    seen = []
    for item in items:
        alts = item.alts if isinstance(item, (Or, Xone)) else (item,)
        for c in alts:
            if not isinstance(c, Constraint):
                raise TypeError(
                    f"a Logical Constraint's operands are atomic constraints; "
                    f"found {type(c).__name__}")
            for v in c.values:
                if v not in seen:
                    seen.append(v)
    return seen


def smt_declarations(constants, with_concept: bool = False) -> str:
    lines = (["(declare-sort Concept 0)"]
             + [f"(declare-fun {c} () Concept)" for c in constants]
             + ["(declare-fun kge_leq (Concept Concept) Bool)"])
    if with_concept:
        lines.append("(declare-fun kge_concept (Concept) Bool)")
    return "\n".join(lines)


def _map_constraint(c: Constraint, g: dict) -> Constraint:
    return Constraint(c.operator, tuple(g.get(v, v) for v in c.values),
                      c.side)


def _map_item(item, g: dict):
    """A tree item with its policy values replaced by concepts.

    The shape is preserved, so the reduction to disjuncts is unchanged by
    grounding and a certificate can still point back at a constraint of
    the original.
    """
    if isinstance(item, Constraint):
        return _map_constraint(item, g)
    alts = tuple(_map_constraint(c, g) for c in item.alts)
    return Or(alts) if isinstance(item, Or) else Xone(alts)


def expand_tree(p: dict) -> dict:
    """Fill the witness, declaration, and theory fields of a tree problem.

    A problem without a tree is returned unchanged, so the two kinds sit in
    one list and the generator does not branch.
    """
    if "tree" not in p:
        return p
    # Ungrounded problems build no queries (requirement D16); the raw
    # value stays in the tree as documentation and the writers emit the
    # case file only.  The marker is checked against the tree so a stale
    # "ungrounded" field on a fixed problem is an error, not a silent skip.
    ungrounded = p.get("ungrounded")
    if ungrounded:
        values = [v for item in p["tree"]
                  for c in (item.alts if hasattr(item, "alts") else (item,))
                  for v in c.values]
        if ungrounded not in values:
            raise ValueError(
                f"{p['id']}: marked ungrounded on {ungrounded!r}, but no "
                f"constraint carries that value; remove the marker or fix "
                f"the tree")
        return p
    grounding = p.get("grounding")
    if grounding:
        p = dict(p)
        p["tree"] = [_map_item(item, grounding) for item in p["tree"]]
    constants = constants_of_tree(p["tree"])
    bad = [c for c in constants
           if not re.fullmatch(r"[a-z][a-zA-Z0-9_]*", c)]
    if bad:
        raise ValueError(
            f"{p['id']}: {bad} are not well-formed constants. A policy "
            f"value reached the signature without being grounded; either "
            f"add it to the problem's grounding map, or mark the problem "
            f"ungrounded if the binding's rule does not resolve it.")
    w = compile_operand(p["tree"], constants, p["sort"])
    derived_res, derived_bg, extras = assertions_for(
        constants, p.get("includes", []))
    q = dict(p)
    q.setdefault("fof_decls", "")
    q["fof_witness"] = w["fof"]
    q.setdefault("smt2_logic", "UF")
    # An explicit field wins; the derivation fills only what is absent.
    q.setdefault("smt2_resource", derived_res)
    q.setdefault("smt2_background", derived_bg)
    used_derived = (q["smt2_resource"] == derived_res
                    or q["smt2_background"] == derived_bg)
    extra = [c for c in p.get("extra_constants", [])
             if c not in constants]
    decl_constants = constants + (extras if used_derived else []) + extra
    with_concept = used_derived and "(kge_concept " in (
        q["smt2_resource"] + q["smt2_background"])
    q["smt2_decls"] = smt_declarations(decl_constants, with_concept)
    q["smt2_witness"] = w["smt"]
    return q


def expect_rejection(p: dict) -> dict:
    """Assert that expanding this problem fails in the signature.

    Expected-error problems (requirement G29) are rejections the compiler
    must make; a rejection that stops happening is a regression in the
    signature, so this raises when expand_tree succeeds.  The exception
    text is recorded on the problem for the writers to quote.
    """
    try:
        expand_tree(p)
    except (ValueError, TypeError) as e:
        q = dict(p)
        q["rejection"] = str(e)
        return q
    raise AssertionError(
        f"{p['id']}: expected the signature to reject this tree, and it "
        f"compiled; the well-sortedness check has regressed")