"""
gen_monotonicity.py
===================
Generates MONO000-0.ax: frame axioms for monotonicity under resource
extension. Provides only the extension closure relating a base resource R
to an extended resource R'. The actual monotonicity conjecture
(Proposition 1) is stated per problem file in the Monotonicity/ folder
and must be DERIVED from these frame axioms plus DENOT000/KGE000 lifted
to the two resources.

Output:
    Problems/ODRL/KGConstraints/Axioms/MONO000-0.ax
Usage:
    uv run Generators/KGConstraints/gen_monotonicity.py
"""
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from header import AXHeader, _ax_comment

VERSION = "1.1"
EXPECTED_COUNT = 4

MONO000_BODY = """\
% ==========================================================================
% Frame axioms for monotonicity                  [Paper: prop:monotonicity]
%
% Proposition 1 hypothesis: R' extends R along four dimensions
% (C \\subseteq C', leq \\subseteq leq', disjoint \\subseteq disjoint',
% gamma \\subseteq gamma') without retraction.  This file encodes only
% these four closure axioms.  The Proposition's CONCLUSIONS (denotation
% growth, Conflict preservation, Compatible preservation) are NOT
% asserted here; they are conjectures in the Monotonicity/ problem files.
%
% Problem files supply two-resource versions of DENOT000/KGE000 predicates
% (suffixes _R and _R_prime) and a monotone_op/1 predicate marking
% constraints built from the six monotone operators.
%
% IMPORTANT: Proposition 1 holds only for the monotone-operator fragment.
% Conjectures over neq or isNoneOf constraints (Remark 2) should be
% guarded by monotone_op/1; failure to guard will yield correct
% counterexamples, not soundness violations.
% ==========================================================================

% Resource extension: every fact in R holds in R'.

fof(extension_concepts, axiom,
    ![X]:
      (in_concepts_R(X) => in_concepts_R_prime(X))).

fof(extension_leq, axiom,
    ![X, Y]:
      (leq_R(X, Y) => leq_R_prime(X, Y))).

fof(extension_disjoint, axiom,
    ![X, Y]:
      (disjoint_R(X, Y) => disjoint_R_prime(X, Y))).

fof(extension_grounding, axiom,
    ![C, G]:
      (grounded_as_R(C, G) => grounded_as_R_prime(C, G))).
"""

def generate_mono000() -> str:
    name = "MONO000-0.ax"
    note = (
        "Depends on conceptual two-resource lifts of KGE000-0.ax and\n"
        "DENOT000-0.ax (predicates suffixed _R and _R_prime). These lifts\n"
        "are emitted by the Monotonicity problem-file generator, not by\n"
        "this file.\n"
        "Problem files in Monotonicity/ emit, in order:\n"
        "  include('Axioms/MONO000-0.ax').\n"
        "  ... two-resource lifts of KGE000 and DENOT000 (problem-local).\n"
        "  ... resource-specific facts for R and R'.\n"
        "  ... constraint instantiation with monotone_op/1 guards.\n"
        "  fof(prop1_denotation, conjecture, ...).\n"
        "  fof(prop1_conflict_preserved, conjecture, ...).\n"
        "  fof(prop1_compatible_preserved, conjecture, ...).\n"
        "No axiom file self-includes this file."
    )
    header = AXHeader(
        file     = name,
        domain   = "kb",
        title    = "Frame axioms for monotonicity under resource extension",
        version  = VERSION,
        english  = (
            "Frame axioms for Proposition 1 (Monotonicity under resource\n"
            "extension). Provides only the four-dimensional extension\n"
            "closure (concepts, leq, disjoint, grounding) from a base\n"
            "resource R to an extended resource R'. The Proposition's\n"
            "conclusions (denotation growth, Conflict preservation,\n"
            "Compatible preservation) are stated as conjectures in problem\n"
            "files and must be derived, not assumed. Restricted to the\n"
            "monotone-operator fragment via problem-file monotone_op/1\n"
            "guards (Remark 2 excludes neq and isNoneOf)."
        ),
        refs     = ["kgc2026"],
        comments = _ax_comment(
            MONO000_BODY,
            "4 extension closure axioms (concepts, leq, disjoint, grounding)",
            note,
        ),
        fof_text = MONO000_BODY,
    ).render()
    return header + "\n" + MONO000_BODY


def main():
    parser = argparse.ArgumentParser(description="Generate MONO000-0.ax")
    parser.add_argument("--out-dir",
                        default="Problems/ODRL/KGConstraints/Axioms")
    parser.add_argument("--stdout", action="store_true")
    args = parser.parse_args()
    content = generate_mono000()
    actual = content.count("fof(")
    ok = "✓" if actual == EXPECTED_COUNT else "✗"
    if args.stdout:
        print(content)
        print(f"\n{actual} formulae (expected {EXPECTED_COUNT}) {ok}",
              file=sys.stderr)
        return
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "MONO000-0.ax"
    path.write_text(content, encoding="utf-8")
    print(f"Written : {path}  ({actual} formulae, expected {EXPECTED_COUNT}) {ok}")


if __name__ == "__main__":
    main()