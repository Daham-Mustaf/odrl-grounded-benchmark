"""
survey_proofs.py
================
Which inference rules the suite's refutations actually use.

    uv run generators/survey_proofs.py
    uv run generators/survey_proofs.py --problem KGC330 --show

Why measure before building
---------------------------
An independent certificate checker replays a refutation step by step.  How
much work that is depends entirely on which rules the prover reached for,
and that is a fact about these problems rather than about Vampire in
general.

The range is wide.  If the refutations are resolution and subsumption over
ground unit clauses, a checker is a few hundred lines and verifies every
step.  If they use superposition with ordering constraints, or AVATAR
splitting, or definition introduction during clausification, replaying them
independently is the problem that proof-reconstruction projects exist to
solve, and a checker that skipped those steps while calling itself complete
would be worse than one that never claimed to be.

The premises here are ground: order assertions are atoms, declared
distinctness is a ground inequation, and the witness condition is
quantifier-free.  Only the three order axioms and declared disjointness are
quantified.  So the expectation is that most refutations are propositional
with a few instantiations, but that is a prediction, and this script exists
to replace it with a count.

What it reports
---------------
Per problem, the rules its refutation used and how many steps.  Across the
suite, a table of rules by frequency, split into the ones a ground checker
can verify and the ones it cannot, with the problems that need each.

The last column is the one that matters: the number of problems whose
refutation lies entirely within the checkable set.  That is the coverage a
checker would have on the day it was written, and it is what an honest
description of the certificate system would report.

Proof formats
-------------
With --proof tptp Vampire prints steps as annotated formulas,
inference(rule_name, ...), rule names with underscores; the default text
format prints "42. $false [rule name 40,41]" with spaces.  This script
parses both and normalises underscores to spaces, so the classification
sets below are written once, and the parser also survives strategies
(CASC schedule children) that fall back to the text format.
"""
import argparse
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

# Rules a checker over ground clauses can verify without an order, a
# unification algorithm, or a clausifier.  Everything else needs machinery,
# and the point of the split is to say how much.  rectify, ennf and nnf
# transformations are boolean-only on ground input and every fof input
# passes through them, so they sit here; on our inputs a checker verifies
# any such step propositionally.
GROUND_CHECKABLE = {
    "resolution",
    "subsumption resolution",
    "factoring",
    "duplicate literal removal",
    "trivial inequality removal",
    "cnf transformation",          # trivial when the input is already clausal
    "ennf transformation",
    "nnf transformation",
    "rectify",
    "flattening",
    "unused predicate definition removal",
    "pure predicate removal",
    "true and false elimination",
}

# Rules that need equality reasoning.  Reachable, but a checker must
# implement congruence, and these are the ones the outstanding premise-list
# correction is about.
EQUALITY = {
    "superposition",
    "forward demodulation",
    "backward demodulation",
    "equality resolution",
    "equality factoring",
    "trivial equality removal",
}

# Rules that need a splitting architecture, skolemisation, or definition
# introduction: preprocessing that changes the problem before the proof
# begins.  Skolemisation should not occur on these inputs (all
# quantification is universal); if it appears, that is a finding.
STRUCTURAL = {
    "avatar splitting",
    "avatar component clause",
    "avatar contradiction clause",
    "avatar split clause",
    "avatar sat refutation",
    "definition unfolding",
    "definition folding",
    "skolemisation",
    "choice axiom",
}

_PROOF = re.compile(r"% SZS output start Proof.*?% SZS output end Proof",
                    re.S)
# tptp proof format: inference(subsumption_resolution,[],[f56,f30])
_STEP_TPTP = re.compile(r"inference\(([a-z][a-z0-9_]*)")
# default text format: 42. $false [subsumption resolution 40,41]
_STEP_TEXT = re.compile(
    r"^\s*\d+\.\s.*\[([a-z][a-z _-]*[a-z])(?:\s+[\d,]+)?\]\s*$", re.M)
_SZS = re.compile(r"SZS status (\w+)")

VAMPIRE = ["--mode", "vampire", "--proof", "tptp",
           "--output_axiom_names", "on", "--proof_extra", "full"]


def classify(rule: str) -> str:
    r = rule.strip().lower()
    if r in GROUND_CHECKABLE:
        return "ground"
    if r in EQUALITY:
        return "equality"
    if r in STRUCTURAL:
        return "structural"
    for known, label in ((GROUND_CHECKABLE, "ground"),
                         (EQUALITY, "equality"),
                         (STRUCTURAL, "structural")):
        if any(r.startswith(k) for k in known):
            return label
    return "unclassified"


def extract_rules(proof_text: str) -> Counter:
    """Rule frequencies from a proof block, either format.

    Leaves are not inference steps: the tptp format marks them file(...)
    and is untouched by the inference() pattern; in the text format they
    appear as [input ...] and are skipped by name.
    """
    names = _STEP_TPTP.findall(proof_text)
    if not names:
        names = _STEP_TEXT.findall(proof_text)
    rules: Counter = Counter()
    for n in names:
        r = n.replace("_", " ").strip().lower()
        if r == "input" or r.startswith("input "):
            continue
        rules[r] += 1
    return rules


def run_one(path: Path, limit: int, binary: str, show: bool, include: Path):
    cmd = [binary, "--include", str(include)] + VAMPIRE + \
          ["-t", str(limit), str(path)]
    out = subprocess.run(cmd, capture_output=True, text=True,
                         timeout=limit + 5).stdout
    m = _SZS.search(out)
    status = m.group(1).lower() if m else "no-status"
    if status not in ("unsatisfiable", "contradictoryaxioms"):
        return status, Counter(), 0
    proof = _PROOF.search(out)
    if not proof:
        return "unsat-no-proof", Counter(), 0
    if show:
        print(proof.group(0))
    rules = extract_rules(proof.group(0))
    return status, rules, sum(rules.values())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[3])
    ap.add_argument("--dir", default="problems/verdict", type=Path)
    ap.add_argument("--binary", default="vampire")
    ap.add_argument("--limit", type=int, default=30)
    ap.add_argument("--include", default="problems", type=Path,
                    help="root for include() directives; run_verdict.sh "
                         "passes the same")
    ap.add_argument("--problem", help="one problem id, both queries")
    ap.add_argument("--show", action="store_true",
                    help="print the proof text as well")
    args = ap.parse_args()

    files = sorted(args.dir.glob("*.p"))
    if args.problem:
        files = [f for f in files if f.stem.startswith(args.problem)]
    if not files:
        print(f"no .p files in {args.dir}", file=sys.stderr)
        return 1

    per_problem: dict[str, Counter] = {}
    per_class: dict[str, set] = defaultdict(set)
    totals: Counter = Counter()
    statuses: Counter = Counter()

    print(f"{'file':16} {'status':16} {'steps':>6}   rules")
    for f in files:
        try:
            status, rules, steps = run_one(f, args.limit, args.binary,
                                           args.show, args.include)
        except FileNotFoundError:
            print(f"{args.binary} is not on PATH", file=sys.stderr)
            return 1
        except subprocess.TimeoutExpired:
            status, rules, steps = "timeout", Counter(), 0
        statuses[status] += 1
        per_problem[f.stem] = rules
        totals.update(rules)
        for r in rules:
            per_class[classify(r)].add(f.stem)
        top = ", ".join(f"{r} x{n}" for r, n in rules.most_common(4))
        print(f"{f.stem:16} {status:16} {steps:>6}   {top}")

    print()
    print("rules across the suite")
    for r, n in totals.most_common():
        print(f"  {n:5}  {r:34} {classify(r)}")

    print()
    print("problems by the machinery their refutation needs")
    for label in ("ground", "equality", "structural", "unclassified"):
        ids = sorted(per_class.get(label, ()))
        print(f"  {label:13} {len(ids):3}   "
              f"{', '.join(ids[:6])}{' ...' if len(ids) > 6 else ''}")

    refuted = [p for p, r in per_problem.items() if r]
    ground_only = [p for p in refuted
                   if all(classify(r) == "ground" for r in per_problem[p])]
    plus_eq = [p for p in refuted
               if all(classify(r) in ("ground", "equality")
                      for r in per_problem[p])]
    print()
    print(f"refutations found              : {len(refuted)}")
    print(f"checkable by a ground checker  : {len(ground_only)}")
    print(f"checkable if equality is added : {len(plus_eq)}")
    print(f"needing structural machinery   : "
          f"{len(refuted) - len(plus_eq)}")

    if statuses:
        print()
        print("statuses:", dict(statuses))

    unclassified = [r for r in totals if classify(r) == "unclassified"]
    if unclassified:
        print()
        print("rules this script does not classify; add them to one of the "
              "three sets before reading the coverage figures:")
        for r in sorted(unclassified):
            print(f"  {r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())