"""
problem_data_bcp47.py
=====================
Eleven problems over the BCP 47 language slice, at the nominal sort.

    KGC370  eq de  x  eq fr         distinctness declared Incompatible
    KGC371  eq de  x  eq fr         declaration withdrawn Unknown
    KGC372  eq de  x  eq "en-US"    exact grounding       rejected, does not ground
    KGC373  eq de  x  eq "en-US"    reducing grounding    Incompatible
    KGC374  eq de  x  neq fr        distinctness declared Compatible
    KGC375  eq de  x  neq fr        declaration withdrawn Unknown
    KGC376  isAllOf {nl, fr}  x  eq nl      distinctness declared Incompatible
    KGC377  isNoneOf {en, it} x  eq it      no declaration        Incompatible
    KGC378  or(eq de, eq fr)  x  eq fr      no declaration        Compatible
    KGC379  xone(eq de, eq fr) x eq de      no declaration        Unknown
    KGC398  isAnyOf {de, fr} x isAllOf {nl, fr}  no declaration   Compatible

The first six use eq and neq on one pair of subtags.  Each pair among them
changes one thing and holds everything else fixed, so that the change is
what the verdict responds to.

    370 -> 371   one set of declarations withdrawn
    372 -> 373   one grounding rule widened
    371 vs 372   an Unknown and a rejection, repaired differently
    374 -> 375   one set of declarations withdrawn

KGC376 to KGC379 are not paired.  They take the set operators and the two
connectives the first six leave out, each in a licensing scenario.  KGC377
and KGC378 are the only definite verdicts here that no declaration can
change: they hold with the registry rule and without it, which is why they
declare nothing.

A note on reading these
-----------------------
The two policies in each problem are ordinary ODRL Set policies: one
permits distribution in German, the other commits to distribution in some
other language.  Nothing in them is unusual, and a reader who knows ODRL and not
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
RFC 5646's requirement that Description fields be unique, and it enters
as a declaration.

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
policies, same resource, same sort, same declarations.  Under the exact
rule the second policy's value cannot be interpreted at all.  Its
constraint is rejected, no query is built, and the value itself is the
evidence.  Under the reducing rule the value is read as English, and the
pair gets an ordinary verdict.

Neither rule is the right one.  A party who cares which variety of English
is distributed declines the reduction and would rather have an
uninterpretable policy than a wrong answer; a party who does not, adopts
it.  What matters is that the choice is written down where a reader can
find it, rather than being whatever the software happened to do.

An Unknown and a rejection
--------------------------
KGC371 is Unknown.  The resource admits structures that identify the two
subtags and structures that separate them, and a declaration by either
party decides which.  The question is open and someone can close it.

KGC372 has no verdict.  Nothing has been left open: the policy names
something the binding cannot read at all.  A declaration does not help,
because there is nothing to declare about a value that names no concept.
Either the policy is corrected or the binding is widened, and KGC373 is
the second of those.  So the constraint is rejected, as an ill-sorted
constraint is, and the case gets a grounding report instead of a verdict.

Why the nominal sort is right here, and would not always be
------------------------------------------------------------
The registry publishes Macrolanguage relations over its language subtags,
each of them an order statement between two subtags.  How many is measured
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

from pathlib import Path

import declarations
from compile import Constraint, Or, Xone, right_operand

# Concepts of the slice, as the constants the axiom files declare.
DE = "bcp_de"
FR = "bcp_fr"
EN = "bcp_en"
IT = "bcp_it"
NL = "bcp_nl"

# What the authority published, and what the parties declared on top of it.
RESOURCE   = "https://w3id.org/odrl-kb/bcp47"
DISTINCT = "https://w3id.org/odrl-kb/bcp47/distinct"
EMPTY_BT   = "https://w3id.org/odrl-kb/bcp47/empty"

# The two profile entries.  They differ in the grounding rule and in
# nothing else; both bind odrl:language at nom over the same resource.
BINDING_EXACT   = "https://w3id.org/odrl-kb/profile/b-language-bcp47"
BINDING_PRIMARY = ("https://w3id.org/odrl-kb/profile/"
                   "b-language-bcp47-primary")

# The resource alone, and the resource with the parties' rule.  The
# withdrawal pair is exactly the difference between these two lists.
INCLUDES            = ["KGE000-0.ax", "BCP47000-0.ax"]
INCLUDES_DISTINCT = INCLUDES + ["BCP47001-0.ax"]


def C(op, *vals, side="offer"):
    return Constraint(op, tuple(vals), side)


_DECL = declarations.load(
    Path(__file__).resolve().parent.parent / "problems" / "background"
    / "bcp47-distinct.ttl")


def _smt_dist(*pairs):
    """The SMT-LIB side of the distinctness a problem adopts.  The TPTP
    side takes the same statements from BCP47001-0.ax, by include.  The
    labels name the notations: bg_dist_bcp47_de_fr."""
    return declarations.instances(
        _DECL, pairs, [], [],
        label=lambda a, b: f"bg_dist_bcp47_{a[4:]}_{b[4:]}")[1]


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
drk:policy-{pid[3:]}-1 a odrl:Set ;
    odrl:uid drk:policy-{pid[3:]}-1 ;
    dcterms:title "Distribute in German only"@en ;
    odrl:assigner drk:publisher ;
    odrl:permission kgc:{pid}-p1-r1 .

kgc:{pid}-p1-r1 a odrl:Permission ;
    odrl:action odrl:distribute ;
    odrl:target drk:work ;
    odrl:constraint kgc:{pid}-p1-c1 .

kgc:{pid}-p1-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:language ;
    odrl:operator odrl:eq ;
    odrl:rightOperand bcp47:de .
"""


def _request(pid, title, value, comment="", operator="eq"):
    note = f'\n    rdfs:comment """{comment}"""@en ;' if comment else ""
    return f"""
drk:policy-{pid[3:]}-2 a odrl:Set ;
    odrl:uid drk:policy-{pid[3:]}-2 ;
    dcterms:title "{title}"@en ;{note}
    odrl:assignee drk:licensee ;
    odrl:permission kgc:{pid}-p2-r1 .

kgc:{pid}-p2-r1 a odrl:Permission ;
    odrl:action odrl:distribute ;
    odrl:target drk:work ;
    odrl:constraint kgc:{pid}-p2-c1 .

kgc:{pid}-p2-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:language ;
    odrl:operator odrl:{operator} ;
    odrl:rightOperand {value} .
"""


def _policy(pid, k, title, constraints, connective=None):
    """Policy k (1 or 2) of a problem whose constraints are not a single eq.

    constraints is a list of (operator, [constants]); two or more are
    written as one Logical Constraint under the connective.  A set
    operator's values are written as an RDF collection.
    """
    n, role = pid[3:], f"p{k}"
    party = ("odrl:assigner drk:publisher" if k == 1
             else "odrl:assignee drk:licensee")
    cids = [f"{pid}-{role}-c{i + 1}" for i in range(len(constraints))]
    if len(cids) == 1:
        cref, lc = f"kgc:{cids[0]}", ""
    else:
        cref = f"kgc:{pid}-{role}-lc"
        lc = (f"\nkgc:{pid}-{role}-lc a odrl:LogicalConstraint ;\n"
              f"    odrl:{connective} ( "
              + " ".join(f"kgc:{c}" for c in cids) + " ) .\n")
    body = f"""
drk:policy-{n}-{k} a odrl:Set ;
    odrl:uid drk:policy-{n}-{k} ;
    dcterms:title "{title}"@en ;
    {party} ;
    odrl:permission kgc:{pid}-{role}-r1 .

kgc:{pid}-{role}-r1 a odrl:Permission ;
    odrl:action odrl:distribute ;
    odrl:target drk:work ;
    odrl:constraint {cref} .
""" + lc
    for cid, (op, consts) in zip(cids, constraints):
        ro = right_operand(op, [f"bcp47:{c[len('bcp_'):]}" for c in consts])
        body += f"""
kgc:{cid} a odrl:Constraint ;
    odrl:leftOperand odrl:language ;
    odrl:operator odrl:{op} ;
    odrl:rightOperand {ro} .
"""
    return body


# Attached to the second policy's constraint in KGC372 and KGC373, since the value is the
# thing those two problems are about and a reader meeting it in a policy
# file deserves to know why it is there.
EN_US_NOTE = (
    "A well-formed BCP 47 language tag, composed by RFC 5646 from the "
    "registered primary subtag en and the registered region subtag US. It "
    "is not itself an entry of the registry and not a concept of the "
    "resource this operand is bound to, which holds primary subtags. "
    "Whether it resolves to one is the profile's grounding rule to decide, "
    "and the two problems using this value are read under rules that "
    "decide it differently."
)


PROBLEMS = [

    {
        "id":                "KGC370",
        "twin":              "KGC371",
        "subdir":            "verdict",
        "name":              "language, eq de against eq fr, "
                             "distinctness rule declared",
        "left_operand":      "language",
        "sort":              "nom",
        "resource":          RESOURCE,
        "background_theory": DISTINCT,
         "smt2_background": _smt_dist((DE, FR)),
        "binding":           BINDING_EXACT,
        "includes":          INCLUDES_DISTINCT,
        "tree": [C("eq", DE), C("eq", FR, side="request")],
        "description": (
            "A publisher distributes a work in German. A licensee's policy "
            "commits to distributing it in French. Both constraints are on "
            "odrl:language, which this profile binds to a fifteen-subtag "
            "slice of the IANA Language Subtag Registry at the nominal "
            "sort.\n\n"
            "The parties have adopted the distinctness rule: "
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
        "summary": (
            "A publisher distributes in German. A licensee's policy commits to "
            "French. The parties adopt the registry rule that different "
            "primary subtags name different languages."),
        "certificate": {
            "kind": "Refutation",
            "comment": "The two subtags are declared to name distinct "
                       "languages, which is the parties' rule and not the "
                       "registry's content. Withdrawing it returns the "
                       "verdict to Unknown, which is KGC371.",
            "premises": [
                ("fromDeclarations",
                 "bcp47:de and bcp47:fr are declared distinct, by the "
                 "distinctness rule"),
            ],
        },
        "ttl": _TTL_HEAD + _offer("KGC370")
               + _request("KGC370", "Distribute in French only", "bcp47:fr"),
    },

    {
        "id":                "KGC371",
        "twin":              "KGC370",
        "subdir":            "verdict",
        "name":              "language, eq de against eq fr, "
                             "declaration withdrawn",
        "left_operand":      "language",
        "sort":              "nom",
        "resource":          RESOURCE,
        # No declarations: withdrawal is the absence of a declaration,
        # not the presence of an empty one.
        "background_theory": EMPTY_BT,
        "binding":           BINDING_EXACT,
        "includes":          INCLUDES,
        "tree": [C("eq", DE), C("eq", FR, side="request")],
        "description": (
            "The policies of KGC370, over the same resource, with the "
            "distinctness rule withdrawn.\n\n"
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
        "expected_q1": "Satisfiable",
        "expected_q2": "Satisfiable",
        "summary": (
            "As KGC370, without the registry rule."),
        "certificate": {
            "kind": "Models",
            "comment": "Both queries are satisfiable. One certifying "
                       "structure interprets bcp47:de and bcp47:fr as one "
                       "concept and the other keeps them apart; the "
                       "registry decides neither.",
            "premises": [],
        },
        "ttl": _TTL_HEAD + _offer("KGC371")
               + _request("KGC371", "Distribute in French only", "bcp47:fr"),
    },

    {
        # No queries are built for this problem. writers.py reads the
        # ungrounded field, skips construction and writes a grounding
        # report, so no expected verdict, expected_q1 or expected_q2
        # appears below, and no tree either: supplying one
        # would turn the unresolved value into a constant of the
        # signature, which is the collapse this problem exists to rule
        # out. A prover asked about such a constant would answer, and the
        # answer would be about nothing.
        "id":                "KGC372",
        "twin":              "KGC373",
        "subdir":            "verdict",
        "name":              "language, eq de against eq \"en-US\", "
                             "exact grounding",
        "left_operand":      "language",
        "sort":              "nom",
        "resource":          RESOURCE,
        "background_theory": DISTINCT,
        "binding":           BINDING_EXACT,
        "includes":          INCLUDES_DISTINCT,
        "ungrounded":        "en-US",
        "description": (
            "A publisher distributes in German. A licensee's policy commits "
            "to distributing in en-US.\n\n"
            "That is a well-formed language tag: RFC 5646 composes it "
            "from the registered primary subtag en and the registered "
            "region subtag US, and any conformant parser accepts it. It "
            "is not a concept of the resource this operand is bound to, "
            "which holds primary subtags.\n\n"
            "This problem is read under the profile's exact grounding "
            "rule, which resolves an IRI of the scheme or a literal "
            "matching a published notation, and nothing else. The "
            "second policy's right operand matches neither, so its "
            "constraint cannot be interpreted against this resource at "
            "all. The constraint is rejected, no query is built, and the "
            "value itself is the evidence.\n\n"
            "This is not an Unknown, and the difference decides the "
            "repair. An Unknown is resolved by a declaration. A rejection "
            "is not: nothing has been left open, "
            "and there is nothing to declare about a value that names no "
            "concept. Either the policy is corrected or the binding is "
            "widened, and KGC373 is the same pair read under a wider "
            "binding."
        ),
        "summary": (
            "A publisher distributes in German. A licensee's policy commits to "
            "American English (en-US), under the exact-match grounding rule."),
        "certificate": {
            "kind": "Ungrounded",
            "comment": "Under the exact-match rule, the value en-US "
                       "resolves to no concept of the resource. The "
                       "constraint is therefore rejected, and no verdict "
                       "is computed. KGC373 reads the same value under the "
                       "rule that reduces it to en.",
            "premises": [],
        },
        "ttl": _TTL_HEAD + _offer("KGC372")
               + _request("KGC372", "Distribute in American English only",
                          '"en-US"', EN_US_NOTE),
    },

    {
        "id":                "KGC373",
        "twin":              "KGC372",
        "subdir":            "verdict",
        "name":              "language, eq de against eq \"en-US\", "
                             "primary-subtag grounding",
        "left_operand":      "language",
        "sort":              "nom",
        "resource":          RESOURCE,
        "background_theory": DISTINCT,
        "summary": (
            "A publisher distributes in German. A licensee's policy commits to "
            "American English (en-US), under the rule that reduces a tag to "
            "its primary subtag."),
        "smt2_background": _smt_dist((DE, EN)),
        "binding":           BINDING_PRIMARY,
        "includes":          INCLUDES_DISTINCT,
        "grounding": {"en-US": "bcp_en"},
        "tree": [C("eq", DE), C("eq", "en-US", side="request")],
        "description": (
            "The policies of KGC372, read under the profile's other "
            "grounding rule.\n\n"
            "That rule takes a well-formed language tag to its primary "
            "subtag, so en-US resolves to en. The value becomes "
            "interpretable and the pair gets an ordinary verdict: German "
            "and English are declared distinct under the same "
            "distinctness rule as KGC370, so no use satisfies both "
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
               "en-US reduces to English, which the registry rule makes "
               "distinct from German."),
            "premises": [
                ("fromDeclarations",
                 "bcp47:de and bcp47:en are declared distinct, by the "
                 "distinctness rule"),
            ],
        },
        "ttl": _TTL_HEAD + _offer("KGC373")
               + _request("KGC373", "Distribute in American English only",
                          '"en-US"', EN_US_NOTE),
    },
        {
        "id":                "KGC374",
        "twin":              "KGC375",
        "subdir":            "verdict",
        "name":              "language, eq de against neq fr, "
                             "distinctness rule declared",
        "left_operand":      "language",
        "sort":              "nom",
        "resource":          RESOURCE,
        "background_theory": DISTINCT,
         "smt2_background": _smt_dist((DE, FR)),
        "binding":           BINDING_EXACT,
        "includes":          INCLUDES_DISTINCT,
        "tree": [C("eq", DE), C("neq", FR, side="request")],
        "expected_verdict":  "Compatible",
        "expected_q1":       "Satisfiable",
        "expected_q2":       "Unsatisfiable",
"summary": (
    "A publisher distributes in German. A licensee's policy accepts any "
    "language except French."),
        "description": (
            "The publisher distributes in German; the licensee accepts "
            "anything that is not French. German itself is the witness, "
            "but only because the parties' distinctness rule separates the "
            "two subtags: in a structure interpreting de and fr as one "
            "language, a use in German is a use in French and the "
            "second policy excludes it.\n\n"
            "So this Compatible rests on a declared premise exactly as "
            "KGC370's Incompatible does. The refutation of the second "
            "query cites the witness condition and one "
            "declaration, and withdrawing that premise is KGC375. A definite "
            "verdict of either polarity can stand on the parties' "
            "declaration; polarity buys no exemption from provenance."
        ),
        "certificate": {
            "kind": "Refutation",
            "comment": (
                "The registry rule the parties adopt makes different primary "
                "subtags name different languages, so German is not French, "
                "and a use in German satisfies both policies."),
            "premises": [
                ("fromDeclarations",
                 "bcp47:de and bcp47:fr are declared distinct, by the "
                 "distinctness rule"),
            ],
        },
        "ttl": _TTL_HEAD + _offer("KGC374")
               + _request("KGC374", "Distribute in any language except French",
                          "bcp47:fr", operator="neq"),
    },
    {
        "id":                "KGC375",
        "twin":              "KGC374",
        "subdir":            "verdict",
        "name":              "language, eq de against neq fr, "
                             "no declaration",
        "left_operand":      "language",
        "sort":              "nom",
        "resource":          RESOURCE,
        "background_theory": EMPTY_BT,
        "binding":           BINDING_EXACT,
        "includes":          INCLUDES,
        "tree": [C("eq", DE), C("neq", FR, side="request")],
        "expected_verdict":  "Unknown",
        "expected_q1":       "Satisfiable",
        "expected_q2":       "Satisfiable",
        "summary": (
            "As KGC374, without the registry rule."),
        "description": (
            "KGC374 with the distinctness rule withdrawn. A structure "
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
            "comment": (
                "Nothing states that German and French are different languages. In a "
                "structure that keeps them apart, a use in German satisfies both "
                "policies. In a structure that identifies them, a use in German is a "
                "use in French, and the second policy excludes it. So the verdict is "
                "Unknown."),
            "premises": [],
        },
        "ttl": _TTL_HEAD + _offer("KGC375")
               + _request("KGC375", "Distribute in any language except French",
                          "bcp47:fr", operator="neq"),
    },

    {
        "id":                "KGC376",
        "subdir":            "verdict",
        "name":              "language, isAllOf nl fr against eq nl, "
                             "distinctness rule declared",
        "left_operand":      "language",
        "sort":              "nom",
        "resource":          RESOURCE,
        "background_theory": DISTINCT,
        "binding":           BINDING_EXACT,
        "includes":          INCLUDES_DISTINCT,
        "tree": [C("isAllOf", NL, FR), C("eq", NL, side="request")],
        "expected_verdict":  "Incompatible",
        "expected_q1":       "Unsatisfiable",
        "expected_q2":       "Satisfiable",
        "summary": (
            "A Belgian federal publisher requires distribution in both "
            "Dutch and French. The licensee distributes in Dutch only. The "
            "parties adopt the registry rule that different primary "
            "subtags name different languages."),
        "description": (
            "A Belgian federal publisher requires distribution in both "
            "Dutch and French. The licensee's policy commits to Dutch "
            "only. Both constraints are on odrl:language, bound to the "
            "BCP 47 slice at the nominal sort.\n\n"
            "isAllOf asks that the languages of the use include both "
            "Dutch and French. eq asks that every language of the use is "
            "Dutch. The two hold together only if Dutch and French are "
            "one language. The parties have adopted the registry rule, "
            "which makes the two subtags distinct languages, so no use "
            "satisfies both policies and the verdict is Incompatible.\n\n"
            "The refutation cites one premise, and it is the parties' "
            "rather than the registry's. Without that rule the registry "
            "separates the two subtags in some structures and not in "
            "others, and the verdict is Unknown."
        ),
        "certificate": {
            "kind": "Refutation",
            "comment": (
                "Dutch and French are declared distinct languages. A use "
                "in both is not a use in Dutch only, so no use satisfies "
                "both policies."),
            "premises": [
                ("fromDeclarations",
                 "bcp47:fr and bcp47:nl are declared distinct, by the "
                 "distinctness rule"),
            ],
        },
        "ttl": _TTL_HEAD
               + _policy("KGC376", 1, "Distribute in both Dutch and French",
                         [("isAllOf", [NL, FR])])
               + _policy("KGC376", 2, "Distribute in Dutch only",
                         [("eq", [NL])]),
    },

    {
        "id":                "KGC377",
        "subdir":            "verdict",
        "name":              "language, isNoneOf en it against eq it, "
                             "no declaration",
        "left_operand":      "language",
        "sort":              "nom",
        "resource":          RESOURCE,
        "background_theory": EMPTY_BT,
        "binding":           BINDING_EXACT,
        "includes":          INCLUDES,
        "tree": [C("isNoneOf", EN, IT), C("eq", IT, side="request")],
        "expected_verdict":  "Incompatible",
        "expected_q1":       "Unsatisfiable",
        "expected_q2":       "Satisfiable",
        "summary": (
            "English and Italian rights were sold separately, so a "
            "publisher permits any language except English and Italian. "
            "The licensee distributes in Italian."),
        "description": (
            "English and Italian rights were sold separately, so a "
            "publisher permits distribution in any language except "
            "English and Italian. The licensee's policy commits to "
            "Italian.\n\n"
            "isNoneOf excludes the listed subtags by identity. Italian is "
            "listed, and the licensee's eq asks for Italian. No structure "
            "admits a language that is Italian and is not Italian, so the "
            "verdict is Incompatible.\n\n"
            "The registry rule is not used. The verdict is the same with "
            "it and without it, which is why this case declares "
            "nothing. The definite verdicts of KGC370 to KGC375 all rest "
            "on that rule."
        ),
        "certificate": {
            "kind": "Refutation",
            "comment": (
                "The first policy excludes Italian and the second policy "
                "requires it. This holds in every structure, so no "
                "declaration is used."),
            "premises": [],
        },
        "ttl": _TTL_HEAD
               + _policy("KGC377", 1,
                         "Distribute in any language except English and Italian",
                         [("isNoneOf", [EN, IT])])
               + _policy("KGC377", 2, "Distribute in Italian only",
                         [("eq", [IT])]),
    },

    {
        "id":                "KGC378",
        "subdir":            "verdict",
        "name":              "language, or(eq de, eq fr) against eq fr, "
                             "no declaration",
        "left_operand":      "language",
        "sort":              "nom",
        "resource":          RESOURCE,
        "background_theory": EMPTY_BT,
        "binding":           BINDING_EXACT,
        "includes":          INCLUDES,
        "tree": [Or((C("eq", DE), C("eq", FR))),
                 C("eq", FR, side="request")],
        "expected_verdict":  "Compatible",
        "expected_q1":       "Satisfiable",
        "expected_q2":       "Unsatisfiable",
        "summary": (
            "A translation licence covers a German or a French edition. "
            "The licensee publishes in French."),
        "description": (
            "A translation licence covers a German edition or a French "
            "edition. The licensee's policy commits to French.\n\n"
            "The second alternative of the or is French, which is the "
            "licensee's language. A use in French satisfies both policies "
            "in every structure, so the verdict is Compatible. The first "
            "alternative matters only if German and French are one "
            "language, and the verdict does not depend on that. No "
            "declaration is used."
        ),
        "certificate": {
            "kind": "Refutation",
            "comment": (
                "French is the second alternative of the licence and the "
                "licensee's language, so a use in French satisfies both "
                "policies in every structure."),
            "premises": [],
        },
        "ttl": _TTL_HEAD
               + _policy("KGC378", 1, "Distribute in German only or in French only",
                         [("eq", [DE]), ("eq", [FR])], connective="or")
               + _policy("KGC378", 2, "Distribute in French only",
                         [("eq", [FR])]),
    },

    {
        "id":                "KGC379",
        "subdir":            "verdict",
        "name":              "language, xone(eq de, eq fr) against eq de, "
                             "no declaration",
        "left_operand":      "language",
        "sort":              "nom",
        "resource":          RESOURCE,
        "background_theory": EMPTY_BT,
        "binding":           BINDING_EXACT,
        "includes":          INCLUDES,
        "tree": [Xone((C("eq", DE), C("eq", FR))),
                 C("eq", DE, side="request")],
        "expected_verdict":  "Unknown",
        "expected_q1":       "Satisfiable",
        "expected_q2":       "Satisfiable",
        "summary": (
            "A licence for a single-language edition allows exactly one of "
            "German and French. The licensee publishes in German."),
        "description": (
            "A licence for a single-language edition allows exactly one "
            "of German and French. The licensee's policy commits to "
            "German.\n\n"
            "xone holds when one alternative holds and the other does not. "
            "A German edition satisfies the first alternative. Whether it "
            "fails the second depends on whether German and French are "
            "one language, and the registry does not state that they are "
            "different. So the verdict is Unknown.\n\n"
            "A declaration by either party decides it. With the registry "
            "rule in force the verdict is Compatible."
        ),
        "certificate": {
            "kind": "Models",
            "comment": (
                "Nothing states that German and French are different "
                "languages. In a structure that keeps them apart, a use in "
                "German satisfies the first alternative only, so both "
                "policies hold. In a structure that identifies them, a use "
                "in German satisfies both alternatives, and exactly one "
                "fails. So the verdict is Unknown."),
            "premises": [],
        },
        "ttl": _TTL_HEAD
               + _policy("KGC379", 1, "Distribute in exactly one language, German or French",
                         [("eq", [DE]), ("eq", [FR])], connective="xone")
               + _policy("KGC379", 2, "Distribute in German only",
                         [("eq", [DE])]),
    },
    {
        "id":                "KGC398",
        "subdir":            "verdict",
        "name":              "language, isAnyOf {de, fr} against isAllOf "
                             "{nl, fr}, no declaration",
        "left_operand":      "language",
        "sort":              "nom",
        "resource":          RESOURCE,
        "background_theory": EMPTY_BT,
        "binding":           BINDING_EXACT,
        "includes":          INCLUDES,
        "tree": [C("isAnyOf", DE, FR),
                 C("isAllOf", NL, FR, side="request")],
        "expected_verdict":  "Compatible",
        "expected_q1":       "Satisfiable",
        "expected_q2":       "Unsatisfiable",
        "summary": (
            "A translation licence covers at least one of a German and a "
            "French edition. The licensee publishes in both Dutch and "
            "French."),
        "description": (
            "A translation licence covers a German edition, a French "
            "edition, or both. The licensee's policy commits to a Dutch and "
            "a French edition together.\n\n"
            "isAnyOf asks that the languages of the use include at least "
            "one of German and French. isAllOf asks that they include both "
            "Dutch and French. A use in Dutch and French together "
            "satisfies both policies: French is on the licence's list and "
            "in the licensee's pair. French is the same concept as itself "
            "in every structure, so the verdict is Compatible whether or "
            "not Dutch and French differ, and no declaration is used. "
            "KGC376 puts the same isAllOf on the other side, against Dutch "
            "only, and there the verdict does need the distinctness rule."
        ),
        "certificate": {
            "kind": "Refutation",
            "comment": (
                "French is on the licence's list and in the licensee's "
                "pair, so a use in Dutch and French satisfies both "
                "policies in every structure."),
            "premises": [],
        },
        "ttl": _TTL_HEAD
               + _policy("KGC398", 1, "Distribute in at least one of German and French",
                         [("isAnyOf", [DE, FR])])
               + _policy("KGC398", 2, "Distribute in both Dutch and French",
                         [("isAllOf", [NL, FR])]),
    },
]