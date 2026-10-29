"""
declarations.py
===============

A set of declarations is a file of RDF.  This module reads it and writes
the statements that follow from it, so that nothing else in the repository
decides which pairs a set declares.

What a set states, and how:

    distinctness   one owl:AllDifferent, attached with bind:states, whose
                   owl:members list the concepts.  Every pair of members is
                   declared distinct.  A single pair is the list of two.
    disjointness   bind:disjointFrom between two concepts: nothing lies
                   below both in the binding's order.  Not owl:disjointWith
                   (that is class semantics) and not a spatial predicate
                   (France and Germany touch).

One set per file.  bind:pairCount is the number of pairs the file states.

The statements the provers see are written here and nowhere else:

    fof_dist, smt_dist      a ground inequation, TPTP and SMT-LIB
    fof_disj, smt_disj      a disjointness, TPTP and SMT-LIB

Both encodings take the pair as the caller writes it.  The label follows
the order of the arguments, so the same two concepts named in the other
order are another label; certificates cite labels, and they stay.  Pairs
are matched unordered.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path

from rdflib import Graph, Namespace, RDF, URIRef
from rdflib.collection import Collection

BIND = Namespace("https://w3id.org/odrl-kb/binding#")
OWL = Namespace("http://www.w3.org/2002/07/owl#")
DCTERMS = Namespace("http://purl.org/dc/terms/")

BACKGROUND = Path("problems/background")


@dataclass
class Decl:
    iri: str
    path: Path
    rule: str
    origin: str
    pair_count: int | None
    scope: str
    applies_to: list
    members: list = field(default_factory=list)      # IRIs, in the order written
    disjoint: list = field(default_factory=list)     # (IRI, IRI), as written

    def distinct_pairs(self):
        m = self.members
        return [(m[i], m[j]) for i in range(len(m)) for j in range(i + 1, len(m))]

    def n_pairs(self) -> int:
        n = len(self.members)
        return n * (n - 1) // 2 + len(self.disjoint)

    def has(self, a, b, constant) -> str | None:
        """'distinct' or 'disjoint' when the set states the pair, in either
        order, else None.  a and b are constants; constant maps an IRI to
        the constant the encodings use for it."""
        names = {constant(m) for m in self.members}
        if a != b and a in names and b in names:
            return "distinct"
        for x, y in self.disjoint:
            if {constant(x), constant(y)} == {a, b}:
                return "disjoint"
        return None


def _local(term) -> str:
    return str(term).rsplit("#", 1)[-1].rsplit("/", 1)[-1]


def load(path) -> Decl:
    """Read one file.  Refuses a file that holds two sets, or two statements
    of distinctness: split the file."""
    path = Path(path)
    g = Graph().parse(path, format="turtle")
    sets = list(g.subjects(RDF.type, BIND.Declarations))
    if len(sets) != 1:
        raise ValueError(f"{path}: {len(sets)} sets of declarations; one per file")
    s = sets[0]
    one = lambda p: next(g.objects(s, p), None)
    members = []
    lists = []
    for node in g.subjects(RDF.type, OWL.AllDifferent):
        for lst in g.objects(node, OWL.members):
            lists.append([str(x) for x in Collection(g, lst)])
    if len(lists) > 1:
        raise ValueError(f"{path}: {len(lists)} owl:AllDifferent lists; one set "
                         f"carries one statement of distinctness")
    if lists:
        members = lists[0]
        if len(set(members)) != len(members):
            raise ValueError(f"{path}: a member is listed twice")
    disjoint = sorted((str(a), str(b)) for a, b in
                      g.subject_objects(BIND.disjointFrom))
    pc = one(BIND.pairCount)
    return Decl(
        iri=str(s), path=path,
        rule=_local(one(BIND.generatedBy)) if one(BIND.generatedBy) else "",
        origin=_local(one(BIND.origin)) if one(BIND.origin) else "",
        pair_count=int(pc) if pc is not None else None,
        scope=str(one(BIND.scopeCondition)) if one(BIND.scopeCondition) else "",
        applies_to=sorted(str(o) for o in g.objects(s, BIND.appliesTo)),
        members=members, disjoint=disjoint)


def load_all(directory=BACKGROUND) -> dict:
    return {d.iri: d for d in (load(p) for p in sorted(Path(directory).glob("*.ttl")))
            if d.pair_count}


# --- the constants the encodings use -----------------------------------------
#
# One function per resource, and it is the builder's own: a constant has one
# spelling, and the builder that writes the resource's axioms spells it.

def _geonames(iri):
    return {"https://sws.geonames.org/3017382/": "gn_france",
            "https://sws.geonames.org/2921044/": "gn_germany"}[str(iri)]


def constant_for(resource: str):
    """The function from a concept IRI to the constant of the encodings,
    for the resource a set applies to."""
    import build_consent, build_dpv, build_dpvloc, build_filetype
    import build_tom
    table = {
        "https://w3id.org/odrl-kb/dpv-purposes":
            lambda i: build_dpv.slug(_local(i)),
        "https://w3id.org/odrl-kb/eu-file-type":
            lambda i: build_filetype.slug(_local(i)),
        "https://w3id.org/odrl-kb/dpv-consent":
            lambda i: build_consent.slug(_local(i)),
        "https://w3id.org/odrl-kb/dpv-tom": build_tom.slug,
        "https://w3id.org/odrl-kb/dpv-loc-geo":
            lambda i: build_dpvloc.slug(_local(i)),
        "https://w3id.org/odrl-kb/dpv-loc-juris":
            lambda i: build_dpvloc.slug(_local(i)),
        "https://w3id.org/odrl-kb/geonames-europe": _geonames,
        "https://w3id.org/odrl-kb/bcp47": lambda i: "bcp_" + _local(i),
    }
    return table[resource]


# --- the statements ----------------------------------------------------------

def dist_label(a, b, infix="") -> str:
    return f"bg_dist_{a}_{infix + '_' if infix else ''}{b}"


def disj_label(a, b) -> str:
    return f"bg_disj_{a}_disjoint_{b}"


def fof_dist(a, b, label=None) -> str:
    n = label or dist_label(a, b)
    return f"fof({n}, axiom,\n    {a} != {b})."


def smt_dist(a, b, label=None) -> str:
    n = label or dist_label(a, b)
    return f"(assert (! (not (= {a} {b})) :named {n}))"


def fof_disj(a, b) -> str:
    n = disj_label(a, b)
    return (f"fof({n}, axiom,\n"
            f"    ! [X] : ~ ( kge_leq(X, {a}) & kge_leq(X, {b}) )).")


def smt_disj(a, b) -> str:
    n = disj_label(a, b)
    return (f"(assert (! (forall ((x Concept))\n"
            f"    (not (and (kge_leq x {a}) (kge_leq x {b}))))\n"
            f"  :named {n}))")


def instances(decl: Decl, pairs, fof_head, smt_head, kind="distinct",
              label=None):
    """The statements a problem carries for the pairs it names.

    The head comments are the caller's, as are the order of the arguments
    and the order of the pairs.  Each pair must be one the set states, in
    either order, and of the kind asked for: a problem cannot carry an
    instance its declarations do not license.  Returns (fof, smt) as the
    problem fields fof_decls and smt2_background want them.
    """
    constant = constant_for(decl.applies_to[0])
    fof, smt = list(fof_head), list(smt_head)
    for a, b in pairs:
        if decl.has(a, b, constant) != kind:
            raise ValueError(
                f"{decl.path.name} does not state {kind} for {a} and {b}")
        if kind == "distinct":
            n = label(a, b) if label else None
            fof.append(fof_dist(a, b, n))
            smt.append(smt_dist(a, b, n))
        else:
            fof.append(fof_disj(a, b))
            smt.append(smt_disj(a, b))
    return "\n".join(fof) + "\n", "\n".join(smt)
