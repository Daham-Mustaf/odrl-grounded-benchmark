"""
check_coverage.py
=================
The coverage guard.  The grid is the eight operators by the three sorts,
24 cells, and the signature says which cells a policy may fill:

  - where the sort admits the operator, some verdict case (Compatible,
    Incompatible or Unknown) puts that operator at that sort;
  - where it does not, some case is rejected as ill sorted for exactly that
    operator at that sort;
  - or and xone each have a verdict case at every sort.

A cell is read from the case files: the sort is the sort of the binding the
report names, the operators are those of the policies' constraints.  A case
that is rejected because a value does not ground fills no cell.

    uv run generators/check_coverage.py [--cases cases] [--profiles problems/resources]

Exit 1 if a cell or a connective has no case.
"""

import argparse
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from rdflib import Graph, Namespace, RDF

from signature import SIGNATURE, NOM, TAX, MER

ODRL = Namespace("http://www.w3.org/ns/odrl/2/")
VREP = Namespace("https://w3id.org/odrl-kb/verdict-report#")
BIND = Namespace("https://w3id.org/odrl-kb/binding#")

SORTS = (NOM, TAX, MER)
CONNECTIVES = ("or", "xone")


def local(x) -> str:
    return str(x).rsplit("/", 1)[-1].rsplit("#", 1)[-1]


def sorts_of_bindings(profiles: Path) -> dict:
    out = {}
    for p in sorted(profiles.glob("profile-*.ttl")):
        g = Graph().parse(p, format="turtle")
        for b in g.subjects(RDF.type, BIND.OperandBinding):
            for s in g.objects(b, BIND.sort):
                out[str(b)] = local(s)
    return out


def read_cases(cases: Path, sort_of: dict):
    """(verdict, rejected): each maps (operator, sort) to the case IDs, and
    connectives maps (connective, sort) to the IDs of verdict cases."""
    verdict, rejected, connective = defaultdict(set), defaultdict(set), defaultdict(set)
    for f in sorted(cases.glob("KGC*.ttl")):
        g = Graph().parse(f, format="turtle")
        cid = f.stem
        for kind, table in ((VREP.OperandVerdictReport, verdict),
                            (VREP.WellSortednessReport, rejected)):
            for rep in g.subjects(RDF.type, kind):
                if kind == VREP.WellSortednessReport and \
                        any(o.toPython() is not False
                            for o in g.objects(rep, VREP.wellSorted)):
                    continue            # an accepted control fills no cell
                binding = next(g.objects(rep, VREP.binding), None)
                sort = sort_of.get(str(binding))
                if sort is None:
                    continue
                for c in g.subjects(RDF.type, ODRL.Constraint):
                    for op in g.objects(c, ODRL.operator):
                        table[(local(op), sort)].add(cid)
                if kind == VREP.OperandVerdictReport:
                    for conn in CONNECTIVES:
                        if any(True for _ in g.subject_objects(ODRL[conn])):
                            connective[(conn, sort)].add(cid)
    return verdict, rejected, connective


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--cases", default="cases", type=Path)
    ap.add_argument("--profiles", default="problems/resources", type=Path)
    args = ap.parse_args()

    verdict, rejected, connective = read_cases(args.cases,
                                               sorts_of_bindings(args.profiles))
    missing = []
    admitted = refused = 0
    for op, (admits, _) in SIGNATURE.items():
        for sort in SORTS:
            if sort in admits:
                admitted += 1
                if not verdict[(op, sort)]:
                    missing.append(f"{op} at {sort}: the sort admits it and no "
                                   f"verdict case uses it")
            else:
                refused += 1
                if not rejected[(op, sort)]:
                    missing.append(f"{op} at {sort}: the sort does not admit it "
                                   f"and no case is rejected for it")
    for conn in CONNECTIVES:
        for sort in SORTS:
            if not connective[(conn, sort)]:
                missing.append(f"{conn} at {sort}: no verdict case")

    cells = len(SIGNATURE) * len(SORTS)
    print(f"5c  coverage: {cells} cells, {admitted} admitted (a verdict case each) "
          f"and {refused} not (a rejection each); "
          f"{' and '.join(CONNECTIVES)} at {len(SORTS)} sorts")
    for m in missing:
        print(f"    FAIL {m}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
