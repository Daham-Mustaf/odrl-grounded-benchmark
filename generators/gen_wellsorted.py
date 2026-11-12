"""
gen_wellsorted.py
=================

Generates the drafting-time check problems and runs it.

No queries are written.  Well-sortedness is decided by the signature, and
for a Logical Constraint by compile.check_tree as well, so a rejected
constraint never reaches a prover.  Each problem produces one case file
recording the constraint and the expected outcome, with the reason when it
is rejected.

Usage:

    uv run generators/gen_wellsorted.py
"""

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from compile import SET_OPERATORS, IllSorted, check_tree
from problem_data_wellsorted import PROBLEMS
from signature import is_well_sorted
from targets import with_targets
from writers import GENERATED_HEADER

DEFAULT_CASES = "cases"

# The sort a binding declares, as the binding vocabulary names it.  These
# are bind: rather than vrep: because a sort is a property of the binding
# and exists before any evaluation; the report vocabulary only refers to
# them.
SORT_TERM = {
    "nom": "bind:nom",
    "tax": "bind:tax",
    "mer": "bind:mer",
}

# Two sentences at the head of every case file.  A reader opening one of
# these should not have to know the generator to see what the file is.
_HEADER = """\
# A check made while a policy is drafted: whether the operator applies to the
# kind of value the policy gives.  The answer comes from the operator and the
# kind of value alone, so no vocabulary was opened and no prover was run.
#
# A rejected policy is not false.  It asks a question the vocabulary cannot
# answer: isA over a vocabulary that arranges nothing in kinds has nothing to
# test, and an evaluator that answered yes or no would be inventing an answer.
"""

# The same for an xone, whose operators all fit the kind of value.
_XONE_HEADER = """\
# A check made while a policy is drafted: whether a choice of exactly one
# combines an isAllOf constraint.  The answer comes from the policy's
# constraints alone, so no vocabulary was opened and no prover was run.
#
# A rejected policy is not false.  Exactly one asks every other constraint
# to fail, and the failure of an isAllOf constraint is not one constraint:
# any one of its values may be missing.
"""


def check(p: dict) -> tuple[bool, str]:
    """Whether the problem's constraint is well sorted, and the reason when
    it is not.  A Constraint is checked against the signature.  For a Logical
    Constraint each constraint it combines is checked so, and then the tree
    goes through compile.check_tree, as it would on its way to a query."""
    if "tree" not in p:
        return is_well_sorted(p["operator"], p["sort"], p["arity"])
    for item in p["tree"]:
        for c in getattr(item, "alts", (item,)):
            arity = "n" if c.operator in SET_OPERATORS else len(c.values)
            ok, why = is_well_sorted(c.operator, p["sort"], arity)
            if not ok:
                return ok, why
    try:
        check_tree(p["tree"])
    except IllSorted as e:
        return False, str(e)
    return True, ""


def case_ttl(p: dict, accepted: bool, reason: str) -> str:
    """One case file: the constraint, and what the check says about it."""
    pid = p["id"]
    lines = [
        GENERATED_HEADER,
        _XONE_HEADER if p["operator"] == "xone" else _HEADER,
        with_targets(p["ttl"]),
        "",
        "### Expected result " + "#" * 55,
        "",
        f"drk:{pid}-report a vrep:WellSortednessReport ;",
        f'    dcterms:identifier "{pid}" ;',
        f"    vrep:constraint {p['constraint']} ;",
        f"    vrep:binding <{p['binding']}> ;",
    ]
    # What a reader sees is the problem's own wording; the check only
    # decides whether the constraint is accepted, and main() checks that
    # against the problem's expectation.
    summary = p["summary"]
    comment = p["reason"]
    lines.append(f'    dcterms:description """{summary}"""@en ;')
    lines.append(f'    rdfs:comment """{comment}"""@en ;')
    lines.append(f"    vrep:wellSorted {'true' if accepted else 'false'} .")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate and run the drafting-time check.")
    parser.add_argument("--cases-dir", default=DEFAULT_CASES)
    args = parser.parse_args()

    cases_dir = Path(args.cases_dir)
    cases_dir.mkdir(parents=True, exist_ok=True)

    print(f"{'id':8} {'operand':9} {'operator':10} {'sort':5} "
          f"{'result':9} check")

    failures = 0
    start = time.perf_counter()
    for p in PROBLEMS:
        accepted, reason = check(p)
        mark = "ok" if accepted == p["accepted"] else "MISMATCH"
        if accepted != p["accepted"]:
            failures += 1
        (cases_dir / f"{p['id']}.ttl").write_text(
            case_ttl(p, accepted, reason), encoding="utf-8")
        print(f"{p['id']:8} {p['left_operand']:9} {p['operator']:10} "
              f"{p['sort']:5} "
              f"{'accepted' if accepted else 'rejected':9} {mark}")
        if reason:
            print(f"{'':35}{reason}")

    elapsed = (time.perf_counter() - start) * 1000
    print(f"\n{len(PROBLEMS) - failures}/{len(PROBLEMS)} as expected, "
          f"{elapsed:.1f} ms, no prover invoked and no resource opened.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())