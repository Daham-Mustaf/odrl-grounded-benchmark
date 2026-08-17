"""
run_certify.py
==============
Runs both queries of each problem under both provers, derives the verdict,
compares what the two refutations rest on, and writes the observed
certificate beside the expected one.

    uv run generators/run_certify.py
    uv run generators/run_certify.py --problem KGC311
    uv run generators/run_certify.py --prover vampire     # one only

Two provers, and what agreement between them means
--------------------------------------------------
Vampire reads the TPTP encoding, Z3 the SMT-LIB one.  The two are the same
theory: the writer emits the same three order axioms into both, quantified,
rather than instantiating them at whichever concepts a problem happens to
need.  So a disagreement on a status is a real disagreement, not an artefact
of one encoding being weaker.

The premise sets are compared at the level of provenance, not of names.  The
TPTP names come from the resource generator and say what each assertion is
(res_dpv_scientific_research_below_dpv_research_and_development); the SMT-LIB
ones are numbered by the writer (res_kgc311_0), because at that point it
knows only the order in which assertions appear.  Comparing the counts by
source is what the two can honestly be asked to agree on:

    Vampire  2 resource, 1 order axiom, 1 constraint
    Z3       2 resource, 1 order axiom, 1 constraint     agree

That is weaker than name-level agreement and worth strengthening later, by
having the problem data carry names for its SMT-LIB assertions.  Until then
the comparison says what it can: the two refutations use the same number of
assertions from the same places.

A caution the KGC311 run makes concrete: two provers may take different
routes through the same resource.  DPV publishes NonCommercialResearch under
two parents, so there are two chains from it to Purpose, and the provers do
not pick the same one.  Both refutations are correct and both cite two
resource assertions and transitivity; they are not the same two assertions.
Provenance-level agreement is therefore the right claim, and name-level
agreement would be the wrong one to want.

Unknown, and the models that report it
--------------------------------------
An Unknown has no refutation.  Both its queries are satisfiable, and what
their models disagree about is the question the resource leaves open.  Z3
prints a model for each; the difference between them is recorded as the
certificate, in place of the empty one an Unknown used to get.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from certificate import (premises_from_vampire, premises_from_z3, classify,
                         to_turtle, withdrawable, model_literals,
                         compare_models, NoAxiomNames, NoProof)

# --mode vampire rather than casc: the schedule mode does not always
# propagate --output_axiom_names to its child strategies, and without names
# no premise can be attributed.  --include makes the run independent of the
# working directory, so a reviewer can reproduce it from anywhere.
VAMPIRE = ["vampire", "--mode", "vampire", "--proof", "tptp",
           "--output_axiom_names", "on"]
Z3 = ["z3"]


def run_vampire(path: Path, timeout: int, root: Path) -> tuple[str, str]:
    """Returns (normalised status, raw output)."""
    try:
        r = subprocess.run(
            VAMPIRE + ["--include", str(root), "--time_limit", str(timeout),
                       str(path)],
            capture_output=True, text=True, timeout=timeout + 10)
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        return ("timeout" if isinstance(e, subprocess.TimeoutExpired)
                else "not-installed"), ""
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


def run_z3(path: Path, timeout: int) -> tuple[str, str]:
    """Returns (status, raw output).

    The file asks for both a core and a model.  Whichever does not apply
    produces an error line that Z3 prints and steps over, so both requests
    are always emitted and the reader takes what arrived.
    """
    try:
        r = subprocess.run(Z3 + [f"-T:{timeout}", str(path)],
                           capture_output=True, text=True,
                           timeout=timeout + 10)
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        return ("timeout" if isinstance(e, subprocess.TimeoutExpired)
                else "not-installed"), ""
    out = r.stdout + r.stderr
    status, _ = premises_from_z3(out)
    return status, out


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


def profile(classified: dict) -> dict:
    """Counts by provenance: what two provers can be compared on."""
    return {k: len(v) for k, v in classified.items() if v}


def constants_of(smt2: Path) -> list[str]:
    """The problem's concept constants, for reading a model."""
    text = smt2.read_text(encoding="utf-8")
    return re.findall(r"\(declare-fun (\w+) \(\) Concept\)", text)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--problems-dir", default="problems/verdict")
    ap.add_argument("--out-dir", default="certificates")
    ap.add_argument("--problem", default=None, help="one problem id")
    ap.add_argument("--prover", choices=("both", "vampire", "z3"),
                    default="both")
    ap.add_argument("--timeout", type=int, default=30)
    args = ap.parse_args()

    pdir, odir = Path(args.problems_dir), Path(args.out_dir)
    odir.mkdir(parents=True, exist_ok=True)
    root = pdir.parent

    pattern = f"{args.problem}-1.p" if args.problem else "*-1.p"
    problems = sorted(pdir.glob(pattern))
    if not problems:
        print(f"no problems matching {pdir}/{pattern}", file=sys.stderr)
        return 1

    use_v = args.prover in ("both", "vampire")
    use_z = args.prover in ("both", "z3")
    agree = disagree = 0

    for q1path in problems:
        pid = q1path.name[:-4]
        q2path = q1path.with_name(f"{pid}-2.p")
        s1 = s2 = None
        vout1 = vout2 = zout1 = zout2 = ""

        if use_v:
            s1, vout1 = run_vampire(q1path, args.timeout, root)
            s2, vout2 = run_vampire(q2path, args.timeout, root)
        if use_z:
            z1, zout1 = run_z3(q1path.with_suffix(".smt2"), args.timeout)
            z2, zout2 = run_z3(q2path.with_suffix(".smt2"), args.timeout)
            if s1 is None:
                s1, s2 = z1, z2
            elif (s1, s2) != (z1, z2):
                print(f"{pid}  STATUS DISAGREEMENT  "
                      f"vampire=({s1},{s2}) z3=({z1},{z2})")

        v = verdict_of(s1, s2)
        print(f"{pid}  q1={s1:8s} q2={s2:8s} -> {v}")

        # The refutation is whichever query came back unsatisfiable.
        which = 1 if s1 == "unsat" else 2 if s2 == "unsat" else None

        if which is None:
            if s1 not in ("sat", "unsat") or s2 not in ("sat", "unsat"):
                print(f"    no verdict: provers returned {s1} and {s2}")
                continue
            # Unknown.  Both queries have models; report what they differ on.
            if use_z and zout1 and zout2:
                syms = constants_of(q1path.with_suffix(".smt2"))
                m1 = model_literals(zout1, syms)
                m2 = model_literals(zout2, syms)
                diff = compare_models(m1, m2)
                if diff:
                    print(f"    two models, differing on: {', '.join(diff)}")
                    print(f"    that difference is the question the resource "
                          f"leaves open")
                else:
                    print("    two models; they agree on the constants, so "
                          "the difference lies in the order relation")
            else:
                print("    Unknown: two models; no refutation to attribute.")
            continue

        # --- a refutation: attribute it under each prover available -----
        profiles, classified_v = {}, None

        if use_v:
            raw = vout1 if which == 1 else vout2
            try:
                names = premises_from_vampire(raw)
                classified_v = classify(names)
                profiles["Vampire"] = profile(classified_v)
                (odir / f"{pid}-{which}.tstp").write_text(raw, encoding="utf-8")
            except (NoAxiomNames, NoProof) as e:
                print(f"    Vampire: {e}")

        if use_z:
            zraw = zout1 if which == 1 else zout2
            _, znames = premises_from_z3(zraw)
            if znames:
                cz = classify(znames)
                profiles["Z3"] = profile(cz)
                (odir / f"{pid}-{which}.core").write_text(
                    "\n".join(znames) + "\n", encoding="utf-8")

        if classified_v is not None:
            for source, ns in classified_v.items():
                if ns and source != "unclassified":
                    print(f"    {source:24s} {', '.join(ns)}")
            if classified_v["unclassified"]:
                print(f"    UNCLASSIFIED             "
                      f"{', '.join(classified_v['unclassified'])}")
            w = withdrawable(classified_v)
            print(f"    withdrawable             "
                  f"{', '.join(w) if w else 'none'}")

            ttl = to_turtle(pid, "Refutation", classified_v,
                            artefact=f"proofs/{pid}-{which}.tstp",
                            prover="Vampire")
            (odir / f"{pid}-observed.ttl").write_text(ttl + "\n",
                                                      encoding="utf-8")
            print(f"    -> {odir / f'{pid}-observed.ttl'}")

        # Provenance-level comparison.  Not names: see the module docstring.
        if len(profiles) == 2:
            a, b = profiles["Vampire"], profiles["Z3"]
            if a == b:
                agree += 1
                shape = ", ".join(f"{k.replace('from','').lower()} {v}"
                                  for k, v in sorted(a.items()))
                print(f"    both provers: {shape}")
            else:
                disagree += 1
                print(f"    PROVERS DIFFER  vampire={a}  z3={b}")

    if use_v and use_z:
        print(f"\nprovenance agreement: {agree} agree, {disagree} differ")
    return 0


if __name__ == "__main__":
    sys.exit(main())