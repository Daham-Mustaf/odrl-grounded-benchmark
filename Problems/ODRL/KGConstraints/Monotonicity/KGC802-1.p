%--------------------------------------------------------------------------
% File     : KGC802-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : Proposition 1: Conflict preservation under disjointness addition [GeoNames+SDA]
% Version  : 1.0
% English  : Proposition 1 (Monotonicity) audit: Conflict preservation
%           : under disjointness addition (a new disjoint pair appears in R').
%           : 
%           : Setup:
%           : R: GeoNames-shaped with two countries asserted disjoint via
%           : the Sibling-Disjointness Assumption (SDA) profile, plus a
%           : sub-region under one of them.
%           : in_concepts_R(gn_germany), in_concepts_R(gn_france),
%           : in_concepts_R(gn_bayern).
%           : leq_R(gn_bayern, gn_germany).
%           : disjoint_R(gn_germany, gn_france).
%           : 
%           : Constraints:
%           : c1 = c_ispartof(gn_germany)
%           : c2 = c_ispartof(gn_france)
%           : R-verdict: verdict_conflict_R(c1, c2).
%           : 
%           : Extension R' (disjointness addition):
%           : Add a fresh disjointness fact UNRELATED to the existing
%           : Conflict pair: disjoint_R_prime(gn_italy, gn_france).
%           : Add the corresponding concept gn_italy.
%           : All R-facts (including the original disjoint_R(germany,
%           : france) and leq_R(bayern, germany)) auto-lift via MONO000
%           : closure axioms.
%           : 
%           : Conjecture (Style B): verdict_conflict_R_prime(c1, c2).
%           : Expected: Theorem.
%           : 
%           : Why: disjointness addition only enlarges the disjointness
%           : relation; it cannot retract any existing fact. The original
%           : Conflict, certified by disjoint_R(germany, france), survives
%           : via closure to disjoint_R_prime(germany, france), and the
%           : R'-version of the propagation axiom fires identically. The
%           : fresh disjoint_R_prime(italy, france) is irrelevant to the
%           : original pair.
%           : 
%           : SMT cross-check: hypothetical witness x with
%           : leq_R_prime(x, gn_germany) and leq_R_prime(x, gn_france).
%           : Closure-derived disjoint_R_prime(germany, france) plus
%           : propagation refute it. Expected: unsat.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC802-1.p
%
% Status   : Theorem
% Verdict  : MonotonicityConflict
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC802-policy.ttl
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
% R-facts: GeoNames-shaped with SDA disjointness and a sub-region.
% ============================================================
fof(r_germany_in_concepts, axiom,
    in_concepts_R(gn_germany)).

fof(r_france_in_concepts, axiom,
    in_concepts_R(gn_france)).

fof(r_bayern_in_concepts, axiom,
    in_concepts_R(gn_bayern)).

fof(r_bayern_leq_germany, axiom,
    leq_R(gn_bayern, gn_germany)).

fof(r_germany_disjoint_france, axiom,
    disjoint_R(gn_germany, gn_france)).

fof(r_distinct_germany_france, axiom,
    gn_germany != gn_france).

fof(r_distinct_germany_bayern, axiom,
    gn_germany != gn_bayern).

fof(r_distinct_france_bayern, axiom,
    gn_france != gn_bayern).

% ============================================================
% R' extension: add italy concept and a disjointness fact UNRELATED
% to the original Conflict pair. R-facts auto-lift via MONO000.
% ============================================================
fof(r_ext_italy_in_concepts_prime, axiom,
    in_concepts_R_prime(gn_italy)).

fof(r_ext_italy_not_in_concepts_R, axiom,
    ~in_concepts_R(gn_italy)).

fof(r_ext_italy_disjoint_france_prime, axiom,
    disjoint_R_prime(gn_italy, gn_france)).

fof(r_ext_distinct_italy_germany, axiom,
    gn_italy != gn_germany).

fof(r_ext_distinct_italy_france, axiom,
    gn_italy != gn_france).

fof(r_ext_distinct_italy_bayern, axiom,
    gn_italy != gn_bayern).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc802, conjecture,
    verdict_conflict_R_prime(c_ispartof(gn_germany), c_ispartof(gn_france))).
%--------------------------------------------------------------------------
