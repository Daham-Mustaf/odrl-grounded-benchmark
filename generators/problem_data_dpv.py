# =====================================================================
# problem_data_dpv.py: three blocks to replace
# Seventeen problems over the DPV purposes slice.
# Nothing else in the file changes. The duplicates were being
# overwritten by Python, so the verdicts do not move; what changes is
# that the file stops carrying another resource's constants.
# =====================================================================


from compile import right_operand as _ro, Constraint, Or, Xone
from pathlib import Path

import declarations

_DECL = declarations.load(
    Path(__file__).resolve().parent.parent / "problems" / "background" / "dpv-purposes-declared.ttl")

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

    The declarations state the rule and list the purposes it ranges
    over; a problem naming two of them carries the inequation between
    them, so a refutation cites the instance it used rather than one
    term standing for all of them. The name must match on both sides:
    an unsat core and a TPTP proof are compared by premise name.  The
    statements come from declarations.py, which refuses a pair the set
    does not state.
    """
    return declarations.instances(
        _DECL, pairs,
        ["% Declarations: declared distinctness instances, stated in",
         "% the declarations file and instantiated here.", ""],
        ["; Declared distinctness this problem adopts, named as the TPTP",
         "; side names it."])


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

_D394 = _iso((ITM, PB), (ITM, NCR))
_D403 = _iso((SR, RND))
_D397 = _iso((ADV, MK))
_D318 = _iso((SR, MK))


"""
Seventeen problems over the DPV purposes slice, in a mobility data space: a
city's traffic data platform (drk:data-platform) shares its traffic sensor
data (drk:traffic-data) with a data user (drk:data-user), who may be a city
transport authority, a company or a university research group.

The order-based eleven, one per thing that can go wrong:

    KGC310  isA R&D      x eq SR    -> Compatible    one resource premise
    KGC311  isA Purpose  x eq NCR   -> Compatible    two premises + transitivity
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
    KGC404  isA R&D      x isA SR   -> Compatible    a category against a
                                                     category

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
            "development. A university commits to use for scientific "
            "research."),
        "description": (
            "First policy (purpose, isA, dpv:ResearchAndDevelopment) against second "
            "policy (purpose, eq, dpv:ScientificResearch).  The vocabulary places "
            "the second policy's purpose under the first policy's directly, so the "
            "witness holds in every model and the verdict is Compatible.  "
            "The refutation should cite one resource premise."
        ),

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
    dcterms:title "Use for research and development purposes only"@en ;
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
        "tree": [C("isA", PUR), C("eq", NCR, side="request")],
         "binding": BINDING,
        "summary": (
            "A city's traffic data platform permits use for any DPV "
            "purpose. A university commits to use for non-commercial "
            "research."),
            "description": (
            "First policy (purpose, isA, dpv:Purpose) against second policy "
            "(purpose, eq, dpv:NonCommercialResearch).  The resource places "
            "NonCommercialResearch below two parents, including "
            "dpv:ResearchAndDevelopment, which is below dpv:Purpose.  The "
            "refutation uses that ResearchAndDevelopment path and transitivity. "
            "Compatible, with two resource premises and one instance of "
            "transitivity."
        ),

        "fof_decls": """\
% Declarations: empty, as above.
""",

        "expected_q1": "Satisfiable",
        "expected_q2": "Unsatisfiable",

        "smt2_logic": "UF",
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
@prefix dpv-odrl: <https://w3id.org/dpv/mappings/odrl#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .

drk:policy-311-1 a odrl:Set ;
    odrl:uid drk:policy-311-1 ;
    odrl:profile dpv-odrl: ;
    dcterms:title "Use for any DPV purpose"@en ;
    odrl:assigner drk:data-platform ;
    odrl:permission kgc:KGC311-p1-r1 .

kgc:KGC311-p1-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:traffic-data ;
    odrl:constraint kgc:KGC311-p1-c1 .

kgc:KGC311-p1-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:Purpose ;
    odrl:operator odrl:isA ;
    odrl:rightOperand dpv:Purpose .

drk:policy-311-2 a odrl:Set ;
    odrl:uid drk:policy-311-2 ;
    odrl:profile dpv-odrl: ;
    dcterms:title "Use for non-commercial research only"@en ;
    odrl:assignee drk:data-user ;
    odrl:permission kgc:KGC311-p2-r1 .

kgc:KGC311-p2-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:traffic-data ;
    odrl:constraint kgc:KGC311-p2-c1 .

kgc:KGC311-p2-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:Purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:NonCommercialResearch .""",
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
        "name":              "purpose, eq dpv:Marketing against eq dpv:SR",
        "left_operand":      "purpose",
        "sort":              "tax",
        "resource":          RESOURCE,
            "binding": BINDING,
        "background_theory": EMPTY_BT,
        "summary": (
            "A city's traffic data platform permits use for marketing. A "
            "university commits to use for scientific research."),
        "includes":          INCLUDES,
        "tree": [C("eq", MK), C("eq", SR, side="request")],
        "description": (
            "First policy (purpose, eq, dpv:Marketing) against second policy "
            "(purpose, eq, dpv:ScientificResearch).  Both denote singletons, and the two "
            "constraints are satisfiable together only if the two concepts "
            "are the same.  DPV publishes no distinctness, so a model may "
            "identify them: Unknown.  The same pair under "
            "declarations that declare the two purposes distinct is Incompatible, "
            "which is what makes the declaration visible in the verdict."
        ),

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
                           "DPV does not declare marketing and scientific "
                           "research distinct. One structure identifies them "
                           "and one does not, so the verdict is Unknown."),
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
    dcterms:title "Use for marketing only"@en ;
    odrl:assigner drk:data-platform ;
    odrl:permission kgc:KGC313-p1-r1 .

kgc:KGC313-p1-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:traffic-data ;
    odrl:constraint kgc:KGC313-p1-c1 .

kgc:KGC313-p1-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:Purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:Marketing .

drk:policy-313-2 a odrl:Set ;
    odrl:uid drk:policy-313-2 ;
    odrl:profile dpv-odrl: ;
    dcterms:title "Use for scientific research only"@en ;
    odrl:assignee drk:data-user ;
    odrl:permission kgc:KGC313-p2-r1 .

kgc:KGC313-p2-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:traffic-data ;
    odrl:constraint kgc:KGC313-p2-c1 .

kgc:KGC313-p2-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:Purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:ScientificResearch .""",
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
        "name":              "purpose, eq dpv:Marketing against eq dpv:SR, "
                             "under a declared distinctness",
        "left_operand":      "purpose",
        "sort":              "tax",
        "resource":          RESOURCE,
        "background_theory": DECLARED_BT,
        "binding": BINDING,
        "includes":          INCLUDES_DECLARED,
        "tree": [C("eq", MK), C("eq", SR, side="request")],
        "summary": (
            "As KGC313, with marketing and scientific research declared "
            "distinct."),
        "description": (
            "The constraints of KGC313, over the same resource, under "
            "declarations in which the two purposes are declared "
            "distinct.  No model then identifies them, the witness fails "
            "everywhere, and the verdict is Incompatible.  DPV publishes no "
            "such distinctness: the verdict rests on the declaration, and "
            "the certificate marks it withdrawable."
        ),

        "fof_decls": _iso((MK, SR))[0],

        "expected_q1": "Unsatisfiable",
        "expected_q2": "Satisfiable",

        "smt2_logic": "UF",
        "smt2_background": _iso((MK, SR))[1],

        "certificate": {
            "kind": "Refutation",
   "comment": (
        "The declarations declare Marketing and ScientificResearch "
        "distinct, so the two constraints cannot be satisfied by the same "
        "purpose. This declaration changes the verdict from Unknown to "
        "Incompatible; withdrawing the declaration would return the verdict "
        "to Unknown."
    ),
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
    dcterms:title "Use for marketing only"@en ;
    odrl:assigner drk:data-platform ;
    odrl:permission kgc:KGC314-p1-r1 .

kgc:KGC314-p1-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:traffic-data ;
    odrl:constraint kgc:KGC314-p1-c1 .

kgc:KGC314-p1-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:Purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:Marketing .

drk:policy-314-2 a odrl:Set ;
    odrl:uid drk:policy-314-2 ;
    odrl:profile dpv-odrl: ;
    dcterms:title "Use for scientific research only"@en ;
    odrl:assignee drk:data-user ;
    odrl:permission kgc:KGC314-p2-r1 .

kgc:KGC314-p2-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:traffic-data ;
    odrl:constraint kgc:KGC314-p2-c1 .

kgc:KGC314-p2-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:Purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:ScientificResearch .""",
    },

    # -----------------------------------------------------------------
    # KGC315  The longest chain in the module, taken in the direction the
    # order runs.  Six resource statements and transitivity.
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
        "tree": [C("isA", PUR), C("eq", RIS, side="request")],
        "summary": (
            "A city's traffic data platform permits use for any DPV "
            "purpose. A company commits to use for recruitment interview "
            "scheduling."),
        "description": (
            "First policy (purpose, isA, dpv:Purpose) against second policy "
            "(purpose, eq, dpv:RecruitmentInterviewScheduling), the deepest concept in the "
            "module.  The resource relates them only through six steps, so "
            "the refutation must chain all six.  Compatible.  The verdict is "
            "the same as KGC310's; what grows with the depth is the "
            "certificate, not the answer."
        ),

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
    "RecruitmentInterviewScheduling lies below Purpose through a six-step "
    "hierarchy: RecruitmentInterviewManagement, RecruitmentManagement, "
    "PersonnelHiring, PersonnelManagement, and HumanResourceManagement. "
    "All six relations are published by DPV. The depth is the point: this "
    "is the longest chain in the module, and no purpose that fits traffic "
    "data lies deeper than two steps, so the case keeps the deepest chain "
    "and not a mobility purpose. It is the counterpart of row D6 in "
    "baseline/solidlab, where a policy engine is asked the same question at "
    "one, two and six steps."
),
            "premises": [
                ("fromResource", "the six order statements of the chain"),
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
    dcterms:title "Use for recruitment interview scheduling only"@en ;
    odrl:assignee drk:data-user ;
    odrl:permission kgc:KGC315-p2-r1 .

kgc:KGC315-p2-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:traffic-data ;
    odrl:constraint kgc:KGC315-p2-c1 .

kgc:KGC315-p2-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:Purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:RecruitmentInterviewScheduling .""",
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
            "research. A company commits to use for research and "
            "development."),
        "description": (
            "KGC310 the other way round: the first policy takes scientific "
            "research and what lies below it, and the second names research "
            "and development. DPV places scientific research directly below "
            "research and development and publishes no edge back. A use for "
            "research and development satisfies both policies only if it "
            "lies below scientific research, and with the published edge "
            "antisymmetry then makes the two purposes one. A structure that "
            "identifies them admits the use. A structure that keeps them "
            "apart has no edge from research and development down to "
            "scientific research, and no use satisfies both. The verdict is "
            "Unknown where KGC310 is Compatible. The pair shows that isA "
            "reads the order in one direction: swapping the operands is not "
            "a symmetry of the semantics."
        ),

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
                "development and publishes no edge back. In a structure "
                "that identifies the two purposes, a use for research and "
                "development is a use for scientific research and satisfies "
                "both policies. In a structure that keeps them apart, "
                "antisymmetry with the published edge forbids the converse "
                "edge, and no use satisfies both. So the verdict is "
                "Unknown."),
            "premises": [],
        },
        "ttl": _ttl("KGC316", PURPOSE,
                    "use for scientific research purposes only",
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
        "fof_decls": _D403[0], "smt2_background": _D403[1],
        "expected_verdict": "Incompatible",
        "expected_q1": "Unsatisfiable", "expected_q2": "Satisfiable",
        "summary": (
            "As KGC316, with scientific research and research and "
            "development declared distinct."),
        "description": (
            "The use must be research and development and must lie under "
            "scientific research. DPV places scientific research below "
            "research and development, so the converse edge would make "
            "antisymmetry identify the two. They are declared distinct, so "
            "no structure admits the use and the verdict is Incompatible. "
            "KGC316 leaves the question open and is Unknown."),
        "certificate": {"kind": "Refutation",
            "comment": (
                "DPV places scientific research below research and "
                "development. A use for research and development under "
                "scientific research would need the converse edge, and "
                "antisymmetry would then make the two purposes one. They "
                "are declared distinct, so no use satisfies both "
                "policies."),
            "premises": [("fromResource", "SR below RnD"),
                         ("fromOrderAxiom", "antisymmetry"),
                         ("fromDeclarations", "SR distinct from RnD")]},
        "provenance": "As KGC316.",
        "ttl": _ttl("KGC403", PURPOSE,
                    "use for scientific research purposes only",
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
            "First policy (purpose, isNoneOf, {dpv:Marketing}) against second "
            "policy (purpose, eq, dpv:Marketing).  The first policy excludes exactly the "
            "purpose the second requires.  No order statement and no "
            "declaration takes part: the witness asks for a concept both "
            "distinct from and identical to marketing, which no structure "
            "provides.  Incompatible, and the certificate has nothing "
            "withdrawable in it, so unlike KGC300 and KGC314 no party can "
            "reopen the verdict by retracting a statement."
        ),

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
    "the verdict is Incompatible without any resource statement or "
    "declaration."),
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
        "fof_decls": _D318[0], "smt2_background": _D318[1],
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
            "use for scientific research satisfies both policies in every "
            "structure and the verdict is Compatible. Without the "
            "declaration a structure may identify the two purposes, and the "
            "verdict is Unknown, as in KGC313. KGC323 and KGC374 show the "
            "same step over file types and languages."),
        "certificate": {"kind": "Refutation",
            "comment": (
                "Scientific research is declared distinct from marketing, so "
                "a use for scientific research is a use for a purpose other "
                "than marketing and satisfies both policies."),
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
            "A city's traffic data platform permits use for exactly one of "
            "commercial and non-commercial purposes. A university research "
            "group commits to use for non-commercial research."),
        "description": (
            "DPV places non-commercial research below non-commercial "
            "purpose, so the second branch holds. Exactly one branch may "
            "hold, so non-commercial research must not also lie below "
            "commercial purpose. DPV states no disjointness between the "
            "two, and none is warranted: it defines a commercial purpose "
            "by a commercial setting or an intention to commercialise, and "
            "a non-commercial purpose by a non-commercial setting or the "
            "lack of that intention, and one purpose can meet both. A "
            "structure that keeps non-commercial research out of "
            "commercial purpose admits the use. A structure that adds the "
            "edge makes both branches hold and refuses it. The verdict is "
            "Unknown. KGC395 joins two branches with or and is Compatible "
            "on the first branch alone."),
        "certificate": {"kind": "Models",
            "comment": (
                "DPV places non-commercial research below non-commercial "
                "purpose, so the second branch holds. DPV defines a "
                "commercial purpose as one performed in \"a commercial "
                "setting or with intention to commercialise\" and a "
                "non-commercial purpose as one performed in \"a "
                "non-commercial setting or without intention to "
                "commercialise\". One purpose can meet both, so no "
                "disjointness between the two is warranted, and none is "
                "declared. In a structure that keeps non-commercial "
                "research out of commercial purpose, a use for it "
                "satisfies both policies. In a structure that also places "
                "it below commercial purpose, both branches hold, so "
                "'exactly one' fails, and no use satisfies both. So the "
                "verdict is "
                "Unknown."),
            "premises": []},
        "provenance": "Data-sharing agreements that split commercial from "
                      "non-commercial use.",
        "ttl": _ttl("KGC319", PURPOSE,
                    "use for exactly one of commercial and non-commercial purposes",
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
        "twin":              "KGC394",
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
            "transport mobility lies below public benefit. isAnyOf does "
            "not read the order; it asks whether the use's purpose is one "
            "of the two named concepts. As published nothing separates "
            "improving transport mobility from either, so a structure may "
            "identify them and the verdict is Unknown. KGC395 is the "
            "draft the drafter meant."),
        "certificate": {"kind": "Models",
            "comment": "One structure identifies improving transport "
                       "mobility with one of the two purposes and admits "
                       "the use; one keeps them apart and does not. The "
                       "published order is not consulted by isAnyOf.",
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
        "fof_decls": _D394[0], "smt2_background": _D394[1],
        "expected_verdict": "Incompatible",
        "expected_q1": "Unsatisfiable", "expected_q2": "Satisfiable",
        "summary": (
            "As KGC393, with improving transport mobility declared "
            "distinct from both purposes the first policy names."),
        "description": (
            "Improving transport mobility is then neither of the two "
            "concepts, the witness fails everywhere, and the verdict is "
            "Incompatible. The distinctness is true, one concept lying "
            "below another does not make them one, and it refutes exactly "
            "the compatibility the drafter intended. The operator, not "
            "the taxonomy, decided."),
        "certificate": {"kind": "Refutation",
            "comment": (
                "Improving transport mobility is declared distinct from "
                "public benefit and from non-commercial research, so it "
                "is neither value the first policy lists."),
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
        "twin":              "KGC399",
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
            "A city's traffic data platform permits use for any purpose "
            "under public benefit or under non-commercial research. A "
            "city transport authority commits to improving transport "
            "mobility."),
        "description": (
            "The taxonomic draft of KGC393's intent. The first disjunct "
            "reads the order, DPV places improving transport mobility "
            "below public benefit, and the verdict is Compatible on one "
            "published statement. Same intent as KGC393, opposite "
            "behaviour: this draft defers to the authority and covers "
            "purposes DPV adds below the branch; KGC393's is fixed to two "
            "names."),
        "certificate": {"kind": "Refutation",
            "comment": "DPV places improving transport mobility below "
                       "public benefit; the first disjunct decides it.",
            "premises": [("fromResource", "ITM below PublicBenefit")]},
        "provenance": "As KGC393.",
        "ttl": _ttl("KGC395", PURPOSE,
                    "use for public benefit or non-commercial research purposes only",
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
            "A city's traffic data platform permits use for public "
            "benefit purposes. A city transport authority commits to data "
            "altruism and improving transport mobility together."),
        "description": (
            "The use carries two purposes. DPV places data altruism and "
            "improving transport mobility directly below public benefit, "
            "so each lies under the category the first policy names, and "
            "the verdict is Compatible on two published statements. The "
            "second policy combines the purposes as DPV's scope note for "
            "data altruism asks. DPV-ODRL's usage note for Purpose lists "
            "isA, eq, neq, isAnyOf and isNoneOf and not isAllOf, so the "
            "second policy goes beyond it."),
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
                    "use for public benefit purposes only",
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
        "fof_decls": _D397[0], "smt2_background": _D397[1],
        "expected_verdict": "Compatible",
        "expected_q1": "Satisfiable", "expected_q2": "Unsatisfiable",
        "summary": (
            "A city's traffic data platform permits use for any purpose "
            "except marketing. A company commits to advertising."),
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
            "A city's traffic data platform permits use for any purpose "
            "under public benefit or under non-commercial research. A "
            "company commits to use for commercial research."),
        "description": (
            "Commercial research lies below commercial purpose and below "
            "research and development. It lies below neither branch of the "
            "first policy, and DPV publishes nothing that keeps it out of "
            "them. A structure that keeps it out has no disjunct that "
            "holds, and no use satisfies both policies. A structure that "
            "also places it below public benefit or below non-commercial "
            "research admits the use. The verdict is Unknown, where "
            "KGC395, with a second policy under the first branch, is "
            "Compatible."),
        "certificate": {"kind": "Models",
            "comment": (
                "DPV places commercial research below commercial purpose "
                "and below research and development, and below neither "
                "public benefit nor non-commercial research. It publishes "
                "nothing that keeps it out of them. In a structure that "
                "keeps it out, no disjunct holds and no use satisfies "
                "both policies. In a structure that also places it below "
                "public benefit or below non-commercial research, a use "
                "for commercial research satisfies both. So the verdict "
                "is Unknown."),
            "premises": []},
        "provenance": "As KGC393.",
        "ttl": _ttl("KGC399", PURPOSE,
                    "use for public benefit or non-commercial research purposes only",
                    [("isA", ["PublicBenefit"]),
                     ("isA", ["NonCommercialResearch"])],
                    "use for commercial research only",
                    [("eq", ["CommercialResearch"])],
                    connective="or"),
    },
    # -----------------------------------------------------------------
    # KGC404  A category against a category.  Both lie above scientific
    # research, so a use for it is under both.
    # -----------------------------------------------------------------
    {
        "id": "KGC404", "subdir": "verdict",
        "name": "purpose, isA dpv:R&D against isA dpv:SR",
        "left_operand": "purpose", "sort": "tax",
        "resource": RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING, "includes": INCLUDES,
        "tree": [C("isA", RND), C("isA", SR, side="request")],
        "expected_verdict": "Compatible",
        "expected_q1": "Satisfiable", "expected_q2": "Unsatisfiable",
        "summary": (
            "A city's traffic data platform permits use for research and "
            "development purposes. A university commits to use for "
            "scientific research purposes."),
        "description": (
            "Each policy names a category. DPV places scientific research "
            "directly below research and development, so a use for "
            "scientific research lies under both categories, and the "
            "verdict is Compatible on one published statement and "
            "reflexivity."),
        "certificate": {"kind": "Refutation",
            "comment": (
                "DPV places scientific research below research and "
                "development, so a use for scientific research lies under "
                "the category of each policy."),
            "premises": [("fromResource", "SR below RnD"),
                         ("fromOrderAxiom", "reflexivity")]},
        "provenance": "Category clauses on both sides of a data-sharing "
                      "agreement.",
        "ttl": _ttl("KGC404", PURPOSE,
                    "use for research and development purposes only",
                    [("isA", ["ResearchAndDevelopment"])],
                    "use for scientific research purposes only",
                    [("isA", ["ScientificResearch"])]),
    },
]