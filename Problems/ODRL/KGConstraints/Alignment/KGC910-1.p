%--------------------------------------------------------------------------
% File     : KGC910-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : Proposition 2 second case: below-preservation closure on dom(α) [Munich forced]
% Version  : 1.0
% English  : Proposition 2 (Verdict under alignment) — second case audit:
%           : below-preservation closure of the alignment domain.
%           : 
%           : Setup: a partial alignment that maps gn_bayern → iso_de_by
%           : but does NOT explicitly assert align(gn_munich, _). However,
%           : gn_munich is below gn_bayern in R_A's hierarchy. Definition
%           : 11's below-preservation condition requires every concept
%           : below an aligned image to be in dom(α). The framework's
%           : encoding enforces this via align_downward_domain.
%           : 
%           : R_A (GeoNames slice with city level):
%           : Concepts: gn_germany, gn_bayern, gn_munich.
%           : Hierarchy: leq_A(gn_bayern, gn_germany),
%           : leq_A(gn_munich, gn_bayern).
%           : 
%           : R_B (ISO 3166 slice — no city codes):
%           : Concepts: iso_de, iso_de_by.
%           : Hierarchy: leq_B(iso_de_by, iso_de).
%           : 
%           : Asserted alignment α (no explicit Munich fact):
%           : align(gn_germany, iso_de),
%           : align(gn_bayern, iso_de_by).
%           : 
%           : Conjecture: align_dom(gn_munich).
%           : Expected: Theorem.
%           : 
%           : Why: align_downward_domain forces gn_munich into dom(α)
%           : because gn_bayern is aligned and gn_munich is below
%           : gn_bayern. The four preservation conditions of Definition
%           : 11 are mutually constraining — you cannot satisfy three
%           : of four. A partial alignment that includes gn_bayern
%           : automatically extends to every concept below gn_bayern.
%           : 
%           : This is the formal content of Example 11 in §4.5: a
%           : 'lost-concept' alignment is not possible if its parent
%           : is included. The framework correctly closes dom(α) under
%           : below-preservation. At the policy level, this manifests
%           : as defensive Unknown verdicts when the consumer's resource
%           : genuinely lacks the necessary granularity: rather than
%           : fabricating an aligned constraint, the system declines.
%           : 
%           : Load-bearing alignment axioms: align_downward_domain.
%           : 
%           : SMT cross-check: assert all R_A, R_B, and alignment facts;
%           : assume ~align_dom(gn_munich); check unsat. The contradiction
%           : follows from the same below-preservation chain.
%           : Expected: unsat.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC910-1.p
%
% Status   : Theorem
% Verdict  : AlignmentLostBoundary
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC910-policy.ttl
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
% R_A facts (GeoNames slice with city level)
% ============================================================
fof(ra_germany_in_concepts, axiom,
    in_concepts_A(gn_germany)).
fof(ra_bayern_in_concepts, axiom,
    in_concepts_A(gn_bayern)).
fof(ra_munich_in_concepts, axiom,
    in_concepts_A(gn_munich)).
fof(ra_bayern_leq_germany, axiom,
    leq_A(gn_bayern, gn_germany)).
fof(ra_munich_leq_bayern, axiom,
    leq_A(gn_munich, gn_bayern)).
fof(ra_distinct_germany_bayern, axiom,
    gn_germany != gn_bayern).
fof(ra_distinct_bayern_munich, axiom,
    gn_bayern != gn_munich).
fof(ra_distinct_germany_munich, axiom,
    gn_germany != gn_munich).
% ============================================================
% R_B facts (ISO 3166 slice — no city codes)
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
fof(distinct_gn_iso_2, axiom, gn_bayern != iso_de_by).
fof(distinct_gn_iso_3, axiom, gn_munich != iso_de).
fof(distinct_gn_iso_4, axiom, gn_munich != iso_de_by).
% ============================================================
% Alignment α (no explicit fact for gn_munich)
% Below-preservation will force gn_munich into dom(α).
% ============================================================
fof(align_germany, axiom,
    align(gn_germany, iso_de)).
fof(align_bayern, axiom,
    align(gn_bayern, iso_de_by)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc910, conjecture,
    align_dom(gn_munich)).
%--------------------------------------------------------------------------
