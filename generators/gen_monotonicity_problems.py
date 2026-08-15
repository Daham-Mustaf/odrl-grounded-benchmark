"""
gen_monotonicity_problems.py
============================
Generates the Proposition 1 (Monotonicity) audit problems from
problem_data_monotonicity.py.

Usage:
    uv run Generators/KGConstraints/gen_monotonicity_problems.py
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from problem_data_monotonicity import PROBLEMS
from writers import (
    write_fof_problem,
    write_smt2_problem,
    write_ttl_policy,
)


DEFAULT_OUT    = "Problems/ODRL/KGConstraints"
DEFAULT_AXIOMS = "Problems/ODRL/KGConstraints/Axioms"


def main():
    parser = argparse.ArgumentParser(
        description="Generate the Proposition 1 (Monotonicity) audit problems."
    )
    parser.add_argument("--out-dir",    default=DEFAULT_OUT)
    parser.add_argument("--axioms-dir", default=DEFAULT_AXIOMS)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    
    # Note: monotonicity problems use problem-local concept constants
    # (e.g., gn_germany, gn_france, gn_spain) that may not appear in
    # the standard vocabulary collected from GN000/DPV000/BCP47000.
    # The vocabulary validator can be skipped or extended for these.
    
    policies_dir = out_dir / "Policies"
    written = []
    for p in PROBLEMS:
        p_path   = write_fof_problem(p, out_dir)
        s_path   = write_smt2_problem(p, out_dir)
        ttl_path = write_ttl_policy(p, policies_dir)
        written.append((p, p_path, s_path, ttl_path))

    print(f"\nGenerated {len(written)} Proposition 1 (Monotonicity) problems:")
    for p, p_path, s_path, ttl_path in written:
        print(f"  {p['id']} ({p['verdict']})")
        print(f"    .p     {p_path}")
        print(f"    .smt2  {s_path}")
        print(f"    .ttl   {ttl_path}")


if __name__ == "__main__":
    main()