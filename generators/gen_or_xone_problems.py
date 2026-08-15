"""
gen_or_xone_problems.py
=======================

Generates KGC710-712 (or-composition audit) and, when KGC713 is added,
xone composition audit problems from problem_data_or_composition.py.

Usage:
    uv run Generators/KGConstraints/gen_or_xone_problems.py
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from problem_data_or_composition import PROBLEMS
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
        description="Generate KGC710-713 (or/xone composition audit)."
    )
    parser.add_argument("--out-dir",    default=DEFAULT_OUT)
    parser.add_argument("--axioms-dir", default=DEFAULT_AXIOMS)
    args = parser.parse_args()

    out_dir    = Path(args.out_dir)
    axioms_dir = Path(args.axioms_dir)

    vocab = collect_vocabulary(axioms_dir)
    print(f"Vocabulary: {len(vocab)} constants from "
          f"GN000/DPV000/BCP47000.")

    for p in PROBLEMS:
        validate_problem_constants(p, vocab)

    policies_dir = out_dir / "Policies"

    written = []
    for p in PROBLEMS:
        p_path   = write_fof_problem(p, out_dir)
        s_path   = write_smt2_problem(p, out_dir)
        ttl_path = write_ttl_policy(p, policies_dir)
        written.append((p, p_path, s_path, ttl_path))

    print(f"\nGenerated {len(written)} or/xone composition problems:")
    for p, p_path, s_path, ttl_path in written:
        print(f"  {p['id']} ({p['verdict']})")
        print(f"    .p     {p_path}")
        print(f"    .smt2  {s_path}")
        print(f"    .ttl   {ttl_path}")


if __name__ == "__main__":
    main()