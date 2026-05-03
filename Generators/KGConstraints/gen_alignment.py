"""
gen_alignment.py
================
Generates ALIGN000-0.ax: cross-resource alignment frame axioms. Encodes
Definition 10 (Resource alignment) of the paper. Proposition 2 (Verdict
under alignment) and Corollary 1 (Refinement under alignment) are NOT
asserted here; they are stated as conjectures in the Alignment/ problem
files and must be derived from these axioms plus DENOT000/REFINE000.

Output:
    Problems/ODRL/KGConstraints/Axioms/ALIGN000-0.ax
Usage:
    uv run Generators/KGConstraints/gen_alignment.py
"""
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from header import AXHeader, _ax_comment

VERSION = "1.1"
EXPECTED_COUNT = 15

ALIGN000_BODY = """\
% ==========================================================================
% Resource alignment alpha : C_A -> C_B      [Paper: def:alignment]
%
% An alignment is a one-to-one partial FUNCTION between two grounding
% resources for the same left operand.  We encode all four conditions
% from Definition 10:
%   - order preservation (biconditional)
%   - disjointness preservation (one-way)
%   - below preservation: domain closure + witness existence
%   - above preservation: domain closure + witness existence
% plus the two function-theoretic basics: functionality and injectivity.
%
% align(X, Y) = "alpha is defined at X and maps to Y".
% align_dom(X) = "X is in the domain of alpha".
%
% Note: the paper's preservation conditions are quantified over grounded
% concepts g = gamma_A(v), but our axioms apply to ANY aligned concept.
% This is a strictly stronger condition; problem-file alignments must
% satisfy it everywhere they are defined, not just at grounded concepts.
% ==========================================================================

% --------------------------------------------------------------------------
% Function-theoretic basics
% --------------------------------------------------------------------------

fof(align_functional, axiom,
    ![X, Y1, Y2]:
      ((align(X, Y1) & align(X, Y2)) => Y1 = Y2)).

fof(align_one_to_one, axiom,
    ![X1, X2, Y]:
      ((align(X1, Y) & align(X2, Y)) => X1 = X2)).

fof(align_dom_intro, axiom,
    ![X, Y]:
      (align(X, Y) => align_dom(X))).

% --------------------------------------------------------------------------
% Order preservation (biconditional, on aligned pairs)
% --------------------------------------------------------------------------

fof(align_order_preserving, axiom,
    ![X1, X2, Y1, Y2]:
      ((align(X1, Y1) & align(X2, Y2)) =>
        (leq_A(X1, X2) <=> leq_B(Y1, Y2)))).

% --------------------------------------------------------------------------
% Disjointness preservation (one direction)
% --------------------------------------------------------------------------

fof(align_disjoint_preserving, axiom,
    ![X1, X2, Y1, Y2]:
      ((align(X1, Y1) & align(X2, Y2) & disjoint_A(X1, X2)) =>
        disjoint_B(Y1, Y2))).

% --------------------------------------------------------------------------
% Below preservation: two clauses
%   (i)  every concept below an aligned image is in alpha's domain
%   (ii) every B-side concept below alpha(g) has an A-side preimage
%        below g
% --------------------------------------------------------------------------

fof(align_downward_domain, axiom,
    ![G, GA, XA]:
      ((align(G, GA) & leq_A(XA, G)) => align_dom(XA))).

fof(align_downward_witness, axiom,
    ![G, GA, YB]:
      ((align(G, GA) & leq_B(YB, GA)) =>
        ?[XA]: (align(XA, YB) & leq_A(XA, G)))).

% --------------------------------------------------------------------------
% Above preservation: two clauses (analogous to below)
% --------------------------------------------------------------------------

fof(align_upward_domain, axiom,
    ![G, GA, XA]:
      ((align(G, GA) & leq_A(G, XA)) => align_dom(XA))).

fof(align_upward_witness, axiom,
    ![G, GA, YB]:
      ((align(G, GA) & leq_B(GA, YB)) =>
        ?[XA]: (align(XA, YB) & leq_A(G, XA)))).

% --------------------------------------------------------------------------
% Constraint-level denotation bridge
%
% aligned_constraint(CA, CB) is a problem-file hook saying constraint CA
% in R_A corresponds to constraint CB in R_B under alpha.  The two axioms
% below transport denotation membership across the alignment, in both
% directions, and are required for Proposition 2 to derive.
% --------------------------------------------------------------------------

fof(aligned_denotation_forward, axiom,
    ![CA, CB, X, Y]:
      ((aligned_constraint(CA, CB) &
        in_denotation_A(X, CA) &
        align(X, Y)) =>
        in_denotation_B(Y, CB))).

fof(aligned_denotation_reverse, axiom,
    ![CA, CB, Y]:
      ((aligned_constraint(CA, CB) &
        in_denotation_B(Y, CB)) =>
        ?[X]: (in_denotation_A(X, CA) & align(X, Y)))).
% --------------------------------------------------------------------------
% Operator-matching aligned_constraint axioms
%
% These derive aligned_constraint/2 from align/2 plus the operator. Without
% them, problem files would have to assert aligned_constraint pairings
% directly, risking operator-mismatch errors. With these axioms, problem
% files only need to assert align/2 facts, and the constraint pairings
% follow automatically for each monotone operator.
% --------------------------------------------------------------------------
fof(aligned_constraint_eq, axiom,
    ![GA, GB]:
      (align(GA, GB) => aligned_constraint(c_eq(GA), c_eq(GB)))).
fof(aligned_constraint_isa, axiom,
    ![GA, GB]:
      (align(GA, GB) => aligned_constraint(c_isa(GA), c_isa(GB)))).
fof(aligned_constraint_ispartof, axiom,
    ![GA, GB]:
      (align(GA, GB) => aligned_constraint(c_ispartof(GA), c_ispartof(GB)))).
fof(aligned_constraint_haspart, axiom,
    ![GA, GB]:
      (align(GA, GB) => aligned_constraint(c_haspart(GA), c_haspart(GB)))).       
"""

def generate_align000() -> str:
    name = "ALIGN000-0.ax"
    note = (
        "Depends on conceptual two-resource lifts of KGE000-0.ax and\n"
        "DENOT000-0.ax (predicates suffixed _A and _B). These lifts are\n"
        "emitted by the Alignment problem-file generator, not by this\n"
        "file.\n"
        "Problem files for Alignment instances emit:\n"
        "  include('Axioms/ALIGN000-0.ax').\n"
        "  ... two-resource lifts of KGE000 and DENOT000 (problem-local).\n"
        "  ... resource-specific facts for R_A and R_B.\n"
        "  ... align/2 facts for the alignment alpha.\n"
        "  ... aligned_constraint/2 facts pairing constraints across resources.\n"
        "  fof(prop2_verdict_preservation, conjecture,\n"
        "      ![C1, C2, C1B, C2B]:\n"
        "        ((aligned_constraint(C1, C1B) &\n"
        "          aligned_constraint(C2, C2B) &\n"
        "          verdict_conflict_A(C1, C2)) =>\n"
        "          verdict_conflict_B(C1B, C2B))).\n"
        "Higher-order quantification over alignments is deferred to a\n"
        "separate THF companion file (Leo-III).  This FOF file handles\n"
        "concrete alignment instances.  No axiom file self-includes this\n"
        "file."
    )
    header = AXHeader(
        file     = name,
        domain   = "kb",
        title    = "Resource alignment frame axioms",
        version  = VERSION,
        english = (
            "Encodes Definition 10 (Resource alignment): a one-to-one\n"
            "partial function alpha: C_A -> C_B preserving order and\n"
            "disjointness, with downward and upward preservation each\n"
            "split into a domain-closure clause and a witness clause.\n"
            "Also includes function-theoretic basics (functionality,\n"
            "injectivity) and a constraint-level denotation bridge for\n"
            "transporting in_denotation across the alignment.\n"
            "Operator-matching aligned_constraint axioms derive constraint\n"
            "pairings from align/2 facts for each of the four currently\n"
            "supported monotone operators (eq, isA, isPartOf, hasPart);\n"
            "isAnyOf and isAllOf require variadic-operator handling and are\n"
            "deferred.\n"
            "Proposition 2 (Verdict preservation) and Corollary 1\n"
            "(Refinement under alignment) are NOT asserted here; they are\n"
            "conjectures in Alignment/ problem files."
        ),
        refs     = ["kgc2026"],
        comments = _ax_comment(
            ALIGN000_BODY,
            "2 function basics + 1 dom intro + 1 order pres + 1 disjoint pres + "
            "2 below preservation (domain, witness) + "
            "2 above preservation (domain, witness) + "
            "2 denotation bridge (forward, reverse) + "
            "4 operator-matching aligned_constraint",
            note,
        ),
        fof_text = ALIGN000_BODY,
    ).render()
    return header + "\n" + ALIGN000_BODY


def main():
    parser = argparse.ArgumentParser(description="Generate ALIGN000-0.ax")
    parser.add_argument("--out-dir",
                        default="Problems/ODRL/KGConstraints/Axioms")
    parser.add_argument("--stdout", action="store_true")
    args = parser.parse_args()
    content = generate_align000()
    actual = sum(1 for line in content.splitlines() if line.startswith("fof("))
    ok = "✓" if actual == EXPECTED_COUNT else "✗"
    if args.stdout:
        print(content)
        print(f"\n{actual} formulae (expected {EXPECTED_COUNT}) {ok}",
              file=sys.stderr)
        return
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "ALIGN000-0.ax"
    path.write_text(content, encoding="utf-8")
    print(f"Written : {path}  ({actual} formulae, expected {EXPECTED_COUNT}) {ok}")


if __name__ == "__main__":
    main()