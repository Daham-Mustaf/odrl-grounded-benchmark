"""
problem_data_bcp47.py
=====================
Four problems over the BCP 47 language slice, at the nominal sort.

    KGC370  eq de  x  eq fr         uniqueness declared   Incompatible
    KGC371  eq de  x  eq fr         declaration withdrawn Unknown, epistemic
    KGC372  eq de  x  eq "en-US"    exact grounding       Unknown, ungrounded
    KGC373  eq de  x  eq "en-US"    reducing grounding    Incompatible

The operators are beside the point.  At nom the signature admits eq, neq,
isAnyOf, isAllOf and isNoneOf, and every one is already exercised on
another operand; all four problems below use eq.  Each pair changes one
thing and holds everything else fixed, so that the change is what the
verdict responds to.

    370 -> 371   one background theory withdrawn
    372 -> 373   one grounding rule widened
    371 vs 372   two Unknowns with different repairs

A note on reading these
-----------------------
The two policies in each problem are ordinary ODRL: an Offer permitting
distribution in German, a Request asking to distribute in some other
language.  Nothing in them is unusual, and a reader who knows ODRL and not
this paper can read the case files without further explanation.

What the problems are about is the layer underneath: which vocabulary the
operand is bound to, what that vocabulary publishes, what the parties have
declared on top of it, and how a policy value is resolved to a concept.
Those four things live in the profile and the resource files, not in the
policies, and changing any of them changes the verdict without touching a
policy.

Problem one: what a registry publishes, and what it does not
-------------------------------------------------------------
The IANA Language Subtag Registry lists the subtags.  Separately it
publishes identity, through Preferred-Value, which says that 'iw' and 'he'
name one language; and an order, through Macrolanguage, which says that
Bosnian falls under Serbo-Croatian.  It nowhere says that two subtags name
two languages.

That is not an oversight.  A registry states what it has established, and
whether two of its entries may be treated as apart is a question about the
use being made of them.  So the parties adopt it as a rule, warranted by
RFC 5646's uniqueness discipline, and it enters as declared background.

KGC370 has that rule in force and KGC371 does not.  The policies are
identical, the resource is identical, and the two problems differ in one
include line.  With the rule, no structure interprets German and French as
one language and the verdict is Incompatible.  Without it, some structures
do and some do not, and the verdict is Unknown.

The refutation for KGC370 cites one premise and it belongs to the parties.
That is the point of keeping the declaration in a file of its own: a party
against whom the verdict goes can see exactly what to withdraw, and
withdrawing it is KGC371.

Problem two: what a value names
--------------------------------
"en-US" is a well-formed language tag.  RFC 5646 composes it from the
registered primary subtag 'en' and the registered region subtag 'US', and
any conformant parser accepts it.

It is not a concept of this resource, which holds primary subtags.

Whether it nonetheless resolves to one is the profile's decision, and the
profile declares two rules.  The exact rule resolves an IRI of the scheme
or a literal matching a published notation, and nothing else.  The
reducing rule additionally takes a well-formed tag to its primary subtag,
so "en-US" resolves to 'en'.

KGC372 is read under the first and KGC373 under the second.  Same
policies, same resource, same sort, same declared theory.  Under the exact
rule the request cannot be interpreted at all, no query is built, and the
verdict is Unknown with the value itself as the certificate.  Under the
reducing rule it is interpreted as a request for English, and the pair
gets an ordinary verdict.

Neither rule is the right one.  A party who cares which variety of English
is distributed declines the reduction and would rather have an
uninterpretable policy than a wrong answer; a party who does not, adopts
it.  What matters is that the choice is written down where a reader can
find it, rather than being whatever the software happened to do.

Two verdicts that read the same and are repaired differently
-------------------------------------------------------------
KGC371 and KGC372 both report Unknown.

KGC371's is epistemic.  The resource admits structures that identify the
two subtags and structures that separate them, and a declaration by either
party settles which.  The question is open and someone can close it.

KGC372's is ungrounded.  Nothing has been left open: the policy names
something the binding cannot read at all.  A declaration does not help,
because there is nothing to declare about a value that names no concept.
Either the policy is corrected or the binding is widened, and KGC373 is
the second of those.

A report that gave only the verdict would leave a reader to guess which
repair applies, which is why the reason is part of the answer and not a
gloss on it.

Why the nominal sort is right here, and would not always be
------------------------------------------------------------
The registry publishes Macrolanguage relations over its language subtags,
each of them an order assertion between two subtags.  How many is measured
from the snapshot by the builder and written into the resource header
rather than typed here.

None of the fifteen members of this slice carries one, and the builder
aborts if a future member does.  So the resource genuinely publishes no
order over these concepts, which is what makes the nominal binding right:
there is nothing for isA to read, and the signature rejects it before the
resource is opened.

A slice containing Mandarin and Chinese would carry such a relation and
would belong at tax.  Same publisher, same file, different sort, depending
on which concepts are taken.  This is the only place in the suite where
that is visible.
"""

from compile import Constraint

# Concepts of the slice, as the constants the axiom files declare.
DE = "bcp_de"
FR = "bcp_fr"
EN = "bcp_en"

# What the authority published, and what the parties declared on top of it.
RESOURCE   = "https://w3id.org/odrl-kb/bcp47"
UNIQUENESS = "https://w3id.org/odrl-kb/bcp47/uniqueness"

# The two profile entries.  They differ in the grounding rule and in
# nothing else; both bind odrl:language at nom over the same resource.
BINDING_EXACT   = "https://w3id.org/odrl-kb/profile/b-language-bcp47"
BINDING_PRIMARY = ("https://w3id.org/odrl-kb/profile/"
                   "b-language-bcp47-primary")

# The resource alone, and the resource with the parties' rule.  The
# withdrawal pair is exactly the difference between these two lists.
INCLUDES            = ["KGE000-0.ax", "BCP47000-0.ax"]
INCLUDES_UNIQUENESS = INCLUDES + ["BCP47001-0.ax"]


def C(op, *vals, side="offer"):
    return Constraint(op, tuple(vals), side)


# The case file holds the two policies and nothing else.  Which profile
# reads them, what the expected verdict is, and what evidence supports it
# are recorded here in the manifest and rendered into their own files, so
# that a consumer loading a case file ingests policies rather than claims
# about them.
_TTL_HEAD = """\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix bcp47:   <https://w3id.org/odrl-kb/bcp47#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .
"""


def _offer(pid):
    """The same offer in all four problems: distribution in German."""
    return f"""
drk:offer-{pid[3:]} a odrl:Set ;
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


def _request(pid, title, value, comment="", operator="eq"):
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
    odrl:operator odrl:{operator} ;
    odrl:rightOperand {value} .
"""


# Attached to the request in KGC372 and KGC373, since the value is the
# thing those two problems are about and a reader meeting it in a policy
# file deserves to know why it is there.
EN_US_NOTE = (
    "A well-formed BCP 47 language tag, composed by RFC 5646 from the "
    "registered primary subtag en and the registered region subtag US. It "
    "is not itself an entry of the registry and not a concept of the "
    "resource this operand is bound to, which holds primary subtags. "
    "Whether it resolves to one is the profile's grounding rule to decide, "
    "and the two problems using this request are read under rules that "
    "decide it differently."
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
         "smt2_background":
        "(assert (! (not (= bcp_de bcp_fr)) "
        ":named bg_dist_bcp47_de_fr))",
        "binding":           BINDING_EXACT,
        "includes":          INCLUDES_UNIQUENESS,
        "tree": [C("eq", DE), C("eq", FR, side="request")],
        "description": (
            "A publisher distributes a dataset in German. A reuser asks "
            "to distribute it in French. Both constraints are on "
            "odrl:language, which this profile binds to a fifteen-subtag "
            "slice of the IANA Language Subtag Registry at the nominal "
            "sort.\n\n"
            "The parties have adopted the registry-uniqueness rule: "
            "distinct primary subtag records, neither deprecated and with "
            "no Preferred-Value link between them, name distinct "
            "languages. With that rule in force no structure interprets "
            "de and fr as one language, so no single use satisfies both "
            "constraints, and the verdict is Incompatible.\n\n"
            "The refutation cites one premise, and it is the parties' "
            "rather than the registry's. IANA lists both subtags and "
            "asserts nothing that separates them; what makes this verdict "
            "definite is a declaration, and a party who withdraws it "
            "reopens the case. KGC371 is that withdrawal."
        ),
        "expected_verdict": "Incompatible",
        "expected_q1": "Unsatisfiable",
        "expected_q2": "Satisfiable",
        "certificate": {
            "kind": "Refutation",
            "comment": "The two subtags are declared to name distinct "
                       "languages, which is the parties' rule and not the "
                       "registry's content. Withdrawing it returns the "
                       "verdict to Unknown, which is KGC371.",
            "premises": [
                ("fromBackgroundTheory",
                 "bcp47:de and bcp47:fr are declared distinct, on RFC "
                 "5646's registry uniqueness"),
            ],
        },
        "ttl": _TTL_HEAD + _offer("KGC370")
               + _request("KGC370", "Distribution in French", "bcp47:fr"),
    },

    {
        "id":                "KGC371",
        "subdir":            "verdict",
        "name":              "language, eq de against eq fr, "
                             "declaration withdrawn",
        "left_operand":      "language",
        "sort":              "nom",
        "resource":          RESOURCE,
        # No background theory: withdrawal is the absence of a declaration,
        # not the presence of an empty one.
        "background_theory": None,
        "binding":           BINDING_EXACT,
        "includes":          INCLUDES,
        "tree": [C("eq", DE), C("eq", FR, side="request")],
        "description": (
            "The policies of KGC370, over the same resource, with the "
            "registry-uniqueness rule withdrawn.\n\n"
            "The registry still lists both subtags and still asserts "
            "nothing that separates them. So some structures admitted by "
            "the resource interpret de and fr as one language and others "
            "keep them apart, and whether a single use can satisfy both "
            "constraints depends on which. The verdict is Unknown, and "
            "the reason is epistemic: a declaration by either party "
            "settles it.\n\n"
            "Read against KGC370 this is what a withdrawable premise "
            "means. Two identical policies over one vocabulary, one "
            "include line apart, and the verdict moves from definite to "
            "open because a party stopped asserting something the "
            "registry never asserted."
        ),
        "expected_verdict": "Unknown",
        "unknown_reason":   "epistemic",
        "expected_q1": "Satisfiable",
        "expected_q2": "Satisfiable",
        "certificate": {
            "kind": "Models",
            "comment": "Both queries are satisfiable. One certifying "
                       "structure interprets bcp47:de and bcp47:fr as one "
                       "concept and the other keeps them apart; the "
                       "registry decides neither.",
            "premises": [],
        },
        "ttl": _TTL_HEAD + _offer("KGC371")
               + _request("KGC371", "Distribution in French", "bcp47:fr"),
    },

    {
        # No queries are built for this problem. writers.py reads the
        # ungrounded field and skips construction, so no expected_q1 or
        # expected_q2 appears below, and no tree either: supplying one
        # would turn the unresolved value into a constant of the
        # signature, which is the collapse this problem exists to rule
        # out. A prover asked about such a constant would answer, and the
        # answer would be about nothing.
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
            "A publisher distributes in German. A reuser asks to "
            "distribute in en-US.\n\n"
            "That is a well-formed language tag: RFC 5646 composes it "
            "from the registered primary subtag en and the registered "
            "region subtag US, and any conformant parser accepts it. It "
            "is not a concept of the resource this operand is bound to, "
            "which holds primary subtags.\n\n"
            "This problem is read under the profile's exact grounding "
            "rule, which resolves an IRI of the scheme or a literal "
            "matching a published notation, and nothing else. The "
            "request's right operand matches neither, so the policy "
            "cannot be interpreted against this resource at all: no query "
            "is built, and the verdict is Unknown with the value itself "
            "as the certificate.\n\n"
            "The reason is ungrounded, not epistemic, and the difference "
            "decides the repair. An epistemic Unknown is settled by a "
            "declaration. This one is not: nothing has been left open, "
            "and there is nothing to declare about a value that names no "
            "concept. Either the policy is corrected or the binding is "
            "widened, and KGC373 is the same pair read under a wider "
            "binding."
        ),
        "expected_verdict": "Unknown",
        "unknown_reason":   "ungrounded",
        "certificate": {
            "kind": "Ungrounded",
            "comment": "The value en-US resolves to no concept of the "
                       "resource under this binding's grounding rule. "
                       "Checkable by applying that rule to the value and "
                       "seeing that it yields nothing.",
            "premises": [],
        },
        "ttl": _TTL_HEAD + _offer("KGC372")
               + _request("KGC372", "Distribution in American English",
                          '"en-US"', EN_US_NOTE),
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
        "summary": (
    "A publisher distributes in German, while a reuser requests American "
    "English."
),
        "smt2_background":
            "(assert (! (not (= bcp_de bcp_en)) "
            ":named bg_dist_bcp47_de_en))",
        "binding":           BINDING_PRIMARY,
        "includes":          INCLUDES_UNIQUENESS,
        "grounding": {"en-US": "bcp_en"},
        "tree": [C("eq", DE), C("eq", "en-US", side="request")],
        "description": (
            "The policies of KGC372, read under the profile's other "
            "grounding rule.\n\n"
            "That rule takes a well-formed language tag to its primary "
            "subtag, so en-US resolves to en. The request becomes "
            "interpretable and the pair gets an ordinary verdict: German "
            "and English are declared distinct under the same "
            "registry-uniqueness rule as KGC370, so no use satisfies both "
            "constraints and the verdict is Incompatible.\n\n"
            "Neither rule is the correct one. A party who cares which "
            "variety of English is distributed declines the reduction and "
            "would rather have an uninterpretable policy than a wrong "
            "answer; a party who does not, adopts it. The two problems "
            "return different verdicts on identical policies over an "
            "identical vocabulary, and the parties disagree about no "
            "concept: what differs is a reading rule, which the profile "
            "records and a report cites."
        ),
        "expected_verdict": "Incompatible",
        "expected_q1": "Unsatisfiable",
        "expected_q2": "Satisfiable",
        "certificate": {
            "kind": "Refutation",
           "comment": (
        "en-US resolves to English, which is distinct from German."
    ),
            "premises": [
                ("fromBackgroundTheory",
                 "bcp47:de and bcp47:en are declared distinct, on RFC "
                 "5646's registry uniqueness"),
            ],
        },
        "ttl": _TTL_HEAD + _offer("KGC373")
               + _request("KGC373", "Distribution in American English",
                          '"en-US"', EN_US_NOTE),
    },
        {
        "id":                "KGC374",
        "subdir":            "verdict",
        "name":              "language, eq de against neq fr, "
                             "registry uniqueness declared",
        "left_operand":      "language",
        "sort":              "nom",
        "resource":          RESOURCE,
        "background_theory": UNIQUENESS,
         "smt2_background":
        "(assert (! (not (= bcp_de bcp_fr)) "
        ":named bg_dist_bcp47_de_fr))",
        "binding":           BINDING_EXACT,
        "includes":          INCLUDES_UNIQUENESS,
        "tree": [C("eq", DE), C("neq", FR, side="request")],
        "expected_verdict":  "Compatible",
        "expected_q1":       "Satisfiable",
        "expected_q2":       "Unsatisfiable",
"summary": (
    "A publisher distributes in German, while a reuser accepts any "
    "language except French."
),
        "description": (
            "The publisher distributes in German; the reuser accepts "
            "anything that is not French. German itself is the witness, "
            "but only because the parties' uniqueness rule separates the "
            "two subtags: in a structure interpreting de and fr as one "
            "language, a use in German is a use in French and the "
            "request excludes it.\n\n"
            "So this Compatible rests on a declared premise exactly as "
            "KGC370's Incompatible does. The refutation of the second "
            "query cites the witness condition and one background "
            "premise, and withdrawing that premise is KGC375. A definite "
            "verdict of either polarity can stand on the parties' "
            "declaration; polarity buys no exemption from provenance."
        ),
        "certificate": {
            "kind": "Refutation",
"description": (
    "The uniqueness rule is withdrawn. German and French may denote the "
    "same language or different languages, so the verdict is Unknown."
),
            "premises": [
                ("fromBackgroundTheory",
                 "bcp47:de and bcp47:fr are declared distinct, on RFC "
                 "5646's registry uniqueness"),
            ],
        },
        "ttl": _TTL_HEAD + _offer("KGC374")
               + _request("KGC374", "Anything but French",
                          "bcp47:fr", operator="neq"),
    },
    {
        "id":                "KGC375",
        "subdir":            "verdict",
        "name":              "language, eq de against neq fr, "
                             "no declaration",
        "left_operand":      "language",
        "sort":              "nom",
        "resource":          RESOURCE,
        "background_theory": None,
        "binding":           BINDING_EXACT,
        "includes":          INCLUDES,
        "tree": [C("eq", DE), C("neq", FR, side="request")],
        "expected_verdict":  "Unknown",
        "unknown_reason":    "epistemic",
        "expected_q1":       "Satisfiable",
        "expected_q2":       "Satisfiable",
        "summary": (
    "A publisher distributes in German, while a reuser accepts any "
    "language except French."
),
        "description": (
            "KGC374 with the uniqueness rule withdrawn. A structure "
            "separating de and fr admits the witness; a structure "
            "identifying them admits none, because a use in German is "
            "then a use in French. The registry decides neither, so the "
            "verdict is Unknown.\n\n"
            "Read with KGC370 and KGC371 this completes the symmetry: "
            "the same withdrawal takes an Incompatible to Unknown there "
            "and a Compatible to Unknown here. What the declaration "
            "buys is definiteness, not a direction."
        ),
        "certificate": {
            "kind": "Models",
           "description": (
    "The uniqueness rule is withdrawn. German and French may denote the "
    "same language or different languages, so the verdict is Unknown."
),
            "premises": [],
        },
        "ttl": _TTL_HEAD + _offer("KGC375")
               + _request("KGC375", "Anything but French",
                          "bcp47:fr", operator="neq"),
    },
]