#!/usr/bin/env python3
"""
export_tptp.py
==============
The suite's queries as problems for the TPTP library.

    uv run generators/export_tptp.py [--out tptp] [--runs results/tptp-runs.csv]

Writes

    tptp/Problems/KGC/KGCnnn+1.p   version 1: one problem per query, the
                                   query's own formulas
    tptp/Problems/KGC/KGCnnn+2.p   version 2: the same problem with the
                                   condition written over the whole
                                   vocabulary, where it is written
    tptp/Axioms/KGC000+0.ax        the order axioms
    tptp/Axioms/KGC000+N.ax        one file per vocabulary
    tptp/manifest.csv              one row per file

The repository's own files keep their names; nothing under problems/ or
cases/ changes.  The names follow the TPTP manual: one abstract problem per
query, numbered KGC001 to KGC122 in the order of the original names, which
go in % Names and in the manifest.  KGC is a provisional domain code; the
maintainer assigns the real domain and numbers.

Version 1 is the query as the repository writes it: the same formulas, the
includes renamed, the includes of files that carry no formula left out (the
rule-form declaration files, whose instances the problem itself carries,
and the EU file type resource, which publishes no order).

Version 2 lists every concept of the binding's vocabulary in every part of
the condition (compile.py with full=True, which the candidate rule is
checked against), with the declaration instances among all concepts of the
vocabulary.  The resource statements are the same, since version 1 already
includes the whole axiom file.  Version 2 is not written where the set of
declarations has more than MAX_PAIRS pairs over the vocabulary (the ISO
rule over the DPV Locations, twelve million), nor where it would be the
same formulas as version 1.  Both are listed, with the reason, in
tptp/README.

--runs reads the Vampire results generators/run_tptp.py writes, for the
manifest and for the comment a version 2 problem gets when no mode solved
it.
"""

import argparse
import csv
import importlib
import re
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import DCTERMS

import declarations
import vocabulary
from compile import FOF, render, tree_term
from tree_expand import _map_item, constants_of_tree

ROOT = Path(__file__).resolve().parent.parent
VREP = Namespace("https://w3id.org/odrl-kb/verdict-report#")
DRK = Namespace("https://w3id.org/odrl-kb/drk/")

REPO = "https://github.com/Daham-Mustaf/odrl-grounded-benchmark"
TAG = "v1.1.1"
REF = (f"[Mus26] Mustafa (2026), odrl-grounded-benchmark, {REPO}, "
       f"tag {TAG}")
DOMAIN = "Semantic Web (ODRL policies), proposed"
MAX_PAIRS = 25_000

MODULES = ["problem_data_motivating", "problem_data_geonames",
           "problem_data_dpv", "problem_data_dpvloc",
           "problem_data_filetype", "problem_data_consent",
           "problem_data_tom", "problem_data_bcp47"]

CHECK = {1: "some use meets the two policies",
         2: "no use meets the two policies"}
SHORT = {1: "some use meets both", 2: "no use meets both"}

# The axiom files with formulas, in the order of their export names.
# (repository file, axiomatisation, English, licence of the source).
DPV_LICENCE = ("W3C Document License 2023. The DPV Community Group's "
               "permission to redistribute this derived slice is not yet "
               "recorded.")
AXIOMS = [
    ("KGE000-0.ax", "A partial order",
     "The order the vocabularies' statements are read in: reflexive, "
     "antisymmetric and transitive. Equality is built in.",
     "CC BY 4.0, this project."),
    ("BCP47000-0.ax", "BCP 47, fifteen primary language subtags",
     "Fifteen primary language subtags of the IANA Language Subtag "
     "Registry (File-Date 2026-08-08). The registry publishes no relation "
     "between them, so the file states only that each is a concept.",
     "IANA states that its protocol registries may be freely used (CC0 1.0 "
     "for rights IANA or IETF hold); https://www.iana.org/help/licensing-terms"),
    ("DPV-consent.ax", "DPV 2.3, consent status",
     "The 12 statements of the consent status module of the Data Privacy "
     "Vocabulary 2.3 that place one of its 13 consent statuses below "
     "another.", DPV_LICENCE),
    ("DPV-dpv-purposes.ax", "DPV 2.3, purposes",
     "The 131 statements of the purposes module of the Data Privacy "
     "Vocabulary 2.3 that place one of its 121 purposes below another.",
     DPV_LICENCE),
    ("DPV-tom.ax", "DPV 2.3, technical and organisational measures",
     "The 75 statements of the Data Privacy Vocabulary 2.3 that place one "
     "of 74 technical and organisational measures below another.",
     DPV_LICENCE),
    ("GN000-0.ax", "GeoNames, a Europe slice",
     "Fifteen places of GeoNames, from Europe down to three cities, each "
     "stated a concept, and the 14 statements that place one within "
     "another.", "CC BY 4.0, credit GeoNames, https://www.geonames.org"),
    ("LOC-dpvloc-geo.ax", "DPV 2.3 Locations, geographic reading",
     "The 4786 statements of the DPV Locations extension 2.3 that place a "
     "region within a country or a country within a country, and the 30 "
     "pairs of ISO codes it publishes as one place, each written as two "
     "order statements: 4846 in all.", DPV_LICENCE),
    ("LOC-dpvloc-juris.ax", "DPV 2.3 Locations, jurisdictional reading",
     "The 4963 statements of the DPV Locations extension 2.3 that place a "
     "region within a country, a country within a country, or a country "
     "within a union such as the EU or the EEA, and the 30 pairs of ISO "
     "codes it publishes as one place, each written as two order "
     "statements: 5023 in all.", DPV_LICENCE),
]
AXIOM_NAME = {repo: f"KGC000+{i}.ax" for i, (repo, *_rest) in enumerate(AXIOMS)}


# --- the header ------------------------------------------------------------

def field(name: str, text: str, wrap: bool = True) -> list:
    """A header field, wrapped at 78 columns unless wrap is False."""
    head = f"% {name:<9}: "
    if not wrap:
        return [head + text]
    lines = textwrap.wrap(text, 78 - len(head)) or [""]
    return [head + lines[0]] + ["%" + " " * (len(head) - 1) + l for l in lines[1:]]


def header(fields: list) -> str:
    rule = "%" + "-" * 78
    out = [rule]
    for item in fields:
        if item is None:
            out.append("")
        elif isinstance(item, str):
            out.append(item)
        else:
            out += field(*item)
    out.append(rule)
    return "\n".join(out) + "\n"


# --- what the repository holds ---------------------------------------------

def formulas_of(text: str) -> list:
    """The annotated formulas of a file, one string each, comments dropped."""
    body = [l for l in text.splitlines()
            if l.strip() and not l.lstrip().startswith("%")
            and not l.startswith("include(")]
    out, cur = [], []
    for line in body:
        if re.match(r"(fof|cnf|tff|thf)\(", line) and cur:
            out.append("\n".join(cur))
            cur = []
        cur.append(line.rstrip())
    if cur:
        out.append("\n".join(cur))
    return out


def has_formulas(repo_ax: str) -> bool:
    return bool(formulas_of((ROOT / "problems/axioms" / repo_ax).read_text()))


def read_query(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    return {
        "status": re.search(r"^% Status\s*:\s*(\w+)", text, re.M).group(1),
        "includes": re.findall(r"^include\('axioms/([^']+)'\)\.", text, re.M),
        "formulas": formulas_of(text),
    }


def read_case(cid: str) -> dict:
    g = Graph().parse(ROOT / "cases" / f"{cid}.ttl", format="turtle")
    rep = DRK[f"{cid}-report"]
    n = cid[3:]
    titles = [str(g.value(DRK[f"policy-{n}-{i}"], DCTERMS.title) or "")
              for i in (1, 2)]
    state = g.value(rep, VREP.compatibilityState)
    return {"story": " ".join(str(g.value(rep, DCTERMS.description)).split()),
            "verdict": str(state).rsplit("#", 1)[-1],
            "titles": titles}


def problems_by_id() -> dict:
    out = {}
    for m in MODULES:
        for p in importlib.import_module(m).PROBLEMS:
            out[p["id"]] = p
    return out


# --- version 2 ---------------------------------------------------------------

GROUP = 64


class Grouped(FOF):
    """FOF with a long disjunction or conjunction grouped in balanced
    parentheses, at most GROUP members to a group.  The formula is the same;
    it nests about log n deep rather than n, so that a recursive parser
    such as tptp4X's does not run out of stack on ten thousand disjuncts."""

    def and_(self, xs):
        return self._group(list(xs), FOF.and_)

    def or_(self, xs):
        return self._group(list(xs), FOF.or_)

    def _group(self, xs, join):
        while len(xs) > GROUP:
            xs = [join(self, xs[i:i + GROUP]) for i in range(0, len(xs), GROUP)]
        return join(self, xs)


def version2(p: dict, q: int):
    """(formulas as written, the same ungrouped, pairs) of version 2, or
    (None, None, pairs) when the set of declarations is too large to write
    out."""
    decl = declarations.set_for(p.get("background_theory"))
    every = vocabulary.concepts(p["resource"])
    if decl is not None:
        constant = declarations.constant_for(decl.applies_to[0])
        members = {constant(m) for m in decl.members}
        k = sum(1 for c in every if c in members)
        pairs = k * (k - 1) // 2 + len(decl.disjoint)
        if pairs > MAX_PAIRS:
            return None, None, pairs
    tree = p["tree"]
    if p.get("grounding"):
        tree = [_map_item(i, p["grounding"]) for i in tree]
    candidates = vocabulary.candidates(p["resource"], constants_of_tree(tree))
    term = tree_term(tree, candidates, p["sort"], full=True)
    fof_d, _, pairs = declarations.statements(decl, candidates, candidates)
    out = []
    for syntax in (Grouped(), FOF()):
        condition = render(term, syntax).strip().replace("\n", "\n    ")
        if q == 2:
            condition = f"~ ( {condition} )"
        out.append(formulas_of(fof_d) + [
            f"fof(w_{p['id'].lower()}, axiom,\n    {condition})."])
    return out[0], out[1], pairs


def normal(formulas: list) -> list:
    return sorted(" ".join(f.split()) for f in formulas)


# --- writing -----------------------------------------------------------------

def problem_text(name, version, original, case, q, status, includes,
                 formulas, partner, comment_extra="") -> str:
    check = CHECK[q]
    first, second = (name[:6], partner) if q == 1 else (partner, name[:6])
    s1, s2 = (status, case["other_status"]) if q == 1 else \
        (case["other_status"], status)
    t = [x for x in case["titles"] if x]
    titles = " against ".join([t[0]] + [x[:1].lower() + x[1:] for x in t[1:]])
    version_field = [("Version", "Especial.")]
    if version == 2:
        version_field += textwrap.wrap(
            "Theorem formulation : The condition is written over the whole "
            "vocabulary, as the paper's definition states; version 1 names "
            "only the concepts a fixed value allows. The two versions have "
            "the same status.", 78, initial_indent="%            ",
            subsequent_indent="%            ")
    comments = (
        f"{original[:6]} is {case['verdict']}. Its two problems state that "
        f"some use meets the two policies ({first}) and that no use does "
        f"({second}). A pair of policies is Incompatible when the first is "
        f"Unsatisfiable, Compatible when the second is Unsatisfiable, and "
        f"Unknown when both are Satisfiable; a Satisfiable problem also shows "
        f"the statements consistent. Here the first is {s1} and the second "
        f"{s2}." + comment_extra)
    head = header([
        ("File", f"{name} : placeholder, for TPTP use only"),
        ("Domain", DOMAIN),
        ("Problem", f"{titles}: {SHORT[q]}", False),
        *version_field,
        ("English", f"{case['story']} This problem states that {check}."),
        None,
        ("Refs", REF),
        ("Source", "[Mus26]"),
        ("Names", f"{original} [Mus26]"),
        None,
        ("Status", status),
        ("Rating", "left to TPTP"),
        ("Syntax", "left to TPTP"),
        ("SPC", "left to TPTP"),
        None,
        ("Comments", comments),
    ])
    body = "".join(f"include('Axioms/{a}').\n" for a in includes)
    body += "\n" + "\n\n".join(formulas) + "\n"
    return head + body + "%" + "-" * 78 + "\n"


def axiom_text(i: int) -> str:
    repo, title, english, licence = AXIOMS[i]
    formulas = formulas_of((ROOT / "problems/axioms" / repo).read_text())
    head = header([
        ("File", f"KGC000+{i} : placeholder, for TPTP use only"),
        ("Domain", DOMAIN),
        ("Axioms", title),
        ("Version", "Especial."),
        ("English", english),
        None,
        ("Refs", REF),
        ("Source", "[Mus26]"),
        ("Names", f"{repo} [Mus26]"),
        None,
        ("Status", "Satisfiable"),
        ("Syntax", "left to TPTP"),
        None,
        ("Comments", f"Licence of the source: {licence}"),
    ])
    return head + "\n" + "\n\n".join(formulas) + "\n" + "%" + "-" * 78 + "\n"


def readme(rows: list, left_out: list) -> str:
    """tptp/README, from the rows of the manifest."""
    from collections import Counter
    v1 = [r for r in rows if r["version"] == 1]
    v2 = [r for r in rows if r["version"] == 2]
    by_status = Counter(r["status"] for r in v1)
    v2_status = Counter(r["status"] for r in v2)
    v1_ok = sum(1 for r in v1 if r["Vampire result"] == r["status"])
    v2_mode = Counter(r["mode"] for r in v2 if r["Vampire result"] == r["status"])
    v2_open = [r for r in v2 if r["Vampire result"] != r["status"]]
    slow = sorted((r for r in v2 if r["time"]), key=lambda r: -float(r["time"]))[:10]
    why = Counter(w for _, _, w in left_out)
    cases = len({r["case"] for r in v1})
    count = lambda c: ", ".join(f"{n} {k}" for k, n in sorted(c.items()))

    out = []

    def title(t):
        out.extend([t, "-" * len(t), ""])

    def para(t):
        # A number and its unit stay on one line; a URL is not broken.
        t = re.sub(r"(\d) (s\b|seconds)", "\\1\u00a0\\2", t)
        lines = textwrap.wrap(t, 74, break_on_hyphens=False,
                              break_long_words=False)
        out.extend([l.replace("\u00a0", " ") for l in lines] + [""])

    def table(lines):
        out.extend(["    " + l for l in lines] + [""])

    out.extend(["KGC: ODRL policy pairs over published vocabularies",
                "=" * 50, ""])
    para(f"A TPTP export of the odrl-grounded-benchmark, {REPO}, tag {TAG}. "
         "The names are provisional: KGC is a proposed domain code and the "
         "problems are numbered in sequence. The original name of each "
         "problem is in its % Names field and in manifest.csv.")
    title("What the problems are")
    para(f"The {len(v1)} problems come from {cases} pairs of ODRL policies "
         "(Open Digital Rights Language). Each pair constrains one property "
         "of a use, such as its purpose, its place, its language or its file "
         "type, with values from a published vocabulary: the Data Privacy "
         "Vocabulary, its Locations extension, GeoNames, the EU file type "
         "table or the IANA Language Subtag Registry. The question is "
         "whether some use can meet both policies.")
    para("A problem holds the vocabulary's published statements, read as a "
         "partial order (Axioms/KGC000+0.ax and one file per vocabulary); "
         "the declarations the parties make, that two values are distinct "
         "or that nothing lies below both, written in the problem; and one "
         "condition: that some use meets the two policies, or that no use "
         "does. Equality is built in and no axioms of equality are added. "
         "An inequation is written only where a declaration states it: two "
         "names are not assumed to name two things. Every problem is "
         "function-free FOF without a conjecture, so its status is "
         "Satisfiable or Unsatisfiable.")
    title("How a verdict follows")
    para("Each pair of policies has two problems: one states that some use "
         "meets the two policies, the other that no use does.")
    table(["first Unsatisfiable      Incompatible",
           "second Unsatisfiable     Compatible",
           "both Satisfiable         Unknown"])
    para("Both Unsatisfiable would mean the statements contradict each "
         "other; it does not occur. A Satisfiable problem also shows that "
         "the statements are consistent, so there is no separate consistency "
         "problem. The % Comments of each problem name its partner and the "
         "pair's verdict.")
    title("Versions")
    para(f"Version 1 (+1), {len(v1)} problems: {count(by_status)}. These are "
         "the queries of the repository. Where a constraint fixes the value "
         "of the use, the condition tries only the concepts that value "
         "allows; elsewhere it lists every concept of the vocabulary. The "
         "declaration instances are those among the concepts the condition "
         "names and the concepts that lie between two of them, which gives "
         "the same status as all of them (the repository's tree_expand.py "
         "says why).")
    para(f"Version 2 (+2), {len(v2)} problems: {count(v2_status)}. The "
         "condition lists every concept of the vocabulary in every part, as "
         "the paper's definition states, with the declaration instances "
         "among all concepts of the vocabulary. The two versions have the "
         "same status. A disjunction or conjunction of more than 64 members "
         "is written in balanced groups of at most 64; it is the same "
         "formula, nested about log n deep, so that a recursive parser does "
         "not run out of stack on the ten thousand disjuncts of the largest.")
    iso = sum(n for w, n in why.items() if "ISO" in w)
    same = sum(n for w, n in why.items() if "same formulas" in w)
    pairs = next((w.split()[2] for w in why if "ISO" in w), "")
    para(f"Version 2 is not written for {len(left_out)} problems: {iso} "
         f"under the ISO rule, whose declarations have {pairs} pairs over "
         f"the vocabulary, and {same} whose condition and declarations "
         f"come out the same in both versions, so that version 2 would "
         f"repeat version 1.")
    table([f"{name:10} {original:10} {w}" for name, original, w in left_out])
    title("Provers")
    para("Vampire 5.0.1, the release binary (commit 1b13eaf), one problem at "
         "a time: version 1 with --mode casc at 60 s; version 2 with --mode "
         "casc at 300 s and, for a Satisfiable problem casc did not solve, "
         "--mode casc_sat at 300 s. The repository also decides every pair "
         "with Z3 4.8.12 on an SMT-LIB encoding of the same statements; that "
         "encoding is not part of this export.")
    para(f"Version 1: {v1_ok} of {len(v1)} solved with the stated status. "
         f"Version 2: " + (", ".join(f"{n} solved with --mode {m}"
                                     for m, n in sorted(v2_mode.items()))
                           or "no runs recorded")
         + f"; {len(v2_open)} not solved within the limit"
         + ("." if not v2_open else
            ", whose status equals version 1's by construction: "
            + ", ".join(r["problem"] for r in v2_open) + "."))
    if slow:
        para("The slowest version 2 problems:")
        table([f"{r['problem']:10} {r['original name']:10} "
               f"{r['Vampire result']:15} {r['mode']:9} {float(r['time']):7.1f} s"
               for r in slow])
    para("Every file parses with tptp4X -x -w, includes expanded, with no "
         "warning. tptp4X was built from the TPTP World sources "
         "(github.com/TPTPWorld/TPTP4X at ce83fd4, JJParser at 94a781a).")
    title("Layout")
    table(["Problems/KGC/KGCnnn+1.p    version 1",
           "Problems/KGC/KGCnnn+2.p    version 2",
           "Axioms/KGC000+0.ax         the order axioms",
           "Axioms/KGC000+1.ax ...     one file per vocabulary",
           "manifest.csv               one row per problem: problem, version,",
           "                           original name, case, check, status,",
           "                           case verdict, axiom files, Vampire",
           "                           result, mode, time"])
    para("Includes are written include('Axioms/KGC000+N.ax'), relative to "
         "this folder.")
    title("Licences")
    for i, (repo, name, _e, licence) in enumerate(AXIOMS):
        out.extend(textwrap.wrap(f"KGC000+{i}.ax, {name}: {licence}", 74,
                                 subsequent_indent="    "))
    out.extend(textwrap.wrap(
        "The EU file type table (EU Vocabularies, Publications Office of the "
        "European Union, version 20260715-0) gives the names of the file "
        "types and no statement, so it has no axiom file: CC BY 4.0. The "
        "repository records that the reuse terms of the snapshot are still "
        "to be confirmed.", 74, subsequent_indent="    "))
    out.extend(textwrap.wrap(
        "The problems, the conditions and the declarations: CC BY 4.0, this "
        "project.", 74, subsequent_indent="    "))
    out.append("")
    para("The DPV-derived files are not to be redistributed until the DPV "
         "Community Group's permission is recorded in the repository's "
         "README.")
    return "\n".join(out)


def read_runs(path: Path) -> dict:
    """problem file -> list of (mode, result, seconds), in run order."""
    out = {}
    if path and path.exists():
        with path.open(encoding="utf-8") as f:
            for r in csv.DictReader(f):
                out.setdefault(r["problem"], []).append(
                    (r["mode"], r["result"], r["seconds"]))
    return out


def solved(runs: list, status: str):
    """The first run that found the status, or None."""
    return next(((m, r, s) for m, r, s in runs if r == status), None)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[3])
    ap.add_argument("--out", default=ROOT / "tptp", type=Path)
    ap.add_argument("--runs", default=ROOT / "results" / "tptp-runs.csv", type=Path)
    args = ap.parse_args()

    queries = sorted((ROOT / "problems/verdict").glob("KGC*-[12].p"),
                     key=lambda p: (p.stem[:6], p.stem[-1]))
    numbers = {q.stem: f"KGC{i:03d}" for i, q in enumerate(queries, 1)}
    problems = problems_by_id()
    runs = read_runs(args.runs)

    pdir, adir = args.out / "Problems" / "KGC", args.out / "Axioms"
    for d in (pdir, adir):
        d.mkdir(parents=True, exist_ok=True)
        for old in d.iterdir():
            old.unlink()
    for i in range(len(AXIOMS)):
        (adir / f"KGC000+{i}.ax").write_text(axiom_text(i), encoding="utf-8")

    rows, left_out = [], []
    cases = {}
    for qpath in queries:
        cid, q = qpath.stem[:6], int(qpath.stem[-1])
        cases.setdefault(cid, read_case(cid))
    for qpath in queries:
        original, cid, q = qpath.stem, qpath.stem[:6], int(qpath.stem[-1])
        partner_stem = f"{cid}-{3 - q}"
        abstract, partner = numbers[original], numbers[partner_stem]
        v1 = read_query(qpath)
        other = read_query(qpath.with_name(f"{partner_stem}.p"))
        case = dict(cases[cid], other_status=other["status"])
        unknown = [a for a in v1["includes"]
                   if has_formulas(a) and a not in AXIOM_NAME]
        if unknown:
            raise SystemExit(f"{original} includes {unknown}, which has "
                             f"formulas and no export name")
        includes = [AXIOM_NAME[a] for a in v1["includes"] if a in AXIOM_NAME]
        dropped = [a for a in v1["includes"] if a not in AXIOM_NAME]

        for version in (1, 2):
            name = f"{abstract}+{version}"
            if version == 1:
                formulas = v1["formulas"]
            else:
                formulas, plain, pairs = version2(problems[cid], q)
                if formulas is None:
                    left_out.append((name, original, f"declarations of "
                                     f"{pairs:,} pairs (the ISO rule)"))
                    continue
                if normal(plain) == normal(v1["formulas"]):
                    left_out.append((name, original, "the same formulas "
                                     "as version 1"))
                    continue
            r = runs.get(f"{name}.p", [])
            hit = solved(r, v1["status"])
            extra = ""
            if version == 2 and r and hit is None:
                extra = (" Vampire 5.0.1 did not solve this version within "
                         "300 s in casc or casc_sat mode; its status equals "
                         "version 1's by construction.")
            text = problem_text(name, version, original, case, q,
                                v1["status"], includes, formulas, partner,
                                extra)
            (pdir / f"{name}.p").write_text(text, encoding="utf-8")
            last = hit or (r[-1] if r else ("", "", ""))
            rows.append({
                "problem": name, "version": version, "original name": original,
                "case": cid, "check": CHECK[q], "status": v1["status"],
                "case verdict": case["verdict"],
                "axiom files": " ".join(includes),
                "Vampire result": last[1], "mode": last[0], "time": last[2],
            })

    with (args.out / "manifest.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    (args.out / "README").write_text(readme(rows, left_out),
                                     encoding="utf-8")
    v1n = sum(1 for r in rows if r["version"] == 1)
    v2n = sum(1 for r in rows if r["version"] == 2)
    print(f"wrote {args.out}: {v1n} version 1, {v2n} version 2, "
          f"{len(AXIOMS)} axiom files; {len(left_out)} version 2 left out")
    return 0


if __name__ == "__main__":
    sys.exit(main())
