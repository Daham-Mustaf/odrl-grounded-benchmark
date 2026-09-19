"""
problem_data_tom.py
===================
Five problems over the technical and organisational measures resource, at
tax. Every isAllOf problem in the suite is here.

    KGC360  isAllOf(encryption, access control) x isA TechnicalMeasure
                                                        -> Compatible
    KGC361  isAllOf(encryption, access control) x isNoneOf(access control)
                                                        -> Incompatible
    KGC362  isAnyOf(encryption, access control) x eq encryption
                                                        -> Compatible
    KGC363  isAllOf(encryption, access control) x eq encryption
                                                        -> Unknown
    KGC364  as KGC363, with the two measures declared distinct
                                                        -> Incompatible

Why isAllOf needs this operand and no other
--------------------------------------------
A valuation binds a finite set of concepts to an operand, and for every
other operand of the suite that set has one element: a processing operation
has one purpose in the sense the constraint asks about, a consent record is
in one state, a transfer rests on one legal basis. Measures are different.
A controller has encryption in place and access control and
pseudonymisation, together, and a clause requiring safeguards requires them
together rather than requiring one of them.

isAllOf is the operator for that, and it is the only one whose satisfaction
condition runs the other way: the constraint's denotation must lie inside
what the use supplies, where every other operator asks that the use lie
inside the denotation. On a single-valued use the operator cannot show
this. Over one value it says what eq says. Over two it holds only if the
two names denote one concept, so the verdict turns on distinctness, not on
the operator. KGC363 and KGC364 make that point. The superset condition
does its own work only on a use that supplies several concepts, which is
why the operator went unexercised until this resource was built.

What KGC360 and KGC361 show
---------------------------
KGC360 puts the requirement against a use whose measures are technical
ones. Both required measures lie below dpv:TechnicalMeasure, which the
resource asserts, so a use supplying exactly those two satisfies the
offer and the request together. The verdict is Compatible, and the
certificate cites the two assertions that carry it.

KGC361 puts the same requirement against a processor that excludes access
control. The requirement needs access control among the measures supplied
and the exclusion keeps it out, so no structure admits a common use: the
verdict is Incompatible, and it holds without any declaration by the
parties. The certificate cites the constraints and nothing else. That is
worth contrasting with the legal-basis problems, where a definite
Incompatible needed the parties to declare concepts distinct: here the two
constraints contradict each other over the same named concept, and the
vocabulary is not consulted at all.

Together they exercise both directions of the superset mode: the case
where the required set is carried by the order, and the case where it is
kept out by a complement.

What KGC362 to KGC364 show
--------------------------
The three keep the values fixed and change one thing at a time. KGC362
asks for at least one of the two measures. A use supplying encryption
meets it on the constraints alone, so the verdict is Compatible. KGC363
changes isAnyOf to isAllOf. The conflict looks immediate but is not
definite. A structure may identify the two measures, and DPV separates
them nowhere, so the verdict is Unknown as published. KGC364 adds the
parties' declaration that the two are distinct, and the verdict becomes
Incompatible. Even the obvious conflict rested on a declared premise.
"""

from compile import Constraint

# Concept slugs, as the TPTP and SMT-LIB encodings name them.
TOM        = "tm_technical_organisational_measure"
TECHNICAL  = "tm_technical_measure"
ENCRYPTION = "tm_encryption"
ACCESS     = "tm_access_control_method"

# The left operand as the Turtle writes it. Not a slug.
TOM_LO     = "dpv-odrl:TechnicalOrganisationalMeasure"

RESOURCE    = "https://w3id.org/odrl-kb/dpv-tom"
EMPTY_BT    = "https://w3id.org/odrl-kb/dpv-tom/empty"
DECLARED_BT = "https://w3id.org/odrl-kb/dpv-tom/declared"
BINDING     = "https://w3id.org/odrl-kb/profile/b-tom"

INCLUDES          = ["KGE000-0.ax", "DPV-tom.ax"]
INCLUDES_DECLARED = INCLUDES + ["DPV-tom-declared.ax"]


def C(op, *vals, side="offer"):
    return Constraint(op, tuple(vals), side)


_TTL_HEAD = """\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix dpv:     <https://w3id.org/dpv#> .
@prefix dpv-odrl:    <https://w3id.org/dpv/mappings/odrl#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .
"""


# ---------------------------------------------------------------------
# Turtle for KGC360 and KGC361. The offer is fixed, the request varies.
# ---------------------------------------------------------------------

def _offer(pid):
    return f"""
drk:offer-{pid[3:]} a odrl:Set ;
    dcterms:title "Use is permitted where encryption and access control are both in place"@en ;
    rdfs:comment "The kind of clause the DPV-ODRL guidance describes for this operand: access to a dataset permitted only where stated measures are implemented. Both are required, not one of them, which is what distinguishes isAllOf from isAnyOf here."@en ;
    odrl:assigner drk:controller ;
    odrl:permission kgc:{pid}-offer-r1 .

kgc:{pid}-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:dataset ;
    odrl:constraint kgc:{pid}-offer-c1 .

kgc:{pid}-offer-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:TechnicalOrganisationalMeasure ;
    odrl:operator odrl:isAllOf ;
    odrl:rightOperand ( dpv:Encryption dpv:AccessControlMethod ) .
"""


def _request(pid, title, operator, value):
    return f"""
drk:request-{pid[3:]} a odrl:Request ;
    dcterms:title "{title}"@en ;
    odrl:assignee drk:processor ;
    odrl:permission kgc:{pid}-request-r1 .

kgc:{pid}-request-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:dataset ;
    odrl:constraint kgc:{pid}-request-c1 .

kgc:{pid}-request-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:TechnicalOrganisationalMeasure ;
    odrl:operator odrl:{operator} ;
    odrl:rightOperand {value} .
"""


# ---------------------------------------------------------------------
# Turtle for KGC362 to KGC364. Same shape as _offer and _request, with
# the operator and values of each side passed in.
# ---------------------------------------------------------------------


_PARTIES = {
    "offer":   ("odrl:Set",   "odrl:assigner drk:controller"),
    "request": ("odrl:Request", "odrl:assignee drk:processor"),
}


def _cnode(pid, side, i, left_operand, operator, values):
    """One odrl:Constraint node. Values are DPV local names.

    A set-valued right operand is written as repeated objects rather than
    as an RDF collection. ODRL's context gives odrl:rightOperand no
    container, so the spec settles neither; the suite uses one form
    throughout so that a consumer reading the case files does not have to
    tell whether a difference in shape means a difference in meaning.
    """
    ro = " ,\n        ".join(f"dpv:{v}" for v in values)
    return f"""
kgc:{pid}-{side}-c{i} a odrl:Constraint ;
    odrl:leftOperand {left_operand} ;
    odrl:operator odrl:{operator} ;
    odrl:rightOperand {ro} .
"""

def _side(pid, side, title, left_operand, constraints):
    """One policy (offer or request), its permission and its constraints.
    constraints is a list of (operator, [DPV local names])."""
    policy, party = _PARTIES[side]
    nodes = ", ".join(f"kgc:{pid}-{side}-c{i}"
                      for i in range(1, len(constraints) + 1))
    head = f"""
drk:{side}-{pid[3:]} a {policy} ;
    dcterms:title "{title}"@en ;
    {party} ;
    odrl:permission kgc:{pid}-{side}-r1 .

kgc:{pid}-{side}-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:dataset ;
    odrl:constraint {nodes} .
"""
    return head + "".join(
        _cnode(pid, side, i, left_operand, op, vals)
        for i, (op, vals) in enumerate(constraints, start=1))


def _ttl(pid, left_operand, offer_phrase, offer, request_phrase, request):
    """Full Turtle for one problem. The phrases fill the two titles."""
    return (_TTL_HEAD
            + _side(pid, "offer",
                    f"Use is permitted with {offer_phrase} in place",
                    left_operand, offer)
            + _side(pid, "request",
                    f"Use is requested with {request_phrase} in place",
                    left_operand, request))


def _iso(*pairs):
    """Declared-distinctness instances, named bg_dist_ on both encodings.

    The declared theory states the rule and lists the measures it ranges
    over; a problem naming two of them carries the inequation between
    them, so a refutation cites the instance it used rather than one of
    2701. The name must match on both sides: an unsat core and a TPTP
    proof are compared by premise name.
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


_D364 = _iso((ENCRYPTION, ACCESS))

PROBLEMS = [

    {
        "id":                "KGC360",
        "subdir":            "verdict",
        "name":              "measures, isAllOf(Encryption, "
                             "AccessControlMethod) against "
                             "isA TechnicalMeasure",
        "left_operand":      "TechnicalOrganisationalMeasure",
        "sort":              "tax",
        "resource":          RESOURCE,
        "background_theory": EMPTY_BT,
        "includes":          INCLUDES,
        "tree": [C("isAllOf", ENCRYPTION, ACCESS),
                 C("isA", TECHNICAL, side="request")],
        "binding": BINDING,
"summary": (
    "A controller requires encryption and access control, while a "
    "processor applies technical measures."
),

        "description": (
            "The controller requires encryption and access control to be "
            "in place together; the processor states that the measures it "
            "applies are technical ones. Both required measures lie below "
            "dpv:TechnicalMeasure in the resource, so a use supplying just "
            "those two satisfies the requirement and the statement at "
            "once, and it does so in every structure. Verdict: "
            "Compatible.\n\n"
            "This is the superset mode carried by the order: isAllOf asks "
            "that its two values lie inside what the use supplies, the "
            "request bounds what the use may supply to the technical "
            "measures, and the two published assertions place the values "
            "within that bound."
        ),
        "expected_q1": "Satisfiable",
        "expected_q2": "Unsatisfiable",
        "certificate": {
            "kind": "Refutation",
            "comment": "Both required measures are technical measures in "
                       "the vocabulary, so a use supplying them satisfies "
                       "the request as well as the offer.",
            "premises": [
                ("fromResource",
                 "dpv:Encryption is below dpv:TechnicalMeasure"),
                ("fromResource",
                 "dpv:AccessControlMethod is below dpv:TechnicalMeasure"),
            ],
        },
        "ttl": _TTL_HEAD + _offer("KGC360")
               + _request("KGC360",
                          "Use only with technical measures in place",
                          "isA", "dpv:TechnicalMeasure"),
    },

    {
        "id":                "KGC361",
        "subdir":            "verdict",
        "name":              "measures, isAllOf(Encryption, "
                             "AccessControlMethod) against "
                             "isNoneOf(AccessControlMethod)",
        "left_operand":      "TechnicalOrganisationalMeasure",
        "sort":              "tax",
        "resource":          RESOURCE,
        "background_theory": EMPTY_BT,
        "includes":          INCLUDES,
        "binding": BINDING,
"summary": (
    "A controller requires encryption and access control, while a "
    "processor excludes access control."
),
        "tree": [C("isAllOf", ENCRYPTION, ACCESS),
                 C("isNoneOf", ACCESS, side="request")],
        "description": (
            "The same requirement against a processor that does not apply "
            "access control. The requirement needs access control among "
            "the measures the use supplies and the exclusion keeps it "
            "out, so no structure admits a common use and the verdict is "
            "Incompatible.\n\n"
            "It is definite without any declaration by the parties, which "
            "is unlike the legal-basis problems: there an Incompatible "
            "verdict needed the parties to declare two concepts distinct, "
            "because the question was whether two names denote one thing. "
            "Here the two constraints name the same concept and pull "
            "against each other over it, so the vocabulary is not "
            "consulted and the certificate cites the constraints alone."
        ),
        "expected_q1": "Unsatisfiable",
        "expected_q2": "Satisfiable",
        "certificate": {
            "kind": "Refutation",
            "comment": "The offer requires access control among the "
                       "measures supplied and the request excludes it. No "
                       "premise of the vocabulary or of the parties is "
                       "used.",
            "premises": [],
        },
        "ttl": _TTL_HEAD + _offer("KGC361")
               + _request("KGC361",
                          "Use without access control",
                          "isNoneOf", "dpv:AccessControlMethod"),
    },

    # -----------------------------------------------------------------
    # KGC362 / 363 / 364  The paired benchmark: same values, one operator.
    # -----------------------------------------------------------------
    {
        "id": "KGC362", "subdir": "verdict",
        "name": "measures, isAnyOf {Encryption, AccessControl} against eq Encryption",
        "left_operand": "TechnicalOrganisationalMeasure", "sort": "tax",
        "resource": RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING, "includes": INCLUDES,
        "tree": [C("isAnyOf", ENCRYPTION, ACCESS), C("eq", ENCRYPTION, side="request")],
        "expected_verdict": "Compatible",
        "expected_q1": "Satisfiable", "expected_q2": "Unsatisfiable",
        "summary": (
            "A provider requires at least one of encryption and access "
            "control; a consumer commits to encryption."),
        "description": (
            "Encryption is one of the two named safeguards, so the "
            "constraints are Compatible without consulting the "
            "vocabulary. Read with KGC363, which changes only the "
            "operator: at least one against both."),
        "certificate": {"kind": "Refutation",
            "comment": "Encryption is among the offer's values.",
            "premises": []},
        "provenance": "Safeguard clauses in data-sharing agreements.",
        "ttl": _ttl("KGC362", TOM_LO, "at least one of encryption and access control",
                    [("isAnyOf", ["Encryption", "AccessControlMethod"])],
                    "encryption", [("eq", ["Encryption"])]),
    },
    {
        "id": "KGC363", "subdir": "verdict",
        "name": "measures, isAllOf {Encryption, AccessControl} against eq Encryption",
        "left_operand": "TechnicalOrganisationalMeasure", "sort": "tax",
        "resource": RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING, "includes": INCLUDES,
        "tree": [C("isAllOf", ENCRYPTION, ACCESS), C("eq", ENCRYPTION, side="request")],
        "expected_verdict": "Unknown", "unknown_reason": "epistemic",
        "expected_q1": "Satisfiable", "expected_q2": "Satisfiable",
        "summary": (
            "A provider requires both encryption and access control; a "
            "consumer commits to encryption only."),
        "description": (
            "The offer needs both safeguards among the use's measures and the "
            "request supplies one. The conflict looks immediate and is not: "
            "a structure that identifies the two measures satisfies both "
            "sides, and DPV separates them nowhere. Unknown as published."),
        "certificate": {"kind": "Models",
            "comment": "One structure identifies encryption with access control "
                       "and admits the use; nothing published forbids it.",
            "premises": []},
        "provenance": "As KGC362; the universal clause.",
        "ttl": _ttl("KGC363", TOM_LO, "both encryption and access control",
                    [("isAllOf", ["Encryption", "AccessControlMethod"])],
                    "encryption", [("eq", ["Encryption"])]),
    },
    {
        "id": "KGC364", "subdir": "verdict",
        "name": "measures, isAllOf {Encryption, AccessControl} against eq "
                "Encryption, declared distinct",
        "left_operand": "TechnicalOrganisationalMeasure", "sort": "tax",
        "resource": RESOURCE, "background_theory": DECLARED_BT,
        "binding": BINDING, "includes": INCLUDES_DECLARED,
        "tree": [C("isAllOf", ENCRYPTION, ACCESS), C("eq", ENCRYPTION, side="request")],
        "fof_decls": _D364[0], "smt2_background": _D364[1],
        "expected_verdict": "Incompatible",
        "expected_q1": "Unsatisfiable", "expected_q2": "Satisfiable",
        "summary": (
            "As KGC363, with encryption and access control declared "
            "distinct."),
        "description": (
            "The two measures are then two, the request supplies one, and no "
            "use satisfies both sides: Incompatible. Read with KGC362: same "
            "values, one operator changed, opposite verdicts; and the "
            "obvious conflict still rested on a declared premise."),
        "certificate": {"kind": "Refutation",
            "comment": "Encryption and access control are declared distinct, so "
                       "a use supplying only encryption lacks the second.",
            "premises": [("fromBackgroundTheory",
                          "Encryption distinct from AccessControlMethod")]},
        "provenance": "As KGC362; warrant DPV's definitions.",
        "ttl": _ttl("KGC364", TOM_LO, "both encryption and access control",
                    [("isAllOf", ["Encryption", "AccessControlMethod"])],
                    "encryption", [("eq", ["Encryption"])]),
    },
]