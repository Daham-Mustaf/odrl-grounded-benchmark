"""
tree_expand.py
==============
Turns a problem carrying a constraint tree into the shape the writers expect.

    from tree_expand import expand_tree
    problems = [expand_tree(p) for p in PROBLEMS]

Why this exists
---------------
Most problems in the suite carry their witness condition as a hand-written
formula, which is readable and reviewable: a reader of the problem data sees
exactly what will be asserted.  That stops working once constraints are
composed under or and xone.  A xone of two alternatives expands to a
disjunction of two literal sets, each carrying the negation of the other, and
the witness condition of the whole is the disjunction of theirs.  Writing
that out by hand would be transcribing the compiler's output, and any
transcription error would show up as a wrong verdict that looks like a
finding.

So a composed problem carries the tree, and this module derives everything
the writers need from it.  The compiler does the expansion; nothing here
duplicates it.

What is derived and what is not
--------------------------------
Derived: the constants the tree names, the two witness formulas, and the SMT
declarations.  These follow from the tree with no choices to make.

Not derived: the SMT resource and background blocks.  The TPTP query includes
the whole axiom file, so it has the resource and the background theory in
full; the SMT query is assembled from the problem data, and which assertions
it needs depends on which ones bear on the verdict.  That is a judgement, and
a problem composed under xone needs it as much as any other: the point of
running both provers is that they see the same theory by two routes, and
deriving one route from the other would defeat it.  A problem that supplies
neither block gets empty ones, and the two provers will then disagree, which
is the intended signal.

The constant order
------------------
Constants are collected in the order the tree names them, not sorted.  The
witness condition ranges over them in that order, so a stable order keeps the
generated formula stable across runs, and a regenerated problem diffs
cleanly.
"""
import re

from compile import Constraint, Or, Xone, compile_operand


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


def smt_declarations(constants) -> str:
    return "\n".join(
        ["(declare-sort Concept 0)"]
        + [f"(declare-fun {c} () Concept)" for c in constants]
        + ["(declare-fun kge_leq (Concept Concept) Bool)"])


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
    """Fill the witness and declaration fields of a tree-carrying problem.

    A problem without a tree is returned unchanged, so the two kinds sit in
    one list and the generator does not branch.
    """
    if "tree" not in p:
        return p
    # Grounding, recorded rather than computed.  The binding's rule maps a
    # policy value to a concept of the bound resource; that map lives in
    # the manifest because grounding procedures are in design/grounding.py
    # and are not wired into this pipeline yet.  A value with no entry is
    # assumed already to be a concept, which is true of every problem whose
    # policies name concepts directly.
    #
    # This runs before the constants are collected, so no policy value can
    # reach the signature.  KGC373 is why it exists: "en-US" became
    # (declare-fun en-US () Concept), a fresh constant satisfying anything,
    # and both provers were asked a question about nothing.
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
    q = dict(p)
    q.setdefault("fof_decls", "")
    q["fof_witness"] = w["fof"]
    q.setdefault("smt2_logic", "UF")
    q["smt2_decls"] = smt_declarations(constants)
    q.setdefault("smt2_resource", "")
    q.setdefault("smt2_background", "")
    q["smt2_witness"] = w["smt"]
    return q