"""
signature.py
============
Whether a constraint's operator applies to its operand at all.

This is the check that runs before any query is built, and it needs only
the constraints and the binding: not the resource, not the concepts, not
what the values turn out to name.  An operator that asks about parthood on
an operand whose resource publishes a taxonomy is not answerable wrongly,
it is not answerable, and saying so is cheaper and more informative than a
verdict.

Rejection is an outcome, not an error
-------------------------------------
A problem may exist in order to be rejected, and several do.  So the check
returns a result rather than raising, the result names which constraint
failed and why, and a problem whose expectation is a rejection passes when
the rejection fires and fails when it does not.
"""

from __future__ import annotations

from dataclasses import dataclass

from problem import Constraint, ConstraintTree, PolicyProblem, Sort, Xone

# Table (Signature) of the paper.  Identity is available at every sort;
# subsumption at tax alone; parthood at mer alone.  Nothing else varies.
ADMISSIBLE: dict[Sort, frozenset[str]] = {
    "nom": frozenset({"eq", "neq", "isAnyOf", "isAllOf", "isNoneOf"}),
    "tax": frozenset({"eq", "neq", "isAnyOf", "isAllOf", "isNoneOf", "isA"}),
    "mer": frozenset({"eq", "neq", "isAnyOf", "isAllOf", "isNoneOf",
                      "isPartOf", "hasPart"}),
}

# Operators the fragment knows at all.  An operator outside this set is not
# ill sorted, it is unrecognised, and the two are reported differently: one
# is a policy the semantics declines to interpret, the other is a policy the
# semantics has never heard of.
KNOWN: frozenset[str] = frozenset().union(*ADMISSIBLE.values())


class Reason:
    """Rejection codes, so a report can count them without matching prose."""

    NOT_ADMISSIBLE = "OPERATOR_NOT_ADMISSIBLE"
    UNKNOWN_OPERATOR = "OPERATOR_UNKNOWN"
    ALLOF_IN_XONE = "ISALLOF_AS_XONE_ALTERNATIVE"


@dataclass(frozen=True)
class Rejection:
    """A problem the signature declines, with what and why.

    ``where`` says which side and which constraint, so that a reader with
    the policy in hand can find it without re-deriving the check.
    """

    problem_id: str
    code: str
    operator: str
    sort: Sort
    where: str
    detail: str

    def __str__(self) -> str:
        return (f"{self.problem_id}: {self.code} "
                f"({self.operator} at {self.sort}, {self.where}) {self.detail}")


@dataclass(frozen=True)
class WellSorted:
    """A problem the signature admits.

    Carries nothing beyond the fact.  The problem itself is unchanged by
    passing, and the next layer takes the problem rather than this.
    """

    problem_id: str
    sort: Sort


def check_constraint(c: Constraint, sort: Sort) -> str | None:
    """The rejection code for one constraint at one sort, or None."""
    if c.operator not in KNOWN:
        return Reason.UNKNOWN_OPERATOR
    if c.operator not in ADMISSIBLE[sort]:
        return Reason.NOT_ADMISSIBLE
    return None


def check_tree(tree: ConstraintTree, sort: Sort, problem_id: str,
               side: str) -> Rejection | None:
    """The first rejection in a tree, or None.

    The first rather than all of them: the tree is not interpreted at all
    once one constraint is inadmissible, so a list of further failures would
    be a list of consequences of the first.
    """
    for n, item in enumerate(tree.items, 1):
        if isinstance(item, Xone):
            for c in item.alts:
                if c.operator == "isAllOf":
                    return Rejection(
                        problem_id, Reason.ALLOF_IN_XONE, "isAllOf", sort,
                        f"{side} item {n}",
                        "an alternative of a xone may not require every "
                        "value it names to be supplied: the witness "
                        "construction adds elements to a set freely, and the "
                        "negation of such an alternative forbids that")
        alts = (item,) if isinstance(item, Constraint) else item.alts
        for c in alts:
            code = check_constraint(c, sort)
            if code == Reason.UNKNOWN_OPERATOR:
                return Rejection(
                    problem_id, code, c.operator, sort, f"{side} item {n}",
                    "not an operator of the fragment")
            if code == Reason.NOT_ADMISSIBLE:
                return Rejection(
                    problem_id, code, c.operator, sort, f"{side} item {n}",
                    f"{c.operator} requires a relation the sort {sort} does "
                    f"not supply; admissible here are "
                    f"{', '.join(sorted(ADMISSIBLE[sort]))}")
    return None


def check(problem: PolicyProblem) -> WellSorted | Rejection:
    """Whether the signature admits the problem, at the binding's sort.

    Offer before request, so that a report reads in the order a reader has
    the documents.
    """
    sort = problem.binding.sort
    for side, tree in (("offer", problem.offer),
                       ("request", problem.request)):
        r = check_tree(tree, sort, problem.id, side)
        if r is not None:
            return r
    return WellSorted(problem.id, sort)