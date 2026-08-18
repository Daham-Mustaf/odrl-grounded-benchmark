"""
build_dpv.py
============
Builds a DPV purposes slice: the resource, the background theory, the TPTP
axioms, and the profile entry.

    python build_dpv.py --purposes purposes.ttl --out problems

This generator reads the SKOS file, in which skos:broader is the only
hierarchy predicate.  Nothing in it says the order is subsumption: the
concepts are skos:Concept instances related by a SKOS predicate whose own
specification declines to fix its logical reading.  Declaring the sort is
therefore a decision, and the profile records it.

DPV also ships an OWL serialisation.  If that file relates the same
concepts by rdfs:subClassOf, it is the same decision made by the publisher,
and worth citing.  Verify the predicate in 2.3/dpv/dpv-owl.ttl before
relying on it.

The background theory is empty.  The purposes module carries no
owl:disjointWith and no distinctness of any kind (grep: zero).  Generating
sibling disjointness here would be wrong, not merely expensive:
NonCommercialResearch is published under both NonCommercialPurpose and
ResearchAndDevelopment, so siblings under one parent routinely overlap.
A generated rule would separate concepts DPV deliberately left joint.

The silence between ScientificResearch and NonCommercialPurpose is
likewise deliberate.  DPV has NonCommercialResearch under both parents, so
the publisher had the vocabulary to say that scientific research is
non-commercial, and did not.  A verdict of Unknown for that pair reports
the gap rather than closing it.
"""

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

try:
    from rdflib import Graph, Namespace, RDFS, SKOS
except ImportError:
    print("needs rdflib: uv add rdflib", file=sys.stderr)
    raise

DPV = Namespace("https://w3id.org/dpv#")


def parse(path: Path):
    """skos:broader edges and labels.

    Read with rdflib rather than by scanning lines.  Turtle wraps
    multi-valued objects across lines:

        skos:broader dpv:CommercialPurpose,
            dpv:ResearchAndDevelopment ;

    and a line scanner takes the first parent and drops the rest, which
    is exactly the multiple inheritance the closure below depends on.
    """
    g = Graph()
    g.parse(path, format="turtle")

    # Subjects defined in this file.  The purposes module publishes one edge
    # whose target is not: RightsFulfilment is below LegalObligation, which
    # is a legal basis defined in legal_basis.ttl.  That edge is dropped.
    #
    # The reason is the operand, not tidiness.  This resource grounds
    # odrl:purpose, and a legal basis is a different left operand with its
    # own binding in the DPV-ODRL mapping.  Keeping the edge would put a
    # concept from one operand's vocabulary into another operand's
    # resource, and a verdict could then rest on an order assertion the
    # profile never bound.  Where a module's boundary falls is a choice,
    # so the resource header states it.
    defined = {str(sub)[len(DPV):] for sub in g.subjects()
               if str(sub).startswith(str(DPV))}

    edges, labels, external = [], {}, []
    for child, parent in g.subject_objects(SKOS.broader):
        if not (str(child).startswith(str(DPV))
                and str(parent).startswith(str(DPV))):
            continue
        c, p = str(child)[len(DPV):], str(parent)[len(DPV):]
        if p not in defined:
            external.append((c, p))
            continue
        edges.append((c, p))
    for subj, lab in g.subject_objects(SKOS.prefLabel):
        if str(subj).startswith(str(DPV)):
            labels[str(subj)[len(DPV):]] = str(lab)
    return sorted(set(edges)), labels, sorted(set(external))


def ancestors(edges, seeds):
    """Full upward closure.  Not one path: DPV concepts have several
    parents (ServicePersonalisation under Personalisation and
    ServiceManagement, among others), and taking one path would leave a
    concept in the slice with a parent missing, producing an Unknown that
    DPV itself settles."""
    up = defaultdict(set)
    for child, parent in edges:
        up[child].add(parent)
    seen, frontier = set(seeds), list(seeds)
    while frontier:
        c = frontier.pop()
        for p in up.get(c, ()):
            if p not in seen:
                seen.add(p)
                frontier.append(p)
    return seen


def find_cycle(edges, concepts):
    """Antisymmetry is required of structures, so a cycle is not an input
    error: its members are identified.  It is still worth reporting, since
    a cycle plus a declared distinctness is unsatisfiable, and the slice
    would then have no model."""
    up = defaultdict(set)
    for c, p in edges:
        if c in concepts and p in concepts:
            up[c].add(p)
    colour = {}

    def walk(n, path):
        colour[n] = 1
        for m in up.get(n, ()):
            if colour.get(m) == 1:
                return path + [n, m]
            if colour.get(m) is None:
                r = walk(m, path + [n])
                if r:
                    return r
        colour[n] = 2
        return None

    for n in concepts:
        if colour.get(n) is None:
            r = walk(n, [])
            if r:
                return r
    return None


def slug(c):
    """Local names are unique and ASCII here, so lowercasing suffices.
    Splitting CamelCase would turn ImproveInternalCRMProcesses into
    improve_internal_c_r_m_processes, which is legal TPTP and unreadable
    in a certificate.  The GeoNames slice uses ids instead, because
    feature names collide across countries."""
    # Split CamelCase but keep runs of capitals together, so
    # ImproveInternalCRMProcesses gives improve_internal_crm_processes
    # rather than improve_internal_c_r_m_processes.
    s = re.sub(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])", "_", c)
    return "dpv_" + re.sub(r"[^a-z0-9_]", "_", s.lower())


def resource_ttl(edges, labels, concepts, meta) -> str:
    kept = [(c, p) for c, p in edges if c in concepts and p in concepts]
    head = [
        "# DPV purposes: the subsumption the vocabulary publishes.",
        "#",
        "# skos:broader edges only.  rdf:type dpv:Purpose is a typing",
        "# assertion, not an order assertion, and is not read here.",
        "#",
        "# skos:broader is the only hierarchy predicate here, and SKOS",
        "# declines to fix its logical reading.  That the order is",
        "# subsumption is declared by the profile, not published here.",
        "#",
        "# Scope: this module only.  DPV publishes one edge out of it,",
        "# RightsFulfilment below LegalObligation, and a legal basis is a",
        "# different left operand with its own binding.  That edge is not",
        "# read here, so RightsFulfilment is a root of this resource and",
        "# not of DPV.  Any excluded edge is listed by the generator.",
        "#",
        f"# Source   : {meta['source']}",
        f"# Version  : {meta['version']}",
        f"# Modified : {meta['modified']}",
        f"# Retrieved: {meta['retrieved']}",
        f"# Licence  : {meta['licence']}",
        "",
        "@prefix dpv:     <https://w3id.org/dpv#> .",
        "@prefix odrlkb:  <https://w3id.org/odrl-kb/dpv-purposes#> .",
        "@prefix dcat:    <http://www.w3.org/ns/dcat#> .",
        "@prefix dcterms: <http://purl.org/dc/terms/> .",
        "@prefix skos:    <http://www.w3.org/2004/02/skos/core#> .",
        "@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .",
        "",
        "<https://w3id.org/odrl-kb/dpv-purposes> a dcat:Dataset ;",
        '    dcterms:title "DPV purposes, subsumption slice"@en ;',
        f"    dcterms:source <{meta['version']}> ;",
        f'    dcterms:modified "{meta["modified"]}"^^<http://www.w3.org/2001/XMLSchema#date> ;',
        "    odrlkb:orderPredicate skos:broader ;",
        f"    odrlkb:conceptCount {len(concepts)} ;",
        f"    odrlkb:orderAssertionCount {len(kept)} .",
        "",
    ]
    body = []
    for c in sorted(concepts):
        body.append(f"odrlkb:{slug(c)[4:]} a odrlkb:Purpose ;")
        if labels.get(c):
            body.append(f'    rdfs:label "{labels[c]}"@en ;')
        body.append(f"    dcterms:identifier dpv:{c} ;")
        parents = sorted(p for x, p in kept if x == c)
        if parents:
            body.append("    skos:broader " +
                        ", ".join(f"odrlkb:{slug(p)[4:]}" for p in parents) + " .")
        else:
            body[-1] = body[-1].rstrip(" ;") + " ."
        body.append("")
    return "\n".join(head + body)


def background_ttl(meta) -> str:
    return f"""\
# Background theory for the DPV purposes slice: empty.
#
# The purposes module publishes no disjointness and no distinctness: no
# owl:disjointWith, no owl:AllDifferent, nothing.  This file records that
# the parties declared nothing either, so every verdict below rests on
# what DPV published and on the constraints alone.
#
# A generated sibling rule would be wrong here, not merely costly.
# NonCommercialResearch is published under both NonCommercialPurpose and
# ResearchAndDevelopment, so concepts sharing a parent routinely overlap.
# Separating them would close gaps the publisher left open.
#
# The party-declared disjointness used by the stability problems lives in
# its own file, so that the verdicts obtained with and without it can be
# compared.
#
# Source: {meta['version']}

@prefix bt:      <https://w3id.org/odrl-kb/background#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

<https://w3id.org/odrl-kb/dpv-purposes/empty> a bt:BackgroundTheory ;
    dcterms:title "No declared distinctness or disjointness"@en ;
    bt:appliesTo <https://w3id.org/odrl-kb/dpv-purposes> ;
    bt:assertionCount 0 .
"""


def declared_ttl(pair, meta) -> str:
    a, b = pair
    return f"""\
# Background theory for the DPV purposes slice: one declared distinctness.
#
# DPV publishes nothing that separates these two purposes.  The parties
# declare it, and the verdict that rests on it is theirs rather than the
# vocabulary's.  A party may withdraw the declaration, and the verdict
# reopens.
#
# This file exists to be compared against the empty theory over the same
# resource and the same constraints: what moves is the declaration, and
# nothing else.
#
# Source: {meta['version']}

@prefix dpv:     <https://w3id.org/dpv#> .
@prefix bt:      <https://w3id.org/odrl-kb/background#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

<https://w3id.org/odrl-kb/dpv-purposes/declared> a bt:BackgroundTheory ;
    dcterms:title "One declared distinctness"@en ;
    bt:appliesTo <https://w3id.org/odrl-kb/dpv-purposes> ;
    bt:generatedBy bt:PartyDeclaration ;
    bt:assertionCount 1 .

dpv:{a} bt:distinctFrom dpv:{b} .
"""


def declared_axioms(pair) -> str:
    a, b = pair
    return (
        "% Background theory: one distinctness, declared by the parties.\n"
        "% DPV publishes nothing that separates these two purposes.  The\n"
        "% bt_ prefix marks the assertion as withdrawable, so a refutation\n"
        "% resting on it is attributable to the declaration.\n"
        "\n"
        f"fof(bt_{slug(a)}_distinct_{slug(b)}, axiom,\n"
        f"    {slug(a)} != {slug(b)}).\n"
    )


def axioms(edges, concepts) -> str:
    kept = sorted((c, p) for c, p in edges if c in concepts and p in concepts)
    lines = ["% Resource: subsumption as published by DPV.  res_ names mark",
             "% what the vocabulary asserts.", ""]
    for c, p in kept:
        lines.append(f"fof(res_{slug(c)}_below_{slug(p)}, axiom,")
        lines.append(f"    kge_leq({slug(c)}, {slug(p)})).")
    lines += ["", "% Background theory: empty.  DPV publishes no disjointness",
              "% among purposes, and the parties declare none here.", ""]
    return "\n".join(lines) + "\n"


def profile_ttl() -> str:
    return """\
# Profile entry.  ODRL cannot carry this, so it is agreed out of band.
#
# The sort is the declaration: DPV's skos:broader is read as subsumption.
# Nothing in the resource says so.

@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix vrep: <https://w3id.org/odrl-verdict-report#> .
@prefix ex:   <https://w3id.org/odrl-kb/profile/> .

ex:b-purpose a vrep:OperandBinding ;
    vrep:leftOperand odrl:purpose ;
    vrep:sort vrep:tax ;
    vrep:resource <https://w3id.org/odrl-kb/dpv-purposes> ;
    vrep:backgroundTheory <https://w3id.org/odrl-kb/dpv-purposes/empty> ;
    vrep:grounding vrep:sliceMembership .
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--purposes", required=True, type=Path)
    ap.add_argument("--seeds", nargs="*", default=None,
                    help="local names to close upward from; default: all")
    ap.add_argument("--tag", default=None,
                    help="output name; defaults to the seed set or 'full'")
    ap.add_argument("--declare-distinct", nargs=2, metavar=("A", "B"),
                    default=None,
                    help="also emit a background theory declaring two "
                         "concepts distinct, for the stability pair")
    ap.add_argument("--retrieved", default="2026-08-16")
    ap.add_argument("--out", default="problems", type=Path)
    args = ap.parse_args()

    edges, labels, external = parse(args.purposes)
    if not edges:
        print("no skos:broader edges found; check the file", file=sys.stderr)
        return 1

    all_concepts = {c for c, _ in edges} | {p for _, p in edges}
    concepts = ancestors(edges, args.seeds) if args.seeds else all_concepts
    if args.seeds:
        missing = [s for s in args.seeds if s not in all_concepts]
        if missing:
            print(f"unknown seeds: {', '.join(missing)}", file=sys.stderr)
            return 1

    meta = {
        "source": "w3c/dpv 2.3/dpv/modules/purposes.ttl",
        "version": "https://w3id.org/dpv/2.3",
        "modified": "2026-02-25",
        "retrieved": args.retrieved,
        "licence": "W3C Software and Document License 2023 (verify before "
                   "redistributing the slice)",
    }

    for d in ("resources", "background", "axioms"):
        (args.out / d).mkdir(parents=True, exist_ok=True)
    # Named by the seed set, not the resulting count: a re-run with the
    # same seeds should overwrite rather than leave a second file behind.
    tag = args.tag or ("dpv-purposes-full" if not args.seeds
                       else "dpv-purposes-"
                       + "-".join(s.lower() for s in sorted(args.seeds))[:60])

    (args.out / "resources" / f"{tag}.ttl").write_text(
        resource_ttl(edges, labels, concepts, meta), encoding="utf-8")
    (args.out / "background" / f"{tag}-empty.ttl").write_text(
        background_ttl(meta), encoding="utf-8")
    (args.out / "axioms" / f"DPV-{tag}.ax").write_text(
        axioms(edges, concepts), encoding="utf-8")
    (args.out / "resources" / f"profile-{tag}.ttl").write_text(
        profile_ttl(), encoding="utf-8")

    if args.declare_distinct:
        a, b = args.declare_distinct
        missing = [x for x in (a, b) if x not in concepts]
        if missing:
            print(f"not in the slice: {', '.join(missing)}", file=sys.stderr)
            return 1
        (args.out / "background" / f"{tag}-declared.ttl").write_text(
            declared_ttl((a, b), meta), encoding="utf-8")
        (args.out / "axioms" / f"DPV-{tag}-declared.ax").write_text(
            declared_axioms((a, b)), encoding="utf-8")

    kept = [(c, p) for c, p in edges if c in concepts and p in concepts]
    multi = sum(1 for c in concepts if sum(1 for x, _ in kept if x == c) > 1)
    print(f"{len(concepts)} concepts, {len(kept)} order assertions, "
          f"0 disjointness assertions")
    for c, p in external:
        print(f"excluded: {c} below {p} ({p} is not defined in this module)")
    print(f"{multi} concepts have more than one parent")
    print(f"transitivity ground instances: {len(concepts)**3:,}  "
          f"(the checker's cost; the prover instantiates lazily)")

    cycle = find_cycle(edges, concepts)
    if cycle:
        print(f"\ncycle: {' -> '.join(cycle)}\n"
              f"  Antisymmetry identifies these concepts.  That is sound, but\n"
              f"  a declared distinctness between any two of them would leave\n"
              f"  the slice with no model.")
    else:
        print("no cycle in the published edges: antisymmetry identifies "
              "no concepts")

    for p in sorted(args.out.rglob(f"*{tag}*")):
        print(f"  {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())