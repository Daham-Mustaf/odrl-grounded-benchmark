"""
problem_data_dpv.py
===================
Five problems over the DPV purposes slice, one per thing that can go wrong.

    KGC310  isA R&D      x eq SR    -> Compatible    one resource premise
    KGC311  isA Purpose  x eq NCR   -> Compatible    two premises + transitivity
    KGC312  isA NCP      x eq SR    -> Unknown       the vocabulary is silent
    KGC313  eq Marketing x eq SR    -> Unknown       nothing declares them apart
    KGC314  the same pair under a background theory that does  -> Incompatible

KGC313 and KGC314 are the same constraints over the same resource, differing
only in the background theory.  What moves the verdict is the declaration,
and the certificate names it and marks it withdrawable.

The resource
------------
DPV 2.3, purposes module, read as SKOS: skos:broader is the only hierarchy
predicate.  The module publishes no owl:disjointWith, no owl:AllDifferent,
and no distinctness of any kind, so the background theory here is empty and
every verdict below rests on the order assertions and the constraints alone.

The order assertions the slice uses:

    scientific_research      <= research_and_development
    non_commercial_research  <= non_commercial_purpose
    non_commercial_research  <= research_and_development
    non_commercial_purpose   <= purpose
    research_and_development <= purpose
    marketing                <= purpose

The witness condition
---------------------
All four pairs use subset-mode operators only, so W(K) reduces to D != empty,
the finite disjunction over the concepts the grounding names:

    OR_c ( c is in every subset-mode denotation of K )

Derived per problem before running anything:

  KGC310  D = {x | x <= rnd} and {sr},  named {rnd, sr}
          W = (rnd <= rnd & rnd = sr) | (sr <= rnd & sr = sr)
          The resource asserts sr <= rnd, so the second disjunct holds in
          every model: W is entailed, q2 is unsatisfiable, Compatible.

  KGC311  D = {x | x <= purpose} and {ncr},  named {purpose, ncr}
          W = (purpose <= purpose & purpose = ncr)
            | (ncr <= purpose & ncr = ncr)
          ncr <= purpose is not asserted.  It follows by transitivity,
          along either of two chains: through non_commercial_purpose or
          through research_and_development, since DPV publishes ncr under
          both.  Which one a prover takes is its own affair; that some
          chain is needed is the point, and this is the first problem in
          the suite whose refutation must use the transitivity axiom.

  KGC312  D = {x | x <= ncp} and {sr},  named {ncp, sr}
          W = (ncp <= ncp & ncp = sr) | (sr <= ncp & sr = sr)
          No path relates them and nothing separates them, so a model may
          place sr under ncp and a model may not: both queries satisfiable.

  KGC313  D = {marketing} and {sr},  named {marketing, sr}
          W = (mk = mk & mk = sr) | (sr = mk & sr = sr)
          Two distinct names, no declared distinctness.  A model may
          identify them.  Unknown, and the pair to re-run once a party
          declares the two purposes distinct.

The unsimplified disjunction is emitted, since that is what the definition
prescribes and what a generator produces mechanically.

On KGC312 and NonCommercialResearch
-----------------------------------
DPV publishes NonCommercialResearch under both NonCommercialPurpose and
ResearchAndDevelopment.  The publisher therefore had the vocabulary to say
that research can be non-commercial, and placed ScientificResearch under
ResearchAndDevelopment alone.  The silence between ScientificResearch and
NonCommercialPurpose is a decision, not an omission, and Unknown reports it
rather than closing it.
"""

# Concepts, with the slugs the resource generator emits.
SR   = "dpv_scientific_research"
RND  = "dpv_research_and_development"
NCP  = "dpv_non_commercial_purpose"
NCR  = "dpv_non_commercial_research"
PUR  = "dpv_purpose"
MK   = "dpv_marketing"

RESOURCE = "https://w3id.org/odrl-kb/dpv-purposes"
EMPTY_BT    = "https://w3id.org/odrl-kb/dpv-purposes/empty"
DECLARED_BT = "https://w3id.org/odrl-kb/dpv-purposes/declared"
INCLUDES          = ["KGE000-0.ax", "DPV-milestone.ax"]
INCLUDES_DECLARED = INCLUDES + ["DPV-milestone-declared.ax"]

# The three order axioms, quantified, as SMT-LIB.  Emitted in full for every
# problem rather than instantiated at the concepts each one happens to need:
# selecting instances per problem makes the two encodings different theories
# and reads as fitting the encoding to the expected answer.
SMT_ORDER_AXIOMS = """\
; Order axioms, quantified.  The same three axioms as KGE000-0.ax, so the
; two encodings are the same theory.  Requires UF, not QF_UF.
(assert (forall ((x Concept)) (kge_leq x x)))
(assert (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))))
(assert (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))))"""


def _decls(*concepts):
    lines = ["(declare-sort Concept 0)"]
    lines += [f"(declare-fun {c} () Concept)" for c in concepts]
    lines.append("(declare-fun kge_leq (Concept Concept) Bool)")
    return "\n".join(lines)


PROBLEMS = [

    # -----------------------------------------------------------------
    # KGC310  One hop.  The smoke test: if this fails, the resource file
    # or the witness compiler is wrong and nothing further is informative.
    # -----------------------------------------------------------------
    {
        "id":                "KGC310",
        "subdir":            "verdict",
        "name":              "purpose, isA dpv:R&D against eq dpv:SR",
        "left_operand":      "purpose",
        "sort":              "tax",
        "resource":          RESOURCE,
        "background_theory": EMPTY_BT,
        "includes":          INCLUDES,
        "description": (
            "Offer (purpose, isA, dpv:ResearchAndDevelopment) against request "
            "(purpose, eq, dpv:ScientificResearch).  The vocabulary places "
            "the requested purpose under the offered one directly, so the "
            "witness holds in every model and the verdict is Compatible.  "
            "The refutation should cite one resource premise."
        ),

        "fof_decls": """\
% Background theory: empty.  The purposes module publishes no disjointness
% and no distinctness, and the parties declare none.
""",
        "fof_witness": f"""\
( ( kge_leq({RND}, {RND}) & {RND} = {SR} )
| ( kge_leq({SR},  {RND}) & {SR}  = {SR}  ) )""",

        "expected_q1": "Satisfiable",
        "expected_q2": "Unsatisfiable",

        "smt2_logic": "UF",
        "smt2_decls": _decls(RND, SR),
        "smt2_asserts": SMT_ORDER_AXIOMS + f"""
; Resource: the containment DPV publishes.
(assert (kge_leq {SR} {RND}))""",
        "smt2_witness": f"""\
(or (and (kge_leq {RND} {RND}) (= {RND} {SR}))
    (and (kge_leq {SR}  {RND}) (= {SR}  {SR})))""",

        "certificate": {
            "kind": "Refutation",
            "comment": "The resource places scientific research under "
                       "research and development, so every model admits the "
                       "common use and its absence is impossible.",
            "premises": [
                ("fromResource",
                 "dpv:ScientificResearch is below dpv:ResearchAndDevelopment"),
            ],
        },
        "ttl": f"""\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dpv:     <https://w3id.org/dpv#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .

drk:bsb-offer-310 a odrl:Offer ;
    dcterms:title "BSB offer: research and development purposes"@en ;
    odrl:assigner drk:bavarian-state-library ;
    odrl:permission kgc:KGC310-offer-r1 .

kgc:KGC310-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:bsb-manuscripts ;
    odrl:constraint kgc:KGC310-offer-c1 .

kgc:KGC310-offer-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:isA ;
    odrl:rightOperand dpv:ResearchAndDevelopment .

drk:bnf-request-310 a odrl:Request ;
    dcterms:title "BnF request: scientific research"@en ;
    odrl:assignee drk:french-national-library ;
    odrl:permission kgc:KGC310-request-r1 .

kgc:KGC310-request-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:bsb-manuscripts ;
    odrl:constraint kgc:KGC310-request-c1 .

kgc:KGC310-request-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:ScientificResearch .""",
    },

    # -----------------------------------------------------------------
    # KGC311  Two hops.  The first problem in the suite whose refutation
    # needs transitivity: the resource asserts neither ncr <= purpose nor
    # anything equivalent, only the two steps.
    # -----------------------------------------------------------------
    {
        "id":                "KGC311",
        "subdir":            "verdict",
        "name":              "purpose, isA dpv:Purpose against eq dpv:NCR",
        "left_operand":      "purpose",
        "sort":              "tax",
        "resource":          RESOURCE,
        "background_theory": EMPTY_BT,
        "includes":          INCLUDES,
        "description": (
            "Offer (purpose, isA, dpv:Purpose) against request (purpose, eq, "
            "dpv:NonCommercialResearch).  The resource relates the two only "
            "through dpv:NonCommercialPurpose, so the refutation must chain "
            "two order assertions.  Compatible, and the certificate should "
            "cite two resource premises and one instance of transitivity."
        ),

        "fof_decls": """\
% Background theory: empty, as above.
""",
        "fof_witness": f"""\
( ( kge_leq({PUR}, {PUR}) & {PUR} = {NCR} )
| ( kge_leq({NCR}, {PUR}) & {NCR} = {NCR} ) )""",

        "expected_q1": "Satisfiable",
        "expected_q2": "Unsatisfiable",

        "smt2_logic": "UF",
        "smt2_decls": _decls(PUR, NCR, NCP),
        "smt2_asserts": SMT_ORDER_AXIOMS + f"""
; Resource: the two steps.  Neither asserts the chain.
(assert (kge_leq {NCR} {NCP}))
(assert (kge_leq {NCP} {PUR}))""",
        "smt2_witness": f"""\
(or (and (kge_leq {PUR} {PUR}) (= {PUR} {NCR}))
    (and (kge_leq {NCR} {PUR}) (= {NCR} {NCR})))""",

        "certificate": {
            "kind": "Refutation",
            "comment": "Non-commercial research lies below purpose by way of "
                       "non-commercial purpose.  The resource asserts the two "
                       "steps and transitivity closes the chain.",
            "premises": [
                ("fromResource",
                 "dpv:NonCommercialResearch is below "
                 "dpv:NonCommercialPurpose"),
                ("fromResource",
                 "dpv:NonCommercialPurpose is below dpv:Purpose"),
                ("fromOrderAxiom", "transitivity"),
            ],
        },
        "ttl": f"""\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dpv:     <https://w3id.org/dpv#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .

drk:bsb-offer-311 a odrl:Offer ;
    dcterms:title "BSB offer: any declared purpose"@en ;
    odrl:assigner drk:bavarian-state-library ;
    odrl:permission kgc:KGC311-offer-r1 .

kgc:KGC311-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:bsb-manuscripts ;
    odrl:constraint kgc:KGC311-offer-c1 .

kgc:KGC311-offer-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:isA ;
    odrl:rightOperand dpv:Purpose .

drk:bnf-request-311 a odrl:Request ;
    dcterms:title "BnF request: non-commercial research"@en ;
    odrl:assignee drk:french-national-library ;
    odrl:permission kgc:KGC311-request-r1 .

kgc:KGC311-request-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:bsb-manuscripts ;
    odrl:constraint kgc:KGC311-request-c1 .

kgc:KGC311-request-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:NonCommercialResearch .""",
    },

    # -----------------------------------------------------------------
    # KGC312  The motivating pair, on the published slice.  Unknown
    # because DPV relates the two concepts in neither direction and
    # separates them in neither direction.
    # -----------------------------------------------------------------
    {
        "id":                "KGC312",
        "subdir":            "verdict",
        "name":              "purpose, isA dpv:NCP against eq dpv:SR",
        "left_operand":      "purpose",
        "sort":              "tax",
        "resource":          RESOURCE,
        "background_theory": EMPTY_BT,
        "includes":          INCLUDES,
        "description": (
            "Offer (purpose, isA, dpv:NonCommercialPurpose) against request "
            "(purpose, eq, dpv:ScientificResearch).  DPV places scientific "
            "research under research and development only, and publishes no "
            "disjointness, so a model may place it under non-commercial "
            "purpose and a model may not.  Unknown.  DPV does publish "
            "dpv:NonCommercialResearch under both parents, so the silence "
            "here is a decision rather than an omission."
        ),

        "fof_decls": """\
% Background theory: empty.  Asserting that the two concepts are unrelated
% would be the closed-world reading this paper rejects.
""",
        "fof_witness": f"""\
( ( kge_leq({NCP}, {NCP}) & {NCP} = {SR} )
| ( kge_leq({SR},  {NCP}) & {SR}  = {SR}  ) )""",

        "expected_q1": "Satisfiable",
        "expected_q2": "Satisfiable",

        "smt2_logic": "UF",
        "smt2_decls": _decls(NCP, SR, RND, PUR),
        "smt2_asserts": SMT_ORDER_AXIOMS + f"""
; Resource: what DPV publishes about these concepts.  Note that it relates
; scientific research to research and development, and not to the offered
; purpose in either direction.
(assert (kge_leq {SR} {RND}))
(assert (kge_leq {RND} {PUR}))
(assert (kge_leq {NCP} {PUR}))""",
        "smt2_witness": f"""\
(or (and (kge_leq {NCP} {NCP}) (= {NCP} {SR}))
    (and (kge_leq {SR}  {NCP}) (= {SR}  {SR})))""",

        "certificate": {
            "kind": "Models",
            "comment": "Both queries are satisfiable.  The models differ on "
                       "whether scientific research falls under "
                       "non-commercial purpose, which is what the vocabulary "
                       "leaves open.",
            "premises": [],
        },
        "ttl": f"""\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dpv:     <https://w3id.org/dpv#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .

drk:bsb-offer-312 a odrl:Offer ;
    dcterms:title "BSB offer: non-commercial purposes"@en ;
    odrl:assigner drk:bavarian-state-library ;
    odrl:permission kgc:KGC312-offer-r1 .

kgc:KGC312-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:bsb-manuscripts ;
    odrl:constraint kgc:KGC312-offer-c1 .

kgc:KGC312-offer-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:isA ;
    odrl:rightOperand dpv:NonCommercialPurpose .

drk:bnf-request-312 a odrl:Request ;
    dcterms:title "BnF request: scientific research"@en ;
    odrl:assignee drk:french-national-library ;
    odrl:permission kgc:KGC312-request-r1 .

kgc:KGC312-request-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:bsb-manuscripts ;
    odrl:constraint kgc:KGC312-request-c1 .

kgc:KGC312-request-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:ScientificResearch .""",
    },

    # -----------------------------------------------------------------
    # KGC313  Unknown for the other reason: two names the resource never
    # relates and the background theory never separates.  Pair this with
    # a background theory declaring them distinct and the verdict moves
    # to Incompatible; that is the stability demonstration.
    # -----------------------------------------------------------------
    {
        "id":                "KGC313",
        "subdir":            "verdict",
        "name":              "purpose, eq dpv:Marketing against eq dpv:SR",
        "left_operand":      "purpose",
        "sort":              "tax",
        "resource":          RESOURCE,
        "background_theory": EMPTY_BT,
        "includes":          INCLUDES,
        "description": (
            "Offer (purpose, eq, dpv:Marketing) against request (purpose, eq, "
            "dpv:ScientificResearch).  Both denote singletons, and the two "
            "constraints are satisfiable together only if the two concepts "
            "are the same.  DPV publishes no distinctness, so a model may "
            "identify them: Unknown.  The same pair under a background "
            "theory declaring the two purposes distinct is Incompatible, "
            "which is what makes the declaration visible in the verdict."
        ),

        "fof_decls": """\
% Background theory: empty.  Two names are not two concepts until something
% says so, and the purposes module says nothing.
""",
        "fof_witness": f"""\
( ( {MK} = {MK} & {MK} = {SR} )
| ( {SR} = {MK} & {SR} = {SR} ) )""",

        "expected_q1": "Satisfiable",
        "expected_q2": "Satisfiable",

        "smt2_logic": "UF",
        "smt2_decls": _decls(MK, SR, RND, PUR),
        "smt2_asserts": SMT_ORDER_AXIOMS + f"""
; Resource: both are purposes, by different routes.  Neither route makes
; them distinct.
(assert (kge_leq {MK} {PUR}))
(assert (kge_leq {SR} {RND}))
(assert (kge_leq {RND} {PUR}))""",
        "smt2_witness": f"""\
(or (and (= {MK} {MK}) (= {MK} {SR}))
    (and (= {SR} {MK}) (= {SR} {SR})))""",

        "certificate": {
            "kind": "Models",
            "comment": "Both queries are satisfiable.  The models differ on "
                       "whether the two names denote one purpose, which no "
                       "assertion settles.",
            "premises": [],
        },
        "ttl": f"""\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dpv:     <https://w3id.org/dpv#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .

drk:bsb-offer-313 a odrl:Offer ;
    dcterms:title "BSB offer: marketing"@en ;
    odrl:assigner drk:bavarian-state-library ;
    odrl:permission kgc:KGC313-offer-r1 .

kgc:KGC313-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:bsb-manuscripts ;
    odrl:constraint kgc:KGC313-offer-c1 .

kgc:KGC313-offer-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:Marketing .

drk:bnf-request-313 a odrl:Request ;
    dcterms:title "BnF request: scientific research"@en ;
    odrl:assignee drk:french-national-library ;
    odrl:permission kgc:KGC313-request-r1 .

kgc:KGC313-request-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:bsb-manuscripts ;
    odrl:constraint kgc:KGC313-request-c1 .

kgc:KGC313-request-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:ScientificResearch .""",
    },

    # -----------------------------------------------------------------
    # KGC314  KGC313 again, under a background theory that separates the
    # two purposes.  Same resource, same constraints, same witness: only
    # the declaration differs, and the verdict moves.  The refutation is
    # attributable to an assertion a party can withdraw.
    # -----------------------------------------------------------------
    {
        "id":                "KGC314",
        "subdir":            "verdict",
        "name":              "purpose, eq dpv:Marketing against eq dpv:SR, "
                             "under a declared distinctness",
        "left_operand":      "purpose",
        "sort":              "tax",
        "resource":          RESOURCE,
        "background_theory": DECLARED_BT,
        "includes":          INCLUDES_DECLARED,
        "description": (
            "The constraints of KGC313, over the same resource, under a "
            "background theory in which the parties declare the two purposes "
            "distinct.  No model then identifies them, the witness fails "
            "everywhere, and the verdict is Incompatible.  DPV publishes no "
            "such distinctness: the verdict rests on the declaration, and "
            "the certificate marks it withdrawable."
        ),

        "fof_decls": """\
% Background theory: one declared distinctness, from
% DPV-milestone-declared.ax.  Nothing in DPV separates these purposes.
""",
        "fof_witness": f"""\
( ( {MK} = {MK} & {MK} = {SR} )
| ( {SR} = {MK} & {SR} = {SR} ) )""",

        "expected_q1": "Unsatisfiable",
        "expected_q2": "Satisfiable",

        "smt2_logic": "UF",
        "smt2_decls": _decls(MK, SR, RND, PUR),
        "smt2_asserts": SMT_ORDER_AXIOMS + f"""
; Resource: unchanged from KGC313.
(assert (kge_leq {MK} {PUR}))
(assert (kge_leq {SR} {RND}))
(assert (kge_leq {RND} {PUR}))
; Background theory: the declaration, and the only difference from KGC313.
(assert (distinct {MK} {SR}))""",
        "smt2_witness": f"""\
(or (and (= {MK} {MK}) (= {MK} {SR}))
    (and (= {SR} {MK}) (= {SR} {SR})))""",

        "certificate": {
            "kind": "Refutation",
            "comment": "The two constraints require one purpose to be both "
                       "concepts, and the declaration holds them apart.  The "
                       "premise is the parties', not the vocabulary's: "
                       "withdrawing it returns the verdict to Unknown.",
            "premises": [
                ("fromBackgroundTheory",
                 "dpv:Marketing and dpv:ScientificResearch are declared "
                 "distinct"),
            ],
        },
        "ttl": f"""\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dpv:     <https://w3id.org/dpv#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .

drk:bsb-offer-314 a odrl:Offer ;
    dcterms:title "BSB offer: marketing"@en ;
    odrl:assigner drk:bavarian-state-library ;
    odrl:permission kgc:KGC314-offer-r1 .

kgc:KGC314-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:bsb-manuscripts ;
    odrl:constraint kgc:KGC314-offer-c1 .

kgc:KGC314-offer-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:Marketing .

drk:bnf-request-314 a odrl:Request ;
    dcterms:title "BnF request: scientific research"@en ;
    odrl:assignee drk:french-national-library ;
    odrl:permission kgc:KGC314-request-r1 .

kgc:KGC314-request-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:bsb-manuscripts ;
    odrl:constraint kgc:KGC314-request-c1 .

kgc:KGC314-request-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:ScientificResearch .""",
    },
]