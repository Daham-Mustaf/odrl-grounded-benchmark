"""
problem_data_bcp47.py
=====================
Four problems over the BCP 47 language slice, at nom.

    KGC370  eq de x eq fr, uniqueness declared      Incompatible
    KGC371  the same pair, declaration withdrawn    Unknown, epistemic
    KGC372  eq de x eq "en-US", exact grounding     Unknown, ungrounded
    KGC373  the same pair, primary-subtag grounding Incompatible

None of them is here to exercise an operator.  At nom the signature admits
eq, neq, isAnyOf, isAllOf and isNoneOf, and every one of those is already
exercised on another operand.  What this resource shows is three things
about resources and one about profiles.

The withdrawal pair
-------------------
KGC370 and KGC371 are the same two policies over the same resource,
differing in one include line.

The registry publishes the subtags.  Separately it publishes identity,
through Preferred-Value, and an order, through Macrolanguage.  It does not
publish distinctness: that two subtags name two languages is a rule the
parties adopt, warranted by RFC 5646's uniqueness discipline and absent
from the data.

So without the declaration a structure may interpret de and fr as one
language and nothing published rules it out, and the verdict is Unknown.
With it, Incompatible, on one premise that belongs to the parties and that
withdrawing reopens.

The grounding pair
------------------
KGC372 and KGC373 are the same two policies over the same resource at the
same sort, differing in which profile reads them.

en-US is a well-formed language tag: RFC 5646 composes it from a
registered primary subtag and a registered region subtag.  It is not a
concept of this slice, which holds primary subtags.

Under the exact binding the grounding resolves an IRI of the scheme or a
literal equal to a published notation, and en-US is neither, so no query
is built and the verdict is Unknown with that value as its certificate.
Under the primary-subtag binding a well-formed tag reduces to its first
component, en-US grounds to en, and the pair gets an ordinary verdict.

Neither reading is wrong.  A party who cares which variety of English is
distributed declines the reduction and gets an uninterpretable policy
rather than a wrong answer; a party who does not, adopts it.  The profile
is where that is recorded, which is what makes the two verdicts different
without any disagreement about a concept.

The two kinds of Unknown
------------------------
KGC371 and KGC372 both report Unknown and are repaired differently.
KGC371's is epistemic: the resource admits structures either way, and a
declaration settles it.  KGC372's is ungrounded: the policy names
something the binding cannot read, and no declaration helps, because
nothing has been left open.  The policy is corrected or the binding is
widened.

That is why an Unknown carries its reason, and why a report that gave only
the verdict would be telling a reader to guess which repair applies.

Why nom is a property of the slice
----------------------------------
The registry publishes Macrolanguage fields over its language subtags,
each an order assertion between two of them; how many is measured from the
snapshot by the builder and written into the resource header.  None of the
fifteen members here carries one, and the builder aborts if a future
member does.

So the nominal binding is right for this slice and would be wrong for one
containing cmn and zh.  This is the suite's only case where one
publisher's data supports two sorts depending on which concepts are taken.
"""

from compile import Constraint

DE = "bcp_de"
FR = "bcp_fr"
EN = "bcp_en"

RESOURCE   = "https://w3id.org/odrl-kb/bcp47"
UNIQUENESS = "https://w3id.org/odrl-kb/bcp47/uniqueness"

BINDING_EXACT   = "https://w3id.org/odrl-kb/profile/b-language-bcp47"
BINDING_PRIMARY = ("https://w3id.org/odrl-kb/profile/"
                   "b-language-bcp47-primary")

# The resource alone, and the resource with the parties' rule.  The
# withdrawal pair is the difference between these two lists.
INCLUDES            = ["KGE000-0.ax", "BCP47000-0.ax"]
INCLUDES_UNIQUENESS = INCLUDES + ["BCP47001-0.ax"]


def C(op, *vals, side="offer"):
    return Constraint(op, tuple(vals), side)


_TTL_HEAD = """\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix bcp47:   <https://w3id.org/odrl-kb/bcp47#> .
@prefix vrep:    <https://w3id.org/odrl-verdict-report#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .
"""


def _offer(pid):
    return f"""
drk:offer-{pid[3:]} a odrl:Offer ;
    dcterms:title "Distribution in German"@en ;
    odrl:assigner drk:publisher ;
    odrl:permission kgc:{pid}-offer-r1 .

kgc:{pid}-offer-r1 a odrl:Permission ;
    odrl:action odrl:distribute ;
    odrl:target drk:dataset ;
    odrl:constraint kgc:{pid}-offer-c1 .

kgc:{pid}-offer-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:language ;
    odrl:operator odrl:eq ;
    odrl:rightOperand bcp47:de .
"""


def _request(pid, title, value, comment=""):
    note = f'\n    rdfs:comment """{comment}"""@en ;' if comment else ""
    return f"""
drk:request-{pid[3:]} a odrl:Request ;
    dcterms:title "{title}"@en ;{note}
    odrl:assignee drk:reuser ;
    odrl:permission kgc:{pid}-request-r1 .

kgc:{pid}-request-r1 a odrl:Permission ;
    odrl:action odrl:distribute ;
    odrl:target drk:dataset ;
    odrl:constraint kgc:{pid}-request-c1 .

kgc:{pid}-request-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:language ;
    odrl:operator odrl:eq ;
    odrl:rightOperand {value} .
"""


def _binding_note(pid, binding):
    return f"""
drk:offer-{pid[3:]} vrep:readUnder <{binding}> .
drk:request-{pid[3:]} vrep:readUnder <{binding}> .
"""


EN_US_COMMENT = (
    "A well-formed BCP 47 language tag: RFC 5646 composes it from the "
    "registered primary subtag en and the registered region subtag US. "
    "It is not a concept of this slice, which holds primary subtags, and "
    "whether it resolves to one is the profile's grounding rule to decide."
)


PROBLEMS = [

    {
        "id":                "KGC370",
        "subdir":            "verdict",
        "name":              "language, eq de against eq fr, "
                             "registry uniqueness declared",
        "left_operand":      "language",
        "sort":              "nom",
        "resource":          RESOURCE,
        "background_theory": UNIQUENESS,
        "binding":           BINDING_EXACT,
        "includes":          INCLUDES_UNIQUENESS,
        "tree": [C("eq", DE), C("eq", FR, side="request")],
        "description": (
            "The publisher distributes in German; the reuser asks for "
            "French. With the parties' registry-uniqueness rule in force "
            "no structure interprets the two subtags as one language, so "
            "no use satisfies both constraints and the verdict is "
            "Incompatible.\n\n"
            "The refutation cites one background premise. The registry "
            "lists both subtags and asserts nothing that separates them, "
            "so what makes this verdict definite is a rule the parties "
            "adopted rather than something IANA published."
        ),
        "expected_verdict": "Incompatible",
        "expected_q1": "Unsatisfiable",
        "expected_q2": "Satisfiable",
        "certificate": {
            "kind": "Refutation",
            "comment": "The two subtags are declared to name distinct "
                       "languages. Withdrawing that declaration returns "
                       "the verdict to Unknown, which is KGC371.",
            "premises": [
                ("fromBackgroundTheory",
                 "bcp47:de and bcp47:fr are declared distinct, on RFC "
                 "5646's registry uniqueness"),
            ],
        },
        "ttl": _TTL_HEAD + _offer("KGC370")
               + _request("KGC370", "Distribution in French", "bcp47:fr")
               + _binding_note("KGC370", BINDING_EXACT),
    },

    {
        "id":                "KGC371",
        "subdir":            "verdict",
        "name":              "language, eq de against eq fr, "
                             "declaration withdrawn",
        "left_operand":      "language",
        "sort":              "nom",
        "resource":          RESOURCE,
        "background_theory": None,
        "binding":           BINDING_EXACT,
        "includes":          INCLUDES,
        "tree": [C("eq", DE), C("eq", FR, side="request")],
        "description": (
            "The constraints of KGC370 with the uniqueness rule "
            "withdrawn. The resource still lists both subtags and still "
            "says nothing that separates them, so a structure may "
            "interpret de and fr as one language and another may keep "
            "them apart. The verdict is Unknown, and the reason is "
            "epistemic: a declaration settles it.\n\n"
            "Read with KGC370 this is what a withdrawable premise is. The "
            "same policies over the same resource, one include line "
            "apart, and the verdict moves from definite to open because a "
            "party stopped asserting something the registry never "
            "asserted."
        ),
        "expected_verdict": "Unknown",
        "unknown_reason":   "epistemic",
        "expected_q1": "Satisfiable",
        "expected_q2": "Satisfiable",
        "certificate": {
            "kind": "Models",
            "comment": "Both queries are satisfiable, and the models "
                       "differ on whether bcp47:de and bcp47:fr are one "
                       "concept, which the registry does not decide.",
            "premises": [],
        },
        "ttl": _TTL_HEAD + _offer("KGC371")
               + _request("KGC371", "Distribution in French", "bcp47:fr")
               + _binding_note("KGC371", BINDING_EXACT),
    },

    {
        # No queries are built for this problem: writers.py reads the
        # ungrounded field and skips construction, so no expected_q1 or
        # expected_q2 appears here.  Supplying them would mean the value
        # had become a constant of the signature, which is the collapse
        # this problem exists to rule out.
        "id":                "KGC372",
        "subdir":            "verdict",
        "name":              "language, eq de against eq \"en-US\", "
                             "exact grounding",
        "left_operand":      "language",
        "sort":              "nom",
        "resource":          RESOURCE,
        "background_theory": UNIQUENESS,
        "binding":           BINDING_EXACT,
        "includes":          INCLUDES_UNIQUENESS,
        "ungrounded":        "en-US",
        "description": (
            "The reuser asks for en-US. Under the exact binding a value "
            "resolves when it is an IRI of the scheme or a literal equal "
            "to a published notation, and en-US is neither: the slice "
            "holds primary subtags and en-US is a composed tag.\n\n"
            "The grounding is therefore undefined on the request's right "
            "operand, no query is built, and the verdict is Unknown with "
            "that value as its certificate. The reason is ungrounded and "
            "not epistemic, and the two are repaired differently: a "
            "declaration settles an epistemic Unknown and does nothing "
            "here, which needs the policy corrected or the binding "
            "widened. KGC373 is the same pair read under the wider "
            "binding."
        ),
        "expected_verdict": "Unknown",
        "unknown_reason":   "ungrounded",
        "certificate": {
            "kind": "Ungrounded",
            "comment": "The value en-US names no concept of the slice "
                       "under this binding's grounding. Checkable by "
                       "applying the grounding to it.",
            "premises": [],
        },
        "ttl": _TTL_HEAD + _offer("KGC372")
               + _request("KGC372", "Distribution in American English",
                          '"en-US"', EN_US_COMMENT)
               + _binding_note("KGC372", BINDING_EXACT),
    },

    {
        "id":                "KGC373",
        "subdir":            "verdict",
        "name":              "language, eq de against eq \"en-US\", "
                             "primary-subtag grounding",
        "left_operand":      "language",
        "sort":              "nom",
        "resource":          RESOURCE,
        "background_theory": UNIQUENESS,
        "binding":           BINDING_PRIMARY,
        "includes":          INCLUDES_UNIQUENESS,
        "tree": [C("eq", DE), C("eq", EN, side="request")],
        "description": (
            "The policies of KGC372 read under the binding whose "
            "grounding reduces a well-formed tag to its primary subtag. "
            "en-US resolves to en, the request is interpretable, and the "
            "pair gets an ordinary verdict: German and English are "
            "declared distinct, so no use satisfies both and the verdict "
            "is Incompatible.\n\n"
            "Neither reading is wrong. A party who cares which variety of "
            "English is distributed declines the reduction and gets an "
            "uninterpretable policy rather than a wrong answer; a party "
            "who does not, adopts it. The two verdicts differ without any "
            "disagreement about a concept, and the profile is where the "
            "difference is recorded."
        ),
        "expected_verdict": "Incompatible",
        "expected_q1": "Unsatisfiable",
        "expected_q2": "Satisfiable",
        "certificate": {
            "kind": "Refutation",
            "comment": "The request's value resolved to bcp_en under this "
                       "binding's grounding, and bcp_de and bcp_en are "
                       "declared distinct.",
            "premises": [
                ("fromBackgroundTheory",
                 "bcp47:de and bcp47:en are declared distinct, on RFC "
                 "5646's registry uniqueness"),
            ],
        },
        "ttl": _TTL_HEAD + _offer("KGC373")
               + _request("KGC373", "Distribution in American English",
                          '"en-US"', EN_US_COMMENT)
               + _binding_note("KGC373", BINDING_PRIMARY),
    },
]