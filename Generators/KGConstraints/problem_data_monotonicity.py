"""
problem_data_monotonicity.py
=============================
Proposition 1 (Monotonicity) audit: verdict and denotation preservation
under resource extension.

The framework's Proposition 1 (paper Section 4.2) states that resource
extension along the four dimensions (concepts, leq, disjointness,
grounding) preserves monotone-operator verdicts. This module audits the
preservation claim using a two-resource encoding.

Encoding strategy
-----------------
Predicates are doubled: the original resource R uses suffix `_R`, the
extended resource R' uses suffix `_R_prime`. MONO000-0.ax provides the
four extension-closure axioms:

    in_concepts_R(x)         => in_concepts_R_prime(x)
    leq_R(x, y)              => leq_R_prime(x, y)
    disjoint_R(x, y)         => disjoint_R_prime(x, y)
    grounded_as_R(c, g)      => grounded_as_R_prime(c, g)

Problem files emit, in order:
  - include('Axioms/MONO000-0.ax')  [extension-closure axioms]
  - Two-resource lifts of KGE000 + DENOT000 (helper-generated boilerplate)
  - Inline R-facts using `_R` predicates
  - Inline R'-only facts using `_R_prime` predicates
  - Constraint instantiation with monotone_op/1 guards
  - Conjecture about verdict or denotation preservation

The closure axioms in MONO000 lift R-facts to R' automatically, so
problem files only assert R-facts in `_R` form and R'-only new facts
in `_R_prime` form.

Grid
----------
Three extension dimensions x three claim shapes = 9 core problems:

    | Extension type     | Conflict | Compatible | Denotation |
    | concept addition   | KGC800   | KGC803     | KGC806     |
    | edge addition      | KGC801   | KGC804     | KGC807     |
    | disjointness add   | KGC802   | KGC805     | KGC808     |

Plus 3 boundary cases:
    KGC810: complement counterexample (Remark 2)
    KGC811: retraction counterexample (Remark 3)
    KGC812: Assumption 1 violation

SMT side
--------
Each problem includes an SMT2 cross-check using Shape B (witness
preservation / witness flip), with single-sort `Concept` plus
`in_concepts_R/1` and `in_concepts_R_prime/1` membership predicates.

Conflict-preservation: hypothetical witness contradicted by propagation
(expect unsat). Compatible-preservation: R-witness survives in R'
(expect sat). Denotation growth: assert x in [c]_R and x not in [c]_R'
(expect unsat via closure).

Problem-specific TPTP and SMT2 are inline; helper functions emit the
shared two-resource boilerplate.
"""

# ---------------------------------------------------------------------------
# Shared TTL header
# ---------------------------------------------------------------------------
_TTL_PREFIX = """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix bcp:  <https://tools.ietf.org/html/bcp47#> .
@prefix dpv:  <https://w3id.org/dpv#> .
@prefix gn:   <https://www.geonames.org/ontology#> .
@prefix gnf:  <https://sws.geonames.org/> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
"""


# ---------------------------------------------------------------------------
# FOF helper: two-resource lifts of KGE000 and DENOT000
# ---------------------------------------------------------------------------

def _fof_two_resource_lifts() -> str:
    """Emit the doubled KGE000 + DENOT000 axioms (R and R' versions).
    
    These are problem-local because the extension-closure axioms in
    MONO000-0.ax presume `_R` and `_R_prime` predicates that are not
    part of the standard KGE000/DENOT000 vocabulary.
    """
    return """\
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
% Excludes neq and isNoneOf; their denotations C \\ {g} are not
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
"""


# ---------------------------------------------------------------------------
# SMT2 helper: parallel SMT theory for R and R' (single-sort)
# ---------------------------------------------------------------------------

_SMT2_TWO_RESOURCE_PRELUDE = """\
; ============================================================
; Single-sort `Concept`. Membership in R and R' tracked by
; in_concepts_R/1 and in_concepts_R_prime/1.
; ============================================================
(declare-sort Concept 0)
(declare-fun in_concepts_R       (Concept) Bool)
(declare-fun in_concepts_R_prime (Concept) Bool)
(declare-fun leq_R               (Concept Concept) Bool)
(declare-fun leq_R_prime         (Concept Concept) Bool)
(declare-fun disjoint_R          (Concept Concept) Bool)
(declare-fun disjoint_R_prime    (Concept Concept) Bool)

; ============================================================
; KGE000 axioms (R and R')
; ============================================================
(assert (forall ((c Concept)) (leq_R c c)))
(assert (forall ((a Concept) (b Concept) (c Concept))
    (=> (and (leq_R a b) (leq_R b c)) (leq_R a c))))
(assert (forall ((a Concept) (b Concept))
    (=> (disjoint_R a b) (disjoint_R b a))))
(assert (forall ((c Concept)) (not (disjoint_R c c))))
(assert (forall ((a Concept) (b Concept) (z Concept))
    (=> (and (disjoint_R a b) (leq_R z a) (leq_R z b))
        false)))

(assert (forall ((c Concept)) (leq_R_prime c c)))
(assert (forall ((a Concept) (b Concept) (c Concept))
    (=> (and (leq_R_prime a b) (leq_R_prime b c)) (leq_R_prime a c))))
(assert (forall ((a Concept) (b Concept))
    (=> (disjoint_R_prime a b) (disjoint_R_prime b a))))
(assert (forall ((c Concept)) (not (disjoint_R_prime c c))))
(assert (forall ((a Concept) (b Concept) (z Concept))
    (=> (and (disjoint_R_prime a b) (leq_R_prime z a) (leq_R_prime z b))
        false)))

; ============================================================
; MONO000 closure axioms: R-facts propagate to R'
; ============================================================
(assert (forall ((c Concept))
    (=> (in_concepts_R c) (in_concepts_R_prime c))))
(assert (forall ((a Concept) (b Concept))
    (=> (leq_R a b) (leq_R_prime a b))))
(assert (forall ((a Concept) (b Concept))
    (=> (disjoint_R a b) (disjoint_R_prime a b))))
"""


def _smt2_two_resource_prelude() -> str:
    """Emit the standard two-resource SMT prelude (sort, predicates,
    KGE axioms, MONO closure)."""
    return _SMT2_TWO_RESOURCE_PRELUDE


# ---------------------------------------------------------------------------
# KGC800: concept addition + Conflict preservation
# ---------------------------------------------------------------------------

KGC800 = {
    "id":            "KGC800",
    "subdir":        "Monotonicity",
    "name":          "Proposition 1: Conflict preservation under concept addition [GeoNames-like]",
    "relation":      "monotonicity",
    "verdict":       "MonotonicityConflict",
    "status_fof":    "Theorem",
    "status_smt":    "unsat",
    "difficulty":    "Hard",
    "includes":      [
        "MONO000-0.ax",
    ],
    "needs_density": False,
    "description": (
        "Proposition 1 (Monotonicity) audit: Conflict preservation\n"
        "under concept addition.\n"
        "\n"
        "Setup:\n"
        "  R: GeoNames-shaped flat registry with two disjoint regions.\n"
        "    in_concepts_R(gn_germany), in_concepts_R(gn_france).\n"
        "    disjoint_R(gn_germany, gn_france).\n"
        "  Constraints:\n"
        "    c1 = c_ispartof(gn_germany)  [denotation: leq_R(., gn_germany)]\n"
        "    c2 = c_ispartof(gn_france)   [denotation: leq_R(., gn_france)]\n"
        "  R-verdict: verdict_conflict_R(c1, c2) holds. Witness search\n"
        "    fails because disjoint_R(gn_germany, gn_france) plus\n"
        "    propagation forces no shared subordinate.\n"
        "\n"
        "Extension R':\n"
        "  Add concept gn_spain with its own disjointness facts:\n"
        "    in_concepts_R_prime(gn_spain) and not in_concepts_R(gn_spain)\n"
        "    disjoint_R_prime(gn_spain, gn_germany)\n"
        "    disjoint_R_prime(gn_spain, gn_france)\n"
        "  All R-facts propagate via MONO000 closure axioms.\n"
        "\n"
        "Conjecture (Style B): verdict_conflict_R_prime(c1, c2).\n"
        "Expected: Theorem.\n"
        "\n"
        "Why: the original Conflict was certified by\n"
        "  disjoint_R(gn_germany, gn_france) + propagation. Under R',\n"
        "  closure gives disjoint_R_prime(gn_germany, gn_france), and\n"
        "  the R'-version of the propagation axiom fires identically.\n"
        "  The introduction of gn_spain doesn't disturb the original\n"
        "  Conflict because gn_spain isn't a subordinate of either\n"
        "  gn_germany or gn_france.\n"
        "\n"
        "SMT cross-check: hypothetical witness x with\n"
        "  leq_R_prime(x, gn_germany) and leq_R_prime(x, gn_france).\n"
        "  Closure-derived disjoint_R_prime(gn_germany, gn_france)\n"
        "  combined with propagation yields false. Expected: unsat.\n"
        "\n"
        "monotone_op guard: c_ispartof and c_eq are monotone (Remark 2);\n"
        "  no neq or isNoneOf used."
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
    odrl:rightOperand <https://sws.geonames.org/3017382/>  # France
  ] .

# Proposition 1 Conflict preservation under concept addition:
#   R: {germany, france} with kge_disjoint(germany, france)
#   R': R + {spain} with new disjointness facts
#   Verdict in R is Conflict (forced_empty via propagation)
#   Conjecture: same Conflict survives in R'.
""",
    "fof_extra_decls": _fof_two_resource_lifts() + """\

% ============================================================
% R-facts: GeoNames-shaped flat registry
% ============================================================
fof(r_germany_in_concepts, axiom,
    in_concepts_R(gn_germany)).

fof(r_france_in_concepts, axiom,
    in_concepts_R(gn_france)).

fof(r_germany_disjoint_france, axiom,
    disjoint_R(gn_germany, gn_france)).

fof(r_distinct_germany_france, axiom,
    gn_germany != gn_france).

% ============================================================
% R' extension: add gn_spain with R'-only disjointness facts
% R-facts auto-lift via MONO000 closure axioms.
% ============================================================
fof(r_ext_spain_in_concepts_prime, axiom,
    in_concepts_R_prime(gn_spain)).

fof(r_ext_spain_not_in_concepts_R, axiom,
    ~in_concepts_R(gn_spain)).

fof(r_ext_spain_disjoint_germany, axiom,
    disjoint_R_prime(gn_spain, gn_germany)).

fof(r_ext_spain_disjoint_france, axiom,
    disjoint_R_prime(gn_spain, gn_france)).

fof(r_ext_distinct_spain_germany, axiom,
    gn_spain != gn_germany).

fof(r_ext_distinct_spain_france, axiom,
    gn_spain != gn_france).
""",
    "fof_conjecture":
        "verdict_conflict_R_prime(c_ispartof(gn_germany), "
        "c_ispartof(gn_france))",
    "smt2_logic": "UF",
    "smt2_decls": """\
; KGC800 SMT cross-check: Conflict preservation under concept addition.
""" + _smt2_two_resource_prelude() + """\

; ============================================================
; Concrete constants for KGC800
; ============================================================
(declare-fun gn_germany () Concept)
(declare-fun gn_france  () Concept)
(declare-fun gn_spain   () Concept)""",
    "smt2_asserts": """\
; ============================================================
; R-facts
; ============================================================
(assert (in_concepts_R gn_germany))
(assert (in_concepts_R gn_france))
(assert (disjoint_R gn_germany gn_france))

; ============================================================
; R' extension: gn_spain is R'-only
; ============================================================
(assert (in_concepts_R_prime gn_spain))
(assert (not (in_concepts_R gn_spain)))
(assert (disjoint_R_prime gn_spain gn_germany))
(assert (disjoint_R_prime gn_spain gn_france))

; ============================================================
; Distinctness
; ============================================================
(assert (distinct gn_germany gn_france gn_spain))

; ============================================================
; Witness search: hypothetical x in [c1]_R' \\cap [c2]_R'
; c1 = c_ispartof(gn_germany), denotation = {x : leq_R_prime(x, gn_germany)}
; c2 = c_ispartof(gn_france),  denotation = {x : leq_R_prime(x, gn_france)}
; ============================================================
(declare-fun x () Concept)
(assert (in_concepts_R_prime x))
(assert (leq_R_prime x gn_germany))
(assert (leq_R_prime x gn_france))

; Expected: unsat. The closure axiom lifts disjoint_R(germany, france)
; to disjoint_R_prime(germany, france); the propagation axiom then
; refutes the witness.""",
}

# ---------------------------------------------------------------------------
# KGC801-KGC812: stubs to instantiate after KGC800 audits clean
# ---------------------------------------------------------------------------
# KGC801: edge addition + Conflict preservation
# R: synthetic DPV-shaped resource where SR ⊥ CR is asserted
#    (this is HYPOTHETICAL — real DPV does not assert this)
# R': add edge SR ≤ AcademicResearch (subsumption growth)
# Conjecture: verdict_conflict_R_prime(c_eq(SR), c_eq(CR))
# Note: synthetic disjointness for monotonicity testing
#
KGC801 = {
    "id":            "KGC801",
    "subdir":        "Monotonicity",
    "name":          "Proposition 1: Conflict preservation under edge addition [synthetic DPV-shaped]",
    "relation":      "monotonicity",
    "verdict":       "MonotonicityConflict",
    "status_fof":    "Theorem",
    "status_smt":    "unsat",
    "difficulty":    "Hard",
    "includes":      [
        "MONO000-0.ax",
    ],
    "needs_density": False,
    "description": (
        "Proposition 1 (Monotonicity) audit: Conflict preservation\n"
        "under edge addition (new subsumption fact in R').\n"
        "\n"
        "Setup:\n"
        "  R: synthetic DPV-shaped taxonomy fragment with two purposes\n"
        "    posited disjoint. NOTE: real DPV does NOT assert this\n"
        "    disjointness; we posit it here as a hypothetical\n"
        "    strengthening to construct a Conflict premise. The audit\n"
        "    tests that adding a subsumption edge (a common parent\n"
        "    relationship) preserves the Conflict verdict.\n"
        "\n"
        "    in_concepts_R(dpv_sr).      [ScientificResearch]\n"
        "    in_concepts_R(dpv_cr).      [CommercialResearch]\n"
        "    in_concepts_R(dpv_rd).      [ResearchAndDevelopment]\n"
        "    leq_R(dpv_sr, dpv_rd).      [SR is below R&D]\n"
        "    leq_R(dpv_cr, dpv_rd).      [CR is below R&D]\n"
        "    disjoint_R(dpv_sr, dpv_cr). [SYNTHETIC: not in real DPV]\n"
        "\n"
        "  Constraints:\n"
        "    c1 = c_ispartof(dpv_sr)   [denotation: leq_R(., dpv_sr)]\n"
        "    c2 = c_ispartof(dpv_cr)   [denotation: leq_R(., dpv_cr)]\n"
        "  R-verdict: verdict_conflict_R(c1, c2). Forced by the\n"
        "    synthetic disjointness plus propagation.\n"
        "\n"
        "Extension R' (edge addition):\n"
        "  Add a new subsumption edge: leq_R_prime(dpv_sr, dpv_ar).\n"
        "    [SR is also below AcademicResearch in R']\n"
        "  Add concept dpv_ar with leq_R_prime(dpv_ar, dpv_rd).\n"
        "  All R-facts auto-lift via MONO000 closure axioms.\n"
        "\n"
        "Conjecture (Style B): verdict_conflict_R_prime(c1, c2).\n"
        "Expected: Theorem.\n"
        "\n"
        "Why: edge addition only enriches the partial order; it does\n"
        "  not retract any disjointness fact. The closure axiom lifts\n"
        "  disjoint_R(dpv_sr, dpv_cr) to disjoint_R_prime(dpv_sr, dpv_cr),\n"
        "  and the R'-version of the propagation axiom forces forced\n"
        "  emptiness identically. The new edge to AcademicResearch is\n"
        "  irrelevant to the Conflict because AR isn't a subordinate\n"
        "  of CR.\n"
        "\n"
        "SMT cross-check: hypothetical witness x with\n"
        "  leq_R_prime(x, dpv_sr) and leq_R_prime(x, dpv_cr).\n"
        "  Closure-derived disjoint_R_prime(dpv_sr, dpv_cr) combined\n"
        "  with propagation yields false. Expected: unsat.\n"
        "\n"
        "monotone_op guard: c_ispartof is monotone (Remark 2)."
    ),
    "ttl": _TTL_PREFIX + """
drk:offer_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:isPartOf ;
    odrl:rightOperand dpv:ScientificResearch
  ] .

drk:request_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:isPartOf ;
    odrl:rightOperand dpv:CommercialResearch
  ] .

# Proposition 1 Conflict preservation under edge addition:
#   R: synthetic DPV-shaped, kge_disjoint(SR, CR) [HYPOTHETICAL]
#   R': R + leq_R_prime(SR, AR) [new subsumption to AcademicResearch]
#   Verdict in R is Conflict (forced_empty via synthetic disjointness)
#   Conjecture: same Conflict survives in R'.
""",
    "fof_extra_decls": _fof_two_resource_lifts() + """\

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
""",
    "fof_conjecture":
        "verdict_conflict_R_prime(c_ispartof(dpv_sr), c_ispartof(dpv_cr))",
    "smt2_logic": "UF",
    "smt2_decls": """\
; KGC801 SMT cross-check: Conflict preservation under edge addition.
""" + _smt2_two_resource_prelude() + """\

; ============================================================
; Concrete constants for KGC801
; ============================================================
(declare-fun dpv_sr () Concept)
(declare-fun dpv_cr () Concept)
(declare-fun dpv_rd () Concept)
(declare-fun dpv_ar () Concept)""",
    "smt2_asserts": """\
; ============================================================
; R-facts: synthetic DPV-shaped resource.
; ============================================================
(assert (in_concepts_R dpv_sr))
(assert (in_concepts_R dpv_cr))
(assert (in_concepts_R dpv_rd))
(assert (leq_R dpv_sr dpv_rd))
(assert (leq_R dpv_cr dpv_rd))
; Synthetic disjointness (not in real DPV)
(assert (disjoint_R dpv_sr dpv_cr))

; ============================================================
; R' extension: dpv_ar is R'-only, with new edge dpv_sr leq_R' dpv_ar
; ============================================================
(assert (in_concepts_R_prime dpv_ar))
(assert (not (in_concepts_R dpv_ar)))
(assert (leq_R_prime dpv_sr dpv_ar))
(assert (leq_R_prime dpv_ar dpv_rd))

; ============================================================
; Distinctness
; ============================================================
(assert (distinct dpv_sr dpv_cr dpv_rd dpv_ar))

; ============================================================
; Witness search: hypothetical x in [c1]_R' \\cap [c2]_R'
; c1 = c_ispartof(dpv_sr), c2 = c_ispartof(dpv_cr)
; ============================================================
(declare-fun x () Concept)
(assert (in_concepts_R_prime x))
(assert (leq_R_prime x dpv_sr))
(assert (leq_R_prime x dpv_cr))

; Expected: unsat. Closure lifts disjoint_R(sr, cr) to
; disjoint_R_prime(sr, cr); propagation refutes the witness.
; The new edge leq_R_prime(sr, ar) is irrelevant — it doesn't
; create any common subordinate of sr and cr.""",
}



# KGC802: disjointness addition + Conflict preservation
# R: GeoNames-shaped, with kge_disjoint(germany, france) [SDA]
# R': add new disjointness fact disjoint_R_prime(germany, italy)
#     and a hierarchy edge bayern ≤ germany
# Conjecture: original Conflict (germany vs france) survives
#
KGC802 = {
    "id":            "KGC802",
    "subdir":        "Monotonicity",
    "name":          "Proposition 1: Conflict preservation under disjointness addition [GeoNames+SDA]",
    "relation":      "monotonicity",
    "verdict":       "MonotonicityConflict",
    "status_fof":    "Theorem",
    "status_smt":    "unsat",
    "difficulty":    "Hard",
    "includes":      [
        "MONO000-0.ax",
    ],
    "needs_density": False,
    "description": (
        "Proposition 1 (Monotonicity) audit: Conflict preservation\n"
        "under disjointness addition (a new disjoint pair appears in R').\n"
        "\n"
        "Setup:\n"
        "  R: GeoNames-shaped with two countries asserted disjoint via\n"
        "    the Sibling-Disjointness Assumption (SDA) profile, plus a\n"
        "    sub-region under one of them.\n"
        "    in_concepts_R(gn_germany), in_concepts_R(gn_france),\n"
        "    in_concepts_R(gn_bayern).\n"
        "    leq_R(gn_bayern, gn_germany).\n"
        "    disjoint_R(gn_germany, gn_france).\n"
        "\n"
        "  Constraints:\n"
        "    c1 = c_ispartof(gn_germany)\n"
        "    c2 = c_ispartof(gn_france)\n"
        "  R-verdict: verdict_conflict_R(c1, c2).\n"
        "\n"
        "Extension R' (disjointness addition):\n"
        "  Add a fresh disjointness fact UNRELATED to the existing\n"
        "  Conflict pair: disjoint_R_prime(gn_italy, gn_france).\n"
        "  Add the corresponding concept gn_italy.\n"
        "  All R-facts (including the original disjoint_R(germany,\n"
        "  france) and leq_R(bayern, germany)) auto-lift via MONO000\n"
        "  closure axioms.\n"
        "\n"
        "Conjecture (Style B): verdict_conflict_R_prime(c1, c2).\n"
        "Expected: Theorem.\n"
        "\n"
        "Why: disjointness addition only enlarges the disjointness\n"
        "  relation; it cannot retract any existing fact. The original\n"
        "  Conflict, certified by disjoint_R(germany, france), survives\n"
        "  via closure to disjoint_R_prime(germany, france), and the\n"
        "  R'-version of the propagation axiom fires identically. The\n"
        "  fresh disjoint_R_prime(italy, france) is irrelevant to the\n"
        "  original pair.\n"
        "\n"
        "SMT cross-check: hypothetical witness x with\n"
        "  leq_R_prime(x, gn_germany) and leq_R_prime(x, gn_france).\n"
        "  Closure-derived disjoint_R_prime(germany, france) plus\n"
        "  propagation refute it. Expected: unsat."
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
    odrl:rightOperand <https://sws.geonames.org/3017382/>  # France
  ] .

# Proposition 1 Conflict preservation under disjointness addition:
#   R: {germany, france, bayern} with kge_disjoint(germany, france)
#      and kge_leq(bayern, germany).
#   R': R + {italy} with new disjoint_R_prime(italy, france).
#   Verdict in R is Conflict (forced_empty via disjointness propagation).
#   Conjecture: same Conflict survives in R'.
""",
    "fof_extra_decls": _fof_two_resource_lifts() + """\

% ============================================================
% R-facts: GeoNames-shaped with SDA disjointness and a sub-region.
% ============================================================
fof(r_germany_in_concepts, axiom,
    in_concepts_R(gn_germany)).

fof(r_france_in_concepts, axiom,
    in_concepts_R(gn_france)).

fof(r_bayern_in_concepts, axiom,
    in_concepts_R(gn_bayern)).

fof(r_bayern_leq_germany, axiom,
    leq_R(gn_bayern, gn_germany)).

fof(r_germany_disjoint_france, axiom,
    disjoint_R(gn_germany, gn_france)).

fof(r_distinct_germany_france, axiom,
    gn_germany != gn_france).

fof(r_distinct_germany_bayern, axiom,
    gn_germany != gn_bayern).

fof(r_distinct_france_bayern, axiom,
    gn_france != gn_bayern).

% ============================================================
% R' extension: add italy concept and a disjointness fact UNRELATED
% to the original Conflict pair. R-facts auto-lift via MONO000.
% ============================================================
fof(r_ext_italy_in_concepts_prime, axiom,
    in_concepts_R_prime(gn_italy)).

fof(r_ext_italy_not_in_concepts_R, axiom,
    ~in_concepts_R(gn_italy)).

fof(r_ext_italy_disjoint_france_prime, axiom,
    disjoint_R_prime(gn_italy, gn_france)).

fof(r_ext_distinct_italy_germany, axiom,
    gn_italy != gn_germany).

fof(r_ext_distinct_italy_france, axiom,
    gn_italy != gn_france).

fof(r_ext_distinct_italy_bayern, axiom,
    gn_italy != gn_bayern).
""",
    "fof_conjecture":
        "verdict_conflict_R_prime(c_ispartof(gn_germany), "
        "c_ispartof(gn_france))",
    "smt2_logic": "UF",
    "smt2_decls": """\
; KGC802 SMT cross-check: Conflict preservation under disjointness addition.
""" + _smt2_two_resource_prelude() + """\

; ============================================================
; Concrete constants for KGC802
; ============================================================
(declare-fun gn_germany () Concept)
(declare-fun gn_france  () Concept)
(declare-fun gn_bayern  () Concept)
(declare-fun gn_italy   () Concept)""",
    "smt2_asserts": """\
; ============================================================
; R-facts
; ============================================================
(assert (in_concepts_R gn_germany))
(assert (in_concepts_R gn_france))
(assert (in_concepts_R gn_bayern))
(assert (leq_R gn_bayern gn_germany))
(assert (disjoint_R gn_germany gn_france))

; ============================================================
; R' extension: italy with new disjointness fact, unrelated to
; the original Conflict pair (germany, france).
; ============================================================
(assert (in_concepts_R_prime gn_italy))
(assert (not (in_concepts_R gn_italy)))
(assert (disjoint_R_prime gn_italy gn_france))

; ============================================================
; Distinctness
; ============================================================
(assert (distinct gn_germany gn_france gn_bayern gn_italy))

; ============================================================
; Witness search: hypothetical x in [c1]_R' \\cap [c2]_R'
; ============================================================
(declare-fun x () Concept)
(assert (in_concepts_R_prime x))
(assert (leq_R_prime x gn_germany))
(assert (leq_R_prime x gn_france))

; Expected: unsat. The new disjoint_R_prime(italy, france) is
; irrelevant; the original disjointness lifts via closure and
; refutes the witness through propagation.""",
}
# KGC803: concept addition + Compatible preservation
# R: GeoNames-shaped, with leq_R(france, europe)
# R': add gn_spain to concepts with leq_R_prime(spain, europe)
# Conjecture: verdict_compatible_R_prime(c_ispartof(europe), c_eq(france))
# Witness: gn_france survives in both denotations.
KGC803 = {
    "id":            "KGC803",
    "subdir":        "Monotonicity",
    "name":          "Proposition 1: Compatible preservation under concept addition [GeoNames]",
    "relation":      "monotonicity",
    "verdict":       "MonotonicityCompatible",
    "status_fof":    "Theorem",
    "status_smt":    "sat",
    "difficulty":    "Hard",
    "includes":      [
        "MONO000-0.ax",
    ],
    "needs_density": False,
    "description": (
        "Proposition 1 (Monotonicity) audit: Compatible preservation\n"
        "under concept addition.\n"
        "\n"
        "Setup:\n"
        "  R: GeoNames-shaped with a containment edge.\n"
        "    in_concepts_R(gn_europe), in_concepts_R(gn_france).\n"
        "    leq_R(gn_france, gn_europe).\n"
        "\n"
        "  Constraints:\n"
        "    c1 = c_ispartof(gn_europe)  [denotation: leq_R(., gn_europe)]\n"
        "    c2 = c_eq(gn_france)        [denotation: gn_france only]\n"
        "  R-verdict: verdict_compatible_R(c1, c2). Witness: gn_france\n"
        "    is in both denotations because leq_R(gn_france, gn_europe).\n"
        "\n"
        "Extension R' (concept addition):\n"
        "  Add concept gn_spain with leq_R_prime(gn_spain, gn_europe).\n"
        "  All R-facts auto-lift via MONO000 closure axioms, so the\n"
        "  R-witness gn_france survives in R'.\n"
        "\n"
        "Conjecture (Style B): verdict_compatible_R_prime(c1, c2).\n"
        "Expected: Theorem.\n"
        "\n"
        "Why: the R-witness gn_france is in [c1]_R and [c2]_R because\n"
        "  leq_R(france, europe) and grounded_as_R(france, france).\n"
        "  Closure axioms lift these to leq_R_prime(france, europe) and\n"
        "  grounded_as_R_prime(france, france), so gn_france is in\n"
        "  [c1]_R' and [c2]_R'. The witness survives; Compatible holds.\n"
        "  The new concept gn_spain doesn't disturb anything.\n"
        "\n"
        "SMT cross-check: assert R-facts and R'-extension facts; check\n"
        "  that a model exists where gn_france satisfies both c1 and c2.\n"
        "  Expected: sat with gn_france as witness."
    ),
    "ttl": _TTL_PREFIX + """
drk:offer_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:isPartOf ;
    odrl:rightOperand <https://sws.geonames.org/6255148/>  # Europe
  ] .

drk:request_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:eq ;
    odrl:rightOperand <https://sws.geonames.org/3017382/>  # France
  ] .

# Proposition 1 Compatible preservation under concept addition:
#   R: {europe, france} with leq_R(france, europe).
#   R': R + {spain} with leq_R_prime(spain, europe).
#   Verdict in R is Compatible (witness gn_france in both denotations).
#   Conjecture: same Compatible survives in R'; witness gn_france survives.
""",
    "fof_extra_decls": _fof_two_resource_lifts() + """\

% ============================================================
% R-facts: GeoNames-shaped with France below Europe.
% Grounding facts establish gn_france as the grounded value of the
% right-operand identifier (so c_eq(gn_france) has a singleton
% denotation containing gn_france).
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
""",
    "fof_conjecture":
        "verdict_compatible_R_prime(c_ispartof(gn_europe), c_eq(gn_france))",
    "smt2_logic": "UF",
    "smt2_decls": """\
; KGC803 SMT cross-check: Compatible preservation under concept addition.
""" + _smt2_two_resource_prelude() + """\

; ============================================================
; Concrete constants for KGC803
; ============================================================
(declare-fun gn_europe () Concept)
(declare-fun gn_france () Concept)
(declare-fun gn_spain  () Concept)""",
    "smt2_asserts": """\
; ============================================================
; R-facts
; ============================================================
(assert (in_concepts_R gn_europe))
(assert (in_concepts_R gn_france))
(assert (leq_R gn_france gn_europe))

; ============================================================
; R' extension: spain is R'-only, with leq_R_prime(spain, europe)
; ============================================================
(assert (in_concepts_R_prime gn_spain))
(assert (not (in_concepts_R gn_spain)))
(assert (leq_R_prime gn_spain gn_europe))

; ============================================================
; Distinctness
; ============================================================
(assert (distinct gn_europe gn_france gn_spain))

; ============================================================
; Compatible verification: gn_france is in both denotations
; under R'. [c_ispartof(europe)]_R' contains gn_france because
; leq_R_prime(france, europe) (lifted from R via closure).
; [c_eq(france)]_R' is the singleton {gn_france}.
;
; The SMT side checks consistency: the model must exist where
; france is the witness. Expected: sat.
;
; No contradiction is asserted; the resource is consistent and a
; satisfying model exists.""",
}
#
# KGC804: edge addition + Compatible preservation
# R: leq_R(france, europe) base
# R': add leq_R_prime(germany, europe) (new concept germany under europe)
# Conjecture: original Compatible (europe ispartof vs france eq) survives

KGC804 = {
    "id":            "KGC804",
    "subdir":        "Monotonicity",
    "name":          "Proposition 1: Compatible preservation under edge addition [GeoNames]",
    "relation":      "monotonicity",
    "verdict":       "MonotonicityCompatible",
    "status_fof":    "Theorem",
    "status_smt":    "sat",
    "difficulty":    "Hard",
    "includes":      [
        "MONO000-0.ax",
    ],
    "needs_density": False,
    "description": (
        "Proposition 1 (Monotonicity) audit: Compatible preservation\n"
        "under edge addition.\n"
        "\n"
        "Setup:\n"
        "  R: GeoNames-shaped with one containment edge.\n"
        "    in_concepts_R(gn_europe), in_concepts_R(gn_france).\n"
        "    leq_R(gn_france, gn_europe).\n"
        "    grounded_as_R(gn_france, gn_france).\n"
        "\n"
        "  Constraints:\n"
        "    c1 = c_ispartof(gn_europe)\n"
        "    c2 = c_eq(gn_france)\n"
        "  R-verdict: verdict_compatible_R(c1, c2). Witness: gn_france.\n"
        "\n"
        "Extension R' (edge addition):\n"
        "  Add concept gn_germany with leq_R_prime(gn_germany, gn_europe).\n"
        "  Germany is R'-only. The new subsumption edge enriches the\n"
        "  partial order without disturbing france's containment.\n"
        "\n"
        "Conjecture (Style B): verdict_compatible_R_prime(c1, c2).\n"
        "Expected: Theorem.\n"
        "\n"
        "Why: gn_france remains in [c1]_R' via closure-lifted\n"
        "  leq_R_prime(france, europe), and in [c2]_R' via closure-lifted\n"
        "  grounded_as_R_prime(france, france). The witness gn_france\n"
        "  survives. Adding the new edge for Germany does not affect\n"
        "  france's relation to europe.\n"
        "\n"
        "SMT cross-check: assert R-facts and R'-extension facts; check\n"
        "  consistency. Expected: sat with gn_france as witness."
    ),
    "ttl": _TTL_PREFIX + """
drk:offer_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:isPartOf ;
    odrl:rightOperand <https://sws.geonames.org/6255148/>  # Europe
  ] .

drk:request_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:eq ;
    odrl:rightOperand <https://sws.geonames.org/3017382/>  # France
  ] .

# Proposition 1 Compatible preservation under edge addition:
#   R: {europe, france} with leq_R(france, europe).
#   R': R + {germany} with leq_R_prime(germany, europe).
#   Verdict in R is Compatible (witness gn_france).
#   Conjecture: same Compatible survives in R'.
""",
    "fof_extra_decls": _fof_two_resource_lifts() + """\

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
""",
    "fof_conjecture":
        "verdict_compatible_R_prime(c_ispartof(gn_europe), c_eq(gn_france))",
    "smt2_logic": "UF",
    "smt2_decls": """\
; KGC804 SMT cross-check: Compatible preservation under edge addition.
""" + _smt2_two_resource_prelude() + """\

; ============================================================
; Concrete constants for KGC804
; ============================================================
(declare-fun gn_europe  () Concept)
(declare-fun gn_france  () Concept)
(declare-fun gn_germany () Concept)""",
    "smt2_asserts": """\
; ============================================================
; R-facts
; ============================================================
(assert (in_concepts_R gn_europe))
(assert (in_concepts_R gn_france))
(assert (leq_R gn_france gn_europe))

; ============================================================
; R' extension: germany is R'-only, with new edge to europe.
; ============================================================
(assert (in_concepts_R_prime gn_germany))
(assert (not (in_concepts_R gn_germany)))
(assert (leq_R_prime gn_germany gn_europe))

; ============================================================
; Distinctness
; ============================================================
(assert (distinct gn_europe gn_france gn_germany))

; ============================================================
; Compatible verification: gn_france is in [c1]_R' (via closure-
; lifted leq_R_prime(france, europe)) and [c2]_R' (singleton).
; Resource is consistent. Expected: sat with france as witness.""",
}

# KGC805: disjointness addition + Compatible preservation
# R: GeoNames-shaped, with leq_R(france, europe), no disjointness
# R': add disjoint_R_prime(usa, china) (irrelevant disjointness)
# Conjecture: original Compatible verdict survives (irrelevant addition)
#
KGC805 = {
    "id":            "KGC805",
    "subdir":        "Monotonicity",
    "name":          "Proposition 1: Compatible preservation under disjointness addition [GeoNames]",
    "relation":      "monotonicity",
    "verdict":       "MonotonicityCompatible",
    "status_fof":    "Theorem",
    "status_smt":    "sat",
    "difficulty":    "Hard",
    "includes":      [
        "MONO000-0.ax",
    ],
    "needs_density": False,
    "description": (
        "Proposition 1 (Monotonicity) audit: Compatible preservation\n"
        "under disjointness addition.\n"
        "\n"
        "Setup:\n"
        "  R: GeoNames-shaped, France below Europe, no disjointness.\n"
        "    in_concepts_R(gn_europe), in_concepts_R(gn_france).\n"
        "    leq_R(gn_france, gn_europe).\n"
        "    grounded_as_R(gn_france, gn_france).\n"
        "\n"
        "  Constraints:\n"
        "    c1 = c_ispartof(gn_europe)\n"
        "    c2 = c_eq(gn_france)\n"
        "  R-verdict: verdict_compatible_R(c1, c2). Witness: gn_france.\n"
        "\n"
        "Extension R' (disjointness addition, irrelevant to witness):\n"
        "  Add concepts gn_usa and gn_china (both R'-only).\n"
        "  Add disjoint_R_prime(gn_usa, gn_china).\n"
        "  The new disjointness involves two fresh concepts that are\n"
        "  not related to France or Europe via any leq edge. The\n"
        "  R-witness gn_france is unaffected.\n"
        "\n"
        "Conjecture (Style B): verdict_compatible_R_prime(c1, c2).\n"
        "Expected: Theorem.\n"
        "\n"
        "Why: gn_france satisfies both denotations under R' via closure-\n"
        "  lifted leq_R_prime(france, europe) and grounded_as_R_prime\n"
        "  (france, france). The new disjoint_R_prime(usa, china) does\n"
        "  not affect france because there are no leq edges from\n"
        "  france to either usa or china. The propagation axiom finds\n"
        "  no contradiction at the witness.\n"
        "\n"
        "  This is the 'noise immunity' test: irrelevant disjointness\n"
        "  additions do not break unrelated Compatible verdicts.\n"
        "\n"
        "SMT cross-check: assert R-facts and R'-extension facts; check\n"
        "  consistency. Expected: sat with gn_france as witness."
    ),
    "ttl": _TTL_PREFIX + """
drk:offer_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:isPartOf ;
    odrl:rightOperand <https://sws.geonames.org/6255148/>  # Europe
  ] .

drk:request_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:eq ;
    odrl:rightOperand <https://sws.geonames.org/3017382/>  # France
  ] .

# Proposition 1 Compatible preservation under disjointness addition:
#   R: {europe, france} with leq_R(france, europe), no disjointness.
#   R': R + {usa, china} with disjoint_R_prime(usa, china).
#   Verdict in R is Compatible (witness gn_france).
#   Conjecture: same Compatible survives in R' because the new
#   disjointness is irrelevant to france.
""",
    "fof_extra_decls": _fof_two_resource_lifts() + """\

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
% R' extension: add gn_usa and gn_china with a fresh disjointness
% fact. Both concepts are R'-only and unrelated to France or Europe
% via any leq edge.
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

fof(r_ext_distinct_usa_france, axiom,
    gn_usa != gn_france).

fof(r_ext_distinct_china_europe, axiom,
    gn_china != gn_europe).

fof(r_ext_distinct_china_france, axiom,
    gn_china != gn_france).
""",
    "fof_conjecture":
        "verdict_compatible_R_prime(c_ispartof(gn_europe), c_eq(gn_france))",
    "smt2_logic": "UF",
    "smt2_decls": """\
; KGC805 SMT cross-check: Compatible preservation under disjointness addition.
""" + _smt2_two_resource_prelude() + """\

; ============================================================
; Concrete constants for KGC805
; ============================================================
(declare-fun gn_europe () Concept)
(declare-fun gn_france () Concept)
(declare-fun gn_usa    () Concept)
(declare-fun gn_china  () Concept)""",
    "smt2_asserts": """\
; ============================================================
; R-facts
; ============================================================
(assert (in_concepts_R gn_europe))
(assert (in_concepts_R gn_france))
(assert (leq_R gn_france gn_europe))

; ============================================================
; R' extension: usa and china R'-only, with fresh disjointness.
; Neither has any leq relation to france or europe.
; ============================================================
(assert (in_concepts_R_prime gn_usa))
(assert (not (in_concepts_R gn_usa)))
(assert (in_concepts_R_prime gn_china))
(assert (not (in_concepts_R gn_china)))
(assert (disjoint_R_prime gn_usa gn_china))

; ============================================================
; Distinctness
; ============================================================
(assert (distinct gn_europe gn_france gn_usa gn_china))

; ============================================================
; Compatible verification: gn_france is in [c1]_R' via closure-
; lifted leq_R_prime(france, europe), and in [c2]_R' as the
; singleton witness for c_eq(france). The new disjoint_R_prime
; (usa, china) does not affect france.
; Expected: sat with france as witness.""",
}
# KGC806: concept addition + denotation growth (universal)
# Conjecture: !X. in_denotation_R(X, c_ispartof(europe)) =>
#                  in_denotation_R_prime(X, c_ispartof(europe))
# This is the underlying mechanism: closure forces denotation growth.
#
KGC806 = {
    "id":            "KGC806",
    "subdir":        "Monotonicity",
    "name":          "Proposition 1: denotation growth under concept addition [GeoNames]",
    "relation":      "monotonicity",
    "verdict":       "MonotonicityDenotation",
    "status_fof":    "Theorem",
    "status_smt":    "unsat",
    "difficulty":    "Hard",
    "includes":      [
        "MONO000-0.ax",
    ],
    "needs_density": False,
    "description": (
        "Proposition 1 (Monotonicity) audit: denotation growth under\n"
        "concept addition. This is the underlying mechanism — the\n"
        "first claim of Proposition 1, on which verdict preservation\n"
        "(audited by KGC800/803) depends.\n"
        "\n"
        "The conjecture is universally quantified over concepts:\n"
        "  forall X. in_denotation_R(X, c_ispartof(gn_europe))\n"
        "         => in_denotation_R_prime(X, c_ispartof(gn_europe))\n"
        "\n"
        "This says: every concept in [c]_R is also in [c]_R'. The claim\n"
        "is independent of any specific witness; it tests the closure\n"
        "axioms uniformly across the concept domain.\n"
        "\n"
        "Setup:\n"
        "  R: GeoNames-shaped with one containment edge.\n"
        "    in_concepts_R(gn_europe), in_concepts_R(gn_france).\n"
        "    leq_R(gn_france, gn_europe).\n"
        "\n"
        "Extension R' (concept addition):\n"
        "  Add concept gn_spain with leq_R_prime(gn_spain, gn_europe).\n"
        "  All R-facts auto-lift via MONO000 closure axioms.\n"
        "\n"
        "Conjecture (Style A): the universal denotation-growth statement.\n"
        "Expected: Theorem.\n"
        "\n"
        "Why: in_denotation_R(X, c_ispartof(europe)) unfolds (via\n"
        "  den_ispartof_R) to leq_R(X, gn_europe). MONO000's closure\n"
        "  axiom extension_leq lifts this to leq_R_prime(X, gn_europe).\n"
        "  Then den_ispartof_R_prime gives in_denotation_R_prime(X,\n"
        "  c_ispartof(europe)). The chain is purely axiomatic; no\n"
        "  witness construction needed.\n"
        "\n"
        "SMT cross-check: assert R-facts plus extension. Assert that\n"
        "  some specific concept x is in [c]_R but NOT in [c]_R'.\n"
        "  Closure axioms force a contradiction. Expected: unsat."
    ),
    "ttl": _TTL_PREFIX + """
drk:offer_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:isPartOf ;
    odrl:rightOperand <https://sws.geonames.org/6255148/>  # Europe
  ] .

# Proposition 1 denotation growth under concept addition:
#   R: {europe, france} with leq_R(france, europe).
#   R': R + {spain} with leq_R_prime(spain, europe).
#   Conjecture: every concept in [c_ispartof(europe)]_R is in
#   [c_ispartof(europe)]_R' (universal denotation-growth claim).
""",
    "fof_extra_decls": _fof_two_resource_lifts() + """\

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
""",
    "fof_conjecture":
        "![X]: (in_denotation_R(X, c_ispartof(gn_europe)) "
        "=> in_denotation_R_prime(X, c_ispartof(gn_europe)))",
    "smt2_logic": "UF",
    "smt2_decls": """\
; KGC806 SMT cross-check: denotation growth under concept addition.
""" + _smt2_two_resource_prelude() + """\

; ============================================================
; Concrete constants for KGC806
; ============================================================
(declare-fun gn_europe () Concept)
(declare-fun gn_france () Concept)
(declare-fun gn_spain  () Concept)""",
    "smt2_asserts": """\
; ============================================================
; R-facts
; ============================================================
(assert (in_concepts_R gn_europe))
(assert (in_concepts_R gn_france))
(assert (leq_R gn_france gn_europe))

; ============================================================
; R' extension: spain R'-only with new edge to europe
; ============================================================
(assert (in_concepts_R_prime gn_spain))
(assert (not (in_concepts_R gn_spain)))
(assert (leq_R_prime gn_spain gn_europe))

; ============================================================
; Distinctness
; ============================================================
(assert (distinct gn_europe gn_france gn_spain))

; ============================================================
; Witness search: hypothetical x that is in [c_ispartof(europe)]_R
; but NOT in [c_ispartof(europe)]_R'.
; In SMT terms: leq_R(x, europe) AND NOT leq_R_prime(x, europe).
; The closure axiom extension_leq forces this contradiction.
; Expected: unsat.
; ============================================================
(declare-fun x () Concept)
(assert (leq_R x gn_europe))
(assert (not (leq_R_prime x gn_europe)))""",
}
# KGC807: edge addition + denotation growth
# Conjecture: !X. leq_R(X, europe) => leq_R_prime(X, europe)
# Direct test of the closure axiom.
#
KGC807 = {
    "id":            "KGC807",
    "subdir":        "Monotonicity",
    "name":          "Proposition 1: denotation growth under edge addition [GeoNames]",
    "relation":      "monotonicity",
    "verdict":       "MonotonicityDenotation",
    "status_fof":    "Theorem",
    "status_smt":    "unsat",
    "difficulty":    "Hard",
    "includes":      [
        "MONO000-0.ax",
    ],
    "needs_density": False,
    "description": (
        "Proposition 1 (Monotonicity) audit: denotation growth under\n"
        "edge addition. Tests the underlying mechanism (closure axiom\n"
        "for kge_leq) directly via universal denotation-growth claim.\n"
        "\n"
        "The conjecture is universally quantified over concepts:\n"
        "  forall X. in_denotation_R(X, c_ispartof(gn_europe))\n"
        "         => in_denotation_R_prime(X, c_ispartof(gn_europe))\n"
        "\n"
        "This is a stronger test than verdict preservation alone:\n"
        "every concept in the original denotation must be in the\n"
        "extended denotation, regardless of any specific witness.\n"
        "\n"
        "Setup:\n"
        "  R: GeoNames-shaped, France below Europe.\n"
        "    in_concepts_R(gn_europe), in_concepts_R(gn_france),\n"
        "    in_concepts_R(gn_germany).\n"
        "    leq_R(gn_france, gn_europe).\n"
        "\n"
        "Extension R' (edge addition):\n"
        "  Add new subsumption edge: leq_R_prime(gn_germany, gn_europe).\n"
        "  Germany is already in R; the new edge enriches the partial\n"
        "  order. R-facts auto-lift via MONO000.\n"
        "\n"
        "Conjecture (Style A): the universal denotation-growth statement.\n"
        "Expected: Theorem.\n"
        "\n"
        "Why: same chain as KGC806 — den_ispartof_R unfolds, closure\n"
        "  lifts leq_R to leq_R_prime, den_ispartof_R_prime closes the\n"
        "  derivation. The new edge for Germany is irrelevant to the\n"
        "  growth claim because the claim is universally quantified.\n"
        "\n"
        "SMT cross-check: assert R-facts and R'-extension. Hypothetical\n"
        "  x in [c]_R but not in [c]_R'. Closure forces contradiction.\n"
        "  Expected: unsat."
    ),
    "ttl": _TTL_PREFIX + """
drk:offer_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:isPartOf ;
    odrl:rightOperand <https://sws.geonames.org/6255148/>  # Europe
  ] .

# Proposition 1 denotation growth under edge addition:
#   R: {europe, france, germany} with leq_R(france, europe).
#   R': R + leq_R_prime(germany, europe).
#   Conjecture: every concept in [c_ispartof(europe)]_R is in
#   [c_ispartof(europe)]_R' (universal).
""",
    "fof_extra_decls": _fof_two_resource_lifts() + """\

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
""",
    "fof_conjecture":
        "![X]: (in_denotation_R(X, c_ispartof(gn_europe)) "
        "=> in_denotation_R_prime(X, c_ispartof(gn_europe)))",
    "smt2_logic": "UF",
    "smt2_decls": """\
; KGC807 SMT cross-check: denotation growth under edge addition.
""" + _smt2_two_resource_prelude() + """\

; ============================================================
; Concrete constants for KGC807
; ============================================================
(declare-fun gn_europe  () Concept)
(declare-fun gn_france  () Concept)
(declare-fun gn_germany () Concept)""",
    "smt2_asserts": """\
; ============================================================
; R-facts
; ============================================================
(assert (in_concepts_R gn_europe))
(assert (in_concepts_R gn_france))
(assert (in_concepts_R gn_germany))
(assert (leq_R gn_france gn_europe))

; ============================================================
; R' extension: new edge germany leq_R' europe (germany was
; already in R; the edge is the new fact).
; ============================================================
(assert (leq_R_prime gn_germany gn_europe))

; ============================================================
; Distinctness
; ============================================================
(assert (distinct gn_europe gn_france gn_germany))

; ============================================================
; Witness search: hypothetical x in [c]_R but not in [c]_R'.
; In SMT terms: leq_R(x, europe) AND NOT leq_R_prime(x, europe).
; Closure axiom extension_leq forces contradiction.
; Expected: unsat.
; ============================================================
(declare-fun x () Concept)
(assert (leq_R x gn_europe))
(assert (not (leq_R_prime x gn_europe)))""",
}
# KGC808: disjointness addition + denotation growth
# Conjecture: !X. !Y. disjoint_R(X, Y) => disjoint_R_prime(X, Y)
# Tests the third closure axiom directly.
#
KGC808= {
    "id":            "KGC808",
    "subdir":        "Monotonicity",
    "name":          "Proposition 1: denotation growth under disjointness addition with c_haspart [GeoNames]",
    "relation":      "monotonicity",
    "verdict":       "MonotonicityDenotation",
    "status_fof":    "Theorem",
    "status_smt":    "unsat",
    "difficulty":    "Hard",
    "includes":      [
        "MONO000-0.ax",
    ],
    "needs_density": False,
    "description": (
        "Proposition 1 (Monotonicity) audit: denotation growth under\n"
        "disjointness addition for the c_haspart operator. This audit\n"
        "is structurally distinct from KGC806/807 because the c_haspart\n"
        "denotation is the upward cone (concepts containing G), not the\n"
        "downward cone (concepts below G). The leq closure axiom is\n"
        "used in the contravariant direction of the variable.\n"
        "\n"
        "The conjecture is universally quantified:\n"
        "  forall X. in_denotation_R(X, c_haspart(gn_germany))\n"
        "         => in_denotation_R_prime(X, c_haspart(gn_germany))\n"
        "\n"
        "Setup:\n"
        "  R: GeoNames-shaped with Germany below Europe.\n"
        "    in_concepts_R(gn_europe), in_concepts_R(gn_germany).\n"
        "    leq_R(gn_germany, gn_europe).\n"
        "\n"
        "Extension R' (disjointness addition, irrelevant):\n"
        "  Add gn_usa and gn_china (R'-only) with disjoint_R_prime.\n"
        "  All R-facts auto-lift via MONO000.\n"
        "\n"
        "Conjecture (Style A): the universal denotation-growth statement.\n"
        "Expected: Theorem.\n"
        "\n"
        "Why: in_denotation_R(X, c_haspart(germany)) unfolds (via\n"
        "  den_haspart_R) to leq_R(germany, X). Closure axiom\n"
        "  extension_leq lifts this to leq_R_prime(germany, X). Then\n"
        "  den_haspart_R_prime gives in_denotation_R_prime(X,\n"
        "  c_haspart(germany)). The new disjointness facts are\n"
        "  irrelevant to the leq chain.\n"
        "\n"
        "  The contravariant direction (G below X, vs. X below G in\n"
        "  isPartOf) tests the same closure axiom but with the variable\n"
        "  on the opposite side. Saturation provers may take a different\n"
        "  inference path here than in KGC806/807.\n"
        "\n"
        "SMT cross-check: hypothetical x in [c_haspart(germany)]_R but\n"
        "  not in [c_haspart(germany)]_R'. In SMT terms: leq_R(germany,\n"
        "  x) AND NOT leq_R_prime(germany, x). Closure forces\n"
        "  contradiction. Expected: unsat."
    ),
    "ttl": _TTL_PREFIX + """
drk:offer_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:hasPart ;
    odrl:rightOperand <https://sws.geonames.org/2921044/>  # Germany
  ] .

# Proposition 1 denotation growth under disjointness addition with c_haspart:
#   R: {europe, germany} with leq_R(germany, europe).
#   R': R + {usa, china} with disjoint_R_prime(usa, china).
#   Conjecture: every concept in [c_haspart(germany)]_R is in
#   [c_haspart(germany)]_R' (contravariant test).
""",
    "fof_extra_decls": _fof_two_resource_lifts() + """\

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
""",
    "fof_conjecture":
        "![X]: (in_denotation_R(X, c_haspart(gn_germany)) "
        "=> in_denotation_R_prime(X, c_haspart(gn_germany)))",
    "smt2_logic": "UF",
    "smt2_decls": """\
; KGC808 SMT cross-check: denotation growth for c_haspart under
; disjointness addition (contravariant variable position).
""" + _smt2_two_resource_prelude() + """\

; ============================================================
; Concrete constants for KGC808
; ============================================================
(declare-fun gn_europe  () Concept)
(declare-fun gn_germany () Concept)
(declare-fun gn_usa     () Concept)
(declare-fun gn_china   () Concept)""",
    "smt2_asserts": """\
; ============================================================
; R-facts: Germany below Europe.
; ============================================================
(assert (in_concepts_R gn_europe))
(assert (in_concepts_R gn_germany))
(assert (leq_R gn_germany gn_europe))

; ============================================================
; R' extension: irrelevant disjointness fact on two R'-only concepts.
; ============================================================
(assert (in_concepts_R_prime gn_usa))
(assert (not (in_concepts_R gn_usa)))
(assert (in_concepts_R_prime gn_china))
(assert (not (in_concepts_R gn_china)))
(assert (disjoint_R_prime gn_usa gn_china))

; ============================================================
; Distinctness
; ============================================================
(assert (distinct gn_europe gn_germany gn_usa gn_china))

; ============================================================
; Witness search: hypothetical x in [c_haspart(germany)]_R but not in
; [c_haspart(germany)]_R'. In SMT terms: leq_R(germany, x) AND NOT
; leq_R_prime(germany, x). Note the variable is on the right-hand
; side of leq, vs. the left in KGC806/807.
; Closure axiom extension_leq forces contradiction.
; Expected: unsat.
; ============================================================
(declare-fun x () Concept)
(assert (leq_R gn_germany x))
(assert (not (leq_R_prime gn_germany x)))""",
}
# KGC810: BOUNDARY — complement counterexample (Remark 2)
# R: {de, fr} only, both R-concepts
# Constraints: c1 = c_neq(de), c2 = c_neq(fr)
#   In R: [c1] = {fr}, [c2] = {de}, intersection empty → Conflict
# R': add bcp_es. Now [c1]_R' = {fr, es}, [c2]_R' = {de, es}
#   intersection = {es}, non-empty → Compatible
# Conjecture: verdict_conflict_R_prime(c1, c2). Expected: CSA.
# Demonstrates why monotone_op guard excludes neq.
#
KGC810 ={
    "id":            "KGC810",
    "subdir":        "Monotonicity",
    "name":          "Proposition 1: complement counterexample [Remark 2 — neq]",
    "relation":      "monotonicity",
    "verdict":       "MonotonicityComplementBoundary",
    "status_fof":    "CounterSatisfiable",
    "status_smt":    "sat",
    "difficulty":    "Hard",
    "includes":      [
        "MONO000-0.ax",
    ],
    "needs_density": False,
    "description": (
        "Proposition 1 (Monotonicity) BOUNDARY audit: complement\n"
        "operators are NOT preserved under resource extension.\n"
        "Demonstrates Remark 2 empirically — c_neq verdicts can flip\n"
        "from Conflict to Compatible under concept addition, which is\n"
        "why Proposition 1 explicitly restricts to monotone operators.\n"
        "\n"
        "Setup:\n"
        "  R: BCP47-shaped flat registry with two concepts.\n"
        "    in_concepts_R(bcp_de), in_concepts_R(bcp_fr).\n"
        "    grounded_as_R(bcp_de, bcp_de),\n"
        "    grounded_as_R(bcp_fr, bcp_fr).\n"
        "\n"
        "  Constraints:\n"
        "    c1 = c_neq(bcp_de)  [denotation: concepts != de]\n"
        "    c2 = c_neq(bcp_fr)  [denotation: concepts != fr]\n"
        "  R-verdict: verdict_conflict_R(c1, c2).\n"
        "    [c1]_R = {bcp_fr}, [c2]_R = {bcp_de}, intersection empty.\n"
        "    Forced empty in R because no concept other than de or fr\n"
        "    exists in R.\n"
        "\n"
        "Extension R' (concept addition):\n"
        "  Add concept bcp_es. Now [c1]_R' = {bcp_fr, bcp_es},\n"
        "  [c2]_R' = {bcp_de, bcp_es}. Intersection = {bcp_es}.\n"
        "\n"
        "Conjecture (Style B): verdict_conflict_R_prime(c1, c2).\n"
        "Expected: CounterSatisfiable.\n"
        "\n"
        "Why: bcp_es satisfies BOTH complement constraints (it is\n"
        "  != de AND != fr), giving a witness in [c1]_R' \\cap [c2]_R'.\n"
        "  The Conflict from R does NOT survive in R'. This concrete\n"
        "  counterexample justifies Remark 2's restriction of\n"
        "  Proposition 1 to monotone operators.\n"
        "\n"
        "  The denotation rule den_neq_R requires both in_concepts(X)\n"
        "  AND ~grounded_as(X, g). The concept-membership guard is\n"
        "  essential here: without it, the prover could hallucinate\n"
        "  Skolem witnesses outside the concept set, masking the\n"
        "  counterexample.\n"
        "\n"
        "SMT cross-check: assert R-facts and R'-extension. The witness\n"
        "  bcp_es is in both denotations under R'. Resource is\n"
        "  consistent with verdict_compatible holding. Expected: sat."
    ),
    "ttl": _TTL_PREFIX + """
drk:offer_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:language ;
    odrl:operator odrl:neq ;
    odrl:rightOperand bcp:de
  ] .

drk:request_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:language ;
    odrl:operator odrl:neq ;
    odrl:rightOperand bcp:fr
  ] .

# BOUNDARY audit: Remark 2 (complement operators).
#   R: {bcp_de, bcp_fr}. Verdict: Conflict (no shared non-de non-fr concept).
#   R': R + {bcp_es}. Verdict: Compatible (bcp_es satisfies both neq).
#   Conjecture asserts conflict_R_prime; expected to NOT derive.
""",
    "fof_extra_decls": _fof_two_resource_lifts() + """\

% ============================================================
% den_neq lifted to R and R' with concept-membership guard.
% This is essential for the boundary audit: complement operators
% reference the complement of the concept set, so denotation
% membership must require in_concepts/1 to prevent the prover from
% hallucinating Skolem witnesses outside the concept set.
% ============================================================
fof(den_neq_R, axiom,
    ![X, G]:
      (in_denotation_R(X, c_neq(G)) <=>
       (in_concepts_R(X) & ~grounded_as_R(X, G)))).

fof(den_neq_R_prime, axiom,
    ![X, G]:
      (in_denotation_R_prime(X, c_neq(G)) <=>
       (in_concepts_R_prime(X) & ~grounded_as_R_prime(X, G)))).

% ============================================================
% R-facts: BCP47-shaped registry with exactly two concepts.
% Closed-world for R: the only concepts are de and fr.
% ============================================================
fof(r_de_in_concepts, axiom,
    in_concepts_R(bcp_de)).

fof(r_fr_in_concepts, axiom,
    in_concepts_R(bcp_fr)).

fof(r_de_grounded, axiom,
    grounded_as_R(bcp_de, bcp_de)).

fof(r_fr_grounded, axiom,
    grounded_as_R(bcp_fr, bcp_fr)).

% Closed-world enumeration for R: only de and fr are in_concepts_R.
fof(r_concepts_closed, axiom,
    ![X]: (in_concepts_R(X) <=> (X = bcp_de | X = bcp_fr))).

fof(r_distinct_de_fr, axiom,
    bcp_de != bcp_fr).

% ============================================================
% R' extension: add concept bcp_es. R-facts auto-lift via MONO000.
% ============================================================
fof(r_ext_es_in_concepts_prime, axiom,
    in_concepts_R_prime(bcp_es)).

fof(r_ext_es_not_in_concepts_R, axiom,
    ~in_concepts_R(bcp_es)).

fof(r_ext_es_grounded, axiom,
    grounded_as_R_prime(bcp_es, bcp_es)).

fof(r_ext_distinct_es_de, axiom,
    bcp_es != bcp_de).

fof(r_ext_distinct_es_fr, axiom,
    bcp_es != bcp_fr).
""",
    "fof_conjecture":
        "verdict_conflict_R_prime(c_neq(bcp_de), c_neq(bcp_fr))",
    "smt2_logic": "UF",
    "smt2_decls": """\
; KGC810 SMT cross-check: complement boundary counterexample.
""" + _smt2_two_resource_prelude() + """\

(declare-fun grounded_as_R       (Concept Concept) Bool)
(declare-fun grounded_as_R_prime (Concept Concept) Bool)

; Closure for grounding (MONO000 axiom in SMT form).
(assert (forall ((c Concept) (g Concept))
    (=> (grounded_as_R c g) (grounded_as_R_prime c g))))

; ============================================================
; Concrete constants for KGC810
; ============================================================
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)
(declare-fun bcp_es () Concept)""",
    "smt2_asserts": """\
; ============================================================
; R-facts: closed-world {bcp_de, bcp_fr}.
; ============================================================
(assert (in_concepts_R bcp_de))
(assert (in_concepts_R bcp_fr))
(assert (grounded_as_R bcp_de bcp_de))
(assert (grounded_as_R bcp_fr bcp_fr))
(assert (forall ((x Concept))
    (=> (in_concepts_R x) (or (= x bcp_de) (= x bcp_fr)))))

; ============================================================
; R' extension: add bcp_es with grounding.
; ============================================================
(assert (in_concepts_R_prime bcp_es))
(assert (not (in_concepts_R bcp_es)))
(assert (grounded_as_R_prime bcp_es bcp_es))

; ============================================================
; Distinctness
; ============================================================
(assert (distinct bcp_de bcp_fr bcp_es))

; ============================================================
; Witness: bcp_es is in [c_neq(de)]_R' \\cap [c_neq(fr)]_R'.
; bcp_es is in_concepts_R_prime, != bcp_de, != bcp_fr.
; The resource is consistent with this witness existing.
; Expected: sat.""",
}

{
    "id":            "KGC810",
    "subdir":        "Monotonicity",
    "name":          "Proposition 1: complement counterexample [Remark 2 — neq, Compatible witness in R']",
    "relation":      "monotonicity",
    "verdict":       "MonotonicityComplementBoundary",
    "status_fof":    "Theorem",
    "status_smt":    "sat",
    "difficulty":    "Hard",
    "includes":      [
        "MONO000-0.ax",
    ],
    "needs_density": False,
    "description": (
        "Proposition 1 (Monotonicity) BOUNDARY audit: complement\n"
        "operators are NOT preserved under resource extension.\n"
        "\n"
        "This audit demonstrates Remark 2 by constructing the\n"
        "verdict-flip empirically. In R the c_neq pair is Conflict\n"
        "(no shared concept). In R' a new concept satisfies BOTH\n"
        "complement constraints, giving Compatible.\n"
        "\n"
        "Setup:\n"
        "  R: BCP47-shaped registry with two concepts.\n"
        "    in_concepts_R(bcp_de), in_concepts_R(bcp_fr).\n"
        "    grounded_as_R(bcp_de, bcp_de),\n"
        "    grounded_as_R(bcp_fr, bcp_fr).\n"
        "\n"
        "  Constraints:\n"
        "    c1 = c_neq(bcp_de)  [denotation: in_concepts ! grounded as de]\n"
        "    c2 = c_neq(bcp_fr)  [denotation: in_concepts ! grounded as fr]\n"
        "\n"
        "Extension R' (concept addition):\n"
        "  Add bcp_es with grounded_as_R_prime(bcp_es, bcp_es).\n"
        "  Now bcp_es is in [c1]_R' (it's a concept and not grounded\n"
        "  to de) AND in [c2]_R' (concept, not grounded to fr).\n"
        "\n"
        "Conjecture (Style A): verdict_compatible_R_prime(c1, c2).\n"
        "Expected: Theorem. The witness bcp_es is in both denotations.\n"
        "\n"
        "Why this audits Remark 2: in R the c_neq pair is Conflict\n"
        "  (only de and fr exist; neither satisfies both complements).\n"
        "  In R' adding bcp_es gives a witness for Compatible. The\n"
        "  Conflict from R does NOT survive in R'. Concrete\n"
        "  counterexample to verdict preservation under extension for\n"
        "  complement operators, justifying Remark 2's exclusion of\n"
        "  c_neq from Proposition 1.\n"
        "\n"
        "  The denotation rule den_neq_R_prime requires both\n"
        "  in_concepts_R_prime(X) AND ~grounded_as_R_prime(X, g). The\n"
        "  concept-membership guard is essential — without it, any\n"
        "  Skolem term outside the concept set could be a hallucinated\n"
        "  witness.\n"
        "\n"
        "SMT cross-check: assert R-facts and extension. Witness bcp_es\n"
        "  satisfies both denotations. Expected: sat."
    ),
    "ttl": _TTL_PREFIX + """
drk:offer_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:language ;
    odrl:operator odrl:neq ;
    odrl:rightOperand bcp:de
  ] .

drk:request_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:language ;
    odrl:operator odrl:neq ;
    odrl:rightOperand bcp:fr
  ] .

# BOUNDARY audit: Remark 2 (complement operators).
#   R: {bcp_de, bcp_fr}; c_neq pair is Conflict (no shared concept).
#   R': R + {bcp_es}; bcp_es satisfies both complements.
#   Conjecture verdict_compatible_R_prime asserts the R'-Compatible
#   verdict; witness bcp_es. Expected: Theorem.
""",
    "fof_extra_decls": _fof_two_resource_lifts() + """\

% ============================================================
% den_neq lifted to R and R' with concept-membership guard.
% Concept-membership is essential because the denotation is
% the complement of the concept set: without the guard, the
% prover could hallucinate Skolem witnesses outside the resource.
% ============================================================
fof(den_neq_R, axiom,
    ![X, G]:
      (in_denotation_R(X, c_neq(G)) <=>
       (in_concepts_R(X) & ~grounded_as_R(X, G)))).

fof(den_neq_R_prime, axiom,
    ![X, G]:
      (in_denotation_R_prime(X, c_neq(G)) <=>
       (in_concepts_R_prime(X) & ~grounded_as_R_prime(X, G)))).

% ============================================================
% R-facts: BCP47-shaped registry with exactly two concepts.
% ============================================================
fof(r_de_in_concepts, axiom,
    in_concepts_R(bcp_de)).

fof(r_fr_in_concepts, axiom,
    in_concepts_R(bcp_fr)).

fof(r_de_grounded, axiom,
    grounded_as_R(bcp_de, bcp_de)).

fof(r_fr_grounded, axiom,
    grounded_as_R(bcp_fr, bcp_fr)).

fof(r_distinct_de_fr, axiom,
    bcp_de != bcp_fr).

% ============================================================
% R' extension: add concept bcp_es. R-facts auto-lift via MONO000.
% ============================================================
fof(r_ext_es_in_concepts_prime, axiom,
    in_concepts_R_prime(bcp_es)).

fof(r_ext_es_not_in_concepts_R, axiom,
    ~in_concepts_R(bcp_es)).

fof(r_ext_es_grounded, axiom,
    grounded_as_R_prime(bcp_es, bcp_es)).

% bcp_es grounds to itself and is distinct from de and fr,
% so it is NOT grounded as de or fr.
fof(r_ext_es_not_grounded_de, axiom,
    ~grounded_as_R_prime(bcp_es, bcp_de)).

fof(r_ext_es_not_grounded_fr, axiom,
    ~grounded_as_R_prime(bcp_es, bcp_fr)).

fof(r_ext_distinct_es_de, axiom,
    bcp_es != bcp_de).

fof(r_ext_distinct_es_fr, axiom,
    bcp_es != bcp_fr).
""",
    "fof_conjecture":
        "verdict_compatible_R_prime(c_neq(bcp_de), c_neq(bcp_fr))",
    "smt2_logic": "UF",
    "smt2_decls": """\
; KGC810 SMT cross-check: complement counterexample.
""" + _smt2_two_resource_prelude() + """\

(declare-fun grounded_as_R       (Concept Concept) Bool)
(declare-fun grounded_as_R_prime (Concept Concept) Bool)

(assert (forall ((c Concept) (g Concept))
    (=> (grounded_as_R c g) (grounded_as_R_prime c g))))

(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)
(declare-fun bcp_es () Concept)""",
    "smt2_asserts": """\
; ============================================================
; R-facts
; ============================================================
(assert (in_concepts_R bcp_de))
(assert (in_concepts_R bcp_fr))
(assert (grounded_as_R bcp_de bcp_de))
(assert (grounded_as_R bcp_fr bcp_fr))

; ============================================================
; R' extension: bcp_es is R'-only, grounded to itself.
; ============================================================
(assert (in_concepts_R_prime bcp_es))
(assert (not (in_concepts_R bcp_es)))
(assert (grounded_as_R_prime bcp_es bcp_es))
(assert (not (grounded_as_R_prime bcp_es bcp_de)))
(assert (not (grounded_as_R_prime bcp_es bcp_fr)))

; ============================================================
; Distinctness
; ============================================================
(assert (distinct bcp_de bcp_fr bcp_es))

; ============================================================
; Witness bcp_es is in [c_neq(de)]_R' (concept, ~grounded as de) AND
; [c_neq(fr)]_R' (concept, ~grounded as fr). Resource is consistent.
; Expected: sat.""",
}
# KGC811: BOUNDARY — retraction counterexample (Remark 3)
# R: {de, fr} with kge_disjoint(de, fr)
# R'': retract kge_disjoint(de, fr) (NOT an extension; retraction)
#   This violates Proposition 1's hypothesis that no axiom is retracted.
# Encoding: don't lift disjoint_R to disjoint_R_prime for this case
#   (problem-locally, omit closure for this specific fact).
# Conjecture: verdict_conflict_R_prime(c_eq(de), c_eq(fr)). Expected: CSA.
# Demonstrates Proposition 1 fails under retraction.
#
# KGC812: BOUNDARY — Assumption 1 violation
# R': adds kge_disjoint_R_prime(de, fr) AND leq_R_prime(de_subtype, de)
#     AND leq_R_prime(de_subtype, fr) — internally inconsistent under
#     the KGE000 propagation axiom.
# Conjecture: $false. Expected: Theorem.
# Demonstrates the framework correctly rejects inconsistent extensions.

KGC812 ={
    "id":            "KGC812",
    "subdir":        "Monotonicity",
    "name":          "Proposition 1: Assumption 1 violation [boundary — inconsistent extension]",
    "relation":      "monotonicity",
    "verdict":       "MonotonicityAssumption1Boundary",
    "status_fof":    "Theorem",
    "status_smt":    "unsat",
    "difficulty":    "Medium",
    "includes":      [
        "MONO000-0.ax",
    ],
    "needs_density": False,
    "description": (
        "Proposition 1 (Monotonicity) BOUNDARY audit: extensions\n"
        "violating Assumption 1 (disjointness propagation coherence)\n"
        "are correctly detected as inconsistent.\n"
        "\n"
        "Setup:\n"
        "  R: BCP47-like, with two concepts and asserted disjointness.\n"
        "    in_concepts_R(bcp_de), in_concepts_R(bcp_fr).\n"
        "    disjoint_R(bcp_de, bcp_fr).\n"
        "\n"
        "Extension R' (Assumption 1 violation):\n"
        "  Add concept bcp_z (R'-only) with subsumption edges to BOTH\n"
        "  bcp_de AND bcp_fr:\n"
        "    leq_R_prime(bcp_z, bcp_de)\n"
        "    leq_R_prime(bcp_z, bcp_fr)\n"
        "  This violates Assumption 1: bcp_de and bcp_fr are\n"
        "  disjoint, but bcp_z is a common subordinate. The\n"
        "  propagation axiom kge_disjoint_propagation_R_prime forces\n"
        "  contradiction.\n"
        "\n"
        "Conjecture: $false.\n"
        "Expected: Theorem.\n"
        "\n"
        "Why: closure axiom extension_disjoint lifts disjoint_R(de, fr)\n"
        "  to disjoint_R_prime(de, fr). The R'-axioms include both\n"
        "  leq_R_prime(z, de) and leq_R_prime(z, fr). The propagation\n"
        "  axiom in R' (kge_disjoint_propagation_R_prime) states that\n"
        "  this configuration is impossible, deriving $false.\n"
        "\n"
        "  This audit demonstrates that the framework correctly\n"
        "  rejects inconsistent extensions: an evaluator hitting this\n"
        "  configuration knows immediately that Assumption 1 has been\n"
        "  violated by the resource update.\n"
        "\n"
        "SMT cross-check: same configuration. Expected: unsat."
    ),
    "ttl": _TTL_PREFIX + """
drk:context a odrl:Asset .

# BOUNDARY audit: Assumption 1 violation.
#   R: {bcp_de, bcp_fr} with kge_disjoint(de, fr).
#   R': R + {bcp_z} with leq_R_prime(z, de) AND leq_R_prime(z, fr).
#   This is internally inconsistent: a common subordinate of two
#   disjoint concepts violates Assumption 1.
#   Conjecture: $false. Expected: Theorem (inconsistency detected).
""",
    "fof_extra_decls": _fof_two_resource_lifts() + """\

% ============================================================
% R-facts: BCP47-like, two disjoint concepts.
% ============================================================
fof(r_de_in_concepts, axiom,
    in_concepts_R(bcp_de)).

fof(r_fr_in_concepts, axiom,
    in_concepts_R(bcp_fr)).

fof(r_de_disjoint_fr, axiom,
    disjoint_R(bcp_de, bcp_fr)).

fof(r_distinct_de_fr, axiom,
    bcp_de != bcp_fr).

% ============================================================
% R' extension: ASSUMPTION 1 VIOLATION
% Add bcp_z as a common subordinate of two disjoint concepts.
% This is internally inconsistent under the kge_disjoint_propagation
% axiom, which the framework expects to detect.
% ============================================================
fof(r_ext_z_in_concepts_prime, axiom,
    in_concepts_R_prime(bcp_z)).

fof(r_ext_z_not_in_concepts_R, axiom,
    ~in_concepts_R(bcp_z)).

fof(r_ext_z_leq_de_prime, axiom,
    leq_R_prime(bcp_z, bcp_de)).

fof(r_ext_z_leq_fr_prime, axiom,
    leq_R_prime(bcp_z, bcp_fr)).

fof(r_ext_distinct_z_de, axiom,
    bcp_z != bcp_de).

fof(r_ext_distinct_z_fr, axiom,
    bcp_z != bcp_fr).
""",
    "fof_conjecture": "$false",
    "smt2_logic": "UF",
    "smt2_decls": """\
; KGC812 SMT cross-check: Assumption 1 violation.
""" + _smt2_two_resource_prelude() + """\

; ============================================================
; Concrete constants for KGC812
; ============================================================
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)
(declare-fun bcp_z  () Concept)""",
    "smt2_asserts": """\
; ============================================================
; R-facts: two disjoint concepts.
; ============================================================
(assert (in_concepts_R bcp_de))
(assert (in_concepts_R bcp_fr))
(assert (disjoint_R bcp_de bcp_fr))

; ============================================================
; R' extension: ASSUMPTION 1 VIOLATION
; bcp_z is a common subordinate of two disjoint concepts.
; ============================================================
(assert (in_concepts_R_prime bcp_z))
(assert (not (in_concepts_R bcp_z)))
(assert (leq_R_prime bcp_z bcp_de))
(assert (leq_R_prime bcp_z bcp_fr))

; ============================================================
; Distinctness
; ============================================================
(assert (distinct bcp_de bcp_fr bcp_z))

; Closure axiom + propagation axiom in R' force unsat.
; Expected: unsat.""",
}
PROBLEMS = [
    KGC800, KGC801, KGC802,        # Conflict preservation (3 extension types)
    KGC803, KGC804, KGC805,        # Compatible preservation (3 extension types)
    KGC806, KGC807, KGC808,        # Denotation growth (3 extension types)
    KGC810, KGC812,                # Boundary cases (Remark 2, Assumption 1)
]

