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

The default background theory is empty.  The purposes module carries no
owl:disjointWith and no distinctness of any kind (grep: zero).

Distinctness and disjointness are not interchangeable
-----------------------------------------------------
--declare-distinct writes a theory in which the named purposes are
pairwise distinct: no two of them are one concept.  That is admissible
over any hierarchy, because one purpose may lie below another and still
be a different purpose.

Disjointness would not be, and this generator does not offer it.  Eleven
concepts in the module have two parents: NonCommercialResearch under
NonCommercialPurpose and ResearchAndDevelopment, PersonalisedAdvertising
under Advertising and Personalisation, and nine more.  Declaring such a
pair to have nothing below both contradicts what DPV publishes, and a
resource together with a theory that contradicts it has no model at all,
so every verdict over the pair is vacuous.  A declaration is the parties'
to adopt but not theirs to adopt in a form the authority contradicts.

The silence between ScientificResearch and NonCommercialPurpose is
deliberate.  DPV has NonCommercialResearch under both parents, so the
publisher had the vocabulary to say that scientific research is
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


def common_children(edges, concepts, names):
    """Pairs among `names` with a concept below both, and that concept.

    Not used to refuse a distinctness declaration, which such a pair
    admits: one purpose may lie below another and still be a different
    purpose.  Reported so that a reader adding a disjointness later sees
    which pairs the resource forbids it over.
    """
    below = defaultdict(set)
    for c, p in edges:
        if c in concepts and p in concepts:
            below[p].add(c)
    out = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            shared = sorted(below.get(a, set()) & below.get(b, set()))
            if shared:
                out.append((a, b, shared))
    return out


def slug(c):
    """Local names are unique and ASCII here, so lowercasing suffices.

    Splitting CamelCase would turn ImproveInternalCRMProcesses into
    improve_internal_c_r_m_processes, which is legal TPTP and unreadable
    in a certificate.  The GeoNames slice uses ids instead, because
    feature names collide across countries.
    """
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
        "# The hierarchy is a directed acyclic graph and not a tree:",
        "# several concepts have two parents.  A concept below two others",
        "# is below each of them, and reaches a common ancestor by either",
        "# path; which path a refutation takes is the prover's affair.",
        "# What multiple parents forbid is a declaration of disjointness",
        "# between two such parents, since the resource publishes a",
        "# concept below both.",
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
        f'    dcterms:modified "{meta["modified"]}"'
        "^^<http://www.w3.org/2001/XMLSchema#date> ;",
        f'    dcterms:issued "{meta["retrieved"]}"'
        "^^<http://www.w3.org/2001/XMLSchema#date> ;",
        "    dcterms:license "
        "<https://www.w3.org/copyright/document-license-2023/> .",
        "",
        f"# Concepts                    : {len(concepts)}",
        f"# Order assertions, published : {len(kept)}",
        "# Order predicate             : skos:broader",
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
            body.append("    skos:broader "
                        + ", ".join(f"odrlkb:{slug(p)[4:]}" for p in parents)
                        + " .")
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
# the parties declared nothing either, so every verdict over it rests on
# what DPV published and on the constraints alone.
#
# A generated sibling rule would be wrong here, not merely costly.
# NonCommercialResearch is published under both NonCommercialPurpose and
# ResearchAndDevelopment, so concepts sharing a parent routinely overlap.
# Separating them would close gaps the publisher left open.
#
# The party-declared distinctness used by the stability problems lives in
# its own file, so that the verdicts obtained with and without it can be
# compared.
#
# Source: {meta['version']}

@prefix bt:      <https://w3id.org/odrl-kb/background#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

<https://w3id.org/odrl-kb/dpv-purposes/empty> a bt:BackgroundTheory ;
    dcterms:title "No declared distinctness or disjointness"@en ;
    bt:appliesTo <https://w3id.org/odrl-kb/dpv-purposes> ;
    bt:pairCount 0 .
"""


def declared_ttl(names, meta) -> str:
    """The parties declare these purposes pairwise distinct.

    Stated as a rule rather than as instances, for the reason the ISO
    rule in build_dpvloc.py is stated that way: n concepts give n(n-1)/2
    inequations, and a refutation should cite the one it used rather than
    one term standing for all of them.  A problem naming two of the
    concepts carries the inequation between them.
    """
    n = len(names)
    listing = "\n".join(f"# {n_}" for n_ in names)
    return f"""\
# Background theory for the DPV purposes slice: declared distinctness.
#
# The parties declare the purposes below pairwise distinct, on the ground
# that DPV defines each of them as a purpose in its own right.  DPV
# publishes no distinctness anywhere in this module, so the rule is the
# parties' and a verdict resting on an instance of it is withdrawable by
# abandoning the rule.
#
# Distinctness only.  Nothing here says two purposes have nothing below
# both: that is disjointness, and this module publishes concepts below
# two parents, so a disjointness over such a pair would contradict what
# DPV asserts and leave the slice with no model.
#
# The rule is stated here and instantiated by the problems: a problem
# naming two of these purposes carries the inequation between them, so
# that a refutation cites the instance it used rather than a term
# standing for all of them.
#
# Purposes: {n}
# Pairs   : {n * (n - 1) // 2}
{listing}
#
# Source: {meta['version']}

@prefix bt:      <https://w3id.org/odrl-kb/background#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

<https://w3id.org/odrl-kb/dpv-purposes/declared> a bt:BackgroundTheory ;
    dcterms:title "Pairwise distinctness of declared purposes"@en ;
    bt:appliesTo <https://w3id.org/odrl-kb/dpv-purposes> ;
    bt:generatedBy bt:PairwiseDistinctness ;
    bt:scopeCondition "Distinctness between the listed purposes, and not disjointness: DPV publishes concepts below two parents, and a disjointness over such a pair would contradict it."@en ;
    bt:pairCount {n * (n - 1) // 2} .
"""


def declared_axioms(names) -> str:
    """The rule, stated but not instantiated.

    As LOC-dpvloc-iso.ax does: the file lists what the rule ranges over
    and leaves the instances to the problems, so a refutation cites the
    inequation it used.
    """
    n = len(names)
    listing = "\n".join("% " + ", ".join(names[i:i + 8])
                        for i in range(0, len(names), 8))
    return (
        "% Background theory: pairwise distinctness, declared by the "
        "parties.\n"
        "%\n"
        "% DPV publishes nothing that separates these purposes.  The rule is\n"
        "% the parties', on the ground that DPV defines each as a purpose in\n"
        "% its own right, and a verdict resting on an instance of it is\n"
        "% withdrawable by abandoning the rule.\n"
        "%\n"
        "% Distinctness, not disjointness: one purpose may lie below another\n"
        "% and still be a different purpose.  Disjointness over a pair with a\n"
        "% common child would contradict the resource, and this module\n"
        "% publishes concepts below two parents.\n"
        "%\n"
        "% The rule is stated here and instantiated by the problems.  A\n"
        "% problem naming two of the purposes below carries the inequation\n"
        "% between them as a bg_dist_ assertion.\n"
        "%\n"
        f"% Purposes: {n}\n"
        f"% Pairs   : {n * (n - 1) // 2}\n"
        "%\n"
        f"{listing}\n"
    )


def declared_instance(a: str, b: str) -> str:
    """The inequation a problem carries when it adopts the rule.

    Named bg_dist_<a>_<b> with no infix, matching the helper the problem
    data uses.  The two must agree: an unsat core and a TPTP proof are
    compared by premise name, and a mismatch reads as two provers citing
    different premises for one verdict.
    """
    return (f"fof(bg_dist_{slug(a)}_{slug(b)}, axiom,\n"
            f"    {slug(a)} != {slug(b)}).")


def axioms(edges, concepts) -> str:
    kept = sorted((c, p) for c, p in edges if c in concepts and p in concepts)
    lines = ["% Resource: subsumption as published by DPV.  res_ names mark",
             "% what the vocabulary asserts.",
             "%",
             "% Several concepts appear as the subject of two assertions: the",
             "% hierarchy is a directed acyclic graph, not a tree.  A"
             " refutation",
             "% may reach a common ancestor by either path.",
             ""]
    for c, p in kept:
        lines.append(f"fof(res_{slug(c)}_below_{slug(p)}, axiom,")
        lines.append(f"    kge_leq({slug(c)}, {slug(p)})).")
    lines += ["",
              "% Background theory: none here.  DPV publishes no disjointness",
              "% among purposes; what the parties declare lives in the",
              "% declared theory file.",
              ""]
    return "\n".join(lines) + "\n"


def profile_ttl() -> str:
    return """\
# Profile entry.  ODRL cannot carry this, so it is agreed out of band.
#
# The sort is the declaration: DPV's skos:broader is read as subsumption.
# Nothing in the resource says so.

@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix bind: <https://w3id.org/odrl-kb/binding#> .
@prefix ex:   <https://w3id.org/odrl-kb/profile/> .

ex:b-purpose a bind:OperandBinding ;
    bind:leftOperand odrl:purpose ;
    bind:sort bind:tax ;
    bind:resource <https://w3id.org/odrl-kb/dpv-purposes> ;
    bind:backgroundTheory <https://w3id.org/odrl-kb/dpv-purposes/empty> ;
    bind:grounding bind:sliceMembership .
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--purposes", required=True, type=Path)
    ap.add_argument("--seeds", nargs="*", default=None,
                    help="local names to close upward from; default: all")
    ap.add_argument("--tag", default=None,
                    help="output name; defaults to the seed set")
    ap.add_argument("--declare-distinct", nargs="+", metavar="CONCEPT",
                    default=None,
                    help="concepts the parties declare pairwise distinct; "
                         "the theory states the rule and the problems carry "
                         "the instances they use")
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
        "licence": "W3C Document License 2023",
    }

    for d in ("resources", "background", "axioms"):
        (args.out / d).mkdir(parents=True, exist_ok=True)

    # Named by the seed set, not the resulting count: a re-run with the
    # same seeds should overwrite rather than leave a second file behind.
    tag = args.tag or ("dpv-purposes" if not args.seeds
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
        names = sorted(set(args.declare_distinct))
        if len(names) < 2:
            print("--declare-distinct needs at least two distinct concepts",
                  file=sys.stderr)
            return 1
        missing = [x for x in names if x not in concepts]
        if missing:
            print(f"not in the slice: {', '.join(missing)}", file=sys.stderr)
            return 1
        (args.out / "background" / f"{tag}-declared.ttl").write_text(
            declared_ttl(names, meta), encoding="utf-8")
        (args.out / "axioms" / f"DPV-{tag}-declared.ax").write_text(
            declared_axioms(names), encoding="utf-8")

    kept = [(c, p) for c, p in edges if c in concepts and p in concepts]
    multi = sum(1 for c in concepts if sum(1 for x, _ in kept if x == c) > 1)

    print(f"{len(concepts)} concepts, {len(kept)} order assertions, "
          f"0 disjointness assertions")
    for c, p in external:
        print(f"excluded: {c} below {p} "
              f"({p} is defined in another module and belongs to another "
              f"operand)")
    print(f"{multi} concepts have more than one parent")

    # The pairs a disjointness declaration would contradict.  Reported
    # whether or not a distinctness was asked for, since the constraint is
    # a property of the resource and not of this run.
    if args.declare_distinct:
        names = sorted(set(args.declare_distinct))
        shared = common_children(edges, concepts, names)
        if shared:
            print("\namong the declared concepts, these pairs have a concept "
                  "below both:")
            for a, b, cs in shared:
                print(f"  {a} and {b}: {', '.join(cs)}")
            print("  Distinctness over them is admissible; disjointness "
                  "would not be.")

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