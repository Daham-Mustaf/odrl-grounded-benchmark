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

A note on the syntax classes
----------------------------
Every method of FOF and SMT returns a term that can be dropped into any
other without changing how it parses.  In TPTP that has to be arranged: the
grammar composes a disjunction out of unit formulas, and a conjunction is
not one, so a mixed unparenthesised chain such as a & b | c is not derivable
at all.  It is ill formed rather than badly bracketed, and a lenient parser
that accepts it is guessing.

That is not a hypothetical.  It happened here, in the meets-mode conjunct of
witness_condition, where a multi-valued isAnyOf produced an unwrapped
disjunction that and_ then joined with &.  Two provers accepted the result
and guessed differently, so the suite reported a disagreement that was
neither prover's doing.  A conforming parser would have rejected the file
and the defect would have surfaced at once, which is the argument for not
relying on a folk precedence rule anywhere in this emitter.

The invariant is therefore: and_, or_ and not_ return self-contained terms.
SMT is prefix and gets this for free; FOF arranges it explicitly.
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
    """The xone clause of Definition Signature, decided on operator names.

    Also rejects a Logical Constraint with no alternatives.  ODRL ranges the
    operands of one over Constraint instances and an empty list is
    malformed, but without the check the failure surfaces three calls away:
    product over an empty alternatives tuple yields nothing, the disjunct
    list is empty, and or_ is handed an empty sequence.  Naming the defect
    here is worth the line, and it makes the empty case unreachable in the
    syntax classes below.
    """
    for it in items:
        if isinstance(it, (Or, Xone)) and not it.alts:
            raise IllSorted("Logical Constraint with no alternatives")
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
    """TPTP.  Infix, so every compound parenthesises itself.

    and_ and or_ wrap their results because & binds tighter than | and a
    term built here may be placed inside either.  A single operand is
    returned unwrapped: the extra parentheses would be noise, and one term
    parses the same wherever it is put.
    """
    def leq(self, a, b):     return f"kge_leq({a}, {b})"
    def eq(self, a, b):      return f"{a} = {b}"
    def neq(self, a, b):     return f"{a} != {b}"

    # xs is never empty: check_tree rejects a Logical Constraint with no
    # alternatives, and witness_condition returns true_() rather than
    # calling and_ on nothing.
    def and_(self, xs):
        xs = list(xs)
        return xs[0] if len(xs) == 1 else "( " + " & ".join(xs) + " )"

    def or_(self, xs):
        xs = list(xs)
        return xs[0] if len(xs) == 1 else "( " + "\n| ".join(xs) + " )"

    def not_(self, x):       return f"~ ( {x} )"

    # Kept for emitters outside this file, which may need to parenthesise a
    # term they did not build.  Nothing here calls it: every constructor
    # above already returns a self-contained term.
    def wrap(self, x):       return f"( {x} )"

    def true_(self):         return "$true"


class SMT:
    """SMT-LIB.  Prefix, so every compound is already self-contained and
    wrap is the identity."""
    def leq(self, a, b):     return f"(kge_leq {a} {b})"
    def eq(self, a, b):      return f"(= {a} {b})"
    def neq(self, a, b):     return f"(not (= {a} {b}))"

    # Arity one returns the operand rather than (and x): SMT-LIB defines and
    # and or as n-ary with n at least two, so the one-element form is of
    # doubtful validity and some solvers reject it.
    def and_(self, xs):
        xs = list(xs)
        return xs[0] if len(xs) == 1 else "(and " + " ".join(xs) + ")"

    def or_(self, xs):
        xs = list(xs)
        return xs[0] if len(xs) == 1 else "(or " + " ".join(xs) + ")"

    def not_(self, x):       return f"(not {x})"
    def wrap(self, x):       return x   # see FOF.wrap
    def true_(self):         return "true"


def admits(c: Constraint, x: str, sort: str, s):
    """Whether the concept x lies in the denotation of c, per Table
    Denotation.  The result is a self-contained term."""
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
        return s.or_([s.eq(x, v) for v in g])
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
    # Not an assert: this guards the soundness of the formula rather than a
    # development invariant, and asserts are removed under python -O.  A
    # negated isAllOf reaching here would compile to a witness condition
    # that does not state Definition Witness.
    for c in neg:
        if MODE[c.operator] != SUBSET:
            raise IllSorted(f"negated {c.operator} is not a subset-mode "
                            f"literal; negate() should have rewritten it")

    subset = [c for c in pos if MODE[c.operator] == SUBSET]
    allof  = [c for c in pos if MODE[c.operator] == SUPERSET]
    anyof  = [c for c in pos if MODE[c.operator] == MEETS]

    def in_D(x):
        return s.and_([admits(c, x, sort, s) for c in subset]) \
            if subset else s.true_()

    conjuncts = []

    # F subset D: every value an isAllOf names must lie in D.
    for c in allof:
        for v in c.values:
            conjuncts.append(in_D(v))

    # D non-empty.  With no subset-mode literal D is everything, and the
    # concept set is non-empty, so the conjunct is omitted rather than
    # emitted as a tautology.
    if subset:
        conjuncts.append(s.or_([in_D(x) for x in concepts]))

    # D meets each isAnyOf denotation.
    for c in anyof:
        conjuncts.append(s.or_(
            [s.and_([in_D(x), admits(c, x, sort, s)]) for x in concepts]))

    # D meets the complement of each negated denotation.
    for c in neg:
        conjuncts.append(s.or_(
            [s.and_([in_D(x), s.not_(admits(c, x, sort, s))])
             for x in concepts]))

    if not conjuncts:
        return s.true_()
    return s.and_(conjuncts)


def witness_of_tree(items, concepts, sort, s):
    ws = [witness_condition(k, concepts, sort, s) for k in disjuncts(items)]
    return s.or_(ws)


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