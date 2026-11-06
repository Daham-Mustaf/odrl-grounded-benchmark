#!/usr/bin/env python3
"""
time_queries.py
===============
The timing pass: every check of the suite, that is every query under its
prover, each alone, one at a time, and the wall time it took.  Three
independent runs of every check, with nothing else running.

    uv run generators/time_queries.py [--repeat 3] [--limit 300] [--results results]

A .p query runs under Vampire as the verdict run runs it (run_verdict.sh,
casc mode), an .smt2 query under Z3.  One process runs at a time, so that no
run competes with another for the machine.  The limit is full-run.sh's
PROVER_LIMIT when --limit is not given.

Each run is written to results/timings-runN.csv, with one row per query and
prover,

    query,prover,status,seconds

under a header of comment lines naming both prover versions, the CPU, the
memory, the operating system, the date, the limit and the run.  A new pass
replaces the old one, results/timings.csv included.  table_data.py
--suite-numbers reads the runs for the time macros, and refuses a run that
does not cover the current queries.

Exit 1 if a prover is already running, so that nothing is timed against it, or
if a query gets no status within the limit; each finished run is written
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
sys.path.insert(0, str(Path(__file__).parent))

import provers

SZS = {"Satisfiable": "sat", "CounterSatisfiable": "sat",
       "Unsatisfiable": "unsat", "Theorem": "unsat",
       "ContradictoryAxioms": "unsat"}


def first_line(cmd) -> str:
    try:
        out = subprocess.run(cmd, capture_output=True, text=True).stdout
    except OSError:
        return "not found"
    return out.splitlines()[0].strip() if out.strip() else "unknown"


def sysctl(name: str) -> str:
    """A value of the machine, on macOS, or the empty string."""
    try:
        return subprocess.run(["sysctl", "-n", name], capture_output=True,
                              text=True).stdout.strip()
    except OSError:
        return ""


def cpu() -> str:
    chip = sysctl("machdep.cpu.brand_string")
    if chip:
        return chip
    try:
        for line in Path("/proc/cpuinfo").read_text().splitlines():
            if line.startswith("model name"):
                return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform.processor() or "unknown"


def ram() -> str:
    size = sysctl("hw.memsize")
    if size:
        return f"{int(size) / 2 ** 30:.1f} GiB"
    try:
        for line in Path("/proc/meminfo").read_text().splitlines():
            if line.startswith("MemTotal:"):
                kb = int(line.split()[1])
                return f"{kb / 2 ** 20:.1f} GiB"
    except OSError:
        pass
    return "unknown"


def os_name() -> str:
    if platform.system() == "Darwin":
        return f"macOS {platform.mac_ver()[0]}"
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
        cmd = [provers.vampire(), "--include", str(ROOT / "problems"), "--mode", "casc",
               "--time_limit", str(limit), str(path)]
    else:
        cmd = [provers.z3(), f"-T:{limit}", str(path)]
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


def provers_running() -> list:
    """Vampire or Z3 processes already on the machine."""
    out = subprocess.run(["ps", "-A", "-o", "comm="], capture_output=True,
                         text=True).stdout
    return sorted({Path(line.strip()).name for line in out.splitlines()
                   if Path(line.strip()).name.startswith(("vampire", "z3"))})


def one_run(number: int, repeat: int, queries, limit: int, out: Path) -> list:
    """Time every check once and write the file; the checks with no status."""
    header = [
        f"{out.name}, written by generators/time_queries.py. Do not edit.",
        f"vampire: {first_line([provers.vampire(), '--version'])}",
        f"z3: {first_line([provers.z3(), '--version'])}",
        f"cpu: {cpu()}, {os.cpu_count()} logical cores",
        f"ram: {ram()}",
        f"os: {os_name()}",
        f"date: {datetime.datetime.now().astimezone().isoformat(timespec='seconds')}",
        f"limit: {limit}",
        f"run: {number} of {repeat}",
        "runs: each query alone, one at a time",
    ]
    rows, missing = [], []
    for q in queries:
        prover = "vampire" if q.suffix == ".p" else "z3"
        status, seconds = run(q, limit)
        rows.append((q.stem, prover, status, f"{seconds:.2f}"))
        if status not in ("sat", "unsat"):
            missing.append(f"{q.name}: {status}")

    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as f:
        f.writelines(f"# {h}\n" for h in header)
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["query", "prover", "status", "seconds"])
        w.writerows(rows)

    total = sum(float(r[3]) for r in rows)
    slow = max(rows, key=lambda r: float(r[3]))
    print(f"wrote {out}: {len(rows)} checks, {total:.1f} s in all, slowest "
          f"{slow[0]} under {slow[1]} at {slow[3]} s", flush=True)
    return missing


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[3])
    ap.add_argument("--dir", default=ROOT / "problems" / "verdict", type=Path)
    ap.add_argument("--results", default=ROOT / "results", type=Path)
    ap.add_argument("--repeat", type=int, default=3,
                    help="independent runs of every check")
    ap.add_argument("--limit", type=int,
                    default=int(os.environ.get("PROVER_LIMIT", 300)),
                    help="seconds a prover may take on one query")
    args = ap.parse_args()

    queries = sorted([*args.dir.glob("*-[12].p"), *args.dir.glob("*-[12].smt2")],
                     key=lambda p: (p.stem, p.suffix))
    if not queries:
        print(f"no queries in {args.dir}", file=sys.stderr)
        return 1

    running = provers_running()
    if running:
        print(f"not timing: {', '.join(running)} already running",
              file=sys.stderr)
        return 1

    for old in [args.results / "timings.csv",
                *args.results.glob("timings-run*.csv")]:
        old.unlink(missing_ok=True)

    missing = []
    for number in range(1, args.repeat + 1):
        out = args.results / f"timings-run{number}.csv"
        missing += one_run(number, args.repeat, queries, args.limit, out)
    for m in missing:
        print(f"    NO STATUS {m}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
