"""
problem_data_geonames.py
========================
Four problems over the GeoNames slice in geonames.ttl, at mer, all composed
under xone.

    KGC303  xone(eq France, eq Germany)             x eq France  -> Unknown
    KGC304  the same, France and Germany distinct                -> Compatible
    KGC305  xone(isPartOf France, isPartOf Germany) x eq France,
            France and Germany distinct                          -> Unknown
    KGC306  the same, France and Germany disjoint                -> Compatible

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
distinctness and disjointness are separate background theories.

The background theories
-----------------------
    empty      geonames-europe-empty.ttl      nothing declared
    declared   geonames-europe-declared.ttl   France and Germany distinct
    siblings   geonames-europe-siblings.ttl   France and Germany disjoint

Both declarations are written into the problems that use them, named as
the TPTP side names them, so the two provers cite one premise by one name.
"""

from compile import Constraint, Xone

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
    n = f"bg_dist_{a}_{b}"
    fof = ("% Background theory: the two countries declared distinct.\n"
           f"fof({n}, axiom,\n    {a} != {b}).\n")
    smt = ("; The same distinctness, named as the TPTP side names it.\n"
           f"(assert (! (not (= {a} {b})) :named {n}))")
    return fof, smt


def _disj(a, b):
    """Declared disjointness: nothing lies within both."""
    n = f"bg_disj_{a}_disjoint_{b}"
    fof = ("% Background theory: the two countries declared disjoint.\n"
           f"fof({n}, axiom,\n"
           f"    ! [X] : ~ ( kge_leq(X, {a}) & kge_leq(X, {b}) )).\n")
    smt = ("; The same disjointness, named as the TPTP side names it.\n"
           f"(assert (! (forall ((x Concept))\n"
           f"    (not (and (kge_leq x {a}) (kge_leq x {b}))))\n"
           f"  :named {n}))")
    return fof, smt


_DIST = _dist(FRANCE, GERMANY)
_DISJ = _disj(FRANCE, GERMANY)

_TTL_HEAD = """\
@prefix odrl:    <http://www.w3.org/ns/odrl/2/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix drk:     <https://w3id.org/odrl-kb/drk/> .
@prefix kgc:     <https://w3id.org/odrl-kb/problem/> .
"""


def _ttl(pid, op, title1, title2):
    """Policy 1: exactly one of France and Germany under op.
    Policy 2: use in France."""
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
    odrl:constraint kgc:{pid}-p1-lc .

kgc:{pid}-p1-lc a odrl:LogicalConstraint ;
    odrl:xone ( kgc:{pid}-p1-c1 kgc:{pid}-p1-c2 ) .

kgc:{pid}-p1-c1 a odrl:Constraint ;
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:{op} ;
    odrl:rightOperand {IRI[FRANCE]} .

kgc:{pid}-p1-c2 a odrl:Constraint ;
    odrl:leftOperand odrl:spatial ;
    odrl:operator odrl:{op} ;
    odrl:rightOperand {IRI[GERMANY]} .

drk:policy-{n}-2 a odrl:Set ;
    odrl:uid drk:policy-{n}-2 ;
    dcterms:title "{title2}"@en ;
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
FR_TITLE = "Use in France"

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
        "expected_verdict": "Unknown", "unknown_reason": "epistemic",
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
                "GeoNames does not state that France and Germany are "
                "different. If they are identified, both alternatives hold "
                "and 'exactly one' fails, so the verdict is Unknown."),
            "premises": []},
        "provenance": PROVENANCE,
        "ttl": _ttl("KGC303", "eq", EQ_TITLE, FR_TITLE),
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
            "premises": [("fromBackgroundTheory",
                          "gn:France and gn:Germany are distinct")]},
        "provenance": PROVENANCE,
        "ttl": _ttl("KGC304", "eq", EQ_TITLE, FR_TITLE),
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
        "expected_verdict": "Unknown", "unknown_reason": "epistemic",
        "expected_q1": "Satisfiable", "expected_q2": "Satisfiable",
        "summary": (
            "A library permits use within exactly one of France and "
            "Germany. A researcher's policy commits to use in France. "
            "France and Germany are declared distinct."),
        "description": (
            "Distinctness says France is not Germany. It does not say "
            "that France does not lie within Germany. A structure that "
            "places France within Germany makes both alternatives hold. "
            "The verdict is Unknown, with the same declaration that "
            "settles KGC304."),
        "certificate": {"kind": "Models",
            "comment": (
                "Distinct areas can still lie one within the other. A "
                "structure that places France within Germany makes both "
                "alternatives hold, so the verdict is Unknown."),
            "premises": []},
        "provenance": PROVENANCE,
        "ttl": _ttl("KGC305", "isPartOf", PART_TITLE, FR_TITLE),
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
            "premises": [("fromBackgroundTheory",
                          "nothing lies within both gn:France and "
                          "gn:Germany")]},
        "provenance": PROVENANCE,
        "ttl": _ttl("KGC306", "isPartOf", PART_TITLE, FR_TITLE),
    },
]
