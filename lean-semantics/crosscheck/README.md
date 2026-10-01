# Brute-force cross-checks

Executable versions of the paper's semantics, checked by enumeration over all
preorders on 2 to 4 concepts (and random constraint sets). Python 3, no
dependencies. They are separate implementations from the Lean files, so
agreement between the two is by review, not by construction.

Lean proves a statement for all models, but only the statement we wrote. These
scripts test that the statement is the intended one. They found three errors
that Lean would have happily proved around: the candidate set `N` was replaced
by `C`, `xone` was counted by content instead of by position, and a negated
`isAnyOf` was not read as `isNoneOf`.

Run from this folder:

    python3 reductions_audit.py     # 14 s
    python3 growth_audit.py         # 9 s
    python3 first_scaffold_audit.py # 2 min, historical

| Claim | Check | Lean |
|---|---|---|
| Witness lemma with the candidate set `N` | T1 in reductions_audit.py | Witness.lean, `admits_atoms_iff` |
| `or`, `xone`, negation reduce to disjuncts | T1 | Disjuncts.lean, `admits_iff_exists_witness` |
| `xone` counts by position | T2 | Disjuncts.lean, `exactlyOne_iff_index` |
| `N = C` is wrong when `N` is smaller | "N-vs-C" line | `Model.cand`, first clause |
| Negated `isAllOf` can be lifted, so the `xone` restriction is optional | T1, second line | not in Lean yet |
| Structures with unnamed elements lose nothing against preorders | T3 | not in Lean yet (collapse) |
| Verdict of two operands is the minimum | T4 | Factoring.lean, `factoring` |
| Monotonicity at a fixed concept set | T5 | not in Lean yet |
| Concept growth: Compatible persists, Incompatible can weaken | growth_audit.py, T6 | not in Lean yet |

Expected output of reductions_audit.py (any change means the semantics moved):

    T1 n=3: 1500 constraint sets (1014 with N strictly inside C) x 29 preorders
       ... 0 disagreements
       ... 0 disagreements
    T2 ... disagrees on 1110 (cset, model) pairs
    N-vs-C: W computed with N=C but true N strictly smaller: 3357 of 23200 pairs wrong
    T3 n=3, carriers up to 4: 14554 structures, 120 theories
       induced-preorder sets differ from preorder models of T: 0
       verdict over structures differs from verdict over preorders: 0 of 177
    T4 factoring: product-model verdict vs min: 0 disagreements of 217
    T5 monotonicity (592 cases): Compatible not preserved 0, Incompatible not preserved 0
       Incompatible under T but T' inconsistent (total verdict would read Compatible): 45 cases

The T2 count is the number of disagreements the wrong reading causes, so it
should stay nonzero. The last T5 line shows why every verdict theorem needs the
assumption that `(R, B)` is consistent.

first_scaffold_audit.py checks the first scaffold's witness condition, which no
longer exists. It is kept as the record of that bug.

`tests/test_witness.py` in the benchmark checks `compile.py` against the
semantics. These scripts check the semantics itself.
