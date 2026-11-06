#!/usr/bin/env python3
"""
closed_world.py
===============
What a checker that reads the resource as complete reports for each test case.

    uv run generators/closed_world.py [--out results/closed-world.csv] [--limit 300]

The closed world has one model: the published order statements and nothing
else.  A concept is below another only if the statements say so, and two names
are one concept only if the statements place each below the other.  Nothing
else changes: the same witness condition, the same sort check, the same
grounding.  So a case with queries gets Compatible when its witness condition
holds in that model and Incompatible when it does not, and is never Unknown.
A case without queries, rejected or an accepted control, keeps its outcome.

The witness condition is read from the case's first query, and the second
query's must be its negation.

results/closed-world.csv has one row per test case,

    case,expected,closed_world,reproduced,kind

kind is written for each Unknown test case, and names the statement the closed
world assumes to settle it.  Each is tried with both queries under the
resource, by Vampire, adding statements until one query is unsatisfiable:

    distinctness   two names no statement relates are different concepts
    identity       two names one statement orders are different concepts, so
                   the order does not also run the other way
    order          a concept is not below another; no statement of difference
                   between names settles the case

The names are those of the witness condition.  The verdict so reached must be
the closed world's, or this script stops.

Exit 1 if a case's kind cannot be determined.
"""

import argparse
import csv
import os
import re
import subprocess
import sys
import tempfile
from collections import defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).parent))

import table_data

VERDICT = ROOT / "problems" / "verdict"
AXIOMS = ROOT / "problems" / "axioms"
ORDER = re.compile(r"kge_leq\(\s*([a-z]\w*)\s*,\s*([a-z]\w*)\s*\)")
SZS = {"Satisfiable": "sat", "CounterSatisfiable": "sat",
       "Unsatisfiable": "unsat", "Theorem": "unsat",
       "ContradictoryAxioms": "unsat"}


def witness(path: Path) -> str:
    """The witness formula of a query, as written."""
    m = re.search(r"^fof\(w_\w+,\s*axiom,\s*(.*?)\)\.\s*$",
                  path.read_text(encoding="utf-8"), re.M | re.S)
    if not m:
        raise ValueError(f"{path.name}: no witness formula")
    return m.group(1)


def includes(path: Path) -> list:
    return re.findall(r"^include\('axioms/([^']+)'\)\.",
                      path.read_text(encoding="utf-8"), re.M)


def published(query: Path) -> dict:
    """Each concept and the concepts the query's resource places it below."""
    up = defaultdict(set)
    for name in includes(query):
        text = (AXIOMS / name).read_text(encoding="utf-8")
        for a, b in re.findall(
                r"^fof\(\S+,\s*axiom,\s*\n?\s*kge_leq\(\s*([a-z]\w*)\s*,\s*"
                r"([a-z]\w*)\s*\)\)\.", text, re.M):
            up[a].add(b)
    return up


class ClosedWorld:
    """The one model: the reflexive and transitive closure of the statements."""

    def __init__(self, up: dict):
        self.up = up
        self.memo = {}

    def above(self, a: str) -> set:
        if a not in self.memo:
            seen, stack = {a}, [a]
            while stack:
                for b in self.up.get(stack.pop(), ()):
                    if b not in seen:
                        seen.add(b)
                        stack.append(b)
            self.memo[a] = seen
        return self.memo[a]

    def leq(self, a: str, b: str) -> bool:
        return b in self.above(a)

    def same(self, a: str, b: str) -> bool:
        return self.leq(a, b) and self.leq(b, a)


def evaluate(formula: str, model: ClosedWorld) -> bool:
    """The truth of a ground formula in the model."""
    expr = ORDER.sub(lambda m: f"L('{m.group(1)}','{m.group(2)}')", formula)
    expr = re.sub(r"\b([a-z]\w*)\s*!=\s*([a-z]\w*)\b",
                  lambda m: f"(not S('{m.group(1)}','{m.group(2)}'))", expr)
    expr = re.sub(r"\b([a-z]\w*)\s*=\s*([a-z]\w*)\b",
                  lambda m: f"S('{m.group(1)}','{m.group(2)}')", expr)
    expr = (expr.replace("$true", "True").replace("$false", "False")
            .replace("~", " not ").replace("&", " and ").replace("|", " or "))
    if re.search(r"[!?\[\]]", expr):
        raise ValueError(f"not a ground formula: {formula[:80]}")
    expr = " ".join(expr.split())
    return bool(eval(expr, {"__builtins__": {}},  # the repository's own files
                     {"L": model.leq, "S": model.same}))


def names_in(formula: str) -> list:
    bare = re.sub(r"\$\w+", " ", formula)
    return sorted(set(re.findall(r"\b[a-z]\w*\b", bare)) - {"kge_leq"})


def status(query: Path, extra: list, limit: int) -> str:
    """Vampire's status for the query with the statements added."""
    text = query.read_text(encoding="utf-8") + "\n".join(extra) + "\n"
    with tempfile.NamedTemporaryFile("w", suffix=".p", delete=False,
                                     encoding="utf-8") as f:
        f.write(text)
    try:
        out = subprocess.run(
            ["vampire", "--include", str(ROOT / "problems"), "--mode", "casc",
             "--time_limit", str(limit), f.name],
            capture_output=True, text=True, timeout=limit + 30).stdout
    except subprocess.TimeoutExpired:
        return "timeout"
    finally:
        os.unlink(f.name)
    m = re.search(r"SZS status (\w+)", out)
    return SZS.get(m.group(1), m.group(1)) if m else "no-status"


def settled(cid: str, extra: list, limit: int):
    """The verdict with the statements added, or None if it is still Unknown."""
    one = status(VERDICT / f"{cid}-1.p", extra, limit)
    two = status(VERDICT / f"{cid}-2.p", extra, limit)
    if {one, two} - {"sat", "unsat"}:
        raise RuntimeError(f"{cid}: no status within {limit} s ({one}, {two})")
    if one == two == "unsat":
        raise RuntimeError(f"{cid}: the added statements have no model")
    if one == "unsat":
        return "I"
    return "C" if two == "unsat" else None


def apart(pairs) -> list:
    return [f"fof(cw_{i}, axiom, {a} != {b})." for i, (a, b) in enumerate(pairs)]


def kind_of(cid: str, formula: str, model: ClosedWorld, verdict: str,
            limit: int) -> str:
    pairs = list(combinations(names_in(formula), 2))
    unrelated = [(a, b) for a, b in pairs
                 if not model.leq(a, b) and not model.leq(b, a)]
    related = [p for p in pairs if p not in set(unrelated)]
    # The published identities stay identities: the closed world assumes
    # no difference between them.
    related = [(a, b) for a, b in related if not model.same(a, b)]

    for name, extra in (("distinctness", apart(unrelated)),
                        ("identity", apart(unrelated + related))):
        got = settled(cid, extra, limit)
        if got is not None:
            if got != verdict:
                raise RuntimeError(f"{cid}: {name} gives {got}, the closed "
                                   f"world gives {verdict}")
            return name
    return "order"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[3])
    ap.add_argument("--out", default=ROOT / "results" / "closed-world.csv",
                    type=Path)
    ap.add_argument("--limit", type=int,
                    default=int(os.environ.get("PROVER_LIMIT", 300)))
    args = ap.parse_args()

    rows, failed = [], 0
    for case in table_data.read_cases(ROOT / "cases"):
        cid, expected = case["id"], case["outcome"]
        kind = ""
        if expected in ("rejected", "control"):
            got = expected
        else:
            one, two = VERDICT / f"{cid}-1.p", VERDICT / f"{cid}-2.p"
            formula = witness(one)
            model = ClosedWorld(published(one))
            holds = evaluate(formula, model)
            if evaluate(witness(two), model) == holds:
                raise ValueError(f"{cid}: query 2 does not negate query 1")
            got = "C" if holds else "I"
            if expected == "U":
                try:
                    kind = kind_of(cid, formula, model, got, args.limit)
                except RuntimeError as e:
                    print(f"    {e}", file=sys.stderr)
                    kind, failed = "?", failed + 1
        rows.append((cid, expected, got,
                     "yes" if got == expected else "no", kind))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["case", "expected", "closed_world", "reproduced", "kind"])
        w.writerows(rows)
    same = sum(1 for r in rows if r[3] == "yes")
    print(f"wrote {args.out}: {same} of {len(rows)} outcomes reproduced")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
