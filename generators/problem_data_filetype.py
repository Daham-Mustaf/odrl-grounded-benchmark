"""
problem_data_filetype.py
========================
Three problems over the EU File type table, at nom.

    KGC320  eq PDF      x eq PDFA1A   -> Unknown       the table relates nothing
    KGC321  the same pair under a declared distinctness -> Incompatible
    KGC322  isAnyOf {PDF, PDFA1A} x eq PDFA1A -> Compatible  on identity alone

What this resource adds that the others do not
-----------------------------------------------
DPV and GeoNames publish an order and the profile declares how to read it.
This table publishes no order: 228 concepts, every one a top concept, and
zero skos:broader, narrower, related, exactMatch or broadMatch.  The builder
checks all five and refuses to emit a resource if any is non-empty, so the
nom binding is not an interpretation.  It is the only sort with anything to
bind, and the publisher decided that.

The consequence for verdicts is visible in the certificates below.  At tax
and mer a Compatible cites resource premises: KGC310 cites one, KGC315 six.
Here no verdict cites a resource premise at all, because the resource has
none to cite.  What a verdict rests on is the constraints and whatever the
parties declared, and the certificate shows the shift.  The more a resource
publishes, the more of a verdict belongs to the authority; the less it
publishes, the more belongs to the parties.  That is a property of the
binding, not a defect in either.

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

  KGC321  The same W, under a theory asserting pdf != pdfa1a.  The witness
          then fails in every structure, so the first query is
          unsatisfiable and the verdict is Incompatible.  The premise is
          the parties', and withdrawing it returns the verdict to Unknown.

  KGC322  D = {pdf} u {pdfa1a} and {pdfa1a},  named {pdf, pdfa1a}
          W = ( (pdf = pdf | pdf = pdfa1a) & pdf = pdfa1a )
            | ( (pdfa1a = pdf | pdfa1a = pdfa1a) & pdfa1a = pdfa1a )
          The second disjunct holds in every structure on reflexivity of
          equality alone.  Compatible, and the refutation cites the witness
          and nothing else: no resource assertion, no declaration, no order
          axiom.  It is the cheapest certificate in the suite and the one
          that shows what nom leaves the resource doing, which is deciding
          whether a value grounds at all.
"""

PDF  = "ft_pdf"
A1A  = "ft_pdfa1a"

RESOURCE    = "https://w3id.org/odrl-kb/eu-file-type"
EMPTY_BT    = "https://w3id.org/odrl-kb/eu-file-type/empty"
DECLARED_BT = "https://w3id.org/odrl-kb/eu-file-type/declared"

INCLUDES          = ["KGE000-0.ax", "EUFT-filetype.ax"]
INCLUDES_DECLARED = INCLUDES + ["EUFT-filetype-declared.ax"]


def _decls(*concepts):
    """Declarations for a nominal problem.

    No kge_leq: the resource declares no order, so the symbol has nothing to
    interpret and the writer, which emits the order axioms only when the
    declarations mention it, correctly emits none.  A nominal problem whose
    file carried the three order axioms would be asserting a structure the
    resource does not have.
    """
    lines = ["(declare-sort Concept 0)"]
    lines += [f"(declare-fun {c} () Concept)" for c in concepts]
    return "\n".join(lines)


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
    # and structurally so: there is no assertion that could have settled
    # it and no sort under which the fragment could read one.
    # -----------------------------------------------------------------
    {
        "id":                "KGC320",
        "subdir":            "verdict",
        "name":              "fileFormat, eq ft:PDF against eq ft:PDFA1A",
        "left_operand":      "fileFormat",
        "sort":              "nom",
        "resource":          RESOURCE,
        "background_theory": EMPTY_BT,
        "includes":          INCLUDES,
        "description": (
            "Offer (fileFormat, eq, ft:PDF) against request (fileFormat, eq, "
            "ft:PDFA1A).  The authority lists both formats and relates them "
            "in no way, so nothing settles whether the two names denote one "
            "format: Unknown.  A PDF/A-1a file is a PDF, and the table does "
            "not say so; nor could the fragment read it if the table did, "
            "since conformance to a profile of a standard is not identity, "
            "subsumption or parthood."
        ),

        "fof_decls": """\
% Resource: no order assertions.  The table publishes none.
% Background theory: empty.  The table separates nothing either.
""",
        "fof_witness": f"""\
( ( {PDF} = {PDF} & {PDF} = {A1A} )
| ( {A1A} = {PDF} & {A1A} = {A1A} ) )""",

        "expected_q1": "Satisfiable",
        "expected_q2": "Satisfiable",

        "smt2_logic": "UF",
        "smt2_decls": _decls(PDF, A1A),
        "smt2_resource": """\
; Resource: nothing.  228 concepts, no relations between any of them.""",
        "smt2_background": "",
        "smt2_witness": f"""\
(or (and (= {PDF} {PDF}) (= {PDF} {A1A}))
    (and (= {A1A} {PDF}) (= {A1A} {A1A})))""",

        "certificate": {
            "kind": "Models",
            "comment": "Both queries are satisfiable.  The models differ on "
                       "whether the two names denote one format.  No "
                       "assertion in the table bears on the question, so the "
                       "verdict reports the authority's silence rather than "
                       "resolving it.",
            "premises": [],
        },
        "ttl": _TTL_HEAD + """
drk:bsb-offer-320 a odrl:Offer ;
    dcterms:title "BSB offer: PDF"@en ;
    odrl:assigner drk:bavarian-state-library ;
    odrl:permission kgc:KGC320-offer-r1 .

kgc:KGC320-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:bsb-manuscripts ;
    odrl:constraint kgc:KGC320-offer-c1 .

kgc:KGC320-offer-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:fileFormat ;
    odrl:operator odrl:eq ;
    odrl:rightOperand ft:PDF .

drk:bnf-request-320 a odrl:Request ;
    dcterms:title "BnF request: PDF/A-1a"@en ;
    odrl:assignee drk:french-national-library ;
    odrl:permission kgc:KGC320-request-r1 .

kgc:KGC320-request-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:bsb-manuscripts ;
    odrl:constraint kgc:KGC320-request-c1 .

kgc:KGC320-request-c1 a odrl:Constraint ;
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
        "subdir":            "verdict",
        "name":              "fileFormat, eq ft:PDF against eq ft:PDFA1A, "
                             "under a declared distinctness",
        "left_operand":      "fileFormat",
        "sort":              "nom",
        "resource":          RESOURCE,
        "background_theory": DECLARED_BT,
        "includes":          INCLUDES_DECLARED,
        "description": (
            "The constraints of KGC320 under a background theory in which "
            "the parties declare the two formats distinct.  Incompatible, "
            "and the sole premise is the declaration: the table contributed "
            "nothing, so withdrawing the declaration returns the verdict to "
            "Unknown and there is nothing else holding it."
        ),

        "fof_decls": """\
% Background theory: one declared distinctness, from
% EUFT-filetype-declared.ax.  The table separates nothing itself.
""",
        "fof_witness": f"""\
( ( {PDF} = {PDF} & {PDF} = {A1A} )
| ( {A1A} = {PDF} & {A1A} = {A1A} ) )""",

        "expected_q1": "Unsatisfiable",
        "expected_q2": "Satisfiable",

        "smt2_logic": "UF",
        "smt2_decls": _decls(PDF, A1A),
        "smt2_resource": """\
; Resource: nothing, as in KGC320.""",
        "smt2_background": f"""\
; Background theory: the declaration, and the only difference from KGC320.
(assert (distinct {PDF} {A1A}))""",
        "smt2_witness": f"""\
(or (and (= {PDF} {PDF}) (= {PDF} {A1A}))
    (and (= {A1A} {PDF}) (= {A1A} {A1A})))""",

        "certificate": {
            "kind": "Refutation",
            "comment": "The two constraints require one format to be both "
                       "concepts, and the declaration holds them apart.  "
                       "Compare KGC314, where a declaration moved a verdict "
                       "over a resource that also published an order: here "
                       "the declaration is doing all of the work, because "
                       "the table publishes nothing at all.",
            "premises": [
                ("fromBackgroundTheory",
                 "ft:PDF and ft:PDFA1A are declared distinct"),
            ],
        },
        "ttl": _TTL_HEAD + """
drk:bsb-offer-321 a odrl:Offer ;
    dcterms:title "BSB offer: PDF"@en ;
    odrl:assigner drk:bavarian-state-library ;
    odrl:permission kgc:KGC321-offer-r1 .

kgc:KGC321-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:bsb-manuscripts ;
    odrl:constraint kgc:KGC321-offer-c1 .

kgc:KGC321-offer-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:fileFormat ;
    odrl:operator odrl:eq ;
    odrl:rightOperand ft:PDF .

drk:bnf-request-321 a odrl:Request ;
    dcterms:title "BnF request: PDF/A-1a"@en ;
    odrl:assignee drk:french-national-library ;
    odrl:permission kgc:KGC321-request-r1 .

kgc:KGC321-request-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:bsb-manuscripts ;
    odrl:constraint kgc:KGC321-request-c1 .

kgc:KGC321-request-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:fileFormat ;
    odrl:operator odrl:eq ;
    odrl:rightOperand ft:PDFA1A .""",
    },

    # -----------------------------------------------------------------
    # KGC322  A set-valued operator at nom.  isAnyOf needs only identity,
    # so it is admissible at every sort, and here it produces a
    # Compatible whose refutation cites nothing but the witness.
    # -----------------------------------------------------------------
    {
        "id":                "KGC322",
        "subdir":            "verdict",
        "name":              "fileFormat, isAnyOf {ft:PDF, ft:PDFA1A} "
                             "against eq ft:PDFA1A",
        "left_operand":      "fileFormat",
        "sort":              "nom",
        "resource":          RESOURCE,
        "background_theory": EMPTY_BT,
        "includes":          INCLUDES,
        "description": (
            "Offer (fileFormat, isAnyOf, {ft:PDF, ft:PDFA1A}) against "
            "request (fileFormat, eq, ft:PDFA1A).  The offer admits either "
            "format and the request requires one of them, so the two are "
            "satisfiable together whatever the table says.  Compatible, and "
            "the refutation cites the witness alone: no resource assertion, "
            "no declaration, no order axiom.  isAnyOf asks only whether "
            "concepts are the same, which is why it is admissible at nom "
            "where isA is not."
        ),

        "fof_decls": """\
% Resource: no order assertions.
% Background theory: empty.  Neither is needed: the verdict follows from
% reflexivity of equality.
""",
        "fof_witness": f"""\
( ( ( {PDF} = {PDF} | {PDF} = {A1A} ) & {PDF} = {A1A} )
| ( ( {A1A} = {PDF} | {A1A} = {A1A} ) & {A1A} = {A1A} ) )""",

        "expected_q1": "Satisfiable",
        "expected_q2": "Unsatisfiable",

        "smt2_logic": "UF",
        "smt2_decls": _decls(PDF, A1A),
        "smt2_resource": """\
; Resource: nothing.  The verdict does not need it.""",
        "smt2_background": "",
        "smt2_witness": f"""\
(or (and (or (= {PDF} {PDF}) (= {PDF} {A1A})) (= {PDF} {A1A}))
    (and (or (= {A1A} {PDF}) (= {A1A} {A1A})) (= {A1A} {A1A})))""",

        "certificate": {
            "kind": "Refutation",
            "comment": "The requested format is among those the offer "
                       "admits, so the two constraints hold together in "
                       "every structure.  Nothing the authority published "
                       "and nothing the parties declared takes part, which "
                       "is what a verdict looks like when identity alone "
                       "settles it.",
            "premises": [
                ("fromConstraints", "the witness condition"),
            ],
        },
        "ttl": _TTL_HEAD + """
drk:bsb-offer-322 a odrl:Offer ;
    dcterms:title "BSB offer: PDF or PDF/A-1a"@en ;
    odrl:assigner drk:bavarian-state-library ;
    odrl:permission kgc:KGC322-offer-r1 .

kgc:KGC322-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:bsb-manuscripts ;
    odrl:constraint kgc:KGC322-offer-c1 .

kgc:KGC322-offer-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:fileFormat ;
    odrl:operator odrl:isAnyOf ;
    odrl:rightOperand ft:PDF, ft:PDFA1A .

drk:bnf-request-322 a odrl:Request ;
    dcterms:title "BnF request: PDF/A-1a"@en ;
    odrl:assignee drk:french-national-library ;
    odrl:permission kgc:KGC322-request-r1 .

kgc:KGC322-request-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:bsb-manuscripts ;
    odrl:constraint kgc:KGC322-request-c1 .

kgc:KGC322-request-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:fileFormat ;
    odrl:operator odrl:eq ;
    odrl:rightOperand ft:PDFA1A .""",
    },
]