"""
test_end_to_end.py
==================
The verdict the pipeline gives against the verdict the definitions give, on
random problems small enough to decide by enumeration.

    uv run tests/test_end_to_end.py                     # 2000 random + 4 fixed
    uv run tests/test_end_to_end.py --count 500 --vampire 50
    uv run tests/test_end_to_end.py --keep /tmp/e2e     # keep the queries

What a problem is
-----------------
Three or four concepts; published order statements between them, at random,
and none when the concepts are read as names only (nom); a set of
declarations at random (distinctness over some of the concepts, disjointness
between some pairs at tax and mer, or none), written as RDF and read through
declarations.py like every set in problems/background; a sort at random; and
two policies drawn from every operator the signature admits at that sort,
some of their constraints inside or and xone.  Four fixed problems are added,
each one a named-only witness gets wrong:

  F1  isA a against isA b, where the two meet only in a third concept
  F2  neq a against neq b, the three concepts declared distinct
  F3  hasPart a against hasPart b, with a common concept above both
  F4  xone whose negated alternative is met only by a concept neither
      policy names

The verdict from the definitions
--------------------------------
Every structure over the concepts (every partition, then every partial order
on its blocks, from test_witness.py) that satisfies the published statements
and the declarations.  In each, every non-empty set of blocks is tried as the
use, by the satisfaction modes of Definition Valuation.  Compatible if every
structure admits a use, Incompatible if none does, Unknown otherwise.  A
problem with no structure at all is skipped.

The verdict from the pipeline
-----------------------------
The problem goes through expand_tree, write_fof and write_smt2 as they are.
Z3 decides both queries of every problem; Vampire those of a sample.  The
verdict is read from the pair as run_verdict.sh reads it.

Every disagreement is printed in full: the problem, the verdict from the
definitions with a structure that shows it, and what each prover said.

The test runs against a checkout from before the whole-vocabulary witness as
well (to show that it finds that defect): there the declarations were the
problem data's to instantiate, for the pairs of concepts a problem names, and
the shim below does what the case data did then.
"""

import argparse
import itertools
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "generators"))
sys.path.insert(0, str(ROOT / "tests"))

import test_witness as TW                      # noqa: E402
import declarations                            # noqa: E402
from compile import Constraint, Or, Xone       # noqa: E402
from signature import SIGNATURE, NOM, TAX, MER  # noqa: E402
from tree_expand import expand_tree            # noqa: E402
from writers import write_fof, write_smt2      # noqa: E402

try:
    import vocabulary                          # noqa: E402
except ImportError:                            # before the change
    vocabulary = None

NS = "https://w3id.org/odrl-kb/test/"
NAMES = ("ca", "cb", "cc", "cd")
SEED = 20261030
LIMIT = 30


# --------------------------------------------------------------------------
# Problems
# --------------------------------------------------------------------------

def admitted(sort):
    return sorted(op for op, (sorts, _) in SIGNATURE.items() if sort in sorts)


def constraint(rng, op, names, side):
    if SIGNATURE[op][1] == "n":
        values = tuple(rng.sample(names, rng.choice((1, 2))))
    else:
        values = (rng.choice(names),)
    return Constraint(op, values, side)


def policy(rng, sort, names, side):
    ops = admitted(sort)
    items = []
    for _ in range(rng.choice((1, 2))):
        r = rng.random()
        if r < 0.6:
            items.append(constraint(rng, rng.choice(ops), names, side))
        else:
            alts = tuple(constraint(rng, rng.choice(ops), names, side)
                         for _ in range(2))
            items.append(Or(alts) if r < 0.8 else Xone(alts))
    return items


def random_problem(rng, i):
    n = rng.choice((3, 4))
    names = list(NAMES[:n])
    sort = rng.choice((NOM, TAX, MER))
    edges = []
    if sort != NOM:
        edges = [(a, b) for a in names for b in names
                 if a != b and rng.random() < 0.22]
    kind = rng.choice(("none", "distinct", "disjoint") if sort != NOM
                      else ("none", "distinct"))
    members, disjoint = [], []
    if kind == "distinct":
        members = rng.sample(names, rng.choice(range(2, n + 1)))
    elif kind == "disjoint":
        pairs = list(itertools.combinations(names, 2))
        disjoint = rng.sample(pairs, rng.choice((1, 2)))
    tree = policy(rng, sort, names, "offer") + policy(rng, sort, names, "request")
    return dict(pid=f"E{i:04d}", names=names, sort=sort, edges=edges,
                members=members, disjoint=disjoint, tree=tree)


def fixed_problems():
    a, b, c = "ca", "cb", "cc"
    C = lambda op, *v, side="offer": Constraint(op, tuple(v), side)
    return [
        dict(pid="F1", names=[a, b, c], sort=TAX, edges=[(c, a), (c, b)],
             members=[], disjoint=[],
             tree=[C("isA", a), C("isA", b, side="request")]),
        dict(pid="F2", names=[a, b, c], sort=NOM, edges=[],
             members=[a, b, c], disjoint=[],
             tree=[C("neq", a), C("neq", b, side="request")]),
        dict(pid="F3", names=[a, b, c], sort=MER, edges=[(a, c), (b, c)],
             members=[], disjoint=[],
             tree=[C("hasPart", a), C("hasPart", b, side="request")]),
        dict(pid="F4", names=[a, b, c], sort=NOM, edges=[],
             members=[a, b, c], disjoint=[],
             tree=[Xone((C("isAnyOf", a, b), C("eq", a))),
                   C("isNoneOf", b, side="request")]),
    ]


def describe(pr) -> str:
    def item(it):
        if isinstance(it, Constraint):
            return f"{it.operator} {' '.join(it.values)}"
        kind = "or" if isinstance(it, Or) else "xone"
        return f"{kind}({', '.join(item(c) for c in it.alts)})"
    sides = {}
    for it in pr["tree"]:
        side = it.side if isinstance(it, Constraint) else it.alts[0].side
        sides.setdefault(side, []).append(item(it))
    decl = ("distinct " + " ".join(pr["members"]) if pr["members"] else
            "disjoint " + ", ".join(f"{x}/{y}" for x, y in pr["disjoint"])
            if pr["disjoint"] else "none")
    return (f"sort {pr['sort']}; concepts {' '.join(pr['names'])}; "
            f"published {', '.join(f'{x}<={y}' for x, y in pr['edges']) or 'none'}; "
            f"declarations {decl}\n"
            f"        offer   {' and '.join(sides.get('offer', []))}\n"
            f"        request {' and '.join(sides.get('request', []))}")


# --------------------------------------------------------------------------
# The verdict from the definitions
# --------------------------------------------------------------------------

_STRUCTURES = {}


def structures(names):
    key = tuple(names)
    if key not in _STRUCTURES:
        _STRUCTURES[key] = list(TW.structures(names))
    return _STRUCTURES[key]


def admissible(M, pr) -> bool:
    if any(not M.below(a, b) for a, b in pr["edges"]):
        return False
    if any(M.same(a, b) for a, b in itertools.combinations(pr["members"], 2)):
        return False
    for a, b in pr["disjoint"]:
        ha, hb = M.block_of(a), M.block_of(b)
        if any(M.leq[x][ha] and M.leq[x][hb] for x in M.domain()):
            return False
    return True


def a_use(M, tree):
    dom = list(M.domain())
    for r in range(1, len(dom) + 1):
        for S in itertools.combinations(dom, r):
            if TW.tree_satisfies(tree, set(S), M):
                return set(S)
    return None


def definitional(pr):
    """(verdict, a structure with a use, a structure without one)."""
    with_use = without = None
    count = 0
    for M in structures(pr["names"]):
        if not admissible(M, pr):
            continue
        count += 1
        S = a_use(M, pr["tree"])
        if S is not None and with_use is None:
            with_use = (M, S)
        if S is None and without is None:
            without = M
        if with_use and without:
            break
    if count == 0:
        return None, None, None
    verdict = ("Unknown" if with_use and without else
               "Compatible" if with_use else "Incompatible")
    return verdict, with_use, without


def show_use(M, S):
    groups = {}
    for k, name in enumerate(M.names):
        groups.setdefault(M.h[k], []).append(name)
    return "{" + ", ".join("=".join(sorted(groups[b])) for b in sorted(S)) + "}"


# --------------------------------------------------------------------------
# The verdict from the pipeline
# --------------------------------------------------------------------------

def constant_of(iri: str) -> str:
    return str(iri).rsplit("/", 1)[-1]


if not hasattr(declarations, "register"):
    # Before the change: no way to name a vocabulary built outside problems/.
    _constant_for = declarations.constant_for
    declarations.constant_for = (lambda r: constant_of if str(r).startswith(NS)
                                 else _constant_for(r))


def declarations_ttl(pr, resource) -> str:
    if pr["members"]:
        rule, n = "PairwiseDistinctness", len(pr["members"])
        pairs = n * (n - 1) // 2
        body = ("    bind:states [ a owl:AllDifferent ; owl:members ( "
                + " ".join(f"<{resource}/{m}>" for m in pr["members"]) + " ) ] .\n")
    elif pr["disjoint"]:
        rule, pairs = "PairwiseDisjointness", len(pr["disjoint"])
        body = "    bind:scopeCondition \"test\"@en .\n" + "".join(
            f"<{resource}/{a}> bind:disjointFrom <{resource}/{b}> .\n"
            for a, b in pr["disjoint"])
    else:
        rule, pairs, body = "PairwiseDistinctness", 0, "    rdfs:comment \"none\"@en .\n"
    return ("@prefix bind: <https://w3id.org/odrl-kb/binding#> .\n"
            "@prefix owl:  <http://www.w3.org/2002/07/owl#> .\n"
            "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"
            f"<{resource}/declared> a bind:Declarations ;\n"
            f"    bind:appliesTo <{resource}> ;\n"
            f"    bind:generatedBy bind:{rule} ;\n"
            f"    bind:origin bind:practiceRule ;\n"
            f"    bind:pairCount {pairs} ;\n" + body)


def build(pr, work: Path) -> dict:
    """The problem as the problem data would write it, through the pipeline."""
    pid = pr["pid"]
    resource = f"{NS}{pid}"
    ax = work / "problems" / "axioms" / f"{pid}.ax"
    ax.write_text("".join(f"fof(res_{pid.lower()}_{a}_below_{b}, axiom,\n"
                          f"    kge_leq({a}, {b})).\n" for a, b in pr["edges"])
                  or "% no published statements\n", encoding="utf-8")
    ttl = work / "problems" / "background" / f"{pid}.ttl"
    ttl.write_text(declarations_ttl(pr, resource), encoding="utf-8")
    decl = declarations.load(ttl)

    p = dict(id=pid, subdir="e2e", name=f"end-to-end {pid}",
             summary=f"end-to-end {pid}", left_operand="x", sort=pr["sort"],
             resource=resource, background_theory=decl.iri,
             includes=["KGE000-0.ax", f"{pid}.ax"], tree=pr["tree"],
             expected_q1="Satisfiable", expected_q2="Satisfiable")
    if hasattr(declarations, "register"):
        vocabulary.register(resource, pr["names"])
        declarations.register_resource(resource, constant_of)
        declarations.register(decl)
    else:
        # Before the change the problem data instantiated the declarations,
        # over the pairs of concepts the problem names.
        named = sorted({v for it in pr["tree"]
                        for c in (it.alts if hasattr(it, "alts") else (it,))
                        for v in c.values})
        kind = "distinct" if decl.members else "disjoint"
        pairs = [(a, b) for a, b in itertools.combinations(named, 2)
                 if decl.has(a, b, constant_of) == kind]
        fof, smt = declarations.instances(decl, pairs, [], [], kind=kind)
        p["fof_decls"], p["smt2_background"] = fof, smt
    return expand_tree(p)


def status_z3(path):
    try:
        out = subprocess.run(["z3", f"-T:{LIMIT}", str(path)], capture_output=True,
                             text=True, timeout=LIMIT + 30).stdout
    except subprocess.TimeoutExpired:
        return "timeout"
    return out.split("\n", 1)[0].strip() or "no-output"


def status_vampire(path, work):
    try:
        out = subprocess.run(["vampire", "--include", str(work / "problems"),
                              "--mode", "casc", "--time_limit", str(LIMIT), str(path)],
                             capture_output=True, text=True, timeout=LIMIT + 30).stdout
    except subprocess.TimeoutExpired:
        return "timeout"
    m = re.search(r"SZS status (\w+)", out)
    return {"Satisfiable": "sat", "CounterSatisfiable": "sat",
            "Unsatisfiable": "unsat", "Theorem": "unsat",
            "ContradictoryAxioms": "unsat"}.get(m and m.group(1), "no-status")


def verdict(q1, q2):
    if q1 == "unsat" and q2 == "unsat":
        return "INCONSISTENT"
    if q1 == "unsat":
        return "Incompatible"
    if q2 == "unsat":
        return "Compatible"
    return "Unknown" if (q1, q2) == ("sat", "sat") else f"undecided({q1},{q2})"


# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--count", type=int, default=2000,
                    help="random problems decided (those with no structure do not count)")
    ap.add_argument("--vampire", type=int, default=200,
                    help="problems whose queries Vampire also decides")
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--keep", type=Path, help="write the queries here and keep them")
    args = ap.parse_args()

    rng = random.Random(args.seed)

    work = Path(tempfile.mkdtemp(prefix="e2e-")) if not args.keep else args.keep
    for d in ("axioms", "background", "verdict"):
        (work / "problems" / d).mkdir(parents=True, exist_ok=True)
    shutil.copy(ROOT / "problems" / "axioms" / "KGE000-0.ax",
                work / "problems" / "axioms" / "KGE000-0.ax")
    here = os.getcwd()
    os.chdir(work)
    try:
        rows, skipped, drawn = [], 0, 0

        def problems():
            nonlocal drawn
            yield from fixed_problems()
            while sum(1 for r in rows if r["pr"]["pid"].startswith("E")) < args.count:
                drawn += 1
                yield random_problem(rng, drawn - 1)

        for pr in problems():
            v, with_use, without = definitional(pr)
            if v is None:
                skipped += 1
                continue
            q = build(pr, work)
            paths = {(enc, n): writer(q, n, work / "problems")
                     for enc, writer in (("fof", write_fof), ("smt", write_smt2))
                     for n in (1, 2)}
            rows.append(dict(pr=pr, expected=v, with_use=with_use,
                             without=without, paths=paths))

        sample = {r["pr"]["pid"] for r in rows if r["pr"]["pid"].startswith("F")}
        step = max(1, len(rows) // max(1, args.vampire))
        sample |= {r["pr"]["pid"] for r in rows[::step]}

        jobs = [(r, "z3", n) for r in rows for n in (1, 2)] + \
               [(r, "vampire", n) for r in rows if r["pr"]["pid"] in sample
                for n in (1, 2)]

        def run(job):
            r, prover, n = job
            if prover == "z3":
                return status_z3(r["paths"][("smt", n)])
            return status_vampire(r["paths"][("fof", n)], work)

        with ThreadPoolExecutor(args.jobs) as ex:
            results = list(ex.map(run, jobs))
        for (r, prover, n), s in zip(jobs, results):
            r.setdefault(prover, [None, None])[n - 1] = s
    finally:
        os.chdir(here)

    # coverage of the draw
    ops = {s: set() for s in (NOM, TAX, MER)}
    conns = {s: set() for s in (NOM, TAX, MER)}
    for r in rows:
        for it in r["pr"]["tree"]:
            for c in (it.alts if hasattr(it, "alts") else (it,)):
                ops[r["pr"]["sort"]].add(c.operator)
            if not isinstance(it, Constraint):
                conns[r["pr"]["sort"]].add("or" if isinstance(it, Or) else "xone")

    bad = []
    for r in rows:
        for prover in ("z3", "vampire"):
            if prover in r:
                got = verdict(*r[prover])
                if got != r["expected"]:
                    bad.append((r, prover, got))

    tally = {}
    for r in rows:
        tally[r["expected"]] = tally.get(r["expected"], 0) + 1
    print(f"end-to-end: {len(rows)} problems decided, {len(rows) - args.count} fixed and "
          f"{args.count} random ({skipped} drawn with no structure skipped), seed {args.seed}")
    print("  from the definitions: " + ", ".join(f"{k} {v}" for k, v in sorted(tally.items())))
    print(f"  Z3 on {len(rows)} problems, Vampire on {len(sample)}")
    for s in (NOM, TAX, MER):
        missing = sorted(set(admitted(s)) - ops[s])
        print(f"  {s}: operators {len(ops[s])} of {len(admitted(s))}"
              + (f" (missing {', '.join(missing)})" if missing else "")
              + f", connectives {' '.join(sorted(conns[s])) or 'none'}")
    for r, prover, got in bad:
        pr = r["pr"]
        print(f"\nDISAGREEMENT {pr['pid']} ({prover}): definitions {r['expected']}, "
              f"pipeline {got} (q1 {r[prover][0]}, q2 {r[prover][1]})")
        print(f"        {describe(pr)}")
        if r["with_use"]:
            M, S = r["with_use"]
            print(f"        a structure with a use: {M.describe()}  use {show_use(M, S)}")
        if r["without"]:
            print(f"        a structure with no use: {r['without'].describe()}")
        print(f"        queries: {r['paths'][('fof', 1)].parent}/{pr['pid']}-*")
    print(f"\n{len(bad)} disagreement(s)")
    if not args.keep:
        shutil.rmtree(work, ignore_errors=True)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
