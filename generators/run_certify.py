"""
run_certify.py
==============
Runs both queries of each problem, derives the verdict, and writes the
observed certificate beside the expected one.

    uv run generators/run_certify.py
    uv run generators/run_certify.py --problem KGC300

Vampire must be run with --output_axiom_names on or every premise comes back
anonymous and nothing can be attributed.  The runner passes it; if a proof
still carries no names, it says so rather than writing an empty certificate.
"""

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from certificate import (premises_from_vampire, classify, to_turtle,
                         withdrawable, NoAxiomNames, NoProof)

# --mode vampire rather than casc: the schedule mode does not always
# propagate --output_axiom_names to its child strategies, and without
# names no premise can be attributed.
VAMPIRE = ["vampire", "--mode", "vampire", "--proof", "tptp",
           "--output_axiom_names", "on"]


def run(path: Path, timeout: int, cwd: Path) -> tuple[str, str]:
    """Returns (normalised status, raw output).

    Runs with cwd set to the problems directory, since include() in a problem
    file resolves against the working directory, not against the file.
    """
    rel = path.relative_to(cwd)
    try:
        r = subprocess.run(VAMPIRE + ["--time_limit", str(timeout), str(rel)],
                           capture_output=True, text=True, timeout=timeout + 10,
                           cwd=str(cwd))
    except subprocess.TimeoutExpired:
        return "timeout", ""
    out = r.stdout + r.stderr
    for line in out.splitlines():
        if "SZS status" in line:
            s = line.split()[3]
            if s in ("Unsatisfiable", "Theorem", "ContradictoryAxioms"):
                return "unsat", out
            if s in ("Satisfiable", "CounterSatisfiable"):
                return "sat", out
            return s, out
    return "no-status", out


def verdict_of(q1: str, q2: str) -> str:
    if q1 == "unsat" and q2 == "unsat":
        return "INCONSISTENT"
    if q1 == "unsat":
        return "Incompatible"
    if q2 == "unsat":
        return "Compatible"
    if q1 == "sat" and q2 == "sat":
        return "Unknown"
    return f"undecided({q1},{q2})"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--problems-dir", default="problems/verdict")
    ap.add_argument("--out-dir", default="certificates")
    ap.add_argument("--problem", default=None, help="one problem id")
    ap.add_argument("--timeout", type=int, default=30)
    args = ap.parse_args()

    pdir, odir = Path(args.problems_dir), Path(args.out_dir)
    odir.mkdir(parents=True, exist_ok=True)

    pattern = f"{args.problem}-1.p" if args.problem else "*-1.p"
    problems = sorted(pdir.glob(pattern))
    if not problems:
        print(f"no problems matching {pdir}/{pattern}", file=sys.stderr)
        return 1

    for q1path in problems:
        pid = q1path.name[:-4]
        q2path = q1path.with_name(f"{pid}-2.p")
        root = pdir.parent
        s1, out1 = run(q1path, args.timeout, root)
        s2, out2 = run(q2path, args.timeout, root)
        v = verdict_of(s1, s2)

        print(f"{pid}  q1={s1:8s} q2={s2:8s} -> {v}")

        # The refutation is whichever query came back unsatisfiable.
        raw, which = (out1, 1) if s1 == "unsat" else \
                     (out2, 2) if s2 == "unsat" else (None, None)
        if raw is None:
            if s1 not in ("sat", "unsat") or s2 not in ("sat", "unsat"):
                print(f"    no verdict: prover returned {s1} and {s2}")
                print(f"    first 5 lines of output:")
                for line in out1.splitlines()[:5]:
                    print(f"      {line}")
                continue
            print("    Unknown: two models; no refutation to attribute.")
            continue

        try:
            names = premises_from_vampire(raw)
        except (NoAxiomNames, NoProof) as e:
            print(f"    {e}")
            continue
        if not names:
            print("    no premises reported; is --proof on taking effect?")
            continue

        c = classify(names)
        ttl = to_turtle(pid, "Refutation", c,
                        artefact=f"proofs/{pid}-{which}.tstp",
                        prover="Vampire")
        (odir / f"{pid}-observed.ttl").write_text(ttl + "\n", encoding="utf-8")
        (odir / f"{pid}-{which}.tstp").write_text(raw, encoding="utf-8")

        for source, ns in c.items():
            if ns and source != "unclassified":
                print(f"    {source:24s} {', '.join(ns)}")
        if c["unclassified"]:
            print(f"    UNCLASSIFIED             {', '.join(c['unclassified'])}")
        w = withdrawable(c)
        print(f"    withdrawable             {', '.join(w) if w else 'none'}")
        print(f"    -> {odir / f'{pid}-observed.ttl'}")

    return 0


if __name__ == "__main__":
    sys.exit(main())