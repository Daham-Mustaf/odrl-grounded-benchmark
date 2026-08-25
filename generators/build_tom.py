"""
build_tom.py
============
Builds the technical and organisational measures resource for the operand
dpv-odrl:TechnicalOrganisationalMeasure at tax.

    uv run generators/build_tom.py \
        --tom      vocabularies/dpv-2.3/modules/TOM.ttl \
        --measures vocabularies/dpv-2.3/modules/technical_measures.ttl \
        --out      problems

Why this operand
----------------
Every other operand in the suite is single-valued: a processing operation
has one purpose in the sense the constraint asks about, a consent record is
in one state, a transfer has one legal basis. Measures are not like that. A
controller has encryption in place and access control and pseudonymisation,
all at once, and a clause requiring safeguards requires them together.

That is what isAllOf is for, and it is the only operator of the fragment
whose satisfaction condition puts the constraint's denotation inside what
the use supplies rather than the other way round. Without a set-valued
operand it cannot be exercised: on a use binding one concept, isAllOf over
one value says what eq says, and over two it is false whatever the
vocabulary publishes.

The two modules
---------------
TOM.ttl carries the top of the hierarchy, five concepts rooted at
dpv:TechnicalOrganisationalMeasure. technical_measures.ttl carries the
measures themselves and places each below dpv:TechnicalMeasure, which the
first module defines. Read alone the second has eight roots; together they
have one. The same boundary decision as the legal-basis resource, and for
the same reason.
"""


import argparse, sys
from collections import defaultdict
from pathlib import Path
from rdflib import Graph, Namespace, RDFS

SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
DPV  = "https://w3id.org/dpv#"
GDPR = "https://w3id.org/dpv#"  # single namespace; kept for shared code

# The seven bases of Article 6(1), as the ODRL Regulatory Compliance
# Profile enumerates them.  Its names are the DPV core concepts; the
# Article 6 concepts of the extension sit below them.
SEVEN = []


def slug(iri: str) -> str:
    """A TPTP constant name, namespace-qualified so the two modules do not
    collide on a shared local name."""
    local = str(iri).split("#")[-1]
    out = []
    for ch in local:
        if ch.isupper() and out and out[-1] != "_":
            out.append("_")
        out.append(ch.lower() if ch.isalnum() else "_")
    return "tm_" + "".join(out).strip("_").replace("__", "_")


def load(core: Path, gdpr: Path):
    g = Graph()
    g.parse(core, format="turtle")
    g.parse(gdpr, format="turtle")
    classes = {s for s in g.subjects(None, RDFS.Class)
               if str(s).startswith((DPV, GDPR))}
    inside, dangling = [], []
    for s, _, o in g.triples((None, SKOS.broader, None)):
        if s not in classes:
            continue
        (inside if o in classes else dangling).append((s, o))
    key = lambda e: (str(e[0]), str(e[1]))
    return g, classes, sorted(inside, key=key), sorted(dangling, key=key)


def depth(concept, parents, memo):
    if concept in memo:
        return memo[concept]
    memo[concept] = 0
    memo[concept] = 1 + max((depth(p, parents, memo)
                             for p in parents[concept]), default=-1)
    return memo[concept]


def census(g, classes, inside, dangling):
    parents = defaultdict(list)
    for s, o in inside:
        parents[s].append(o)
    multi = sum(1 for c in classes if len(parents[c]) > 1)
    mx = max((len(parents[c]) for c in classes), default=0)
    roots = [c for c in classes if not parents[c]]
    memo = {}
    deepest = max(classes, key=lambda c: depth(c, parents, memo))
    core = sum(1 for s, o in inside if str(s).startswith(DPV))
    ext  = len(inside) - core

    print(f"{len(classes)} concepts, {len(inside)} order assertions "
          f"({core} within the core module, {ext} from the extension)")
    print(f"multi-parent: {multi} concepts, at most {mx} parents")
    print(f"roots: {', '.join(sorted(str(r).split('#')[-1] for r in roots))}")
    print(f"longest chain: {depth(deepest, parents, memo)} hops "
          f"({str(deepest).split('#')[-1]})")
    if dangling:
        print(f"dropped at the module boundary: {len(dangling)}")
        for s, o in dangling:
            still = [p for p in parents[s]]
            print(f"    {str(s).split('#')[-1]} below "
                  f"{str(o).split('#')[-1]}"
                  f"{'' if still else '   LEAVES IT UNROOTED'}")
    n_dis = sum(1 for p in g.predicates()
                if "disjoint" in str(p).lower() or "sameAs" in str(p))
    print(f"disjointness or identity assertions in either module: {n_dis}")
    return parents


def resource_axioms(inside) -> str:
    lines = [
        "% Resource: the legal bases of GDPR Article 6, as the Data Privacy",
        "% Vocabulary and its GDPR extension publish them.",
        "%",
        "% Each assertion is one skos:broader triple.  The extension places",
        "% each Article 6 concept both under the article it refines and",
        "% under the DPV category it belongs to, so a concept may appear",
        "% below more than one other.",
        "",
    ]
    for s, o in inside:
        a, b = slug(s), slug(o)
        lines.append(f"fof(res_{a}_below_{b}, axiom, kge_leq({a}, {b})).")
    return "\n".join(lines) + "\n"


def declared_axioms(classes) -> str:
    """The concepts of the resource declared pairwise distinct.

    Stated as inequations rather than as disjointness: the claim is that no
    two names denote the same legal basis, not that nothing falls under two
    of them.  A controller relying on both consent and contract for one
    operation is not thereby claiming the two are one thing.

    Neither module asserts this, and it is not obviously right.  Article
    6(1) lists its bases without saying a controller may rely on only one,
    and whether two of them can coincide is a question of law rather than of
    vocabulary.  This is the opposite of the consent status case, where the
    module's own definitions warranted the disjointness and only the
    assertion was missing: here the assertion is missing and so is the
    warrant.  The theory is offered separately so that a verdict resting on
    it says so, and so that a party who reads Article 6 differently can
    withdraw it.
    """
    names = sorted((c for c in classes), key=str)
    lines = [
        "% Background theory: distinct concepts denote distinct legal bases.",
        "%",
        "% A pairwise distinctness rule over the concepts of the resource,",
        "% in the manner of a registry.  Neither the Data Privacy Vocabulary",
        "% nor its GDPR extension asserts distinctness anywhere, so this is",
        "% the parties' declaration and a refutation citing it is open to",
        "% whoever made it.",
        "%",
        "% Whether it is right is a question of law.  Article 6(1) lists its",
        "% legal bases without saying that a controller may rely on only",
        "% one, and a party who reads the Article as permitting a basis to",
        "% coincide with another can withdraw the declaration.",
        "%",
        f"% {len(names)} concepts, {len(names) * (len(names) - 1) // 2} "
        "inequations.",
        "",
    ]
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            x, y = slug(a), slug(b)
            lines.append(f"fof(bt_{x}_distinct_{y}, axiom, {x} != {y}).")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[3])
    ap.add_argument("--tom", required=True, type=Path)
    ap.add_argument("--measures", required=True, type=Path)
    ap.add_argument("--out", default="problems", type=Path)
    args = ap.parse_args()

    g, classes, inside, dangling = load(args.tom, args.measures)
    census(g, classes, inside, dangling)

    (args.out / "axioms").mkdir(parents=True, exist_ok=True)
    (args.out / "background").mkdir(parents=True, exist_ok=True)

    p = args.out / "axioms" / "DPV-tom.ax"
    p.write_text(resource_axioms(inside), encoding="utf-8")
    print(f"  {p}")

    p = args.out / "axioms" / "DPV-tom-declared.ax"
    p.write_text(declared_axioms(classes), encoding="utf-8")
    print(f"  {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())