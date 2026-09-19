"""Check that each policy's Turtle uses the operators its tree compiles.

The Turtle is written by hand in the problem_data modules while the
queries are compiled from the tree, so the two can drift: a generator
that ignores its operator argument yields a case whose policy says one
thing and whose verdict rests on another.  That happened once, in the
BCP 47 request builder.
"""
import importlib
import re
import sys

MODULES = [
    "problem_data_bcp47", "problem_data_consent", "problem_data_dpv",
    "problem_data_dpvloc", "problem_data_filetype", "problem_data_gdprlb",
    "problem_data_motivating", "problem_data_tom", "problem_data_wellsorted",
]

TREE_OP = re.compile(r"operator='(\w+)'")
TTL_OP = re.compile(r"odrl:operator\s+odrl:(\w+)")

bad = 0
seen = 0
for name in MODULES:
    mod = importlib.import_module(name)
    for p in getattr(mod, "PROBLEMS", []):
        if "tree" not in p or "ttl" not in p:
            continue
        seen += 1
        tree = set(TREE_OP.findall(repr(p["tree"])))
        ttl = set(TTL_OP.findall(p["ttl"]))
        if tree != ttl:
            print(f"{p.get('id','?')}: tree {sorted(tree)} "
                  f"policy {sorted(ttl)}")
            bad += 1

print(f"{seen} problems checked, {bad} mismatches")
sys.exit(1 if bad else 0)
