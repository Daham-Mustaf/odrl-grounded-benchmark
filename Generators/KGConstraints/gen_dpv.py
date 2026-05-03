"""
gen_dpv.py
==========

Generates DPV000-0.ax from the canonical Resources/dpv.ttl source.

Encodes the DPV (Data Privacy Vocabulary) Purpose hierarchy as a
partial-order lattice. Extracts skos:broader edges and emits one
kge_leq fact per direct edge; transitive closure is provided by
KGE000-0.ax::kge_leq_transitive at proof time.

Each concept is also asserted as a member of the resource's universe
via kge_concept/1 (declared in KGE000-0.ax), enabling concept-membership
guards on complement-operator denotations (den_neq, den_isnoneof in
DENOT000-0.ax).

Crucially: this file asserts NO disjointness between sibling purposes.
DPV does not assert sibling disjointness, and the open-world assumption
is what gives the motivating-example Unknown verdict on the purpose
operand. Sibling-Disjointness Assumption (SDA) profiles are applied
at evaluation time, not here.

Source:
    Problems/ODRL/KGConstraints/Resources/dpv.ttl

Output:
    Problems/ODRL/KGConstraints/Axioms/DPV000-0.ax

Usage:
    uv run Generators/KGConstraints/gen_dpv.py
"""

import argparse
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from header import AXHeader, _ax_comment

try:
    from rdflib import Graph, RDF, URIRef
    from rdflib.namespace import SKOS
except ImportError:
    print("ERROR: rdflib is required. Install with: uv pip install rdflib",
          file=sys.stderr)
    sys.exit(1)

VERSION = "1.2"

DEFAULT_TTL = "Problems/ODRL/KGConstraints/Resources/dpv.ttl"
DEFAULT_OUT = "Problems/ODRL/KGConstraints/Axioms"

DPV_NS = URIRef("https://w3id.org/dpv#")


def _local(uri: URIRef, namespace: URIRef) -> str:
    s = str(uri)
    n = str(namespace)
    if not s.startswith(n):
        raise ValueError(f"URI {s!r} not in namespace {n!r}")
    return s[len(n):]


def _tptp_const(local_name: str) -> str:
    out = []
    for i, ch in enumerate(local_name):
        if ch.isupper() and i > 0:
            out.append("_")
        out.append(ch.lower())
    return "dpv_" + "".join(out)


def _check_acyclic(edges: list[tuple[str, str]]) -> None:
    children_of = defaultdict(set)
    for c, p in edges:
        children_of[c].add(p)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = defaultdict(lambda: WHITE)
    def visit(node: str, stack: list[str]) -> None:
        color[node] = GRAY
        for parent in children_of.get(node, ()):
            if color[parent] == GRAY:
                cycle = stack[stack.index(parent):] + [parent]
                raise ValueError(
                    f"Cycle in skos:broader: {' -> '.join(cycle)}"
                )
            if color[parent] == WHITE:
                visit(parent, stack + [parent])
        color[node] = BLACK
    for node in list(children_of.keys()):
        if color[node] == WHITE:
            visit(node, [node])


def parse_dpv(ttl_path: Path) -> tuple[list[str], list[tuple[str, str]]]:
    g = Graph()
    g.parse(str(ttl_path), format="turtle")

    PurposeClass = URIRef(str(DPV_NS) + "Purpose")
    concepts: set[str] = set()
    for s in g.subjects(RDF.type, PurposeClass):
        concepts.add(_local(s, DPV_NS))
    for s in g.subjects(RDF.type, SKOS.Concept):
        if str(s).startswith(str(DPV_NS)):
            concepts.add(_local(s, DPV_NS))

    if not concepts:
        raise ValueError(f"{ttl_path}: no DPV purpose concepts found.")

    edges: list[tuple[str, str]] = []
    for child, parent in g.subject_objects(SKOS.broader):
        if not (str(child).startswith(str(DPV_NS)) and
                str(parent).startswith(str(DPV_NS))):
            continue
        edges.append((_local(child, DPV_NS), _local(parent, DPV_NS)))

    if not edges:
        raise ValueError(f"{ttl_path}: no skos:broader edges found.")

    for c, p in edges:
        if c not in concepts:
            raise ValueError(
                f"{ttl_path}: edge child {c!r} is not a typed concept."
            )
        if p not in concepts:
            raise ValueError(
                f"{ttl_path}: edge parent {p!r} is not a typed concept."
            )

    _check_acyclic(edges)

    constants = sorted(_tptp_const(c) for c in concepts)
    edges_t = sorted(
        (_tptp_const(c), _tptp_const(p))
        for c, p in edges
    )
    return constants, edges_t


def _format_concept_axioms(constants: list[str]) -> str:
    """Emit kge_concept(c) for every DPV concept."""
    lines = []
    for c in constants:
        # Strip the dpv_ prefix for a readable formula name.
        short = c[len("dpv_"):]
        lines.append(
            f"fof(dpv_{short}_concept, axiom, kge_concept({c}))."
        )
    return "\n".join(lines) + "\n"


def _format_leq_axioms(edges: list[tuple[str, str]]) -> str:
    lines = []
    for child, parent in edges:
        cn = child[len("dpv_"):]
        pn = parent[len("dpv_"):]
        lines.append(
            f"fof(dpv_{cn}_leq_{pn}, axiom, kge_leq({child}, {parent}))."
        )
    return "\n".join(lines) + "\n"


def generate_dpv000(ttl_path: Path) -> str:
    constants, edges = parse_dpv(ttl_path)
    n_concepts = len(constants)
    n_edges = len(edges)

    body = (
        "% ==========================================================================\n"
        "% DPV (Data Privacy Vocabulary) Purpose hierarchy\n"
        "%                                            [Paper: tab:realizations,\n"
        "%                                             Example 1 purpose pair]\n"
        "%\n"
        "% Source: Resources/dpv.ttl\n"
        "% Encoding: each DPV purpose concept is a TPTP constant; skos:broader\n"
        "% edges are emitted as direct kge_leq facts.  Transitive closure is\n"
        "% provided by KGE000-0.ax::kge_leq_transitive at proof time.\n"
        "% Each concept is also asserted as a kge_concept (resource universe\n"
        "% membership) for use by complement-operator denotations.\n"
        "%\n"
        "% NO disjointness facts are asserted in this file.  DPV does not assert\n"
        "% sibling disjointness, and that absence is exactly what gives the\n"
        "% motivating-example Unknown verdict on the purpose operand:\n"
        "%   (purpose, isA, dpv:NonCommercialPurpose) cap (purpose, eq,\n"
        "%   dpv:ScientificResearch) yields Unknown because DPV asserts neither\n"
        "%   ScientificResearch leq NonCommercialPurpose nor disjointness.\n"
        "%\n"
        "% Cross-resource convention: this file asserts only DPV facts.  No\n"
        "% kge_disjoint or kge_leq fact involves constants from other resources;\n"
        "% maintaining this convention across all resource files prevents\n"
        "% cross-domain disjointness propagation pathology.\n"
        "%\n"
        f"% Concepts: {n_concepts}.  Concept assertions: {n_concepts}.\n"
        f"% Direct skos:broader edges: {n_edges}.\n"
        "% Acyclicity verified at generation time.\n"
        "% ==========================================================================\n"
        "\n% ----- Concept universe membership (kge_concept) -----\n"
        + _format_concept_axioms(constants)
        + "\n% ----- skos:broader edges (kge_leq) -----\n"
        + _format_leq_axioms(edges)
    )

    note = (
        f"Generated from Resources/dpv.ttl by gen_dpv.py.\n"
        f"Depends on KGE000-0.ax (kge_leq + kge_concept signatures, "
        f"kge_leq_transitive, kge_leq_antisymmetric, kge_leq_reflexive).\n"
        f"{n_concepts} kge_concept assertions + "
        f"{n_edges} direct skos:broader edges over {n_concepts} concepts.\n"
        f"Acyclicity is verified at generation time.\n"
        f"NO disjointness asserted (OWA).  Problem files emit:\n"
        f"  include('Axioms/KGE000-0.ax').\n"
        f"  include('Axioms/DENOT000-0.ax').\n"
        f"  include('Axioms/DPV000-0.ax').\n"
        f"No axiom file self-includes this file."
    )
    header = AXHeader(
        file     = "DPV000-0.ax",
        domain   = "kb",
        title    = "DPV Purpose hierarchy fragment",
        version  = VERSION,
        english  = (
            f"Concrete grounding facts for the purpose left operand,\n"
            f"derived from a {n_concepts}-concept slice of the W3C Data Privacy\n"
            f"Vocabulary (DPV v2.3, https://w3id.org/dpv) with {n_edges}\n"
            f"direct skos:broader edges. Each concept is declared as a\n"
            f"kge_concept (resource universe membership).\n"
            f"Disjointness is NOT asserted: DPV does not assert sibling\n"
            f"disjointness, and the open-world absence of an axiom between\n"
            f"ScientificResearch and NonCommercialPurpose is exactly what\n"
            f"yields the Unknown verdict in the paper's Example 1. The\n"
            f"Sibling-Disjointness Assumption (SDA) profile is applied at\n"
            f"evaluation time, not here."
        ),
        refs     = ["kgc2026"],
        comments = _ax_comment(
            body,
            f"{n_concepts} concept assertions + "
            f"{n_edges} direct skos:broader edges (transitive closure via KGE000-0.ax)",
            note,
        ),
        fof_text = body,
    ).render()
    return header + "\n" + body


def main():
    parser = argparse.ArgumentParser(
        description="Generate DPV000-0.ax from Resources/dpv.ttl."
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

    content = generate_dpv000(ttl_path)
    actual = content.count("fof(")
    if args.stdout:
        print(content)
        print(f"\n{actual} formulae", file=sys.stderr)
        return

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "DPV000-0.ax"
    path.write_text(content, encoding="utf-8")
    print(f"Written : {path}  ({actual} formulae)")


if __name__ == "__main__":
    main()