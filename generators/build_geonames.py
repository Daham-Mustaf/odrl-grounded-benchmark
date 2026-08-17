"""
build_geonames.py
=================
Builds a GeoNames slice from the official dump: the resource, the background
theory, the TPTP axioms, and the profile entry that binds them.

    python build_geonames.py --hierarchy hierarchy.txt \
        --country-info countryInfo.txt --depth 1 --out problems

Depth, not geography, is the knob.  At depth 1 every mer problem is a
two-step chain and transitivity is never exercised; at depth 2 an isPartOf
Europe against an eq on an administrative unit needs a two-hop chain, and a
refutation visibly cites two resource premises and a transitivity instance.
Widening to other continents adds nothing the depth series does not show.

Only ADM-typed edges are followed.  The dump also carries entries added
through the user interface, which are not the administrative hierarchy the
gazetteer publishes; one of them puts Sudan under Europe.

Sibling disjointness is generated, not published.  GeoNames asserts no
disjointness at all.  Two administrative units under one parent do not
overlap, so the parties declare it, and it belongs in the background theory.
Its scope is a choice the paper has to state:

    --siblings parent   units sharing a parent
    --siblings depth    all units at the same depth, quadratic

The two are not semantically distinct below the first level.  Take Bavaria
within Germany and Tyrol within Austria, with Germany and Austria separated
as siblings under Europe.  Anything below both Bavaria and Tyrol is below
both countries by transitivity, contradicting their disjointness, so the
parent rule already separates them in every model.  What `depth` adds at the
second level is therefore derivable, at quadratic cost.  It differs only at
the first level, where the root's children are the level.

Only pairs whose separation depends on an unseparated intermediate ancestor
come out Unknown under `parent`.
"""

import argparse
import sys
from collections import defaultdict
from pathlib import Path

LICENCE = ("CC BY 4.0.  Credit GeoNames: https://www.geonames.org")


def read_hierarchy(path: Path) -> dict[str, list[str]]:
    """parent -> ADM children, in file order."""
    kids = defaultdict(list)
    with path.open(encoding="utf-8") as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) >= 3 and p[2] == "ADM":
                kids[p[0]].append(p[1])
    return kids


def read_names(path: Path) -> dict[str, str]:
    """geonameid -> name, from countryInfo.txt.  Deeper levels have no entry
    there, so they fall back to their id."""
    names = {}
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                continue
            c = line.rstrip("\n").split("\t")
            if len(c) >= 17 and c[16].isdigit():
                names[c[16]] = c[4]
    return names


def descend(kids, root: str, depth: int, limit_per_level=None):
    """Levels below root, each sorted by id so a series is nested.

    Sorting before truncation matters: with --limit applied first, a slice of
    10 and a slice of 20 need not share their first 10, and the stability
    experiment requires one resource to be a subset of the other.
    """
    levels, frontier = [], [root]
    for _ in range(depth):
        nxt = []
        for parent in frontier:
            children = sorted(kids.get(parent, []), key=lambda x: int(x))
            if limit_per_level:
                children = children[:limit_per_level]
            nxt.extend((parent, c) for c in children)
        if not nxt:
            break
        levels.append(nxt)
        frontier = [c for _, c in nxt]
    return levels


def slug(gid: str, names: dict | None = None) -> str:
    """The GeoNames id, always.

    Not the name.  Names collide across countries, and two concepts sharing a
    slug would make the resource assert a unit within two parents and the
    sibling rule declare a concept disjoint from itself, which is
    unsatisfiable and would turn every spatial verdict Incompatible.  Names
    are also not TPTP-safe: Aaland Islands is an administrative child of
    Europe, and Python's isalnum accepts its non-ASCII first letter, so a
    name-derived constant would be illegal in a lower_word.  The id is what
    GeoNames publishes as identity, and it is the honest grounding target;
    the human name is carried as rdfs:label.
    """
    return f"gn_{gid}"


def resource_ttl(root, levels, names, root_slug, tag) -> str:
    edges = [e for lvl in levels for e in lvl]
    concepts = {root} | {c for _, c in edges}
    head = [
        "# GeoNames slice: the containment the gazetteer publishes.",
        "#",
        f"# Root {root}, ADM-typed edges only, {len(levels)} level(s) deep.",
        "# The dump also carries entries added through the user interface;",
        "# those are not the administrative hierarchy and are excluded.",
        "#",
        "# Order assertions only.  GeoNames asserts no disjointness, so the",
        "# sibling rule the parties adopt is in the background theory.",
        "#",
        "# Source  : https://download.geonames.org/export/dump/",
        f"# Licence : {LICENCE}",
        "",
        "@prefix odrlkb:  <https://w3id.org/odrl-kb/geonames#> .",
        "@prefix dcat:    <http://www.w3.org/ns/dcat#> .",
        "@prefix dcterms: <http://purl.org/dc/terms/> .",
        "@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .",
        "",
        f"<https://w3id.org/odrl-kb/geonames/{tag}> a dcat:Dataset ;",
        f'    dcterms:title "GeoNames containment below {root}, depth '
        f'{len(levels)}"@en ;',
        "    dcterms:source <https://download.geonames.org/export/dump/> ;",
        "    dcterms:license <https://creativecommons.org/licenses/by/4.0/> ;",
        "    odrlkb:orderPredicate odrlkb:within ;",
        f"    odrlkb:conceptCount {len(concepts)} ;",
        f"    odrlkb:orderAssertionCount {len(edges)} .",
        "",
        f'odrlkb:{root_slug[3:]} a odrlkb:Feature ; rdfs:label "root"@en .',
        "",
    ]
    body = []
    for parent, child in edges:
        cs, ps = slug(child, names), slug(parent, names)
        body.append(f"odrlkb:{cs[3:]} a odrlkb:Feature ;")
        if names.get(child):
            body.append(f'    rdfs:label "{names[child]}"@en ;')
        body.append(f"    dcterms:identifier <https://sws.geonames.org/{child}/> ;")
        body.append(f"    odrlkb:within odrlkb:{ps[3:]} .")
        body.append("")
    return "\n".join(head + body)


def sibling_pairs(levels, scope: str):
    """Pairs the sibling rule separates."""
    pairs = []
    for lvl in levels:
        if scope == "parent":
            groups = defaultdict(list)
            for parent, child in lvl:
                groups[parent].append(child)
            for g in groups.values():
                pairs += [(a, b) for i, a in enumerate(g) for b in g[i + 1:]]
        else:                                    # depth
            g = [c for _, c in lvl]
            pairs += [(a, b) for i, a in enumerate(g) for b in g[i + 1:]]
    return pairs


def background_ttl(tag, pairs, names, scope) -> str:
    lines = [
        "# Background theory for the GeoNames slice: sibling disjointness.",
        "#",
        "# GeoNames publishes no disjointness.  Administrative units that do",
        "# not overlap are separated here because the parties declare it, not",
        "# because the authority asserted it.  A party may withdraw this",
        "# rule, and any Incompatible verdict resting on it reopens.",
        "#",
        f"# Scope: {scope}.  " + (
            "Units sharing a parent are separated.  Units under different "
            "parents are separated too where their ancestors are, since "
            "anything below both would be below both ancestors by "
            "transitivity."
            if scope == "parent" else
            "Every pair at the same depth is separated."),
        f"# {len(pairs)} assertions.",
        "",
        "@prefix odrlkb:  <https://w3id.org/odrl-kb/geonames#> .",
        "@prefix bt:      <https://w3id.org/odrl-kb/background#> .",
        "@prefix dcterms: <http://purl.org/dc/terms/> .",
        "",
        f"<https://w3id.org/odrl-kb/geonames/{tag}/siblings> a bt:BackgroundTheory ;",
        '    dcterms:title "Sibling disjointness for administrative units"@en ;',
        f"    bt:generatedBy bt:SiblingDisjointness ;",
        f'    bt:scope "{scope}" ;',
        f"    bt:appliesTo <https://w3id.org/odrl-kb/geonames/{tag}> .",
        "",
    ]
    for a, b in pairs:
        lines.append(f"odrlkb:{slug(a,names)[3:]} bt:disjointWith "
                     f"odrlkb:{slug(b,names)[3:]} .")
    return "\n".join(lines) + "\n"


def axioms(levels, pairs, names) -> str:
    lines = ["% Resource: administrative containment.  res_ names mark what",
             "% the authority published.", ""]
    for parent, child in [e for lvl in levels for e in lvl]:
        cs, ps = slug(child, names), slug(parent, names)
        lines.append(f"fof(res_{cs}_within_{ps}, axiom,")
        lines.append(f"    kge_leq({cs}, {ps})).")
    lines += ["", "% Background theory: sibling disjointness, as the denial of",
              "% a common lower bound.  bt_ names mark what a party may",
              "% withdraw.", ""]
    for a, b in pairs:
        sa, sb = slug(a, names), slug(b, names)
        lines.append(f"fof(bt_{sa}_disjoint_{sb}, axiom,")
        lines.append(f"    ~ ? [X] : (kge_leq(X, {sa}) & kge_leq(X, {sb}))).")
    return "\n".join(lines) + "\n"


def profile_ttl(tag) -> str:
    return f"""\
# Profile entry.  ODRL cannot carry this, so it is agreed out of band; the
# paper's conclusion proposes an extension that would.
#
# The order predicate is a property of the resource, not of this binding, so
# it is declared in the resource file and not repeated here.

@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix vrep: <https://w3id.org/odrl-verdict-report#> .
@prefix ex:   <https://w3id.org/odrl-kb/profile/> .

ex:b-spatial a vrep:OperandBinding ;
    vrep:leftOperand odrl:spatial ;
    vrep:sort vrep:mer ;
    vrep:resource <https://w3id.org/odrl-kb/geonames/{tag}> ;
    vrep:backgroundTheory <https://w3id.org/odrl-kb/geonames/{tag}/siblings> ;
    vrep:grounding vrep:sliceMembership .
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hierarchy", required=True, type=Path)
    ap.add_argument("--country-info", required=True, type=Path)
    ap.add_argument("--root", default="6255148", help="default: Europe")
    ap.add_argument("--root-name", default="europe")
    ap.add_argument("--depth", type=int, default=1)
    ap.add_argument("--limit", type=int, default=None,
                    help="children per parent; applied after sorting, so a "
                         "series of slices is nested")
    ap.add_argument("--siblings", choices=("parent", "depth"), default="parent")
    ap.add_argument("--out", default="problems", type=Path)
    args = ap.parse_args()

    kids = read_hierarchy(args.hierarchy)
    names = read_names(args.country_info)
    levels = descend(kids, args.root, args.depth, args.limit)

    if not levels:
        print(f"no ADM children of {args.root}", file=sys.stderr)
        return 1

    edges = [e for lvl in levels for e in lvl]
    concepts = {args.root} | {c for _, c in edges}
    pairs = sibling_pairs(levels, args.siblings)
    root_slug = f"gn_{args.root_name}"
    tag = f"{args.root_name}-d{len(levels)}-{len(concepts)}"

    for d in ("resources", "background", "axioms"):
        (args.out / d).mkdir(parents=True, exist_ok=True)

    (args.out / "resources" / f"geonames-{tag}.ttl").write_text(
        resource_ttl(args.root, levels, names, root_slug, tag), "utf-8")
    (args.out / "background" / f"geonames-{tag}.ttl").write_text(
        background_ttl(tag, pairs, names, args.siblings), "utf-8")
    (args.out / "axioms" / f"GN-{tag}.ax").write_text(
        axioms(levels, pairs, names), encoding="utf-8")
    (args.out / "resources" / f"profile-{tag}.ttl").write_text(
        profile_ttl(tag), encoding="utf-8")

    n = len(concepts)
    print(f"depth {len(levels)}: " +
          ", ".join(f"level {i+1}: {len(l)}" for i, l in enumerate(levels)))
    print(f"{n} concepts, {len(edges)} order assertions, "
          f"{len(pairs)} disjointness assertions ({args.siblings} scope)")
    print(f"transitivity ground instances: {n**3:,}  "
          f"(the checker's cost; the prover instantiates lazily)")
    named = sum(1 for c in concepts if names.get(c))
    print(f"{named}/{n} concepts have a name in countryInfo.txt; constants "
          f"are GeoNames ids in every case")
    if args.depth > len(levels):
        print(f"\nAsked for depth {args.depth}, found {len(levels)}.  The "
              f"dump's readme says the toponym-to-admin relation is not in "
              f"hierarchy.txt and must be built from admin codes, so deeper "
              f"levels need admin1CodesASCII.txt and a second join.")
    for p in sorted(args.out.rglob(f"*{tag}*")):
        print(f"  {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())