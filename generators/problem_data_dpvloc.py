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

NL   = "loc_nl"
BQ   = "loc_bq"
EU   = "loc_eu"
DE   = "loc_de"
FR   = "loc_fr"
TF   = "loc_tf"
FRTF = "loc_fr_tf"

GEO_RESOURCE   = "https://w3id.org/odrl-kb/dpv-loc-geo"
JURIS_RESOURCE = "https://w3id.org/odrl-kb/dpv-loc-juris"
EMPTY_BT       = "https://w3id.org/odrl-kb/dpv-loc/empty"
ISO_BT         = "https://w3id.org/odrl-kb/dpv-loc/iso"

# profile_ttl() in build_dpvloc.py names these exactly: ex:b-spatial-dpvloc-geo
# and ex:b-spatial-dpvloc-juris, under ex: <https://w3id.org/odrl-kb/profile/>.
BINDING_GEO    = "https://w3id.org/odrl-kb/profile/b-spatial-dpvloc-geo"
BINDING_JURIS  = "https://w3id.org/odrl-kb/profile/b-spatial-dpvloc-juris"

INCLUDES_GEO   = ["KGE000-0.ax", "LOC-dpvloc-geo.ax"]
INCLUDES_JURIS = ["KGE000-0.ax", "LOC-dpvloc-juris.ax"]
INCLUDES_ISO   = INCLUDES_GEO + ["LOC-dpvloc-iso.ax"]


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


def _ttl(pid, offer_title, offer_op, offer_val, req_title, req_val):
    return _TTL_HEAD + f"""
drk:bsb-offer-{pid[3:]} a odrl:Offer ;
    dcterms:title "BSB offer: {offer_title}"@en ;
    odrl:assigner drk:bavarian-state-library ;
    odrl:permission kgc:{pid}-offer-r1 .

kgc:{pid}-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:bsb-manuscripts ;
    odrl:constraint kgc:{pid}-offer-c1 .

kgc:{pid}-offer-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:{offer_op} ;
    odrl:rightOperand loc:{offer_val} .

drk:bnf-request-{pid[3:]} a odrl:Request ;
    dcterms:title "BnF request: {req_title}"@en ;
    odrl:assignee drk:french-national-library ;
    odrl:permission kgc:{pid}-request-r1 .

kgc:{pid}-request-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:bsb-manuscripts ;
    odrl:constraint kgc:{pid}-request-c1 .

kgc:{pid}-request-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:eq ;
    odrl:rightOperand loc:{req_val} ."""


PROBLEMS = [
    # -----------------------------------------------------------------
    # KGC330  One step of the containment order.  The smoke test for this
    # resource: if it fails, the slice or the boundary filter is wrong.
    # -----------------------------------------------------------------
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
        "description": (
            "Offer (spatial, isPartOf, loc:NL) against request (spatial, eq, "
            "loc:BQ).  The extension places Bonaire, Sint Eustatius and Saba "
            "within the Netherlands, so the witness holds in every model and "
            "the verdict is Compatible.  The refutation cites one resource "
            "premise and no transitivity: under the geographic reading the "
            "order is two levels deep and this is one step of it."
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
            "comment": "The extension places Bonaire within the Netherlands, "
                       "so every model admits the common use and its absence "
                       "is impossible.",
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
        "subdir":            "verdict",
        "name":              "spatial, isPartOf loc:EU against eq loc:DE",
        "left_operand":      "spatial",
        "sort":              "mer",
        "resource":          JURIS_RESOURCE,
        "background_theory": EMPTY_BT,
        "binding":           BINDING_JURIS,
        "includes":          INCLUDES_JURIS,
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
            "comment": "Germany is a member of the European Union and this "
                       "profile reads membership as the order.  The premise "
                       "is the extension's; what is the profile's is the "
                       "decision to read it, and the geographic profile does "
                       "not.",
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
        "subdir":            "verdict",
        "name":              "spatial, eq loc:DE against eq loc:FR",
        "left_operand":      "spatial",
        "sort":              "mer",
        "resource":          GEO_RESOURCE,
        "background_theory": EMPTY_BT,
        "binding":           BINDING_GEO,
        "includes":          INCLUDES_GEO,
        "description": (
            "Offer (spatial, eq, loc:DE) against request (spatial, eq, "
            "loc:FR).  Both denote singletons, so the constraints hold "
            "together only if the two codes denote one place.  The extension "
            "asserts no distinctness anywhere, so a model may identify them: "
            "Unknown.  The file looks as though it settles this and does "
            "not: every country has an inverse jurisdiction concept, and "
            "non-DE is narrower than France, but that says which concepts "
            "belong to a complement and not that the two are different."
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
            "comment": "Both queries are satisfiable.  The models differ on "
                       "whether the two codes denote one place, which no "
                       "assertion in the extension settles.",
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
        "background_theory": ISO_BT,
        "binding":           BINDING_GEO,
        "includes":          INCLUDES_ISO,
        "description": (
            "The constraints of KGC333 under a background theory generated "
            "from the rule that ISO 3166 assigns one code to an area.  No "
            "model then identifies the two, the witness fails everywhere, "
            "and the verdict is Incompatible.  The extension asserts no such "
            "distinctness: the rule is the parties', and the certificate "
            "marks it withdrawable.  The rule separates areas rather than "
            "codes, since the extension itself records thirty pairs of codes "
            "denoting one area, and a rule applied to the codes would "
            "contradict it."
        ),
        "fof_decls": """\
% Background theory: one instance of the ISO 3166 uniqueness rule.
%
% The rule is stated in LOC-dpvloc-iso.ax and ranges over 249 areas.  It is
% instantiated here rather than expanded there: a refutation should cite the
% inequation it used, not one term standing for thirty thousand.
fof(bt_loc_de_distinct_loc_fr, axiom,
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
(assert (! (distinct loc_de loc_fr) :named bt_loc_de_distinct_loc_fr))""",
        "smt2_witness": f"""\
(or (and (= {DE} {DE}) (= {DE} {FR}))
    (and (= {FR} {DE}) (= {FR} {FR})))""",
        "certificate": {
            "kind": "Refutation",
            "comment": "The two constraints require one place to be both "
                       "codes, and the registry rule holds the areas apart.  "
                       "The premise is a rule the parties adopted on the "
                       "authority of ISO 3166, not an assertion the "
                       "extension makes: abandoning the rule returns the "
                       "verdict to Unknown.",
            "premises": [
                ("fromBackgroundTheory",
                 "loc:DE and loc:FR are distinct areas under ISO 3166"),
            ],
        },
        "ttl": _ttl("KGC334", "use in Germany", "eq", "DE",
                    "use in France", "FR"),
    },
]