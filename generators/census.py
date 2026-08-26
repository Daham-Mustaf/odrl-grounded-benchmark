"""
census.py
=========
Surveys what a published vocabulary asserts, and which of it the fragment
reads.

    uv run generators/census.py vocabularies/dpv-2.3/modules/purposes.ttl
    uv run generators/census.py --all vocabularies/**/*.ttl

Why this exists
---------------
Every resource in the suite was built by deciding which of a file's
predicates carry the order, which carry something else, and which are
ignored.  Those decisions were made one file at a time and recorded in each
builder's docstring, where they are easy to state and hard to check.  This
runs the same partition over any file and prints it, so a claim about what
a vocabulary publishes is measured on the spot.

It answers two kinds of question for each file.

First, the partition: what is asserted between concepts of the vocabulary
itself (the candidates for the order), what is asserted between a concept
and something outside the vocabulary (typing, alignment, membership; not
an order over these concepts, and reading one as though it were is the
error the sorts exist to prevent), what is asserted to an own-namespace
node the file never declares a concept (usually a builder bug: the
undeclared union subjects in the Locations file were exactly this), and
what is asserted about a concept rather than between concepts (labels,
dates, deprecation; the fragment reads none of it).

Second, the structure, computed separately for every order-candidate
relation the file publishes:

  - edges are oriented child to parent regardless of which direction the
    file writes; narrower and hasPart families are inverted, so levels
    mean the same thing across files
  - cycles, as strongly connected components; a cycle is an antisymmetry
    collapse waiting for a distinctness declaration, so it is reported
    with a witness, and cyclic nodes are excluded from level computation
  - roots, compared against declared top concepts where the relation is
    skos:broader; leaves; concepts the relation never touches
  - levels as longest path from a root (what publishers mean when they
    claim "5 levels"), printed as a histogram, with the longest chain and
    one witness
  - multi-parent nodes (polyhierarchy), branching, weakly connected
    components
  - the size of the reflexive transitive closure, which is the number of
    comparable pairs a resource built from this relation can be asked
    about, i.e. the premise budget
  - interaction with deprecation: edges whose endpoints are retired, in
    particular live children of retired parents, which is the reading
    decision retirement forces on a profile
  - redundancy with the inverse relation when the file publishes both

What it does not do
-------------------
It does not decide which predicate is the order.  That is the profile's
job, and two profiles over one file may differ: the DPV Locations resource
is built twice from one file, once reading union membership as containment
and once not.  This prints every candidate's structure and leaves the
choice where it belongs.

It counts triples, not meanings.  A predicate used for five different
relations, as skos:broader is in DPV Locations, is one structure block
here; separating those needs the object's type, which the resource builder
does and this does not.

Deprecation is detected from a known predicate list, not discovered.  When
a file encodes retirement some other way, find the predicate first (the
probe diff in verify_medtop.py does that) and add it to DEPRECATION.
"""
import argparse
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path

try:
    from rdflib import Graph, URIRef, BNode, Literal
    from rdflib.namespace import SKOS, RDF, RDFS, OWL, DCTERMS
except ImportError:
    print("needs rdflib: uv add rdflib", file=sys.stderr)
    raise

XKOS = "http://rdf-vocabulary.ddialliance.org/xkos#"

# Order candidates, with the orientation that makes the edge read child to
# parent.  "up" edges are stored as written, "down" edges are inverted.
ORIENT = {
    str(SKOS.broader): "up",
    str(SKOS.broaderTransitive): "up",
    str(RDFS.subClassOf): "up",
    str(DCTERMS.isPartOf): "up",
    XKOS + "isPartOf": "up",
    XKOS + "specializes": "up",
    str(SKOS.narrower): "down",
    str(SKOS.narrowerTransitive): "down",
    str(DCTERMS.hasPart): "down",
    XKOS + "hasPart": "down",
    XKOS + "generalizes": "down",
}
INVERSE = {
    str(SKOS.broader): str(SKOS.narrower),
    str(SKOS.narrower): str(SKOS.broader),
    str(SKOS.broaderTransitive): str(SKOS.narrowerTransitive),
    str(SKOS.narrowerTransitive): str(SKOS.broaderTransitive),
    str(DCTERMS.isPartOf): str(DCTERMS.hasPart),
    str(DCTERMS.hasPart): str(DCTERMS.isPartOf),
    XKOS + "isPartOf": XKOS + "hasPart",
    XKOS + "hasPart": XKOS + "isPartOf",
    XKOS + "specializes": XKOS + "generalizes",
    XKOS + "generalizes": XKOS + "specializes",
}

# Identity between concepts.  The background theory reads these; the
# resource does not.
IDENTITY = {
    str(OWL.sameAs), str(SKOS.exactMatch),
    "http://www.w3.org/2004/02/skos/core#sameAs",  # not a SKOS term; DPV uses it
}
# Assertions that two concepts are apart.  No resource in the suite has
# ever had one; the count is printed because its absence is a finding.
SEPARATION = {
    str(OWL.disjointWith), str(OWL.differentFrom),
}
# Mapping predicates: cross-vocabulary alignment, never the order.
MAPPING = {
    str(SKOS.exactMatch), str(SKOS.closeMatch), str(SKOS.broadMatch),
    str(SKOS.narrowMatch), str(SKOS.relatedMatch),
}
ANNOTATION = {
    str(SKOS.prefLabel), str(SKOS.altLabel), str(SKOS.hiddenLabel),
    str(SKOS.definition), str(SKOS.scopeNote), str(SKOS.note),
    str(SKOS.editorialNote), str(SKOS.changeNote), str(SKOS.historyNote),
    str(SKOS.example), str(RDFS.label), str(RDFS.comment),
    str(DCTERMS.created), str(DCTERMS.modified), str(DCTERMS.issued),
    str(DCTERMS.creator), str(DCTERMS.contributor), str(DCTERMS.source),
    str(DCTERMS.title), str(DCTERMS.description), str(DCTERMS.identifier),
    str(DCTERMS.license), str(DCTERMS.rightsHolder),
}
DEPRECATION = {
    str(OWL.deprecated),
    "http://cv.iptc.org/newscodes/ikos/retired",
    "http://www.w3.org/2003/06/sw-vocab-status/ns#term_status",
    str(DCTERMS.isReplacedBy), str(DCTERMS.replaces),
}


def short(u, g) -> str:
    try:
        return g.namespace_manager.normalizeUri(URIRef(u))
    except Exception:
        return str(u)


def loc(u) -> str:
    s = str(u)
    return s.rsplit("#", 1)[-1] if "#" in s else s.rstrip("/").rsplit("/", 1)[-1]


def namespaces_of(nodes):
    out = Counter()
    for c in nodes:
        s = str(c)
        out[s.rsplit("#", 1)[0] + "#" if "#" in s else
            s.rsplit("/", 1)[0] + "/"] += 1
    return out


# ---------------------------------------------------------------------
# graph algorithms, all iterative
# ---------------------------------------------------------------------

def tarjan_sccs(nodes, adj):
    """Strongly connected components; nontrivial ones are cycles."""
    index, low, on, stack, out = {}, {}, set(), [], []
    counter = [0]
    for root in nodes:
        if root in index:
            continue
        work = [(root, iter(adj.get(root, ())))]
        index[root] = low[root] = counter[0]
        counter[0] += 1
        stack.append(root)
        on.add(root)
        while work:
            node, it = work[-1]
            advanced = False
            for nxt in it:
                if nxt not in index:
                    index[nxt] = low[nxt] = counter[0]
                    counter[0] += 1
                    stack.append(nxt)
                    on.add(nxt)
                    work.append((nxt, iter(adj.get(nxt, ()))))
                    advanced = True
                    break
                if nxt in on:
                    low[node] = min(low[node], index[nxt])
            if advanced:
                continue
            work.pop()
            if work:
                low[work[-1][0]] = min(low[work[-1][0]], low[node])
            if low[node] == index[node]:
                comp = []
                while True:
                    w = stack.pop()
                    on.discard(w)
                    comp.append(w)
                    if w == node:
                        break
                out.append(comp)
    return out


def weak_components(nodes, edges):
    parent = {n: n for n in nodes}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    return len({find(n) for n in nodes})


def analyse_relation(pred, edges, declared, retired, g, declared_tops,
                     inverse_pairs, closure_cap):
    """Full structural report for one relation, edges child to parent."""
    up = defaultdict(set)
    down = defaultdict(set)
    self_loops = []
    for c, p in edges:
        if c == p:
            self_loops.append(c)
            continue
        up[c].add(p)
        down[p].add(c)
    nodes = set(up) | set(down) | set(self_loops)
    undecl = {n for n in nodes if n not in declared}

    print(f"\n  structure via {short(pred, g)} "
          f"(edges read child to parent"
          f"{', inverted from the file' if ORIENT[pred] == 'down' else ''})")
    print(f"    nodes {len(nodes)} ({len(nodes) - len(undecl)} declared, "
          f"{len(undecl)} undeclared)   edges "
          f"{sum(len(v) for v in up.values())}   "
          f"self-loops {len(self_loops)}")
    if undecl:
        print(f"    undeclared nodes, e.g.: "
              f"{', '.join(loc(n) for n in sorted(undecl)[:5])}")
        print("    (a resource over this relation asserts order over "
              "concepts the file never declares; declare or intend)")
    if self_loops:
        print(f"    self-loops, e.g.: "
              f"{', '.join(loc(n) for n in self_loops[:5])}")

    # cycles
    sccs = [c for c in tarjan_sccs(sorted(nodes), up) if len(c) > 1]
    cyclic = {n for c in sccs for n in c} | set(self_loops)
    if sccs:
        w = sccs[0]
        print(f"    cycles: {len(sccs)} strongly connected components, "
              f"largest {max(len(c) for c in sccs)}, e.g. "
              f"{' < '.join(loc(n) for n in w[:4])} < {loc(w[0])}")
        print("    (a cycle plus antisymmetry identifies its members; "
              "consistent only while nothing declares them distinct)")
    else:
        print("    cycles: none")

    # roots, leaves, coverage
    roots = sorted(n for n in nodes if not up.get(n) and n not in cyclic)
    leaves = sorted(n for n in nodes if not down.get(n) and n not in cyclic)
    untouched = len(declared - nodes)
    line = f"    roots {len(roots)}"
    if pred == str(SKOS.broader) and declared_tops:
        agree = set(roots) == declared_tops
        line += (f" (declared top concepts {len(declared_tops)}, "
                 f"{'agree' if agree else 'DISAGREE'})")
        if not agree:
            for n in sorted(set(roots) ^ declared_tops)[:5]:
                side = "computed only" if n in set(roots) else "declared only"
                line += f"\n      {side}: {loc(n)}"
    print(line)
    print(f"    leaves {len(leaves)}   declared concepts this relation "
          f"never touches: {untouched}")

    # multi-parent
    multi = sorted((n, v) for n, v in up.items() if len(v) > 1)
    print(f"    multi-parent nodes: {len(multi)}")
    for n, v in multi[:5]:
        print(f"      {loc(n)} -> {', '.join(loc(p) for p in sorted(v))}")

    # levels by longest path from a root, on the acyclic part
    acyc = {n for n in nodes if n not in cyclic}
    remaining = {n: len([p for p in up.get(n, ()) if p in acyc])
                 for n in acyc}
    level = {}
    best_pred = {}
    q = deque(n for n in acyc if remaining[n] == 0)
    for n in q:
        level[n] = 1
    order = []
    while q:
        p = q.popleft()
        order.append(p)
        for c in down.get(p, ()):
            if c not in acyc:
                continue
            if level[p] + 1 > level.get(c, 0):
                level[c] = level[p] + 1
                best_pred[c] = p
            remaining[c] -= 1
            if remaining[c] == 0:
                q.append(c)
    hist = Counter(level.values())
    if hist:
        print("    levels (longest path from a root): " + "  ".join(
            f"{lv}:{hist[lv]}" for lv in sorted(hist)))
        deep = max(level, key=lambda n: level[n])
        chain = [deep]
        while chain[-1] in best_pred:
            chain.append(best_pred[chain[-1]])
        print(f"    longest chain {level[deep] - 1} hops: "
              f"{' < '.join(loc(n) for n in chain)}")
    if cyclic:
        print(f"    ({len(cyclic)} cyclic nodes excluded from levels)")

    # branching, components
    if down:
        widest = max(down.items(), key=lambda kv: len(kv[1]))
        mean = sum(len(v) for v in down.values()) / len(down)
        print(f"    branching: max {len(widest[1])} children "
              f"({loc(widest[0])}), mean {mean:.1f} over nodes with "
              "children")
    print(f"    weakly connected components: "
          f"{weak_components(nodes, [(c, p) for c, ps in up.items() for p in ps])}")

    # closure: comparable pairs, the premise budget of a resource
    if len(nodes) <= closure_cap:
        reach = {}
        strict = 0
        for n in order:  # parents before children
            r = set()
            for p in up.get(n, ()):
                if p in acyc:
                    r |= reach[p]
                    r.add(p)
            reach[n] = r
            strict += len(r)
        print(f"    comparable pairs in the reflexive transitive closure: "
              f"{strict} strict + {len(acyc)} reflexive"
              f"{' (acyclic part only)' if cyclic else ''}")
    else:
        print(f"    closure skipped ({len(nodes)} nodes > cap "
              f"{closure_cap}; raise --closure-cap to compute)")

    # deprecation interaction
    if retired:
        cats = Counter()
        witness = {}
        for c, ps in up.items():
            for p in ps:
                key = (c in retired, p in retired)
                cats[key] += 1
                witness.setdefault(key, (c, p))
        lbl = {(False, True): "live below retired",
               (True, False): "retired below live",
               (True, True): "retired below retired"}
        parts = []
        for key, name in lbl.items():
            parts.append(f"{name} {cats.get(key, 0)}")
        print("    deprecation interaction: " + ", ".join(parts))
        if cats.get((False, True)):
            c, p = witness[(False, True)]
            print(f"      e.g. {loc(c)} below retired {loc(p)}; a "
                  "pass-through reading decision is live for this file")

    # inverse redundancy
    inv = INVERSE.get(pred)
    if inv and inverse_pairs.get(inv):
        mirrored = sum(1 for c, ps in up.items() for p in ps
                       if (c, p) in inverse_pairs[inv])
        total = sum(len(v) for v in up.values())
        print(f"    inverse {short(inv, g)} also published: "
              f"{mirrored} of {total} edges mirrored")

    return {
        "edges": sum(len(v) for v in up.values()) + len(self_loops),
        "depth": max(hist) - 1 if hist else 0,
        "roots": len(roots),
        "multi": len(multi),
        "cycles": len(sccs) + (1 if self_loops else 0),
    }


# ---------------------------------------------------------------------
# per-file survey
# ---------------------------------------------------------------------

def survey(path: Path, verbose: bool, home_override, closure_cap):
    fmt = "xml" if path.suffix.lower() in (".rdf", ".xml", ".owl") else "turtle"
    g = Graph()
    g.parse(path, format=fmt)

    concepts = {s for t in (SKOS.Concept, RDFS.Class, OWL.Class)
                for s in g.subjects(RDF.type, t) if isinstance(s, URIRef)}
    if not concepts:
        concepts = {s for s in g.subjects(SKOS.inScheme, None)
                    if isinstance(s, URIRef)}

    ns = namespaces_of(concepts)
    if home_override:
        home = set(home_override)
    else:
        home = {n for n, k in ns.items()
                if k >= max(1, len(concepts) // 20)}

    def is_own(node):
        return isinstance(node, URIRef) and any(str(node).startswith(n)
                                                for n in home)

    # retired set, from the known predicate list
    retired = set()
    for p in DEPRECATION:
        for s, o in g.subject_objects(URIRef(p)):
            if isinstance(o, Literal) and str(o).lower() in ("false", "accepted", "stable"):
                continue
            if is_own(s):
                retired.add(s)

    declared_tops = {o for o in g.objects(None, SKOS.hasTopConcept)
                     if isinstance(o, URIRef)}
    declared_tops |= {s for s in g.subjects(SKOS.topConceptOf, None)
                      if isinstance(s, URIRef)}

    internal = Counter()       # concept to declared concept
    own_undeclared = Counter() # own namespace, endpoint not declared
    external = Counter()       # to a named node elsewhere
    literal = Counter()
    ext_targets = defaultdict(Counter)
    rel_edges = defaultdict(list)     # oriented child to parent
    raw_pairs = defaultdict(set)      # as written, for inverse checks
    ident_edges = []

    for s, p, o in g:
        own_s = is_own(s)
        if not own_s:
            continue
        ps = str(p)
        if isinstance(o, Literal):
            if s in concepts:
                literal[ps] += 1
            continue
        own_o = is_own(o)
        if own_o:
            if s in concepts and o in concepts:
                internal[ps] += 1
            else:
                own_undeclared[ps] += 1
            if ps in ORIENT:
                edge = (s, o) if ORIENT[ps] == "up" else (o, s)
                rel_edges[ps].append(edge)
                raw_pairs[ps].add(edge)
            if ps in IDENTITY:
                ident_edges.append((s, o))
        elif isinstance(o, (URIRef, BNode)):
            if s in concepts:
                external[ps] += 1
                host = (str(o).split("//")[-1].split("/")[0]
                        if isinstance(o, URIRef) else "(blank node)")
                ext_targets[ps][host] += 1

    print(f"\n=== {path}")
    print(f"{len(g)} triples, {len(concepts)} declared concepts, "
          f"{len(retired)} retired")
    if len(ns) > 1:
        print("namespaces of the concepts:")
        for n, k in ns.most_common(5):
            mark = "  <- home" if n in home else ""
            print(f"    {k:6}  {n}{mark}")

    def role_of(ps):
        if ps in ORIENT:
            return "   ORDER CANDIDATE"
        if ps in IDENTITY:
            return "   identity"
        if ps in SEPARATION:
            return "   separation"
        if ps in MAPPING:
            return "   mapping"
        if ps in DEPRECATION:
            return "   deprecation"
        if ps in ANNOTATION:
            return "   annotation"
        return ""

    def block(title, counter, note=None, targets=None):
        if not counter:
            return
        print(f"\n  {title}")
        if note:
            print(f"    {note}")
        for ps, k in counter.most_common():
            print(f"    {k:6}  {short(ps, g)}{role_of(ps)}")
            if targets and verbose:
                for host, hk in targets[ps].most_common(4):
                    print(f"            {hk:6}  -> {host}")

    block("between declared concepts of this vocabulary", internal,
          "candidates for the order; which one a profile reads is its "
          "decision")
    block("to an own-namespace node not declared a concept", own_undeclared,
          "usually a builder bug detector: order over undeclared subjects")
    block("to something outside this vocabulary", external,
          "not an order over these concepts: typing, alignment, or "
          "membership", ext_targets)
    block("about a concept rather than between concepts", literal)

    # malformed Wikidata targets, page URL where the entity IRI is meant
    malformed = sorted((s, o) for p in MAPPING
                       for s, o in g.subject_objects(URIRef(p))
                       if "wikidata.org/wiki/" in str(o))
    if malformed:
        print("\n  malformed Wikidata targets (page URL, not entity IRI):")
        for s, o in malformed[:10]:
            print(f"    {loc(s)} -> {o}")

    # per-relation structure
    stats = {}
    for pred in sorted(rel_edges, key=lambda p: -len(rel_edges[p])):
        stats[pred] = analyse_relation(
            pred, rel_edges[pred], concepts, retired, g, declared_tops,
            raw_pairs, closure_cap)

    # identity structure
    ident_pairs = {frozenset(e) for e in ident_edges if e[0] != e[1]}
    if ident_edges:
        nodes = {n for e in ident_edges for n in e}
        parent = {n: n for n in nodes}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for a, b in ident_edges:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb
        clusters = Counter(find(n) for n in nodes)
        print(f"\n  identity structure: {len(ident_edges)} directional "
              f"assertions, {len(ident_pairs)} unordered pairs, "
              f"{len(clusters)} clusters, largest "
              f"{max(clusters.values())}")

    # summary
    sep = sum(k for p, k in (internal + external).items()
              if p in SEPARATION)
    print("\n  summary")
    if stats:
        for p, st in stats.items():
            print(f"    {st['edges']:6}  order assertions via {short(p, g)}"
                  f", depth {st['depth']}, roots {st['roots']}, "
                  f"multi-parent {st['multi']}, cycles {st['cycles']}")
    else:
        print("           no order candidate between concepts of this file")
    print(f"    {len(ident_pairs) if ident_edges else 0:6}  identity pairs")
    print(f"    {sep:6}  separation assertions "
          f"{'' if sep else '(none: distinctness is the parties to declare)'}")
    print(f"    {len(retired):6}  retired concepts")
    lic = list(g.objects(None, DCTERMS.license))
    print(f"    licence: {lic[0] if lic else 'not stated in the file'}")

    dom = max(stats.items(), key=lambda kv: kv[1]["edges"])[1] if stats \
        else {"edges": 0, "depth": 0, "roots": 0, "multi": 0, "cycles": 0}
    return {"path": str(path), "concepts": len(concepts),
            "retired": len(retired), "sep": sep, **dom}


def main() -> int:
    ap = argparse.ArgumentParser(
        description="survey a vocabulary's relations and their structure")
    ap.add_argument("files", nargs="+", type=Path)
    ap.add_argument("-v", "--verbose", action="store_true",
                    help="also show where external targets point")
    ap.add_argument("--home", help="comma-separated namespace prefixes to "
                    "treat as the vocabulary's own, overriding the "
                    "heuristic")
    ap.add_argument("--closure-cap", type=int, default=20000,
                    help="skip the closure computation above this many "
                    "nodes")
    args = ap.parse_args()
    home = args.home.split(",") if args.home else None

    rows = []
    for f in args.files:
        try:
            rows.append(survey(f, args.verbose, home, args.closure_cap))
        except Exception as e:
            print(f"\n=== {f}\n  could not read: {type(e).__name__}: "
                  f"{str(e).splitlines()[0][:70]}")

    if len(rows) > 1:
        print("\n\n=== all files (dominant relation per file)")
        print(f"{'concepts':>9} {'edges':>7} {'depth':>6} {'roots':>6} "
              f"{'multi':>6} {'cyc':>4} {'ret':>5} {'sep':>4}   file")
        for r in rows:
            print(f"{r['concepts']:>9} {r['edges']:>7} {r['depth']:>6} "
                  f"{r['roots']:>6} {r['multi']:>6} {r['cycles']:>4} "
                  f"{r['retired']:>5} {r['sep']:>4}   "
                  f"{Path(r['path']).name}")
        print("\nseparation is zero everywhere it is zero for the same "
              "reason: a\npublished vocabulary states what it has "
              "established, and whether two\nof its concepts may be treated "
              "as apart is a question about the use\nbeing made of them.")
    return 0


if __name__ == "__main__":
    sys.exit(main())