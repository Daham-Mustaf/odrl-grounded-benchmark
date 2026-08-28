"""
check_encodings.py
==================
Fails when the two encodings of a problem disagree.

    uv run generators/check_encodings.py                    # all problems
    uv run generators/check_encodings.py --allow-known      # known gaps pass

Exit status is 0 when every problem's TPTP and SMT-LIB queries return the
same pair of statuses, and 1 otherwise.  Intended for CI, where the point is
that a divergence stops the build rather than appearing in a table someone
may or may not read.

What this tests, and what it does not
-------------------------------------
The paper defines what a constraint denotes and what a witness condition
is; the generator emits two encodings of that condition, one TPTP and one
SMT-LIB.  Nothing states, and nothing has ever checked, that either encoding
means what the definition means.  That obligation is a translation-adequacy
lemma the paper does not yet carry.

This is the weaker, checkable shadow of it: not that each encoding is
faithful to the definition, but that the two agree with each other.  An
encoding bug on one side and not the other shows up here.  A bug both sides
share does not, and no amount of running will find it; only the lemma will.

It is worth having anyway, because the bug that actually occurred was of the
first kind.  A multi-valued isAnyOf in the meets conjunct produced an
unparenthesised disjunction that the TPTP conjunction then swallowed; the
SMT side, being prefix, was unaffected.  Two provers returned different
verdicts on the same problem and the difference was the encoding rather than
either prover.  It was noticed because someone read the table.

Known gaps
----------
Some problems leave smt2_resource or smt2_background empty, so the SMT query
carries fewer assertions than the TPTP one and the two legitimately differ.
That is a defect in the problem data, not in the encodings, and it is listed
below rather than silently tolerated: --allow-known lets the run pass while
still printing them, so the list has to shrink deliberately.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

# Problems whose SMT side is known to carry less than the TPTP side.
# Each entry is a defect to fix, not an accepted difference.
KNOWN_GAPS = {
    "KGC334": "smt2_background empty; $distinct is not read by a "
              "first-order prover, so the two sides carry different "
              "distinctness information",
}

VAMPIRE = ["vampire", "--mode", "vampire", "--proof", "tptp",
           "--output_axiom_names", "on", "-t", "30"]
Z3 = ["z3", "-T:30"]

_SZS = re.compile(r"SZS status (\w+)")


def run_fof(path: Path) -> str:
    try:
        out = subprocess.run(VAMPIRE + [str(path)], capture_output=True,
                             text=True, timeout=60).stdout
    except subprocess.TimeoutExpired:
        return "timeout"
    m = _SZS.search(out)
    if not m:
        return "no-status"
    s = m.group(1).lower()
    return {"unsatisfiable": "unsat", "satisfiable": "sat",
            "countersatisfiable": "sat"}.get(s, s)


def run_smt(path: Path) -> str:
    try:
        out = subprocess.run(Z3 + [str(path)], capture_output=True,
                             text=True, timeout=60).stdout
    except subprocess.TimeoutExpired:
        return "timeout"
    for line in out.splitlines():
        line = line.strip()
        if line in ("sat", "unsat", "unknown"):
            return line
    return "no-status"


def verdict(q1: str, q2: str) -> str:
    """The verdict the pair of statuses gives, or why it gives none."""
    if q1 == "unsat" and q2 == "unsat":
        return "INCONSISTENT"
    if q1 == "unsat":
        return "Incompatible"
    if q2 == "unsat":
        return "Compatible"
    if "sat" in (q1, q2) and q1 == q2 == "sat":
        return "Unknown"
    return f"undecided({q1},{q2})"


def assertion_names(p_file: Path, smt_file: Path) -> tuple[set, set]:
    """The named assertions each side carries.

    A difference here is the usual cause of a verdict divergence, and it
    localises the defect to a field of the problem rather than to the
    encoder: an empty smt2_resource shows up as names present in the TPTP
    includes and absent from the SMT file.
    """
    fof_text = p_file.read_text(encoding="utf-8")
    fof = set(re.findall(r"fof\(\s*([a-z]+_[a-z0-9_]+)", fof_text))
    # Included axiom files carry the resource and background assertions.
    for inc in re.findall(r"include\('([^']+)'\)", fof_text):
        ax = p_file.parent.parent / inc
        if ax.exists():
            fof |= set(re.findall(r"fof\(\s*([a-z]+_[a-z0-9_]+)",
                                  ax.read_text(encoding="utf-8")))
    smt = set(re.findall(r":named ([a-z]+_[a-z0-9_]+)",
                         smt_file.read_text(encoding="utf-8")))
    keep = lambda s: {n for n in s if n.split("_")[0] in
                      ("res", "bt", "ax", "w")}
    return keep(fof), keep(smt)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[3])
    ap.add_argument("--dir", default="problems/verdict", type=Path)
    ap.add_argument("--allow-known", action="store_true",
                    help="exit 0 despite the divergences listed in "
                         "KNOWN_GAPS; they are still printed")
    ap.add_argument("--names-only", action="store_true",
                    help="compare the assertions each side carries and "
                         "skip the provers")
    args = ap.parse_args()

    ids = sorted({p.stem.rsplit("-", 1)[0] for p in args.dir.glob("*-1.p")})
    if not ids:
        print(f"no problems in {args.dir}", file=sys.stderr)
        return 1

    diverged, gapped = [], []
    print(f"{'problem':10} {'TPTP':>14} {'SMT-LIB':>14}   assertions")
    for pid in ids:
        p1, p2 = args.dir / f"{pid}-1.p", args.dir / f"{pid}-2.p"
        s1, s2 = args.dir / f"{pid}-1.smt2", args.dir / f"{pid}-2.smt2"

        fof_names, smt_names = assertion_names(p1, s1)
        only_fof = fof_names - smt_names
        only_smt = smt_names - fof_names
        note = ""
        if only_fof or only_smt:
            note = f"TPTP only {len(only_fof)}, SMT only {len(only_smt)}"

        if args.names_only:
            print(f"{pid:10} {'':>14} {'':>14}   {note or 'same'}")
            if note:
                diverged.append((pid, "assertion sets differ", note))
            continue

        f = verdict(run_fof(p1), run_fof(p2))
        s = verdict(run_smt(s1), run_smt(s2))
        mark = "" if f == s else "   DIVERGENT"
        print(f"{pid:10} {f:>14} {s:>14}   {note}{mark}")
        if f != s:
            (gapped if pid in KNOWN_GAPS else diverged).append((pid, f, s))

    print()
    for pid, f, s in gapped:
        print(f"known gap  {pid}: {f} vs {s}")
        print(f"           {KNOWN_GAPS[pid]}")
    for pid, f, s in diverged:
        print(f"DIVERGENT  {pid}: {f} vs {s}")

    if diverged:
        print(f"\n{len(diverged)} problem(s) encode differently in the two "
              f"languages.\nThe verdict is a property of the constraints and "
              f"the resource, so a\ndifference between the encodings is a "
              f"defect in one of them.")
        return 1
    if gapped and not args.allow_known:
        print(f"\n{len(gapped)} known gap(s); pass --allow-known to "
              f"tolerate them.")
        return 1
    print("the two encodings agree on every problem.")
    return 0


if __name__ == "__main__":
    sys.exit(main())