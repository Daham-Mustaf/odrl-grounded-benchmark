%--------------------------------------------------------------------------
% File     : KGC804-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : Proposition 1: Compatible preservation under edge addition [GeoNames]
% Version  : 1.0
% English  : Proposition 1 (Monotonicity) audit: Compatible preservation
%           : under edge addition.
%           : 
%           : Setup:
%           : R: GeoNames-shaped with one containment edge.
%           : in_concepts_R(gn_europe), in_concepts_R(gn_france).
%           : leq_R(gn_france, gn_europe).
%           : grounded_as_R(gn_france, gn_france).
%           : 
%           : Constraints:
%           : c1 = c_ispartof(gn_europe)
%           : c2 = c_eq(gn_france)
%           : R-verdict: verdict_compatible_R(c1, c2). Witness: gn_france.
%           : 
%           : Extension R' (edge addition):
%           : Add concept gn_germany with leq_R_prime(gn_germany, gn_europe).
%           : Germany is R'-only. The new subsumption edge enriches the
%           : partial order without disturbing france's containment.
%           : 
%           : Conjecture (Style B): verdict_compatible_R_prime(c1, c2).
%           : Expected: Theorem.
%           : 
%           : Why: gn_france remains in [c1]_R' via closure-lifted
%           : leq_R_prime(france, europe), and in [c2]_R' via closure-lifted
%           : grounded_as_R_prime(france, france). The witness gn_france
%           : survives. Adding the new edge for Germany does not affect
%           : france's relation to europe.
%           : 
%           : SMT cross-check: assert R-facts and R'-extension facts; check
%           : consistency. Expected: sat with gn_france as witness.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC804-1.p
%
% Status   : Theorem
% Verdict  : MonotonicityCompatible
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC804-policy.ttl
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
% R' extension: add gn_germany with new edge to gn_europe.
% gn_germany is R'-only. R-facts auto-lift via MONO000.
% ============================================================
fof(r_ext_germany_in_concepts_prime, axiom,
    in_concepts_R_prime(gn_germany)).

fof(r_ext_germany_not_in_concepts_R, axiom,
    ~in_concepts_R(gn_germany)).

fof(r_ext_germany_leq_europe_prime, axiom,
    leq_R_prime(gn_germany, gn_europe)).

fof(r_ext_distinct_germany_europe, axiom,
    gn_germany != gn_europe).

fof(r_ext_distinct_germany_france, axiom,
    gn_germany != gn_france).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc804, conjecture,
    verdict_compatible_R_prime(c_ispartof(gn_europe), c_eq(gn_france))).
%--------------------------------------------------------------------------
