"""
problem_data_alignment.py
=========================
Proposition 2 (alignment) audit: cross-resource verdict preservation
under a partial alignment function α : C_A ⇀ C_B satisfying the four
preservation conditions of Definition 11 (§4.5).

Encoding
--------
Two-resource encoding with `_A` and `_B` predicate suffixes. Predicates
are doubled across R_A and R_B independently, with the alignment
relation `align/2` connecting them.

ALIGN000-0.ax provides 15 alignment axioms:
  - functional, injective (2)
  - dom intro (1)
  - order preservation biconditional (1)
  - disjointness preservation (1)
  - below preservation: domain closure + witness (2)
  - above preservation: domain closure + witness (2)
  - denotation bridge: forward + reverse (2)
  - operator-matching aligned_constraint: eq, isA, isPartOf, hasPart (4)

Problem files emit, in order:
  - include('Axioms/ALIGN000-0.ax')
  - Two-resource lifts of KGE000 + DENOT000 (helper-generated)
  - Inline R_A facts using `_A` predicates
  - Inline R_B facts using `_B` predicates
  - Alignment facts (align/2) for the concrete problem
  - Constraint instantiation
  - Conjecture about R_B verdict

Audit grid (4 problems, realistic GeoNames ↔ ISO 3166)
------------------------------------------------------
KGC900: Conflict transport in aligned subdomain (Prop 2 first case)
        c_ispartof(gn_bayern) ⊥ c_ispartof(gn_ile_de_france) in R_A,
        transports to c_ispartof(iso_de_by) ⊥ c_ispartof(iso_fr_idf).

KGC901: Compatible transport in aligned subdomain
        c_ispartof(gn_germany) compatible with c_eq(gn_bayern) via
        witness gn_bayern; aligned witness iso_de_by transports.

KGC902: Refinement preservation under alignment (Corollary 1)
        c_ispartof(gn_germany) refines c_ispartof(gn_bayern); aligned
        refinement holds in R_B.

KGC910: Lost-concept boundary (Example 11)
        gn_munich is in R_A but not in dom(α); aligned constraint
        for c_eq(gn_munich) cannot be derived. Defensive Unknown.
"""

# ---------------------------------------------------------------------------
# Shared TTL header
# ---------------------------------------------------------------------------
_TTL_PREFIX = """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix gn:   <https://www.geonames.org/ontology#> .
@prefix gnf:  <https://sws.geonames.org/> .
@prefix iso:  <https://www.iso.org/iso/iso3166#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
"""

# ---------------------------------------------------------------------------
# FOF helper: two-resource lifts of KGE000 and DENOT000 for alignment
# (R_A and R_B with _A and _B suffixes, matching ALIGN000)
# ---------------------------------------------------------------------------
def _fof_two_resource_lifts_alignment() -> str:
    """Emit the doubled KGE000 + DENOT000 axioms for R_A and R_B.

    Verdict definitions use one-way implications (Lesson 1 from
    monotonicity audit: biconditionals admit Skolem-witness shortcuts
    that allow inversion-test bugs).
    """
    return """\
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
"""


# ---------------------------------------------------------------------------
# SMT2 helper: parallel SMT theory for R_A and R_B with alignment
# ---------------------------------------------------------------------------
_SMT2_TWO_RESOURCE_PRELUDE_ALIGNMENT = """\
; ============================================================
; Single-sort `Concept`. R_A and R_B membership tracked by
; in_concepts_A/1 and in_concepts_B/1. Alignment relation
; align/2 connects R_A to R_B.
; ============================================================
(declare-sort Concept 0)
(declare-fun in_concepts_A (Concept) Bool)
(declare-fun in_concepts_B (Concept) Bool)
(declare-fun leq_A         (Concept Concept) Bool)
(declare-fun leq_B         (Concept Concept) Bool)
(declare-fun disjoint_A    (Concept Concept) Bool)
(declare-fun disjoint_B    (Concept Concept) Bool)
(declare-fun grounded_as_A (Concept Concept) Bool)
(declare-fun grounded_as_B (Concept Concept) Bool)
(declare-fun align         (Concept Concept) Bool)
(declare-fun align_dom     (Concept) Bool)
; ============================================================
; KGE axioms for R_A and R_B (transitivity, symmetry, propagation)
; ============================================================
(assert (forall ((c Concept)) (leq_A c c)))
(assert (forall ((a Concept) (b Concept) (c Concept))
    (=> (and (leq_A a b) (leq_A b c)) (leq_A a c))))
(assert (forall ((a Concept) (b Concept))
    (=> (disjoint_A a b) (disjoint_A b a))))
(assert (forall ((c Concept)) (not (disjoint_A c c))))
(assert (forall ((a Concept) (b Concept) (z Concept))
    (=> (and (disjoint_A a b) (leq_A z a) (leq_A z b)) false)))
(assert (forall ((c Concept)) (leq_B c c)))
(assert (forall ((a Concept) (b Concept) (c Concept))
    (=> (and (leq_B a b) (leq_B b c)) (leq_B a c))))
(assert (forall ((a Concept) (b Concept))
    (=> (disjoint_B a b) (disjoint_B b a))))
(assert (forall ((c Concept)) (not (disjoint_B c c))))
(assert (forall ((a Concept) (b Concept) (z Concept))
    (=> (and (disjoint_B a b) (leq_B z a) (leq_B z b)) false)))
; ============================================================
; Alignment preservation axioms (subset of ALIGN000 for SMT)
; ============================================================
; Functional
(assert (forall ((c Concept) (d1 Concept) (d2 Concept))
    (=> (and (align c d1) (align c d2)) (= d1 d2))))
; One-to-one (injective)
(assert (forall ((c1 Concept) (c2 Concept) (d Concept))
    (=> (and (align c1 d) (align c2 d)) (= c1 c2))))
; Domain intro (one-way)
(assert (forall ((x Concept) (y Concept))
    (=> (align x y) (align_dom x))))
; Order preservation (biconditional)
(assert (forall ((x Concept) (y Concept) (nux Concept) (nuy Concept))
    (=> (and (align x nux) (align y nuy))
        (= (leq_A x y) (leq_B nux nuy)))))
; Disjointness preservation (one-way)
(assert (forall ((x Concept) (y Concept) (nux Concept) (nuy Concept))
    (=> (and (align x nux) (align y nuy) (disjoint_A x y))
        (disjoint_B nux nuy))))
; Grounding preservation (one-way)
(assert (forall ((c Concept) (nuc Concept) (v Concept))
    (=> (and (align c nuc) (grounded_as_A v c))
        (grounded_as_B v nuc))))
; Below preservation: domain closure
(assert (forall ((g Concept) (ga Concept) (xa Concept))
    (=> (and (align g ga) (leq_A xa g)) (align_dom xa))))
; Below preservation: witness existence
(assert (forall ((g Concept) (ga Concept) (yb Concept))
    (=> (and (align g ga) (leq_B yb ga))
        (exists ((xa Concept)) (and (align xa yb) (leq_A xa g))))))
; Above preservation: domain closure
(assert (forall ((g Concept) (ga Concept) (xa Concept))
    (=> (and (align g ga) (leq_A g xa)) (align_dom xa))))
; Above preservation: witness existence
(assert (forall ((g Concept) (ga Concept) (yb Concept))
    (=> (and (align g ga) (leq_B ga yb))
        (exists ((xa Concept)) (and (align xa yb) (leq_A g xa))))))
"""

def _smt2_two_resource_prelude_alignment() -> str:
    return _SMT2_TWO_RESOURCE_PRELUDE_ALIGNMENT


# ---------------------------------------------------------------------------
# KGC900: Conflict transport in aligned subdomain (Prop 2 first case)
# ---------------------------------------------------------------------------
KGC900 = {
    "id":            "KGC900",
    "subdir":        "Alignment",
    "name":          "Proposition 2: Conflict transport in aligned subdomain [GeoNames ↔ ISO 3166, ADM1]",
    "relation":      "alignment",
    "verdict":       "AlignmentConflict",
    "status_fof":    "Theorem",
    "status_smt":    "unsat",
    "difficulty":    "Hard",
    "includes": [
        "ALIGN000-0.ax",
    ],
    "needs_density": False,

    "description": (
        "Proposition 2 (Verdict under alignment) — first case audit:\n"
        "Conflict on the aligned subdomain transports across the\n"
        "GeoNames ↔ ISO 3166 alignment.\n"
        "\n"
        "Setup uses real-world resource heterogeneity: GeoNames has\n"
        "country and ADM1 levels (PCLI and ADM1 feature codes); ISO\n"
        "3166 has matching ISO 3166-1 (countries) and ISO 3166-2\n"
        "(subdivisions). The aligned subdomain consists of country\n"
        "and ADM1 concepts; cities and the continent have no ISO\n"
        "equivalent and remain outside dom(α).\n"
        "\n"
        "R_A (GeoNames slice):\n"
        "  Concepts: gn_germany, gn_france, gn_bayern,\n"
        "    gn_ile_de_france.\n"
        "  Hierarchy: leq_A(gn_bayern, gn_germany),\n"
        "    leq_A(gn_ile_de_france, gn_france).\n"
        "  Disjointness (SDA): disjoint_A(gn_germany, gn_france).\n"
        "\n"
        "R_B (ISO 3166 slice):\n"
        "  Concepts: iso_de, iso_fr, iso_de_by, iso_fr_idf.\n"
        "  Hierarchy: leq_B(iso_de_by, iso_de),\n"
        "    leq_B(iso_fr_idf, iso_fr).\n"
        "  No direct disjointness — transports via alignment.\n"
        "\n"
        "Alignment α (4 facts):\n"
        "  align(gn_germany, iso_de),\n"
        "  align(gn_france, iso_fr),\n"
        "  align(gn_bayern, iso_de_by),\n"
        "  align(gn_ile_de_france, iso_fr_idf).\n"
        "\n"
        "R_A verdict: verdict_conflict_A on c_ispartof(gn_bayern) and\n"
        "  c_ispartof(gn_ile_de_france). Forced empty because any\n"
        "  shared subordinate would lie below both gn_germany and\n"
        "  gn_france via transitivity, contradicting disjoint_A.\n"
        "\n"
        "Conjecture: verdict_conflict_B(c_ispartof(iso_de_by),\n"
        "  c_ispartof(iso_fr_idf)).\n"
        "Expected: Theorem.\n"
        "\n"
        "Proof chain:\n"
        "  1. align_disjoint_preserving applied to (germany, france)\n"
        "     and aligned pair (iso_de, iso_fr) yields\n"
        "     disjoint_B(iso_de, iso_fr).\n"
        "  2. Asserted leq_B hierarchy plus transitivity propagates\n"
        "     any hypothetical witness up to iso_de and iso_fr.\n"
        "  3. R_B propagation refutes the witness.\n"
        "  4. forced_empty_B(c_ispartof(iso_de_by),\n"
        "     c_ispartof(iso_fr_idf)) derives.\n"
        "  5. verdict_conflict_intro_B yields the conclusion.\n"
        "\n"
        "Load-bearing alignment axioms: align_disjoint_preserving.\n"
        "  align_functional and align_one_to_one are present but may\n"
        "  not appear on the proof critical path; the axiom-coverage\n"
        "  diagnostic confirms which axioms participate.\n"
        "\n"
        "SMT cross-check: hypothetical witness x with\n"
        "  leq_B(x, iso_de_by) and leq_B(x, iso_fr_idf). Alignment-\n"
        "  derived disjoint_B(iso_de, iso_fr) plus B-side propagation\n"
        "  refute. Expected: unsat."
    ),

    "ttl": _TTL_PREFIX + """
drk:offer_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:isPartOf ;
    odrl:rightOperand <https://sws.geonames.org/2951839/>  # Bayern
  ] .
drk:request_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:isPartOf ;
    odrl:rightOperand <https://sws.geonames.org/3012874/>  # Ile-de-France
  ] .
# Proposition 2 Conflict transport at ADM1 level via GeoNames ↔ ISO 3166.
# Both constraints reference concepts in dom(α): the alignment carries
# disjointness from R_A's country level down through the hierarchy.
""",

    "fof_extra_decls": _fof_two_resource_lifts_alignment() + """\
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
""",

    "fof_conjecture":
        "verdict_conflict_B(c_ispartof(iso_de_by), c_ispartof(iso_fr_idf))",

    "smt2_logic": "UF",

    "smt2_decls":
        "; KGC900 SMT cross-check: alignment preserves Conflict at ADM1 level.\n"
        + _smt2_two_resource_prelude_alignment() + """\
; ============================================================
; Concrete constants for KGC900
; ============================================================
(declare-fun gn_germany       () Concept)
(declare-fun gn_france        () Concept)
(declare-fun gn_bayern        () Concept)
(declare-fun gn_ile_de_france () Concept)
(declare-fun iso_de           () Concept)
(declare-fun iso_fr           () Concept)
(declare-fun iso_de_by        () Concept)
(declare-fun iso_fr_idf       () Concept)""",

    "smt2_asserts": """\
; ============================================================
; R_A facts
; ============================================================
(assert (in_concepts_A gn_germany))
(assert (in_concepts_A gn_france))
(assert (in_concepts_A gn_bayern))
(assert (in_concepts_A gn_ile_de_france))
(assert (leq_A gn_bayern gn_germany))
(assert (leq_A gn_ile_de_france gn_france))
(assert (disjoint_A gn_germany gn_france))
; ============================================================
; R_B facts (independent ISO 3166-2 hierarchy)
; ============================================================
(assert (in_concepts_B iso_de))
(assert (in_concepts_B iso_fr))
(assert (in_concepts_B iso_de_by))
(assert (in_concepts_B iso_fr_idf))
(assert (leq_B iso_de_by iso_de))
(assert (leq_B iso_fr_idf iso_fr))
; ============================================================
; Alignment α
; ============================================================
(assert (align gn_germany iso_de))
(assert (align gn_france iso_fr))
(assert (align gn_bayern iso_de_by))
(assert (align gn_ile_de_france iso_fr_idf))
; ============================================================
; Distinctness
; ============================================================
(assert (distinct gn_germany gn_france gn_bayern gn_ile_de_france
                  iso_de iso_fr iso_de_by iso_fr_idf))
; ============================================================
; Witness search: hypothetical x in [c_ispartof(iso_de_by)]_B ∩
; [c_ispartof(iso_fr_idf)]_B. The witness would need to satisfy
; leq_B(x, iso_de_by) and leq_B(x, iso_fr_idf), then via
; transitivity leq_B(x, iso_de) and leq_B(x, iso_fr).
; Alignment-derived disjoint_B(iso_de, iso_fr) plus R_B propagation
; refute. Expected: unsat.
; ============================================================
(declare-fun x () Concept)
(assert (in_concepts_B x))
(assert (leq_B x iso_de_by))
(assert (leq_B x iso_fr_idf))""",
}
KGC910 = {
    "id":            "KGC910",
    "subdir":        "Alignment",
    "name":          "Proposition 2 second case: below-preservation closure on dom(α) [Munich forced]",
    "relation":      "alignment",
    "verdict":       "AlignmentLostBoundary",
    "status_fof":    "Theorem",
    "status_smt":    "unsat",
    "difficulty":    "Hard",
    "includes": [
        "ALIGN000-0.ax",
    ],
    "needs_density": False,

    "description": (
        "Proposition 2 (Verdict under alignment) — second case audit:\n"
        "below-preservation closure of the alignment domain.\n"
        "\n"
        "Setup: a partial alignment that maps gn_bayern → iso_de_by\n"
        "but does NOT explicitly assert align(gn_munich, _). However,\n"
        "gn_munich is below gn_bayern in R_A's hierarchy. Definition\n"
        "11's below-preservation condition requires every concept\n"
        "below an aligned image to be in dom(α). The framework's\n"
        "encoding enforces this via align_downward_domain.\n"
        "\n"
        "R_A (GeoNames slice with city level):\n"
        "  Concepts: gn_germany, gn_bayern, gn_munich.\n"
        "  Hierarchy: leq_A(gn_bayern, gn_germany),\n"
        "    leq_A(gn_munich, gn_bayern).\n"
        "\n"
        "R_B (ISO 3166 slice — no city codes):\n"
        "  Concepts: iso_de, iso_de_by.\n"
        "  Hierarchy: leq_B(iso_de_by, iso_de).\n"
        "\n"
        "Asserted alignment α (no explicit Munich fact):\n"
        "  align(gn_germany, iso_de),\n"
        "  align(gn_bayern, iso_de_by).\n"
        "\n"
        "Conjecture: align_dom(gn_munich).\n"
        "Expected: Theorem.\n"
        "\n"
        "Why: align_downward_domain forces gn_munich into dom(α)\n"
        "  because gn_bayern is aligned and gn_munich is below\n"
        "  gn_bayern. The four preservation conditions of Definition\n"
        "  11 are mutually constraining — you cannot satisfy three\n"
        "  of four. A partial alignment that includes gn_bayern\n"
        "  automatically extends to every concept below gn_bayern.\n"
        "\n"
        "  This is the formal content of Example 11 in §4.5: a\n"
        "  'lost-concept' alignment is not possible if its parent\n"
        "  is included. The framework correctly closes dom(α) under\n"
        "  below-preservation. At the policy level, this manifests\n"
        "  as defensive Unknown verdicts when the consumer's resource\n"
        "  genuinely lacks the necessary granularity: rather than\n"
        "  fabricating an aligned constraint, the system declines.\n"
        "\n"
        "Load-bearing alignment axioms: align_downward_domain.\n"
        "\n"
        "SMT cross-check: assert all R_A, R_B, and alignment facts;\n"
        "  assume ~align_dom(gn_munich); check unsat. The contradiction\n"
        "  follows from the same below-preservation chain.\n"
        "  Expected: unsat."
    ),

    "ttl": _TTL_PREFIX + """
drk:request_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:eq ;
    odrl:rightOperand <https://sws.geonames.org/2867714/>  # Munich (GeoNames)
  ] .
# Proposition 2 second case: GeoNames has city-level granularity (Munich)
# but ISO 3166 stops at the ADM1 level (DE-BY). An attempted partial
# alignment that includes Bayern but excludes Munich is impossible:
# below-preservation forces Munich into dom(α). The framework's encoding
# detects this via align_downward_domain. At the policy level, this
# means consumers using ISO 3166 must accept Unknown verdicts on
# city-level constraints — the framework refuses to fabricate.
""",

    "fof_extra_decls": _fof_two_resource_lifts_alignment() + """\
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
""",

    "fof_conjecture":
        "align_dom(gn_munich)",

    "smt2_logic": "UF",

    "smt2_decls":
        "; KGC910 SMT cross-check: below-preservation forces gn_munich into dom(α).\n"
        + _smt2_two_resource_prelude_alignment() + """\
; ============================================================
; Concrete constants for KGC910
; ============================================================
(declare-fun gn_germany () Concept)
(declare-fun gn_bayern  () Concept)
(declare-fun gn_munich  () Concept)
(declare-fun iso_de     () Concept)
(declare-fun iso_de_by  () Concept)""",

    "smt2_asserts": """\
; ============================================================
; R_A facts (GeoNames with city level)
; ============================================================
(assert (in_concepts_A gn_germany))
(assert (in_concepts_A gn_bayern))
(assert (in_concepts_A gn_munich))
(assert (leq_A gn_bayern gn_germany))
(assert (leq_A gn_munich gn_bayern))
; ============================================================
; R_B facts (ISO 3166 — no city codes)
; ============================================================
(assert (in_concepts_B iso_de))
(assert (in_concepts_B iso_de_by))
(assert (leq_B iso_de_by iso_de))
; ============================================================
; Alignment α (Munich not explicitly aligned)
; ============================================================
(assert (align gn_germany iso_de))
(assert (align gn_bayern iso_de_by))
; ============================================================
; Distinctness
; ============================================================
(assert (distinct gn_germany gn_bayern gn_munich iso_de iso_de_by))
; ============================================================
; Boundary check: assume align_dom(gn_munich) is FALSE.
; align_downward_domain forces a contradiction because gn_bayern
; is aligned and gn_munich is below gn_bayern. Expected: unsat.
; ============================================================
(assert (not (align_dom gn_munich)))""",
}


# ---------------------------------------------------------------------------
# KGC901: Compatible transport in aligned subdomain
# ---------------------------------------------------------------------------
KGC901 = {
    "id":            "KGC901",
    "subdir":        "Alignment",
    "name":          "Proposition 2: Compatible transport in aligned subdomain [GeoNames ↔ ISO 3166]",
    "relation":      "alignment",
    "verdict":       "AlignmentCompatible",
    "status_fof":    "Theorem",
    "status_smt":    "sat",
    "difficulty":    "Hard",
    "includes": [
        "ALIGN000-0.ax",
    ],
    "needs_density": False,

    "description": (
        "Proposition 2 (Verdict under alignment) — first case audit:\n"
        "Compatible transports across the GeoNames ↔ ISO 3166\n"
        "alignment via witness construction.\n"
        "\n"
        "This is the dual of KGC900: where KGC900 transports Conflict\n"
        "via disjointness preservation, KGC901 transports Compatible\n"
        "via grounding preservation and order preservation. The R_A\n"
        "witness gn_bayern transports to R_B as iso_de_by through\n"
        "the alignment.\n"
        "\n"
        "R_A (GeoNames slice):\n"
        "  Concepts: gn_germany, gn_bayern.\n"
        "  Hierarchy: leq_A(gn_bayern, gn_germany).\n"
        "  Grounding: grounded_as_A(gn_bayern, gn_bayern).\n"
        "\n"
        "R_B (ISO 3166 slice):\n"
        "  Concepts: iso_de, iso_de_by.\n"
        "  Hierarchy: leq_B(iso_de_by, iso_de).\n"
        "  No direct grounding asserted — transports via alignment.\n"
        "\n"
        "Alignment α (2 facts):\n"
        "  align(gn_germany, iso_de),\n"
        "  align(gn_bayern, iso_de_by).\n"
        "\n"
        "R_A constraints:\n"
        "  c1 = c_ispartof(gn_germany)  -- Bayern is part of Germany\n"
        "  c2 = c_eq(gn_bayern)         -- exactly Bayern\n"
        "  R_A verdict: verdict_compatible_A. Witness gn_bayern is in\n"
        "    both denotations: leq_A(gn_bayern, gn_germany) puts it\n"
        "    in [c1]_A; grounded_as_A(gn_bayern, gn_bayern) puts it\n"
        "    in [c2]_A.\n"
        "\n"
        "R_B aligned constraints (via operator-matching axioms):\n"
        "  c1' = c_ispartof(iso_de),\n"
        "  c2' = c_eq(iso_de_by).\n"
        "\n"
        "Conjecture (Style B): verdict_compatible_B(c_ispartof(iso_de),\n"
        "  c_eq(iso_de_by)).\n"
        "Expected: Theorem.\n"
        "\n"
        "Why: align_grounding_preservation applied to\n"
        "  grounded_as_A(gn_bayern, gn_bayern) and\n"
        "  align(gn_bayern, iso_de_by) yields\n"
        "  grounded_as_B(gn_bayern, iso_de_by). By den_eq_B, this puts\n"
        "  gn_bayern into [c_eq(iso_de_by)]_B. The asserted\n"
        "  leq_B(iso_de_by, iso_de), combined with reflexivity\n"
        "  (or directly: gn_bayern grounded as iso_de_by, leq_B\n"
        "  iso_de_by iso_de), establishes gn_bayern in\n"
        "  [c_ispartof(iso_de)]_B. Both denotations contain a witness;\n"
        "  verdict_compatible_intro_B fires.\n"
        "\n"
        "  Note: the witness in R_B is gn_bayern (same constant), but\n"
        "  via grounded_as_B(gn_bayern, iso_de_by) it represents the\n"
        "  ISO 3166 concept iso_de_by. This is how cross-resource\n"
        "  witness transport works: the value (gn_bayern) has\n"
        "  different groundings in the two resources.\n"
        "\n"
        "Load-bearing alignment axioms: align_grounding_preservation\n"
        "  (transports the eq witness across resources).\n"
        "\n"
        "SMT cross-check: assert all R_A, R_B, and alignment facts;\n"
        "  check satisfiability with witness gn_bayern in both\n"
        "  R_B-denotations. Expected: sat. Z3 should construct a model\n"
        "  with gn_bayern as the witness; cvc5 may return unknown\n"
        "  due to known limitations on quantifier instantiation for\n"
        "  Compatible-class problems."
    ),

    "ttl": _TTL_PREFIX + """
drk:offer_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:isPartOf ;
    odrl:rightOperand <https://sws.geonames.org/2921044/>  # Germany
  ] .
drk:request_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:eq ;
    odrl:rightOperand <https://sws.geonames.org/2951839/>  # Bayern
  ] .
# Proposition 2 Compatible transport: Bayern is part of Germany in
# GeoNames; under alignment, the witness transports to ISO 3166 with
# iso_de_by serving as the aligned image. The grounding preservation
# axiom is load-bearing.
""",

    "fof_extra_decls": _fof_two_resource_lifts_alignment() + """\
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
""",

    "fof_conjecture":
        "verdict_compatible_B(c_ispartof(iso_de), c_eq(iso_de_by))",

    "smt2_logic": "UF",

    "smt2_decls":
        "; KGC901 SMT cross-check: alignment preserves Compatible via grounding transport.\n"
        + _smt2_two_resource_prelude_alignment() + """\
; ============================================================
; Concrete constants for KGC901
; ============================================================
(declare-fun gn_germany () Concept)
(declare-fun gn_bayern  () Concept)
(declare-fun iso_de     () Concept)
(declare-fun iso_de_by  () Concept)""",

    "smt2_asserts": """\
; ============================================================
; R_A facts
; ============================================================
(assert (in_concepts_A gn_germany))
(assert (in_concepts_A gn_bayern))
(assert (leq_A gn_bayern gn_germany))
(assert (grounded_as_A gn_bayern gn_bayern))
; ============================================================
; R_B facts
; ============================================================
(assert (in_concepts_B iso_de))
(assert (in_concepts_B iso_de_by))
(assert (leq_B iso_de_by iso_de))
; ============================================================
; Alignment α
; ============================================================
(assert (align gn_germany iso_de))
(assert (align gn_bayern iso_de_by))
; ============================================================
; Distinctness
; ============================================================
(assert (distinct gn_germany gn_bayern iso_de iso_de_by))
; ============================================================
; Witness check: gn_bayern should be in both R_B-denotations.
; [c_ispartof(iso_de)]_B contains gn_bayern via leq_B (assuming
; grounding preservation gives leq_B from align_order_preserving).
; [c_eq(iso_de_by)]_B contains gn_bayern via grounded_as_B from
; alignment. The model should be satisfiable with gn_bayern as
; the witness.
; ============================================================
(declare-fun x () Concept)
(assert (= x gn_bayern))
(assert (leq_B x iso_de))
(assert (grounded_as_B x iso_de_by))""",
}


# ---------------------------------------------------------------------------
# KGC902: Refinement preservation under alignment (Corollary 1)
# ---------------------------------------------------------------------------
KGC902 = {
    "id":            "KGC902",
    "subdir":        "Alignment",
    "name":          "Corollary 1: Refinement preservation under alignment [GeoNames ↔ ISO 3166]",
    "relation":      "alignment",
    "verdict":       "AlignmentRefinement",
    "status_fof":    "Theorem",
    "status_smt":    "unsat",
    "difficulty":    "Hard",
    "includes": [
        "ALIGN000-0.ax",
    ],
    "needs_density": False,

    "description": (
        "Corollary 1 (Refinement preservation under alignment) audit:\n"
        "if c1 refines c2 in R_A and both grounded concepts are in\n"
        "dom(α), then the aligned constraints c1' refines c2' in R_B.\n"
        "\n"
        "Refinement: c_ispartof(g1) refines c_ispartof(g2) iff every\n"
        "concept in [c_ispartof(g1)] is also in [c_ispartof(g2)],\n"
        "i.e., leq(g1, g2). In R_A: leq_A(gn_bayern, gn_germany)\n"
        "establishes that c_ispartof(gn_bayern) refines\n"
        "c_ispartof(gn_germany).\n"
        "\n"
        "Setup: To make alignment load-bearing for this audit, R_B's\n"
        "hierarchy is NOT asserted directly. Instead, the aligned\n"
        "leq_B(iso_de_by, iso_de) is derived from R_A's hierarchy via\n"
        "align_order_preserving (the biconditional that order in R_A\n"
        "carries to order in R_B for aligned pairs).\n"
        "\n"
        "R_A (GeoNames):\n"
        "  Concepts: gn_germany, gn_bayern.\n"
        "  Hierarchy: leq_A(gn_bayern, gn_germany).\n"
        "\n"
        "R_B (ISO 3166 — hierarchy NOT directly asserted):\n"
        "  Concepts: iso_de, iso_de_by.\n"
        "  No leq_B fact asserted directly.\n"
        "\n"
        "Alignment α:\n"
        "  align(gn_germany, iso_de),\n"
        "  align(gn_bayern, iso_de_by).\n"
        "\n"
        "Conjecture: ![X]: (in_denotation_B(X, c_ispartof(iso_de_by))\n"
        "  => in_denotation_B(X, c_ispartof(iso_de))).\n"
        "Expected: Theorem.\n"
        "\n"
        "Why: align_order_preserving applied to (gn_bayern, gn_germany,\n"
        "  iso_de_by, iso_de) plus leq_A(gn_bayern, gn_germany) yields\n"
        "  leq_B(iso_de_by, iso_de). Combined with R_B transitivity:\n"
        "  for any X with leq_B(X, iso_de_by), we have leq_B(X, iso_de)\n"
        "  via transitivity. By den_ispartof_B, X in\n"
        "  [c_ispartof(iso_de_by)]_B implies X in\n"
        "  [c_ispartof(iso_de)]_B.\n"
        "\n"
        "  This audit demonstrates that order preservation is load-\n"
        "  bearing: R_B's hierarchy isn't asserted, only the\n"
        "  alignment is. Without align_order_preserving, the proof\n"
        "  would not go through.\n"
        "\n"
        "Load-bearing alignment axioms: align_order_preserving.\n"
        "\n"
        "SMT cross-check: assert R_A and alignment, assume a witness\n"
        "  in [c_ispartof(iso_de_by)]_B but not in [c_ispartof(iso_de)]_B;\n"
        "  the alignment-derived leq_B plus transitivity refute.\n"
        "  Expected: unsat."
    ),

    "ttl": _TTL_PREFIX + """
drk:offer_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:isPartOf ;
    odrl:rightOperand <https://sws.geonames.org/2921044/>  # Germany
  ] .
drk:request_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:isPartOf ;
    odrl:rightOperand <https://sws.geonames.org/2951839/>  # Bayern
  ] .
# Corollary 1: Refinement c_ispartof(gn_bayern) refines c_ispartof(gn_germany)
# in R_A; alignment transports refinement to R_B via order preservation.
""",

    "fof_extra_decls": _fof_two_resource_lifts_alignment() + """\
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
""",

    "fof_conjecture":
        "![X]: (in_denotation_B(X, c_ispartof(iso_de_by)) "
        "=> in_denotation_B(X, c_ispartof(iso_de)))",

    "smt2_logic": "UF",

    "smt2_decls":
        "; KGC902 SMT cross-check: refinement preservation under alignment.\n"
        + _smt2_two_resource_prelude_alignment() + """\
; ============================================================
; Concrete constants for KGC902
; ============================================================
(declare-fun gn_germany () Concept)
(declare-fun gn_bayern  () Concept)
(declare-fun iso_de     () Concept)
(declare-fun iso_de_by  () Concept)""",

    "smt2_asserts": """\
; ============================================================
; R_A facts (only GeoNames hierarchy)
; ============================================================
(assert (in_concepts_A gn_germany))
(assert (in_concepts_A gn_bayern))
(assert (leq_A gn_bayern gn_germany))
; ============================================================
; R_B facts (NO hierarchy — derives via alignment)
; ============================================================
(assert (in_concepts_B iso_de))
(assert (in_concepts_B iso_de_by))
; ============================================================
; Alignment α
; ============================================================
(assert (align gn_germany iso_de))
(assert (align gn_bayern iso_de_by))
; ============================================================
; Distinctness
; ============================================================
(assert (distinct gn_germany gn_bayern iso_de iso_de_by))
; ============================================================
; Refinement check: hypothetical witness x in [c_ispartof(iso_de_by)]_B
; but NOT in [c_ispartof(iso_de)]_B. By den_ispartof_B, this means
; leq_B(x, iso_de_by) but ~leq_B(x, iso_de). The alignment-derived
; leq_B(iso_de_by, iso_de) plus R_B transitivity refute.
; Expected: unsat.
; ============================================================
(declare-fun x () Concept)
(assert (leq_B x iso_de_by))
(assert (not (leq_B x iso_de)))""",
}


PROBLEMS = [KGC900, KGC901, KGC902, KGC910]