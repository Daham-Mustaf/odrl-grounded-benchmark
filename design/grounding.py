"""
grounding.py
============
Values to concepts, and the point at which a problem may stop.

Grounding is the first mapping in the pipeline and the only one that can
fail without anything being wrong.  A value that names no concept of the
bound resource is a policy that cannot be interpreted against that
resource, which is a different thing from two policies that cannot be
satisfied together.  The verdict is Unknown either way, and the reason
distinguishes them.

Why this is its own layer
-------------------------
Because the answer depends on the resource and not on the semantics.  A
published graph resolves an IRI by identity: the concept either is in the
graph or is not.  A registry resolves a tag by validating it: ``en-US`` is
well formed over registered subtags although the registry contains no such
entry, so the concept set is not the registry's contents and membership is
decided by a rule.  Two procedures, one interface, named in the binding.

Folding this into the compiler would make the choice of procedure an
implicit behaviour of whichever builder ran, and would put raw policy
values inside encodings, where a reader could not tell a value from a
concept.

What a procedure is
-------------------
A partial function from values to concepts, registered under a name that a
binding cites.  Partial is the whole point: ``resolve`` returns None for a
value it does not recognise, and nothing downstream is entitled to invent a
concept for it.

Concepts are opaque here.  A procedure returns an identifier for something
in the resource; whether that identifier is an IRI, a normalised tag or a
code is the procedure's business.  What matters downstream is that two
values ground to the same concept exactly when they name the same thing,
which is the procedure's obligation and not the semantics'.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Protocol

from problem import Constraint, ConstraintTree, Item, Or, PolicyProblem, Xone
from vocabulary import UnknownReason, Verdict


class GroundingProcedure(Protocol):
    """Resolves a policy value to a concept of one resource, or does not."""

    id: str

    def resolve(self, value: str) -> str | None:
        ...


@dataclass(frozen=True)
class IRIIdentity:
    """Resolution by IRI identity against a set of published concepts.

    The procedure for a resource published as a graph.  A value names a
    concept when the graph declares that IRI and not otherwise; there is no
    normalisation, because the authority chose the IRIs and two different
    IRIs are two different concepts unless the authority says otherwise.

    ``prefixes`` expands the abbreviated forms a policy may use, so that
    ``dpv:ScientificResearch`` and the full IRI ground to one concept.  That
    is a syntactic convenience of the serialisation, not an identification
    of two concepts.
    """

    id: str
    concepts: frozenset[str]
    prefixes: dict[str, str] = field(default_factory=dict)

    def resolve(self, value: str) -> str | None:
        iri = value
        if ":" in value and not value.startswith(("http://", "https://")):
            prefix, local = value.split(":", 1)
            if prefix in self.prefixes:
                iri = self.prefixes[prefix] + local
        return iri if iri in self.concepts else None


@dataclass(frozen=True)
class SyntacticValidation:
    """Resolution by a validity rule over a registry.

    The procedure for a resource whose concepts are not its entries.  The
    IETF Language Subtag Registry lists subtags; a policy names tags; and a
    well-formed tag over registered subtags is a concept although the
    registry contains no record for it.  So membership is decided by
    ``validate`` rather than by lookup, and the concept set is whatever the
    policies name and the rule admits.

    ``canonical`` is applied to an admitted value, for a registry that
    publishes a preferred form.  It identifies two values that name one
    thing, which is the registry's claim and not ours.
    """

    id: str
    validate: Callable[[str], bool]
    canonical: Callable[[str], str] = lambda v: v

    def resolve(self, value: str) -> str | None:
        return self.canonical(value) if self.validate(value) else None


# --- the result --------------------------------------------------------

@dataclass(frozen=True)
class Ungrounded:
    """A problem that stops here.

    Carries the offending values rather than only the first, so that a
    report can name every one a reader would have to fix, and so that
    fixing one does not merely reveal the next.
    """

    problem_id: str
    values: tuple[str, ...]
    procedure: str

    verdict: Verdict = Verdict.UNKNOWN
    reason: UnknownReason = UnknownReason.UNGROUNDED

    def certificate(self) -> dict:
        """The certificate for an ungrounded Unknown: the values themselves.

        Checkable by applying the named procedure to each and seeing that it
        resolves none of them.  No query exists to model or refute.
        """
        return {"class": "ungrounded",
                "procedure": self.procedure,
                "values": list(self.values)}


@dataclass(frozen=True)
class GroundedTree:
    """A constraint tree whose right operands are concepts.

    The same shape as the tree it came from, with values replaced.  Keeping
    the shape means the reduction to disjuncts is unchanged by grounding,
    and that a certificate can point back at a constraint of the original.
    """

    items: tuple[Item, ...]


@dataclass(frozen=True)
class GroundedProblem:
    """A problem whose every value names a concept.

    ``mapping`` records what resolved to what, so that a certificate over
    concepts can be read back into the policy values a party wrote.  Without
    it a refutation naming ``dpv_scientific_research`` would leave the
    reader to guess which constraint that came from.
    """

    id: str
    source: PolicyProblem
    offer: GroundedTree
    request: GroundedTree
    mapping: dict[str, str]

    @property
    def concepts(self) -> frozenset[str]:
        """The concepts the problem names.

        Not the concept set of the resource, which is larger: this is what
        the constraints mention, and what the witness condition ranges over
        is decided later, by the query builder, from the resource.
        """
        return frozenset(self.mapping.values())

    def conjunction(self) -> GroundedTree:
        return GroundedTree(self.offer.items + self.request.items)


# --- the mapping -------------------------------------------------------

def _ground_item(item: Item, resolve, missing: list[str]) -> Item:
    def one(c: Constraint) -> Constraint:
        out = []
        for v in c.values:
            g = resolve(v)
            if g is None:
                missing.append(v)
                out.append(v)          # kept, so the shape survives
            else:
                out.append(g)
        return Constraint(c.operator, tuple(out), c.side)

    if isinstance(item, Constraint):
        return one(item)
    alts = tuple(one(c) for c in item.alts)
    return Or(alts) if isinstance(item, Or) else Xone(alts)


def ground(problem: PolicyProblem,
           procedure: GroundingProcedure) -> GroundedProblem | Ungrounded:
    """Resolve every value of a problem, or report the ones that do not.

    All values are attempted before failing.  Stopping at the first would
    make a report name one value where several are wrong, and a reader
    fixing that one would return to find the next.

    The procedure must be the one the binding names; the caller looks it up
    rather than this function, because a registry is loaded from a fixture
    and this module does not read files.
    """
    if procedure.id != problem.binding.grounding:
        raise ValueError(
            f"{problem.id} binds grounding procedure "
            f"{problem.binding.grounding!r}, given {procedure.id!r}")

    missing: list[str] = []
    offer = GroundedTree(tuple(_ground_item(i, procedure.resolve, missing)
                               for i in problem.offer.items))
    request = GroundedTree(tuple(_ground_item(i, procedure.resolve, missing)
                                 for i in problem.request.items))

    if missing:
        seen, ordered = set(), []
        for v in missing:
            if v not in seen:
                seen.add(v)
                ordered.append(v)
        return Ungrounded(problem.id, tuple(ordered), procedure.id)

    mapping = {}
    for v in problem.values():
        g = procedure.resolve(v)
        if g is not None:
            mapping[v] = g
    return GroundedProblem(problem.id, problem, offer, request, mapping)