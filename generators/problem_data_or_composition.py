"""
problem_data_or_composition.py
==============================

Theorem 5 audit (or-fragment): Composition Soundness via cross-disjunct
decomposition (Proposition~\\ref{prop:cross-disjunct}, paper Section 4.3).

Proposition 2 states: for constraint sets in the and/or fragment with
DNF expansions or(d_1, ..., d_n) and or(d'_1, ..., d'_m), rule-level
Conflict iff every cross-pair (d_i, d'_j) has disjunct-level Conflict.
Definition 9 (rule-level verdict) extends this with Compatible iff some
cross-pair has Compatible, Unknown otherwise.

This module produces three problems exercising the three branches:

  KGC710 -- or-Conflict: every cross-pair has disjunct-Conflict.
            All cross-pairs atomic-Conflict via BCP47 registry uniqueness.
            Conjecture: rule_or(r1, r2) = conflict.
            Style A. Expected FOF: Theorem.

  KGC711 -- or-Compatible: some cross-pair has disjunct-Compatible.
            One cross-pair witnesses a common satisfier (matching tag).
            Conjecture: rule_or(r1, r2) = compatible.
            Style A. Expected FOF: Theorem.

  KGC712 -- or-Unknown: no Compatible, not all Conflict.
            Single-disjunct each side; cross-pair atomic-Unknown
            (asserted as premise per OWA non-derivability, as in
            KGC702 and KGC706).
            Conjecture: rule_or(r1, r2) = unknown.
            Style A. Expected FOF: Theorem.

KGC713 (xone conservative reduction) is added separately and reuses
the same encoding by appealing to the paper's xone footnote: for
xone(c_1, ..., c_n) vs c', rule-level Conflict iff every (c_k, c')
has Conflict, which is exactly rule_or applied to the DNF expansion
of xone.

Each problem instantiates COMPOSE001's predicates (has_disjunct,
disjunct_conflict, disjunct_compat) from the atomic verdicts of the
disjunct-level constraints. For single-atomic disjuncts, the bridges
reduce to verdict_compatible/verdict_conflict on the atomic constraint
pair.
"""

# ---------------------------------------------------------------------------
# Shared TTL header.
# ---------------------------------------------------------------------------
_TTL_PREFIX = """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix bcp:  <https://tools.ietf.org/html/bcp47#> .
@prefix dpv:  <https://w3id.org/dpv#> .
@prefix gn:   <https://www.geonames.org/ontology#> .
@prefix gnf:  <https://sws.geonames.org/> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
"""


PROBLEMS = [
    # =====================================================================
    # KGC710 -- or-Conflict: all cross-pairs have disjunct-Conflict.
    # =====================================================================
    {
        "id":            "KGC710",
        "subdir":        "Composition",
        "name":          "Proposition 2 (or): all cross-pairs Conflict [BCP47]",
        "relation":      "composition",
        "verdict":       "OrConflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "includes":      [
            "KGE000-0.ax",
            "DENOT000-0.ax",
            "COMPOSE000-0.ax",
            "COMPOSE001-0.ax",
            "BCP47000-0.ax",
        ],
        "needs_density": False,
        "description": (
            "Proposition~\\ref{prop:cross-disjunct} or-Conflict.\n"
            "Two or-composed rules whose every cross-pair has\n"
            "disjunct-level Conflict; rule_or(r1, r2) = conflict.\n"
            "\n"
            "Setup:\n"
            "  CS  = or(d1, d2):\n"
            "    d1  = (language, eq, bcp:de)\n"
            "    d2  = (language, eq, bcp:fr)\n"
            "  CS' = or(d1p):\n"
            "    d1p = (language, eq, bcp:it)\n"
            "\n"
            "Cross-pairs:\n"
            "  (d1, d1p): bcp:de vs bcp:it -- disjoint by BCP47 registry\n"
            "    uniqueness; atomic-level B1 fires; disjunct_conflict.\n"
            "  (d2, d1p): bcp:fr vs bcp:it -- disjoint; disjunct_conflict.\n"
            "\n"
            "Both cross-pairs Conflict, so by Proposition 2,\n"
            "rule_or(r1, r2) = conflict.\n"
            "\n"
            "Conjecture (Style A): rule_or(r1, r2) = conflict.\n"
            "Expected: Theorem."
        ),
        "ttl": _TTL_PREFIX + """
drk:offer_rule a odrl:Permission ;
  odrl:constraint [
    odrl:operator odrl:or ;
    odrl:rightOperand (
      [ odrl:leftOperand odrl:language ; odrl:operator odrl:eq ;
        odrl:rightOperand bcp:de ]
      [ odrl:leftOperand odrl:language ; odrl:operator odrl:eq ;
        odrl:rightOperand bcp:fr ]
    )
  ] .

drk:request_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:language ;
    odrl:operator odrl:eq ;
    odrl:rightOperand bcp:it
  ] .
# Proposition 2 or-Conflict:
#   r1 = or(d1=eq:de, d2=eq:fr); r2 = eq:it.
#   Both cross-pairs are atomic-Conflict (BCP47 registry uniqueness).
#   rule_or(r1, r2) = conflict.
""",
        "fof_extra_decls": """\
% --- Disjunct membership ---
fof(r1_disjunct_d1,  axiom, has_disjunct(r1, d1)).
fof(r1_disjunct_d2,  axiom, has_disjunct(r1, d2)).
fof(r2_disjunct_d1p, axiom, has_disjunct(r2, d1p)).

fof(r1_closure, axiom,
    ![D]: (has_disjunct(r1, D) <=> (D = d1 | D = d2))).
fof(r2_closure, axiom,
    ![D]: (has_disjunct(r2, D) <=> D = d1p)).

fof(disjuncts_distinct, axiom,
    d1 != d2 & d1 != d1p & d2 != d1p).

% --- Atomic-level constraint denotations per disjunct ---
fof(c_d1_defined, axiom, ~denotation_undef(c_d1)).
fof(c_d1_den, axiom,
    ![X]: (in_denotation(X, c_d1) <=> den_eq(X, bcp_de))).

fof(c_d2_defined, axiom, ~denotation_undef(c_d2)).
fof(c_d2_den, axiom,
    ![X]: (in_denotation(X, c_d2) <=> den_eq(X, bcp_fr))).

fof(c_d1p_defined, axiom, ~denotation_undef(c_d1p)).
fof(c_d1p_den, axiom,
    ![X]: (in_denotation(X, c_d1p) <=> den_eq(X, bcp_it))).

% --- Disjunct-pair Conflict bridges ---
% Each disjunct is a single atomic constraint, so disjunct-level
% Conflict reduces to atomic verdict_conflict on the constraint pair.
fof(d1_d1p_conflict_bridge, axiom,
    (disjunct_conflict(d1, d1p) <=> verdict_conflict(c_d1, c_d1p))).
fof(d2_d1p_conflict_bridge, axiom,
    (disjunct_conflict(d2, d1p) <=> verdict_conflict(c_d2, c_d1p))).
""",
        "fof_conjecture": "rule_or(r1, r2) = conflict",
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)
(declare-fun bcp_it () Concept)
(declare-fun kge_disjoint (Concept Concept) Bool)""",
        "smt2_asserts": """\
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
(assert (forall ((c Concept)) (not (kge_disjoint c c))))
; BCP47 registry uniqueness.
(assert (kge_disjoint bcp_de bcp_it))
(assert (kge_disjoint bcp_fr bcp_it))
(assert (distinct bcp_de bcp_fr bcp_it))
;
; SMT cross-check: a request would have to satisfy r1 (lang in {de, fr})
; AND r2 (lang = it). Both constraints distinct from it; unsat.
(declare-fun req_lang () Concept)
(assert (or (= req_lang bcp_de) (= req_lang bcp_fr)))
(assert (= req_lang bcp_it))""",
    },

    # =====================================================================
    # KGC711 -- or-Compatible: some cross-pair has disjunct-Compatible.
    # =====================================================================
    {
        "id":            "KGC711",
        "subdir":        "Composition",
        "name":          "Proposition 2 (or): one cross-pair Compatible [BCP47]",
        "relation":      "composition",
        "verdict":       "OrCompatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "includes":      [
            "KGE000-0.ax",
            "DENOT000-0.ax",
            "COMPOSE000-0.ax",
            "COMPOSE001-0.ax",
            "BCP47000-0.ax",
        ],
        "needs_density": False,
        "description": (
            "Proposition~\\ref{prop:cross-disjunct} or-Compatible.\n"
            "One cross-pair has disjunct-level Compatible (matching\n"
            "language tag); rule_or(r1, r2) = compatible.\n"
            "\n"
            "Setup:\n"
            "  CS  = or(d1, d2):\n"
            "    d1  = (language, eq, bcp:de)\n"
            "    d2  = (language, eq, bcp:fr)\n"
            "  CS' = or(d1p):\n"
            "    d1p = (language, eq, bcp:de)\n"
            "\n"
            "Cross-pairs:\n"
            "  (d1, d1p): bcp:de vs bcp:de -- same tag; witness bcp_de;\n"
            "    disjunct_compat.\n"
            "  (d2, d1p): bcp:fr vs bcp:de -- BCP47 disjoint;\n"
            "    disjunct_conflict (irrelevant for the verdict here).\n"
            "\n"
            "By Proposition 2, some cross-pair Compatible suffices:\n"
            "rule_or(r1, r2) = compatible.\n"
            "\n"
            "Conjecture (Style A): rule_or(r1, r2) = compatible.\n"
            "Expected: Theorem."
        ),
        "ttl": _TTL_PREFIX + """
drk:offer_rule a odrl:Permission ;
  odrl:constraint [
    odrl:operator odrl:or ;
    odrl:rightOperand (
      [ odrl:leftOperand odrl:language ; odrl:operator odrl:eq ;
        odrl:rightOperand bcp:de ]
      [ odrl:leftOperand odrl:language ; odrl:operator odrl:eq ;
        odrl:rightOperand bcp:fr ]
    )
  ] .

drk:request_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:language ;
    odrl:operator odrl:eq ;
    odrl:rightOperand bcp:de
  ] .
# Proposition 2 or-Compatible:
#   r1 = or(d1=eq:de, d2=eq:fr); r2 = eq:de.
#   Cross-pair (d1, d1p) is Compatible (witness bcp_de).
#   rule_or(r1, r2) = compatible.
""",
        "fof_extra_decls": """\
% --- Disjunct membership ---
fof(r1_disjunct_d1,  axiom, has_disjunct(r1, d1)).
fof(r1_disjunct_d2,  axiom, has_disjunct(r1, d2)).
fof(r2_disjunct_d1p, axiom, has_disjunct(r2, d1p)).

fof(r1_closure, axiom,
    ![D]: (has_disjunct(r1, D) <=> (D = d1 | D = d2))).
fof(r2_closure, axiom,
    ![D]: (has_disjunct(r2, D) <=> D = d1p)).

fof(disjuncts_distinct, axiom,
    d1 != d2 & d1 != d1p & d2 != d1p).

% --- Atomic-level constraint denotations per disjunct ---
fof(c_d1_defined, axiom, ~denotation_undef(c_d1)).
fof(c_d1_den, axiom,
    ![X]: (in_denotation(X, c_d1) <=> den_eq(X, bcp_de))).

fof(c_d2_defined, axiom, ~denotation_undef(c_d2)).
fof(c_d2_den, axiom,
    ![X]: (in_denotation(X, c_d2) <=> den_eq(X, bcp_fr))).

fof(c_d1p_defined, axiom, ~denotation_undef(c_d1p)).
fof(c_d1p_den, axiom,
    ![X]: (in_denotation(X, c_d1p) <=> den_eq(X, bcp_de))).

% --- Disjunct-pair Compatible bridges ---
fof(d1_d1p_compat_bridge, axiom,
    (disjunct_compat(d1, d1p) <=> verdict_compatible(c_d1, c_d1p))).
fof(d2_d1p_compat_bridge, axiom,
    (disjunct_compat(d2, d1p) <=> verdict_compatible(c_d2, c_d1p))).
""",
        "fof_conjecture": "rule_or(r1, r2) = compatible",
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)
(declare-fun kge_disjoint (Concept Concept) Bool)""",
        "smt2_asserts": """\
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
(assert (forall ((c Concept)) (not (kge_disjoint c c))))
(assert (kge_disjoint bcp_de bcp_fr))
(assert (distinct bcp_de bcp_fr))
;
; Witness: req_lang = bcp_de satisfies both d1 (in or for r1) and
; d1p (= bcp_de for r2). rule_or = compatible. Z3 returns sat.
(declare-fun req_lang () Concept)
(assert (or (= req_lang bcp_de) (= req_lang bcp_fr)))
(assert (= req_lang bcp_de))""",
    },

    # =====================================================================
    # KGC712 -- or-Unknown: cross-pair atomic-Unknown (premise).
    # =====================================================================
    {
        "id":            "KGC712",
        "subdir":        "Composition",
        "name":          "Proposition 2 (or): Unknown propagation [DPV]",
        "relation":      "composition",
        "verdict":       "OrUnknown",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "includes":      [
            "KGE000-0.ax",
            "DENOT000-0.ax",
            "COMPOSE000-0.ax",
            "COMPOSE001-0.ax",
            "DPV000-0.ax",
        ],
        "needs_density": False,
        "description": (
            "Proposition~\\ref{prop:cross-disjunct} or-Unknown propagation.\n"
            "Single-disjunct each side; the cross-pair is atomic-Unknown\n"
            "(DPV silent on the relevant pair). Asserted as a premise\n"
            "since OWA-Unknown is not positively derivable in FOL\n"
            "(see KGC702/706 audit notes; atomic Unknown audited at\n"
            "KGC412).\n"
            "\n"
            "Setup:\n"
            "  CS  = or(d1):\n"
            "    d1  = (purpose, isA, dpv:NonCommercialPurpose)\n"
            "  CS' = or(d1p):\n"
            "    d1p = (purpose, eq, dpv:ScientificResearch)\n"
            "\n"
            "Cross-pair (d1, d1p): DPV asserts neither a skos:broader\n"
            "edge nor disjointness between ScientificResearch and\n"
            "NonCommercialPurpose; atomic verdict is Unknown.\n"
            "\n"
            "No cross-pair is disjunct_compat; not every cross-pair is\n"
            "disjunct_conflict; so by Proposition 2 and the rule-level\n"
            "verdict definition, rule_or(r1, r2) = unknown.\n"
            "\n"
            "Conjecture (Style A): rule_or(r1, r2) = unknown.\n"
            "Expected: Theorem."
        ),
        "ttl": _TTL_PREFIX + """
drk:offer_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:isA ;
    odrl:rightOperand dpv:NonCommercialPurpose
  ] .

drk:request_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:ScientificResearch
  ] .
# Proposition 2 or-Unknown:
#   r1 = or(d1=isA:NonCommercialPurpose); r2 = or(d1p=eq:ScientificResearch).
#   Cross-pair (d1, d1p) atomic-Unknown (DPV silent).
#   rule_or(r1, r2) = unknown.
""",
        "fof_extra_decls": """\
% --- Disjunct membership (single disjunct each side) ---
fof(r1_disjunct_d1,  axiom, has_disjunct(r1, d1)).
fof(r2_disjunct_d1p, axiom, has_disjunct(r2, d1p)).

fof(r1_closure, axiom,
    ![D]: (has_disjunct(r1, D) <=> D = d1)).
fof(r2_closure, axiom,
    ![D]: (has_disjunct(r2, D) <=> D = d1p)).

fof(disjuncts_distinct, axiom,
    d1 != d1p).

% --- Atomic-level constraint denotations per disjunct ---
fof(c_d1_defined, axiom, ~denotation_undef(c_d1)).
fof(c_d1_den, axiom,
    ![X]: (in_denotation(X, c_d1) <=>
              den_isa(X, dpv_non_commercial_purpose))).

fof(c_d1p_defined, axiom, ~denotation_undef(c_d1p)).
fof(c_d1p_den, axiom,
    ![X]: (in_denotation(X, c_d1p) <=>
              den_eq(X, dpv_scientific_research))).

% --- Atomic-level Unknown asserted as premise ---
% OWA non-derivability for verdict_unknown; see KGC702/706 audit notes
% and atomic audit KGC412.
fof(d1_d1p_atomic_unknown, axiom,
    verdict_unknown(c_d1, c_d1p)).

% --- Disjunct-pair verdict bridges ---
% Single-atomic disjuncts: disjunct verdicts mirror atomic verdicts.
fof(d1_d1p_compat_bridge, axiom,
    (disjunct_compat(d1, d1p) <=> verdict_compatible(c_d1, c_d1p))).
fof(d1_d1p_conflict_bridge, axiom,
    (disjunct_conflict(d1, d1p) <=> verdict_conflict(c_d1, c_d1p))).
""",
        "fof_conjecture": "rule_or(r1, r2) = unknown",
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun dpv_non_commercial_purpose () Concept)
(declare-fun dpv_scientific_research    () Concept)
(declare-fun kge_leq      (Concept Concept) Bool)
(declare-fun kge_disjoint (Concept Concept) Bool)""",
        "smt2_asserts": """\
(assert (forall ((c Concept)) (kge_leq c c)))
(assert (forall ((a Concept) (b Concept) (c Concept))
    (=> (and (kge_leq a b) (kge_leq b c)) (kge_leq a c))))
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
; DPV: no edge or disjointness between SR and NonCommercial.
(assert (distinct dpv_non_commercial_purpose dpv_scientific_research))
;
; Atomic-level Unknown verdict lives in FOL via verdict_unknown_def
; in DENOT000.  SMT side confirms resource consistency only.""",
    },
    # =====================================================================
    # KGC713 -- xone conservative reduction: xone-Conflict via or-Conflict.
    # =====================================================================
    {
        "id":            "KGC713",
        "subdir":        "Composition",
        "name":          "xone conservative reduction: xone-Conflict via or-Conflict [BCP47]",
        "relation":      "composition",
        "verdict":       "XoneConflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "includes":      [
            "KGE000-0.ax",
            "DENOT000-0.ax",
            "COMPOSE000-0.ax",
            "COMPOSE001-0.ax",
            "BCP47000-0.ax",
        ],
        "needs_density": False,
        "description": (
            "xone conservative reduction (paper Section 4.3 footnote):\n"
            "xone-Conflict is taken as or-Conflict over the same\n"
            "disjuncts, since xone-satisfaction implies or-satisfaction.\n"
            "If every cross-pair has atomic-Conflict, no request\n"
            "satisfies any xone-disjunct alongside c'.\n"
            "\n"
            "Setup:\n"
            "  CS  = xone(c1, c2, c3):\n"
            "    c1 = (language, eq, bcp:de)\n"
            "    c2 = (language, eq, bcp:fr)\n"
            "    c3 = (language, eq, bcp:es)\n"
            "  CS' = (language, eq, bcp:it).\n"
            "\n"
            "Conservative reduction: treat xone-rule's disjuncts as\n"
            "or-disjuncts for the purpose of Conflict detection.\n"
            "Disjunct membership for r1 includes d1, d2, d3.\n"
            "\n"
            "Cross-pairs:\n"
            "  (d1, d1p): bcp:de vs bcp:it -- BCP47 disjoint; Conflict.\n"
            "  (d2, d1p): bcp:fr vs bcp:it -- BCP47 disjoint; Conflict.\n"
            "  (d3, d1p): bcp:es vs bcp:it -- BCP47 disjoint; Conflict.\n"
            "\n"
            "All three cross-pairs Conflict; by Proposition 2 applied\n"
            "to the conservative or-reduction of xone, rule_or = conflict.\n"
            "\n"
            "This problem reuses the or-encoding (rule_or, has_disjunct,\n"
            "disjunct_conflict) without new axioms, in line with the\n"
            "paper's claim that xone-Conflict requires no machinery\n"
            "beyond or.\n"
            "\n"
            "Conjecture (Style A): rule_or(r1, r2) = conflict.\n"
            "Expected: Theorem."
        ),
        "ttl": _TTL_PREFIX + """
drk:offer_rule a odrl:Permission ;
  odrl:constraint [
    odrl:operator odrl:xone ;
    odrl:rightOperand (
      [ odrl:leftOperand odrl:language ; odrl:operator odrl:eq ;
        odrl:rightOperand bcp:de ]
      [ odrl:leftOperand odrl:language ; odrl:operator odrl:eq ;
        odrl:rightOperand bcp:fr ]
      [ odrl:leftOperand odrl:language ; odrl:operator odrl:eq ;
        odrl:rightOperand bcp:es ]
    )
  ] .

drk:request_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:language ;
    odrl:operator odrl:eq ;
    odrl:rightOperand bcp:it
  ] .
# xone conservative reduction:
#   r1 = xone(d1=eq:de, d2=eq:fr, d3=eq:es); r2 = eq:it.
#   xone-Conflict reduces to or-Conflict over the same disjuncts.
#   All three cross-pairs are atomic-Conflict (BCP47 registry uniqueness).
#   rule_or(r1, r2) = conflict.
""",
        "fof_extra_decls": """\
% --- Disjunct membership (xone treated as or for Conflict reduction) ---
fof(r1_disjunct_d1,  axiom, has_disjunct(r1, d1)).
fof(r1_disjunct_d2,  axiom, has_disjunct(r1, d2)).
fof(r1_disjunct_d3,  axiom, has_disjunct(r1, d3)).
fof(r2_disjunct_d1p, axiom, has_disjunct(r2, d1p)).

fof(r1_closure, axiom,
    ![D]: (has_disjunct(r1, D) <=> (D = d1 | D = d2 | D = d3))).
fof(r2_closure, axiom,
    ![D]: (has_disjunct(r2, D) <=> D = d1p)).

fof(disjuncts_distinct, axiom,
    d1 != d2 & d1 != d3 & d2 != d3 &
    d1 != d1p & d2 != d1p & d3 != d1p).

% --- Atomic-level constraint denotations per disjunct ---
fof(c_d1_defined, axiom, ~denotation_undef(c_d1)).
fof(c_d1_den, axiom,
    ![X]: (in_denotation(X, c_d1) <=> den_eq(X, bcp_de))).

fof(c_d2_defined, axiom, ~denotation_undef(c_d2)).
fof(c_d2_den, axiom,
    ![X]: (in_denotation(X, c_d2) <=> den_eq(X, bcp_fr))).

fof(c_d3_defined, axiom, ~denotation_undef(c_d3)).
fof(c_d3_den, axiom,
    ![X]: (in_denotation(X, c_d3) <=> den_eq(X, bcp_es))).

fof(c_d1p_defined, axiom, ~denotation_undef(c_d1p)).
fof(c_d1p_den, axiom,
    ![X]: (in_denotation(X, c_d1p) <=> den_eq(X, bcp_it))).

% --- Disjunct-pair Conflict bridges ---
fof(d1_d1p_conflict_bridge, axiom,
    (disjunct_conflict(d1, d1p) <=> verdict_conflict(c_d1, c_d1p))).
fof(d2_d1p_conflict_bridge, axiom,
    (disjunct_conflict(d2, d1p) <=> verdict_conflict(c_d2, c_d1p))).
fof(d3_d1p_conflict_bridge, axiom,
    (disjunct_conflict(d3, d1p) <=> verdict_conflict(c_d3, c_d1p))).
""",
        "fof_conjecture": "rule_or(r1, r2) = conflict",
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)
(declare-fun bcp_es () Concept)
(declare-fun bcp_it () Concept)
(declare-fun kge_disjoint (Concept Concept) Bool)""",
        "smt2_asserts": """\
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
(assert (forall ((c Concept)) (not (kge_disjoint c c))))
; BCP47 registry uniqueness.
(assert (kge_disjoint bcp_de bcp_it))
(assert (kge_disjoint bcp_fr bcp_it))
(assert (kge_disjoint bcp_es bcp_it))
(assert (distinct bcp_de bcp_fr bcp_es bcp_it))
;
; SMT cross-check: a request satisfying r1's xone (any one of the three
; disjuncts) AND r2 (= bcp_it) must equal one of {de, fr, es} AND it.
; All three cases conflict with it; unsat.
(declare-fun req_lang () Concept)
(assert (or (= req_lang bcp_de)
            (= req_lang bcp_fr)
            (= req_lang bcp_es)))
(assert (= req_lang bcp_it))""",
    },
]