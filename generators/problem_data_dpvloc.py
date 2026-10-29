"""
problem_data_dpvloc.py
======================
Six problems over the DPV Locations resource, at mer.

    KGC331  isPartOf EU x eq DE   -> Compatible    under the jurisdictional
                                                   reading; not grounded at
                                                   all under the territorial
    KGC333  eq DE       x eq FR   -> Unknown       nothing separates them
    KGC334  the same pair under the ISO rule       -> Incompatible
    KGC335  neq DE      x eq FR   -> Compatible    under the ISO rule
    KGC336  isAnyOf {DE, FR} x eq DE-BY -> Incompatible  identity, not containment
    KGC337  isAllOf {DE, FR} x eq DE    -> Incompatible  under the ISO rule

One resource, two readings
---------------------------
KGC331 is the reason this resource is in the suite.  Its two constraints are
well sorted: isPartOf requires parthood, the operand is bound at mer, and the
signature admits it without consulting anything.  Whether it has a verdict
depends on which of the file's relations the profile reads.

The territorial profile reads containment, and the European Union is not in
its concept set: the union edges are membership, which that profile does not
take, so dpv-loc:EU grounds to nothing and the constraint has no denotation.
The jurisdictional profile reads containment together with membership, and
the same constraint is Compatible on one statement.

Neither profile is the correct reading of the file.  They are two readings,
both faithful to what the extension publishes, differing in which published
relation they treat as the order.  Same operand, same sort, same file,
opposite outcome, and the profile is the only place the difference is
recorded.  That is the paper's claim with the resource held fixed.

The reading also changes the shape of the certificates.  Under the
territorial reading the containment order is two levels deep and no verdict
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

The statements are in the resource because the slice is faithful to what the
extension publishes, not because a verdict rests on them.  A resource whose
identities did carry a verdict would be worth having; this one does not, and
saying so is better than constructing a problem that appears to need it.

The witness condition
---------------------
Every pair uses subset-mode operators, so W(K) is the finite disjunction
over the concepts the grounding names.

  KGC331  D = {x | x <= eu} and {de},  named {eu, de}
          W = (eu <= eu & eu = de) | (de <= eu & de = de)
          Under the jurisdictional reading de <= eu is asserted and the
          verdict is Compatible.  Under the territorial reading eu is not a
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
          premise is a rule the parties adopted, not a statement the
          extension makes, and the certificate marks it withdrawable.
          The rule ranges over 4,977 identity classes, which is 12,382,776
          pairs, and is stated in the axiom file rather than expanded
          there: instantiating it would add twelve million inequations to
          every problem, and a refutation should cite the one it used.

On the ISO rule and the identity statements
--------------------------------------------
The rule is that ISO 3166 assigns one code to an area, so two codes name two
areas.  Applied to the codes directly it would contradict the extension,
which records thirty pairs of codes denoting one area.  It is therefore
applied to the areas: distinctness holds between the equivalence classes the
identity statements induce, and TF and FR-TF are one class represented by
its country code.

This is the only set of declarations in the suite constrained by something the
resource publishes.  A generated rule is the parties' to adopt, but not
theirs to adopt in a form the authority contradicts.

It is also the reason the identity statements are worth keeping even though
no verdict rests on them: they are not load-bearing for reachability, and
they are load-bearing for what the rule may say.
"""
from compile import right_operand as _ro, Constraint, Or, Xone
from pathlib import Path

import declarations

_DECL = declarations.load(
    Path(__file__).resolve().parent.parent / "problems" / "background" / "dpvloc-iso.ttl")
 
EU    = "loc_eu"
DE    = "loc_de"
DE_NW = "loc_de_nw"
DE_BY = "loc_de_by"
DE_BE = "loc_de_be"
DE_HH = "loc_de_hh"
WF    = "loc_wf"
WF_UV = "loc_wf_uv"
NL   = "loc_nl"
NL_BQ1 = "loc_nl_bq1"
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



_TTL_HEAD = """\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix loc:     <https://w3id.org/dpv/loc#> .
@prefix dpv-odrl: <https://w3id.org/dpv/mappings/odrl#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .
"""

def C(op, *vals, side="offer"):
    return Constraint(op, tuple(vals), side)
 
 
_TTL_HEAD = """\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix loc:     <https://w3id.org/dpv/loc#> .
@prefix dpv-odrl: <https://w3id.org/dpv/mappings/odrl#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .
"""
 
 
def _iso(*pairs):
    """Explicit ISO rule instances, one fof per pair, named bg_dist_ as
    KGC334 names its one instance, plus the matching :named SMT lines.
    The statements come from declarations.py, which refuses a pair the set
    does not state."""
    return declarations.instances(
        _DECL, pairs,
        ["% Declarations: instances of the ISO 3166 distinctness rule,",
         "% stated in LOC-dpvloc-iso.ax and instantiated here.", ""],
        ["; Instances of the registry rule this problem adopts, named as",
         "; the TPTP side names them."])


def _cnode(cid, op, vals):
    ro = _ro(op, [f"loc:{v}" for v in vals])
    return f"""kgc:{cid} a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:Location ;
    odrl:operator odrl:{op} ;
    odrl:rightOperand {ro} .
"""
 
 
def _side(pid, k, title, party_line, constraints, connective=None):
    """One policy.  constraints: list of (op, [vals]).  With more than one
    constraint a Logical Constraint under `connective` (or, xone) holds
    them, as ODRL 2.2 serialises it: an rdf:List of constraint IRIs."""
    n, role = pid[3:], f"p{k}"
    cids = [f"{pid}-{role}-c{i+1}" for i in range(len(constraints))]
    if len(cids) == 1:
        cref = f"kgc:{cids[0]}"
        lc = ""
    else:
        cref = f"kgc:{pid}-{role}-lc"
        lc = (f"kgc:{pid}-{role}-lc a odrl:LogicalConstraint ;\n"
              f"    odrl:{connective} ( " + " ".join(f"kgc:{c}" for c in cids)
              + " ) .\n")
    body = (f"drk:policy-{n}-{k} a odrl:Set ;\n"
            f"    odrl:uid drk:policy-{n}-{k} ;\n"
            f"    odrl:profile dpv-odrl: ;\n"
            f'    dcterms:title "{title[:1].upper() + title[1:]}"@en ;\n'
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
            + _side(pid, 1, offer_title,
                    "odrl:assigner drk:library ;\n", offer_cs, connective)
            + _side(pid, 2, req_title,
                    "odrl:assignee drk:researcher ;\n", req_cs))
 
 
_D334 = declarations.instances(
    _DECL, [(DE, FR)],
    ["% Declarations: one instance of the ISO 3166 distinctness rule.",
     "%",
     "% The rule is stated in LOC-dpvloc-iso.ax and ranges over 4,977 identity",
     "% classes, which is 12,382,776 pairs.  It is instantiated here rather than",
     "% expanded there: a refutation should cite the inequation it used, not one",
     "% term standing for twelve million."],
    ["; The instance of the registry rule this problem adopts, named as the TPTP",
     "; side names it so that a proof and an unsat core cite one statement."])
_ISO_DE_FR = _iso((DE, FR))
_ISO_336 = _iso((DE_BY, DE), (DE_BY, FR))

def _ttl(pid, offer_title, offer_op, offer_val, req_title, req_val):
    return _TTL_HEAD + f"""
drk:policy-{pid[3:]}-1 a odrl:Set ;
    odrl:uid drk:policy-{pid[3:]}-1 ;
    odrl:profile dpv-odrl: ;
    dcterms:title "{offer_title[:1].upper() + offer_title[1:]}"@en ;
    odrl:assigner drk:library ;
    odrl:permission kgc:{pid}-p1-r1 .

kgc:{pid}-p1-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:{pid}-p1-c1 .

kgc:{pid}-p1-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:Location ;
    odrl:operator odrl:{offer_op} ;
    odrl:rightOperand loc:{offer_val} .

drk:policy-{pid[3:]}-2 a odrl:Set ;
    odrl:uid drk:policy-{pid[3:]}-2 ;
    odrl:profile dpv-odrl: ;
    dcterms:title "{req_title[:1].upper() + req_title[1:]}"@en ;
    odrl:assignee drk:researcher ;
    odrl:permission kgc:{pid}-p2-r1 .

kgc:{pid}-p2-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:{pid}-p2-c1 .

kgc:{pid}-p2-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:Location ;
    odrl:operator odrl:eq ;
    odrl:rightOperand loc:{req_val} ."""


PROBLEMS = [

    # -----------------------------------------------------------------
    # KGC331  The pair the resource exists for.  Compatible under the
    # jurisdictional reading; not grounded at all under the territorial.
    # -----------------------------------------------------------------
    {
        "id":                "KGC331",
        "twin":              "KGC381",
        "subdir":            "verdict",
        "name":              "spatial, isPartOf loc:EU against eq loc:DE",
        "left_operand":      "spatial",
        "sort":              "mer",
        "resource":          JURIS_RESOURCE,
        "background_theory": EMPTY_BT,
        "binding":           BINDING_JURIS,
        "includes":          INCLUDES_JURIS,
        "tree": [C("isPartOf", EU), C("eq", DE, side="request")],
        "summary": (
            "A library permits use within the European Union; a "
            "researcher's policy commits to use in Germany. DPV places "
            "Germany in the EU, and this reading takes membership as "
            "containment."),
        "description": (
            "A library permits use within the European Union; a "
            "researcher's policy commits to use in Germany. Under the "
            "jurisdictional reading, Germany is a member of the European "
            "Union and the reading takes membership as containment, so the "
            "verdict is Compatible on one DPV statement. Under the "
            "territorial reading the same policies are rejected: that "
            "reading takes containment only, the European Union is not "
            "among the entries it uses, and the first policy's value names "
            "no entry of the vocabulary (KGC381). The difference is the "
            "reading and nothing else."),
        "fof_decls": """\
% Declarations: empty.
% Resource: the jurisdictional reading, containment together with union
% membership.  Under the territorial reading loc:EU is not a concept and this
% problem does not arise.
""",
        "expected_q1": "Satisfiable",
        "expected_q2": "Unsatisfiable",
        "smt2_logic": "UF",
        "smt2_background": "",
        "certificate": {
            "kind": "Refutation",
"comment": (
    "DPV states that Germany is a member of the European Union. The "
    "jurisdictional reading takes membership as containment, so a use in "
    "Germany is a use within the Union and both policies can be met. The "
    "territorial reading does not take membership as containment (see "
    "KGC381)."),
            "premises": [
                ("fromResource", "loc:DE is a member of loc:EU"),
            ],
        },
        "ttl": _ttl("KGC331", "Use within the European Union", "isPartOf", "EU",
                    "Use in Germany only", "DE"),
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
        "binding":           BINDING_GEO,
        "includes":          INCLUDES_GEO,
        "tree": [C("eq", DE), C("eq", FR, side="request")],
        "description": (
            "A library permits use in Germany, and a researcher's policy "
            "commits to use in France. Each names exactly one place, so "
            "both can be met only if Germany and France are the same place. "
            "DPV never states they are different, so that cannot be ruled "
            "out.\n\n"
            "DPV does list France among the places its definition calls "
            "'not in Germany'. The territorial reading does not use that "
            "list, and only the prose definition states that the list "
            "leaves Germany out. So nothing the reading uses separates the "
            "two countries."),
"summary": (
    "A library permits use in Germany. A researcher's policy commits to use "
    "in France."),
        "fof_decls": """\
% Declarations: empty.  Two codes are not two places until something
% says so, and the extension says nothing.
""",
        "expected_q1": "Satisfiable",
        "expected_q2": "Satisfiable",
        "smt2_logic": "UF",
        "smt2_background": "",
        "certificate": {
            "kind": "Models",
"comment": (
    "DPV does not state that Germany and France are different places. If "
    "they are the same place, a use in Germany meets both policies; if they "
    "are different, no use does. So the verdict is Unknown."),
            "premises": [],
        },
        "ttl": _ttl("KGC333", "Use in Germany only", "eq", "DE",
                    "Use in France only", "FR"),
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
                             "ISO 3166 distinctness rule",
        "left_operand":      "spatial",
        "sort":              "mer",
        "resource":          GEO_RESOURCE,
        "twin":              "KGC333",
        "background_theory": ISO_BT,
        "binding":           BINDING_GEO,
        "includes":          INCLUDES_ISO,
        "tree": [C("eq", DE), C("eq", FR, side="request")],
        "description": (
            "The same two constraints as KGC333, with one addition: the ISO "
            "3166 rule that different codes name different areas is "
            "adopted. Germany and France are then different places, so no "
            "use can meet both policies, and the verdict is Incompatible.\n\n"
            "DPV itself states nothing of the kind: the verdict rests on "
            "the declared rule, and without it the verdict is Unknown "
            "(KGC333)."),
        "maintainer_note": (
            "DPV records thirty identity pairs between codes, and the rule "
            "separates areas, not codes. Five of the thirty pair a group "
            "with a part of it and are not two names for one place: BQ with "
            "each of NL-BQ1, NL-BQ2 and NL-BQ3 (Bonaire, Saba and Sint "
            "Eustatius), and SJ with NO-21 and NO-22 (Svalbard and Jan "
            "Mayen). The rule does not depend on them."),
        "summary": (
            "As KGC333, with the ISO 3166 rule that different country codes "
            "name different countries."),
        "fof_decls": _D334[0],
        "expected_q1": "Unsatisfiable",
        "expected_q2": "Satisfiable",
        "smt2_logic": "UF",
        "smt2_background": _D334[1],
        "certificate": {
            "kind": "Refutation",
  "comment": (
      "Both policies can be met only if Germany and France are the same "
      "place. The declared ISO 3166 rule, that different codes name "
      "different areas, makes them different places, so no use meets both "
      "policies."),
            "premises": [
                ("fromDeclarations",
                 "loc:DE and loc:FR are distinct areas under ISO 3166"),
            ],
        },
        "ttl": _ttl("KGC334", "Use in Germany only", "eq", "DE",
                    "Use in France only", "FR"),
    },
    # -----------------------------------------------------------------
    # KGC335  neq over places: the complement of one country, against a
    # country the ISO rule keeps apart from it.
    # -----------------------------------------------------------------
    {
        "id": "KGC335", "subdir": "verdict",
        "name": "spatial, neq loc:DE against eq loc:FR, ISO rule",
        "left_operand": "spatial", "sort": "mer",
        "resource": GEO_RESOURCE, "background_theory": ISO_BT,
        "binding": BINDING_GEO, "includes": INCLUDES_ISO,
        "tree": [C("neq", DE), C("eq", FR, side="request")],
        "fof_decls": _ISO_DE_FR[0], "smt2_background": _ISO_DE_FR[1],
        "expected_verdict": "Compatible",
        "expected_q1": "Satisfiable", "expected_q2": "Unsatisfiable",
        "summary": (
            "A library permits use anywhere except Germany. A researcher's "
            "policy commits to use in France. The ISO 3166 rule makes the two "
            "countries different places."),
        "description": (
            "Use anywhere except Germany, against use in France. neq "
            "excludes Germany by identity. The ISO 3166 rule makes France a "
            "different place from Germany, so a use in France meets both "
            "policies and the verdict is Compatible. The same pair without "
            "the rule would be Unknown, because France might be the same "
            "place as Germany. KGC334 is the same pair under eq."),
        "certificate": {"kind": "Refutation",
            "comment": (
                "The ISO 3166 rule makes Germany and France different "
                "countries, so a use in France is a use outside Germany and "
                "satisfies both policies."),
            "premises": [("fromDeclarations",
                          "loc:DE and loc:FR are distinct areas under "
                          "ISO 3166")]},
        "provenance": "Exclusion clauses in data licences.",
        "ttl": _ttl2("KGC335", "Use anywhere except Germany",
                     [("neq", ["DE"])], "Use in France only",
                     [("eq", ["FR"])]),
    },
    # -----------------------------------------------------------------
    # KGC336  isAnyOf over places is identity: a part of a listed country
    # is not a listed country.
    # -----------------------------------------------------------------
    {
        "id": "KGC336", "subdir": "verdict",
        "name": "spatial, isAnyOf {loc:DE, loc:FR} against eq loc:DE-BY, "
                "ISO rule",
        "left_operand": "spatial", "sort": "mer",
        "resource": GEO_RESOURCE, "background_theory": ISO_BT,
        "binding": BINDING_GEO, "includes": INCLUDES_ISO,
        "tree": [C("isAnyOf", DE, FR), C("eq", DE_BY, side="request")],
        "fof_decls": _ISO_336[0], "smt2_background": _ISO_336[1],
        "expected_verdict": "Incompatible",
        "expected_q1": "Unsatisfiable", "expected_q2": "Satisfiable",
        "summary": (
            "A library permits use in at least one of Germany and France. A "
            "researcher's policy commits to use in Bavaria. The ISO 3166 rule "
            "makes Bavaria a different place from both countries."),
        "description": (
            "Use in at least one of Germany and France, against use in "
            "Bavaria. Bavaria lies within Germany, but isAnyOf compares by "
            "identity and not by containment, and Bavaria is not Germany. "
            "The ISO 3166 rule keeps Bavaria apart from Germany and from "
            "France, so no use meets both policies and the verdict is "
            "Incompatible. A drafter who meant Germany and its parts needs "
            "isPartOf, as in KGC382. The same pitfall in an exclusion is "
            "KGC392. Without the rule Bavaria might be the "
            "same area as Germany, and the verdict would be Unknown."),
        "certificate": {"kind": "Refutation",
            "comment": (
                "The ISO 3166 rule makes Bavaria distinct from Germany and "
                "from France, so it is neither value the first policy "
                "lists."),
            "premises": [("fromDeclarations",
                          "loc:DE-BY distinct from loc:DE"),
                         ("fromDeclarations",
                          "loc:DE-BY distinct from loc:FR")]},
        "provenance": "Territory lists in data licences.",
        "ttl": _ttl2("KGC336", "Use in at least one of Germany and France",
                     [("isAnyOf", ["DE", "FR"])], "Use in Bavaria only",
                     [("eq", ["DE-BY"])]),
    },
    # -----------------------------------------------------------------
    # KGC337  isAllOf over places, resting on the ISO rule as KGC376
    # rests on the BCP 47 rule.
    # -----------------------------------------------------------------
    {
        "id": "KGC337", "subdir": "verdict",
        "name": "spatial, isAllOf {loc:DE, loc:FR} against eq loc:DE, "
                "ISO rule",
        "left_operand": "spatial", "sort": "mer",
        "resource": GEO_RESOURCE, "background_theory": ISO_BT,
        "binding": BINDING_GEO, "includes": INCLUDES_ISO,
        "tree": [C("isAllOf", DE, FR), C("eq", DE, side="request")],
        "fof_decls": _ISO_DE_FR[0], "smt2_background": _ISO_DE_FR[1],
        "expected_verdict": "Incompatible",
        "expected_q1": "Unsatisfiable", "expected_q2": "Satisfiable",
        "summary": (
            "A library lends its digitised manuscripts to a Franco-German "
            "research programme and requires use at partner sites in both "
            "Germany and France. A researcher's policy commits to use in "
            "Germany only. The ISO 3166 rule makes the two countries "
            "different places."),
        "description": (
            "A Franco-German research programme requires that the digitised "
            "manuscripts be used at partner sites in both countries. "
            "isAllOf asks that the areas of the use include both countries, "
            "and eq asks that the use is Germany. The two hold together "
            "only if Germany and France are one place. The ISO 3166 rule is "
            "adopted: it makes them different places, so no use meets both "
            "policies and the verdict is Incompatible.\n\n"
            "The verdict rests on one declaration, the ISO 3166 rule, and "
            "on nothing DPV states. Without the rule Germany and France "
            "might be the same place and the verdict would be Unknown, as "
            "in KGC333. KGC376 is the same case over languages."),
        "maintainer_note": (
            "The refutation cites one premise, the instance of the ISO "
            "rule."),
        "certificate": {"kind": "Refutation",
            "comment": (
                "Germany and France are different places under the ISO 3166 "
                "rule. A use in both is not a use in Germany only, so no "
                "use meets both policies. The verdict rests on that rule: "
                "without it, Germany and France might be the same place, "
                "and a use in Germany would meet both policies."),
            "premises": [("fromDeclarations",
                          "loc:DE and loc:FR are distinct areas under "
                          "ISO 3166")]},
        "provenance": "Territory clauses that require several countries.",
        "ttl": _ttl2("KGC337", "Use in both Germany and France",
                     [("isAllOf", ["DE", "FR"])], "Use in Germany only",
                     [("eq", ["DE"])]),
    },
    # -----------------------------------------------------------------
    # KGC380  The Bonaire problem: composition that is false.  The verdict
    # is correct relative to the resource and wrong relative to the world.
    # -----------------------------------------------------------------
    {
        "id": "KGC380", "subdir": "verdict",
        "twin": "KGC383",
        "name": "spatial, isPartOf loc:EU against eq loc:NL-BQ1, jurisdictional",
        "left_operand": "spatial", "sort": "mer",
        "resource": JURIS_RESOURCE, "background_theory": EMPTY_BT,
        "summary": (
            "A library permits use within the European Union. A researcher's "
            "policy commits to use in Bonaire."),
        "binding": BINDING_JURIS, "includes": INCLUDES_JURIS,
        "tree": [C("isPartOf", EU), C("eq", NL_BQ1, side="request")],
        "expected_verdict": "Compatible",
        "expected_q1": "Satisfiable", "expected_q2": "Unsatisfiable",
        "reading_caveat": (
            "Bonaire is an overseas country and territory (Art. 355(2) "
            "TFEU); EU law and the GDPR do not apply there. The "
            "jurisdictional reading composes territorial parthood (NL-BQ1 "
            "within NL) with union membership (NL in EU) into NL-BQ1 "
            "within EU, which is false."),
        "description": (
            "A library permits use within the European Union; a "
            "researcher's policy commits to use in Bonaire. Under the "
            "jurisdictional reading DPV places Bonaire within the "
            "Netherlands and the Netherlands within the European Union, the "
            "two statements chain together, and the verdict is Compatible.\n\n"
            "The jurisdictional reading takes the Netherlands' EU "
            "membership as if all Dutch territory were EU territory. For "
            "North Rhine-Westphalia this gives the true answer; for "
            "Bonaire, an overseas territory outside the EU, it gives a "
            "false one. The error lies in the reading's choice, not in the "
            "reasoning. The territorial reading places Bonaire within the "
            "Netherlands, which is right (ISO 3166-2 lists Bonaire among the "
            "Netherlands' subdivisions). KGC383 is the case where the same "
            "reading gives the "
            "true answer."),
        "certificate": {"kind": "Refutation",
"comment": (
    "The jurisdictional reading takes union membership as containment. It "
    "chains Bonaire within the Netherlands (a DPV edge) with the "
    "Netherlands within the European Union (a DPV membership edge), so a "
    "use in Bonaire is a use within the Union and the verdict is "
    "Compatible. In law this does not hold: Bonaire is an overseas country "
    "and territory under Art. 355(2) TFEU, outside the ordinary territorial "
    "scope of EU law. The verdict follows from the reading, not from the "
    "law. KGC383 shows the same reading giving a correct answer for a "
    "German region."),
            "premises": [("fromResource", "loc:NL-BQ1 is within loc:NL"),
                         ("fromResource", "loc:NL is a member of loc:EU"),
                         ("fromOrderAxiom", "transitivity")]},
        "provenance": "EU-territory clauses (GDPR Chapter V pattern); "
                      "OCT status per Art. 355 TFEU.",
        "ttl": _ttl2("KGC380", "Use within the European Union",
                     [("isPartOf", ["EU"])],
                     "Use in Bonaire only",
                     [("eq", ["NL-BQ1"])]),
    },
    # -----------------------------------------------------------------
    # KGC381  KGC331 under the territorial binding: loc:EU is not a concept
    # of that slice, so the first policy's value does not ground.
    # -----------------------------------------------------------------
    {
        "id": "KGC381", "subdir": "verdict",
        "twin": "KGC331",
    "name": "spatial, isPartOf loc:EU against eq loc:DE, territorial",
    "left_operand": "spatial", "sort": "mer",
    "resource": GEO_RESOURCE, "background_theory": EMPTY_BT,
    "binding": BINDING_GEO,
    "includes": INCLUDES_GEO,
    "ungrounded": "loc:EU",
     "summary": (
         "As KGC331, under the territorial reading. A library permits use "
         "within the European Union, and a researcher's policy commits to "
         "use in Germany."),
    "tree": [C("isPartOf", "loc:EU"), C("eq", DE, side="request")],
        "description": (
            "The policies of KGC331 under the territorial reading, which "
            "takes containment only. The union edges are membership and are "
            "not used, so the European Union names no entry of the part of "
            "DPV used here and the first policy's value cannot be read. The "
            "policy is rejected and no verdict is computed. Same policies, "
            "same DPV source, different reading, no verdict."),
        "certificate": {"kind": "Ungrounded",
            "comment": (
                "The territorial reading does not use union membership, so "
                "the European Union names no entry of the part of DPV used "
                "here. The policy is therefore rejected, and no verdict is "
                "computed. KGC331 reads the same policies under the "
                "jurisdictional reading, where the Union is an entry and "
                "the verdict is Compatible."),
            "premises": []},
        "provenance": "The two-readings pair of KGC331.",
        "ttl": _ttl2("KGC381", "Use within the European Union",
                     [("isPartOf", ["EU"])], "Use in Germany only",
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
            "DPV places DE-NW within DE; one published statement, both "
            "readings agree. The baseline for subdivisions."),
        "summary": (
            "A library permits use within Germany. A researcher's policy "
            "commits to use in North Rhine-Westphalia."),
        "certificate": {"kind": "Refutation",
            "comment": (
                "DPV places North Rhine-Westphalia within Germany, so a use "
                "there meets both policies. Both readings agree on this "
                "case."),
            "premises": [("fromResource", "loc:DE-NW is within loc:DE")]},
        "provenance": "Territorial licensing by federal state.",
        "ttl": _ttl2("KGC382", "Use within Germany", [("isPartOf", ["DE"])],
                     "Use in North Rhine-Westphalia only", [("eq", ["DE-NW"])]),
    },
    # -----------------------------------------------------------------
    # KGC383  Two hops, two relations, and the composition is true.  The
    # control for KGC380.
    # -----------------------------------------------------------------
    {
        "id": "KGC383", "subdir": "verdict",
        "twin": "KGC380",
        "name": "spatial, isPartOf loc:EU against eq loc:DE-NW, jurisdictional",
        "left_operand": "spatial", "sort": "mer",
        "resource": JURIS_RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING_JURIS, "includes": INCLUDES_JURIS,
        "tree": [C("isPartOf", EU), C("eq", DE_NW, side="request")],
        "expected_verdict": "Compatible",
        "expected_q1": "Satisfiable", "expected_q2": "Unsatisfiable",
        "description": (
            "Use within the European Union against use in North "
            "Rhine-Westphalia, jurisdictional reading: North "
            "Rhine-Westphalia within Germany, Germany a member of the EU, "
            "one chaining step. Compatible, and here the answer is true. "
            "KGC380 is the case where the same reading gives a false "
            "answer."),
        "summary": (
            "A library permits use within the European Union. A researcher's "
            "policy commits to use in North Rhine-Westphalia."),
        "certificate": {"kind": "Refutation",
            "comment": (
                "The jurisdictional reading chains North Rhine-Westphalia "
                "within Germany (a DPV edge) with Germany's membership of "
                "the EU (a DPV edge). Here the result is also true in law: "
                "the Treaties apply to the Federal Republic of Germany "
                "(Art. 52(1) TEU)."),
            "premises": [("fromResource", "loc:DE-NW is within loc:DE"),
                         ("fromResource", "loc:DE is a member of loc:EU"),
                         ("fromOrderAxiom", "transitivity")]},
        "provenance": "EU-territory clause against a regional request.",
        "ttl": _ttl2("KGC383", "Use within the European Union",
                     [("isPartOf", ["EU"])], "Use in North Rhine-Westphalia only",
                     [("eq", ["DE-NW"])]),
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
            "Use within North Rhine-Westphalia or Bavaria, against use in "
            "North Rhine-Westphalia. The first alternative holds because "
            "every area lies within itself, so the verdict is Compatible "
            "without any DPV statement. In ODRL, or does not admit a use that "
            "mixes both alternatives."),
        "maintainer_note": (
            "The refutation must cite the alternative it used, which tests "
            "that attribution follows the branch."),
        "summary": (
            "A library permits use within North Rhine-Westphalia or within "
            "Bavaria. A researcher's policy commits to use in North "
            "Rhine-Westphalia."),
        "certificate": {"kind": "Refutation",
            "comment": (
                "The first alternative holds, because every area lies within "
                "itself. The second alternative does not need to be checked."),
            "premises": [("fromOrderAxiom", "reflexivity")]},
        "provenance": "A licence covering either of two regions.",
        "ttl": _ttl2("KGC388", "Use within North Rhine-Westphalia or Bavaria",
                     [("isPartOf", ["DE-NW"]), ("isPartOf", ["DE-BY"])],
                     "Use in North Rhine-Westphalia only", [("eq", ["DE-NW"])],
                     connective="or"),
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
            "A digitisation grant from North Rhine-Westphalia requires that "
            "the digitised manuscripts be made available across the whole "
            "state, so the library permits use only in an area that covers "
            "all of North Rhine-Westphalia. hasPart asks that the area of "
            "the use contain North Rhine-Westphalia. Germany has North "
            "Rhine-Westphalia as a part, on the same statement as KGC382 "
            "read upward, so a use in Germany meets both policies and the "
            "verdict is Compatible."),
        "summary": (
            "A library, bound by a digitisation grant from North "
            "Rhine-Westphalia, permits use only in an area that covers all "
            "of the state. A researcher's policy commits to use in Germany, "
            "which covers the state."),
        "certificate": {"kind": "Refutation",
            "comment": (
                "DPV places North Rhine-Westphalia within Germany, so Germany "
                "is an area that contains it, and a use in Germany satisfies "
                "both policies."),
            "premises": [("fromResource", "loc:DE-NW is within loc:DE")]},
        "provenance": "Coverage; nearest practice is a national-scope "
                      "deployment that must include a region.",
        "ttl": _ttl2("KGC391", "Use in an area that covers all of North Rhine-Westphalia", [("hasPart", ["DE-NW"])],
                     "Use in Germany only", [("eq", ["DE"])]),
    },
    # -----------------------------------------------------------------
    # KGC392  isNoneOf excludes areas by identity, not their parts.  The
    # verdict is faithful to ODRL's operator and defeats the drafter's
    # intent; the case the conclusion's isNotA remark needs.
    # -----------------------------------------------------------------
    {
        "id": "KGC392", "subdir": "verdict",
        "name": (
            "spatial, isNoneOf {loc:DE} against eq loc:DE-BY, ISO rule"),
        "left_operand": "spatial", "sort": "mer",
        "resource": GEO_RESOURCE, "background_theory": ISO_BT,
        "binding": BINDING_GEO, "includes": INCLUDES_ISO,
        "tree": [C("isNoneOf", DE), C("eq", DE_BY, side="request")],
        "fof_decls": _iso((DE_BY, DE))[0],
        "smt2_background": _iso((DE_BY, DE))[1],
        "expected_verdict": "Compatible",
        "expected_q1": "Satisfiable", "expected_q2": "Unsatisfiable",
        "description": (
            "Use anywhere except Germany, against use in Bavaria only. "
            "isNoneOf excludes the named area itself, Bavaria is a "
            "different area from Germany under the ISO rule, and the "
            "verdict is Compatible, although Bavaria lies within Germany.\n\n"
            "The verdict is faithful to ODRL's operator and defeats what "
            "the drafter meant: 'not in Germany' is a claim about parts, "
            "and isNoneOf only asks whether the place is Germany itself. A "
            "drafter who means Germany and all its parts writes a "
            "prohibition with isPartOf Germany. The same pitfall over "
            "a list of places is KGC336, and over purposes KGC397."),
        "summary": (
            "A library permits use anywhere except Germany. A researcher's "
            "policy commits to use in Bavaria, a state of Germany."),
        "certificate": {"kind": "Refutation",
            "comment": (
                "isNoneOf excludes the named area itself, not its parts. "
                "The ISO 3166 rule makes Bavaria distinct from Germany, so "
                "the use is not excluded, although DPV places Bavaria "
                "within Germany."),
            "premises": [("fromDeclarations",
                          "loc:DE-BY distinct from loc:DE")]},
        "provenance": "Exclusion clauses; the drafting error they invite.",
        "ttl": _ttl2("KGC392", "Use in any area except Germany",
                     [("isNoneOf", ["DE"])], "Use in Bavaria only",
                     [("eq", ["DE-BY"])]),
    },
]