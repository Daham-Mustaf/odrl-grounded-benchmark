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
    r"fof\(\s*([a-z][a-z0-9_]*)\s*,\s*axiom,\s*"
    r"(?:kge_leq\(\s*([a-z0-9_]+)\s*,\s*([a-z0-9_]+)\s*\)"
    r"|kge_concept\(\s*([a-z0-9_]+)\s*\)"
    r"|([a-z0-9_]+)\s*!=\s*([a-z0-9_]+))\s*\)\s*\.",
    re.S)


def _parse_assertions(text):
    """Yield (label, kind, args) for every matching statement, file order.

    Any label is accepted: a resource names its statements as it likes
    (res_ for most, gn_ for GeoNames).  Whether a statement is the
    parties' or the authority's is decided by the label alone: bg_ is a
    declaration, every other label is a resource statement.

    kind is one of leq, concept, dist.  Anything the pattern does not
    match (quantified disjointness, definitions) is left to the axiom
    module includes on the TPTP side and to the writer's axiom template on
    the SMT side; only ground resource statements and declarations are inlined.
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
    """The included statements the SMT side needs, and the extra constants.

    Returns (resource_block, declarations_block, extras): the two blocks as
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
        (bg if label.startswith("bg_") else res).append(line)
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


# The formula fields a case used to carry by hand.  Every one of them is
# derived from the tree, so an entry that still writes one is refused: two
# sources for one query is how the TPTP and SMT-LIB sides drifted apart.
# Declarations are the exception that stays: fof_decls and smt2_background.
LEGACY_FIELDS = ("fof_witness", "smt2_witness", "smt2_asserts",
                 "smt2_decls", "smt2_resource")


def refuse_hand_written(p: dict) -> None:
    pid = p.get("id", "?")
    found = [k for k in LEGACY_FIELDS if k in p and not p.get("_derived")]
    if found:
        raise ValueError(
            f"{pid}: hand-written {', '.join(found)}. A case is a tree; the "
            f"compiler derives the witness, the declarations and the "
            f"resource. Give {pid} a tree and remove the field(s).")
    if "tree" not in p and not p.get("ungrounded"):
        raise ValueError(f"{pid}: no tree. A verdict case is a constraint "
                         f"tree, or it is marked ungrounded.")
    refuse_non_declarations(p)


def refuse_non_declarations(p: dict) -> None:
    """fof_decls and smt2_background hold declarations, and only those.

    A declaration is labelled bg_, on both sides, so that a proof and an
    unsat core cite one statement.  A resource statement comes from the
    axiom file the case includes, and the derivation writes it into the
    SMT-LIB file under the same label.  A statement written here under any
    other label, or an SMT-LIB statement with no label at all, is refused.
    """
    pid = p.get("id", "?")
    fof = "\n".join(l for l in p.get("fof_decls", "").split("\n")
                    if not l.lstrip().startswith("%"))
    smt = "\n".join(l for l in p.get("smt2_background", "").split("\n")
                    if not l.lstrip().startswith(";"))
    labels = (re.findall(r"fof\(\s*([A-Za-z0-9_]+)\s*,", fof)
              + re.findall(r":named\s+([A-Za-z0-9_]+)", smt))
    bad = [l for l in labels if not l.startswith("bg_")]
    if bad:
        raise ValueError(
            f"{pid}: {', '.join(bad)} in fof_decls or smt2_background does "
            f"not start with bg_. Those fields hold declarations; a resource "
            f"statement comes from the included axiom file.")
    unnamed = len(re.findall(r"\(assert\b", smt)) - len(re.findall(r":named\b", smt))
    if unnamed > 0:
        raise ValueError(
            f"{pid}: smt2_background has {unnamed} statement(s) with no "
            f":named label. Give each the bg_ label the TPTP side uses.")


def expand_tree(p: dict) -> dict:
    """Fill the witness, declaration, and declarations fields of a tree problem.

    An entry carrying a hand-written formula, or no tree, is refused with its
    case ID.  An entry marked ungrounded builds no queries and is returned
    as it is.
    """
    refuse_hand_written(p)
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
    # A declaration may name a concept neither constraint mentions:
    # the consent disjointness ranges over both branches while the
    # constraints name one. Those concepts go into the statement filter as
    # well as the declarations, or an edge to one of them is dropped as
    # leading outside the problem.
    extra = [c for c in p.get("extra_constants", []) if c not in constants]
    derived_res, derived_bg, extras = assertions_for(
        constants + extra, p.get("includes", []))
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
    decl_constants = constants + extra + (extras if used_derived else [])
    with_concept = used_derived and "(kge_concept " in (
        q["smt2_resource"] + q["smt2_background"])
    q["smt2_decls"] = smt_declarations(decl_constants, with_concept)
    q["smt2_witness"] = w["smt"]
    q["_derived"] = True
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