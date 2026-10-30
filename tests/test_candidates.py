"""
test_candidates.py
==================
Regression tests for the candidates of the witness.

Definition Witness lets the value of a use be any concept of the operand's
vocabulary, so a pair query ranges over every concept of the vocabulary and
not over the concepts the two policies name.  Three pairs that only a concept
neither policy names can settle:

  1. KGC404: isA research and development against isA non-commercial
     purpose.  Neither policy names non-commercial research, which DPV
     places below both categories.
  2. neq German against neq French under the language declarations.  Any of
     the other thirteen languages is a use that satisfies both.
  3. neq marketing against neq scientific research under the purposes
     declarations, which declare every pair of purposes distinct, not only
     the pair the policies name.  Any other purpose is a use.

Each is expected Compatible, by both provers on both encodings.  The tests
are not cases: nothing here is written under cases/ or problems/.

    uv run tests/test_candidates.py

Exit 1 if a pair is not Compatible, or if its witness does not range
over a concept that neither policy names.
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "generators"))

from compile import Constraint
from tree_expand import expand_tree
from writers import write_fof, write_smt2

import problem_data_dpv
import problem_data_motivating

LIMIT = 120


def entry(module, cid):
    return next(p for p in module.PROBLEMS if p["id"] == cid)


def c(op, value, side="offer"):
    return Constraint(op, (value,), side)


def kgc404_non_commercial():
    p = dict(entry(problem_data_dpv, "KGC404"))
    p.update(
        id="TEST404", subdir="test",
        name="purpose, isA dpv:R&D against isA dpv:NonCommercialPurpose",
        tree=[c("isA", problem_data_dpv.RND),
              c("isA", problem_data_dpv.NCP, side="request")])
    return p, "dpv_non_commercial_research"


def neq_german_neq_french():
    p = dict(entry(problem_data_motivating, "KGC300"))
    p.update(
        id="TEST300", subdir="test",
        name="language, neq bcp:de against neq bcp:fr",
        tree=[c("neq", problem_data_motivating.DE),
              c("neq", problem_data_motivating.FR, side="request")])
    return p, "bcp_en"


def neq_marketing_neq_research():
    p = dict(entry(problem_data_dpv, "KGC318"))
    p.update(
        id="TEST318", subdir="test",
        name="purpose, neq dpv:Marketing against neq dpv:ScientificResearch, "
             "purposes declared distinct",
        tree=[c("neq", problem_data_dpv.MK),
              c("neq", problem_data_dpv.SR, side="request")])
    return p, "dpv_academic_research"


TESTS = [kgc404_non_commercial, neq_german_neq_french, neq_marketing_neq_research]


def vampire(path):
    r = subprocess.run(["vampire", "--include", str(ROOT / "problems"),
                        "--mode", "casc", "--time_limit", str(LIMIT), str(path)],
                       capture_output=True, text=True, timeout=LIMIT + 60)
    m = re.search(r"SZS status (\w+)", r.stdout)
    return {"Satisfiable": "sat", "CounterSatisfiable": "sat",
            "Unsatisfiable": "unsat", "Theorem": "unsat",
            "ContradictoryAxioms": "unsat"}.get(m and m.group(1), "no-status")


def z3(path):
    r = subprocess.run(["z3", f"-T:{LIMIT}", str(path)], capture_output=True,
                       text=True, timeout=LIMIT + 60)
    return r.stdout.split("\n", 1)[0].strip() or "no-output"


def verdict(q1, q2):
    if q1 == "unsat":
        return "Incompatible"
    if q2 == "unsat":
        return "Compatible"
    return "Unknown" if (q1, q2) == ("sat", "sat") else f"undecided({q1},{q2})"


def main() -> int:
    failures = 0
    with tempfile.TemporaryDirectory() as tmp:
        for build in TESTS:
            p, third = build()
            p["expected_q1"], p["expected_q2"] = "Satisfiable", "Unsatisfiable"
            q = expand_tree(p)
            names = set(q["named_constants"])
            ranges_wide = third in q["fof_witness"] and third in q["smt2_witness"] \
                and third not in names
            got = {}
            for prover, write, run in (("vampire", write_fof, vampire),
                                       ("z3", write_smt2, z3)):
                got[prover] = [run(write(q, n, Path(tmp))) for n in (1, 2)]
            ok = ranges_wide and all(verdict(*s) == "Compatible"
                                     for s in got.values())
            failures += 0 if ok else 1
            print(f"{'ok  ' if ok else 'FAIL'} {p['name']}: "
                  + "; ".join(f"{k} {v[0]}/{v[1]} {verdict(*v)}"
                              for k, v in got.items())
                  + f"; witness ranges over {third}: {ranges_wide}")
    print(f"{len(TESTS) - failures} of {len(TESTS)} pass")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
