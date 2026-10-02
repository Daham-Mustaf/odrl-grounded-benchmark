"""Second brute-force audit of the paper's reductions.

T1  Constraint-set witness lemma (or/xone expansion + distribution + W) against the
    direct semantics, with a candidate set N that may be a strict subset of C.
    Variants: paper restriction (no isAllOf under xone) and a lifted version in
    which a negated isAllOf is expanded into a disjunction of isNoneOf literals.
T2  xone by index (paper) versus xone by content (the first Lean scaffold).
T3  Small-model claim: partial-order structures with unnamed carrier elements
    versus preorders on C, at the level of induced preorders and of verdicts.
T4  Operand factoring: product of model spaces versus min.
T5  Monotonicity under extension of the theory.
"""
import itertools, random, sys

random.seed(1)

SINGLE = ["eq", "neq", "isA", "isPartOf", "hasPart"]
SETOPS = ["isAnyOf", "isAllOf", "isNoneOf"]


def mode(op):
    return {"isAnyOf": "meets", "isAllOf": "superset"}.get(op, "subset")


# ---------------------------------------------------------------- preorders
def relations_closed(n, antisym):
    pairs = [(i, j) for i in range(n) for j in range(n) if i != j]
    out = []
    for mask in range(1 << len(pairs)):
        le = [[i == j for j in range(n)] for i in range(n)]
        for k, (i, j) in enumerate(pairs):
            if mask >> k & 1:
                le[i][j] = True
        if any(le[a][b] and le[b][c] and not le[a][c]
               for a in range(n) for b in range(n) for c in range(n)):
            continue
        if antisym and any(le[a][b] and le[b][a] for a in range(n) for b in range(n) if a != b):
            continue
        out.append(tuple(tuple(r) for r in le))
    return out


PRE = {n: relations_closed(n, False) for n in (1, 2, 3)}
POSETS = {m: relations_closed(m, True) for m in (1, 2, 3, 4)}


# --------------------------------------------- generic semantics on a carrier
# A "model" is (carrier size m, order le on carrier, h : C -> carrier).
# For a preorder on C, use m = n, h = identity and treat eqv as identity.
def eqv_pre(le, a, b):
    return le[a][b] and le[b][a]


def denot_pre(le, n, op, args):
    C = range(n)
    if op == "eq":
        return {x for x in C if eqv_pre(le, x, args[0])}
    if op == "neq":
        return {x for x in C if not eqv_pre(le, x, args[0])}
    if op in ("isAnyOf", "isAllOf"):
        return {x for x in C if any(eqv_pre(le, x, g) for g in args)}
    if op == "isNoneOf":
        return {x for x in C if all(not eqv_pre(le, x, g) for g in args)}
    if op in ("isA", "isPartOf"):
        return {x for x in C if le[x][args[0]]}
    if op == "hasPart":
        return {x for x in C if le[args[0]][x]}
    raise ValueError(op)


def sat_atom_pre(le, n, rho, atom):
    op, args = atom
    d = denot_pre(le, n, op, args)
    m = mode(op)
    if m == "meets":
        return any(x in d for x in rho)
    if m == "superset":
        return all(any(eqv_pre(le, x, g) for x in rho) for g in args)
    return all(x in d for x in rho)


def sat_lit_pre(le, n, rho, lit):
    atom, pos = lit
    s = sat_atom_pre(le, n, rho, atom)
    return s if pos else (not s)


def valuations(N):
    N = sorted(N)
    for r in range(1, len(N) + 1):
        for rho in itertools.combinations(N, r):
            yield rho


def admits_lits_pre(le, n, N, K):
    return any(all(sat_lit_pre(le, n, rho, l) for l in K) for rho in valuations(N))


# ----------------------------------------------------------- cset semantics
# Item = ("atom", a) | ("or", [a..]) | ("xone", [a..]);  ConstraintSet = [Item..]
def sat_item_pre(le, n, rho, item, xone_mode="index"):
    kind, x = item
    if kind == "atom":
        return sat_atom_pre(le, n, rho, x)
    if kind == "or":
        return any(sat_atom_pre(le, n, rho, a) for a in x)
    if kind == "xone":
        if xone_mode == "index":
            return sum(1 for a in x if sat_atom_pre(le, n, rho, a)) == 1
        # content: exists a in alts satisfied, and every OTHER (different) alt not
        return any(sat_atom_pre(le, n, rho, a) and
                   all(not sat_atom_pre(le, n, rho, b) for b in x if b != a)
                   for a in x)
    raise ValueError(kind)


def admits_cset_pre(le, n, N, cset, xone_mode="index"):
    return any(all(sat_item_pre(le, n, rho, it, xone_mode) for it in cset)
               for rho in valuations(N))


def disjuncts(cset):
    """Paper: xone -> OR_i (c_i and AND_{j!=i} not c_j); distribute."""
    per_item = []
    for kind, x in cset:
        if kind == "atom":
            per_item.append([[(x, True)]])
        elif kind == "or":
            per_item.append([[(a, True)] for a in x])
        else:
            per_item.append([[(x[i], True)] + [(x[j], False) for j in range(len(x)) if j != i]
                             for i in range(len(x))])
    for combo in itertools.product(*per_item):
        yield [l for part in combo for l in part]


def normalise(K):
    out = []
    for (op, args), pos in K:
        if not pos and op == "isAnyOf":
            out.append((("isNoneOf", args), True))
        else:
            out.append(((op, args), pos))
    return out


def lift_neg_allof(K):
    """Lifted variant: not isAllOf(g1..gk) == OR_i isNoneOf({g_i}); returns list of literal sets."""
    base, pending = [], []
    for (op, args), pos in K:
        if not pos and op == "isAllOf":
            pending.append([(("isNoneOf", (g,)), True) for g in args])
        else:
            base.append(((op, args), pos))
    if not pending:
        yield base
        return
    for combo in itertools.product(*pending):
        yield base + list(combo)


def W_pre(le, n, N, K):
    """Witness condition of the paper with candidate set N (K already normalised)."""
    subsets = [(a, p) for (a, p) in K if p and mode(a[0]) == "subset"]
    allofs = [(a, p) for (a, p) in K if p and a[0] == "isAllOf"]
    anyofs = [(a, p) for (a, p) in K if p and a[0] == "isAnyOf"]
    negs = [(a, p) for (a, p) in K if not p]
    assert all(a[0] != "isAnyOf" and a[0] != "isAllOf" for (a, p) in negs), "needs normalise / paper restriction"
    C = set(range(n))
    D = {x for x in N if all(x in denot_pre(le, n, *a) for a, _ in subsets)}
    F = {x for x in N if any(any(eqv_pre(le, x, g) for g in a[1]) for a, _ in allofs)}
    Ms = [denot_pre(le, n, *a) for a, _ in anyofs] + [C - denot_pre(le, n, *a) for a, _ in negs]
    return F <= D and len(D) > 0 and all(D & T for T in Ms)


def W_cset_pre(le, n, N, cset, lifted=False):
    for K in disjuncts(cset):
        K = normalise(K)
        subs = lift_neg_allof(K) if lifted else [K]
        for K2 in subs:
            if W_pre(le, n, N, K2):
                return True
    return False


# ------------------------------------------------------------------ generators
def atoms_over(n, N):
    out = []
    for op in SINGLE:
        for g in N:
            out.append((op, (g,)))
    for op in SETOPS:
        for r in (1, 2):
            for args in itertools.combinations(sorted(N), r):
                out.append((op, args))
    return out


def rand_cset(n, N, allow_allof_in_xone):
    A = atoms_over(n, N)
    A_noall = [a for a in A if a[0] != "isAllOf"]
    cset = []
    for _ in range(random.randint(1, 3)):
        k = random.random()
        if k < 0.4:
            cset.append(("atom", random.choice(A)))
        elif k < 0.7:
            cset.append(("or", [random.choice(A) for _ in range(random.randint(2, 3))]))
        else:
            pool = A if allow_allof_in_xone else A_noall
            cset.append(("xone", [random.choice(pool) for _ in range(random.randint(2, 3))]))
    return cset


# =========================================================== T1 / T2 / N
def run_T1(n, trials):
    pres = PRE[n]
    bad_paper = bad_lift = bad_content = n_nonfull = 0
    first_bad = None
    first_content = None
    for _ in range(trials):
        N = set(random.sample(range(n), random.randint(1, n)))
        if len(N) < n:
            n_nonfull += 1
        cset = rand_cset(n, N, allow_allof_in_xone=False)
        for le in pres:
            truth = admits_cset_pre(le, n, N, cset)
            if truth != W_cset_pre(le, n, N, cset):
                bad_paper += 1
                first_bad = first_bad or (n, N, cset, le)
            if admits_cset_pre(le, n, N, cset, "content") != truth:
                bad_content += 1
                first_content = first_content or (N, cset, le)
        cset2 = rand_cset(n, N, allow_allof_in_xone=True)
        for le in pres:
            truth2 = admits_cset_pre(le, n, N, cset2)
            if truth2 != W_cset_pre(le, n, N, cset2, lifted=True):
                bad_lift += 1
    print(f"T1 n={n}: {trials} constraint sets ({n_nonfull} with N strictly inside C) x {len(pres)} preorders")
    print(f"   W (paper, with N) vs direct semantics, no isAllOf under xone: {bad_paper} disagreements")
    print(f"   W with negated isAllOf lifted to OR isNoneOf, isAllOf allowed under xone: {bad_lift} disagreements")
    print(f"T2 xone by content vs by index disagrees on {bad_content} (cset, model) pairs")
    if first_content:
        print("   example:", first_content[1], "N=", first_content[0])
    return bad_paper, bad_lift


def run_T1_allN_vs_true_N(n, trials):
    """How wrong is a W that silently takes N = C when the true N is smaller?"""
    pres = PRE[n]
    bad = tot = 0
    for _ in range(trials):
        N = set(random.sample(range(n), random.randint(1, n - 1)))
        cset = rand_cset(n, N, False)
        for le in pres:
            tot += 1
            if admits_cset_pre(le, n, N, cset) != W_cset_pre(le, n, set(range(n)), cset):
                bad += 1
    print(f"N-vs-C: W computed with N=C but true N strictly smaller: {bad} of {tot} pairs wrong")


# ================================================================ T3 collapse
def sat_assert_pre(le, n, a):
    kind, (x, y) = a
    if kind == "below":
        return le[x][y]
    if kind == "same":
        return eqv_pre(le, x, y)
    if kind == "distinct":
        return not eqv_pre(le, x, y)
    if kind == "disjoint":
        return not any(le[z][x] and le[z][y] for z in range(n))
    raise ValueError(kind)


def sat_assert_struct(P, h, a):
    m, le = P
    kind, (x, y) = a
    if kind == "below":
        return le[h[x]][h[y]]
    if kind == "same":
        return h[x] == h[y]
    if kind == "distinct":
        return h[x] != h[y]
    if kind == "disjoint":
        return not any(le[z][h[x]] and le[z][h[y]] for z in range(m))
    raise ValueError(kind)


def induced(P, h, n):
    m, le = P
    return tuple(tuple(le[h[a]][h[b]] for b in range(n)) for a in range(n))


def denot_struct(P, h, op, args):
    m, le = P
    G = [h[g] for g in args]
    M = range(m)
    if op == "eq":
        return {G[0]}
    if op == "neq":
        return set(M) - {G[0]}
    if op in ("isAnyOf", "isAllOf"):
        return set(G)
    if op == "isNoneOf":
        return set(M) - set(G)
    if op in ("isA", "isPartOf"):
        return {x for x in M if le[x][G[0]]}
    if op == "hasPart":
        return {x for x in M if le[G[0]][x]}


def sat_atom_struct(P, h, rho_elems, atom):
    op, args = atom
    d = denot_struct(P, h, op, args)
    md = mode(op)
    if md == "meets":
        return bool(rho_elems & d)
    if md == "superset":
        return d <= rho_elems
    return rho_elems <= d


def admits_cset_struct(P, h, N, cset):
    hN = sorted({h[x] for x in N})
    for r in range(1, len(hN) + 1):
        for rho in itertools.combinations(hN, r):
            rho = set(rho)
            ok = True
            for kind, x in cset:
                if kind == "atom":
                    v = sat_atom_struct(P, h, rho, x)
                elif kind == "or":
                    v = any(sat_atom_struct(P, h, rho, a) for a in x)
                else:
                    v = sum(1 for a in x if sat_atom_struct(P, h, rho, a)) == 1
                if not v:
                    ok = False
                    break
            if ok:
                return True
    return False


def all_structs(n, max_m):
    for m in range(1, max_m + 1):
        for le in POSETS[m]:
            for h in itertools.product(range(m), repeat=n):
                yield (m, le), h


def verdict(admit_list):
    if not admit_list:
        return None
    if all(admit_list):
        return "C"
    if not any(admit_list):
        return "I"
    return "U"


def run_T3(n=3, max_m=4, n_T=150, n_K=3):
    structs = list(all_structs(n, max_m))
    asserts = [(k, (x, y)) for k in ("below", "same", "distinct", "disjoint")
               for x in range(n) for y in range(n)]
    bad_sets = bad_verd = checked = 0
    for _ in range(n_T):
        T = random.sample(asserts, random.randint(1, 4))
        S1 = {induced(P, h, n) for P, h in structs if all(sat_assert_struct(P, h, a) for a in T)}
        S2 = {tuple(map(tuple, le)) for le in PRE[n] if all(sat_assert_pre(le, n, a) for a in T)}
        if S1 != S2:
            bad_sets += 1
        if not S2:
            continue
        for _ in range(n_K):
            N = set(random.sample(range(n), random.randint(1, n)))
            cset = rand_cset(n, N, False)
            vs = verdict([admits_cset_struct(P, h, N, cset) for P, h in structs
                          if all(sat_assert_struct(P, h, a) for a in T)])
            vp = verdict([admits_cset_pre(le, n, N, cset) for le in PRE[n]
                          if all(sat_assert_pre(le, n, a) for a in T)])
            checked += 1
            if vs != vp:
                bad_verd += 1
    print(f"T3 n={n}, carriers up to {max_m}: {len(structs)} structures, {n_T} theories")
    print(f"   induced-preorder sets differ from preorder models of T: {bad_sets}")
    print(f"   verdict over structures differs from verdict over preorders: {bad_verd} of {checked}")


# =============================================================== T4 factoring
def run_T4(trials=400):
    asserts = lambda n: [(k, (x, y)) for k in ("below", "same", "distinct", "disjoint")
                         for x in range(n) for y in range(n)]
    rank = {"I": 0, "U": 1, "C": 2}
    bad = checked = 0
    for _ in range(trials):
        n1, n2 = random.choice([2, 3]), random.choice([2, 3])
        T1 = random.sample(asserts(n1), random.randint(0, 3))
        T2 = random.sample(asserts(n2), random.randint(0, 3))
        M1 = [le for le in PRE[n1] if all(sat_assert_pre(le, n1, a) for a in T1)]
        M2 = [le for le in PRE[n2] if all(sat_assert_pre(le, n2, a) for a in T2)]
        if not M1 or not M2:
            continue
        N1, N2 = set(range(n1)), set(range(n2))
        t1, t2 = rand_cset(n1, N1, False), rand_cset(n2, N2, False)
        a1 = [admits_cset_pre(le, n1, N1, t1) for le in M1]
        a2 = [admits_cset_pre(le, n2, N2, t2) for le in M2]
        glob = verdict([x and y for x in a1 for y in a2])
        mn = min(verdict(a1), verdict(a2), key=lambda v: rank[v])
        checked += 1
        if glob != mn:
            bad += 1
    print(f"T4 factoring: product-model verdict vs min: {bad} disagreements of {checked}")


# ============================================================ T5 monotonicity
def run_T5(trials=600, n=3):
    asserts = [(k, (x, y)) for k in ("below", "same", "distinct", "disjoint")
               for x in range(n) for y in range(n)]
    bad_c = bad_i = bad_i_inconsistent = checked = 0
    for _ in range(trials):
        T = random.sample(asserts, random.randint(0, 3))
        Tp = T + random.sample(asserts, random.randint(1, 3))
        M = [le for le in PRE[n] if all(sat_assert_pre(le, n, a) for a in T)]
        Mp = [le for le in PRE[n] if all(sat_assert_pre(le, n, a) for a in Tp)]
        if not M:
            continue
        N = set(range(n))
        cset = rand_cset(n, N, False)
        v = verdict([admits_cset_pre(le, n, N, cset) for le in M])
        vp = verdict([admits_cset_pre(le, n, N, cset) for le in Mp])
        checked += 1
        if not Mp:
            # inconsistent extension: total Lean verdict (Compatible tested first) says C
            if v == "I":
                bad_i_inconsistent += 1
            continue
        if v == "C" and vp != "C":
            bad_c += 1
        if v == "I" and vp != "I":
            bad_i += 1
    print(f"T5 monotonicity ({checked} cases): Compatible not preserved {bad_c}, Incompatible not preserved {bad_i}")
    print(f"   Incompatible under T but T' inconsistent (total verdict would read Compatible): {bad_i_inconsistent} cases")


if __name__ == "__main__":
    b1 = run_T1(3, 1500)
    b1b = run_T1(2, 800)
    run_T1_allN_vs_true_N(3, 800)
    run_T3(3, 4, 120, 3)
    run_T4(500)
    run_T5(800)
    sys.exit(0 if not any(b1) and not any(b1b) else 1)
