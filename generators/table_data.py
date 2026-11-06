#!/usr/bin/env python3
"""
table_data.py
=============
Every figure the evaluation table needs, measured rather than recalled.

    uv run generators/table_data.py                 # readable
    uv run generators/table_data.py --tex > tab.tex # LaTeX rows
    uv run generators/table_data.py --macros        # \newcommand lines
    uv run generators/table_data.py --suite-numbers # writes suite-numbers.tex
    uv run generators/table_data.py --challenges    # the rows, and any case in none

Each row is one binding, not one resource: a file read under two
profiles produces two rows, which is the table's point. Counts come from
the generated artefacts, so a figure that moves when a builder changes
moves here too.

--suite-numbers writes suite-numbers.tex: the macros of counts, those of the
timing pass and the tables, for the paper to include. It refuses to
write when the numbers do not add up: the rows must sum to the case files,
every case must fall in exactly one of definite, Unknown, rejected and
accepted, and every binding a case cites must have a row. A file that is
written is therefore one whose figures agree.

The time macros come from the runs generators/time_queries.py writes,
results/timings-runN.csv.  A check is one query under one prover.  The macros
are the number of runs, the median of the run totals, the median and the 95th
percentile (nearest rank) over the checks of each check's median, the slowest
check by its median, the limit, the machine, and the two prover versions.
Every run must time every current query under its prover and nothing else, or
suite-numbers.tex is not written.

The proof checker, the two-provers stage and the end-to-end test each leave a
JSON file in results/: proof-check.json, two-provers.json, end-to-end.json.
The macros for the certificates, the agreement of the provers and the
end-to-end test are read from them, and suite-numbers.tex is not written when
one is missing or does not fit the case files and certificates.

What is counted, per row:

    concepts     subjects the resource file types as its concept class
    order        kge_leq statements in the resource's .ax file
    test cases   case files whose binding is this one
    C, I, U      those with that verdict
    rejected     those rejected as ill sorted or ungrounded; the accepted
                 controls are in test cases and in no other column
    reads        the relation the profile's prose says the sort takes

The last is the only field not measured. It is read from the profile
file's header comment, since no triple states it: the profile declares
bind:sort and bind:resource, and which published relation that sort is
taken from is a claim the header makes in prose.
"""
import argparse
import csv
import json
import math
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

from rdflib import Graph, Literal, Namespace, RDF
from rdflib.collection import Collection

sys.path.insert(0, str(Path(__file__).parent))

from operator_notes import beyond
from signature import SIGNATURE, NOM, TAX, MER

ODRL = Namespace("http://www.w3.org/ns/odrl/2/")
VREP = Namespace("https://w3id.org/odrl-kb/verdict-report#")
BIND = Namespace("https://w3id.org/odrl-kb/binding#")

# One entry per binding. The resource tag is the builder's; the binding
# IRI is what the case files cite.
BINDINGS = [
    ("DPV purposes",                 "dpv-purposes",   "tax", "b-purpose"),
    ("DPV consent status",           "consent",        "tax", "b-consent-status"),
    ("DPV measures",                 "tom",            "tax", "b-tom"),
    ("DPV Locations, geographic",    "dpvloc-geo",     "mer", "b-spatial-dpvloc-geo"),
    ("DPV Locations, jurisdictional","dpvloc-juris",   "mer", "b-spatial-dpvloc-juris"),
    ("GeoNames Europe slice",        "geonames",       "mer", "b-spatial-geonames"),
    ("EU file type table",           "filetype",       "nom", "b-fileformat"),
    ("BCP 47 subtags, exact",        "bcp47",          "nom", "b-language-bcp47"),
    ("BCP 47 subtags, primary",      "bcp47",          "nom", "b-language-bcp47-primary"),
]

# The axiom file each resource writes, since the naming is not uniform.
AXIOMS = {
    "dpv-purposes":   "DPV-dpv-purposes.ax",
    "consent":        "DPV-consent.ax",
    "tom":            "DPV-tom.ax",
    "dpvloc-geo":     "LOC-dpvloc-geo.ax",
    "dpvloc-juris":   "LOC-dpvloc-juris.ax",
    "geonames":       "GN000-0.ax",
    "filetype":       "EUFT-filetype.ax",
    "bcp47":          "BCP47000-0.ax",
}


def count_order(ax_path: Path) -> int:
    """kge_leq statements in a resource axiom file.

    Ground facts only: the label is the builder's and varies (res_ for
    most resources, gn_ for GeoNames), and the first argument is a constant,
    which keeps the quantified order axioms out of the count.
    """
    if not ax_path.exists():
        return -1
    return len(re.findall(r"^fof\(\S+,\s*axiom,\s*\n?\s*kge_leq\(\s*[a-z]",
                          ax_path.read_text(encoding="utf-8"), re.M))


def count_concepts(ttl_path: Path) -> int:
    """Subjects the resource types as its concept class.

    Counted from the Turtle rather than from the axioms: a concept the
    resource lists and no statement mentions is still a concept, and the
    nominal resources are exactly the ones where that matters.

    The class is odrlkb: for the builders' own resources, skos:Concept for
    the BCP 47 slice and gn:Feature for GeoNames.
    """
    if not ttl_path.exists():
        return -1
    text = ttl_path.read_text(encoding="utf-8")
    return len(re.findall(
        r"^\S+\s+a\s+(?:odrlkb:\w+|skos:Concept|gn:Feature)\s*[;.]",
        text, re.M))


def profile_reads(profile_path: Path) -> str:
    """The relation the profile's header says the sort reads.

    Prose, not a triple. Returned as the first header line mentioning a
    published property, or the empty string.
    """
    if not profile_path.exists():
        return ""
    for line in profile_path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("#"):
            break
        if "skos:" in line or "identity" in line.lower():
            return line.lstrip("# ").strip()
    return ""


def cases_by_binding(cases_dir: Path) -> Counter:
    """Verdict cases per binding IRI, from the case files themselves."""
    c = Counter()
    for f in sorted(cases_dir.rglob("*.ttl")):
        if f.name == "README.md":
            continue
        m = re.search(r"vrep:binding\s+<([^>]+)>", f.read_text(encoding="utf-8"))
        if m:
            c[m.group(1).rsplit("/", 1)[-1]] += 1
    return c


def suite_totals(cases_dir: Path, verdict_dir: Path) -> dict:
    """The counts the results paragraph needs."""
    files = [f for f in cases_dir.rglob("*.ttl")]
    states = Counter()
    ungrounded = ill_sorted = accepted = 0
    cited = set()
    for f in files:
        t = f.read_text(encoding="utf-8")
        m = re.search(r"vrep:compatibilityState\s+vrep:(\w+)\s*[;.]", t)
        if m:
            states[m.group(1)] += 1
        if re.search(r"vrep:grounded\s+false", t):
            ungrounded += 1
        if re.search(r"vrep:wellSorted\s+false", t):
            ill_sorted += 1
        elif re.search(r"vrep:wellSorted\s+true", t):
            accepted += 1
        b = re.search(r"vrep:binding\s+<([^>]+)>", t)
        if b:
            cited.add(b.group(1).rsplit("/", 1)[-1])
    queries = len(list(verdict_dir.glob("*-[12].p")))
    return {
        "files": len(files),
        "queries": queries,
        "compatible": states.get("Compatible", 0),
        "incompatible": states.get("Incompatible", 0),
        "unknown": states.get("Unknown", 0),
        # Every Unknown is epistemic now; the macro is kept for the paper.
        "epistemic": states.get("Unknown", 0),
        # Constraints rejected because a value does not ground.
        "ungrounded": ungrounded,
        # Constraints rejected because the operator does not fit the sort.
        "ill_sorted": ill_sorted,
        "rejected": ill_sorted + ungrounded,
        # Well-sorted controls: checked, accepted, no verdict asked for.
        "accepted": accepted,
        # The bindings the case files cite, by the last segment of the IRI.
        "cited": sorted(cited),
    }


def local(x) -> str:
    return str(x).rsplit("/", 1)[-1].rsplit("#", 1)[-1]


def constraint_term(g, node):
    """A constraint as a value that compares: the operator and its values, or
    the connective and its members in order."""
    op = next(g.objects(node, ODRL.operator), None)
    if op is not None:
        right = next(g.objects(node, ODRL.rightOperand))
        values = (list(Collection(g, right))
                  if (right, RDF.first, None) in g else [right])
        return (local(op), tuple(str(v) for v in values))
    for conn in ("or", "xone", "and", "andSequence"):
        head = next(g.objects(node, ODRL[conn]), None)
        if head is not None:
            return (conn, tuple(constraint_term(g, m)
                                for m in Collection(g, head)))
    raise ValueError(f"{node} is neither a constraint nor a logical constraint")


def read_cases(cases_dir: Path) -> list:
    """Every test case: what it asks and its outcome.

    The outcome is C, I, U, rejected, or control (a constraint checked and
    accepted, for which no verdict is asked).
    """
    out = []
    for f in sorted(cases_dir.glob("KGC*.ttl")):
        g = Graph().parse(f, format="turtle")
        report = next(s for s in g.subjects(VREP.binding, None))
        state = next(g.objects(report, VREP.compatibilityState), None)
        if state is not None:
            outcome = {"Compatible": "C", "Incompatible": "I",
                       "Unknown": "U"}[local(state)]
        elif (report, VREP.wellSorted, None) in g:
            well = next(g.objects(report, VREP.wellSorted)).toPython()
            outcome = "control" if well else "rejected"
        elif next(g.objects(report, VREP.grounded)).toPython() is False:
            outcome = "rejected"
        else:
            raise ValueError(f"{f.name}: no outcome in its report")
        declarations = next(g.objects(report, VREP.declarations), None)
        pair = [next(g.objects(report, p), None)
                for p in (VREP.referenceConstraint, VREP.comparedConstraint)]
        conflicts = []
        for c in g.subjects(RDF.type, ODRL.Constraint):
            op = local(next(g.objects(c, ODRL.operator)))
            for lo in g.objects(c, ODRL.leftOperand):
                if beyond(lo, op):
                    conflicts.append((local(lo), op))
        out.append({
            "id": f.stem,
            "outcome": outcome,
            "ill_sorted": (report, VREP.wellSorted, Literal(False)) in g,
            "read_against": {local(o).removesuffix("-report")
                             for o in g.objects(report, VREP.readAgainst)},
            "note_conflicts": conflicts,
            "binding": local(next(g.objects(report, VREP.binding))),
            "declarations": str(declarations) if declarations else "",
            "operators": {local(o) for o in g.objects(None, ODRL.operator)},
            "connectives": {c for c in ("or", "xone", "and", "andSequence")
                            if any(True for _ in g.subject_objects(ODRL[c]))},
            "constraints": tuple(constraint_term(g, c) for c in pair
                                 if c is not None),
        })
    return out


def left_operand(profile: Path, binding: str) -> str:
    """The binding's left operand, as the case files write it."""
    g = Graph().parse(profile, format="turtle")
    for b, o in g.subject_objects(BIND.leftOperand):
        if local(b) == binding:
            return ("odrl:" if str(o).startswith(str(ODRL))
                    else "dpv-odrl:") + local(o)
    return ""


def rows(root: Path):
    cases = cases_by_binding(root / "cases")
    tests = read_cases(root / "cases")
    out = []
    for label, tag, sort, binding in BINDINGS:
        outcomes = Counter(c["outcome"] for c in tests
                           if c["binding"] == binding)
        profile = root / "problems" / "resources" / f"profile-{tag}.ttl"
        out.append({
            "operand":  left_operand(profile, binding),
            "outcomes": outcomes,
            "label":    label,
            "sort":     sort,
            "concepts": count_concepts(root / "problems" / "resources" / f"{tag}.ttl"),
            "order":    count_order(root / "problems" / "axioms" / AXIOMS[tag]),
            "cases":    cases.get(binding, 0),
            "reads":    profile_reads(
                            root / "problems" / "resources" / f"profile-{tag}.ttl"),
            "binding":  binding,
        })
    return out


def suite_problems(rs, totals) -> list:
    """Why the figures do not add up, or an empty list when they do."""
    out = []
    n = sum(r["cases"] for r in rs)
    if n != totals["files"]:
        out.append(f"the rows sum to {n} cases but there are "
                   f"{totals['files']} case files")
    rowed = {r["binding"] for r in rs}
    for b in sorted(set(totals["cited"]) - rowed):
        out.append(f"cases cite {b}, which has no row in BINDINGS")
    for b in sorted(rowed - set(totals["cited"])):
        out.append(f"BINDINGS has a row for {b}, which no case cites")
    classes = (totals["compatible"] + totals["incompatible"]
               + totals["unknown"] + totals["rejected"] + totals["accepted"])
    if classes != totals["files"]:
        out.append(f"definite + Unknown + rejected + accepted is {classes}, "
                   f"not {totals['files']}: some case is in no class or two")
    for r in rs:
        if r["concepts"] < 0 or r["order"] < 0:
            out.append(f"{r['label']}: resource or axiom file not found")
    return out


RESULTS = Path("results")
PROVER = {"vampire": "Vampire", "z3": "Z3"}


# What each of a case's two queries asks.
CHECK_IN_WORDS = {"1": "a use that meets the policies",
                  "2": "no use that meets the policies"}


def read_timing_file(path: Path):
    """(header, rows) of one run."""
    header, body = {}, []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            key, sep, value = line[1:].strip().partition(": ")
            if sep:
                header[key] = value
        elif line.strip():
            body.append(line)
    return header, list(csv.DictReader(body))


def timing_paths(results: Path) -> list:
    """The runs time_queries.py writes.  The one results/timings.csv of an
    earlier release stands until the first three-run pass; \\suiteRuns then
    says 1."""
    runs = sorted(results.glob("timings-run*.csv"))
    if runs:
        return runs
    legacy = results / "timings.csv"
    return [legacy] if legacy.exists() else []


def read_timings(results: Path):
    """Each run, as (path, header, rows)."""
    return [(p, *read_timing_file(p)) for p in timing_paths(results)]


def timing_problems(timings, verdict_dir: Path) -> list:
    """Why the runs do not fit the suite, or an empty list."""
    if not timings:
        return ["no timing runs in results/: run generators/time_queries.py"]
    out = []
    want = {(q.stem, "vampire") for q in verdict_dir.glob("*-[12].p")} \
        | {(q.stem, "z3") for q in verdict_dir.glob("*-[12].smt2")}
    for path, header, rows in timings:
        out += [f"{path.name} has no {k} line in its header"
                for k in ("vampire", "z3", "cpu", "ram", "date", "limit")
                if k not in header]
        have = [(r["query"], r["prover"]) for r in rows]
        if len(have) != len(set(have)):
            out.append(f"{path.name} times a query twice")
        for what, runs in (("has no time for", want - set(have)),
                           ("times what is not a query of the suite:",
                            set(have) - want)):
            if runs:
                shown = ", ".join(f"{q} under {PROVER.get(p, p)}"
                                  for q, p in sorted(runs)[:4])
                more = f" and {len(runs) - 4} more" if len(runs) > 4 else ""
                out.append(f"{path.name} {what} {shown}{more}: "
                           f"run generators/time_queries.py")
    for key in ("vampire", "z3", "cpu", "limit"):
        if len({header.get(key) for _, header, _ in timings}) > 1:
            out.append(f"the timing runs differ in {key}")
    return out


def median(values) -> float:
    return statistics.median(values)


def percentile(values, q: int) -> float:
    """Nearest rank: the smallest value with q percent of them at or below."""
    ordered = sorted(values)
    return ordered[math.ceil(q / 100 * len(ordered)) - 1]


def time_macros(timings) -> list:
    """The macros of the timing pass, from its runs."""
    header = timings[0][1]
    totals = [sum(float(r["seconds"]) for r in rows) for _, _, rows in timings]
    per_check = {}
    for _, _, rows in timings:
        for r in rows:
            per_check.setdefault((r["query"], r["prover"]), []).append(
                float(r["seconds"]))
    medians = {check: median(s) for check, s in per_check.items()}
    query, prover = max(medians, key=medians.get)
    # "Intel(R) Core(TM) Ultra 7 165U, 14 logical cores" -> "Intel Core Ultra 7 165U"
    cpu = header["cpu"].split(", ")[0]
    cpu = re.sub(r"\((R|TM)\)|\bCPU\b|\bProcessor\b|@.*", "", cpu)
    cpu = " ".join(cpu.split())

    def version(line, pattern):
        m = re.search(pattern, line)
        return m.group(1) if m else line

    return [
        ("suiteRuns",     str(len(timings))),
        ("suiteTime",     f"{median(totals):.1f}"),
        ("suiteTimeMedian", f"{median(medians.values()):.2f}"),
        ("suiteTimePninetyfive", f"{percentile(medians.values(), 95):.2f}"),
        ("suiteSlowest",  f"{query.rsplit('-', 1)[0]} ({PROVER[prover]}, "
                          f"{medians[(query, prover)]:.1f} s)"),
        ("suiteSlowestCheck", CHECK_IN_WORDS[query.rsplit("-", 1)[1]]),
        ("suiteLimit",    header["limit"]),
        ("suiteHardware", f"{cpu}, {header['ram']} RAM"),
        ("suiteVampire",  version(header["vampire"], r"Vampire (\S+)")),
        ("suiteZthree",   version(header["z3"], r"version (\S+)")),
    ]


def tex_escape(s: str) -> str:
    for ch in "\\&%$#_{}":
        s = s.replace(ch, "\\" + ch)
    return s


def sort_of_binding() -> dict:
    return {binding: sort for _, _, sort, binding in BINDINGS}


def coverage_table(tests) -> list:
    """Operators by sorts.  An allowed cell holds the C/I/U counts of the test
    cases that use the operator at that sort; a cell the signature does not
    allow says rejected."""
    sorts = (NOM, TAX, MER)
    sort_of = sort_of_binding()
    lines = [
        "\\newcommand{\\suiteCoverageTable}{%",
        "\\begin{tabular}{lccc}",
        "\\hline",
        "operator & " + " & ".join(sorts) + " \\\\",
        "\\hline",
    ]
    for op, (admits, _) in SIGNATURE.items():
        cells = []
        for sort in sorts:
            if sort not in admits:
                cells.append("rejected")
                continue
            n = Counter(c["outcome"] for c in tests
                        if sort_of[c["binding"]] == sort and op in c["operators"])
            cells.append(f"{n['C']}/{n['I']}/{n['U']}")
        lines.append(f"{op} & " + " & ".join(cells) + " \\\\")
    lines += ["\\hline", "\\end{tabular}%", "}"]
    return lines


def declaration_pairs(tests) -> list:
    """Policy pairs that differ in the declarations only: one binding and the
    same constraints in the same places, asked under more than one set of
    declarations.  One entry per policy pair, with its test cases."""
    groups = {}
    for c in tests:
        if c["constraints"]:
            groups.setdefault((c["binding"], c["constraints"]), []).append(c)
    return sorted([c["id"] for c in same] for same in groups.values()
                  if len({c["declarations"] for c in same}) > 1)


CLOSED_WORLD = Path("results") / "closed-world.csv"

# The paper's running example comes first when a row holds one of its cases.
RUNNING_EXAMPLE = ("KGC310", "KGC302", "KGC371", "KGC370")
CONSTRAINT_FORMS = {"or", "xone", "isAnyOf", "isAllOf", "isNoneOf"}
BINDING_CHOICE = {"b-spatial-dpvloc-juris", "b-language-bcp47-primary"}
SILENT = "nothing, the resource decides or is silent"


def read_closed_world(path: Path):
    """Each test case's row of results/closed-world.csv, or None."""
    if not path.exists():
        return None
    with path.open(encoding="utf-8", newline="") as f:
        return {r["case"]: r for r in csv.DictReader(f)}


def cited(certificates: Path, cid: str) -> list:
    """(source, statement) for each premise the case's proof cites."""
    path = certificates / f"{cid}-observed.ttl"
    if not path.exists():
        return []
    return re.findall(r'vrep:premiseSource vrep:(\w+) ;\s*'
                      r'vrep:formulaName "([^"]+)"',
                      path.read_text(encoding="utf-8"))


def cites_order(premises) -> bool:
    """An order statement of the resource.  Identity is written as two order
    statements named _same_, and is not counted."""
    return any(src == "fromResource" and "_same_" not in name
               for src, name in premises)


def cites_distinctness(premises) -> bool:
    return any(name.startswith("bg_dist_") for _, name in premises)


def challenges(tests, closed, certificates: Path) -> list:
    """One row per challenge: its name, what varies, and its test cases.

    A test case may fall under several."""
    definite = ("C", "I")

    def kind(c):
        return closed[c["id"]]["kind"]

    def proof(c):
        return cited(certificates, c["id"])

    rules = [
        ("C1 order in the resource", SILENT,
         lambda c: c["outcome"] in definite and cites_order(proof(c))),
        ("C2 unstated distinctness", SILENT,
         lambda c: (c["outcome"] == "U" and kind(c) in ("distinctness", "identity"))
         or (c["outcome"] in definite and cites_distinctness(proof(c)))),
        ("C3 unstated order", SILENT,
         lambda c: c["outcome"] == "U" and kind(c) == "order"),
        ("C4 declarations", "declarations",
         lambda c: bool(c["declarations"])
         and not c["declarations"].endswith("/empty")),
        ("C5 choice of binding", "binding",
         lambda c: c["binding"] in BINDING_CHOICE),
        ("C6 ill-formed constraints", "the constraint",
         lambda c: c["outcome"] in ("rejected", "control")),
        ("C7 combined constraints", "the constraint",
         lambda c: bool((c["operators"] | c["connectives"]) & CONSTRAINT_FORMS)),
    ]
    return [(name, varies, [c for c in tests if rule(c)])
            for name, varies, rule in rules]


def example_of(members) -> str:
    ids = [c["id"] for c in members]
    for cid in RUNNING_EXAMPLE:
        if cid in ids:
            return cid
    return ids[0] if ids else "none"


def challenge_table(rows) -> list:
    lines = [
        "\\newcommand{\\suiteChallengeTable}{%",
        "\\begin{tabular}{llrrrrrl}",
        "\\hline",
        "challenge & what varies & test cases & C & I & U & rejected"
        " & example \\\\",
        "\\hline",
    ]
    for name, varies, members in rows:
        n = Counter(c["outcome"] for c in members)
        lines.append(f"{name} & {varies} & {len(members)} & {n['C']} & {n['I']}"
                     f" & {n['U']} & {n['rejected']} & {example_of(members)}"
                     " \\\\")
    lines += ["\\hline", "\\end{tabular}%", "}"]
    return lines


def challenge_cw_table(rows, closed) -> list:
    """The same rows, and how many expected outcomes the closed world keeps."""
    lines = [
        "\\newcommand{\\suiteChallengeCWTable}{%",
        "\\begin{tabular}{lrr}",
        "\\hline",
        "challenge & test cases & reproduced \\\\",
        "\\hline",
    ]
    for name, _, members in rows:
        same = sum(1 for c in members if closed[c["id"]]["reproduced"] == "yes")
        lines.append(f"{name} & {len(members)} & {same} \\\\")
    lines += ["\\hline", "\\end{tabular}%", "}"]
    return lines


def under_no_challenge(rows, tests) -> list:
    inside = {c["id"] for _, _, members in rows for c in members}
    return [c for c in tests if c["id"] not in inside]


def plain_term(term) -> str:
    head, rest = term
    if head in ("or", "xone", "and", "andSequence"):
        return f"{head}(" + ", ".join(plain_term(m) for m in rest) + ")"
    return f"{head} " + " ".join(local(v) for v in rest)


def print_challenges(rows, tests) -> None:
    for name, varies, members in rows:
        print(f"{name} ({varies}): {len(members)}: "
              + " ".join(c["id"] for c in members))
    outside = under_no_challenge(rows, tests)
    print(f"\nunder no challenge: {len(outside)}")
    for c in outside:
        print(f"  {c['id']}  {c['outcome']}  "
              + " against ".join(plain_term(t) for t in c["constraints"]))


def closed_world_problems(closed, tests) -> list:
    if closed is None:
        return [f"{CLOSED_WORLD} not found: run generators/closed_world.py"]
    out = []
    have, want = set(closed), {c["id"] for c in tests}
    if have != want:
        out.append(f"{CLOSED_WORLD} does not cover the test cases: "
                   + ", ".join(sorted(have ^ want)[:4]))
    moved = Counter(r["closed_world"] for r in closed.values()
                    if r["expected"] == "U")
    if set(moved) - {"C", "I"}:
        out.append(f"{CLOSED_WORLD}: an Unknown test case has no closed-world "
                   f"verdict")
    for c in tests:
        row = closed.get(c["id"])
        if row and c["outcome"] != "U" and row["reproduced"] != "yes":
            out.append(f"{CLOSED_WORLD}: {c['id']} is {c['outcome']}, and the "
                       f"closed world gives {row['closed_world']}")
        if row and row["expected"] != c["outcome"]:
            out.append(f"{CLOSED_WORLD}: {c['id']} expected {row['expected']}, "
                       f"its case file says {c['outcome']}")
        if row and c["outcome"] == "U" and row["kind"] not in (
                "distinctness", "identity", "order"):
            out.append(f"{CLOSED_WORLD}: {c['id']} has no kind")
    return out


PROOF_CHECK = RESULTS / "proof-check.json"
TWO_PROVERS = RESULTS / "two-provers.json"
END_TO_END = RESULTS / "end-to-end.json"


def read_outputs(root: Path) -> dict:
    """The JSON files the proof checker, the two-provers stage and the
    end-to-end test write.  A file that is not there is None."""
    out = {}
    for key, rel in (("proof", PROOF_CHECK), ("provers", TWO_PROVERS),
                     ("e2e", END_TO_END)):
        path = root / rel
        out[key] = (json.loads(path.read_text(encoding="utf-8"))
                    if path.exists() else None)
    return out


def coverage_cells(tests) -> tuple:
    """(admitted, excluded): the cells of the grid the case files fill.  An
    admitted cell has a test case with a verdict, an excluded one a test case
    rejected as ill sorted for that operator at that sort."""
    sort_of = sort_of_binding()
    admitted = excluded = 0
    for op, (admits, _) in SIGNATURE.items():
        for sort in (NOM, TAX, MER):
            at = [c for c in tests
                  if sort_of[c["binding"]] == sort and op in c["operators"]]
            if sort in admits:
                admitted += any(c["outcome"] in ("C", "I", "U") for c in at)
            else:
                excluded += any(c["ill_sorted"] for c in at)
    return admitted, excluded


def read_against_links(tests) -> set:
    """Every read-against link, once, whichever case states it."""
    return {frozenset((c["id"], other)) for c in tests
            for other in c["read_against"]}


def note_conflicts(tests) -> tuple:
    """(constraints in test cases with a verdict, rejected test cases): the
    constraints whose operator the DPV-ODRL notes do not list."""
    verdict = sum(len(c["note_conflicts"]) for c in tests
                  if c["outcome"] in ("C", "I", "U"))
    rejected = [c["id"] for c in tests
                if c["outcome"] == "rejected" and c["note_conflicts"]]
    return verdict, rejected


CITES = (("constraints and order axioms only", False, False),
         ("statements of the resource", True, False),
         ("declarations", False, True),
         ("statements of the resource and declarations", True, True))


def cites_counts(tests, certificates: Path) -> list:
    """(label, Compatible, Incompatible) for what each Vampire proof cites."""
    n = Counter()
    for c in tests:
        if c["outcome"] in ("C", "I"):
            sources = {src for src, _ in cited(certificates, c["id"])}
            n[("fromResource" in sources, "fromDeclarations" in sources,
               c["outcome"])] += 1
    return [(label, n[(res, decl, "C")], n[(res, decl, "I")])
            for label, res, decl in CITES]


def cites_table(rows) -> list:
    lines = [
        "\\newcommand{\\suiteCitesTable}{%",
        "\\begin{tabular}{lrrr}",
        "\\hline",
        "the proof cites & Compatible & Incompatible & total \\\\",
        "\\hline",
    ]
    for label, comp, inc in rows:
        lines.append(f"{label} & {comp} & {inc} & {comp + inc} \\\\")
    lines += ["\\hline",
              f"total & {sum(r[1] for r in rows)} & {sum(r[2] for r in rows)}"
              f" & {sum(r[1] + r[2] for r in rows)} \\\\",
              "\\hline", "\\end{tabular}%", "}"]
    return lines


def certificate_ids(certificates: Path) -> set:
    return {p.name.removesuffix("-observed.ttl")
            for p in certificates.glob("*-observed.ttl")}


def output_problems(outputs, tests, certificates: Path) -> list:
    """Why the run outputs do not fit the case files, or an empty list."""
    out = [f"{rel} not found: run full-run.sh"
           for key, rel in (("proof", PROOF_CHECK), ("provers", TWO_PROVERS),
                            ("e2e", END_TO_END)) if outputs[key] is None]
    definite = {c["id"] for c in tests if c["outcome"] in ("C", "I")}
    have = certificate_ids(certificates)
    for cid in sorted(definite - have):
        out.append(f"{cid} has a definite verdict and no observed certificate")
    for cid in sorted(have - definite):
        out.append(f"{cid} has an observed certificate and no definite verdict")
    if outputs["proof"] is not None:
        s = outputs["proof"]["summary"]
        checked = (s.get("FULLY_CHECKED", 0) + s.get("PARTIALLY_CHECKED", 0)
                   + s.get("REJECTED", 0))
        if checked != len(definite):
            out.append(f"{PROOF_CHECK} checked {checked} proofs, and "
                       f"{len(definite)} verdicts are definite")
        if set(s) - {"FULLY_CHECKED", "PARTIALLY_CHECKED", "REJECTED",
                     "SATISFIABLE"}:
            out.append(f"{PROOF_CHECK}: a query got no status: {s}")
    if outputs["provers"] is not None:
        v = outputs["provers"]
        if v["refutations"] != len(definite):
            out.append(f"{TWO_PROVERS} has {v['refutations']} refutations, and "
                       f"{len(definite)} verdicts are definite")
        if v["provenance_agree"] + len(v["provenance_differ"]) != v["refutations"]:
            out.append(f"{TWO_PROVERS}: agree and differ do not sum to the "
                       f"refutations")
        if v["status_disagreement"]:
            out.append(f"{TWO_PROVERS}: the provers disagree on "
                       + ", ".join(v["status_disagreement"]))
    if outputs["e2e"] is not None and outputs["e2e"]["disagreements"]:
        out.append(f"{END_TO_END}: the pipeline and the definitions disagree "
                   f"on {outputs['e2e']['disagreements']} problems")
    admitted, excluded = coverage_cells(tests)
    if admitted + excluded != len(SIGNATURE) * 3:
        out.append(f"the case files fill {admitted} admitted and {excluded} "
                   f"excluded cells of {len(SIGNATURE) * 3}")
    links = read_against_links(tests)
    stated = sum(len(c["read_against"]) for c in tests)
    if stated != 2 * len(links):
        out.append(f"{stated} read-against statements for {len(links)} links: "
                   f"a link is not stated from both sides")
    if sum(a + b for _, a, b in cites_counts(tests, certificates)) != len(definite):
        out.append("the proofs cited do not sum to the definite verdicts")
    return out


def suite_numbers_tex(rs, totals, timings, tests, closed, certificates,
                      outputs) -> str:
    """suite-numbers.tex: the macros and the tables."""
    definite = totals["compatible"] + totals["incompatible"]
    macros = [
        ("suiteCases",        totals["files"]),
        ("suiteQueries",      totals["queries"]),
        ("suiteDefinite",     definite),
        ("suiteCompatible",   totals["compatible"]),
        ("suiteIncompatible", totals["incompatible"]),
        ("suiteUnknown",      totals["unknown"]),
        ("suiteRejected",     totals["rejected"]),
        ("suiteIllSorted",    totals["ill_sorted"]),
        ("suiteUngrounded",   totals["ungrounded"]),
        ("suiteBindings",     len(rs)),
    ]
    lines = [
        "% suite-numbers.tex",
        "% Written by generators/table_data.py --suite-numbers. Do not edit.",
        f"% {totals['files']} cases = {definite} definite"
        f" + {totals['unknown']} Unknown + {totals['rejected']} rejected"
        f" + {totals['accepted']} accepted controls.",
        "% Rejected is ill sorted plus ungrounded.",
        "% Times: " + ", ".join(
            f"{path.as_posix().split('/')[-1]} of {head['date']}"
            for path, head, _ in timings) +
        f"; each query alone, one at a time, at most"
        f" {timings[0][1]['limit']} s.",
    ]
    admitted, excluded = coverage_cells(tests)
    conflicts, rejected_conflicts = note_conflicts(tests)
    checked = outputs["proof"]["summary"]
    macros += [
        ("suiteControls",        totals["accepted"]),
        ("suiteCellsAdmitted",   admitted),
        ("suiteCellsExcluded",   excluded),
        ("suiteNoteConflicts",   conflicts),
        ("suiteCertificates",    len(certificate_ids(certificates))),
        ("suiteFullyChecked",    checked.get("FULLY_CHECKED", 0)),
        ("suitePartlyChecked",   checked.get("PARTIALLY_CHECKED", 0)),
        ("suiteProofRejected",   checked.get("REJECTED", 0)),
        ("suiteProvenanceAgree", outputs["provers"]["provenance_agree"]),
        ("suiteEtoEProblems",    outputs["e2e"]["problems"]),
        ("suiteEtoEDisagree",    outputs["e2e"]["disagreements"]),
        ("suiteReadAgainst",     len(read_against_links(tests))),
    ]
    moved = Counter(r["closed_world"] for r in closed.values()
                    if r["expected"] == "U")
    macros += [
        ("suiteCWToCompatible",   moved["C"]),
        ("suiteCWToIncompatible", moved["I"]),
    ]
    lines.append(f"% suiteNoteConflicts counts constraints in test cases with a"
                 f" verdict. Rejected test cases hold"
                 f" {len(rejected_conflicts)} more: "
                 + ", ".join(rejected_conflicts) + ".")
    pairs = declaration_pairs(tests)
    macros.append(("suiteReadAgainstDecl", len(pairs)))
    lines.append("% Differ in the declarations only: "
                 + ", ".join("/".join(ids) for ids in pairs) + ".")
    lines += [f"\\newcommand{{\\{name}}}{{{value}}}" for name, value in macros]
    lines += [f"\\newcommand{{\\{name}}}{{{tex_escape(value)}}}"
              for name, value in time_macros(timings)]
    outcome_total = Counter()
    for r in rs:
        outcome_total.update(r["outcomes"])
    lines += [
        "\\newcommand{\\suiteBindingsTable}{%",
        "\\begin{tabular}{lllrrrrrrr}",
        "\\hline",
        "left operand & resource and binding & sort & concepts & order"
        " & test cases & C & I & U & rejected \\\\",
        "\\hline",
    ]
    for r in rs:
        o = r["outcomes"]
        lines.append(f"{tex_escape(r['operand'])} & {tex_escape(r['label'])}"
                     f" & {r['sort']} & {r['concepts']} & {r['order']}"
                     f" & {r['cases']} & {o['C']} & {o['I']} & {o['U']}"
                     f" & {o['rejected']} \\\\")
    lines += [
        "\\hline",
        f"total & & & & & {sum(r['cases'] for r in rs)}"
        f" & {outcome_total['C']} & {outcome_total['I']}"
        f" & {outcome_total['U']} & {outcome_total['rejected']} \\\\",
        "\\hline",
        "\\end{tabular}%",
        "}",
    ]
    lines += coverage_table(tests)
    lines += cites_table(cites_counts(tests, certificates))
    rows = challenges(tests, closed, certificates)
    outside = under_no_challenge(rows, tests)
    lines.insert(5, "% Under no challenge: "
                 + (", ".join(c["id"] for c in outside) or "none") + ".")
    lines += challenge_table(rows)
    lines += challenge_cw_table(rows, closed)
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", type=Path)
    ap.add_argument("--tex", action="store_true", help="table rows only")
    ap.add_argument("--macros", action="store_true",
                    help="\\newcommand lines for the results paragraph")
    ap.add_argument("--suite-numbers", nargs="?", const="suite-numbers.tex",
                    metavar="FILE",
                    help="write the macros and the bindings table "
                         "(default suite-numbers.tex, under --root)")
    ap.add_argument("--timings", type=Path, default=None,
                    help="the directory of the timing runs (default results)")
    ap.add_argument("--challenges", action="store_true",
                    help="each challenge's test cases, and those under none")
    args = ap.parse_args()

    if args.challenges:
        tests = read_cases(args.root / "cases")
        closed = read_closed_world(args.root / CLOSED_WORLD)
        problems = closed_world_problems(closed, tests)
        if problems:
            print("\n".join(problems), file=sys.stderr)
            return 1
        print_challenges(challenges(tests, closed, args.root / "certificates"),
                         tests)
        return 0

    rs = rows(args.root)
    totals = suite_totals(args.root / "cases",
                          args.root / "problems" / "verdict")

    if args.suite_numbers:
        timings = read_timings(args.timings or args.root / RESULTS)
        tests = read_cases(args.root / "cases")
        closed = read_closed_world(args.root / CLOSED_WORLD)
        problems = suite_problems(rs, totals) + timing_problems(
            timings, args.root / "problems" / "verdict") + \
            closed_world_problems(closed, tests)
        outputs = read_outputs(args.root)
        problems += output_problems(outputs, tests, args.root / "certificates")
        if problems:
            print("not written, the figures do not add up:", file=sys.stderr)
            for pr in problems:
                print(f"  {pr}", file=sys.stderr)
            return 1
        out = args.root / args.suite_numbers
        out.write_text(suite_numbers_tex(
            rs, totals, timings, tests, closed, args.root / "certificates",
            outputs),
            encoding="utf-8")
        print(f"wrote {out}: {totals['files']} cases, {len(rs)} bindings")
        return 0

    if args.tex:
        for r in rs:
            print(f"{r['label']:32} & {r['sort']} & {r['concepts']:5} & "
                  f"{r['order']:5} & {r['cases']:3} & \\\\")
        print(f"% cases sum: {sum(r['cases'] for r in rs)}")
        return 0

    if args.macros:
        print(f"\\newcommand{{\\suiteCases}}{{{totals['files']}}}")
        print(f"\\newcommand{{\\suiteQueries}}{{{totals['queries']}}}")
        print(f"\\newcommand{{\\suiteDefinite}}"
              f"{{{totals['compatible'] + totals['incompatible']}}}")
        print(f"\\newcommand{{\\suiteCompatible}}{{{totals['compatible']}}}")
        print(f"\\newcommand{{\\suiteIncompatible}}{{{totals['incompatible']}}}")
        print(f"\\newcommand{{\\suiteUnknown}}{{{totals['unknown']}}}")
        # Old name, kept until the paper stops using it.
        print("\\newcommand{\\suiteUndetermined}{\\suiteUnknown}")
        print(f"\\newcommand{{\\suiteEpistemic}}{{{totals['epistemic']}}}")
        print(f"\\newcommand{{\\suiteUngrounded}}{{{totals['ungrounded']}}}")
        return 0

    w = max(len(r["label"]) for r in rs)
    print(f"{'resource and binding':{w}}  sort  concepts  order  test cases")
    for r in rs:
        print(f"{r['label']:{w}}  {r['sort']:4}  {r['concepts']:8}  "
              f"{r['order']:5}  {r['cases']:5}")
    print(f"{'':{w}}  {'':4}  {'':8}  {'':5}  "
          f"{sum(r['cases'] for r in rs):5}   total")

    print("\nwhat each profile says it reads")
    for r in rs:
        print(f"  {r['label']:{w}}  {r['reads'] or 'NO HEADER LINE FOUND'}")

    print("\nthe suite")
    for k, v in totals.items():
        print(f"  {k:14} {v}")

    missing = [r["label"] for r in rs if r["concepts"] < 0 or r["order"] < 0]
    if missing:
        print(f"\nfiles not found for: {', '.join(missing)}")
        print("check the tag and axiom names at the top of this script")
    if totals["files"] != sum(r["cases"] for r in rs):
        print(f"\ncase files {totals['files']} but rows sum to "
              f"{sum(r['cases'] for r in rs)}: some case file carries no "
              f"binding, or carries one not in BINDINGS")
    return 0


if __name__ == "__main__":
    sys.exit(main())