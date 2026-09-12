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
from the constraints and from explicit background assertions.

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
BINDING = "https://w3id.org/odrl-kb/profile/b-fileformat"

def _iso(*pairs):
    """Declared-distinctness instances, named bg_dist_ on both encodings.

    The declared theory states the rule and lists the purposes it ranges
    over; a problem naming two of them carries the inequation between
    them, so a refutation cites the instance it used rather than one
    term standing for all of them. The name must match on both sides:
    an unsat core and a TPTP proof are compared by premise name.
    """
    fof = ["% Background theory: declared distinctness instances, stated in",
           "% the declared theory file and instantiated here.", ""]
    smt = ["; Declared distinctness this problem adopts, named as the TPTP",
           "; side names it."]
    for a, b in pairs:
        n = f"bg_dist_{a}_{b}"
        fof.append(f"fof({n}, axiom,\n    {a} != {b}).")
        smt.append(f"(assert (! (not (= {a} {b})) :named {n}))")
    return "\n".join(fof) + "\n", "\n".join(smt)

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
         "unknown_reason": "epistemic",
        "includes":          INCLUDES,
        "summary": (
    "A library permits PDF, while a researcher requests PDF/A-1a."
),
        "description": (
    "The EU File Type table lists both PDF and PDF/A-1a but publishes no "
    "selected relation between them. At the nominal sort, the formal "
    "semantics therefore leaves their identity open. The case also shows "
    "that the fragment does not interpret conformance to a file-format "
    "profile as identity, subsumption, or parthood."
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
"comment": (
    "The two constraints can be satisfied both when ft:PDF and ft:PDFA1A "
    "denote the same element and when they denote different elements. No "
    "resource or background assertion selects between these possibilities."
),
            "premises": [],
        },
        "ttl": _TTL_HEAD + """
drk:offer-320 a odrl:Offer ;
    dcterms:title "BSB offer: PDF"@en ;
    odrl:assigner drk:library ;
    odrl:permission kgc:KGC320-offer-r1 .

kgc:KGC320-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC320-offer-c1 .

kgc:KGC320-offer-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:fileFormat ;
    odrl:operator odrl:eq ;
    odrl:rightOperand ft:PDF .

drk:request-320 a odrl:Request ;
    dcterms:title "BnF request: PDF/A-1a"@en ;
    odrl:assignee drk:researcher ;
    odrl:permission kgc:KGC320-request-r1 .

kgc:KGC320-request-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
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
        "summary": (
    "A library permits PDF, while a researcher requests PDF/A-1a, with "
    "the two formats declared distinct."
),
"description": (
    "The case is the KGC320 pair with a background assertion declaring "
    "ft:PDF and ft:PDFA1A distinct. The resource contributes no relation "
    "between the two concepts, so the declaration is the premise that "
    "changes the verdict from Unknown to Incompatible."
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
   "comment": (
        "The two constraints require ft:PDF and ft:PDFA1A to denote the "
        "same element, while the background assertion requires them to "
        "denote different elements. The two conditions cannot both hold."
    ),
            "premises": [
                ("fromBackgroundTheory",
                 "ft:PDF and ft:PDFA1A are declared distinct"),
            ],
        },
        "ttl": _TTL_HEAD + """
drk:offer-321 a odrl:Offer ;
    dcterms:title "BSB offer: PDF"@en ;
    odrl:assigner drk:library ;
    odrl:permission kgc:KGC321-offer-r1 .

kgc:KGC321-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC321-offer-c1 .

kgc:KGC321-offer-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:fileFormat ;
    odrl:operator odrl:eq ;
    odrl:rightOperand ft:PDF .

drk:request-321 a odrl:Request ;
    dcterms:title "BnF request: PDF/A-1a"@en ;
    odrl:assignee drk:researcher ;
    odrl:permission kgc:KGC321-request-r1 .

kgc:KGC321-request-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC321-request-c1 .

kgc:KGC321-request-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:fileFormat ;
    odrl:operator odrl:eq ;
    odrl:rightOperand ft:PDFA1A .""",
    },
# KGC322  A nominal set-valued case.  isAnyOf uses identity over its
# explicitly listed values, so compatibility can follow from the
# constraints alone.
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
        "summary": (
    "A library permits either PDF or PDF/A-1a, while a researcher requests "
    "PDF/A-1a."
),
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
    "comment": (
        "The request requires ft:PDFA1A, and the offer includes ft:PDFA1A "
        "among the values accepted by isAnyOf. The two constraints can "
        "therefore be satisfied together without any resource or background "
        "assertion."
    ),        "premises": [
                ("fromConstraints", "the witness condition"),
            ],
        },
        "ttl": _TTL_HEAD + """
drk:offer-322 a odrl:Offer ;
    dcterms:title "BSB offer: PDF or PDF/A-1a"@en ;
    odrl:assigner drk:library ;
    odrl:permission kgc:KGC322-offer-r1 .

kgc:KGC322-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC322-offer-c1 .

kgc:KGC322-offer-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:fileFormat ;
    odrl:operator odrl:isAnyOf ;
    odrl:rightOperand ft:PDF ,
        ft:PDFA1A .

drk:request-322 a odrl:Request ;
    dcterms:title "BnF request: PDF/A-1a"@en ;
    odrl:assignee drk:researcher ;
    odrl:permission kgc:KGC322-request-r1 .

kgc:KGC322-request-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC322-request-c1 .

kgc:KGC322-request-c1 a odrl:Constraint ;
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
        "A library excludes PDF, while a researcher requests PDF/A-1a, "
        "with the two formats declared distinct."
    ),

    "left_operand": "fileFormat",
    "sort": "nom",
    "resource": RESOURCE,
    "background_theory": DECLARED_BT,
    "binding": BINDING,
    "includes": INCLUDES_DECLARED,

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
% Resource: no order assertions.
% Background theory: ft:PDF and ft:PDFA1A are declared distinct.
""",

    "fof_witness": f"""\
( ( {PDF} != {PDF} & {PDF} = {A1A} )
| ( {A1A} != {PDF} & {A1A} = {A1A} ) )""",

    "expected_q1": "Satisfiable",
    "expected_q2": "Unsatisfiable",

    "smt2_logic": "UF",

    "smt2_decls": _decls(PDF, A1A),

    "smt2_resource": """\
; Resource: no order relation between the file-type concepts.
""",

    "smt2_background": f"""\
; Background theory: ft:PDF and ft:PDFA1A are declared distinct.
(assert (distinct {PDF} {A1A}))
""",

    "smt2_witness": f"""\
(or (and (not (= {PDF} {PDF})) (= {PDF} {A1A}))
    (and (not (= {A1A} {PDF})) (= {A1A} {A1A})))""",

    "certificate": {
        "kind": "Refutation",
        "comment": (
            "The offer excludes ft:PDF, while the request requires "
            "ft:PDFA1A. The background assertion declares the two concepts "
            "distinct, so the requested value is not excluded."
        ),
        "premises": [
            (
                "fromBackgroundTheory",
                "ft:PDF and ft:PDFA1A are declared distinct"
            ),
            (
                "fromConstraints",
                "the witness condition"
            ),
        ],
    },

    "ttl": _TTL_HEAD + """
drk:offer-323 a odrl:Offer ;
    dcterms:title "BSB offer: not PDF"@en ;
    odrl:assigner drk:library ;
    odrl:permission kgc:KGC323-offer-r1 .

kgc:KGC323-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC323-offer-c1 .

kgc:KGC323-offer-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:fileFormat ;
    odrl:operator odrl:neq ;
    odrl:rightOperand ft:PDF .

drk:request-323 a odrl:Request ;
    dcterms:title "BnF request: PDF/A-1a"@en ;
    odrl:assignee drk:researcher ;
    odrl:permission kgc:KGC323-request-r1 .

kgc:KGC323-request-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC323-request-c1 .

kgc:KGC323-request-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:fileFormat ;
    odrl:operator odrl:eq ;
    odrl:rightOperand ft:PDFA1A .
""",
},
]