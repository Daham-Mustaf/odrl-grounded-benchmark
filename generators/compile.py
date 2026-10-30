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


# The set-based operators.  Their right operand is written as an RDF
# collection, one-element lists included, so that the Turtle shows the arity
# the signature checks.  Every other operator takes one value.
SET_OPERATORS = ("isAnyOf", "isAllOf", "isNoneOf")


def right_operand(op: str, values) -> str:
    """The odrl:rightOperand object as Turtle, from already-prefixed terms."""
    values = list(values)
    if op in SET_OPERATORS:
        return "( " + " ".join(values) + " )"
    if len(values) != 1:
        raise ValueError(f"{op} takes one value, got {len(values)}")
    return values[0]


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
    """Rejects a Logical Constraint with no alternatives.

    ODRL ranges the operands of one over Constraint instances and an empty
    list is malformed, but without the check the failure surfaces three
    calls away: product over an empty alternatives tuple yields nothing, the
    disjunct list is empty, and or_ is handed an empty sequence.  Naming the
    defect here is worth the line, and it makes the empty case unreachable
    in the syntax classes below.
    """
    for it in items:
        if isinstance(it, (Or, Xone)) and not it.alts:
            raise IllSorted("Logical Constraint with no alternatives")


def negate(c: Constraint) -> tuple:
    """Literal negation for the xone expansion, as a disjunction of literals.

    isAnyOf is the one meets-mode operator, so its negation is a subset
    condition and rewrites to a positive isNoneOf on the same values.

    isAllOf is the one superset-mode operator.  A bound set fails it when
    some listed value is missing, so its negation is the disjunction of
    neq v over the listed values, each a positive subset-mode literal.

    Every other negation is the failure of a subset condition and stays a
    negative literal; the witness gives it a meets requirement against the
    complement.
    """
    if c.operator == "isAnyOf":
        return (Lit(Constraint("isNoneOf", c.values, c.side)),)
    if c.operator == "isAllOf":
        return tuple(Lit(Constraint("neq", (v,), c.side)) for v in c.values)
    return (Lit(c, positive=False),)


def alternatives(item):
    """The literal sets an item contributes, one per alternative.

    An xone alternative i is c_i together with the negation of every other
    c_j.  A negated isAllOf is a disjunction, so alternative i contributes
    one literal set per choice of disjunct from each negation.
    """
    if isinstance(item, Constraint):
        return ((Lit(item),),)
    if isinstance(item, Or):
        return tuple((Lit(c),) for c in item.alts)
    if isinstance(item, Xone):
        out = []
        for i, ci in enumerate(item.alts):
            negs = [negate(cj) for j, cj in enumerate(item.alts) if j != i]
            for pick in product(*negs):
                out.append((Lit(ci),) + pick)
        return tuple(out)
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


# The witness condition is built as data first, so that it can be cleaned
# before either encoding prints it.  The cleaning is syntactic only: c = c is
# true, x and not x in one conjunction is false, a repeated literal and a
# constant part go.  It never assumes two constants distinct.
TRUE, FALSE = ("true",), ("false",)


class Term:
    """A syntax whose operations build the formula as nested tuples."""
    def leq(self, a, b):     return ("leq", a, b)
    def eq(self, a, b):      return ("eq", a, b)
    def neq(self, a, b):     return ("not", ("eq", a, b))
    def and_(self, xs):      return ("and", tuple(xs))
    def or_(self, xs):       return ("or", tuple(xs))
    def not_(self, x):       return ("not", x)
    def wrap(self, x):       return x
    def true_(self):         return TRUE


def clean(t):
    kind = t[0]
    if kind == "eq":
        return TRUE if t[1] == t[2] else t
    if kind == "not":
        x = clean(t[1])
        return FALSE if x == TRUE else TRUE if x == FALSE else ("not", x)
    if kind in ("and", "or"):
        unit, zero = (TRUE, FALSE) if kind == "and" else (FALSE, TRUE)
        out = {}
        for x in map(clean, t[1]):
            if x == zero:
                return zero
            if x == unit:
                continue
            for y in (x[1] if x[0] == kind else (x,)):
                out.setdefault(y, None)
        if kind == "and" and any(("not", y) in out for y in out):
            return FALSE
        out = list(out)
        return unit if not out else out[0] if len(out) == 1 else (kind, tuple(out))
    return t


def render(t, s):
    kind = t[0]
    if kind == "true":
        return s.true_()
    if kind == "false":
        return s.not_(s.true_())
    if kind == "eq":
        return s.eq(t[1], t[2])
    if kind == "leq":
        return s.leq(t[1], t[2])
    if kind == "not":
        x = t[1]
        return s.neq(x[1], x[2]) if x[0] == "eq" else s.not_(render(x, s))
    return (s.and_ if kind == "and" else s.or_)([render(x, s) for x in t[1]])


def constants_in(t, out=None) -> list:
    """The constants a cleaned formula names, in order of appearance."""
    out = {} if out is None else out
    if t[0] in ("eq", "leq"):
        out.setdefault(t[1], None)
        out.setdefault(t[2], None)
    elif t[0] == "not":
        constants_in(t[1], out)
    elif t[0] in ("and", "or"):
        for x in t[1]:
            constants_in(x, out)
    return list(out)


def witness_term(literals, concepts, sort, full=False):
    """W(K) for one disjunct, as data, before cleaning.

        F subset D  and  D non-empty  and  D meets each T in M

    where M is the isAnyOf denotations together with one complement per
    negative literal.  Definition Witness as restated; quantifier-free.

    D is the set of the concepts every subset-mode literal admits, and a
    part of W asks whether some concept is in it.  Where a literal fixes
    which concepts can be, the part tries only those (full=False):

      F subset D        each value the isAllOf lists; no enumeration.
      D meets isAnyOf   only that list's values.
      D non-empty       if K has an eq literal, only its value; else, if K
                        has isAnyOf or isAllOf, the part is implied and
                        goes; else every concept.
      D meets the complement of a negated literal
                        if K has an eq literal, only its value; else every
                        concept.

    An element of D equals the eq value, and so satisfies what the value
    satisfies; an isAnyOf is met only by its values; a value an isAllOf
    lists is in D.  So each part is the same condition as the part over
    every concept.  full=True tries every concept in every part, which the
    rule is checked against.
    """
    s = Term()
    pos = [l.c for l in literals if l.positive]
    neg = [l.c for l in literals if not l.positive]
    # Not an assert: this guards the soundness of the formula rather than a
    # development invariant, and asserts are removed under python -O.  A
    # negated isAnyOf or isAllOf reaching here would compile to a witness
    # condition that does not state Definition Witness; negate() rewrites
    # both to positive literals.
    for c in neg:
        if MODE[c.operator] != SUBSET:
            raise IllSorted(f"negated {c.operator} is not a subset-mode "
                            f"literal; negate() should have rewritten it")

    subset = [c for c in pos if MODE[c.operator] == SUBSET]
    allof  = [c for c in pos if MODE[c.operator] == SUPERSET]
    anyof  = [c for c in pos if MODE[c.operator] == MEETS]
    pinned = [c.values[0] for c in pos if c.operator == "eq"]

    def in_D(x):
        return s.and_([admits(c, x, sort, s) for c in subset]) \
            if subset else s.true_()

    def some(xs, f):
        return s.or_([f(x) for x in xs])

    conjuncts = []

    # F subset D: every value an isAllOf names must lie in D.
    for c in allof:
        for v in c.values:
            conjuncts.append(in_D(v))

    # D non-empty.  With no subset-mode literal D is everything, and the
    # concept set is non-empty, so the conjunct is omitted rather than
    # emitted as a tautology.
    if subset:
        if full:
            conjuncts.append(some(concepts, in_D))
        elif pinned:
            conjuncts.append(in_D(pinned[0]))
        elif not (anyof or allof):
            conjuncts.append(some(concepts, in_D))

    # D meets each isAnyOf denotation.
    for c in anyof:
        xs = concepts if full else c.values
        conjuncts.append(some(xs, lambda x, c=c: s.and_([in_D(x), admits(c, x, sort, s)])))

    # D meets the complement of each negated denotation.
    for c in neg:
        xs = concepts if full or not pinned else pinned[:1]
        conjuncts.append(some(xs, lambda x, c=c: s.and_(
            [in_D(x), s.not_(admits(c, x, sort, s))])))

    return s.and_(conjuncts) if conjuncts else TRUE


def witness_condition(literals, concepts, sort, s, full=False):
    """W(K) for one disjunct, cleaned and printed in the syntax s."""
    return render(clean(witness_term(literals, concepts, sort, full)), s)


def tree_term(items, concepts, sort, full=False):
    return clean(("or", tuple(witness_term(k, concepts, sort, full)
                              for k in disjuncts(items))))


def witness_of_tree(items, concepts, sort, s, full=False):
    return render(tree_term(items, concepts, sort, full), s)


def compile_operand(items, concepts, sort, full=False):
    """Both encodings for one operand, and the constants the witness uses.

    `items` is the conjunction of Constraints, Or nodes and Xone nodes for
    that operand, offer and request concatenated.  A flat list of
    Constraints is the previous interface and takes the identical path:
    one all-positive disjunct, returned unwrapped.
    """
    t = tree_term(items, concepts, sort, full)
    used = set(constants_in(t))
    return {
        "fof": render(t, FOF()),
        "smt": render(t, SMT()),
        "constants": [c for c in concepts if c in used],
    }
