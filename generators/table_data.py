#!/usr/bin/env python3
"""
table_data.py
=============
Every figure the evaluation table needs, measured rather than recalled.

    uv run generators/table_data.py                 # readable
    uv run generators/table_data.py --tex > tab.tex # LaTeX rows
    uv run generators/table_data.py --macros        # \newcommand lines
    uv run generators/table_data.py --suite-numbers # writes suite-numbers.tex

Each row is one binding, not one resource: a file read under two
profiles produces two rows, which is the table's point. Counts come from
the generated artefacts, so a figure that moves when a builder changes
moves here too.

--suite-numbers writes suite-numbers.tex: ten macros of counts, six from the
timing pass and the bindings table, for the paper to include. It refuses to
write when the numbers do not add up: the rows must sum to the case files,
every case must fall in exactly one of definite, Unknown, rejected and
accepted, and every binding a case cites must have a row. A file that is
written is therefore one whose figures agree.

The six time macros come from results/timings.csv, which
generators/time_queries.py writes: the seconds of all runs together, the
slowest query, the limit, the machine, and the two prover versions. The file
must time every current query under its prover and nothing else, or
suite-numbers.tex is not written.

What is counted, per row:

    concepts     subjects the resource file types as its concept class
    order        kge_leq statements in the resource's .ax file
    cases        verdict problems whose binding is this one
    reads        the relation the profile's prose says the sort takes

The last is the only field not measured. It is read from the profile
file's header comment, since no triple states it: the profile declares
bind:sort and bind:resource, and which published relation that sort is
taken from is a claim the header makes in prose.
"""
import argparse
import csv
import re
import sys
from collections import Counter
from pathlib import Path

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


def rows(root: Path):
    cases = cases_by_binding(root / "cases")
    out = []
    for label, tag, sort, binding in BINDINGS:
        out.append({
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


TIMINGS = Path("results") / "timings.csv"
PROVER = {"vampire": "Vampire", "z3": "Z3"}


def read_timings(path: Path):
    """(header, rows) of the timing pass, or None when there is no file."""
    if not path.exists():
        return None
    header, body = {}, []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            key, sep, value = line[1:].strip().partition(": ")
            if sep:
                header[key] = value
        elif line.strip():
            body.append(line)
    return header, list(csv.DictReader(body))


def timing_problems(timings, verdict_dir: Path) -> list:
    """Why the timing file does not fit the suite, or an empty list."""
    if timings is None:
        return [f"{TIMINGS} not found: run generators/time_queries.py"]
    header, rows = timings
    out = [f"{TIMINGS} has no {k} line in its header"
           for k in ("vampire", "z3", "cpu", "ram", "date", "limit")
           if k not in header]
    want = {(q.stem, "vampire") for q in verdict_dir.glob("*-[12].p")} \
        | {(q.stem, "z3") for q in verdict_dir.glob("*-[12].smt2")}
    have = [(r["query"], r["prover"]) for r in rows]
    if len(have) != len(set(have)):
        out.append(f"{TIMINGS} times a query twice")
    for what, runs in (("has no time for", want - set(have)),
                       ("times what is not a query of the suite:", set(have) - want)):
        if runs:
            shown = ", ".join(f"{q} under {PROVER.get(p, p)}" for q, p in sorted(runs)[:4])
            more = f" and {len(runs) - 4} more" if len(runs) > 4 else ""
            out.append(f"{TIMINGS} {what} {shown}{more}: "
                       f"run generators/time_queries.py")
    return out


def time_macros(timings) -> list:
    """The six macros of the timing pass."""
    header, rows = timings
    total = sum(float(r["seconds"]) for r in rows)
    slow = max(rows, key=lambda r: float(r["seconds"]))
    # "Intel(R) Core(TM) Ultra 7 165U, 14 logical cores" -> "Intel Core Ultra 7 165U"
    cpu = header["cpu"].split(", ")[0]
    cpu = re.sub(r"\((R|TM)\)|\bCPU\b|\bProcessor\b|@.*", "", cpu)
    cpu = " ".join(cpu.split())

    def version(line, pattern):
        m = re.search(pattern, line)
        return m.group(1) if m else line

    return [
        ("suiteTime",     f"{total:.1f}"),
        ("suiteSlowest",  f"{slow['query']} ({PROVER[slow['prover']]}, "
                          f"{float(slow['seconds']):.1f} s)"),
        ("suiteLimit",    header["limit"]),
        ("suiteHardware", f"{cpu}, {header['ram']} RAM"),
        ("suiteVampire",  version(header["vampire"], r"Vampire (\S+)")),
        ("suiteZthree",   version(header["z3"], r"version (\S+)")),
    ]


def tex_escape(s: str) -> str:
    for ch in "\\&%$#_{}":
        s = s.replace(ch, "\\" + ch)
    return s


def suite_numbers_tex(rs, totals, timings) -> str:
    """suite-numbers.tex: the macros and the bindings table."""
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
        f"% Times: {TIMINGS}, {timings[0]['date']}, each query alone,"
        f" one at a time, at most {timings[0]['limit']} s.",
    ]
    lines += [f"\\newcommand{{\\{name}}}{{{value}}}" for name, value in macros]
    lines += [f"\\newcommand{{\\{name}}}{{{tex_escape(value)}}}"
              for name, value in time_macros(timings)]
    lines += [
        "\\newcommand{\\suiteBindingsTable}{%",
        "\\begin{tabular}{llrrr}",
        "\\hline",
        "resource and binding & sort & concepts & order & cases \\\\",
        "\\hline",
    ]
    for r in rs:
        lines.append(f"{tex_escape(r['label'])} & {r['sort']} & {r['concepts']}"
                     f" & {r['order']} & {r['cases']} \\\\")
    lines += [
        "\\hline",
        f"total & & & & {sum(r['cases'] for r in rs)} \\\\",
        "\\hline",
        "\\end{tabular}%",
        "}",
    ]
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
    args = ap.parse_args()

    rs = rows(args.root)
    totals = suite_totals(args.root / "cases",
                          args.root / "problems" / "verdict")

    if args.suite_numbers:
        timings = read_timings(args.root / TIMINGS)
        problems = suite_problems(rs, totals) + timing_problems(
            timings, args.root / "problems" / "verdict")
        if problems:
            print("not written, the figures do not add up:", file=sys.stderr)
            for pr in problems:
                print(f"  {pr}", file=sys.stderr)
            return 1
        out = args.root / args.suite_numbers
        out.write_text(suite_numbers_tex(rs, totals, timings), encoding="utf-8")
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
    print(f"{'resource and binding':{w}}  sort  concepts  order  cases")
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