#!/usr/bin/env python3
"""
table_data.py
=============
Every figure the evaluation table needs, measured rather than recalled.

    uv run generators/table_data.py                 # readable
    uv run generators/table_data.py --tex > tab.tex # LaTeX rows
    uv run generators/table_data.py --macros        # \newcommand lines

Each row is one binding, not one resource: a file read under two
profiles produces two rows, which is the table's point. Counts come from
the generated artefacts, so a figure that moves when a builder changes
moves here too.

What is counted, per row:

    concepts     subjects the resource file types as its concept class
    order        kge_leq assertions in the resource's .ax file
    cases        verdict problems whose binding is this one
    reads        the relation the profile's prose says the sort takes

The last is the only field not measured. It is read from the profile
file's header comment, since no triple states it: the profile declares
bind:sort and bind:resource, and which published relation that sort is
taken from is a claim the header makes in prose.
"""
import argparse
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
    ("GDPR Article 6 bases",         "gdprlb",         "tax", "b-legalbasis"),
    ("DPV Locations, geographic",    "dpvloc-geo",     "mer", "b-spatial-dpvloc-geo"),
    ("DPV Locations, jurisdictional","dpvloc-juris",   "mer", "b-spatial-dpvloc-juris"),
    ("EU file type table",           "filetype",       "nom", "b-fileformat"),
    ("BCP 47 subtags",               "bcp47",          "nom", "b-language"),
]

# The axiom file each resource writes, since the naming is not uniform.
AXIOMS = {
    "dpv-purposes":   "DPV-dpv-purposes.ax",
    "consent":        "DPV-consent.ax",
    "tom":            "DPV-tom.ax",
    "gdprlb":         "DPV-gdprlb.ax",
    "dpvloc-geo":     "LOC-dpvloc-geo.ax",
    "dpvloc-juris":   "LOC-dpvloc-juris.ax",
    "filetype":       "EUFT-filetype.ax",
    "bcp47":          "BCP47000-0.ax",
}


def count_order(ax_path: Path) -> int:
    """kge_leq assertions in a resource axiom file."""
    if not ax_path.exists():
        return -1
    return len(re.findall(r"^fof\(res_\S+,\s*axiom,\s*\n?\s*kge_leq",
                          ax_path.read_text(encoding="utf-8"), re.M))


def count_concepts(ttl_path: Path) -> int:
    """Subjects the resource types as its concept class.

    Counted from the Turtle rather than from the axioms: a concept the
    resource lists and no assertion mentions is still a concept, and the
    nominal resources are exactly the ones where that matters.
    """
    if not ttl_path.exists():
        return -1
    text = ttl_path.read_text(encoding="utf-8")
    return len(re.findall(r"^\S+\s+a\s+odrlkb:\w+\s*[;.]", text, re.M))


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
    reasons = Counter()
    for f in files:
        t = f.read_text(encoding="utf-8")
        m = re.search(r"report:satisfactionState\s+(\S+)\s*[;.]", t)
        if m:
            states[m.group(1)] += 1
        m = re.search(r"vrep:undeterminedReason\s+vrep:(\w+)", t)
        if m:
            reasons[m.group(1)] += 1
    queries = len(list(verdict_dir.glob("*-[12].p")))
    return {
        "files": len(files),
        "queries": queries,
        "satisfied": states.get("report:Satisfied", 0),
        "unsatisfied": states.get("report:Unsatisfied", 0),
        "undetermined": states.get("vrep:Undetermined", 0),
        "epistemic": reasons.get("Epistemic", 0),
        "ungrounded": reasons.get("Ungrounded", 0),
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", type=Path)
    ap.add_argument("--tex", action="store_true", help="table rows only")
    ap.add_argument("--macros", action="store_true",
                    help="\\newcommand lines for the results paragraph")
    args = ap.parse_args()

    rs = rows(args.root)
    totals = suite_totals(args.root / "cases",
                          args.root / "problems" / "verdict")

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
              f"{{{totals['satisfied'] + totals['unsatisfied']}}}")
        print(f"\\newcommand{{\\suiteCompatible}}{{{totals['satisfied']}}}")
        print(f"\\newcommand{{\\suiteIncompatible}}{{{totals['unsatisfied']}}}")
        print(f"\\newcommand{{\\suiteUndetermined}}{{{totals['undetermined']}}}")
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