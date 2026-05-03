%--------------------------------------------------------------------------
% File     : KGC801-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : Proposition 1: Conflict preservation under edge addition [synthetic DPV-shaped]
% Version  : 1.0
% English  : Proposition 1 (Monotonicity) audit: Conflict preservation
%           : under edge addition (new subsumption fact in R').
%           : 
%           : Setup:
%           : R: synthetic DPV-shaped taxonomy fragment with two purposes
%           : posited disjoint. NOTE: real DPV does NOT assert this
%           : disjointness; we posit it here as a hypothetical
%           : strengthening to construct a Conflict premise. The audit
%           : tests that adding a subsumption edge (a common parent
%           : relationship) preserves the Conflict verdict.
%           : 
%           : in_concepts_R(dpv_sr).      [ScientificResearch]
%           : in_concepts_R(dpv_cr).      [CommercialResearch]
%           : in_concepts_R(dpv_rd).      [ResearchAndDevelopment]
%           : leq_R(dpv_sr, dpv_rd).      [SR is below R&D]
%           : leq_R(dpv_cr, dpv_rd).      [CR is below R&D]
%           : disjoint_R(dpv_sr, dpv_cr). [SYNTHETIC: not in real DPV]
%           : 
%           : Constraints:
%           : c1 = c_ispartof(dpv_sr)   [denotation: leq_R(., dpv_sr)]
%           : c2 = c_ispartof(dpv_cr)   [denotation: leq_R(., dpv_cr)]
%           : R-verdict: verdict_conflict_R(c1, c2). Forced by the
%           : synthetic disjointness plus propagation.
%           : 
%           : Extension R' (edge addition):
%           : Add a new subsumption edge: leq_R_prime(dpv_sr, dpv_ar).
%           : [SR is also below AcademicResearch in R']
%           : Add concept dpv_ar with leq_R_prime(dpv_ar, dpv_rd).
%           : All R-facts auto-lift via MONO000 closure axioms.
%           : 
%           : Conjecture (Style B): verdict_conflict_R_prime(c1, c2).
%           : Expected: Theorem.
%           : 
%           : Why: edge addition only enriches the partial order; it does
%           : not retract any disjointness fact. The closure axiom lifts
%           : disjoint_R(dpv_sr, dpv_cr) to disjoint_R_prime(dpv_sr, dpv_cr),
%           : and the R'-version of the propagation axiom forces forced
%           : emptiness identically. The new edge to AcademicResearch is
%           : irrelevant to the Conflict because AR isn't a subordinate
%           : of CR.
%           : 
%           : SMT cross-check: hypothetical witness x with
%           : leq_R_prime(x, dpv_sr) and leq_R_prime(x, dpv_cr).
%           : Closure-derived disjoint_R_prime(dpv_sr, dpv_cr) combined
%           : with propagation yields false. Expected: unsat.
%           : 
%           : monotone_op guard: c_ispartof is monotone (Remark 2).
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC801-1.p
%
% Status   : Theorem
% Verdict  : MonotonicityConflict
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC801-policy.ttl
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
% R-facts: synthetic DPV-shaped taxonomy fragment.
% NOTE: kge_disjoint(dpv_sr, dpv_cr) is NOT in real DPV. It is a
% hypothetical strengthening for monotonicity testing. The audit
% claims that, given any consistent resource where this disjointness
% holds, edge addition preserves Conflict.
% ============================================================
fof(r_sr_in_concepts, axiom,
    in_concepts_R(dpv_sr)).

fof(r_cr_in_concepts, axiom,
    in_concepts_R(dpv_cr)).

fof(r_rd_in_concepts, axiom,
    in_concepts_R(dpv_rd)).

fof(r_sr_leq_rd, axiom,
    leq_R(dpv_sr, dpv_rd)).

fof(r_cr_leq_rd, axiom,
    leq_R(dpv_cr, dpv_rd)).

fof(r_sr_disjoint_cr_synthetic, axiom,
    disjoint_R(dpv_sr, dpv_cr)).

fof(r_distinct_sr_cr, axiom,
    dpv_sr != dpv_cr).

fof(r_distinct_sr_rd, axiom,
    dpv_sr != dpv_rd).

fof(r_distinct_cr_rd, axiom,
    dpv_cr != dpv_rd).

% ============================================================
% R' extension: add edge dpv_sr leq dpv_ar via the new concept
% AcademicResearch. Concept dpv_ar is R'-only (concept addition
% accompanies the edge addition, since the new edge needs a target).
% R-facts auto-lift via MONO000 closure axioms.
% ============================================================
fof(r_ext_ar_in_concepts_prime, axiom,
    in_concepts_R_prime(dpv_ar)).

fof(r_ext_ar_not_in_concepts_R, axiom,
    ~in_concepts_R(dpv_ar)).

fof(r_ext_sr_leq_ar_prime, axiom,
    leq_R_prime(dpv_sr, dpv_ar)).

fof(r_ext_ar_leq_rd_prime, axiom,
    leq_R_prime(dpv_ar, dpv_rd)).

fof(r_ext_distinct_ar_sr, axiom,
    dpv_ar != dpv_sr).

fof(r_ext_distinct_ar_cr, axiom,
    dpv_ar != dpv_cr).

fof(r_ext_distinct_ar_rd, axiom,
    dpv_ar != dpv_rd).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc801, conjecture,
    verdict_conflict_R_prime(c_ispartof(dpv_sr), c_ispartof(dpv_cr))).
%--------------------------------------------------------------------------
