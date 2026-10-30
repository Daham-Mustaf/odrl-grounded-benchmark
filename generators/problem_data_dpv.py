# =====================================================================
# problem_data_dpv.py: three blocks to replace
# Seventeen problems over the DPV purposes slice.
# Nothing else in the file changes. The duplicates were being
# overwritten by Python, so the verdicts do not move; what changes is
# that the file stops carrying another resource's constants.
# =====================================================================


from compile import right_operand as _ro, Constraint, Or, Xone


SR   = "dpv_scientific_research"
RND  = "dpv_research_and_development"
MK   = "dpv_marketing"
ADV  = "dpv_advertising"
SVC  = "dpv_service_provision"
NCP  = "dpv_non_commercial_purpose"
NCR  = "dpv_non_commercial_research"
PB   = "dpv_public_benefit"
ITM  = "dpv_improve_transport_mobility"
DA   = "dpv_data_altruism"
CP   = "dpv_commercial_purpose"
CR   = "dpv_commercial_research"
PUR  = "dpv_purpose"

# A deep purpose that fits traffic data: four edges, one parent at each
# step (RequestedServiceProvision, ServiceProvision, ServiceManagement,
# Purpose), so the route from bottom to top is unique.
DOG  = "dpv_delivery_of_goods"

RESOURCE          = "https://w3id.org/odrl-kb/dpv-purposes"
EMPTY_BT          = "https://w3id.org/odrl-kb/dpv-purposes/empty"
DECLARED_BT       = "https://w3id.org/odrl-kb/dpv-purposes/declared"
BINDING           = "https://w3id.org/odrl-kb/profile/b-purpose"
INCLUDES          = ["KGE000-0.ax", "DPV-dpv-purposes.ax"]
INCLUDES_DECLARED = INCLUDES + ["DPV-dpv-purposes-declared.ax"]


def C(op, *vals, side="offer"):
    return Constraint(op, tuple(vals), side)


_HEAD = """\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dpv:     <https://w3id.org/dpv#> .
@prefix dpv-odrl: <https://w3id.org/dpv/mappings/odrl#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .
"""


def _cnode(cid, lo, op, vals):
    """One odrl:Constraint node.  A set operator's values are written as
    an RDF collection, one-element lists included."""
    ro = _ro(op, [f"dpv:{v}" for v in vals])
    return f"""kgc:{cid} a odrl:Constraint ;
    odrl:leftOperand {lo} ;
    odrl:operator odrl:{op} ;
    odrl:rightOperand {ro} .
"""

def _side(pid, k, title, party, lo, constraints, connective=None):
    """Policy k (1 or 2) of the pair."""
    n, role = pid[3:], f"p{k}"
    cids = [f"{pid}-{role}-c{i+1}" for i in range(len(constraints))]
    if len(cids) == 1:
        cref, lc = f"kgc:{cids[0]}", ""
    else:
        cref = f"kgc:{pid}-{role}-lc"
        lc = (f"kgc:{pid}-{role}-lc a odrl:LogicalConstraint ;\n"
              f"    odrl:{connective} ( "
              + " ".join(f"kgc:{c}" for c in cids) + " ) .\n")
    body = (f"drk:policy-{n}-{k} a odrl:Set ;\n"
            f"    odrl:uid drk:policy-{n}-{k} ;\n"
            f"    odrl:profile dpv-odrl: ;\n"
            f'    dcterms:title "{title[:1].upper() + title[1:]}"@en ;\n'
            f"    {party}\n"
            f"    odrl:permission kgc:{pid}-{role}-r1 .\n"
            f"kgc:{pid}-{role}-r1 a odrl:Permission ;\n"
            f"    odrl:action odrl:use ;\n"
            f"    odrl:target drk:traffic-data ;\n"
            f"    odrl:constraint {cref} .\n" + lc)
    for cid, (op, vals) in zip(cids, constraints):
        body += _cnode(cid, lo, op, vals)
    return body


def _ttl(pid, lo, offer_title, offer_cs, req_title, req_cs, connective=None):
    return (_HEAD
            + _side(pid, 1, offer_title,
                    "odrl:assigner drk:data-platform ;", lo, offer_cs, connective)
            + _side(pid, 2, req_title,
                    "odrl:assignee drk:data-user ;", lo, req_cs))


PURPOSE = "dpv-odrl:Purpose"


"""
Seventeen problems over the DPV purposes slice, in a mobility data space: a
city's traffic data platform (drk:data-platform) shares its traffic sensor
data (drk:traffic-data) with a data user (drk:data-user), who may be a city
transport authority, a company or a university research group.

The order-based eleven, one per thing that can go wrong:

    KGC310  isA R&D      x eq SR    -> Compatible    one resource premise
    KGC313  eq Marketing x eq SR    -> Unknown       nothing declares them apart
    KGC314  the same pair under declarations that do -> Incompatible
    KGC315  isA Purpose  x eq RIS   -> Compatible    six premises + transitivity
    KGC316  isA SR       x eq R&D   -> Unknown       the order runs one way,
                                                     twin of KGC310 and KGC403
    KGC317  isNoneOf {Mk} x eq Mk   -> Incompatible  from the constraints alone
    KGC318  neq Mk       x eq SR    -> Compatible    under declared distinctness
    KGC319  xone(isA CP, isA NCP) x eq NCR -> Unknown the branches are not
                                                     disjoint
    KGC403  isA SR       x eq R&D, declared distinct -> Incompatible
    KGC404  isA R&D      x isA NCP  -> Compatible    two categories, neither
                                                     inside the other

And six on the set operators and the connectives, which read identity and
not the order unless a branch names a category:

    KGC393  isAnyOf {PB, NCR} x eq ITM        -> Unknown
    KGC394  the same under declared distinctness -> Incompatible
    KGC395  or(isA PB, isA NCR) x eq ITM      -> Compatible
    KGC396  isA PB x isAllOf {DataAltruism, ITM} -> Compatible
    KGC397  isNoneOf {Mk} x eq Advertising    -> Compatible
    KGC399  or(isA PB, isA NCR) x eq CommercialResearch -> Unknown

KGC393 and KGC395 are one intention drafted two ways: enumerating the
values, and naming the branches that hold them. Both are legitimate and
they behave differently as the vocabulary grows. KGC399 puts the second
draft against a purpose that lies under neither branch. KGC396 combines
two purposes with isAllOf, which the DPV-ODRL usage note for Purpose does
not list, and KGC397 is the purpose twin of the spatial case KGC392.

Declarations over this resource
-------------------------------
The module publishes concepts below two parents: NonCommercialResearch
lies below both NonCommercialPurpose and ResearchAndDevelopment, and ten
other concepts have two parents. Those pairs may be declared distinct,
which is what the declarations state, and may not be declared
disjoint: the resource publishes a concept below both, so the declarations
and the resource would share no model.  The declarations list every
purpose of the slice, so any pair a problem names is one they declare.
"""
PROBLEMS = [

    {
        "id":                "KGC310",
        "twin":              "KGC316",
        "subdir":            "verdict",
        "name":              "purpose, isA dpv:R&D against eq dpv:SR",
        "left_operand":      "purpose",
        "sort":              "tax",
        "resource":          RESOURCE,
        "background_theory": EMPTY_BT,
        "binding": BINDING,
        "includes":          INCLUDES,
        "tree": [C("isA", RND), C("eq", SR, side="request")],
        "summary": (
            "A city's traffic data platform permits use for research and "
            "development or any narrower purpose. A university commits to "
            "use for scientific research."),
        "description": (
            "A policy for research and development and everything below it, "
            "against a commitment to scientific research. DPV places "
            "scientific research directly below research and development, "
            "so a use for scientific research meets both policies, whatever "
            "else DPV leaves open. The verdict is Compatible on one "
            "published statement."),
        "maintainer_note": "The refutation should cite one resource premise.",

        "fof_decls": """\
% Declarations: empty.  The purposes module publishes no disjointness
% and no distinctness, and the parties declare none.
""",

        "expected_q1": "Satisfiable",
        "expected_q2": "Unsatisfiable",

        "smt2_logic": "UF",

        "certificate": {
            "kind": "Refutation",
"comment": (
    "DPV places scientific research directly below research and development, "
    "so a use for scientific research satisfies both policies."),
            "premises": [
                ("fromResource",
                 "dpv:ScientificResearch is below dpv:ResearchAndDevelopment"),
            ],
        },
        "ttl": f"""\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dpv:     <https://w3id.org/dpv#> .
@prefix dpv-odrl: <https://w3id.org/dpv/mappings/odrl#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .

drk:policy-310-1 a odrl:Set ;
    odrl:uid drk:policy-310-1 ;
    odrl:profile dpv-odrl: ;
    dcterms:title "Use for research and development or any narrower purpose"@en ;
    odrl:assigner drk:data-platform ;
    odrl:permission kgc:KGC310-p1-r1 .

kgc:KGC310-p1-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:traffic-data ;
    odrl:constraint kgc:KGC310-p1-c1 .

kgc:KGC310-p1-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:Purpose ;
    odrl:operator odrl:isA ;
    odrl:rightOperand dpv:ResearchAndDevelopment .

drk:policy-310-2 a odrl:Set ;
    odrl:uid drk:policy-310-2 ;
    odrl:profile dpv-odrl: ;
    dcterms:title "Use for scientific research only"@en ;
    odrl:assignee drk:data-user ;
    odrl:permission kgc:KGC310-p2-r1 .

kgc:KGC310-p2-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:traffic-data ;
    odrl:constraint kgc:KGC310-p2-c1 .

kgc:KGC310-p2-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:Purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:ScientificResearch .""",
    },

    # -----------------------------------------------------------------
    # KGC313  Unknown for the other reason: two names the resource never
    # relates and the declarations never separate.  Pair this with
    # a set of declarations declaring them distinct and the verdict moves
    # to Incompatible; that is the stability demonstration.
    # -----------------------------------------------------------------
    {
        "id":                "KGC313",
        "twin":              "KGC314",
        "subdir":            "verdict",
        "name":              (
            "purpose, eq dpv:ScientificResearch against eq dpv:Marketing"),
        "left_operand":      "purpose",
        "sort":              "tax",
        "resource":          RESOURCE,
            "binding": BINDING,
        "background_theory": EMPTY_BT,
        "summary": (
            "A city's traffic data platform permits use for scientific "
            "research only. A company commits to use for marketing."),
        "includes":          INCLUDES,
        "tree": [C("eq", SR), C("eq", MK, side="request")],
        "description": (
            "A platform that allows scientific research only, and a data "
            "user that commits to marketing. Each policy names exactly one "
            "purpose, so both can be met only if the two purposes are one. "
            "DPV publishes no distinctness, so they may be one. The verdict "
            "is Unknown. The same pair with the purposes declared distinct "
            "is Incompatible (KGC314), which is what makes the declaration "
            "visible in the verdict."),
        "maintainer_note": "Both constraints denote singletons.",

        "fof_decls": """\
% Declarations: empty.  Two names are not two concepts until something
% says so, and the purposes module says nothing.
""",

        "expected_q1": "Satisfiable",
        "expected_q2": "Satisfiable",

        "smt2_logic": "UF",

        "certificate": {
            "kind": "Models",                   
                       "comment": (
                           "DPV does not state that marketing and "
                           "scientific research are different purposes. If "
                           "they are the same purpose, a use for marketing "
                           "meets both policies; if they are different, no "
                           "use does. So the verdict is Unknown."),
            "premises": [],
        },
        "ttl": f"""\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dpv:     <https://w3id.org/dpv#> .
@prefix dpv-odrl: <https://w3id.org/dpv/mappings/odrl#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .

drk:policy-313-1 a odrl:Set ;
    odrl:uid drk:policy-313-1 ;
    odrl:profile dpv-odrl: ;
    dcterms:title "Use for scientific research only"@en ;
    odrl:assigner drk:data-platform ;
    odrl:permission kgc:KGC313-p1-r1 .

kgc:KGC313-p1-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:traffic-data ;
    odrl:constraint kgc:KGC313-p1-c1 .

kgc:KGC313-p1-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:Purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:ScientificResearch .

drk:policy-313-2 a odrl:Set ;
    odrl:uid drk:policy-313-2 ;
    odrl:profile dpv-odrl: ;
    dcterms:title "Use for marketing only"@en ;
    odrl:assignee drk:data-user ;
    odrl:permission kgc:KGC313-p2-r1 .

kgc:KGC313-p2-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:traffic-data ;
    odrl:constraint kgc:KGC313-p2-c1 .

kgc:KGC313-p2-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:Purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:Marketing .""",
    },

    # -----------------------------------------------------------------
    # KGC314  KGC313 again, under a set of declarations that separates the
    # two purposes.  Same resource, same constraints, same witness: only
    # the declaration differs, and the verdict moves.  The refutation is
    # attributable to a statement a party can withdraw.
    # -----------------------------------------------------------------
    {
        "id":                "KGC314",
        "twin":              "KGC313",
        "subdir":            "verdict",
        "name":              (
            "purpose, eq dpv:ScientificResearch against eq dpv:Marketing, "
            "under a declared distinctness"),
        "left_operand":      "purpose",
        "sort":              "tax",
        "resource":          RESOURCE,
        "background_theory": DECLARED_BT,
        "binding": BINDING,
        "includes":          INCLUDES_DECLARED,
        "tree": [C("eq", SR), C("eq", MK, side="request")],
        "summary": (
            "As KGC313, with scientific research and marketing declared "
            "distinct."),
        "description": (
            "KGC313 with every pair of purposes declared distinct. "
            "Scientific research and marketing are then two purposes, so no "
            "use satisfies both policies and the verdict is Incompatible. "
            "DPV publishes no such distinctness: the verdict rests on the "
            "declaration, and withdrawing it returns the verdict to "
            "Unknown."),
        "maintainer_note": "The certificate marks the declaration as withdrawable.",


        "expected_q1": "Unsatisfiable",
        "expected_q2": "Satisfiable",

        "smt2_logic": "UF",

        "certificate": {
            "kind": "Refutation",
   "comment": (
       "The declarations state that scientific research and marketing are "
       "different purposes, because DPV defines each as a purpose of its "
       "own. No use is both, so no use meets both policies. Without the "
       "declaration the verdict is Unknown, as in KGC313."),
            "premises": [
                ("fromDeclarations",
                 "dpv:Marketing and dpv:ScientificResearch are declared "
                 "distinct"),
            ],
        },
        "ttl": f"""\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dpv:     <https://w3id.org/dpv#> .
@prefix dpv-odrl: <https://w3id.org/dpv/mappings/odrl#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .

drk:policy-314-1 a odrl:Set ;
    odrl:uid drk:policy-314-1 ;
    odrl:profile dpv-odrl: ;
    dcterms:title "Use for scientific research only"@en ;
    odrl:assigner drk:data-platform ;
    odrl:permission kgc:KGC314-p1-r1 .

kgc:KGC314-p1-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:traffic-data ;
    odrl:constraint kgc:KGC314-p1-c1 .

kgc:KGC314-p1-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:Purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:ScientificResearch .

drk:policy-314-2 a odrl:Set ;
    odrl:uid drk:policy-314-2 ;
    odrl:profile dpv-odrl: ;
    dcterms:title "Use for marketing only"@en ;
    odrl:assignee drk:data-user ;
    odrl:permission kgc:KGC314-p2-r1 .

kgc:KGC314-p2-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:traffic-data ;
    odrl:constraint kgc:KGC314-p2-c1 .

kgc:KGC314-p2-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:Purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:Marketing .""",
    },

    # -----------------------------------------------------------------
    # KGC315  The longest chain in the module, taken in the direction the
    # order runs.  Six resource statements and transitivity.
    # -----------------------------------------------------------------
    {
        "id":                "KGC315",
        "subdir":            "verdict",
        "name":              (
            "purpose, isA dpv:Purpose against eq dpv:DeliveryOfGoods"),
        "left_operand":      "purpose",
        "sort":              "tax",
        "resource":          RESOURCE,
        "background_theory": EMPTY_BT,
        "binding": BINDING,  
        "includes":          INCLUDES,
        "tree": [C("isA", PUR), C("eq", DOG, side="request")],
        "summary": (
            "A city's traffic data platform permits use for any DPV "
            "purpose. A logistics company commits to use for delivery of "
            "goods."),
        "description": (
            "DPV places delivery of goods four steps below Purpose, through "
            "RequestedServiceProvision, ServiceProvision and "
            "ServiceManagement. All four statements are published, so a use "
            "for delivery of goods is a use for a DPV purpose. An open-data "
            "platform states, as open licences do, that the data may be "
            "used for any purpose. The case shows that the answer does not "
            "change with depth."),
        "maintainer_note": (
            "Four steps, so the refutation chains four statements and "
            "transitivity; what grows with depth is the proof, not the "
            "answer. Until tag pre-review this case used "
            "RecruitmentInterviewScheduling at six steps, one of five "
            "purposes at that depth, and the baseline/solidlab D6 row was "
            "recorded against that."),

        "fof_decls": """\
% Declarations: empty.
""",

        "expected_q1": "Satisfiable",
        "expected_q2": "Unsatisfiable",

        "smt2_logic": "UF",
        "smt2_background": "",

        "certificate": {
            "kind": "Refutation",
"comment": (
    "DPV places delivery of goods below Purpose in four steps, so a use for "
    "delivery of goods is a use for a DPV purpose."),
            "premises": [
                ("fromResource", "the four order statements of the chain"),
                ("fromOrderAxiom", "transitivity"),
            ],
        },
        "ttl": f"""\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dpv:     <https://w3id.org/dpv#> .
@prefix dpv-odrl: <https://w3id.org/dpv/mappings/odrl#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .

drk:policy-315-1 a odrl:Set ;
    odrl:uid drk:policy-315-1 ;
    odrl:profile dpv-odrl: ;
    dcterms:title "Use for any DPV purpose"@en ;
    odrl:assigner drk:data-platform ;
    odrl:permission kgc:KGC315-p1-r1 .

kgc:KGC315-p1-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:traffic-data ;
    odrl:constraint kgc:KGC315-p1-c1 .

kgc:KGC315-p1-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:Purpose ;
    odrl:operator odrl:isA ;
    odrl:rightOperand dpv:Purpose .

drk:policy-315-2 a odrl:Set ;
    odrl:uid drk:policy-315-2 ;
    odrl:profile dpv-odrl: ;
    dcterms:title "Use for delivery of goods only"@en ;
    odrl:assignee drk:data-user ;
    odrl:permission kgc:KGC315-p2-r1 .

kgc:KGC315-p2-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:traffic-data ;
    odrl:constraint kgc:KGC315-p2-c1 .

kgc:KGC315-p2-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:Purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:DeliveryOfGoods .""",
    },

    # -----------------------------------------------------------------
    # KGC316  KGC310 read the other way.  The published edge runs from
    # scientific research up to research and development.  The converse
    # edge would make antisymmetry identify the two, so the verdict is
    # open where KGC310's is closed.
    # -----------------------------------------------------------------
    {
        "id":                "KGC316",
        "twin":              ["KGC310", "KGC403"],
        "subdir":            "verdict",
        "name":              "purpose, isA dpv:SR against eq dpv:R&D",
        "left_operand":      "purpose",
        "sort":              "tax",
        "resource":          RESOURCE,
        "background_theory": EMPTY_BT,
        "binding": BINDING,
        "includes":          INCLUDES,
        "tree": [C("isA", SR), C("eq", RND, side="request")],
        "expected_verdict":  "Unknown",
        "summary": (
            "A city's traffic data platform permits use for scientific "
            "research or any narrower purpose. A company commits to use for "
            "research and development."),
        "description": (
            "KGC310 the other way round. The first policy covers scientific "
            "research and everything below it; the second names research "
            "and development. DPV places scientific research below research "
            "and development and publishes no edge back, so a use for "
            "research and development meets the first policy only if the "
            "two purposes are one. If they are the same purpose, the use "
            "meets both policies; if they are different, none does. The "
            "verdict is Unknown where KGC310 is Compatible. The pair shows "
            "that isA reads the order in one direction: swapping the two "
            "policies can change the verdict."),

        "fof_decls": """\
% Declarations: empty.  The purposes module publishes no disjointness
% and no distinctness, and the parties declare none.
""",

        "expected_q1": "Satisfiable",
        "expected_q2": "Satisfiable",

        "smt2_logic": "UF",

        "certificate": {
            "kind": "Models",
            "comment": (
                "DPV places scientific research below research and "
                "development and publishes no edge back. A use for research "
                "and development meets the first policy only if research "
                "and development also lies below scientific research, and "
                "then the two are one purpose. If they are the same "
                "purpose, the use meets both policies; if they are "
                "different, no use does. So the verdict is Unknown."),
            "premises": [],
        },
        "ttl": _ttl("KGC316", PURPOSE,
                    "use for scientific research or any narrower purpose",
                    [("isA", ["ScientificResearch"])],
                    "use for research and development only",
                    [("eq", ["ResearchAndDevelopment"])]),
    },

    # -----------------------------------------------------------------
    # KGC403  KGC316 under declarations that keep the two purposes apart.
    # The published edge runs one way, antisymmetry would turn the other
    # way into identity, and identity is now declared away.
    # -----------------------------------------------------------------
    {
        "id": "KGC403", "subdir": "verdict",
        "twin": "KGC316",
        "name": "purpose, isA dpv:SR against eq dpv:R&D, declared distinct",
        "left_operand": "purpose", "sort": "tax",
        "resource": RESOURCE, "background_theory": DECLARED_BT,
        "binding": BINDING, "includes": INCLUDES_DECLARED,
        "tree": [C("isA", SR), C("eq", RND, side="request")],
        "expected_verdict": "Incompatible",
        "expected_q1": "Unsatisfiable", "expected_q2": "Satisfiable",
        "summary": (
            "As KGC316, with scientific research and research and "
            "development declared distinct."),
        "description": (
            "KGC316 with every pair of purposes declared distinct. DPV "
            "places scientific research below research and development, so "
            "a use for research and development meets the first policy only "
            "if the two purposes are one. They are declared distinct, so no "
            "use meets both policies and the verdict is Incompatible. "
            "KGC316 leaves the question open and is Unknown."),
        "certificate": {"kind": "Refutation",
            "comment": (
                "DPV places scientific research below research and "
                "development. A use for research and development meets the "
                "first policy only if research and development also lies "
                "below scientific research, and then the two are one "
                "purpose. They are declared distinct, because DPV defines "
                "each as a purpose of its own, so no use meets both "
                "policies."),
            "premises": [("fromResource", "SR below RnD"),
                         ("fromOrderAxiom", "antisymmetry"),
                         ("fromDeclarations", "SR distinct from RnD")]},
        "provenance": "As KGC316.",
        "ttl": _ttl("KGC403", PURPOSE,
                    "use for scientific research or any narrower purpose",
                    [("isA", ["ScientificResearch"])],
                    "use for research and development only",
                    [("eq", ["ResearchAndDevelopment"])]),
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
        "tree": [C("isNoneOf", MK), C("eq", MK, side="request")],
        "summary": (
            "A city's traffic data platform permits use for any purpose "
            "other than marketing. A company commits to use for marketing."),
        "description": (
            "A policy for any purpose except marketing, against a "
            "commitment to marketing. The first policy excludes exactly the "
            "purpose the second requires, so no use can meet both, and the "
            "verdict is Incompatible. No order statement and no declaration "
            "takes part, so nobody can reopen the verdict by withdrawing a "
            "statement, unlike KGC300 and KGC314."),
        "maintainer_note": (
            "The witness asks for a concept both distinct from and "
            "identical to marketing, which no structure provides. The "
            "certificate has nothing withdrawable in it."),

        "fof_decls": """\
% Declarations: empty, and it stays empty.  The incompatibility here
% is between the two constraints, not between a constraint and something a
% party declared.
""",

        "expected_q1": "Unsatisfiable",
        "expected_q2": "Satisfiable",

        "smt2_logic": "UF",
        "smt2_background": "",

        "certificate": {
            "kind": "Refutation",
"comment": (
    "The first policy excludes exactly the purpose the second requires, so "
    "the verdict is Incompatible without any DPV statement or declaration."),
            "premises": [
                ("fromConstraints", "the witness condition"),
            ],
        },
        "ttl": f"""\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dpv:     <https://w3id.org/dpv#> .
@prefix dpv-odrl: <https://w3id.org/dpv/mappings/odrl#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .

drk:policy-317-1 a odrl:Set ;
    odrl:uid drk:policy-317-1 ;
    odrl:profile dpv-odrl: ;
    dcterms:title "Use for any purpose except marketing"@en ;
    odrl:assigner drk:data-platform ;
    odrl:permission kgc:KGC317-p1-r1 .

kgc:KGC317-p1-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:traffic-data ;
    odrl:constraint kgc:KGC317-p1-c1 .

kgc:KGC317-p1-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:Purpose ;
    odrl:operator odrl:isNoneOf ;
    odrl:rightOperand ( dpv:Marketing ) .

drk:policy-317-2 a odrl:Set ;
    odrl:uid drk:policy-317-2 ;
    odrl:profile dpv-odrl: ;
    dcterms:title "Use for marketing only"@en ;
    odrl:assignee drk:data-user ;
    odrl:permission kgc:KGC317-p2-r1 .

kgc:KGC317-p2-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:traffic-data ;
    odrl:constraint kgc:KGC317-p2-c1 .

kgc:KGC317-p2-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:Purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:Marketing .""",
    },
    # -----------------------------------------------------------------
    # KGC318  neq over the taxonomy: the complement of one concept,
    # against a purpose the parties declare apart from it.
    # -----------------------------------------------------------------
    {
        "id": "KGC318", "subdir": "verdict",
        "name": "purpose, neq dpv:Marketing against eq dpv:ScientificResearch, "
                "declared distinct",
        "left_operand": "purpose", "sort": "tax",
        "resource": RESOURCE, "background_theory": DECLARED_BT,
        "binding": BINDING, "includes": INCLUDES_DECLARED,
        "tree": [C("neq", MK), C("eq", SR, side="request")],
        "expected_verdict": "Compatible",
        "expected_q1": "Satisfiable", "expected_q2": "Unsatisfiable",
        "summary": (
            "A city's traffic data platform permits use for any purpose "
            "other than marketing. A university commits to use for "
            "scientific research. Scientific research is declared distinct "
            "from marketing."),
        "description": (
            "Use for any purpose except marketing, against use for "
            "scientific research. neq excludes marketing by identity. "
            "Scientific research is declared distinct from marketing, so a "
            "use for scientific research meets both policies and the "
            "verdict is Compatible. The same pair without the declaration "
            "would be Unknown, because scientific research might be the "
            "same purpose as marketing. KGC323 and KGC374 show the same "
            "step over file types and languages."),
        "certificate": {"kind": "Refutation",
            "comment": (
                "Scientific research is declared distinct from marketing, "
                "because DPV defines each as a purpose of its own, so a use "
                "for scientific research is a use for a purpose other than "
                "marketing and meets both policies."),
            "premises": [("fromDeclarations",
                          "dpv:ScientificResearch is distinct from "
                          "dpv:Marketing")]},
        "provenance": "Purpose limitation: an exclusion list.",
        "ttl": _ttl("KGC318", PURPOSE,
                    "use for any purpose except marketing",
                    [("neq", ["Marketing"])],
                    "use for scientific research only",
                    [("eq", ["ScientificResearch"])]),
    },
    # -----------------------------------------------------------------
    # KGC319  xone over the taxonomy: the second branch has to fail, and
    # it fails only if the two branches are disjoint.  DPV defines the
    # commercial and the non-commercial purposes by setting or intention,
    # which one purpose can meet both of.
    # -----------------------------------------------------------------
    {
        "id": "KGC319", "subdir": "verdict",
        "name": "purpose, xone(isA CommercialPurpose, isA "
                "NonCommercialPurpose) against eq NonCommercialResearch",
        "left_operand": "purpose", "sort": "tax",
        "resource": RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING, "includes": INCLUDES,
        "tree": [Xone((C("isA", CP), C("isA", NCP))),
                 C("eq", NCR, side="request")],
        "expected_verdict": "Unknown",
        "expected_q1": "Satisfiable", "expected_q2": "Satisfiable",
        "summary": (
            "A city's traffic data platform prices its data in two tiers, "
            "commercial and non-commercial, and each use must fall under "
            "exactly one tier. A university research group commits to use "
            "for non-commercial research."),
        "description": (
            "Each use must fall under exactly one tier, commercial or "
            "non-commercial, and each tier covers the purpose it names and "
            "every narrower one. DPV places non-commercial research below "
            "non-commercial purpose, so the non-commercial tier applies. "
            "Exactly one tier may apply, so non-commercial research must "
            "not also lie below commercial purpose. DPV states no "
            "disjointness between the two, and none is warranted: it "
            "defines a commercial purpose by a commercial setting or an "
            "intention to commercialise, and a non-commercial purpose by a "
            "non-commercial setting or the lack of that intention, and one "
            "purpose can meet both. If non-commercial research is not also "
            "a commercial purpose, the use is admitted. If it is, both "
            "tiers apply and the use is refused. The verdict is Unknown."),
        "certificate": {"kind": "Models",
            "comment": (
                "DPV places non-commercial research below non-commercial "
                "purpose, so the non-commercial tier applies. DPV defines a "
                "commercial purpose as one performed in \"a commercial "
                "setting or with intention to commercialise\" and a "
                "non-commercial purpose as one performed in \"a "
                "non-commercial setting or without intention to "
                "commercialise\". One purpose can meet both, so DPV warrants "
                "no disjointness between the two, and none is declared. If "
                "non-commercial research is not also a commercial purpose, "
                "a use for it meets both policies. If it is, both tiers "
                "apply, 'exactly one' fails, and no use meets both. So the "
                "verdict is Unknown."),
            "premises": []},
        "provenance": "Data-sharing agreements that split commercial from "
                      "non-commercial use.",
        "ttl": _ttl("KGC319", PURPOSE,
                    "use under exactly one of the commercial and non-commercial tiers",
                    [("isA", ["CommercialPurpose"]),
                     ("isA", ["NonCommercialPurpose"])],
                    "use for non-commercial research only",
                    [("eq", ["NonCommercialResearch"])],
                    connective="xone"),
    },
    # -----------------------------------------------------------------
    # KGC393 / 394 / 395 / 399  One intent, three drafts: isAnyOf is
    # identity.  Improving transport mobility lies below public benefit,
    # and only the draft that names the branch reads the order.
    # -----------------------------------------------------------------
    {
        "id": "KGC393", "subdir": "verdict",
        "twin": ["KGC394", "KGC395"],
        "name": "purpose, isAnyOf {PublicBenefit, NonCommercialResearch} "
                "against eq ImproveTransportMobility",
        "left_operand": "purpose", "sort": "tax",
        "resource": RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING, "includes": INCLUDES,
        "tree": [C("isAnyOf", PB, NCR), C("eq", ITM, side="request")],
        "expected_verdict": "Unknown",
        "expected_q1": "Satisfiable", "expected_q2": "Satisfiable",
        "summary": (
            "A city's traffic data platform permits use for at least one "
            "of public benefit and non-commercial research. A city "
            "transport authority commits to improving transport "
            "mobility."),
        "description": (
            "The drafter expects the taxonomy to carry this: improving "
            "transport mobility lies below public benefit. isAnyOf does not "
            "read the order; it asks whether the use's purpose is one of "
            "the two named purposes. As published nothing separates "
            "improving transport mobility from either, so it may be the "
            "same purpose as one of them or a different one, and the "
            "verdict is Unknown. KGC395 is the draft the drafter meant."),
        "certificate": {"kind": "Models",
            "comment": (
                "If improving transport mobility is the same purpose as "
                "public benefit or as non-commercial research, a use for it "
                "meets both policies; if it is a different purpose from "
                "both, no use does. isAnyOf asks only whether the use's "
                "purpose is the same as a listed one and does not look "
                "below the listed purposes, so DPV's statement that "
                "improving transport mobility lies below public benefit "
                "does not help. So the verdict is Unknown."),
            "premises": []},
        "provenance": "Purpose limitation lists in data-sharing "
                      "agreements.",
        "ttl": _ttl("KGC393", PURPOSE,
                    "use for at least one of public benefit and non-commercial research",
                    [("isAnyOf", ["PublicBenefit", "NonCommercialResearch"])],
                    "use for improving transport mobility only",
                    [("eq", ["ImproveTransportMobility"])]),
    },
    {
        "id": "KGC394", "subdir": "verdict",
        "twin":              "KGC393",
        "name": "purpose, isAnyOf {PublicBenefit, NonCommercialResearch} "
                "against eq ImproveTransportMobility, declared distinct",
        "left_operand": "purpose", "sort": "tax",
        "resource": RESOURCE, "background_theory": DECLARED_BT,
        "binding": BINDING, "includes": INCLUDES_DECLARED,
        "tree": [C("isAnyOf", PB, NCR), C("eq", ITM, side="request")],
        "expected_verdict": "Incompatible",
        "expected_q1": "Unsatisfiable", "expected_q2": "Satisfiable",
        "summary": (
            "As KGC393, with improving transport mobility declared "
            "distinct from both purposes the first policy names."),
        "description": (
            "KGC393 with every pair of purposes declared distinct. "
            "Improving transport mobility is then neither public benefit "
            "nor non-commercial research, so no use satisfies both "
            "policies. The declaration is true, yet it defeats the "
            "compatibility the drafter wanted: isAnyOf, not the taxonomy, "
            "decides."),
        "maintainer_note": "The witness fails everywhere.",
        "certificate": {"kind": "Refutation",
            "comment": (
                "Improving transport mobility is declared distinct from "
                "public benefit and from non-commercial research, because "
                "DPV defines each as a purpose of its own, so it is neither "
                "value the first policy lists."),
            "premises": [("fromDeclarations", "ITM distinct from PublicBenefit"),
                         ("fromDeclarations", "ITM distinct from NonCommercialResearch")]},
        "provenance": "As KGC393; warrant DPV's definitions of distinct "
                      "purposes.",
        "ttl": _ttl("KGC394", PURPOSE,
                    "use for at least one of public benefit and non-commercial research",
                    [("isAnyOf", ["PublicBenefit", "NonCommercialResearch"])],
                    "use for improving transport mobility only",
                    [("eq", ["ImproveTransportMobility"])]),
    },
    {
        "id": "KGC395", "subdir": "verdict",
        "twin": ["KGC399", "KGC393"],
        "name": "purpose, or(isA PublicBenefit, isA NonCommercialResearch) "
                "against eq ImproveTransportMobility",
        "left_operand": "purpose", "sort": "tax",
        "resource": RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING, "includes": INCLUDES,
        "tree": [Or((C("isA", PB), C("isA", NCR))),
                 C("eq", ITM, side="request")],
        "expected_verdict": "Compatible",
        "expected_q1": "Satisfiable", "expected_q2": "Unsatisfiable",
        "summary": (
            "A city's traffic data platform permits use for public benefit "
            "or non-commercial research, or any narrower purpose. A city "
            "transport authority commits to improving transport mobility."),
        "description": (
            "The taxonomic draft of KGC393's intent. The first alternative "
            "reads the order: DPV places improving transport mobility below "
            "public benefit, and the verdict is Compatible on one published "
            "statement. Same intent as KGC393, opposite behaviour: this "
            "draft defers to the authority and covers purposes DPV adds "
            "below the branch; KGC393's is fixed to two names. In ODRL, or "
            "does not admit a use that mixes both alternatives."),
        "certificate": {"kind": "Refutation",
            "comment": (
                "DPV places improving transport mobility below public "
                "benefit, so the first alternative holds for a use for "
                "improving transport mobility."),
            "premises": [("fromResource", "ITM below PublicBenefit")]},
        "provenance": "As KGC393.",
        "ttl": _ttl("KGC395", PURPOSE,
                    "use for public benefit or non-commercial research, or any narrower purpose",
                    [("isA", ["PublicBenefit"]),
                     ("isA", ["NonCommercialResearch"])],
                    "use for improving transport mobility only",
                    [("eq", ["ImproveTransportMobility"])],
                    connective="or"),
    },
    # -----------------------------------------------------------------
    # KGC396  A category against a pair of purposes.  DPV says data
    # altruism is meant to be combined with another purpose, and ODRL's
    # isAllOf is the operator that says "both".
    # -----------------------------------------------------------------
    {
        "id": "KGC396", "subdir": "verdict",
        "name": "purpose, isA PublicBenefit against isAllOf "
                "{DataAltruism, ImproveTransportMobility}",
        "left_operand": "purpose", "sort": "tax",
        "resource": RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING, "includes": INCLUDES,
        "tree": [C("isA", PB), C("isAllOf", DA, ITM, side="request")],
        "expected_verdict": "Compatible",
        "expected_q1": "Satisfiable", "expected_q2": "Unsatisfiable",
        "summary": (
            "A city's traffic data platform permits use for public benefit "
            "or any narrower purpose. A city transport authority commits to "
            "data altruism and improving transport mobility together."),
        "description": (
            "The use carries two purposes. DPV places data altruism and "
            "improving transport mobility directly below public benefit, so "
            "each lies under the category the first policy names, and the "
            "verdict is Compatible on two published statements. The second "
            "policy combines the purposes as DPV's scope note for data "
            "altruism asks."),
        "certificate": {"kind": "Refutation",
            "comment": (
                "DPV places data altruism and improving transport mobility "
                "directly below public benefit, so a use for both lies "
                "under the category the first policy names. DPV's scope "
                "note for data altruism asks that it be combined with "
                "other purposes: it \"should be combined with other "
                "purposes to indicate their altruistic interpretation or "
                "application\". The second policy does that."),
            "premises": [("fromResource", "DataAltruism below PublicBenefit"),
                         ("fromResource", "ITM below PublicBenefit")]},
        "provenance": "Altruistic data sharing combined with a concrete "
                      "public purpose.",
        "ttl": _ttl("KGC396", PURPOSE,
                    "use for public benefit or any narrower purpose",
                    [("isA", ["PublicBenefit"])],
                    "use for both data altruism and improving transport mobility",
                    [("isAllOf", ["DataAltruism", "ImproveTransportMobility"])]),
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
        "expected_verdict": "Compatible",
        "expected_q1": "Satisfiable", "expected_q2": "Unsatisfiable",
        "summary": (
            "A city's traffic data platform permits use for any purpose "
            "except marketing. A company commits to advertising."),
        "description": (
            "The drafter meant to exclude marketing and every kind of "
            "marketing. isNoneOf excludes only the named purpose, so "
            "advertising, which DPV places below marketing, passes. No ODRL "
            "2.2 operator in a permission excludes a purpose together with "
            "the purposes below it; a prohibition with isA Marketing does "
            "that. The same pitfall over places is KGC392."),
        "certificate": {"kind": "Refutation",
            "comment": (
                "Advertising is declared distinct from marketing, because "
                "DPV defines each as a purpose of its own, so the exclusion "
                "of marketing does not cover it; that DPV places "
                "advertising below marketing is not consulted."),
            "premises": [("fromDeclarations",
                          "Advertising distinct from Marketing")]},
        "provenance": "Marketing exclusions in research-data licences; the "
                      "drafting error they invite.",
        "ttl": _ttl("KGC397", PURPOSE, "use for any purpose except marketing",
                    [("isNoneOf", ["Marketing"])], "use for advertising only",
                    [("eq", ["Advertising"])]),
    },
    # -----------------------------------------------------------------
    # KGC399  KGC395's policy against a purpose under neither branch.
    # DPV places commercial research below commercial purpose and below
    # research and development, and publishes nothing that keeps it out
    # of public benefit or non-commercial research.
    # -----------------------------------------------------------------
    {
        "id": "KGC399", "subdir": "verdict",
        "twin":              "KGC395",
        "name": "purpose, or(isA PublicBenefit, isA NonCommercialResearch) "
                "against eq CommercialResearch",
        "left_operand": "purpose", "sort": "tax",
        "resource": RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING, "includes": INCLUDES,
        "tree": [Or((C("isA", PB), C("isA", NCR))),
                 C("eq", CR, side="request")],
        "expected_verdict": "Unknown",
        "expected_q1": "Satisfiable", "expected_q2": "Satisfiable",
        "summary": (
            "A city's traffic data platform permits use for public benefit "
            "or non-commercial research, or any narrower purpose. A company "
            "commits to use for commercial research."),
        "description": (
            "Commercial research lies below commercial purpose and below "
            "research and development. DPV does not place it below public "
            "benefit or below non-commercial research, and it publishes "
            "nothing that keeps it out of them. If it lies outside both, no "
            "alternative holds and no use meets both policies. If it also "
            "lies below public benefit or below non-commercial research, "
            "the use is admitted. The verdict is Unknown, where KGC395, "
            "with a second policy under the first alternative, is "
            "Compatible."),
        "certificate": {"kind": "Models",
            "comment": (
                "DPV places commercial research below commercial purpose "
                "and below research and development. It does not place it "
                "below public benefit or below non-commercial research, and "
                "it publishes nothing that keeps it out of them. If "
                "commercial research lies outside both, no alternative "
                "holds and no use meets both policies; if it lies below "
                "public benefit or below non-commercial research, a use for "
                "it meets both. So the verdict is Unknown."),
            "premises": []},
        "provenance": "As KGC393.",
        "ttl": _ttl("KGC399", PURPOSE,
                    "use for public benefit or non-commercial research, or any narrower purpose",
                    [("isA", ["PublicBenefit"]),
                     ("isA", ["NonCommercialResearch"])],
                    "use for commercial research only",
                    [("eq", ["CommercialResearch"])],
                    connective="or"),
    },
    # -----------------------------------------------------------------
    # KGC404  Two categories, neither inside the other.  Both lie above
    # non-commercial research, so a use for it is under both.
    # -----------------------------------------------------------------
    {
        "id": "KGC404", "subdir": "verdict",
        "name": "purpose, isA dpv:R&D against isA dpv:NonCommercialPurpose",
        "left_operand": "purpose", "sort": "tax",
        "resource": RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING, "includes": INCLUDES,
        "tree": [C("isA", RND), C("isA", NCP, side="request")],
        "expected_verdict": "Compatible",
        "expected_q1": "Satisfiable", "expected_q2": "Unsatisfiable",
        "summary": (
            "A city's traffic data platform permits use for research and "
            "development or any narrower purpose. A university commits to "
            "use for non-commercial purposes or any narrower purpose."),
        "description": (
            "Two category policies, neither inside the other. DPV places "
            "non-commercial research below research and development and "
            "below non-commercial purpose, so a use for non-commercial "
            "research lies under both categories, and the verdict is "
            "Compatible on two published statements. Read against KGC310."),
        "certificate": {"kind": "Refutation",
            "comment": (
                "DPV places non-commercial research below research and "
                "development and below non-commercial purpose, so a use for "
                "non-commercial research lies under the category of each "
                "policy."),
            "premises": [("fromResource", "NCR below RnD"),
                         ("fromResource", "NCR below NCP")]},
        "provenance": "Category clauses on both sides of a data-sharing "
                      "agreement.",
        "ttl": _ttl("KGC404", PURPOSE,
                    "use for research and development or any narrower purpose",
                    [("isA", ["ResearchAndDevelopment"])],
                    "use for non-commercial purposes or any narrower purpose",
                    [("isA", ["NonCommercialPurpose"])]),
    },
]