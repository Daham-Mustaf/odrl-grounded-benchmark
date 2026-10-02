"""T6: adding concepts (n=2 -> n=3), and T1 at n=4. Imports reductions_audit."""
import random, itertools
import reductions_audit as tc
tc.PRE[4] = tc.relations_closed(4, False)
random.seed(7)

# T1 at n=4
bad = 0; N_csets = 250
for _ in range(N_csets):
    N = set(random.sample(range(4), random.randint(1, 4)))
    cset = tc.rand_cset(4, N, False)
    cset2 = tc.rand_cset(4, N, True)
    for le in tc.PRE[4]:
        if tc.admits_cset_pre(le, 4, N, cset) != tc.W_cset_pre(le, 4, N, cset): bad += 1
        if tc.admits_cset_pre(le, 4, N, cset2) != tc.W_cset_pre(le, 4, N, cset2, lifted=True): bad += 1
print(f"T1 n=4: {N_csets} constraint sets x {len(tc.PRE[4])} preorders, W vs direct (paper form and lifted form): {bad} disagreements")

# T6: concept growth.  C={0,1}, C'={0,1,2}; N=C, N'=C'. T over {0,1}; T' = T + assertions possibly using 2.
def asserts(n): return [(k,(x,y)) for k in ("below","same","distinct","disjoint") for x in range(n) for y in range(n)]
def verd(models, n, N, cset):
    return tc.verdict([tc.admits_cset_pre(le, n, N, cset) for le in models])
c_to_c = i_to_c = c_to_i = c_to_u = i_to_u = i_to_i = total = 0
ex = None
for _ in range(1500):
    T = random.sample(asserts(2), random.randint(0, 2))
    Tp = T + random.sample(asserts(3), random.randint(0, 3))
    M = [le for le in tc.PRE[2] if all(tc.sat_assert_pre(le,2,a) for a in T)]
    Mp = [le for le in tc.PRE[3] if all(tc.sat_assert_pre(le,3,a) for a in Tp)]
    if not M or not Mp: continue
    cset = tc.rand_cset(2, {0,1}, False)
    v, vp = verd(M,2,{0,1},cset), verd(Mp,3,{0,1,2},cset)
    total += 1
    if v == "C":
        if vp == "C": c_to_c += 1
        elif vp == "I": c_to_i += 1
        else: c_to_u += 1
    if v == "I":
        if vp == "I": i_to_i += 1
        elif vp == "C": i_to_c += 1; ex = ex or (T, Tp, cset)
        else: i_to_u += 1
print(f"T6 concept growth ({total} cases): Compatible stays {c_to_c}, Compatible->Incompatible {c_to_i}, Compatible->Unknown {c_to_u}")
print(f"   Incompatible stays {i_to_i}, Incompatible->Compatible {i_to_c}, Incompatible->Unknown {i_to_u}")
print("   example Incompatible->Compatible:", ex)
# the textbook example: neq a and neq b on C={a,b} vs C'={a,b,c}
t = [("atom",("neq",(0,))),("atom",("neq",(1,)))]
print("   neq a, neq b, no assertions: C={a,b} ->", verd(tc.PRE[2],2,{0,1},t), "; C'={a,b,c} ->", verd(tc.PRE[3],3,{0,1,2},t))
# multi-valued eq: does eq restrict a multi-valued use?
le = tc.PRE[2][0]
print("   eq a with use {a,b} on discrete 2-concept model:", tc.sat_atom_pre(le,2,(0,1),("eq",(0,))), "(False means eq does restrict)")
