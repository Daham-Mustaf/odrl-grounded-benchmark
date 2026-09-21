"""
problem_data_dpvloc.py
======================
Five problems over the DPV Locations resource, at mer.

    KGC330  isPartOf NL x eq BQ   -> Compatible    one containment premise
    KGC331  isPartOf EU x eq DE   -> Compatible    under the jurisdictional
                                                   reading; not grounded at
                                                   all under the geographic
    KGC333  eq DE       x eq FR   -> Unknown       nothing separates them
    KGC334  the same pair under the ISO rule       -> Incompatible

One resource, two readings
---------------------------
KGC331 is the reason this resource is in the suite.  Its two constraints are
well sorted: isPartOf requires parthood, the operand is bound at mer, and the
signature admits it without consulting anything.  Whether it has a verdict
depends on which of the file's relations the profile reads.

The geographic profile reads containment, and the European Union is not in
its concept set: the union edges are membership, which that profile does not
take, so dpv-loc:EU grounds to nothing and the constraint has no denotation.
The jurisdictional profile reads containment together with membership, and
the same constraint is Compatible on one assertion.

Neither profile is the correct reading of the file.  They are two readings,
both faithful to what the extension publishes, differing in which published
relation they treat as the order.  Same operand, same sort, same file,
opposite outcome, and the profile is the only place the difference is
recorded.  That is the paper's claim with the resource held fixed.

The reading also changes the shape of the certificates.  Under the
geographic reading the containment order is two levels deep and no verdict
in this file needs transitivity.  Under the jurisdictional reading the
unions nest, EEA30 below EEA, and a chain runs four steps from a Caribbean
municipality to the European Economic Area.  Depth is a property of what an
authority published and of what a profile reads, not of the semantics.

Identity the authority publishes, and why no problem uses it
-------------------------------------------------------------
The extension publishes thirty identity pairs: ISO 3166 assigns some places
both a country code and a subdivision code, TF and FR-TF for the French
Southern Territories, and the extension records that the two denote one
place.  This is the only resource in the suite whose identities come from
the authority rather than from a registry rule the profile applies or from a
declaration the parties make.

None of them is load-bearing, and that was measured rather than assumed.
For every pair, both codes carry the same containment edge: TF is within FR
and FR-TF is within FR, so nothing is reachable only by way of an identity.
A problem built to need one would be answered by the containment before the
identity was consulted.

The assertions are in the resource because the slice is faithful to what the
extension publishes, not because a verdict rests on them.  A resource whose
identities did carry a verdict would be worth having; this one does not, and
saying so is better than constructing a problem that appears to need it.

The witness condition
---------------------
Every pair uses subset-mode operators, so W(K) is the finite disjunction
over the concepts the grounding names.

  KGC330  D = {x | x <= nl} and {bq},  named {nl, bq}
          W = (nl <= nl & nl = bq) | (bq <= nl & bq = bq)
          The extension places Bonaire under the Netherlands, so the second
          disjunct holds in every model.  Compatible on one assertion, and
          the certificate needs no transitivity: the geographic order is two
          levels deep and this is one step of it.

  KGC331  D = {x | x <= eu} and {de},  named {eu, de}
          W = (eu <= eu & eu = de) | (de <= eu & de = de)
          Under the jurisdictional reading de <= eu is asserted and the
          verdict is Compatible.  Under the geographic reading eu is not a
          concept of the resource, the grounding is undefined, and there is
          no D to compute: the constraint is not evaluated rather than
          evaluated to Unknown.

  KGC333  D = {de} and {fr},  named {de, fr}
          W = (de = de & de = fr) | (fr = de & fr = fr)
          Two country codes, and the extension separates them in no way.  A
          model may identify them: Unknown.

  KGC334  The same W under one instance of the ISO rule, that Germany and
          France are distinct areas.  No model then identifies them, the
          witness fails everywhere, and the verdict is Incompatible.  The
          premise is a rule the parties adopted, not an assertion the
          extension makes, and the certificate marks it withdrawable.
          The rule ranges over 249 areas and is stated in the axiom file
          rather than expanded there: instantiating it would add thirty
          thousand inequations to every problem, and a refutation should
          cite the one it used.

On the ISO rule and the identity assertions
--------------------------------------------
The rule is that ISO 3166 assigns one code to an area, so two codes name two
areas.  Applied to the codes directly it would contradict the extension,
which records thirty pairs of codes denoting one area.  It is therefore
applied to the areas: distinctness holds between the equivalence classes the
identity assertions induce, and TF and FR-TF are one class represented by
its country code.

This is the only background theory in the suite constrained by something the
resource publishes.  A generated rule is the parties' to adopt, but not
theirs to adopt in a form the authority contradicts.

It is also the reason the identity assertions are worth keeping even though
no verdict rests on them: they are not load-bearing for reachability, and
they are load-bearing for what the rule may say.
"""
from compile import Constraint, Or, Xone
 
EU    = "loc_eu"
DE    = "loc_de"
BQ    = "loc_bq"
DE_NW = "loc_de_nw"
DE_BY = "loc_de_by"
DE_BE = "loc_de_be"
DE_HH = "loc_de_hh"
WF    = "loc_wf"
WF_UV = "loc_wf_uv"
NL   = "loc_nl"
BQ   = "loc_bq"
EU   = "loc_eu"
DE   = "loc_de"
FR   = "loc_fr"
TF   = "loc_tf"
FRTF = "loc_fr_tf"

GEO_RESOURCE   = "https://w3id.org/odrl-kb/dpv-loc-geo"
JURIS_RESOURCE = "https://w3id.org/odrl-kb/dpv-loc-juris"
ISO_BT         = "https://w3id.org/odrl-kb/dpv-loc/iso"
BINDING_GEO    = "https://w3id.org/odrl-kb/profile/b-spatial-dpvloc-geo"
BINDING_JURIS  = "https://w3id.org/odrl-kb/profile/b-spatial-dpvloc-juris"
INCLUDES_GEO   = ["KGE000-0.ax", "LOC-dpvloc-geo.ax"]
INCLUDES_JURIS = ["KGE000-0.ax", "LOC-dpvloc-juris.ax"]
INCLUDES_ISO   = INCLUDES_GEO + ["LOC-dpvloc-iso.ax"]

GEO_RESOURCE   = "https://w3id.org/odrl-kb/dpv-loc-geo"
JURIS_RESOURCE = "https://w3id.org/odrl-kb/dpv-loc-juris"
EMPTY_BT       = "https://w3id.org/odrl-kb/dpv-loc/empty"
ISO_BT         = "https://w3id.org/odrl-kb/dpv-loc/iso"



def _decls(*concepts):
    lines = ["(declare-sort Concept 0)"]
    lines += [f"(declare-fun {c} () Concept)" for c in concepts]
    lines.append("(declare-fun kge_leq (Concept Concept) Bool)")
    return "\n".join(lines)


_TTL_HEAD = """\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix loc:     <https://w3id.org/dpv/loc#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .
"""

def C(op, *vals, side="offer"):
    return Constraint(op, tuple(vals), side)
 
 
def _iso(*pairs):
    """Explicit ISO rule instances, one fof per pair, named bg_dist_ as
    KGC334 names its one instance, plus the matching :named SMT lines."""
    fof = ["% Background theory: instances of the ISO 3166 uniqueness rule,",
           "% stated in LOC-dpvloc-iso.ax and instantiated here.", ""]
    smt = ["; Instances of the registry rule this problem adopts, named as",
           "; the TPTP side names them."]
    for a, b in pairs:
        n = f"bg_dist_{a}_{b}"
        fof.append(f"fof({n}, axiom,\n    {a} != {b}).")
        smt.append(f"(assert (! (not (= {a} {b})) :named {n}))")
    return "\n".join(fof) + "\n", "\n".join(smt)
 
 
_TTL_HEAD = """\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix loc:     <https://w3id.org/dpv/loc#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .
"""
 
 
def _cnode(cid, op, vals):
    ro = " ,\n        ".join(f"loc:{v}" for v in vals)
    return f"""kgc:{cid} a odrl:Constraint ;
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:{op} ;
    odrl:rightOperand {ro} .
"""
 
 
def _side(pid, role, cls, title, party_line, constraints, connective=None):
    """One policy.  constraints: list of (op, [vals]).  With more than one
    constraint a Logical Constraint under `connective` (or, xone) holds
    them, as ODRL 2.2 serialises it: an rdf:List of constraint IRIs."""
    n = pid[3:]
    cids = [f"{pid}-{role}-c{i+1}" for i in range(len(constraints))]
    if len(cids) == 1:
        cref = f"kgc:{cids[0]}"
        lc = ""
    else:
        cref = f"kgc:{pid}-{role}-lc"
        lc = (f"kgc:{pid}-{role}-lc a odrl:LogicalConstraint ;\n"
              f"    odrl:{connective} ( " + " ".join(f"kgc:{c}" for c in cids)
              + " ) .\n")
    body = (f"drk:{role}-{n} a odrl:{cls} ;\n"
            f'    dcterms:title "{title}"@en ;\n'
            + (f"    {party_line}" if party_line else "")
            + f"    odrl:permission kgc:{pid}-{role}-r1 .\n"
            f"kgc:{pid}-{role}-r1 a odrl:Permission ;\n"
            f"    odrl:action odrl:use ;\n"
            f"    odrl:target drk:manuscripts ;\n"
            f"    odrl:constraint {cref} .\n" + lc)
    for cid, (op, vals) in zip(cids, constraints):
        body += _cnode(cid, op, vals)
    return body
 
 
def _ttl2(pid, offer_title, offer_cs, req_title, req_cs, connective=None):
    return (_TTL_HEAD
            + _side(pid, "offer", "Set", "Offer: " + offer_title,
                    "odrl:assigner drk:library ;\n", offer_cs, connective)
            + _side(pid, "request", "Request", "Request: " + req_title,
                    "", req_cs))
 
 
_ISO_385 = _iso((DE_NW, DE_BY))
_ISO_387 = _iso((DE_HH, DE_BY), (DE_HH, DE_BE))
_ISO_390 = _iso((DE_NW, DE_BY))

def _ttl(pid, offer_title, offer_op, offer_val, req_title, req_val):
    return _TTL_HEAD + f"""
drk:offer-{pid[3:]} a odrl:Set ;
    dcterms:title "Offer: {offer_title}"@en ;
    odrl:assigner drk:library ;
    odrl:permission kgc:{pid}-offer-r1 .

kgc:{pid}-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:{pid}-offer-c1 .

kgc:{pid}-offer-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:{offer_op} ;
    odrl:rightOperand loc:{offer_val} .

drk:request-{pid[3:]} a odrl:Request ;
    dcterms:title "Request: {req_title}"@en ;
    odrl:permission kgc:{pid}-request-r1 .

kgc:{pid}-request-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:{pid}-request-c1 .

kgc:{pid}-request-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:eq ;
    odrl:rightOperand loc:{req_val} ."""


PROBLEMS = [

 {
        "id":                "KGC330",
        "subdir":            "verdict",
        "name":              "spatial, isPartOf loc:NL against eq loc:BQ",
        "left_operand":      "spatial",
        "sort":              "mer",
        "resource":          GEO_RESOURCE,
        "background_theory": EMPTY_BT,
        "binding":           BINDING_GEO,
        "includes":          INCLUDES_GEO,
        "summary": (
            "A library permits use within the Netherlands; a researcher "
            "asks to use the material in Bonaire. DPV places Bonaire "
            "within the Netherlands."
        ),
        "description": (
            "A library permits use of its digitised manuscripts anywhere "
            "within the Netherlands; a researcher asks to use them in "
            "Bonaire, Sint Eustatius and Saba. DPV asserts BQ "
            "skos:broader NL, so the constraints are Compatible on that "
            "one published relation.\n\n"
            "This is the baseline for the resource: one hop, no "
            "transitivity, nothing declared by the parties. It is also "
            "the control for KGC380, which puts the same request against "
            "an offer naming the European Union. There the verdict is "
            "Compatible as well, by composing this assertion with the "
            "one placing the Netherlands in the EU, and Bonaire lies "
            "outside EU territory. The two problems differ in one edge "
            "of the offer and in the binding."
        ),

        "fof_decls": """\
% Background theory: empty.  The extension asserts no disjointness between
% places and no distinctness between the codes it lists.
""",
        "fof_witness": f"""\
( ( kge_leq({NL}, {NL}) & {NL} = {BQ} )
| ( kge_leq({BQ}, {NL}) & {BQ} = {BQ} ) )""",

        "expected_q1": "Satisfiable",
        "expected_q2": "Unsatisfiable",

        "smt2_logic": "UF",
        "smt2_decls": _decls(NL, BQ),
        "smt2_resource": f"""\
; Resource: the containment the extension publishes.
(assert (kge_leq {BQ} {NL}))""",
        "smt2_background": "",
        "smt2_witness": f"""\
(or (and (kge_leq {NL} {NL}) (= {NL} {BQ}))
    (and (kge_leq {BQ} {NL}) (= {BQ} {BQ})))""",

        "certificate": {
            "kind": "Refutation",
            # What the resource publishes, and what follows. Becomes the
            # report's rdfs:comment.
            "comment": "DPV says Bonaire is part of the Netherlands, so a "
                       "use in Bonaire is a use in the Netherlands and "
                       "both sides get what they asked for.",
            "premises": [
                ("fromResource", "loc:BQ is within loc:NL"),
            ],
        },

        "ttl": _ttl("KGC330", "use within the Netherlands", "isPartOf", "NL",
                    "use in Bonaire, Sint Eustatius and Saba", "BQ"),
    },
    # -----------------------------------------------------------------
    # KGC331  The pair the resource exists for.  Compatible under the
    # jurisdictional reading; not grounded at all under the geographic.
    # -----------------------------------------------------------------
    {
        "id":                "KGC331",
        "twin" :               "KGC381",
        "subdir":            "verdict",
        "name":              "spatial, isPartOf loc:EU against eq loc:DE",
        "left_operand":      "spatial",
        "sort":              "mer",
        "resource":          JURIS_RESOURCE,
        "background_theory": EMPTY_BT,
        "binding":           BINDING_JURIS,
        "includes":          INCLUDES_JURIS,
        "summary": (
            "A library permits use within the European Union; a researcher "
            "asks to use the material in Germany. DPV places Germany in "
            "the EU, and this binding reads membership as containment."
        ),
        "description": (
            "Offer (spatial, isPartOf, loc:EU) against request (spatial, eq, "
            "loc:DE), under the jurisdictional reading.  Germany is a member "
            "of the European Union, the reading takes membership as the "
            "order, and the verdict is Compatible on one assertion.  Under "
            "the geographic reading the same constraints are well sorted and "
            "have no verdict: that reading takes only containment, loc:EU is "
            "not among its concepts, and the offer's right operand grounds "
            "to nothing.  The difference is the profile and nothing else."
        ),
        "fof_decls": """\
% Background theory: empty.
% Resource: the jurisdictional reading, containment together with union
% membership.  Under the geographic reading loc:EU is not a concept and this
% problem does not arise.
""",
        "fof_witness": f"""\
( ( kge_leq({EU}, {EU}) & {EU} = {DE} )
| ( kge_leq({DE}, {EU}) & {DE} = {DE} ) )""",
        "expected_q1": "Satisfiable",
        "expected_q2": "Unsatisfiable",
        "smt2_logic": "UF",
        "smt2_decls": _decls(EU, DE),
        "smt2_resource": f"""\
; Resource: membership, read as the order by the jurisdictional profile and
; not read at all by the geographic one.
(assert (kge_leq {DE} {EU}))""",
        "smt2_background": "",
        "smt2_witness": f"""\
(or (and (kge_leq {EU} {EU}) (= {EU} {DE}))
    (and (kge_leq {DE} {EU}) (= {DE} {DE})))""",
        "certificate": {
            "kind": "Refutation",
"comment": "DPV states that Germany is in the European Union, and "
           "the jurisdictional binding interprets this membership "
           "relation as containment, so the constraints are "
           "compatible. The geographic binding does not interpret "
           "membership as geographic containment.",
            "premises": [
                ("fromResource", "loc:DE is a member of loc:EU"),
            ],
        },
        "ttl": _ttl("KGC331", "use within the European Union", "isPartOf", "EU",
                    "use in Germany", "DE"),
    },
    # -----------------------------------------------------------------
    # KGC333  Two country codes the extension never separates.  Unknown,
    # and the pair to re-run once the parties adopt the registry rule.
    # -----------------------------------------------------------------
    {
        "id":                "KGC333",
        "twin":              "KGC334",
        "subdir":            "verdict",
        "name":              "spatial, eq loc:DE against eq loc:FR",
        "left_operand":      "spatial",
        "sort":              "mer",
        "resource":          GEO_RESOURCE,
        "background_theory": EMPTY_BT,
        "unknown_reason": "epistemic",
        "binding":           BINDING_GEO,
        "includes":          INCLUDES_GEO,
        "description": (
            "One side permits use in Germany, the other asks for France. "
            "Each names exactly one place, so both can be satisfied only "
            "if Germany and France are the same place. DPV never says "
            "they are different, so we cannot rule that out.\n\n"
            "The file looks as though it settles this and does not. "
            "Every country has an inverse concept, and non-DE is listed "
            "under France. But that says which countries belong to a "
            "complement, not that the two countries differ."
        ),
"summary": (
    "A library permits use in Germany; a researcher requests use in France."
),
        "fof_decls": """\
% Background theory: empty.  Two codes are not two places until something
% says so, and the extension says nothing.
""",
        "fof_witness": f"""\
( ( {DE} = {DE} & {DE} = {FR} )
| ( {FR} = {DE} & {FR} = {FR} ) )""",
        "expected_q1": "Satisfiable",
        "expected_q2": "Satisfiable",
        "smt2_logic": "UF",
        "smt2_decls": _decls(DE, FR),
        "smt2_resource": """\
; Resource: nothing about these two relates or separates them.""",
        "smt2_background": "",
        "smt2_witness": f"""\
(or (and (= {DE} {DE}) (= {DE} {FR}))
    (and (= {FR} {DE}) (= {FR} {FR})))""",
        "certificate": {
            "kind": "Models",
"comment": (
    "Neither the resource nor the parties assert that Germany and France "
    "are distinct, so the compatibility cannot be determined."
),
            "premises": [],
        },
        "ttl": _ttl("KGC333", "use in Germany", "eq", "DE",
                    "use in France", "FR"),
    },
    # -----------------------------------------------------------------
    # KGC334  KGC333 under the ISO rule.  Same resource, same constraints:
    # what moves the verdict is a rule the parties adopted, and the rule
    # is constrained by what the extension publishes about identity.
    # -----------------------------------------------------------------
    {
        "id":                "KGC334",
        "subdir":            "verdict",
        "name":              "spatial, eq loc:DE against eq loc:FR, under the "
                             "ISO 3166 uniqueness rule",
        "left_operand":      "spatial",
        "sort":              "mer",
        "resource":          GEO_RESOURCE,
        "twin":              "KGC333",
        "background_theory": ISO_BT,
        "binding":           BINDING_GEO,
        "includes":          INCLUDES_ISO,
        "description": (
            "The same two constraints as KGC333, with one addition: the "
            "parties adopt ISO 3166's rule that a code names one area. "
            "Germany and France are then different places, so no use can "
            "satisfy both sides, and the answer is definite.\n\n"
            "DPV itself says nothing of the kind. The rule is the "
            "parties', and the report records it as something they can "
            "withdraw. Note that the rule separates areas, not codes: "
            "DPV records thirty pairs of codes naming one area, and a "
            "rule applied to codes would contradict it."
        ),
        "summary": (
            "A library permits use in Germany; a researcher requests use in France."
        ),
        "fof_decls": """\
% Background theory: one instance of the ISO 3166 uniqueness rule.
%
% The rule is stated in LOC-dpvloc-iso.ax and ranges over 249 areas.  It is
% instantiated here rather than expanded there: a refutation should cite the
% inequation it used, not one term standing for thirty thousand.
fof(bg_dist_loc_de_loc_fr, axiom,
    loc_de != loc_fr).
""",
        "fof_witness": f"""\
( ( {DE} = {DE} & {DE} = {FR} )
| ( {FR} = {DE} & {FR} = {FR} ) )""",
        "expected_q1": "Unsatisfiable",
        "expected_q2": "Satisfiable",
        "smt2_logic": "UF",
        "smt2_decls": _decls(DE, FR),
        "smt2_resource": """\
; Resource: unchanged from KGC333.""",
        "smt2_background": """\
; The instance of the registry rule this problem adopts, named as the TPTP
; side names it so that a proof and an unsat core cite one assertion.
(assert (! (distinct loc_de loc_fr) :named bg_dist_loc_de_loc_fr))""",
        "smt2_witness": f"""\
(or (and (= {DE} {DE}) (= {DE} {FR}))
    (and (= {FR} {DE}) (= {FR} {FR})))""",
        "certificate": {
            "kind": "Refutation",
  "comment": (
        "Both constraints can be satisfied only if Germany and France "
        "denote the same place. The adopted rule asserts that they are "
        "distinct, so the constraints cannot both be satisfied."
    ),
            "premises": [
                ("fromBackgroundTheory",
                 "loc:DE and loc:FR are distinct areas under ISO 3166"),
            ],
        },
        "ttl": _ttl("KGC334", "use in Germany", "eq", "DE",
                    "use in France", "FR"),
    },
    # -----------------------------------------------------------------
    # KGC380  The Bonaire problem: composition that is false.  The verdict
    # is correct relative to the resource and wrong relative to the world.
    # -----------------------------------------------------------------
    {
        "id": "KGC380", "subdir": "verdict",
        "name": "spatial, isPartOf loc:EU against eq loc:BQ, jurisdictional",
        "left_operand": "spatial", "sort": "mer",
        "resource": JURIS_RESOURCE, "background_theory": EMPTY_BT,
        "summary": (
        "A library permits use within the European Union; a researcher "
        "requests use in Bonaire, Sint Eustatius and Saba."
        ),
        "binding": BINDING_JURIS, "includes": INCLUDES_JURIS,
        "tree": [C("isPartOf", EU), C("eq", BQ, side="request")],
        "expected_verdict": "Compatible",
        "expected_q1": "Satisfiable", "expected_q2": "Unsatisfiable",
        "reading_caveat": (
            "Bonaire, Sint Eustatius and Saba are overseas countries and "
            "territories (Art. 355 TFEU); EU law and the GDPR do not apply "
            "there. The jurisdictional reading composes territorial "
            "parthood (BQ within NL) with union membership (NL in EU) into "
            "BQ within EU, which is false."),
        "description": (
            "A library permits use within the European Union; a researcher "
            "asks to use the material in Bonaire. Under the jurisdictional "
            "reading DPV places BQ within NL and NL within EU, transitivity "
            "closes the chain, and the verdict is Compatible.\n\n"
            "The world disagrees: the Caribbean Netherlands lie outside EU "
            "territory. Nothing the semantics did is wrong; the reading "
            "that composes two relations is. KGC383 is the control, same "
            "reading, same depth, where the composition is true."),
        "certificate": {"kind": "Refutation",
"comment": (
    "The jurisdictional binding composes Bonaire's relation to the "
    "Netherlands with the Netherlands' relation to the EU, so the "
    "constraints are compatible under this reading."
),
            "premises": [("fromResource", "loc:BQ is within loc:NL"),
                         ("fromResource", "loc:NL is a member of loc:EU"),
                         ("fromOrderAxiom", "transitivity")]},
        "provenance": "EU-territory clauses (GDPR Chapter V pattern); "
                      "OCT status per Art. 355 TFEU.",
        "ttl": _ttl2("KGC380", "use within the European Union",
                     [("isPartOf", ["EU"])],
                     "use in Bonaire, Sint Eustatius and Saba",
                     [("eq", ["BQ"])]),
    },
    # -----------------------------------------------------------------
    # KGC381  KGC331 under the geographic binding: loc:EU is not a concept
    # of that slice, so the offer's value does not ground.
    # -----------------------------------------------------------------
    {
   "id": "KGC381", "subdir": "verdict",
   "twin": "KGC331",
    "name": "spatial, isPartOf loc:EU against eq loc:DE, geographic",
    "left_operand": "spatial", "sort": "mer",
    "resource": GEO_RESOURCE, "background_theory": EMPTY_BT,
    "binding": BINDING_GEO,
    "includes": INCLUDES_GEO,
    "ungrounded": "loc:EU",
     "summary": (
        "A library permits use within the European Union; a researcher "
        "requests use in Germany."
    ),
    "tree": [C("isPartOf", "loc:EU"), C("eq", DE, side="request")],
    "expected_verdict": "Unknown",
    "unknown_reason": "ungrounded",
        "description": (
            "The policies of KGC331 under the geographic binding, which "
            "reads containment only. The union edges are membership and "
            "are not read, so loc:EU is not a concept of this slice and "
            "the offer's value grounds to nothing. No query is built; the "
            "verdict is Unknown with the value as its certificate. Same "
            "policies, same file, different reading, no verdict."),
        "certificate": {"kind": "Ungrounded",
            "comment": "loc:EU names no concept of the geographic slice.",
            "premises": []},
        "provenance": "The two-readings pair of KGC331.",
        "ttl": _ttl2("KGC381", "use within the European Union",
                     [("isPartOf", ["EU"])], "use in Germany",
                     [("eq", ["DE"])]),
    },
    # -----------------------------------------------------------------
    # KGC382  One hop into a Land.  Baseline for subdivisions.
    # -----------------------------------------------------------------
    {
        "id": "KGC382", "subdir": "verdict",
        "name": "spatial, isPartOf loc:DE against eq loc:DE-NW",
        "left_operand": "spatial", "sort": "mer",
        "resource": GEO_RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING_GEO, "includes": INCLUDES_GEO,
        "tree": [C("isPartOf", DE), C("eq", DE_NW, side="request")],
        "expected_verdict": "Compatible",
        "expected_q1": "Satisfiable", "expected_q2": "Unsatisfiable",
        "description": (
            "Use within Germany against use in North Rhine-Westphalia. "
            "DPV places DE-NW within DE; one published assertion, both "
            "readings agree. The baseline for subdivisions."),
        "certificate": {"kind": "Refutation",
            "comment": "One containment edge.",
            "premises": [("fromResource", "loc:DE-NW is within loc:DE")]},
        "provenance": "Territorial licensing by federal state.",
        "ttl": _ttl2("KGC382", "use within Germany", [("isPartOf", ["DE"])],
                     "use in North Rhine-Westphalia", [("eq", ["DE-NW"])]),
    },
    # -----------------------------------------------------------------
    # KGC383  Two hops, two relations, and the composition is true.  The
    # control for KGC380.
    # -----------------------------------------------------------------
    {
        "id": "KGC383", "subdir": "verdict",
        "name": "spatial, isPartOf loc:EU against eq loc:DE-NW, jurisdictional",
        "left_operand": "spatial", "sort": "mer",
        "resource": JURIS_RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING_JURIS, "includes": INCLUDES_JURIS,
        "tree": [C("isPartOf", EU), C("eq", DE_NW, side="request")],
        "expected_verdict": "Compatible",
        "expected_q1": "Satisfiable", "expected_q2": "Unsatisfiable",
        "description": (
            "Use within the European Union against use in North "
            "Rhine-Westphalia, jurisdictional reading: DE-NW within DE, DE "
            "a member of EU, one transitivity step. Compatible, and here "
            "the composed answer is true. Read with KGC380: same reading, "
            "same depth, same two relations; the reading is faithful, and "
            "composing two relations is what can fail."),
        "certificate": {"kind": "Refutation",
            "comment": "Containment composed with membership; true here.",
            "premises": [("fromResource", "loc:DE-NW is within loc:DE"),
                         ("fromResource", "loc:DE is a member of loc:EU"),
                         ("fromOrderAxiom", "transitivity")]},
        "provenance": "EU-territory clause against a regional request.",
        "ttl": _ttl2("KGC383", "use within the European Union",
                     [("isPartOf", ["EU"])], "use in North Rhine-Westphalia",
                     [("eq", ["DE-NW"])]),
    },
    # -----------------------------------------------------------------
    # KGC384 / KGC385  Two Laender, nothing between them; then the ISO
    # rule over subdivision codes.
    # -----------------------------------------------------------------
    {
        "id": "KGC384", "subdir": "verdict",
        "twin": "KGC385",
        "name": "spatial, eq loc:DE-NW against eq loc:DE-BY",
        "left_operand": "spatial", "sort": "mer",
        "resource": GEO_RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING_GEO, "includes": INCLUDES_GEO,
        "tree": [C("eq", DE_NW), C("eq", DE_BY, side="request")],
        "expected_verdict": "Unknown", "unknown_reason": "epistemic",
        "expected_q1": "Satisfiable", "expected_q2": "Satisfiable",
        "description": (
            "Use in North Rhine-Westphalia against use in Bavaria. Both "
            "sides name one Land, and both can be satisfied only if the "
            "two are one place. The file relates the Laender to DE and to "
            "nothing sideways, and separates nothing: Unknown."),
        "certificate": {"kind": "Models",
            "comment": "One structure identifies the two Laender, one "
                       "keeps them apart; the file decides neither.",
            "premises": []},
        "provenance": "Regional licences of two neighbouring states.",
        "ttl": _ttl2("KGC384", "use in North Rhine-Westphalia",
                     [("eq", ["DE-NW"])], "use in Bavaria", [("eq", ["DE-BY"])]),
    },
    {
        "id": "KGC385", "subdir": "verdict",
        "twin": "KGC384",
        "name": "spatial, eq loc:DE-NW against eq loc:DE-BY, ISO rule",
        "left_operand": "spatial", "sort": "mer",
        "resource": GEO_RESOURCE, "background_theory": ISO_BT,
        "binding": BINDING_GEO, "includes": INCLUDES_ISO,
        "tree": [C("eq", DE_NW), C("eq", DE_BY, side="request")],
        "fof_decls": _ISO_385[0], "smt2_background": _ISO_385[1],
        "expected_verdict": "Incompatible",
        "expected_q1": "Unsatisfiable", "expected_q2": "Satisfiable",
        "description": (
            "KGC384 under the ISO 3166-2 rule, one code per subdivision "
            "within a country. The two Laender are then distinct areas, no "
            "use satisfies both sides, and the verdict is Incompatible on "
            "the parties' rule, withdrawable by dropping it."),
        "certificate": {"kind": "Refutation",
            "comment": "One instance of the registry rule over subdivision "
                       "codes.",
            "premises": [("fromBackgroundTheory",
                          "loc:DE-NW and loc:DE-BY are distinct areas")]},
        "provenance": "As KGC384; warrant ISO 3166-2.",
        "ttl": _ttl2("KGC385", "use in North Rhine-Westphalia",
                     [("eq", ["DE-NW"])], "use in Bavaria", [("eq", ["DE-BY"])]),
    },
    # -----------------------------------------------------------------
    # KGC386 / KGC387  A complement settled positively by declaration.
    # -----------------------------------------------------------------
    {
        "id": "KGC386", "subdir": "verdict",
"twin": "KGC387",
        "name": "spatial, isNoneOf {loc:DE-BY, loc:DE-BE} against eq loc:DE-HH",
        "left_operand": "spatial", "sort": "mer",
        "resource": GEO_RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING_GEO, "includes": INCLUDES_GEO,
        "tree": [C("isNoneOf", DE_BY, DE_BE), C("eq", DE_HH, side="request")],
        "expected_verdict": "Unknown", "unknown_reason": "epistemic",
        "expected_q1": "Satisfiable", "expected_q2": "Satisfiable",
        "description": (
            "Use anywhere except Bavaria and Berlin against use in "
            "Hamburg. Hamburg lies in the complement only if it differs "
            "from both, and the file publishes no distinctness: Unknown."),
        "certificate": {"kind": "Models",
            "comment": "A structure identifying Hamburg with Bavaria "
                       "defeats the witness; nothing published forbids it.",
            "premises": []},
        "provenance": "Exclusion clauses in regional licensing.",
        "ttl": _ttl2("KGC386", "use anywhere except Bavaria and Berlin",
                     [("isNoneOf", ["DE-BY", "DE-BE"])], "use in Hamburg",
                     [("eq", ["DE-HH"])]),
    },
    {
        "id": "KGC387", "subdir": "verdict",
        "twin": "KGC386",
        "name": "spatial, isNoneOf {loc:DE-BY, loc:DE-BE} against eq loc:DE-HH, "
                "ISO rule",
        "left_operand": "spatial", "sort": "mer",
        "resource": GEO_RESOURCE, "background_theory": ISO_BT,
        "binding": BINDING_GEO, "includes": INCLUDES_ISO,
        "tree": [C("isNoneOf", DE_BY, DE_BE), C("eq", DE_HH, side="request")],
        "fof_decls": _ISO_387[0], "smt2_background": _ISO_387[1],
        "expected_verdict": "Compatible",
        "expected_q1": "Satisfiable", "expected_q2": "Unsatisfiable",
        "description": (
            "KGC386 under the ISO rule: Hamburg is distinct from Bavaria "
            "and from Berlin, so it lies in the complement in every "
            "structure and the verdict is Compatible. The only case in "
            "the suite where a declaration settles a complement "
            "positively; KGC317's isNoneOf is Incompatible on the "
            "constraints alone."),
        "certificate": {"kind": "Refutation",
            "comment": "Two rule instances place Hamburg outside the "
                       "excluded pair.",
            "premises": [("fromBackgroundTheory",
                          "loc:DE-HH distinct from loc:DE-BY"),
                         ("fromBackgroundTheory",
                          "loc:DE-HH distinct from loc:DE-BE")]},
        "provenance": "As KGC386; warrant ISO 3166-2.",
        "ttl": _ttl2("KGC387", "use anywhere except Bavaria and Berlin",
                     [("isNoneOf", ["DE-BY", "DE-BE"])], "use in Hamburg",
                     [("eq", ["DE-HH"])]),
    },
    # -----------------------------------------------------------------
    # KGC388  or across two Laender: attribution must follow the branch.
    # -----------------------------------------------------------------
    {
        "id": "KGC388", "subdir": "verdict",
        "name": "spatial, or(isPartOf loc:DE-NW, isPartOf loc:DE-BY) against "
                "eq loc:DE-NW",
        "left_operand": "spatial", "sort": "mer",
        "resource": GEO_RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING_GEO, "includes": INCLUDES_GEO,
        "tree": [Or((C("isPartOf", DE_NW), C("isPartOf", DE_BY))),
                 C("eq", DE_NW, side="request")],
        "expected_verdict": "Compatible",
        "expected_q1": "Satisfiable", "expected_q2": "Unsatisfiable",
        "description": (
            "Use within North Rhine-Westphalia or within Bavaria against "
            "use in North Rhine-Westphalia. Compatible through the first "
            "disjunct, by reflexivity. The first verdict problem in the "
            "suite with a Logical Constraint; the refutation must cite the "
            "disjunct it used, which tests that attribution follows the "
            "branch."),
        "certificate": {"kind": "Refutation",
            "comment": "The first disjunct and reflexivity; the second "
                       "disjunct is not consulted.",
            "premises": [("fromOrderAxiom", "reflexivity")]},
        "provenance": "A licence covering either of two regions.",
        "ttl": _ttl2("KGC388", "use within North Rhine-Westphalia or Bavaria",
                     [("isPartOf", ["DE-NW"]), ("isPartOf", ["DE-BY"])],
                     "use in North Rhine-Westphalia", [("eq", ["DE-NW"])],
                     connective="or"),
    },
    # -----------------------------------------------------------------
    # KGC389 / KGC390  xone: a declaration making a positive verdict
    # through a negated literal.  A construction, and says so.
    # -----------------------------------------------------------------
    {
        "id": "KGC389", "subdir": "verdict",
        "twin": "KGC390",
        "name": "spatial, xone(eq loc:DE-NW, eq loc:DE-BY) against eq loc:DE-NW",
        "left_operand": "spatial", "sort": "mer",
        "resource": GEO_RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING_GEO, "includes": INCLUDES_GEO,
        "tree": [Xone((C("eq", DE_NW), C("eq", DE_BY))),
                 C("eq", DE_NW, side="request")],
        "expected_verdict": "Unknown", "unknown_reason": "epistemic",
        "expected_q1": "Satisfiable", "expected_q2": "Satisfiable",
        "description": (
            "Exactly one of North Rhine-Westphalia and Bavaria, against "
            "North Rhine-Westphalia. Expanded, the live alternative is NRW "
            "and not Bavaria, which needs the two to differ; the file does "
            "not say so: Unknown as published.\n\nA construction: rights "
            "managers rarely write exactly-one-region; the case exists to "
            "exercise the negated literal of the xone expansion."),
        "certificate": {"kind": "Models",
            "comment": "Identifying the two Laender makes both alternatives "
                       "true and exactly-one false.",
            "premises": []},
        "provenance": "Construction; exclusivity clauses are the nearest "
                      "practice.",
        "ttl": _ttl2("KGC389", "use in exactly one of North Rhine-Westphalia "
                     "and Bavaria",
                     [("eq", ["DE-NW"]), ("eq", ["DE-BY"])],
                     "use in North Rhine-Westphalia", [("eq", ["DE-NW"])],
                     connective="xone"),
    },
    {
        "id": "KGC390", "subdir": "verdict",
        "twin": "KGC389",
        "name": "spatial, xone(eq loc:DE-NW, eq loc:DE-BY) against eq loc:DE-NW, "
                "ISO rule",
        "left_operand": "spatial", "sort": "mer",
        "resource": GEO_RESOURCE, "background_theory": ISO_BT,
        "binding": BINDING_GEO, "includes": INCLUDES_ISO,
        "tree": [Xone((C("eq", DE_NW), C("eq", DE_BY))),
                 C("eq", DE_NW, side="request")],
        "fof_decls": _ISO_390[0], "smt2_background": _ISO_390[1],
        "expected_verdict": "Compatible",
        "expected_q1": "Satisfiable", "expected_q2": "Unsatisfiable",
        "description": (
            "KGC389 under the ISO rule: the two Laender differ, the "
            "negated literal holds, and the verdict is Compatible. The "
            "only place in the suite where a declaration yields a positive "
            "verdict through a negated literal."),
        "certificate": {"kind": "Refutation",
            "comment": "The rule instance discharges the negated literal.",
            "premises": [("fromBackgroundTheory",
                          "loc:DE-NW and loc:DE-BY are distinct areas")]},
        "provenance": "Construction, as KGC389.",
        "ttl": _ttl2("KGC390", "use in exactly one of North Rhine-Westphalia "
                     "and Bavaria",
                     [("eq", ["DE-NW"]), ("eq", ["DE-BY"])],
                     "use in North Rhine-Westphalia", [("eq", ["DE-NW"])],
                     connective="xone"),
    },
    # -----------------------------------------------------------------
    # KGC391  hasPart: the only up-set denotation.  Coverage-motivated.
    # -----------------------------------------------------------------
    {
        "id": "KGC391", "subdir": "verdict",
        "name": "spatial, hasPart loc:DE-NW against eq loc:DE",
        "left_operand": "spatial", "sort": "mer",
        "resource": GEO_RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING_GEO, "includes": INCLUDES_GEO,
        "tree": [C("hasPart", DE_NW), C("eq", DE, side="request")],
        "expected_verdict": "Compatible",
        "expected_q1": "Satisfiable", "expected_q2": "Unsatisfiable",
        "description": (
            "Use in an area that has North Rhine-Westphalia as a part, "
            "against use in Germany. Germany has NRW as a part, on the "
            "same assertion as KGC382 read upward. The only up-set "
            "operator in the table, and nothing else exercises it.\n\n"
            "Coverage-motivated: a spatial hasPart clause is rare in "
            "practice."),
        "certificate": {"kind": "Refutation",
            "comment": "The containment edge, read as the up-set.",
            "premises": [("fromResource", "loc:DE-NW is within loc:DE")]},
        "provenance": "Coverage; nearest practice is a national-scope "
                      "deployment that must include a region.",
        "ttl": _ttl2("KGC391", "use in an area containing North "
                     "Rhine-Westphalia", [("hasPart", ["DE-NW"])],
                     "use in Germany", [("eq", ["DE"])]),
    },
    # -----------------------------------------------------------------
    # KGC392  isNoneOf excludes areas by identity, not their parts.  The
    # verdict is faithful to ODRL's operator and defeats the drafter's
    # intent; the case the conclusion's isNotA remark needs.
    # -----------------------------------------------------------------
    {
        "id": "KGC392", "subdir": "verdict",
        "name": "spatial, isNoneOf {loc:WF} against eq loc:WF-UV, ISO rule",
        "left_operand": "spatial", "sort": "mer",
        "resource": GEO_RESOURCE, "background_theory": ISO_BT,
        "binding": BINDING_GEO, "includes": INCLUDES_ISO,
        "tree": [C("isNoneOf", WF), C("eq", WF_UV, side="request")],
        "fof_decls": _iso((WF_UV, WF))[0],
        "smt2_background": _iso((WF_UV, WF))[1],
        "expected_verdict": "Compatible",
        "expected_q1": "Satisfiable", "expected_q2": "Unsatisfiable",
        "description": (
            "Use anywhere except Wallis and Futuna, against use in Uvea, a "
            "commune the file places within Wallis and Futuna. isNoneOf "
            "excludes the named area by identity, Uvea is a different "
            "concept under the ISO rule, and the verdict is Compatible.\n\n"
            "The verdict is faithful to ODRL's set-based operator and "
            "defeats what the drafter meant: 'not in Wallis and Futuna' "
            "is a claim about parthood, and no ODRL operator tests the "
            "complement of a down-set. The spatial twin of neq EU not "
            "meaning outside the EU."),
        "certificate": {"kind": "Refutation",
            "comment": "Uvea is distinct from Wallis and Futuna, so it lies "
                       "in the complement; that it lies within it is not "
                       "consulted.",
            "premises": [("fromBackgroundTheory",
                          "loc:WF-UV distinct from loc:WF")]},
        "provenance": "Exclusion clauses; the drafting error they invite.",
        "ttl": _ttl2("KGC392", "use anywhere except Wallis and Futuna",
                     [("isNoneOf", ["WF"])], "use in Uvea",
                     [("eq", ["WF-UV"])]),
    },
]