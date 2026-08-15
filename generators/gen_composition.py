"""
gen_composition.py
==================
Generates COMPOSE000-0.ax: rule-level composition for the symmetric
`and` fragment via Strong Kleene three-valued logic.

Encodes Corollary 3 of the paper (Section 4.3, "Operand-wise composition
for and"): rule-level verdict for and-composed rules over the same
operand set is determined by per-operand verdicts via Strong Kleene
aggregation.

The `or` and `xone` connectives are deliberately omitted: the paper's
§4.3 lift uses satisfying-set semantics (σ-based, Proposition 4 cross-
disjunct decomposition) for those connectives, which cannot be expressed
via per-operand summary predicates. Audit of `or`/`xone` requires a
separate axiom file (COMPOSE001-0.ax) with σ-level reasoning, deferred
to extended work.

Output:
    Problems/ODRL/KGConstraints/Axioms/COMPOSE000-0.ax

Usage:
    uv run Generators/KGConstraints/gen_composition.py
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from header import AXHeader, _ax_comment


VERSION = "2.0"
EXPECTED_COUNT = 7


COMPOSE000_BODY = """\
% ==========================================================================
% Per-operand verdict aggregation for `and` composition (Corollary 3)
%
% Per-operand verdicts V_k come from Definition 6 (verdict_*).  At rule
% level, two `and`-composed rules over the same operand set aggregate via
% Strong Kleene three-valued logic.  We use a rule-level function
% rule_and/1 over a rule R, valued in {compatible, conflict, unknown}.
%
% Rule-level summary hooks (instantiated by problem files from per-operand
% verdict_compatible/2, verdict_conflict/2, verdict_unknown/2):
%
%   has_conflict(R)  : at least one operand-level verdict is Conflict
%   all_compat(R)    : every operand-level verdict is Compatible
%
% Mutual exclusion (e.g., all_compat AND has_conflict cannot both hold)
% follows from problem-file construction, not from axioms here.
%
% Note: `or` and `xone` composition are NOT encoded in this file.  The
% paper's §4.3 satisfying-set semantics handles those connectives via
% cross-disjunct decomposition (Proposition 4), which requires σ-level
% reasoning over requests rather than per-operand summary predicates.
% ==========================================================================
% --------------------------------------------------------------------------
% AND composition (Strong Kleene conjunction, Corollary 3)
%   Compatible : every operand pair Compatible
%   Conflict   : at least one operand pair Conflict
%   Unknown    : otherwise (some Unknown, no Conflict)
% --------------------------------------------------------------------------
fof(rule_and_compatible, axiom,
    ![R]:
      (rule_and(R) = compatible <=> all_compat(R))).

fof(rule_and_conflict, axiom,
    ![R]:
      (rule_and(R) = conflict <=> has_conflict(R))).

fof(rule_and_unknown, axiom,
    ![R]:
      (rule_and(R) = unknown <=>
        (~all_compat(R) & ~has_conflict(R)))).

fof(rule_and_total, axiom,
    ![R]:
      (rule_and(R) = compatible |
       rule_and(R) = conflict |
       rule_and(R) = unknown)).

% ==========================================================================
% Verdict-value distinctness (so the prover can do case analysis)
% ==========================================================================
fof(verdicts_distinct_cf_cp, axiom, conflict   != compatible).
fof(verdicts_distinct_cf_un, axiom, conflict   != unknown).
fof(verdicts_distinct_cp_un, axiom, compatible != unknown).
"""


def generate_compose000() -> str:
    name = "COMPOSE000-0.ax"
    note = (
        "Logically independent of DENOT000-0.ax: COMPOSE works over\n"
        "rule-level summary predicates, not directly over verdict_*/2.\n"
        "Problem files using `and` composition must:\n"
        "  1. include the foundation axiom files in order:\n"
        "       Axioms/KGE000-0.ax\n"
        "       Axioms/DENOT000-0.ax\n"
        "       Axioms/COMPOSE000-0.ax\n"
        "       Axioms/<resource>.ax\n"
        "  2. emit per-rule bridge axioms linking has_conflict/1 and\n"
        "     all_compat/1 to the operand-level verdicts of that rule.\n"
        "     Example for a 2-operand rule R1:\n"
        "       has_conflict(r1) <=> (verdict_conflict(c1, c1') |\n"
        "                             verdict_conflict(c2, c2'))\n"
        "       all_compat(r1)   <=> (verdict_compatible(c1, c1') &\n"
        "                             verdict_compatible(c2, c2'))\n"
        "  3. for partial-overlap cases (operand sets neither equal nor\n"
        "     disjoint), use Proposition 4 case (iii): rule-level\n"
        "     Conflict iff some shared operand has atomic-level Conflict.\n"
        "     Encode the bridge over only the shared operands.\n"
        "\n"
        "`or` and `xone` audit requires COMPOSE001-0.ax (satisfying-set\n"
        "semantics, σ-level), not yet authored. Deferred to extended work.\n"
        "No axiom file self-includes this file."
    )
    header = AXHeader(
        file     = name,
        domain   = "kb",
        title    = "Strong Kleene `and` composition for rule-level verdicts",
        version  = VERSION,
        english  = (
            "Encodes Corollary 3 (Operand-wise composition for `and`).\n"
            "Strong Kleene conjunction over per-operand verdicts:\n"
            "  Compatible iff every operand pair Compatible;\n"
            "  Conflict   iff any operand pair Conflict;\n"
            "  Unknown    otherwise.\n"
            "rule_and is total (returns one of compatible, conflict,\n"
            "unknown) and the three verdict values are distinct.\n"
            "`or` and `xone` are not encoded here: the paper's §4.3\n"
            "satisfying-set semantics handles them via cross-disjunct\n"
            "decomposition (Proposition 4), requiring σ-level reasoning.\n"
            "See COMPOSE001-0.ax (deferred) for σ-level encoding."
        ),
        refs     = ["kgc2026"],
        comments = _ax_comment(
            COMPOSE000_BODY,
            "4 rule_and + 3 distinct = 7 formulae",
            note,
        ),
        fof_text = COMPOSE000_BODY,
    ).render()
    return header + "\n" + COMPOSE000_BODY


def main():
    parser = argparse.ArgumentParser(
        description="Generate COMPOSE000-0.ax (and-only Strong Kleene)"
    )
    parser.add_argument("--out-dir",
                        default="Problems/ODRL/KGConstraints/Axioms")
    parser.add_argument("--stdout", action="store_true")
    args = parser.parse_args()

    content = generate_compose000()
    actual = content.count("fof(")
    ok = "✓" if actual == EXPECTED_COUNT else "✗"

    if args.stdout:
        print(content)
        print(f"\n{actual} formulae (expected {EXPECTED_COUNT}) {ok}",
              file=sys.stderr)
        return

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "COMPOSE000-0.ax"
    path.write_text(content, encoding="utf-8")
    print(f"Written : {path}  ({actual} formulae, expected {EXPECTED_COUNT}) {ok}")


if __name__ == "__main__":
    main()