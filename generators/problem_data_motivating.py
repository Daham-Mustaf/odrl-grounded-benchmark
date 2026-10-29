"""
problem_data_motivating.py
==========================
The three constraint pairs of the motivating example, one per sort, one per
verdict.  Reproducing this table mechanically is the first milestone.

    KGC300  language  nom  eq bcp:de        x eq bcp:fr      -> Incompatible
    KGC301  purpose   tax  isA dpv:NCP      x eq dpv:SR      -> Unknown
    KGC302  spatial   mer  isPartOf gn:EU   x eq gn:FR       -> Compatible

Each problem is decided by two queries over the same witness condition.

The witness condition
---------------------
For the constraints K on one operand, W(K) is computed over the concepts the
grounding names.  All three pairs here use subset-mode operators only, with
no isAllOf and no isAnyOf, so F is empty and there are no A_k.  W reduces to
D != empty, which over the named concepts c is the finite disjunction

    OR_c ( c is in every subset-mode denotation of K )

and is therefore quantifier-free.  Worked per problem:

  KGC300  D = [[eq de]] and [[eq fr]] = {de} and {fr}
          W = (de = de & de = fr) | (fr = de & fr = fr)
            = (de = fr)                                  after simplification

  KGC301  D = [[isA ncp]] and [[eq sr]] = {x | x leq ncp} and {sr}
          W = (ncp leq ncp & ncp = sr) | (sr leq ncp & sr = sr)
            = (ncp = sr) | (sr leq ncp)
          with ncp = dpv_non_commercial_purpose, sr = dpv_scientific_research

  KGC302  D = [[isPartOf eu]] and [[eq fr]] = {x | x leq eu} and {fr}
          W = (eu = fr) | (fr leq eu)

We emit the unsimplified disjunction, since that is what Definition Witness
prescribes and what a generator produces mechanically.
"""

from compile import Constraint

DE, FR = "bcp_de", "bcp_fr"
NCP, SR = "dpv_non_commercial_purpose", "dpv_scientific_research"
EUROPE, FRANCE = "gn_europe", "gn_france"


def C(op, *vals, side="offer"):
    return Constraint(op, tuple(vals), side)


PROBLEMS = [

    # -----------------------------------------------------------------
    # KGC300  language, nominal.  B declares the two subtags distinct,
    # so no structure identifies them and no witness exists.
    # -----------------------------------------------------------------
    {
        "id":                "KGC300",
        "binding":           "https://w3id.org/odrl-kb/profile/b-language-bcp47",
        "subdir":            "verdict",
        "name":              "language, eq bcp:de against eq bcp:fr",
        "left_operand":      "language",
        "sort":              "nom",
        "resource":          "https://w3id.org/odrl-kb/bcp47",
        "background_theory": "https://w3id.org/odrl-kb/bcp47/distinct",
        "includes":          ["KGE000-0.ax", "BCP47000-0.ax", "BCP47001-0.ax"],
        "fof_decls": """\
% Declarations: the distinctness rule, BCP47001-0.ax.  The
% pair de, fr is one of its 105 instances.
""",
        "tree": [C("eq", DE), C("eq", FR, side="request")],
        "description": (
            "A German library permits use in German only, and a French "
            "library commits to use in French only. The two policies can "
            "hold together only if German and French are one language. The "
            "declared registry rule, that different primary language "
            "subtags name different languages, makes them two, so no use "
            "satisfies both."),
        "maintainer_note": (
            "The refutation cites the one distinctness instance. The "
            "witness fails in every structure."),

        # D != empty over the named concepts {de, fr}

        "expected_q1": "Unsatisfiable",   # no model admits a witness
        "expected_q2": "Satisfiable",

        "smt2_logic": "UF",

        "summary": (
            "A German library permits use of its manuscripts in German only. "
            "A French library's policy commits to use in French only."),
        "certificate": {
            "kind": "Refutation",
            "comment": (
                "Both policies can hold together only if German and French "
                "are one language. The declared rule that different primary "
                "language subtags name different languages, warranted by "
                "RFC 5646 sections 3 and 3.1.5, makes them two, so no use "
                "meets both policies."),
            "premises": [
                ("fromDeclarations",
                 "bcp:de and bcp:fr are distinct (distinctness rule)"),
            ],
        },
        "ttl": """\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix bcp47:   <https://w3id.org/odrl-kb/bcp47#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .
@prefix vrep:    <https://w3id.org/odrl-kb/verdict-report#> .

drk:policy-300-1 a odrl:Set ;
    odrl:uid drk:policy-300-1 ;
    dcterms:title "Use in German only"@en ;
    odrl:assigner drk:german-library ;
    odrl:permission kgc:KGC300-p1-r1 .

kgc:KGC300-p1-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC300-p1-c1 .

kgc:KGC300-p1-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:language ;
    odrl:operator odrl:eq ;
    odrl:rightOperand bcp47:de .

drk:policy-300-2 a odrl:Set ;
    odrl:uid drk:policy-300-2 ;
    dcterms:title "Use in French only"@en ;
    odrl:assignee drk:french-library ;
    odrl:permission kgc:KGC300-p2-r1 .

kgc:KGC300-p2-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC300-p2-c1 .

kgc:KGC300-p2-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:language ;
    odrl:operator odrl:eq ;
    odrl:rightOperand bcp47:fr .""",
    },

    # -----------------------------------------------------------------
    # KGC301  purpose, taxonomic.  DPV neither places SR under NCP nor
    # separates them, so some models admit a witness and some do not.
    # -----------------------------------------------------------------
    {
        "id":                "KGC301",
        "binding":           "https://w3id.org/odrl-kb/profile/b-purpose",
        "subdir":            "verdict",
        "name":              "purpose, isA dpv:NCP against eq dpv:SR",
        "left_operand":      "purpose",
        "sort":              "tax",
        "resource":          "https://w3id.org/odrl-kb/dpv-purposes",
        "background_theory": "https://w3id.org/odrl-kb/dpv-purposes/empty",
        "includes":          ["KGE000-0.ax", "DPV-dpv-purposes.ax"],
        "tree": [C("isA", NCP), C("eq", SR, side="request")],
        "description": (
            "A policy for non-commercial purposes and everything below "
            "them, against a commitment to scientific research. DPV neither "
            "places scientific research below non-commercial purpose nor "
            "keeps it out. If it lies there, a use meets both policies; if "
            "not, none does. So the verdict is Unknown."),
        "maintainer_note": "Both queries are satisfiable.",

        "fof_decls": """\
% The vocabulary is silent on the two concepts.  Nothing is asserted here:
% asserting a negative would be the closed-world reading this paper rejects.
""",
        # D != empty over the named concepts {ncp, sr}

        "expected_q1": "Satisfiable",     # some model admits a witness
        "expected_q2": "Satisfiable",     # some model admits none

        "smt2_logic": "UF",

        "summary": (
            "A German library permits use for non-commercial purposes or "
            "any narrower purpose. A French library's policy commits to use "
            "for scientific research only."),
        "certificate": {
            "kind": "Models",
            "comment": (
                "DPV does not state whether scientific research is a "
                "non-commercial purpose. If it is, a use for scientific "
                "research meets both policies; if it is not, no use does. "
                "So the verdict is Unknown."),
            "premises": [],
        },
        "ttl": """\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dpv:     <https://w3id.org/dpv#> .
@prefix dpv-odrl: <https://w3id.org/dpv/mappings/odrl#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .
@prefix vrep:    <https://w3id.org/odrl-kb/verdict-report#> .

drk:policy-301-1 a odrl:Set ;
    odrl:uid drk:policy-301-1 ;
    odrl:profile dpv-odrl: ;
    dcterms:title "Use for non-commercial purposes or any narrower purpose"@en ;
    odrl:assigner drk:german-library ;
    odrl:permission kgc:KGC301-p1-r1 .

kgc:KGC301-p1-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC301-p1-c1 .

kgc:KGC301-p1-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:Purpose ;
    odrl:operator odrl:isA ;
    odrl:rightOperand dpv:NonCommercialPurpose .

drk:policy-301-2 a odrl:Set ;
    odrl:uid drk:policy-301-2 ;
    odrl:profile dpv-odrl: ;
    dcterms:title "Use for scientific research only"@en ;
    odrl:assignee drk:french-library ;
    odrl:permission kgc:KGC301-p2-r1 .

kgc:KGC301-p2-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC301-p2-c1 .

kgc:KGC301-p2-c1 a odrl:Constraint ;
    odrl:leftOperand dpv-odrl:Purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:ScientificResearch .""",
    },

    # -----------------------------------------------------------------
    # KGC302  spatial, mereological.  The gazetteer places France within
    # Europe, so every model admits the witness.
    # -----------------------------------------------------------------
    {
        "id":                "KGC302",
        "binding":           "https://w3id.org/odrl-kb/profile/b-spatial-geonames",
        "subdir":            "verdict",
        "name":              "spatial, isPartOf gn:Europe against eq gn:France",
        "left_operand":      "spatial",
        "sort":              "mer",
        "resource":          "https://w3id.org/odrl-kb/geonames-europe",
        "background_theory": "https://w3id.org/odrl-kb/geonames-europe/empty",
        "includes":          ["KGE000-0.ax", "GN000-0.ax"],
        "tree": [C("isPartOf", EUROPE), C("eq", FRANCE, side="request")],
        # The gazetteer's labels (gn_...) are not parsed by the derivation, so
        # the one resource statement this verdict needs is carried here, under
        # the name the TPTP side gives it in fof_decls.
        "description": (
            "A German library permits use within Europe, and a French "
            "library commits to use in France only. GeoNames places France "
            "within Europe, so a use in France meets both policies."),
        "maintainer_note": (
            "The witness condition holds in every structure, and the "
            "negated query is unsatisfiable."),

        # D != empty over the named concepts {europe, france}

        "expected_q1": "Satisfiable",
        "expected_q2": "Unsatisfiable",   # no model lacks a witness

        "smt2_logic": "UF",

        "summary": (
            "A German library permits use within Europe. A French library's "
            "policy commits to use in France only."),
        "certificate": {
            "kind": "Refutation",
            "comment": (
                "GeoNames places France within Europe, so a use in France "
                "meets both policies."),
            "premises": [
                ("fromResource", "gn:France lies within gn:Europe"),
            ],
            "witness": "gn:France",
        },
        "ttl": """\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix gn:      <https://sws.geonames.org/> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .
@prefix vrep:    <https://w3id.org/odrl-kb/verdict-report#> .

drk:policy-302-1 a odrl:Set ;
    odrl:uid drk:policy-302-1 ;
    dcterms:title "Use within Europe"@en ;
    odrl:assigner drk:german-library ;
    odrl:permission kgc:KGC302-p1-r1 .

kgc:KGC302-p1-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC302-p1-c1 .

kgc:KGC302-p1-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:isPartOf ;
    odrl:rightOperand <https://sws.geonames.org/6255148/> .

drk:policy-302-2 a odrl:Set ;
    odrl:uid drk:policy-302-2 ;
    dcterms:title "Use in France only"@en ;
    odrl:assignee drk:french-library ;
    odrl:permission kgc:KGC302-p2-r1 .

kgc:KGC302-p2-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC302-p2-c1 .

kgc:KGC302-p2-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:eq ;
    odrl:rightOperand <https://sws.geonames.org/3017382/> .""",
    },
]