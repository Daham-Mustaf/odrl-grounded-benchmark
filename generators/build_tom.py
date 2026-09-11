"""
build_tom.py
============

Builds the technical and organisational measures resource for the operand
dpvo:TechnicalOrganisationalMeasure at tax: the concept set, the order,
the background theories, the TPTP axioms, and the profile entry.

    uv run generators/build_tom.py \
        --tom      vocabularies/dpv-2.3/modules/TOM.ttl \
        --measures vocabularies/dpv-2.3/modules/technical_measures.ttl \
        --out      problems

Why this operand
----------------
Every other operand in the suite is single-valued: a processing operation
has one purpose in the sense the constraint asks about, a consent record is
in one state, a transfer has one legal basis.  Measures are not like that.
A controller has encryption in place and access control and
pseudonymisation, all at once, and a clause requiring safeguards requires
them together.

That is what isAllOf is for, and it is the only operator of the fragment
whose satisfaction condition puts the constraint's denotation inside what
the use supplies rather than the other way round.  Without a set-valued
operand it cannot be exercised: on a use binding one concept, isAllOf over
one value says what eq says, and over two it is false whatever the
vocabulary publishes.

How many values an operand takes is not something a binding can currently
declare.  This resource is set-valued and the others are not, and nothing
in the profile records the difference; the paper discusses the gap.

The two modules
---------------
TOM.ttl carries the top of the hierarchy, five concepts rooted at
dpv:TechnicalOrganisationalMeasure.  technical_measures.ttl carries the
measures themselves and places each below dpv:TechnicalMeasure, which the
first module defines.  Read alone the second has eight roots; together they
have one.  The same boundary decision as the other resources, and for the
same reason: an edge whose target is defined in neither module is reported
and not read.

Distinctness, and why not disjointness
--------------------------------------
The declared theory states that no two of the listed names denote one
measure.  That is admissible over any hierarchy: encryption lies below
technical measure and is a different measure from it.

Disjointness would not be.  It says nothing lies below both, and the
modules publish concepts below two parents; declaring such a pair disjoint
contradicts the resource, leaving it with no model and every verdict over
it vacuous.  The generator reports the pairs this affects.

Neither module asserts distinctness anywhere, so the rule is the parties'
and a verdict resting on an instance of it is withdrawable.  The rule is
stated in the theory and instantiated by the problems, so that a refutation
cites the inequation it used rather than one term standing for thousands.
"""

import argparse
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path

try:
    from rdflib import Graph, Namespace, RDFS, SKOS
except ImportError:
    print("needs rdflib: uv add rdflib", file=sys.stderr)
    raise

DPV = "https://w3id.org/dpv#"


def slug(iri: str) -> str:
    """A TPTP constant name for a measure.

    Splitting CamelCase keeps a certificate readable: tm_access_control_method
    rather than tm_accesscontrolmethod.  The prefix keeps measures apart from
    the concepts of the other resources in a shared vocabulary.
    """
    local = str(iri).split("#")[-1]
    out = []
    for ch in local:
        if ch.isupper() and out and out[-1] != "_":
            out.append("_")
        out.append(ch.lower() if ch.isalnum() else "_")
    return "tm_" + "".join(out).strip("_").replace("__", "_")


def local(iri) -> str:
    return str(iri).split("#")[-1]


def load(tom: Path, measures: Path):
    """Concepts, labels, the order, and the edges leaving the two modules."""
    g = Graph()
    g.parse(tom, format="turtle")
    g.parse(measures, format="turtle")

    classes = {s for s in g.subjects(None, RDFS.Class)
               if str(s).startswith(DPV)}

    labels = {}
    for s, o in g.subject_objects(SKOS.prefLabel):
        if s in classes and getattr(o, "language", None) == "en":
            labels[s] = str(o)

    inside, dangling = [], []
    for s, _, o in g.triples((None, SKOS.broader, None)):
        if s not in classes:
            continue
        (inside if o in classes else dangling).append((s, o))

    key = lambda e: (str(e[0]), str(e[1]))
    return g, classes, labels, sorted(inside, key=key), sorted(dangling, key=key)


def depth(concept, parents, memo):
    if concept in memo:
        return memo[concept]
    memo[concept] = 0
    memo[concept] = 1 + max((depth(p, parents, memo)
                             for p in parents[concept]), default=-1)
    return memo[concept]


def common_children(inside, classes):
    """Pairs with a concept below both, and that concept.

    Reported rather than acted on: such a pair admits a distinctness, which
    is what the declared theory states, and refuses a disjointness, which
    nothing here writes.  A reader adding one later needs the list.
    """
    below = defaultdict(set)
    for s, o in inside:
        below[o].add(s)
    out = []
    for a, b in combinations(sorted(below, key=str), 2):
        shared = below[a] & below[b]
        if shared:
            out.append((a, b, sorted(shared, key=str)))
    return out


def census(g, classes, labels, inside, dangling):
    parents = defaultdict(list)
    for s, o in inside:
        parents[s].append(o)
    multi = sum(1 for c in classes if len(parents[c]) > 1)
    mx = max((len(parents[c]) for c in classes), default=0)
    roots = [c for c in classes if not parents[c]]
    memo = {}
    deepest = max(classes, key=lambda c: depth(c, parents, memo))

    print(f"{len(classes)} concepts, {len(inside)} order assertions")
    print(f"multi-parent: {multi} concepts, at most {mx} parents")
    print(f"roots: {', '.join(sorted(local(r) for r in roots))}")
    print(f"longest chain: {depth(deepest, parents, memo)} hops "
          f"({local(deepest)})")

    if dangling:
        print(f"dropped at the module boundary: {len(dangling)}")
        for s, o in dangling:
            still = parents[s]
            print(f"    {local(s)} below {local(o)}"
                  f"{'' if still else '   LEAVES IT UNROOTED'}")

    shared = common_children(inside, classes)
    if shared:
        print(f"\n{len(shared)} pairs have a concept below both, so a "
              f"disjointness over them would contradict the resource:")
        for a, b, cs in shared[:6]:
            print(f"    {local(a)} and {local(b)}: "
                  f"{', '.join(local(c) for c in cs[:3])}")
        if len(shared) > 6:
            print(f"    ... and {len(shared) - 6} more")
        print("  Distinctness over them is admissible and is what the "
              "declared theory states.")

    n_dis = sum(1 for p in g.predicates()
                if "disjoint" in str(p).lower() or "sameAs" in str(p))
    print(f"\ndisjointness or identity assertions in either module: {n_dis}")
    return parents


# --------------------------------------------------------------------------
# Resource
# --------------------------------------------------------------------------

def resource_ttl(classes, labels, inside, meta) -> str:
    parents = defaultdict(list)
    for s, o in inside:
        parents[s].append(o)
    head = [
        "# DPV technical and organisational measures: the subsumption the",
        "# modules publish.",
        "#",
        "# skos:broader edges between concepts the two modules define.  An",
        "# edge whose target is defined in neither is reported by the",
        "# generator and not read, so a measure is placed here only under a",
        "# measure.",
        "#",
        "# The hierarchy is a directed acyclic graph and not a tree: some",
        "# measures have two parents.  A concept below two others is below",
        "# each of them.  What that forbids is a declaration of disjointness",
        "# between two such parents, since the resource publishes a concept",
        "# below both; distinctness over the same pair is untouched.",
        "#",
        f"# Source   : {meta['source']}",
        f"# Modules  : {meta['modules']}",
        f"# Retrieved: {meta['retrieved']}",
        f"# Licence  : {meta['licence']}",
        "#",
        f"# Concepts                    : {len(classes)}",
        f"# Order assertions, published : {len(inside)}",
        "",
        "@prefix dpv:     <https://w3id.org/dpv#> .",
        "@prefix odrlkb:  <https://w3id.org/odrl-kb/dpv-tom#> .",
        "@prefix dcat:    <http://www.w3.org/ns/dcat#> .",
        "@prefix dcterms: <http://purl.org/dc/terms/> .",
        "@prefix skos:    <http://www.w3.org/2004/02/skos/core#> .",
        "@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .",
        "",
        "<https://w3id.org/odrl-kb/dpv-tom> a dcat:Dataset ;",
        '    dcterms:title "DPV technical and organisational measures"@en ;',
        f"    dcterms:source <{meta['source_iri']}> ;",
        "    dcterms:license "
        "<https://www.w3.org/copyright/document-license-2023/> .",
        "",
    ]
    body = []
    for c in sorted(classes, key=str):
        body.append(f"odrlkb:{slug(c)[3:]} a odrlkb:Measure ;")
        if labels.get(c):
            body.append(f'    rdfs:label "{labels[c]}"@en ;')
        body.append(f"    dcterms:identifier dpv:{local(c)} ;")
        ps = sorted(parents[c], key=str)
        if ps:
            body.append("    skos:broader "
                        + ", ".join(f"odrlkb:{slug(p)[3:]}" for p in ps)
                        + " .")
        else:
            body[-1] = body[-1].rstrip(" ;") + " ."
        body.append("")
    return "\n".join(head + body)


def resource_axioms(inside) -> str:
    lines = [
        "% Resource: the subsumption between technical and organisational",
        "% measures, as the Data Privacy Vocabulary publishes it.",
        "%",
        "% Each assertion is one skos:broader triple.  Some measures appear",
        "% as the subject of two: the hierarchy is a directed acyclic graph,",
        "% and a refutation may reach a common ancestor by either path.",
        "",
    ]
    for s, o in inside:
        a, b = slug(s), slug(o)
        lines.append(f"fof(res_{a}_below_{b}, axiom, kge_leq({a}, {b})).")
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------
# Background theories
# --------------------------------------------------------------------------

def background_ttl(meta) -> str:
    return f"""\
# Background theory for the measures resource: empty.
#
# Neither module asserts disjointness or distinctness between measures.
# Two constraints naming different measures are therefore satisfiable
# together unless a party declares them apart, and the certificate for such
# a verdict names the declaration.
#
# Source: {meta['source_iri']}

@prefix bt:      <https://w3id.org/odrl-kb/background#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

<https://w3id.org/odrl-kb/dpv-tom/empty> a bt:BackgroundTheory ;
    dcterms:title "No declared distinctness or disjointness"@en ;
    bt:appliesTo <https://w3id.org/odrl-kb/dpv-tom> ;
    bt:pairCount 0 .
"""


def declared_ttl(names, meta) -> str:
    """The parties declare the measures pairwise distinct.

    Stated as a rule rather than as instances, for the reason the ISO rule
    over DPV Locations is: n concepts give n(n-1)/2 inequations, and a
    refutation should cite the one it used rather than one term standing for
    all of them.
    """
    n = len(names)
    return f"""\
# Background theory for the measures resource: declared distinctness.
#
# The parties declare that no two of the listed names denote one measure.
# Neither module asserts this, so the rule is the parties' and a verdict
# resting on an instance of it is withdrawable by abandoning the rule.
#
# Distinctness only.  Nothing here says two measures have nothing below
# both: that is disjointness, and the modules publish concepts below two
# parents, so a disjointness over such a pair would contradict the resource
# and leave it with no model.  A use employing both encryption and access
# control is not thereby claiming the two are one measure.
#
# The rule is stated here and instantiated by the problems: a problem naming
# two measures carries the inequation between them, so that a refutation
# cites the instance it used.
#
# Concepts: {n}
# Pairs   : {n * (n - 1) // 2}
# Source  : {meta['source_iri']}

@prefix bt:      <https://w3id.org/odrl-kb/background#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

<https://w3id.org/odrl-kb/dpv-tom/declared> a bt:BackgroundTheory ;
    dcterms:title "Pairwise distinctness of measures"@en ;
    bt:appliesTo <https://w3id.org/odrl-kb/dpv-tom> ;
    bt:generatedBy bt:PairwiseDistinctness ;
    bt:scopeCondition "Distinctness between the measures the modules list, and not disjointness: the modules publish concepts below two parents, and a disjointness over such a pair would contradict the resource."@en ;
    bt:pairCount {n * (n - 1) // 2} .
"""


def declared_axioms(names) -> str:
    """The rule, stated but not instantiated.

    As LOC-dpvloc-iso.ax does.  Instantiating every pair would bury the one
    assertion a refutation actually uses: 74 measures give 2701 inequations,
    and an unsat core over them says nothing a reader can follow.
    """
    n = len(names)
    listing = "\n".join("% " + ", ".join(names[i:i + 6])
                        for i in range(0, len(names), 6))
    return (
        "% Background theory: pairwise distinctness, declared by the "
        "parties.\n"
        "%\n"
        "% No two of the names below denote one measure.  Neither module\n"
        "% asserts this, so the rule is the parties' and a verdict resting\n"
        "% on an instance of it is withdrawable by abandoning the rule.\n"
        "%\n"
        "% Distinctness, not disjointness: a measure may lie below another\n"
        "% and still be a different measure, and a use employing two of\n"
        "% them is not claiming they are one.  Disjointness over a pair\n"
        "% with a common child would contradict the resource.\n"
        "%\n"
        "% The rule is stated here and instantiated by the problems.  A\n"
        "% problem naming two of the measures below carries the inequation\n"
        "% between them as a bg_dist_ assertion, so that a refutation cites\n"
        "% the instance it used rather than one of "
        f"{n * (n - 1) // 2}.\n"
        "%\n"
        f"% Measures: {n}\n"
        f"% Pairs   : {n * (n - 1) // 2}\n"
        "%\n"
        f"{listing}\n"
    )


def declared_instance(a: str, b: str) -> str:
    """The inequation a problem carries when it adopts the rule.

    Named bg_dist_<a>_<b> with no infix, matching the helper the problem
    data uses: an unsat core and a TPTP proof are compared by premise name.
    """
    return (f"fof(bg_dist_{a}_{b}, axiom,\n"
            f"    {a} != {b}).")


# --------------------------------------------------------------------------
# Profile
# --------------------------------------------------------------------------

def profile_ttl() -> str:
    return """\
# Profile entry for dpvo:TechnicalOrganisationalMeasure over the DPV
# measures modules.
#
# The binding assigns the taxonomic sort.  The modules publish skos:broader
# between measures, so isA reads a hierarchy: a use employing symmetric
# encryption employs encryption, and employs a technical measure.
#
# The left operand is the DPV-ODRL mapping's.  ODRL's core vocabulary has no
# term for a security measure, and the mapping mints one; a policy using it
# declares conformance to that profile.
#
# This is the suite's only set-valued operand: a use carries several
# measures at once, which is what isAllOf is for and what makes it
# exercisable here and nowhere else.  How many values an operand takes is
# not something this binding can declare, and that is a limitation of the
# framework rather than of the vocabulary.

@prefix dpvo: <https://w3id.org/dpv/mappings/odrl#> .
@prefix bind: <https://w3id.org/odrl-kb/binding#> .
@prefix ex:   <https://w3id.org/odrl-kb/profile/> .

ex:b-tom a bind:OperandBinding ;
    bind:leftOperand dpvo:TechnicalOrganisationalMeasure ;
    bind:sort bind:tax ;
    bind:resource <https://w3id.org/odrl-kb/dpv-tom> ;
    bind:backgroundTheory <https://w3id.org/odrl-kb/dpv-tom/empty> ;
    bind:grounding bind:sliceMembership .
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[3])
    ap.add_argument("--tom", required=True, type=Path,
                    help="TOM.ttl, the top of the hierarchy")
    ap.add_argument("--measures", required=True, type=Path,
                    help="technical_measures.ttl, the measures themselves")
    ap.add_argument("--retrieved", default="2026-08-19",
                    help="the date this snapshot was fetched, ISO 8601")
    ap.add_argument("--tag", default="tom")
    ap.add_argument("--out", default="problems", type=Path)
    args = ap.parse_args()

    g, classes, labels, inside, dangling = load(args.tom, args.measures)
    if not classes:
        print("no concepts found; check the two modules", file=sys.stderr)
        return 1

    parents = census(g, classes, labels, inside, dangling)

    meta = {
        "source": "Data Privacy Vocabulary 2.3, technical and "
                  "organisational measures",
        "modules": f"{args.tom.name}, {args.measures.name}",
        "source_iri": "https://w3id.org/dpv/2.3",
        "retrieved": args.retrieved,
        "licence": "W3C Document License 2023",
    }

    for d in ("resources", "background", "axioms"):
        (args.out / d).mkdir(parents=True, exist_ok=True)
    tag = args.tag

    (args.out / "resources" / f"{tag}.ttl").write_text(
        resource_ttl(classes, labels, inside, meta), encoding="utf-8")
    (args.out / "resources" / f"profile-{tag}.ttl").write_text(
        profile_ttl(), encoding="utf-8")
    (args.out / "background" / f"{tag}-empty.ttl").write_text(
        background_ttl(meta), encoding="utf-8")
    (args.out / "axioms" / f"DPV-{tag}.ax").write_text(
        resource_axioms(inside), encoding="utf-8")

    names = sorted(slug(c) for c in classes)
    (args.out / "background" / f"{tag}-declared.ttl").write_text(
        declared_ttl(names, meta), encoding="utf-8")
    (args.out / "axioms" / f"DPV-{tag}-declared.ax").write_text(
        declared_axioms(names), encoding="utf-8")

    print()
    for p in sorted(args.out.rglob(f"*{tag}*")):
        print(f"  {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())