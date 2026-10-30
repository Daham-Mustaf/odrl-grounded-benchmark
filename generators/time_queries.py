#!/usr/bin/env python3
"""
time_queries.py
===============
The timing pass: every query of the suite under its prover, each alone, one
at a time, and the wall time it took.

    uv run generators/time_queries.py [--limit 60] [--out results/timings.csv]

A .p query runs under Vampire as the verdict run runs it (run_verdict.sh,
casc mode), an .smt2 query under Z3.  One process runs at a time, so that no
run competes with another for the machine.  The limit is full-run.sh's
PROVER_LIMIT when --limit is not given.

results/timings.csv has one row per query and prover,

    query,prover,status,seconds

under a header of comment lines naming both prover versions, the CPU, the
memory, the operating system, the date and the limit.  table_data.py
--suite-numbers reads it for the time macros, and refuses a file that does
not cover the current queries.

Exit 1 if a query gets no status within the limit; the file is written
either way.
"""

import argparse
import csv
import datetime
import os
import platform
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SZS = {"Satisfiable": "sat", "CounterSatisfiable": "sat",
       "Unsatisfiable": "unsat", "Theorem": "unsat",
       "ContradictoryAxioms": "unsat"}


def first_line(cmd) -> str:
    try:
        out = subprocess.run(cmd, capture_output=True, text=True).stdout
    except OSError:
        return "not found"
    return out.splitlines()[0].strip() if out.strip() else "unknown"


def cpu() -> str:
    try:
        for line in Path("/proc/cpuinfo").read_text().splitlines():
            if line.startswith("model name"):
                return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform.processor() or "unknown"


def ram() -> str:
    try:
        for line in Path("/proc/meminfo").read_text().splitlines():
            if line.startswith("MemTotal:"):
                kb = int(line.split()[1])
                return f"{kb / 2 ** 20:.1f} GiB"
    except OSError:
        pass
    return "unknown"


def os_name() -> str:
    name = platform.system()
    try:
        for line in Path("/etc/os-release").read_text().splitlines():
            if line.startswith("PRETTY_NAME="):
                name = line.split("=", 1)[1].strip('"')
    except OSError:
        pass
    return f"{name}, {platform.system()} {platform.release()}"


def run(path: Path, limit: int) -> tuple:
    """(status, seconds) of one query."""
    if path.suffix == ".p":
        cmd = ["vampire", "--include", str(ROOT / "problems"), "--mode", "casc",
               "--time_limit", str(limit), str(path)]
    else:
        cmd = ["z3", f"-T:{limit}", str(path)]
    start = time.monotonic()
    try:
        out = subprocess.run(cmd, capture_output=True, text=True,
                             timeout=limit + 30).stdout
    except subprocess.TimeoutExpired:
        return "timeout", time.monotonic() - start
    seconds = time.monotonic() - start
    if path.suffix == ".p":
        m = re.search(r"SZS status (\w+)", out)
        return (SZS.get(m.group(1), m.group(1)) if m else "no-status"), seconds
    line = out.split("\n", 1)[0].strip()
    return (line or "no-output"), seconds


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[3])
    ap.add_argument("--dir", default=ROOT / "problems" / "verdict", type=Path)
    ap.add_argument("--out", default=ROOT / "results" / "timings.csv", type=Path)
    ap.add_argument("--limit", type=int,
                    default=int(os.environ.get("PROVER_LIMIT", 60)),
                    help="seconds a prover may take on one query")
    args = ap.parse_args()

    queries = sorted([*args.dir.glob("*-[12].p"), *args.dir.glob("*-[12].smt2")],
                     key=lambda p: (p.stem, p.suffix))
    if not queries:
        print(f"no queries in {args.dir}", file=sys.stderr)
        return 1

    header = [
        "timings.csv, written by generators/time_queries.py. Do not edit.",
        f"vampire: {first_line(['vampire', '--version'])}",
        f"z3: {first_line(['z3', '--version'])}",
        f"cpu: {cpu()}, {os.cpu_count()} logical cores",
        f"ram: {ram()}",
        f"os: {os_name()}",
        f"date: {datetime.datetime.now().astimezone().isoformat(timespec='seconds')}",
        f"limit: {args.limit}",
        "runs: each query alone, one at a time",
    ]
    rows, missing = [], []
    for q in queries:
        prover = "vampire" if q.suffix == ".p" else "z3"
        status, seconds = run(q, args.limit)
        rows.append((q.stem, prover, status, f"{seconds:.2f}"))
        if status not in ("sat", "unsat"):
            missing.append(f"{q.name}: {status}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as f:
        f.writelines(f"# {h}\n" for h in header)
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["query", "prover", "status", "seconds"])
        w.writerows(rows)

    total = sum(float(r[3]) for r in rows)
    slow = max(rows, key=lambda r: float(r[3]))
    print(f"wrote {args.out}: {len(rows)} runs, {total:.1f} s in all, slowest "
          f"{slow[0]} under {slow[1]} at {slow[3]} s")
    for m in missing:
        print(f"    NO STATUS {m}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
