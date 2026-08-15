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
        "subdir":            "Verdict",
        "name":              "language, eq bcp:de against eq bcp:fr",
        "left_operand":      "language",
        "sort":              "nom",
        "resource":          "https://example.org/resources/bcp47",
        "background_theory": "https://example.org/bt/bcp47-uniqueness",
        "includes":          ["KGE000-0.ax", "BCP47000-0.ax"],
        "description": (
            "Offer (language, eq, bcp:de) against request (language, eq, "
            "bcp:fr).  The registry's uniqueness rule places the two subtags "
            "in the background theory as distinct, so no model identifies "
            "them and the witness condition fails in every model."
        ),

        "fof_decls": """\
% Background theory: the registry's uniqueness rule, as distinctness.
fof(bt_de_distinct_fr, axiom,
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
        "smt2_asserts": """\
; Background theory: registry uniqueness, as distinctness.
(assert (distinct bcp_de bcp_fr))""",
        "smt2_witness": """\
(or (and (= bcp_de bcp_de) (= bcp_de bcp_fr))
    (and (= bcp_fr bcp_de) (= bcp_fr bcp_fr)))""",

        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix bcp:  <https://tools.ietf.org/html/bcp47#> .
@prefix ex:   <https://example.org/> .

ex:offer a odrl:Offer ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand odrl:language ;
                      odrl:operator odrl:eq ;
                      odrl:rightOperand bcp:de ] ] .

ex:request a odrl:Request ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand odrl:language ;
                      odrl:operator odrl:eq ;
                      odrl:rightOperand bcp:fr ] ] .""",
    },

    # -----------------------------------------------------------------
    # KGC301  purpose, taxonomic.  DPV neither places SR under NCP nor
    # separates them, so some models admit a witness and some do not.
    # -----------------------------------------------------------------
    {
        "id":                "KGC301",
        "subdir":            "Verdict",
        "name":              "purpose, isA dpv:NCP against eq dpv:SR",
        "left_operand":      "purpose",
        "sort":              "tax",
        "resource":          "https://example.org/resources/dpv-purpose",
        "background_theory": "https://example.org/bt/dpv-declared",
        "includes":          ["KGE000-0.ax", "DPV000-0.ax"],
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
; Order axioms, restricted to the named concepts.
(assert (kge_leq dpv_non_commercial_purpose dpv_non_commercial_purpose))
(assert (kge_leq dpv_scientific_research  dpv_scientific_research))
; The vocabulary says nothing further.  No negative assertion is made.""",
        "smt2_witness": """\
(or (and (kge_leq dpv_non_commercial_purpose dpv_non_commercial_purpose) (= dpv_non_commercial_purpose dpv_scientific_research))
    (and (kge_leq dpv_scientific_research  dpv_non_commercial_purpose) (= dpv_scientific_research  dpv_scientific_research)))""",

        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix dpv:  <https://w3id.org/dpv#> .
@prefix ex:   <https://example.org/> .

ex:offer a odrl:Offer ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand odrl:purpose ;
                      odrl:operator odrl:isA ;
                      odrl:rightOperand dpv:NonCommercialPurpose ] ] .

ex:request a odrl:Request ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand odrl:purpose ;
                      odrl:operator odrl:eq ;
                      odrl:rightOperand dpv:ScientificResearch ] ] .""",
    },

    # -----------------------------------------------------------------
    # KGC302  spatial, mereological.  The gazetteer places France within
    # Europe, so every model admits the witness.
    # -----------------------------------------------------------------
    {
        "id":                "KGC302",
        "subdir":            "Verdict",
        "name":              "spatial, isPartOf gn:Europe against eq gn:France",
        "left_operand":      "spatial",
        "sort":              "mer",
        "resource":          "https://example.org/resources/geonames-europe",
        "background_theory": "https://example.org/bt/geonames-admin-siblings",
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
; Order axioms, restricted to the named concepts.
(assert (kge_leq gn_europe gn_europe))
(assert (kge_leq gn_france gn_france))
; Resource: France is within Europe.
(assert (kge_leq gn_france gn_europe))""",
        "smt2_witness": """\
(or (and (kge_leq gn_europe gn_europe) (= gn_europe gn_france))
    (and (kge_leq gn_france gn_europe) (= gn_france gn_france)))""",

        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix gn:   <https://sws.geonames.org/> .
@prefix ex:   <https://example.org/> .

ex:offer a odrl:Offer ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand odrl:spatial ;
                      odrl:operator odrl:isPartOf ;
                      odrl:rightOperand <https://sws.geonames.org/6255148/> ] ] .

ex:request a odrl:Request ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand odrl:spatial ;
                      odrl:operator odrl:eq ;
                      odrl:rightOperand <https://sws.geonames.org/3017382/> ] ] .""",
    },
]