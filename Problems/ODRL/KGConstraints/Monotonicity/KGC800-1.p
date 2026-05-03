%--------------------------------------------------------------------------
% File     : KGC800-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : Proposition 1: Conflict preservation under concept addition [GeoNames-like]
% Version  : 1.0
% English  : Proposition 1 (Monotonicity) audit: Conflict preservation
%           : under concept addition.
%           : 
%           : Setup:
%           : R: GeoNames-shaped flat registry with two disjoint regions.
%           : in_concepts_R(gn_germany), in_concepts_R(gn_france).
%           : disjoint_R(gn_germany, gn_france).
%           : Constraints:
%           : c1 = c_ispartof(gn_germany)  [denotation: leq_R(., gn_germany)]
%           : c2 = c_ispartof(gn_france)   [denotation: leq_R(., gn_france)]
%           : R-verdict: verdict_conflict_R(c1, c2) holds. Witness search
%           : fails because disjoint_R(gn_germany, gn_france) plus
%           : propagation forces no shared subordinate.
%           : 
%           : Extension R':
%           : Add concept gn_spain with its own disjointness facts:
%           : in_concepts_R_prime(gn_spain) and not in_concepts_R(gn_spain)
%           : disjoint_R_prime(gn_spain, gn_germany)
%           : disjoint_R_prime(gn_spain, gn_france)
%           : All R-facts propagate via MONO000 closure axioms.
%           : 
%           : Conjecture (Style B): verdict_conflict_R_prime(c1, c2).
%           : Expected: Theorem.
%           : 
%           : Why: the original Conflict was certified by
%           : disjoint_R(gn_germany, gn_france) + propagation. Under R',
%           : closure gives disjoint_R_prime(gn_germany, gn_france), and
%           : the R'-version of the propagation axiom fires identically.
%           : The introduction of gn_spain doesn't disturb the original
%           : Conflict because gn_spain isn't a subordinate of either
%           : gn_germany or gn_france.
%           : 
%           : SMT cross-check: hypothetical witness x with
%           : leq_R_prime(x, gn_germany) and leq_R_prime(x, gn_france).
%           : Closure-derived disjoint_R_prime(gn_germany, gn_france)
%           : combined with propagation yields false. Expected: unsat.
%           : 
%           : monotone_op guard: c_ispartof and c_eq are monotone (Remark 2);
%           : no neq or isNoneOf used.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC800-1.p
%
% Status   : Theorem
% Verdict  : MonotonicityConflict
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC800-policy.ttl
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
% R-facts: GeoNames-shaped flat registry
% ============================================================
fof(r_germany_in_concepts, axiom,
    in_concepts_R(gn_germany)).

fof(r_france_in_concepts, axiom,
    in_concepts_R(gn_france)).

fof(r_germany_disjoint_france, axiom,
    disjoint_R(gn_germany, gn_france)).

fof(r_distinct_germany_france, axiom,
    gn_germany != gn_france).

% ============================================================
% R' extension: add gn_spain with R'-only disjointness facts
% R-facts auto-lift via MONO000 closure axioms.
% ============================================================
fof(r_ext_spain_in_concepts_prime, axiom,
    in_concepts_R_prime(gn_spain)).

fof(r_ext_spain_not_in_concepts_R, axiom,
    ~in_concepts_R(gn_spain)).

fof(r_ext_spain_disjoint_germany, axiom,
    disjoint_R_prime(gn_spain, gn_germany)).

fof(r_ext_spain_disjoint_france, axiom,
    disjoint_R_prime(gn_spain, gn_france)).

fof(r_ext_distinct_spain_germany, axiom,
    gn_spain != gn_germany).

fof(r_ext_distinct_spain_france, axiom,
    gn_spain != gn_france).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc800, conjecture,
    verdict_conflict_R_prime(c_ispartof(gn_germany), c_ispartof(gn_france))).
%--------------------------------------------------------------------------
