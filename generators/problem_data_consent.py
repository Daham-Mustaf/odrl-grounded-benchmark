"""
problem_data_consent.py
=======================
Six problems over the DPV consent status resource, at tax.  One composes
constraints under `or`.

    KGC340  isA Valid                 x eq Given      -> Compatible
    KGC341  or(eq Given, eq Renewed)  x eq Renewed    -> Compatible
    KGC342  isA Valid                 x eq Withdrawn  -> Unknown
    KGC343  the same, branches declared disjoint      -> Incompatible
    KGC348  the same, every state declared distinct   -> Unknown
    KGC349  isNoneOf {Withdrawn, Revoked} x eq Expired,
            every state declared distinct             -> Compatible

The four xone problems that were here (KGC344 to KGC347) permitted use
under an invalid consent state, which no lawful policy does.  The xone
tests moved to the GeoNames problems KGC303 and KGC304, where "exactly one
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
ConsentStatusValidForProcessing`; the verdict rests on a statement DPV
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

Distinctness is not disjointness
--------------------------------
KGC348 is KGC342 under declarations that separate every state from every
other.  The withdrawn state is then a different concept from the valid
branch, and it may still lie below it: one concept below another is not the
same concept, so distinctness never decides isA.  Only disjointness does,
which is the declaration of KGC343.  KGC349 is the other side of the same
point.  An exclusion list works by identity, so declaring expired consent
distinct from withdrawn and revoked consent lets it through, where a policy
written over the valid branch would refuse it once the branches are declared
disjoint.

The declarations
-----------------------
    empty          what the module publishes alone
    definitional   the two branches disjoint, on the module's definitions
    declared       every state distinct from every other, on the module's
                   separate definition of each

KGC342/343 isolate the definitional declarations.

Notes on the encoding
---------------------
Composed offers are given as trees and compiled by expand_tree: expansion,
distribution, and the disjunction of the disjuncts' witness conditions.
The disjunction is inside both queries, not around them.  No xone
alternative is an isAllOf constraint, as the signature requires.
"""
from compile import Constraint, Or, right_operand as _ro



VALID     = "dpv_consent_status_valid_for_processing"
INVALID   = "dpv_consent_status_invalid_for_processing"
GIVEN     = "dpv_consent_given"
RENEWED   = "dpv_renewed_consent_given"
WITHDRAWN = "dpv_consent_withdrawn"
EXPIRED   = "dpv_consent_expired"
REVOKED   = "dpv_consent_revoked"

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


def C(op, *vals, side="offer"):
    return Constraint(op, tuple(vals), side)


_TTL_HEAD = """\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dpv:     <https://w3id.org/dpv#> .
@prefix dpv-odrl:    <https://w3id.org/dpv/mappings/odrl#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .
"""


def _offer_atomic(pid, title, operator, value):
    # A set operator takes a list, one value or several; the others take one.
    if isinstance(value, (list, tuple)):
        right = _ro(operator, [f"dpv:{v}" for v in value])
    else:
        right = f"dpv:{value}"
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
    odrl:rightOperand {right} .
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


OFFER_GATE = "Use only while the consent on record may justify processing"
OFFER_ENUM = "Use only under given or renewed consent"
REQ_GIVEN   = "Use only under given consent"
REQ_RENEWED = "Use only under renewed consent"
REQ_POST    = "Use only records whose consent was withdrawn"
OFFER_EXCEPT = "Use under any consent status except withdrawn and revoked"
REQ_EXPIRED  = "Use only records whose consent has expired"

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
            "statement. The first policy names the branch rather than the states, so "
            "a state DPV adds to that branch later is covered without the "
            "policy being rewritten."),
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
            "The controller lists the two valid states instead of naming "
            "the branch. A use under renewed consent meets the second "
            "alternative, so the verdict is Compatible without any DPV "
            "statement. The list is narrower than KGC340's branch in two "
            "ways: it does not cover a valid state that DPV adds later, and "
            "a dataset that mixes given and renewed consent meets neither "
            "alternative, because each requires every record to have the "
            "same state."),
        "certificate": {"kind": "Refutation",
            "comment": (
                "The required state is one the first policy names, so the "
                "constraints decide the verdict without any DPV statement."),
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
         "twin": ["KGC343", "KGC348"],
        "name": "consent status, isA ValidForProcessing against eq "
                "ConsentWithdrawn",
        "left_operand": "Status", "sort": "tax",
        "resource": RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING, "includes": INCLUDES,
        "tree": [C("isA", VALID), C("eq", WITHDRAWN, side="request")],
        "expected_verdict": "Unknown",
        "expected_q1": "Satisfiable", "expected_q2": "Satisfiable",
        "summary": (
            "A controller permits use only while the consent on record may "
            "justify processing. A processor commits to use only records "
            "whose consent was withdrawn, in an erasure audit for the "
            "controller."),
  "description": (
      "The processor audits erasure, so it looks only at records whose "
      "consent was withdrawn. DPV places the withdrawn state below the "
      "invalid branch. DPV does not state that the valid and invalid "
      "branches are disjoint. If withdrawn consent also lies below the "
      "valid branch, a use meets both policies; if it does not, none does. "
      "The verdict is therefore Unknown. KGC343 adds the disjointness as a "
      "declaration."),
        "certificate": {"kind": "Models",
            "comment": (
                "DPV places the withdrawn state below the invalid branch, "
                "which it defines as the states that cannot justify "
                "processing, but does not state that the valid and invalid "
                "branches are disjoint. If withdrawn consent also lies "
                "below the valid branch, a use meets both policies; if it "
                "does not, no use does. So the verdict is Unknown."),
            "premises": []},
        "provenance": PROV_POST,
        "ttl": _TTL_HEAD
               + _offer_atomic("KGC342", OFFER_GATE, "isA",
                               "ConsentStatusValidForProcessing")
               + _request("KGC342", REQ_POST, "ConsentWithdrawn"),
    },
    {
        "id": "KGC343", "subdir": "verdict",
        "twin": ["KGC342", "KGC348"],
        "name": "consent status, isA ValidForProcessing against eq "
                "ConsentWithdrawn, branches disjoint",
        "left_operand": "Status", "sort": "tax",
        "resource": RESOURCE, "background_theory": DEFINITIONAL_BT,
        "binding": BINDING, "includes": INCLUDES_DEFINITIONAL,
        "tree": [C("isA", VALID), C("eq", WITHDRAWN, side="request")],
        "expected_verdict": "Incompatible",
        "expected_q1": "Unsatisfiable", "expected_q2": "Satisfiable",
        "summary": (
            "As KGC342, with the valid and invalid branches declared "
            "disjoint."),
 "description": (
     "The declarations make the valid and invalid branches disjoint, "
     "meaning that nothing lies below both. The withdrawn state lies below "
     "the invalid branch, so it cannot also lie below the valid branch. No "
     "use satisfies both policies, and the verdict is Incompatible. DPV's "
     "definitions support the disjointness, but DPV does not state it."),
"certificate": {"kind": "Refutation",
    "comment": (
        "DPV places withdrawn consent below the invalid branch, and the "
        "declarations state that the valid and invalid branches are "
        "disjoint, which DPV's definitions imply: states that can justify "
        "processing and states that cannot. So withdrawn consent cannot "
        "also lie below the valid branch. Without those declarations the "
        "verdict is Unknown, as in KGC342."),
            "premises": [
                ("fromResource",
                 "dpv:ConsentWithdrawn is below "
                 "dpv:ConsentStatusInvalidForProcessing"),
                ("fromDeclarations",
                 "dpv:ConsentStatusValidForProcessing and "
                 "dpv:ConsentStatusInvalidForProcessing are disjoint")]},
        "provenance": PROV_POST,
        "ttl": _TTL_HEAD
               + _offer_atomic("KGC343", OFFER_GATE, "isA",
                               "ConsentStatusValidForProcessing")
               + _request("KGC343", REQ_POST, "ConsentWithdrawn"),
    },
    # -----------------------------------------------------------------
    # KGC348  KGC342 under declarations that separate every state.  The
    # withdrawn state is a different concept from the valid branch and may
    # still lie below it: distinctness never decides isA.
    # -----------------------------------------------------------------
    {
        "id": "KGC348", "subdir": "verdict",
        "twin": ["KGC342", "KGC343"],
        "name": "consent status, isA ValidForProcessing against eq "
                "ConsentWithdrawn, states declared distinct",
        "left_operand": "Status", "sort": "tax",
        "resource": RESOURCE, "background_theory": DECLARED_BT,
        "binding": BINDING, "includes": INCLUDES_DECLARED,
        "tree": [C("isA", VALID), C("eq", WITHDRAWN, side="request")],
        "expected_verdict": "Unknown",
        "expected_q1": "Satisfiable", "expected_q2": "Satisfiable",
        "summary": (
            "As KGC342, with the consent states declared distinct from one "
            "another."),
        "description": (
            "KGC342 with every consent state declared distinct from every "
            "other, since DPV defines each separately. Distinctness only "
            "means that withdrawn consent is not the valid branch itself; "
            "it does not stop withdrawn consent from lying below that "
            "branch. Only the disjointness of KGC343 does. The verdict "
            "stays Unknown."),
        "certificate": {"kind": "Models",
            "comment": (
                "The states are declared distinct, since DPV defines each "
                "separately. Distinctness only means that withdrawn consent "
                "is not the valid branch itself; it does not stop withdrawn "
                "consent from lying below that branch. If it does, a use "
                "meets both policies; if it does not, no use does. Only the "
                "disjointness of KGC343 rules it out."),
            "premises": []},
        "provenance": PROV_POST,
        "ttl": _TTL_HEAD
               + _offer_atomic("KGC348", OFFER_GATE, "isA",
                               "ConsentStatusValidForProcessing")
               + _request("KGC348", REQ_POST, "ConsentWithdrawn"),
    },

    # -----------------------------------------------------------------
    # KGC349  An exclusion list works by identity.  Expired consent is
    # declared different from the two states the list names, so it passes,
    # where a policy over the valid branch would refuse it.
    # -----------------------------------------------------------------
    {
        "id": "KGC349", "subdir": "verdict",
        "name": "consent status, isNoneOf {ConsentWithdrawn, "
                "ConsentRevoked} against eq ConsentExpired, states "
                "declared distinct",
        "left_operand": "Status", "sort": "tax",
        "resource": RESOURCE, "background_theory": DECLARED_BT,
        "binding": BINDING, "includes": INCLUDES_DECLARED,
        "tree": [C("isNoneOf", WITHDRAWN, REVOKED),
                 C("eq", EXPIRED, side="request")],
        "expected_verdict": "Compatible",
        "expected_q1": "Satisfiable", "expected_q2": "Unsatisfiable",
        "summary": (
            "A controller permits use under any consent status except "
            "withdrawn and revoked. A processor commits to use only records "
            "whose consent has expired, in a consent-renewal campaign."),
        "description": (
            "The controller's list is a drafting error: it also lets "
            "through refused, deferred, invalidated and unknown consent, "
            "and consent that is only asked for, which no controller means "
            "to permit. isNoneOf excludes the named states by identity. "
            "Expired consent is declared a different state from withdrawn "
            "and from revoked consent, so the list lets it through and the "
            "verdict is Compatible. A policy written over the valid branch "
            "(isA, as in KGC343) would have refused it once the branches "
            "are declared disjoint, because expired consent lies below the "
            "invalid branch. The processor runs the renewal campaign and "
            "contacts only people whose consent has expired."),
        "certificate": {"kind": "Refutation",
            "comment": (
                "Expired consent is declared distinct from withdrawn and "
                "from revoked consent, since DPV defines each state "
                "separately, so the exclusion list does not exclude it."),
            "premises": [("fromDeclarations",
                          "dpv:ConsentExpired distinct from "
                          "dpv:ConsentWithdrawn"),
                         ("fromDeclarations",
                          "dpv:ConsentExpired distinct from "
                          "dpv:ConsentRevoked")]},
        "provenance": ("Consent-status exclusion lists in processing "
                       "agreements."),
        "ttl": _TTL_HEAD
               + _offer_atomic("KGC349", OFFER_EXCEPT, "isNoneOf",
                               ["ConsentWithdrawn", "ConsentRevoked"])
               + _request("KGC349", REQ_EXPIRED, "ConsentExpired"),
    },

]