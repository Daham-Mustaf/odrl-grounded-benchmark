"""Lint the case files: text rules, operator wording, party words, one shape per family.

Run from the repo root:

    uv run generators/lint_cases.py [--cases cases]

The family table (FAMILIES) is also read by generators/catalogue.py, so
nothing runs on import.

Exit 1 if anything fails.  A case whose ID is in no family below fails with a
message: add the ID to FAMILIES, and give a new family its party pair and
target in PARTIES.  full-run.sh runs it; --cases points it at another
directory of case files, for example an older checkout, which it must fail.
"""
import argparse
import glob
import re
import sys
from collections import defaultdict

from rdflib import Graph, Namespace, RDF, URIRef
from rdflib.collection import Collection
from rdflib.namespace import RDFS, DCTERMS

ODRL = Namespace("http://www.w3.org/ns/odrl/2/")
VREP = Namespace("https://w3id.org/odrl-kb/verdict-report#")


def local(x):
    return re.sub(r"^.*[#/]", "", str(x))


FAMILY = {}
FAMILIES = {
    "motivating example":      [300, 301, 302],
    "file type":               [320, 321, 322, 323],
    "GeoNames spatial":        list(range(303, 307)) + [308, 309],
    "DPV purposes":            list(range(310, 320)) + list(range(393, 398)) + [399, 403, 404],
    "DPV Locations":           list(range(330, 338)) + list(range(380, 393)),
    "consent status":          list(range(340, 344)) + [348, 349],
    "technical measures":      range(360, 367),
    "language":                list(range(370, 380)) + [398],
    "well-sortedness":         [100, 101, 102, 103, 104, 105, 110, 111, 112],
}
for fam, ids in FAMILIES.items():
    for i in ids:
        FAMILY[f"KGC{i}"] = fam

# --- the rules ------------------------------------------------------------
BAD_WORDS = re.compile(r"\b(offers?|offered|requests?|requested|settles?|settled|says?|said)\b", re.I)
DASH = re.compile("[–—]")
OLD_WORDING = re.compile(r"\b(background|assertions?)\b", re.I)
INSTITUTION = re.compile(r"\b(BSB|BnF)\b|Bavarian State|Biblioth", re.I)
STALE_ROLE = re.compile(r"\b(provider|consumer|reuser)\b", re.I)
# Words of the machinery.  A reader of a case is not told what a witness, a
# refutation or a down-set is, so none of them appears in a title, a summary,
# a reason or a lesson; neither does triple notation like (purpose, isA, X).
JARGON = re.compile(
    r"\b(witness(es)?|refut\w*|certificat\w*|quer(y|ies)|models?|premises?|"
    r"antisymmetr\w*|down-?sets?|up-?sets?|nominal sort|satisfiab\w*|singletons?|"
    r"withdrawable|order axioms?|polarity|provenance|converse edge|disjuncts?|"
    r"negated|epistemic)\b", re.I)
TRIPLE = re.compile(r"\(\s*[A-Za-z]+,\s*(?:eq|neq|isA|isPartOf|hasPart|isAnyOf|isAllOf|isNoneOf)\b")
NEED = {  # operator -> substrings, any one suffices
    "eq": ["only"], "isA": ["only"], "isPartOf": ["within"],
    "hasPart": ["includes", "covers"],
    "neq": ["except"], "isNoneOf": ["except"],
    "isAnyOf": ["at least one of"], "isAllOf": ["both", "all of"],
}
ROLE_WORDS = {"german-library": "german library", "french-library": "french library", "library": "library",
              "researcher": "researcher", "controller": "controller", "processor": "processor",
              "publisher": "publisher", "licensee": "licensee",
              "data-platform": "data platform", "data-user": "data user"}

fails = []
shape = defaultdict(set)


def fail(cid, msg):
    fails.append(f"{cid}: {msg}")


def leaf_constraints(g, c):
    """The atomic constraints under c, through any connective."""
    for conn in ("or", "xone", "and"):
        for lst in g.objects(c, ODRL[conn]):
            return [x for m in Collection(g, lst) for x in leaf_constraints(g, m)]
    return [c]


def constraint_ops(g, c):
    """(connective or None, [operators of the leaves])"""
    for conn in ("or", "xone", "and"):
        for lst in g.objects(c, ODRL[conn]):
            return conn, [local(next(g.objects(m, ODRL.operator))) for m in Collection(g, lst)]
    return None, [local(next(g.objects(c, ODRL.operator)))]


DRK = "https://w3id.org/odrl-kb/drk/"
TARGET_EXPECT = {
    "manuscripts": ("http://www.w3.org/ns/dcat#Dataset", "Digitised manuscripts of a library"),
    "dataset":     ("http://www.w3.org/ns/dcat#Dataset", "Personal data held by a controller"),
    "traffic-data": ("http://www.w3.org/ns/dcat#Dataset", "Traffic sensor data of a city"),
    "work":        ("http://purl.org/dc/terms/BibliographicResource", "A work distributed by a publisher"),
}
LIB = (("library",), ("researcher",), ("manuscripts",))
DE_FR = (("german-library",), ("french-library",), ("manuscripts",))
CTRL = (("controller",), ("processor",), ("dataset",))
PARTIES = {
    "motivating example": DE_FR, "file type": DE_FR,
    "well-sortedness":    (("german-library",), (), ("manuscripts",)),
    "GeoNames spatial": LIB, "DPV Locations": LIB,
    "DPV purposes":       (("data-platform",), ("data-user",), ("traffic-data",)),
    "consent status": CTRL, "technical measures": CTRL,
    "language":           (("publisher",), ("licensee",), ("work",)),
}
if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cases", default="cases", help="directory of case files")
    ARGS = ap.parse_args()
    target_seen = defaultdict(set); by_iri = defaultdict(set); by_prefix = defaultdict(set)
    n_titles = 0
    for f in sorted(glob.glob(f"{ARGS.cases}/KGC*.ttl")):
        cid = f.split("/")[-1][:-4]
        raw = open(f, encoding="utf-8").read()
        g = Graph().parse(f, format="turtle")
        # --- text rules over everything a reader sees: literals and # comments ---
        texts = [str(o) for p in (DCTERMS.title, DCTERMS.description, RDFS.comment) for o in g.objects(None, p)]
        texts += [l for l in raw.split("\n") if l.lstrip().startswith("#")]
        for t in texts:
            if DASH.search(t): fail(cid, f"dash in {t[:70]!r}")
            if BAD_WORDS.search(t): fail(cid, f"banned word {BAD_WORDS.search(t).group(0)!r} in {t[:70]!r}")
            if INSTITUTION.search(t): fail(cid, f"institution name in {t[:70]!r}")
            if OLD_WORDING.search(t): fail(cid, f"old wording {OLD_WORDING.search(t).group(0)!r} in {t[:70]!r}")
            if STALE_ROLE.search(t): fail(cid, f"stale role word {STALE_ROLE.search(t).group(0)!r} in {t[:70]!r}")
            if JARGON.search(t): fail(cid, f"jargon {JARGON.search(t).group(0)!r} in {t[:70]!r}")
            if TRIPLE.search(t): fail(cid, f"triple notation in {t[:70]!r}")
        # --- every target is typed and titled, once, the same way in every case ---
        for iri, (kind, ttl_title) in TARGET_EXPECT.items():
            node = URIRef(DRK + iri)
            used = (None, ODRL.target, node) in g
            if not used:
                if (node, None, None) in g: fail(cid, f"{iri} described but not the target of any rule")
                continue
            types = set(g.objects(node, RDF.type)); titles = {str(t) for t in g.objects(node, DCTERMS.title)}
            if types != {URIRef(kind)}: fail(cid, f"target {iri} has types {sorted(map(str, types))}, expected {kind}")
            if titles != {ttl_title}: fail(cid, f"target {iri} has titles {sorted(titles)}, expected {ttl_title!r}")
            target_seen[iri].add(cid)
        for line in raw.split("\n"):
            m = re.match(r"@prefix\s+([\w-]*):\s*<([^>]*)>", line)
            if m:
                by_iri[m.group(2)].add(m.group(1)); by_prefix[m.group(1)].add(m.group(2))
        # --- the policies ---
        pols = sorted((s for s in g.subjects(RDF.type, ODRL.Set)), key=str)
        for pol in pols:
            if cid not in FAMILY:
                fail(cid, "is in no family: add it to FAMILIES in generators/lint_cases.py"); break
            k = 1 if str(pol).endswith("-1") else 2
            title = str(next(g.objects(pol, DCTERMS.title)))
            n_titles += 1
            rules = [r for pr in (ODRL.permission,) for r in g.objects(pol, pr)]
            action = local(next(g.objects(rules[0], ODRL.action)))
            if not title.lower().startswith(action):
                fail(cid, f"title {title!r} does not start with action {action!r}")
            cons = [c for r in rules for c in g.objects(r, ODRL.constraint)]
            conn, ops = constraint_ops(g, cons[0])
            tl = title.lower()
            if conn == "xone":
                if "exactly one" not in tl and not (" either " in f" {tl}" and " or " in tl):
                    fail(cid, f"xone title lacks 'exactly one' or 'either ... or': {title!r}")
                need = [o for o in ops if o in ("isPartOf", "isAllOf", "isAnyOf", "hasPart")]
            elif conn == "or":
                if " or " not in tl: fail(cid, f"or title lacks ' or ': {title!r}")
                need = ops
            else:
                need = ops
            roots = {local(r) for c in cons for r in g.objects(c, ODRL.rightOperand)} if ops == ["isA"] else set()
            if roots & {"Purpose"}:
                if "only" in tl.split() or "any" not in tl.split():
                    fail(cid, f"isA on a root concept must say 'any' and not 'only': {title!r}")
                need = []
            else:
                need = need
                # isA on a purpose reads the order, so the title says so: "X or
                # any narrower purpose", never "X only", which is what eq says.
                isa_purpose = [x for x in leaf_constraints(g, cons[0])
                               if local(next(g.objects(x, ODRL.operator), "")) == "isA"
                               and local(next(g.objects(x, ODRL.leftOperand), "")).lower() == "purpose"]
                if isa_purpose and conn in (None, "or"):
                    if "narrower" not in tl or "only" in tl.split():
                        fail(cid, f"isA on a purpose must read 'X or any narrower purpose': {title!r}")
                    need = [o for o in need if o != "isA"]
            for o in set(need):
                if not any(s in tl for s in NEED[o]):
                    fail(cid, f"{o} title {title!r} lacks one of {NEED[o]}")
            # party presence: policy 1 has an assigner only, policy 2 an assignee only
            has_er = (pol, ODRL.assigner, None) in g; has_ee = (pol, ODRL.assignee, None) in g
            if k == 1 and not (has_er and not has_ee): fail(cid, "policy 1 must have an assigner and no assignee")
            if k == 2 and not (has_ee and not has_er): fail(cid, "policy 2 must have an assignee and no assigner")
            who = local(next(g.objects(pol, ODRL.assigner if k == 1 else ODRL.assignee), ""))
            tg = {local(t) for r in rules for t in g.objects(r, ODRL.target)}
            shape[cid].add((k, who, tuple(sorted(tg))))
        # --- the report's text names the parties the IRIs name ---
        summ = next(g.objects(None, DCTERMS.description), None)
        if summ is not None:
            s = str(summ).lower()
            parties = {ROLE_WORDS.get(w, w) for (_, w, _) in shape[cid] if w}
            named = {w for w in ROLE_WORDS.values() if re.search(rf"\b{w}\b", s)}
            # "library" inside "german library" is the same party
            named -= {"library"} if re.search(r"\b(german|french) library\b", s) else set()
            if named - parties:
                fail(cid, f"summary names {sorted(named - parties)} but the parties are {sorted(parties)}")

    # --- one party pair and one target per family -----------------------------
    fam_choice = defaultdict(set)
    for cid, rows in shape.items():
        if cid not in FAMILY: continue
        er = {w for k, w, _ in rows if k == 1}; ee = {w for k, w, _ in rows if k == 2}
        tg = {t for _, _, ts in rows for t in ts}
        fam_choice[FAMILY[cid]].add((tuple(sorted(er)), tuple(sorted(ee)), tuple(sorted(tg))))
    for fam, ch in sorted(fam_choice.items()):
        if len(ch) != 1:
            fail(fam, f"more than one party pair or target: {sorted(ch)}")

    for fam, want in PARTIES.items():
        if fam_choice[fam] != {want}: fail(fam, f"expected {want}, found {sorted(fam_choice[fam])}")
    for iri, ps in by_iri.items():
        if len(ps) > 1: fail("prefixes", f"{iri} has more than one prefix: {sorted(ps)}")
    for p, iris in by_prefix.items():
        if len(iris) > 1: fail("prefixes", f"prefix {p}: names more than one IRI: {sorted(iris)}")
    for iri in TARGET_EXPECT:
        print(f"target drk:{iri}: described in {len(target_seen[iri])} cases")
    print(f"namespaces: {len(by_iri)}, prefixes: {len(by_prefix)}, any namespace with two prefixes: {[i for i, ps in by_iri.items() if len(ps) > 1] or 'none'}")
    print(f"policies linted: {n_titles}   case files: {len(shape)}")
    print("per-family choice (assigner / assignee / target):")
    for fam, ch in sorted(fam_choice.items()):
        for er, ee, tg in sorted(ch):
            print(f"   {fam:20} {','.join(er)} / {','.join(ee) or '-'} / {','.join(tg)}")
    print("FAILURES:" if fails else "lint clean")
    for x in fails: print("  ", x)
    sys.exit(1 if fails else 0)
