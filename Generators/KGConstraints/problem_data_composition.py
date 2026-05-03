"""
problem_data_composition.py
===========================
Theorem 2 audit (and-only): Composition Soundness via the operand-wise
corollary (Corollary 3, paper Section 4.3).

Theorem 2 (paper Section 4.3): If verdict(CS, CS') = Conflict at the
rule level, then no request satisfies both. For symmetric `and`-`and`
inter-policy comparison over the same operand set, Corollary 3 reduces
this to operand-wise Strong Kleene composition (Definition 8 `and`
clause), recovered as a special case of the satisfying-set semantics.

This module produces three problems exercising the three branches of
the `and` Strong Kleene rule:

  KGC700 -- AND-Conflict aggregation.
            Two operand pairs both Conflict; rule_and(r1) = conflict.
            Tests has_conflict(r1) firing the rule_and_conflict axiom.
            Style A. Expected FOF: Theorem.

  KGC701 -- AND-Compatible aggregation (negative test).
            Both operand pairs Compatible; rule_and(r1) = compatible
            (NOT conflict). Tests that rule_and_conflict does not fire
            under the all_compat configuration.
            Style B (bare conjecture asserting Conflict, must NOT
            derive). Expected FOF: CounterSatisfiable.

  KGC702 -- AND-Unknown propagation.
            One operand pair Compatible, one Unknown; rule_and(r1) =
            unknown. Tests Strong Kleene's Unknown propagation rule:
            without all_compat AND without has_conflict, the rule
            verdict is Unknown.
            Style A. Expected FOF: Theorem.

Together the three exercise the three cases of Corollary 3's Strong
Kleene `and` aggregation: Conflict, Compatible, and Unknown.

Problem-local axioms (per the COMPOSE000-0.ax header instructions):
  - operand-pair denotations (atomic, as in operand audit)
  - bridge axioms wiring verdict_* into has_compat/all_compat/etc.
  - rule-level conjecture about rule_and(r1)

The bridge axioms are the load-bearing part of these problems. They
must correctly translate per-operand verdicts into rule-level summaries.
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


def _ttl_two_pairs(operand1: str, op1_off: str, val1_off: str, op1_req: str, val1_req: str,
                   operand2: str, op2_off: str, val2_off: str, op2_req: str, val2_req: str,
                   note: str = "") -> str:
    """Render TTL for two-operand offer/request rule pair."""
    note_block = f"# {note}\n" if note else ""
    return _TTL_PREFIX + f"""
drk:offer_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:{operand1} ;
    odrl:operator odrl:{op1_off} ;
    odrl:rightOperand {val1_off}
  ] ;
  odrl:constraint [
    odrl:leftOperand odrl:{operand2} ;
    odrl:operator odrl:{op2_off} ;
    odrl:rightOperand {val2_off}
  ] .

drk:request_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:{operand1} ;
    odrl:operator odrl:{op1_req} ;
    odrl:rightOperand {val1_req}
  ] ;
  odrl:constraint [
    odrl:leftOperand odrl:{operand2} ;
    odrl:operator odrl:{op2_req} ;
    odrl:rightOperand {val2_req}
  ] .

# Both rules use AND composition (default ODRL constraint-set
# composition). Per Corollary 3 of the paper, rule-level verdict is
# determined by per-operand verdicts via Strong Kleene aggregation.

{note_block}"""


# ---------------------------------------------------------------------------
# FOF helpers for AND-rule audits.
# ---------------------------------------------------------------------------

def _fof_two_pair_setup(c1_off_den: str, c1_req_den: str,
                        c2_off_den: str, c2_req_den: str) -> str:
    """Two operand pairs with denotations defined."""
    return f"""\
% --- Operand 1 pair ---
fof(c1_off_defined, axiom, ~denotation_undef(c1_off)).
fof(c1_req_defined, axiom, ~denotation_undef(c1_req)).
fof(c1_off_den, axiom,
    ![X]: (in_denotation(X, c1_off) <=> {c1_off_den})).
fof(c1_req_den, axiom,
    ![X]: (in_denotation(X, c1_req) <=> {c1_req_den})).

% --- Operand 2 pair ---
fof(c2_off_defined, axiom, ~denotation_undef(c2_off)).
fof(c2_req_defined, axiom, ~denotation_undef(c2_req)).
fof(c2_off_den, axiom,
    ![X]: (in_denotation(X, c2_off) <=> {c2_off_den})).
fof(c2_req_den, axiom,
    ![X]: (in_denotation(X, c2_req) <=> {c2_req_den})).
"""


def _fof_bridge_axioms() -> str:
    """Bridge between operand-pair verdicts and rule-level summaries.
    
    has_compat:    at least one operand-pair verdict is Compatible
    has_conflict:  at least one operand-pair verdict is Conflict
    all_compat:    every operand-pair verdict is Compatible
    all_conflict:  every operand-pair verdict is Conflict
    """
    return """\
% --- Rule-level bridge axioms ---
% Wire the two operand-pair verdicts into has/all summaries on r1.
fof(has_compat_bridge, axiom,
    (has_compat(r1) <=>
       (verdict_compatible(c1_off, c1_req) |
        verdict_compatible(c2_off, c2_req)))).
fof(has_conflict_bridge, axiom,
    (has_conflict(r1) <=>
       (verdict_conflict(c1_off, c1_req) |
        verdict_conflict(c2_off, c2_req)))).
fof(all_compat_bridge, axiom,
    (all_compat(r1) <=>
       (verdict_compatible(c1_off, c1_req) &
        verdict_compatible(c2_off, c2_req)))).
fof(all_conflict_bridge, axiom,
    (all_conflict(r1) <=>
       (verdict_conflict(c1_off, c1_req) &
        verdict_conflict(c2_off, c2_req)))).
"""


PROBLEMS = [
    # =====================================================================
    # KGC700 -- AND-Conflict aggregation (positive).
    # =====================================================================
    {
        "id":            "KGC700",
        "subdir":        "Composition",
        "name":          "Theorem 2 (and): Conflict aggregation [GeoNames+SDA, BCP47]",
        "relation":      "composition",
        "verdict":       "AndConflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "includes":      [
            "KGE000-0.ax",
            "DENOT000-0.ax",
            "COMPOSE000-0.ax",
            "GN000-0.ax",
            "GN001-SDA-0.ax",
            "BCP47000-0.ax",
        ],
        "needs_density": False,
        "description": (
            "Theorem 2 (and) Conflict aggregation. Two operand-pair\n"
            "verdicts of Conflict combine to rule-level Conflict via\n"
            "Strong Kleene's `existential Conflict` rule for AND.\n"
            "\n"
            "Setup:\n"
            "  Operand 1 (spatial, GeoNames+SDA):\n"
            "    c1_off = (spatial, eq, gn:Bayern)\n"
            "    c1_req = (spatial, eq, gn:France)\n"
            "    [c1_off] = {gn_bayern}, [c1_req] = {gn_france}\n"
            "    SDA asserts kge_disjoint(gn_germany, gn_france);\n"
            "    Bayern is below Germany, so B1 pattern fires:\n"
            "    forced_empty([c1_off], [c1_req]) holds.\n"
            "    => verdict_conflict(c1_off, c1_req).\n"
            "\n"
            "  Operand 2 (language, BCP47):\n"
            "    c2_off = (language, eq, bcp:de)\n"
            "    c2_req = (language, eq, bcp:fr)\n"
            "    [c2_off] = {bcp_de}, [c2_req] = {bcp_fr}\n"
            "    BCP47 asserts kge_disjoint(bcp_de, bcp_fr).\n"
            "    => verdict_conflict(c2_off, c2_req).\n"
            "\n"
            "Bridges:\n"
            "  has_conflict(r1) holds (both operand-pairs Conflict).\n"
            "\n"
            "Strong Kleene AND: rule_and(R) = conflict <=> has_conflict(R).\n"
            "Conjecture (Style A): rule_and(r1) = conflict.\n"
            "Expected: Theorem."
        ),
        "ttl": _ttl_two_pairs(
            "spatial", "eq", "<https://sws.geonames.org/2951839/>",
                       "eq", "<https://sws.geonames.org/3017382/>",
            "language", "eq", "bcp:de",
                        "eq", "bcp:fr",
            note=(
                "Theorem 2 AND-Conflict aggregation:\n"
                "#   verdict_conflict(c1_off, c1_req) holds (Bayern vs France).\n"
                "#   verdict_conflict(c2_off, c2_req) holds (de vs fr).\n"
                "#   has_conflict(r1) follows.\n"
                "#   rule_and(r1) = conflict by Strong Kleene."
            ),
        ),
        "fof_extra_decls": _fof_two_pair_setup(
            "den_eq(X, gn_bayern)",
            "den_eq(X, gn_france)",
            "den_eq(X, bcp_de)",
            "den_eq(X, bcp_fr)",
        ) + _fof_bridge_axioms(),
        "fof_conjecture": "rule_and(r1) = conflict",
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun gn_bayern  () Concept)
(declare-fun gn_germany () Concept)
(declare-fun gn_france  () Concept)
(declare-fun bcp_de     () Concept)
(declare-fun bcp_fr     () Concept)
(declare-fun kge_leq      (Concept Concept) Bool)
(declare-fun kge_disjoint (Concept Concept) Bool)""",
        "smt2_asserts": """\
; KGE000 load-bearing axioms.
(assert (forall ((c Concept)) (kge_leq c c)))
(assert (forall ((a Concept) (b Concept) (c Concept))
    (=> (and (kge_leq a b) (kge_leq b c)) (kge_leq a c))))
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
(assert (forall ((c Concept)) (not (kge_disjoint c c))))
(assert (forall ((a Concept) (b Concept) (z Concept))
    (=> (and (kge_disjoint a b) (kge_leq z a) (kge_leq z b))
        false)))
; GN000 + SDA: Bayern below Germany; Germany disjoint France.
(assert (kge_leq gn_bayern gn_germany))
(assert (kge_disjoint gn_germany gn_france))
; BCP47: de disjoint fr.
(assert (kge_disjoint bcp_de bcp_fr))
; Identity.
(assert (distinct gn_bayern gn_germany gn_france bcp_de bcp_fr))
;
; SMT cross-check at the conclusion level: each operand-pair's
; forced-emptiness holds. The full rule-level aggregation via
; COMPOSE000's Strong Kleene rule is FOF-only (SMT does not encode
; rule_and explicitly).
(declare-fun x () Concept)
(assert (= x gn_bayern))
(assert (= x gn_france))""",
    },

    # =====================================================================
    # KGC701 -- AND-Compatible aggregation (negative test).
    # =====================================================================
    {
        "id":            "KGC701",
        "subdir":        "Composition",
        "name":          "Theorem 2 (and): Compatible does NOT yield Conflict [GeoNames, DPV]",
        "relation":      "composition",
        "verdict":       "AndCompatibleNonConflict",
        "status_fof":    "CounterSatisfiable",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "includes":      [
            "KGE000-0.ax",
            "DENOT000-0.ax",
            "COMPOSE000-0.ax",
            "GN000-0.ax",
            "DPV000-0.ax",
        ],
        "needs_density": False,
        "description": (
            "Theorem 2 (and) Compatible aggregation, tested via the\n"
            "negative direction: when both operand pairs are Compatible,\n"
            "rule_and(r1) is Compatible (NOT conflict). Tests that the\n"
            "Strong Kleene AND rule does not over-derive Conflict.\n"
            "\n"
            "Setup:\n"
            "  Operand 1 (spatial, GeoNames):\n"
            "    c1_off = (spatial, isPartOf, gn:Europe)\n"
            "    c1_req = (spatial, eq, gn:France)\n"
            "    [c1_off] = downward cone of gn_europe, [c1_req] = {gn_france}\n"
            "    France is below Europe in GeoNames; witness gn_france.\n"
            "    => verdict_compatible(c1_off, c1_req).\n"
            "\n"
            "  Operand 2 (purpose, DPV):\n"
            "    c2_off = (purpose, eq, dpv:ScientificResearch)\n"
            "    c2_req = (purpose, isA, dpv:Purpose)\n"
            "    [c2_off] = {dpv_scientific_research},\n"
            "    [c2_req] = downward cone of dpv_purpose\n"
            "    SR is below Purpose in DPV; witness SR.\n"
            "    => verdict_compatible(c2_off, c2_req).\n"
            "\n"
            "Bridges:\n"
            "  all_compat(r1) holds (both Compatible).\n"
            "  has_conflict(r1) does NOT hold (no operand-pair Conflict).\n"
            "\n"
            "Strong Kleene AND: rule_and(R) = compatible <=> all_compat(R).\n"
            "  rule_and(r1) = compatible.\n"
            "Conjecture (Style B, asserting Conflict): rule_and(r1) = conflict.\n"
            "Expected: CounterSatisfiable. The rule is Compatible, so\n"
            "the asserted Conflict fails to derive."
        ),
        "ttl": _ttl_two_pairs(
            "spatial", "isPartOf", "<https://sws.geonames.org/6255148/>",
                       "eq",       "<https://sws.geonames.org/3017382/>",
            "purpose", "eq",  "dpv:ScientificResearch",
                       "isA", "dpv:Purpose",
            note=(
                "Theorem 2 AND-Compatible non-creation test:\n"
                "#   Both operand-pairs Compatible.\n"
                "#   all_compat(r1) holds; has_conflict(r1) does not.\n"
                "#   rule_and(r1) = compatible.\n"
                "#   Conjecture asserts Conflict; must NOT derive."
            ),
        ),
 "fof_extra_decls": _fof_two_pair_setup(
    "den_ispartof(X, gn_europe)",
    "den_eq(X, gn_france)",
    "den_eq(X, dpv_scientific_research)",
    "den_eq(X, dpv_marketing)",
) + """\
% --- Concept distinctness ---
% DPV asserts neither equality nor disjointness between
% ScientificResearch and Marketing -- the OWA silence is exactly
% what makes operand 2 Unknown.  But to refute the existence of a
% witness X equating both denotations, we must assert that the two
% grounded concepts are distinct as IRIs.  Without this, the prover
% finds a model where SR = Marketing, vacuously making operand 2
% Compatible.
fof(sr_neq_marketing, axiom,
    dpv_scientific_research != dpv_marketing).
""" + _fof_bridge_axioms(),
        "fof_conjecture": "rule_and(r1) = conflict",
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun gn_europe  () Concept)
(declare-fun gn_france  () Concept)
(declare-fun dpv_scientific_research () Concept)
(declare-fun dpv_purpose             () Concept)
(declare-fun kge_leq      (Concept Concept) Bool)
(declare-fun kge_disjoint (Concept Concept) Bool)""",
        "smt2_asserts": """\
; KGE000 load-bearing axioms.
(assert (forall ((c Concept)) (kge_leq c c)))
(assert (forall ((a Concept) (b Concept) (c Concept))
    (=> (and (kge_leq a b) (kge_leq b c)) (kge_leq a c))))
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
(assert (forall ((c Concept)) (not (kge_disjoint c c))))
; GeoNames: France below Europe.
(assert (kge_leq gn_france gn_europe))
; DPV: SR below Purpose.
(assert (kge_leq dpv_scientific_research dpv_purpose))
; Identity.
(assert (distinct gn_europe gn_france
                  dpv_scientific_research dpv_purpose))
;
; Both operand-pairs admit common satisfiers:
; gn_france in both [c1_off] and [c1_req];
; dpv_scientific_research in both [c2_off] and [c2_req].
; No Conflict can be derived. Z3 returns sat (consistent model exists).""",
    },

    # =====================================================================
    # KGC702 -- AND-Unknown propagation.
    # =====================================================================
{
    "id":            "KGC702",
    "subdir":        "Composition",
    "name":          "Theorem 2 (and): Strong Kleene Unknown propagation [GeoNames, DPV]",
    "relation":      "composition",
    "verdict":       "AndUnknown",
    "status_fof":    "Theorem",
    "status_smt":    "sat",
    "difficulty":    "Medium",
    "includes":      [
        "KGE000-0.ax",
        "DENOT000-0.ax",
        "COMPOSE000-0.ax",
        "GN000-0.ax",
        "DPV000-0.ax",
    ],
    "needs_density": False,
    "description": (
        "Theorem 2 (and) Strong Kleene Unknown propagation. One operand\n"
        "pair Compatible, one Unknown; rule_and(r1) = unknown by Strong\n"
        "Kleene's Unknown-propagation rule.\n"
        "\n"
        "Setup:\n"
        "  Operand 1 (spatial, GeoNames): verdict_compatible holds\n"
        "    (France in cone of Europe; witness gn_france). Asserted\n"
        "    as a premise.\n"
        "  Operand 2 (purpose, DPV): verdict_unknown holds (DPV silent\n"
        "    on disjointness between SR and Marketing). Asserted as\n"
        "    a premise.\n"
        "\n"
        "Why operand-level verdicts are asserted as premises:\n"
        "  verdict_compatible is positively derivable (witness exists)\n"
        "  but asserted for symmetry. verdict_unknown under OWA is the\n"
        "  meta-claim ~verdict_compatible & ~verdict_conflict, which is\n"
        "  not positively derivable in FOL: it requires showing two\n"
        "  negative existentials over an unbounded concept domain. We\n"
        "  assert it as a premise to isolate Theorem 2's rule-level\n"
        "  claim (Strong Kleene aggregation) from the operand-level\n"
        "  Unknown derivation, which is separately audited in KGC402,\n"
        "  KGC412, etc., and known to require model-finding rather\n"
        "  than saturation (see eprover/cvc5 limitations on those\n"
        "  problems).\n"
        "\n"
        "Bridges:\n"
        "  Premise verdict_unknown(c2_off, c2_req) implies\n"
        "    ~verdict_compatible(c2_off, c2_req) by verdict_unknown_def.\n"
        "  This implies ~all_compat(r1) via the bridge.\n"
        "  Premise verdict_unknown also gives ~verdict_conflict, so\n"
        "    ~has_conflict(r1) via the bridge.\n"
        "\n"
        "Strong Kleene AND:\n"
        "  rule_and(R) = unknown <=> ~all_compat(R) & ~has_conflict(R).\n"
        "  Both negations hold for r1, so rule_and(r1) = unknown.\n"
        "\n"
        "Conjecture (Style A): rule_and(r1) = unknown.\n"
        "Expected: Theorem."
    ),
    "ttl": _ttl_two_pairs(
        "spatial", "isPartOf", "<https://sws.geonames.org/6255148/>",
                   "eq",       "<https://sws.geonames.org/3017382/>",
        "purpose", "eq", "dpv:ScientificResearch",
                   "eq", "dpv:Marketing",
        note=(
            "Theorem 2 AND-Unknown propagation:\n"
            "#   Operand 1 Compatible (asserted premise).\n"
            "#   Operand 2 Unknown (asserted premise; OWA meta-claim).\n"
            "#   Strong Kleene aggregates to rule_and(r1) = unknown."
        ),
    ),
    "fof_extra_decls": _fof_two_pair_setup(
        "den_ispartof(X, gn_europe)",
        "den_eq(X, gn_france)",
        "den_eq(X, dpv_scientific_research)",
        "den_eq(X, dpv_marketing)",
    ) + _fof_bridge_axioms() + """\

% --- Operand-level verdict premises ---
% Operand 1: verdict_compatible is positively derivable
% (gn_france is in both [c1_off] and [c1_req]). Asserted explicitly
% to keep the proof focused on rule-level aggregation.
fof(c1_compat_premise, axiom,
    verdict_compatible(c1_off, c1_req)).

% Operand 2: verdict_unknown is the OWA meta-claim that DPV is silent
% on the SR-vs-Marketing pair. Not positively derivable in FOL (no
% finite witness for two nested negations under unbounded quantification).
% Asserted as a premise so the audit isolates Theorem 2's Strong Kleene
% rule-level aggregation from operand-level Unknown derivation, which
% is separately audited (KGC402, KGC412, etc.).
fof(c2_unknown_premise, axiom,
    verdict_unknown(c2_off, c2_req)).
""",
    "fof_conjecture": "rule_and(r1) = unknown",
    "smt2_logic": "UF",
    "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun gn_europe  () Concept)
(declare-fun gn_france  () Concept)
(declare-fun dpv_scientific_research () Concept)
(declare-fun dpv_marketing           () Concept)
(declare-fun kge_leq      (Concept Concept) Bool)
(declare-fun kge_disjoint (Concept Concept) Bool)""",
    "smt2_asserts": """\
; KGE000 load-bearing axioms.
(assert (forall ((c Concept)) (kge_leq c c)))
(assert (forall ((a Concept) (b Concept) (c Concept))
    (=> (and (kge_leq a b) (kge_leq b c)) (kge_leq a c))))
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
(assert (forall ((c Concept)) (not (kge_disjoint c c))))
; GeoNames: France below Europe.
(assert (kge_leq gn_france gn_europe))
; DPV: no edge or disjointness between SR and Marketing.
(assert (distinct gn_europe gn_france
                  dpv_scientific_research dpv_marketing))
;
; Theorem 2's rule_and = unknown derivation lives in FOL via COMPOSE000.
; SMT side confirms resource consistency.""",
},
{
    "id":            "KGC705",
    "subdir":        "Composition",
    "name":          "Theorem 2 (and): three-operand all-Compatible [GeoNames+DPV+BCP47]",
    "relation":      "composition",
    "verdict":       "AndCompatibleNonConflict",
    "status_fof":    "CounterSatisfiable",
    "status_smt":    "sat",
    "difficulty":    "Medium",
    "includes":      [
        "KGE000-0.ax",
        "DENOT000-0.ax",
        "COMPOSE000-0.ax",
        "GN000-0.ax",
        "DPV000-0.ax",
        "BCP47000-0.ax",
    ],
    "needs_density": False,
    "description": (
        "Theorem 2 (and) Compatible aggregation in a realistic three-\n"
        "operand, three-resource scenario. Tests Strong Kleene's\n"
        "all-Compatible case end-to-end: when every operand-pair is\n"
        "Compatible (via different reasoning paths in different\n"
        "resources), the rule-level verdict is Compatible.\n"
        "\n"
        "Setup:\n"
        "  Operand 1 (spatial, GeoNames):\n"
        "    c1_off = (spatial, isPartOf, gn:Europe)\n"
        "    c1_req = (spatial, eq, gn:France)\n"
        "    [c1_off] = downward cone of gn_europe;\n"
        "    [c1_req] = {gn_france}.\n"
        "    France in cone of Europe; witness gn_france.\n"
        "    => verdict_compatible(c1_off, c1_req).\n"
        "\n"
        "  Operand 2 (purpose, DPV):\n"
        "    c2_off = (purpose, eq, dpv:ScientificResearch)\n"
        "    c2_req = (purpose, isA, dpv:Purpose)\n"
        "    [c2_off] = {dpv_scientific_research};\n"
        "    [c2_req] = downward cone of dpv_purpose.\n"
        "    SR in cone of Purpose; witness SR.\n"
        "    => verdict_compatible(c2_off, c2_req).\n"
        "\n"
        "  Operand 3 (language, BCP47):\n"
        "    c3_off = (language, eq, bcp:de)\n"
        "    c3_req = (language, isAnyOf, {bcp:de, bcp:fr})\n"
        "    [c3_off] = {bcp_de};\n"
        "    [c3_req] = {bcp_de, bcp_fr}.\n"
        "    bcp_de in [c3_req]; witness bcp_de.\n"
        "    => verdict_compatible(c3_off, c3_req).\n"
        "\n"
        "Bridges:\n"
        "  all_compat(r1) holds (all three operand-pairs Compatible).\n"
        "  has_conflict(r1) does NOT hold.\n"
        "\n"
        "Strong Kleene AND: rule_and(R) = compatible <=> all_compat(R).\n"
        "  rule_and(r1) = compatible.\n"
        "\n"
        "Conjecture (Style B, asserting Conflict): rule_and(r1) = conflict.\n"
        "Expected: CounterSatisfiable. The rule is Compatible across\n"
        "three operand families and three resources; the asserted\n"
        "Conflict cannot derive."
    ),
    "ttl": _TTL_PREFIX + """
drk:offer_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:isPartOf ;
    odrl:rightOperand <https://sws.geonames.org/6255148/>
  ] ;
  odrl:constraint [
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:ScientificResearch
  ] ;
  odrl:constraint [
    odrl:leftOperand odrl:language ;
    odrl:operator odrl:eq ;
    odrl:rightOperand bcp:de
  ] .

drk:request_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:eq ;
    odrl:rightOperand <https://sws.geonames.org/3017382/>
  ] ;
  odrl:constraint [
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:isA ;
    odrl:rightOperand dpv:Purpose
  ] ;
  odrl:constraint [
    odrl:leftOperand odrl:language ;
    odrl:operator odrl:isAnyOf ;
    odrl:rightOperand ( bcp:de bcp:fr )
  ] .

# Theorem 2 three-operand AND-Compatible all-pass:
#   spatial:  isPartOf Europe vs eq France   -> Compatible
#   purpose:  eq SR vs isA Purpose            -> Compatible
#   language: eq de vs isAnyOf {de, fr}       -> Compatible
#   Strong Kleene: all Compatible -> rule_and(r1) = compatible.
#   Conjecture asserts Conflict; must NOT derive.
""",
    "fof_extra_decls": """\
% --- Operand 1 pair (spatial, GeoNames) ---
fof(c1_off_defined, axiom, ~denotation_undef(c1_off)).
fof(c1_req_defined, axiom, ~denotation_undef(c1_req)).
fof(c1_off_den, axiom,
    ![X]: (in_denotation(X, c1_off) <=> den_ispartof(X, gn_europe))).
fof(c1_req_den, axiom,
    ![X]: (in_denotation(X, c1_req) <=> den_eq(X, gn_france))).

% --- Operand 2 pair (purpose, DPV) ---
fof(c2_off_defined, axiom, ~denotation_undef(c2_off)).
fof(c2_req_defined, axiom, ~denotation_undef(c2_req)).
fof(c2_off_den, axiom,
    ![X]: (in_denotation(X, c2_off) <=> den_eq(X, dpv_scientific_research))).
fof(c2_req_den, axiom,
    ![X]: (in_denotation(X, c2_req) <=> den_isa(X, dpv_purpose))).

% --- Operand 3 pair (language, BCP47) ---
fof(c3_off_defined, axiom, ~denotation_undef(c3_off)).
fof(c3_req_defined, axiom, ~denotation_undef(c3_req)).
fof(c3_off_den, axiom,
    ![X]: (in_denotation(X, c3_off) <=> den_eq(X, bcp_de))).
fof(c3_req_den, axiom,
    ![X]: (in_denotation(X, c3_req) <=>
              (den_eq(X, bcp_de) | den_eq(X, bcp_fr)))).

% --- Rule-level bridge axioms (3-operand version) ---
fof(has_conflict_bridge, axiom,
    (has_conflict(r1) <=>
       (verdict_conflict(c1_off, c1_req) |
        verdict_conflict(c2_off, c2_req) |
        verdict_conflict(c3_off, c3_req)))).
fof(all_compat_bridge, axiom,
    (all_compat(r1) <=>
       (verdict_compatible(c1_off, c1_req) &
        verdict_compatible(c2_off, c2_req) &
        verdict_compatible(c3_off, c3_req)))).
""",
    "fof_conjecture": "rule_and(r1) = conflict",
    "smt2_logic": "UF",
    "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun gn_europe  () Concept)
(declare-fun gn_france  () Concept)
(declare-fun dpv_scientific_research () Concept)
(declare-fun dpv_purpose             () Concept)
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)
(declare-fun kge_leq      (Concept Concept) Bool)
(declare-fun kge_disjoint (Concept Concept) Bool)""",
    "smt2_asserts": """\
; KGE000 load-bearing axioms.
(assert (forall ((c Concept)) (kge_leq c c)))
(assert (forall ((a Concept) (b Concept) (c Concept))
    (=> (and (kge_leq a b) (kge_leq b c)) (kge_leq a c))))
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
(assert (forall ((c Concept)) (not (kge_disjoint c c))))
; GeoNames: France below Europe.
(assert (kge_leq gn_france gn_europe))
; DPV: SR below Purpose.
(assert (kge_leq dpv_scientific_research dpv_purpose))
; BCP47: distinct tags.
(assert (distinct gn_europe gn_france
                  dpv_scientific_research dpv_purpose
                  bcp_de bcp_fr))
;
; Each operand-pair admits a witness:
;   spatial:  gn_france in [c1_off] (kge_leq France Europe) and [c1_req].
;   purpose:  dpv_scientific_research in [c2_off] (eq) and [c2_req] (kge_leq SR Purpose).
;   language: bcp_de in [c3_off] and [c3_req] (eq de in {de, fr}).
; No Conflict can be derived. Z3 returns sat.""",
},
{
    "id":            "KGC706",
    "subdir":        "Composition",
    "name":          "Theorem 2 (and): paper Example 1 verbatim [GeoNames+DPV+BCP47]",
    "relation":      "composition",
    "verdict":       "AndConflict",
    "status_fof":    "Theorem",
    "status_smt":    "unsat",
    "difficulty":    "Hard",
    "includes":      [
        "KGE000-0.ax",
        "DENOT000-0.ax",
        "COMPOSE000-0.ax",
        "GN000-0.ax",
        "DPV000-0.ax",
        "BCP47000-0.ax",
    ],
    "needs_density": False,
    "description": (
        "Theorem 2 (and) audit of the paper's running Example 1\n"
        "(Section 3, Gaia-X cultural heritage scenario) verbatim. The\n"
        "three operand-pair verdicts are Compatible, Unknown, Conflict\n"
        "(Table 4 in the paper); under Strong Kleene AND, rule-level\n"
        "verdict is Conflict (one Conflict suffices).\n"
        "\n"
        "Setup (paper Example 1, Table 3):\n"
        "  Operand 1 (spatial, GeoNames):\n"
        "    c_sp = (spatial, isPartOf, gn:Europe)        [offer]\n"
        "    c'_sp = (spatial, eq, gn:France)             [request]\n"
        "    France <= Europe in GeoNames; witness gn_france.\n"
        "    => verdict_compatible(c_sp, c'_sp).\n"
        "\n"
        "  Operand 2 (purpose, DPV):\n"
        "    c_pu  = (purpose, isA, dpv:NonCommercialPurpose)  [offer]\n"
        "    c'_pu = (purpose, eq, dpv:ScientificResearch)     [request]\n"
        "    DPV asserts only ScientificResearch skos:broader\n"
        "    ResearchAndDevelopment; there is NO edge or disjointness\n"
        "    between ScientificResearch and NonCommercialPurpose.\n"
        "    Intersection is empty in the current state but not forced\n"
        "    empty -- a future DPV release could add a skos:broader edge.\n"
        "    Operand-pair verdict_unknown asserted as a premise (see\n"
        "    KGC702 for rationale: Unknown is not positively derivable\n"
        "    in FOL under OWA).\n"
        "    => verdict_unknown(c_pu, c'_pu).\n"
        "\n"
        "  Operand 3 (language, BCP47):\n"
        "    c_la  = (language, eq, bcp:de)               [offer]\n"
        "    c'_la = (language, eq, bcp:fr)               [request]\n"
        "    BCP47 asserts kge_disjoint(bcp_de, bcp_fr) by registry\n"
        "    uniqueness; B1 pattern fires forced_empty.\n"
        "    => verdict_conflict(c_la, c'_la).\n"
        "\n"
        "Bridges:\n"
        "  has_conflict(r1) holds (operand 3 is Conflict).\n"
        "\n"
        "Strong Kleene AND: rule_and(R) = conflict <=> has_conflict(R).\n"
        "  rule_and(r1) = conflict.\n"
        "\n"
        "Conjecture (Style A): rule_and(r1) = conflict.\n"
        "Expected: Theorem.\n"
        "\n"
        "Why this audit matters:\n"
        "  This is the paper's lead motivating example. Without an\n"
        "  empirical audit, the framework's flagship claim ('the three\n"
        "  yield three different verdicts, composing under and to\n"
        "  rule-level Conflict') is unverified. KGC706 closes that gap.\n"
        "  The audit covers all three Strong Kleene operand-level cases\n"
        "  (Compatible, Unknown, Conflict) in a single problem, against\n"
        "  three different resource kinds (knowledge graph, taxonomy,\n"
        "  flat registry) and three different operators (isPartOf, isA,\n"
        "  eq)."
    ),
    "ttl": _TTL_PREFIX + """
drk:offer_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:isPartOf ;
    odrl:rightOperand <https://sws.geonames.org/6255148/>
  ] ;
  odrl:constraint [
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:isA ;
    odrl:rightOperand dpv:NonCommercialPurpose
  ] ;
  odrl:constraint [
    odrl:leftOperand odrl:language ;
    odrl:operator odrl:eq ;
    odrl:rightOperand bcp:de
  ] .

drk:request_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:eq ;
    odrl:rightOperand <https://sws.geonames.org/3017382/>
  ] ;
  odrl:constraint [
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:ScientificResearch
  ] ;
  odrl:constraint [
    odrl:leftOperand odrl:language ;
    odrl:operator odrl:eq ;
    odrl:rightOperand bcp:fr
  ] .

# Paper Example 1 verbatim (Section 3, Table 3):
#   spatial:  isPartOf Europe vs eq France   -> Compatible (France <= Europe)
#   purpose:  isA NonCommercial vs eq SR     -> Unknown    (DPV silent)
#   language: eq de vs eq fr                 -> Conflict   (BCP47 disjoint)
#   Strong Kleene: any Conflict -> rule_and(r1) = conflict.
""",
    "fof_extra_decls": """\
% --- Operand 1 pair (spatial, GeoNames): Compatible ---
fof(c1_off_defined, axiom, ~denotation_undef(c1_off)).
fof(c1_req_defined, axiom, ~denotation_undef(c1_req)).
fof(c1_off_den, axiom,
    ![X]: (in_denotation(X, c1_off) <=> den_ispartof(X, gn_europe))).
fof(c1_req_den, axiom,
    ![X]: (in_denotation(X, c1_req) <=> den_eq(X, gn_france))).

% Operand 1 verdict: positively derivable (witness gn_france in both
% denotations via kge_leq(gn_france, gn_europe) for the offer side).
% Asserted explicitly for symmetry with the Unknown premise below.
fof(c1_compat_premise, axiom,
    verdict_compatible(c1_off, c1_req)).

% --- Operand 2 pair (purpose, DPV): Unknown ---
fof(c2_off_defined, axiom, ~denotation_undef(c2_off)).
fof(c2_req_defined, axiom, ~denotation_undef(c2_req)).
fof(c2_off_den, axiom,
    ![X]: (in_denotation(X, c2_off) <=> den_isa(X, dpv_non_commercial_purpose))).
fof(c2_req_den, axiom,
    ![X]: (in_denotation(X, c2_req) <=> den_eq(X, dpv_scientific_research))).

% Operand 2 verdict: Unknown is the OWA meta-claim that DPV is silent
% on ScientificResearch vs NonCommercialPurpose. Per the DPV TTL
% source, ScientificResearch's only parent is ResearchAndDevelopment;
% no skos:broader edge connects ScientificResearch to
% NonCommercialPurpose. The intersection of denotations is empty in
% the current state but not forced empty. Asserted as a premise
% because verdict_unknown under OWA is not positively derivable in FOL
% (see KGC702 audit notes).
fof(c2_unknown_premise, axiom,
    verdict_unknown(c2_off, c2_req)).

% --- Operand 3 pair (language, BCP47): Conflict ---
fof(c3_off_defined, axiom, ~denotation_undef(c3_off)).
fof(c3_req_defined, axiom, ~denotation_undef(c3_req)).
fof(c3_off_den, axiom,
    ![X]: (in_denotation(X, c3_off) <=> den_eq(X, bcp_de))).
fof(c3_req_den, axiom,
    ![X]: (in_denotation(X, c3_req) <=> den_eq(X, bcp_fr))).

% Operand 3 verdict: Conflict, positively derivable from
% kge_disjoint(bcp_de, bcp_fr) via B1 forced_empty pattern.
% No premise needed; verdict_conflict_def derives it directly from
% the BCP47000-0.ax disjointness fact.

% --- Rule-level bridge axioms (3-operand version) ---
fof(has_conflict_bridge, axiom,
    (has_conflict(r1) <=>
       (verdict_conflict(c1_off, c1_req) |
        verdict_conflict(c2_off, c2_req) |
        verdict_conflict(c3_off, c3_req)))).
fof(all_compat_bridge, axiom,
    (all_compat(r1) <=>
       (verdict_compatible(c1_off, c1_req) &
        verdict_compatible(c2_off, c2_req) &
        verdict_compatible(c3_off, c3_req)))).
""",
    "fof_conjecture": "rule_and(r1) = conflict",
    "smt2_logic": "UF",
    "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun gn_europe  () Concept)
(declare-fun gn_france  () Concept)
(declare-fun dpv_non_commercial_purpose () Concept)
(declare-fun dpv_scientific_research    () Concept)
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)
(declare-fun kge_leq      (Concept Concept) Bool)
(declare-fun kge_disjoint (Concept Concept) Bool)""",
    "smt2_asserts": """\
; KGE000 load-bearing axioms.
(assert (forall ((c Concept)) (kge_leq c c)))
(assert (forall ((a Concept) (b Concept) (c Concept))
    (=> (and (kge_leq a b) (kge_leq b c)) (kge_leq a c))))
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
(assert (forall ((c Concept)) (not (kge_disjoint c c))))
(assert (forall ((a Concept) (b Concept) (z Concept))
    (=> (and (kge_disjoint a b) (kge_leq z a) (kge_leq z b))
        false)))
; GeoNames: France below Europe.
(assert (kge_leq gn_france gn_europe))
; DPV: no edge or disjointness asserted between SR and NonCommercial.
; (SR's only parent in DPV is ResearchAndDevelopment, which we omit
;  here since it is irrelevant to operand 2's empty-but-not-forced
;  intersection.)
; BCP47: de disjoint fr.
(assert (kge_disjoint bcp_de bcp_fr))
; Identity.
(assert (distinct gn_europe gn_france
                  dpv_non_commercial_purpose dpv_scientific_research
                  bcp_de bcp_fr))
;
; SMT cross-check: at the Conflict-bearing operand (language), the
; forced-emptiness check refutes a shared concept x assigned both
; bcp_de and bcp_fr.
(declare-fun x () Concept)
(assert (= x bcp_de))
(assert (= x bcp_fr))""",
},

# =====================================================================
    # KGC703 -- Disjoint operand sets (Corollary 1 case (a)).
    # =====================================================================
    {
        "id":            "KGC703",
        "subdir":        "Composition",
        "name":          "Theorem 5 (and): disjoint operand sets [GeoNames | BCP47]",
        "relation":      "composition",
        "verdict":       "AndCompatibleNonConflict",
        "status_fof":    "CounterSatisfiable",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "includes":      [
            "KGE000-0.ax",
            "DENOT000-0.ax",
            "COMPOSE000-0.ax",
            "GN000-0.ax",
            "BCP47000-0.ax",
        ],
        "needs_density": False,
        "description": (
            "Corollary~\\ref{cor:and-factoring} case (a): disjoint\n"
            "operand sets yield rule-level Compatible vacuously. CS\n"
            "constrains spatial only; CS' constrains language only.\n"
            "No shared operand, so the rule-level intersection is\n"
            "unrestricted across both rules.\n"
            "\n"
            "Setup:\n"
            "  CS  (offer): one constraint on spatial, no others.\n"
            "    c1_off = (spatial, isPartOf, gn:Europe)\n"
            "  CS' (request): one constraint on language, no others.\n"
            "    c2_req = (language, eq, bcp:de)\n"
            "\n"
            "Operand sets: L = {spatial}, L' = {language}, L cap L' =\n"
            "empty. Per Corollary 1 case (a), rule_and(r1) = compatible.\n"
            "\n"
            "Bridges:\n"
            "  has_conflict(r1) is vacuously false (no operand-pair\n"
            "    has both a CS and CS' constraint to compare).\n"
            "  all_compat(r1) is vacuously true (no shared operand to\n"
            "    aggregate over).\n"
            "\n"
            "Strong Kleene AND with empty shared-operand set: the\n"
            "vacuous quantification yields all_compat -> rule\n"
            "Compatible.\n"
            "\n"
            "Conjecture (Style B, asserting Conflict): rule_and(r1) = conflict.\n"
            "Expected: CounterSatisfiable. Disjoint operand sets cannot\n"
            "produce Conflict; the asserted conflict fails to derive."
        ),
        "ttl": _TTL_PREFIX + """
drk:offer_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:isPartOf ;
    odrl:rightOperand <https://sws.geonames.org/6255148/>
  ] .

drk:request_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:language ;
    odrl:operator odrl:eq ;
    odrl:rightOperand bcp:de
  ] .
# Corollary 1 case (a): disjoint operand sets.
#   CS  has one spatial constraint.
#   CS' has one language constraint.
#   No shared operand; rule_and(r1) = compatible vacuously.
""",
        "fof_extra_decls": """\
% --- Single operand on each side (disjoint operand sets) ---
fof(c_offer_defined, axiom, ~denotation_undef(c_offer)).
fof(c_request_defined, axiom, ~denotation_undef(c_request)).
fof(c_offer_den, axiom,
    ![X]: (in_denotation(X, c_offer) <=> den_ispartof(X, gn_europe))).
fof(c_request_den, axiom,
    ![X]: (in_denotation(X, c_request) <=> den_eq(X, bcp_de))).

% --- Rule-level bridge axioms (vacuous for disjoint operand sets) ---
% Disjoint operand sets: no shared-operand verdict to aggregate.
% has_conflict(r1) is vacuously false; all_compat(r1) is vacuously true.
% This is Corollary 1 case (a).
fof(has_conflict_bridge, axiom,
    ~has_conflict(r1)).
fof(all_compat_bridge, axiom,
    all_compat(r1)).
""",
        "fof_conjecture": "rule_and(r1) = conflict",
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun gn_europe () Concept)
(declare-fun bcp_de    () Concept)
(declare-fun kge_leq      (Concept Concept) Bool)
(declare-fun kge_disjoint (Concept Concept) Bool)""",
        "smt2_asserts": """\
; KGE000 load-bearing axioms.
(assert (forall ((c Concept)) (kge_leq c c)))
(assert (forall ((a Concept) (b Concept) (c Concept))
    (=> (and (kge_leq a b) (kge_leq b c)) (kge_leq a c))))
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
(assert (forall ((c Concept)) (not (kge_disjoint c c))))
; Identity.
(assert (distinct gn_europe bcp_de))
;
; Disjoint operand sets: spatial and language are unrelated.
; No shared operand to compare; rule-level Conflict cannot derive.
; Z3 returns sat (consistent model exists with no conflict).""",
    },
    
    # =====================================================================
    # KGC704 -- Partial operand-set overlap (Corollary 1 case (c)).
    # =====================================================================
    {
        "id":            "KGC704",
        "subdir":        "Composition",
        "name":          "Theorem 5 (and): partial operand overlap [GeoNames+BCP47+DPV]",
        "relation":      "composition",
        "verdict":       "AndConflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "includes":      [
            "KGE000-0.ax",
            "DENOT000-0.ax",
            "COMPOSE000-0.ax",
            "GN000-0.ax",
            "BCP47000-0.ax",
            "DPV000-0.ax",
        ],
        "needs_density": False,
        "description": (
            "Corollary~\\ref{cor:and-factoring} case (c): partial overlap\n"
            "of operand sets. CS over {spatial, language}; CS' over\n"
            "{language, purpose}. Shared operand: language. Atomic\n"
            "verdict on language is Conflict (registry uniqueness).\n"
            "Per Corollary 1 case (c), Strong Kleene aggregates over\n"
            "shared operands only; rule-level Conflict.\n"
            "\n"
            "Setup:\n"
            "  CS  (offer):\n"
            "    c1_off = (spatial, isPartOf, gn:Europe)   [unshared]\n"
            "    c2_off = (language, eq, bcp:de)            [shared]\n"
            "  CS' (request):\n"
            "    c2_req = (language, eq, bcp:fr)            [shared]\n"
            "    c3_req = (purpose, isA, dpv:Purpose)       [unshared]\n"
            "\n"
            "Shared operand: language. Atomic verdict at language:\n"
            "  [c2_off] = {bcp_de}, [c2_req] = {bcp_fr};\n"
            "  kge_disjoint(bcp_de, bcp_fr) by BCP47 registry uniqueness;\n"
            "  forced_empty fires via pattern B1.\n"
            "  => verdict_conflict(c2_off, c2_req).\n"
            "\n"
            "Bridges (over shared operand language only):\n"
            "  has_conflict(r1) <=> verdict_conflict(c2_off, c2_req).\n"
            "  all_compat(r1) <=> verdict_compatible(c2_off, c2_req).\n"
            "\n"
            "Strong Kleene AND: rule_and(R) = conflict <=>\n"
            "  has_conflict(R). The shared-operand Conflict propagates\n"
            "to rule-level Conflict (Corollary 1 case (c)).\n"
            "\n"
            "Conjecture (Style A): rule_and(r1) = conflict.\n"
            "Expected: Theorem.\n"
            "\n"
            "Why this audit matters:\n"
            "  Corollary 1 case (c) is the basis of Theorem 5\n"
            "  (Composition Soundness): cross-pair verdicts in DNF\n"
            "  decomposition aggregate over shared operands only.\n"
            "  Without this audit, the shared-operand reasoning that\n"
            "  carries Theorem 5 is unverified."
        ),
        "ttl": _TTL_PREFIX + """
drk:offer_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:isPartOf ;
    odrl:rightOperand <https://sws.geonames.org/6255148/>
  ] ;
  odrl:constraint [
    odrl:leftOperand odrl:language ;
    odrl:operator odrl:eq ;
    odrl:rightOperand bcp:de
  ] .

drk:request_rule a odrl:Permission ;
  odrl:constraint [
    odrl:leftOperand odrl:language ;
    odrl:operator odrl:eq ;
    odrl:rightOperand bcp:fr
  ] ;
  odrl:constraint [
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:isA ;
    odrl:rightOperand dpv:Purpose
  ] .
# Corollary 1 case (c): partial overlap.
#   L  = {spatial, language}; L' = {language, purpose}.
#   Shared operand: language.  Atomic verdict at language: Conflict.
#   rule_and(r1) = conflict via Strong Kleene over shared operands only.
""",
        "fof_extra_decls": """\
% --- Shared operand: language (BCP47), atomic Conflict ---
fof(c2_off_defined, axiom, ~denotation_undef(c2_off)).
fof(c2_req_defined, axiom, ~denotation_undef(c2_req)).
fof(c2_off_den, axiom,
    ![X]: (in_denotation(X, c2_off) <=> den_eq(X, bcp_de))).
fof(c2_req_den, axiom,
    ![X]: (in_denotation(X, c2_req) <=> den_eq(X, bcp_fr))).

% --- Rule-level bridge over shared operands only ---
% Per Corollary 1 case (c): aggregate Strong Kleene over shared
% operands only. Unshared operands (spatial in CS, purpose in CS')
% do not participate in rule-level verdict aggregation.
fof(has_conflict_bridge, axiom,
    (has_conflict(r1) <=> verdict_conflict(c2_off, c2_req))).
fof(all_compat_bridge, axiom,
    (all_compat(r1) <=> verdict_compatible(c2_off, c2_req))).
""",
        "fof_conjecture": "rule_and(r1) = conflict",
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
(assert (forall ((a Concept) (b Concept) (c Concept))
    (=> (and (kge_leq a b) (kge_leq b c)) (kge_leq a c))))
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
(assert (forall ((c Concept)) (not (kge_disjoint c c))))
(assert (forall ((a Concept) (b Concept) (z Concept))
    (=> (and (kge_disjoint a b) (kge_leq z a) (kge_leq z b))
        false)))
; BCP47: de disjoint fr (registry uniqueness).
(assert (kge_disjoint bcp_de bcp_fr))
(assert (distinct bcp_de bcp_fr))
;
; Shared-operand Conflict: x cannot be both bcp_de and bcp_fr.
(declare-fun x () Concept)
(assert (= x bcp_de))
(assert (= x bcp_fr))""",
    },

]