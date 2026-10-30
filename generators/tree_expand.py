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

import declarations
import vocabulary
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


def assertions_for(kept, includes, keep_all=False,
                   axioms_dir: Path = Path("problems/axioms")):
    """The statements of the included resource files the SMT side carries.

    Returns (block, constants): the named asserts, in file order, and the
    constants they name, which the caller declares.  The TPTP side includes
    the files whole; the SMT side carries every statement among the kept
    concepts, the candidates the witness uses together with every concept on
    a path of statements between two of them, under the same labels.

    That is exact when the binding's declarations are distinctness only.  A
    concept outside the kept set can be a fresh element of its own, placed
    by its statements, and the order among the kept concepts does not change:
    a published path through it that joined two kept concepts would make it
    lie between them, and it would be kept.  The distinctness the query
    carries is over the kept concepts too (declarations.statements), and a
    fresh element is distinct from every other.  So a model of the kept
    statements extends to one of all of them, and the query's status is the
    same.

    It is not exact where a declaration says that nothing lies below both of
    two concepts: a concept below one of them, outside the kept set, can make
    the other its equal impossible.  A binding with a disjointness among its
    declarations (consent, GeoNames, both small) keeps every statement:
    keep_all.

    A declaration (bg_) in an included file is refused: a query's
    declarations come from the set the problem names.  Duplicate premise
    names across the included files abort: :named must be unique in one SMT
    query, and two files defining one name is a build bug the TPTP side
    would also mislabel.
    """
    kept = set(kept)
    lines, constants, seen = [], [], {}
    for name in includes:
        path = axioms_dir / name
        if not path.exists() or name.startswith("KGE"):
            continue
        for label, kind, args in _parse_assertions(
                path.read_text(encoding="utf-8")):
            if label.startswith("bg_"):
                raise ValueError(
                    f"{name}: {label} is a declaration in an included file; "
                    f"declarations come from the set the problem names")
            if label in seen:
                if seen[label] != (kind, args):
                    raise ValueError(
                        f"premise name {label} defined twice with different "
                        f"content across {includes}")
                continue
            seen[label] = (kind, args)
            if not keep_all and any(a not in kept for a in args):
                continue
            if kind == "leq":
                body = f"(kge_leq {args[0]} {args[1]})"
            elif kind == "concept":
                body = f"(kge_concept {args[0]})"
            else:
                body = f"(not (= {args[0]} {args[1]}))"
            lines.append(f"(assert (! {body} :named {label}))")
            constants.extend(args)
    return "\n".join(lines), list(dict.fromkeys(constants))


def included_edges(includes, axioms_dir: Path = Path("problems/axioms")):
    """The order statements of the included files, as (below, above)."""
    edges = []
    for name in includes:
        path = axioms_dir / name
        if not path.exists() or name.startswith("KGE"):
            continue
        edges += [args for _, kind, args in
                  _parse_assertions(path.read_text(encoding="utf-8"))
                  if kind == "leq"]
    return edges


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
    """fof_decls and smt2_background hold no statements a problem writes.

    The declarations of a query are the set the problem names
    (background_theory), instantiated by declarations.statements over every
    pair of the witness's candidates, and a resource statement comes from
    the axiom file the case includes.  A problem may put comments in
    fof_decls; a statement there, or in smt2_background, is refused.
    """
    pid = p.get("id", "?")
    fof = "\n".join(l for l in p.get("fof_decls", "").split("\n")
                    if not l.lstrip().startswith("%"))
    smt = "\n".join(l for l in p.get("smt2_background", "").split("\n")
                    if not l.lstrip().startswith(";"))
    if re.search(r"\bfof\s*\(", fof) or re.search(r"\(assert\b", smt):
        raise ValueError(
            f"{pid}: fof_decls or smt2_background carries a statement. The "
            f"declarations come from the set background_theory names, and "
            f"the resource statements from the included axiom files.")


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
    # The value of a use can be any concept of the operand's vocabulary
    # (Definition Witness), so the witness ranges over every concept of the
    # vocabulary the binding reads, for every vocabulary alike.  A caller may
    # pass fewer candidates: a use found among fewer is a use among all,
    # which is what check_policies relies on for a policy alone.  The real
    # queries pass none.
    if p.get("candidates"):
        candidates = list(constants) + [c for c in p["candidates"]
                                        if c not in constants]
    elif p.get("resource"):
        candidates = vocabulary.candidates(p["resource"], constants)
    else:
        raise ValueError(f"{p['id']}: no resource, so no concepts for the "
                         f"witness to range over")
    w = compile_operand(p["tree"], candidates, p["sort"])
    # The kept concepts: the candidates the witness uses and every concept on
    # a path of published statements between two of them.  The SMT side
    # carries the statements among them (assertions_for, which says why that
    # is exact), and the declared distinctness among them, in both encodings:
    # cc <= cb <= ca published and cb declared distinct from cc keeps cc from
    # being ca, though the witness names only ca and cc.  A disjointness can
    # matter through any connected concept, ca <= cc published and ca
    # disjoint from cb keeping cb from being cc, so it is carried for every
    # pair connected to the witness's candidates, and a binding with a
    # disjointness among its declarations keeps every statement.
    edges = included_edges(p.get("includes", []))
    kept = vocabulary.between(w["constants"], edges)
    reach = vocabulary.connected(w["constants"], edges)
    keep_all = declarations.has_disjointness(p.get("resource"))
    resource, named_by_resource = assertions_for(
        kept, p.get("includes", []), keep_all)
    decl = declarations.set_for(p.get("background_theory"))
    fof_d, smt_d, n = declarations.statements(
        decl, [c for c in candidates if c in kept],
        [c for c in candidates if c in reach])
    if n:
        fof_d = (f"% Declarations: {decl.iri}, over every pair of the\n"
                 f"% witness's candidates it states ({n}).\n\n" + fof_d)
        smt_d = f"; Declarations: {decl.iri}\n" + smt_d
    q = dict(p)
    head = p.get("fof_decls", "").rstrip()
    q["fof_decls"] = "\n\n".join(x for x in (head, fof_d) if x) + "\n"
    q["fof_witness"] = w["fof"]
    q.setdefault("smt2_logic", "UF")
    q["smt2_resource"] = resource
    q["smt2_background"] = smt_d
    declared = set(w["constants"]) | kept | set(named_by_resource) | \
        (reach if decl is not None and decl.disjoint else set())
    q["smt2_decls"] = smt_declarations(
        [c for c in candidates if c in declared]
        + [c for c in named_by_resource if c not in candidates],
        "(kge_concept " in resource)
    q["smt2_witness"] = w["smt"]
    q["named_constants"] = constants
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