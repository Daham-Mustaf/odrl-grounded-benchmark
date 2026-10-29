"""
problem_data_geonames.py
========================
Six problems over the GeoNames slice in geonames.ttl, at mer.  Four are
composed under xone.

    KGC303  xone(eq France, eq Germany)             x eq France  -> Unknown
    KGC304  the same, France and Germany distinct                -> Compatible
    KGC305  xone(isPartOf France, isPartOf Germany) x eq France,
            France and Germany distinct                          -> Unknown
    KGC306  the same, France and Germany disjoint                -> Compatible
    KGC308  isPartOf Germany                        x eq France  -> Unknown
    KGC309  the same, France and Germany disjoint                -> Incompatible

They replace the consent problems KGC344 to KGC347, which tested the same
expansion but permitted use under an invalid consent state.  "Use in
exactly one of two countries" is a clause a data provider writes, for
example to keep processing inside one jurisdiction.

What the four show
------------------
Expanded, xone(A, B) is (A and not B) or (B and not A).  For a use in
France the first alternative holds, so the verdict turns on the negated
second alternative.

With eq, that literal says France is not Germany.  GeoNames publishes no
distinctness, so a structure may identify the two, and then both
alternatives hold and "exactly one" fails: KGC303 is Unknown.  Declaring
the two countries distinct settles it: KGC304 is Compatible.

With isPartOf, the literal says France does not lie within Germany.
Distinctness does not settle that: two different areas can still lie one
within the other.  So KGC305, with the same declaration as KGC304, stays
Unknown.  Declaring the countries disjoint, meaning nothing lies within
both, settles it: France lies within itself, so it cannot also lie within
Germany, and KGC306 is Compatible.

The pair KGC304 and KGC305 is the point.  The same declaration settles the
identity question and leaves the order question open, which is why
distinctness and disjointness are separate declarations.

KGC308 and KGC309 put the point without xone.  "Use within Germany" against
"Use in France only" asks whether France lies within Germany.  Nothing
published says it does not, so KGC308 is Unknown.  Declared disjoint, France
and Germany have no common part, and France lies within itself, so it cannot
lie within Germany: KGC309 is Incompatible.  Declared only distinct, the
pair would stay Unknown, as KGC348 shows for consent.

The declarations
-----------------------
    empty      geonames-europe-empty.ttl      nothing declared
    declared   geonames-europe-declared.ttl   every feature distinct from
                                              every other (105 pairs)
    siblings   geonames-europe-siblings.ttl   features with the same parent
                                              disjoint (19 pairs)

Both declarations are written into the problems that use them, named as
the TPTP side names them, so the two provers cite one premise by one name.
"""

from compile import Constraint, Xone, right_operand
from pathlib import Path

import declarations

_BG = Path(__file__).resolve().parent.parent / "problems" / "background"
_DECLARED = declarations.load(_BG / "geonames-europe-declared.ttl")
_SIBLINGS = declarations.load(_BG / "geonames-europe-siblings.ttl")

FRANCE = "gn_france"
GERMANY = "gn_germany"

IRI = {
    FRANCE: "<https://sws.geonames.org/3017382/>",
    GERMANY: "<https://sws.geonames.org/2921044/>",
}

RESOURCE = "https://w3id.org/odrl-kb/geonames-europe"
EMPTY_BT = "https://w3id.org/odrl-kb/geonames-europe/empty"
DECLARED_BT = "https://w3id.org/odrl-kb/geonames-europe/declared"
SIBLINGS_BT = "https://w3id.org/odrl-kb/geonames-europe/siblings"
BINDING = "https://w3id.org/odrl-kb/profile/b-spatial-geonames"
INCLUDES = ["KGE000-0.ax", "GN000-0.ax"]


def C(op, *vals, side="offer"):
    return Constraint(op, tuple(vals), side)


def _dist(a, b):
    """Declared distinctness, ground, on both encodings."""
    return declarations.instances(
        _DECLARED, [(a, b)],
        ["% Declarations: the two countries declared distinct."],
        ["; The same distinctness, named as the TPTP side names it."])


def _disj(a, b):
    """Declared disjointness: nothing lies within both."""
    return declarations.instances(
        _SIBLINGS, [(a, b)],
        ["% Declarations: the two countries declared disjoint."],
        ["; The same disjointness, named as the TPTP side names it."],
        kind="disjoint")


_DIST = _dist(FRANCE, GERMANY)
_DISJ = _disj(FRANCE, GERMANY)

_TTL_HEAD = """\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .
"""


def _alt(op, *names):
    """One xone alternative: its operator and its right operand in Turtle."""
    return op, right_operand(op, [IRI[v] for v in names])


def _ttl(pid, alt1, alt2, title1, title2):
    """Policy 1: exactly one of two alternatives, each from _alt.
    Policy 2: use in France."""
    n = pid[3:]
    (op1, ro1), (op2, ro2) = alt1, alt2
    return _TTL_HEAD + f"""
drk:policy-{n}-1 a odrl:Set ;
    odrl:uid drk:policy-{n}-1 ;
    dcterms:title "{title1}"@en ;
    odrl:assigner drk:library ;
    odrl:permission kgc:{pid}-p1-r1 .

kgc:{pid}-p1-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:{pid}-p1-lc .

kgc:{pid}-p1-lc a odrl:LogicalConstraint ;
    odrl:xone ( kgc:{pid}-p1-c1 kgc:{pid}-p1-c2 ) .

kgc:{pid}-p1-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:{op1} ;
    odrl:rightOperand {ro1} .

kgc:{pid}-p1-c2 a odrl:Constraint ;
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:{op2} ;
    odrl:rightOperand {ro2} .

drk:policy-{n}-2 a odrl:Set ;
    odrl:uid drk:policy-{n}-2 ;
    dcterms:title "{title2}"@en ;
    odrl:assignee drk:researcher ;
    odrl:permission kgc:{pid}-p2-r1 .

kgc:{pid}-p2-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:{pid}-p2-c1 .

kgc:{pid}-p2-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:eq ;
    odrl:rightOperand {IRI[FRANCE]} .
"""


def _ttl_within(pid, title1, op1, value1, title2):
    """Policy 1: one constraint on a country.  Policy 2: use in France."""
    n = pid[3:]
    return _TTL_HEAD + f"""
drk:policy-{n}-1 a odrl:Set ;
    odrl:uid drk:policy-{n}-1 ;
    dcterms:title "{title1}"@en ;
    odrl:assigner drk:library ;
    odrl:permission kgc:{pid}-p1-r1 .

kgc:{pid}-p1-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:{pid}-p1-c1 .

kgc:{pid}-p1-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:{op1} ;
    odrl:rightOperand {IRI[value1]} .

drk:policy-{n}-2 a odrl:Set ;
    odrl:uid drk:policy-{n}-2 ;
    dcterms:title "{title2}"@en ;
    odrl:assignee drk:researcher ;
    odrl:permission kgc:{pid}-p2-r1 .

kgc:{pid}-p2-r1 a odrl:Permission ;
    odrl:action odrl:use ;
    odrl:target drk:manuscripts ;
    odrl:constraint kgc:{pid}-p2-c1 .

kgc:{pid}-p2-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:eq ;
    odrl:rightOperand {IRI[FRANCE]} .
"""


EQ_TREE = [Xone((C("eq", FRANCE), C("eq", GERMANY))),
           C("eq", FRANCE, side="request")]
PART_TREE = [Xone((C("isPartOf", FRANCE), C("isPartOf", GERMANY))),
             C("eq", FRANCE, side="request")]

EQ_TITLE = "Use in exactly one of France and Germany"
PART_TITLE = "Use within exactly one of France and Germany"
FR_TITLE = "Use in France only"
DE_TITLE = "Use within Germany"
WITHIN_TREE = [C("isPartOf", GERMANY), C("eq", FRANCE, side="request")]

EQ_ALTS = (_alt("eq", FRANCE), _alt("eq", GERMANY))
PART_ALTS = (_alt("isPartOf", FRANCE), _alt("isPartOf", GERMANY))

PROVENANCE = ("Data localisation: a provider keeps processing inside one "
              "jurisdiction and accepts either of two.")

PROBLEMS = [

    {
        "id": "KGC303", "subdir": "verdict",
        "twin": "KGC304",
        "name": "spatial, xone(eq France, eq Germany) against eq France",
        "left_operand": "spatial", "sort": "mer",
        "resource": RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING, "includes": INCLUDES,
        "tree": EQ_TREE,
        "expected_verdict": "Unknown",
        "expected_q1": "Satisfiable", "expected_q2": "Satisfiable",
        "summary": (
            "A library permits use in exactly one of France and Germany. "
            "A researcher's policy commits to use in France."),
        "description": (
            "GeoNames publishes no distinctness. A structure that "
            "identifies France with Germany makes both alternatives hold, "
            "so 'exactly one' fails there. Another structure keeps them "
            "apart. The verdict is Unknown."),
        "certificate": {"kind": "Models",
            "comment": (
                "GeoNames does not state that France and Germany are different. "
                "In a structure that keeps them apart, a use in France satisfies "
                "exactly one alternative, so both policies hold. In a structure that "
                "identifies them, both alternatives hold and 'exactly one' fails. So "
                "the verdict is Unknown."),
            "premises": []},
        "provenance": PROVENANCE,
        "ttl": _ttl("KGC303", *EQ_ALTS, EQ_TITLE, FR_TITLE),
    },

    {
        "id": "KGC304", "subdir": "verdict",
        "twin": "KGC303",
        "name": "spatial, xone(eq France, eq Germany) against eq France, "
                "countries distinct",
        "left_operand": "spatial", "sort": "mer",
        "resource": RESOURCE, "background_theory": DECLARED_BT,
        "binding": BINDING, "includes": INCLUDES,
        "fof_decls": _DIST[0], "smt2_background": _DIST[1],
        "tree": EQ_TREE,
        "expected_verdict": "Compatible",
        "expected_q1": "Satisfiable", "expected_q2": "Unsatisfiable",
        "summary": "As KGC303, with France and Germany declared distinct.",
        "description": (
            "The declaration makes France and Germany different "
            "countries. For a use in France only the first alternative "
            "holds, so 'exactly one' is satisfied and the verdict is "
            "Compatible."),
        "certificate": {"kind": "Refutation",
            "comment": (
                "France and Germany are declared distinct, so a use in "
                "France satisfies only the first alternative, and 'exactly "
                "one' holds."),
            "premises": [("fromDeclarations",
                          "gn:France and gn:Germany are distinct")]},
        "provenance": PROVENANCE,
        "ttl": _ttl("KGC304", *EQ_ALTS, EQ_TITLE, FR_TITLE),
    },

    {
        "id": "KGC305", "subdir": "verdict",
        "twin": "KGC306",
        "name": "spatial, xone(isPartOf France, isPartOf Germany) against "
                "eq France, countries distinct",
        "left_operand": "spatial", "sort": "mer",
        "resource": RESOURCE, "background_theory": DECLARED_BT,
        "binding": BINDING, "includes": INCLUDES,
        "fof_decls": _DIST[0], "smt2_background": _DIST[1],
        "tree": PART_TREE,
        "expected_verdict": "Unknown",
        "expected_q1": "Satisfiable", "expected_q2": "Satisfiable",
        "summary": (
            "A library permits use within exactly one of France and "
            "Germany. A researcher's policy commits to use in France. "
            "France and Germany are declared distinct."),
        "description": (
            "Distinctness states that France is not Germany. It does not "
            "state that France does not lie within Germany. A structure that "
            "places France within Germany makes both alternatives hold. "
            "The verdict is Unknown, with the same declaration that "
            "decides KGC304."),
        "certificate": {"kind": "Models",
            "comment": (
                "France and Germany are declared distinct, but distinct areas can "
                "still lie one within the other. In a structure where France does not "
                "lie within Germany, a use in France satisfies exactly one "
                "alternative, so both policies hold. In a structure that places France "
                "within Germany, both alternatives hold and 'exactly one' fails. So "
                "the verdict is Unknown."),
            "premises": []},
        "provenance": PROVENANCE,
        "ttl": _ttl("KGC305", *PART_ALTS, PART_TITLE, FR_TITLE),
    },

    {
        "id": "KGC306", "subdir": "verdict",
        "twin": "KGC305",
        "name": "spatial, xone(isPartOf France, isPartOf Germany) against "
                "eq France, countries disjoint",
        "left_operand": "spatial", "sort": "mer",
        "resource": RESOURCE, "background_theory": SIBLINGS_BT,
        "binding": BINDING, "includes": INCLUDES,
        "fof_decls": _DISJ[0], "smt2_background": _DISJ[1],
        "tree": PART_TREE,
        "expected_verdict": "Compatible",
        "expected_q1": "Satisfiable", "expected_q2": "Unsatisfiable",
        "summary": (
            "As KGC305, with France and Germany declared disjoint: nothing "
            "lies within both."),
        "description": (
            "France lies within itself. Since nothing lies within both "
            "countries, France does not lie within Germany, only the first "
            "alternative holds, and the verdict is Compatible."),
        "certificate": {"kind": "Refutation",
            "comment": (
                "France lies within itself, and nothing lies within both "
                "France and Germany. So France does not lie within "
                "Germany, and 'exactly one' holds."),
            "premises": [("fromDeclarations",
                          "nothing lies within both gn:France and "
                          "gn:Germany")]},
        "provenance": PROVENANCE,
        "ttl": _ttl("KGC306", *PART_ALTS, PART_TITLE, FR_TITLE),
    },
    # -----------------------------------------------------------------
    # KGC308 / KGC309  Does France lie within Germany?  Nothing published
    # says it does not; the siblings declaration does.
    # -----------------------------------------------------------------
    {
        "id": "KGC308", "subdir": "verdict",
        "twin": "KGC309",
        "name": "spatial, isPartOf Germany against eq France",
        "left_operand": "spatial", "sort": "mer",
        "resource": RESOURCE, "background_theory": EMPTY_BT,
        "binding": BINDING, "includes": INCLUDES,
        "tree": WITHIN_TREE,
        "expected_verdict": "Unknown",
        "expected_q1": "Satisfiable", "expected_q2": "Satisfiable",
        "summary": (
            "A library permits use within Germany. A researcher's policy "
            "commits to use in France."),
        "description": (
            "A use in France satisfies both policies only if France lies "
            "within Germany. GeoNames places both countries within Europe "
            "and publishes nothing that keeps France out of Germany. A "
            "structure that places France within Germany admits the use, "
            "and one that does not, admits none. The verdict is Unknown. "
            "KGC309 adds the declarations that decide it."),
        "certificate": {"kind": "Models",
            "comment": (
                "GeoNames places France and Germany within Europe and "
                "nothing more. A structure that places France within "
                "Germany admits a use in France under both policies. A "
                "structure that does not, admits none. Nothing published "
                "places France outside Germany, so the verdict is "
                "Unknown."),
            "premises": []},
        "provenance": "Data localisation: a provider keeps processing "
                      "inside one jurisdiction.",
        "ttl": _ttl_within("KGC308", DE_TITLE, "isPartOf", GERMANY,
                           FR_TITLE),
    },
    {
        "id": "KGC309", "subdir": "verdict",
        "twin": "KGC308",
        "name": "spatial, isPartOf Germany against eq France, countries "
                "disjoint",
        "left_operand": "spatial", "sort": "mer",
        "resource": RESOURCE, "background_theory": SIBLINGS_BT,
        "binding": BINDING, "includes": INCLUDES,
        "fof_decls": _DISJ[0], "smt2_background": _DISJ[1],
        "tree": WITHIN_TREE,
        "expected_verdict": "Incompatible",
        "expected_q1": "Unsatisfiable", "expected_q2": "Satisfiable",
        "summary": (
            "As KGC308, with the features that share a parent declared "
            "disjoint: nothing lies within both."),
        "description": (
            "France and Germany share a parent, Europe, and are declared "
            "disjoint. France lies within itself, so it cannot also lie "
            "within Germany, and no use satisfies both policies. The "
            "verdict is Incompatible. Declared only distinct, the two "
            "countries would leave it Unknown, because distinct areas can "
            "still lie one within the other."),
        "certificate": {"kind": "Refutation",
            "comment": (
                "France and Germany share a parent and are declared "
                "disjoint, so they have no common part. France lies within "
                "itself, so it cannot lie within Germany, and no use "
                "satisfies both policies. Distinctness alone would leave "
                "the verdict Unknown, as KGC348 shows for consent."),
            "premises": [("fromDeclarations",
                          "nothing lies within both gn:France and "
                          "gn:Germany")]},
        "provenance": "As KGC308.",
        "ttl": _ttl_within("KGC309", DE_TITLE, "isPartOf", GERMANY,
                           FR_TITLE),
    },

]
