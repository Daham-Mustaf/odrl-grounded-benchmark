"""
problem_data_operators.py
=========================

Per-operator audit grid for Theorem 1 (operand-level conflict
detection).  Every monotone operator in the single-valued fragment
is exercised against each of the three verdicts (Conflict, Compatible,
Unknown), plus complement operators tested for Conflict and Compatible
(Unknown is not audited for complement operators because it does not
arise naturally when resource distinctness is fully declared).

Operators (single-valued fragment, paper Section 2.2):
  Monotone:   eq, isA, isPartOf, hasPart, isAnyOf
  Complement: neq, isNoneOf

Operator isAllOf is omitted: it collapses to isAnyOf for single-valued
left operands.

Resource choice per cell follows what the verdict requires:
  - Conflict cells (monotone) need asserted disjointness
       -> BCP 47 (only resource asserting disjointness)
  - Conflict cells (complement) require no disjointness; B3/B4 patterns
    fire structurally.  We use BCP 47 for parallelism with the eq cell.
  - Compatible cells need a witness
       -> any resource where one exists
  - Unknown cells need silence
       -> DPV or GeoNames (no disjointness asserted)

KGC430 (hasPart / Conflict) is expected to return CounterSatisfiable
in FOF: it exceeds the certification fragment of forced_empty's
current pattern set (B1 downward-pair, B2 list-vs-eq, B3 neq-vs-eq,
B4 isNoneOf-vs-eq), none of which covers upward cones. The hand-rolled
SMT encoding bypasses forced_empty and certifies the conflict directly
via kge_disjoint_propagation; Z3 and cvc5 both return unsat. KGC430
therefore documents the remaining FOF-encoding gap relative to
Definition 7, not a fundamental incompleteness of the
conflict-detection approach.

KGC440 (isAnyOf / Conflict) was previously in this same gap. The
B2 (list-vs-eq) pattern added to DENOT000-0.ax certifies it: when
each list member is asserted disjoint from the request value
(BCP 47 registry uniqueness), forced_empty fires by Assumption 1
applied pointwise. All five FOF provers now derive Theorem.

KGC450 (neq / Conflict) and KGC460 (isNoneOf / Conflict) use the
B3 and B4 patterns added in DENOT000-0.ax v1.3. Both fire structurally
without requiring resource-level disjointness assertions: the
denotation of c_neq(g) excludes g by definition, and c_isnoneof(S)
excludes every list member. When paired with c_eq targeting the
excluded element, the intersection is empty by construction.

Numbering: KGC4{op}{verdict}, where:
  op:      0=eq, 1=isA, 2=isPartOf, 3=hasPart, 4=isAnyOf,
           5=neq, 6=isNoneOf
  verdict: 0=Conflict, 1=Compatible, 2=Unknown
           (verdict 2 omitted for op=5, op=6 -- see header note above)
"""

# ---------------------------------------------------------------------------
# Shared TTL header used by all rows; row-specific constraints follow.
# ---------------------------------------------------------------------------
_TTL_PREFIX = """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix bcp:  <https://tools.ietf.org/html/bcp47#> .
@prefix dpv:  <https://w3id.org/dpv#> .
@prefix gn:   <https://www.geonames.org/ontology#> .
@prefix gnf:  <https://sws.geonames.org/> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
"""


def _ttl(left_operand: str, op_offer: str, val_offer: str,
         op_request: str, val_request: str) -> str:
    """Render a minimal two-rule policy TTL for one row."""
    return _TTL_PREFIX + f"""
drk:policyOffer a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand odrl:{left_operand} ;
      odrl:operator odrl:{op_offer} ;
      odrl:rightOperand {val_offer}
    ]
  ] .

drk:policyRequest a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand odrl:{left_operand} ;
      odrl:operator odrl:{op_request} ;
      odrl:rightOperand {val_request}
    ]
  ] .
"""


# ---------------------------------------------------------------------------
# Per-row constraint denotation hooks.
# Each generator returns the fof_extra_decls block.
# ---------------------------------------------------------------------------
def _fof_decls(offer_den: str, request_den: str) -> str:
    """Standard decls: undef guards + denotation bridges."""
    return f"""\
% Constraint tokens: defined denotations.
fof(c_offer_defined,   axiom, ~denotation_undef(c_offer)).
fof(c_request_defined, axiom, ~denotation_undef(c_request)).

% Denotations
fof(c_offer_den,   axiom,
    ![X]: (in_denotation(X, c_offer)   <=> {offer_den})).
fof(c_request_den, axiom,
    ![X]: (in_denotation(X, c_request) <=> {request_den})).
"""


# ---------------------------------------------------------------------------
# 5 x 3 operator grid.  Each row is one TPTP problem.
# Note: writers.py adds (check-sat) automatically; do NOT include it
# in smt2_asserts below.
# ---------------------------------------------------------------------------
PROBLEMS = [

    # =====================================================================
    # eq row: KGC400 (Conflict), KGC401 (Compatible), KGC402 (Unknown)
    # =====================================================================

    {
        "id":            "KGC400",
        "subdir":        "Conflict",
        "name":          "eq / Conflict: bcp:de x bcp:fr",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      ["KGE000-0.ax", "DENOT000-0.ax", "BCP47000-0.ax"],
        "needs_density": False,
        "description": (
            "eq operator, Conflict verdict.  BCP 47 asserts\n"
            "kge_disjoint(bcp_de, bcp_fr); the eq/eq pair has empty\n"
            "intersection forced by registry uniqueness."
        ),
        "ttl": _ttl("language", "eq", "bcp:de", "eq", "bcp:fr"),
        "fof_extra_decls": _fof_decls(
            "den_eq(X, bcp_de)",
            "den_eq(X, bcp_fr)",
        ),
        "fof_conjecture": "verdict_conflict(c_offer, c_request)",
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)
(declare-fun kge_disjoint (Concept Concept) Bool)""",
        "smt2_asserts": """\
; KGE000: disjointness symmetry/irreflexivity.
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
(assert (forall ((c Concept)) (not (kge_disjoint c c))))
; BCP47000: registry uniqueness.
(assert (kge_disjoint bcp_de bcp_fr))
(assert (distinct bcp_de bcp_fr))
; Negation of Conflict: witness x in both eq denotations.
(declare-fun x () Concept)
(assert (= x bcp_de))
(assert (= x bcp_fr))""",
    },

    {
        "id":            "KGC401",
        "subdir":        "Conflict",
        "name":          "eq / Compatible: bcp:de x bcp:de",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "includes":      ["KGE000-0.ax", "DENOT000-0.ax", "BCP47000-0.ax"],
        "needs_density": False,
        "description": (
            "eq operator, Compatible verdict.  Both sides ground to\n"
            "bcp_de; reflexivity gives a witness."
        ),
        "ttl": _ttl("language", "eq", "bcp:de", "eq", "bcp:de"),
        "fof_extra_decls": _fof_decls(
            "den_eq(X, bcp_de)",
            "den_eq(X, bcp_de)",
        ),
        "fof_conjecture": "verdict_compatible(c_offer, c_request)",
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun bcp_de () Concept)""",
        "smt2_asserts": """\
(declare-fun x () Concept)
(assert (= x bcp_de))""",
    },

    {
        "id":            "KGC402",
        "subdir":        "Conflict",
        "name":          "eq / Unknown: dpv:ScientificResearch x dpv:CommercialResearch",
        "relation":      "conflict",
        "verdict":       "Unknown",
        "status_fof":    "CounterSatisfiable",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "includes":      ["KGE000-0.ax", "DENOT000-0.ax", "DPV000-0.ax"],
        "needs_density": False,
        "description": (
            "eq operator, Unknown verdict.  DPV asserts neither equality\n"
            "nor disjointness between ScientificResearch and\n"
            "CommercialResearch directly; OWA leaves the verdict open.\n"
            "\n"
            "FOF side: Vampire returns CounterSatisfiable - verdict_unknown\n"
            "is not derivable as a theorem under OWA.\n"
            "SMT side: Z3 returns sat - the axioms have a model where\n"
            "neither Compatible nor Conflict is forced."
        ),
        "ttl": _ttl("purpose",
                    "eq", "dpv:ScientificResearch",
                    "eq", "dpv:CommercialResearch"),
        "fof_extra_decls": _fof_decls(
            "den_eq(X, dpv_scientific_research)",
            "den_eq(X, dpv_commercial_research)",
        ),
        "fof_conjecture": "verdict_unknown(c_offer, c_request)",
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun dpv_scientific_research      () Concept)
(declare-fun dpv_commercial_research      () Concept)
(declare-fun dpv_research_and_development () Concept)
(declare-fun kge_leq      (Concept Concept) Bool)
(declare-fun kge_disjoint (Concept Concept) Bool)""",
        "smt2_asserts": """\
; KGE000 load-bearing axioms.
(assert (forall ((c Concept)) (kge_leq c c)))
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
(assert (forall ((c Concept)) (not (kge_disjoint c c))))
(assert (forall ((a Concept) (b Concept) (z Concept))
    (=> (and (kge_disjoint a b) (kge_leq z a) (kge_leq z b))
        false)))
; DPV asserts both concepts share the parent ResearchAndDevelopment,
; but NEITHER ScientificResearch <= CommercialResearch NOR disjointness.
(assert (kge_leq dpv_scientific_research dpv_research_and_development))
(assert (kge_leq dpv_commercial_research dpv_research_and_development))
; Identity (the three concepts are distinct as IRIs).
(assert (distinct dpv_scientific_research
                  dpv_commercial_research
                  dpv_research_and_development))""",
    },

    # =====================================================================
    # isA row: KGC410 (Conflict), KGC411 (Compatible), KGC412 (Unknown)
    # =====================================================================

    {
        "id":            "KGC410",
        "subdir":        "Conflict",
        "name":          "isA / Conflict: isA bcp:de x eq bcp:fr",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      ["KGE000-0.ax", "DENOT000-0.ax", "BCP47000-0.ax"],
        "needs_density": False,
        "description": (
            "isA operator, Conflict verdict.  Offer's downward cone of\n"
            "bcp_de contains only bcp_de (flat registry); request is\n"
            "{bcp_fr}; bcp_de disjoint bcp_fr forces empty intersection."
        ),
        "ttl": _ttl("language", "isA", "bcp:de", "eq", "bcp:fr"),
        "fof_extra_decls": _fof_decls(
            "den_isa(X, bcp_de)",
            "den_eq(X, bcp_fr)",
        ),
        "fof_conjecture": "verdict_conflict(c_offer, c_request)",
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)
(declare-fun kge_leq      (Concept Concept) Bool)
(declare-fun kge_disjoint (Concept Concept) Bool)""",
        "smt2_asserts": """\
; KGE000: reflexivity, disjointness symmetry/irreflexivity, propagation.
(assert (forall ((c Concept)) (kge_leq c c)))
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
(assert (forall ((c Concept)) (not (kge_disjoint c c))))
(assert (forall ((a Concept) (b Concept) (z Concept))
    (=> (and (kge_disjoint a b) (kge_leq z a) (kge_leq z b))
        false)))
; BCP47000: registry uniqueness.
(assert (kge_disjoint bcp_de bcp_fr))
(assert (distinct bcp_de bcp_fr))
; Negation of Conflict: witness x in both denotations.
; [[c_offer]]   = downward cone of bcp_de (isA)
; [[c_request]] = {bcp_fr}
(declare-fun x () Concept)
(assert (kge_leq x bcp_de))
(assert (= x bcp_fr))""",
    },

    {
        "id":            "KGC411",
        "subdir":        "Conflict",
        "name":          "isA / Compatible: isA dpv:Purpose x eq dpv:ScientificResearch",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "includes":      ["KGE000-0.ax", "DENOT000-0.ax", "DPV000-0.ax"],
        "needs_density": False,
        "description": (
            "isA operator, Compatible verdict.  Offer's downward cone\n"
            "of dpv:Purpose contains every DPV purpose; request's\n"
            "ScientificResearch is one such purpose, providing a witness."
        ),
        "ttl": _ttl("purpose",
                    "isA", "dpv:Purpose",
                    "eq", "dpv:ScientificResearch"),
        "fof_extra_decls": _fof_decls(
            "den_isa(X, dpv_purpose)",
            "den_eq(X, dpv_scientific_research)",
        ),
        "fof_conjecture": "verdict_compatible(c_offer, c_request)",
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun dpv_purpose () Concept)
(declare-fun dpv_scientific_research () Concept)
(declare-fun kge_leq (Concept Concept) Bool)""",
        "smt2_asserts": """\
; DPV: ScientificResearch <= Purpose (transitive closure stand-in).
(assert (kge_leq dpv_scientific_research dpv_purpose))
(declare-fun x () Concept)
(assert (= x dpv_scientific_research))
(assert (kge_leq x dpv_purpose))""",
    },

    {
        "id":            "KGC412",
        "subdir":        "Conflict",
        "name":          "isA / Unknown: isA dpv:NonCommercialPurpose x eq dpv:ScientificResearch",
        "relation":      "conflict",
        "verdict":       "Unknown",
        "status_fof":    "CounterSatisfiable",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "includes":      ["KGE000-0.ax", "DENOT000-0.ax", "DPV000-0.ax"],
        "needs_density": False,
        "description": (
            "isA operator, Unknown verdict.  This is the motivating\n"
            "example's purpose pair: DPV silent on ScientificResearch\n"
            "<= NonCommercialPurpose; OWA gives Unknown."
        ),
        "ttl": _ttl("purpose",
                    "isA", "dpv:NonCommercialPurpose",
                    "eq", "dpv:ScientificResearch"),
        "fof_extra_decls": _fof_decls(
            "den_isa(X, dpv_non_commercial_purpose)",
            "den_eq(X, dpv_scientific_research)",
        ),
        "fof_conjecture": "verdict_unknown(c_offer, c_request)",
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun dpv_non_commercial_purpose () Concept)
(declare-fun dpv_scientific_research    () Concept)
(declare-fun kge_leq      (Concept Concept) Bool)
(declare-fun kge_disjoint (Concept Concept) Bool)""",
        "smt2_asserts": """\
; KGE000 load-bearing axioms.
(assert (forall ((c Concept)) (kge_leq c c)))
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
(assert (forall ((c Concept)) (not (kge_disjoint c c))))
(assert (forall ((a Concept) (b Concept) (z Concept))
    (=> (and (kge_disjoint a b) (kge_leq z a) (kge_leq z b))
        false)))
; DPV silence on (NCP, SR): no leq, no disjointness.
(assert (distinct dpv_non_commercial_purpose dpv_scientific_research))""",
    },

    # =====================================================================
    # isPartOf row: KGC420 (Conflict), KGC421 (Compatible), KGC422 (Unknown)
    # =====================================================================

    {
        "id":            "KGC420",
        "subdir":        "Conflict",
        "name":          "isPartOf / Conflict: isPartOf bcp:de x eq bcp:fr",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      ["KGE000-0.ax", "DENOT000-0.ax", "BCP47000-0.ax"],
        "needs_density": False,
        "description": (
            "isPartOf operator, Conflict verdict.  Same as isA Conflict\n"
            "(both are downward cones); paper Definition 4 collapses\n"
            "the operators."
        ),
        "ttl": _ttl("language", "isPartOf", "bcp:de", "eq", "bcp:fr"),
        "fof_extra_decls": _fof_decls(
            "den_ispartof(X, bcp_de)",
            "den_eq(X, bcp_fr)",
        ),
        "fof_conjecture": "verdict_conflict(c_offer, c_request)",
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)
(declare-fun kge_leq      (Concept Concept) Bool)
(declare-fun kge_disjoint (Concept Concept) Bool)""",
        "smt2_asserts": """\
; KGE000: reflexivity, disjointness symmetry/irreflexivity, propagation.
(assert (forall ((c Concept)) (kge_leq c c)))
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
(assert (forall ((c Concept)) (not (kge_disjoint c c))))
(assert (forall ((a Concept) (b Concept) (z Concept))
    (=> (and (kge_disjoint a b) (kge_leq z a) (kge_leq z b))
        false)))
; BCP47000: registry uniqueness.
(assert (kge_disjoint bcp_de bcp_fr))
(assert (distinct bcp_de bcp_fr))
; Negation of Conflict: witness x in both denotations.
; [[c_offer]]   = downward cone of bcp_de (isPartOf)
; [[c_request]] = {bcp_fr}
(declare-fun x () Concept)
(assert (kge_leq x bcp_de))
(assert (= x bcp_fr))""",
    },

    {
        "id":            "KGC421",
        "subdir":        "Conflict",
        "name":          "isPartOf / Compatible: isPartOf gn:Europe x eq gn:France",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "includes":      ["KGE000-0.ax", "DENOT000-0.ax", "GN000-0.ax"],
        "needs_density": False,
        "description": (
            "isPartOf operator, Compatible verdict.  Reuses the\n"
            "motivating example's spatial pair: France <= Europe\n"
            "by gn:parentFeature; France is the witness."
        ),
        "ttl": _ttl("spatial",
                    "isPartOf", "<https://sws.geonames.org/6255148/>",
                    "eq",       "<https://sws.geonames.org/3017382/>"),
        "fof_extra_decls": _fof_decls(
            "den_ispartof(X, gn_europe)",
            "den_eq(X, gn_france)",
        ),
        "fof_conjecture": "verdict_compatible(c_offer, c_request)",
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun gn_europe () Concept)
(declare-fun gn_france () Concept)
(declare-fun kge_leq (Concept Concept) Bool)""",
        "smt2_asserts": """\
(assert (kge_leq gn_france gn_europe))
(declare-fun x () Concept)
(assert (= x gn_france))
(assert (kge_leq x gn_europe))""",
    },

    {
        "id":            "KGC422",
        "subdir":        "Conflict",
        "name":          "isPartOf / Unknown: isPartOf gn:Germany x eq gn:Strasbourg",
        "relation":      "conflict",
        "verdict":       "Unknown",
        "status_fof":    "CounterSatisfiable",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "includes":      ["KGE000-0.ax", "DENOT000-0.ax", "GN000-0.ax"],
        "needs_density": False,
        "description": (
            "isPartOf operator, Unknown verdict.  GeoNames asserts neither\n"
            "Strasbourg <= Germany nor disjointness; OWA gives Unknown.\n"
            "(In closed-world geography, Strasbourg is in France, but\n"
            "GeoNames doesn't assert sibling-country disjointness.)"
        ),
        "ttl": _ttl("spatial",
                    "isPartOf", "<https://sws.geonames.org/2921044/>",
                    "eq",       "<https://sws.geonames.org/2973783/>"),
        "fof_extra_decls": _fof_decls(
            "den_ispartof(X, gn_germany)",
            "den_eq(X, gn_strasbourg)",
        ),
        "fof_conjecture": "verdict_unknown(c_offer, c_request)",
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun gn_germany    () Concept)
(declare-fun gn_strasbourg () Concept)
(declare-fun kge_leq      (Concept Concept) Bool)
(declare-fun kge_disjoint (Concept Concept) Bool)""",
        "smt2_asserts": """\
; KGE000 load-bearing axioms.
(assert (forall ((c Concept)) (kge_leq c c)))
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
(assert (forall ((c Concept)) (not (kge_disjoint c c))))
(assert (forall ((a Concept) (b Concept) (z Concept))
    (=> (and (kge_disjoint a b) (kge_leq z a) (kge_leq z b))
        false)))
; GeoNames silent on (Strasbourg, Germany): no parentFeature, no disjointness.
(assert (distinct gn_germany gn_strasbourg))""",
    },

    # =====================================================================
    # hasPart row: KGC430 (Conflict expected CSA - incompleteness),
    #              KGC431 (Compatible), KGC432 (Unknown)
    # =====================================================================

    {
        "id":            "KGC430",
        "subdir":        "Conflict",
        "name":          "hasPart / Conflict: hasPart bcp:de x eq bcp:fr",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "CounterSatisfiable",
        "status_smt":    "unsat",
        "difficulty":    "Hard",
        "includes":      ["KGE000-0.ax", "DENOT000-0.ax", "BCP47000-0.ax"],
        "needs_density": False,
        "description": (
            "hasPart operator, Conflict verdict. FOF-encoding incomplete,\n"
            "SMT-encoding complete.\n"
            "\n"
            "FOF side: hasPart denotes an upward cone of bcp_de.  Neither\n"
            "the B1 (downward-pair) nor the B2 (list-vs-eq) pattern in\n"
            "DENOT000-0.ax covers upward cones, so forced_empty does not\n"
            "fire.  Vampire and E return CounterSatisfiable.  This\n"
            "documents the remaining FOF-encoding gap relative to\n"
            "Definition 7.\n"
            "\n"
            "SMT side: the hand-rolled encoding bypasses forced_empty and\n"
            "uses kge_disjoint_propagation directly. With reflexivity\n"
            "kge_leq(bcp_de, bcp_de) and the witness assertion\n"
            "kge_leq(bcp_de, bcp_fr), propagation instantiated at\n"
            "(a=bcp_de, b=bcp_fr, z=bcp_de) derives false. Z3 and cvc5\n"
            "return unsat."
        ),
        "ttl": _ttl("language", "hasPart", "bcp:de", "eq", "bcp:fr"),
        "fof_extra_decls": _fof_decls(
            "den_haspart(X, bcp_de)",
            "den_eq(X, bcp_fr)",
        ),
        "fof_conjecture": "verdict_conflict(c_offer, c_request)",
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)
(declare-fun kge_leq      (Concept Concept) Bool)
(declare-fun kge_disjoint (Concept Concept) Bool)""",
        "smt2_asserts": """\
; KGE000 load-bearing axioms.
(assert (forall ((c Concept)) (kge_leq c c)))
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
(assert (forall ((c Concept)) (not (kge_disjoint c c))))
(assert (forall ((a Concept) (b Concept) (z Concept))
    (=> (and (kge_disjoint a b) (kge_leq z a) (kge_leq z b))
        false)))
; BCP47000: registry uniqueness.
(assert (kge_disjoint bcp_de bcp_fr))
(assert (distinct bcp_de bcp_fr))
; hasPart bcp_de denotes upward cone of bcp_de.
; eq bcp_fr denotes {bcp_fr}.
; Witness x: x is above bcp_de AND x = bcp_fr.
; After substitution: kge_leq(bcp_de, bcp_fr). Combined with reflexivity
; kge_leq(bcp_de, bcp_de) and kge_disjoint(bcp_de, bcp_fr), propagation
; instantiated at (a=bcp_de, b=bcp_fr, z=bcp_de) derives false. Unsat.
(declare-fun x () Concept)
(assert (kge_leq bcp_de x))
(assert (= x bcp_fr))""",
    },

    {
        "id":            "KGC431",
        "subdir":        "Conflict",
        "name":          "hasPart / Compatible: hasPart gn:France x eq gn:Europe",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "includes":      ["KGE000-0.ax", "DENOT000-0.ax", "GN000-0.ax"],
        "needs_density": False,
        "description": (
            "hasPart operator, Compatible verdict.  Offer's upward cone\n"
            "of France contains Europe (France <= Europe in GeoNames);\n"
            "Europe is the witness."
        ),
        "ttl": _ttl("spatial",
                    "hasPart", "<https://sws.geonames.org/3017382/>",
                    "eq",      "<https://sws.geonames.org/6255148/>"),
        "fof_extra_decls": _fof_decls(
            "den_haspart(X, gn_france)",
            "den_eq(X, gn_europe)",
        ),
        "fof_conjecture": "verdict_compatible(c_offer, c_request)",
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun gn_france () Concept)
(declare-fun gn_europe () Concept)
(declare-fun kge_leq (Concept Concept) Bool)""",
        "smt2_asserts": """\
(assert (kge_leq gn_france gn_europe))
(declare-fun x () Concept)
(assert (= x gn_europe))
(assert (kge_leq gn_france x))""",
    },

    {
        "id":            "KGC432",
        "subdir":        "Conflict",
        "name":          "hasPart / Unknown: hasPart gn:Strasbourg x eq gn:Germany",
        "relation":      "conflict",
        "verdict":       "Unknown",
        "status_fof":    "CounterSatisfiable",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "includes":      ["KGE000-0.ax", "DENOT000-0.ax", "GN000-0.ax"],
        "needs_density": False,
        "description": (
            "hasPart operator, Unknown verdict.  Offer's upward cone of\n"
            "Strasbourg in GeoNames goes through Bas-Rhin -> Grand Est ->\n"
            "France -> Europe.  Germany is not on this chain, but\n"
            "GeoNames asserts no disjointness; OWA gives Unknown."
        ),
        "ttl": _ttl("spatial",
                    "hasPart", "<https://sws.geonames.org/2973783/>",
                    "eq",      "<https://sws.geonames.org/2921044/>"),
        "fof_extra_decls": _fof_decls(
            "den_haspart(X, gn_strasbourg)",
            "den_eq(X, gn_germany)",
        ),
        "fof_conjecture": "verdict_unknown(c_offer, c_request)",
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun gn_strasbourg () Concept)
(declare-fun gn_germany    () Concept)
(declare-fun kge_leq      (Concept Concept) Bool)
(declare-fun kge_disjoint (Concept Concept) Bool)""",
        "smt2_asserts": """\
; KGE000 load-bearing axioms.
(assert (forall ((c Concept)) (kge_leq c c)))
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
(assert (forall ((c Concept)) (not (kge_disjoint c c))))
(assert (forall ((a Concept) (b Concept) (z Concept))
    (=> (and (kge_disjoint a b) (kge_leq z a) (kge_leq z b))
        false)))
; GeoNames silent on relation; OWA gives Unknown.
(assert (distinct gn_strasbourg gn_germany))""",
    },

    # =====================================================================
    # isAnyOf row: KGC440 (Conflict expected CSA - incompleteness),
    #              KGC441 (Compatible), KGC442 (Unknown)
    # =====================================================================
    #
    # Note: in_list/2 is the problem-file hook for isAnyOf; each problem
    # asserts the membership facts directly.
    # =====================================================================

    {
        "id":            "KGC440",
        "subdir":        "Conflict",
        "name":          "isAnyOf / Conflict: isAnyOf {bcp:de, bcp:fr} x eq bcp:it",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      ["KGE000-0.ax", "DENOT000-0.ax", "BCP47000-0.ax"],
        "needs_density": False,
        "description": (
            "isAnyOf operator, Conflict verdict.  Offer's denotation is\n"
            "{bcp_de, bcp_fr}; request's is {bcp_it}.  BCP 47 asserts\n"
            "kge_disjoint pairwise across all language tags, so each list\n"
            "member is disjoint from bcp_it.  Pattern B2 (list-vs-eq) in\n"
            "DENOT000-0.ax fires: forced_empty(c_offer, c_request) follows\n"
            "from Assumption 1 applied pointwise to each list member.\n"
            "\n"
            "FOF side: all five provers derive verdict_conflict as Theorem.\n"
            "SMT side: Z3 and cvc5 return unsat via direct list-membership\n"
            "and pairwise-distinctness reasoning."
        ),
        "ttl": _TTL_PREFIX + """
drk:policyOffer a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand odrl:language ;
      odrl:operator odrl:isAnyOf ;
      odrl:rightOperand ( bcp:de bcp:fr )
    ]
  ] .

drk:policyRequest a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand odrl:language ;
      odrl:operator odrl:eq ;
      odrl:rightOperand bcp:it
    ]
  ] .
""",
        "fof_extra_decls": """\
% Constraint tokens: defined denotations.
fof(c_offer_defined,   axiom, ~denotation_undef(c_offer)).
fof(c_request_defined, axiom, ~denotation_undef(c_request)).

% List membership for isAnyOf {bcp_de, bcp_fr}.
fof(in_list_de, axiom, in_list(bcp_de, list_de_fr)).
fof(in_list_fr, axiom, in_list(bcp_fr, list_de_fr)).
fof(in_list_closed, axiom,
    ![X]: (in_list(X, list_de_fr) <=> (X = bcp_de | X = bcp_fr))).

% Denotations
fof(c_offer_den,   axiom,
    ![X]: (in_denotation(X, c_offer)   <=> den_isanyof(X, list_de_fr))).
fof(c_request_den, axiom,
    ![X]: (in_denotation(X, c_request) <=> den_eq(X, bcp_it))).
""",
        "fof_conjecture": "verdict_conflict(c_offer, c_request)",
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)
(declare-fun bcp_it () Concept)""",
        "smt2_asserts": """\
(assert (distinct bcp_de bcp_fr bcp_it))
(declare-fun x () Concept)
(assert (or (= x bcp_de) (= x bcp_fr)))
(assert (= x bcp_it))""",
    },

    {
        "id":            "KGC441",
        "subdir":        "Conflict",
        "name":          "isAnyOf / Compatible: isAnyOf {bcp:de, bcp:fr} x eq bcp:de",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "includes":      ["KGE000-0.ax", "DENOT000-0.ax", "BCP47000-0.ax"],
        "needs_density": False,
        "description": (
            "isAnyOf operator, Compatible verdict.  Offer's list contains\n"
            "bcp_de; request equals bcp_de; bcp_de is the witness."
        ),
        "ttl": _TTL_PREFIX + """
drk:policyOffer a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand odrl:language ;
      odrl:operator odrl:isAnyOf ;
      odrl:rightOperand ( bcp:de bcp:fr )
    ]
  ] .

drk:policyRequest a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand odrl:language ;
      odrl:operator odrl:eq ;
      odrl:rightOperand bcp:de
    ]
  ] .
""",
        "fof_extra_decls": """\
fof(c_offer_defined,   axiom, ~denotation_undef(c_offer)).
fof(c_request_defined, axiom, ~denotation_undef(c_request)).

fof(in_list_de, axiom, in_list(bcp_de, list_de_fr)).
fof(in_list_fr, axiom, in_list(bcp_fr, list_de_fr)).
fof(in_list_closed, axiom,
    ![X]: (in_list(X, list_de_fr) <=> (X = bcp_de | X = bcp_fr))).

fof(c_offer_den,   axiom,
    ![X]: (in_denotation(X, c_offer)   <=> den_isanyof(X, list_de_fr))).
fof(c_request_den, axiom,
    ![X]: (in_denotation(X, c_request) <=> den_eq(X, bcp_de))).
""",
        "fof_conjecture": "verdict_compatible(c_offer, c_request)",
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)""",
        "smt2_asserts": """\
(assert (distinct bcp_de bcp_fr))
(declare-fun x () Concept)
(assert (or (= x bcp_de) (= x bcp_fr)))
(assert (= x bcp_de))""",
    },

    {
        "id":            "KGC442",
        "subdir":        "Conflict",
        "name":          "isAnyOf / Unknown: isAnyOf {dpv:SR, dpv:CR} x eq dpv:NCP",
        "relation":      "conflict",
        "verdict":       "Unknown",
        "status_fof":    "CounterSatisfiable",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "includes":      ["KGE000-0.ax", "DENOT000-0.ax", "DPV000-0.ax"],
        "needs_density": False,
        "description": (
            "isAnyOf operator, Unknown verdict.  Offer's list is\n"
            "{ScientificResearch, CommercialResearch}; request is\n"
            "{NonCommercialPurpose}.  DPV asserts neither equality\n"
            "(witness) nor disjointness (forced); OWA gives Unknown."
        ),
        "ttl": _TTL_PREFIX + """
drk:policyOffer a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand odrl:purpose ;
      odrl:operator odrl:isAnyOf ;
      odrl:rightOperand ( dpv:ScientificResearch dpv:CommercialResearch )
    ]
  ] .

drk:policyRequest a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand odrl:purpose ;
      odrl:operator odrl:eq ;
      odrl:rightOperand dpv:NonCommercialPurpose
    ]
  ] .
""",
        "fof_extra_decls": """\
fof(c_offer_defined,   axiom, ~denotation_undef(c_offer)).
fof(c_request_defined, axiom, ~denotation_undef(c_request)).

fof(in_list_sr, axiom, in_list(dpv_scientific_research, list_sr_cr)).
fof(in_list_cr, axiom, in_list(dpv_commercial_research, list_sr_cr)).
fof(in_list_closed, axiom,
    ![X]: (in_list(X, list_sr_cr) <=>
            (X = dpv_scientific_research | X = dpv_commercial_research))).

fof(c_offer_den,   axiom,
    ![X]: (in_denotation(X, c_offer)   <=> den_isanyof(X, list_sr_cr))).
fof(c_request_den, axiom,
    ![X]: (in_denotation(X, c_request) <=> den_eq(X, dpv_non_commercial_purpose))).
""",
        "fof_conjecture": "verdict_unknown(c_offer, c_request)",
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun dpv_scientific_research    () Concept)
(declare-fun dpv_commercial_research    () Concept)
(declare-fun dpv_non_commercial_purpose () Concept)
(declare-fun kge_leq      (Concept Concept) Bool)
(declare-fun kge_disjoint (Concept Concept) Bool)""",
        "smt2_asserts": """\
; KGE000 load-bearing axioms.
(assert (forall ((c Concept)) (kge_leq c c)))
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
(assert (forall ((c Concept)) (not (kge_disjoint c c))))
(assert (forall ((a Concept) (b Concept) (z Concept))
    (=> (and (kge_disjoint a b) (kge_leq z a) (kge_leq z b))
        false)))
; DPV silent on these relations; OWA gives Unknown.
(assert (distinct dpv_scientific_research
                  dpv_commercial_research
                  dpv_non_commercial_purpose))""",
    },
# =====================================================================
    # neq row: KGC450 (Conflict), KGC451 (Compatible)
    # =====================================================================
    #
    # Note: Unknown is not audited for complement operators because it
    # does not arise naturally when resource distinctness is fully
    # declared (BCP 47 owl:AllDifferent, DPV distinct IRIs). For a
    # complement-vs-eq pair, the verdict is determined by whether the
    # eq value equals the excluded value (Conflict) or differs (Compatible).
    # =====================================================================
    {
        "id":            "KGC450",
        "subdir":        "Conflict",
        "name":          "neq / Conflict: neq bcp:de x eq bcp:de",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      ["KGE000-0.ax", "DENOT000-0.ax", "BCP47000-0.ax"],
        "needs_density": False,
        "description": (
            "neq operator, Conflict verdict.  Offer's denotation is\n"
            "C \\ {bcp_de} (every concept except bcp_de, restricted to\n"
            "the resource universe via kge_concept guard).  Request's\n"
            "denotation is {bcp_de}.  Intersection is empty by\n"
            "construction: the excluded value is exactly the eq target.\n"
            "Pattern B3 (neq-vs-eq) in DENOT000 fires structurally; no\n"
            "disjointness assertion is needed because the denotations\n"
            "are complementary by definition.\n"
            "\n"
            "FOF side: all five provers derive verdict_conflict as Theorem.\n"
            "SMT side: Z3 and cvc5 return unsat via direct denotation\n"
            "membership reasoning."
        ),
        "ttl": _ttl("language", "neq", "bcp:de", "eq", "bcp:de"),
        "fof_extra_decls": _fof_decls(
            "den_neq(X, bcp_de)",
            "den_eq(X, bcp_de)",
        ),
        "fof_conjecture": "verdict_conflict(c_offer, c_request)",
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun bcp_de () Concept)""",
        "smt2_asserts": """\
; Negation of Conflict: witness x in both denotations.
; [[c_offer]]   = C \\ {bcp_de}, so x must satisfy x != bcp_de
; [[c_request]] = {bcp_de}, so x must satisfy x = bcp_de
; These constraints are unsatisfiable; unsat is correct.
(declare-fun x () Concept)
(assert (distinct x bcp_de))
(assert (= x bcp_de))""",
    },
    {
        "id":            "KGC451",
        "subdir":        "Conflict",
        "name":          "neq / Compatible: neq bcp:de x eq bcp:fr",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "includes":      ["KGE000-0.ax", "DENOT000-0.ax", "BCP47000-0.ax"],
        "needs_density": False,
        "description": (
            "neq operator, Compatible verdict.  Offer's denotation is\n"
            "C \\ {bcp_de} (every concept except bcp_de).  Request's\n"
            "denotation is {bcp_fr}.  Witness: bcp_fr is in C \\ {bcp_de}\n"
            "(since bcp_fr != bcp_de by BCP 47 registry uniqueness) AND\n"
            "in {bcp_fr}, providing a common element.  The kge_concept\n"
            "guard is satisfied because bcp_fr is asserted as a concept\n"
            "in BCP47000."
        ),
        "ttl": _ttl("language", "neq", "bcp:de", "eq", "bcp:fr"),
        "fof_extra_decls": _fof_decls(
            "den_neq(X, bcp_de)",
            "den_eq(X, bcp_fr)",
        ),
        "fof_conjecture": "verdict_compatible(c_offer, c_request)",
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)""",
        "smt2_asserts": """\
(assert (distinct bcp_de bcp_fr))
(declare-fun x () Concept)
(assert (distinct x bcp_de))
(assert (= x bcp_fr))""",
    },
    # =====================================================================
    # isNoneOf row: KGC460 (Conflict), KGC461 (Compatible)
    # =====================================================================
    #
    # Note: in_list/2 is the problem-file hook for isNoneOf operands;
    # each problem asserts list membership directly.  Unknown is not
    # audited for the same reason as the neq row.
    # =====================================================================
    {
        "id":            "KGC460",
        "subdir":        "Conflict",
        "name":          "isNoneOf / Conflict: isNoneOf {bcp:de, bcp:fr} x eq bcp:de",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      ["KGE000-0.ax", "DENOT000-0.ax", "BCP47000-0.ax"],
        "needs_density": False,
        "description": (
            "isNoneOf operator, Conflict verdict.  Offer's denotation is\n"
            "C \\ {bcp_de, bcp_fr} (every concept except those on the\n"
            "list).  Request's denotation is {bcp_de}.  Since bcp_de\n"
            "is on the excluded list, it cannot be in offer's denotation,\n"
            "and the intersection is empty by construction.  Pattern B4\n"
            "(isNoneOf-vs-eq) in DENOT000 fires structurally.\n"
            "\n"
            "FOF side: all five provers derive verdict_conflict as Theorem.\n"
            "SMT side: Z3 and cvc5 return unsat via direct list-membership\n"
            "and complement reasoning."
        ),
        "ttl": _TTL_PREFIX + """
drk:policyOffer a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand odrl:language ;
      odrl:operator odrl:isNoneOf ;
      odrl:rightOperand ( bcp:de bcp:fr )
    ]
  ] .

drk:policyRequest a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand odrl:language ;
      odrl:operator odrl:eq ;
      odrl:rightOperand bcp:de
    ]
  ] .
""",
        "fof_extra_decls": """\
% Constraint tokens: defined denotations.
fof(c_offer_defined,   axiom, ~denotation_undef(c_offer)).
fof(c_request_defined, axiom, ~denotation_undef(c_request)).

% List membership for isNoneOf {bcp_de, bcp_fr}.
fof(in_list_de, axiom, in_list(bcp_de, list_de_fr)).
fof(in_list_fr, axiom, in_list(bcp_fr, list_de_fr)).
fof(in_list_closed, axiom,
    ![X]: (in_list(X, list_de_fr) <=> (X = bcp_de | X = bcp_fr))).

% Denotations
fof(c_offer_den,   axiom,
    ![X]: (in_denotation(X, c_offer)   <=> den_isnoneof(X, list_de_fr))).
fof(c_request_den, axiom,
    ![X]: (in_denotation(X, c_request) <=> den_eq(X, bcp_de))).
""",
        "fof_conjecture": "verdict_conflict(c_offer, c_request)",
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)""",
        "smt2_asserts": """\
(assert (distinct bcp_de bcp_fr))
; Negation of Conflict: witness x in both denotations.
; [[c_offer]]   = C \\ {bcp_de, bcp_fr}, so x must NOT be in the list
; [[c_request]] = {bcp_de}, so x = bcp_de
; bcp_de is on the excluded list; constraints unsatisfiable.
(declare-fun x () Concept)
(assert (and (distinct x bcp_de) (distinct x bcp_fr)))
(assert (= x bcp_de))""",
    },
    {
        "id":            "KGC461",
        "subdir":        "Conflict",
        "name":          "isNoneOf / Compatible: isNoneOf {bcp:de, bcp:fr} x eq bcp:it",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "includes":      ["KGE000-0.ax", "DENOT000-0.ax", "BCP47000-0.ax"],
        "needs_density": False,
        "description": (
            "isNoneOf operator, Compatible verdict.  Offer's denotation\n"
            "is C \\ {bcp_de, bcp_fr}.  Request's denotation is {bcp_it}.\n"
            "Witness: bcp_it is in C \\ {bcp_de, bcp_fr} (since bcp_it\n"
            "is distinct from both list members by BCP 47 registry\n"
            "uniqueness) AND in {bcp_it}, providing a common element."
        ),
        "ttl": _TTL_PREFIX + """
drk:policyOffer a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand odrl:language ;
      odrl:operator odrl:isNoneOf ;
      odrl:rightOperand ( bcp:de bcp:fr )
    ]
  ] .

drk:policyRequest a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand odrl:language ;
      odrl:operator odrl:eq ;
      odrl:rightOperand bcp:it
    ]
  ] .
""",
        "fof_extra_decls": """\
fof(c_offer_defined,   axiom, ~denotation_undef(c_offer)).
fof(c_request_defined, axiom, ~denotation_undef(c_request)).

fof(in_list_de, axiom, in_list(bcp_de, list_de_fr)).
fof(in_list_fr, axiom, in_list(bcp_fr, list_de_fr)).
fof(in_list_closed, axiom,
    ![X]: (in_list(X, list_de_fr) <=> (X = bcp_de | X = bcp_fr))).

fof(c_offer_den,   axiom,
    ![X]: (in_denotation(X, c_offer)   <=> den_isnoneof(X, list_de_fr))).
fof(c_request_den, axiom,
    ![X]: (in_denotation(X, c_request) <=> den_eq(X, bcp_it))).
""",
        "fof_conjecture": "verdict_compatible(c_offer, c_request)",
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)
(declare-fun bcp_it () Concept)""",
        "smt2_asserts": """\
(assert (distinct bcp_de bcp_fr bcp_it))
(declare-fun x () Concept)
(assert (and (distinct x bcp_de) (distinct x bcp_fr)))
(assert (= x bcp_it))""",
    },
]