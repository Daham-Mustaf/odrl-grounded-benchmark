"""
query.py
========
A grounded problem and a fixture become two queries.

The verdict asks whether every admissible structure admits a valuation
satisfying both parties' constraints.  A solver cannot be asked that: the
question quantifies over valuations and the query language has no symbol
for one.  So the valuation is eliminated first, into a witness condition
true in exactly the structures that admit one, and the remaining question
is asked twice.

    R u B u {W}       unsatisfiable: no structure admits one  -> Incompatible
    R u B u {not W}   unsatisfiable: every structure does     -> Compatible
    both satisfiable                                          -> Unknown

Premises keep the fixture's names
---------------------------------
Nothing here invents a name.  A query holds the Premise objects the fixture
built, so an assertion is called the same thing in both encodings, and a
proof from one prover and an unsat core from the other can be compared
premise by premise rather than counted.

The witness condition is a formula, not a premise
-------------------------------------------------
It is what the query asks about, and it carries the class ``wc`` so that a
refutation citing it is visibly resting on the constraints rather than on
anything published or declared.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Literal

from fixture import Fixture, Premise
from grounding import GroundedProblem, GroundedTree
from problem import Constraint, Item, Or, Xone
from vocabulary import PremiseClass

# How each operator compares the concepts a use names with the concepts a
# constraint admits.  Table (Denotation) of the paper, as three modes.
SUBSET, MEETS, SUPERSET = "subset", "meets", "superset"

MODE: dict[str, str] = {
    "eq": SUBSET, "neq": SUBSET, "isNoneOf": SUBSET,
    "isA": SUBSET, "isPartOf": SUBSET, "hasPart": SUBSET,
    "isAnyOf": MEETS, "isAllOf": SUPERSET,
}


# --- the formula language ----------------------------------------------
#
# Small enough to be read at a glance, and deliberately not an expression
# tree with an evaluator: the encodings walk it, the certificate checker
# walks it, and neither should need to understand more than five shapes.

@dataclass(frozen=True)
class Eq:
    lhs: str
    rhs: str


@dataclass(frozen=True)
class Leq:
    lhs: str
    rhs: str


@dataclass(frozen=True)
class Not:
    inner: "Formula"


@dataclass(frozen=True)
class And:
    parts: tuple["Formula", ...]


@dataclass(frozen=True)
class Or_:
    parts: tuple["Formula", ...]


@dataclass(frozen=True)
class Top:
    pass


Formula = Eq | Leq | Not | And | Or_ | Top


def conj(parts: list[Formula]) -> Formula:
    parts = [p for p in parts if not isinstance(p, Top)]
    if not parts:
        return Top()
    return parts[0] if len(parts) == 1 else And(tuple(parts))


def disj(parts: list[Formula]) -> Formula:
    if not parts:
        raise ValueError("empty disjunction: no concept to range over")
    return parts[0] if len(parts) == 1 else Or_(tuple(parts))


# --- literals, and the xone expansion ----------------------------------

@dataclass(frozen=True)
class Literal:
    constraint: Constraint
    positive: bool = True


def negate(c: Constraint) -> Literal:
    """The negation of a constraint, as a literal.

    ``isAnyOf`` is the one meets-mode operator, so its negation is a subset
    condition and rewrites to ``isNoneOf`` on the same values.  A negated
    ``isAllOf`` cannot occur: the signature rejects it as a xone
    alternative, which is the only place a negation arises.
    """
    if c.operator == "isAnyOf":
        return Literal(Constraint("isNoneOf", c.values, c.side))
    if c.operator == "isAllOf":
        raise ValueError(
            "negated isAllOf: the signature should have rejected this "
            "problem before a query was built")
    return Literal(c, positive=False)


def alternatives(item: Item) -> tuple[tuple[Literal, ...], ...]:
    if isinstance(item, Constraint):
        return ((Literal(item),),)
    if isinstance(item, Or):
        return tuple((Literal(c),) for c in item.alts)
    return tuple(
        (Literal(ci),) + tuple(negate(cj) for j, cj in enumerate(item.alts)
                               if j != i)
        for i, ci in enumerate(item.alts))


def disjuncts(tree: GroundedTree) -> list[tuple[Literal, ...]]:
    """The tree in disjunctive normal form, one distribution step.

    Legal in one step because ODRL's Logical Constraints do not nest, so
    the tree is a conjunction of items each of which is atomic or a flat
    alternation.
    """
    return [sum(choice, ())
            for choice in product(*map(alternatives, tree.items))]


# --- denotation and witness condition ----------------------------------

def admits(c: Constraint, x: str) -> Formula:
    """Whether the concept x lies in the denotation of c."""
    g = c.values
    if c.operator == "eq":
        return Eq(x, g[0])
    if c.operator == "neq":
        return Not(Eq(x, g[0]))
    if c.operator in ("isA", "isPartOf"):
        return Leq(x, g[0])
    if c.operator == "hasPart":
        return Leq(g[0], x)
    if c.operator in ("isAnyOf", "isAllOf"):
        return disj([Eq(x, v) for v in g])
    if c.operator == "isNoneOf":
        return conj([Not(Eq(x, v)) for v in g])
    raise ValueError(f"no denotation for {c.operator}")


def witness_of_literals(lits: tuple[Literal, ...],
                        concepts: list[str]) -> Formula:
    """W(K): the structures admitting a valuation that satisfies every
    literal of K.

        F subset D  and  D non-empty  and  D meets each T

    where D is the intersection of the subset-mode denotations, F the union
    of the isAllOf denotations, and the T are the isAnyOf denotations
    together with one complement per negated literal.
    """
    pos = [l.constraint for l in lits if l.positive]
    neg = [l.constraint for l in lits if not l.positive]
    for c in neg:
        if MODE[c.operator] != SUBSET:
            raise ValueError(
                f"negated {c.operator} is not a subset-mode literal; "
                f"negate() should have rewritten it")

    subset = [c for c in pos if MODE[c.operator] == SUBSET]
    allof = [c for c in pos if MODE[c.operator] == SUPERSET]
    anyof = [c for c in pos if MODE[c.operator] == MEETS]

    def in_D(x: str) -> Formula:
        # With no subset-mode literal D is every concept, so membership is
        # unconditional.  The convention matters: without it the empty
        # intersection would be read as empty rather than as everything.
        return conj([admits(c, x) for c in subset]) if subset else Top()

    parts: list[Formula] = []
    for c in allof:                       # F subset D
        for v in c.values:
            parts.append(in_D(v))
    if subset:                            # D non-empty
        parts.append(disj([in_D(x) for x in concepts]))
    for c in anyof:                       # D meets each isAnyOf denotation
        parts.append(disj([conj([in_D(x), admits(c, x)]) for x in concepts]))
    for c in neg:                         # D meets each complement
        parts.append(disj([conj([in_D(x), Not(admits(c, x))])
                           for x in concepts]))
    return conj(parts)


def witness_condition(tree: GroundedTree, concepts: list[str]) -> Formula:
    ds = disjuncts(tree)
    return disj([witness_of_literals(k, concepts) for k in ds])


# --- the queries -------------------------------------------------------

@dataclass(frozen=True)
class Query:
    """One satisfiability question: premises together with a target.

    ``kind`` is ``inc`` for the query whose unsatisfiability gives
    Incompatible and ``comp`` for the one whose unsatisfiability gives
    Compatible.  It is part of the object rather than of a filename, so
    that nothing has to infer it from a suffix.
    """

    problem_id: str
    kind: Literal["inc", "comp"]
    premises: tuple[Premise, ...]
    target: Formula
    target_name: str
    concepts: tuple[str, ...]
    uses_order: bool

    def premise_names(self) -> set[str]:
        return {p.name for p in self.premises} | {self.target_name}

    def legal_premise(self, name: str) -> bool:
        """Whether a certificate may cite this name.

        A formula of the query, or an instance of an axiom the query
        declares.  The axioms are not premises of the query, since they are
        schemas rather than assertions, but their ground instances are
        legitimate in a refutation, which is what a checker must allow.
        """
        if name in self.premise_names():
            return True
        cls = PremiseClass.from_name(name)
        return cls is not None and cls.is_constitutive and self.uses_order


@dataclass(frozen=True)
class QueryPair:
    """The two queries a problem produces.

    Both carry the same premises; they differ in the target alone.  That is
    the invariant this type exists to hold: a difference in premises
    between the two would mean the pair was asking about two different
    theories, and the verdict would be about neither.
    """

    problem_id: str
    inc: Query
    comp: Query
    theory_id: str

    def __post_init__(self) -> None:
        if self.inc.premise_names() - {self.inc.target_name} != \
           self.comp.premise_names() - {self.comp.target_name}:
            raise ValueError(
                f"{self.problem_id}: the two queries carry different "
                f"premises; they must differ only in the target")


def build(problem: GroundedProblem, fixture: Fixture) -> QueryPair:
    """The two queries for a grounded problem over a fixture.

    The premises are the resource's order assertions and the declarations
    of the theory the binding names.  The concepts are the fixture's, not
    the problem's: the non-emptiness conjunct asks whether *some* concept
    satisfies the constraints, and that ranges over everything the resource
    names.
    """
    theory = fixture.theory(problem.source.binding.background)
    premises = fixture.order + theory.premises
    concepts = sorted(fixture.concepts)

    W = witness_condition(problem.conjunction(), concepts)
    name = f"wc_{problem.id.lower()}"

    # The order axioms are needed only when an assertion or the condition
    # mentions the order.  A purely nominal problem that declared them
    # would reference a symbol nothing else uses.
    uses_order = bool(fixture.order) or _mentions_order(W)

    return QueryPair(
        problem_id=problem.id,
        theory_id=theory.id,
        inc=Query(problem.id, "inc", premises, W, name,
                  tuple(concepts), uses_order),
        comp=Query(problem.id, "comp", premises, Not(W), name,
                   tuple(concepts), uses_order),
    )


def _mentions_order(f: Formula) -> bool:
    if isinstance(f, Leq):
        return True
    if isinstance(f, Not):
        return _mentions_order(f.inner)
    if isinstance(f, (And, Or_)):
        return any(_mentions_order(p) for p in f.parts)
    return False