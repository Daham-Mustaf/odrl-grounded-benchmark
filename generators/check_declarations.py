"""
check_declarations.py
=====================

A set of declarations is RDF, and everything else follows from it.  This
checks that it does.

For every file in problems/background that states something:

  1. count      bind:pairCount is the number of pairs the RDF states.
  2. resource   every member is a concept of the resource the set applies to;
                a set that ranges over the whole resource lists all of it.
  3. axioms     the .ax file says what the RDF says: the same pairs, with
                the labels the encodings use; or, where the file states the
                rule and leaves the instances to the problems, the same
                members and the same counts.
  4. queries    every bg_ statement in every query is a pair of the set its
                case cites, in the right kind, with the right label, and in
                the one form the writer produces.  Pairs match unordered; a
                label keeps the order the problem wrote, because certificates
                cite it.
  5. areas      every area that ISO codes twice sits in one identity class
                of DPV Locations or is named as left out in dpvloc-iso.

Exit 1 on any failure.

    uv run generators/check_declarations.py
"""

import json
import re
import sys
import unicodedata
from pathlib import Path

from rdflib import Graph, RDF, RDFS, URIRef
from rdflib.namespace import DCTERMS, OWL

sys.path.insert(0, str(Path(__file__).parent))
import declarations as D

BG, AX, VERDICT = Path("problems/background"), Path("problems/axioms"), Path("problems/verdict")

# One row per set that states something.  form: expanded (one formula per pair
# in the .ax), rule (the .ax lists the members and leaves the pairs to the
# problems), inline (no .ax; the problems carry the statements).  label: how
# the encodings spell the name of a distinctness.
SETS = {
    "bcp47-distinct":           dict(ax="BCP47001-0.ax", form="rule", noun="Languages",
                                     token="constant", label="bcp47"),
    "consent-declared":         dict(ax="DPV-consent-declared.ax", form="rule",
                                     noun="States", token="local"),
    "consent-definitional":     dict(ax="DPV-consent-definitional.ax", form="rule"),
    "dpv-purposes-declared":    dict(ax="DPV-dpv-purposes-declared.ax", form="rule",
                                     noun="Purposes", token="local"),
    "dpvloc-iso":               dict(ax="LOC-dpvloc-iso.ax", form="rule",
                                     noun="Areas", token="local"),
    "filetype-declared":        dict(ax="EUFT-filetype-declared.ax", form="rule",
                                     noun="Formats", token="constant",
                                     label="const-distinct"),
    "geonames-europe-declared": dict(ax=None, form="inline"),
    "geonames-europe-siblings": dict(ax=None, form="inline"),
    "tom-declared":             dict(ax="DPV-tom-declared.ax", form="rule",
                                     noun="Measures", token="constant"),
}
# Sets whose members are the whole resource, less what the set names as left out.
WHOLE = {"consent-declared", "dpv-purposes-declared", "tom-declared",
         "geonames-europe-declared", "filetype-declared"}
RULES = {"PairwiseDistinctness", "PairwiseDisjointness", "PublishedDefinition"}

fails = []


def fail(where, msg):
    fails.append(f"{where}: {msg}")


def label_of(style, kind, a, b):
    if kind == "disjoint":
        return D.disj_label(a, b)
    if style == "bcp47":
        return f"bg_dist_bcp47_{a[4:]}_{b[4:]}"
    return D.dist_label(a, b, "distinct" if style == "const-distinct" else "")


# --- the statements in a file ------------------------------------------------

FOF_DIST = re.compile(r"fof\((bg_dist_[^,\s]+),\s*axiom,\s*(\w+) != (\w+)\)\.")
FOF_DISJ = re.compile(r"fof\((bg_disj_[^,\s]+),\s*axiom,\s*! \[X\] : ~ \( kge_leq\(X, (\w+)\) "
                      r"& kge_leq\(X, (\w+)\) \)\)\.")
SMT_DIST = re.compile(r"\(assert \(! \(not \(= (\w+) (\w+)\)\) :named (bg_dist_\w+)\)\)")
SMT_DISJ = re.compile(r"\(assert \(! \(forall \(\(x Concept\)\)\n    \(not \(and \(kge_leq x (\w+)\) "
                      r"\(kge_leq x (\w+)\)\)\)\)\n  :named (bg_disj_\w+)\)\)")


def statements(text, smt):
    """(kind, label, a, b) for every recognised bg_ statement, and the count of
    bg_ names the recognisers did not account for."""
    found = []
    if smt:
        found += [("distinct", m[3], m[1], m[2]) for m in SMT_DIST.finditer(text)]
        found += [("disjoint", m[3], m[1], m[2]) for m in SMT_DISJ.finditer(text)]
        names = len(re.findall(r":named bg_", text))
    else:
        found += [("distinct", m[1], m[2], m[3]) for m in FOF_DIST.finditer(text)]
        found += [("disjoint", m[1], m[2], m[3]) for m in FOF_DISJ.finditer(text)]
        names = len(re.findall(r"fof\(bg_", text))
    return found, names - len(found)


# --- the resource ------------------------------------------------------------

_resources = {}


# The GeoNames slice does not describe itself under the IRI its bindings use.
FILE_OF = {"https://w3id.org/odrl-kb/geonames-europe": "geonames.ttl"}


def resource(iri):
    if iri not in _resources:
        for p in sorted(Path("problems/resources").glob("*.ttl")):
            if p.name.startswith("profile-"):
                continue
            g = Graph().parse(p)
            if (URIRef(iri), None, None) in g or FILE_OF.get(iri) == p.name:
                ids = {str(o) for o in g.objects(None, DCTERMS.identifier)}
                ids |= {str(s) for s in g.subjects(RDF.type, None) if str(s) != iri}
                _resources[iri] = (ids, g)
                break
        else:
            raise SystemExit(f"no resource file declares {iri}")
    return _resources[iri]


def loc_classes():
    """DPV Locations: code -> class key, kind of each code, the identity classes."""
    ids, g = resource("https://w3id.org/odrl-kb/dpv-loc-geo")
    code, kind, label = {}, {}, {}
    for s in g.subjects(RDF.type, None):
        k = [str(t).rsplit("#", 1)[-1] for t in g.objects(s, RDF.type)]
        if "Country" in k or "Region" in k:
            ident = next(g.objects(s, DCTERMS.identifier), None)
            code[s] = str(ident).rsplit("#", 1)[-1]
            kind[code[s]] = "Country" if "Country" in k else "Region"
            label[code[s]] = str(next(g.objects(s, RDFS.label), ""))
    parent = {c: c for c in code.values()}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for s, o in ((s, o) for s, p, o in g if str(p).endswith("sameAs")):
        if s in code and o in code:
            ra, rb = find(code[s]), find(code[o])
            if ra != rb:
                parent[max(ra, rb)] = min(ra, rb)
    groups = {}
    for c in parent:
        groups.setdefault(find(c), []).append(c)
    key = {}
    for members in groups.values():
        countries = [m for m in members if kind[m] == "Country"]
        k = min(countries) if countries else min(members)
        for m in members:
            key[m] = k
    return key, kind, label


# --- the checks --------------------------------------------------------------

def main() -> int:
    decls = {p.stem: D.load(p) for p in sorted(BG.glob("*.ttl"))}
    stating = {n: d for n, d in decls.items() if d.pair_count}
    for n in sorted(set(stating) - set(SETS)):
        fail(n, "states something and is not in SETS: say how its axioms and queries are checked")
    for n in sorted(set(SETS) - set(stating)):
        fail(n, "is in SETS and states nothing or is missing")

    cases_set = {}
    for f in sorted(Path("cases").glob("KGC*.ttl")):
        m = re.search(r"vrep:declarations <([^>]+)>", f.read_text(encoding="utf-8"))
        if m:
            cases_set[f.stem] = m.group(1)
    by_iri = {d.iri: n for n, d in stating.items()}

    rows = []
    for n, spec in SETS.items():
        d = stating.get(n)
        if d is None:
            continue
        const = D.constant_for(d.applies_to[0])
        consts = [const(m) for m in d.members]
        dpairs = [(const(a), const(b)) for a, b in d.distinct_pairs()]
        jpairs = [(const(a), const(b)) for a, b in d.disjoint]
        want = {frozenset(p) for p in dpairs} | {frozenset(p) for p in jpairs}

        # 1. count and vocabulary
        if d.pair_count != d.n_pairs():
            fail(n, f"bind:pairCount {d.pair_count} but the RDF states {d.n_pairs()}")
        if d.members and len(d.members) < 2:
            fail(n, "an owl:AllDifferent needs two members")
        if d.rule not in RULES:
            fail(n, f"bind:generatedBy {d.rule!r} is not one of {sorted(RULES)}")
        if d.members and d.rule == "PairwiseDisjointness":
            fail(n, "states distinctness and names a disjointness rule")
        if d.disjoint and d.rule == "PairwiseDistinctness":
            fail(n, "states disjointness and names a distinctness rule")

        # 2. the resource
        ids, rg = resource(d.applies_to[0])
        for m in d.members + [x for p in d.disjoint for x in p]:
            if m not in ids:
                fail(n, f"{m} is not a concept of {d.applies_to[0]}")
        if n in WHOLE:
            # What the resource marks as deprecated is left out, and the scope
            # condition has to say so.
            left_out = {str(i) for s in rg.subjects(OWL.deprecated, None)
                        if str(next(rg.objects(s, OWL.deprecated))).lower() == "true"
                        for i in rg.objects(s, DCTERMS.identifier)}
            missing = sorted(i for i in ids if i.startswith("http") and i not in set(d.members)
                             and i not in left_out
                             and any(i.startswith(s) for s in ("https://w3id.org/dpv",
                                                               "https://sws.geonames.org/",
                                                               "http://publications.europa.eu/resource/authority/file-type/")))
            if missing:
                fail(n, f"the set ranges over the whole resource and omits {len(missing)} concepts, e.g. {missing[:2]}")
            if n == "filetype-declared":
                for i in sorted(left_out & set(d.members)):
                    fail(n, f"{i} is deprecated in the resource and is a member")
                for i in sorted(left_out):
                    if D._local(i) in {D._local(x) for x in ids} and D._local(i) not in d.scope:
                        fail(n, f"the scope condition does not name {D._local(i)}, which is left out")

        # 2b. GeoNames: the siblings are every pair with the same parent
        if n == "geonames-europe-siblings":
            _, gg = resource(d.applies_to[0])
            parent_of = {str(f): str(p) for f, p in
                         gg.subject_objects(URIRef("https://www.geonames.org/ontology#parentFeature"))}
            kin = {}
            for f, p in parent_of.items():
                kin.setdefault(p, []).append(f)
            sib = {frozenset((a, b)) for fs in kin.values() for i, a in enumerate(fs) for b in fs[i + 1:]}
            got = {frozenset(p) for p in d.disjoint}
            if got != sib:
                fail(n, f"states {len(got)} pairs and the slice has {len(sib)} pairs of features "
                        f"with the same parent; {len(got - sib)} only in the RDF, {len(sib - got)} only in the slice")

        # 3. the axioms
        axstate = "-"
        if spec["form"] == "expanded":
            text = (AX / spec["ax"]).read_text(encoding="utf-8")
            found, odd = statements(text, smt=False)
            if odd:
                fail(n, f"{spec['ax']} has {odd} bg_ names the recognisers do not account for")
            got = {frozenset((a, b)) for _, _, a, b in found}
            if got != want or len(found) != len(want):
                fail(n, f"{spec['ax']} states {len(found)} pairs and the RDF {len(want)}; "
                        f"{len(got - want)} only in the axioms, {len(want - got)} only in the RDF")
            for kind, lab, a, b in found:
                if lab != label_of(spec.get("label"), kind, a, b):
                    fail(n, f"{spec['ax']}: label {lab} for {a} and {b}")
            axstate = f"{len(found)} formulas"
        elif spec["form"] == "rule" and not d.members:
            # a rule of disjointness: the pairs, one per line, "a disjoint b"
            text = (AX / spec["ax"]).read_text(encoding="utf-8")
            pm = re.search(r"^% Pairs\s*: (\d+)$", text, re.M)
            if not pm or int(pm[1]) != d.n_pairs():
                fail(n, f"{spec['ax']} says {pm and pm[1]} pairs, the RDF states {d.n_pairs()}")
            listed = {frozenset(m) for m in re.findall(r"^% (\w+) disjoint (\w+)$", text, re.M)}
            if listed != {frozenset(p) for p in jpairs}:
                fail(n, f"{spec['ax']} lists {len(listed)} disjoint pairs and they are not the RDF's {len(jpairs)}")
            if re.search(r"^fof\(", text, re.M):
                fail(n, f"{spec['ax']} states the rule and carries formulas")
            axstate = f"rule, {len(listed)} pairs"
        elif spec["form"] == "rule":
            text = (AX / spec["ax"]).read_text(encoding="utf-8")
            nm = re.search(rf"^% {spec['noun']}\s*: (\d+)$", text, re.M)
            pm = re.search(r"^% Pairs\s*: (\d+)$", text, re.M)
            if not nm or int(nm[1]) != len(d.members):
                fail(n, f"{spec['ax']} says {nm and nm[1]} {spec['noun'].lower()}, the RDF lists {len(d.members)}")
            if not pm or int(pm[1]) != d.n_pairs():
                fail(n, f"{spec['ax']} says {pm and pm[1]} pairs, the RDF states {d.n_pairs()}")
            tokens = [t.strip() for line in text[(pm.end() if pm else 0):].splitlines()
                      if line.startswith("% ") for t in line[2:].split(",") if t.strip()]
            expect = ([D._local(m) for m in d.members] if spec["token"] == "local" else consts)
            if sorted(tokens) != sorted(expect):
                fail(n, f"{spec['ax']} lists {len(tokens)} names and they are not the RDF's {len(expect)} members")
            if re.search(r"^fof\(", text, re.M):
                fail(n, f"{spec['ax']} states the rule and carries formulas")
            axstate = f"rule, {len(tokens)} names"
        else:
            axstate = "inline"

        # 4. the queries
        users = sorted(c for c, s in cases_set.items() if s == d.iri)
        used = set()
        for c in users:
            for q in sorted(VERDICT.glob(f"{c}-*.p")) + sorted(VERDICT.glob(f"{c}-*.smt2")):
                found, odd = statements(q.read_text(encoding="utf-8"), smt=q.suffix == ".smt2")
                if odd:
                    fail(q.name, f"{odd} bg_ statements in a form the writer does not produce")
                for kind, lab, a, b in found:
                    want = label_of(spec.get("label"), kind, a, b)
                    if d.has(a, b, const) != kind:
                        fail(q.name, f"{lab}: the set does not state {kind} for {a} and {b}")
                    elif lab != want:
                        fail(q.name, f"label {lab} for {a} and {b}")
                    used.add(frozenset((a, b)))
        for c, s in cases_set.items():
            if s not in by_iri:
                for q in list(VERDICT.glob(f"{c}-*.p")) + list(VERDICT.glob(f"{c}-*.smt2")):
                    found, odd = statements(q.read_text(encoding="utf-8"), q.suffix == ".smt2")
                    if found or odd:
                        fail(q.name, f"carries bg_ statements and cites {s}, which states nothing")
        rows.append((n, len(d.members), d.n_pairs(), axstate, len(users), len(used), d.rule))

    # 5. the areas ISO codes twice
    d = stating["dpvloc-iso"]
    key, kind, label = loc_classes()
    data = json.loads((BG / "dpvloc-double-coded.json").read_text(encoding="utf-8"))
    members = {D._local(m) for m in d.members}
    left_out = {c for cs in data["excluded"].values() for c in cs}
    want_members = {k for k in set(key.values()) if k not in left_out}
    if members != want_members:
        fail("dpvloc-iso", f"lists {len(members)} areas; the identity classes of the resource "
                           f"less the {len(left_out)} left out are {len(want_members)}")
    for cc, subs in data["same_area"].items():
        for s in subs:
            if cc not in key or s not in key:
                fail("dpvloc-double-coded", f"{cc} or {s} is not a code of DPV Locations")
            elif key[cc] != key[s]:
                fail("dpvloc-double-coded", f"{cc} and {s} name one area and are not in one identity class")
    for cc, subs in data["excluded"].items():
        for s in subs:
            if key.get(cc) == key.get(s):
                fail("dpvloc-double-coded", f"{s} is listed as left out and is in the class of {cc}")
            if s in members:
                fail("dpvloc-iso", f"{s} is listed as left out and is a member")
            if s not in d.scope:
                fail("dpvloc-iso", f"the scope condition does not name {s}, which is left out")
            if cc not in members:
                fail("dpvloc-iso", f"{cc} is not a member, and only the second code {s} should be left out")
    norm = lambda s: re.sub(r"[^a-z]", "", unicodedata.normalize("NFKD", re.sub(r"\s*\(.*?\)", "", s).lower())
                            .encode("ascii", "ignore").decode())
    classified = ({(cc, s) for cc, subs in data["same_area"].items() for s in subs}
                  | {(cc, s) for cc, subs in data["excluded"].items() for s in subs}
                  | {tuple(p) for p in data["different_areas"]})
    candidates = set()
    for c, k in kind.items():
        if k != "Region":
            continue
        for cc, k2 in kind.items():
            if k2 == "Country" and cc != c.split("-")[0] and norm(label[c]) and norm(label[c]) == norm(label[cc]):
                candidates.add((cc, c))
    for pair in sorted(candidates - classified):
        fail("dpvloc-double-coded", f"{pair[0]} and {pair[1]} share a name and are in none of "
                                    f"same_area, excluded and different_areas")

    print(f"{'set':26} {'members':>8} {'pairs':>12}  {'axioms':18} {'cases':>5} {'pairs used':>10}  rule")
    for n, mem, pairs, ax, users, used, rule in rows:
        print(f"{n:26} {mem:>8} {pairs:>12,}  {ax:18} {users:>5} {used:>10}  {rule}")
    print(f"\nareas ISO codes twice: {sum(len(v) for v in data['same_area'].values())} subdivision "
          f"codes in one identity class with their country code, "
          f"{sum(len(v) for v in data['excluded'].values())} left out of dpvloc-iso, "
          f"{len(data['different_areas'])} name coincidences")
    print(f"name candidates found in the resource: {len(candidates)}, all classified"
          if not (candidates - classified) else "")
    print("FAILURES:" if fails else "declarations agree with their axioms and queries")
    for f in fails:
        print("  ", f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
