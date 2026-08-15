"""
gen_all_problems.py
===================
Convenience runner: regenerates all KGConstraints problem files.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent

scripts = [
    "gen_motivating.py",
    "gen_operators.py",
   "gen_refinement_problems.py",
]

for script in scripts:
    print(f"\n{'='*70}\n  Running {script}\n{'='*70}")
    result = subprocess.run(
        [sys.executable, str(HERE / script)] + sys.argv[1:],
        check=False,
    )
    if result.returncode != 0:
        print(f"ERROR: {script} exited with code {result.returncode}",
              file=sys.stderr)
        sys.exit(result.returncode)