#!/usr/bin/env python3
"""
run_tptp.py
===========
Checks and runs the TPTP export that export_tptp.py writes.

    uv run generators/run_tptp.py check [--tptp4x PATH]
    uv run generators/run_tptp.py run --version 1 --limit 60
    uv run generators/run_tptp.py run --version 2 --limit 300 --sat-retry
    uv run generators/run_tptp.py axioms --limit 300

check   parses every problem and axiom file with tptp4X, includes expanded
        (-x) and warnings on (-w), and fails on an error, a warning, or a
        function symbol: every term must be a variable or a constant.
run     runs Vampire on the problems of one version, one at a time, with
        --mode casc and the given limit; with --sat-retry, a Satisfiable
        problem casc does not solve is run again with --mode casc_sat.  Each
        run is appended to results/tptp-runs.csv (problem, mode, limit,
        result, seconds) as it ends, so a run that stops resumes where it
        stopped.
axioms  runs Vampire on each file of tptp/Axioms alone, with --mode casc, and
        fails unless each is Satisfiable.  The runs go in the same file.

tptp4X is built from the TPTP World sources (github.com/TPTPWorld/TPTP4X
and JJParser); TPTP is set to the export folder, so that the includes,
written include('Axioms/...'), resolve there.
"""

import argparse
import csv
import os
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).parent))

import provers

EXPORT = ROOT / "tptp"
RUNS = ROOT / "results" / "tptp-runs.csv"
FIELDS = ["problem", "mode", "limit", "result", "seconds"]


def status_of(path: Path) -> str:
    return re.search(r"^% Status\s*:\s*(\w+)", path.read_text(encoding="utf-8"),
                     re.M).group(1)


def check(tptp4x: str) -> int:
    files = sorted((EXPORT / "Problems").rglob("*.p")) + \
        sorted((EXPORT / "Axioms").glob("*.ax"))
    env = dict(os.environ, TPTP=str(EXPORT))
    bad = []
    # A term applied to arguments that is not one of the predicates.
    functor = re.compile(r"(?<![\w$])(?!kge_leq\(|kge_concept\()([a-z]\w*)\(")
    for f in files:
        r = subprocess.run([tptp4x, "-x", "-w", str(f.relative_to(EXPORT))],
                           cwd=EXPORT, env=env, capture_output=True, text=True)
        noise = [l for l in (r.stdout + r.stderr).splitlines()
                 if re.search(r"\b(WARNING|Warning|ERROR|Error)\b", l)]
        if r.returncode or noise:
            bad.append((f.name, r.returncode, noise[:3]))
            continue
        body = [l for l in r.stdout.splitlines() if not l.startswith("%")]
        heads = {m for l in body for m in functor.findall(l)} - {"fof"}
        if heads:
            bad.append((f.name, 0, [f"function symbols {sorted(heads)}"]))
    for name, code, noise in bad:
        print(f"    FAIL {name}: exit {code}; " + "; ".join(noise))
    print(f"tptp4X -x -w: {len(files)} files, "
          + (f"{len(bad)} failing" if bad else
             "every one parses with no warning, and no term is a function"))
    return 1 if bad else 0


def vampire(path: Path, mode: str, limit: int) -> tuple:
    start = time.monotonic()
    try:
        out = subprocess.run(
            [provers.vampire(), "--include", str(EXPORT), "--mode", mode,
             "--time_limit", str(limit), str(path)],
            capture_output=True, text=True, timeout=limit + 60).stdout
    except subprocess.TimeoutExpired:
        return "Timeout", time.monotonic() - start
    m = re.search(r"SZS status (\w+)", out)
    return (m.group(1) if m else "no-status"), time.monotonic() - start


def run(version: int, limit: int, sat_retry: bool) -> int:
    files = sorted((EXPORT / "Problems").rglob(f"*+{version}.p"))
    done = {}
    if RUNS.exists():
        with RUNS.open(encoding="utf-8") as f:
            for r in csv.DictReader(f):
                done.setdefault(r["problem"], []).append(r)
    new = not RUNS.exists()
    RUNS.parent.mkdir(parents=True, exist_ok=True)
    wrong = []
    with RUNS.open("a", encoding="utf-8", newline="") as out:
        w = csv.DictWriter(out, fieldnames=FIELDS, lineterminator="\n")
        if new:
            w.writeheader()
        for f in files:
            want = status_of(f)
            modes = ["casc"] + (["casc_sat"] if sat_retry and want == "Satisfiable" else [])
            prior = {r["mode"]: r for r in done.get(f.name, [])
                     if r["limit"] == str(limit)}
            for mode in modes:
                if mode in prior:
                    result = prior[mode]["result"]
                else:
                    result, seconds = vampire(f, mode, limit)
                    w.writerow({"problem": f.name, "mode": mode, "limit": limit,
                                "result": result, "seconds": f"{seconds:.2f}"})
                    out.flush()
                    print(f"  {f.name:12} {mode:9} {result:15} {seconds:7.2f} s",
                          flush=True)
                if result in ("Satisfiable", "Unsatisfiable"):
                    if result != want:
                        wrong.append((f.name, mode, result, want))
                    break
    for name, mode, result, want in wrong:
        print(f"    WRONG {name}: {mode} says {result}, the header says {want}")
    return 1 if wrong else 0


def axioms(limit: int) -> int:
    files = sorted((EXPORT / "Axioms").glob("*.ax"))
    done = {}
    if RUNS.exists():
        with RUNS.open(encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r["limit"] == str(limit):
                    done[r["problem"]] = r["result"]
    new = not RUNS.exists()
    wrong = []
    with RUNS.open("a", encoding="utf-8", newline="") as out:
        w = csv.DictWriter(out, fieldnames=FIELDS, lineterminator="\n")
        if new:
            w.writeheader()
        for f in files:
            result = done.get(f.name)
            if result is None:
                result, seconds = vampire(f, "casc", limit)
                w.writerow({"problem": f.name, "mode": "casc", "limit": limit,
                            "result": result, "seconds": f"{seconds:.2f}"})
                out.flush()
                print(f"  {f.name:12} casc      {result:15} {seconds:7.2f} s",
                      flush=True)
            if result != "Satisfiable":
                wrong.append((f.name, result))
    for name, result in wrong:
        print(f"    WRONG {name}: {result}, and it must be Satisfiable alone")
    print(f"axiom files: {len(files)}, {len(files) - len(wrong)} Satisfiable alone")
    return 1 if wrong else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[3])
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("--tptp4x", default=os.environ.get("TPTP4X", "tptp4X"))
    r = sub.add_parser("run")
    r.add_argument("--version", type=int, required=True)
    r.add_argument("--limit", type=int, required=True)
    r.add_argument("--sat-retry", action="store_true")
    x = sub.add_parser("axioms")
    x.add_argument("--limit", type=int, required=True)
    args = ap.parse_args()
    if args.cmd == "check":
        return check(args.tptp4x)
    if args.cmd == "axioms":
        return axioms(args.limit)
    return run(args.version, args.limit, args.sat_retry)


if __name__ == "__main__":
    sys.exit(main())
