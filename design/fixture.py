"""
fixture.py
==========
A resource and its background theories, as premises with names.

A fixture is what a binding points at.  It holds the assertions an
authority published, the declarations parties have made over them, the
concepts they range over, and the provenance of the file all of that was
read from.  Problems name a fixture and a version; they do not carry
copies of it.

Parsed, not referenced
----------------------
The assertions are held as objects rather than as a path to an axiom file,
and that decision has three consequences worth the extra work.

A premise gets its name once, here, from what it says.  Both encodings then
serialise the same objects, so ``res_france_within_europe`` is that
assertion's name in TPTP and in SMT-LIB alike.  When the two encodings
named premises independently, one by content and one by position, nothing
could compare them assertion by assertion, and the claim that two provers
used the same premises was a claim about counts.

A query can carry the premises a problem needs rather than the whole
resource.  Including all of DPV Locations puts five thousand assertions in
front of a solver to decide something about two countries.

And a certificate can be checked.  A checker asks whether every premise a
refutation cites is a formula of the query, which requires knowing what the
query's formulas are.  With an include directive it would have to re-read
and re-parse the resource, which is the compiler's job done twice.

Concepts
--------
The concept set is the resource's, not the problem's.  The witness
condition's non-emptiness conjunct is a disjunction over the concepts the
grounding names, and that is a property of the resource: a problem
mentioning two countries still asks whether some concept satisfies its
constraints, and the answer ranges over all of them.

Counts
------
Every number a fixture reports comes from its census file.  None is typed
into a docstring, a manifest or a paper, because a typed number is a claim
about a file that nothing checks and that goes stale the first time the
file is refetched.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from vocabulary import PremiseClass


@dataclass(frozen=True)
class Premise:
    """One assertion, with its provenance and a name derived from it.

    The name is the identifier both encodings use, and it is built from
    what the assertion says rather than from where it sits, so that adding
    an assertion does not renumber the others and a diff between two
    versions of a resource is readable.
    """

    name: str
    kind: PremiseClass
    lhs: str
    rhs: str

    def __post_init__(self) -> None:
        declared = PremiseClass.from_name(self.name)
        if declared is not self.kind:
            raise ValueError(
                f"premise {self.name!r} is declared {self.kind} but its "
                f"name reads as {declared}; the name is what a proof or an "
                f"unsat core carries, so the two cannot differ")

    @property
    def is_ground(self) -> bool:
        """Whether the assertion has no quantifier.

        Everything except declared disjointness.  The decidability argument
        turns on this: disjointness is the only quantified part of a
        background theory, and saying so requires being able to tell.
        """
        return self.kind is not PremiseClass.BG_DISJOINTNESS


@dataclass(frozen=True)
class BackgroundTheory:
    """A set of declarations the parties may adopt, and may withdraw.

    Named, so that a problem cites one and a report says which.  The empty
    theory is a theory: it is what the parties declare when they declare
    nothing, and a verdict under it rests on the resource alone.

    ``warrant`` records why the declarations are held to be right.  For a
    theory generated from a publisher's own definitions it names them; for
    one the parties assert on their own authority it says so.  A refutation
    citing a premise from here is open to whoever made the declaration, and
    the warrant is what they would have to defend.
    """

    id: str
    title: str
    premises: tuple[Premise, ...]
    warrant: str = ""

    def __post_init__(self) -> None:
        for p in self.premises:
            if not p.kind.is_withdrawable:
                raise ValueError(
                    f"{p.name} is {p.kind}, which is not a party's to "
                    f"declare; a background theory holds only distinctness "
                    f"and disjointness")


@dataclass(frozen=True)
class Provenance:
    """Where the file came from, and when.

    Every field is required.  A resource whose version is unrecorded cannot
    be refetched, and one whose licence is unrecorded cannot be
    redistributed, and both are questions a reader of the artefact asks
    first.
    """

    namespace: str
    version: str
    retrieved: str
    source_url: str
    checksum: str
    licence: str
    licence_note: str = ""


@dataclass(frozen=True)
class Fixture:
    """One resource, its concepts, its background theories, its provenance.

    ``order`` holds what the authority published, read through whichever
    relation the profile's reading takes.  Two fixtures may be built from
    one file: the Locations extension is read once as containment and once
    as containment together with union membership, and they are different
    resources although they share a source.
    """

    id: str
    title: str
    concepts: frozenset[str]
    order: tuple[Premise, ...]
    theories: dict[str, BackgroundTheory]
    provenance: Provenance
    census: dict = field(default_factory=dict)
    reading: str = ""

    def __post_init__(self) -> None:
        for p in self.order:
            if p.kind is not PremiseClass.RESOURCE:
                raise ValueError(
                    f"{p.name} is {p.kind}; the order holds only what the "
                    f"authority published")
        loose = {e for p in self.order for e in (p.lhs, p.rhs)
                 } - self.concepts
        if loose:
            raise ValueError(
                f"{self.id}: {len(loose)} order assertion endpoints are not "
                f"concepts of this fixture, e.g. {sorted(loose)[:3]}; either "
                f"declare them or exclude the assertions")
        if "empty" not in self.theories:
            raise ValueError(
                f"{self.id}: every fixture offers an empty theory, since a "
                f"verdict resting on the resource alone is the base case")

    def theory(self, theory_id: str) -> BackgroundTheory:
        if theory_id not in self.theories:
            raise KeyError(
                f"{self.id} has no background theory {theory_id!r}; it "
                f"offers {', '.join(sorted(self.theories))}")
        return self.theories[theory_id]

    def count(self, key: str) -> int:
        """A measured count, from the census file.

        Raises rather than returning zero for a key the census does not
        carry: a missing measurement and a measurement of nothing are
        different, and only one of them is an answer.
        """
        if key not in self.census:
            raise KeyError(
                f"{self.id}: the census records no {key!r}; it has "
                f"{', '.join(sorted(self.census))}. Numbers are measured, "
                f"not supplied")
        return self.census[key]

    def summary(self) -> str:
        reading = f", {self.reading} reading" if self.reading else ""
        return (f"{self.id} ({self.provenance.version}{reading}): "
                f"{len(self.concepts)} concepts, {len(self.order)} order "
                f"assertions, theories "
                f"{', '.join(sorted(self.theories))}")


# --- loading -----------------------------------------------------------

def _slug(iri: str) -> str:
    """A formula-name fragment for a concept.

    Local name, lowercased, non-alphanumerics to underscores.  Collisions
    across namespaces are the caller's to avoid by prefixing, and
    :func:`load` checks that none survive.
    """
    local = iri.rsplit("#", 1)[-1] if "#" in iri else iri.rstrip("/").rsplit("/", 1)[-1]
    out = []
    for ch in local:
        if ch.isupper() and out and out[-1] != "_":
            out.append("_")
        out.append(ch.lower() if ch.isalnum() else "_")
    return "".join(out).strip("_").replace("__", "_")


def order_premise(lhs: str, rhs: str, prefix: str) -> Premise:
    """An order assertion, named for what it says."""
    return Premise(f"res_{prefix}{_slug(lhs)}_below_{prefix}{_slug(rhs)}",
                   PremiseClass.RESOURCE, lhs, rhs)


def distinctness_premise(a: str, b: str, prefix: str) -> Premise:
    lo, hi = sorted((a, b))
    return Premise(
        f"bg_dist_{prefix}{_slug(lo)}_from_{prefix}{_slug(hi)}",
        PremiseClass.BG_DISTINCTNESS, lo, hi)


def disjointness_premise(a: str, b: str, prefix: str) -> Premise:
    lo, hi = sorted((a, b))
    return Premise(
        f"bg_disj_{prefix}{_slug(lo)}_from_{prefix}{_slug(hi)}",
        PremiseClass.BG_DISJOINTNESS, lo, hi)


def load(path: Path) -> Fixture:
    """Read a fixture directory: metadata, order, theories, census.

        <path>/metadata.json    provenance, id, title, reading, prefix
        <path>/order.json       [[child, parent], ...]
        <path>/theories.json    {id: {title, warrant, distinct, disjoint}}
        <path>/census.json      measured counts

    The census is required.  A fixture without one has numbers nobody has
    checked, and every count the paper quotes comes from here.
    """
    meta = json.loads((path / "metadata.json").read_text())
    pairs = json.loads((path / "order.json").read_text())
    census = json.loads((path / "census.json").read_text())
    prefix = meta.get("prefix", "")

    concepts = frozenset(meta["concepts"])
    order = tuple(order_premise(a, b, prefix) for a, b in pairs)

    names = [p.name for p in order]
    if len(set(names)) != len(names):
        dup = sorted({n for n in names if names.count(n) > 1})
        raise ValueError(
            f"{meta['id']}: {len(dup)} order assertions share a name, e.g. "
            f"{dup[:2]}; two concepts have collided under the slug rule and "
            f"the prefix must separate them")

    raw = json.loads((path / "theories.json").read_text())
    theories = {}
    for tid, t in raw.items():
        prem = tuple(
            [distinctness_premise(a, b, prefix)
             for a, b in t.get("distinct", [])]
            + [disjointness_premise(a, b, prefix)
               for a, b in t.get("disjoint", [])])
        theories[tid] = BackgroundTheory(tid, t["title"], prem,
                                         t.get("warrant", ""))
    theories.setdefault(
        "empty", BackgroundTheory("empty", "No declarations", (),
                                  "the resource alone"))

    return Fixture(
        id=meta["id"], title=meta["title"], concepts=concepts, order=order,
        theories=theories, census=census, reading=meta.get("reading", ""),
        provenance=Provenance(**meta["provenance"]))