# =====================================================================
# problem_data_dpv.py: three blocks to replace
# Twelve problems over the DPV purposes slice.
# Nothing else in the file changes. The duplicates were being
# overwritten by Python, so the verdicts do not move; what changes is
# that the file stops carrying another resource's constants.
# =====================================================================


from compile import Constraint, Or

SR   = "dpv_scientific_research"
RND  = "dpv_research_and_development"
MK   = "dpv_marketing"
ADV  = "dpv_advertising"
SVC  = "dpv_service_provision"
NCP  = "dpv_non_commercial_purpose"
NCR  = "dpv_non_commercial_research"
PUR  = "dpv_purpose"

# The longest chain in the module, six edges with a single parent at each
# step.  Measured, not assumed: no concept on it has a second parent, so
# the route from bottom to top is unique and the certificate is
# predictable.
RIS  = "dpv_recruitment_interview_scheduling"
RIM  = "dpv_recruitment_interview_management"
RM   = "dpv_recruitment_management"
PH   = "dpv_personnel_hiring"
PM   = "dpv_personnel_management"
HRM  = "dpv_human_resource_management"

RESOURCE          = "https://w3id.org/odrl-kb/dpv-purposes"
EMPTY_BT          = "https://w3id.org/odrl-kb/dpv-purposes/empty"
DECLARED_BT       = "https://w3id.org/odrl-kb/dpv-purposes/declared"
BINDING           = "https://w3id.org/odrl-kb/profile/b-purpose"
INCLUDES          = ["KGE000-0.ax", "DPV-dpv-purposes.ax"]
INCLUDES_DECLARED = INCLUDES + ["DPV-dpv-purposes-declared.ax"]


def C(op, *vals, side="offer"):
    return Constraint(op, tuple(vals), side)


def _iso(*pairs):
    """Declared-distinctness instances, named bg_dist_ on both encodings.

    The declared theory states the rule and lists the purposes it ranges
    over; a problem naming two of them carries the inequation between
    them, so a refutation cites the instance it used rather than one
    term standing for all of them. The name must match on both sides:
    an unsat core and a TPTP proof are compared by premise name.
    """
    fof = ["% Background theory: declared distinctness instances, stated in",
           "% the declared theory file and instantiated here.", ""]
    smt = ["; Declared distinctness this problem adopts, named as the TPTP",
           "; side names it."]
    for a, b in pairs:
        n = f"bg_dist_{a}_{b}"
        fof.append(f"fof({n}, axiom,\n    {a} != {b}).")
        smt.append(f"(assert (! (not (= {a} {b})) :named {n}))")
    return "\n".join(fof) + "\n", "\n".join(smt)


_HEAD = """\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dpv:     <https://w3id.org/dpv#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .
"""


def _cnode(pid, side, i, left_operand, operator, values):
    ro = " ,\n        ".join(f"dpv:{v}" for v in values)
    return f"""
kgc:{pid}-{side}-c{i} a odrl:Constraint ;
    odrl:leftOperand {left_operand} ;
    odrl:operator odrl:{operator} ;
    odrl:rightOperand {ro} .
"""


def _side(pid, role, cls, title, party, lo, constraints, connective=None):
    n = pid[3:]
    cids = [f"{pid}-{role}-c{i+1}" for i in range(len(constraints))]
    if len(cids) == 1:
        cref, lc = f"kgc:{cids[0]}", ""
    else:
        cref = f"kgc:{pid}-{role}-lc"
        lc = (f"kgc:{pid}-{role}-lc a odrl:LogicalConstraint ;\n"
              f"    odrl:{connective} ( "
              + " ".join(f"kgc:{c}" for c in cids) + " ) .\n")
    body = (f"drk:{role}-{n} a odrl:{cls} ;\n"
            f'    dcterms:title "{title}"@en ;\n'
            f"    {party}\n"
            f"    odrl:permission kgc:{pid}-{role}-r1 .\n"
            f"kgc:{pid}-{role}-r1 a odrl:Permission ;\n"
            f"    odrl:action odrl:use ;\n"
            f"    odrl:target drk:dataset ;\n"
            f"    odrl:constraint {cref} .\n" + lc)
    for cid, (op, vals) in zip(cids, constraints):
        body += _cnode(cid, lo, op, vals)
    return body


def _ttl(pid, lo, offer_title, offer_cs, req_title, req_cs, connective=None):
    return (_HEAD
            + _side(pid, "offer", "Offer", "Offer: " + offer_title,
                    "odrl:assigner drk:provider ;", lo, offer_cs, connective)
            + _side(pid, "request", "Request", "Request: " + req_title,
                    "odrl:assignee drk:consumer ;", lo, req_cs))


PURPOSE = "odrl:purpose"

_D394 = _iso((SR, RND), (SR, MK))
_D397 = _iso((ADV, MK))


def _decls(*concepts):
    lines = ["(declare-sort Concept 0)"]
    lines += [f"(declare-fun {c} () Concept)" for c in concepts]
    lines.append("(declare-fun kge_leq (Concept Concept) Bool)")
    return "\n".join(lines)
"""
Twelve problems over the DPV purposes slice.

The order-based seven, one per thing that can go wrong:

    KGC310  isA R&D      x eq SR    -> Compatible    one resource premise
    KGC311  isA Purpose  x eq NCR   -> Compatible    two premises + transitivity
    KGC313  eq Marketing x eq SR    -> Unknown       nothing declares them apart
    KGC314  the same pair under a theory that does   -> Incompatible
    KGC315  isA Purpose  x eq RIS   -> Compatible    six premises + transitivity
    KGC316  isA RIS      x eq Purpose -> Unknown     the order runs one way
    KGC317  isNoneOf {Mk} x eq Mk   -> Incompatible  from the constraints alone

And five on the set operators, which read identity and not the order:

    KGC393  isAnyOf {RnD, Mk} x eq SR         -> Unknown
    KGC394  the same under declared distinctness -> Incompatible
    KGC395  or(isA RnD, isA Mk) x eq SR       -> Compatible
    KGC396  isAnyOf {RnD, Mk} x isAllOf {RnD, Svc} -> Compatible
    KGC397  isNoneOf {Mk} x eq Advertising    -> Compatible

KGC393 and KGC395 are one intention drafted two ways: enumerating the
values, and naming the branches that hold them. Both are legitimate and
they behave differently as the vocabulary grows. KGC396 is an intention
no operator expresses, and KGC397 is the purpose twin of the spatial
case KGC392.

Declarations over this resource
-------------------------------
The module publishes concepts below two parents: NonCommercialResearch
lies below both NonCommercialPurpose and ResearchAndDevelopment, and ten
other concepts have two parents. Those pairs may be declared distinct,
which is what the declared theory states, and may not be declared
disjoint: the resource publishes a concept below both, so the theory and
the resource would share no model.
"""
PROBLEMS = [

    {
        "id":                "KGC310",
        "subdir":            "verdict",
        "name":              "purpose, isA dpv:R&D against eq dpv:SR",
        "left_operand":      "purpose",
        "sort":              "tax",
        "resource":          RESOURCE,
        "background_theory": EMPTY_BT,
        "binding": BINDING,
        "includes":          INCLUDES,
        "summary": (
    "A library permits use for research and development, and a researcher "
    "requests use for scientific research."
),
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
"comment": (
    "ScientificResearch is directly below ResearchAndDevelopment in DPV, "
    "so the request is compatible with the offer."
),
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

drk:offer-310 a odrl:Offer ;
    dcterms:title "Offer: research and development purposes"@en ;
    odrl:assigner drk:library ;
    odrl:permission kgc:KGC310-offer-r1 .

kgc:KGC310-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC310-offer-c1 .

kgc:KGC310-offer-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:isA ;
    odrl:rightOperand dpv:ResearchAndDevelopment .

drk:request-310 a odrl:Request ;
    dcterms:title "Request: scientific research"@en ;
    odrl:assignee drk:researcher ;
    odrl:permission kgc:KGC310-request-r1 .

kgc:KGC310-request-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
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
         "binding": BINDING,
        "summary": (
    "A library permits use for any DPV purpose, and a researcher requests "
    "use for non-commercial research."
),
            "description": (
            "Offer (purpose, isA, dpv:Purpose) against request (purpose, eq, "
            "dpv:NonCommercialResearch).  The resource places "
            "NonCommercialResearch below two parents, including "
            "dpv:ResearchAndDevelopment, which is below dpv:Purpose.  The "
            "refutation uses that ResearchAndDevelopment path and transitivity. "
            "Compatible, with two resource premises and one instance of "
            "transitivity."
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
            "comment": (
                "NonCommercialResearch is below ResearchAndDevelopment, which "
                "is below Purpose; the certificate uses this two-step path."
            ),
            "premises": [
                ("fromResource",
                 "dpv:NonCommercialResearch is below "
                 "dpv:ResearchAndDevelopment"),
                ("fromResource",
                 "dpv:ResearchAndDevelopment is below dpv:Purpose"),
                ("fromOrderAxiom", "transitivity"),
            ],
        },
        "ttl": f"""\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dpv:     <https://w3id.org/dpv#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .

drk:offer-311 a odrl:Offer ;
    dcterms:title "Offer: any declared purpose"@en ;
    odrl:assigner drk:library ;
    odrl:permission kgc:KGC311-offer-r1 .

kgc:KGC311-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC311-offer-c1 .

kgc:KGC311-offer-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:isA ;
    odrl:rightOperand dpv:Purpose .

drk:request-311 a odrl:Request ;
    dcterms:title "Request: non-commercial research"@en ;
    odrl:assignee drk:researcher ;
    odrl:permission kgc:KGC311-request-r1 .

kgc:KGC311-request-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
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
            "binding": BINDING,
        "background_theory": EMPTY_BT,
        "unknown_reason": "epistemic",
        "summary": (
    "A library permits use for marketing, while a researcher requests use "
    "for scientific research."
),
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
                       "comment": (
    "DPV does not declare Marketing and ScientificResearch distinct, so "
    "open-world semantics cannot establish either compatibility or conflict."
),
            "premises": [],
        },
        "ttl": f"""\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dpv:     <https://w3id.org/dpv#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .

drk:offer-313 a odrl:Offer ;
    dcterms:title "Offer: marketing"@en ;
    odrl:assigner drk:library ;
    odrl:permission kgc:KGC313-offer-r1 .

kgc:KGC313-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC313-offer-c1 .

kgc:KGC313-offer-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:Marketing .

drk:request-313 a odrl:Request ;
    dcterms:title "Request: scientific research"@en ;
    odrl:assignee drk:researcher ;
    odrl:permission kgc:KGC313-request-r1 .

kgc:KGC313-request-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
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
        "binding": BINDING,
        "includes":          INCLUDES_DECLARED,
        "summary": (
    "The marketing offer and scientific-research request are evaluated with "
    "the two purpose concepts declared distinct."
),
        "description": (
            "The constraints of KGC313, over the same resource, under a "
            "background theory in which the parties declare the two purposes "
            "distinct.  No model then identifies them, the witness fails "
            "everywhere, and the verdict is Incompatible.  DPV publishes no "
            "such distinctness: the verdict rests on the declaration, and "
            "the certificate marks it withdrawable."
        ),

        "fof_decls": _iso((MK, SR))[0],
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
        "smt2_background": _iso((MK, SR))[1],
        "smt2_witness": f"""\
(or (and (= {MK} {MK}) (= {MK} {SR}))
    (and (= {SR} {MK}) (= {SR} {SR})))""",

        "certificate": {
            "kind": "Refutation",
   "comment": (
        "The background theory declares Marketing and ScientificResearch "
        "distinct, so the two constraints cannot be satisfied by the same "
        "purpose. This declaration changes the verdict from Unknown to "
        "Incompatible; withdrawing the declaration would return the verdict "
        "to Unknown."
    ),
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

drk:offer-314 a odrl:Offer ;
    dcterms:title "Offer: marketing"@en ;
    odrl:assigner drk:library ;
    odrl:permission kgc:KGC314-offer-r1 .

kgc:KGC314-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC314-offer-c1 .

kgc:KGC314-offer-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:Marketing .

drk:request-314 a odrl:Request ;
    dcterms:title "Request: scientific research"@en ;
    odrl:assignee drk:researcher ;
    odrl:permission kgc:KGC314-request-r1 .

kgc:KGC314-request-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
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
        "binding": BINDING,  
        "includes":          INCLUDES,
        "summary": (
    "A library permits use for any DPV purpose, and a researcher requests "
    "use for recruitment interview scheduling."
),
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
"comment": (
    "RecruitmentInterviewScheduling lies below Purpose through a six-step "
    "hierarchy: RecruitmentInterviewManagement, RecruitmentManagement, "
    "PersonnelHiring, PersonnelManagement, and HumanResourceManagement. "
    "All six relations are published by DPV."
),
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

drk:offer-315 a odrl:Offer ;
    dcterms:title "Offer: any declared purpose"@en ;
    odrl:assigner drk:library ;
    odrl:permission kgc:KGC315-offer-r1 .

kgc:KGC315-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC315-offer-c1 .

kgc:KGC315-offer-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:isA ;
    odrl:rightOperand dpv:Purpose .

drk:request-315 a odrl:Request ;
    dcterms:title "Request: recruitment interview scheduling"@en ;
    odrl:assignee drk:researcher ;
    odrl:permission kgc:KGC315-request-r1 .

kgc:KGC315-request-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
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
                "unknown_reason": "epistemic",
        "includes":          INCLUDES,
        "binding": BINDING,
        "summary": (
    "A library permits use for recruitment interview scheduling, while a "
    "researcher requests use for the general Purpose concept."
),
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
"comment": (
    "DPV places RecruitmentInterviewScheduling below Purpose, but does not "
    "establish the reverse relation or that the two concepts are distinct. "
    "The available knowledge therefore leaves the verdict Unknown."
),
            "premises": [],
        },
        "ttl": f"""\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dpv:     <https://w3id.org/dpv#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .

drk:offer-316 a odrl:Offer ;
    dcterms:title "Offer: recruitment interview scheduling"@en ;
    odrl:assigner drk:library ;
    odrl:permission kgc:KGC316-offer-r1 .

kgc:KGC316-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC316-offer-c1 .

kgc:KGC316-offer-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:isA ;
    odrl:rightOperand dpv:RecruitmentInterviewScheduling .

drk:request-316 a odrl:Request ;
    dcterms:title "Request: any declared purpose"@en ;
    odrl:assignee drk:researcher ;
    odrl:permission kgc:KGC316-request-r1 .

kgc:KGC316-request-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
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
        "binding": BINDING,
        "includes":          INCLUDES,
        "summary": (
    "A library excludes marketing, while a researcher requests use for "
    "marketing."
),
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
"comment": (
    "The offer excludes exactly the purpose required by the request, so the "
    "constraints are Incompatible without any resource or background "
    "declaration."
),
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

drk:offer-317 a odrl:Offer ;
    dcterms:title "Offer: any purpose other than marketing"@en ;
    odrl:assigner drk:library ;
    odrl:permission kgc:KGC317-offer-r1 .

kgc:KGC317-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC317-offer-c1 .

kgc:KGC317-offer-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:isNoneOf ;
    odrl:rightOperand dpv:Marketing .

drk:request-317 a odrl:Request ;
    dcterms:title "Request: marketing"@en ;
    odrl:assignee drk:researcher ;
    odrl:permission kgc:KGC317-request-r1 .

kgc:KGC317-request-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC317-request-c1 .

kgc:KGC317-request-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:Marketing .""",
    },
   # -----------------------------------------------------------------
    # KGC393 / 394 / 395  One intent, three drafts: isAnyOf is identity.
    # -----------------------------------------------------------------
    {
        "id": "KGC393", "subdir": "verdict",
        "name": "purpose, isAnyOf {RnD, Marketing} against eq ScientificResearch",
        "left_operand": "purpose", "sort": "tax",
        "resource": RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING, "includes": INCLUDES,
        "tree": [C("isAnyOf", RND, MK), C("eq", SR, side="request")],
        "expected_verdict": "Unknown", "unknown_reason": "epistemic",
        "expected_q1": "Satisfiable", "expected_q2": "Satisfiable",
        "summary": (
            "A provider permits use for research and development or "
            "marketing; a consumer commits to scientific research."),
        "description": (
            "The drafter expects the taxonomy to carry this: scientific "
            "research lies below research and development. isAnyOf does not "
            "read the order; it asks whether the use's purpose is one of the "
            "two named concepts. As published nothing separates scientific "
            "research from either, so a structure may identify them and "
            "the verdict is Unknown. KGC395 is the draft the drafter meant."),
        "certificate": {"kind": "Models",
            "comment": "One structure identifies scientific research with "
                       "research and development and admits the use; one keeps "
                       "them apart and does not. The published order is not "
                       "consulted by isAnyOf.",
            "premises": []},
        "provenance": "Purpose limitation lists in data licences.",
        "ttl": _ttl("KGC393", PURPOSE,
                    "use for research and development or marketing",
                    [("isAnyOf", ["ResearchAndDevelopment", "Marketing"])],
                    "scientific research", [("eq", ["ScientificResearch"])]),
    },
    {
        "id": "KGC394", "subdir": "verdict",
        "name": "purpose, isAnyOf {RnD, Marketing} against eq ScientificResearch, "
                "declared distinct",
        "left_operand": "purpose", "sort": "tax",
        "resource": RESOURCE, "background_theory": DECLARED_BT,
        "binding": BINDING, "includes": INCLUDES_DECLARED,
        "tree": [C("isAnyOf", RND, MK), C("eq", SR, side="request")],
        "fof_decls": _D394[0], "smt2_background": _D394[1],
        "expected_verdict": "Incompatible",
        "expected_q1": "Unsatisfiable", "expected_q2": "Satisfiable",
        "summary": (
            "As KGC393, with scientific research declared distinct from both "
            "named purposes."),
        "description": (
            "Scientific research is then neither of the two concepts, the "
            "witness fails everywhere, and the verdict is Incompatible. The "
            "distinctness is true, one concept lying below another does not "
            "make them one, and it refutes exactly the compatibility the "
            "drafter intended. The operator, not the taxonomy, decided."),
        "certificate": {"kind": "Refutation",
            "comment": "Scientific research is declared distinct from research "
                       "and development and from marketing, so it is neither "
                       "of the offer's values.",
            "premises": [("fromBackgroundTheory", "SR distinct from RnD"),
                         ("fromBackgroundTheory", "SR distinct from Marketing")]},
        "provenance": "As KGC393; warrant DPV's definitions of distinct purposes.",
        "ttl": _ttl("KGC394", PURPOSE,
                    "use for research and development or marketing",
                    [("isAnyOf", ["ResearchAndDevelopment", "Marketing"])],
                    "scientific research", [("eq", ["ScientificResearch"])]),
    },
    {
        "id": "KGC395", "subdir": "verdict",
        "name": "purpose, or(isA RnD, isA Marketing) against eq ScientificResearch",
        "left_operand": "purpose", "sort": "tax",
        "resource": RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING, "includes": INCLUDES,
        "tree": [Or((C("isA", RND), C("isA", MK))), C("eq", SR, side="request")],
        "expected_verdict": "Compatible",
        "expected_q1": "Satisfiable", "expected_q2": "Unsatisfiable",
        "summary": (
            "A provider permits use for any purpose under research and "
            "development or under marketing; a consumer commits to "
            "scientific research."),
        "description": (
            "The taxonomic draft of KGC393's intent. The first disjunct reads "
            "the order, DPV places scientific research below research and "
            "development, and the verdict is Compatible on one published "
            "assertion. Same intent as KGC393, opposite behaviour: this draft "
            "defers to the authority and covers purposes DPV adds below the "
            "branch; KGC393's is fixed to two names."),
        "certificate": {"kind": "Refutation",
            "comment": "DPV places scientific research below research and "
                       "development; the first disjunct settles it.",
            "premises": [("fromResource", "SR below RnD")]},
        "provenance": "As KGC393.",
        "ttl": _ttl("KGC395", PURPOSE,
                    "use for research and development or marketing purposes",
                    [("isA", ["ResearchAndDevelopment"]), ("isA", ["Marketing"])],
                    "scientific research", [("eq", ["ScientificResearch"])],
                    connective="or"),
    },
    # -----------------------------------------------------------------
    # KGC396  "Only these purposes" is inexpressible for a multi-valued use.
    # -----------------------------------------------------------------
    {
        "id": "KGC396", "subdir": "verdict",
        "name": "purpose, isAnyOf {RnD, Marketing} against isAllOf {RnD, "
                "ServiceProvision}",
        "left_operand": "purpose", "sort": "tax",
        "resource": RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING, "includes": INCLUDES,
        "tree": [C("isAnyOf", RND, MK), C("isAllOf", RND, SVC, side="request")],
        "expected_verdict": "Compatible",
        "expected_q1": "Satisfiable", "expected_q2": "Unsatisfiable",
        "summary": (
            "A provider permits use for research and development or "
            "marketing; a consumer commits to research and development and "
            "to service provision, both."),
        "description": (
            "The use carries two purposes. isAnyOf asks only that one of them "
            "is among the offer's values, and research and development is, so "
            "the verdict is Compatible on the constraints alone; service "
            "provision rides along. The offer meant 'only these purposes', "
            "and no ODRL operator says that of a multi-valued use: isAnyOf is "
            "existential, isAllOf a superset, or(eq, eq) fails on two values. "
            "Declaring the operand functional is the remedy; this request is "
            "then ill-sorted at drafting, and isAnyOf means 'the one purpose "
            "is among these'."),
        "certificate": {"kind": "Refutation",
            "comment": "Research and development is among the offer's values, "
                       "and nothing in the offer limits the use's other "
                       "purposes.",
            "premises": []},
        "provenance": "Purpose limitation (GDPR Art. 5(1)(b)) against a "
                      "consumer declaring several purposes.",
        "ttl": _ttl("KGC396", PURPOSE,
                    "use for research and development or marketing",
                    [("isAnyOf", ["ResearchAndDevelopment", "Marketing"])],
                    "research and development and service provision",
                    [("isAllOf", ["ResearchAndDevelopment", "ServiceProvision"])]),
    },
    # -----------------------------------------------------------------
    # KGC397  Negation does not inherit the order: the purpose twin of KGC392.
    # -----------------------------------------------------------------
    {
        "id": "KGC397", "subdir": "verdict",
        "name": "purpose, isNoneOf {Marketing} against eq Advertising, declared "
                "distinct",
        "left_operand": "purpose", "sort": "tax",
        "resource": RESOURCE, "background_theory": DECLARED_BT,
        "binding": BINDING, "includes": INCLUDES_DECLARED,
        "tree": [C("isNoneOf", MK), C("eq", ADV, side="request")],
        "fof_decls": _D397[0], "smt2_background": _D397[1],
        "expected_verdict": "Compatible",
        "expected_q1": "Satisfiable", "expected_q2": "Unsatisfiable",
        "summary": (
            "A provider permits use for any purpose except marketing; a "
            "consumer commits to advertising."),
        "description": (
            "DPV places advertising below marketing. isNoneOf excludes the "
            "named concept by identity, advertising is declared a different "
            "concept, and the verdict is Compatible: faithful to ODRL's "
            "operator and contrary to what the drafter meant, which was the "
            "complement of a down-set. No ODRL operator tests that; the "
            "community's isNotA would. The purpose twin of the spatial case "
            "KGC392."),
        "certificate": {"kind": "Refutation",
            "comment": "Advertising is declared distinct from marketing, so it "
                       "lies in the complement; that it lies below marketing "
                       "is not consulted.",
            "premises": [("fromBackgroundTheory",
                          "Advertising distinct from Marketing")]},
        "provenance": "Marketing exclusions in research-data licences; the "
                      "drafting error they invite.",
        "ttl": _ttl("KGC397", PURPOSE, "use for any purpose except marketing",
                    [("isNoneOf", ["Marketing"])], "advertising",
                    [("eq", ["Advertising"])]),
    },
]