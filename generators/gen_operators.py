"""
gen_operators.py
================
Generates the per-operator audit grid problems (KGC400–KGC442) from
problem_data_operators.py, plus their .smt2 and .ttl companions.

The grid covers every monotone operator in the single-valued fragment
(eq, isA, isPartOf, hasPart, isAnyOf) against every verdict (Conflict,
Compatible, Unknown). Together with the motivating-example problems
(KGC300-302), this forms the complete Theorem 1 audit suite.

Output:
    Problems/ODRL/KGConstraints/Conflict/KGC4xx-1.p
    Problems/ODRL/KGConstraints/Conflict/KGC4xx-1.smt2
    Problems/ODRL/KGConstraints/Policies/KGC4xx-policy.ttl

Usage:
    uv run Generators/KGConstraints/gen_operators.py
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from problem_data_operators import PROBLEMS
from writers import (
    write_fof_problem,
    write_smt2_problem,
    write_ttl_policy,
    collect_vocabulary,
    validate_problem_constants,
)

DEFAULT_OUT    = "Problems/ODRL/KGConstraints"
DEFAULT_AXIOMS = "Problems/ODRL/KGConstraints/Axioms"


def main():
    parser = argparse.ArgumentParser(
        description="Generate the per-operator audit grid problems "
                    "(KGC400-KGC442)."
    )
    parser.add_argument("--out-dir", default=DEFAULT_OUT,
                        help=f"Output root (default: {DEFAULT_OUT})")
    parser.add_argument("--axioms-dir", default=DEFAULT_AXIOMS,
                        help=f"Axioms directory for vocabulary check "
                             f"(default: {DEFAULT_AXIOMS})")
    args = parser.parse_args()

    out_dir    = Path(args.out_dir)
    axioms_dir = Path(args.axioms_dir)

    # No-hallucination check: every (gn|dpv|bcp)_* constant referenced
    # in any problem must exist in the included axiom files.
    vocab = collect_vocabulary(axioms_dir)
    if not vocab:
        print(f"WARNING: no vocabulary found in {axioms_dir}.  "
              f"Did you generate the resource axiom files first?",
              file=sys.stderr)
    else:
        print(f"Vocabulary: {len(vocab)} constants from "
              f"GN000/DPV000/BCP47000.")
    for p in PROBLEMS:
        validate_problem_constants(p, vocab)

    # Generate
    policies_dir = out_dir / "Policies"
    written = []
    for p in PROBLEMS:
        p_path   = write_fof_problem(p, out_dir)
        s_path   = write_smt2_problem(p, out_dir)
        ttl_path = write_ttl_policy(p, policies_dir)
        written.append((p, p_path, s_path, ttl_path))

    # Group output by operator for readability
    print(f"\nGenerated {len(written)} problems:")
    by_op = {}
    for entry in written:
        p = entry[0]
        # Extract operator from id: KGC4{op}{verdict} -> op digit
        op_digit = p["id"][4]
        by_op.setdefault(op_digit, []).append(entry)

    op_names = {
        "0": "eq",
        "1": "isA",
        "2": "isPartOf",
        "3": "hasPart",
        "4": "isAnyOf",
    }

    for op_digit in sorted(by_op):
        print(f"\n  {op_names.get(op_digit, '?')}:")
        for p, p_path, s_path, ttl_path in by_op[op_digit]:
            note = ""
            if p["status_fof"] == "CounterSatisfiable" and \
               p["verdict"] == "Conflict":
                note = "  [expected incompleteness]"
            print(f"    {p['id']} ({p['verdict']:>10s}){note}")
            print(f"      .p     {p_path}")
            print(f"      .smt2  {s_path}")
            print(f"      .ttl   {ttl_path}")


if __name__ == "__main__":
    main()