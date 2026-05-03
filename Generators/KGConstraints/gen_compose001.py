"""
gen_compose001.py
=================

Generates COMPOSE001-0.ax: rule-level composition for the `or`
fragment via cross-disjunct decomposition.

Encodes Proposition 3 of the paper (Section 4.3, "Cross-disjunct
decomposition"): for constraint sets in the and/or fragment with
DNF expansions or(d_1, ..., d_n) and or(d'_1, ..., d'_m), rule-level
Conflict iff every cross-pair (d_i, d'_j) has disjunct-level Conflict;
Compatible iff some cross-pair has Compatible; Unknown otherwise.

This file is logically independent of COMPOSE000-0.ax: where COMPOSE000
aggregates per-operand atomic verdicts via Strong Kleene `and` for
single-disjunct rules, COMPOSE001 aggregates per-disjunct verdicts via
cross-pair quantification for multi-disjunct rules. They share the
verdict-value sort {compatible, conflict, unknown} and reuse the
distinctness axioms of COMPOSE000.

Output:
    Problems/ODRL/KGConstraints/Axioms/COMPOSE001-0.ax

Usage:
    uv run Generators/KGConstraints/gen_compose001.py
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from header import AXHeader, _ax_comment

VERSION = "1.0"
EXPECTED_COUNT = 4

COMPOSE001_BODY = """\
% ==========================================================================
% Cross-disjunct decomposition for `or` composition (Proposition 3)
%
% After DNF expansion, a constraint set CS = or(d_1, ..., d_n) where
% each d_i is a conjunction of atomic constraints. Per Proposition 3
% (paper Section 4.3), rule-level Conflict between CS and CS' holds
% iff every cross-pair (d_i, d'_j) has disjunct-level Conflict.
%
% Predicates expected from problem files:
%   has_disjunct(R, D)        : D is a disjunct of rule R's DNF
%   disjunct_conflict(D, D')  : disjunct-pair (D, D') has atomic-level
%                               Conflict at some shared operand.  Problem
%                               files instantiate this from the atomic
%                               verdicts via the same Strong Kleene `and'
%                               aggregation as in COMPOSE000.
%   disjunct_compat(D, D')    : disjunct-pair has atomic-level Compatible
%                               (every shared operand Compatible).
%
% rule_or(R, R') is total in {compatible, conflict, unknown}; the three
% verdict values are distinct (axioms in COMPOSE000-0.ax, reused).
%
% Both CS and CS' are assumed to have at least one disjunct: a
% constraint set with at least one constraint always has at least one
% DNF disjunct.  This non-emptiness is asserted explicitly in the
% rule_or_conflict axiom to prevent vacuous Conflict on empty disjunct
% sets.
% ==========================================================================

% --------------------------------------------------------------------------
% OR composition (cross-disjunct decomposition, Proposition 3)
%   Conflict   : every cross-pair has Conflict (and both rules have
%                at least one disjunct).
%   Compatible : some cross-pair has Compatible.
%   Unknown    : otherwise (no Compatible, at least one Unknown).
% --------------------------------------------------------------------------

fof(rule_or_conflict, axiom,
    ![R, RP] :
      ( rule_or(R, RP) = conflict
    <=> ( ( ?[D]  : has_disjunct(R, D) )
        & ( ?[DP] : has_disjunct(RP, DP) )
        & ( ![D, DP] :
              ( ( has_disjunct(R, D) & has_disjunct(RP, DP) )
             => disjunct_conflict(D, DP) ) ) ) ) ).

fof(rule_or_compatible, axiom,
    ![R, RP] :
      ( rule_or(R, RP) = compatible
    <=> ?[D, DP] :
          ( has_disjunct(R, D)
          & has_disjunct(RP, DP)
          & disjunct_compat(D, DP) ) ) ).

fof(rule_or_unknown, axiom,
    ![R, RP] :
      ( rule_or(R, RP) = unknown
    <=> ( rule_or(R, RP) != compatible
        & rule_or(R, RP) != conflict ) ) ).

fof(rule_or_total, axiom,
    ![R, RP] :
      ( rule_or(R, RP) = compatible
      | rule_or(R, RP) = conflict
      | rule_or(R, RP) = unknown ) ).
"""


def generate_compose001() -> str:
    name = "COMPOSE001-0.ax"
    note = (
        "Logically independent of COMPOSE000-0.ax but reuses the\n"
        "verdict-value distinctness axioms (verdicts_distinct_*).\n"
        "Problem files using `or` composition must:\n"
        "  1. include the foundation axiom files in order:\n"
        "       Axioms/KGE000-0.ax\n"
        "       Axioms/DENOT000-0.ax\n"
        "       Axioms/COMPOSE000-0.ax    (verdict-value distinctness)\n"
        "       Axioms/COMPOSE001-0.ax\n"
        "       Axioms/<resource>.ax\n"
        "  2. emit per-rule disjunct membership axioms:\n"
        "       has_disjunct(r1, d1).  has_disjunct(r1, d2).\n"
        "       has_disjunct(r2, d1p).\n"
        "     plus closure axioms ruling out unintended disjuncts:\n"
        "       ![D]: (has_disjunct(r1, D) <=> (D=d1 | D=d2)).\n"
        "  3. emit disjunct-pair verdict bridges from the atomic\n"
        "     operand-level verdicts. For each cross-pair (D, D'):\n"
        "       disjunct_conflict(D, D') <=> some shared-operand\n"
        "         verdict_conflict;\n"
        "       disjunct_compat(D, D')   <=> every shared-operand\n"
        "         verdict_compatible.\n"
        "  4. assert distinctness among disjunct names\n"
        "     (distinct(d1, d2, d1p, ...)).\n"
        "\n"
        "xone-Conflict reduces to or-Conflict over the same disjuncts\n"
        "(paper Section 4.3 footnote): for xone(c_1, ..., c_n) vs c',\n"
        "rule-level Conflict iff every (c_k, c') has Conflict, which is\n"
        "exactly rule_or(xone-rule, single-rule) = conflict under the\n"
        "DNF expansion of xone.  No additional axioms are required.\n"
        "\n"
        "No axiom file self-includes this file."
    )
    header = AXHeader(
        file     = name,
        domain   = "kb",
        title    = "Cross-disjunct decomposition for `or` composition",
        version  = VERSION,
        english  = (
            "Encodes Proposition 3 (Cross-disjunct decomposition).\n"
            "Rule-level verdict for `or`-composed (DNF-expanded)\n"
            "constraint sets:\n"
            "  Conflict   iff every cross-pair has disjunct Conflict;\n"
            "  Compatible iff some cross-pair has disjunct Compatible;\n"
            "  Unknown    otherwise.\n"
            "rule_or is total in {compatible, conflict, unknown};\n"
            "verdict-value distinctness is provided by COMPOSE000-0.ax.\n"
            "xone-Conflict reduces to or-Conflict over the same\n"
            "disjuncts and requires no additional axioms."
        ),
        refs     = ["kgc2026"],
        comments = _ax_comment(
            COMPOSE001_BODY,
            "4 rule_or axioms (conflict, compatible, unknown, total)",
            note,
        ),
        fof_text = COMPOSE001_BODY,
    ).render()
    return header + "\n" + COMPOSE001_BODY


def main():
    parser = argparse.ArgumentParser(
        description="Generate COMPOSE001-0.ax (or-handling)"
    )
    parser.add_argument("--out-dir",
                        default="Problems/ODRL/KGConstraints/Axioms")
    parser.add_argument("--stdout", action="store_true")
    args = parser.parse_args()
    content = generate_compose001()
    actual = content.count("fof(")
    ok = "✓" if actual == EXPECTED_COUNT else "✗"
    if args.stdout:
        print(content)
        print(f"\n{actual} formulae (expected {EXPECTED_COUNT}) {ok}",
              file=sys.stderr)
        return
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "COMPOSE001-0.ax"
    path.write_text(content, encoding="utf-8")
    print(f"Written : {path}  ({actual} formulae, expected {EXPECTED_COUNT}) {ok}")


if __name__ == "__main__":
    main()