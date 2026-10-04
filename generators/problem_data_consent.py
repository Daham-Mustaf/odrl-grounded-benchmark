"""
problem_data_consent.py
=======================
Four problems over the DPV consent status resource, at tax.  One composes
constraints under `or`.

    KGC340  isA Valid                 x eq Given      -> Compatible
    KGC341  or(eq Given, eq Renewed)  x eq Renewed    -> Compatible
    KGC342  isA Valid                 x eq Withdrawn  -> Unknown
    KGC343  the same, branches declared disjoint      -> Incompatible

The four xone problems that were here (KGC344 to KGC347) permitted use
under an invalid consent state, which no lawful policy does.  The xone
tests moved to the GeoNames problems KGC303 to KGC306, where "exactly one
region" is a clause someone writes.

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

KGC340 to KGC343 are clauses a controller and a processor write.

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

KGC342 and KGC343 turn on one disjointness.  Its warrant is in DPV's own definitions: one branch
is "states of consent that can be used as valid justifications for
processing data", the other "states of consent that cannot".  That is
disjointness in prose and nowhere in the RDF, so the certificate marks the
premise withdrawable even though the publisher's words warrant it.  What
the definitions warrant, they do not assert.

The background theories
-----------------------
    empty          what the module publishes alone
    definitional   the two branches disjoint, on the module's definitions

KGC342/343 isolate the definitional theory.

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
vocab/background.ttl; define them or stop writing them.  KGC343 can
disagree between provers because Vampire refutes through the quantified
disjointness pattern the SMT derivation does not inline; the fix is in
tree_expand's assertion parser, not here.
"""
from compile import Constraint, Or

VALID     = "dpv_consent_status_valid_for_processing"
INVALID   = "dpv_consent_status_invalid_for_processing"
GIVEN     = "dpv_consent_given"
RENEWED   = "dpv_renewed_consent_given"
WITHDRAWN = "dpv_consent_withdrawn"

RESOURCE        = "https://w3id.org/odrl-kb/dpv-consent"
EMPTY_BT        = "https://w3id.org/odrl-kb/dpv-consent/empty"
DEFINITIONAL_BT = "https://w3id.org/odrl-kb/dpv-consent/definitional"

# Must match the binding node profile-consent.ttl defines for dpv-odrl:Status.
BINDING         = "https://w3id.org/odrl-kb/profile/b-consent-status"

INCLUDES              = ["KGE000-0.ax", "DPV-consent.ax"]
INCLUDES_DEFINITIONAL = INCLUDES + ["DPV-consent-definitional.ax"]

PROV_GATE = ("Consent-based processing gate, GDPR Art. 6(1)(a) with "
             "Art. 7(3); consent management platforms enforce it.")
PROV_ENUM = ("As PROV_GATE; enumerating the accepted states is how most "
             "implementations write the gate.")
PROV_POST = ("Processing after withdrawal, the Art. 7(3) against Art. 17 "
             "case; a processor needs a separate legal basis for it.")


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
drk:policy-{pid[3:]}-1 a odrl:Set ;
    odrl:uid drk:policy-{pid[3:]}-1 ;
    odrl:profile dpv-odrl: ;
    dcterms:title "{title}"@en ;
    odrl:assigner drk:controller ;
    odrl:permission kgc:{pid}-p1-r1 .
kgc:{pid}-p1-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:dataset ;
    odrl:constraint kgc:{pid}-p1-c1 .
kgc:{pid}-p1-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:Status ;
    odrl:operator odrl:{operator} ;
    odrl:rightOperand dpv:{value} .
"""


def _offer_logical(pid, title, connective, alts):
    """A Logical Constraint whose operands are atomic constraints, as ODRL
    2.2 serialises it: an rdf:List of constraint IRIs under the connective."""
    refs = " ".join(f"kgc:{pid}-p1-a{i}" for i in range(1, len(alts) + 1))
    body = f"""
drk:policy-{pid[3:]}-1 a odrl:Set ;
    odrl:uid drk:policy-{pid[3:]}-1 ;
    odrl:profile dpv-odrl: ;
    dcterms:title "{title}"@en ;
    odrl:assigner drk:controller ;
    odrl:permission kgc:{pid}-p1-r1 .
kgc:{pid}-p1-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:dataset ;
    odrl:constraint kgc:{pid}-p1-c1 .
kgc:{pid}-p1-c1 a odrl:LogicalConstraint ;
    odrl:{connective} ( {refs} ) .
"""
    for i, (op, val) in enumerate(alts, start=1):
        body += f"""
kgc:{pid}-p1-a{i} a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:Status ;
    odrl:operator odrl:{op} ;
    odrl:rightOperand dpv:{val} .
"""
    return body


def _request(pid, title, value):
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
    odrl:leftOperand dpv-odrl:Status ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:{value} .
"""


OFFER_GATE = "Use is permitted while the consent on record may justify processing"
OFFER_ENUM = "Use is permitted under given or renewed consent"
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
            "A controller permits use under given or renewed consent. A "
            "processor's policy commits to processing only under renewed "
            "consent."),
        "description": (
            "The same gate as KGC340, written by enumerating the two states "
            "rather than naming the branch. Compatible again, and the "
            "certificate cites no resource assertion: the requested state is "
            "one the offer names. The offer is fixed against the vocabulary as "
            "it stands, where KGC340's is not."),
        "certificate": {"kind": "Refutation",
            "comment": (
                "The required state is one the first policy names, so the "
                "constraints settle the verdict without the resource."),
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
         "twin": "KGC343",
        "name": "consent status, isA ValidForProcessing against eq "
                "ConsentWithdrawn",
        "left_operand": "Status", "sort": "tax",
        "resource": RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING, "includes": INCLUDES,
        "tree": [C("isA", VALID), C("eq", WITHDRAWN, side="request")],
        "expected_verdict": "Unknown", "unknown_reason": "epistemic",
        "expected_q1": "Satisfiable", "expected_q2": "Satisfiable",
        "summary": (
            "A controller permits use only while consent can justify "
            "processing. A processor states that it continues processing "
            "after consent is withdrawn."),
  "description": (
            "DPV places the withdrawn state below the invalid branch. It "
            "does not state in RDF that the valid and invalid branches are "
            "disjoint. So one structure that satisfies the published "
            "assertions also places the withdrawn state below the valid "
            "branch, and another does not. The verdict is therefore Unknown. "
            "KGC343 adds the disjointness as a background theory."),
        "certificate": {"kind": "Models",
            "comment": (
                "The published assertions do not exclude the withdrawn "
                "state from the valid branch. One structure places it below "
                "both branches, and both constraints can hold. Another does "
                "not, and they cannot."),
            "premises": []},
        "provenance": PROV_POST,
        "ttl": _TTL_HEAD
               + _offer_atomic("KGC342", OFFER_GATE, "isA",
                               "ConsentStatusValidForProcessing")
               + _request("KGC342", REQ_POST, "ConsentWithdrawn"),
    },
    {
        "id": "KGC343", "subdir": "verdict",
        "twin": "KGC342",
        "name": "consent status, isA ValidForProcessing against eq "
                "ConsentWithdrawn, branches disjoint",
        "left_operand": "Status", "sort": "tax",
        "resource": RESOURCE, "background_theory": DEFINITIONAL_BT,
        "binding": BINDING, "includes": INCLUDES_DEFINITIONAL,
        "fof_decls": _DISJ[0],
        "smt2_background": _DISJ[1],
        "extra_constants": [INVALID],
        "tree": [C("isA", VALID), C("eq", WITHDRAWN, side="request")],
        "expected_verdict": "Incompatible",
        "expected_q1": "Unsatisfiable", "expected_q2": "Satisfiable",
        "summary": (
            "As KGC342, with the valid and invalid branches declared "
            "disjoint by the background theory."),
 "description": (
            "The background theory declares the valid and invalid branches "
            "disjoint, meaning that nothing lies below both. The withdrawn "
            "state lies below the invalid branch, so it cannot also lie "
            "below the valid branch. No use satisfies both policies, and the "
            "verdict is Incompatible. DPV's definitions support the "
            "disjointness, but the DPV RDF does not assert it."),
"certificate": {"kind": "Refutation",
    "comment": (
                "ConsentWithdrawn lies below the invalid branch, and the "
                "background theory declares the two branches disjoint. So it "
                "cannot also lie below the valid branch. Without that "
                "background theory the verdict is Unknown, as in KGC342."),
            "premises": [
                ("fromResource",
                 "dpv:ConsentWithdrawn is below "
                 "dpv:ConsentStatusInvalidForProcessing"),
                ("fromBackgroundTheory",
                 "dpv:ConsentStatusValidForProcessing and "
                 "dpv:ConsentStatusInvalidForProcessing are disjoint")]},
        "provenance": PROV_POST,
        "ttl": _TTL_HEAD
               + _offer_atomic("KGC343", OFFER_GATE, "isA",
                               "ConsentStatusValidForProcessing")
               + _request("KGC343", REQ_POST, "ConsentWithdrawn"),
    },
]