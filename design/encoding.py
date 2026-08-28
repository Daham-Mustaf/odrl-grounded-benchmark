"""
encoding.py
===========
One query, written down twice.

TPTP and SMT-LIB are serialisations.  They add nothing and choose nothing:
the premises, their names, the target and the concepts all arrive from the
query, and each writer's only job is to render the same objects in its own
syntax.  Two encodings that disagree about a verdict are therefore a bug in
a writer, and there is one place to look.


Bracketing
----------
TPTP's grammar composes a disjunction out of unit formulas, and a
conjunction is not one, so ``a & b | c`` is not derivable: it is ill formed
rather than badly bracketed, and a lenient parser accepting it is guessing.
Two provers once guessed differently on a formula this module's predecessor
emitted, and the suite reported a disagreement that was neither prover's
doing.

So every compound is parenthesised by the function that builds it, and
nothing relies on precedence.  SMT-LIB is prefix and gets this free.

Order axioms
------------
Emitted whole, as quantified schemas, rather than instantiated at the
concepts a problem happens to need.  Hand-picked instances would make the
two encodings different theories, so agreement between them would stop
meaning anything; and choosing exactly the instances a proof needs is
indistinguishable, from outside, from fitting the encoding to the answer.

They are declared only when the query mentions the order.  A nominal
operand has no order to axiomatise and declaring one would introduce a
symbol nothing else uses.
"""

from __future__ import annotations

from dataclasses import dataclass

from fixture import Premise
from query import And, Eq, Formula, Leq, Not, Or_, Query, QueryPair, Top
from vocabulary import PremiseClass

# The three order axioms, one text per language, identical in content.  The
# names match across the two, so a proof and an unsat core classify through
# one provenance map.
AX_NAMES = ["ax_order_reflexive", "ax_order_antisymmetric",
            "ax_order_transitive"]

_TPTP_AXIOMS = """\
fof(ax_order_reflexive, axiom, ! [X] : leq(X, X)).

fof(ax_order_antisymmetric, axiom,
    ! [X, Y] : ( ( leq(X, Y) & leq(Y, X) ) => X = Y )).

fof(ax_order_transitive, axiom,
    ! [X, Y, Z] : ( ( leq(X, Y) & leq(Y, Z) ) => leq(X, Z) )).
"""

_SMT_AXIOMS = """\
(assert (! (forall ((x Concept)) (leq x x)) :named ax_order_reflexive))
(assert (! (forall ((x Concept) (y Concept))
    (=> (and (leq x y) (leq y x)) (= x y))) :named ax_order_antisymmetric))
(assert (! (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (leq x y) (leq y z)) (leq x z))) :named ax_order_transitive))
"""


def const(iri: str) -> str:
    """The constant a concept is written as.

    Derived from the IRI so that the same concept is the same constant in
    both languages and across problems.  Collisions are the fixture's to
    prevent by prefixing; it checks for them when it loads.
    """
    local = iri.rsplit("#", 1)[-1] if "#" in iri \
        else iri.rstrip("/").rsplit("/", 1)[-1]
    out: list[str] = []
    for ch in local:
        if ch.isupper() and out and out[-1] != "_":
            out.append("_")
        out.append(ch.lower() if ch.isalnum() else "_")
    return "c_" + "".join(out).strip("_").replace("__", "_")


# --- TPTP ---------------------------------------------------------------

def _tptp(f: Formula) -> str:
    """A formula as TPTP, every compound self-contained.

    A single operand comes back unwrapped: one term parses the same
    wherever it is placed, and the extra parentheses would be noise.
    """
    if isinstance(f, Top):
        return "$true"
    if isinstance(f, Eq):
        return f"{const(f.lhs)} = {const(f.rhs)}"
    if isinstance(f, Leq):
        return f"leq({const(f.lhs)}, {const(f.rhs)})"
    if isinstance(f, Not):
        return f"~ ( {_tptp(f.inner)} )"
    parts = [_tptp(p) for p in f.parts]
    if len(parts) == 1:
        return parts[0]
    sep = " & " if isinstance(f, And) else "\n    | "
    return "( " + sep.join(parts) + " )"


def _tptp_premise(p: Premise) -> str:
    if p.kind is PremiseClass.RESOURCE:
        body = f"leq({const(p.lhs)}, {const(p.rhs)})"
    elif p.kind is PremiseClass.BG_DISTINCTNESS:
        body = f"{const(p.lhs)} != {const(p.rhs)}"
    elif p.kind is PremiseClass.BG_DISJOINTNESS:
        body = (f"! [X] : ~ ( leq(X, {const(p.lhs)}) "
                f"& leq(X, {const(p.rhs)}) )")
    else:
        raise ValueError(f"{p.kind} is not a premise of a query")
    return f"fof({p.name}, axiom, {body})."


def to_tptp(q: Query) -> str:
    lines = [
        f"% {q.problem_id}, query {q.kind}.",
        f"% {'Unsatisfiable here gives Incompatible.' if q.kind == 'inc' else 'Unsatisfiable here gives Compatible.'}",
        "",
    ]
    if q.uses_order:
        lines += ["% Order axioms, quantified.", "", _TPTP_AXIOMS]
    if q.premises:
        lines.append("% Premises: resource assertions and declarations.")
        lines.append("")
        lines += [_tptp_premise(p) for p in q.premises]
        lines.append("")
    lines += [
        "% The witness condition"
        + (", negated." if q.kind == "comp" else "."),
        "",
        f"fof({q.target_name}, axiom,\n    {_tptp(q.target)}).",
        "",
    ]
    return "\n".join(lines)


# --- SMT-LIB ------------------------------------------------------------

def _smt(f: Formula) -> str:
    if isinstance(f, Top):
        return "true"
    if isinstance(f, Eq):
        return f"(= {const(f.lhs)} {const(f.rhs)})"
    if isinstance(f, Leq):
        return f"(leq {const(f.lhs)} {const(f.rhs)})"
    if isinstance(f, Not):
        return f"(not {_smt(f.inner)})"
    parts = [_smt(p) for p in f.parts]
    if len(parts) == 1:
        return parts[0]
    op = "and" if isinstance(f, And) else "or"
    return f"({op} " + " ".join(parts) + ")"


def _smt_premise(p: Premise) -> str:
    if p.kind is PremiseClass.RESOURCE:
        body = f"(leq {const(p.lhs)} {const(p.rhs)})"
    elif p.kind is PremiseClass.BG_DISTINCTNESS:
        body = f"(not (= {const(p.lhs)} {const(p.rhs)}))"
    elif p.kind is PremiseClass.BG_DISJOINTNESS:
        body = (f"(forall ((x Concept)) (not (and (leq x {const(p.lhs)}) "
                f"(leq x {const(p.rhs)}))))")
    else:
        raise ValueError(f"{p.kind} is not a premise of a query")
    return f"(assert (! {body} :named {p.name}))"


def to_smt(q: Query) -> str:
    lines = [
        f"; {q.problem_id}, query {q.kind}.",
        f"; {'unsat here gives Incompatible.' if q.kind == 'inc' else 'unsat here gives Compatible.'}",
        "",
        f"(set-logic {'UF' if q.uses_order else 'QF_UF'})",
        "(set-option :produce-unsat-cores true)",
        "(set-option :produce-models true)",
        "",
        "(declare-sort Concept 0)",
    ]
    if q.uses_order:
        lines.append("(declare-fun leq (Concept Concept) Bool)")
    lines += [f"(declare-const {const(c)} Concept)" for c in q.concepts]
    lines.append("")
    if q.uses_order:
        lines += ["; Order axioms, quantified.", _SMT_AXIOMS]
    if q.premises:
        lines.append("; Premises: resource assertions and declarations.")
        lines += [_smt_premise(p) for p in q.premises]
        lines.append("")
    target = _smt(q.target)
    lines += [
        "; The witness condition" + (", negated." if q.kind == "comp" else "."),
        f"(assert (! {target} :named {q.target_name}))",
        "",
        "(check-sat)",
        # One of the two applies; a solver prints an error for the other and
        # carries on, and the reader takes whichever arrived.
        "(get-unsat-core)",
        "(get-model)",
        "(exit)",
        "",
    ]
    return "\n".join(lines)


# --- the pair -----------------------------------------------------------

@dataclass(frozen=True)
class EncodingPair:
    """Both languages, both queries, four texts.

    Named by problem and query kind, so a file called ``KGC302.comp.p``
    says which question it asks without a reader consulting anything.
    """

    problem_id: str
    tptp_inc: str
    tptp_comp: str
    smt_inc: str
    smt_comp: str

    def files(self) -> dict[str, str]:
        return {
            f"{self.problem_id}.inc.p": self.tptp_inc,
            f"{self.problem_id}.comp.p": self.tptp_comp,
            f"{self.problem_id}.inc.smt2": self.smt_inc,
            f"{self.problem_id}.comp.smt2": self.smt_comp,
        }


def encode(pair: QueryPair) -> EncodingPair:
    """Both encodings of both queries, from one query pair.

    The premise names are checked to match across languages before the
    result is returned.  They cannot differ, since both writers read the
    same objects, and the check is here so that a future change which makes
    them differ fails at once rather than as a verdict.
    """
    enc = EncodingPair(
        pair.problem_id,
        to_tptp(pair.inc), to_tptp(pair.comp),
        to_smt(pair.inc), to_smt(pair.comp),
    )
    for kind, tptp, smt in (("inc", enc.tptp_inc, enc.smt_inc),
                            ("comp", enc.tptp_comp, enc.smt_comp)):
        expected = {p.name for p in pair.inc.premises} | {pair.inc.target_name}
        if pair.inc.uses_order:
            expected |= set(AX_NAMES)
        for name in expected:
            if name not in tptp or name not in smt:
                missing = "TPTP" if name not in tptp else "SMT-LIB"
                raise ValueError(
                    f"{pair.problem_id} {kind}: {name} is absent from the "
                    f"{missing} encoding; the two languages must carry the "
                    f"same assertions under the same names")
    return enc