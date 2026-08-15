"""
gen_bcp47.py
============

Generates BCP47000-0.ax from the canonical Resources/bcp47.ttl source.

Encodes BCP 47 (RFC 5646) language tags as a flat registry. The registry-
uniqueness rule of RFC 5646 §2.2.1 is captured as an owl:AllDifferent
assertion in the TTL; this generator unfolds it into pairwise
kge_disjoint/2 facts in TPTP FOF.

Each constant is also asserted as a member of the resource's concept
universe via kge_concept/1 (declared in KGE000-0.ax), enabling
concept-membership guards on complement-operator denotations
(den_neq, den_isnoneof in DENOT000-0.ax).

Source:
    Problems/ODRL/KGConstraints/Resources/bcp47.ttl

Output:
    Problems/ODRL/KGConstraints/Axioms/BCP47000-0.ax

Usage:
    uv run Generators/KGConstraints/gen_bcp47.py
"""

import argparse
import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from header import AXHeader, _ax_comment

try:
    from rdflib import Graph, RDF, OWL, URIRef
    from rdflib.collection import Collection
except ImportError:
    print("ERROR: rdflib is required. Install with: uv pip install rdflib",
          file=sys.stderr)
    sys.exit(1)

VERSION = "1.1"

DEFAULT_TTL = "Problems/ODRL/KGConstraints/Resources/bcp47.ttl"
DEFAULT_OUT = "Problems/ODRL/KGConstraints/Axioms"

BCP_NS = URIRef("https://tools.ietf.org/html/bcp47#")


def _local(uri: URIRef, namespace: URIRef) -> str:
    s = str(uri)
    n = str(namespace)
    if not s.startswith(n):
        raise ValueError(f"URI {s!r} not in namespace {n!r}")
    return s[len(n):]


def _tptp_const(local_name: str) -> str:
    safe = local_name.replace("-", "_")
    return f"bcp_{safe}"


def parse_bcp47(ttl_path: Path) -> tuple[list[str], list[tuple[str, str]]]:
    g = Graph()
    g.parse(str(ttl_path), format="turtle")

    LangTagClass = URIRef(str(BCP_NS) + "LanguageTag")
    tags = sorted(
        _local(s, BCP_NS)
        for s in g.subjects(RDF.type, LangTagClass)
    )

    all_different_members: list[str] = []
    for ad_node in g.subjects(RDF.type, OWL.AllDifferent):
        for members_list in g.objects(ad_node, OWL.distinctMembers):
            members = list(Collection(g, members_list))
            all_different_members = sorted(_local(m, BCP_NS) for m in members)
            break
        if all_different_members:
            break

    if not all_different_members:
        raise ValueError(
            f"{ttl_path}: no owl:AllDifferent assertion found. "
            "BCP 47 fragment requires registry uniqueness."
        )

    if set(all_different_members) != set(tags):
        missing_in_tags = set(all_different_members) - set(tags)
        missing_in_ad   = set(tags) - set(all_different_members)
        raise ValueError(
            f"{ttl_path}: owl:AllDifferent membership does not match the "
            f"set of bcp:LanguageTag instances.\n"
            f"  In AllDifferent but not typed: {sorted(missing_in_tags)}\n"
            f"  Typed but not in AllDifferent: {sorted(missing_in_ad)}"
        )

    constants = [_tptp_const(t) for t in tags]
    pairs = [(a, b) for a, b in combinations(constants, 2)]
    return constants, pairs


def _format_concept_axioms(constants: list[str]) -> str:
    """Emit kge_concept(c) for every BCP 47 constant."""
    lines = []
    for c in constants:
        # Strip the bcp_ prefix for a readable formula name.
        short = c[len("bcp_"):]
        lines.append(
            f"fof(bcp_{short}_concept, axiom, kge_concept({c}))."
        )
    return "\n".join(lines) + "\n"


def _format_disjoint_axioms(pairs: list[tuple[str, str]]) -> str:
    lines = []
    for a, b in pairs:
        an = a[len("bcp_"):]
        bn = b[len("bcp_"):]
        lines.append(
            f"fof(bcp_{an}_disjoint_{bn}, axiom, kge_disjoint({a}, {b}))."
        )
    return "\n".join(lines) + "\n"


def generate_bcp47000(ttl_path: Path) -> str:
    constants, pairs = parse_bcp47(ttl_path)

    body = (
        "% =========================================================================="
        "\n% BCP 47 language-tag fragment              [Paper: tab:realizations,"
        "\n%                                            Example 2 language pair]"
        "\n%"
        "\n% Source: Resources/bcp47.ttl"
        "\n% Encoding: each ISO 639-1 primary language subtag is a TPTP constant"
        "\n% asserted as a kge_concept (resource universe membership) and"
        "\n% pairwise kge_disjoint via RFC 5646 § 2.2.1 registry uniqueness."
        "\n% Partial order is equality (flat registry); the kge_leq_reflexive"
        "\n% axiom from KGE000-0.ax suffices."
        f"\n% Tags: {len(constants)}.  Concept assertions: {len(constants)}."
        f"\n% Pairwise disjoint pairs: {len(pairs)}."
        "\n% =========================================================================="
        "\n"
        "\n% ----- Concept universe membership (kge_concept) -----"
        "\n"
        + _format_concept_axioms(constants)
        + "\n% ----- Pairwise disjointness (RFC 5646 § 2.2.1) -----"
        "\n"
        + _format_disjoint_axioms(pairs)
    )

    n_concepts = len(constants)
    n_pairs = len(pairs)
    note = (
        f"Generated from Resources/bcp47.ttl by gen_bcp47.py.\n"
        f"Depends on KGE000-0.ax (kge_disjoint and kge_concept signatures).\n"
        f"{n_concepts} kge_concept assertions + "
        f"{n_pairs} pairwise disjointness facts.\n"
        f"Problem files emit:\n"
        f"  include('Axioms/KGE000-0.ax').\n"
        f"  include('Axioms/DENOT000-0.ax').\n"
        f"  include('Axioms/BCP47000-0.ax').\n"
        f"No axiom file self-includes this file."
    )
    header = AXHeader(
        file     = "BCP47000-0.ax",
        domain   = "kb",
        title    = "BCP 47 language-tag registry fragment",
        version  = VERSION,
        english  = (
            "Concrete grounding facts for the language left operand,\n"
            "derived from a 15-tag slice of the IANA Language Subtag\n"
            "Registry covering EU official languages plus the motivating\n"
            "example pair (bcp:de, bcp:fr). Flat registry: partial order\n"
            "is equality. Each tag is declared as a kge_concept (resource\n"
            "universe membership) and asserted pairwise disjoint via RFC\n"
            "5646 § 2.2.1 registry uniqueness. This is the resource that\n"
            "yields the Conflict verdict on the language operand in the\n"
            "paper's Example 2."
        ),
        refs     = ["kgc2026"],
        comments = _ax_comment(
            body,
            f"{n_concepts} concept assertions + "
            f"{n_pairs} pairwise disjointness facts (BCP 47 registry uniqueness)",
            note,
        ),
        fof_text = body,
    ).render()
    return header + "\n" + body


def main():
    parser = argparse.ArgumentParser(
        description="Generate BCP47000-0.ax from Resources/bcp47.ttl."
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

    content = generate_bcp47000(ttl_path)
    actual = content.count("fof(")
    if args.stdout:
        print(content)
        print(f"\n{actual} formulae", file=sys.stderr)
        return

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "BCP47000-0.ax"
    path.write_text(content, encoding="utf-8")
    print(f"Written : {path}  ({actual} formulae)")


if __name__ == "__main__":
    main()