"""
problem_data_filetype.py
========================
Four problems over the EU File Type table, at nom.

    KGC320  eq PDF x eq PDFA1A
            -> Unknown       the resource provides no relation between them

    KGC321  same pair with declared distinctness
            -> Incompatible  the declaration separates the two concepts

    KGC322  isAnyOf {PDF, PDFA1A} x eq PDFA1A
            -> Compatible    the requested value is explicitly included

    KGC323  neq PDF x eq PDFA1A with declared distinctness
            -> Compatible    the exclusion does not apply to the request

The four cases cover equality, distinctness, set-valued identity, and
inequality at the nominal sort. The resource contributes no selected
relation between the file-type concepts, so the cases isolate what follows
from the constraints and from explicit declarations.

The PDF family
--------------
The table lists PDF, PDF1X, PDFA1A, PDFA1B, PDFA2A, PDFA2B, PDFA3, PDFA3A,
PDFA3B, PDFA3U, PDFUA, PDFX, PDFX1A, PDFX2A and PDFX4: fifteen concepts, all
siblings, none related to any other.  A PDF/A-1a file is a PDF, and the
authority does not say so.

The relation is conformance to a profile of a base standard, which is
neither identity nor subsumption nor parthood, so the fragment could not
express it even if the table published it.  Unknown is therefore the right
verdict twice over: the resource is silent, and the fragment has no sort
that would make the silence fillable.  This is the scoping argument of the
paper meeting a real vocabulary rather than a constructed one.

The witness condition
---------------------
At nom the order is absent from the denotations, which reduce to identity
and its Boolean combinations.  W(K) is still the finite disjunction over
the concepts the grounding names.

  KGC320  D = {pdf} and {pdfa1a},  named {pdf, pdfa1a}
          W = (pdf = pdf & pdf = pdfa1a) | (pdfa1a = pdf & pdfa1a = pdfa1a)
          Both disjuncts reduce to pdf = pdfa1a.  Nothing asserts it and
          nothing denies it, so a structure may identify the two formats
          and a structure may keep them apart: both queries satisfiable.

  KGC321  The same W, under declarations asserting pdf != pdfa1a.  The witness
          then fails in every structure, so the first query is
          unsatisfiable and the verdict is Incompatible.  The premise is
          the parties', and withdrawing it returns the verdict to Unknown.

  KGC322  D = {pdf} u {pdfa1a} and {pdfa1a},  named {pdf, pdfa1a}
          W = ( (pdf = pdf | pdf = pdfa1a) & pdf = pdfa1a )
            | ( (pdfa1a = pdf | pdfa1a = pdfa1a) & pdfa1a = pdfa1a )
          The second disjunct holds in every structure on reflexivity of
          equality alone.  Compatible, and the refutation cites the witness
          and nothing else: no resource statement, no declaration, no order
          axiom.  It is the cheapest certificate in the suite and the one
          that shows what nom leaves the resource doing, which is deciding
          whether a value grounds at all.
"""


from compile import Constraint

PDF  = "ft_pdf"
A1A  = "ft_pdfa1a"

RESOURCE    = "https://w3id.org/odrl-kb/eu-file-type"
EMPTY_BT    = "https://w3id.org/odrl-kb/eu-file-type/empty"
DECLARED_BT = "https://w3id.org/odrl-kb/eu-file-type/declared"
INCLUDES          = ["KGE000-0.ax", "EUFT-filetype.ax"]
INCLUDES_DECLARED = INCLUDES + ["EUFT-filetype-declared.ax"]
BINDING = "https://w3id.org/odrl-kb/profile/b-fileformat"


def C(op, *vals, side="offer"):
    return Constraint(op, tuple(vals), side)


_TTL_HEAD = """\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ft:      <http://publications.europa.eu/resource/authority/file-type/> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .
"""


PROBLEMS = [

    # -----------------------------------------------------------------
    # KGC320  Two formats the table lists and never relates.  Unknown,
    # and structurally so: there is no statement that could have settled
    # it and no sort under which the fragment could read one.
    # -----------------------------------------------------------------
    {
        "id":                "KGC320",
        "twin":              "KGC321",
        "binding":           BINDING,
        "subdir":            "verdict",
        "name":              "fileFormat, eq ft:PDF against eq ft:PDFA1A",
        "left_operand":      "fileFormat",
        "sort":              "nom",
        "resource":          RESOURCE,
        "background_theory": EMPTY_BT,
        "includes":          INCLUDES,
        "tree": [C("eq", PDF), C("eq", A1A, side="request")],
        "summary": (
            "A German library permits use in PDF only. A French library's policy "
            "commits to use in PDF/A-1a only."),
        "description": (
            "The EU file type table lists both PDF and PDF/A-1a and links "
            "the two entries by no relation; only the prose of the PDF/A-1a "
            "entry mentions the PDF standard. The media type "
            "application/pdf, which both entries carry, is not used to tell "
            "formats apart in this reading. Where values are told apart by "
            "name only, nothing therefore decides whether the two formats "
            "are one."),

        "fof_decls": """\
% Resource: no order statements.  The table publishes none.
% Declarations: empty.  The table separates nothing either.
""",

        "expected_q1": "Satisfiable",
        "expected_q2": "Satisfiable",

        "smt2_logic": "UF",
        "smt2_background": "",

        "certificate": {
            "kind": "Models",
"comment": (
    "If PDF and PDF/A-1a are the same format, a use in one is a use in the "
    "other and both policies are met; if they are different formats, no use "
    "meets both. The EU file type table lists them as two entries and links "
    "them by no relation. Its PDF/A-1a entry states in prose that PDF/A-1 "
    "is part of the PDF standard (ISO 19005-1), but this reading tells "
    "formats apart by name only and uses neither that prose nor the media "
    "type application/pdf that both entries carry."),
            "premises": [],
        },
        "ttl": _TTL_HEAD + """
drk:policy-320-1 a odrl:Set ;
    odrl:uid drk:policy-320-1 ;
    dcterms:title "Use in PDF only"@en ;
    odrl:assigner drk:german-library ;
    odrl:permission kgc:KGC320-p1-r1 .

kgc:KGC320-p1-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC320-p1-c1 .

kgc:KGC320-p1-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:fileFormat ;
    odrl:operator odrl:eq ;
    odrl:rightOperand ft:PDF .

drk:policy-320-2 a odrl:Set ;
    odrl:uid drk:policy-320-2 ;
    dcterms:title "Use in PDF/A-1a only"@en ;
    odrl:assignee drk:french-library ;
    odrl:permission kgc:KGC320-p2-r1 .

kgc:KGC320-p2-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC320-p2-c1 .

kgc:KGC320-p2-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:fileFormat ;
    odrl:operator odrl:eq ;
    odrl:rightOperand ft:PDFA1A .""",
    },

    # -----------------------------------------------------------------
    # KGC321  The same pair under a declaration.  At nom the declaration
    # is the whole of what moves the verdict, since the resource
    # contributes nothing to it.
    # -----------------------------------------------------------------
    {
        "id":                "KGC321",
        "twin":              "KGC320",
        "binding":           BINDING,
        "subdir":            "verdict",
        "name":              "fileFormat, eq ft:PDF against eq ft:PDFA1A, "
                             "under a declared distinctness",
        "left_operand":      "fileFormat",
        "sort":              "nom",
        "resource":          RESOURCE,
        "background_theory": DECLARED_BT,
        "includes":          INCLUDES_DECLARED,
        "tree": [C("eq", PDF), C("eq", A1A, side="request")],
        "summary": (
            "As KGC320, with the two formats declared distinct."),
"description": (
    "KGC320 with a declaration that PDF and PDF/A-1a are different formats. "
    "The EU file type table links the two entries by no relation, so the "
    "declaration is what changes the verdict from Unknown to Incompatible.\n\n"
    "The verdict holds for this reading only. In fact a PDF/A-1a file is "
    "also a PDF file (ISO 19005-1), so a library that supplies PDF/A-1a "
    "keeps both promises. The case shows what reading file types by name "
    "costs, as KGC380 does for the jurisdictional reading of places."),

        "expected_q1": "Unsatisfiable",
        "expected_q2": "Satisfiable",

        "smt2_logic": "UF",

        "certificate": {
            "kind": "Refutation",
   "comment": (
       "The policies need a use in PDF and in PDF/A-1a only, which is "
       "possible only if the two are the same format; the declaration "
       "states they are different formats, since the EU file type table "
       "lists them as separate entries. The table links the two entries by "
       "no relation, and the media type application/pdf that both carry is "
       "not used to tell formats apart in this reading. So no use meets "
       "both policies."),
            "premises": [
                ("fromDeclarations",
                 "ft:PDF and ft:PDFA1A are declared distinct"),
            ],
        },
        "ttl": _TTL_HEAD + """
drk:policy-321-1 a odrl:Set ;
    odrl:uid drk:policy-321-1 ;
    dcterms:title "Use in PDF only"@en ;
    odrl:assigner drk:german-library ;
    odrl:permission kgc:KGC321-p1-r1 .

kgc:KGC321-p1-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC321-p1-c1 .

kgc:KGC321-p1-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:fileFormat ;
    odrl:operator odrl:eq ;
    odrl:rightOperand ft:PDF .

drk:policy-321-2 a odrl:Set ;
    odrl:uid drk:policy-321-2 ;
    dcterms:title "Use in PDF/A-1a only"@en ;
    odrl:assignee drk:french-library ;
    odrl:permission kgc:KGC321-p2-r1 .

kgc:KGC321-p2-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC321-p2-c1 .

kgc:KGC321-p2-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:fileFormat ;
    odrl:operator odrl:eq ;
    odrl:rightOperand ft:PDFA1A .""",
    },
# KGC322  A nominal set-valued case.  isAnyOf uses identity over its
# explicitly listed values, so compatibility can follow from the
# constraints alone.
    {
        "id":                "KGC322",
        "binding":           BINDING,
        "subdir":            "verdict",
        "name":              "fileFormat, isAnyOf {ft:PDF, ft:PDFA1A} "
                             "against eq ft:PDFA1A",
        "left_operand":      "fileFormat",
        "sort":              "nom",
        "resource":          RESOURCE,
        "background_theory": EMPTY_BT,
        "includes":          INCLUDES,
        "tree": [C("isAnyOf", PDF, A1A), C("eq", A1A, side="request")],
        "summary": (
            "A German library permits use in at least one of PDF and PDF/A-1a. "
            "A French library's policy commits to use in PDF/A-1a only."),
        "description": (
            "A policy that lists both PDF and PDF/A-1a with isAnyOf, "
            "against a commitment to PDF/A-1a. PDF/A-1a is on the list, so "
            "a use in PDF/A-1a meets both policies whatever the table "
            "states, and the verdict is Compatible. isAnyOf asks only "
            "whether a value is the same as a listed one, which is why it "
            "works where values are told apart by name only and isA does "
            "not. It also admits PDF/A-1a together with any other format."),
        "maintainer_note": (
            "The refutation cites the witness alone: no resource statement, "
            "no declaration, no order axiom."),

        "fof_decls": """\
% Resource: no order statements.
% Declarations: empty.  Neither is needed: the verdict follows from
% reflexivity of equality.
""",

        "expected_q1": "Satisfiable",
        "expected_q2": "Unsatisfiable",

        "smt2_logic": "UF",
        "smt2_background": "",

        "certificate": {
            "kind": "Refutation",
    "comment": (
        "The second policy requires PDF/A-1a, and the first lists it among "
        "the formats isAnyOf accepts, so a use in PDF/A-1a meets both "
        "policies. The EU file type table links no two formats by any "
        "relation, so listing both is how a policy author makes PDF/A-1a "
        "acceptable."),
            "premises": [
                ("fromConstraints", "the witness condition"),
            ],
        },
        "ttl": _TTL_HEAD + """
drk:policy-322-1 a odrl:Set ;
    odrl:uid drk:policy-322-1 ;
    dcterms:title "Use in at least one of PDF and PDF/A-1a"@en ;
    odrl:assigner drk:german-library ;
    odrl:permission kgc:KGC322-p1-r1 .

kgc:KGC322-p1-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC322-p1-c1 .

kgc:KGC322-p1-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:fileFormat ;
    odrl:operator odrl:isAnyOf ;
    odrl:rightOperand ( ft:PDF ft:PDFA1A ) .

drk:policy-322-2 a odrl:Set ;
    odrl:uid drk:policy-322-2 ;
    dcterms:title "Use in PDF/A-1a only"@en ;
    odrl:assignee drk:french-library ;
    odrl:permission kgc:KGC322-p2-r1 .

kgc:KGC322-p2-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC322-p2-c1 .

kgc:KGC322-p2-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:fileFormat ;
    odrl:operator odrl:eq ;
    odrl:rightOperand ft:PDFA1A .""",
    },
    # -----------------------------------------------------------------
# KGC323  A nominal negation case.  This is the only benchmark case
# for neq.  The offer excludes PDF, while the request requires
# PDF/A-1a.  The explicit distinctness declaration makes the two
# constraints compatible.
# -----------------------------------------------------------------
{
    "id": "KGC323",
    "subdir": "verdict",
    "binding":           BINDING,
    "name": (
        "fileFormat, neq ft:PDF against eq ft:PDFA1A, "
        "under a declared distinctness"
    ),

    "summary": (
        "A German library permits use in any format except PDF. A French "
        "library's policy commits to use in PDF/A-1a only. "
        "The two formats are declared distinct."),

    "left_operand": "fileFormat",
    "sort": "nom",
    "resource": RESOURCE,
    "background_theory": DECLARED_BT,
    "binding": BINDING,
    "includes": INCLUDES_DECLARED,
    "tree": [C("neq", PDF), C("eq", A1A, side="request")],

    "description": (
        "A German library excludes plain PDF because it wants archival "
        "copies, expecting PDF/A to pass as well. It does pass, but only "
        "because the exclusion names PDF alone. As in KGC392 and KGC397, "
        "the exclusion covers only the format it names. PDF/A-1a is a "
        "restricted form of PDF (ISO 19005-1, which the EU file type table "
        "names in its PDF/A-1a entry), but the table links the two entries "
        "by no relation, so excluding PDF does not exclude PDF/A-1a. Where "
        "values are told apart by name only, the way to exclude both is to "
        "list both: any format except PDF and PDF/A-1a."),


    "expected_q1": "Satisfiable",
    "expected_q2": "Unsatisfiable",

    "smt2_logic": "UF",


    "certificate": {
        "kind": "Refutation",
        "comment": (
            "The first policy excludes PDF, and the second requires "
            "PDF/A-1a. The declarations state that the two formats are "
            "different, since the EU file type table lists them as separate "
            "entries, so the required format is not excluded. Excluding PDF "
            "does not exclude PDF/A-1a, because the table links the two "
            "entries by no relation."),
        "premises": [
            (
                "fromDeclarations",
                "ft:PDF and ft:PDFA1A are declared distinct"
            ),
            (
                "fromConstraints",
                "the witness condition"
            ),
        ],
    },

    "ttl": _TTL_HEAD + """
drk:policy-323-1 a odrl:Set ;
    odrl:uid drk:policy-323-1 ;
    dcterms:title "Use in any format except PDF"@en ;
    odrl:assigner drk:german-library ;
    odrl:permission kgc:KGC323-p1-r1 .

kgc:KGC323-p1-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC323-p1-c1 .

kgc:KGC323-p1-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:fileFormat ;
    odrl:operator odrl:neq ;
    odrl:rightOperand ft:PDF .

drk:policy-323-2 a odrl:Set ;
    odrl:uid drk:policy-323-2 ;
    dcterms:title "Use in PDF/A-1a only"@en ;
    odrl:assignee drk:french-library ;
    odrl:permission kgc:KGC323-p2-r1 .

kgc:KGC323-p2-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC323-p2-c1 .

kgc:KGC323-p2-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:fileFormat ;
    odrl:operator odrl:eq ;
    odrl:rightOperand ft:PDFA1A .
""",
},
]