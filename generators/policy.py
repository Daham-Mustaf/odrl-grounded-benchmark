"""
policy.py
=========
Reads ODRL policies, a profile and a resource out of Turtle, and produces the
objects the semantics works on.

The profile is required.  Without it there is no sort, and without a sort
well-sortedness cannot be checked: defaulting to nom would silently accept
some constraints and reject others with no basis.  A missing profile entry is
an error, not a default.

The background theory may be empty.  That is a legitimate state of the world,
not a failure: with no distinctness or disjointness declared, nothing is
Incompatible except where an operator meets its own complement, because a
structure may identify any two concepts the resource has not separated.
"""

from dataclasses import dataclass, field

try:
    from rdflib import Graph, Namespace, RDF
    from rdflib.namespace import RDFS
except ImportError:                                   # pragma: no cover
    Graph = None

ODRL = "http://www.w3.org/ns/odrl/2/"
VREP = "https://w3id.org/odrl-kb/verdict-report#"

SET_OPERATORS = {"isAnyOf", "isAllOf", "isNoneOf"}


class ProfileError(Exception):
    """The profile does not cover an operand the policy constrains."""


class GroundingError(Exception):
    """A right-operand value names no concept of its resource."""


@dataclass
class Binding:
    """What the profile declares for one operand."""
    operand: str
    sort: str
    resource: str
    background: str | None = None


@dataclass
class Constraint:
    operand: str
    operator: str
    values: tuple
    iri: str | None = None
    side: str = "offer"


@dataclass
class Resource:
    """Concepts and the order the authority published."""
    iri: str
    concepts: set = field(default_factory=set)
    order: set = field(default_factory=set)      # (below, above) pairs

    def term(self, iri: str) -> str:
        """The constant a concept IRI is encoded as."""
        return _slug(iri)


def _slug(iri: str) -> str:
    """A TPTP constant for an IRI.  Stable, lowercase, prefix preserved."""
    tail = iri.rstrip("/").rsplit("/", 1)[-1].rsplit("#", 1)[-1]
    return "".join(ch if ch.isalnum() else "_" for ch in tail).lower()


def _local(uri) -> str:
    s = str(uri)
    return s.rsplit("#", 1)[-1].rsplit("/", 1)[-1]


def read_profile(path) -> dict[str, Binding]:
    """Operand -> Binding.  One entry per operand in scope."""
    g = Graph().parse(path, format="turtle")
    out = {}
    V = Namespace(VREP)
    for b in g.subjects(RDF.type, V.OperandBinding):
        operand = _local(g.value(b, V.leftOperand))
        sort = _local(g.value(b, V.sort))
        resource = str(g.value(b, V.resource))
        background = g.value(b, V.backgroundTheory)
        out[operand] = Binding(operand, sort, resource,
                               str(background) if background else None)
    return out


def read_policy(path, side: str) -> list[Constraint]:
    """Every constraint of a policy, in document order."""
    g = Graph().parse(path, format="turtle")
    O = Namespace(ODRL)
    out = []
    for c in g.subjects(O.leftOperand, None):
        operand = _local(g.value(c, O.leftOperand))
        operator = _local(g.value(c, O.operator))
        values = [v for v in g.objects(c, O.rightOperand)]
        out.append(Constraint(operand, operator,
                              tuple(_slug(str(v)) for v in values),
                              iri=str(c) if not str(c).startswith("N") else None,
                              side=side))
    return out


def read_resource(path, iri: str) -> Resource:
    """Concepts and order assertions.  Nothing else is read."""
    g = Graph().parse(path, format="turtle")
    r = Resource(iri)
    SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
    GN = Namespace("https://www.geonames.org/ontology#")
    for s in set(g.subjects()):
        if isinstance(s, type(next(iter(g.subjects())))) and "#" in str(s) or "/" in str(s):
            r.concepts.add(_slug(str(s)))
    for pred in (SKOS.broader, GN.parentFeature, RDFS.subClassOf):
        for s, o in g.subject_objects(pred):
            r.order.add((_slug(str(s)), _slug(str(o))))
            r.concepts.update({_slug(str(s)), _slug(str(o))})
    return r


def bind(constraints, profile: dict[str, Binding]):
    """Attach each constraint to its binding, refusing unprofiled operands."""
    missing = {c.operand for c in constraints} - set(profile)
    if missing:
        raise ProfileError(
            "no sort declared for: " + ", ".join(sorted(missing)) +
            ".  The profile must bind every operand in scope; there is no "
            "default sort.")
    return {c.operand: profile[c.operand] for c in constraints}


def ground(constraints, resource: Resource):
    """Every right-operand value must name a concept of the resource."""
    bad = [v for c in constraints for v in c.values if v not in resource.concepts]
    if bad:
        raise GroundingError(", ".join(sorted(set(bad))))
    return True


def by_operand(*constraint_lists):
    """Group the constraints of both policies by left operand."""
    out = {}
    for cs in constraint_lists:
        for c in cs:
            out.setdefault(c.operand, []).append(c)
    return out