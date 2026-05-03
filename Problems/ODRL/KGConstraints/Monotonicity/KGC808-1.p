%--------------------------------------------------------------------------
% File     : KGC808-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : Proposition 1: denotation growth under disjointness addition with c_haspart [GeoNames]
% Version  : 1.0
% English  : Proposition 1 (Monotonicity) audit: denotation growth under
%           : disjointness addition for the c_haspart operator. This audit
%           : is structurally distinct from KGC806/807 because the c_haspart
%           : denotation is the upward cone (concepts containing G), not the
%           : downward cone (concepts below G). The leq closure axiom is
%           : used in the contravariant direction of the variable.
%           : 
%           : The conjecture is universally quantified:
%           : forall X. in_denotation_R(X, c_haspart(gn_germany))
%           : => in_denotation_R_prime(X, c_haspart(gn_germany))
%           : 
%           : Setup:
%           : R: GeoNames-shaped with Germany below Europe.
%           : in_concepts_R(gn_europe), in_concepts_R(gn_germany).
%           : leq_R(gn_germany, gn_europe).
%           : 
%           : Extension R' (disjointness addition, irrelevant):
%           : Add gn_usa and gn_china (R'-only) with disjoint_R_prime.
%           : All R-facts auto-lift via MONO000.
%           : 
%           : Conjecture (Style A): the universal denotation-growth statement.
%           : Expected: Theorem.
%           : 
%           : Why: in_denotation_R(X, c_haspart(germany)) unfolds (via
%           : den_haspart_R) to leq_R(germany, X). Closure axiom
%           : extension_leq lifts this to leq_R_prime(germany, X). Then
%           : den_haspart_R_prime gives in_denotation_R_prime(X,
%           : c_haspart(germany)). The new disjointness facts are
%           : irrelevant to the leq chain.
%           : 
%           : The contravariant direction (G below X, vs. X below G in
%           : isPartOf) tests the same closure axiom but with the variable
%           : on the opposite side. Saturation provers may take a different
%           : inference path here than in KGC806/807.
%           : 
%           : SMT cross-check: hypothetical x in [c_haspart(germany)]_R but
%           : not in [c_haspart(germany)]_R'. In SMT terms: leq_R(germany,
%           : x) AND NOT leq_R_prime(germany, x). Closure forces
%           : contradiction. Expected: unsat.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC808-1.p
%
% Status   : Theorem
% Verdict  : MonotonicityDenotation
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC808-policy.ttl
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
% R-facts: Germany below Europe (so [c_haspart(germany)]_R = {germany,
% europe, ...} -- every concept that contains Germany).
% ============================================================
fof(r_europe_in_concepts, axiom,
    in_concepts_R(gn_europe)).

fof(r_germany_in_concepts, axiom,
    in_concepts_R(gn_germany)).

fof(r_germany_leq_europe, axiom,
    leq_R(gn_germany, gn_europe)).

fof(r_distinct_europe_germany, axiom,
    gn_europe != gn_germany).

% ============================================================
% R' extension: irrelevant disjointness on two new R'-only concepts.
% Tests that disjointness addition does not break c_haspart denotation
% growth. R-facts auto-lift via MONO000.
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

fof(r_ext_distinct_usa_germany, axiom,
    gn_usa != gn_germany).

fof(r_ext_distinct_china_europe, axiom,
    gn_china != gn_europe).

fof(r_ext_distinct_china_germany, axiom,
    gn_china != gn_germany).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc808, conjecture,
    ![X]: (in_denotation_R(X, c_haspart(gn_germany)) => in_denotation_R_prime(X, c_haspart(gn_germany)))).
%--------------------------------------------------------------------------
