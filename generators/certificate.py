"""
certificate.py
==============
Evidence for a verdict, checkable without trusting what produced it.

A decision procedure returns a verdict and, on its own, the verdict must be
taken on the procedure's word.  A certificate is what a party against whom
the verdict goes can examine instead: for an unsatisfiable query, the
premises a refutation used; for a satisfiable one, a structure satisfying
it; for an ungrounded value, the value.

This module has its own evaluator and does not import the encoders.  That
is the point of it.  A checker sharing the compiler's code would agree with
the compiler about anything the compiler got wrong, and the one bug that
mattered this year was exactly of that kind: a formula the encoder built
incorrectly and two provers then disagreed about.

What is checked, and what is only recorded
------------------------------------------
A model certificate is checked: the structure is finite and explicit, and
every formula of the query is evaluated in it.  A refutation certificate is
checked only for premise legality, not for derivation: a prover's proof
uses unification and superposition, and the propositional replay the
proposition asks for is a normalisation step that does not exist here.

So the names are ``attributed`` rather than ``verified``, and the report
says which.  Attribution is still the half a party needs, since they
withdraw an assertion rather than an inference step.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from query import And, Eq, Formula, Leq, Not, Or_, Query, QueryPair, Top
from runner import RunResult
from vocabulary import (PremiseClass, RunStatus, UnknownReason, Verdict,
                        derive_verdict)


# --- a structure, and evaluation in it ---------------------------------

@dataclass(frozen=True)
class Structure:
    """A finite interpretation of the query's constants.

    ``classes`` sends each constant to an element of the domain, so two
    constants naming one element is how a structure identifies concepts.
    ``leq`` holds the pairs of elements the order relates.

    Explicit and small: a model certificate has at most as many elements as
    the query has constants, and a reader can check it by hand.
    """

    classes: dict[str, int]
    leq: frozenset[tuple[int, int]]

    def eq(self, a: str, b: str) -> bool:
        return self.classes[a] == self.classes[b]

    def below(self, a: str, b: str) -> bool:
        return (self.classes[a], self.classes[b]) in self.leq

    def holds(self, f: Formula) -> bool:
        if isinstance(f, Top):
            return True
        if isinstance(f, Eq):
            return self.eq(f.lhs, f.rhs)
        if isinstance(f, Leq):
            return self.below(f.lhs, f.rhs)
        if isinstance(f, Not):
            return not self.holds(f.inner)
        if isinstance(f, And):
            return all(self.holds(p) for p in f.parts)
        if isinstance(f, Or_):
            return any(self.holds(p) for p in f.parts)
        raise TypeError(f"not a formula: {f!r}")

    def order_axioms_hold(self) -> str | None:
        """Whether the order is reflexive, antisymmetric and transitive.

        A structure violating them is not admissible, so a model
        certificate over one proves nothing.  Returned as a message rather
        than a boolean so a report can say which axiom failed.
        """
        elems = set(self.classes.values())
        for x in elems:
            if (x, x) not in self.leq:
                return "not reflexive"
        for x, y in self.leq:
            if (y, x) in self.leq and x != y:
                return "not antisymmetric"
        for x, y in self.leq:
            for y2, z in self.leq:
                if y == y2 and (x, z) not in self.leq:
                    return "not transitive"
        return None


# --- the certificates --------------------------------------------------

@dataclass(frozen=True)
class Refutation:
    """The premises a refutation used, for an unsatisfiable query.

    ``attributed`` is what the prover reported; nothing here reconstructs
    the derivation.  ``withdrawable`` is the subset a party may retract,
    and retracting any of them returns the verdict to Unknown.
    """

    problem_id: str
    query_kind: str
    attributed: tuple[str, ...]
    prover: str

    def by_class(self) -> dict[PremiseClass | None, list[str]]:
        out: dict[PremiseClass | None, list[str]] = {}
        for n in self.attributed:
            out.setdefault(PremiseClass.from_name(n), []).append(n)
        return out

    def withdrawable(self) -> list[str]:
        return [n for n in self.attributed
                if (c := PremiseClass.from_name(n)) and c.is_withdrawable]


@dataclass(frozen=True)
class Models:
    """Two structures, for an Unknown that is epistemic.

    They satisfy the two queries respectively, so they differ on the
    witness condition, and what they disagree about is the question the
    resource leaves open.
    """

    problem_id: str
    inc_model: Structure
    comp_model: Structure

    def differ_on(self) -> list[str]:
        """The constants the two structures interpret differently.

        Read as: whether these name one concept is what nothing published
        or declared decides.
        """
        keys = sorted(set(self.inc_model.classes) | set(self.comp_model.classes))
        out = []
        for a in keys:
            for b in keys:
                if a >= b:
                    continue
                if self.inc_model.eq(a, b) != self.comp_model.eq(a, b):
                    out.append(f"{a} = {b}")
        return out


@dataclass(frozen=True)
class UngroundedCertificate:
    """The values that named no concept."""

    problem_id: str
    procedure: str
    values: tuple[str, ...]


Certificate = Refutation | Models | UngroundedCertificate


# --- checking ----------------------------------------------------------

@dataclass
class CheckResult:
    """What the checker found.

    ``ok`` is the conjunction of the complaints being empty.  A certificate
    that cannot be checked at all, as against one that fails, is reported
    as a complaint too, since silence would read as approval.
    """

    problem_id: str
    ok: bool
    complaints: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        head = "ok  " if self.ok else "FAIL"
        body = "; ".join(self.complaints or self.notes)
        return f"{head} {self.problem_id}  {body}"


def check_refutation(cert: Refutation, pair: QueryPair) -> CheckResult:
    """Whether every cited premise is one the query permits.

    The query's own formulas, and ground instances of the axioms it
    declares.  A name outside both is either a premise from somewhere else
    or a name the checker cannot classify, and both are defects.
    """
    q = pair.inc if cert.query_kind == "inc" else pair.comp
    r = CheckResult(cert.problem_id, True)

    if not cert.attributed:
        r.notes.append("no premises reported; the contradiction lies in the "
                       "target alone, which is possible and unverified here")

    for name in cert.attributed:
        if q.legal_premise(name):
            continue
        cls = PremiseClass.from_name(name)
        if cls is None:
            r.complaints.append(
                f"{name}: no provenance class; a premise whose origin "
                f"cannot be determined is a defect, not a guess")
        else:
            r.complaints.append(
                f"{name}: {cls} is not a premise of this query")

    used = {PremiseClass.from_name(n) for n in cert.attributed}
    if PremiseClass.AX_EQUALITY in used:
        r.notes.append(
            "an equality axiom instance was used; the premise list of "
            "Proposition (Certificates) does not yet admit these")

    r.ok = not r.complaints
    return r


def check_models(cert: Models, pair: QueryPair) -> CheckResult:
    """Whether each structure satisfies the query it is offered for.

    Every formula, not a sample: the premises and the target.  A structure
    that satisfies the premises but not the target is not a model of the
    query, and one that violates an order axiom is not admissible at all.
    """
    r = CheckResult(cert.problem_id, True)

    for kind, model, q in (("inc", cert.inc_model, pair.inc),
                           ("comp", cert.comp_model, pair.comp)):
        bad = model.order_axioms_hold()
        if bad:
            r.complaints.append(f"{kind} model is {bad}, so not admissible")
            continue
        for p in q.premises:
            f = Leq(p.lhs, p.rhs) if p.kind is PremiseClass.RESOURCE else \
                Not(Eq(p.lhs, p.rhs)) if p.kind is PremiseClass.BG_DISTINCTNESS \
                else None
            if f is None:
                r.notes.append(f"{p.name}: quantified, not evaluated here")
                continue
            if not model.holds(f):
                r.complaints.append(
                    f"{kind} model does not satisfy {p.name}")
        try:
            if not model.holds(q.target):
                r.complaints.append(
                    f"{kind} model does not satisfy the target, so it is "
                    f"not a model of this query")
        except KeyError as e:
            r.complaints.append(
                f"{kind} model does not interpret {e}, so the target "
                f"cannot be evaluated in it")

    if not r.complaints and not cert.differ_on():
        r.complaints.append(
            "the two models agree on every constant; an Unknown needs two "
            "structures that disagree, or the verdict is not Unknown")

    r.ok = not r.complaints
    return r


def check(cert: Certificate, pair: QueryPair | None) -> CheckResult:
    if isinstance(cert, UngroundedCertificate):
        return CheckResult(
            cert.problem_id, True,
            notes=[f"{len(cert.values)} value(s) unresolved by "
                   f"{cert.procedure}; re-check by applying it"])
    if pair is None:
        return CheckResult(cert.problem_id, False,
                           ["no query pair to check against"])
    if isinstance(cert, Refutation):
        return check_refutation(cert, pair)
    return check_models(cert, pair)


# --- from runs ---------------------------------------------------------

@dataclass(frozen=True)
class VerdictResult:
    """The verdict, its reason, and the certificate, from a pair of runs.

    Holds the derived verdict only.  An expectation lives in the manifest
    and the two meet in the report, in separate columns, so that neither
    can be filled from the other.
    """

    problem_id: str
    verdict: Verdict | None
    reason: UnknownReason | None
    certificate: Certificate | None
    inc: RunResult
    comp: RunResult

    @property
    def determined(self) -> bool:
        return self.verdict is not None


def from_runs(inc: RunResult, comp: RunResult) -> VerdictResult:
    """The verdict a pair of runs gives, with the refutation if there is one.

    Model certificates are not built here: a structure has to be read out
    of a solver's model, which is that adapter's business, and a run that
    was satisfiable carries the text rather than the structure.
    """
    verdict, reason = derive_verdict(inc.status, comp.status)
    cert: Certificate | None = None
    if verdict is Verdict.INCOMPATIBLE:
        cert = Refutation(inc.problem_id, "inc", inc.premises,
                          inc.solver.name)
    elif verdict is Verdict.COMPATIBLE:
        cert = Refutation(comp.problem_id, "comp", comp.premises,
                          comp.solver.name)
    return VerdictResult(inc.problem_id, verdict, reason, cert, inc, comp)