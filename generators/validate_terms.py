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
Four namespaces are ours: bind:, bt:, vrep: and odrlkb:. Their schemas
live in vocab/. Instance files are written by builders and generators,
at different times, by hand and by template, and nothing until now
checked that a term written into a file is a term the schema defines.

The result was predictable. vrep:Refutation, vrep:premise,
vrep:premiseSource, vrep:clashingConstraint, vrep:witness and
vrep:ungroundedValue were written into every case file for months; none
is in vocab/verdict-report.ttl. bt:assertionCount and bt:distinctFrom
were written into a background theory; neither is in
vocab/background.ttl.

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

# The namespaces this project controls, and the schema file that defines
# each. A prefix not listed here is somebody else's and is skipped.
OURS = {
    "bind":   "binding.ttl",
    "bt":     "background.ttl",
    "vrep":   "verdict-report.ttl",
    "odrlkb": None,     # minted per resource by the builders; see below
}

# odrlkb: terms are minted by the resource builders (odrlkb:within,
# odrlkb:sameAs, odrlkb:Place and the like) and have no schema file yet.
# They are collected and reported rather than checked, so the report says
# how large that gap is without failing the build over it.

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


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[3])
    ap.add_argument("--schemas", default="vocab", type=Path,
                    help="directory of schema .ttl files")
    ap.add_argument("--instances", nargs="+", type=Path,
                    default=[Path("problems"), Path("cases")],
                    help="directories or files to check")
    ap.add_argument("--show-files", action="store_true",
                    help="list the files using each undefined term")
    args = ap.parse_args()

    if not args.schemas.is_dir():
        print(f"no schema directory {args.schemas}", file=sys.stderr)
        return 2

    defined = defined_terms(args.schemas)
    used = used_terms(args.instances)

    if not defined:
        print(f"no definitions found in {args.schemas}. Schemas are read "
              f"as lines of the form 'prefix:Term a ...'; check the "
              f"layout.", file=sys.stderr)
        return 2

    print("schema coverage")
    for prefix in sorted(OURS):
        n_def = len(defined.get(prefix, ()))
        n_use = len(used.get(prefix, {}))
        schema = OURS[prefix] or "(no schema file)"
        print(f"  {prefix + ':':10} {n_def:3} defined in {schema:22} "
              f"{n_use:3} used")

    failures = 0
    for prefix in sorted(used):
        if prefix not in OURS:
            continue
        if OURS[prefix] is None:
            # Minted by the builders; reported, not failed.
            names = sorted(used[prefix])
            if names:
                print()
                print(f"{prefix}: {len(names)} terms minted by the builders "
                      f"and defined by no schema:")
                for name in names[:12]:
                    print(f"  {prefix}:{name}")
                if len(names) > 12:
                    print(f"  ... and {len(names) - 12} more")
                print("  These need a schema file before the artefact is "
                      "published.")
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

    # A term defined and never used is not an error, but a schema that has
    # drifted ahead of what anything writes is worth seeing.
    print()
    for prefix in sorted(OURS):
        if OURS[prefix] is None:
            continue
        unused = sorted(defined.get(prefix, set()) - set(used.get(prefix, {})))
        if unused:
            print(f"{prefix}: {len(unused)} defined and unused: "
                  + ", ".join(unused[:8])
                  + (" ..." if len(unused) > 8 else ""))

    print()
    if failures:
        print(f"{failures} undefined terms. Either define them in the "
              f"schema or stop writing them.")
        return 1
    print("every term in a controlled namespace is defined by its schema.")
    return 0


if __name__ == "__main__":
    sys.exit(main())