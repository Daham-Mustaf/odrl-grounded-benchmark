"""
compile.py
==========
Turns a constraint tree into a witness condition.

This is Definition Denotation, Definition Witness and the xone reduction of
Section 6 as code.  Given the constraint tree on one operand, the concepts
the grounding names, and the sort, it expands each xone, distributes to
disjuncts, computes each disjunct's witness condition, and emits their
disjunction.

Nothing here is specific to a problem.  A benchmark problem supplies its
tree and its resource; so does a real policy pair.
"""
from dataclasses import dataclass
from itertools import product

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

# Logical Constraints.  ODRL IM 2.5.2 ranges their operands over atomic
# constraints, so alternatives do not nest: a tree is a conjunction of
# items, each a Constraint, an Or or a Xone.  The offer tree and the
# request tree of one operand are compiled as one concatenated conjunction.
@dataclass(frozen=True)
class Or:
    alts: tuple            # of Constraint

@dataclass(frozen=True)
class Xone:
    alts: tuple            # of Constraint

@dataclass(frozen=True)
class Lit:
    """A literal of Definition Witness: a constraint or its negation."""
    c: Constraint
    positive: bool = True

class IllSorted(ValueError):
    pass

def check_tree(items):
    """The xone clause of Definition Signature, decided on operator names."""
    for it in items:
        if isinstance(it, Xone):
            for c in it.alts:
                if c.operator == "isAllOf":
                    raise IllSorted("isAllOf as a xone alternative")

def negate(c: Constraint) -> Lit:
    """Literal negation for the xone expansion.

    isAnyOf is the one meets-mode operator, so its negation is a subset
    condition and rewrites to a positive isNoneOf on the same values.
    Every other negation is the failure of a subset condition and stays a
    negative literal; the witness gives it a meets requirement against the
    complement.  A negated isAllOf cannot occur: check_tree rejected it.
    """
    if c.operator == "isAnyOf":
        return Lit(Constraint("isNoneOf", c.values, c.side))
    if c.operator == "isAllOf":
        raise IllSorted("negated isAllOf")
    return Lit(c, positive=False)

def alternatives(item):
    """The literal sets an item contributes, one per alternative."""
    if isinstance(item, Constraint):
        return ((Lit(item),),)
    if isinstance(item, Or):
        return tuple((Lit(c),) for c in item.alts)
    if isinstance(item, Xone):
        return tuple(
            (Lit(ci),) + tuple(negate(cj)
                               for j, cj in enumerate(item.alts) if j != i)
            for i, ci in enumerate(item.alts))
    raise TypeError(item)

def disjuncts(items):
    """DNF of the tree: one distribution step, alternatives being atomic."""
    check_tree(items)
    return [sum(choice, ()) for choice in product(*map(alternatives, items))]

class Order:
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
    def true_(self):         return "$true"

class SMT:
    def leq(self, a, b):     return f"(kge_leq {a} {b})"
    def eq(self, a, b):      return f"(= {a} {b})"
    def neq(self, a, b):     return f"(not (= {a} {b}))"
    def and_(self, xs):      return "(and " + " ".join(xs) + ")"
    def or_(self, xs):       return "(or " + " ".join(xs) + ")"
    def not_(self, x):       return f"(not {x})"
    def wrap(self, x):       return x
    def true_(self):         return "true"

def admits(c: Constraint, x: str, sort: str, s):
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

def witness_condition(literals, concepts, sort, s):
    """W(K) for one disjunct, over the concepts the grounding names.

        F subset D  and  D non-empty  and  D meets each T in M

    where M is the isAnyOf denotations together with one complement per
    negative literal.  Definition Witness as restated; quantifier-free.
    """
    pos = [l.c for l in literals if l.positive]
    neg = [l.c for l in literals if not l.positive]
    assert all(MODE[c.operator] == SUBSET for c in neg), "negate() invariant"
    subset = [c for c in pos if MODE[c.operator] == SUBSET]
    allof  = [c for c in pos if MODE[c.operator] == SUPERSET]
    anyof  = [c for c in pos if MODE[c.operator] == MEETS]
    def in_D(x):
        return s.and_([admits(c, x, sort, s) for c in subset]) if subset else s.true_()
    conjuncts = []
    for c in allof:
        for v in c.values:
            conjuncts.append(s.wrap(in_D(v)))
    if subset:
        conjuncts.append(s.wrap(s.or_([s.wrap(in_D(x)) for x in concepts])))
    for c in anyof:
        conjuncts.append(s.wrap(s.or_(
            [s.wrap(s.and_([in_D(x), admits(c, x, sort, s)])) for x in concepts])))
    # D meets the complement of each negated denotation.
    for c in neg:
        conjuncts.append(s.wrap(s.or_(
            [s.wrap(s.and_([in_D(x), s.not_(admits(c, x, sort, s))]))
             for x in concepts])))
    if not conjuncts:
        return s.true_()
    return conjuncts[0] if len(conjuncts) == 1 else s.and_(conjuncts)

def witness_of_tree(items, concepts, sort, s):
    ws = [witness_condition(k, concepts, sort, s) for k in disjuncts(items)]
    return ws[0] if len(ws) == 1 else s.or_(ws)

def compile_operand(items, concepts, sort):
    """Both encodings for one operand.

    `items` is the conjunction of Constraints, Or nodes and Xone nodes for
    that operand, offer and request concatenated.  A flat list of
    Constraints is the previous interface and takes the identical path:
    one all-positive disjunct, returned unwrapped.
    """
    return {
        "fof": witness_of_tree(items, concepts, sort, FOF()),
        "smt": witness_of_tree(items, concepts, sort, SMT()),
    }