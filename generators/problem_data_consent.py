"""
problem_data_consent.py
=======================
Eight problems over the DPV consent status resource, at tax.  Four compose
constraints under `or` and `xone`, and they were the first in the suite to
do so.

    KGC340  isA Valid                 x eq Given      -> Compatible
    KGC341  or(eq Given, eq Renewed)  x eq Renewed    -> Compatible
    KGC342  isA Valid                 x eq Withdrawn  -> Unknown
    KGC343  the same, branches declared disjoint      -> Incompatible
    KGC344  xone(eq Given, eq Withdrawn) x eq Given   -> Unknown
    KGC345  the same, the two states declared distinct -> Compatible
    KGC346  xone(isA Valid, isA Invalid) x eq Given   -> Unknown
    KGC347  the same, branches declared disjoint      -> Compatible

The policies these express
--------------------------
A controller offers a dataset for use while the consent on record may
justify processing.  DPV publishes the states of consent and divides them
into two branches: states that may justify processing, given and renewed,
and eight that may not.  The offer says which states it accepts.

A request's constraint is the consumer's stated operating condition, not a
report about a record: it says under which consent states the processor
will use the data.  Compatibility asks whether the controller's gate and
that condition can hold of one use.

KGC340 to KGC343 are clauses a controller and a processor write.  KGC344 to
KGC347 are constructions and say so: consent states are exclusive by
nature, so no controller requires exactly one of them; the cases exist to
exercise the negated literal of the xone expansion, which is where counting
alternatives turns on distinctness.

Two ways to say the same thing
------------------------------
KGC340 and KGC341 accept the same two states and reach the same verdict by
different routes.  KGC340 names the branch, `isA
ConsentStatusValidForProcessing`; the verdict rests on an assertion DPV
published, and a state DPV adds to the branch tomorrow is covered without
rewriting.  KGC341 enumerates, `or(eq ConsentGiven, eq RenewedConsentGiven)`;
the verdict rests on the constraints alone, and the offer is fixed against
the vocabulary.  DPV's own scope note says "practically, given consent is
the only valid state for processing", yet publishes RenewedConsentGiven
below the same branch: the enumeration is right today and already one
state behind the file.

Why xone needs a declaration
----------------------------
Expanded, xone(A, B) is (A and not B) or (B and not A).  Take KGC344's
first alternative: the state is given and not withdrawn.  The second
conjunct is a negated equality, and DPV publishes nothing that separates
the two states, so a structure may interpret them as one concept, in which
a record is both and neither alternative holds alone.  Verdict Unknown;
declare the two distinct and it is Compatible.  Exactly-one is a claim
about how many alternatives hold, and counting requires knowing when two
alternatives are the same one.

KGC346 makes the point over the order.  Consent given lies below the valid
branch by assertion; whether it also lies below the invalid branch is not
settled, since a structure may order what the resource leaves unordered.
Declaring the branches disjoint settles it.

The warrant for that disjointness is in DPV's own definitions: one branch
is "states of consent that can be used as valid justifications for
processing data", the other "states of consent that cannot".  That is
disjointness in prose and nowhere in the RDF, so the certificate marks the
premise withdrawable even though the publisher's words warrant it.  What
the definitions warrant, they do not assert.

The background theories
-----------------------
    none           what the module publishes alone (background_theory None)
    definitional   the two branches disjoint, on the module's definitions
    declared       consent given and consent withdrawn declared distinct

KGC342/343, KGC344/345 and KGC346/347 each isolate one theory.

Notes on the encoding
---------------------
Composed offers are given as trees and compiled by expand_tree: expansion,
distribution, and the disjunction of the disjuncts' witness conditions.
The disjunction is inside both queries, not around them.  No xone
alternative is an isAllOf constraint, as the signature requires.

Open
----
consent-definitional.ttl uses bt:PublishedDefinition, bt:assertedByPublisher,
bt:concept, bt:disjointFrom and bt:warrant, none defined by
vocab/background.ttl; define them or stop writing them.  KGC343 and KGC347
disagree between provers because Vampire refutes through the quantified
disjointness pattern the SMT derivation does not inline; the fix is in
tree_expand's assertion parser, not here.
"""
from compile import Constraint, Or, Xone

VALID     = "dpv_consent_status_valid_for_processing"
INVALID   = "dpv_consent_status_invalid_for_processing"
GIVEN     = "dpv_consent_given"
RENEWED   = "dpv_renewed_consent_given"
WITHDRAWN = "dpv_consent_withdrawn"

RESOURCE        = "https://w3id.org/odrl-kb/dpv-consent"
EMPTY_BT        = "https://w3id.org/odrl-kb/dpv-consent/empty"
DEFINITIONAL_BT = "https://w3id.org/odrl-kb/dpv-consent/definitional"
DECLARED_BT     = "https://w3id.org/odrl-kb/dpv-consent/declared"

# Must match the binding node profile-consent.ttl defines for dpv-odrl:Status.
BINDING         = "https://w3id.org/odrl-kb/profile/b-consent-status"

INCLUDES              = ["KGE000-0.ax", "DPV-consent.ax"]
INCLUDES_DEFINITIONAL = INCLUDES + ["DPV-consent-definitional.ax"]
INCLUDES_DECLARED     = INCLUDES + ["DPV-consent-declared.ax"]

PROV_GATE = ("Consent-based processing gate, GDPR Art. 6(1)(a) with "
             "Art. 7(3); consent management platforms enforce it.")
PROV_ENUM = ("As PROV_GATE; enumerating the accepted states is how most "
             "implementations write the gate.")
PROV_POST = ("Processing after withdrawal, the Art. 7(3) against Art. 17 "
             "case; a processor needs a separate legal basis for it.")
PROV_CONS = ("Construction: consent states are exclusive by nature, so the "
             "clause is not written in practice; exercises the xone "
             "expansion's negated literal.")


def C(op, *vals, side="offer"):
    return Constraint(op, tuple(vals), side)

def _disj(*pairs):
    """Declared disjointness: nothing lies below both branches.

    Quantified where _iso's distinctness is ground, so the SMT side
    needs an explicit forall. The name matches what
    DPV-consent-definitional.ax writes, or the two provers would cite
    different names for one premise.
    """
    fof = ["% Background theory: the branches declared disjoint, warranted",
           "% by the module's definitions and asserted by it nowhere.", ""]
    smt = ["; The same disjointness, named as the TPTP side names it."]
    for a, b in pairs:
        n = f"bg_disj_{a}_disjoint_{b}"
        fof.append(f"fof({n}, axiom,\n"
                   f"    ! [X] : ~ ( kge_leq(X, {a}) & kge_leq(X, {b}) )).")
        smt.append(f"(assert (! (forall ((x Concept))\n"
                   f"    (not (and (kge_leq x {a}) (kge_leq x {b}))))\n"
                   f"  :named {n}))")
    return "\n".join(fof) + "\n", "\n".join(smt)


_DISJ = _disj((VALID, INVALID))

_TTL_HEAD = """\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dpv:     <https://w3id.org/dpv#> .
@prefix dpv-odrl:    <https://w3id.org/dpv/mappings/odrl#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .
"""


def _offer_atomic(pid, title, operator, value):
    return f"""
drk:offer-{pid[3:]} a odrl:Set ;
    dcterms:title "{title}"@en ;
    odrl:assigner drk:controller ;
    odrl:permission kgc:{pid}-offer-r1 .
kgc:{pid}-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:dataset ;
    odrl:constraint kgc:{pid}-offer-c1 .
kgc:{pid}-offer-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:Status ;
    odrl:operator odrl:{operator} ;
    odrl:rightOperand dpv:{value} .
"""


def _offer_logical(pid, title, connective, alts):
    """A Logical Constraint whose operands are atomic constraints, as ODRL
    2.2 serialises it: an rdf:List of constraint IRIs under the connective."""
    refs = " ".join(f"kgc:{pid}-offer-a{i}" for i in range(1, len(alts) + 1))
    body = f"""
drk:offer-{pid[3:]} a odrl:Set ;
    dcterms:title "{title}"@en ;
    odrl:assigner drk:controller ;
    odrl:permission kgc:{pid}-offer-r1 .
kgc:{pid}-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:dataset ;
    odrl:constraint kgc:{pid}-offer-c1 .
kgc:{pid}-offer-c1 a odrl:LogicalConstraint ;
    odrl:{connective} ( {refs} ) .
"""
    for i, (op, val) in enumerate(alts, start=1):
        body += f"""
kgc:{pid}-offer-a{i} a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:Status ;
    odrl:operator odrl:{op} ;
    odrl:rightOperand dpv:{val} .
"""
    return body


def _request(pid, title, value):
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
    odrl:leftOperand dpv-odrl:Status ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:{value} .
"""


OFFER_GATE = "Use is permitted while the consent on record may justify processing"
OFFER_ENUM = "Use is permitted under given or renewed consent"
OFFER_XONE_STATES = ("Use is permitted while the record is in exactly one of "
                     "the given and withdrawn states")
OFFER_XONE_BRANCH = ("Use is permitted while the record falls under exactly "
                     "one of the two consent branches")
REQ_GIVEN   = "Processing only under given consent"
REQ_RENEWED = "Processing only under renewed consent"
REQ_POST    = "Processing continues after consent is withdrawn"

PROBLEMS = [
    # ------------------------------------------------------------------
    # KGC340  The constraint the resource exists for.
    # ------------------------------------------------------------------
    {
        "id": "KGC340", "subdir": "verdict",
        "name": "consent status, isA ValidForProcessing against eq ConsentGiven",
        "left_operand": "Status", "sort": "tax",
        "resource": RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING, "includes": INCLUDES,
        "tree": [C("isA", VALID), C("eq", GIVEN, side="request")],
        "expected_verdict": "Compatible",
        "expected_q1": "Satisfiable", "expected_q2": "Unsatisfiable",
        "summary": (
            "A controller permits use while the consent on record may justify "
            "processing; a processor commits to processing only under given "
            "consent."),
        "description": (
            "DPV places consent given below the branch of states valid for "
            "processing, so the verdict is Compatible on one published "
            "assertion. The offer names the branch rather than the states, so "
            "a state DPV adds to that branch later is covered without the "
            "offer being rewritten."),
        "certificate": {"kind": "Refutation",
            "comment": "DPV places consent given among the states valid for "
                       "processing, so both sides can be satisfied.",
            "premises": [("fromResource",
                          "dpv:ConsentGiven is below "
                          "dpv:ConsentStatusValidForProcessing")]},
        "provenance": PROV_GATE,
        "ttl": _TTL_HEAD
               + _offer_atomic("KGC340", OFFER_GATE, "isA",
                               "ConsentStatusValidForProcessing")
               + _request("KGC340", REQ_GIVEN, "ConsentGiven"),
    },
    # ------------------------------------------------------------------
    # KGC341  The same gate, enumerated instead of named.
    # ------------------------------------------------------------------
    {
        "id": "KGC341", "subdir": "verdict",
        "name": "consent status, or(eq ConsentGiven, eq RenewedConsentGiven) "
                "against eq RenewedConsentGiven",
        "left_operand": "Status", "sort": "tax",
        "resource": RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING, "includes": INCLUDES,
        "tree": [Or((C("eq", GIVEN), C("eq", RENEWED))),
                 C("eq", RENEWED, side="request")],
        "expected_verdict": "Compatible",
        "expected_q1": "Satisfiable", "expected_q2": "Unsatisfiable",
        "summary": (
            "A controller permits use under given or renewed consent; a "
            "processor commits to processing only under renewed consent."),
        "description": (
            "The same gate as KGC340, written by enumerating the two states "
            "rather than naming the branch. Compatible again, and the "
            "certificate cites no resource assertion: the requested state is "
            "one the offer names. The offer is fixed against the vocabulary as "
            "it stands, where KGC340's is not."),
        "certificate": {"kind": "Refutation",
            "comment": "The requested state is one the offer names, so the "
                       "constraints settle the verdict without the resource.",
            "premises": []},
        "provenance": PROV_ENUM,
        "ttl": _TTL_HEAD
               + _offer_logical("KGC341", OFFER_ENUM, "or",
                                [("eq", "ConsentGiven"),
                                 ("eq", "RenewedConsentGiven")])
               + _request("KGC341", REQ_RENEWED, "RenewedConsentGiven"),
    },
    # ------------------------------------------------------------------
    # KGC342 / KGC343  The branches, undeclared and declared disjoint.
    # The request keeps odrl:use: it says processing continues after
    # withdrawal, not that a different action is taken.
    # ------------------------------------------------------------------
    {
        "id": "KGC342", "subdir": "verdict",
        "name": "consent status, isA ValidForProcessing against eq "
                "ConsentWithdrawn",
        "left_operand": "Status", "sort": "tax",
        "resource": RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING, "includes": INCLUDES,
        "tree": [C("isA", VALID), C("eq", WITHDRAWN, side="request")],
        "expected_verdict": "Unknown", "unknown_reason": "epistemic",
        "expected_q1": "Satisfiable", "expected_q2": "Satisfiable",
        "summary": (
            "A controller permits use only while consent may justify "
            "processing; a processor states that its processing continues "
            "after consent is withdrawn."),
        "description": (
            "DPV places consent withdrawn below the invalid branch and asserts "
            "nothing that keeps the two branches apart, so a structure may "
            "place the withdrawn state below both. Unknown is the right "
            "answer to what the module publishes, even though its definitions "
            "read otherwise."),
        "certificate": {"kind": "Models",
            "comment": "Nothing published keeps the withdrawn state out of the "
                       "valid branch, so one structure admits the use and one "
                       "does not.",
            "premises": []},
        "provenance": PROV_POST,
        "ttl": _TTL_HEAD
               + _offer_atomic("KGC342", OFFER_GATE, "isA",
                               "ConsentStatusValidForProcessing")
               + _request("KGC342", REQ_POST, "ConsentWithdrawn"),
    },
    {
        "id": "KGC343", "subdir": "verdict",
        "name": "consent status, isA ValidForProcessing against eq "
                "ConsentWithdrawn, branches disjoint",
        "left_operand": "Status", "sort": "tax",
        "resource": RESOURCE, "background_theory": DEFINITIONAL_BT,
                "fof_decls": _DISJ[0],
        "smt2_background": _DISJ[1],
        "extra_constants": [INVALID],
        "binding": BINDING, "includes": INCLUDES_DEFINITIONAL,
        "tree": [C("isA", VALID), C("eq", WITHDRAWN, side="request")],
                "fof_decls": _DISJ[0],
        "smt2_background": _DISJ[1],
        "expected_verdict": "Incompatible",
        "expected_q1": "Unsatisfiable", "expected_q2": "Satisfiable",
        "summary": (
            "As KGC342, with the valid and invalid branches declared "
            "disjoint on DPV's definitions."),
        "description": (
            "Nothing then lies below both branches; the withdrawn state lies "
            "below the invalid one and so not below the valid one: "
            "Incompatible. The controller's gate and the processor's practice "
            "cannot hold of one use, which is the Art. 7(3) against Art. 17 "
            "case where a separate legal basis would be needed. The "
            "declaration is warranted by the module's definitions and "
            "asserted by it nowhere, so the certificate marks it "
            "withdrawable."),
        "certificate": {"kind": "Refutation",
            "comment": "The withdrawn state lies below the invalid branch, and "
                       "the branches are declared to have nothing below both. "
                       "The declaration follows DPV's definitions but is not "
                       "asserted by DPV; withdrawing it reopens the verdict.",
            "premises": [("fromResource",
                          "dpv:ConsentWithdrawn is below "
                          "dpv:ConsentStatusInvalidForProcessing"),
                         ("fromBackgroundTheory",
                          "the two branches have nothing below both")]},
        "provenance": PROV_POST,
        "ttl": _TTL_HEAD
               + _offer_atomic("KGC343", OFFER_GATE, "isA",
                               "ConsentStatusValidForProcessing")
               + _request("KGC343", REQ_POST, "ConsentWithdrawn"),
    },
    # ------------------------------------------------------------------
    # KGC344 / KGC345  xone over identity: counting needs distinctness.
    # Constructions.
    # ------------------------------------------------------------------
    {
        "id": "KGC344", "subdir": "verdict",
        "name": "consent status, xone(eq ConsentGiven, eq ConsentWithdrawn) "
                "against eq ConsentGiven",
        "left_operand": "Status", "sort": "tax",
        "resource": RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING, "includes": INCLUDES,
        "tree": [Xone((C("eq", GIVEN), C("eq", WITHDRAWN))),
                 C("eq", GIVEN, side="request")],
        "expected_verdict": "Unknown", "unknown_reason": "epistemic",
        "expected_q1": "Satisfiable", "expected_q2": "Satisfiable",
        "summary": (
            "An offer requires the record to be in exactly one of the given "
            "and withdrawn states; a processor commits to processing only "
            "under given consent."),
        "description": (
            "Expanded, the live alternative is given and not withdrawn. DPV "
            "publishes nothing that separates the two states, so a structure "
            "may interpret them as one, in which the record is both and "
            "neither alternative holds alone: Unknown. Counting alternatives "
            "requires knowing when two of them are the same.\n\n"
            "A construction. Consent states are exclusive by nature, so no "
            "controller writes this clause; the case exists to exercise the "
            "negated literal of the xone expansion."),
        "certificate": {"kind": "Models",
            "comment": "One structure makes the given and withdrawn states one "
                       "concept, and exactly-one then fails; nothing published "
                       "forbids it.",
            "premises": []},
        "provenance": PROV_CONS,
        "ttl": _TTL_HEAD
               + _offer_logical("KGC344", OFFER_XONE_STATES, "xone",
                                [("eq", "ConsentGiven"),
                                 ("eq", "ConsentWithdrawn")])
               + _request("KGC344", REQ_GIVEN, "ConsentGiven"),
    },
    {
        "id": "KGC345", "subdir": "verdict",
        "name": "consent status, xone(eq ConsentGiven, eq ConsentWithdrawn) "
                "against eq ConsentGiven, the two states declared distinct",
        "left_operand": "Status", "sort": "tax",
        "resource": RESOURCE, "background_theory": DECLARED_BT,
        "binding": BINDING, "includes": INCLUDES_DECLARED,
        "tree": [Xone((C("eq", GIVEN), C("eq", WITHDRAWN))),
                 C("eq", GIVEN, side="request")],
        "expected_verdict": "Compatible",
        "expected_q1": "Satisfiable", "expected_q2": "Unsatisfiable",
        "summary": (
            "As KGC344, with the given and withdrawn states declared "
            "distinct."),
        "description": (
            "Every structure then separates the two states, the first "
            "alternative holds and the second does not: Compatible. The "
            "declaration is what makes the exclusive requirement decidable; "
            "with it the offer means what it appears to mean, without it the "
            "same offer is open. A construction, as KGC344."),
        "certificate": {"kind": "Refutation",
            "comment": "The two states are declared distinct, so exactly one "
                       "alternative holds of a record in the given state. The "
                       "premise is the parties'; withdrawing it returns the "
                       "verdict to Unknown.",
            "premises": [("fromBackgroundTheory",
                          "dpv:ConsentGiven and dpv:ConsentWithdrawn are "
                          "distinct")]},
        "provenance": PROV_CONS,
        "ttl": _TTL_HEAD
               + _offer_logical("KGC345", OFFER_XONE_STATES, "xone",
                                [("eq", "ConsentGiven"),
                                 ("eq", "ConsentWithdrawn")])
               + _request("KGC345", REQ_GIVEN, "ConsentGiven"),
    },
    # ------------------------------------------------------------------
    # KGC346 / KGC347  xone over the order.  Constructions.
    # ------------------------------------------------------------------
    {
        "id": "KGC346", "subdir": "verdict",
        "name": "consent status, xone(isA ValidForProcessing, isA "
                "InvalidForProcessing) against eq ConsentGiven",
        "left_operand": "Status", "sort": "tax",
        "resource": RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING, "includes": INCLUDES,
        "tree": [Xone((C("isA", VALID), C("isA", INVALID))),
                 C("eq", GIVEN, side="request")],
        "expected_verdict": "Unknown", "unknown_reason": "epistemic",
        "expected_q1": "Satisfiable", "expected_q2": "Satisfiable",
        "summary": (
            "An offer requires the record to fall under exactly one of the "
            "two consent branches; a processor commits to processing only "
            "under given consent."),
        "description": (
            "Consent given lies below the valid branch by assertion; whether "
            "it also lies below the invalid branch is not settled, since a "
            "structure may order what the resource leaves unordered. Both "
            "alternatives would then hold and exactly-one fails: Unknown. A "
            "construction, as KGC344, over the order rather than identity."),
        "certificate": {"kind": "Models",
            "comment": "One structure places the given state below both "
                       "branches; DPV does not rule it out.",
            "premises": []},
        "provenance": PROV_CONS,
        "ttl": _TTL_HEAD
               + _offer_logical("KGC346", OFFER_XONE_BRANCH, "xone",
                                [("isA", "ConsentStatusValidForProcessing"),
                                 ("isA", "ConsentStatusInvalidForProcessing")])
               + _request("KGC346", REQ_GIVEN, "ConsentGiven"),
    },
    {
        "id": "KGC347", "subdir": "verdict",
        "name": "consent status, xone(isA ValidForProcessing, isA "
                "InvalidForProcessing) against eq ConsentGiven, branches "
                "disjoint",
        "left_operand": "Status", "sort": "tax",
           "fof_decls": _DISJ[0],
        "smt2_background": _DISJ[1],
                        "extra_constants": [INVALID],
        "resource": RESOURCE, "background_theory": DEFINITIONAL_BT,
        "binding": BINDING, "includes": INCLUDES_DEFINITIONAL,
        "tree": [Xone((C("isA", VALID), C("isA", INVALID))),
                 C("eq", GIVEN, side="request")],
        "expected_verdict": "Compatible",
        "expected_q1": "Satisfiable", "expected_q2": "Unsatisfiable",
        "summary": (
            "As KGC346, with the valid and invalid branches declared "
            "disjoint on DPV's definitions."),
        "description": (
            "Nothing lies below both, so the given state lies below the valid "
            "branch alone, exactly one alternative holds, and the verdict is "
            "Compatible. The refutation cites an assertion DPV published and "
            "a declaration the parties made, and the certificate marks which "
            "is which. A construction, as KGC344."),
        "certificate": {"kind": "Refutation",
            "comment": "The given state lies below the valid branch, and the "
                       "branches are declared to have nothing below both, so "
                       "it lies below that branch alone.",
            "premises": [("fromResource",
                          "dpv:ConsentGiven is below "
                          "dpv:ConsentStatusValidForProcessing"),
                         ("fromBackgroundTheory",
                          "the two branches have nothing below both")]},
        "provenance": PROV_CONS,
        "ttl": _TTL_HEAD
               + _offer_logical("KGC347", OFFER_XONE_BRANCH, "xone",
                                [("isA", "ConsentStatusValidForProcessing"),
                                 ("isA", "ConsentStatusInvalidForProcessing")])
               + _request("KGC347", REQ_GIVEN, "ConsentGiven"),
    },
]