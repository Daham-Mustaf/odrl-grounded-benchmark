"""
gen_wellsorted.py
=================
Generates the drafting-time check problems and runs it.

No queries are written.  Well-sortedness is decided by the signature alone,
so a rejected constraint never reaches a prover.  Each problem produces one
case file recording the constraint and the expected outcome, with the reason
when it is rejected.

Usage:
    uv run generators/gen_wellsorted.py
"""

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from problem_data_wellsorted import PROBLEMS
from signature import is_well_sorted

DEFAULT_CASES = "cases"


def case_ttl(p: dict, accepted: bool, reason: str) -> str:
    pid = p["id"]
    lines = [
        p["ttl"],
        "",
        "### Expected result " + "#" * 55,
        "",
        f"drk:{pid}-report a vrep:WellSortednessReport ;",
        f'    dcterms:identifier "{pid}" ;',
        f"    vrep:constraint kgc:{pid}-offer-c1 ;",
        f"    vrep:leftOperand odrl:{p['left_operand']} ;",
        f"    vrep:sort vrep:{p['sort']} ;",
        f"    vrep:resource <{p['resource']}> ;",
    ]
    if accepted:
        lines.append("    vrep:wellSorted true .")
    else:
        lines.append("    vrep:wellSorted false ;")
        lines.append(f'    rdfs:comment """{reason}"""@en .')
    lines.append("")
    lines.append("# No query is built for a rejected constraint, and none is")
    lines.append("# built to accept one: the check reads the signature and")
    lines.append("# nothing else.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate and run the drafting-time check.")
    parser.add_argument("--cases-dir", default=DEFAULT_CASES)
    args = parser.parse_args()
    cases_dir = Path(args.cases_dir)
    cases_dir.mkdir(parents=True, exist_ok=True)

    print(f"{'id':8} {'operand':9} {'operator':10} {'sort':5} {'result':9} check")
    failures = 0
    start = time.perf_counter()

    for p in PROBLEMS:
        accepted, reason = is_well_sorted(p["operator"], p["sort"], p["arity"])
        mark = "ok" if accepted == p["accepted"] else "MISMATCH"
        if accepted != p["accepted"]:
            failures += 1
        (cases_dir / f"{p['id']}.ttl").write_text(
            case_ttl(p, accepted, reason), encoding="utf-8")
        print(f"{p['id']:8} {p['left_operand']:9} {p['operator']:10} "
              f"{p['sort']:5} {'accepted' if accepted else 'rejected':9} {mark}")
        if reason:
            print(f"{'':35}{reason}")

    elapsed = (time.perf_counter() - start) * 1000
    print(f"\n{len(PROBLEMS) - failures}/{len(PROBLEMS)} as expected, "
          f"{elapsed:.1f} ms, no prover invoked and no resource opened.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())