"""
provers.py
==========
The two provers, named by the environment variables VAMPIRE and Z3 and never
found through PATH: a run says which binaries it uses, and another Vampire or
Z3 on the machine cannot stand in for them.
"""

import os
from pathlib import Path


def _binary(variable: str) -> str:
    value = os.environ.get(variable, "")
    if not value:
        raise SystemExit(f"set {variable} to the path of the binary; "
                         f"PATH is not searched")
    if not (Path(value).is_file() and os.access(value, os.X_OK)):
        raise SystemExit(f"{variable}={value} is not an executable file")
    return value


def vampire() -> str:
    return _binary("VAMPIRE")


def z3() -> str:
    return _binary("Z3")
