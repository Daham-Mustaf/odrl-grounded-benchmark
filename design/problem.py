"""
problem.py
==========
The canonical form of a benchmark problem, before anything is computed
about it.

A ``PolicyProblem`` is what a manifest loads into.  It holds what the two
parties wrote, what the profile binds their operand to, what the parties
declared, and what the problem's author expects and why.  It holds no
concepts, no formulas, no encodings and no verdict, because none of those
are properties of the policies: they are produced by the layers below, each
by one named mapping.

The line this draws
-------------------
Right operands here are *values*: the IRIs and literals a policy document
contains.  They are strings at this layer and they stay strings, because
whether a value names a concept is a question about the resource, decided
by grounding, and the answer may be no.  A problem that recorded concepts
would have answered that question before asking it.

The expectation is likewise the author's, arrived at by reading the
resource and the definitions.  It is compared against what the solvers
derive; it is never set from them.  That is why it carries a justification:
an expectation without a reason is a record of what a solver said the first
time it ran, and the whole point of expecting something is to be able to
disagree with the solver.

What is deliberately absent
---------------------------
No resource contents.  The problem names a resource and a version; the
fixture holds the file.  Two problems over one resource should not carry two
copies of it.

No sort check.  Well-sortedness is decided by the signature against the
binding, which is the next layer's job, and a problem that recorded its own
well-sortedness could disagree with the signature.

No formula names.  Premises acquire names when a query is built, so that
the names come from one place and mean the same thing in both encodings.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from vocabulary import UnknownReason, Verdict

Sort = Literal["nom", "tax", "mer"]
Side = Literal["offer", "request"]


# --- what the parties wrote -------------------------------------------

@dataclass(frozen=True)
class Constraint:
    """One atomic constraint, with its right operand still a policy value.

    ``values`` is a tuple because the set operators take a list; for the
    others it holds one element.  Its members are values, not concepts:
    ``"https://w3id.org/dpv#ScientificResearch"`` rather than whatever that
    IRI turns out to name.
    """

    operator: str
    values: tuple[str, ...]
    side: Side = "offer"

    def __post_init__(self) -> None:
        if not self.values:
            raise ValueError(f"{self.operator} with no right operand")


@dataclass(frozen=True)
class Or:
    """An ``odrl:or`` over atomic constraints.

    ODRL ranges the operands of a Logical Constraint over atomic
    constraints, so alternatives do not nest and ``alts`` holds
    Constraints rather than trees.
    """

    alts: tuple[Constraint, ...]

    def __post_init__(self) -> None:
        if not self.alts:
            raise ValueError("Logical Constraint with no alternatives")


@dataclass(frozen=True)
class Xone:
    """An ``odrl:xone`` over atomic constraints."""

    alts: tuple[Constraint, ...]

    def __post_init__(self) -> None:
        if not self.alts:
            raise ValueError("Logical Constraint with no alternatives")


Item = Constraint | Or | Xone


@dataclass(frozen=True)
class ConstraintTree:
    """One party's constraints on one operand.

    A conjunction of items, each atomic or a Logical Constraint.  Flat,
    because ODRL's Logical Constraints do not nest; the reduction to
    disjuncts relies on that and would be wrong if they did.
    """

    items: tuple[Item, ...]

    def __post_init__(self) -> None:
        if not self.items:
            raise ValueError("constraint tree with no items")

    def values(self) -> list[str]:
        """Every right-operand value the tree names, in order of appearance.

        This is what grounding is applied to, and what an ungrounded-value
        report points into.
        """
        out: list[str] = []
        for item in self.items:
            alts = (item,) if isinstance(item, Constraint) else item.alts
            for c in alts:
                out.extend(c.values)
        return out

    def operators(self) -> list[str]:
        """Every operator the tree uses, for the signature check."""
        out: list[str] = []
        for item in self.items:
            alts = (item,) if isinstance(item, Constraint) else item.alts
            out.extend(c.operator for c in alts)
        return out


# --- what the profile and the parties supply ---------------------------

@dataclass(frozen=True)
class Binding:
    """What the profile says about one operand.

    The sort is declared here and nowhere else.  It is the profile's
    reading of what the resource publishes, not a property the resource
    has: two profiles may bind one operand to one file at one sort and read
    different relations from it, and two more may read the same relation at
    different sorts.

    ``grounding`` names the procedure that resolves a value to a concept.
    It differs by resource: identity of IRIs for a published graph,
    syntactic validation for a registry.  Naming it here keeps it out of the
    builders, where it would be an implicit behaviour rather than a stated
    one.
    """

    operand: str
    resource: str            # fixture id, not a path
    resource_version: str
    sort: Sort
    grounding: str           # procedure id, resolved by the grounding layer
    background: str = "empty"   # background theory id within the fixture


@dataclass(frozen=True)
class Expectation:
    """What the problem's author expects, and the reason.

    ``reason`` is prose naming the decisive premises: which published
    assertions carry the verdict, or which declaration does, or what the
    resource leaves open.  It is required because an expectation without one
    cannot be distinguished from a transcript of the first solver run.

    ``unknown_reason`` is required when the verdict is Unknown and refused
    otherwise, so that a bare Unknown cannot be written down.
    """

    verdict: Verdict
    reason: str
    unknown_reason: UnknownReason | None = None

    def __post_init__(self) -> None:
        if self.verdict is Verdict.UNKNOWN and self.unknown_reason is None:
            raise ValueError(
                "an Unknown expectation must say which kind: an ungrounded "
                "value is repaired by fixing the policy or the binding, an "
                "epistemic Unknown by a declaration, and the verdict alone "
                "does not distinguish them")
        if self.verdict is not Verdict.UNKNOWN and self.unknown_reason:
            raise ValueError(
                f"unknown_reason on a {self.verdict} expectation")
        if not self.reason.strip():
            raise ValueError(
                "an expectation without a reason records what a solver said "
                "rather than what the author derived")


# --- the problem -------------------------------------------------------

@dataclass(frozen=True)
class PolicyProblem:
    """One pair of constraint trees on one operand, with its expectation.

    The pair is the object a verdict is about.  The two trees are kept
    apart rather than conjoined because the report says which party wrote
    what, and because a certificate names the constraints it used.  Their
    conjunction is what the decision procedure receives, and it is formed
    where that happens rather than here.
    """

    id: str
    title: str
    binding: Binding
    offer: ConstraintTree
    request: ConstraintTree
    expectation: Expectation
    description: str = ""
    declarations: tuple[str, ...] = field(default_factory=tuple)

    def values(self) -> list[str]:
        """Every right-operand value in the problem, offer then request."""
        return self.offer.values() + self.request.values()

    def operators(self) -> list[str]:
        return self.offer.operators() + self.request.operators()

    def conjunction(self) -> ConstraintTree:
        """The two trees as one, which is what the decision procedure takes.

        Legal because ODRL's Logical Constraints do not nest: conjoining two
        flat conjunctions gives a flat conjunction.  The operand is fixed
        throughout, so nothing needs re-checking.
        """
        return ConstraintTree(self.offer.items + self.request.items)