"""
build_consent.py
================
Builds the DPV consent status resource: the concept set, the order, three
declarations, the TPTP axioms, and the profile entry.

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
rests on a declaration, and the certificate says so, even
though the authority's own prose is what warrants it.

The declared set separates every state of the slice from every other.  It
rests on the DPV definitions: the module defines each state separately, in
a definition of its own, and does not say in RDF that the states are
distinct.  The definitional set separates every state below one branch from
every state below the other, and rests on the definitions of the branches.
Here the vocabulary states the intent in the definition and omits it from the
file, and adopting it follows the publisher rather than adding to it.  The
verdict is still withdrawable and the certificate still marks it: what the
definitions warrant, they do not assert.

The module boundary
-------------------
The module publishes thirteen order statements.  One, ConsentStatus below
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
until a declaration separates them.  And no identity statements.

Typing is present and is not read.  Every concept carries
rdf:type dpv:ConsentStatus, including the two mid-level concepts, so the type
names the nearest ancestor carrying rdfs:subClassOf rather than the immediate
parent.  Nothing is typed dpv:ConsentStatusValidForProcessing at all.  A
reading of isA that follows rdf:type therefore cannot satisfy the constraint
this resource exists for, whatever the state; a reading that follows the
order can.  The typing is outside the definition of a resource either way:
it relates an individual to a class, and a resource relates concepts to
concepts.

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

import declarations

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
# these numbers are in the resource header.
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
        "# distinctness between any pair; see the declarations.",
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
        f"# Order statements : {len(order)}",
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
        f"    dcterms:source <{meta['source_iri']}> .",
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
# Declarations for the DPV consent status resource: empty.
#
# This set states nothing; only the resource's statements apply.  The module
# asserts no disjointness and no distinctness.  Two constraints naming
# different states are therefore satisfiable together, and a verdict
# separating them rests on a declaration.
#
# The absence is worth stating, because the definitions read as though they
# supply it.  A state that may justify processing and a state that may not
# cannot be the same state; the module says so in prose and asserts nothing.
# See the definitional declarations.
#
# Source: {meta['source_iri']}

@prefix bind:    <https://w3id.org/odrl-kb/binding#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

<https://w3id.org/odrl-kb/dpv-consent/empty> a bind:Declarations ;
    dcterms:title "No declared distinctness or disjointness"@en ;
    bind:appliesTo <https://w3id.org/odrl-kb/dpv-consent> ;
    bind:pairCount 0 .
"""


def definitional_ttl(definitions, meta) -> str:
    """The disjointness the module's definitions warrant.

    The warrant is quoted rather than paraphrased.  Adopting these
    declarations claims the publisher already said it, and a reader deciding
    whether to accept or withdraw the premise needs the publisher's words,
    not this generator's reading of them.  The definitions are taken from the
    module at build time, so the quotation cannot drift from the file.
    """
    d_valid = definitions.get(VALID, "")
    d_invalid = definitions.get(INVALID, "")
    d_withdrawn = definitions.get("ConsentWithdrawn", "")

    return f"""\
# Declarations for the DPV consent status resource: the two branches are
# disjoint.
#
# Adopted on the strength of the module's own definitions, which are quoted
# below as bind:warrant.  One branch is defined as the states of consent that
# CAN be used as valid justifications for processing, the other as the states
# that CANNOT.  Individual states say the same again: the withdrawn state is
# defined as one that prevents consent from being further used as a valid
# state.  Nothing can lie below both branches if those definitions hold.
#
# The module asserts no owl:disjointWith, anywhere.  So the disjointness is
# stated three times in prose and carried nowhere in the file, and a consumer
# reading the RDF alone cannot recover it.
#
# What follows is a decision, not a derivation.  These declarations follow
# what the publisher wrote; the certificate still marks the premise
# withdrawable, because what the definitions warrant they do not assert, and
# a different reading can withdraw the statement and watch the verdict reopen
# as Unknown.
#
# Source: {meta['source_iri']}

@prefix dpv:     <https://w3id.org/dpv#> .
@prefix bind:    <https://w3id.org/odrl-kb/binding#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix skos:    <http://www.w3.org/2004/02/skos/core#> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .

<https://w3id.org/odrl-kb/dpv-consent/definitional> a bind:Declarations ;
    dcterms:title "The valid and invalid branches are disjoint"@en ;
    bind:appliesTo <https://w3id.org/odrl-kb/dpv-consent> ;
    bind:generatedBy bind:PublishedDefinition ;
    bind:origin bind:proseDefinition ;
    bind:pairCount 1 ;
    bind:warrant [
        bind:concept dpv:{VALID} ;
        skos:definition "{d_valid}"@en ] ,
      [
        bind:concept dpv:{INVALID} ;
        skos:definition "{d_invalid}"@en ] ,
      [
        bind:concept dpv:ConsentWithdrawn ;
        skos:definition "{d_withdrawn}"@en ] ;
    rdfs:comment "The module defines one branch as the states that can \
justify processing and the other as the states that cannot, and asserts no \
disjointness between them."@en .

dpv:{VALID} bind:disjointFrom dpv:{INVALID} .
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
        f"% Order statements : {len(order)}",
        f"% Source           : {meta['source_iri']}",
        "",
    ]
    for a, b in order:
        lines.append(f"fof(res_{slug(a)}_below_{slug(b)}, axiom,")
        lines.append(f"    kge_leq({slug(a)}, {slug(b)})).")
        lines.append("")
    return "\n".join(lines)


def _wrap(text: str, width: int = 72) -> list:
    """Wrap a definition into TPTP comment lines."""
    words, lines, cur = text.split(), [], "%   "
    for w in words:
        if len(cur) + len(w) + 1 > width:
            lines.append(cur)
            cur = "%   " + w
        else:
            cur += (" " if cur.strip("% ") else "") + w
    if cur.strip("% "):
        lines.append(cur)
    return lines


def definitional_axioms(definitions) -> str:
    """Disjointness of the two branches, on the module's own definitions.

    The order clause: nothing lies below both.  Not an
    inequation, which would separate the two mid-level concepts and leave
    their subtrees free to overlap.

    The definitions are quoted in the header.  A reader of a refutation that
    cites this axiom sees the premise's warrant beside it, and can judge
    whether the reading is right without opening the vocabulary.
    """
    v, i = slug(VALID), slug(INVALID)
    lines = [
        "% Declarations: the valid and invalid branches are disjoint.",
        "%",
        "% Adopted from the module's own definitions, quoted here:",
        "%",
        f"% {VALID}:",
    ]
    lines += _wrap(definitions.get(VALID, "(not found)"))
    lines += ["%", f"% {INVALID}:"]
    lines += _wrap(definitions.get(INVALID, "(not found)"))
    if definitions.get("ConsentWithdrawn"):
        lines += ["%", "% ConsentWithdrawn:"]
        lines += _wrap(definitions["ConsentWithdrawn"])
    lines += [
        "%",
        "% Can and cannot: nothing lies below both branches if the",
        "% definitions hold.  The module asserts no owl:disjointWith, so a",
        "% verdict resting on this axiom rests on a reading of the",
        "% definitions, and the certificate marks it withdrawable.",
        "%",
        "% Disjointness rather than distinctness: nothing below both, so no",
        "% state of consent is at once valid and invalid for processing.",
        "",
        f"fof(bg_disj_{v}_disjoint_{i}, axiom,",
        f"    ! [X] : ~ ( kge_leq(X, {v}) & kge_leq(X, {i}) )).",
        "",
    ]
    return "\n".join(lines)


def declared_ttl(members, meta) -> str:
    """Every state of the slice declared distinct from every other.

    Distinctness only.  One state may lie below another and still be a
    different state, so nothing here says that two states have nothing
    below both: that is disjointness, and the definitional set carries it
    for the two branches.  The members are all the concepts of the slice,
    written as an owl:AllDifferent, and the axioms are written from what is
    read back.
    """
    n = len(members)
    listing = "\n".join(f"            <{m}>" for m in members)
    return f"""\
# Declarations for the DPV consent status resource: declared distinctness.
#
# Every state of the slice is declared distinct from every other.  The
# module defines each state separately, in a definition of its own, and
# these definitions are what the declarations rest on.  The module does
# not state the distinctness in RDF, so a verdict resting on an instance of
# it is withdrawable by abandoning the declarations.
#
# Distinctness only.  One state may lie below another and still be a
# different state; whether nothing lies below two of them is disjointness,
# which is a different declaration (consent-definitional.ttl).
#
# The declarations are stated here and instantiated by the problems: a
# problem naming two states carries the inequation between them, so that a
# refutation cites the instance it used rather than a term standing for all
# of them.
#
# States: {n}
# Pairs : {n * (n - 1) // 2}
#
# Source: {meta['source_iri']}

@prefix bind:    <https://w3id.org/odrl-kb/binding#> .
@prefix owl:     <http://www.w3.org/2002/07/owl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .

<https://w3id.org/odrl-kb/dpv-consent/declared> a bind:Declarations ;
    dcterms:title "Pairwise distinctness of consent states"@en ;
    bind:appliesTo <https://w3id.org/odrl-kb/dpv-consent> ;
    bind:generatedBy bind:PairwiseDistinctness ;
    bind:origin bind:proseDefinition ;
    rdfs:comment "The origin rests on DPV's separate definition of each state."@en ;
    bind:scopeCondition "Distinctness between the listed states, and not disjointness: one state may lie below another and still be a different state."@en ;
    bind:pairCount {n * (n - 1) // 2} ;
    bind:states [
        a owl:AllDifferent ;
        owl:members (
{listing}
        )
    ] .
"""


def declared_axioms(names) -> str:
    """The declarations, stated but not instantiated.

    As DPV-dpv-purposes-declared.ax does: the file lists what the
    declarations range over and leaves the instances to the problems, so a
    refutation cites the inequation it used.
    """
    n = len(names)
    listing = "\n".join("% " + ", ".join(names[i:i + 6])
                        for i in range(0, n, 6))
    return (
        "% Declarations: pairwise distinctness of the consent states.\n"
        "%\n"
        "% DPV defines each state separately, in a definition of its own, and\n"
        "% does not say in RDF that the states are distinct.  The declarations\n"
        "% rest on the definitions, and a verdict resting on an instance of\n"
        "% them is withdrawable by abandoning the declarations.\n"
        "%\n"
        "% Distinctness, not disjointness: one state may lie below another and\n"
        "% still be a different state.  Disjointness is a different\n"
        "% declaration, DPV-consent-definitional.ax.\n"
        "%\n"
        "% The declarations are stated here and instantiated by the problems.\n"
        "% A problem naming two of the states below carries the inequation\n"
        "% between them as a bg_dist_ statement.\n"
        "%\n"
        f"% States: {n}\n"
        f"% Pairs : {n * (n - 1) // 2}\n"
        "%\n"
        f"{listing}\n"
    )


def profile_ttl() -> str:
    return """\
# Profile entry for a consent status operand over the DPV consent module.
#
# The sort is tax.  The module publishes a hierarchy of states, and the
# constraint a controller writes, that the status be one which may justify
# processing, is a question about that hierarchy: which states lie below the
# concept the controller's policy names.
#
# The module also types its concepts, and a profile binding this operand to
# the typing rather than to the order would answer a different question.

@prefix dpv-odrl: <https://w3id.org/dpv/mappings/odrl#> .
@prefix bind: <https://w3id.org/odrl-kb/binding#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix ex:   <https://w3id.org/odrl-kb/profile/> .

ex:b-consent-status a bind:OperandBinding ;
    rdfs:label "DPV consent status, read as kinds"@en ;
    bind:leftOperand dpv-odrl:Status ;
    bind:sort bind:tax ;
    bind:resource <https://w3id.org/odrl-kb/dpv-consent> ;
    bind:grounding bind:sliceMembership .
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--module", required=True, type=Path)
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
            print("re-read the module, update EXPECT, or pass "
                  "--allow-count-change.", file=sys.stderr)
            return 1

    for c in (VALID, INVALID):
        if c not in concepts:
            print(f"{c} is not in the module; the definitional declarations assume "
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
        definitional_ttl(definitions, meta), encoding="utf-8")
    (args.out / "axioms" / f"DPV-{tag}.ax").write_text(
        axioms(order, crossing, meta), encoding="utf-8")
    (args.out / "axioms" / f"DPV-{tag}-definitional.ax").write_text(
        definitional_axioms(definitions), encoding="utf-8")
    (args.out / "resources" / f"profile-{tag}.ttl").write_text(
        profile_ttl(), encoding="utf-8")

    # The declarations cover every state of the slice and are written as
    # RDF; the axioms are written from what is read back.
    declared = args.out / "background" / f"{tag}-declared.ttl"
    declared.write_text(
        declared_ttl([f"https://w3id.org/dpv#{c}" for c in sorted(concepts)],
                     meta), encoding="utf-8")
    names = sorted(local(m) for m in declarations.load(declared).members)
    (args.out / "axioms" / f"DPV-{tag}-declared.ax").write_text(
        declared_axioms(names), encoding="utf-8")

    hops, witness = depth(order)
    print(f"{len(concepts)} concepts, {len(order)} order statements")
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