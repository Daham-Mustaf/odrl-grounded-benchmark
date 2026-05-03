"""
gen_motivating.py
=================
Generates the three motivating-example problems (KGC300, KGC301, KGC302)
from problem_data_motivating.py, plus their .smt2 and .ttl companions.

Output:
    Problems/ODRL/KGConstraints/Conflict/KGC30x-1.p
    Problems/ODRL/KGConstraints/Conflict/KGC30x-1.smt2
    Problems/ODRL/KGConstraints/Policies/KGC30x-policy.ttl

Usage:
    uv run Generators/KGConstraints/gen_motivating.py
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from problem_data_motivating import PROBLEMS
from writers import (
    write_fof_problem,
    write_smt2_problem,
    write_ttl_policy,
    collect_vocabulary,
    validate_problem_constants,
)

DEFAULT_OUT     = "Problems/ODRL/KGConstraints"
DEFAULT_AXIOMS  = "Problems/ODRL/KGConstraints/Axioms"


def main():
    parser = argparse.ArgumentParser(
        description="Generate the motivating-example problems "
                    "(KGC300, KGC301, KGC302)."
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

    print(f"\nGenerated {len(written)} problems:")
    for p, p_path, s_path, ttl_path in written:
        print(f"  {p['id']} ({p['verdict']:>10s})")
        print(f"    .p     {p_path}")
        print(f"    .smt2  {s_path}")
        print(f"    .ttl   {ttl_path}")


if __name__ == "__main__":
    main()