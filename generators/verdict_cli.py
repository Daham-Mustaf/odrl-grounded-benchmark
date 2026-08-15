"""
verdict_cli.py
==============
Decides two ODRL policies against each other, from Turtle in to verdict out.

    uv run verdict_cli.py offer.ttl request.ttl --profile profile.ttl \
        --resource purpose=dpv.ttl --background purpose=dpv-declared.ttl

For each operand both policies constrain, it computes the witness condition,
writes the two queries, runs a prover, and reports the verdict with its
certificate.

The benchmark is one caller of this.  Nothing here knows about a problem id.
"""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from policy import (read_policy, read_profile, read_resource, bind, ground,
                    by_operand, ProfileError, GroundingError)
from compile import Constraint as CC, compile_operand
from signature import is_well_sorted
from certificate import premises_from_vampire, classify, NoAxiomNames, WITHDRAWABLE

VAMPIRE = ["vampire", "--mode", "casc", "--proof", "on",
           "--output_axiom_names", "on", "--time_limit", "30"]

ORDER_AXIOMS = """\
fof(ax_leq_reflexive, axiom, ![X]: kge_leq(X, X)).
fof(ax_leq_transitive, axiom,
    ![X,Y,Z]: ((kge_leq(X,Y) & kge_leq(Y,Z)) => kge_leq(X,Z))).
fof(ax_leq_antisymmetric, axiom,
    ![X,Y]: ((kge_leq(X,Y) & kge_leq(Y,X)) => X = Y)).
"""


def arity_of(operator, values):
    return "n" if operator in ("isAnyOf", "isAllOf", "isNoneOf") else len(values)


def query_text(order_pairs, background_lines, witness, negate):
    parts = [ORDER_AXIOMS]
    for i, (a, b) in enumerate(sorted(order_pairs)):
        parts.append(f"fof(res_{a}_leq_{b}, axiom, kge_leq({a}, {b})).")
    parts.extend(background_lines)
    w = f"~ ( {witness} )" if negate else witness
    parts.append(f"fof(w_query, axiom,\n    {w}).")
    return "\n".join(parts) + "\n"


def run(text):
    with tempfile.NamedTemporaryFile("w", suffix=".p", delete=False) as f:
        f.write(text)
        path = f.name
    try:
        r = subprocess.run(VAMPIRE + [path], capture_output=True, text=True,
                           timeout=60)
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        return "unavailable", str(e)
    out = r.stdout + r.stderr
    for line in out.splitlines():
        if "SZS status" in line:
            s = line.split()[3]
            if s in ("Unsatisfiable", "Theorem", "ContradictoryAxioms"):
                return "unsat", out
            if s in ("Satisfiable", "CounterSatisfiable"):
                return "sat", out
    return "no-status", out


def main() -> int:
    ap = argparse.ArgumentParser(description="Decide two ODRL policies.")
    ap.add_argument("offer")
    ap.add_argument("request")
    ap.add_argument("--profile", required=True)
    ap.add_argument("--resource", action="append", default=[],
                    metavar="OPERAND=FILE")
    ap.add_argument("--background", action="append", default=[],
                    metavar="OPERAND=FILE")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the queries without running a prover")
    args = ap.parse_args()

    resources = dict(x.split("=", 1) for x in args.resource)
    backgrounds = dict(x.split("=", 1) for x in args.background)

    profile = read_profile(args.profile)
    offer = read_policy(args.offer, "offer")
    request = read_policy(args.request, "request")

    try:
        bindings = bind(offer + request, profile)
    except ProfileError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    groups = by_operand(offer, request)
    verdicts = {}

    for operand, constraints in sorted(groups.items()):
        b = bindings[operand]
        print(f"\n{operand}  (sort {b.sort})")

        # 1. the drafting-time check
        for c in constraints:
            ok, why = is_well_sorted(c.operator, b.sort,
                                     arity_of(c.operator, c.values))
            if not ok:
                print(f"  ill sorted: {c.operator} — {why}")
                verdicts[operand] = "IllSorted"
                break
        if verdicts.get(operand) == "IllSorted":
            continue

        if operand not in resources:
            print(f"  no resource file given for {operand}; pass "
                  f"--resource {operand}=<file>")
            continue
        res = read_resource(resources[operand], b.resource)

        # 2. grounding
        try:
            ground(constraints, res)
        except GroundingError as e:
            print(f"  Unknown: value names no concept of the resource: {e}")
            verdicts[operand] = "Unknown"
            continue

        # 3. the witness condition
        concepts = sorted({v for c in constraints for v in c.values})
        w = compile_operand([CC(c.operator, c.values, c.side)
                             for c in constraints], concepts, b.sort)

        bg = []
        if operand in backgrounds:
            bg = Path(backgrounds[operand]).read_text().splitlines()
            bg = [l for l in bg if l.strip().startswith("fof(")]
        if not bg:
            print("  (no background theory: nothing is separated, so a "
                  "definite Incompatible is unreachable)")

        q1 = query_text(res.order, bg, w["fof"], negate=False)
        q2 = query_text(res.order, bg, w["fof"], negate=True)

        if args.dry_run:
            print("  --- query 1 ---"); print(q1)
            print("  --- query 2 ---"); print(q2)
            continue

        s1, out1 = run(q1)
        s2, out2 = run(q2)
        if s1 == "unavailable":
            print(f"  prover unavailable: {out1}")
            return 3

        v = ("Incompatible" if s1 == "unsat" else
             "Compatible" if s2 == "unsat" else
             "Unknown" if s1 == s2 == "sat" else f"undecided({s1},{s2})")
        verdicts[operand] = v
        print(f"  {v}")

        raw = out1 if s1 == "unsat" else out2 if s2 == "unsat" else None
        if raw:
            try:
                c = classify(premises_from_vampire(raw), "query")
                for source, ns in c.items():
                    if ns and source != "unclassified":
                        print(f"    {source:22s} {', '.join(ns)}")
                w_ = [n for s in WITHDRAWABLE for n in c[s]]
                print(f"    withdrawable           "
                      f"{', '.join(w_) if w_ else 'none'}")
            except NoAxiomNames as e:
                print(f"    {e}")

    if verdicts:
        print()
        if "IllSorted" in verdicts.values():
            print("Overall: ill sorted; no verdict.")
        elif "Incompatible" in verdicts.values():
            print("Overall: Incompatible")
        elif all(v == "Compatible" for v in verdicts.values()):
            print("Overall: Compatible")
        else:
            print("Overall: Unknown")
    return 0


if __name__ == "__main__":
    sys.exit(main())