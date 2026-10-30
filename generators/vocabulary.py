"""
vocabulary.py
=============
The candidates of a witness.

Definition Witness lets the value of a use be any concept of the operand's
vocabulary.  A pair query therefore ranges over every concept of the
vocabulary the binding reads, and not over the concepts the two policies
happen to name: a third language satisfies "anywhere but German" and
"anywhere but French" together, and a policy pair that only a concept neither
policy names can satisfy has to be found Compatible.

    concepts(resource)                      every concept of a resource, as the
                                            constants the encodings use
    candidates(resource, named)             the named constants first, then the
                                            rest, sorted
    register(resource, constants)           a vocabulary built outside
                                            problems/resources (the tests)
    connected(seeds, edges)                 the concepts order statements
                                            connect to the seeds
    between(seeds, edges)                   the seeds and the concepts on a
                                            path of statements between two

Every vocabulary takes the same path, DPV Locations' five thousand places
included.  The witness condition (compile.py) does not enumerate every
candidate in every part: where a literal pins the use to a value, that value
is the only one it has to try.  A check that only asks whether some use
exists may search fewer candidates (check_policies, 5a); a query that must
also find that no use exists may not.
"""

from collections import defaultdict, deque
from pathlib import Path

from rdflib import Graph, Namespace, RDF, URIRef
from rdflib.namespace import DCTERMS, SKOS

import declarations

RESOURCES = Path(__file__).resolve().parent.parent / "problems" / "resources"
GN = Namespace("https://www.geonames.org/ontology#")

FILE = {
    "https://w3id.org/odrl-kb/dpv-purposes": "dpv-purposes.ttl",
    "https://w3id.org/odrl-kb/dpv-consent": "consent.ttl",
    "https://w3id.org/odrl-kb/dpv-tom": "tom.ttl",
    "https://w3id.org/odrl-kb/eu-file-type": "filetype.ttl",
    "https://w3id.org/odrl-kb/bcp47": "bcp47.ttl",
    "https://w3id.org/odrl-kb/geonames-europe": "geonames.ttl",
    "https://w3id.org/odrl-kb/dpv-loc-geo": "dpvloc-geo.ttl",
    "https://w3id.org/odrl-kb/dpv-loc-juris": "dpvloc-juris.ttl",
}

_cache: dict = {}


def concepts(resource: str) -> list:
    """Every concept of the resource, as a constant, sorted."""
    if resource not in _cache:
        if resource not in FILE:
            raise ValueError(f"no concept set known for resource {resource}")
        g = Graph().parse(RESOURCES / FILE[resource], format="turtle")
        if resource == "https://w3id.org/odrl-kb/geonames-europe":
            iris = list(g.subjects(RDF.type, GN.Feature))
        elif resource == "https://w3id.org/odrl-kb/bcp47":
            iris = list(g.subjects(RDF.type, SKOS.Concept))
        else:
            iris = [o for o in g.objects(None, DCTERMS.identifier)
                    if isinstance(o, URIRef)]
        constant = declarations.constant_for(resource)
        _cache[resource] = sorted({constant(i) for i in iris})
    return list(_cache[resource])


def register(resource: str, constants) -> None:
    """A vocabulary built in memory, as the end-to-end test builds them."""
    _cache[resource] = sorted(set(constants))


def candidates(resource: str, named: list) -> list:
    """The named constants in the order given, then every other concept."""
    every = concepts(resource)
    missing = [c for c in named if c not in every]
    if missing:
        raise ValueError(f"{', '.join(missing)} named by the problem but not "
                         f"a concept of {resource}")
    return list(named) + [c for c in every if c not in named]


def connected(seeds, edges) -> set:
    """The seeds and every concept an order statement connects to one of
    them, in either direction, until no statement leads out of the set."""
    adj = defaultdict(set)
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    seen = set(seeds)
    queue = deque(seeds)
    while queue:
        for nxt in adj.get(queue.popleft(), ()):
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return seen


def between(seeds, edges) -> set:
    """The seeds and every concept on a path of order statements from one
    seed up to another: x with a <= x <= b published, a and b seeds."""
    up, down = defaultdict(set), defaultdict(set)
    for a, b in edges:
        up[a].add(b)
        down[b].add(a)

    def reach(start, adj):
        seen, queue = {start}, deque([start])
        while queue:
            for nxt in adj.get(queue.popleft(), ()):
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
        return seen

    seeds = list(dict.fromkeys(seeds))
    above = set().union(*(reach(s, up) for s in seeds)) if seeds else set()
    below = set().union(*(reach(s, down) for s in seeds)) if seeds else set()
    return set(seeds) | (above & below)

