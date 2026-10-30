"""
problem_data_tom.py
===================
Six problems over the technical and organisational measures resource, at
tax.  Four use isAllOf.

    KGC360  isAllOf(encryption, access control) x isA TechnicalMeasure
                                                        -> Compatible
    KGC362  isAnyOf(encryption, access control) x eq encryption
                                                        -> Compatible
    KGC363  isAllOf(encryption, access control) x eq encryption
                                                        -> Unknown
    KGC364  as KGC363, with the two measures declared distinct
                                                        -> Incompatible
    KGC365  isAllOf(encryption, access control) x
            isAllOf(encryption, access control, pseudonymisation)
                                                        -> Compatible
    KGC366  isAnyOf(encryption, access control) x eq encryption at rest,
            the measures declared distinct              -> Incompatible

KGC361, which set the same requirement against a policy that excludes
access control, is retired.  The contradiction it showed is in KGC317 and
KGC377.

Why isAllOf reads naturally here
--------------------------------
A controller has encryption in place and access control and
pseudonymisation, together, and a clause requiring safeguards requires them
together rather than requiring one of them.  In the semantics every
operand takes a set of values, so isAllOf is not special to this resource:
it appears on purposes, language and locations as well.

isAllOf is the operator whose satisfaction condition runs the other way:
the constraint's denotation must lie inside what the use supplies, where
every other operator asks that the use lie inside the denotation.  Over one
supplied value it says what eq says.  Over two it holds only if the two
names denote one concept, so the verdict turns on distinctness, not on the
operator.  KGC363 and KGC364 make that point.

What KGC360 shows
-----------------
KGC360 puts the requirement against a use whose measures are technical
ones.  Both required measures lie below dpv:TechnicalMeasure, which the
resource asserts, so a use supplying exactly those two satisfies the
controller's policy and the processor's together.  The verdict is
Compatible, and the certificate cites the two statements that carry it.

What KGC362 to KGC364 show
--------------------------
The three keep the values fixed and change one thing at a time.  KGC362
asks for at least one of the two measures.  A use supplying encryption
meets it on the constraints alone, so the verdict is Compatible.  KGC363
changes isAnyOf to isAllOf.  The conflict looks immediate but is not
definite.  A structure may identify the two measures, and DPV separates
them nowhere, so the verdict is Unknown as published.  KGC364 adds the
declaration that the two are distinct, and the verdict becomes
Incompatible.  Even the obvious conflict rested on a declared premise.

What KGC365 shows
-----------------
isAllOf states a minimum.  The controller's policy needs encryption and
access control among the measures in use and says nothing against others.
A use that also applies pseudonymisation has both, so it satisfies the
processor's policy and the controller's, in every structure.  The verdict
is Compatible on the constraints alone, and the resource is not consulted.
Two minimums never conflict: a use with both sets of measures satisfies
both.

What KGC366 shows
-----------------
isAnyOf matches by name.  DPV places encryption at rest below encryption,
but a use whose only measure is encryption at rest has neither of the two
names the controller lists.  As published a structure may identify the
measure with one of them, so the verdict is Unknown.  With the measures
declared distinct no use satisfies both, and the verdict is Incompatible.
ODRL has no operator for "includes some kind of encryption": isAnyOf and
isAllOf compare names, and a drafter who wants the kinds of encryption
has to list them.  Read with KGC362, where the processor's measure is
encryption itself and the verdict is Compatible.
"""

from compile import right_operand as _ro, Constraint


# Concept slugs, as the TPTP and SMT-LIB encodings name them.
TOM        = "tm_technical_organisational_measure"
TECHNICAL  = "tm_technical_measure"
ENCRYPTION = "tm_encryption"
ACCESS     = "tm_access_control_method"
PSEUDO     = "tm_pseudonymisation"
EAR        = "tm_encryption_at_rest"

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
# Turtle for KGC360. The offer is fixed, the request varies.
# ---------------------------------------------------------------------

def _offer(pid):
    return f"""
drk:policy-{pid[3:]}-1 a odrl:Set ;
    odrl:uid drk:policy-{pid[3:]}-1 ;
    odrl:profile dpv-odrl: ;
    dcterms:title "Use with both encryption and access control in place"@en ;
    rdfs:comment "The kind of clause the DPV-ODRL guidance describes for this operand: access to a dataset permitted only where stated measures are implemented. Both are required, not one of them, which is what distinguishes isAllOf from isAnyOf here."@en ;
    odrl:assigner drk:controller ;
    odrl:permission kgc:{pid}-p1-r1 .

kgc:{pid}-p1-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:dataset ;
    odrl:constraint kgc:{pid}-p1-c1 .

kgc:{pid}-p1-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:TechnicalOrganisationalMeasure ;
    odrl:operator odrl:isAllOf ;
    odrl:rightOperand ( dpv:Encryption dpv:AccessControlMethod ) .
"""


def _request(pid, title, operator, value):
    return f"""
drk:policy-{pid[3:]}-2 a odrl:Set ;
    odrl:uid drk:policy-{pid[3:]}-2 ;
    odrl:profile dpv-odrl: ;
    dcterms:title "{title}"@en ;
    odrl:assignee drk:processor ;
    odrl:permission kgc:{pid}-p2-r1 .

kgc:{pid}-p2-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:dataset ;
    odrl:constraint kgc:{pid}-p2-c1 .

kgc:{pid}-p2-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:TechnicalOrganisationalMeasure ;
    odrl:operator odrl:{operator} ;
    odrl:rightOperand {value} .
"""


# ---------------------------------------------------------------------
# Turtle for KGC362 to KGC364. Same shape as _offer and _request, with
# the operator and values of each side passed in.
# ---------------------------------------------------------------------


_PARTIES = {
    1: "odrl:assigner drk:controller",
    2: "odrl:assignee drk:processor",
}


def _cnode(pid, k, i, left_operand, operator, values):
    """One odrl:Constraint node. Values are DPV local names; a set
    operator's values are written as an RDF collection."""
    ro = _ro(operator, [f"dpv:{v}" for v in values])
    return f"""
kgc:{pid}-p{k}-c{i} a odrl:Constraint ;
    odrl:leftOperand {left_operand} ;
    odrl:operator odrl:{operator} ;
    odrl:rightOperand {ro} .
"""

def _side(pid, k, title, left_operand, constraints):
    """Policy k (1 or 2) of the pair, its permission and its constraints.
    constraints is a list of (operator, [DPV local names])."""
    nodes = ", ".join(f"kgc:{pid}-p{k}-c{i}"
                      for i in range(1, len(constraints) + 1))
    head = f"""
drk:policy-{pid[3:]}-{k} a odrl:Set ;
    odrl:uid drk:policy-{pid[3:]}-{k} ;
    odrl:profile dpv-odrl: ;
    dcterms:title "{title}"@en ;
    {_PARTIES[k]} ;
    odrl:permission kgc:{pid}-p{k}-r1 .

kgc:{pid}-p{k}-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:dataset ;
    odrl:constraint {nodes} .
"""
    return head + "".join(
        _cnode(pid, k, i, left_operand, op, vals)
        for i, (op, vals) in enumerate(constraints, start=1))


def _ttl(pid, left_operand, offer_phrase, offer, request_phrase, request):
    """Full Turtle for one problem. The phrases fill the two titles."""
    return (_TTL_HEAD
            + _side(pid, 1,
                    f"Use with {offer_phrase} in place",
                    left_operand, offer)
            + _side(pid, 2,
                    f"Use with {request_phrase}",
                    left_operand, request))


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
    "A controller permits use where encryption and access control are both "
    "in place. A processor states that it applies technical measures only, "
    "no organisational ones."),

        "description": (
            "The controller requires encryption and access control to be in "
            "place together; the processor states that the measures it "
            "applies are technical ones. isAllOf asks that both measures be "
            "among those in use; the processor's isA asks that every "
            "measure in use be a technical one. DPV places both measures "
            "below technical measure, so a use with just those two meets "
            "both policies. Verdict: Compatible."),
        "expected_q1": "Satisfiable",
        "expected_q2": "Unsatisfiable",
        "certificate": {
            "kind": "Refutation",
            "comment": (
                "Both required measures are technical measures in DPV, so a "
                "use with encryption and access control meets both "
                "policies. The processor's policy covers technical "
                "safeguards only; organisational measures are agreed "
                "separately in the processing contract."),
            "premises": [
                ("fromResource",
                 "dpv:Encryption is below dpv:TechnicalMeasure"),
                ("fromResource",
                 "dpv:AccessControlMethod is below dpv:TechnicalMeasure"),
            ],
        },
        "ttl": _TTL_HEAD + _offer("KGC360")
               + _request("KGC360",
                          "Applies technical measures only, no organisational ones",
                          "isA", "dpv:TechnicalMeasure"),
    },

    # -----------------------------------------------------------------
    # KGC362 / 363 / 364  The paired benchmark: same values, one operator.
    # -----------------------------------------------------------------
    {
        "id": "KGC362", "subdir": "verdict",
        "twin": ["KGC363", "KGC364", "KGC366"],
        "name": "measures, isAnyOf {Encryption, AccessControl} against eq Encryption",
        "left_operand": "TechnicalOrganisationalMeasure", "sort": "tax",
        "resource": RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING, "includes": INCLUDES,
        "tree": [C("isAnyOf", ENCRYPTION, ACCESS), C("eq", ENCRYPTION, side="request")],
        "expected_verdict": "Compatible",
        "expected_q1": "Satisfiable", "expected_q2": "Unsatisfiable",
        "summary": (
            "A controller requires at least one of encryption and access "
            "control. A processor's policy commits to encryption as the "
            "only measure."),
        "description": (
            "Encryption is one of the two named safeguards, so the "
            "constraints are Compatible without consulting the vocabulary. "
            "Real processors usually list the measures they apply, and two "
            "such lists never conflict (KGC365); what could conflict is the "
            "processor's \"only\", and here encryption alone is on the first "
            "policy's list. Read with KGC363, which changes only the "
            "operator: at least one against both."),
        "certificate": {"kind": "Refutation",
            "comment": (
                "Encryption is one of the values the first policy lists, so a "
                "use with encryption satisfies both policies."),
            "premises": []},
        "provenance": "Safeguard clauses in data-sharing agreements.",
        "ttl": _ttl("KGC362", TOM_LO, "at least one of encryption and access control",
                    [("isAnyOf", ["Encryption", "AccessControlMethod"])],
                    "encryption as the only measure", [("eq", ["Encryption"])]),
    },
    {
        "id": "KGC363", "subdir": "verdict",
        "twin": ["KGC364", "KGC362"],
        "name": "measures, isAllOf {Encryption, AccessControl} against eq Encryption",
        "left_operand": "TechnicalOrganisationalMeasure", "sort": "tax",
        "resource": RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING, "includes": INCLUDES,
        "tree": [C("isAllOf", ENCRYPTION, ACCESS), C("eq", ENCRYPTION, side="request")],
        "expected_verdict": "Unknown",
        "expected_q1": "Satisfiable", "expected_q2": "Satisfiable",
        "summary": (
            "A controller requires both encryption and access control; a "
            "processor commits to encryption only."),
        "description": (
            "The first policy needs both safeguards among the use's "
            "measures and the second supplies one. Real processors usually "
            "list the measures they apply, and two such lists never "
            "conflict (KGC365); the conflict here comes from the processor "
            "stating \"only\". It looks immediate and is not: if encryption "
            "and access control are the same measure, a use meets both "
            "policies, and DPV separates them nowhere. Unknown as "
            "published."),
        "certificate": {"kind": "Models",
            "comment": (
                "If encryption and access control are the same measure, a "
                "use applying encryption applies both and meets both "
                "policies; if they are different measures, the use lacks "
                "access control and no use meets both. DPV separates them "
                "nowhere, so the verdict is Unknown."),
            "premises": []},
        "provenance": "As KGC362; the universal clause.",
        "ttl": _ttl("KGC363", TOM_LO, "both encryption and access control",
                    [("isAllOf", ["Encryption", "AccessControlMethod"])],
                    "encryption as the only measure", [("eq", ["Encryption"])]),
    },
    {
        "id": "KGC364", "subdir": "verdict",
        "twin": ["KGC363", "KGC362"],
        "name": "measures, isAllOf {Encryption, AccessControl} against eq "
                "Encryption, declared distinct",
        "left_operand": "TechnicalOrganisationalMeasure", "sort": "tax",
        "resource": RESOURCE, "background_theory": DECLARED_BT,
        "binding": BINDING, "includes": INCLUDES_DECLARED,
        "tree": [C("isAllOf", ENCRYPTION, ACCESS), C("eq", ENCRYPTION, side="request")],
        "expected_verdict": "Incompatible",
        "expected_q1": "Unsatisfiable", "expected_q2": "Satisfiable",
        "summary": (
            "As KGC363, with encryption and access control declared "
            "distinct."),
        "description": (
            "KGC363 with every pair of measures declared distinct. "
            "Encryption and access control are then two measures, the "
            "processor supplies one, and no use satisfies both. Real "
            "processors usually list the measures they apply, and two such "
            "lists never conflict (KGC365); the conflict here comes from "
            "the processor stating \"only\". Compare KGC362 (at least one of "
            "the two, no declarations), which is Compatible."),
        "certificate": {"kind": "Refutation",
            "comment": (
                "Encryption and access control are declared distinct, since "
                "DPV defines each measure separately, so a use supplying "
                "only encryption lacks the second."),
            "premises": [("fromDeclarations",
                          "Encryption distinct from AccessControlMethod")]},
        "provenance": "As KGC362; warrant DPV's definitions.",
        "ttl": _ttl("KGC364", TOM_LO, "both encryption and access control",
                    [("isAllOf", ["Encryption", "AccessControlMethod"])],
                    "encryption as the only measure", [("eq", ["Encryption"])]),
    },
    # -----------------------------------------------------------------
    # KGC365  isAllOf states a minimum: a use with more measures still has
    # the two the controller requires.
    # -----------------------------------------------------------------
    {
        "id": "KGC365", "subdir": "verdict",
        "name": "measures, isAllOf {Encryption, AccessControl} against "
                "isAllOf {Encryption, AccessControl, Pseudonymisation}",
        "left_operand": "TechnicalOrganisationalMeasure", "sort": "tax",
        "resource": RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING, "includes": INCLUDES,
        "tree": [C("isAllOf", ENCRYPTION, ACCESS),
                 C("isAllOf", ENCRYPTION, ACCESS, PSEUDO, side="request")],
        "expected_verdict": "Compatible",
        "expected_q1": "Satisfiable", "expected_q2": "Unsatisfiable",
        "summary": (
            "A controller requires both encryption and access control. A "
            "processor commits to encryption, access control and "
            "pseudonymisation together."),
        "description": (
            "isAllOf states a minimum. The controller needs encryption and "
            "access control among the measures in use and does not exclude "
            "others. A use that also applies pseudonymisation has both "
            "required measures, so it meets both policies and the verdict "
            "is Compatible on the constraints alone."),
        "certificate": {"kind": "Refutation",
            "comment": (
                "isAllOf states a minimum. A use with encryption, access "
                "control and pseudonymisation has the two measures the "
                "first policy requires, so it meets both policies and no "
                "DPV statement or declaration is used. Two minimums never "
                "conflict: a use with both sets of measures meets both."),
            "premises": []},
        "provenance": "Safeguard clauses in data-sharing agreements.",
        "ttl": _ttl("KGC365", TOM_LO, "both encryption and access control",
                    [("isAllOf", ["Encryption", "AccessControlMethod"])],
                    "all of encryption, access control and pseudonymisation",
                    [("isAllOf", ["Encryption", "AccessControlMethod",
                                  "Pseudonymisation"])]),
    },

    # -----------------------------------------------------------------
    # KGC366  isAnyOf matches by name.  Encryption at rest is a kind of
    # encryption and is neither of the two names the controller lists.
    # -----------------------------------------------------------------
    {
        "id": "KGC366", "subdir": "verdict",
        "twin":              "KGC362",
        "name": "measures, isAnyOf {Encryption, AccessControl} against eq "
                "EncryptionAtRest, declared distinct",
        "left_operand": "TechnicalOrganisationalMeasure", "sort": "tax",
        "resource": RESOURCE, "background_theory": DECLARED_BT,
        "binding": BINDING, "includes": INCLUDES_DECLARED,
        "tree": [C("isAnyOf", ENCRYPTION, ACCESS),
                 C("eq", EAR, side="request")],
        "expected_verdict": "Incompatible",
        "expected_q1": "Unsatisfiable", "expected_q2": "Satisfiable",
        "summary": (
            "A controller requires at least one of encryption and access "
            "control. A processor's policy commits to encryption at rest as "
            "the only measure."),
        "description": (
            "isAnyOf asks whether a measure in use is the same as a listed "
            "one; it does not look below the listed measures. DPV places "
            "encryption at rest below encryption, but encryption at rest is "
            "neither encryption nor access control, and the processor's use "
            "has no other measure. Real processors usually list the "
            "measures they apply, and two such lists never conflict "
            "(KGC365); the conflict here comes from the processor stating "
            "\"only\". As published it might be the same measure as one of "
            "the two, and the verdict would be Unknown. With the measures "
            "declared distinct no use meets both policies, and the verdict "
            "is Incompatible. ODRL has no operator for \"includes some kind "
            "of encryption\". Read with KGC362, where the processor's "
            "measure is encryption itself and the verdict is Compatible."),
        "certificate": {"kind": "Refutation",
            "comment": (
                "isAnyOf asks whether a measure in use is the same as a "
                "listed one. DPV places encryption at rest below "
                "encryption, yet it is neither encryption nor access "
                "control. With the measures declared distinct, since DPV "
                "defines each separately, a use whose only measure is "
                "encryption at rest has neither measure the first policy "
                "lists, and no use meets both policies. ODRL has no "
                "operator for \"includes some kind of encryption\". Without "
                "the declarations the verdict would be Unknown."),
            "premises": [("fromDeclarations",
                          "Encryption distinct from EncryptionAtRest"),
                         ("fromDeclarations",
                          "AccessControlMethod distinct from "
                          "EncryptionAtRest")]},
        "provenance": "As KGC362; warrant DPV's definitions.",
        "ttl": _ttl("KGC366", TOM_LO,
                    "at least one of encryption and access control",
                    [("isAnyOf", ["Encryption", "AccessControlMethod"])],
                    "encryption at rest as the only measure",
                    [("eq", ["EncryptionAtRest"])]),
    },

]