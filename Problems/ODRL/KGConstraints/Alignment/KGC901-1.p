%--------------------------------------------------------------------------
% File     : KGC901-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : Proposition 2: Compatible transport in aligned subdomain [GeoNames ↔ ISO 3166]
% Version  : 1.0
% English  : Proposition 2 (Verdict under alignment) — first case audit:
%           : Compatible transports across the GeoNames ↔ ISO 3166
%           : alignment via witness construction.
%           : 
%           : This is the dual of KGC900: where KGC900 transports Conflict
%           : via disjointness preservation, KGC901 transports Compatible
%           : via grounding preservation and order preservation. The R_A
%           : witness gn_bayern transports to R_B as iso_de_by through
%           : the alignment.
%           : 
%           : R_A (GeoNames slice):
%           : Concepts: gn_germany, gn_bayern.
%           : Hierarchy: leq_A(gn_bayern, gn_germany).
%           : Grounding: grounded_as_A(gn_bayern, gn_bayern).
%           : 
%           : R_B (ISO 3166 slice):
%           : Concepts: iso_de, iso_de_by.
%           : Hierarchy: leq_B(iso_de_by, iso_de).
%           : No direct grounding asserted — transports via alignment.
%           : 
%           : Alignment α (2 facts):
%           : align(gn_germany, iso_de),
%           : align(gn_bayern, iso_de_by).
%           : 
%           : R_A constraints:
%           : c1 = c_ispartof(gn_germany)  -- Bayern is part of Germany
%           : c2 = c_eq(gn_bayern)         -- exactly Bayern
%           : R_A verdict: verdict_compatible_A. Witness gn_bayern is in
%           : both denotations: leq_A(gn_bayern, gn_germany) puts it
%           : in [c1]_A; grounded_as_A(gn_bayern, gn_bayern) puts it
%           : in [c2]_A.
%           : 
%           : R_B aligned constraints (via operator-matching axioms):
%           : c1' = c_ispartof(iso_de),
%           : c2' = c_eq(iso_de_by).
%           : 
%           : Conjecture (Style B): verdict_compatible_B(c_ispartof(iso_de),
%           : c_eq(iso_de_by)).
%           : Expected: Theorem.
%           : 
%           : Why: align_grounding_preservation applied to
%           : grounded_as_A(gn_bayern, gn_bayern) and
%           : align(gn_bayern, iso_de_by) yields
%           : grounded_as_B(gn_bayern, iso_de_by). By den_eq_B, this puts
%           : gn_bayern into [c_eq(iso_de_by)]_B. The asserted
%           : leq_B(iso_de_by, iso_de), combined with reflexivity
%           : (or directly: gn_bayern grounded as iso_de_by, leq_B
%           : iso_de_by iso_de), establishes gn_bayern in
%           : [c_ispartof(iso_de)]_B. Both denotations contain a witness;
%           : verdict_compatible_intro_B fires.
%           : 
%           : Note: the witness in R_B is gn_bayern (same constant), but
%           : via grounded_as_B(gn_bayern, iso_de_by) it represents the
%           : ISO 3166 concept iso_de_by. This is how cross-resource
%           : witness transport works: the value (gn_bayern) has
%           : different groundings in the two resources.
%           : 
%           : Load-bearing alignment axioms: align_grounding_preservation
%           : (transports the eq witness across resources).
%           : 
%           : SMT cross-check: assert all R_A, R_B, and alignment facts;
%           : check satisfiability with witness gn_bayern in both
%           : R_B-denotations. Expected: sat. Z3 should construct a model
%           : with gn_bayern as the witness; cvc5 may return unknown
%           : due to known limitations on quantifier instantiation for
%           : Compatible-class problems.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC901-1.p
%
% Status   : Theorem
% Verdict  : AlignmentCompatible
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC901-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ALIGN000-0.ax').

% ─── Constraint tokens, groundings, and resource hooks ───────────────────
% ============================================================
% KGE000 lifted to R_A
% ============================================================
fof(kge_leq_reflexive_A, axiom,
    ![X]: leq_A(X, X)).
fof(kge_leq_transitive_A, axiom,
    ![X, Y, Z]:
      ((leq_A(X, Y) & leq_A(Y, Z)) => leq_A(X, Z))).
fof(kge_leq_antisymmetric_A, axiom,
    ![X, Y]:
      ((leq_A(X, Y) & leq_A(Y, X)) => X = Y)).
fof(kge_disjoint_symmetric_A, axiom,
    ![X, Y]:
      (disjoint_A(X, Y) => disjoint_A(Y, X))).
fof(kge_disjoint_irreflexive_A, axiom,
    ![X]: ~disjoint_A(X, X)).
fof(kge_disjoint_propagation_A, axiom,
    ![X1, X2, Z]:
      ((disjoint_A(X1, X2) & leq_A(Z, X1) & leq_A(Z, X2))
       => $false)).
% ============================================================
% KGE000 lifted to R_B
% ============================================================
fof(kge_leq_reflexive_B, axiom,
    ![X]: leq_B(X, X)).
fof(kge_leq_transitive_B, axiom,
    ![X, Y, Z]:
      ((leq_B(X, Y) & leq_B(Y, Z)) => leq_B(X, Z))).
fof(kge_leq_antisymmetric_B, axiom,
    ![X, Y]:
      ((leq_B(X, Y) & leq_B(Y, X)) => X = Y)).
fof(kge_disjoint_symmetric_B, axiom,
    ![X, Y]:
      (disjoint_B(X, Y) => disjoint_B(Y, X))).
fof(kge_disjoint_irreflexive_B, axiom,
    ![X]: ~disjoint_B(X, X)).
fof(kge_disjoint_propagation_B, axiom,
    ![X1, X2, Z]:
      ((disjoint_B(X1, X2) & leq_B(Z, X1) & leq_B(Z, X2))
       => $false)).
% ============================================================
% DENOT000 lifted to R_A and R_B
% ============================================================
fof(den_eq_A, axiom,
    ![X, G]:
      (in_denotation_A(X, c_eq(G)) <=> grounded_as_A(X, G))).
fof(den_isa_A, axiom,
    ![X, G]:
      (in_denotation_A(X, c_isa(G)) <=> leq_A(X, G))).
fof(den_ispartof_A, axiom,
    ![X, G]:
      (in_denotation_A(X, c_ispartof(G)) <=> leq_A(X, G))).
fof(den_haspart_A, axiom,
    ![X, G]:
      (in_denotation_A(X, c_haspart(G)) <=> leq_A(G, X))).
fof(den_eq_B, axiom,
    ![X, G]:
      (in_denotation_B(X, c_eq(G)) <=> grounded_as_B(X, G))).
fof(den_isa_B, axiom,
    ![X, G]:
      (in_denotation_B(X, c_isa(G)) <=> leq_B(X, G))).
fof(den_ispartof_B, axiom,
    ![X, G]:
      (in_denotation_B(X, c_ispartof(G)) <=> leq_B(X, G))).
fof(den_haspart_B, axiom,
    ![X, G]:
      (in_denotation_B(X, c_haspart(G)) <=> leq_B(G, X))).
% ============================================================
% Forced-emptiness lifted to R_A and R_B
% ============================================================
fof(forced_empty_A_def, axiom,
    ![C1, C2]:
      (forced_empty_A(C1, C2) <=>
       (![X]: ~(in_denotation_A(X, C1) & in_denotation_A(X, C2))))).
fof(forced_empty_B_def, axiom,
    ![C1, C2]:
      (forced_empty_B(C1, C2) <=>
       (![X]: ~(in_denotation_B(X, C1) & in_denotation_B(X, C2))))).
% ============================================================
% Verdict definitions lifted to R_A and R_B
%
% LESSON FROM MONOTONICITY: verdict definitions MUST be one-way
% implications, not biconditionals. Biconditionals plus existentials
% admit Skolem-witness shortcuts that pass inverted-conjecture tests
% spuriously. One-way implications are sufficient for forward proofs
% (Compatible/Conflict derivable from witness/forced-empty) and avoid
% the bug pattern.
% ============================================================
fof(verdict_compatible_intro_A, axiom,
    ![C1, C2, X]:
      ((in_denotation_A(X, C1) & in_denotation_A(X, C2))
       => verdict_compatible_A(C1, C2))).
fof(verdict_conflict_intro_A, axiom,
    ![C1, C2]:
      (forced_empty_A(C1, C2) => verdict_conflict_A(C1, C2))).
fof(verdict_compatible_intro_B, axiom,
    ![C1, C2, X]:
      ((in_denotation_B(X, C1) & in_denotation_B(X, C2))
       => verdict_compatible_B(C1, C2))).
fof(verdict_conflict_intro_B, axiom,
    ![C1, C2]:
      (forced_empty_B(C1, C2) => verdict_conflict_B(C1, C2))).
% ============================================================
% Monotone-operator guard (matches monotonicity audit)
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
% R_A facts (GeoNames slice with grounding for Bayern)
% ============================================================
fof(ra_germany_in_concepts, axiom,
    in_concepts_A(gn_germany)).
fof(ra_bayern_in_concepts, axiom,
    in_concepts_A(gn_bayern)).
fof(ra_bayern_leq_germany, axiom,
    leq_A(gn_bayern, gn_germany)).
fof(ra_bayern_grounded, axiom,
    grounded_as_A(gn_bayern, gn_bayern)).
fof(ra_distinct_germany_bayern, axiom,
    gn_germany != gn_bayern).
% ============================================================
% R_B facts (ISO 3166 slice — grounding will derive via alignment)
% ============================================================
fof(rb_de_in_concepts, axiom,
    in_concepts_B(iso_de)).
fof(rb_de_by_in_concepts, axiom,
    in_concepts_B(iso_de_by)).
fof(rb_de_by_leq_de, axiom,
    leq_B(iso_de_by, iso_de)).
fof(rb_distinct_de_de_by, axiom,
    iso_de != iso_de_by).
% ============================================================
% Cross-resource distinctness
% ============================================================
fof(distinct_gn_iso_1, axiom, gn_germany != iso_de).
fof(distinct_gn_iso_2, axiom, gn_germany != iso_de_by).
fof(distinct_gn_iso_3, axiom, gn_bayern != iso_de).
fof(distinct_gn_iso_4, axiom, gn_bayern != iso_de_by).
% ============================================================
% Alignment α: country and ADM1 levels
% ============================================================
fof(align_germany, axiom,
    align(gn_germany, iso_de)).
fof(align_bayern, axiom,
    align(gn_bayern, iso_de_by)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc901, conjecture,
    verdict_compatible_B(c_ispartof(iso_de), c_eq(iso_de_by))).
%--------------------------------------------------------------------------
