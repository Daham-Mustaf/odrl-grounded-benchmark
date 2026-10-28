# =====================================================================
# problem_data_dpv.py: three blocks to replace
# Fourteen problems over the DPV purposes slice.
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
    an unsat core and a TPTP proof are compared by premise name.
    """
    fof = ["% Declarations: declared distinctness instances, stated in",
           "% the declarations file and instantiated here.", ""]
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
            f"    odrl:target drk:manuscripts ;\n"
            f"    odrl:constraint {cref} .\n" + lc)
    for cid, (op, vals) in zip(cids, constraints):
        body += _cnode(cid, lo, op, vals)
    return body


def _ttl(pid, lo, offer_title, offer_cs, req_title, req_cs, connective=None):
    return (_HEAD
            + _side(pid, 1, offer_title,
                    "odrl:assigner drk:library ;", lo, offer_cs, connective)
            + _side(pid, 2, req_title,
                    "odrl:assignee drk:researcher ;", lo, req_cs))


PURPOSE = "dpv-odrl:Purpose"

_D394 = _iso((SR, RND), (SR, MK))
_D397 = _iso((ADV, MK))
_D318 = _iso((SR, MK))


"""
Fourteen problems over the DPV purposes slice.

The order-based nine, one per thing that can go wrong:

    KGC310  isA R&D      x eq SR    -> Compatible    one resource premise
    KGC311  isA Purpose  x eq NCR   -> Compatible    two premises + transitivity
    KGC313  eq Marketing x eq SR    -> Unknown       nothing declares them apart
    KGC314  the same pair under declarations that do -> Incompatible
    KGC315  isA Purpose  x eq RIS   -> Compatible    six premises + transitivity
    KGC316  isA SR       x eq R&D   -> Unknown     the order runs one way, twin of KGC310
    KGC317  isNoneOf {Mk} x eq Mk   -> Incompatible  from the constraints alone
    KGC318  neq Mk       x eq SR    -> Compatible    under declared distinctness
    KGC319  xone(isA R&D, isA Mk) x eq SR -> Unknown the branches are not disjoint

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
which is what the declarations state, and may not be declared
disjoint: the resource publishes a concept below both, so the declarations
and the resource would share no model.
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
            "A library permits use for research and development. A "
            "researcher's policy commits to use for scientific research."),
        "description": (
            "Offer (purpose, isA, dpv:ResearchAndDevelopment) against request "
            "(purpose, eq, dpv:ScientificResearch).  The vocabulary places "
            "the requested purpose under the offered one directly, so the "
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
    odrl:assigner drk:library ;
    odrl:permission kgc:KGC310-p1-r1 .

kgc:KGC310-p1-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC310-p1-c1 .

kgc:KGC310-p1-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:Purpose ;
    odrl:operator odrl:isA ;
    odrl:rightOperand dpv:ResearchAndDevelopment .

drk:policy-310-2 a odrl:Set ;
    odrl:uid drk:policy-310-2 ;
    odrl:profile dpv-odrl: ;
    dcterms:title "Use for scientific research only"@en ;
    odrl:assignee drk:researcher ;
    odrl:permission kgc:KGC310-p2-r1 .

kgc:KGC310-p2-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
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
            "A library permits use for any DPV purpose. A researcher's policy "
            "commits to use for non-commercial research."),
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
    odrl:assigner drk:library ;
    odrl:permission kgc:KGC311-p1-r1 .

kgc:KGC311-p1-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC311-p1-c1 .

kgc:KGC311-p1-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:Purpose ;
    odrl:operator odrl:isA ;
    odrl:rightOperand dpv:Purpose .

drk:policy-311-2 a odrl:Set ;
    odrl:uid drk:policy-311-2 ;
    odrl:profile dpv-odrl: ;
    dcterms:title "Use for non-commercial research only"@en ;
    odrl:assignee drk:researcher ;
    odrl:permission kgc:KGC311-p2-r1 .

kgc:KGC311-p2-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
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
            "A library permits use for marketing. A researcher's policy "
            "commits to use for scientific research."),
        "includes":          INCLUDES,
        "tree": [C("eq", MK), C("eq", SR, side="request")],
        "description": (
            "Offer (purpose, eq, dpv:Marketing) against request (purpose, eq, "
            "dpv:ScientificResearch).  Both denote singletons, and the two "
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
    odrl:assigner drk:library ;
    odrl:permission kgc:KGC313-p1-r1 .

kgc:KGC313-p1-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC313-p1-c1 .

kgc:KGC313-p1-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:Purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:Marketing .

drk:policy-313-2 a odrl:Set ;
    odrl:uid drk:policy-313-2 ;
    odrl:profile dpv-odrl: ;
    dcterms:title "Use for scientific research only"@en ;
    odrl:assignee drk:researcher ;
    odrl:permission kgc:KGC313-p2-r1 .

kgc:KGC313-p2-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
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
            "declarations in which the parties declare the two purposes "
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
    odrl:assigner drk:library ;
    odrl:permission kgc:KGC314-p1-r1 .

kgc:KGC314-p1-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC314-p1-c1 .

kgc:KGC314-p1-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:Purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:Marketing .

drk:policy-314-2 a odrl:Set ;
    odrl:uid drk:policy-314-2 ;
    odrl:profile dpv-odrl: ;
    dcterms:title "Use for scientific research only"@en ;
    odrl:assignee drk:researcher ;
    odrl:permission kgc:KGC314-p2-r1 .

kgc:KGC314-p2-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
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
            "A library permits use for any DPV purpose. A researcher's policy "
            "commits to use for recruitment interview scheduling."),
        "description": (
            "Offer (purpose, isA, dpv:Purpose) against request (purpose, eq, "
            "dpv:RecruitmentInterviewScheduling), the deepest concept in the "
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
    "All six relations are published by DPV."
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
    odrl:assigner drk:library ;
    odrl:permission kgc:KGC315-p1-r1 .

kgc:KGC315-p1-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC315-p1-c1 .

kgc:KGC315-p1-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:Purpose ;
    odrl:operator odrl:isA ;
    odrl:rightOperand dpv:Purpose .

drk:policy-315-2 a odrl:Set ;
    odrl:uid drk:policy-315-2 ;
    odrl:profile dpv-odrl: ;
    dcterms:title "Use for recruitment interview scheduling only"@en ;
    odrl:assignee drk:researcher ;
    odrl:permission kgc:KGC315-p2-r1 .

kgc:KGC315-p2-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
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
        "twin":              "KGC310",
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
            "A library permits use for scientific research. A researcher's "
            "policy commits to use for research and development."),
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
            "A library permits use for any purpose other than marketing. A "
            "researcher's policy commits to use for marketing."),
        "description": (
            "Offer (purpose, isNoneOf, {dpv:Marketing}) against request "
            "(purpose, eq, dpv:Marketing).  The offer excludes exactly the "
            "purpose the request requires.  No order statement and no "
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
    odrl:assigner drk:library ;
    odrl:permission kgc:KGC317-p1-r1 .

kgc:KGC317-p1-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC317-p1-c1 .

kgc:KGC317-p1-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:Purpose ;
    odrl:operator odrl:isNoneOf ;
    odrl:rightOperand ( dpv:Marketing ) .

drk:policy-317-2 a odrl:Set ;
    odrl:uid drk:policy-317-2 ;
    odrl:profile dpv-odrl: ;
    dcterms:title "Use for marketing only"@en ;
    odrl:assignee drk:researcher ;
    odrl:permission kgc:KGC317-p2-r1 .

kgc:KGC317-p2-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
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
            "A library permits use for any purpose other than marketing. A "
            "researcher's policy commits to use for scientific research. "
            "Scientific research is declared distinct from marketing."),
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
    # it fails only if the two branches are disjoint.
    # -----------------------------------------------------------------
    {
        "id": "KGC319", "subdir": "verdict",
        "name": "purpose, xone(isA RnD, isA Marketing) against eq "
                "ScientificResearch",
        "left_operand": "purpose", "sort": "tax",
        "resource": RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING, "includes": INCLUDES,
        "tree": [Xone((C("isA", RND), C("isA", MK))),
                 C("eq", SR, side="request")],
        "expected_verdict": "Unknown",
        "expected_q1": "Satisfiable", "expected_q2": "Satisfiable",
        "summary": (
            "A library permits use for exactly one of research and "
            "development and marketing. A researcher's policy commits to use "
            "for scientific research."),
        "description": (
            "DPV places scientific research below research and development, "
            "so the first branch holds. Exactly one branch may hold, so "
            "scientific research must not also lie below marketing. DPV "
            "states no disjointness between research and development and "
            "marketing, and the declarations here add none. A structure that "
            "keeps scientific research out of marketing admits the use. A "
            "structure that adds the edge makes both branches hold and "
            "refuses it. The verdict is Unknown. KGC395 joins the same two "
            "branches with or and is Compatible on the first branch alone."),
        "certificate": {"kind": "Models",
            "comment": (
                "In a structure that keeps scientific research out of "
                "marketing, a use for scientific research satisfies both "
                "policies. In a structure that also places scientific "
                "research below marketing, both branches hold, exactly one "
                "fails, and no use satisfies both. DPV states no "
                "disjointness between the two branches, so the verdict is "
                "Unknown."),
            "premises": []},
        "provenance": "Purpose limitation lists in data licences.",
        "ttl": _ttl("KGC319", PURPOSE,
                    "use for exactly one of research and development and marketing",
                    [("isA", ["ResearchAndDevelopment"]), ("isA", ["Marketing"])],
                    "use for scientific research only",
                    [("eq", ["ScientificResearch"])],
                    connective="xone"),
    },
   # -----------------------------------------------------------------
    # KGC393 / 394 / 395  One intent, three drafts: isAnyOf is identity.
    # -----------------------------------------------------------------
    {
        "id": "KGC393", "subdir": "verdict",
        "twin":              "KGC394",
        "name": "purpose, isAnyOf {RnD, Marketing} against eq ScientificResearch",
        "left_operand": "purpose", "sort": "tax",
        "resource": RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING, "includes": INCLUDES,
        "tree": [C("isAnyOf", RND, MK), C("eq", SR, side="request")],
        "expected_verdict": "Unknown",
        "expected_q1": "Satisfiable", "expected_q2": "Satisfiable",
        "summary": (
            "A library permits use for research and development or "
            "marketing; a researcher commits to scientific research."),
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
                    "use for at least one of research and development and marketing",
                    [("isAnyOf", ["ResearchAndDevelopment", "Marketing"])],
                    "use for scientific research only", [("eq", ["ScientificResearch"])]),
    },
    {
        "id": "KGC394", "subdir": "verdict",
        "twin":              "KGC393",
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
            "purposes the first policy names."),
        "description": (
            "Scientific research is then neither of the two concepts, the "
            "witness fails everywhere, and the verdict is Incompatible. The "
            "distinctness is true, one concept lying below another does not "
            "make them one, and it refutes exactly the compatibility the "
            "drafter intended. The operator, not the taxonomy, decided."),
        "certificate": {"kind": "Refutation",
            "comment": (
                "Scientific research is declared distinct from research and "
                "development and from marketing, so it is neither value the "
                "first policy lists."),
            "premises": [("fromDeclarations", "SR distinct from RnD"),
                         ("fromDeclarations", "SR distinct from Marketing")]},
        "provenance": "As KGC393; warrant DPV's definitions of distinct purposes.",
        "ttl": _ttl("KGC394", PURPOSE,
                    "use for at least one of research and development and marketing",
                    [("isAnyOf", ["ResearchAndDevelopment", "Marketing"])],
                    "use for scientific research only", [("eq", ["ScientificResearch"])]),
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
            "A library permits use for any purpose under research and "
            "development or under marketing; a researcher commits to "
            "scientific research."),
        "description": (
            "The taxonomic draft of KGC393's intent. The first disjunct reads "
            "the order, DPV places scientific research below research and "
            "development, and the verdict is Compatible on one published "
            "statement. Same intent as KGC393, opposite behaviour: this draft "
            "defers to the authority and covers purposes DPV adds below the "
            "branch; KGC393's is fixed to two names."),
        "certificate": {"kind": "Refutation",
            "comment": "DPV places scientific research below research and "
                       "development; the first disjunct decides it.",
            "premises": [("fromResource", "SR below RnD")]},
        "provenance": "As KGC393.",
        "ttl": _ttl("KGC395", PURPOSE,
                    "use for research and development or marketing purposes only",
                    [("isA", ["ResearchAndDevelopment"]), ("isA", ["Marketing"])],
                    "use for scientific research only", [("eq", ["ScientificResearch"])],
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
            "A library permits use for research and development or "
            "marketing. A researcher's policy commits to both research and "
            "development and service provision."),
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
            "comment": (
                "Research and development is one of the values the first "
                "policy lists, and nothing in the first policy limits the "
                "use's other purposes."),
            "premises": []},
        "provenance": "Purpose limitation (GDPR Art. 5(1)(b)) against a "
                      "consumer declaring several purposes.",
        "ttl": _ttl("KGC396", PURPOSE,
                    "use for at least one of research and development and marketing",
                    [("isAnyOf", ["ResearchAndDevelopment", "Marketing"])],
                    "use for both research and development and service provision",
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
            "A library permits use for any purpose except marketing; a "
            "researcher commits to advertising."),
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
]