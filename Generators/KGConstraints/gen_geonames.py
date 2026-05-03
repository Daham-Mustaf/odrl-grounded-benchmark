"""
gen_geonames.py
===============

Generates GN000-0.ax from the canonical Resources/geonames.ttl source.

Encodes a GeoNames slice covering Europe, France, Germany, their first-
order administrative divisions, and anchor cities. The hierarchy is
extracted from gn:parentFeature edges; transitive closure is provided
by KGE000-0.ax::kge_leq_transitive at proof time.

Each feature is also asserted as a member of the resource's universe via
kge_concept/1 (declared in KGE000-0.ax), enabling concept-membership
guards on complement-operator denotations (den_neq, den_isnoneof in
DENOT000-0.ax).

Note on the partial order: the paper (Table 1) names gn:sfWithin as the
spatial-containment relation. We operationalize this for administrative
units via gn:parentFeature, which is the relation GeoNames uses to
encode the political/administrative hierarchy. gn:sfWithin would
require explicit GeoSPARQL geometries that the GeoNames RDF dump does
not consistently provide.

This file asserts NO disjointness. GeoNames does not assert sibling
disjointness, and the base resource yields Compatible or Unknown
verdicts for spatial constraints. Conflict verdicts on the spatial
operand require the SDA (Sibling Disjointness Assumption) profile,
which is applied separately at evaluation time.

Source:
    Problems/ODRL/KGConstraints/Resources/geonames.ttl

Output:
    Problems/ODRL/KGConstraints/Axioms/GN000-0.ax

Usage:
    uv run Generators/KGConstraints/gen_geonames.py
"""

import argparse
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from header import AXHeader, _ax_comment

try:
    from rdflib import Graph, RDF, URIRef
except ImportError:
    print("ERROR: rdflib is required. Install with: uv pip install rdflib",
          file=sys.stderr)
    sys.exit(1)

VERSION = "1.2"

DEFAULT_TTL = "Problems/ODRL/KGConstraints/Resources/geonames.ttl"
DEFAULT_OUT = "Problems/ODRL/KGConstraints/Axioms"

GN_NS = URIRef("https://www.geonames.org/ontology#")
SWS_PREFIX = "https://sws.geonames.org/"


def _gn_id(uri: URIRef) -> str:
    s = str(uri)
    if not s.startswith(SWS_PREFIX):
        raise ValueError(f"Not a GeoNames sws IRI: {s!r}")
    rest = s[len(SWS_PREFIX):].rstrip("/")
    if not rest.isdigit():
        raise ValueError(f"Expected numeric ID, got {rest!r} in {s!r}")
    return rest


def _slug(name: str) -> str:
    s = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode()
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = s.strip("_")
    return s


def _tptp_const(name: str) -> str:
    return "gn_" + _slug(name)


def _check_acyclic(edges: list[tuple[str, str]]) -> None:
    children_of = defaultdict(set)
    for c, p, *_ in edges:
        children_of[c].add(p)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = defaultdict(lambda: WHITE)
    def visit(node: str, stack: list[str]) -> None:
        color[node] = GRAY
        for parent in children_of.get(node, ()):
            if color[parent] == GRAY:
                cycle = stack[stack.index(parent):] + [parent]
                raise ValueError(
                    f"Cycle in gn:parentFeature: {' -> '.join(cycle)}"
                )
            if color[parent] == WHITE:
                visit(parent, stack + [parent])
        color[node] = BLACK
    for node in list(children_of.keys()):
        if color[node] == WHITE:
            visit(node, [node])


def parse_geonames(ttl_path: Path):
    g = Graph()
    g.parse(str(ttl_path), format="turtle")

    GN_FEATURE = URIRef(str(GN_NS) + "Feature")
    GN_NAME    = URIRef(str(GN_NS) + "name")
    GN_FCODE   = URIRef(str(GN_NS) + "featureCode")
    GN_PARENT  = URIRef(str(GN_NS) + "parentFeature")

    features: dict[str, dict] = {}
    for s in g.subjects(RDF.type, GN_FEATURE):
        gid = _gn_id(s)
        name_objs = list(g.objects(s, GN_NAME))
        if not name_objs:
            raise ValueError(f"Feature {s} has no gn:name.")
        name = str(name_objs[0])
        fcode_objs = list(g.objects(s, GN_FCODE))
        fcode = str(fcode_objs[0]) if fcode_objs else None
        if fcode and fcode.startswith(str(GN_NS)):
            fcode = fcode[len(str(GN_NS)):]
        features[gid] = {
            "name":  name,
            "const": _tptp_const(name),
            "fcode": fcode,
            "iri":   str(s),
        }

    if not features:
        raise ValueError(f"{ttl_path}: no gn:Feature instances found.")

    seen_consts: dict[str, str] = {}
    for gid, f in features.items():
        if f["const"] in seen_consts:
            raise ValueError(
                f"{ttl_path}: TPTP constant collision on '{f['const']}': "
                f"both feature {gid} ({f['name']!r}) and "
                f"feature {seen_consts[f['const']]} share this slug."
            )
        seen_consts[f["const"]] = gid

    edges = []
    for child, parent in g.subject_objects(GN_PARENT):
        try:
            cid = _gn_id(child)
            pid = _gn_id(parent)
        except ValueError as e:
            raise ValueError(f"{ttl_path}: parentFeature edge has bad IRI: {e}")
        if cid not in features:
            raise ValueError(
                f"{ttl_path}: parentFeature child {cid} not typed gn:Feature."
            )
        if pid not in features:
            raise ValueError(
                f"{ttl_path}: parentFeature parent {pid} not typed gn:Feature."
            )
        edges.append((
            features[cid]["const"], features[pid]["const"],
            cid, pid,
            features[cid]["name"], features[pid]["name"],
        ))

    if not edges:
        raise ValueError(f"{ttl_path}: no gn:parentFeature edges found.")

    _check_acyclic(edges)
    edges.sort(key=lambda e: (e[0], e[1]))
    return features, edges


def _format_concept_axioms(features: dict) -> str:
    """Emit kge_concept(c) for every GeoNames feature."""
    lines = []
    lines.append("% Concept universe membership (kge_concept)")
    for gid, f in sorted(features.items(), key=lambda kv: kv[1]["const"]):
        const = f["const"]
        # Strip the gn_ prefix for a readable formula name.
        short = const[len("gn_"):]
        lines.append(
            f"fof(gn_{short}_concept, axiom, kge_concept({const}))."
        )
    return "\n".join(lines) + "\n"


def _format_axioms(features: dict, edges: list) -> str:
    lines = []
    lines.append("% Features in this fragment (numeric IDs from sws.geonames.org):")
    for gid, f in sorted(features.items(), key=lambda kv: kv[1]["const"]):
        fcode = f"  [{f['fcode']}]" if f["fcode"] else ""
        lines.append(f"%   {f['const']:<32s} = {gid}{fcode}  ({f['name']})")
    lines.append("")
    lines.append("% gn:parentFeature edges (transitive closure via KGE000-0.ax)")
    for child_c, parent_c, cid, pid, cname, pname in edges:
        cn = child_c[len("gn_"):]
        pn = parent_c[len("gn_"):]
        lines.append(
            f"% {cname} ({cid}) parentFeature {pname} ({pid})"
        )
        lines.append(
            f"fof(gn_{cn}_leq_{pn}, axiom, kge_leq({child_c}, {parent_c}))."
        )
    return "\n".join(lines) + "\n"


def generate_gn000(ttl_path: Path) -> str:
    features, edges = parse_geonames(ttl_path)
    n_features = len(features)
    n_edges = len(edges)

    body = (
        "% ==========================================================================\n"
        "% GeoNames slice                            [Paper: tab:realizations,\n"
        "%                                             Example 1 spatial pair]\n"
        "%\n"
        "% Source: Resources/geonames.ttl\n"
        "% Encoding: each gn:Feature is a TPTP constant named from gn:name;\n"
        "% the numeric GeoNames ID is preserved as a comment for traceability\n"
        "% to the live sws.geonames.org IRIs.  Each feature is asserted as a\n"
        "% kge_concept (resource universe membership), and gn:parentFeature\n"
        "% edges are emitted as direct kge_leq facts; transitive closure is\n"
        "% provided by KGE000-0.ax::kge_leq_transitive at proof time.\n"
        "%\n"
        "% Note on relation choice: the paper's Table 1 names gn:sfWithin as\n"
        "% the spatial-containment relation.  We operationalize this for\n"
        "% administrative units via gn:parentFeature, the relation GeoNames\n"
        "% uses for political/administrative hierarchy.  gn:sfWithin would\n"
        "% require GeoSPARQL geometries that GeoNames RDF does not\n"
        "% consistently provide.\n"
        "%\n"
        "% gn:parentCountry and gn:parentADM1 shortcut edges are NOT emitted.\n"
        "% Soundness assumes the gn:parentFeature chain is complete from each\n"
        "% feature up to the resource root; verified at generation time only\n"
        "% to the extent that all referenced features are typed gn:Feature.\n"
        "%\n"
        "% Cross-resource convention: this file asserts only GeoNames facts.\n"
        "%\n"
        "% NO disjointness facts are asserted.  GeoNames does not assert\n"
        "% sibling disjointness, and that absence yields Unknown verdicts\n"
        "% on spatial pairs without a shared descendant.  Conflict verdicts\n"
        "% on the spatial operand require the SDA (Sibling Disjointness\n"
        "% Assumption) profile, applied at evaluation time.\n"
        "%\n"
        f"% Features: {n_features}.  Concept assertions: {n_features}.\n"
        f"% Direct gn:parentFeature edges: {n_edges}.\n"
        "% Acyclicity verified at generation time.\n"
        "% ==========================================================================\n"
        + _format_concept_axioms(features)
        + "\n"
        + _format_axioms(features, edges)
    )
    note = (
        f"Generated from Resources/geonames.ttl by gen_geonames.py.\n"
        f"Depends on KGE000-0.ax (kge_leq + kge_concept signatures, "
        f"kge_leq_transitive, kge_leq_antisymmetric, kge_leq_reflexive).\n"
        f"{n_features} kge_concept assertions + "
        f"{n_edges} direct gn:parentFeature edges over {n_features} features.\n"
        f"Acyclicity is verified at generation time.\n"
        f"NO disjointness asserted (OWA).  Problem files emit:\n"
        f"  include('Axioms/KGE000-0.ax').\n"
        f"  include('Axioms/DENOT000-0.ax').\n"
        f"  include('Axioms/GN000-0.ax').\n"
        f"No axiom file self-includes this file."
    )
    header = AXHeader(
        file     = "GN000-0.ax",
        domain   = "kb",
        title    = "GeoNames slice for the spatial operand",
        version  = VERSION,
        english  = (
            f"Concrete grounding facts for the spatial left operand,\n"
            f"derived from a {n_features}-feature slice of GeoNames covering\n"
            f"the EU example region with {n_edges} direct gn:parentFeature\n"
            f"edges. Each feature is declared as a kge_concept (resource\n"
            f"universe membership). Disjointness is NOT asserted: GeoNames\n"
            f"does not assert sibling disjointness, so the base resource\n"
            f"yields Compatible or Unknown verdicts for spatial constraints.\n"
            f"Conflict verdicts require the SDA (Sibling Disjointness\n"
            f"Assumption) profile, applied separately."
        ),
        refs     = ["kgc2026"],
        comments = _ax_comment(
            body,
            f"{n_features} concept assertions + "
            f"{n_edges} direct gn:parentFeature edges (transitive closure via KGE000-0.ax)",
            note,
        ),
        fof_text = body,
    ).render()
    return header + "\n" + body


def main():
    parser = argparse.ArgumentParser(
        description="Generate GN000-0.ax from Resources/geonames.ttl."
    )
    parser.add_argument("--ttl", default=DEFAULT_TTL,
                        help=f"Source TTL file (default: {DEFAULT_TTL})")
    parser.add_argument("--out-dir", default=DEFAULT_OUT,
                        help=f"Output axioms directory (default: {DEFAULT_OUT})")
    parser.add_argument("--stdout", action="store_true",
                        help="Print to stdout instead of writing the file.")
    args = parser.parse_args()

    ttl_path = Path(args.ttl)
    if not ttl_path.exists():
        print(f"ERROR: TTL file not found: {ttl_path}", file=sys.stderr)
        sys.exit(1)

    content = generate_gn000(ttl_path)
    actual = content.count("fof(")
    if args.stdout:
        print(content)
        print(f"\n{actual} formulae", file=sys.stderr)
        return

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "GN000-0.ax"
    path.write_text(content, encoding="utf-8")
    print(f"Written : {path}  ({actual} formulae)")


if __name__ == "__main__":
    main()