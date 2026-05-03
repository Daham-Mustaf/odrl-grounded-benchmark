%--------------------------------------------------------------------------
% File     : KGC807-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : Proposition 1: denotation growth under edge addition [GeoNames]
% Version  : 1.0
% English  : Proposition 1 (Monotonicity) audit: denotation growth under
%           : edge addition. Tests the underlying mechanism (closure axiom
%           : for kge_leq) directly via universal denotation-growth claim.
%           : 
%           : The conjecture is universally quantified over concepts:
%           : forall X. in_denotation_R(X, c_ispartof(gn_europe))
%           : => in_denotation_R_prime(X, c_ispartof(gn_europe))
%           : 
%           : This is a stronger test than verdict preservation alone:
%           : every concept in the original denotation must be in the
%           : extended denotation, regardless of any specific witness.
%           : 
%           : Setup:
%           : R: GeoNames-shaped, France below Europe.
%           : in_concepts_R(gn_europe), in_concepts_R(gn_france),
%           : in_concepts_R(gn_germany).
%           : leq_R(gn_france, gn_europe).
%           : 
%           : Extension R' (edge addition):
%           : Add new subsumption edge: leq_R_prime(gn_germany, gn_europe).
%           : Germany is already in R; the new edge enriches the partial
%           : order. R-facts auto-lift via MONO000.
%           : 
%           : Conjecture (Style A): the universal denotation-growth statement.
%           : Expected: Theorem.
%           : 
%           : Why: same chain as KGC806 — den_ispartof_R unfolds, closure
%           : lifts leq_R to leq_R_prime, den_ispartof_R_prime closes the
%           : derivation. The new edge for Germany is irrelevant to the
%           : growth claim because the claim is universally quantified.
%           : 
%           : SMT cross-check: assert R-facts and R'-extension. Hypothetical
%           : x in [c]_R but not in [c]_R'. Closure forces contradiction.
%           : Expected: unsat.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC807-1.p
%
% Status   : Theorem
% Verdict  : MonotonicityDenotation
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC807-policy.ttl
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
% R-facts: GeoNames-shaped with three concepts; only one edge.
% ============================================================
fof(r_europe_in_concepts, axiom,
    in_concepts_R(gn_europe)).

fof(r_france_in_concepts, axiom,
    in_concepts_R(gn_france)).

fof(r_germany_in_concepts, axiom,
    in_concepts_R(gn_germany)).

fof(r_france_leq_europe, axiom,
    leq_R(gn_france, gn_europe)).

fof(r_distinct_europe_france, axiom,
    gn_europe != gn_france).

fof(r_distinct_europe_germany, axiom,
    gn_europe != gn_germany).

fof(r_distinct_france_germany, axiom,
    gn_france != gn_germany).

% ============================================================
% R' extension: add edge leq_R_prime(germany, europe). Germany
% was already in R; the edge is the new fact. R-facts auto-lift
% via MONO000 closure axioms.
% ============================================================
fof(r_ext_germany_leq_europe_prime, axiom,
    leq_R_prime(gn_germany, gn_europe)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc807, conjecture,
    ![X]: (in_denotation_R(X, c_ispartof(gn_europe)) => in_denotation_R_prime(X, c_ispartof(gn_europe)))).
%--------------------------------------------------------------------------
