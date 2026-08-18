"""
build_filetype.py
=================
Builds the EU File type resource: the concept set, the background theory,
the TPTP axioms, and the profile entry.

    python build_filetype.py --table vocabularies/eu-file-type/filetypes-skos-ap-act.rdf \\
                             --out problems

Why this resource exists in the suite
-------------------------------------
The other two resources publish an order and leave its reading open.  This
one publishes no order at all: every one of its concepts is a top concept of
the scheme, and the table contains no skos:broader, no skos:related, and no
mapping relation between its own concepts.  So nom is not a reading the
profile chooses among several.  It is the only sort with anything to bind,
and the order operators are rejected at drafting time because the resource
supports no comparison beyond identity.

That makes the table the clearest case of the paper's claim that the sort
belongs to the binding rather than to the operand.  odrl:fileFormat is not
a nominal operand: bound to a registry that published a subtype relation it
would be taxonomic.  Bound here it is nominal, and the publisher decided
that, not the profile.

What the table publishes and this resource does not read
--------------------------------------------------------
Three kinds of thing are left out, each for a stated reason.

Eleven boolean flags -- euvoc:isDocumentFormat, isImageFormat, isTextual,
isArchiveFormat, isCompressedFormat, isStructuredFormat, isTabularFormat,
isGeographicalFormat, isAudioFormat, isVideoFormat, isPackageFormat.  The
table therefore does classify its formats: thirty-six are document formats,
twenty-one image formats.  But it records the classification as attributes
of a concept, not as concepts related by an order.  Reading them as an order
would require inventing a concept for each class, which is the fabrication
this paper argues against: the authority had the option of publishing
skos:broader and did not take it.

Two dcterms:isReplacedBy assertions, FMX2 by FMX3 and FMX3 by FMX4.  This is
supersession between versions of Formex, not identity: the three are
different formats and a document in one is not a document in another.
Encoding them as a bidirectional pair, the way a genuine alias would be
encoded, would make antisymmetry identify three distinct formats.  So the
relation stays out, and a pair of constraints naming two of them is Unknown,
which is what a resource that says only "this one came later" supports.

Deprecation.  Twenty-two concepts carry owl:deprecated with an end date.
They stay in the concept set, since a policy written last year may name one
and the grounding has to resolve it; the deprecation is recorded in the
resource file as an annotation and takes no part in the order.

Source
------
EU Vocabularies, File type authority table, SKOS_AP_ACT distribution.
Governed by the Interinstitutional Metadata and Formats Committee, maintained
by the Publications Office of the European Union.  Licensed CC BY 4.0, so the
slice below is a permitted derivative provided the attribution stands.
"""

import argparse
import re
import sys
from pathlib import Path

try:
    from rdflib import Graph, Namespace, URIRef, RDF, OWL, SKOS
except ImportError:
    print("needs rdflib: uv add rdflib", file=sys.stderr)
    raise

FT = Namespace("http://publications.europa.eu/resource/authority/file-type/")
EUVOC = Namespace("http://publications.europa.eu/ontology/euvoc#")
DCT = Namespace("http://purl.org/dc/terms/")
SCHEME = URIRef("http://publications.europa.eu/resource/authority/file-type")

# The flags that classify a format without relating it to anything.  Listed
# so the generator can report how many it saw rather than leaving the reader
# to trust the docstring.
FORMAT_FLAGS = ["isArchiveFormat", "isAudioFormat", "isCompressedFormat",
                "isDocumentFormat", "isGeographicalFormat", "isImageFormat",
                "isPackageFormat", "isStructuredFormat", "isTabularFormat",
                "isTextual", "isVideoFormat"]


def local(u) -> str:
    return str(u).rsplit("/", 1)[-1]


def slug(code: str) -> str:
    """TPTP constant for a file type code.

    The codes are already unique, ASCII and short: PDFA1A, TAR_GZ, 7Z.  Only
    two adjustments are needed.  TPTP constants must not start with a digit,
    so 7Z becomes ft_7z under the prefix.  And the prefix keeps file types
    apart from concepts of the other resources in a shared vocabulary.
    """
    return "ft_" + re.sub(r"[^a-z0-9_]", "_", code.lower())


def parse(path: Path):
    """Concepts, English labels, and the relations deliberately not read.

    Returns (concepts, labels, deprecated, replaced_by, flag_counts).  The
    last two are reported rather than used: the generator prints what it
    declined to encode, so that the resource's emptiness is visibly a
    property of the table and not of the reader.
    """
    g = Graph()
    g.parse(path, format="xml")

    concepts = sorted(local(s) for s in g.subjects(SKOS.inScheme, SCHEME))

    labels = {}
    for s, o in g.subject_objects(SKOS.prefLabel):
        if str(s).startswith(str(FT)) and getattr(o, "language", None) == "en":
            labels[local(s)] = str(o)

    deprecated = sorted(local(s) for s, o in g.subject_objects(OWL.deprecated)
                        if str(o).lower() == "true"
                        and str(s).startswith(str(FT)))

    replaced_by = sorted((local(s), local(o))
                         for s, o in g.subject_objects(DCT.isReplacedBy)
                         if str(s).startswith(str(FT)))

    flags = {}
    for name in FORMAT_FLAGS:
        n = sum(1 for _ in g.subject_objects(EUVOC[name]))
        if n:
            flags[name] = n

    # The claim the whole binding rests on, checked rather than assumed.
    order_predicates = {
        "skos:broader": len(list(g.subject_objects(SKOS.broader))),
        "skos:narrower": len(list(g.subject_objects(SKOS.narrower))),
        "skos:related": len(list(g.subject_objects(SKOS.related))),
        "skos:exactMatch": len(list(g.subject_objects(SKOS.exactMatch))),
        "skos:broadMatch": len(list(g.subject_objects(SKOS.broadMatch))),
    }

    version = str(g.value(SCHEME, OWL.versionInfo) or "unknown")
    return concepts, labels, deprecated, replaced_by, flags, order_predicates, version


def resource_ttl(concepts, labels, deprecated, meta) -> str:
    head = [
        "# EU File type: the concepts the authority publishes, and no order.",
        "#",
        "# The table relates none of its concepts to any other.  Every one is",
        "# a top concept of the scheme; there is no skos:broader, narrower,",
        "# related, or mapping relation between them.  This file therefore",
        "# has no order assertions, and that is a property of the table.",
        "#",
        "# The table does classify its formats, through boolean attributes",
        "# such as euvoc:isDocumentFormat.  Those are not read here: a class",
        "# recorded as an attribute is not a concept, and turning it into one",
        "# would add an order the authority chose not to publish.",
        "#",
        "# Two formats are marked as replacing earlier ones (Formex 2, 3, 4).",
        "# Supersession between versions is not identity, so it is not read",
        "# as an order assertion either.",
        "#",
        f"# Source    : {meta['source']}",
        f"# Version   : {meta['version']}",
        f"# VersionIRI: {meta['version_iri']}",
        f"# Published : {meta['published']}",
        f"# Retrieved : {meta['retrieved']}",
        f"# Licence   : {meta['licence']}",
        f"# Governance: {meta['governance']}",
        "",
        "@prefix ft:      <http://publications.europa.eu/resource/authority/file-type/> .",
        "@prefix odrlkb:  <https://w3id.org/odrl-kb/eu-file-type#> .",
        "@prefix dcat:    <http://www.w3.org/ns/dcat#> .",
        "@prefix dcterms: <http://purl.org/dc/terms/> .",
        "@prefix owl:     <http://www.w3.org/2002/07/owl#> .",
        "@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .",
        "",
        "<https://w3id.org/odrl-kb/eu-file-type> a dcat:Dataset ;",
        '    dcterms:title "EU File type, concept set"@en ;',
        f"    dcterms:source <{meta['version_iri']}> ;",
        f'    dcterms:license <{meta["licence_uri"]}> ;',
        f"    odrlkb:conceptCount {len(concepts)} ;",
        "    odrlkb:orderAssertionCount 0 .",
        "",
    ]
    body = []
    for c in concepts:
        body.append(f"odrlkb:{slug(c)[3:]} a odrlkb:FileType ;")
        if labels.get(c):
            body.append(f'    rdfs:label "{labels[c]}"@en ;')
        if c in deprecated:
            body.append("    owl:deprecated true ;")
        body.append(f"    dcterms:identifier ft:{c} .")
        body.append("")
    return "\n".join(head + body)


def background_ttl(meta) -> str:
    return f"""\
# Background theory for the EU File type resource: empty.
#
# The table asserts no disjointness and no distinctness between its formats.
# It does not, for instance, say that a PDF/A-1a file is not a PDF, nor that
# it is one.  With this theory in force, two constraints naming different
# formats are Unknown unless they name the same one.
#
# At nom the background theory carries more of a verdict than it does at the
# other sorts, because there is no order for the resource to contribute.
# Whatever separates two formats here was declared by the parties, and the
# certificate marks it withdrawable.  That is the honest position: the
# authority lists formats and says nothing about how they relate.
#
# Source: {meta['version_iri']}

@prefix bt:      <https://w3id.org/odrl-kb/background#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

<https://w3id.org/odrl-kb/eu-file-type/empty> a bt:BackgroundTheory ;
    dcterms:title "No declared distinctness or disjointness"@en ;
    bt:appliesTo <https://w3id.org/odrl-kb/eu-file-type> ;
    bt:assertionCount 0 .
"""


def declared_ttl(pair, meta) -> str:
    a, b = pair
    return f"""\
# Background theory for the EU File type resource: one distinctness.
#
# The parties declare that these two formats are different.  The table does
# not: it lists both and relates them in no way.  A verdict resting on this
# assertion is the parties' and can be reopened by withdrawing it.
#
# Source: {meta['version_iri']}

@prefix ft:      <http://publications.europa.eu/resource/authority/file-type/> .
@prefix bt:      <https://w3id.org/odrl-kb/background#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

<https://w3id.org/odrl-kb/eu-file-type/declared> a bt:BackgroundTheory ;
    dcterms:title "One declared distinctness"@en ;
    bt:appliesTo <https://w3id.org/odrl-kb/eu-file-type> ;
    bt:generatedBy bt:PartyDeclaration ;
    bt:assertionCount 1 .

ft:{a} bt:distinctFrom ft:{b} .
"""


def axioms(concepts) -> str:
    """The resource contributes no formulae.

    A TPTP file with no axioms is still the right artefact: the problems
    include it, and its emptiness is what they rest on.  The constants are
    declared by the problems that name them, since nothing here asserts
    anything about any of them.
    """
    return (
        "% EU File type: no order assertions.\n"
        "%\n"
        "% The authority publishes 228 formats and relates none of them.\n"
        "% This file is empty by construction, not by omission, and the\n"
        "% problems that include it rest on that emptiness: at nom a verdict\n"
        "% comes from the constraints and from what the parties declared.\n"
        "%\n"
        f"% Concepts in the resource: {len(concepts)}\n"
        "% Order assertions: 0\n"
        "% Disjointness assertions: 0\n"
    )


def declared_axioms(pair) -> str:
    a, b = pair
    return (
        "% Background theory: one distinctness, declared by the parties.\n"
        "% The table publishes nothing that separates these two formats.\n"
        "\n"
        f"fof(bt_{slug(a)}_distinct_{slug(b)}, axiom,\n"
        f"    {slug(a)} != {slug(b)}).\n"
    )


def profile_ttl() -> str:
    return """\
# Profile entry for odrl:fileFormat over the EU File type table.
#
# The sort is nom, and here that is not a choice among readings.  The table
# publishes no order, so identity is the only comparison it supports, and
# isA, isPartOf and hasPart are rejected before any resource is consulted.
#
# Bound to a registry that published a subtype relation, the same operand
# would be taxonomic.  The sort belongs to the binding.

@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix vrep: <https://w3id.org/odrl-verdict-report#> .
@prefix ex:   <https://w3id.org/odrl-kb/profile/> .

ex:b-fileformat a vrep:OperandBinding ;
    vrep:leftOperand odrl:fileFormat ;
    vrep:sort vrep:nom ;
    vrep:resource <https://w3id.org/odrl-kb/eu-file-type> ;
    vrep:backgroundTheory <https://w3id.org/odrl-kb/eu-file-type/empty> ;
    vrep:grounding vrep:sliceMembership .
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--table", required=True, type=Path,
                    help="the SKOS_AP_ACT distribution (it carries labels)")
    ap.add_argument("--declare-distinct", nargs=2, metavar=("A", "B"),
                    default=None,
                    help="also emit a background theory declaring two "
                         "formats distinct, for the stability pair")
    ap.add_argument("--retrieved", default="2026-08-18")
    ap.add_argument("--tag", default="filetype")
    ap.add_argument("--out", default="problems", type=Path)
    args = ap.parse_args()

    (concepts, labels, deprecated, replaced_by,
     flags, order_predicates, version) = parse(args.table)

    if not concepts:
        print("no concepts found; is this the right distribution?",
              file=sys.stderr)
        return 1

    total_order = sum(order_predicates.values())
    if total_order:
        print("the table publishes relations after all:", file=sys.stderr)
        for k, v in order_predicates.items():
            if v:
                print(f"  {k}: {v}", file=sys.stderr)
        print("the nom binding assumed none; re-read before continuing.",
              file=sys.stderr)
        return 1

    meta = {
        "source": "EU Vocabularies, File type authority table, SKOS_AP_ACT",
        "version": version,
        "version_iri":
            f"http://publications.europa.eu/resource/authority/file-type/{version}",
        "published": "2026-07-15",
        "retrieved": args.retrieved,
        "licence": "Creative Commons Attribution 4.0 International",
        "licence_uri": "http://creativecommons.org/licenses/by/4.0/",
        "governance": "Interinstitutional Metadata and Formats Committee; "
                      "Publications Office of the European Union",
    }

    for d in ("resources", "background", "axioms"):
        (args.out / d).mkdir(parents=True, exist_ok=True)
    tag = args.tag

    (args.out / "resources" / f"{tag}.ttl").write_text(
        resource_ttl(concepts, labels, deprecated, meta), encoding="utf-8")
    (args.out / "background" / f"{tag}-empty.ttl").write_text(
        background_ttl(meta), encoding="utf-8")
    (args.out / "axioms" / f"EUFT-{tag}.ax").write_text(
        axioms(concepts), encoding="utf-8")
    (args.out / "resources" / f"profile-{tag}.ttl").write_text(
        profile_ttl(), encoding="utf-8")

    if args.declare_distinct:
        a, b = args.declare_distinct
        missing = [x for x in (a, b) if x not in concepts]
        if missing:
            print(f"not in the table: {', '.join(missing)}", file=sys.stderr)
            return 1
        (args.out / "background" / f"{tag}-declared.ttl").write_text(
            declared_ttl((a, b), meta), encoding="utf-8")
        (args.out / "axioms" / f"EUFT-{tag}-declared.ax").write_text(
            declared_axioms((a, b)), encoding="utf-8")

    print(f"{len(concepts)} concepts, 0 order assertions, "
          f"0 disjointness assertions")
    print(f"{len(labels)} English labels, {len(deprecated)} deprecated")
    print("\nchecked absent, which is what the nom binding rests on:")
    for k, v in order_predicates.items():
        print(f"  {k:18s} {v}")

    print("\npublished but not read, each for a reason in the header:")
    print(f"  format flags       {sum(flags.values())} assertions "
          f"across {len(flags)} attributes (classification without concepts)")
    for a, b in replaced_by:
        print(f"  isReplacedBy       {a} by {b} (supersession, not identity)")

    print()
    for p in sorted(args.out.rglob(f"*{tag}*")):
        print(f"  {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())