%--------------------------------------------------------------------------
% File     : KGC900-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : Proposition 2: Conflict transport in aligned subdomain [GeoNames ↔ ISO 3166, ADM1]
% Version  : 1.0
% English  : Proposition 2 (Verdict under alignment) — first case audit:
%           : Conflict on the aligned subdomain transports across the
%           : GeoNames ↔ ISO 3166 alignment.
%           : 
%           : Setup uses real-world resource heterogeneity: GeoNames has
%           : country and ADM1 levels (PCLI and ADM1 feature codes); ISO
%           : 3166 has matching ISO 3166-1 (countries) and ISO 3166-2
%           : (subdivisions). The aligned subdomain consists of country
%           : and ADM1 concepts; cities and the continent have no ISO
%           : equivalent and remain outside dom(α).
%           : 
%           : R_A (GeoNames slice):
%           : Concepts: gn_germany, gn_france, gn_bayern,
%           : gn_ile_de_france.
%           : Hierarchy: leq_A(gn_bayern, gn_germany),
%           : leq_A(gn_ile_de_france, gn_france).
%           : Disjointness (SDA): disjoint_A(gn_germany, gn_france).
%           : 
%           : R_B (ISO 3166 slice):
%           : Concepts: iso_de, iso_fr, iso_de_by, iso_fr_idf.
%           : Hierarchy: leq_B(iso_de_by, iso_de),
%           : leq_B(iso_fr_idf, iso_fr).
%           : No direct disjointness — transports via alignment.
%           : 
%           : Alignment α (4 facts):
%           : align(gn_germany, iso_de),
%           : align(gn_france, iso_fr),
%           : align(gn_bayern, iso_de_by),
%           : align(gn_ile_de_france, iso_fr_idf).
%           : 
%           : R_A verdict: verdict_conflict_A on c_ispartof(gn_bayern) and
%           : c_ispartof(gn_ile_de_france). Forced empty because any
%           : shared subordinate would lie below both gn_germany and
%           : gn_france via transitivity, contradicting disjoint_A.
%           : 
%           : Conjecture: verdict_conflict_B(c_ispartof(iso_de_by),
%           : c_ispartof(iso_fr_idf)).
%           : Expected: Theorem.
%           : 
%           : Proof chain:
%           : 1. align_disjoint_preserving applied to (germany, france)
%           : and aligned pair (iso_de, iso_fr) yields
%           : disjoint_B(iso_de, iso_fr).
%           : 2. Asserted leq_B hierarchy plus transitivity propagates
%           : any hypothetical witness up to iso_de and iso_fr.
%           : 3. R_B propagation refutes the witness.
%           : 4. forced_empty_B(c_ispartof(iso_de_by),
%           : c_ispartof(iso_fr_idf)) derives.
%           : 5. verdict_conflict_intro_B yields the conclusion.
%           : 
%           : Load-bearing alignment axioms: align_disjoint_preserving.
%           : align_functional and align_one_to_one are present but may
%           : not appear on the proof critical path; the axiom-coverage
%           : diagnostic confirms which axioms participate.
%           : 
%           : SMT cross-check: hypothetical witness x with
%           : leq_B(x, iso_de_by) and leq_B(x, iso_fr_idf). Alignment-
%           : derived disjoint_B(iso_de, iso_fr) plus B-side propagation
%           : refute. Expected: unsat.
%
% Refs     : ()
% Source   : 
% Authors  : 
% Names    : KGC900-1.p
%
% Status   : Theorem
% Verdict  : AlignmentConflict
% SPC      : FOF_THM_RFN
%
% Comments : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC900-policy.ttl
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
% R_A facts (GeoNames, ADM1 level)
% ============================================================
fof(ra_germany_in_concepts, axiom,
    in_concepts_A(gn_germany)).
fof(ra_france_in_concepts, axiom,
    in_concepts_A(gn_france)).
fof(ra_bayern_in_concepts, axiom,
    in_concepts_A(gn_bayern)).
fof(ra_idf_in_concepts, axiom,
    in_concepts_A(gn_ile_de_france)).
fof(ra_bayern_leq_germany, axiom,
    leq_A(gn_bayern, gn_germany)).
fof(ra_idf_leq_france, axiom,
    leq_A(gn_ile_de_france, gn_france)).
fof(ra_germany_disjoint_france, axiom,
    disjoint_A(gn_germany, gn_france)).
fof(ra_distinct_germany_france, axiom,
    gn_germany != gn_france).
fof(ra_distinct_bayern_idf, axiom,
    gn_bayern != gn_ile_de_france).
fof(ra_distinct_bayern_germany, axiom,
    gn_bayern != gn_germany).
fof(ra_distinct_idf_france, axiom,
    gn_ile_de_france != gn_france).
% ============================================================
% R_B facts (ISO 3166, ADM1 level — independently asserted hierarchy)
% ============================================================
fof(rb_de_in_concepts, axiom,
    in_concepts_B(iso_de)).
fof(rb_fr_in_concepts, axiom,
    in_concepts_B(iso_fr)).
fof(rb_de_by_in_concepts, axiom,
    in_concepts_B(iso_de_by)).
fof(rb_fr_idf_in_concepts, axiom,
    in_concepts_B(iso_fr_idf)).
fof(rb_de_by_leq_de, axiom,
    leq_B(iso_de_by, iso_de)).
fof(rb_fr_idf_leq_fr, axiom,
    leq_B(iso_fr_idf, iso_fr)).
fof(rb_distinct_de_fr, axiom,
    iso_de != iso_fr).
fof(rb_distinct_de_by_fr_idf, axiom,
    iso_de_by != iso_fr_idf).
fof(rb_distinct_de_by_de, axiom,
    iso_de_by != iso_de).
fof(rb_distinct_fr_idf_fr, axiom,
    iso_fr_idf != iso_fr).
% ============================================================
% Cross-resource distinctness (no GeoNames concept = ISO concept)
% ============================================================
fof(distinct_gn_iso_1, axiom, gn_germany != iso_de).
fof(distinct_gn_iso_2, axiom, gn_germany != iso_fr).
fof(distinct_gn_iso_3, axiom, gn_france != iso_de).
fof(distinct_gn_iso_4, axiom, gn_france != iso_fr).
fof(distinct_gn_iso_5, axiom, gn_bayern != iso_de_by).
fof(distinct_gn_iso_6, axiom, gn_ile_de_france != iso_fr_idf).
% ============================================================
% Alignment α: 4 facts on the aligned subdomain
% (countries + ADM1 level)
% ============================================================
fof(align_germany, axiom,
    align(gn_germany, iso_de)).
fof(align_france, axiom,
    align(gn_france, iso_fr)).
fof(align_bayern, axiom,
    align(gn_bayern, iso_de_by)).
fof(align_idf, axiom,
    align(gn_ile_de_france, iso_fr_idf)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc900, conjecture,
    verdict_conflict_B(c_ispartof(iso_de_by), c_ispartof(iso_fr_idf))).
%--------------------------------------------------------------------------
