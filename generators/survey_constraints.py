#!/usr/bin/env python3
"""
survey_constraints.py
=====================
What the suite's policies actually constrain, read from the case files
rather than from the problem data.

    uv run generators/survey_constraints.py

Why the case files and not the problem dicts
---------------------------------------------
The problem dicts hold two representations: a tree the compiler reads,
and a TTL string the case file is written from. They can disagree, and
one of them is what a reader of the artefact sees. This reads the TTL,
so the survey describes the policies as published.

What it reports
---------------
Every (operand, operator) pair with its count and the problems using it,
then the operators of ODRL 2.2 that no policy uses, then the Logical
Constraint connectives. The last is where the suite is thinnest.
"""
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# The eight operators interpreted over concepts, plus the four scalar
# comparators the paper leaves out. Listed so the survey can report what
# is absent as well as what is present.
CONCEPT_OPS = ["eq", "neq", "isA", "isPartOf", "hasPart",
               "isAnyOf", "isAllOf", "isNoneOf"]
SCALAR_OPS = ["lt", "lteq", "gt", "gteq"]

CONNECTIVES = ["and", "or", "xone", "andSequence"]

_CONSTRAINT = re.compile(
    r"odrl:leftOperand\s+(\S+)\s*;\s*"
    r"odrl:operator\s+odrl:(\w+)\s*;\s*"
    r"odrl:rightOperand\s+([^.]+)\.",
    re.S)


def survey(cases_dir: Path):
    pairs = Counter()
    where = defaultdict(set)
    connectives = Counter()
    arity = Counter()

    files = sorted(cases_dir.glob("*.ttl"))
    if not files:
        print(f"no case files in {cases_dir}", file=sys.stderr)
        return 1

    for f in files:
        text = f.read_text(encoding="utf-8")
        pid = f.stem
        for m in _CONSTRAINT.finditer(text):
            operand, op, right = m.group(1), m.group(2), m.group(3)
            operand = operand.split(":")[-1]
            pairs[(operand, op)] += 1
            where[(operand, op)].add(pid)
            # A right operand written as an RDF collection or a repeated
            # triple is set-valued; anything else is a single value.
            arity[(op, "set" if "(" in right or "," in right
                   else "one")] += 1
        for c in CONNECTIVES:
            n = len(re.findall(rf"odrl:{c}\b", text))
            if n:
                connectives[c] += n

    print(f"{len(files)} case files\n")

    print("operand and operator, as the policies write them")
    for (operand, op), n in sorted(pairs.items()):
        ids = ", ".join(sorted(where[(operand, op)])[:6])
        more = "" if len(where[(operand, op)]) <= 6 else " ..."
        print(f"  {operand:34} {op:10} {n:3}   {ids}{more}")

    used = {op for _, op in pairs}
    print("\nconcept operators the suite does not exercise")
    missing = [op for op in CONCEPT_OPS if op not in used]
    for op in missing:
        print(f"  {op}")
    if not missing:
        print("  (none)")

    print("\nscalar operators, out of scope by design")
    for op in SCALAR_OPS:
        mark = "  PRESENT, and should not be" if op in used else "  absent"
        print(f"  {op:8}{mark}")

    print("\narity of the right operand, by operator")
    for (op, kind), n in sorted(arity.items()):
        print(f"  {op:10} {kind:4} {n:3}")

    print("\nLogical Constraint connectives")
    for c in CONNECTIVES:
        n = connectives.get(c, 0)
        print(f"  {c:14} {n}")
    if not connectives:
        print("  none: every policy is a flat conjunction of constraints.")

    print("\nleft operands, by namespace")
    ns = Counter(operand for operand, _ in pairs)
    for operand, _ in sorted(ns.items()):
        print(f"  {operand}")

    return 0


if __name__ == "__main__":
    d = Path(sys.argv[1] if len(sys.argv) > 1 else "cases")
    sys.exit(survey(d))