"""
build_consent.py
================
Builds the DPV consent status resource: the concept set, the order, three
background theories, the TPTP axioms, and the profile entry.

    python build_consent.py --module vocabularies/dpv-2.3/modules/consent_status.ttl \
                            --out problems

Why this resource is in the suite
----------------------------------
It is the smallest, and it is the one where a policy anyone would write meets
a hierarchy worth traversing.  Thirteen concepts, two levels, and the
constraint (Status, isA, ConsentStatusValidForProcessing) admits exactly the
two states the vocabulary says may justify processing.  A controller writes
that constraint; the resource decides what it covers.

It is also the case where the disjointness is stated and not asserted.  DPV
defines ConsentStatusValidForProcessing as the states of consent that can be
used as valid justifications for processing data, and
ConsentStatusInvalidForProcessing as the states that cannot.  Can and cannot:
the two are disjoint by the definitions, and the module publishes no
owl:disjointWith.  A verdict turning on the two being disjoint therefore
rests on a declaration the parties make, and the certificate says so, even
though the authority's own prose is what warrants it.

That is a better warrant than any other background theory in the suite.  The
ISO 3166 rule rests on a registry convention read from a standard's text; a
bilateral distinctness declaration rests on nothing but the parties' say-so.
Here the vocabulary states the intent in the definition and omits it from the
file, and a party adopting it follows the publisher rather than adding to
them.  The verdict is still withdrawable and the certificate still marks it:
what the definitions warrant, they do not assert.

The module boundary
-------------------
The module publishes thirteen order assertions.  One, ConsentStatus below
Status, leaves the module: Status belongs to the status module and is itself
below Context in the DPV core.  It is dropped, and ConsentStatus becomes the
root of the slice, which leaves twelve.

This is the decision taken for the purposes module, where RightsFulfilment
below LegalObligation crosses into the legal basis module and is dropped for
the same reason: an operand bound to consent status is bound to the states of
consent, and a chain leaving the module leads to concepts the binding does
not cover.  Recorded here rather than left implicit, since the count in the
paper is the count after the boundary.

What the module does not publish
---------------------------------
No disjointness, as above.  No distinctness: nothing separates any two of the
thirteen, so two constraints naming different states are satisfiable together
until a party says otherwise.  And no identity assertions.

Typing is present and is not read.  Every concept carries
rdf:type dpv:ConsentStatus, including the two mid-level concepts, so the type
names the nearest ancestor carrying rdfs:subClassOf rather than the immediate
parent.  Nothing is typed dpv:ConsentStatusValidForProcessing at all.  A
reading of isA that follows rdf:type therefore cannot satisfy the constraint
this resource exists for, whatever the state; a reading that follows the
order can.  Section 7 reports that comparison.  The typing is outside
Definition 4 either way: it relates an individual to a class, and a resource
relates concepts to concepts.

Source
------
Data Privacy Vocabulary, consent status module, from the 2.3 release.  The
file itself carries owl:versionInfo "2.0" and owl:versionIRI
<https://w3id.org/dpv/2.0>, which is what the file says rather than what the
release directory says.  PROVENANCE.md records the retrieval URL and date,
which is what makes the slice reproducible.

Licensed under the W3C Document License 2023, which permits verbatim
redistribution and not derivative works.  This slice is a derivative.  The
same applies to the other DPV modules used in the suite.
"""

import argparse
import sys
from pathlib import Path

try:
    from rdflib import Graph, Namespace, URIRef, OWL, SKOS
except ImportError:
    print("needs rdflib: uv add rdflib", file=sys.stderr)
    raise

DPV = Namespace("https://w3id.org/dpv#")
SCHEME = DPV["consent-status-classes"]

VALID = "ConsentStatusValidForProcessing"
INVALID = "ConsentStatusInvalidForProcessing"

# What the module has once the boundary is applied.  Checked on every run:
# these numbers are in the resource header and in the paper.
EXPECT = {"concepts": 13, "order": 12, "crossing": 1}


def local(u) -> str:
    return str(u).rsplit("#", 1)[-1]


def slug(name: str) -> str:
    """TPTP constant for a concept name, CamelCase to snake_case."""
    out = []
    for i, ch in enumerate(name):
        if ch.isupper() and i and not name[i - 1].isupper():
            out.append("_")
        out.append(ch.lower())
    return "dpv_" + "".join(out)


def read(g):
    """Concepts, labels, definitions and the order, with the boundary applied.

    The crossing edges are returned rather than discarded, so the generator
    reports what it dropped instead of leaving the reader to infer it from a
    count.
    """
    concepts = sorted(local(s) for s in g.subjects(SKOS.inScheme, SCHEME))
    inside = set(concepts)

    labels, definitions = {}, {}
    for s in g.subjects(SKOS.inScheme, SCHEME):
        for o in g.objects(s, SKOS.prefLabel):
            if getattr(o, "language", None) == "en":
                labels[local(s)] = str(o)
        for o in g.objects(s, SKOS.definition):
            if getattr(o, "language", None) == "en":
                definitions[local(s)] = str(o)

    order, crossing = [], []
    for s, o in g.subject_objects(SKOS.broader):
        if local(s) not in inside:
            continue
        (order if local(o) in inside else crossing).append((local(s), local(o)))

    return concepts, labels, definitions, sorted(order), sorted(crossing)


def roots(concepts, order):
    below = {a for a, _ in order}
    return sorted(c for c in concepts if c not in below)


def depth(order):
    parents = {}
    for a, b in order:
        parents.setdefault(a, []).append(b)
    best, witness = 0, []

    def walk(node, path, seen):
        nonlocal best, witness
        if len(path) - 1 > best:
            best, witness = len(path) - 1, list(path)
        for p in parents.get(node, []):
            if p not in seen:
                walk(p, path + [p], seen | {p})

    for start in parents:
        walk(start, [start], {start})
    return best, witness


def resource_ttl(concepts, labels, definitions, order, crossing, meta) -> str:
    head = [
        "# DPV consent status: the order the module publishes.",
        "#",
        "# Thirteen states of consent under two mid-level concepts, one for",
        "# the states that may justify processing and one for the states that",
        "# may not.  The module asserts no disjointness between the two and no",
        "# distinctness between any pair; see the background theories.",
        "#",
        "# The module also types every concept dpv:ConsentStatus.  That is not",
        "# read here: typing relates an individual to a class, and a resource",
        "# relates concepts to concepts.",
        "#",
    ]
    if crossing:
        head += ["# Dropped at the module boundary:"]
        head += [f"#   {a} below {b}, which belongs to another module"
                 for a, b in crossing]
        head += ["#"]

    head += [
        f"# Source    : {meta['source']}",
        f"# Version   : {meta['version']} (as the file states)",
        f"# Retrieved : {meta['retrieved']}",
        f"# Licence   : {meta['licence']}",
        f"# NOTE      : {meta['licence_note']}",
        "#",
        f"# Concepts         : {len(concepts)}",
        f"# Order assertions : {len(order)}",
        "",
        "@prefix dpv:     <https://w3id.org/dpv#> .",
        "@prefix odrlkb:  <https://w3id.org/odrl-kb/dpv-consent#> .",
        "@prefix dcat:    <http://www.w3.org/ns/dcat#> .",
        "@prefix dcterms: <http://purl.org/dc/terms/> .",
        "@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .",
        "@prefix skos:    <http://www.w3.org/2004/02/skos/core#> .",
        "",
        "<https://w3id.org/odrl-kb/dpv-consent> a dcat:Dataset ;",
        '    dcterms:title "DPV consent status, module slice"@en ;',
        f"    dcterms:source <{meta['source_iri']}> ;",
        f"    odrlkb:conceptCount {len(concepts)} ;",
        f"    odrlkb:orderAssertionCount {len(order)} .",
        "",
    ]

    body = []
    for c in concepts:
        body.append(f"odrlkb:{slug(c)[4:]} a odrlkb:ConsentState ;")
        if labels.get(c):
            body.append(f'    rdfs:label "{labels[c]}"@en ;')
        if definitions.get(c):
            body.append(f'    skos:definition "{definitions[c].replace(chr(34), chr(39))}"@en ;')
        body.append(f"    dcterms:identifier dpv:{c} .")
        body.append("")

    body.append("# The order, as the module publishes it.")
    for a, b in order:
        body.append(f"odrlkb:{slug(a)[4:]} odrlkb:below odrlkb:{slug(b)[4:]} .")

    return "\n".join(head + body)


def background_ttl(meta) -> str:
    return f"""\
# Background theory for the DPV consent status resource: empty.
#
# The module asserts no disjointness and no distinctness.  Two constraints
# naming different states are therefore satisfiable together, and a verdict
# separating them rests on something the parties supply.
#
# The absence is worth stating, because the definitions read as though they
# supply it.  A state that may justify processing and a state that may not
# cannot be the same state; the module says so in prose and asserts nothing.
# See the definitional theory.
#
# Source: {meta['source_iri']}

@prefix bt:      <https://w3id.org/odrl-kb/background#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

<https://w3id.org/odrl-kb/dpv-consent/empty> a bt:BackgroundTheory ;
    dcterms:title "No declared distinctness or disjointness"@en ;
    bt:appliesTo <https://w3id.org/odrl-kb/dpv-consent> ;
    bt:assertionCount 0 .
"""


def definitional_ttl(meta) -> str:
    return f"""\
# Background theory for the DPV consent status resource: the two branches are
# disjoint.
#
# Adopted on the strength of the module's own definitions.
# ConsentStatusValidForProcessing is defined as the states of consent that
# can be used as valid justifications for processing data, and
# ConsentStatusInvalidForProcessing as the states that cannot.  Nothing below
# both can therefore exist, which is disjointness.
#
# The module does not assert it.  A party adopting this theory follows the
# publisher's stated intent rather than adding to it, and the certificate
# still marks the premise withdrawable: what the definitions warrant, they do
# not assert, and a reader who disagrees with the reading can withdraw the
# assertion and see the verdict reopen.
#
# Source: {meta['source_iri']}

@prefix dpv:     <https://w3id.org/dpv#> .
@prefix bt:      <https://w3id.org/odrl-kb/background#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

<https://w3id.org/odrl-kb/dpv-consent/definitional> a bt:BackgroundTheory ;
    dcterms:title "The valid and invalid branches are disjoint"@en ;
    bt:appliesTo <https://w3id.org/odrl-kb/dpv-consent> ;
    bt:generatedBy bt:PublishedDefinition ;
    bt:rule "states that can and cannot justify processing have nothing in common"@en ;
    bt:assertionCount 1 .

dpv:{VALID} bt:disjointFrom dpv:{INVALID} .
"""


def declared_ttl(pair, meta) -> str:
    a, b = pair
    return f"""\
# Background theory for the DPV consent status resource: one distinctness.
#
# The parties declare that these two states are different.  The module does
# not: it lists both and separates them in no way.  A verdict resting on this
# assertion is the parties' and can be reopened by withdrawing it.
#
# Source: {meta['source_iri']}

@prefix dpv:     <https://w3id.org/dpv#> .
@prefix bt:      <https://w3id.org/odrl-kb/background#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

<https://w3id.org/odrl-kb/dpv-consent/declared> a bt:BackgroundTheory ;
    dcterms:title "One declared distinctness"@en ;
    bt:appliesTo <https://w3id.org/odrl-kb/dpv-consent> ;
    bt:generatedBy bt:PartyDeclaration ;
    bt:assertionCount 1 .

dpv:{a} bt:distinctFrom dpv:{b} .
"""


def axioms(order, crossing, meta) -> str:
    lines = [
        "% DPV consent status: the order the module publishes.",
        "%",
        "% Thirteen states under two mid-level concepts.  The typing the",
        "% module also carries is not here: it relates an individual to a",
        "% class, and this resource relates concepts to concepts.",
        "%",
    ]
    if crossing:
        lines += ["% Dropped at the module boundary:"]
        lines += [f"%   {a} below {b}" for a, b in crossing]
        lines += ["%"]
    lines += [
        f"% Order assertions : {len(order)}",
        f"% Source           : {meta['source_iri']}",
        "",
    ]
    for a, b in order:
        lines.append(f"fof(res_{slug(a)}_below_{slug(b)}, axiom,")
        lines.append(f"    kge_leq({slug(a)}, {slug(b)})).")
        lines.append("")
    return "\n".join(lines)


def definitional_axioms() -> str:
    """Disjointness of the two branches, on the module's own definitions.

    The order clause of Definition 4: nothing lies below both.  Not an
    inequation, which would separate the two mid-level concepts and leave
    their subtrees free to overlap.
    """
    v, i = slug(VALID), slug(INVALID)
    return (
        "% Background theory: the valid and invalid branches are disjoint.\n"
        "%\n"
        "% Adopted from the module's definitions, which say that one branch\n"
        "% holds the states that can justify processing and the other the\n"
        "% states that cannot.  The module asserts no owl:disjointWith, so a\n"
        "% verdict resting on this is the parties'.\n"
        "%\n"
        "% Disjointness rather than distinctness: nothing lies below both, so\n"
        "% no state of consent is at once valid and invalid for processing.\n"
        "\n"
        f"fof(bt_{v}_disjoint_{i}, axiom,\n"
        f"    ! [X] : ~ ( kge_leq(X, {v}) & kge_leq(X, {i}) )).\n"
    )


def declared_axioms(pair) -> str:
    a, b = pair
    return (
        "% Background theory: one distinctness, declared by the parties.\n"
        "% The module publishes nothing that separates these two states.\n"
        "\n"
        f"fof(bt_{slug(a)}_distinct_{slug(b)}, axiom,\n"
        f"    {slug(a)} != {slug(b)}).\n"
    )


def profile_ttl() -> str:
    return """\
# Profile entry for a consent status operand over the DPV consent module.
#
# The sort is tax.  The module publishes a hierarchy of states, and the
# constraint a controller writes, that the status be one which may justify
# processing, is a question about that hierarchy: which states lie below the
# concept the offer names.
#
# The module also types its concepts, and a profile binding this operand to
# the typing rather than to the order would answer a different question.
# Section 7 reports what that reading returns.

@prefix dpvo: <https://w3id.org/dpv/mappings/odrl#> .
@prefix vrep: <https://w3id.org/odrl-verdict-report#> .
@prefix ex:   <https://w3id.org/odrl-kb/profile/> .

ex:b-consent-status a vrep:OperandBinding ;
    vrep:leftOperand dpvo:Status ;
    vrep:sort vrep:tax ;
    vrep:resource <https://w3id.org/odrl-kb/dpv-consent> ;
    vrep:backgroundTheory <https://w3id.org/odrl-kb/dpv-consent/empty> ;
    vrep:grounding vrep:sliceMembership .
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--module", required=True, type=Path)
    ap.add_argument("--declare-distinct", nargs=2, metavar=("A", "B"),
                    default=None)
    ap.add_argument("--retrieved", default="2026-08-19")
    ap.add_argument("--tag", default="consent")
    ap.add_argument("--out", default="problems", type=Path)
    ap.add_argument("--allow-count-change", action="store_true")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.module, format="turtle")

    concepts, labels, definitions, order, crossing = read(g)

    measured = {"concepts": len(concepts), "order": len(order),
                "crossing": len(crossing)}
    if not args.allow_count_change:
        drift = [(k, v, EXPECT[k]) for k, v in measured.items()
                 if v != EXPECT[k]]
        if drift:
            print("the module no longer has the shape the resource describes:",
                  file=sys.stderr)
            for k, got, want in drift:
                print(f"  {k}: {got}, expected {want}", file=sys.stderr)
            print("re-read the module, update EXPECT and the paper, or pass "
                  "--allow-count-change.", file=sys.stderr)
            return 1

    for c in (VALID, INVALID):
        if c not in concepts:
            print(f"{c} is not in the module; the definitional theory assumes "
                  f"both branches are present.", file=sys.stderr)
            return 1

    meta = {
        "source": "Data Privacy Vocabulary, consent status module",
        "source_iri": "https://w3id.org/dpv/2.3",
        "version": str(g.value(URIRef("https://w3id.org/dpv"),
                               OWL.versionInfo) or "unknown"),
        "retrieved": args.retrieved,
        "licence": "W3C Document License 2023",
        "licence_note": "permits verbatim redistribution, not derivatives; "
                        "this slice is a derivative and the licence is "
                        "unresolved",
    }

    for d in ("resources", "background", "axioms"):
        (args.out / d).mkdir(parents=True, exist_ok=True)
    tag = args.tag

    (args.out / "resources" / f"{tag}.ttl").write_text(
        resource_ttl(concepts, labels, definitions, order, crossing, meta),
        encoding="utf-8")
    (args.out / "background" / f"{tag}-empty.ttl").write_text(
        background_ttl(meta), encoding="utf-8")
    (args.out / "background" / f"{tag}-definitional.ttl").write_text(
        definitional_ttl(meta), encoding="utf-8")
    (args.out / "axioms" / f"DPV-{tag}.ax").write_text(
        axioms(order, crossing, meta), encoding="utf-8")
    (args.out / "axioms" / f"DPV-{tag}-definitional.ax").write_text(
        definitional_axioms(), encoding="utf-8")
    (args.out / "resources" / f"profile-{tag}.ttl").write_text(
        profile_ttl(), encoding="utf-8")

    if args.declare_distinct:
        a, b = args.declare_distinct
        missing = [x for x in (a, b) if x not in concepts]
        if missing:
            print(f"not in the module: {', '.join(missing)}", file=sys.stderr)
            return 1
        (args.out / "background" / f"{tag}-declared.ttl").write_text(
            declared_ttl((a, b), meta), encoding="utf-8")
        (args.out / "axioms" / f"DPV-{tag}-declared.ax").write_text(
            declared_axioms((a, b)), encoding="utf-8")

    hops, witness = depth(order)
    print(f"{len(concepts)} concepts, {len(order)} order assertions")
    print(f"roots: {', '.join(roots(concepts, order))}")
    print(f"longest chain: {hops} hops"
          + (f" ({' < '.join(witness)})" if witness else ""))
    print(f"version, as the file states: {meta['version']}")

    if crossing:
        print("\ndropped at the module boundary:")
        for a, b in crossing:
            print(f"  {a} below {b}")

    below = {}
    for a, b in order:
        below.setdefault(b, []).append(a)
    print(f"\nbelow {VALID}:")
    for c in sorted(below.get(VALID, [])):
        print(f"  {c}")
    print(f"below {INVALID}: {len(below.get(INVALID, []))} states")

    print()
    for p in sorted(args.out.rglob(f"*{tag}*")):
        print(f"  {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())