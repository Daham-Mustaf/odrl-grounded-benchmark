"""
problem_data_consent.py
=======================
Seven problems over the DPV consent status resource, at tax.  Four of them
compose constraints under `or` and `xone`, and they are the first in the
suite to do so.

    KGC340  isA Valid            x eq ConsentGiven     -> Compatible
    KGC341  or(eq Given, eq Renewed) x eq Renewed      -> Compatible
    KGC342  isA Valid            x eq ConsentWithdrawn -> Unknown
    KGC343  the same pair, branches declared disjoint  -> Incompatible
    KGC344  xone(eq Given, eq Withdrawn) x eq Given    -> Unknown
    KGC345  the same, the two states declared distinct -> Compatible
    KGC346  xone(isA Valid, isA Invalid) x eq Given    -> Unknown
    KGC347  the same, branches declared disjoint       -> Compatible

The policy these express
-------------------------
A controller holds a record of consent and offers a dataset for use while
that consent may justify processing.  DPV publishes the states of consent and
divides them: two that may justify processing, given and renewed, and eight
that may not.  The offer says which states it accepts and the request says
which state the record is in.

Every constraint below is one a controller would write.  None was chosen to
exercise an operator.

Three ways to say the same thing
---------------------------------
KGC340 and KGC341 accept the same two states and reach the same verdict by
different routes, which is what makes the pair worth having.

KGC340 names the branch: `isA ConsentStatusValidForProcessing`.  The verdict
rests on an assertion DPV published, that consent given lies below that
branch, and the certificate cites it.  If DPV adds a third valid state
tomorrow, the offer covers it without being rewritten.

KGC341 enumerates: `or(eq ConsentGiven, eq RenewedConsentGiven)`.  The
verdict rests on nothing but the constraints, as KGC317 and KGC322 do, and
the certificate cites no resource assertion at all.  The offer is fixed
against the vocabulary: a third valid state would not be covered.

Same intent, same answer, different evidence, different behaviour under
growth.  A drafter choosing between them is choosing whether to defer to the
authority, and the certificates make the choice visible.

Why xone needs a declaration
------------------------------
KGC344 is the pair that shows what `xone` costs.  The offer says the record
must be in exactly one of two states, given or withdrawn: a natural thing to
require of a consent record, and the shape ODRL's `xone` exists for.

Expanded, it is a disjunction of two alternatives, each carrying the negation
of the other.  Take the first: the state is given and is not withdrawn.  The
second conjunct is a negated equality, and DPV publishes nothing that
separates the two states, so a structure may interpret them as one concept.
In such a structure the record is both given and withdrawn, neither
alternative holds exactly once, and the offer is not satisfied.  Verdict:
Unknown.

Declare the two distinct and every structure separates them, the first
alternative holds, and the verdict is Compatible.  The declaration is doing
the work `xone` appears to do on its own.  This is worth saying plainly
because it is easy to miss: exactly-one is a claim about how many
alternatives hold, and counting requires knowing when two alternatives are
the same one.

KGC346 makes the same point over the order rather than over identity.  The
offer requires the record to be in exactly one of the two branches.  Consent
given lies below the valid branch, which DPV asserts; whether it also lies
below the invalid branch is not settled, since a structure may order concepts
the resource does not.  Both branches would then hold, and exactly-one fails.
Declaring the branches disjoint rules that out, and the verdict is
Compatible.

The disjointness is the one the module's own definitions warrant: DPV defines
one branch as the states that can justify processing and the other as the
states that cannot.  It publishes no owl:disjointWith.  So the certificate
marks the premise withdrawable even though the publisher's prose is what
warrants it, which is the honest reading: what the definitions warrant, they
do not assert.

The four background theories
------------------------------
    empty          nothing declared; what the module publishes alone
    definitional   the two branches disjoint, on the module's definitions
    declared       consent given and consent withdrawn declared distinct

KGC342 and KGC343 differ only in the first two, KGC344 and KGC345 only in the
first and third, KGC346 and KGC347 only in the first two.  Three pairs, each
isolating one declaration.

Notes on the encoding
----------------------
The offer of a `xone` problem is given as a tree rather than a flat list, and
the generator compiles it: expansion, distribution, and the disjunction of
the disjuncts' witness conditions.  The disjunction is inside both queries,
not around them; a per-alternative verdict combined afterwards would be
wrong for the reason the per-operand combination is confined to conjunction.

No `xone` alternative is an `isAllOf` constraint, as the signature requires.
"""

from compile import Constraint, Or, Xone

VALID    = "dpv_consent_status_valid_for_processing"
INVALID  = "dpv_consent_status_invalid_for_processing"
GIVEN    = "dpv_consent_given"
RENEWED  = "dpv_renewed_consent_given"
WITHDRAWN = "dpv_consent_withdrawn"

RESOURCE       = "https://w3id.org/odrl-kb/dpv-consent"
EMPTY_BT       = "https://w3id.org/odrl-kb/dpv-consent/empty"
DEFINITIONAL_BT = "https://w3id.org/odrl-kb/dpv-consent/definitional"
DECLARED_BT    = "https://w3id.org/odrl-kb/dpv-consent/declared"

INCLUDES               = ["KGE000-0.ax", "DPV-consent.ax"]
INCLUDES_DEFINITIONAL  = INCLUDES + ["DPV-consent-definitional.ax"]
INCLUDES_DECLARED      = INCLUDES + ["DPV-consent-declared.ax"]


def C(op, *vals, side="offer"):
    return Constraint(op, tuple(vals), side)


_TTL_HEAD = """\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dpv:     <https://w3id.org/dpv#> .
@prefix dpvo:    <https://w3id.org/dpv/mappings/odrl#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .
"""


def _offer_atomic(pid, title, operator, value):
    return f"""
drk:offer-{pid[3:]} a odrl:Offer ;
    dcterms:title "{title}"@en ;
    odrl:assigner drk:controller ;
    odrl:permission kgc:{pid}-offer-r1 .

kgc:{pid}-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:dataset ;
    odrl:constraint kgc:{pid}-offer-c1 .

kgc:{pid}-offer-c1 a odrl:Constraint ;
    odrl:leftOperand dpvo:Status ;
    odrl:operator odrl:{operator} ;
    odrl:rightOperand dpv:{value} .
"""


def _offer_logical(pid, title, operand, alts):
    """A Logical Constraint whose operands are atomic constraints.

    ODRL ranges a Logical Constraint's operands over Constraint instances, so
    the alternatives are written out as constraints and referenced from the
    list.
    """
    refs = ", ".join(f"kgc:{pid}-offer-a{i}" for i in range(1, len(alts) + 1))
    body = f"""
drk:offer-{pid[3:]} a odrl:Offer ;
    dcterms:title "{title}"@en ;
    odrl:assigner drk:controller ;
    odrl:permission kgc:{pid}-offer-r1 .

kgc:{pid}-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:dataset ;
    odrl:constraint kgc:{pid}-offer-c1 .

kgc:{pid}-offer-c1 a odrl:LogicalConstraint ;
    odrl:{operand} ( {refs} ) .
"""
    for i, (op, val) in enumerate(alts, start=1):
        body += f"""
kgc:{pid}-offer-a{i} a odrl:Constraint ;
    odrl:leftOperand dpvo:Status ;
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
    odrl:leftOperand dpvo:Status ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:{value} .
"""


PROBLEMS = [

    # ------------------------------------------------------------------
    # KGC340  The constraint the resource exists for.
    # ------------------------------------------------------------------
    {
        "id":                "KGC340",
        "subdir":            "verdict",
        "name":              "consent status, isA ValidForProcessing "
                             "against eq ConsentGiven",
        "left_operand":      "Status",
        "sort":              "tax",
        "resource":          RESOURCE,
        "background_theory": EMPTY_BT,
        "includes":          INCLUDES,
        "tree": [C("isA", VALID), C("eq", GIVEN, side="request")],
        "description": (
            "The controller permits use while the consent may justify "
            "processing; the record is in the given state.  DPV places "
            "consent given below the branch of states valid for processing, "
            "so the verdict is Compatible on one assertion.  The offer names "
            "the branch rather than the states, so a state DPV adds to that "
            "branch later is covered without the offer being rewritten."
        ),
        "expected_q1": "Satisfiable",
        "expected_q2": "Unsatisfiable",
        "certificate": {
            "kind": "Refutation",
            "comment": "DPV places consent given among the states valid for "
                       "processing.",
            "premises": [
                ("fromResource",
                 "dpv:ConsentGiven is below dpv:ConsentStatusValidForProcessing"),
            ],
        },
        "ttl": _TTL_HEAD
               + _offer_atomic("KGC340",
                               "Use is permitted while consent may justify "
                               "processing",
                               "isA", "ConsentStatusValidForProcessing")
               + _request("KGC340", "The consent record is in the given state",
                          "ConsentGiven"),
    },

    # ------------------------------------------------------------------
    # KGC341  The same policy, enumerated instead of named.
    # ------------------------------------------------------------------
    {
        "id":                "KGC341",
        "subdir":            "verdict",
        "name":              "consent status, or(eq ConsentGiven, "
                             "eq RenewedConsentGiven) against eq "
                             "RenewedConsentGiven",
        "left_operand":      "Status",
        "sort":              "tax",
        "resource":          RESOURCE,
        "background_theory": EMPTY_BT,
        "includes":          INCLUDES,
        "tree": [Or((C("eq", GIVEN), C("eq", RENEWED))),
                 C("eq", RENEWED, side="request")],
        "description": (
            "The same policy as KGC340, written by enumerating the two states "
            "rather than by naming the branch that holds them.  The verdict "
            "is again Compatible, and the certificate cites no resource "
            "assertion: the second alternative is the requested state, and "
            "nothing needs to be looked up.  The offer is fixed against the "
            "vocabulary as it stands, where KGC340's is not."
        ),
        "expected_q1": "Satisfiable",
        "expected_q2": "Unsatisfiable",
        "certificate": {
            "kind": "Refutation",
            "comment": "The requested state is one the offer names, so the "
                       "constraints settle the verdict without the resource.",
            "premises": [],
        },
        "ttl": _TTL_HEAD
               + _offer_logical("KGC341",
                                "Use is permitted for consent given or "
                                "renewed consent given",
                                "or",
                                [("eq", "ConsentGiven"),
                                 ("eq", "RenewedConsentGiven")])
               + _request("KGC341",
                          "The consent record is in the renewed given state",
                          "RenewedConsentGiven"),
    },

    # ------------------------------------------------------------------
    # KGC342 / KGC343  The branches, undeclared and declared disjoint.
    # ------------------------------------------------------------------
    {
        "id":                "KGC342",
        "subdir":            "verdict",
        "name":              "consent status, isA ValidForProcessing "
                             "against eq ConsentWithdrawn",
        "left_operand":      "Status",
        "sort":              "tax",
        "resource":          RESOURCE,
        "background_theory": EMPTY_BT,
        "includes":          INCLUDES,
        "tree": [C("isA", VALID), C("eq", WITHDRAWN, side="request")],
        "description": (
            "The record is withdrawn and the offer requires a state valid for "
            "processing.  DPV places consent withdrawn below the invalid "
            "branch and asserts nothing that keeps the two branches apart, so "
            "a structure may place the withdrawn state below both.  The "
            "verdict is Unknown, which is the right answer to what the module "
            "publishes even though the definitions read otherwise."
        ),
        "expected_q1": "Satisfiable",
        "expected_q2": "Satisfiable",
        "certificate": {
            "kind": "Models",
            "comment": "Both queries are satisfiable.  The models differ on "
                       "whether the withdrawn state lies below the branch of "
                       "states valid for processing, which the module does "
                       "not settle.",
            "premises": [],
        },
        "ttl": _TTL_HEAD
               + _offer_atomic("KGC342",
                               "Use is permitted while consent may justify "
                               "processing",
                               "isA", "ConsentStatusValidForProcessing")
               + _request("KGC342",
                          "The consent record is in the withdrawn state",
                          "ConsentWithdrawn"),
    },
    {
        "id":                "KGC343",
        "subdir":            "verdict",
        "name":              "consent status, isA ValidForProcessing "
                             "against eq ConsentWithdrawn, branches disjoint",
        "left_operand":      "Status",
        "sort":              "tax",
        "resource":          RESOURCE,
        "background_theory": DEFINITIONAL_BT,
        "includes":          INCLUDES_DEFINITIONAL,
        "tree": [C("isA", VALID), C("eq", WITHDRAWN, side="request")],
        "description": (
            "The constraints of KGC342 with the two branches declared "
            "disjoint.  Nothing then lies below both, the withdrawn state "
            "lies below the invalid branch, and no structure places it below "
            "the valid one: Incompatible.  The declaration is warranted by "
            "the module's own definitions, one branch being the states that "
            "can justify processing and the other the states that cannot, and "
            "the module asserts it nowhere.  The certificate marks it "
            "withdrawable on that ground."
        ),
        "expected_q1": "Unsatisfiable",
        "expected_q2": "Satisfiable",
        "certificate": {
            "kind": "Refutation",
            "comment": "The withdrawn state lies below the invalid branch, "
                       "and the branches are declared to have nothing in "
                       "common.  The declaration follows the module's "
                       "definitions; the module does not assert it, so a "
                       "party may withdraw it and reopen the verdict.",
            "premises": [
                ("fromResource",
                 "dpv:ConsentWithdrawn is below "
                 "dpv:ConsentStatusInvalidForProcessing"),
                ("fromBackgroundTheory",
                 "the two branches have nothing below both"),
            ],
        },
        "ttl": _TTL_HEAD
               + _offer_atomic("KGC343",
                               "Use is permitted while consent may justify "
                               "processing",
                               "isA", "ConsentStatusValidForProcessing")
               + _request("KGC343",
                          "The consent record is in the withdrawn state",
                          "ConsentWithdrawn"),
    },

    # ------------------------------------------------------------------
    # KGC344 / KGC345  xone over identity: counting needs distinctness.
    # ------------------------------------------------------------------
    {
        "id":                "KGC344",
        "subdir":            "verdict",
        "name":              "consent status, xone(eq ConsentGiven, "
                             "eq ConsentWithdrawn) against eq ConsentGiven",
        "left_operand":      "Status",
        "sort":              "tax",
        "resource":          RESOURCE,
        "background_theory": EMPTY_BT,
        "includes":          INCLUDES,
        "tree": [Xone((C("eq", GIVEN), C("eq", WITHDRAWN))),
                 C("eq", GIVEN, side="request")],
        "description": (
            "The offer requires the record to be settled: in exactly one of "
            "the given and withdrawn states.  The record is given, so the "
            "answer looks immediate.  It is not.  Expanded, the first "
            "alternative requires the state to be given and not withdrawn, "
            "and DPV publishes nothing that separates the two: a structure "
            "may interpret them as one state, in which case the record is "
            "both and neither alternative holds alone.  Verdict: Unknown.  "
            "Counting alternatives requires knowing when two of them are the "
            "same."
        ),
        "expected_q1": "Satisfiable",
        "expected_q2": "Satisfiable",
        "certificate": {
            "kind": "Models",
            "comment": "Both queries are satisfiable.  The models differ on "
                       "whether the given and withdrawn states are one, and "
                       "the exclusive requirement turns on that.",
            "premises": [],
        },
        "ttl": _TTL_HEAD
               + _offer_logical("KGC344",
                                "Use is permitted while the consent record is "
                                "settled: given or withdrawn, and not both",
                                "xone",
                                [("eq", "ConsentGiven"),
                                 ("eq", "ConsentWithdrawn")])
               + _request("KGC344", "The consent record is in the given state",
                          "ConsentGiven"),
    },
    {
        "id":                "KGC345",
        "subdir":            "verdict",
        "name":              "consent status, xone(eq ConsentGiven, "
                             "eq ConsentWithdrawn) against eq ConsentGiven, "
                             "the two states declared distinct",
        "left_operand":      "Status",
        "sort":              "tax",
        "resource":          RESOURCE,
        "background_theory": DECLARED_BT,
        "includes":          INCLUDES_DECLARED,
        "tree": [Xone((C("eq", GIVEN), C("eq", WITHDRAWN))),
                 C("eq", GIVEN, side="request")],
        "description": (
            "The constraints of KGC344 with the two states declared distinct.  "
            "Every structure then separates them, the first alternative holds "
            "and the second does not, and the verdict is Compatible.  The "
            "declaration is what makes the exclusive requirement decidable: "
            "with it the offer means what it appears to mean, and without it "
            "the same offer is open.  This is the pair to read together."
        ),
        "expected_q1": "Satisfiable",
        "expected_q2": "Unsatisfiable",
        "certificate": {
            "kind": "Refutation",
            "comment": "The two states are declared distinct, so exactly one "
                       "alternative holds of a record in the given state.  "
                       "The premise is the parties', and withdrawing it "
                       "returns the verdict to Unknown.",
            "premises": [
                ("fromBackgroundTheory",
                 "dpv:ConsentGiven and dpv:ConsentWithdrawn are distinct"),
            ],
        },
        "ttl": _TTL_HEAD
               + _offer_logical("KGC345",
                                "Use is permitted while the consent record is "
                                "settled: given or withdrawn, and not both",
                                "xone",
                                [("eq", "ConsentGiven"),
                                 ("eq", "ConsentWithdrawn")])
               + _request("KGC345", "The consent record is in the given state",
                          "ConsentGiven"),
    },

    # ------------------------------------------------------------------
    # KGC346 / KGC347  xone over the order: the same point, one level up.
    # ------------------------------------------------------------------
    {
        "id":                "KGC346",
        "subdir":            "verdict",
        "name":              "consent status, xone(isA ValidForProcessing, "
                             "isA InvalidForProcessing) against eq ConsentGiven",
        "left_operand":      "Status",
        "sort":              "tax",
        "resource":          RESOURCE,
        "background_theory": EMPTY_BT,
        "includes":          INCLUDES,
        "tree": [Xone((C("isA", VALID), C("isA", INVALID))),
                 C("eq", GIVEN, side="request")],
        "description": (
            "The offer requires the record to fall under exactly one of the "
            "two branches, which is what the division means.  DPV places "
            "consent given below the valid branch; whether it also lies below "
            "the invalid branch is not settled, since a structure may order "
            "concepts the resource leaves unordered.  Both alternatives would "
            "then hold and the exclusive requirement fails.  Verdict: "
            "Unknown."
        ),
        "expected_q1": "Satisfiable",
        "expected_q2": "Satisfiable",
        "certificate": {
            "kind": "Models",
            "comment": "Both queries are satisfiable.  The models differ on "
                       "whether the given state also lies below the invalid "
                       "branch, which the module does not rule out.",
            "premises": [],
        },
        "ttl": _TTL_HEAD
               + _offer_logical("KGC346",
                                "Use is permitted while the consent record "
                                "falls under exactly one of the two branches",
                                "xone",
                                [("isA", "ConsentStatusValidForProcessing"),
                                 ("isA", "ConsentStatusInvalidForProcessing")])
               + _request("KGC346", "The consent record is in the given state",
                          "ConsentGiven"),
    },
    {
        "id":                "KGC347",
        "subdir":            "verdict",
        "name":              "consent status, xone(isA ValidForProcessing, "
                             "isA InvalidForProcessing) against eq "
                             "ConsentGiven, branches disjoint",
        "left_operand":      "Status",
        "sort":              "tax",
        "resource":          RESOURCE,
        "background_theory": DEFINITIONAL_BT,
        "includes":          INCLUDES_DEFINITIONAL,
        "tree": [Xone((C("isA", VALID), C("isA", INVALID))),
                 C("eq", GIVEN, side="request")],
        "description": (
            "The constraints of KGC346 with the branches declared disjoint.  "
            "Nothing lies below both, so the given state lies below the valid "
            "branch and not the invalid one, exactly one alternative holds, "
            "and the verdict is Compatible.  The refutation cites an "
            "assertion DPV published and a declaration the parties made, and "
            "the certificate marks which is which."
        ),
        "expected_q1": "Satisfiable",
        "expected_q2": "Unsatisfiable",
        "certificate": {
            "kind": "Refutation",
            "comment": "The given state lies below the valid branch, and the "
                       "branches are declared to have nothing below both, so "
                       "it lies below that branch alone.",
            "premises": [
                ("fromResource",
                 "dpv:ConsentGiven is below "
                 "dpv:ConsentStatusValidForProcessing"),
                ("fromBackgroundTheory",
                 "the two branches have nothing below both"),
            ],
        },
        "ttl": _TTL_HEAD
               + _offer_logical("KGC347",
                                "Use is permitted while the consent record "
                                "falls under exactly one of the two branches",
                                "xone",
                                [("isA", "ConsentStatusValidForProcessing"),
                                 ("isA", "ConsentStatusInvalidForProcessing")])
               + _request("KGC347", "The consent record is in the given state",
                          "ConsentGiven"),
    },
]