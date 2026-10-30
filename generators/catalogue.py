"""
catalogue.py
============
Writes the catalogue of the cases as one HTML page, an entry per case.

    uv run generators/catalogue.py            cases/catalogue.html
    uv run generators/catalogue.py --blind    cases/catalogue-blind.html

An entry gives the two policies in plain words: each one's title, party,
action, target and constraints, then the binding the verdict is relative to
and the declarations in force with their origin.  Unless --blind is given it
also gives the lesson the case teaches, its verdict and the reason for the
verdict.  The blind page leaves those three out, so that a reader can decide
a case before reading how the suite decides it.

Everything is read from the case files, the declaration sets under
problems/background, the resources and vocab/binding.ttl.  The lesson is the
`description` of the problem in the generator that wrote the case; the verdict
and the reason are the case's own report.  Cases are grouped by the family
table of generators/lint_cases.py.  The page is generated: do not edit it.
"""

import argparse
import html
import importlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.collection import Collection
from rdflib.namespace import DCTERMS, RDFS, SKOS

from lint_cases import (BAD_WORDS, DASH, FAMILIES, FAMILY, INSTITUTION, JARGON,
                        OLD_WORDING, STALE_ROLE, TRIPLE)

ODRL = Namespace("http://www.w3.org/ns/odrl/2/")
VREP = Namespace("https://w3id.org/odrl-kb/verdict-report#")
BIND = Namespace("https://w3id.org/odrl-kb/binding#")
GN = Namespace("https://www.geonames.org/ontology#")

PROBLEM_MODULES = ["motivating", "geonames", "dpv", "dpvloc", "filetype",
                   "consent", "tom", "bcp47", "wellsorted"]

OPERATOR = {
    "eq": "is", "neq": "is not", "isA": "is a kind of",
    "isPartOf": "lies within", "hasPart": "includes as a part",
    "isAnyOf": "is at least one of", "isAllOf": "includes all of",
    "isNoneOf": "is none of",
}
CONNECTIVE = {
    "or": "At least one of these holds:",
    "xone": "Exactly one of these holds:",
    "and": "All of these hold:",
}
# What each verdict means, in the words of the page header.
MEANING = {
    "Compatible": "Whatever the vocabulary leaves open, some use meets both policies.",
    "Incompatible": "Whatever the vocabulary leaves open, no use meets both policies.",
    "Unknown": "It depends on something the vocabulary leaves open, and the reason names it.",
    "Rejected": "The policy uses an operator that does not apply to this kind of value, "
                "or a value that names no entry of the vocabulary.",
    "Accepted": "A control. The condition fits this kind of value, and the policy goes "
                "on to a verdict.",
}
VERDICT = {name: (name.lower(), text) for name, text in MEANING.items()
           if name not in ("Rejected", "Accepted")}
# How the cases are read, whatever the verdict.
READING = (
    "Every use has at least one value for each condition, for example at least one language.",
    "If each of two values lies below the other, they are the same value.",
    "For places, 'Use in France only' means the place given for the use is France itself, "
    "not a place within France.",
)


# The text rules the case files obey (lint_cases.py) hold for the lesson too,
# since the catalogue shows it; and nobody declares, adopts or withdraws as a
# party, so that framing is out as well.
PARTY = re.compile(r"\b(the|a|both|two) part(y|ies)\b|parties'|party's", re.I)
RULES = {"banned word": BAD_WORDS, "dash": DASH, "old wording": OLD_WORDING,
         "institution name": INSTITUTION, "stale role word": STALE_ROLE,
         "party wording": PARTY, "jargon": JARGON, "triple notation": TRIPLE}


def rule_failures(text: str) -> list:
    return [f"{name} {m.group(0)!r}" for name, rx in RULES.items()
            for m in [rx.search(text)] if m]


def local(x) -> str:
    return str(x).rsplit("/", 1)[-1].rsplit("#", 1)[-1]


def words(name: str) -> str:
    """A party's name as a reader writes it: german-library -> German library."""
    text = " ".join(w.capitalize() if w in ("german", "french") else w
                    for w in local(name).replace("-", " ").split())
    return text[:1].upper() + text[1:]


# --- what the catalogue reads ------------------------------------------------

def lessons() -> dict:
    """Case ID -> the problem's description, from the generators."""
    out = {}
    for m in PROBLEM_MODULES:
        for p in importlib.import_module("problem_data_" + m).PROBLEMS:
            out[p["id"]] = p.get("description", "")
    return out


def labels(resources: Path) -> dict:
    """IRI or code -> a name a reader knows, from the resources."""
    out = {}
    for f in sorted(resources.glob("*.ttl")):
        if f.name.startswith("profile-"):
            continue
        g = Graph().parse(f, format="turtle")
        for pred in (RDFS.label, SKOS.prefLabel, GN.name):
            for s, o in g.subject_objects(pred):
                out.setdefault(str(s), str(o))
                for ident in g.objects(s, DCTERMS.identifier):
                    out.setdefault(str(ident), str(o))
    return out


def declaration_sets(background: Path, vocab: Path) -> tuple:
    """Subject IRI -> title, origin, pairs, comment; and origin IRI -> label."""
    sets = {}
    for f in sorted(background.glob("*.ttl")):
        g = Graph().parse(f, format="turtle")
        for s in g.subjects(RDF.type, BIND.Declarations):
            one = lambda p: next(g.objects(s, p), None)
            sets[str(s)] = dict(
                title=str(one(DCTERMS.title) or ""),
                origin=one(BIND.origin),
                pairs=int(one(BIND.pairCount) or 0),
                comment=str(one(RDFS.comment) or ""),
                rule=str(one(DCTERMS.description) or ""),
                scope=str(one(BIND.scopeCondition) or ""),
                file=f.name)
    v = Graph().parse(vocab / "binding.ttl", format="turtle")
    origins = {str(o): (str(next(v.objects(o, RDFS.label), local(o))),
                        str(next(v.objects(o, SKOS.definition), "")))
               for o in v.subjects(RDF.type, BIND.Origin)}
    return sets, origins


def sorts(resources: Path) -> dict:
    out = {}
    for f in sorted(resources.glob("profile-*.ttl")):
        g = Graph().parse(f, format="turtle")
        for b in g.subjects(RDF.type, BIND.OperandBinding):
            out[str(b)] = (local(b), local(next(g.objects(b, BIND.sort), "")),
                           str(next(g.objects(b, RDFS.label), local(b))))
    return out


# --- a case ---------------------------------------------------------------

def value_text(g, node, names) -> str:
    """A right operand in words: a name and, where the resource has one, its label."""
    if isinstance(node, Literal):
        return f"“{node}”"
    key = str(node)
    name = names.get(key) or names.get(local(node))
    return f"{local(node)} ({name})" if name and name != local(node) else local(node)


def values_of(g, c, names) -> list:
    out = []
    for ro in g.objects(c, ODRL.rightOperand):
        if ro == RDF.nil or (ro, RDF.first, None) in g:
            out += [value_text(g, v, names) for v in Collection(g, ro)]
        else:
            out.append(value_text(g, ro, names))
    return out


def constraint(g, c, names):
    """('atom', operand, operator words, values) or (connective, [children])."""
    for conn in ("or", "xone", "and"):
        for lst in g.objects(c, ODRL[conn]):
            return conn, [constraint(g, m, names) for m in Collection(g, lst)]
    op = local(next(g.objects(c, ODRL.operator), ""))
    operand = local(next(g.objects(c, ODRL.leftOperand), ""))
    return "atom", operand, OPERATOR.get(op, op), values_of(g, c, names)


def constraint_html(item) -> str:
    if item[0] == "atom":
        _, operand, op, vals = item
        shown = ", ".join(html.escape(v) for v in vals)
        return (f"<span class=\"operand\">{html.escape(operand)}</span> "
                f"{html.escape(op)} {shown}")
    conn, children = item
    inner = "".join(f"<li>{constraint_html(c)}</li>" for c in children)
    return f"{CONNECTIVE[conn]}<ul>{inner}</ul>"


def policy(g, pol, names) -> dict:
    role = "assigner" if (pol, ODRL.assigner, None) in g else "assignee"
    party = next(g.objects(pol, ODRL[role]), None)
    rules = [r for kind in ("permission", "prohibition", "obligation")
             for r in g.objects(pol, ODRL[kind])]
    targets = sorted({t for r in rules for t in g.objects(r, ODRL.target)}, key=str)
    return dict(
        title=str(next(g.objects(pol, DCTERMS.title), "")),
        role=role, party=words(party) if party is not None else "",
        actions=sorted({local(a) for r in rules for a in g.objects(r, ODRL.action)}),
        targets=[(local(t), str(next(g.objects(t, DCTERMS.title), ""))) for t in targets],
        constraints=[constraint(g, c, names) for r in rules
                     for c in g.objects(r, ODRL.constraint)])


def case(path: Path, names, sets, origins, bindings) -> dict:
    g = Graph().parse(path, format="turtle")
    pols = sorted(g.subjects(RDF.type, ODRL.Set), key=str)
    rep = next((s for kind in (VREP.OperandVerdictReport, VREP.WellSortednessReport,
                               VREP.GroundingReport) for s in g.subjects(RDF.type, kind)), None)
    types = {local(t) for t in g.objects(rep, RDF.type)}
    if "OperandVerdictReport" in types:
        state = local(next(g.objects(rep, VREP.compatibilityState)))
        verdict = (state, VERDICT[state][0], VERDICT[state][1])
    elif "WellSortednessReport" in types:
        ok = next(g.objects(rep, VREP.wellSorted)).toPython()
        verdict = (("Accepted: the operator applies to this kind of value", "control",
                    "A control: the operator applies, and the policy goes on to a verdict.")
                   if ok else
                   ("Rejected: the operator does not apply to this kind of value", "rejected",
                    "The operator does not apply to this kind of value, so no verdict is computed."))
    else:
        verdict = ("Rejected: names no entry of the vocabulary", "rejected",
                   "A value names no entry of the part of the vocabulary used here, "
                   "so no verdict is computed.")
    binding = next(g.objects(rep, VREP.binding), None)
    declared = next(g.objects(rep, VREP.declarations), None)
    return dict(
        id=path.stem, policies=[policy(g, p, names) for p in pols],
        verdict=verdict, reason=str(next(g.objects(rep, RDFS.comment), "")),
        profile_note=str(next(g.objects(rep, VREP.profileNote), "")),
        binding=bindings.get(str(binding)), declarations=sets.get(str(declared)),
        declarations_iri=str(declared) if declared is not None else None,
        read_against=sorted(local(o).replace("-report", "") for o in g.objects(rep, VREP.readAgainst)))


# --- the page --------------------------------------------------------------

CSS = """
:root{--bg:#fff;--fg:#1c1c1e;--muted:#5c5c63;--line:#d9d9de;--card:#f7f7f9;
--compatible:#0f6b3a;--incompatible:#a3202c;--unknown:#8a5a00;--rejected:#55555c;--control:#2c5d8f}
@media (prefers-color-scheme:dark){:root{--bg:#161618;--fg:#ececf0;--muted:#a2a2ab;--line:#34343a;
--card:#1e1e22;--compatible:#52c785;--incompatible:#f08088;--unknown:#e0b24d;--rejected:#aaaab3;--control:#7fb2e6}}
*{box-sizing:border-box}
body{margin:0 auto;max-width:62rem;padding:1.5rem 1rem 4rem;background:var(--bg);color:var(--fg);
font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
h1{font-size:1.6rem;margin:.2rem 0 .4rem}h2{font-size:1.25rem;margin:2.2rem 0 .6rem;
border-bottom:1px solid var(--line);padding-bottom:.25rem}h3{font-size:1.05rem;margin:0}
h4{font-size:.8rem;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);margin:1rem 0 .25rem}
a{color:inherit}.muted{color:var(--muted)}.note{font-size:.92rem;color:var(--muted)}
nav ul{columns:2 16rem;list-style:none;padding:0;margin:.5rem 0}
article{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:.9rem 1rem;margin:.9rem 0}
article>header{display:flex;flex-wrap:wrap;gap:.5rem 1rem;align-items:baseline}
.badge{font-weight:600;font-size:.9rem}.compatible{color:var(--compatible)}
.incompatible{color:var(--incompatible)}.unknown{color:var(--unknown)}
.rejected{color:var(--rejected)}.control{color:var(--control)}
.policies{display:grid;grid-template-columns:repeat(auto-fit,minmax(18rem,1fr));gap:.8rem;margin-top:.6rem}
.policy{background:var(--bg);border:1px solid var(--line);border-radius:6px;padding:.6rem .8rem}
.policy .title{font-weight:600;margin:.1rem 0 .3rem}
dl{display:grid;grid-template-columns:7.5rem 1fr;gap:.15rem .7rem;margin:.3rem 0}
dt{color:var(--muted);font-size:.9rem}dd{margin:0}
ul{margin:.2rem 0;padding-left:1.2rem}.operand{font-family:ui-monospace,Menlo,monospace;font-size:.92em}
.ref{font-family:ui-monospace,Menlo,monospace;font-size:.75rem;color:var(--muted)}
ul.note{margin:.4rem 0;padding-left:1.2rem}
p{margin:.3rem 0}
"""


def entry(c: dict, lesson: str, blind: bool) -> str:
    out = [f'<article id="{c["id"]}">',
           f'<header><h3>{c["id"]}</h3>']
    if not blind:
        name, css, _ = c["verdict"]
        out.append(f'<span class="badge {css}">{html.escape(name)}</span>')
    out.append("</header><div class=\"policies\">")
    for k, p in enumerate(c["policies"], start=1):
        targets = "; ".join(f"{html.escape(t)}" + (f" ({html.escape(ti)})" if ti else "")
                            for t, ti in p["targets"])
        cons = "".join(f"<li>{constraint_html(x)}</li>" for x in p["constraints"])
        out.append(
            f'<section class="policy"><h4>Policy {k}</h4>'
            f'<p class="title">“{html.escape(p["title"])}”</p><dl>'
            f'<dt>Party</dt><dd>{html.escape(p["party"])} ({p["role"]})</dd>'
            f'<dt>Action</dt><dd>{html.escape(", ".join(p["actions"]))}</dd>'
            f'<dt>Target</dt><dd>{targets}</dd>'
            f'<dt>Constraint</dt><dd><ul>{cons}</ul></dd></dl></section>')
    out.append("</div><dl>")
    if c["binding"]:
        b, sort, label = c["binding"]
        # The technical name stays in the markup as a tooltip, for anyone who
        # wants to find the profile entry; the page shows the plain name.
        out.append(f'<dt>How the vocabulary is read</dt>'
                   f'<dd><span title="{html.escape(b)}">{html.escape(label)}</span></dd>')
    d = c["declarations"]
    if d is None:
        out.append("<dt>Declarations</dt><dd>none cited</dd>")
    elif d["pairs"] == 0:
        out.append('<dt>Declarations</dt><dd>No declaration. Only what the '
                   'vocabulary itself states applies.</dd>')
    else:
        label, _ = c["_origins"].get(str(d["origin"]), (local(d["origin"]), ""))
        rows = [f'{html.escape(d["title"])}: {d["pairs"]} '
                f'statement{"s" if d["pairs"] != 1 else ""}.']
        # The set's own account of itself: where it comes from, what it says,
        # and what it covers.  Not the generic definition of its origin.
        if d["rule"]:
            rows.append(f'<span class="muted">Rule: {html.escape(d["rule"])}</span>')
        rows.append(f'<span class="muted">Origin: <b>{html.escape(label)}</b>. '
                    f'{html.escape(d["comment"])}</span>')
        if d["scope"]:
            rows.append(f'<span class="muted">Scope: {html.escape(d["scope"])}</span>')
        out.append("<dt>Declarations</dt><dd>" + "<br>".join(rows) + "</dd>")
    if c["profile_note"]:
        out.append(f'<dt>Profile note</dt><dd>{html.escape(c["profile_note"])}</dd>')
    if c["read_against"]:
        links = ", ".join(f'<a href="#{r}">{r}</a>' for r in c["read_against"])
        out.append(f"<dt>Read against</dt><dd>{links}</dd>")
    out.append("</dl>")
    if not blind:
        _, _, meaning = c["verdict"]
        paras = "".join(f"<p>{html.escape(x.strip())}</p>" for x in lesson.split("\n\n") if x.strip())
        out.append(f"<h4>Lesson</h4>{paras or '<p class=\"muted\">none recorded</p>'}")
        out.append(f'<h4>Verdict</h4><p><b>{html.escape(c["verdict"][0])}</b>. '
                   f'<span class="muted">{html.escape(meaning)}</span></p>')
        out.append(f"<h4>Reason</h4><p>{html.escape(c['reason'])}</p>")
    out.append("</article>")
    return "\n".join(out)


def visible(fragment: str) -> str:
    """The text a reader sees: no style, no tags, no small-print references."""
    fragment = re.sub(r"<style>.*?</style>", " ", fragment, flags=re.S)
    fragment = re.sub(r'<small class="ref">.*?</small>', " ", fragment, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", fragment))


def page(cases: dict, lesson: dict, blind: bool) -> tuple:
    by_family = {}
    for cid in sorted(cases, key=lambda x: int(x[3:])):
        by_family.setdefault(FAMILY.get(cid, "no family"), []).append(cid)
    families = [f for f in FAMILIES if f in by_family] + \
               [f for f in by_family if f not in FAMILIES]
    title = "Case catalogue" + (" (blind)" if blind else "")
    parts = [f"<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
             f"<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
             f"<title>{title}</title><style>{CSS}</style></head><body>",
             f"<h1>{title}</h1>",
             f'<p class="note">{len(cases)} cases in {len(families)} families. Generated by '
             f'generators/catalogue.py from the case files; do not edit.'
             + (" Lessons, verdicts and reasons are left out." if blind else "") + "</p>",
             '<p class="note">A verdict is relative to how the vocabulary is read and to the '
             'declarations in force.</p>',
             "<ul class=\"note\">"
             + "".join(f"<li><b>{name}</b>: {text[:1].lower() + text[1:] if name in ('Rejected', 'Accepted') else text}</li>"
                       for name, text in MEANING.items())
             + "</ul>",
             "<ul class=\"note\">"
             + "".join(f"<li>{html.escape(text, quote=False)}</li>" for text in READING)
             + "</ul>",
             "<nav><ul>"]
    for f in families:
        parts.append(f'<li><a href="#fam-{f.replace(" ", "-")}">{html.escape(f)}</a> '
                     f'<span class="muted">({len(by_family[f])})</span></li>')
    parts.append("</ul></nav>")
    # Everything visible is held to the word list of the case files: the header
    # and the labels as much as a lesson.  A failure names the entry.
    failures = [("header", f) for f in rule_failures(visible("\n".join(parts)))]
    for f in families:
        parts.append(f'<h2 id="fam-{f.replace(" ", "-")}">{html.escape(f)}</h2>')
        for cid in by_family[f]:
            text = entry(cases[cid], lesson.get(cid, ""), blind)
            failures += [(cid, x) for x in rule_failures(visible(text))]
            parts.append(text)
    parts.append("</body></html>\n")
    return "\n".join(parts), failures


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--cases", default="cases", type=Path)
    ap.add_argument("--resources", default="problems/resources", type=Path)
    ap.add_argument("--background", default="problems/background", type=Path)
    ap.add_argument("--vocab", default="vocab", type=Path)
    ap.add_argument("--blind", action="store_true",
                    help="leave out the lesson, the verdict and the reason")
    ap.add_argument("--out", type=Path, help="default: cases/catalogue[-blind].html")
    args = ap.parse_args()

    names = labels(args.resources)
    sets, origins = declaration_sets(args.background, args.vocab)
    bindings = sorts(args.resources)
    cases = {}
    for f in sorted(args.cases.glob("KGC*.ttl")):
        c = case(f, names, sets, origins, bindings)
        c["_origins"] = origins
        cases[c["id"]] = c
    lesson = lessons()
    missing = [cid for cid in cases if not lesson.get(cid)]
    broken = [(cid, f) for cid in cases for f in rule_failures(lesson.get(cid, ""))]
    out = args.out or args.cases / ("catalogue-blind.html" if args.blind else "catalogue.html")
    text, shown = page(cases, lesson, args.blind)
    broken = sorted(set(broken) | set(shown))
    out.write_text(text, encoding="utf-8")
    print(f"{len(cases)} cases -> {out}" + (" (blind)" if args.blind else ""))
    for cid in missing:
        print(f"  no lesson recorded for {cid}", file=sys.stderr)
    for cid, f in broken:
        print(f"  {cid}: a text a reader sees breaks a rule: {f}", file=sys.stderr)
    return 1 if missing or broken else 0


if __name__ == "__main__":
    sys.exit(main())
