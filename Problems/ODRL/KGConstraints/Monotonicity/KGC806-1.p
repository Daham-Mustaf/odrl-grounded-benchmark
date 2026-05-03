%--------------------------------------------------------------------------
% File     : KGC806-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : Proposition 1: denotation growth under concept addition [GeoNames]
% Version  : 1.0
% English  : Proposition 1 (Monotonicity) audit: denotation growth under
%           : concept addition. This is the underlying mechanism — the
%           : first claim of Proposition 1, on which verdict preservation
%           : (audited by KGC800/803) depends.
%           : 
%           : The conjecture is universally quantified over concepts:
%           : forall X. in_denotation_R(X, c_ispartof(gn_europe))
%           : => in_denotation_R_prime(X, c_ispartof(gn_europe))
%           : 
%           : This says: every concept in [c]_R is also in [c]_R'. The claim
%           : is independent of any specific witness; it tests the closure
%           : axioms uniformly across the concept domain.
%           : 
%           : Setup:
%           : R: GeoNames-shaped with one containment edge.
%           : in_concepts_R(gn_europe), in_concepts_R(gn_france).
%           : leq_R(gn_france, gn_europe).
%           : 
%           : Extension R' (concept addition):
%           : Add concept gn_spain with leq_R_prime(gn_spain, gn_europe).
%           : All R-facts auto-lift via MONO000 closure axioms.
%           : 
%           : Conjecture (Style A): the universal denotation-growth statement.
%           : Expected: Theorem.
%           : 
%           : Why: in_denotation_R(X, c_ispartof(europe)) unfolds (via
%           : den_ispartof_R) to leq_R(X, gn_europe). MONO000's closure
%           : axiom extension_leq lifts this to leq_R_prime(X, gn_europe).
%           : Then den_ispartof_R_prime gives in_denotation_R_prime(X,
%           : c_ispartof(europe)). The chain is purely axiomatic; no
%           : witness construction needed.
%           : 
%           : SMT cross-check: assert R-facts plus extension. Assert that
%           : some specific concept x is in [c]_R but NOT in [c]_R'.
%           : Closure axioms force a contradiction. Expected: unsat.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC806-1.p
%
% Status   : Theorem
% Verdict  : MonotonicityDenotation
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC806-policy.ttl
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

fof(r_distinct_europe_france, axiom,
    gn_europe != gn_france).

% ============================================================
% R' extension: add gn_spain with leq_R_prime(spain, europe).
% R-facts auto-lift via MONO000 closure axioms.
% ============================================================
fof(r_ext_spain_in_concepts_prime, axiom,
    in_concepts_R_prime(gn_spain)).

fof(r_ext_spain_not_in_concepts_R, axiom,
    ~in_concepts_R(gn_spain)).

fof(r_ext_spain_leq_europe_prime, axiom,
    leq_R_prime(gn_spain, gn_europe)).

fof(r_ext_distinct_spain_europe, axiom,
    gn_spain != gn_europe).

fof(r_ext_distinct_spain_france, axiom,
    gn_spain != gn_france).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc806, conjecture,
    ![X]: (in_denotation_R(X, c_ispartof(gn_europe)) => in_denotation_R_prime(X, c_ispartof(gn_europe)))).
%--------------------------------------------------------------------------
