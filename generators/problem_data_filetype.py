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
    "The EU File Type table lists both PDF and PDF/A-1a but publishes no "
    "selected relation between them. At the nominal sort, the formal "
    "semantics therefore leaves their identity open. The case also shows "
    "that the fragment does not interpret conformance to a file-format "
    "profile as identity, subsumption, or parthood."
),

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
    "The two constraints can be satisfied both when ft:PDF and ft:PDFA1A "
    "denote the same element and when they denote different elements. No "
    "resource statement or declaration selects between these possibilities. "
    "PDF/A-1a is a restricted form of PDF, but the table publishes no "
    "relation between the two, so this binding cannot use that relation."
),
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
    "The case is the KGC320 pair with a declaration that "
    "ft:PDF and ft:PDFA1A are distinct. The resource contributes no relation "
    "between the two concepts, so the declaration is the premise that "
    "changes the verdict from Unknown to Incompatible."
),
        "fof_decls": """\
% Declarations: one declared distinctness, from
% EUFT-filetype-declared.ax.  The table separates nothing itself.
""",

        "expected_q1": "Unsatisfiable",
        "expected_q2": "Satisfiable",

        "smt2_logic": "UF",

        "certificate": {
            "kind": "Refutation",
   "comment": (
        "The two constraints require ft:PDF and ft:PDFA1A to denote the "
        "same element, while the declaration requires them to "
        "denote different elements. The two conditions cannot both hold. "
        "PDF/A-1a is a restricted form of PDF, but the table publishes no "
        "relation between the two, so under this binding a use in PDF/A-1a "
        "is not a use in PDF."
    ),
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
            "Offer (fileFormat, isAnyOf, {ft:PDF, ft:PDFA1A}) against "
            "request (fileFormat, eq, ft:PDFA1A).  The offer admits either "
            "format and the request requires one of them, so the two are "
            "satisfiable together whatever the table says.  Compatible, and "
            "the refutation cites the witness alone: no resource statement, "
            "no declaration, no order axiom.  isAnyOf asks only whether "
            "concepts are the same, which is why it is admissible at nom "
            "where isA is not."
        ),

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
        "the values isAnyOf accepts. The two constraints can be satisfied "
        "together without any resource statement or declaration. Listing "
        "both formats is how a policy author makes PDF/A-1a acceptable "
        "under a flat table."),
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
        "The offer excludes ft:PDF, while the request requires "
        "ft:PDFA1A. The two concepts are declared distinct, so the "
        "constraints are Compatible. At the nominal sort, exclusion by "
        "identity is the applicable reading: the resource publishes no "
        "order relation for file formats. This case therefore provides "
        "a control for cases such as KGC392 and KGC397, where the same "
        "identity-based exclusion is insufficient for an order-based "
        "interpretation."
    ),

    "fof_decls": """\
% Resource: no order statements.
% Declarations: ft:PDF and ft:PDFA1A are declared distinct.
""",


    "expected_q1": "Satisfiable",
    "expected_q2": "Unsatisfiable",

    "smt2_logic": "UF",





    "certificate": {
        "kind": "Refutation",
        "comment": (
            "The first policy excludes PDF, and the second requires PDF/A-1a. "
            "The declarations declare the two formats distinct, so the "
            "required format is not excluded. The exclusion of PDF does not "
            "exclude PDF/A-1a, because the table does not relate them."),
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