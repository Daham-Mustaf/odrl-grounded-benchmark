%--------------------------------------------------------------------------
% File     : KGC902-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : Corollary 1: Refinement preservation under alignment [GeoNames ↔ ISO 3166]
% Version  : 1.0
% English  : Corollary 1 (Refinement preservation under alignment) audit:
%           : if c1 refines c2 in R_A and both grounded concepts are in
%           : dom(α), then the aligned constraints c1' refines c2' in R_B.
%           : 
%           : Refinement: c_ispartof(g1) refines c_ispartof(g2) iff every
%           : concept in [c_ispartof(g1)] is also in [c_ispartof(g2)],
%           : i.e., leq(g1, g2). In R_A: leq_A(gn_bayern, gn_germany)
%           : establishes that c_ispartof(gn_bayern) refines
%           : c_ispartof(gn_germany).
%           : 
%           : Setup: To make alignment load-bearing for this audit, R_B's
%           : hierarchy is NOT asserted directly. Instead, the aligned
%           : leq_B(iso_de_by, iso_de) is derived from R_A's hierarchy via
%           : align_order_preserving (the biconditional that order in R_A
%           : carries to order in R_B for aligned pairs).
%           : 
%           : R_A (GeoNames):
%           : Concepts: gn_germany, gn_bayern.
%           : Hierarchy: leq_A(gn_bayern, gn_germany).
%           : 
%           : R_B (ISO 3166 — hierarchy NOT directly asserted):
%           : Concepts: iso_de, iso_de_by.
%           : No leq_B fact asserted directly.
%           : 
%           : Alignment α:
%           : align(gn_germany, iso_de),
%           : align(gn_bayern, iso_de_by).
%           : 
%           : Conjecture: ![X]: (in_denotation_B(X, c_ispartof(iso_de_by))
%           : => in_denotation_B(X, c_ispartof(iso_de))).
%           : Expected: Theorem.
%           : 
%           : Why: align_order_preserving applied to (gn_bayern, gn_germany,
%           : iso_de_by, iso_de) plus leq_A(gn_bayern, gn_germany) yields
%           : leq_B(iso_de_by, iso_de). Combined with R_B transitivity:
%           : for any X with leq_B(X, iso_de_by), we have leq_B(X, iso_de)
%           : via transitivity. By den_ispartof_B, X in
%           : [c_ispartof(iso_de_by)]_B implies X in
%           : [c_ispartof(iso_de)]_B.
%           : 
%           : This audit demonstrates that order preservation is load-
%           : bearing: R_B's hierarchy isn't asserted, only the
%           : alignment is. Without align_order_preserving, the proof
%           : would not go through.
%           : 
%           : Load-bearing alignment axioms: align_order_preserving.
%           : 
%           : SMT cross-check: assert R_A and alignment, assume a witness
%           : in [c_ispartof(iso_de_by)]_B but not in [c_ispartof(iso_de)]_B;
%           : the alignment-derived leq_B plus transitivity refute.
%           : Expected: unsat.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC902-1.p
%
% Status   : Theorem
% Verdict  : AlignmentRefinement
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC902-policy.ttl
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
% R_A facts (GeoNames hierarchy)
% ============================================================
fof(ra_germany_in_concepts, axiom,
    in_concepts_A(gn_germany)).
fof(ra_bayern_in_concepts, axiom,
    in_concepts_A(gn_bayern)).
fof(ra_bayern_leq_germany, axiom,
    leq_A(gn_bayern, gn_germany)).
fof(ra_distinct_germany_bayern, axiom,
    gn_germany != gn_bayern).
% ============================================================
% R_B facts: NO hierarchy asserted directly. R_B's leq_B
% relations must be derived from alignment + R_A hierarchy via
% align_order_preserving.
% ============================================================
fof(rb_de_in_concepts, axiom,
    in_concepts_B(iso_de)).
fof(rb_de_by_in_concepts, axiom,
    in_concepts_B(iso_de_by)).
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
% Alignment α
% ============================================================
fof(align_germany, axiom,
    align(gn_germany, iso_de)).
fof(align_bayern, axiom,
    align(gn_bayern, iso_de_by)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc902, conjecture,
    ![X]: (in_denotation_B(X, c_ispartof(iso_de_by)) => in_denotation_B(X, c_ispartof(iso_de)))).
%--------------------------------------------------------------------------
