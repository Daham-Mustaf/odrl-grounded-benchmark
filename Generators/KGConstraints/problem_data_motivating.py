"""
problem_data_motivating.py
==========================
Motivating-example problems from the paper (Section 3, Example 1).
Three constraint pairs across three different grounding resources, each
yielding a different verdict — together exhibiting the full three-valued
verdict space:

  KGC300 — language pair  (BCP 47, eq de × eq fr)         → Conflict
  KGC301 — purpose pair   (DPV, isA NCP × eq SR)          → Unknown
  KGC302 — spatial pair   (GeoNames, isPartOf EU × eq FR) → Compatible

These are the seed problems for KGConstraints. All three include
KGE000-0.ax + DENOT000-0.ax plus the relevant resource file.

Encoding choices:
  - Constraint tokens (c_offer, c_request) are ground constants.
  - Each problem ties its tokens to in_denotation via
    in_denotation(X, C) <=> den_<op>(X, G) per-problem axioms.
  - ~denotation_undef/1 is asserted per token: required by the
    verdict predicates' undef guards (DENOT000 Section C).
  - The conjecture is the verdict predicate (verdict_conflict /
    verdict_compatible / verdict_unknown).

Note on `needs_density`: a downstream-generator flag indicating whether
the problem requires the dense reflexive closure of leq beyond what
KGE000's leq_reflexive provides; false means base axioms suffice.
"""
PROBLEMS = [
    # ----------------------------------------------------------------
    # KGC300 — language: bcp:de _|_ bcp:fr -> Conflict
    # Paper: Example 1, language pair, Table 3 (Conflict)
    # Resource: BCP 47 (registry uniqueness from RFC 5646 § 2.2.1)
    # ----------------------------------------------------------------
    {
        "id":            "KGC300",
        "subdir":        "Conflict",
        "name":          "language: eq bcp:de x eq bcp:fr -> Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      ["KGE000-0.ax", "DENOT000-0.ax", "BCP47000-0.ax"],
        "needs_density": False,
        "description": (
            "Offer:   (language, eq, bcp:de) -> [[c_offer]]   = {bcp:de}\n"
            "Request: (language, eq, bcp:fr) -> [[c_request]] = {bcp:fr}\n"
            "BCP 47 asserts kge_disjoint(bcp_de, bcp_fr) (registry\n"
            "uniqueness, RFC 5646 sec 2.2.1) -> verdict_conflict(c_offer,\n"
            "c_request)  [def:conflict, motivating example]"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix bcp:  <https://tools.ietf.org/html/bcp47#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyOffer a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand odrl:language ;
      odrl:operator odrl:eq ;
      odrl:rightOperand bcp:de
    ]
  ] .

drk:policyRequest a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand odrl:language ;
      odrl:operator odrl:eq ;
      odrl:rightOperand bcp:fr
    ]
  ] .""",
        "fof_extra_decls": """\
% Constraint tokens: defined denotations (no grounding failure).
fof(c_offer_defined,   axiom, ~denotation_undef(c_offer)).
fof(c_request_defined, axiom, ~denotation_undef(c_request)).

% Denotations: eq operator
fof(c_offer_den,   axiom,
    ![X]: (in_denotation(X, c_offer)   <=> den_eq(X, bcp_de))).
fof(c_request_den, axiom,
    ![X]: (in_denotation(X, c_request) <=> den_eq(X, bcp_fr))).
""",
        "fof_conjecture": "verdict_conflict(c_offer, c_request)",
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)""",
        "smt2_asserts": """\
; Registry uniqueness: bcp_de and bcp_fr are distinct (kge_disjoint).
(assert (distinct bcp_de bcp_fr))
; Conflict claim: there is no concept X in both denotations.
; [[c_offer]]   = {bcp_de},  [[c_request]] = {bcp_fr}
; Negation: there exists X with X = bcp_de AND X = bcp_fr.
(declare-fun x () Concept)
(assert (= x bcp_de))
(assert (= x bcp_fr))""",
    },
    # ----------------------------------------------------------------
    # KGC301 — purpose: DPV silence on ScientificResearch <= NCP
    #          -> Unknown
    # Paper: Example 1, purpose pair, Table 3 (Unknown)
    # Resource: DPV (no disjointness, no chain to NonCommercialPurpose)
    # ----------------------------------------------------------------
    {
        "id":            "KGC301",
        "subdir":        "Conflict",
        "name":          "purpose: isA dpv:NonCommercialPurpose x eq dpv:ScientificResearch -> Unknown",
        "relation":      "conflict",
        "verdict":       "Unknown",
        "status_fof":    "CounterSatisfiable",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "includes":      ["KGE000-0.ax", "DENOT000-0.ax", "DPV000-0.ax"],
        "needs_density": False,
        "description": (
            "Offer:   (purpose, isA, dpv:NonCommercialPurpose)\n"
            "Request: (purpose, eq,  dpv:ScientificResearch)\n"
            "DPV asserts neither ScientificResearch <= NonCommercialPurpose\n"
            "NOR kge_disjoint between them. Open-world: silence is not\n"
            "evidence either way. The conjecture asks for verdict_unknown,\n"
            "which is not entailed (a model exists where SR <= NCP makes\n"
            "Compatible), so the expected status is CounterSatisfiable.\n"
            "[def:conflict, motivating example, OWA]"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix dpv:  <https://w3id.org/dpv#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyOffer a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand odrl:purpose ;
      odrl:operator odrl:isA ;
      odrl:rightOperand dpv:NonCommercialPurpose
    ]
  ] .

drk:policyRequest a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand odrl:purpose ;
      odrl:operator odrl:eq ;
      odrl:rightOperand dpv:ScientificResearch
    ]
  ] .""",
        "fof_extra_decls": """\
% Constraint tokens: defined denotations.
fof(c_offer_defined,   axiom, ~denotation_undef(c_offer)).
fof(c_request_defined, axiom, ~denotation_undef(c_request)).

% Denotations
fof(c_offer_den,   axiom,
    ![X]: (in_denotation(X, c_offer)   <=> den_isa(X, dpv_non_commercial_purpose))).
fof(c_request_den, axiom,
    ![X]: (in_denotation(X, c_request) <=> den_eq (X, dpv_scientific_research))).
""",
        "fof_conjecture": "verdict_unknown(c_offer, c_request)",
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun dpv_non_commercial_purpose () Concept)
(declare-fun dpv_scientific_research    () Concept)
(declare-fun kge_leq      (Concept Concept) Bool)
(declare-fun kge_disjoint (Concept Concept) Bool)""",
        "smt2_asserts": """\
; Reflexivity of leq.
(assert (kge_leq dpv_non_commercial_purpose dpv_non_commercial_purpose))
(assert (kge_leq dpv_scientific_research    dpv_scientific_research))
; DPV is silent on the relation between SR and NCP.
; Open-world: do NOT assert (not (kge_leq ...)) or (not (kge_disjoint ...)).
; Solver freely chooses; sat means the silence is consistent.
(check-sat)""",
    },
    # ----------------------------------------------------------------
    # KGC302 — spatial: gn:France <= gn:Europe -> Compatible
    # Paper: Example 1, spatial pair, Table 3 (Compatible)
    # Resource: GeoNames (parentFeature: France <= Europe)
    # ----------------------------------------------------------------
    {
        "id":            "KGC302",
        "subdir":        "Conflict",
        "name":          "spatial: isPartOf gn:Europe x eq gn:France -> Compatible",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "includes":      ["KGE000-0.ax", "DENOT000-0.ax", "GN000-0.ax"],
        "needs_density": False,
        "description": (
            "Offer:   (spatial, isPartOf, gn:Europe) -> [[c_offer]]   contains downward cone of gn:Europe\n"
            "Request: (spatial, eq,       gn:France) -> [[c_request]] = {gn:France}\n"
            "GeoNames asserts kge_leq(gn_france, gn_europe), so gn:France\n"
            "is in the offer's denotation: witness exists ->\n"
            "verdict_compatible(c_offer, c_request)\n"
            "[def:conflict, motivating example]"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix gn:   <https://www.geonames.org/ontology#> .
@prefix gnf:  <https://sws.geonames.org/> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyOffer a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand odrl:spatial ;
      odrl:operator odrl:isPartOf ;
      odrl:rightOperand <https://sws.geonames.org/6255148/>
    ]
  ] .

drk:policyRequest a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand odrl:spatial ;
      odrl:operator odrl:eq ;
      odrl:rightOperand <https://sws.geonames.org/3017382/>
    ]
  ] .""",
        "fof_extra_decls": """\
% Constraint tokens: defined denotations.
fof(c_offer_defined,   axiom, ~denotation_undef(c_offer)).
fof(c_request_defined, axiom, ~denotation_undef(c_request)).

% Denotations
fof(c_offer_den,   axiom,
    ![X]: (in_denotation(X, c_offer)   <=> den_ispartof(X, gn_europe))).
fof(c_request_den, axiom,
    ![X]: (in_denotation(X, c_request) <=> den_eq      (X, gn_france))).
""",
        "fof_conjecture": "verdict_compatible(c_offer, c_request)",
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun gn_europe () Concept)
(declare-fun gn_france () Concept)
(declare-fun kge_leq (Concept Concept) Bool)""",
        "smt2_asserts": """\
; Reflexivity.
(assert (kge_leq gn_france gn_france))
(assert (kge_leq gn_europe gn_europe))
; GeoNames: France parentFeature Europe -> kge_leq(gn_france, gn_europe).
(assert (kge_leq gn_france gn_europe))
; Compatible: a witness x exists in both denotations.
(declare-fun x () Concept)
(assert (= x gn_france))
(assert (kge_leq x gn_europe))""",
    },
]