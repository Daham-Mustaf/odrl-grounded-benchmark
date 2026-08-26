"""
build_dpvloc.py
===============
Builds the DPV Locations resource: the concept set, the containment order,
the identity assertions, the background theory, the TPTP axioms, and the
profile entry.

    python build_dpvloc.py --loc vocabularies/dpv-loc-2.3/loc.ttl \\
                           --out problems

Why this resource is in the suite
----------------------------------
It is the second resource bound to odrl:spatial, and it is bound at the same
sort as the first.  GeoNames and DPV LOC are different files, published by
different bodies, on different principles, and a profile can name either one
for the same operand.  What the operand means is therefore not a property of
the operand: it is what the binding says, which is the claim of Section 4.1
stated as two profiles rather than as an argument.

The two resources also have opposite shapes, and the certificates show it.
DPV purposes runs six levels deep, so a Compatible there may cite six order
assertions and an instance of transitivity.  LOC is two levels deep and
nearly five thousand assertions wide: almost every verdict cites one
assertion and no transitivity at all.  Depth and breadth are properties of
what an authority chose to publish, not of the semantics.

One predicate, five relations
------------------------------
The file uses skos:broader for five different things, and separating them is
the whole of the boundary decision below.  The counts are measured, not
estimated, and the generator re-measures them on every run.

   4786  location -> location             containment       READ
    177  country  -> union                membership        READ by juris
    255  location -> dpv: class           typing            not read
  63073  inverse  -> location             complement        not read

The last is counted from skos:narrower, which is how the file writes it:
loc:non-IE skos:narrower loc:AD.  The other three are counted from
skos:broader.  The extension also publishes 30 identity pairs, written as
60 directed skos:sameAs assertions.

The typing edges are the plainest case.  loc:AD skos:broader dpv:Country
says Andorra is a country; it does not say Andorra lies inside a region
called Country.  Reading it as containment would put a class into the order
alongside the places, and isPartOf would then have an answer for a question
about kinds.

The membership edges are the subtle case.  Germany is a member of the EU;
Bavaria is a part of Germany.  Both are written skos:broader and they are
not the same relation: a union admits and expels members while its parts
stay where they are, and the file records six membership sets for the EU
across time for exactly that reason.  Reading both as containment would put
two relations into one sort, which is the error this paper is about.

The complement edges are the case the paper treats at length.  loc:non-IE
has skos:narrower to every country but Ireland, so loc:AD skos:broader
loc:non-IE says Andorra belongs to the set of jurisdictions other than
Ireland.  That is membership of a complement, and no ODRL operator reads a
complement over an order.  The vocabulary's own solution is instructive:
rather than assume completeness and negate, the publisher enumerated 249
complement concepts by hand.  A resource that has to enumerate a complement
is a resource that cannot express one.

Identity
--------
The file also publishes 57 skos:sameAs pairs.  ISO 3166 assigns some places
both a country code and a subdivision code, TF and FR-TF for the French
Southern Territories, and the extension records that these denote the same
place.  This is the only resource in the suite whose identities come from
the authority: BCP 47's are a registry rule the profile applies, and the EU
table's isReplacedBy is supersession rather than identity.  Each pair is
emitted as two order assertions in opposite directions, which antisymmetry
collapses, so eq over either code is the same constraint.

What the publisher says about the reading
------------------------------------------
Section 1.2 of the specification states that the SKOS properties are
"bidirectional and transitive".  SKOS defines skos:broader as neither: it is
not declared transitive, skos:broaderTransitive is the transitive form, and
broader and narrower are inverses rather than one bidirectional property.
The intended reading is therefore in the prose and not in the file, which is
the situation this paper's profiles exist to correct.  The reading is not
wrong; it is simply not something a consumer of the RDF can recover.

Source and licence
-------------------
Locations extension of the Data Privacy Vocabulary, version 2.3, published
by the W3C Data Privacy Vocabularies and Controls Community Group.

The file carries dct:license <https://www.w3.org/copyright/document-license-2023/>,
the W3C Document License, which permits verbatim redistribution and does not
permit derivative works.  The slice this generator emits is a derivative.
The same licence applies to the DPV purposes module used elsewhere in the
suite.  Resolve this before publishing the artefact.
"""

import argparse
import sys
from pathlib import Path

try:
    from rdflib import Graph, Namespace, URIRef, RDF, OWL, SKOS
except ImportError:
    print("needs rdflib: uv add rdflib", file=sys.stderr)
    raise

DPV = Namespace("https://w3id.org/dpv#")
LOC = Namespace("https://w3id.org/dpv/loc#")

# LOC writes its identity assertions with skos:sameAs, which SKOS does not
# define; owl:sameAs is the term with that meaning.  Both are read, so the
# generator keeps working when the vocabulary is corrected, and it reports
# which one it found.
SKOS_SAMEAS = URIRef("http://www.w3.org/2004/02/skos/core#sameAs")

LOCATIONS_SCHEME = LOC["locations-classes"]

# The counts the resource header and the paper quote.  If the file changes,
# the generator stops rather than emitting a description that is no longer
# true of what it read.
EXPECT = {
    "containment": 4786,
    "typing":       255,
    "membership":   177,
    "complement": 63073,
    "identity":      30,
}


def local(u) -> str:
    return str(u).rsplit("#", 1)[-1]


PREFIX = "loc_"


def slug(code: str) -> str:
    return PREFIX + code.lower().replace("-", "_")


def bare(code: str) -> str:
    """The slug without the namespace prefix, for the Turtle serialisation."""
    return slug(code)[len(PREFIX):]


def classify(g):
    """Partition the skos:broader edges by what they relate.

    Returns (containment, typing, membership, complement, other), each a
    sorted list of (subject-code, object-code) or (subject-code, object-IRI).
    The partition is by the type of the object, since the predicate is the
    same in every case and the subject is a location in every case.

    Both containment and membership are returned.  Which of them a profile
    reads is the profile's decision, not this function's: see --read.
    """
    containment, typing, membership, complement, other = [], [], [], [], []

    def is_a(n, cls):
        return (n, RDF.type, cls) in g

    for s, o in g.subject_objects(SKOS.broader):
        if not str(s).startswith(str(LOC)):
            continue
        if str(o).startswith(str(DPV)):
            typing.append((local(s), str(o)))
        elif is_a(o, DPV.SupraNationalUnion) or is_a(o, DPV.EconomicUnion):
            membership.append((local(s), local(o)))
        elif is_a(o, DPV.Country) or is_a(o, DPV.Region) or is_a(o, DPV.City):
            containment.append((local(s), local(o)))
        else:
            other.append((local(s), str(o)))

    # The complement is written narrower only: loc:non-IE skos:narrower
    # loc:AD.  Every other relation is written both ways, so reading
    # broader alone loses nothing the profiles take.
    for s_, o_ in g.subject_objects(SKOS.narrower):
        if is_a(s_, DPV.InverseJurisdiction):
            complement.append((local(s_), local(o_)))

    return (sorted(containment), sorted(typing), sorted(membership),
            sorted(complement), sorted(other))


def identities(g):
    """The identity pairs, deduplicated and ordered, and the predicate used.

    ISO 3166 assigns some places both a country code and a subdivision code,
    TF and FR-TF for the French Southern Territories, and the extension
    records that the two denote one place.  Section 1.1 of the specification
    states the intent.

    The file writes this with skos:sameAs, which SKOS does not define, so a
    consumer validating against the SKOS vocabulary discards all of it.  Both
    that term and owl:sameAs are read here, and which was found is reported,
    so the generator survives a correction to the vocabulary without an edit.
    """
    seen, found = set(), set()
    for pred in (SKOS_SAMEAS, OWL.sameAs):
        for s, o in g.subject_objects(pred):
            if not (str(s).startswith(str(LOC)) and str(o).startswith(str(LOC))):
                continue
            seen.add(tuple(sorted((local(s), local(o)))))
            found.add(str(pred))
    return sorted(seen), sorted(found)


def classes(concepts, ident):
    """Equivalence classes of codes under the identity pairs.

    Needed by the ISO distinctness rule below: the rule separates areas, and
    two codes for one area are not two areas.  Union-find over the pairs,
    with each class keyed by its least code.
    """
    parent = {c: c for c in concepts}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in ident:
        if a in parent and b in parent:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[max(ra, rb)] = min(ra, rb)

    out = {}
    for c in concepts:
        out.setdefault(find(c), []).append(c)
    return {k: sorted(v) for k, v in out.items()}


def concepts_and_labels(g):
    """Places in the locations scheme, with their English labels.

    The inverse-jurisdiction concepts are in their own scheme and are not
    collected: they are not places, and nothing below reads them.
    """
    concepts, labels, kinds = set(), {}, {}
    for s in g.subjects(SKOS.inScheme, LOCATIONS_SCHEME):
        if not str(s).startswith(str(LOC)):
            continue
        code = local(s)
        concepts.add(code)
        for o in g.objects(s, SKOS.prefLabel):
            if getattr(o, "language", None) == "en":
                labels[code] = str(o)
        for cls in ("Country", "Region", "City"):
            if (s, RDF.type, DPV[cls]) in g:
                kinds[code] = cls
                break
    return sorted(concepts), labels, kinds


def depth(containment):
    """Longest chain in the containment order, and one witness.

    Reported rather than assumed: the shape of the order is a fact about the
    resource and it is what the certificates will reflect.
    """
    parents = {}
    for a, b in containment:
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


def resource_ttl(concepts, labels, kinds, order, ident, meta, mode) -> str:
    reads = {
        "geo": [
            "# DPV Locations, geographic reading: containment only.",
            "#",
            "# The file uses skos:broader for five relations.  This resource",
            "# reads the two that are containment, region within country and",
            "# country within country, and reads neither the typing edges to",
            "# dpv:Country, nor the membership edges to supranational unions,",
            "# nor the complement edges to inverse jurisdictions.",
            "#",
            "# Excluding membership makes the unions unusable under this",
            "# reading: isPartOf EU is not grounded here.  That is a property",
            "# of the reading and not a defect in the file, and the",
            "# jurisdictional reading below admits it.",
        ],
        "juris": [
            "# DPV Locations, jurisdictional reading: containment and union",
            "# membership.",
            "#",
            "# The same file as the geographic reading, with the membership",
            "# edges to supranational unions read as containment as well.",
            "# Germany within the EU is then an order assertion, and",
            "# isPartOf EU has an answer.",
            "#",
            "# The two are not the same relation.  A union admits and expels",
            "# members while the parts of a country stay where they are, and",
            "# the extension records six membership sets for the EU across",
            "# time for that reason.  Reading them together is a decision a",
            "# profile may make for a jurisdictional purpose, since for data",
            "# transfer what matters is which rules reach a place; it is not",
            "# a claim that membership is parthood.  Pin the versioned",
            "# concept, EU27 rather than EU, if the reading must be stable.",
        ],
    }[mode]

    title = ("DPV Locations, containment slice" if mode == "geo"
             else "DPV Locations, containment and union membership slice")
    head = reads + [
        "#",
        "# The identity assertions use skos:sameAs, which SKOS does not",
        "# define.  Section 1.1 of the specification states the intent: ISO",
        "# 3166 gives some places both a country code and a subdivision code,",
        "# and the two denote one place.  They are read as identity on that",
        "# statement.  A consumer validating against the SKOS vocabulary",
        "# would discard them.",
        "#",
        f"# Source     : {meta['source']}",
        f"# Version    : {meta['version']}",
        f"# Retrieved  : {meta['retrieved']}",
        f"# Licence    : {meta['licence']}",
        f"# NOTE       : {meta['licence_note']}",
        "#",
        f"# Identity predicate   : {meta['identity_predicate']}",
        "#",
        f"# Concepts                     : {len(concepts)}",
        f"# Order assertions, published  : {len(order)}",
        f"# Identity pairs, published    : {len(ident)}",
        f"# Order assertions, encoded    : {2 * len(ident)} (two per identity pair)",
        "",
        "@prefix loc:     <https://w3id.org/dpv/loc#> .",
        "@prefix odrlkb:  <https://w3id.org/odrl-kb/dpv-loc#> .",
        "@prefix dcat:    <http://www.w3.org/ns/dcat#> .",
        "@prefix dcterms: <http://purl.org/dc/terms/> .",
        "@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .",
        "",
        f"<https://w3id.org/odrl-kb/dpv-loc-{mode}> a dcat:Dataset ;",
        f'    dcterms:title "{title}"@en ;',
        f"    dcterms:source <{meta['source_iri']}> ;",
        f"    odrlkb:conceptCount {len(concepts)} ;",
        f"    odrlkb:publishedOrderAssertionCount {len(order)} ;",
        f"    odrlkb:identityPairCount {len(ident)} ;",
        f"    odrlkb:encodedOrderAssertionCount {2 * len(ident)} .",
        "",
    ]

    body = []
    for c in concepts:
        body.append(f"odrlkb:{bare(c)} a odrlkb:{kinds.get(c, 'Place')} ;")
        if labels.get(c):
            body.append(f'    rdfs:label "{labels[c]}"@en ;')
        body.append(f"    dcterms:identifier loc:{c} .")
        body.append("")
    if mode == "juris":
        body.append("# Unions, read as containers under this reading only.")
        body.append("")
        for u in sorted({b for _, b in order} - set(concepts)):
            body.append(f"odrlkb:{bare(u)} a odrlkb:Union ;")
            body.append(f"    dcterms:identifier loc:{u} .")
            body.append("")
    body.append("# The order, as the extension publishes it.")
    for a, b in order:
        body.append(f"odrlkb:{bare(a)} odrlkb:within odrlkb:{bare(b)} .")
    body.append("")
    body.append("# Identity: one place, two ISO codes.  Not an order")
    body.append("# assertion in the file; two of them in the encoding.")
    for a, b in ident:
        body.append(f"odrlkb:{bare(a)} odrlkb:sameAs odrlkb:{bare(b)} .")

    return "\n".join(head + body)


def background_ttl(meta) -> str:
    return f"""\
# Background theory for the DPV Locations resource: empty.
#
# The extension asserts no disjointness between places and no distinctness
# between the codes it lists.  Two constraints naming different countries
# are therefore satisfiable together unless a party declares them apart, and
# the certificate for such a verdict names the declaration.
#
# The absence is worth stating plainly, because the file looks as though it
# supplies distinctness and does not.  Every country has an inverse
# jurisdiction concept, and non-IE is narrower than every country but
# Ireland.  A reader may take that as saying the countries are pairwise
# distinct.  It does not: it says which concepts belong to a complement, and
# a structure identifying two countries satisfies those memberships as well.
#
# Distinctness is available as a generated rule rather than as an assertion
# in the file: see the iso theory, which the parties may adopt on the
# strength of ISO 3166 assigning one code per area.  Adopting it is their
# decision and the certificate records it as theirs.
#
# Source: {meta['source_iri']}

@prefix bt:      <https://w3id.org/odrl-kb/background#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

<https://w3id.org/odrl-kb/dpv-loc/empty> a bt:BackgroundTheory ;
    dcterms:title "No declared distinctness or disjointness"@en ;
    bt:appliesTo <https://w3id.org/odrl-kb/dpv-loc> ;
    bt:assertionCount 0 .
"""


def iso_ttl(reps, multi, meta) -> str:
    """Background theory generated from the ISO 3166 one-code-per-area rule.

    ISO 3166 assigns one code to an area, so two country codes name two
    areas.  That licenses pairwise distinctness, and the rule is the
    parties', not the extension's: the file states no distinctness anywhere.

    The quotient matters.  The extension also records that some places carry
    two codes, TF and FR-TF, and those are one area with two names.
    Distinctness therefore separates equivalence classes under the identity
    pairs and not codes, or the theory would contradict the identity
    assertions and every verdict over it would be vacuous.
    """
    n = len(reps)
    return f"""\
# Background theory for the DPV Locations resource: ISO distinctness.
#
# Generated from the rule that ISO 3166 assigns one code per area, so that
# two areas listed by the extension are two places.  The extension asserts
# none of this; the rule is the parties', and a verdict resting on it is
# withdrawable by abandoning the rule.
#
# The distinctness is between areas, not between codes.  The extension
# records {multi} places under two codes, a country code and a
# subdivision code for the same area, and those pairs are identified rather
# than separated.  Distinctness is asserted between the classes those
# identities induce.
#
# Classes: {n}
# Source : {meta['source_iri']}

@prefix bt:      <https://w3id.org/odrl-kb/background#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

<https://w3id.org/odrl-kb/dpv-loc/iso> a bt:BackgroundTheory ;
    dcterms:title "Pairwise distinctness of ISO 3166 areas"@en ;
    bt:appliesTo <https://w3id.org/odrl-kb/dpv-loc> ;
    bt:generatedBy bt:RegistryUniquenessRule ;
    bt:rule "ISO 3166 assigns one code per area; codes identified by the extension name one area"@en ;
    bt:classCount {n} .
"""


def declared_ttl(pair, meta) -> str:
    a, b = pair
    return f"""\
# Background theory for the DPV Locations resource: one distinctness.
#
# The parties declare that these two places are different.  The extension
# does not: it lists both and separates them in no way.  A verdict resting
# on this assertion is the parties' and can be reopened by withdrawing it.
#
# Source: {meta['source_iri']}

@prefix loc:     <https://w3id.org/dpv/loc#> .
@prefix bt:      <https://w3id.org/odrl-kb/background#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

<https://w3id.org/odrl-kb/dpv-loc/declared> a bt:BackgroundTheory ;
    dcterms:title "One declared distinctness"@en ;
    bt:appliesTo <https://w3id.org/odrl-kb/dpv-loc> ;
    bt:generatedBy bt:PartyDeclaration ;
    bt:assertionCount 1 .

loc:{a} bt:distinctFrom loc:{b} .
"""


def axioms(order, ident, meta, mode) -> str:
    what = ("region within country and country within country"
            if mode == "geo"
            else "region within country, country within country, and country "
                 "within union")
    lines = [
        f"% DPV Locations: the order, {mode} reading.",
        "%",
        f"% {what[0].upper()}{what[1:]}.",
        "% The edges the reading does not take are named in the resource",
        "% header, with what each of them relates.",
        "%",
        "% The identity assertions below are this encoding's, not the",
        "% extension's: it publishes identity, and identity is written here",
        "% as two order assertions which antisymmetry collapses.  They are",
        "% named res_x_same_y so that a refutation citing one is visibly",
        "% resting on identity rather than on published containment.",
        "%",
        f"% Order assertions, published : {len(order)}",
        f"% Identity pairs, published   : {len(ident)}",
        f"% Order assertions, encoded   : {2 * len(ident)}",
        f"% Source                      : {meta['source_iri']}",
        "",
    ]
    for a, b in order:
        lines.append(f"fof(res_{slug(a)}_within_{slug(b)}, axiom,")
        lines.append(f"    kge_leq({slug(a)}, {slug(b)})).")
        lines.append("")
    if ident:
        lines.append("% Identity: one place under two ISO codes.")
        lines.append("")
        for a, b in ident:
            lines.append(f"fof(res_{slug(a)}_same_{slug(b)}, axiom,")
            lines.append(f"    kge_leq({slug(a)}, {slug(b)})).")
            lines.append("")
            lines.append(f"fof(res_{slug(b)}_same_{slug(a)}, axiom,")
            lines.append(f"    kge_leq({slug(b)}, {slug(a)})).")
            lines.append("")
    return "\n".join(lines)


def iso_axioms(reps) -> str:
    """The registry rule, stated but not instantiated.

    The rule licenses pairwise distinctness over 249 areas, which is 30876
    inequations.  Instantiating all of them in every problem would bury the
    one assertion a refutation actually uses, and TPTP's $distinct is a
    typed-language construct that a first-order prover reads as an ordinary
    predicate, constraining nothing.

    So the file states the rule, lists the areas it ranges over, and leaves
    the instances to the problems.  A problem naming two areas carries the
    one inequation between them, named bt_, and an unsat core then cites the
    rule instance the verdict rests on rather than a term the prover
    ignored.  The SMT encoding has always worked this way; this makes the
    two agree.
    """
    listing = "\n".join(
        "% " + ", ".join(reps[i:i + 12]) for i in range(0, len(reps), 12))
    return (
        "% Background theory: the ISO 3166 uniqueness rule.\n"
        "%\n"
        "% ISO 3166 assigns one code to an area, so two areas listed by the\n"
        "% extension are two places.  The extension asserts none of this: the\n"
        "% rule is the parties', and a verdict resting on an instance of it is\n"
        "% withdrawable by abandoning the rule.\n"
        "%\n"
        "% Distinctness is between areas rather than codes.  Where the\n"
        "% extension records two codes for one area, a country code and a\n"
        "% subdivision code, the area appears once below under its country\n"
        "% code; a rule applied to the codes would contradict the identity\n"
        "% the extension publishes.\n"
        "%\n"
        "% The rule is stated here and instantiated by the problems.  A\n"
        "% problem naming two of the areas below carries the inequation\n"
        "% between them as a bt_ assertion, so that a refutation cites the\n"
        "% instance it used.\n"
        "%\n"
        f"% Areas: {len(reps)}\n"
        "%\n"
        f"{listing}\n"
    )


def iso_instance(a: str, b: str) -> str:
    """The inequation a problem carries when it adopts the registry rule."""
    return (f"fof(bt_{slug(a)}_distinct_{slug(b)}, axiom,\n"
            f"    {slug(a)} != {slug(b)}).")


def declared_axioms(pair) -> str:
    a, b = pair
    return (
        "% Background theory: one distinctness, declared by the parties.\n"
        "% The extension publishes nothing that separates these places.\n"
        "\n"
        f"fof(bt_{slug(a)}_distinct_{slug(b)}, axiom,\n"
        f"    {slug(a)} != {slug(b)}).\n"
    )


def profile_ttl(mode) -> str:
    """Profile entry for odrl:spatial over DPV Locations.

    Two of these are emitted, differing only in which published relation the
    resource reads.  Both bind the same operand at the same sort, and both
    are correct readings of the same file for different purposes.
    """
    body = {
        "geo": (
            "geo", "the containment slice",
            "# The resource is containment only.  A constraint whose right\n"
            "# operand is a supranational union does not ground under this\n"
            "# profile: the union edges are membership, and this reading does\n"
            "# not take them as containment.",
        ),
        "juris": (
            "juris", "the jurisdictional slice",
            "# The resource is containment together with union membership,\n"
            "# read as jurisdictional containment.  isPartOf EU has an answer\n"
            "# here and does not under the geographic profile.  Neither is\n"
            "# the correct reading of the file: they are two readings, and\n"
            "# the profile is where a party says which one it means.",
        ),
    }[mode]
    tag, title, note = body
    return f"""\
# Profile entry for odrl:spatial over DPV Locations, {title}.
#
# The sort is mer, the same sort the GeoNames profile declares for the same
# operand, and the same sort the other DPV Locations profile declares.  What
# differs between the three is the resource: which file, and which of the
# relations in that file the binding reads.  That is what it means for the
# meaning to belong to the binding rather than to the operand.
#
{note}

@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix vrep: <https://w3id.org/odrl-verdict-report#> .
@prefix ex:   <https://w3id.org/odrl-kb/profile/> .

ex:b-spatial-dpvloc-{tag} a vrep:OperandBinding ;
    vrep:leftOperand odrl:spatial ;
    vrep:sort vrep:mer ;
    vrep:resource <https://w3id.org/odrl-kb/dpv-loc-{tag}> ;
    vrep:backgroundTheory <https://w3id.org/odrl-kb/dpv-loc/empty> ;
    vrep:grounding vrep:sliceMembership .
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--loc", required=True, type=Path,
                    help="loc.ttl, the SKOS serialisation")
    ap.add_argument("--read", choices=("geo", "juris", "both"), default="both",
                    help="which published relations the resource reads: "
                         "containment only, containment with union "
                         "membership, or emit both readings")
    ap.add_argument("--declare-distinct", nargs=2, metavar=("A", "B"),
                    default=None,
                    help="also emit a background theory declaring two places "
                         "distinct, for the stability pair")
    ap.add_argument("--retrieved", default="2026-08-19")
    ap.add_argument("--out", default="problems", type=Path)
    ap.add_argument("--allow-count-change", action="store_true",
                    help="proceed even if the measured counts differ from "
                         "those the resource header and the paper state")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.loc, format="turtle")

    containment, typing, membership, complement, other = classify(g)
    ident, id_preds = identities(g)
    concepts, labels, kinds = concepts_and_labels(g)

    measured = {
        "containment": len(containment),
        "typing":      len(typing),
        "membership":  len(membership),
        "complement":  len(complement),
        "identity":    len(ident),
    }

    # Every one of these numbers appears in the resource header and in the
    # paper.  If the file has moved, the description would be false, so the
    # generator stops rather than writing it.
    if not args.allow_count_change:
        drift = [(k, v, EXPECT[k]) for k, v in measured.items()
                 if v != EXPECT[k]]
        if drift:
            print("the file no longer has the shape the resource describes:",
                  file=sys.stderr)
            for k, got, want in drift:
                print(f"  {k}: {got}, expected {want}", file=sys.stderr)
            print("re-read the file, update EXPECT and the paper, or pass "
                  "--allow-count-change.", file=sys.stderr)
            return 1

    if other:
        print(f"{len(other)} skos:broader edges the partition does not "
              f"classify; the resource would not describe them:",
              file=sys.stderr)
        for a, b in other[:10]:
            print(f"  {a} -> {b}", file=sys.stderr)
        return 1

    meta = {
        "source": "DPV Locations extension 2.3 (W3C DPVCG), SKOS serialisation",
        "source_iri": "https://w3id.org/dpv/2.3/loc",
        "version": str(g.value(LOC[""], OWL.versionInfo) or "2.3"),
        "retrieved": args.retrieved,
        "licence": "W3C Document License 2023",
        "licence_note": "permits verbatim redistribution, not derivatives; "
                        "this slice is a derivative and the licence is "
                        "unresolved",
        "identity_predicate": ", ".join(id_preds) or "none found",
    }

    for d in ("resources", "background", "axioms"):
        (args.out / d).mkdir(parents=True, exist_ok=True)

    modes = ("geo", "juris") if args.read == "both" else (args.read,)
    for mode in modes:
        tag = f"dpvloc-{mode}"
        order = containment if mode == "geo" else sorted(containment + membership)
        (args.out / "resources" / f"{tag}.ttl").write_text(
            resource_ttl(concepts, labels, kinds, order, ident, meta, mode),
            encoding="utf-8")
        (args.out / "axioms" / f"LOC-{tag}.ax").write_text(
            axioms(order, ident, meta, mode), encoding="utf-8")
        (args.out / "resources" / f"profile-{tag}.ttl").write_text(
            profile_ttl(mode), encoding="utf-8")
        print(f"{mode:6}  {len(order)} order assertions "
              f"({len(ident)} identity pairs, {2 * len(ident)} encoded)")

    (args.out / "background" / "dpvloc-empty.ttl").write_text(
        background_ttl(meta), encoding="utf-8")

    # ISO distinctness, between areas rather than codes.  Codes the extension
    # identifies name one area, so the rule is applied to the quotient.
    cls = classes(concepts, ident)
    multi = sum(1 for v in cls.values() if len(v) > 1)   # pass this in
    reps = sorted(k for k, v in cls.items()
                  if any(kinds.get(c) == "Country" for c in v))
    (args.out / "background" / "dpvloc-iso.ttl").write_text(
        iso_ttl(reps, multi, meta), encoding="utf-8")
    (args.out / "axioms" / "LOC-dpvloc-iso.ax").write_text(
        iso_axioms(reps), encoding="utf-8")

    if args.declare_distinct:
        a, b = args.declare_distinct
        missing = [x for x in (a, b) if x not in concepts]
        if missing:
            print(f"not in the locations scheme: {', '.join(missing)}",
                  file=sys.stderr)
            return 1
        (args.out / "background" / "dpvloc-declared.ttl").write_text(
            declared_ttl((a, b), meta), encoding="utf-8")
        (args.out / "axioms" / "LOC-dpvloc-declared.ax").write_text(
            declared_axioms((a, b)), encoding="utf-8")

    hops, witness = depth(containment)
    hops_j, witness_j = depth(sorted(containment + membership))
    print(f"\n{len(concepts)} concepts")
    print(f"longest chain, containment  : {hops} hops"
          + (f" ({' < '.join(witness)})" if witness else ""))
    print(f"longest chain, with unions  : {hops_j} hops"
          + (f" ({' < '.join(witness_j)})" if witness_j else ""))
    print(f"identity predicate          : {meta['identity_predicate']}")
    print(f"ISO areas (identity classes): {len(reps)} of "
          f"{sum(1 for c in concepts if kinds.get(c) == 'Country')} country codes")

    print("\nskos:broader, partitioned by what the object is:")
    print(f"  {len(containment):6}  containment   read by both readings")
    print(f"  {len(membership):6}  membership    read by juris only")
    print(f"  {len(typing):6}  typing        not read (object is a dpv: class)")
    print(f"  {len(complement):6}  complement    not read (no operator reads it)")

    print()
    for p in sorted(args.out.rglob("*dpvloc*")):
        print(f"  {p}")

    return 0


if __name__ == "__main__":
    sys.exit(main())