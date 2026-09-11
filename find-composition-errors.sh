#!/usr/bin/env bash
# Find every place in DPV Locations where a subdivision reaches a union
# by transitivity, and report the ones where that conclusion is false.
#
#     bash find-composition-errors.sh
#
# The problem, in one line: DPV writes skos:broader for administrative
# parthood (BQ in NL) and for union membership (NL in EU). Each edge is
# true. Composing them under one order derives that Bonaire is in the
# EU, which no publisher asserted and which is false in law.

set -u
cd "$(dirname "$0")"
V=vocabularies/dpv-2.3/loc/loc.ttl

echo "=== 1. how many subdivisions reach a union by two hops"
uv run python - "$V" <<'PY'
import sys
from collections import defaultdict
from rdflib import Graph, Namespace, RDF, SKOS

DPV = Namespace("https://w3id.org/dpv#")
LOC = Namespace("https://w3id.org/dpv/loc#")
g = Graph().parse(sys.argv[1], format="turtle")

def local(u): return str(u).rsplit("#", 1)[-1]

unions, countries, subdivisions = set(), set(), set()
for s in g.subjects(RDF.type, DPV.SupraNationalUnion):
    unions.add(local(s))
for s in g.subjects(RDF.type, DPV.EconomicUnion):
    unions.add(local(s))
for s in g.subjects(RDF.type, DPV.Country):
    countries.add(local(s))
for s in g.subjects(RDF.type, DPV.Region):
    subdivisions.add(local(s))

up = defaultdict(set)
for s, o in g.subject_objects(SKOS.broader):
    if str(s).startswith(str(LOC)) and str(o).startswith(str(LOC)):
        up[local(s)].add(local(o))

# A two-hop path: subdivision -> country -> union.
chains = []
for sub in sorted(subdivisions):
    for mid in sorted(up.get(sub, ())):
        if mid not in countries:
            continue
        for top in sorted(up.get(mid, ())):
            if top in unions:
                chains.append((sub, mid, top))

print(f"  {len(subdivisions)} subdivisions, {len(countries)} countries, "
      f"{len(unions)} unions")
print(f"  {len(chains)} subdivision-country-union chains")
print(f"  distinct subdivisions reaching a union: "
      f"{len({c[0] for c in chains})}")
print()
print("  first ten chains:")
for sub, mid, top in chains[:10]:
    print(f"    {sub:12} < {mid:6} < {top}")

# The ones worth checking by hand: subdivisions of EU member states that
# are not themselves EU territory. DPV marks none of this, so the list
# below is the candidate set a lawyer would have to review, not a set of
# confirmed errors.
print()
print("  overseas and special-status subdivisions among them, by the")
print("  only signal the file carries, a hyphenated code whose prefix")
print("  differs from a European parent:")
seen = set()
for sub, mid, top in chains:
    if "-" in sub and sub.split("-")[0] != mid:
        if sub not in seen:
            seen.add(sub)
            print(f"    {sub:12} < {mid:6} < {top}")
print(f"  {len(seen)} such")
PY

echo
echo "=== 2. what DPV says about jurisdiction, which neither reading takes"
grep -c "dpv:hasInverseJurisdiction" $V
echo "  hasInverseJurisdiction assertions; and the property itself:"
grep -n -A8 "^dpv:hasInverseJurisdiction a" $V | head -12

echo
echo "=== 3. does the file mark territorial status anywhere"
grep -c "OverseasCountry\|OutermostRegion\|SpecialTerritory\|OCT" $V
echo "  mentions of overseas or special territorial status"

echo
echo "=== 4. Bonaire, in full, as the file writes it"
grep -n -A16 "^loc:BQ a" $V