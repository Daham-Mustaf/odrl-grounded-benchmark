%--------------------------------------------------------------------------
% File     : KGC805-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : Proposition 1: Compatible preservation under disjointness addition [GeoNames]
% Version  : 1.0
% English  : Proposition 1 (Monotonicity) audit: Compatible preservation
%           : under disjointness addition.
%           : 
%           : Setup:
%           : R: GeoNames-shaped, France below Europe, no disjointness.
%           : in_concepts_R(gn_europe), in_concepts_R(gn_france).
%           : leq_R(gn_france, gn_europe).
%           : grounded_as_R(gn_france, gn_france).
%           : 
%           : Constraints:
%           : c1 = c_ispartof(gn_europe)
%           : c2 = c_eq(gn_france)
%           : R-verdict: verdict_compatible_R(c1, c2). Witness: gn_france.
%           : 
%           : Extension R' (disjointness addition, irrelevant to witness):
%           : Add concepts gn_usa and gn_china (both R'-only).
%           : Add disjoint_R_prime(gn_usa, gn_china).
%           : The new disjointness involves two fresh concepts that are
%           : not related to France or Europe via any leq edge. The
%           : R-witness gn_france is unaffected.
%           : 
%           : Conjecture (Style B): verdict_compatible_R_prime(c1, c2).
%           : Expected: Theorem.
%           : 
%           : Why: gn_france satisfies both denotations under R' via closure-
%           : lifted leq_R_prime(france, europe) and grounded_as_R_prime
%           : (france, france). The new disjoint_R_prime(usa, china) does
%           : not affect france because there are no leq edges from
%           : france to either usa or china. The propagation axiom finds
%           : no contradiction at the witness.
%           : 
%           : This is the 'noise immunity' test: irrelevant disjointness
%           : additions do not break unrelated Compatible verdicts.
%           : 
%           : SMT cross-check: assert R-facts and R'-extension facts; check
%           : consistency. Expected: sat with gn_france as witness.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC805-1.p
%
% Status   : Theorem
% Verdict  : MonotonicityCompatible
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC805-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/MONO000-0.ax').

% ─── Constraint tokens, groundings, and resource hooks ───────────────────
% ============================================================
% KGE000 lifted to R
% ============================================================
fof(kge_leq_reflexive_R, axiom,
    ![X]: leq_R(X, X)).

fof(kge_leq_transitive_R, axiom,
    ![X, Y, Z]:
      ((leq_R(X, Y) & leq_R(Y, Z)) => leq_R(X, Z))).

fof(kge_leq_antisymmetric_R, axiom,
    ![X, Y]:
      ((leq_R(X, Y) & leq_R(Y, X)) => X = Y)).

fof(kge_disjoint_symmetric_R, axiom,
    ![X, Y]:
      (disjoint_R(X, Y) => disjoint_R(Y, X))).

fof(kge_disjoint_irreflexive_R, axiom,
    ![X]: ~disjoint_R(X, X)).

fof(kge_disjoint_propagation_R, axiom,
    ![A, B, Z]:
      ((disjoint_R(A, B) & leq_R(Z, A) & leq_R(Z, B))
       => $false)).

% ============================================================
% KGE000 lifted to R' (same axioms, `_R_prime` suffix)
% ============================================================
fof(kge_leq_reflexive_R_prime, axiom,
    ![X]: leq_R_prime(X, X)).

fof(kge_leq_transitive_R_prime, axiom,
    ![X, Y, Z]:
      ((leq_R_prime(X, Y) & leq_R_prime(Y, Z))
       => leq_R_prime(X, Z))).

fof(kge_leq_antisymmetric_R_prime, axiom,
    ![X, Y]:
      ((leq_R_prime(X, Y) & leq_R_prime(Y, X)) => X = Y)).

fof(kge_disjoint_symmetric_R_prime, axiom,
    ![X, Y]:
      (disjoint_R_prime(X, Y) => disjoint_R_prime(Y, X))).

fof(kge_disjoint_irreflexive_R_prime, axiom,
    ![X]: ~disjoint_R_prime(X, X)).

fof(kge_disjoint_propagation_R_prime, axiom,
    ![A, B, Z]:
      ((disjoint_R_prime(A, B) & leq_R_prime(Z, A)
        & leq_R_prime(Z, B))
       => $false)).

% ============================================================
% DENOT000 lifted to R: per-operator denotation rules
% Constraint terms: c_eq/1, c_isa/1, c_ispartof/1, c_haspart/1.
% ============================================================
fof(den_eq_R, axiom,
    ![X, G]:
      (in_denotation_R(X, c_eq(G)) <=> grounded_as_R(X, G))).

fof(den_isa_R, axiom,
    ![X, G]:
      (in_denotation_R(X, c_isa(G)) <=> leq_R(X, G))).

fof(den_ispartof_R, axiom,
    ![X, G]:
      (in_denotation_R(X, c_ispartof(G)) <=> leq_R(X, G))).

fof(den_haspart_R, axiom,
    ![X, G]:
      (in_denotation_R(X, c_haspart(G)) <=> leq_R(G, X))).

% ============================================================
% DENOT000 lifted to R'
% ============================================================
fof(den_eq_R_prime, axiom,
    ![X, G]:
      (in_denotation_R_prime(X, c_eq(G)) <=>
       grounded_as_R_prime(X, G))).

fof(den_isa_R_prime, axiom,
    ![X, G]:
      (in_denotation_R_prime(X, c_isa(G)) <=>
       leq_R_prime(X, G))).

fof(den_ispartof_R_prime, axiom,
    ![X, G]:
      (in_denotation_R_prime(X, c_ispartof(G)) <=>
       leq_R_prime(X, G))).

fof(den_haspart_R_prime, axiom,
    ![X, G]:
      (in_denotation_R_prime(X, c_haspart(G)) <=>
       leq_R_prime(G, X))).

% ============================================================
% Forced-emptiness lifted to R and R'
% ============================================================
fof(forced_empty_R_def, axiom,
    ![C1, C2]:
      (forced_empty_R(C1, C2) <=>
       (![X]: ~(in_denotation_R(X, C1) & in_denotation_R(X, C2))))).

fof(forced_empty_R_prime_def, axiom,
    ![C1, C2]:
      (forced_empty_R_prime(C1, C2) <=>
       (![X]: ~(in_denotation_R_prime(X, C1)
                & in_denotation_R_prime(X, C2))))).

% ============================================================
% Verdict definitions lifted to R and R'
% ============================================================
fof(verdict_compatible_intro_R, axiom,
    ![C1, C2, X]:
      ((in_denotation_R(X, C1) & in_denotation_R(X, C2))
       => verdict_compatible_R(C1, C2))).
fof(verdict_conflict_intro_R, axiom,
    ![C1, C2]:
      (forced_empty_R(C1, C2) => verdict_conflict_R(C1, C2))).
      
fof(verdict_compatible_intro_R_prime, axiom,
    ![C1, C2, X]:
      ((in_denotation_R_prime(X, C1) & in_denotation_R_prime(X, C2))
       => verdict_compatible_R_prime(C1, C2))).
       
fof(verdict_conflict_intro_R_prime, axiom,
    ![C1, C2]:
      (forced_empty_R_prime(C1, C2) => verdict_conflict_R_prime(C1, C2))).

% ============================================================
% Monotone-operator guard (Remark 2 fragment)
% Excludes neq and isNoneOf; their denotations C \ {g} are not
% monotone in leq or disjoint. Asserted on each constraint term used
% in the conjectures of monotone-fragment problems.
% ============================================================
fof(monotone_op_eq, axiom,
    ![G]: monotone_op(c_eq(G))).

fof(monotone_op_isa, axiom,
    ![G]: monotone_op(c_isa(G))).

fof(monotone_op_ispartof, axiom,
    ![G]: monotone_op(c_ispartof(G))).

fof(monotone_op_haspart, axiom,
    ![G]: monotone_op(c_haspart(G))).

% ============================================================
% R-facts: GeoNames-shaped, France below Europe.
% ============================================================
fof(r_europe_in_concepts, axiom,
    in_concepts_R(gn_europe)).

fof(r_france_in_concepts, axiom,
    in_concepts_R(gn_france)).

fof(r_france_leq_europe, axiom,
    leq_R(gn_france, gn_europe)).

fof(r_france_grounded, axiom,
    grounded_as_R(gn_france, gn_france)).

fof(r_distinct_europe_france, axiom,
    gn_europe != gn_france).

% ============================================================
% R' extension: add gn_usa and gn_china with a fresh disjointness
% fact. Both concepts are R'-only and unrelated to France or Europe
% via any leq edge.
% ============================================================
fof(r_ext_usa_in_concepts_prime, axiom,
    in_concepts_R_prime(gn_usa)).

fof(r_ext_usa_not_in_concepts_R, axiom,
    ~in_concepts_R(gn_usa)).

fof(r_ext_china_in_concepts_prime, axiom,
    in_concepts_R_prime(gn_china)).

fof(r_ext_china_not_in_concepts_R, axiom,
    ~in_concepts_R(gn_china)).

fof(r_ext_usa_disjoint_china_prime, axiom,
    disjoint_R_prime(gn_usa, gn_china)).

fof(r_ext_distinct_usa_china, axiom,
    gn_usa != gn_china).

fof(r_ext_distinct_usa_europe, axiom,
    gn_usa != gn_europe).

fof(r_ext_distinct_usa_france, axiom,
    gn_usa != gn_france).

fof(r_ext_distinct_china_europe, axiom,
    gn_china != gn_europe).

fof(r_ext_distinct_china_france, axiom,
    gn_china != gn_france).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc805, conjecture,
    verdict_compatible_R_prime(c_ispartof(gn_europe), c_eq(gn_france))).
%--------------------------------------------------------------------------
