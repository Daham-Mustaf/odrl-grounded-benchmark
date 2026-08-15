"""
problem_data_runtime.py
=======================
Theorem 3 audit: Runtime soundness layer of the paper's denotational
semantics.

Theorem 3 (paper Section 3.6): If verdict(c1, c2) = Conflict, then no
request R satisfies both c1 and c2.

This module produces problems exercising the runtime layer:

  KGC600 -- Theorem 3 universal.
            For any request R, static Conflict(c1, c2) implies R does
            not satisfy both c1 and c2. Quantifies over all possible
            requests; tests the theorem in its full generality.
            Resource: BCP 47 (only resource asserting disjointness for
            a Conflict premise).
            Style A: conjecture is the implication.
            Expected FOF status: Theorem.

  KGC601 -- (planned, write after KGC600 audit clean)
  KGC602 -- (planned, write after KGC600 audit clean)
"""

# ---------------------------------------------------------------------------
# Shared TTL header.
# ---------------------------------------------------------------------------
_TTL_PREFIX = """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix bcp:  <https://tools.ietf.org/html/bcp47#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
"""


def _ttl_two_constraints(left_operand: str,
                         op1: str, val1: str,
                         op2: str, val2: str,
                         note: str = "") -> str:
    """Render a TTL fragment showing the constraint pair."""
    note_block = f"# {note}\n" if note else ""
    return _TTL_PREFIX + f"""
drk:c1 a odrl:Constraint ;
  odrl:leftOperand odrl:{left_operand} ;
  odrl:operator odrl:{op1} ;
  odrl:rightOperand {val1} .

drk:c2 a odrl:Constraint ;
  odrl:leftOperand odrl:{left_operand} ;
  odrl:operator odrl:{op2} ;
  odrl:rightOperand {val2} .

{note_block}"""


# ---------------------------------------------------------------------------
# Problem grid (KGC600 only for now).
# ---------------------------------------------------------------------------
PROBLEMS = [
    # =====================================================================
    # KGC600 -- Theorem 3 universal (BCP 47).
    # =====================================================================
    {
        "id":            "KGC600",
        "subdir":        "Runtime",
        "name":          "Theorem 3 universal: static Conflict implies no request satisfies both [BCP 47]",
        "relation":      "runtime",
        "verdict":       "RuntimeSoundness",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "includes":      [
            "KGE000-0.ax",
            "DENOT000-0.ax",
            "RUNTIME000-0.ax",
            "BCP47000-0.ax",
        ],
        "needs_density": False,
        "description": (
            "Theorem 3 universal case. Demonstrates that a static Conflict\n"
            "verdict between c1 and c2 implies no runtime request R can\n"
            "satisfy both constraints simultaneously.\n"
            "\n"
            "Setup:\n"
            "  c1 = (language, eq, bcp:de)  =>  [c1] = {bcp_de}\n"
            "  c2 = (language, eq, bcp:fr)  =>  [c2] = {bcp_fr}\n"
            "\n"
            "Static side:\n"
            "  Both denotations defined; intersection [c1] cap [c2] is empty\n"
            "  and forced empty via BCP 47's kge_disjoint(bcp_de, bcp_fr).\n"
            "  By verdict_conflict_def, verdict_conflict(c1, c2) holds.\n"
            "\n"
            "Runtime side:\n"
            "  operand_of(c1, language) and operand_of(c2, language) tie\n"
            "  the constraints to the language operand.\n"
            "  grounded_as_value functionality is asserted problem-locally:\n"
            "  the runtime grounding map gamma is deterministic. This is\n"
            "  not in RUNTIME000-0.ax because gamma is conceptually\n"
            "  resource-side; we make the functionality assumption explicit\n"
            "  here.\n"
            "  No specific request is asserted: the conjecture quantifies\n"
            "  universally over R.\n"
            "\n"
            "Theorem 3 conclusion:\n"
            "  ![R]: ~(satisfies(R, c1) & satisfies(R, c2)).\n"
            "  Proof sketch: any R satisfying both would witness L, V, G\n"
            "  for c1 and L', V', G' for c2. Both operand_of's force\n"
            "  L = L' = language. omega_functional forces V = V'.\n"
            "  grounded_as_value functionality forces G = G'. Then\n"
            "  in_denotation(G, c1) and in_denotation(G, c2) requires\n"
            "  G = bcp_de and G = bcp_fr, contradicting BCP47's distinct.\n"
            "\n"
            "Conjecture style A: full implication.\n"
            "  verdict_conflict(c1, c2) => ![R]: ~(sat(R, c1) & sat(R, c2))."
        ),
        "ttl": _ttl_two_constraints(
            "language",
            "eq", "bcp:de",
            "eq", "bcp:fr",
            note=(
                "Theorem 3 (paper Section 3.6):\n"
                "#   verdict_conflict(c1, c2) ==> no request R satisfies both.\n"
                "# Static Conflict via BCP 47 registry uniqueness.\n"
                "# Universal conjecture: holds for ALL possible requests."
            ),
        ),
    "fof_extra_decls": """\
% --- Static-side wiring ---------------------------------------------------
fof(c1_defined, axiom, ~denotation_undef(c1)).
fof(c2_defined, axiom, ~denotation_undef(c2)).
fof(c1_den, axiom, ![X]: (in_denotation(X, c1) <=> den_eq(X, bcp_de))).
fof(c2_den, axiom, ![X]: (in_denotation(X, c2) <=> den_eq(X, bcp_fr))).

% --- Runtime hooks --------------------------------------------------------
fof(c1_operand, axiom, operand_of(c1, language)).
fof(c2_operand, axiom, operand_of(c2, language)).

% Functionality of operand_of: each constraint has at most one left operand.
% Per Definition 2 of the paper, a constraint is a triple (l, op, v_or_S);
% l is single-valued. Not axiomatized in RUNTIME000-0.ax (it's a structural
% property of the encoding, not the runtime layer); we assert it here.
fof(operand_of_functional, axiom,
    ![C, L1, L2]:
      ((operand_of(C, L1) & operand_of(C, L2))
        => L1 = L2)).

% Functionality of the runtime grounding map gamma.
% Definition 1 in the paper says gamma is a partial function: each value
% V maps to at most one concept G. RUNTIME000-0.ax does not axiomatize
% this; we assert it here so the proof can equate G witnesses across
% sat(R, c1) and sat(R, c2) for the same V.
fof(grounded_as_value_functional, axiom,
    ![V, G1, G2]:
      ((grounded_as_value(V, G1) & grounded_as_value(V, G2))
        => G1 = G2)).
""",
        "fof_conjecture": (
            "verdict_conflict(c1, c2)\n"
            "       => (![R]: ~(satisfies(R, c1) & satisfies(R, c2)))"
        ),
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)
(declare-fun kge_disjoint (Concept Concept) Bool)""",
        "smt2_asserts": """\
; KGE000 load-bearing axioms.
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
(assert (forall ((c Concept)) (not (kge_disjoint c c))))
; BCP47000: registry uniqueness.
(assert (kge_disjoint bcp_de bcp_fr))
(assert (distinct bcp_de bcp_fr))
;
; This SMT encoding tests the conclusion-level Conflict between c1 and c2
; on a witness basis, not the full universal Theorem 3 statement.
; Theorem 3's universal quantifier over requests R, the operand_of /
; grounded_as_value indirection, and the satisfies_def biconditional are
; tested in the FOF encoding via RUNTIME000-0.ax.
;
; Witness query: a single x in both [c1] and [c2] (i.e., x = bcp_de and
; x = bcp_fr). Contradicts (distinct bcp_de bcp_fr). Z3 returns unsat.
(declare-fun x () Concept)
(assert (= x bcp_de))
(assert (= x bcp_fr))""",
    },
# =====================================================================
    # KGC601 -- Theorem 3 specialized to a concrete request (BCP 47).
    # =====================================================================
    {
        "id":            "KGC601",
        "subdir":        "Runtime",
        "name":          "Theorem 3 concrete request: r0 satisfies c1, must NOT satisfy c2 [BCP 47]",
        "relation":      "runtime",
        "verdict":       "RuntimeSoundness",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "includes":      [
            "KGE000-0.ax",
            "DENOT000-0.ax",
            "RUNTIME000-0.ax",
            "BCP47000-0.ax",
        ],
        "needs_density": False,
        "description": (
            "Theorem 3 specialized to a concrete request. Demonstrates that\n"
            "a runtime request witnessing one constraint of a Conflict pair\n"
            "is forbidden from witnessing the other.\n"
            "\n"
            "Setup:\n"
            "  c1 = (language, eq, bcp:de)  =>  [c1] = {bcp_de}\n"
            "  c2 = (language, eq, bcp:fr)  =>  [c2] = {bcp_fr}\n"
            "  verdict_conflict(c1, c2) holds via BCP 47 disjointness.\n"
            "\n"
            "Concrete request:\n"
            "  r0 assigns the language operand the value val_de.\n"
            "  val_de grounds to the concept bcp_de.\n"
            "\n"
            "Theorem 3 specialization:\n"
            "  satisfies(r0, c1) holds: witnesses L = language, V = val_de,\n"
            "    G = bcp_de; in_denotation(bcp_de, c1) holds since\n"
            "    [c1] = {bcp_de}.\n"
            "  ~satisfies(r0, c2) must hold: any L', V', G' witnesses must\n"
            "    equal language, val_de, bcp_de via the three functionality\n"
            "    axioms, then in_denotation(bcp_de, c2) requires\n"
            "    bcp_de = bcp_fr, contradicting BCP47 distinctness.\n"
            "\n"
            "Conjecture style A: conjunctive (positive + negative). Tests\n"
            "the runtime layer on a single concrete witness rather than\n"
            "universally."
        ),
        "ttl": _ttl_two_constraints(
            "language",
            "eq", "bcp:de",
            "eq", "bcp:fr",
            note=(
                "Theorem 3 concrete-request specialization:\n"
                "#   verdict_conflict(c1, c2) AND r0 satisfies c1\n"
                "#     ==> r0 does NOT satisfy c2.\n"
                "# r0 = the runtime request that assigns 'de' to language.\n"
                "# val_de grounds to bcp_de via gamma."
            ),
        ),
        "fof_extra_decls": """\
% --- Static-side wiring ---------------------------------------------------
fof(c1_defined, axiom, ~denotation_undef(c1)).
fof(c2_defined, axiom, ~denotation_undef(c2)).
fof(c1_den, axiom, ![X]: (in_denotation(X, c1) <=> den_eq(X, bcp_de))).
fof(c2_den, axiom, ![X]: (in_denotation(X, c2) <=> den_eq(X, bcp_fr))).

% --- Runtime hooks --------------------------------------------------------
fof(c1_operand, axiom, operand_of(c1, language)).
fof(c2_operand, axiom, operand_of(c2, language)).

fof(operand_of_functional, axiom,
    ![C, L1, L2]:
      ((operand_of(C, L1) & operand_of(C, L2))
        => L1 = L2)).

fof(grounded_as_value_functional, axiom,
    ![V, G1, G2]:
      ((grounded_as_value(V, G1) & grounded_as_value(V, G2))
        => G1 = G2)).

% --- Concrete request r0 --------------------------------------------------
% r0 assigns the language operand the value val_de;
% gamma grounds val_de to bcp_de.
fof(r0_assigns,         axiom, omega_assigns(r0, language, val_de)).
fof(val_de_grounds,     axiom, grounded_as_value(val_de, bcp_de)).
""",
        "fof_conjecture": (
            "satisfies(r0, c1) & ~satisfies(r0, c2)"
        ),
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)
(declare-fun kge_disjoint (Concept Concept) Bool)""",
        "smt2_asserts": """\
; KGE000 load-bearing axioms.
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
(assert (forall ((c Concept)) (not (kge_disjoint c c))))
; BCP47000: registry uniqueness.
(assert (kge_disjoint bcp_de bcp_fr))
(assert (distinct bcp_de bcp_fr))
;
; SMT scope: as in KGC600, the SMT side cross-checks the conclusion-level
; Conflict between c1 and c2. The full runtime chain (operand_of,
; omega_assigns, grounded_as_value, satisfies_def) is tested in FOF only.
;
; Witness query: a single x in both [c1] and [c2]. Contradicts
; (distinct bcp_de bcp_fr).
(declare-fun x () Concept)
(assert (= x bcp_de))
(assert (= x bcp_fr))""",
    },

    # =====================================================================
    # KGC602 -- Default-deny via undef grounding.
    # =====================================================================
    {
        "id":            "KGC602",
        "subdir":        "Runtime",
        "name":          "Default-deny: undef-grounded constraint admits no satisfying request [BCP 47]",
        "relation":      "runtime",
        "verdict":       "RuntimeSoundness",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      [
            "KGE000-0.ax",
            "DENOT000-0.ax",
            "RUNTIME000-0.ax",
            "BCP47000-0.ax",
        ],
        "needs_density": False,
        "description": (
            "Default-deny corner case. Tests that the runtime layer\n"
            "correctly refuses to satisfy any constraint whose denotation\n"
            "is undefined.\n"
            "\n"
            "Setup:\n"
            "  c_undef is a constraint over the language operand whose\n"
            "  right-operand value did not ground successfully (e.g., a\n"
            "  typo or deprecated tag like bcp:xz). Its denotation is\n"
            "  undef.\n"
            "\n"
            "  Per Definition 4 of the paper, an undef denotation must\n"
            "  yield denotation_undef(c_undef) -- asserted directly here\n"
            "  rather than derived from a denotation bridge.\n"
            "\n"
            "Default-deny via satisfies_def:\n"
            "  satisfies(R, c_undef) requires ~denotation_undef(c_undef)\n"
            "  as one of its conjuncts. Since denotation_undef(c_undef)\n"
            "  is asserted, the conjunct fails for any R, L, V, G witness\n"
            "  combination. Hence ~satisfies(R, c_undef) for all R.\n"
            "\n"
            "This is the only problem in the audit grid that exercises\n"
            "the undef branch of satisfies_def. The operand-level audit\n"
            "always asserts ~denotation_undef.\n"
            "\n"
            "Conjecture style A: universal closure ![R]: ~sat(R, c_undef).\n"
            "No functionality axioms or concrete request needed -- the\n"
            "default-deny fires before any L/V/G witnesses are reached."
        ),
        "ttl": _TTL_PREFIX + """
drk:c_undef a odrl:Constraint ;
  odrl:leftOperand odrl:language ;
  odrl:operator odrl:eq ;
  odrl:rightOperand bcp:xz .

# bcp:xz is not a registered BCP 47 tag.
# Per Definition 4 of the paper, gamma(bcp:xz) is undefined,
# so denotation(c_undef) = undef. Default-deny applies at runtime:
# no request can satisfy c_undef regardless of its assignment.
""",
        "fof_extra_decls": """\
% --- Static-side wiring ---------------------------------------------------
% c_undef's right-operand value does not ground; per Definition 4,
% denotation(c_undef) = undef.  Asserted directly (no denotation bridge).
fof(c_undef_undef, axiom, denotation_undef(c_undef)).

% --- Runtime hooks --------------------------------------------------------
% operand_of/2: c_undef's left operand is language.
fof(c_undef_operand, axiom, operand_of(c_undef, language)).
""",
        "fof_conjecture": (
            "![R]: ~satisfies(R, c_undef)"
        ),
        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Constraint 0)
(declare-fun c_undef () Constraint)
(declare-fun denotation_undef (Constraint) Bool)""",
        "smt2_asserts": """\
; SMT side directly tests the default-deny conclusion via the
; denotation_undef predicate.  satisfies(_, c_undef) requires
; ~denotation_undef(c_undef), which contradicts the asserted fact.
(assert (denotation_undef c_undef))
;
; A request satisfies c_undef only if denotation_undef does not hold.
; The negation of the conjecture asserts a witness; combined with the
; above, contradiction follows immediately.
(declare-fun sat_witness () Bool)
(assert (=> sat_witness (not (denotation_undef c_undef))))
(assert sat_witness)""",
    },
]