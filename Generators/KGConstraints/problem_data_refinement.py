"""
problem_data_refinement.py
==========================
Lemma 1 audit: Refinement layer of the paper's denotational semantics.

Lemma 1 (paper Section 3.4, Definition 9 + Lemma 1):
  If c1 refines c2 (i.e., [[c1]] subseteq [[c2]]) and verdict(c2, c3) = Conflict,
  then verdict(c1, c3) = Conflict.

This module produces three problems exercising three substantively distinct
properties of the refinement layer:

  KGC500 -- Lemma 1 positive case.
            Conflict propagates from (c2, c3) to (c1, c3) when c1 refines c2.
            Resource: GeoNames + SDA profile.  Uses real refinement structure
            (downward cone inclusion: Bayern is below Germany), exercising
            the lemma's proof rather than degenerate identity.
            Style A: conjecture is the full implication.
            Expected FOF status: Theorem.

  KGC501 -- Refinement does NOT manufacture Conflict.
            Antecedent c1 refines c2 holds, but premise verdict(c2, c3) is
            Compatible (NOT Conflict).  The encoding must NOT derive
            verdict(c1, c3) = Conflict.
            Resource: DPV.  DPV is silent on disjointness between sibling
            purposes, so verdict(c1, c3) is genuinely Unknown.
            Style B: antecedents asserted as axioms, conjecture is the bare
            (negative) conclusion.  A Style A implication would be vacuously
            Theorem (false antecedent), testing classical implication, not
            the encoding.
            Expected FOF status: CounterSatisfiable.

  KGC502 -- Compatible non-propagation: the verdict-asymmetry.
            The Compatible-analog of Lemma 1 is:
              c1 refines c2 AND verdict(c2, c3) = Compatible
                ==> verdict(c1, c3) = Compatible.
            This is FALSE in general.  KGC502 demonstrates: c1's denotation
            can be a strict subset of c2's that misses c3's witness.  The
            encoding must NOT derive Compatible propagation.
            Resource: GeoNames (no SDA).  c2's denotation contains France
            (witness for c2 vs c3), but c1's denotation = {Germany} does not.
            Style A: conjecture is the full Compatible implication.
            Expected FOF status: CounterSatisfiable.

Together, the three problems characterize the refinement layer's
correctness boundary: Conflict propagates (KGC500), no spurious Conflict
manufacture (KGC501), and Compatible is non-monotone (KGC502).

Resource choice rationale:
  - GeoNames + SDA (KGC500): only configuration where forced_empty fires
    over a real downward-cone refinement.  Uses the paper's spatial
    operand, exercising mereological partial order.
  - DPV (KGC501): genuine OWA silence on disjointness; the encoding's
    refusal to derive Conflict is honest non-creation, not solver weakness.
  - GeoNames no SDA (KGC502): the verdict-asymmetry is independent of
    disjointness profile.  Without SDA, verdict(c1, c3) is Unknown; with
    SDA it would be Conflict; in neither case is it Compatible.

Numbering convention: KGC5{nn}, where nn picks out the refinement test.
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


def _ttl_three_constraints(left_operand: str,
                           op1: str, val1: str,
                           op2: str, val2: str,
                           op3: str, val3: str,
                           lemma_note: str = "") -> str:
    """Render TTL showing all three constraints for a refinement triple."""
    note_block = f"# {lemma_note}\n" if lemma_note else ""
    return _TTL_PREFIX + f"""
drk:c1 a odrl:Constraint ;
  odrl:leftOperand odrl:{left_operand} ;
  odrl:operator odrl:{op1} ;
  odrl:rightOperand {val1} .

drk:c2 a odrl:Constraint ;
  odrl:leftOperand odrl:{left_operand} ;
  odrl:operator odrl:{op2} ;
  odrl:rightOperand {val2} .

drk:c3 a odrl:Constraint ;
  odrl:leftOperand odrl:{left_operand} ;
  odrl:operator odrl:{op3} ;
  odrl:rightOperand {val3} .

{note_block}"""


# ---------------------------------------------------------------------------
# FOF helpers.
# ---------------------------------------------------------------------------

def _fof_three_denotations(c1_den: str, c2_den: str, c3_den: str) -> str:
    """Three constraint tokens with defined denotations."""
    return f"""\
% Three constraint tokens with defined denotations.
fof(c1_defined, axiom, ~denotation_undef(c1)).
fof(c2_defined, axiom, ~denotation_undef(c2)).
fof(c3_defined, axiom, ~denotation_undef(c3)).

% Denotations
fof(c1_den, axiom, ![X]: (in_denotation(X, c1) <=> {c1_den})).
fof(c2_den, axiom, ![X]: (in_denotation(X, c2) <=> {c2_den})).
fof(c3_den, axiom, ![X]: (in_denotation(X, c3) <=> {c3_den})).
"""


# ---------------------------------------------------------------------------
# Problem grid.
# ---------------------------------------------------------------------------
PROBLEMS = [
    # =====================================================================
    # KGC500 -- Lemma 1 positive case (GeoNames + SDA).
    # =====================================================================
    {
        "id":            "KGC500",
        "subdir":        "Refinement",
        "name":          "Lemma 1 positive: refines + Conflict premise => Conflict conclusion [GeoNames+SDA]",
        "relation":      "refinement",
        "verdict":       "ConflictPropagation",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      [
            "KGE000-0.ax",
            "DENOT000-0.ax",
            "REFINE000-0.ax",
            "GN000-0.ax",
            "GN001-SDA-0.ax",
        ],
        "needs_density": False,
        "description": (
            "Lemma 1 positive case. Demonstrates that Conflict propagates\n"
            "downward through refinement, using a structural (non-trivial)\n"
            "refinement over GeoNames + SDA profile.\n"
            "\n"
            "Setup:\n"
            "  c1 = (spatial, eq,        gn:Bayern)\n"
            "         => [c1] = {gn_bayern}\n"
            "  c2 = (spatial, isPartOf,  gn:Germany)\n"
            "         => [c2] = downward cone of gn_germany\n"
            "                  = {Germany, Bayern, Berlin, Baden-Wuerttemberg}\n"
            "  c3 = (spatial, eq,        gn:France)\n"
            "         => [c3] = {gn_france}\n"
            "\n"
            "Refinement:  [c1] = {Bayern} subseteq [c2] (Bayern <= Germany).\n"
            "             Real downward-cone inclusion, not identity.\n"
            "Premise:     verdict_conflict(c2, c3) holds. SDA asserts\n"
            "             kge_disjoint(gn_germany, gn_france); B1 pattern\n"
            "             fires for ([c2], [c3]) via ancestor pair\n"
            "             (gn_germany, gn_france) -- forced empty.\n"
            "Conclusion:  same ancestor pair certifies forced_empty for\n"
            "             ([c1], [c3]) since [c1] is below gn_germany.\n"
            "             verdict_conflict(c1, c3) follows.\n"
            "\n"
            "Conjecture style A: the implication itself is the Theorem to derive."
        ),
        "ttl": _ttl_three_constraints(
            "spatial",
            "eq",        "<https://sws.geonames.org/2951839/>",
            "isPartOf",  "<https://sws.geonames.org/2921044/>",
            "eq",        "<https://sws.geonames.org/3017382/>",
            lemma_note=(
                "Lemma 1 (paper Definition 9 + Lemma 1):\n"
                "#   refines(c1, c2) AND verdict_conflict(c2, c3)\n"
                "#     ==> verdict_conflict(c1, c3)\n"
                "# c1 refines c2: Bayern is in the downward cone of Germany.\n"
                "# verdict(c2, c3) = Conflict via SDA: Germany disjoint France."
            ),
        ),
        "fof_extra_decls": _fof_three_denotations(
            "den_eq(X, gn_bayern)",
            "den_ispartof(X, gn_germany)",
            "den_eq(X, gn_france)",
        ),
        "fof_conjecture": (
            "(refines(c1, c2) & verdict_conflict(c2, c3))\n"
            "       => verdict_conflict(c1, c3)"
        ),
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun gn_bayern  () Concept)
(declare-fun gn_germany () Concept)
(declare-fun gn_france  () Concept)
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
; GN000: Bayern parentFeature Germany.
(assert (kge_leq gn_bayern gn_germany))
; GN001-SDA: Germany disjoint France.
(assert (kge_disjoint gn_germany gn_france))
; Identity.
(assert (distinct gn_bayern gn_germany gn_france))
; Lemma 1 negation: a witness x exists in [c1] AND [c3].
; [c1] = {gn_bayern}; [c3] = {gn_france}.
; A witness equates them, contradicting (distinct ...).
;
; This SMT encoding tests the conclusion-level Conflict between c1 and c3.
; The full Lemma 1 propagation (refinement + premise) is tested in the FOF
; encoding via REFINE000-0.ax's refines_def and DENOT000-0.ax's
; verdict_conflict_def. The SMT side cross-checks that the conclusion
; verdict_conflict(c1, c3) holds at the witness level.
(declare-fun x () Concept)
(assert (= x gn_bayern))
(assert (= x gn_france))""",
    },

    # =====================================================================
    # KGC501 -- Refinement does NOT manufacture Conflict (DPV).
    # =====================================================================
    {
        "id":            "KGC501",
        "subdir":        "Refinement",
        "name":          "Lemma 1 non-creation: refines holds, premise NOT Conflict, conclusion not derivable [DPV]",
        "relation":      "refinement",
        "verdict":       "NoConflictCreation",
        "status_fof":    "CounterSatisfiable",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "includes":      [
            "KGE000-0.ax",
            "DENOT000-0.ax",
            "REFINE000-0.ax",
            "DPV000-0.ax",
        ],
        "needs_density": False,
        "description": (
            "Lemma 1 non-creation: refinement preserves Conflict but does\n"
            "NOT manufacture it where the lemma's hypothesis fails.\n"
            "\n"
            "Setup:\n"
            "  c1 = (purpose, eq,  dpv:ScientificResearch)\n"
            "         => [c1] = {dpv_scientific_research}\n"
            "  c2 = (purpose, isA, dpv:Purpose)\n"
            "         => [c2] = downward cone of dpv_purpose\n"
            "                  ⊇ {ScientificResearch, Marketing, ...}\n"
            "  c3 = (purpose, eq,  dpv:Marketing)\n"
            "         => [c3] = {dpv_marketing}\n"
            "\n"
            "Refinement holds: ScientificResearch is below Purpose in DPV,\n"
            "so [c1] = {SR} subseteq downward cone of Purpose = [c2].\n"
            "Asserted as axiom under Style B.\n"
            "\n"
            "Premise verdict_conflict(c2, c3) does NOT hold: Marketing is\n"
            "in the cone of Purpose (kge_leq(dpv_marketing, dpv_purpose) is\n"
            "asserted in DPV000-0.ax), so [c2] cap [c3] = {Marketing} is\n"
            "non-empty. The pair (c2, c3) is Compatible, not Conflict.\n"
            "\n"
            "Bare conclusion verdict_conflict(c1, c3): DPV asserts no\n"
            "kge_disjoint between ScientificResearch and Marketing, and the\n"
            "denotations [c1] = {SR} and [c3] = {Marketing} do not share\n"
            "a witness. Under OWA, verdict(c1, c3) = Unknown; the\n"
            "verdict_conflict(c1, c3) conjecture is not derivable.\n"
            "Vampire returns CounterSatisfiable; Z3 returns sat.\n"
            "\n"
            "Conjecture style B: the bare conclusion is the conjecture; the\n"
            "antecedent refines(c1, c2) is inserted as an axiom. A Style A\n"
            "implication conjecture would be vacuously Theorem (false\n"
            "antecedent: verdict_conflict(c2, c3) does not hold), which\n"
            "tests classical implication, not the encoding's behavior."
        ),
        "ttl": _ttl_three_constraints(
            "purpose",
            "eq",  "dpv:ScientificResearch",
            "isA", "dpv:Purpose",
            "eq",  "dpv:Marketing",
            lemma_note=(
                "Lemma 1 antecedents:\n"
                "#   c1 refines c2: ScientificResearch is below Purpose. ✓\n"
                "#   verdict(c2, c3) = Compatible (Marketing is below Purpose).\n"
                "#                     NOT Conflict.\n"
                "# Lemma 1's conclusion is NOT licensed; encoding must NOT\n"
                "# derive verdict_conflict(c1, c3)."
            ),
        ),
        "fof_extra_decls": _fof_three_denotations(
            "den_eq(X, dpv_scientific_research)",
            "den_isa(X, dpv_purpose)",
            "den_eq(X, dpv_marketing)",
        ) + """\

% Lemma 1 antecedent: refines(c1, c2). Asserted as axiom (Style B).
% This is licensed by [c1] = {ScientificResearch} subseteq [c2] = downward
% cone of Purpose, since DPV asserts kge_leq(SR, Purpose).
fof(refines_premise, axiom, refines(c1, c2)).
""",
        "fof_conjecture": "verdict_conflict(c1, c3)",
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun dpv_scientific_research () Concept)
(declare-fun dpv_marketing           () Concept)
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
(assert (forall ((a Concept) (b Concept) (z Concept))
    (=> (and (kge_disjoint a b) (kge_leq z a) (kge_leq z b))
        false)))
; DPV000: ScientificResearch and Marketing are both DPV purposes,
; with no asserted equality and no asserted disjointness.
(assert (kge_leq dpv_scientific_research dpv_purpose))
(assert (kge_leq dpv_marketing           dpv_purpose))
; Identity.
(assert (distinct dpv_scientific_research
                  dpv_marketing
                  dpv_purpose))
;
; Under these axioms there is no derivation of a witness in
; [c1] cap [c3], and there is no derivation of forced-empty for the
; pair. The corresponding FOF conjecture verdict_conflict(c1, c3) is
; CounterSatisfiable. Z3 returns sat: the axioms are consistent and
; admit a model where Conflict is not forced.""",
    },

    # =====================================================================
    # KGC502 -- Compatible non-propagation (GeoNames, no SDA).
    # =====================================================================
    {
        "id":            "KGC502",
        "subdir":        "Refinement",
        "name":          "Lemma 1 verdict-asymmetry: Compatible does NOT propagate through refinement [GeoNames]",
        "relation":      "refinement",
        "verdict":       "CompatibleNonPropagation",
        "status_fof":    "CounterSatisfiable",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "includes":      [
            "KGE000-0.ax",
            "DENOT000-0.ax",
            "REFINE000-0.ax",
            "GN000-0.ax",
        ],
        "needs_density": False,
        "description": (
            "Lemma 1 verdict-asymmetry. Lemma 1 is stated for Conflict only.\n"
            "The Compatible-analog -- 'c1 refines c2 AND verdict(c2, c3) =\n"
            "Compatible ==> verdict(c1, c3) = Compatible' -- is FALSE in\n"
            "general. KGC502 demonstrates this with a concrete counterexample.\n"
            "\n"
            "Setup:\n"
            "  c1 = (spatial, eq,        gn:Germany)\n"
            "         => [c1] = {gn_germany}\n"
            "  c2 = (spatial, isPartOf,  gn:Europe)\n"
            "         => [c2] = downward cone of gn_europe\n"
            "                  ⊇ {Europe, Germany, France, Bayern, ...}\n"
            "  c3 = (spatial, eq,        gn:France)\n"
            "         => [c3] = {gn_france}\n"
            "\n"
            "Refinement: [c1] = {Germany} subseteq [c2] (Germany <= Europe\n"
            "in GeoNames).  Real downward-cone inclusion.\n"
            "Premise:    verdict_compatible(c2, c3) holds. France is in the\n"
            "            cone of Europe (kge_leq(gn_france, gn_europe) in\n"
            "            GN000-0.ax), so [c2] cap [c3] = {France} -- a\n"
            "            non-empty witness exists.\n"
            "\n"
            "Compatible-analog conclusion verdict_compatible(c1, c3) FAILS:\n"
            "  [c1] cap [c3] = {Germany} cap {France} = empty.\n"
            "  No witness exists in the intersection.\n"
            "  Under OWA without SDA: verdict(c1, c3) = Unknown.\n"
            "  Under SDA:             verdict(c1, c3) = Conflict.\n"
            "  In neither case:       verdict(c1, c3) = Compatible.\n"
            "\n"
            "Refinement narrowed [c1] from [c2] but did not preserve the\n"
            "common satisfier. This is the structural reason Lemma 1 is\n"
            "one-directional: Conflict propagates, Compatible does not.\n"
            "\n"
            "Conjecture style A: the Compatible-analog implication is the\n"
            "conjecture. Vampire returns CounterSatisfiable: a model exists\n"
            "where the antecedents hold but the conclusion does not."
        ),
        "ttl": _ttl_three_constraints(
            "spatial",
            "eq",        "<https://sws.geonames.org/2921044/>",
            "isPartOf",  "<https://sws.geonames.org/6255148/>",
            "eq",        "<https://sws.geonames.org/3017382/>",
            lemma_note=(
                "Compatible-analog of Lemma 1 (FALSE in general):\n"
                "#   refines(c1, c2) AND verdict_compatible(c2, c3)\n"
                "#     =/=> verdict_compatible(c1, c3)\n"
                "# c1 refines c2: Germany is in the downward cone of Europe.\n"
                "# verdict(c2, c3) = Compatible: France is also in the cone\n"
                "#                  of Europe; witness France lies in the\n"
                "#                  intersection of [c2] and [c3].\n"
                "# But [c1] = {Germany} does not contain France, so\n"
                "# [c1] cap [c3] = empty. The witness was lost when [c1]\n"
                "# narrowed [c2] to a singleton."
            ),
        ),
        "fof_extra_decls": _fof_three_denotations(
            "den_eq(X, gn_germany)",
            "den_ispartof(X, gn_europe)",
            "den_eq(X, gn_france)",
        ),
        "fof_conjecture": (
            "(refines(c1, c2) & verdict_compatible(c2, c3))\n"
            "       => verdict_compatible(c1, c3)"
        ),
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun gn_germany () Concept)
(declare-fun gn_europe  () Concept)
(declare-fun gn_france  () Concept)
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
; GN000: parentFeature edges.
(assert (kge_leq gn_germany gn_europe))
(assert (kge_leq gn_france  gn_europe))
; Identity.
(assert (distinct gn_germany gn_europe gn_france))
;
; No SDA loaded: GeoNames asserts no kge_disjoint between Germany and
; France. The Compatible-analog implication has a model where the
; antecedents hold (refinement, Compatible premise) but the conclusion
; (verdict_compatible(c1, c3)) does not. SMT cross-check: Z3 returns
; sat -- no contradiction can be derived.
;
; The full Compatible-analog implication is tested in the FOF encoding
; via REFINE000-0.ax's refines_def and DENOT000-0.ax's
; verdict_compatible_def. The SMT side asserts only the resource axioms
; and confirms consistency.""",
    },
]