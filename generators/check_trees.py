"""
check_trees.py
==============
Checks that the policies of every case file are the tree its queries are
built from.

The queries are built from the authored trees, and the Turtle of the policies
is written separately.  The two can drift: a builder that ignores its operator
argument writes a case whose policies say one thing and whose verdict rests on
another.  That happened once, in the BCP 47 request builder.

This reads the published case files with policy.read_policy and compares the
tree of each with the authored one: the operators, the values, the
connectives, the order of what a connective combines and of the values of a
set operator, and the policy of each constraint.  Policy 1 of a case is the
offer of the tree and policy 2 the request.  Both trees are conjunctions, and
the order of their items is not compared.

A value is compared as a concept: an IRI the case's resource holds is its
constant.  Any other value is as the policy writes it, a prefixed name or the
text of a literal, which is how an authored tree writes a value that its
binding resolves by another rule or not at all (KGC373, KGC381).  A literal
that reads like a constant or a prefixed name keeps its quotes.

Two kinds of case build no query.  A well-sortedness case is authored as an
operator and a value, or as a tree (KGC123), its values named by
problem_data_wellsorted.VALUE; it is compared like the others.  A case whose
value does not ground may have no tree (KGC372); it is listed, and its policies
must write that value.

    uv run generators/check_trees.py [--cases cases]

Exit 1, and the differences, if any case differs or has no counterpart.
"""

import argparse
import importlib
import sys
from collections import Counter
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from rdflib import Graph, Namespace, URIRef

import declarations
import vocabulary
from compile import Constraint
from policy import PolicyError, atoms, by_operand, policies, read_policy
from problem_data_wellsorted import PREFIX, VALUE
from tree_expand import _map_item

DRK = Namespace("https://w3id.org/odrl-kb/drk/")
SIDES = (("1", "offer"), ("2", "request"))


def authored_problems() -> dict:
    """Case ID -> its problem data, from every problem_data module."""
    out = {}
    for f in sorted(Path(__file__).parent.glob("problem_data_*.py")):
        for p in importlib.import_module(f.stem).PROBLEMS:
            out[p["id"]] = p
    return out


@lru_cache(maxsize=None)
def constants_of(resource: str) -> dict:
    """Concept IRI -> its constant, for every concept of the resource."""
    constant = declarations.constant_for(resource)
    return {i: constant(i) for i in vocabulary.iris(resource)}


def value_in(resource: str, g):
    """The function from a value of a policy to what a tree writes for it."""
    named = constants_of(resource)
    constants = set(named.values())

    def value(term):
        if isinstance(term, URIRef):
            return named.get(term) or term.n3(g.namespace_manager)
        text = str(term)
        return term.n3() if text in constants or ":" in text else text
    return value


def tree_of(p: dict, value):
    """The authored tree of a problem, or None when it has none."""
    if "accepted" not in p:
        return p.get("tree")
    tree = p.get("tree") or [Constraint(p["operator"], (p["value"],))]
    prefix = PREFIX[p["left_operand"]][1]

    def concept(key):
        g = Graph().parse(data=f"{prefix}\n[] a {VALUE[key]} .", format="turtle")
        return value(next(g.objects()))
    return [_map_item(i, {v: concept(v) for c in atoms([i]) for v in c.values})
            for i in tree]


def read_tree(cid: str, g, value) -> list:
    """The tree of both policies of a case file, as one conjunction."""
    sides = {DRK[f"policy-{cid[3:]}-{n}"]: side for n, side in SIDES}
    found = policies(g)
    if not found or set(found) - set(sides):
        raise PolicyError(f"the policies are {', '.join(found) or 'none'}")
    trees = by_operand(*(read_policy(g, sides[pol], pol, value)
                         for pol in found))
    if len(trees) != 1:
        raise PolicyError(f"constraints on {' and '.join(sorted(trees)) or 'none'}"
                          f", where a tree is on one left operand")
    return next(iter(trees.values()))


def show(items) -> str:
    def one(i):
        if isinstance(i, Constraint):
            return f"{i.side} {i.operator} {' '.join(i.values)}"
        return f"{type(i).__name__.lower()}({', '.join(map(one, i.alts))})"
    return "; ".join(map(one, items)) or "nothing"


def difference(p: dict, path: Path):
    """What differs between a case file and its problem data, or None."""
    g = Graph().parse(path, format="turtle")
    value = value_in(p["resource"], g)
    try:
        read = read_tree(p["id"], g, value)
    except PolicyError as e:
        return f"the policies do not read as a tree: {e}"
    tree = tree_of(p, value)
    if tree is None:
        missing = p.get("ungrounded")
        if any(missing in c.values for c in atoms(read)):
            return None
        return f"no authored tree, and the policies do not write {missing!r}"
    if Counter(read) == Counter(tree):
        return None
    return f"the policies  {show(read)}\n        the tree      {show(tree)}"


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Compare the policies of the case files with the authored "
                    "trees.")
    ap.add_argument("--cases", default="cases", type=Path)
    args = ap.parse_args()

    problems = authored_problems()
    files = {f.stem: f for f in sorted(args.cases.glob("KGC*.ttl"))}
    bad = [(cid, "a case file and no problem data")
           for cid in sorted(files.keys() - problems.keys())]
    bad += [(cid, "problem data and no case file")
            for cid in sorted(problems.keys() - files.keys())]
    both = sorted(files.keys() & problems.keys())
    for cid in both:
        why = difference(problems[cid], files[cid])
        if why:
            bad.append((cid, why))

    no_tree = [cid for cid in both
               if "accepted" not in problems[cid] and "tree" not in problems[cid]]
    differ = {cid for cid, _ in bad}
    same = [cid for cid in both if cid not in differ and cid not in no_tree]
    print(f"trees: {len(files)} case files; the policies are the authored tree "
          f"in {len(same)}; differences: {len(bad)}")
    for cid in no_tree:
        if cid not in differ:
            print(f"    no authored tree: {cid} builds no query, since its value "
                  f"{problems[cid]['ungrounded']!r} does not ground; its policies "
                  f"write that value")
    for cid, why in sorted(bad):
        print(f"    FAIL {cid}: {why}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
