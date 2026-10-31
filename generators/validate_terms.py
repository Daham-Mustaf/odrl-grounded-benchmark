#!/usr/bin/env python3
"""
validate_terms.py
=================
Every term in a namespace this project controls must be defined by that
namespace's schema.

    uv run generators/validate_terms.py --schemas vocab --instances problems
    uv run generators/validate_terms.py --schemas vocab \
        --instances problems cases probes

Why this exists
---------------
Three namespaces are ours: bind:, vrep: and odrlkb:. Their schemas
live in vocab/. Instance files are written by builders and generators,
at different times, by hand and by template, and nothing until now
checked that a term written into a file is a term the schema defines.

odrlkb: is the prefix the resource builders mint their terms with, and it
names each resource's own namespace, https://w3id.org/odrl-kb/<resource>#.
Its terms are therefore compared as IRIs, read with rdflib. A term is
defined when vocab/odrlkb.ttl defines it as a class or a property with a
label, or when a file in problems/resources types and labels it: a concept
a resource publishes is defined by the resource that publishes it.

The result was predictable. vrep:Refutation, vrep:premise,
vrep:premiseSource, vrep:clashingConstraint, vrep:witness and
vrep:ungroundedValue were written into every case file for months; none
is in vocab/verdict-report.ttl. bt:assertionCount and bt:distinctFrom
were written into a set of declarations; neither was in the schema of the
time.

The bt: namespace is retired. Its terms live in bind: (vocab/binding.ttl),
and a bt: term left in any file is reported as a failure.

An undefined term is not a typo. It is a claim in a controlled namespace
that no schema backs, so a consumer resolving it gets nothing, and the
file says less than it appears to.

What it does not check
----------------------
Terms in namespaces we do not control: odrl:, dcterms:, skos:, dpv:,
loc:, report:. Those belong to their publishers and are theirs to define.
This checks only what we mint.
"""

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

from rdflib import Graph, OWL, RDF, RDFS, URIRef
from rdflib.namespace import SKOS

# The namespaces this project controls, and the schema file that defines
# each. A prefix not listed here is somebody else's and is skipped.
OURS = {
    "bind":   "binding.ttl",
    "vrep":   "verdict-report.ttl",
    "odrlkb": "odrlkb.ttl",     # compared as IRIs; see the docstring
}

# Namespaces that no longer exist. A term in one is a failure, whether or
# not any schema defines it.
RETIRED = {"bt": "bind:"}

_TERM = re.compile(r"\b(bind|bt|vrep|odrlkb):([A-Za-z][A-Za-z0-9_-]*)\b")

# A definition is a term appearing as the subject of a triple at the start
# of a line. Turtle allows other layouts, but every schema in vocab/ is
# written this way, and a looser pattern would count a term as defined
# because it appeared as an object somewhere.
_DEFINED = re.compile(r"^(bind|bt|vrep|odrlkb):([A-Za-z][A-Za-z0-9_-]*)\s+a\s",
                      re.M)


def defined_terms(schema_dir: Path) -> dict:
    """Terms each schema defines, by prefix."""
    out = defaultdict(set)
    for path in sorted(schema_dir.glob("*.ttl")):
        for prefix, name in _DEFINED.findall(path.read_text(encoding="utf-8")):
            out[prefix].add(name)
    return out


def used_terms(paths) -> dict:
    """Terms each file uses, by prefix, with the files that use them."""
    out = defaultdict(lambda: defaultdict(set))
    for root in paths:
        files = ([root] if root.is_file()
                 else sorted(p for p in root.rglob("*")
                             if p.suffix in (".ttl", ".json", ".ax", ".p")))
        for path in files:
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            for prefix, name in _TERM.findall(text):
                out[prefix][name].add(str(path))
    return out


_GRAPHS: dict = {}


def graph(path: Path) -> Graph:
    if path not in _GRAPHS:
        _GRAPHS[path] = Graph().parse(path, format="turtle")
    return _GRAPHS[path]


def odrlkb_used(paths) -> dict:
    """odrlkb: terms as IRIs, with the files that write them.  A file other
    than Turtle that writes odrlkb: names no namespace, and its terms are
    kept by name, so that they are reported."""
    out = defaultdict(set)
    for root in paths:
        files = ([root] if root.is_file()
                 else sorted(p for p in root.rglob("*")
                             if p.suffix in (".ttl", ".json", ".ax", ".p")))
        for path in files:
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            if "odrlkb:" not in text:
                continue
            if path.suffix != ".ttl":
                for prefix, name in _TERM.findall(text):
                    if prefix == "odrlkb":
                        out[f"odrlkb:{name}"].add(str(path))
                continue
            g = graph(path)
            ns = dict(g.namespaces()).get("odrlkb")
            if ns is None:
                continue
            for t in {x for triple in g for x in triple
                      if isinstance(x, URIRef) and str(x).startswith(str(ns))}:
                out[str(t)].add(str(path))
    return out


SCHEMA_KINDS = (RDFS.Class, OWL.Class, RDF.Property, OWL.ObjectProperty,
                OWL.DatatypeProperty)


def odrlkb_defined(schema: Path, resources: Path) -> tuple:
    """(the labelled classes and properties schema defines, the concepts a
    resource file types and labels), as IRIs."""
    classes = set()
    if schema.exists():
        g = graph(schema)
        classes = {str(c) for kind in SCHEMA_KINDS
                   for c in g.subjects(RDF.type, kind)
                   if g.value(c, RDFS.label) is not None}
    concepts = set()
    for path in sorted(resources.glob("*.ttl")):
        g = graph(path)
        concepts |= {str(c) for c in set(g.subjects(RDF.type, None))
                     if isinstance(c, URIRef)
                     and (g.value(c, RDFS.label) is not None
                          or g.value(c, SKOS.prefLabel) is not None)}
    return classes, concepts


def short(iri: str) -> str:
    """odrlkb:name and the resource whose namespace it is in."""
    ns, _, name = iri.rpartition("#")
    return f"odrlkb:{name} ({ns.rsplit('/', 1)[-1]})" if name else iri


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[3])
    ap.add_argument("--schemas", default="vocab", type=Path,
                    help="directory of schema .ttl files")
    ap.add_argument("--instances", nargs="+", type=Path,
                    default=[Path("problems"), Path("cases")],
                    help="directories or files to check")
    ap.add_argument("--resources", default=Path("problems/resources"),
                    type=Path, help="the resource files, whose typed and "
                                    "labelled concepts are odrlkb: terms "
                                    "they define")
    ap.add_argument("--show-files", action="store_true",
                    help="list the files using each undefined term")
    args = ap.parse_args()

    if not args.schemas.is_dir():
        print(f"no schema directory {args.schemas}", file=sys.stderr)
        return 2

    defined = defined_terms(args.schemas)
    used = used_terms(args.instances)
    kb_used = odrlkb_used(args.instances)
    kb_classes, kb_concepts = odrlkb_defined(args.schemas / OURS["odrlkb"],
                                             args.resources)

    if not defined:
        print(f"no definitions found in {args.schemas}. Schemas are read "
              f"as lines of the form 'prefix:Term a ...'; check the "
              f"layout.", file=sys.stderr)
        return 2

    print("schema coverage")
    for prefix in sorted(OURS):
        if prefix == "odrlkb":
            in_res = len(set(kb_used) & kb_concepts)
            print(f"  {prefix + ':':10} {len(kb_classes):3} defined in "
                  f"{OURS[prefix]:22} {len(kb_used):3} used, {in_res} of them "
                  f"concepts {args.resources} types and labels")
            continue
        n_def = len(defined.get(prefix, ()))
        n_use = len(used.get(prefix, {}))
        print(f"  {prefix + ':':10} {n_def:3} defined in {OURS[prefix]:22} "
              f"{n_use:3} used")

    failures = 0
    kb_undefined = sorted(set(kb_used) - kb_classes - kb_concepts)
    if kb_undefined:
        failures += len(kb_undefined)
        print()
        print(f"odrlkb: {len(kb_undefined)} terms used and neither defined in "
              f"{OURS['odrlkb']} nor typed and labelled in {args.resources}:")
        for iri in kb_undefined:
            files = sorted(kb_used[iri])
            where = f"  ({len(files)} files)" if len(files) > 3 \
                else "  " + ", ".join(Path(f).name for f in files)
            print(f"  {short(iri)}{where}")
            if args.show_files:
                for f in files[:10]:
                    print(f"      {f}")

    for prefix in sorted(used):
        if prefix not in OURS or prefix == "odrlkb":
            continue

        undefined = sorted(set(used[prefix]) - defined.get(prefix, set()))
        if not undefined:
            continue
        failures += len(undefined)
        print()
        print(f"{prefix}: {len(undefined)} terms used and not defined in "
              f"{OURS[prefix]}:")
        for name in undefined:
            files = sorted(used[prefix][name])
            where = f"  ({len(files)} files)" if len(files) > 3 \
                else "  " + ", ".join(Path(f).name for f in files)
            print(f"  {prefix}:{name}{where}")
            if args.show_files:
                for f in files[:10]:
                    print(f"      {f}")

    for prefix, moved_to in sorted(RETIRED.items()):
        names = sorted(used.get(prefix, {}))
        if not names:
            continue
        failures += len(names)
        print()
        print(f"{prefix}: retired namespace, its terms moved to {moved_to}; "
              f"still written:")
        for name in names:
            files = sorted(used[prefix][name])
            where = f"  ({len(files)} files)" if len(files) > 3 \
                else "  " + ", ".join(Path(f).name for f in files)
            print(f"  {prefix}:{name}{where}")

    # A term defined and never used is not an error, but a schema that has
    # drifted ahead of what anything writes is worth seeing.
    print()
    kb_unused = sorted(short(c) for c in kb_classes - set(kb_used))
    if kb_unused:
        print(f"odrlkb: {len(kb_unused)} defined and unused: "
              + ", ".join(kb_unused))
    for prefix in sorted(OURS):
        if prefix == "odrlkb":
            continue
        unused = sorted(defined.get(prefix, set()) - set(used.get(prefix, {})))
        if unused:
            print(f"{prefix}: {len(unused)} defined and unused: "
                  + ", ".join(unused[:8])
                  + (" ..." if len(unused) > 8 else ""))

    print()
    if failures:
        print(f"{failures} undefined or retired terms. Either define them "
              f"in the schema or stop writing them.")
        return 1
    print("every term in a controlled namespace is defined by its schema.")
    return 0


if __name__ == "__main__":
    sys.exit(main())