"""
compile.py
==========
Turns a constraint set into a witness condition.

This is Definition Denotation and Definition Witness as code.  Given the
constraints on one operand, the concepts the grounding names, and the sort,
it computes the denotations, intersects them, and emits the disjunction that
Definition Witness prescribes.

Nothing here is specific to a problem.  A benchmark problem supplies its
constraints and its resource; so does a real policy pair.
"""

from dataclasses import dataclass

NOM, TAX, MER = "nom", "tax", "mer"

# How each operator compares a bound set with what a constraint admits.
SUBSET, MEETS, SUPERSET = "subset", "meets", "superset"

MODE = {
    "eq": SUBSET, "neq": SUBSET, "isNoneOf": SUBSET,
    "isA": SUBSET, "isPartOf": SUBSET, "hasPart": SUBSET,
    "isAnyOf": MEETS, "isAllOf": SUPERSET,
}


@dataclass(frozen=True)
class Constraint:
    operator: str
    values: tuple          # grounded concepts, in order
    side: str = "offer"    # for naming the emitted conjunct


class Order:
    """The order the resource publishes, as asserted pairs.

    `below(a, b)` is what the encoding will be asked to decide, so it returns
    a formula rather than a truth value: what holds is settled by the prover
    over R and B, not here.
    """

    def __init__(self, concepts, asserted=()):
        self.concepts = list(concepts)
        self.asserted = set(asserted)

    def leq(self, a, b, syntax):
        return syntax.leq(a, b)


class FOF:
    def leq(self, a, b):     return f"kge_leq({a}, {b})"
    def eq(self, a, b):      return f"{a} = {b}"
    def neq(self, a, b):     return f"{a} != {b}"
    def and_(self, xs):      return " & ".join(xs)
    def or_(self, xs):       return "\n| ".join(f"( {x} )" for x in xs)
    def not_(self, x):       return f"~ ( {x} )"
    def wrap(self, x):       return f"( {x} )"


class SMT:
    def leq(self, a, b):     return f"(kge_leq {a} {b})"
    def eq(self, a, b):      return f"(= {a} {b})"
    def neq(self, a, b):     return f"(not (= {a} {b}))"
    def and_(self, xs):      return "(and " + " ".join(xs) + ")"
    def or_(self, xs):       return "(or " + " ".join(xs) + ")"
    def not_(self, x):       return f"(not {x})"
    def wrap(self, x):       return x


def admits(c: Constraint, x: str, sort: str, s):
    """Whether concept x is in the denotation of c, as a formula.

    Table Denotation, one clause per operator.  `x` ranges over the concepts
    the grounding names, so every clause is an order or identity literal, or
    a finite disjunction of them.
    """
    g = c.values
    if c.operator == "eq":
        return s.eq(x, g[0])
    if c.operator == "neq":
        return s.neq(x, g[0])
    if c.operator in ("isA", "isPartOf"):
        return s.leq(x, g[0])
    if c.operator == "hasPart":
        return s.leq(g[0], x)
    if c.operator in ("isAnyOf", "isAllOf"):
        return s.or_([s.eq(x, v) for v in g]) if len(g) > 1 else s.eq(x, g[0])
    if c.operator == "isNoneOf":
        return s.and_([s.neq(x, v) for v in g])
    raise ValueError(f"no denotation for {c.operator}")


def witness_condition(constraints, concepts, sort, s):
    """W(K), over the concepts the grounding names.

        F subset D  and  D non-empty  and  D meets each A_k

    F is the union of the isAllOf denotations, D the intersection of the
    subset-mode denotations, and the A_k the isAnyOf denotations.  Each is
    computed over `concepts`, so W is quantifier-free.
    """
    subset = [c for c in constraints if MODE[c.operator] == SUBSET]
    allof  = [c for c in constraints if MODE[c.operator] == SUPERSET]
    anyof  = [c for c in constraints if MODE[c.operator] == MEETS]

    def in_D(x):
        return s.and_([admits(c, x, sort, s) for c in subset]) if subset else "$true"

    conjuncts = []

    # F subset D: every concept in some isAllOf denotation is in D.
    for c in allof:
        for v in c.values:
            conjuncts.append(s.wrap(in_D(v)))

    # D non-empty.
    if subset:
        conjuncts.append(s.wrap(s.or_([s.wrap(in_D(x)) for x in concepts])))

    # D meets each A_k.
    for c in anyof:
        conjuncts.append(s.wrap(s.or_(
            [s.wrap(s.and_([in_D(x), admits(c, x, sort, s)])) for x in concepts])))

    if not conjuncts:
        return "$true"
    return conjuncts[0] if len(conjuncts) == 1 else s.and_(conjuncts)


def compile_operand(constraints, concepts, sort):
    """Both encodings of W for one operand."""
    return {
        "fof": witness_condition(constraints, concepts, sort, FOF()),
        "smt": witness_condition(constraints, concepts, sort, SMT()),
    }