#!/usr/bin/env python3
"""
closed_world.py
===============
What a checker that reads the resource as complete reports for each test case.

    uv run generators/closed_world.py [--out results/closed-world.csv] [--limit 300]

The closed world has one structure: the published order statements and nothing
else.  It is built in three steps.

  - The order is the reflexive and transitive closure of the statements of R.
  - Every loop of that order is collapsed to one concept, since an order is
    antisymmetric.  The loops are reported.  In DPV Locations they should all
    come from the identity pairs, each written as two statements; a loop that
    does not is printed as one beyond them.
  - The structure must satisfy every statement of R and of the declarations the
    test case names, or the run fails.  Nothing here assumes the declarations:
    the structure either satisfies them or does not.

The input checks stay: a rejected test case and a control keep their outcome.
Every other test case gets the truth of its condition in that structure: true
is Compatible and false is Incompatible, and the closed world is never Unknown.
The condition evaluated is the full formula, which tries every concept of the
vocabulary in every part (compile.py, full=True).  It must have the same truth
as the formula the queries carry, or the run fails.

Since the structure satisfies R and the declarations, a verdict that holds in
every such structure holds in this one.  The run fails if the closed world
disagrees with a Compatible or an Incompatible verdict.

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

The names are those of the formula the queries carry.  The verdict so reached
must be the closed world's, or the run fails.

Exit 1 if any of these checks fails, or a test case gets no kind.
"""

import argparse
import csv
import importlib
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

import declarations
import provers
import table_data
import vocabulary
from compile import constants_in, tree_term
from tree_expand import _map_item, _parse_assertions, constants_of_tree

VERDICT = ROOT / "problems" / "verdict"
AXIOMS = ROOT / "problems" / "axioms"
MODULES = ["problem_data_motivating", "problem_data_geonames",
           "problem_data_dpv", "problem_data_dpvloc",
           "problem_data_filetype", "problem_data_consent",
           "problem_data_tom", "problem_data_bcp47"]
SZS = {"Satisfiable": "sat", "CounterSatisfiable": "sat",
       "Unsatisfiable": "unsat", "Theorem": "unsat",
       "ContradictoryAxioms": "unsat"}


class Failed(Exception):
    """A check of this script did not hold."""


def strongly_connected(nodes, edges) -> list:
    """The strongly connected components of a graph, iteratively: DPV Locations
    has five thousand concepts and a recursive walk has no need to be deep, but
    nothing here should depend on how deep the data happens to be."""
    succ = defaultdict(list)
    for a, b in edges:
        succ[a].append(b)
    index, low, on, stack, out, n = {}, {}, set(), [], [], 0
    for root in nodes:
        if root in index:
            continue
        work = [(root, iter(succ[root]))]
        index[root] = low[root] = n
        n += 1
        stack.append(root)
        on.add(root)
        while work:
            v, it = work[-1]
            for w in it:
                if w not in index:
                    index[w] = low[w] = n
                    n += 1
                    stack.append(w)
                    on.add(w)
                    work.append((w, iter(succ[w])))
                    break
                if w in on:
                    low[v] = min(low[v], index[w])
            else:
                work.pop()
                if work:
                    low[work[-1][0]] = min(low[work[-1][0]], low[v])
                if low[v] == index[v]:
                    comp = []
                    while True:
                        w = stack.pop()
                        on.discard(w)
                        comp.append(w)
                        if w == v:
                            break
                    out.append(sorted(comp))
    return out


class Structure:
    """The one structure of the closed world over a resource's statements."""

    def __init__(self, concepts, statements):
        """statements: (label, below, above) for each order statement of R."""
        self.statements = statements
        edges = [(a, b) for _, a, b in statements]
        nodes = list(dict.fromkeys(list(concepts) + [x for e in edges for x in e]))
        self.nodes = nodes
        comps = strongly_connected(nodes, edges)
        self.cls = {x: comp[0] for comp in comps for x in comp}
        self.loops = [comp for comp in comps if len(comp) > 1]
        self.up = defaultdict(set)
        for a, b in edges:
            if self.cls[a] != self.cls[b]:
                self.up[self.cls[a]].add(self.cls[b])
        self.memo = {}

    def above(self, a: str) -> set:
        """The classes at or above the class of a."""
        start = self.cls.get(a, a)
        if start not in self.memo:
            seen, todo = {start}, [start]
            while todo:
                for b in self.up.get(todo.pop(), ()):
                    if b not in seen:
                        seen.add(b)
                        todo.append(b)
            self.memo[start] = seen
        return self.memo[start]

    def leq(self, a: str, b: str) -> bool:
        return self.cls.get(b, b) in self.above(a)

    def same(self, a: str, b: str) -> bool:
        return self.cls.get(a, a) == self.cls.get(b, b)

    def loops_beyond_identity(self) -> list:
        """The loops that are not exactly a class of the identity statements."""
        identity = [(a, b) for label, a, b in self.statements if "_same_" in label]
        classes = [set(c) for c in strongly_connected(
            list(dict.fromkeys(x for e in identity for x in e)), identity)]
        return [loop for loop in self.loops if set(loop) not in classes]

    def check_resource(self) -> None:
        for label, a, b in self.statements:
            if not self.leq(a, b):
                raise Failed(f"the structure does not satisfy {label}")

    def check_declarations(self, decl) -> None:
        """Every statement the set makes, over the whole set."""
        constant = declarations.constant_for(decl.applies_to[0])
        members = [constant(m) for m in decl.members]
        classes = defaultdict(list)
        for m in members:
            classes[self.cls.get(m, m)].append(m)
        for names in classes.values():
            if len(names) > 1:
                raise Failed(f"{decl.iri} declares {', '.join(names)} distinct, "
                             f"and the structure makes them one concept")
        for x, y in decl.disjoint:
            a, b = constant(x), constant(y)
            for c in self.nodes:
                if self.leq(c, a) and self.leq(c, b):
                    raise Failed(f"{decl.iri} declares nothing below both {a} "
                                 f"and {b}, and {c} lies below both")


def value(t, model: Structure) -> bool:
    """The truth of a formula, as compile.py builds it, in the structure."""
    kind = t[0]
    if kind == "true":
        return True
    if kind == "false":
        return False
    if kind == "eq":
        return model.same(t[1], t[2])
    if kind == "leq":
        return model.leq(t[1], t[2])
    if kind == "not":
        return not value(t[1], model)
    if kind == "and":
        return all(value(x, model) for x in t[1])
    if kind == "or":
        return any(value(x, model) for x in t[1])
    raise ValueError(f"not a formula: {kind}")


def status(query: Path, extra: list, limit: int) -> str:
    """Vampire's status for the query with the statements added."""
    text = query.read_text(encoding="utf-8") + "\n".join(extra) + "\n"
    with tempfile.NamedTemporaryFile("w", suffix=".p", delete=False,
                                     encoding="utf-8") as f:
        f.write(text)
    try:
        out = subprocess.run(
            [provers.vampire(), "--include", str(ROOT / "problems"), "--mode", "casc",
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
        raise Failed(f"{cid}: no status within {limit} s ({one}, {two})")
    if one == two == "unsat":
        raise Failed(f"{cid}: the added statements have no model")
    if one == "unsat":
        return "I"
    return "C" if two == "unsat" else None


def apart(pairs) -> list:
    return [f"fof(cw_{i}, axiom, {a} != {b})." for i, (a, b) in enumerate(pairs)]


def kind_of(cid: str, names, model: Structure, verdict: str, limit: int) -> str:
    pairs = list(combinations(names, 2))
    unrelated = [(a, b) for a, b in pairs
                 if not model.leq(a, b) and not model.leq(b, a)]
    # A published identity stays one: the closed world assumes no difference
    # between two names the statements make one.
    related = [(a, b) for a, b in pairs
               if (a, b) not in set(unrelated) and not model.same(a, b)]
    for name, extra in (("distinctness", apart(unrelated)),
                        ("identity", apart(unrelated + related))):
        got = settled(cid, extra, limit)
        if got is not None:
            if got != verdict:
                raise Failed(f"{cid}: {name} gives {got}, the closed world "
                             f"gives {verdict}")
            return name
    return "order"


def problems_by_id() -> dict:
    out = {}
    for module in MODULES:
        for p in importlib.import_module(module).PROBLEMS:
            out[p["id"]] = p
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[3])
    ap.add_argument("--out", default=ROOT / "results" / "closed-world.csv",
                    type=Path)
    ap.add_argument("--limit", type=int,
                    default=int(os.environ.get("PROVER_LIMIT", 300)))
    args = ap.parse_args()
    args.out = args.out.resolve()
    os.chdir(ROOT)      # declarations and vocabulary read relative paths

    problems = problems_by_id()
    structures, checked = {}, set()
    rows, failures = [], []
    for case in table_data.read_cases(ROOT / "cases"):
        cid, expected = case["id"], case["outcome"]
        kind, got = "", "?"
        if expected in ("rejected", "control"):
            rows.append((cid, expected, expected, "yes", ""))
            continue
        try:
            p = problems[cid]
            tree = p["tree"]
            if p.get("grounding"):
                tree = [_map_item(i, p["grounding"]) for i in tree]
            candidates = vocabulary.candidates(p["resource"],
                                               constants_of_tree(tree))
            key = p["resource"]
            if key not in structures:
                statements = []
                for name in p["includes"]:
                    if name.startswith("KGE"):
                        continue
                    text = (AXIOMS / name).read_text(encoding="utf-8")
                    statements += [(label, *a) for label, k, a in
                                   _parse_assertions(text) if k == "leq"]
                structures[key] = Structure(vocabulary.concepts(key), statements)
                structures[key].check_resource()
            model = structures[key]
            decl = declarations.set_for(p.get("background_theory"))
            if decl is not None and (key, decl.iri) not in checked:
                model.check_declarations(decl)
                checked.add((key, decl.iri))

            holds = value(tree_term(tree, candidates, p["sort"], full=True), model)
            carried = tree_term(tree, candidates, p["sort"])
            if value(carried, model) != holds:
                raise Failed(f"{cid}: the full formula and the query's differ "
                             f"in the closed world")
            got = "C" if holds else "I"
            if expected in ("C", "I") and got != expected:
                raise Failed(f"{cid}: the verdict is {expected}, and the closed "
                             f"world gives {got}")
            if expected == "U":
                kind = kind_of(cid, constants_in(carried), model, got, args.limit)
        except Failed as e:
            print(f"FAILED: {e}", file=sys.stderr)
            failures.append(cid)
            kind = "?" if expected == "U" else ""
        rows.append((cid, expected, got, "yes" if got == expected else "no", kind))

    print("resource                concepts  loops  beyond the identity pairs")
    for key, model in sorted(structures.items()):
        beyond = model.loops_beyond_identity()
        print(f"{key.rsplit('/', 1)[-1]:22}  {len(model.nodes):8}  "
              f"{len(model.loops):5}  {len(beyond)}")
        for loop in beyond:
            print(f"    LOOP BEYOND THE IDENTITY PAIRS: {', '.join(loop)}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["case", "expected", "closed_world", "reproduced", "kind"])
        w.writerows(rows)
    same = sum(1 for r in rows if r[3] == "yes")
    print(f"structures checked against R and {len(checked)} sets of declarations")
    print(f"wrote {args.out.relative_to(ROOT) if args.out.is_relative_to(ROOT) else args.out}: "
          f"{same} of {len(rows)} outcomes reproduced")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
