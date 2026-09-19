"""
problem_data_gdprlb.py
======================
Four problems over the GDPR Article 6 legal-basis resource, at tax.

    KGC350  isAnyOf(seven bases) x eq dpv:Consent          -> Compatible
    KGC351  isAnyOf(seven bases) x eq A6-1-a-explicit       -> Unknown
    KGC352  the same, concepts declared distinct            -> Incompatible
    KGC353  isA dpv:LegalBasis   x eq A6-1-a-explicit       -> Compatible

The offer is not ours
---------------------
The ODRL Regulatory Compliance Profile encodes Article 6(1) as a single
constraint: the legal basis must be any of consent, contract, legal
obligation, vital interest, public interest, official authority, or
legitimate interest. That is the Article's list, and the profile's names
are the Data Privacy Vocabulary's concepts. All four problems below use it
verbatim as the offer, so the constraint under test is one a published
profile wrote rather than one chosen to exercise an operator.

What is taken from the profile is that constraint and nothing else. The
same policy carries a prohibition for processing that affects the data
subject's fundamental rights, an obligation to provide safeguards, and a
dispensation for public authorities. Those are rules standing in deontic
relations to one another, and the verdict here does not decide which
prevails; it decides whether two constraint sets admit a common use, which
is an input to that question. Their constraints are nevertheless evidence
that the operators of the fragment occur in practice: the Article 46
permission composes two operands under or, and the Article 6(2)
dispensation composes two under and.

The profile adopts two operators, isA and isAnyOf, and says so in prose.
The other six of the fragment apply to this operand unchanged: neq and
isNoneOf would exclude a basis, isAllOf would require several. The
restriction is the profile author's choice rather than a limit of the
operand or of the vocabulary.

What the four show
------------------
KGC350 is the case the profile was written for. The record names one of
the seven, the enumeration matches it, and the verdict rests on nothing but
the constraints: the certificate cites no assertion of the vocabulary at
all.

KGC351 is the same offer against a record naming explicit consent under
Article 6(1)(a). This is a legal basis: GDPR Article 6(1)(a) covers it, and
the extension places it below the Article 6(1)(a) concept, which lies below
consent, which lies below the legal-basis root. The enumeration does not
reach it, because isAnyOf compares by identity and explicit consent is not
one of the seven names. The verdict is nevertheless Unknown rather than
Incompatible: the vocabulary declares nothing distinct, so a structure may
interpret explicit consent and consent as one concept.

KGC352 adds the parties' distinctness declaration and the verdict becomes
Incompatible. An offer encoding Article 6(1) now refuses a legal basis that
Article 6(1) provides.

KGC353 is the same record against an offer that names the branch instead of
enumerating it. The chain from explicit consent up to the legal-basis root
is four assertions of the vocabulary, and the verdict is Compatible in
every structure.

The pair KGC352 and KGC353 is the point. Two ways to encode the same
Article, the same record, opposite verdicts, and the difference is whether
the offer defers to the vocabulary's order or fixes a list against it. The
certificates say which: KGC353's cites four published assertions and the
transitivity of the order, KGC352's cites a declaration the parties made.

Sorting note
------------
Both encodings are well sorted. The operand is tax, and isAnyOf is
admissible at every sort while isA is admissible at tax, so neither is
rejected by the signature. The difference is semantic, which is why the
signature alone does not settle it.
"""

from compile import Constraint, Or, Xone

LB       = "lb_dpv_legal_basis"
CONSENT  = "lb_dpv_consent"
CONTRACT = "lb_dpv_contract"
LEGALOB  = "lb_dpv_legal_obligation"
VITAL    = "lb_dpv_vital_interest"
PUBLIC   = "lb_dpv_public_interest"
AUTH     = "lb_dpv_official_authority_of_controller"
LEGITIM  = "lb_dpv_legitimate_interest"
EXPLICIT = "lb_gdpr_a6_1_a_explicit_consent"

SEVEN = [CONSENT, CONTRACT, LEGALOB, VITAL, PUBLIC, AUTH, LEGITIM]

RESOURCE     = "https://w3id.org/odrl-kb/dpv-gdpr-legal-basis"
EMPTY_BT     = "https://w3id.org/odrl-kb/dpv-gdpr-legal-basis/empty"
DECLARED_BT  = "https://w3id.org/odrl-kb/dpv-gdpr-legal-basis/declared"
BINDING = "https://w3id.org/odrl-kb/profile/b-legalbasis"
INCLUDES          = ["KGE000-0.ax", "DPV-gdprlb.ax"]
INCLUDES_DECLARED = INCLUDES + ["DPV-gdprlb-declared.ax"]


def C(op, *vals, side="offer"):
    return Constraint(op, tuple(vals), side)


_TTL_HEAD = """\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dpv:     <https://w3id.org/dpv#> .
@prefix eu-gdpr: <https://w3id.org/dpv/legal/eu/gdpr#> .
@prefix dpv-odrl:    <https://w3id.org/dpv/mappings/odrl#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .
"""

_SEVEN_TTL = """( dpv:Consent
        dpv:Contract
        dpv:LegalObligation
        dpv:VitalInterest
        dpv:PublicInterest
        dpv:OfficialAuthorityOfController
        dpv:LegitimateInterest )"""


def _offer_isanyof(pid):
    """The Article 6(1) constraint of the Regulatory Compliance Profile.

    Taken verbatim from Example 1 of the profile, at
    https://ai.wu.ac.at/policies/orcp/regulatory-model.html, section 2.10.1.
    What is taken is the predicateConstraint of the permission rule and
    nothing else: the rule's deontic role is not modelled here.  The profile
    also carries a prohibition, an obligation and a dispensation in the same
    policy, and those stand in deontic relations to one another that our
    verdict does not decide.  We decide whether two constraint sets admit a
    common use, which is an input to a conflict between a permission and a
    prohibition rather than that conflict itself.

    The profile names the seven bases by the concepts of the Data Privacy
    Vocabulary, which is where the order they are read in comes from.  The
    profile itself publishes no order between them.
    """
    return f"""
# The constraint below is the predicateConstraint of the permission rule in
# Example 1 of the ODRL Regulatory Compliance Profile, section 2.10.1, at
# https://ai.wu.ac.at/policies/orcp/regulatory-model.html .  The rule's
# deontic role is not modelled: the verdict decides whether two constraint
# sets admit a common use, not which rule prevails where they do.

drk:offer-{pid[3:]} a odrl:Offer ;
    dcterms:title "Processing is lawful on any legal basis of Article 6(1)"@en ;
    dcterms:source <https://ai.wu.ac.at/policies/orcp/regulatory-model.html> ;
    rdfs:comment "The predicateConstraint of Example 1 of the ODRL \
Regulatory Compliance Profile, section 2.10.1, with the profile's own \
names for the seven bases of Article 6(1) read as concepts of the Data \
Privacy Vocabulary."@en ;
    odrl:assigner drk:controller ;
    odrl:permission kgc:{pid}-offer-r1 .

kgc:{pid}-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:dataset ;
    odrl:constraint kgc:{pid}-offer-c1 .

kgc:{pid}-offer-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:LegalBasis ;
    odrl:operator odrl:isAnyOf ;
    odrl:rightOperand {_SEVEN_TTL} .
"""


def _offer_isa(pid):
    return f"""
drk:offer-{pid[3:]} a odrl:Offer ;
    dcterms:title "Processing is lawful on any legal basis"@en ;
    odrl:assigner drk:controller ;
    odrl:permission kgc:{pid}-offer-r1 .

kgc:{pid}-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:dataset ;
    odrl:constraint kgc:{pid}-offer-c1 .

kgc:{pid}-offer-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:LegalBasis ;
    odrl:operator odrl:isA ;
    odrl:rightOperand dpv:LegalBasis .
"""


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
    odrl:leftOperand dpv-odrl:LegalBasis ;
    odrl:operator odrl:eq ;
    odrl:rightOperand {value} .
"""


PROBLEMS = [

    {
        "id":                "KGC350",
        "subdir":            "verdict",
        "name":              "legal basis, isAnyOf Article 6(1) against "
                             "eq dpv:Consent",
        "binding": BINDING,
        "left_operand":      "LegalBasis",
        "sort":              "tax",
        "resource":          RESOURCE,
        "background_theory": EMPTY_BT,
        "includes":          INCLUDES,
        "summary": (
    "A controller permits processing under any of the seven Article 6(1) "
    "legal bases, and a processor requests processing on the basis of consent."
),
        "tree": [C("isAnyOf", *SEVEN), C("eq", CONSENT, side="request")],
        "description": (
            "The controller permits processing on any of the seven legal "
            "bases of Article 6(1), as the Regulatory Compliance Profile "
            "encodes them, and the processor names consent. The offer names "
            "the requested basis, so the verdict is Compatible and the "
            "certificate cites no assertion of the vocabulary: the "
            "constraints settle it between themselves."
        ),
        "expected_q1": "Satisfiable",
        "expected_q2": "Unsatisfiable",
        "certificate": {
            "kind": "Refutation",
            
"comment": (
    "Consent is one of the seven values listed by isAnyOf, so the two "
    "constraints are Compatible without any resource or background assertion."
),
            "premises": [],
        },
        "ttl": _TTL_HEAD + _offer_isanyof("KGC350")
               + _request("KGC350",
                          "Processing is on the basis of consent",
                          "dpv:Consent"),
    },

    {
        "id":                "KGC351",
        "subdir":            "verdict",
        "name":              "legal basis, isAnyOf Article 6(1) against "
                             "eq A6-1-a-explicit-consent",
        "left_operand":      "LegalBasis",
        "sort":              "tax",
        "binding": BINDING,
        "resource":          RESOURCE,
        "background_theory": EMPTY_BT,
        "includes":          INCLUDES,
        "unknown_reason": "epistemic",
        "tree": [C("isAnyOf", *SEVEN), C("eq", EXPLICIT, side="request")],
        "description": (
            "The same offer against a processor naming explicit consent "
            "under Article 6(1)(a). That is a legal basis the Article "
            "provides, and the extension places it below the Article "
            "6(1)(a) concept, below consent, below the legal-basis root. "
            "The enumeration does not reach it: isAnyOf compares by "
            "identity and explicit consent is not one of the seven names. "
            "The verdict is Unknown rather than Incompatible, because "
            "nothing published declares the two apart and a structure may "
            "interpret explicit consent and consent as one concept."
        ),
        "summary": (
    "A controller permits processing under any of the seven Article 6(1) "
    "legal bases, while a processor requests processing on the basis of "
    "explicit consent under Article 6(1)(a)."
),
        "expected_q1": "Satisfiable",
        "expected_q2": "Satisfiable",
        "certificate": {
            "kind": "Models",
 "comment": (
    "Explicit consent is not one of the seven values listed by isAnyOf, "
    "and the resource does not declare it distinct from consent. The "
    "available knowledge therefore leaves the verdict Unknown."
    "The requested basis is one the offer enumerates."
),
            "premises": [],
        },
        "ttl": _TTL_HEAD + _offer_isanyof("KGC351")
               + _request("KGC351",
                          "Processing is on the basis of explicit consent "
                          "under Article 6(1)(a)",
                          "eu-gdpr:A6-1-a-explicit-consent"),
    },

    {
        "id":                "KGC352",
        "subdir":            "verdict",
        "name":              "legal basis, isAnyOf Article 6(1) against "
                             "eq A6-1-a-explicit-consent, concepts declared "
                             "distinct",
        "left_operand":      "LegalBasis",
        "sort":              "tax",
        "resource":          RESOURCE,
        "binding": BINDING,
        "background_theory": DECLARED_BT,
        "includes":          INCLUDES_DECLARED,
        "tree": [C("isAnyOf", *SEVEN), C("eq", EXPLICIT, side="request")],
        "description": (
            "The constraints of KGC351 with distinct concepts declared to "
            "denote distinct bases. No structure now identifies explicit "
            "consent with any of the seven, the enumeration cannot reach "
            "it, and the verdict is Incompatible. An offer encoding "
            "Article 6(1) thereby refuses a legal basis that Article 6(1) "
            "provides. The declaration is the parties', and it is what "
            "makes the refusal definite rather than open."
        ),
        "summary": (
    "A controller permits processing under any of the seven Article 6(1) "
    "legal bases, while a processor requests processing on the basis of "
    "explicit consent under Article 6(1)(a), with the two concepts "
    "declared distinct."
),

        "expected_q1": "Unsatisfiable",
        "expected_q2": "Satisfiable",
        "certificate": {
            "kind": "Refutation",
 "comment": (
        "The background theory declares explicit consent distinct from "
        "each of the seven values listed by isAnyOf. The requested value "
        "therefore cannot satisfy the offer."
    ),
             "premises": [
        ("fromBackgroundTheory",
         "dpv:Consent is distinct from explicit consent under Article 6(1)(a)"),
        ("fromBackgroundTheory",
         "dpv:Contract is distinct from explicit consent under Article 6(1)(a)"),
        ("fromBackgroundTheory",
         "dpv:LegalObligation is distinct from explicit consent under Article 6(1)(a)"),
        ("fromBackgroundTheory",
         "dpv:VitalInterest is distinct from explicit consent under Article 6(1)(a)"),
        ("fromBackgroundTheory",
         "dpv:PublicInterest is distinct from explicit consent under Article 6(1)(a)"),
        ("fromBackgroundTheory",
         "dpv:OfficialAuthorityOfController is distinct from explicit consent under Article 6(1)(a)"),
        ("fromBackgroundTheory",
         "dpv:LegitimateInterest is distinct from explicit consent under Article 6(1)(a)"),
    ],
        },
        "ttl": _TTL_HEAD + _offer_isanyof("KGC352")
               + _request("KGC352",
                          "Processing is on the basis of explicit consent "
                          "under Article 6(1)(a)",
                          "eu-gdpr:A6-1-a-explicit-consent"),
    },

    {
        "id":                "KGC353",
        "subdir":            "verdict",
        "name":              "legal basis, isA dpv:LegalBasis against "
                             "eq A6-1-a-explicit-consent",
        "left_operand":      "LegalBasis",
        "sort":              "tax",
        "resource":          RESOURCE,
        "background_theory": EMPTY_BT,
        "includes":          INCLUDES,
         "binding": BINDING,
        "tree": [C("isA", LB), C("eq", EXPLICIT, side="request")],
        "description": (
            "The record of KGC351 and KGC352 against an offer that names "
            "the branch rather than enumerating its members. Four "
            "assertions of the vocabulary carry explicit consent up to the "
            "legal-basis root, and with transitivity the verdict is "
            "Compatible in every structure. Read together with KGC352 this "
            "is the cost of the enumeration: the same Article, the same "
            "record, opposite verdicts, and the certificates say which "
            "rests on what."
        ),
          "summary": (
        "A controller permits processing under the legal-basis hierarchy, "
        "while a processor requests processing on the basis of explicit "
        "consent under Article 6(1)(a)."
    ),
        "expected_q1": "Satisfiable",
        "expected_q2": "Unsatisfiable",
        "certificate": {
            "kind": "Refutation",
  "comment": (
            "The vocabulary places explicit consent below the legal-basis "
            "root through three published order assertions. Transitivity "
            "of the order yields the relation used by isA."
        ),
            "premises": [
                ("fromResource",
                 "eu-gdpr:A6-1-a-explicit-consent is below eu-gdpr:A6-1-a"),
                ("fromResource",
                 "eu-gdpr:A6-1-a is below eu-gdpr:Consent"),
                ("fromResource",
                 "eu-gdpr:Consent is below dpv:Consent"),
                ("fromResource",
                 "dpv:Consent is below dpv:LegalBasis"),
                ("fromOrderAxiom", "transitivity of the order"),
            ],
        },
        "ttl": _TTL_HEAD + _offer_isa("KGC353")
               + _request("KGC353",
                          "Processing is on the basis of explicit consent "
                          "under Article 6(1)(a)",
                          "eu-gdpr:A6-1-a-explicit-consent"),
    },
]