"""
check_policies.py
=================
Two checks on what the policies of a case ask, reported by case ID.

  a. Each policy alone admits a use.  The resource statements, the case's
     declarations and the witness condition of that one policy are
     satisfiable together (Z3).  A policy that no use can satisfy would make
     every verdict over it Incompatible for a reason that has nothing to do
     with the other policy.  The query is built the way the case's own
     queries are: the same tree, cut to one policy, through expand_tree and
     write_smt2.

  b. Both policies of a case have the same action and the same target.  A
     comparison of two policies that act on different things says nothing.

Cases with no query (ill sorted, or a value that does not ground) are
skipped for a: there is no witness to build.  A case with one policy is
skipped for b.

    uv run generators/check_policies.py [--cases cases] [-v]

Exit 1 if any case fails either check.
"""

import argparse
import importlib
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from rdflib import Graph, Namespace, RDF
from rdflib.namespace import DCTERMS

from compile import Constraint
from tree_expand import expand_tree, constants_of_tree, _map_item
from writers import write_smt2

ODRL = Namespace("http://www.w3.org/ns/odrl/2/")

MODULES = ["problem_data_motivating", "problem_data_geonames",
           "problem_data_dpv", "problem_data_dpvloc",
           "problem_data_filetype", "problem_data_consent",
           "problem_data_tom", "problem_data_bcp47"]


# One concept of the resource that no constraint names.  A policy that
# excludes (neq, isNoneOf) is met by it; the resource has more concepts than
# any case names, and says nothing about this one, so nothing is assumed.
OTHER = "other_concept"


def side_of(item) -> str:
    c = item if isinstance(item, Constraint) else item.alts[0]
    return c.side


def alone(p: dict, side: str) -> dict:
    """The problem with only one policy's constraints.

    The constants of the other policy stay declared and stay in the
    statement filter, because the declarations the case carries may name
    them.  The witness also gets OTHER as a candidate, which a pair query
    gets from the second policy.
    """
    grounding = p.get("grounding")
    mapped = (lambda items: [_map_item(i, grounding) for i in items]) \
        if grounding else (lambda items: list(items))
    mine = [i for i in p["tree"] if side_of(i) == side]
    kept = constants_of_tree(mapped(mine))
    every = constants_of_tree(mapped(p["tree"]))
    q = dict(p)
    q["tree"] = mine
    q["witness_candidates"] = [OTHER]
    q["extra_constants"] = [c for c in every if c not in kept] \
        + [c for c in p.get("extra_constants", []) if c not in kept] + [OTHER]
    return q


def z3_status(path: Path, seconds: int) -> str:
    try:
        out = subprocess.run(["z3", f"-T:{seconds}", str(path)],
                             capture_output=True, text=True,
                             timeout=seconds + 10).stdout
    except subprocess.TimeoutExpired:
        return "timeout"
    return out.split("\n", 1)[0].strip() or "no-output"


def admits_a_use(problems, seconds: int):
    """(checked, skipped, failures); a failure is (case id, side, status)."""
    checked, skipped, failures = [], [], []
    with tempfile.TemporaryDirectory() as tmp:
        for p in problems:
            if p.get("ungrounded") or "tree" not in p:
                skipped.append(p["id"])
                continue
            for side in ("offer", "request"):
                q = expand_tree(alone(p, side))
                q = dict(q, id=p["id"], subdir="alone", name=p["name"])
                path = write_smt2(q, 1, Path(tmp) / side)
                status = z3_status(path, seconds)
                checked.append((p["id"], side, status))
                if status != "sat":
                    failures.append((p["id"], side, status))
    return checked, skipped, failures


def local(x) -> str:
    return str(x).rsplit("/", 1)[-1].rsplit("#", 1)[-1]


def acts_alike(cases_dir: Path):
    """(cases compared, failures); a failure is (case id, what differs)."""
    compared, failures = 0, []
    for f in sorted(cases_dir.glob("KGC*.ttl")):
        g = Graph().parse(f, format="turtle")
        pols = sorted(g.subjects(RDF.type, ODRL.Set), key=str)
        if len(pols) < 2:
            continue
        compared += 1
        acts, targets = [], []
        for pol in pols:
            rules = [r for kind in ("permission", "prohibition", "obligation")
                     for r in g.objects(pol, ODRL[kind])]
            acts.append({local(a) for r in rules for a in g.objects(r, ODRL.action)})
            targets.append({local(t) for r in rules for t in g.objects(r, ODRL.target)})
        if any(a != acts[0] for a in acts):
            failures.append((f.stem, "action " + " vs ".join(
                ",".join(sorted(a)) or "none" for a in acts)))
        if any(t != targets[0] for t in targets):
            failures.append((f.stem, "target " + " vs ".join(
                ",".join(sorted(t)) or "none" for t in targets)))
    return compared, failures


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--cases", default="cases", type=Path)
    ap.add_argument("--limit", type=int, default=30, help="Z3 seconds per query")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    problems = []
    for name in MODULES:
        problems += importlib.import_module(name).PROBLEMS

    checked, skipped, bad_a = admits_a_use(problems, args.limit)
    cases_a = len({c for c, _, _ in checked})
    print(f"5a  each policy alone admits a use: {len(checked)} policies in "
          f"{cases_a} cases checked, {len(skipped)} cases without a query skipped")
    if args.verbose:
        for cid, side, status in checked:
            print(f"      {cid} {side:8} {status}")
    for cid, side, status in bad_a:
        print(f"    FAIL {cid}: the {side} policy alone is {status}")

    compared, bad_b = acts_alike(args.cases)
    print(f"5b  both policies share action and target: {compared} cases compared")
    for cid, what in bad_b:
        print(f"    FAIL {cid}: {what}")

    return 1 if bad_a or bad_b else 0


if __name__ == "__main__":
    sys.exit(main())
