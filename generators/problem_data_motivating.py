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

PROBLEMS = [

    # -----------------------------------------------------------------
    # KGC300  language, nominal.  B declares the two subtags distinct,
    # so no structure identifies them and no witness exists.
    # -----------------------------------------------------------------
    {
        "id":                "KGC300",
        "subdir":            "verdict",
        "name":              "language, eq bcp:de against eq bcp:fr",
        "left_operand":      "language",
        "sort":              "nom",
        "resource":          "https://w3id.org/odrl-kb/bcp47",
        "background_theory": "https://w3id.org/odrl-kb/bcp47/uniqueness",
        "includes":          ["KGE000-0.ax", "BCP47000-0.ax"],
        "description": (
            "Offer (language, eq, bcp:de) against request (language, eq, "
            "bcp:fr).  The registry's uniqueness rule places the two subtags "
            "in the background theory as distinct, so no model identifies "
            "them and the witness condition fails in every model."
        ),

        "fof_decls": """\
% Background theory: the registry's uniqueness rule, as distinctness.
fof(bg_disj_de_distinct_fr, axiom,
    bcp_de != bcp_fr).
""",
        # D != empty over the named concepts {de, fr}
        "fof_witness": """\
( ( bcp_de = bcp_de & bcp_de = bcp_fr )
| ( bcp_fr = bcp_de & bcp_fr = bcp_fr ) )""",

        "expected_q1": "Unsatisfiable",   # no model admits a witness
        "expected_q2": "Satisfiable",

        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)""",
        "smt2_resource": "",
        "smt2_background": """\
; Background theory: registry uniqueness, as distinctness.
(assert (distinct bcp_de bcp_fr))""",
        "smt2_witness": """\
(or (and (= bcp_de bcp_de) (= bcp_de bcp_fr))
    (and (= bcp_fr bcp_de) (= bcp_fr bcp_fr)))""",

        "certificate": {
            "kind": "Refutation",
            "comment": "No model admits a common use.  The two constraints "
                       "require one concept to be both subtags, and the "
                       "background theory holds them distinct.",
            "premises": [
                ("fromBackgroundTheory",
                 "bcp:de and bcp:fr are distinct (registry uniqueness)"),
            ],
        },
        "ttl": """\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix odrlkb:  <https://w3id.org/odrl-kb/bcp47#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .
@prefix vrep:    <https://w3id.org/odrl-kb/verdict-report#> .

drk:manuscripts a dcterms:Dataset ;
    dcterms:title "Digitised manuscripts, Bavarian State Library"@en .

drk:offer a odrl:Offer ;
    dcterms:title "BSB offer: access in German"@en ;
    odrl:assigner drk:library ;
    odrl:permission kgc:KGC300-offer-r1 .

kgc:KGC300-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC300-offer-c1 .

kgc:KGC300-offer-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:language ;
    odrl:operator odrl:eq ;
    odrl:rightOperand odrlkb:de .

drk:request a odrl:Request ;
    dcterms:title "BnF request: access in French"@en ;
    odrl:assignee drk:researcher ;
    odrl:permission kgc:KGC300-request-r1 .

kgc:KGC300-request-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC300-request-c1 .

kgc:KGC300-request-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:language ;
    odrl:operator odrl:eq ;
    odrl:rightOperand odrlkb:fr .""",
    },

    # -----------------------------------------------------------------
    # KGC301  purpose, taxonomic.  DPV neither places SR under NCP nor
    # separates them, so some models admit a witness and some do not.
    # -----------------------------------------------------------------
    {
        "id":                "KGC301",
        "subdir":            "verdict",
        "name":              "purpose, isA dpv:NCP against eq dpv:SR",
        "left_operand":      "purpose",
        "sort":              "tax",
        "resource":          "https://w3id.org/odrl-kb/dpv-purpose",
        "background_theory": "https://w3id.org/odrl-kb/dpv-purpose/declared",
        "unknown_reason": "epistemic",
        "includes":          ["KGE000-0.ax", "DPV-dpv-purposes.ax"],
        "description": (
            "Offer (purpose, isA, dpv:NonCommercialPurpose) against request "
            "(purpose, eq, dpv:ScientificResearch).  The vocabulary neither "
            "places one under the other nor separates them, so both queries "
            "are satisfiable and the verdict is Unknown."
        ),

        "fof_decls": """\
% The vocabulary is silent on the two concepts.  Nothing is asserted here:
% asserting a negative would be the closed-world reading this paper rejects.
""",
        # D != empty over the named concepts {ncp, sr}
        "fof_witness": """\
( ( kge_leq(dpv_non_commercial_purpose, dpv_non_commercial_purpose) & dpv_non_commercial_purpose = dpv_scientific_research )
| ( kge_leq(dpv_scientific_research,  dpv_non_commercial_purpose) & dpv_scientific_research  = dpv_scientific_research  ) )""",

        "expected_q1": "Satisfiable",     # some model admits a witness
        "expected_q2": "Satisfiable",     # some model admits none

        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun dpv_non_commercial_purpose () Concept)
(declare-fun dpv_scientific_research  () Concept)
(declare-fun kge_leq (Concept Concept) Bool)""",
        "smt2_asserts": """\
; The vocabulary says nothing about these two concepts.  No assertion is
; made here: the order axioms are emitted by the writer, in full.""",
        "smt2_witness": """\
(or (and (kge_leq dpv_non_commercial_purpose dpv_non_commercial_purpose) (= dpv_non_commercial_purpose dpv_scientific_research))
    (and (kge_leq dpv_scientific_research  dpv_non_commercial_purpose) (= dpv_scientific_research  dpv_scientific_research)))""",

        "certificate": {
            "kind": "Models",
            "comment": "Both queries are satisfiable, so some models admit a "
                       "common use and some do not.  The models differ on "
                       "whether dpv:ScientificResearch falls under "
                       "dpv:NonCommercialPurpose, which is what the "
                       "vocabulary leaves open.",
            "premises": [],
        },
        "ttl": """\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dpv:     <https://w3id.org/dpv#> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .
@prefix vrep:    <https://w3id.org/odrl-kb/verdict-report#> .

drk:manuscripts a dcterms:Dataset ;
    dcterms:title "Digitised manuscripts, Bavarian State Library"@en .

drk:offer a odrl:Offer ;
    dcterms:title "BSB offer: non-commercial research only"@en ;
    odrl:assigner drk:library ;
    odrl:permission kgc:KGC301-offer-r1 .

kgc:KGC301-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC301-offer-c1 .

kgc:KGC301-offer-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:isA ;
    odrl:rightOperand dpv:NonCommercialPurpose .

drk:request a odrl:Request ;
    dcterms:title "BnF request: scientific research"@en ;
    odrl:assignee drk:researcher ;
    odrl:permission kgc:KGC301-request-r1 .

kgc:KGC301-request-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC301-request-c1 .

kgc:KGC301-request-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:purpose ;
    odrl:operator odrl:eq ;
    odrl:rightOperand dpv:ScientificResearch .""",
    },

    # -----------------------------------------------------------------
    # KGC302  spatial, mereological.  The gazetteer places France within
    # Europe, so every model admits the witness.
    # -----------------------------------------------------------------
    {
        "id":                "KGC302",
        "subdir":            "verdict",
        "name":              "spatial, isPartOf gn:Europe against eq gn:France",
        "left_operand":      "spatial",
        "sort":              "mer",
        "resource":          "https://w3id.org/odrl-kb/geonames-europe",
        "background_theory": "https://w3id.org/odrl-kb/geonames-europe/admin-siblings",
        "includes":          ["KGE000-0.ax", "GN000-0.ax"],
        "description": (
            "Offer (spatial, isPartOf, gn:Europe) against request (spatial, "
            "eq, gn:France).  The gazetteer places France within Europe, so "
            "the witness condition holds in every model and the negated "
            "query is unsatisfiable."
        ),

        "fof_decls": """\
% Resource: the gazetteer places France within Europe.
fof(res_france_within_europe, axiom,
    kge_leq(gn_france, gn_europe)).
""",
        # D != empty over the named concepts {europe, france}
        "fof_witness": """\
( ( kge_leq(gn_europe, gn_europe) & gn_europe = gn_france )
| ( kge_leq(gn_france, gn_europe) & gn_france = gn_france ) )""",

        "expected_q1": "Satisfiable",
        "expected_q2": "Unsatisfiable",   # no model lacks a witness

        "smt2_logic": "UF",
        "smt2_decls": """\
(declare-sort Concept 0)
(declare-fun gn_europe () Concept)
(declare-fun gn_france () Concept)
(declare-fun kge_leq (Concept Concept) Bool)""",
        "smt2_asserts": """\
; Resource: France is within Europe.  The order axioms are emitted by the
; writer, in full and quantified, so this file states only the resource.
(assert (kge_leq gn_france gn_europe))""",
        "smt2_witness": """\
(or (and (kge_leq gn_europe gn_europe) (= gn_europe gn_france))
    (and (kge_leq gn_france gn_europe) (= gn_france gn_france)))""",

        "certificate": {
            "kind": "Refutation",
            "comment": "No model lacks a common use.  The gazetteer places "
                       "France within Europe, so France itself is an "
                       "admissible use in every model.",
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

drk:manuscripts a dcterms:Dataset ;
    dcterms:title "Digitised manuscripts, Bavarian State Library"@en .

drk:offer a odrl:Offer ;
    dcterms:title "BSB offer: recipients in Europe"@en ;
    odrl:assigner drk:library ;
    odrl:permission kgc:KGC302-offer-r1 .

kgc:KGC302-offer-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC302-offer-c1 .

kgc:KGC302-offer-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:isPartOf ;
    odrl:rightOperand <https://sws.geonames.org/6255148/> .

drk:request a odrl:Request ;
    dcterms:title "BnF request: recipient in France"@en ;
    odrl:assignee drk:researcher ;
    odrl:permission kgc:KGC302-request-r1 .

kgc:KGC302-request-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:KGC302-request-c1 .

kgc:KGC302-request-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:eq ;
    odrl:rightOperand <https://sws.geonames.org/3017382/> .""",
    },
]