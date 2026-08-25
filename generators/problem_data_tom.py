"""
problem_data_tom.py
===================
Two problems over the technical and organisational measures resource, at
tax. They are the only problems in the suite that exercise isAllOf.

    KGC360  isAllOf(encryption, access control) x isA TechnicalMeasure
                                                        -> Compatible
    KGC361  isAllOf(encryption, access control) x isNoneOf(access control)
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
this. Over one value it says what eq says; over two it is false whatever
the vocabulary publishes, since a set of one element cannot contain two.
Neither is worth a problem, which is why the operator went unexercised
until this resource was built.

What the two show
-----------------
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
"""

from compile import Constraint

TOM        = "tm_technical_organisational_measure"
TECHNICAL  = "tm_technical_measure"
ENCRYPTION = "tm_encryption"
ACCESS     = "tm_access_control_method"

RESOURCE = "https://w3id.org/odrl-kb/dpv-tom"
EMPTY_BT = "https://w3id.org/odrl-kb/dpv-tom/empty"

INCLUDES = ["KGE000-0.ax", "DPV-tom.ax"]


def C(op, *vals, side="offer"):
    return Constraint(op, tuple(vals), side)


_TTL_HEAD = """\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix dpv:     <https://w3id.org/dpv#> .
@prefix dpvo:    <https://w3id.org/dpv/mappings/odrl#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .
"""


def _offer(pid):
    return f"""
drk:offer-{pid[3:]} a odrl:Offer ;
    dcterms:title "Use is permitted where encryption and access control are both in place"@en ;
    rdfs:comment "The kind of clause the DPV-ODRL guidance describes for this operand: access to a dataset permitted only where stated measures are implemented. Both are required, not one of them, which is what distinguishes isAllOf from isAnyOf here."@en ;
    odrl:assigner drk:controller ;
    odrl:permission kgc:{pid}-offer-r1 .

kgc:{pid}-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:dataset ;
    odrl:constraint kgc:{pid}-offer-c1 .

kgc:{pid}-offer-c1 a odrl:Constraint ;
    odrl:leftOperand dpvo:TechnicalOrganisationalMeasure ;
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
    odrl:leftOperand dpvo:TechnicalOrganisationalMeasure ;
    odrl:operator odrl:{operator} ;
    odrl:rightOperand {value} .
"""


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
                          "The measures applied are technical measures",
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
                          "Access control is not among the measures applied",
                          "isNoneOf", "( dpv:AccessControlMethod )"),
    },
]