"""
gen_bcp47.py
============
Builds the BCP 47 language resource and its background theory.

    uv run generators/gen_bcp47.py \
        --ttl        problems/resources/bcp47.ttl \
        --background problems/background/bcp47-uniqueness.ttl \
        --registry   vocabularies/bcp47-20260826/language-subtag-registry.txt \
        --out        problems/axioms

Two files out, not one
----------------------
    BCP47000-0.ax    the resource: concept membership, no order assertions
    BCP47001-0.ax    the parties' theory: 105 inequations

The split is the point.  A resource is what an authority published; the
IANA registry publishes a set of subtags and, over this slice, no relation
between them at all, so the resource file asserts membership of each
concept and nothing over them.  That emptiness of the order is what makes
isA unanswerable at nom rather than false.

The membership facts stand by decision, not habit: they document the
published tag set, they are the universe a complement operator would need
if the encodings ever relativise to one, and they are marked
measured-unused until that check is made.  Dropping them is a decision to
take explicitly after the measurement, not inside this generator.

Registry uniqueness is a rule the parties adopt.  Keeping it in its own
file is what lets a refutation say which of its premises a party may
withdraw, and it makes the withdrawal test one include line: the same
problem with and without this file is Incompatible and Unknown.

Distinctness, not disjointness
------------------------------
The previous version emitted kge_disjoint/2, which is wrong three times
over.  Disjointness says nothing lies below both, which needs an order the
nominal sort does not have.  kge_disjoint is not declared in KGE000-0.ax,
so a prover read those facts as an uninterpreted predicate and learned
nothing from them.  And they were stored one direction only, which would
have needed a symmetry axiom that does not exist.

Built-in inequality has none of those problems: symmetric for free, no
bridging axiom, and it is what the paper's decidability argument calls
ground.

The scope condition, which is executable
----------------------------------------
RFC 5646 does not say that distinct subtags name distinct languages, and
the registry contains a counterexample: 'iw' is deprecated with
Preferred-Value 'he', both described "Hebrew".  Two subtags, one language.

So the rule is: distinct primary language subtag records, neither
deprecated and with no Preferred-Value link between them, name distinct
languages.  This generator checks that condition against the registry
snapshot for every member and aborts if it fails, because a future slice
containing a deprecated synonym would otherwise generate a false premise
in silence.

The same check verifies the resource's claim that the slice carries no
published relation: no member may have a Macrolanguage field.  How many
such fields the whole registry carries is measured from the snapshot each
run and written into the header; it is a property of the slice, and the
generator is what makes it true rather than hopeful.
"""
import argparse
import hashlib
import sys
from itertools import combinations
from pathlib import Path

try:
    from rdflib import Graph, RDF, OWL, URIRef, Namespace
    from rdflib.collection import Collection
    from rdflib.namespace import SKOS, DCTERMS
except ImportError:
    print("needs rdflib: uv add rdflib", file=sys.stderr)
    raise

VERSION = "2.1"
BCP47 = Namespace("https://w3id.org/odrl-kb/bcp47#")
SCHEME = URIRef("https://w3id.org/odrl-kb/bcp47")
BT = Namespace("https://w3id.org/odrl-kb/background#")
THEORY = URIRef("https://w3id.org/odrl-kb/bcp47/uniqueness")


def const(notation: str) -> str:
    """The TPTP constant for a subtag, from its published notation.

    From skos:notation rather than the IRI's local name: the notation is a
    field the registry publishes and the grounding matches against, and
    parsing IRIs for data is the move this project exists to avoid.
    """
    return "bcp_" + notation.replace("-", "_").lower()


def name_part(notation: str) -> str:
    return notation.replace("-", "_").lower()


# --- the registry snapshot ---------------------------------------------

def read_registry(path: Path) -> tuple[str, dict[str, dict]]:
    """The File-Date and every language record, keyed by subtag.

    RFC 5646 section 3.1: records are separated by %%, each a set of
    Field-Name: value lines, and a field may repeat (Description does, for
    subtags with more than one name).  Some Subtag field-bodies are ranges
    such as qaa..qtz (private use); those records are kept under the range
    key, so a slice member inside such a range reports as having no
    individual record, which is correct: it has none.
    """
    text = path.read_text(encoding="utf-8")
    blocks = text.split("%%")
    file_date = ""
    for line in blocks[0].splitlines():
        if line.startswith("File-Date:"):
            file_date = line.split(":", 1)[1].strip()
    records: dict[str, dict] = {}
    for block in blocks[1:]:
        rec: dict[str, list[str]] = {}
        field = None
        for line in block.splitlines():
            if not line.strip():
                continue
            if line[0].isspace() and field:        # continuation line
                rec[field][-1] += " " + line.strip()
                continue
            if ":" not in line:
                continue
            field, value = line.split(":", 1)
            rec.setdefault(field.strip(), []).append(value.strip())
        if rec.get("Type", [""])[0] == "language" and "Subtag" in rec:
            records[rec["Subtag"][0]] = rec
    if not file_date:
        raise ValueError(f"{path}: no File-Date record; the snapshot cannot "
                         f"be identified and the resource cannot cite it")
    return file_date, records


def check_slice(notations: list[str], records: dict[str, dict]) -> None:
    """The scope condition of the uniqueness rule, enforced.

    Aborts rather than warns.  A member failing any of these makes the
    generated distinctness false, and a false premise that a prover then
    uses produces a definite verdict resting on nothing.

    The Macrolanguage check is one-directional by design: an intra-slice
    order edge can only enter through a member's own Macrolanguage field,
    so a member that is itself a macrolanguage contributes no edge unless
    an encompassed member is also present, whose own field is checked.
    """
    problems = []
    for n in notations:
        rec = records.get(n)
        if rec is None:
            problems.append(f"{n}: no individual language record in the "
                            f"registry (private-use ranges have none)")
            continue
        if "Deprecated" in rec:
            problems.append(
                f"{n}: deprecated {rec['Deprecated'][0]}; a deprecated "
                f"subtag may share a language with its preferred value")
        if "Preferred-Value" in rec:
            problems.append(
                f"{n}: Preferred-Value {rec['Preferred-Value'][0]}; the "
                f"registry says these name one language")
        if "Macrolanguage" in rec:
            problems.append(
                f"{n}: Macrolanguage {rec['Macrolanguage'][0]}; the "
                f"registry publishes an order over this member, so the "
                f"resource's claim to carry none is false and a profile "
                f"could bind this slice at tax")
    if problems:
        raise SystemExit(
            "the slice does not satisfy the uniqueness rule's scope "
            "condition:\n  " + "\n  ".join(problems) +
            "\n\nEither remove the member or narrow the rule; generating "
            "distinctness over these would assert something the registry "
            "contradicts.")


# --- the slice ---------------------------------------------------------

def read_slice(ttl: Path) -> tuple[Graph, list[tuple[str, str, list[str]]]]:
    """Concepts of the slice as (notation, prefLabel, altLabels), plus the
    graph for IRI-to-notation lookups.

    Read through skos:inScheme, which is how census.py finds concepts and
    how every other resource in the suite declares them.
    """
    g = Graph()
    g.parse(ttl, format="turtle")
    out = []
    for s in g.subjects(SKOS.inScheme, SCHEME):
        notations = sorted(str(o) for o in g.objects(s, SKOS.notation))
        if not notations:
            raise ValueError(
                f"{s} has no skos:notation; the grounding matches values "
                f"against notations, so a concept without one cannot be "
                f"named by any policy")
        if len(notations) > 1:
            print(f"  {s} has {len(notations)} notations; using "
                  f"{notations[0]!r}", file=sys.stderr)
        pref = next((str(o) for o in g.objects(s, SKOS.prefLabel)), "")
        alts = sorted(str(o) for o in g.objects(s, SKOS.altLabel))
        out.append((notations[0], pref, alts))
    if not out:
        raise ValueError(f"{ttl}: no concepts in scheme {SCHEME}")
    return g, sorted(out)


def read_theory(ttl: Path, slice_graph: Graph) -> tuple[list[str], str, int]:
    """The members of the AllDifferent as notations, the warrant, and the
    declared count.

    Members are kept as IRIs and mapped to notations through the slice
    graph's skos:notation; local names are never parsed.  Both owl:members
    (OWL 2) and owl:distinctMembers (OWL 1) are accepted.  The warrant
    (dcterms:source) and bt:pairCount are required: recording the warrant
    is the point of the split, and the declared count is the EXPECT.
    """
    g = Graph()
    g.parse(ttl, format="turtle")
    lists = []
    for node in g.subjects(RDF.type, OWL.AllDifferent):
        for prop in (OWL.members, URIRef(str(OWL) + "distinctMembers")):
            for lst in g.objects(node, prop):
                lists.append(list(Collection(g, lst)))
    if not lists:
        raise ValueError(
            f"{ttl}: no owl:AllDifferent with members; the theory declares "
            f"nothing and the file should say so or be removed")
    if len(lists) > 1:
        raise SystemExit(
            f"{ttl}: {len(lists)} AllDifferent member lists; one theory "
            f"file carries one assertion, split the file")
    members = []
    for iri in lists[0]:
        notation = next(
            (str(o) for o in slice_graph.objects(iri, SKOS.notation)), None)
        if notation is None:
            raise SystemExit(
                f"{ttl}: member {iri} has no skos:notation in the slice; "
                f"the theory speaks about a concept the resource does not "
                f"declare")
        members.append(notation)
    source = next((str(o) for o in g.objects(THEORY, DCTERMS.source)), "")
    if not source:
        raise SystemExit(
            f"{ttl}: the theory has no dcterms:source; the warrant is the "
            f"point, record it")
    declared = next((int(o) for o in g.objects(THEORY, BT.pairCount)), None)
    if declared is None:
        raise SystemExit(
            f"{ttl}: no bt:pairCount; the schema requires the declared "
            f"count and the generator verifies against it")
    return sorted(members), source, declared


# --- emission ----------------------------------------------------------

def resource_ax(concepts, file_date: str, digest: str,
                macro_total: int) -> str:
    n = len(concepts)
    lines = [
        "%" + "-" * 73,
        "% File     : BCP47000-0.ax",
        "% Domain   : ODRL policy, knowledge-grounded constraints",
        "% Axioms   : BCP 47 primary language subtags, resource",
        f"% Version  : {VERSION}",
        "% English  : The concepts the language operand is bound to, and",
        "%            nothing over them.  A registry publishes a set of",
        "%            subtags and, over this slice, no relation between",
        "%            them, so this file asserts concept membership and no",
        "%            order.  That emptiness of the order is the resource:",
        "%            at the nominal sort there is nothing for isA to",
        "%            read, and the signature rejects isA on this operand",
        "%            before the file is opened.",
        "%",
        "%            Registry uniqueness, which makes the subtags",
        "%            pairwise distinct, is the parties' rule and lives in",
        "%            BCP47001-0.ax.  A problem including this file and",
        "%            not that one gets Unknown where the declaration",
        "%            would have given a definite verdict.",
        "%",
        "% Source   : IANA Language Subtag Registry",
        f"% Snapshot : File-Date {file_date}",
        f"% Checksum : sha256:{digest}",
        "% Licence  : IETF Trust, RFC 5646",
        "%",
        "% Status   : Satisfiable",
        "% SPC      : FOF_SAT_RFN",
        "%",
        f"% Concepts : {n}",
        "% Order assertions : 0",
        f"% Macrolanguage fields in the whole snapshot: {macro_total};",
        "% in this slice: 0, generator-verified.",
        "%" + "-" * 73,
        "",
        "% Concept membership.  These facts stand by decision: they",
        "% document the published tag set and are the universe a",
        "% complement operator would need if the encodings relativise to",
        "% one.  Measured unused by the current witness encodings; drop",
        "% them only by explicit decision after that measurement.",
        "",
    ]
    for notation, pref, alts in concepts:
        label = pref + (" / " + ", ".join(alts) if alts else "")
        lines.append(f"% {notation:6} {label}")
        lines.append(
            f"fof(res_bcp47_{name_part(notation)}, axiom, "
            f"kge_concept({const(notation)})).")
    lines += [
        "",
        "% No order assertions: the registry publishes none over this",
        "% slice, and the generator aborts if any member carries a",
        "% Macrolanguage field.",
        "",
    ]
    return "\n".join(lines)


def theory_ax(pairs, source: str, file_date: str) -> str:
    lines = [
        "%" + "-" * 73,
        "% File     : BCP47001-0.ax",
        "% Domain   : ODRL policy, knowledge-grounded constraints",
        "% Axioms   : Registry uniqueness for BCP 47 primary subtags",
        f"% Version  : {VERSION}",
        "% English  : The parties' rule that distinct primary language",
        "%            subtag records, neither deprecated and with no",
        "%            Preferred-Value link between them, name distinct",
        "%            languages.",
        "%",
        "%            The registry does not assert this.  It publishes",
        "%            identity, through Preferred-Value, and an order,",
        "%            through Macrolanguage, and no distinctness at all.",
        "%            The scope condition is not decoration: 'iw' is",
        "%            deprecated with Preferred-Value 'he', both described",
        "%            Hebrew, so unrestricted distinctness over registry",
        "%            subtags is false.  The generator checks every member",
        "%            against the snapshot and aborts if the condition",
        "%            fails.",
        "%",
        "%            Distinctness, not disjointness.  Distinctness denies",
        "%            that two concepts are the same element; disjointness",
        "%            denies that anything lies below both, which needs an",
        "%            order this sort does not have.",
        "%",
        "%            A party withdraws this theory by omitting the",
        "%            include.  Any definite verdict resting on it",
        "%            reopens, Compatible as well as Incompatible.",
        "%",
        f"% Source   : {source}",
        f"% Slice    : File-Date {file_date}",
        f"% Pairs    : {len(pairs)}",
        "%",
        "% Status   : Satisfiable",
        "% SPC      : FOF_SAT_EPR",
        "%" + "-" * 73,
        "",
    ]
    for a, b in pairs:
        lines.append(
            f"fof(bg_dist_bcp47_{name_part(a)}_{name_part(b)}, axiom, "
            f"{const(a)} != {const(b)}).")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[3])
    ap.add_argument("--ttl", required=True, type=Path,
                    help="the resource slice")
    ap.add_argument("--background", required=True, type=Path,
                    help="the uniqueness theory")
    ap.add_argument("--registry", required=True, type=Path,
                    help="the IANA snapshot; the scope condition is checked "
                         "against it and the File-Date is read from it")
    ap.add_argument("--out", default=Path("problems/axioms"), type=Path)
    args = ap.parse_args()

    file_date, records = read_registry(args.registry)
    digest = hashlib.sha256(args.registry.read_bytes()).hexdigest()
    macro_total = sum(1 for r in records.values() if "Macrolanguage" in r)

    slice_graph, concepts = read_slice(args.ttl)
    notations = [n for n, _, _ in concepts]
    check_slice(notations, records)

    members, source, declared = read_theory(args.background, slice_graph)
    if set(members) != set(notations):
        raise SystemExit(
            f"the theory and the resource disagree about the slice:\n"
            f"  in the theory only : {sorted(set(members) - set(notations))}\n"
            f"  in the resource only: {sorted(set(notations) - set(members))}")

    pairs = list(combinations(notations, 2))
    if declared != len(pairs):
        raise SystemExit(
            f"the theory declares bt:pairCount {declared} and the slice "
            f"gives {len(pairs)}")

    # Labels are read from the registry rather than from the slice, so a
    # hand-typed label cannot drift from what IANA publishes.
    checked = []
    for notation, pref, alts in concepts:
        descs = records[notation].get("Description", [])
        if descs and pref and descs[0] != pref:
            print(f"  label differs from the registry: {notation} has "
                  f"{pref!r}, the registry says {descs[0]!r}",
                  file=sys.stderr)
        checked.append((notation, descs[0] if descs else pref, descs[1:]))

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "BCP47000-0.ax").write_text(
        resource_ax(checked, file_date, digest, macro_total),
        encoding="utf-8")
    (args.out / "BCP47001-0.ax").write_text(
        theory_ax(pairs, source, file_date), encoding="utf-8")

    print(f"registry    : File-Date {file_date}, sha256:{digest[:16]}...")
    print(f"concepts    : {len(concepts)}, order assertions 0")
    print(f"distinctness: {len(pairs)} pairs, all members scope-checked")
    print(f"macrolanguage fields, whole snapshot: {macro_total}; "
          f"slice: 0")
    print(f"  {args.out / 'BCP47000-0.ax'}")
    print(f"  {args.out / 'BCP47001-0.ax'}")
    print()
    print("EXPECT = {")
    print(f'    "concepts":      {len(concepts)},')
    print('    "order_edges":   0,')
    print(f'    "bg_dist_pairs": {len(pairs)},')
    print(f'    "file_date":     "{file_date}",')
    print("}")
    return 0


if __name__ == "__main__":
    sys.exit(main())