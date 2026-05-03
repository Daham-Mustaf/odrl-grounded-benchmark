"""
gen_runtime.py
==============
Generates RUNTIME000-0.ax: runtime evaluation request semantics. Encodes
Definition 11 (Evaluation request) and Definition 12 (Constraint
satisfaction) of the paper.

Theorem 3 (Runtime soundness) is NOT asserted in this file; it is
stated as a conjecture in the Runtime/ problem files and must be
derived from these axioms plus DENOT000/KGE000.

Output:
    Problems/ODRL/KGConstraints/Axioms/RUNTIME000-0.ax
Usage:
    uv run Generators/KGConstraints/gen_runtime.py
"""
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from header import AXHeader, _ax_comment

VERSION = "1.1"
EXPECTED_COUNT = 4

RUNTIME000_BODY = """\
% ==========================================================================
% Evaluation request                         [Paper: def:context]
%
% A request omega is a partial function from left operands to values.
% omega_assigns(R, L, V) means request R assigns value V to left operand L.
% omega_dom(R, L) means R is defined at L (the request mentions L).
% ==========================================================================

fof(omega_dom_def, axiom,
    ![R, L]:
      (omega_dom(R, L) <=> ?[V]: omega_assigns(R, L, V))).

% Functionality of omega: a request assigns at most one value per operand.

fof(omega_functional, axiom,
    ![R, L, V1, V2]:
      ((omega_assigns(R, L, V1) & omega_assigns(R, L, V2)) => V1 = V2)).

% ==========================================================================
% Constraint satisfaction                    [Paper: def:satisfaction]
%
% Request R satisfies constraint C, written satisfies(R, C), iff
% there exist L, V, G such that:
%   (i)   C has left operand L                       (operand_of)
%   (ii)  R assigns L the value V                    (omega_assigns)
%   (iii) V grounds in the resource as G             (grounded_as_value)
%   (iv)  C's denotation is defined (not undef)      (DENOT000 hook)
%   (v)   G lies in C's denotation                   (in_denotation)
% Default-deny: if no such L, V, G exist, satisfies is false.
%
% Note: denotation-undef is reused from DENOT000-0.ax rather than a
% local det_denotation/1 predicate.
% ==========================================================================

fof(satisfies_def, axiom,
    ![R, C]:
      (satisfies(R, C) <=>
        ?[L, V, G]:
          (operand_of(C, L) &
           omega_assigns(R, L, V) &
           grounded_as_value(V, G) &
           ~denotation_undef(C) &
           in_denotation(G, C)))).

% ==========================================================================
% Optional helper                            [derived from satisfies_def]
%
% If R satisfies C, then C's denotation is non-empty.  Logically derivable
% from satisfies_def; included as a proof hint for Compatible-side
% witness problems.
% ==========================================================================

fof(satisfies_witness, axiom,
    ![R, C]:
      (satisfies(R, C) => ?[X]: in_denotation(X, C))).
"""

def generate_runtime000() -> str:
    name = "RUNTIME000-0.ax"
    note = (
        "Depends on DENOT000-0.ax (in_denotation, denotation_undef).\n"
        "Problem files for runtime soundness emit:\n"
        "  include('Axioms/KGE000-0.ax').\n"
        "  include('Axioms/DENOT000-0.ax').\n"
        "  include('Axioms/RUNTIME000-0.ax').\n"
        "  include('Axioms/<resource>.ax').\n"
        "  ... constraint instantiation and request facts ...\n"
        "  fof(thm3_runtime_soundness, conjecture,\n"
        "      ![C1, C2]:\n"
        "        (verdict_conflict(C1, C2) =>\n"
        "          ![R]: ~(satisfies(R, C1) & satisfies(R, C2)))).\n"
        "Hooks expected from problem files:\n"
        "  omega_assigns/3        -- request value assignment\n"
        "  operand_of/2           -- which left operand a constraint uses\n"
        "  grounded_as_value/2    -- value-side grounding (gamma applied)\n"
        "Note: denotation_undef/1 is provided by DENOT000-0.ax.\n"
        "No axiom file self-includes this file."
    )
    header = AXHeader(
        file     = name,
        domain   = "kb",
        title    = "Runtime evaluation request semantics",
        version  = VERSION,
        english  = (
            "Encodes Definition 11 (Evaluation request) and Definition 12\n"
            "(Constraint satisfaction with default-deny). Theorem 3\n"
            "(Runtime soundness: static Conflict verdict implies no request\n"
            "can satisfy both constraints jointly) is NOT asserted here;\n"
            "it is a conjecture stated in Runtime/ problem files. The\n"
            "default-deny rule fires whenever the request has no value\n"
            "for the operand, the value fails to ground, or the\n"
            "denotation is undefined."
        ),
        refs     = ["kgc2026"],
        comments = _ax_comment(
            RUNTIME000_BODY,
            "1 omega_dom def + 1 omega functionality + "
            "1 satisfaction def + 1 satisfaction witness helper",
            note,
        ),
        fof_text = RUNTIME000_BODY,
    ).render()
    return header + "\n" + RUNTIME000_BODY


def main():
    parser = argparse.ArgumentParser(description="Generate RUNTIME000-0.ax")
    parser.add_argument("--out-dir",
                        default="Problems/ODRL/KGConstraints/Axioms")
    parser.add_argument("--stdout", action="store_true")
    args = parser.parse_args()
    content = generate_runtime000()
    actual = content.count("fof(")
    ok = "✓" if actual == EXPECTED_COUNT else "✗"
    if args.stdout:
        print(content)
        print(f"\n{actual} formulae (expected {EXPECTED_COUNT}) {ok}",
              file=sys.stderr)
        return
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "RUNTIME000-0.ax"
    path.write_text(content, encoding="utf-8")
    print(f"Written : {path}  ({actual} formulae, expected {EXPECTED_COUNT}) {ok}")


if __name__ == "__main__":
    main()