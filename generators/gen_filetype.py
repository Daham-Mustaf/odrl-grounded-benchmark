"""
gen_filetype.py
===============
Generates the four EU File Type benchmark problems, each as two
satisfiability queries, together with the corresponding ODRL policies
and expected verdict reports.

For each problem:
    problems/verdict/<id>-1.p     R + B + W
    problems/verdict/<id>-1.smt2  R + B + W
    problems/verdict/<id>-2.p     R + B + not W
    problems/verdict/<id>-2.smt2  R + B + not W
    cases/<id>.ttl                policies + expected report

The four cases cover equality, declared distinctness, isAnyOf, and neq
at the nominal sort of odrl:fileFormat.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from problem_data_filetype import PROBLEMS
from writers import (
    write_problem,
    expected_verdict,
    collect_vocabulary,
    validate_problem_constants,
)

DEFAULT_OUT    = "problems"
DEFAULT_AXIOMS = "problems/axioms"
DEFAULT_CASES  = "cases"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate the motivating-example problems."
    )
    parser.add_argument("--out-dir", default=DEFAULT_OUT)
    parser.add_argument("--axioms-dir", default=DEFAULT_AXIOMS)
    parser.add_argument("--cases-dir", default=DEFAULT_CASES)
    parser.add_argument("--check-only", action="store_true",
                        help="Validate without writing anything.")
    args = parser.parse_args()

    out_dir    = Path(args.out_dir)
    axioms_dir = Path(args.axioms_dir)
    cases_dir  = Path(args.cases_dir)

    # Every gn_/dpv_/bcp_ constant a problem names must be declared by a
    # resource axiom file.  Refuses to write otherwise.
    vocab = collect_vocabulary(axioms_dir)
    if not vocab:
        print(f"ERROR: no constants found in {axioms_dir}.  Generate the "
              f"resource axiom files first.", file=sys.stderr)
        return 1
    print(f"Vocabulary: {len(vocab)} constants.")

    for p in PROBLEMS:
        validate_problem_constants(p, vocab)

    if args.check_only:
        print("Validation passed; nothing written.")
        return 0

    print()
    for p in PROBLEMS:
        paths = write_problem(p, out_dir, cases_dir)
        print(f"{p['id']}  {p['left_operand']:9s} {p['sort']}  "
              f"q1={p['expected_q1']:14s} q2={p['expected_q2']:14s} "
              f"-> {expected_verdict(p)}")
        for path in paths:
            print(f"    {path}")

    print(f"\n{len(PROBLEMS)} problems, "
          f"{sum(1 for p in PROBLEMS if not p.get('ungrounded')) * 4} query "
          f"files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())