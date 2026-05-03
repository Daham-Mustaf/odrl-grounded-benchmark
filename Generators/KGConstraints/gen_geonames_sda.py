"""
gen_geonames_sda.py
===================
Generates GN001-SDA-0.ax: the Sibling Disjointness Assumption profile
for GeoNames. Reads the same Resources/geonames.ttl source as
gen_geonames.py, then emits kge_disjoint facts for every pair of
siblings sharing both a parent and a featureCode.

Cross-featureCode pairs (e.g., a city and an ADM1 region under the
same country) are NOT made disjoint — they are nested in the
geographic hierarchy, not disjoint.

Singleton groups (only one child of a (parent, featureCode) pair)
emit no axioms.

GeoNames as published does not assert sibling disjointness; this
profile is required for spatial Conflict verdicts. Problem files that
should remain Unknown under OWA do NOT include this file.

Source:
    Problems/ODRL/KGConstraints/Resources/geonames.ttl
Output:
    Problems/ODRL/KGConstraints/Axioms/GN001-SDA-0.ax

Usage:
    uv run Generators/KGConstraints/gen_geonames_sda.py
"""
import argparse
import itertools
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from header import AXHeader, _ax_comment

# Reuse the parsing logic from gen_geonames so we stay in sync with GN000.
from KGConstraints.gen_geonames import parse_geonames

VERSION = "1.0"
DEFAULT_TTL = "Problems/ODRL/KGConstraints/Resources/geonames.ttl"
DEFAULT_OUT = "Problems/ODRL/KGConstraints/Axioms"


def group_siblings(features: dict, edges: list) -> dict:
    """
    Group child constants by (parent_const, child_featureCode).
    Only groups with >= 2 children produce SDA axioms.
    """
    by_const = {f["const"]: f for f in features.values()}
    groups: dict[tuple[str, str], list[str]] = defaultdict(list)
    for child_c, parent_c, _cid, _pid, _cname, _pname in edges:
        fcode = by_const[child_c].get("fcode") or "UNKNOWN"
        groups[(parent_c, fcode)].append(child_c)
    # Drop singleton groups: no pairs to emit.
    return {k: sorted(v) for k, v in groups.items() if len(v) >= 2}


def render_disjointness_facts(groups: dict) -> tuple[str, int]:
    """Emit kge_disjoint axioms for all same-featureCode sibling pairs."""
    lines = []
    count = 0
    for (parent, fcode), children in sorted(groups.items()):
        lines.append(f"% ----- Siblings under {parent} (featureCode {fcode}) -----")
        for a, b in itertools.combinations(children, 2):
            short_a = a[len("gn_"):]
            short_b = b[len("gn_"):]
            ax_name = f"sda_{short_a}_disjoint_{short_b}"
            lines.append(
                f"fof({ax_name}, axiom, kge_disjoint({a}, {b}))."
            )
            count += 1
        lines.append("")
    return "\n".join(lines), count


def generate_gn001_sda(ttl_path: Path) -> tuple[str, int]:
    features, edges = parse_geonames(ttl_path)
    groups = group_siblings(features, edges)
    body_axioms, count = render_disjointness_facts(groups)

    n_groups = len(groups)
    n_features = len(features)

    body = (
        "% ==========================================================================\n"
        "% GeoNames Sibling Disjointness Assumption (SDA) profile\n"
        "%                                          [Paper: tab:realizations]\n"
        "%\n"
        "% Source: Resources/geonames.ttl (same as GN000-0.ax)\n"
        "% Encoding: for each (parent, featureCode) group with at least two\n"
        "% children, emit pairwise kge_disjoint facts among the children.\n"
        "%\n"
        "% Rationale: GeoNames as published does not assert that siblings\n"
        "% are mutually exclusive. For static conflict detection on the\n"
        "% spatial operand, we adopt the closed-world convention that two\n"
        "% same-kind administrative or political units sharing a parent\n"
        "% (e.g., two A.PCLI countries under Europe; two A.ADM1 regions\n"
        "% under France) name disjoint sets of places. This is sound for\n"
        "% standard administrative hierarchies; cross-featureCode pairs\n"
        "% (city vs region) are nested, not disjoint, and are NOT made\n"
        "% disjoint here.\n"
        "%\n"
        "% Use: problems that need spatial Conflict verdicts include this\n"
        "% file IN ADDITION TO GN000-0.ax. Problems testing spatial Unknown\n"
        "% verdicts do NOT include this file -- their Unknown verdict\n"
        "% depends on the absence of asserted disjointness.\n"
        "%\n"
        f"% Sibling groups with at least two members: {n_groups}.\n"
        f"% Pairwise disjointness facts emitted: {count}.\n"
        f"% Source features (from GN000-0.ax): {n_features}.\n"
        "% ==========================================================================\n"
        + body_axioms
    )

    note = (
        "Generated from Resources/geonames.ttl by gen_geonames_sda.py.\n"
        "Depends on KGE000-0.ax (kge_disjoint signature, kge_disjoint_symmetric,\n"
        "kge_disjoint_irreflexive, kge_disjoint_propagation) and GN000-0.ax\n"
        "(parent edges; transitive closure via kge_leq_transitive).\n"
        "Problems requiring spatial Conflict verdicts emit, in order:\n"
        "  include('Axioms/KGE000-0.ax').\n"
        "  include('Axioms/DENOT000-0.ax').\n"
        "  include('Axioms/GN000-0.ax').\n"
        "  include('Axioms/GN001-SDA-0.ax').    -- adds sibling disjointness\n"
        "Problems testing spatial Unknown verdicts MUST NOT include this\n"
        "file -- their Unknown verdict depends on absence of disjointness.\n"
        "No axiom file self-includes this file."
    )
    header = AXHeader(
        file     = "GN001-SDA-0.ax",
        domain   = "kb",
        title    = "GeoNames Sibling Disjointness Assumption (SDA) profile",
        version  = VERSION,
        english  = (
            "Sibling disjointness profile for GeoNames. Augments GN000-0.ax\n"
            "with pairwise kge_disjoint facts for siblings sharing both a\n"
            "parent and a featureCode. Cross-featureCode 'siblings'\n"
            "(e.g., city vs region under the same country) are NOT made\n"
            "disjoint, because they're nested. GeoNames as published does\n"
            "not assert sibling disjointness; this profile is required for\n"
            "spatial Conflict verdicts."
        ),
        refs     = ["kgc2026"],
        comments = _ax_comment(
            body,
            f"{count} pairwise disjointness facts across {n_groups} sibling groups",
            note,
        ),
        fof_text = body,
    ).render()
    return header + "\n" + body, count


def main():
    parser = argparse.ArgumentParser(
        description="Generate GN001-SDA-0.ax from Resources/geonames.ttl."
    )
    parser.add_argument("--ttl", default=DEFAULT_TTL)
    parser.add_argument("--out-dir", default=DEFAULT_OUT)
    parser.add_argument("--stdout", action="store_true")
    args = parser.parse_args()

    ttl_path = Path(args.ttl)
    if not ttl_path.exists():
        print(f"ERROR: TTL file not found: {ttl_path}", file=sys.stderr)
        sys.exit(1)

    content, count = generate_gn001_sda(ttl_path)
    actual = content.count("fof(")
    ok = "✓" if actual == count else "✗"

    if args.stdout:
        print(content)
        print(f"\n{actual} formulae (expected {count}) {ok}", file=sys.stderr)
        return

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "GN001-SDA-0.ax"
    path.write_text(content, encoding="utf-8")
    print(f"Written : {path}  ({actual} formulae) {ok}")


if __name__ == "__main__":
    main()