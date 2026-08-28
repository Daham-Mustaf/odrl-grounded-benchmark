"""
runner.py
=========
Solvers in, statuses out.

This layer produces run statuses and nothing else.  It does not know what a
verdict is and cannot construct one, which is the point: a solver reports
what it found about one file on one machine on one day, and turning a pair
of those into a claim about every admissible structure is a separate step
with its own module.

The temptation this rules out is small and specific.  A runner that knew
about verdicts would, on a timeout, be one line away from returning the
expected verdict instead, and the result would be a table where nothing
distinguishes a checked answer from an assumed one.

Recording the environment
-------------------------
Every result carries the solver's name, its version, the hash of the binary,
the exact command, the time limit and the host.  This is not bookkeeping
for its own sake: a result that says only ``unsat`` is unreproducible, and
an old binary invoked in a mode that silently dropped a flag has already
cost this project a day of confusion about which prover was right.

Adapters
--------
One per solver, each mapping that solver's output to a RunStatus and
nothing more.  A solver that prints something unrecognised gives
UNDETERMINED rather than a guess; a solver that fails to start gives ERROR.
Neither is a kind of Unknown, because Unknown is a verdict and this layer
has none.

Premise names are harvested here because that is where the output is, but
they are not classified here.  What a proof used is a fact about the run;
what class a premise belongs to is a fact about the query, and the
certificate layer puts the two together.
"""

from __future__ import annotations

import hashlib
import platform
import re
import shutil
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from vocabulary import RunStatus


@dataclass(frozen=True)
class SolverInfo:
    """What was run, precisely enough to run it again."""

    name: str
    version: str
    binary: str
    binary_sha256: str
    host: str

    @classmethod
    def probe(cls, name: str, binary: str, version_args: list[str],
              version_re: str) -> "SolverInfo":
        path = shutil.which(binary)
        if path is None:
            raise FileNotFoundError(
                f"{binary} is not on PATH; a run without a recorded binary "
                f"is not reproducible, so this is an error rather than a "
                f"skipped solver")
        out = subprocess.run([path] + version_args, capture_output=True,
                             text=True, timeout=30).stdout
        m = re.search(version_re, out)
        digest = hashlib.sha256(Path(path).read_bytes()).hexdigest()
        return cls(name, m.group(1) if m else "unrecorded", path,
                   digest, platform.node())


@dataclass(frozen=True)
class RunResult:
    """One solver, one query file, one outcome.

    ``premises`` holds the formula names the solver reported using, when it
    reported any.  Empty is a real answer for an unsatisfiable query whose
    contradiction lies in the target alone, and it is not the same as a
    solver that was never asked.
    """

    problem_id: str
    kind: str                     # inc | comp
    language: str                 # tptp | smt
    status: RunStatus
    seconds: float
    solver: SolverInfo
    command: tuple[str, ...]
    time_limit: int
    premises: tuple[str, ...] = ()
    raw: str = ""
    note: str = ""

    def line(self) -> str:
        return (f"{self.problem_id} {self.kind:4} {self.language:4} "
                f"{self.status!s:13} {self.seconds:6.2f}s "
                f"{len(self.premises)} premises")


class Adapter(Protocol):
    name: str
    language: str

    def info(self) -> SolverInfo: ...
    def command(self, path: Path, limit: int) -> list[str]: ...
    def read(self, out: str) -> tuple[RunStatus, tuple[str, ...], str]: ...


# --- Vampire ------------------------------------------------------------

_SZS = re.compile(r"SZS status (\w+)")
_PROOF = re.compile(r"% SZS output start Proof.*?% SZS output end Proof",
                    re.S)
_LEAF = re.compile(r"file\(\s*'[^']*'\s*,\s*([A-Za-z0-9_]+)\s*\)")

_SZS_MAP = {
    "unsatisfiable": RunStatus.UNSAT,
    "contradictoryaxioms": RunStatus.UNSAT,
    "satisfiable": RunStatus.SAT,
    "countersatisfiable": RunStatus.SAT,
    "timeout": RunStatus.TIMEOUT,
    "gaveup": RunStatus.UNDETERMINED,
}


@dataclass
class Vampire:
    """TPTP.

    ``--output_axiom_names on`` is not optional: without it the proof names
    every leaf ``unknown`` and the run is useless for attribution.  The
    schedule modes do not always propagate the flag to their children, so
    the mode is pinned too.
    """

    name: str = "vampire"
    language: str = "tptp"
    binary: str = "vampire"
    _info: SolverInfo | None = field(default=None, repr=False)

    def info(self) -> SolverInfo:
        if self._info is None:
            self._info = SolverInfo.probe(
                self.name, self.binary, ["--version"], r"([0-9][\w.]*)")
        return self._info

    def command(self, path: Path, limit: int) -> list[str]:
        return [self.info().binary, "--mode", "vampire", "--proof", "tptp",
                "--output_axiom_names", "on", "-t", str(limit), str(path)]

    def read(self, out: str) -> tuple[RunStatus, tuple[str, ...], str]:
        m = _SZS.search(out)
        if not m:
            return RunStatus.UNDETERMINED, (), "no SZS status in the output"
        status = _SZS_MAP.get(m.group(1).lower(), RunStatus.UNDETERMINED)
        if status is not RunStatus.UNSAT:
            return status, (), ""
        proof = _PROOF.search(out)
        if not proof:
            return status, (), "unsatisfiable but no proof block"
        names = list(dict.fromkeys(_LEAF.findall(proof.group(0))))
        if names and all(n == "unknown" for n in names):
            return status, (), ("every premise reported as unknown; "
                                "--output_axiom_names did not take effect")
        return status, tuple(names), ""


# --- Z3 -----------------------------------------------------------------

@dataclass
class Z3:
    """SMT-LIB.

    The core arrives on the line after ``unsat``.  An empty core is a real
    answer, meaning the target contradicts itself without any premise, and
    it is distinguished from a missing core by the parenthesised line being
    present but empty.
    """

    name: str = "z3"
    language: str = "smt"
    binary: str = "z3"
    _info: SolverInfo | None = field(default=None, repr=False)

    def info(self) -> SolverInfo:
        if self._info is None:
            self._info = SolverInfo.probe(
                self.name, self.binary, ["--version"], r"([0-9][\w.]*)")
        return self._info

    def command(self, path: Path, limit: int) -> list[str]:
        return [self.info().binary, f"-T:{limit}", str(path)]

    def read(self, out: str) -> tuple[RunStatus, tuple[str, ...], str]:
        lines = [l.strip() for l in out.splitlines() if l.strip()]
        status = next((l for l in lines
                       if l in ("sat", "unsat", "unknown")), None)
        if status is None:
            err = next((l for l in lines if l.startswith("(error")), "")
            return RunStatus.UNDETERMINED, (), err[:120]
        if status == "sat":
            return RunStatus.SAT, (), ""
        if status == "unknown":
            return RunStatus.UNKNOWN, (), "the solver's own unknown"
        i = lines.index("unsat")
        for line in lines[i + 1:]:
            if line.startswith("(") and not line.startswith("(error"):
                return (RunStatus.UNSAT,
                        tuple(n for n in line.strip("()").split() if n), "")
        return RunStatus.UNSAT, (), "unsatisfiable but no core reported"


# --- running ------------------------------------------------------------

def run(adapter: Adapter, path: Path, problem_id: str, kind: str,
        limit: int = 30) -> RunResult:
    """One solver on one file.

    A timeout at the process level is one second beyond the solver's own,
    so that a solver which honours its limit reports TIMEOUT itself and
    only one which does not gets killed.
    """
    cmd = adapter.command(path, limit)
    start = time.monotonic()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              timeout=limit + 1)
        out = proc.stdout + proc.stderr
        status, premises, note = adapter.read(out)
    except subprocess.TimeoutExpired:
        out, status, premises = "", RunStatus.TIMEOUT, ()
        note = "killed by the harness; the solver did not honour its limit"
    except OSError as e:
        out, status, premises, note = "", RunStatus.ERROR, (), str(e)[:120]

    return RunResult(
        problem_id=problem_id, kind=kind, language=adapter.language,
        status=status, seconds=time.monotonic() - start,
        solver=adapter.info(), command=tuple(cmd), time_limit=limit,
        premises=premises, raw=out, note=note)