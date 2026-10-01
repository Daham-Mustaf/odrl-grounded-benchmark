"""Historical. Brute-force check of the first Lean scaffold's witness lemma.

The scaffold (no longer in the repository) had a witness condition that used
N = C and did not normalise a negated isAnyOf. This script ports that W and
shows it disagrees with the direct semantics. It also tests the repaired W
that normalises a negated isAnyOf to isNoneOf, as the paper prescribes.
Slow (about two minutes). The current claims are checked by reductions_audit.py.
"""
import itertools, random, sys

random.seed(0)

SINGLE = ["eq", "neq", "isA", "isPartOf", "hasPart"]
SETOPS = ["isAnyOf", "isAllOf", "isNoneOf"]
MODE = {"isAnyOf": "meets", "isAllOf": "superset"}


def mode(op):
    return MODE.get(op, "subset")


def preorders(n):
    pairs = [(i, j) for i in range(n) for j in range(n) if i != j]
    out = []
    for mask in range(1 << len(pairs)):
        le = [[i == j for j in range(n)] for i in range(n)]
        for k, (i, j) in enumerate(pairs):
            if mask >> k & 1:
                le[i][j] = True
        if all(not (le[a][b] and le[b][c]) or le[a][c]
               for a in range(n) for b in range(n) for c in range(n)):
            out.append(le)
    return out


def eqv(le, a, b):
    return le[a][b] and le[b][a]


def denot(le, n, op, args):
    C = range(n)
    if op == "eq":
        return {x for x in C if eqv(le, x, args[0])}
    if op == "neq":
        return {x for x in C if not eqv(le, x, args[0])}
    if op in ("isAnyOf", "isAllOf"):
        return {x for x in C if any(eqv(le, x, g) for g in args)}
    if op == "isNoneOf":
        return {x for x in C if all(not eqv(le, x, g) for g in args)}
    if op in ("isA", "isPartOf"):
        return {x for x in C if le[x][args[0]]}
    if op == "hasPart":
        return {x for x in C if le[args[0]][x]}
    raise ValueError(op)


def satisfies(le, n, rho, atom):
    op, args = atom
    m = mode(op)
    d = denot(le, n, op, args)
    if m == "meets":
        return any(x in d for x in rho)
    if m == "superset":
        return all(any(eqv(le, x, g) for x in rho) for g in args)
    return all(x in d for x in rho)


def sat_lit(le, n, rho, lit):
    atom, pos = lit
    s = satisfies(le, n, rho, atom)
    return s if pos else not s


def admits(le, n, K):
    for r in range(1, n + 1):
        for rho in itertools.combinations(range(n), r):
            if all(sat_lit(le, n, rho, l) for l in K):
                return True
    return False


def W(le, n, K):
    """Exactly Model.W of the scaffold."""
    C = range(n)
    subsets = [l for l in K if l[1] and mode(l[0][0]) == "subset"]
    allofs = [l for l in K if l[1] and l[0][0] == "isAllOf"]
    anyofs = [l for l in K if l[1] and l[0][0] == "isAnyOf"]
    negs = [l for l in K if not l[1]]
    D = {x for x in C if all(x in denot(le, n, *l[0]) for l in subsets)}
    F = {x for x in C if any(any(eqv(le, x, g) for g in l[0][1]) for l in allofs)}
    return (F <= D and len(D) > 0
            and all(any(x in D and x in denot(le, n, *l[0]) for x in C) for l in anyofs)
            and all(any(x in D and x not in denot(le, n, *l[0]) for x in C) for l in negs))


def normalise(K):
    """Paper: a negated isAnyOf is read as isNoneOf on the same values."""
    out = []
    for (op, args), pos in K:
        if not pos and op == "isAnyOf":
            out.append((("isNoneOf", args), True))
        else:
            out.append(((op, args), pos))
    return out


def atoms(n):
    out = []
    for op in SINGLE:
        for g in range(n):
            out.append((op, (g,)))
    for op in SETOPS:
        for r in (1, 2):
            for args in itertools.combinations(range(n), r):
                out.append((op, args))
    return out


def lits(n):
    out = []
    for a in atoms(n):
        out.append((a, True))
        if a[0] != "isAllOf":  # a negated isAllOf cannot occur (signature)
            out.append((a, False))
    return out


def main(n, size3_samples):
    ms = preorders(n)
    L = lits(n)
    bad_scaffold, bad_fixed, total = [], [], 0
    Ks = [list(k) for r in (1, 2) for k in itertools.combinations(L, r)]
    Ks += [random.sample(L, 3) for _ in range(size3_samples)]
    for K in Ks:
        Kn = normalise(K)
        for le in ms:
            total += 1
            truth = admits(le, n, K)
            if truth != W(le, n, K):
                bad_scaffold.append((K, le, truth))
            if truth != W(le, n, Kn):
                bad_fixed.append((K, le, truth))
    print(f"n={n}: {len(ms)} preorders, {len(Ks)} literal sets, {total} (K,M) pairs")
    print(f"  scaffold W disagrees with 'exists valuation': {len(bad_scaffold)}")
    print(f"  W after normalising negated isAnyOf disagrees: {len(bad_fixed)}")
    return bad_scaffold, bad_fixed


if __name__ == "__main__":
    bs, bf = main(3, 20000)
    if bs:
        # report the smallest counterexample
        bs.sort(key=lambda t: len(t[0]))
        K, le, truth = bs[0]
        print("  smallest scaffold counterexample:")
        print("   K =", K)
        print("   le =", le)
        print("   exists valuation:", truth, " W says:", not truth)
    bs4, bf4 = main(4, 3000)
    sys.exit(0 if not bf and not bf4 else 1)
