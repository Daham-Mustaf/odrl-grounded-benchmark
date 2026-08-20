"""
test_witness.py
===============
Checks the witness lemma by exhaustion, over structures small enough to
enumerate.

    python test_witness.py                 # the standard battery
    python test_witness.py --concepts 4    # slower, wider
    python test_witness.py --verbose       # print each failure in full

What this tests, and why it is worth having
--------------------------------------------
Lemma Witness says: a structure admits a valuation satisfying every literal
of K if and only if it satisfies W(K).  That is the load-bearing claim of the
decision procedure, and it is proved by a construction.  A construction can
be wrong in ways a proof sketch does not reveal, and the way to find out is
not to argue about it but to enumerate every structure over three concepts
and check both sides independently.

Two sides, computed by different routes.

  Left:   for each structure, search every non-empty set of concepts and ask
          whether it satisfies every literal, by the satisfaction modes of
          Definition Valuation, read straight from the definition.

  Right:  evaluate W(K), the formula compile.py emits, in the same structure.

If they ever disagree, the witness condition is wrong for that literal set,
and the test names the structure and the set.  Nothing here consults a
resource, an axiom file or a prover: a disagreement is a bug in the
denotations or in the witness construction, not in an encoding or a solver.

The enumeration
---------------
A structure over C is a partial order on a quotient of C together with the
map h.  Enumerating it means: every partition of C, giving h, then every
partial order on the blocks.  With three concepts that is five partitions and
at most nineteen orders on the largest, a few hundred structures, which runs
in well under a second.  Four concepts is a few tens of thousands and still
tolerable; five is not, and the third concept is where the interesting
failures live anyway, since two concepts cannot separate a down-set from a
singleton.

Identification is the point of enumerating partitions rather than fixing h to
be injective.  A resource that publishes no distinctness admits structures
that identify two names, and several results in the paper turn on that: the
Unknown verdicts, the unsoundness of rewriting a negated equality as a
membership in the complement, and the antisymmetry that collapses a cycle.  A
test over injective h only would miss all of it.

What is not tested here
-----------------------
The reduction from a constraint tree to disjuncts, which is a separate claim
(a valuation satisfies the tree iff it satisfies every literal of some
disjunct), is tested by a second battery below over small trees, by the same
method: enumerate structures, compare the tree's satisfaction against the
disjunction of the disjuncts' witness conditions.

The order axioms are enforced by construction here, so this test says nothing
about whether the axiom files encode them correctly.  That is what the two
provers agreeing on every refutation checks.
"""

import argparse
import itertools
import sys
from dataclasses import dataclass
from typing import Iterator


# --------------------------------------------------------------------------
# The fragment under test, imported if available and mirrored if not.
# --------------------------------------------------------------------------

try:
    sys.path.insert(0, "generators")
    from compile import (Constraint, MODE, SUBSET, MEETS, SUPERSET,
                         witness_condition)
    try:
        from compile import Lit, Or, Xone, disjuncts, witness_of_tree
        HAVE_TREES = True
    except ImportError:
        HAVE_TREES = False
    IMPORTED = True
except ImportError:
    IMPORTED = False
    HAVE_TREES = False
    print("compile.py not importable; nothing to test.", file=sys.stderr)
    raise


# --------------------------------------------------------------------------
# Structures over a small concept set.
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Structure:
    """A partial order on blocks, with h mapping concept names to blocks.

    `h[name]` is the index of the block the name denotes.  `leq[i][j]` is
    whether block i lies below block j.  The order is reflexive, transitive
    and antisymmetric by construction, so every structure enumerated is one
    Definition Structure admits.
    """
    names: tuple
    h: tuple            # h[k] is the block of names[k]
    leq: tuple          # leq[i][j], over blocks

    @property
    def blocks(self):
        return len(set(self.h))

    def below(self, a: str, b: str) -> bool:
        return self.leq[self.h[self.names.index(a)]][self.h[self.names.index(b)]]

    def same(self, a: str, b: str) -> bool:
        return self.h[self.names.index(a)] == self.h[self.names.index(b)]

    def domain(self) -> tuple:
        """The blocks, as the elements a valuation may name."""
        return tuple(range(self.blocks))

    def block_of(self, name: str) -> int:
        return self.h[self.names.index(name)]

    def describe(self) -> str:
        groups = {}
        for k, name in enumerate(self.names):
            groups.setdefault(self.h[k], []).append(name)
        parts = ["=".join(sorted(v)) for _, v in sorted(groups.items())]
        edges = [f"{parts[i]}<{parts[j]}"
                 for i in range(self.blocks) for j in range(self.blocks)
                 if i != j and self.leq[i][j]]
        return f"[{' | '.join(parts)}]" + (f" {' '.join(edges)}" if edges else "")


def partitions(items) -> Iterator[tuple]:
    """Every partition of items, as an assignment of block indices."""
    n = len(items)
    if n == 0:
        yield ()
        return

    def go(k, assigned, used):
        if k == n:
            yield tuple(assigned)
            return
        for b in range(used + 1):
            yield from go(k + 1, assigned + [b], max(used, b + 1))

    yield from go(0, [], 0)


def partial_orders(n: int) -> Iterator[tuple]:
    """Every reflexive, antisymmetric, transitive relation on n elements."""
    off = [(i, j) for i in range(n) for j in range(n) if i != j]
    for bits in itertools.product((False, True), repeat=len(off)):
        m = [[i == j for j in range(n)] for i in range(n)]
        for (i, j), b in zip(off, bits):
            m[i][j] = b
        # antisymmetry
        if any(m[i][j] and m[j][i] for i, j in off):
            continue
        # transitivity
        ok = True
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if m[i][j] and m[j][k] and not m[i][k]:
                        ok = False
                        break
                if not ok:
                    break
            if not ok:
                break
        if ok:
            yield tuple(tuple(r) for r in m)


def structures(names) -> Iterator[Structure]:
    for h in partitions(names):
        for leq in partial_orders(max(h) + 1 if h else 0):
            yield Structure(tuple(names), h, leq)


# --------------------------------------------------------------------------
# Satisfaction, read straight from the definition.
# --------------------------------------------------------------------------

def denotation(c: Constraint, M: Structure) -> set:
    """Table Denotation, as a set of blocks.

    Computed over the whole domain, not over the concepts the grounding
    names, so that the complements are the real complements: this is the
    definition's side of the comparison, and it must not borrow the witness
    condition's finite range.
    """
    dom = set(M.domain())
    g = [M.block_of(v) for v in c.values]
    op = c.operator
    if op == "eq":
        return {g[0]}
    if op == "neq":
        return dom - {g[0]}
    if op in ("isAnyOf", "isAllOf"):
        return set(g)
    if op == "isNoneOf":
        return dom - set(g)
    if op in ("isA", "isPartOf"):
        return {x for x in dom if M.leq[x][g[0]]}
    if op == "hasPart":
        return {x for x in dom if M.leq[g[0]][x]}
    raise ValueError(op)


def satisfies(c: Constraint, S: set, M: Structure) -> bool:
    """Definition Valuation, for one constraint and a bound set S."""
    D = denotation(c, M)
    mode = MODE[c.operator]
    if mode == MEETS:
        return bool(S & D)
    if mode == SUPERSET:
        return D <= S
    return S <= D


def literal_holds(lit, S: set, M: Structure) -> bool:
    ok = satisfies(lit.c, S, M)
    return ok if lit.positive else not ok


def some_valuation(literals, M: Structure) -> bool:
    """The left side: does any non-empty S satisfy every literal?

    Brute force over every non-empty subset of the domain, which is what the
    definition quantifies over once values are ranged over the concepts.
    """
    dom = list(M.domain())
    for r in range(1, len(dom) + 1):
        for S in itertools.combinations(dom, r):
            if all(literal_holds(l, set(S), M) for l in literals):
                return True
    return False


# --------------------------------------------------------------------------
# Evaluating the emitted formula.
# --------------------------------------------------------------------------

class Eval:
    """A syntax whose operations evaluate rather than print.

    Passed to witness_condition in place of FOF or SMT, so the formula the
    compiler builds is the formula this test evaluates: no reimplementation
    of the witness condition, and no parser.
    """

    def __init__(self, M: Structure):
        self.M = M

    def leq(self, a, b):
        return self.M.leq[self._b(a)][self._b(b)]

    def eq(self, a, b):
        return self._b(a) == self._b(b)

    def neq(self, a, b):
        return self._b(a) != self._b(b)

    def and_(self, xs):
        return all(xs)

    def or_(self, xs):
        return any(xs)

    def not_(self, x):
        return not x

    def wrap(self, x):
        return x

    def true_(self):
        return True

    def _b(self, x):
        """Concept names and raw block indices both appear as terms."""
        return x if isinstance(x, int) else self.M.block_of(x)


def witness_holds(literals, concepts, M: Structure) -> bool:
    return witness_condition(literals, list(concepts), "tax", Eval(M))


# --------------------------------------------------------------------------
# The batteries.
# --------------------------------------------------------------------------

def C(op, *vals, side="offer"):
    return Constraint(op, tuple(vals), side)


def L(c, positive=True):
    return Lit(c, positive) if HAVE_TREES else _FallbackLit(c, positive)


@dataclass(frozen=True)
class _FallbackLit:
    c: Constraint
    positive: bool = True


def positive_battery(names):
    """Literal sets over positive operators only.

    These are what the suite already exercises, so a failure here would mean
    the conjunctive case was wrong before any of the xone work.
    """
    a, b, c = names[0], names[1], names[2]
    return [
        ("eq alone",            [L(C("eq", a))]),
        ("eq, eq same",         [L(C("eq", a)), L(C("eq", a))]),
        ("eq, eq different",    [L(C("eq", a)), L(C("eq", b))]),
        ("neq alone",           [L(C("neq", a))]),
        ("eq, neq same",        [L(C("eq", a)), L(C("neq", a))]),
        ("eq, neq different",   [L(C("eq", a)), L(C("neq", b))]),
        ("isA alone",           [L(C("isA", a))]),
        ("isA, eq below",       [L(C("isA", a)), L(C("eq", b))]),
        ("isA, isA",            [L(C("isA", a)), L(C("isA", b))]),
        ("hasPart, isA",        [L(C("hasPart", a)), L(C("isA", b))]),
        ("isAnyOf one",         [L(C("isAnyOf", a))]),
        ("isAnyOf two",         [L(C("isAnyOf", a, b))]),
        ("isAnyOf, eq",         [L(C("isAnyOf", a, b)), L(C("eq", a))]),
        ("isAnyOf, isA",        [L(C("isAnyOf", a, b)), L(C("isA", c))]),
        ("isNoneOf one",        [L(C("isNoneOf", a))]),
        ("isNoneOf, eq clash",  [L(C("isNoneOf", a)), L(C("eq", a))]),
        ("isNoneOf, eq other",  [L(C("isNoneOf", a)), L(C("eq", b))]),
        ("isAllOf one",         [L(C("isAllOf", a))]),
        ("isAllOf two",         [L(C("isAllOf", a, b))]),
        ("isAllOf, isA",        [L(C("isAllOf", a)), L(C("isA", b))]),
        ("isAllOf two, isA",    [L(C("isAllOf", a, b)), L(C("isA", c))]),
        ("isAllOf, isAnyOf",    [L(C("isAllOf", a)), L(C("isAnyOf", b, c))]),
        ("isAllOf, eq clash",   [L(C("isAllOf", a)), L(C("eq", b))]),
    ]


def negative_battery(names):
    """Literal sets containing negations, as the xone expansion produces them.

    The four negations with no dual, and the two that could have been
    rewritten and deliberately are not.  A negated isAnyOf is absent: the
    compiler rewrites it to isNoneOf before it reaches the witness, and that
    rewrite is tested separately.
    """
    a, b, c = names[0], names[1], names[2]
    return [
        ("not eq",              [L(C("eq", a), False)]),
        ("not eq, eq other",    [L(C("eq", a), False), L(C("eq", b))]),
        ("not eq, eq same",     [L(C("eq", a), False), L(C("eq", a))]),
        ("not isA",             [L(C("isA", a), False)]),
        ("not isA, eq",         [L(C("isA", a), False), L(C("eq", b))]),
        ("not isA, isA",        [L(C("isA", a), False), L(C("isA", b))]),
        ("not isPartOf, isA",   [L(C("isPartOf", a), False), L(C("isA", b))]),
        ("not hasPart",         [L(C("hasPart", a), False)]),
        ("not hasPart, isA",    [L(C("hasPart", a), False), L(C("isA", b))]),
        ("not neq",             [L(C("neq", a), False)]),
        ("not neq, eq same",    [L(C("neq", a), False), L(C("eq", a))]),
        ("not neq, eq other",   [L(C("neq", a), False), L(C("eq", b))]),
        ("not isNoneOf",        [L(C("isNoneOf", a), False)]),
        ("not isNoneOf, eq",    [L(C("isNoneOf", a), False), L(C("eq", a))]),
        ("not isNoneOf two",    [L(C("isNoneOf", a, b), False)]),
        ("two negations",       [L(C("eq", a), False), L(C("eq", b), False)]),
        ("xone de/fr, alt 1",   [L(C("eq", a)), L(C("eq", b), False)]),
        ("xone de/fr, alt 2",   [L(C("eq", b)), L(C("eq", a), False)]),
        ("xone isA/eq, alt 1",  [L(C("isA", a)), L(C("eq", b), False)]),
        ("xone isA/eq, alt 2",  [L(C("eq", b)), L(C("isA", a), False)]),
    ]


def run(battery, names, verbose=False):
    """Compare the two sides over every structure, for every literal set."""
    failures = []
    checked = 0
    for label, literals in battery:
        for M in structures(names):
            left = some_valuation(literals, M)
            right = witness_holds(literals, names, M)
            checked += 1
            if left != right:
                failures.append((label, M, left, right))
                if verbose:
                    print(f"  {label}: {M.describe()}  "
                          f"valuation={left} witness={right}")
    return checked, failures


# --------------------------------------------------------------------------
# The tree reduction, when compile.py has it.
# --------------------------------------------------------------------------

def tree_satisfies(items, S: set, M: Structure) -> bool:
    """Definition Valuation lifted to a tree, read straight from it."""
    for it in items:
        if isinstance(it, Constraint):
            if not satisfies(it, S, M):
                return False
        elif isinstance(it, Or):
            if not any(satisfies(c, S, M) for c in it.alts):
                return False
        elif isinstance(it, Xone):
            if sum(1 for c in it.alts if satisfies(c, S, M)) != 1:
                return False
        else:
            raise TypeError(it)
    return True


def some_valuation_tree(items, M: Structure) -> bool:
    dom = list(M.domain())
    for r in range(1, len(dom) + 1):
        for S in itertools.combinations(dom, r):
            if tree_satisfies(items, set(S), M):
                return True
    return False


def tree_battery(names):
    a, b, c = names[0], names[1], names[2]
    return [
        ("xone(eq a, eq b)",
            [Xone((C("eq", a), C("eq", b)))]),
        ("xone(eq a, eq b), isA c",
            [Xone((C("eq", a), C("eq", b))), C("isA", c)]),
        ("xone(isA a, eq b)",
            [Xone((C("isA", a), C("eq", b)))]),
        ("xone(eq a, eq b, eq c)",
            [Xone((C("eq", a), C("eq", b), C("eq", c)))]),
        ("or(eq a, eq b)",
            [Or((C("eq", a), C("eq", b)))]),
        ("or(isA a, isA b)",
            [Or((C("isA", a), C("isA", b)))]),
        ("or(eq a, eq b), neq c",
            [Or((C("eq", a), C("eq", b))), C("neq", c)]),
        ("xone and or",
            [Xone((C("eq", a), C("eq", b))), Or((C("isA", c), C("eq", a)))]),
        ("xone(isAnyOf, eq)",
            [Xone((C("isAnyOf", a, b), C("eq", c)))]),
        ("plain conjunction",
            [C("isA", a), C("eq", b)]),
    ]


def run_trees(battery, names, verbose=False):
    failures = []
    checked = 0
    for label, items in battery:
        for M in structures(names):
            left = some_valuation_tree(items, M)
            right = witness_of_tree(items, list(names), "tax", Eval(M))
            checked += 1
            if left != right:
                failures.append((label, M, left, right))
                if verbose:
                    print(f"  {label}: {M.describe()}  "
                          f"valuation={left} witness={right}")
    return checked, failures


# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--concepts", type=int, default=3,
                    help="how many concept names to enumerate over "
                         "(3 is the standard battery; 4 is slower)")
    ap.add_argument("--verbose", action="store_true",
                    help="print every disagreement as it is found")
    args = ap.parse_args()

    names = tuple("abcdefg"[:args.concepts])
    n_struct = sum(1 for _ in structures(names))
    print(f"{len(names)} concepts, {n_struct} structures\n")

    total_failures = []

    for title, battery, runner in [
        ("positive operators", positive_battery(names), run),
        ("negated literals", negative_battery(names), run),
    ]:
        checked, failures = runner(battery, names, args.verbose)
        status = "ok" if not failures else f"{len(failures)} DISAGREEMENTS"
        print(f"{title:24} {len(battery):3} sets, {checked:6} checks   {status}")
        total_failures += failures

    if HAVE_TREES:
        checked, failures = run_trees(tree_battery(names), names, args.verbose)
        status = "ok" if not failures else f"{len(failures)} DISAGREEMENTS"
        print(f"{'trees (or, xone)':24} {len(tree_battery(names)):3} sets, "
              f"{checked:6} checks   {status}")
        total_failures += failures

        # The rewrite the expansion depends on: a negated isAnyOf must become
        # a positive isNoneOf, not a negative literal.  If a refactor removes
        # it, the negation would emit a meets requirement against the
        # complement, which is satisfiable whenever anything else is in D.
        from compile import negate
        got = negate(C("isAnyOf", names[0], names[1]))
        expect_ok = got.positive and got.c.operator == "isNoneOf"
        print(f"{'negate(isAnyOf) rewrite':24} "
              f"{'ok' if expect_ok else 'WRONG: ' + repr(got)}")
        if not expect_ok:
            total_failures.append(("negate(isAnyOf)", None, None, None))
    else:
        print(f"{'trees (or, xone)':24} not in compile.py yet")

    print()
    if not total_failures:
        print("witness lemma holds on every structure checked.")
        return 0

    print(f"{len(total_failures)} disagreements. The first few:\n")
    seen = set()
    for label, M, left, right in total_failures:
        if label in seen:
            continue
        seen.add(label)
        if M is None:
            print(f"  {label}")
        else:
            print(f"  {label}")
            print(f"    structure : {M.describe()}")
            print(f"    valuation : {left}   (some S satisfies every literal)")
            print(f"    witness   : {right}   (W(K) holds)")
        if len(seen) >= 5:
            break
    return 1


if __name__ == "__main__":
    sys.exit(main())