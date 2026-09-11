"""
build_gdprlb.py
===============
Builds the GDPR Article 6 legal-basis resource for the operand
dpv-odrl:LegalBasis at tax.

    uv run generators/build_gdprlb.py \
        --core   vocabularies/dpv-2.3/modules/legal_basis.ttl \
        --gdpr   vocabularies/dpv-2.3/legal/eu/gdpr/modules/legal_basis.ttl \
        --declare-distinct-from-seven \
        --out    problems

Two modules, and why
--------------------
The GDPR extension names the Article 6 legal bases and places each below a
concept of the DPV core: A6-1-b below dpv:Contract, A6-1-c below
dpv:LegalObligation, and so on. Of its 31 order assertions, 18 leave the
extension's own namespace. Reading the extension alone, as the consent
status builder reads its module alone, would leave A6-1-b, A6-1-c, A6-1-d
and A6-1-f with no parent at all, and a constraint naming dpv:LegalBasis
would reach nothing. The resource is therefore the union of the two
modules, and the census below reports both halves so the reader can see
which assertions came from where.

The core module is a tree: 16 concepts, 15 assertions, one root at
dpv:LegalBasis, no concept with two parents. The extension is not: 17
concepts, 12 of them with more than one parent and two with three, since
each Article 6 concept is placed both under the article it refines and
under the DPV category it belongs to. A6-1-e sits under both
dpv:OfficialAuthorityOfController and dpv:PublicInterest, which is the
Article's own disjunction ("public interest or official authority") carried
into the order.

Three assertions are dropped at the boundary: A6-1-a and its two variants
are also placed under dpv:ExpressedConsent and
dpv:ExplicitlyExpressedConsent, which the DPV core defines in its consent
module rather than in its legal-basis one. Each of the three has another
parent inside the union, so nothing is left unrooted by the drop. The
count is reported rather than silently absorbed.

Neither module asserts distinctness or disjointness anywhere.

Background theories
-------------------
    empty       what the two modules publish, and nothing else
    declared    the seven DPV-core bases of Article 6(1) declared
                pairwise distinct, and each declared distinct from the
                Article 6 concepts below it

The second is the parties' and is marked withdrawable. It is not warranted
by anything either module publishes, and it is not obviously right as a
matter of law: a controller may rely on more than one legal basis for one
operation, and whether the bases of Article 6(1) exclude one another is
contested. This is the opposite of the consent status case, where the
module's own definitions warranted the disjointness and only the assertion
was missing. Here the assertion is missing and so is the warrant, which is
why the theory is offered separately rather than folded into the resource.
"""

import argparse, sys
from collections import defaultdict
from pathlib import Path
from rdflib import Graph, Namespace, RDFS

SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
DPV  = "https://w3id.org/dpv#"
GDPR = "https://w3id.org/dpv/legal/eu/gdpr#"

# The seven bases of Article 6(1), as the ODRL Regulatory Compliance
# Profile enumerates them.  Its names are the DPV core concepts; the
# Article 6 concepts of the extension sit below them.
SEVEN = ["Consent", "Contract", "LegalObligation", "VitalInterest",
         "PublicInterest", "OfficialAuthorityOfController",
         "LegitimateInterest"]


def slug(iri: str) -> str:
    """A TPTP constant name, namespace-qualified so the two modules do not
    collide on a shared local name."""
    local = str(iri).split("#")[-1]
    pre = "gdpr" if str(iri).startswith(GDPR) else "dpv"
    out = []
    for ch in local:
        if ch.isupper() and out and out[-1] != "_":
            out.append("_")
        out.append(ch.lower() if ch.isalnum() else "_")
    return f"lb_{pre}_" + "".join(out).strip("_").replace("__", "_")


def load(core: Path, gdpr: Path):
    g = Graph()
    g.parse(core, format="turtle")
    g.parse(gdpr, format="turtle")
    classes = {s for s in g.subjects(None, RDFS.Class)
               if str(s).startswith((DPV, GDPR))}
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
    return (g, classes, labels,
            sorted(inside, key=key), sorted(dangling, key=key))


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

def resource_ttl(classes, labels, inside, meta) -> str:
    """The concepts and the order, as the two modules publish them."""
    parents = defaultdict(list)
    for s, o in inside:
        parents[s].append(o)
    head = [
        "# GDPR Article 6 legal bases: the subsumption the Data Privacy",
        "# Vocabulary and its GDPR extension publish.",
        "#",
        "# skos:broader edges between concepts the two modules define. An",
        "# edge whose target is defined in neither is reported by the",
        "# generator and not read.",
        "#",
        "# The extension places each Article 6 concept below the article",
        "# it refines and below the DPV category it belongs to, so a",
        "# concept may appear below more than one other. It also",
        "# publishes shortcuts: explicit consent lies below both",
        "# eu-gdpr:A6-1-a and eu-gdpr:Consent directly, and a refutation",
        "# will take whichever path is shorter.",
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
        "@prefix eu-gdpr: <https://w3id.org/dpv/legal/eu/gdpr#> .",
        "@prefix odrlkb:  <https://w3id.org/odrl-kb/dpv-gdpr-legal-basis#> .",
        "@prefix dcat:    <http://www.w3.org/ns/dcat#> .",
        "@prefix dcterms: <http://purl.org/dc/terms/> .",
        "@prefix skos:    <http://www.w3.org/2004/02/skos/core#> .",
        "@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .",
        "",
        "<https://w3id.org/odrl-kb/dpv-gdpr-legal-basis> a dcat:Dataset ;",
        '    dcterms:title "GDPR Article 6 legal bases"@en ;',
        f"    dcterms:source <{meta['source_iri']}> ;",
        "    dcterms:license "
        "<https://www.w3.org/copyright/document-license-2023/> .",
        "",
    ]
    body = []
    for c in sorted(classes, key=str):
        body.append(f"odrlkb:{slug(c)[3:]} a odrlkb:LegalBasis ;")
        if labels.get(c):
            body.append(f'    rdfs:label "{labels[c]}"@en ;')
        body.append(f"    dcterms:identifier <{c}> ;")
        ps = sorted(parents[c], key=str)
        if ps:
            body.append("    skos:broader "
                        + ", ".join(f"odrlkb:{slug(p)[3:]}" for p in ps)
                        + " .")
        else:
            body[-1] = body[-1].rstrip(" ;") + " ."
        body.append("")
    return "\n".join(head + body)

def background_ttl(meta) -> str:
        return """\
# Background theory for the legal-basis resource: empty.
#
# Neither module asserts distinctness or disjointness between legal
# bases. Two constraints naming different bases are therefore
# satisfiable together unless a party declares them apart, and the
# certificate for such a verdict names the declaration.
#
# Source: {meta['source_iri']}

@prefix bt:      <https://w3id.org/odrl-kb/background#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

<https://w3id.org/odrl-kb/dpv-gdpr-legal-basis/empty>
        a bt:BackgroundTheory ;
    dcterms:title "No declared distinctness or disjointness"@en ;
    bt:appliesTo <https://w3id.org/odrl-kb/dpv-gdpr-legal-basis> ;
    bt:pairCount 0 .
"""
def declared_ttl(names, meta) -> str:
    n = len(names)
    return f"""\\
# Background theory for the legal-basis resource: declared distinctness.
#
# The parties declare that no two of the listed names denote one legal
# basis. Neither module asserts this, so the rule is the parties' and a
# verdict resting on an instance of it is withdrawable.
#
# Whether it is right is a question of law. Article 6(1) lists its bases
# without saying that a controller may rely on only one, and a party who
# reads the Article as permitting a basis to coincide with another can
# withdraw the declaration.
#
# Distinctness only, not disjointness: the extension places a concept
# below two others in several places, and a disjointness over such a
# pair would contradict the resource.
#
# Concepts: {n}
# Pairs   : {n * (n - 1) // 2}
# Source  : {meta['source_iri']}

@prefix bt:      <https://w3id.org/odrl-kb/background#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

<https://w3id.org/odrl-kb/dpv-gdpr-legal-basis/declared>
        a bt:BackgroundTheory ;
    dcterms:title "Pairwise distinctness of legal bases"@en ;
    bt:appliesTo <https://w3id.org/odrl-kb/dpv-gdpr-legal-basis> ;
    bt:generatedBy bt:PairwiseDistinctness ;
    bt:scopeCondition "Distinctness between the listed bases, and not disjointness: the extension publishes concepts below two parents."@en ;
    bt:pairCount {n * (n - 1) // 2} .
"""

def profile_ttl() -> str:
    return """\
# Profile entry for dpvo:LegalBasis over the DPV and GDPR modules.
#
# The binding assigns the taxonomic sort. The modules publish
# skos:broader between bases, so isA reads a hierarchy: explicit consent
# under Article 6(1)(a) lies below consent, which lies below the
# legal-basis root.
#
# The left operand is the DPV-ODRL mapping's. ODRL's core vocabulary has
# no term for a legal basis, and the mapping mints one; a policy using
# it declares conformance to that profile.
#
# The mapping restricts which operators it uses on this operand. That
# restriction is the profile's and is recorded there; the sort below
# says which operators the semantics admits, which is a different and
# wider question.

@prefix dpvo: <https://w3id.org/dpv/mappings/odrl#> .
@prefix bind: <https://w3id.org/odrl-kb/binding#> .
@prefix ex:   <https://w3id.org/odrl-kb/profile/> .

ex:b-legalbasis a bind:OperandBinding ;
    bind:leftOperand dpvo:LegalBasis ;
    bind:sort bind:tax ;
    bind:resource <https://w3id.org/odrl-kb/dpv-gdpr-legal-basis> ;
    bind:backgroundTheory
        <https://w3id.org/odrl-kb/dpv-gdpr-legal-basis/empty> ;
    bind:grounding bind:sliceMembership .
"""

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
            lines.append(f"fof(bg_dist_{x}_{y}, axiom, {x} != {y}).")
    return "\n".join(lines) + "\n"
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[3])
    ap.add_argument("--core", required=True, type=Path)
    ap.add_argument("--gdpr", required=True, type=Path)
    ap.add_argument("--retrieved", default="2026-08-19")
    ap.add_argument("--out", default="problems", type=Path)
    args = ap.parse_args()

    g, classes, labels, inside, dangling = load(args.core, args.gdpr)
    census(g, classes, inside, dangling)

    meta = {
        "source": "Data Privacy Vocabulary 2.3 and its GDPR extension",
        "modules": f"{args.core.name}, {args.gdpr.name}",
        "source_iri": "https://w3id.org/dpv/2.3",
        "retrieved": args.retrieved,
        "licence": "W3C Document License 2023",
    }

    for d in ("resources", "background", "axioms"):
        (args.out / d).mkdir(parents=True, exist_ok=True)

    (args.out / "axioms" / "DPV-gdprlb.ax").write_text(
        resource_axioms(inside), encoding="utf-8")
    (args.out / "axioms" / "DPV-gdprlb-declared.ax").write_text(
        declared_axioms(classes), encoding="utf-8")
    (args.out / "resources" / "gdprlb.ttl").write_text(
        resource_ttl(classes, labels, inside, meta), encoding="utf-8")
    (args.out / "resources" / "profile-gdprlb.ttl").write_text(
        profile_ttl(), encoding="utf-8")
    (args.out / "background" / "gdprlb-empty.ttl").write_text(
        background_ttl(meta), encoding="utf-8")
    (args.out / "background" / "gdprlb-declared.ttl").write_text(
        declared_ttl(sorted(slug(c) for c in classes), meta),
        encoding="utf-8")

    for p in sorted(args.out.rglob("*gdprlb*")):
        print(f"  {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())