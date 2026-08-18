"""
problem_data_dpv.py
===================
Seven problems over the DPV purposes slice, one per thing that can go wrong.

    KGC310  isA R&D      x eq SR    -> Compatible    one resource premise
    KGC311  isA Purpose  x eq NCR   -> Compatible    two premises + transitivity
    KGC313  eq Marketing x eq SR    -> Unknown       nothing declares them apart
    KGC314  the same pair under a background theory that does  -> Incompatible
    KGC315  isA Purpose  x eq RIS   -> Compatible    six premises + transitivity
    KGC316  isA RIS      x eq Purpose -> Unknown     the order runs one way
    KGC317  isNoneOf {Mk} x eq Mk   -> Incompatible  from the constraints alone

KGC315 and KGC316 are the same two concepts in the two possible arrangements.
The order relates them in one direction only, so one is Compatible and the
other Unknown.  That asymmetry is what distinguishes isA from eq, and it is
why the sort has to be declared: at nom neither problem is well sorted.

KGC317 is the only Incompatible in the suite that rests on no declaration.
Its refutation cites the witness condition and nothing else, so no party can
withdraw a premise and reopen it.  Compare KGC300 and KGC314, whose verdicts
each rest on one withdrawable assertion.

KGC313 and KGC314 are the same constraints over the same resource, differing
only in the background theory.  What moves the verdict is the declaration,
and the certificate names it and marks it withdrawable.

KGC312 is not here.  It was (purpose, isA, NonCommercialPurpose) against
(purpose, eq, ScientificResearch), which is the motivating pair and is
already KGC301 in problem_data_motivating.py.  Both were built over this
resource and this background theory, so they were one test entered twice.
The number is left unused rather than reassigned, since it appears in the
run logs of earlier sessions.

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
Every pair below uses subset-mode operators only, so W(K) reduces to
D != empty,
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

  KGC315  D = {x | x <= purpose} and {ris},  named {purpose, ris}
          W = (purpose <= purpose & purpose = ris)
            | (ris <= purpose & ris = ris)
          ris <= purpose is six transitivity steps from the resource:
          ris <= rim <= rm <= ph <= pm <= hrm <= purpose.  Compatible, and
          the certificate should name six resource assertions.

  KGC316  D = {x | x <= ris} and {purpose},  named {ris, purpose}
          W = (ris <= ris & ris = purpose) | (purpose <= ris & purpose = purpose)
          The first disjunct needs ris = purpose, the second purpose <= ris.
          Neither is asserted and neither is denied, so both queries are
          satisfiable: Unknown.  Note that reflexivity makes ris <= ris hold
          in the first disjunct and purpose = purpose hold in the second, so
          what is left open is exactly the relation between the two concepts
          and nothing else.

  KGC317  D = complement{marketing} and {marketing},  named {marketing}
          W = (mk != mk & mk = mk)
          The only concept the grounding names is the one the offer excludes
          and the request requires.  The witness is false in every structure,
          on equality alone: no order assertion and no declaration takes
          part.  Incompatible, and nothing in the certificate is withdrawable.

  KGC313  D = {marketing} and {sr},  named {marketing, sr}
          W = (mk = mk & mk = sr) | (sr = mk & sr = sr)
          Two distinct names, no declared distinctness.  A model may
          identify them.  Unknown, and the pair to re-run once a party
          declares the two purposes distinct.

The unsimplified disjunction is emitted, since that is what the definition
prescribes and what a generator produces mechanically.

On the motivating pair and NonCommercialResearch
------------------------------------------------
This concerns KGC301 rather than any problem in this file, but the reading
of the resource belongs with the resource.


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

# The longest chain in the module, six edges with a single parent at each
# step.  Measured, not assumed: no concept on it has a second parent, so the
# route from bottom to top is unique and the certificate is predictable.
RIS  = "dpv_recruitment_interview_scheduling"
RIM  = "dpv_recruitment_interview_management"
RM   = "dpv_recruitment_management"
PH   = "dpv_personnel_hiring"
PM   = "dpv_personnel_management"
HRM  = "dpv_human_resource_management"

RESOURCE = "https://w3id.org/odrl-kb/dpv-purposes"
EMPTY_BT    = "https://w3id.org/odrl-kb/dpv-purposes/empty"
DECLARED_BT = "https://w3id.org/odrl-kb/dpv-purposes/declared"
INCLUDES          = ["KGE000-0.ax", "DPV-milestone.ax"]
INCLUDES_DECLARED = INCLUDES + ["DPV-milestone-declared.ax"]

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
        "smt2_asserts": f"""\
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
        "smt2_asserts": f"""\
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
        "smt2_asserts": f"""\
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
        "smt2_resource": f"""\
; Resource: unchanged from KGC313.
(assert (kge_leq {MK} {PUR}))
(assert (kge_leq {SR} {RND}))
(assert (kge_leq {RND} {PUR}))""",
        "smt2_background": f"""\
; Background theory: the declaration, and the only difference from KGC313.
; Named bt_, so that an unsat core attributes it to the parties rather than
; to the vocabulary.
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

    # -----------------------------------------------------------------
    # KGC315  The longest chain in the module, taken in the direction the
    # order runs.  Six resource assertions and transitivity.
    # -----------------------------------------------------------------
    {
        "id":                "KGC315",
        "subdir":            "verdict",
        "name":              "purpose, isA dpv:Purpose against eq dpv:RIS",
        "left_operand":      "purpose",
        "sort":              "tax",
        "resource":          RESOURCE,
        "background_theory": EMPTY_BT,
        "includes":          INCLUDES,
        "description": (
            "Offer (purpose, isA, dpv:Purpose) against request (purpose, eq, "
            "dpv:RecruitmentInterviewScheduling), the deepest concept in the "
            "module.  The resource relates them only through six steps, so "
            "the refutation must chain all six.  Compatible.  The verdict is "
            "the same as KGC310's; what grows with the depth is the "
            "certificate, not the answer."
        ),

        "fof_decls": """\
% Background theory: empty.
""",
        "fof_witness": f"""\
( ( kge_leq({PUR}, {PUR}) & {PUR} = {RIS} )
| ( kge_leq({RIS}, {PUR}) & {RIS} = {RIS} ) )""",

        "expected_q1": "Satisfiable",
        "expected_q2": "Unsatisfiable",

        "smt2_logic": "UF",
        "smt2_decls": _decls(RIS, RIM, RM, PH, PM, HRM, PUR),
        "smt2_resource": f"""\
; Resource: the six steps.  None of them asserts the chain.
(assert (kge_leq {RIS} {RIM}))
(assert (kge_leq {RIM} {RM}))
(assert (kge_leq {RM} {PH}))
(assert (kge_leq {PH} {PM}))
(assert (kge_leq {PM} {HRM}))
(assert (kge_leq {HRM} {PUR}))""",
        "smt2_background": "",
        "smt2_witness": f"""\
(or (and (kge_leq {PUR} {PUR}) (= {PUR} {RIS}))
    (and (kge_leq {RIS} {PUR}) (= {RIS} {RIS})))""",

        "certificate": {
            "kind": "Refutation",
            "comment": "Interview scheduling for recruitment lies below "
                       "purpose by six steps through recruitment, personnel, "
                       "and human resource management.  Every step is the "
                       "vocabulary's; none is the parties'.",
            "premises": [
                ("fromResource", "the six order assertions of the chain"),
                ("fromOrderAxiom", "transitivity"),
            ],
        },
        "ttl": f"""\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dpv:     <https://w3id.org/dpv#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .

drk:bsb-offer-315 a odrl:Offer ;
    dcterms:title "BSB offer: any declared purpose"@en ;
    odrl:assigner drk:bavarian-state-library ;
    odrl:permission kgc:KGC315-offer-r1 .

kgc:KGC315-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:bsb-manuscripts ;
    odrl:constraint kgc:KGC315-offer-c1 .

kgc:KGC315-offer-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:isA ;
    odrl:rightOperand dpv:Purpose .

drk:bnf-request-315 a odrl:Request ;
    dcterms:title "BnF request: recruitment interview scheduling"@en ;
    odrl:assignee drk:french-national-library ;
    odrl:permission kgc:KGC315-request-r1 .

kgc:KGC315-request-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:bsb-manuscripts ;
    odrl:constraint kgc:KGC315-request-c1 .

kgc:KGC315-request-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:RecruitmentInterviewScheduling .""",
    },

    # -----------------------------------------------------------------
    # KGC316  The same two concepts, the other way round.  The order
    # relates them downward and not upward, so the verdict changes even
    # though nothing about the resource has.
    # -----------------------------------------------------------------
    {
        "id":                "KGC316",
        "subdir":            "verdict",
        "name":              "purpose, isA dpv:RIS against eq dpv:Purpose",
        "left_operand":      "purpose",
        "sort":              "tax",
        "resource":          RESOURCE,
        "background_theory": EMPTY_BT,
        "includes":          INCLUDES,
        "description": (
            "KGC315 reversed: offer (purpose, isA, "
            "dpv:RecruitmentInterviewScheduling) against request (purpose, "
            "eq, dpv:Purpose).  The resource places the narrow concept below "
            "the broad one and says nothing the other way, so the verdict is "
            "Unknown.  The pair shows that isA reads the order in one "
            "direction: swapping the operands is not a symmetry of the "
            "semantics, and a reader who expects Compatible here has "
            "confused subsumption with identity."
        ),

        "fof_decls": """\
% Background theory: empty.
""",
        "fof_witness": f"""\
( ( kge_leq({RIS}, {RIS}) & {RIS} = {PUR} )
| ( kge_leq({PUR}, {RIS}) & {PUR} = {PUR} ) )""",

        "expected_q1": "Satisfiable",
        "expected_q2": "Satisfiable",

        "smt2_logic": "UF",
        "smt2_decls": _decls(RIS, RIM, RM, PH, PM, HRM, PUR),
        "smt2_resource": f"""\
; Resource: unchanged from KGC315.  What changed is the pair of
; constraints, and with it the direction the witness asks about.
(assert (kge_leq {RIS} {RIM}))
(assert (kge_leq {RIM} {RM}))
(assert (kge_leq {RM} {PH}))
(assert (kge_leq {PH} {PM}))
(assert (kge_leq {PM} {HRM}))
(assert (kge_leq {HRM} {PUR}))""",
        "smt2_background": "",
        "smt2_witness": f"""\
(or (and (kge_leq {RIS} {RIS}) (= {RIS} {PUR}))
    (and (kge_leq {PUR} {RIS}) (= {PUR} {PUR})))""",

        "certificate": {
            "kind": "Models",
            "comment": "Both queries are satisfiable.  A structure may place "
                       "purpose below interview scheduling, or identify the "
                       "two, or do neither; the vocabulary settles none of "
                       "these, and the chain it does publish runs the other "
                       "way.",
            "premises": [],
        },
        "ttl": f"""\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dpv:     <https://w3id.org/dpv#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .

drk:bsb-offer-316 a odrl:Offer ;
    dcterms:title "BSB offer: recruitment interview scheduling"@en ;
    odrl:assigner drk:bavarian-state-library ;
    odrl:permission kgc:KGC316-offer-r1 .

kgc:KGC316-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:bsb-manuscripts ;
    odrl:constraint kgc:KGC316-offer-c1 .

kgc:KGC316-offer-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:isA ;
    odrl:rightOperand dpv:RecruitmentInterviewScheduling .

drk:bnf-request-316 a odrl:Request ;
    dcterms:title "BnF request: any declared purpose"@en ;
    odrl:assignee drk:french-national-library ;
    odrl:permission kgc:KGC316-request-r1 .

kgc:KGC316-request-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:bsb-manuscripts ;
    odrl:constraint kgc:KGC316-request-c1 .

kgc:KGC316-request-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:Purpose .""",
    },

    # -----------------------------------------------------------------
    # KGC317  Complement against identity on one concept.  The only
    # Incompatible in the suite that rests on nothing withdrawable.
    # -----------------------------------------------------------------
    {
        "id":                "KGC317",
        "subdir":            "verdict",
        "name":              "purpose, isNoneOf {dpv:Marketing} against eq "
                             "dpv:Marketing",
        "left_operand":      "purpose",
        "sort":              "tax",
        "resource":          RESOURCE,
        "background_theory": EMPTY_BT,
        "includes":          INCLUDES,
        "description": (
            "Offer (purpose, isNoneOf, {dpv:Marketing}) against request "
            "(purpose, eq, dpv:Marketing).  The offer excludes exactly the "
            "purpose the request requires.  No order assertion and no "
            "declaration takes part: the witness asks for a concept both "
            "distinct from and identical to marketing, which no structure "
            "provides.  Incompatible, and the certificate has nothing "
            "withdrawable in it, so unlike KGC300 and KGC314 no party can "
            "reopen the verdict by retracting an assertion."
        ),

        "fof_decls": """\
% Background theory: empty, and it stays empty.  The incompatibility here
% is between the two constraints, not between a constraint and something a
% party declared.
""",
        "fof_witness": f"""\
( {MK} != {MK} & {MK} = {MK} )""",

        "expected_q1": "Unsatisfiable",
        "expected_q2": "Satisfiable",

        "smt2_logic": "UF",
        "smt2_decls": _decls(MK, PUR),
        "smt2_resource": f"""\
; Resource: marketing is a purpose.  The verdict does not use this.
(assert (kge_leq {MK} {PUR}))""",
        "smt2_background": "",
        "smt2_witness": f"""\
(and (not (= {MK} {MK})) (= {MK} {MK}))""",

        "certificate": {
            "kind": "Refutation",
            "comment": "The offer admits every purpose but marketing and the "
                       "request admits only marketing, so no purpose "
                       "satisfies both.  The refutation is on equality "
                       "alone and cites no assertion any party could "
                       "withdraw.",
            "premises": [
                ("fromConstraints", "the witness condition"),
            ],
        },
        "ttl": f"""\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dpv:     <https://w3id.org/dpv#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .

drk:bsb-offer-317 a odrl:Offer ;
    dcterms:title "BSB offer: any purpose other than marketing"@en ;
    odrl:assigner drk:bavarian-state-library ;
    odrl:permission kgc:KGC317-offer-r1 .

kgc:KGC317-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:bsb-manuscripts ;
    odrl:constraint kgc:KGC317-offer-c1 .

kgc:KGC317-offer-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:isNoneOf ;
    odrl:rightOperand dpv:Marketing .

drk:bnf-request-317 a odrl:Request ;
    dcterms:title "BnF request: marketing"@en ;
    odrl:assignee drk:french-national-library ;
    odrl:permission kgc:KGC317-request-r1 .

kgc:KGC317-request-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:bsb-manuscripts ;
    odrl:constraint kgc:KGC317-request-c1 .

kgc:KGC317-request-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:Marketing .""",
    },
]