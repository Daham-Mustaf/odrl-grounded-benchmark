#!/usr/bin/env bash
# Walk the DPV Locations resource through the pipeline, one stage at a
# time, and stop at the first thing that is wrong.
#
#     bash check-loc.sh
#
# Read-only except stage 3, which regenerates. Nothing else writes.

set -u
cd "$(dirname "$0")"

hdr() { echo; echo "=== $1"; }

# --- 1. the vendored file ---------------------------------------------
hdr "1. the vendored source"
ls -la --time-style=long-iso vocabularies/dpv-2.3/loc/loc.ttl
sha256sum vocabularies/dpv-2.3/loc/loc.ttl | cut -c1-24
echo "  -> the resource must record this digest; compare below"

# --- 2. the census -----------------------------------------------------
hdr "2. what the file publishes, measured"
uv run generators/census.py vocabularies/dpv-2.3/loc/loc.ttl 2>/dev/null |
  grep -E "triples|declared concepts|ORDER CANDIDATE|identity|separation|retired concepts|licence"

# --- 3. the builder ----------------------------------------------------
hdr "3. the builder, regenerating"
uv run generators/build_dpvloc.py \
  --loc vocabularies/dpv-2.3/loc/loc.ttl \
  --retrieved 2026-08-19 --out problems
echo "  -> must complete and print the partition; an EXPECT mismatch aborts"

# --- 4. what it wrote --------------------------------------------------
hdr "4. the emitted files"
for f in problems/resources/dpvloc-geo.ttl \
         problems/resources/dpvloc-juris.ttl \
         problems/resources/profile-dpvloc-geo.ttl \
         problems/resources/profile-dpvloc-juris.ttl \
         problems/background/dpvloc-empty.ttl \
         problems/background/dpvloc-iso.ttl \
         problems/axioms/LOC-dpvloc-geo.ax \
         problems/axioms/LOC-dpvloc-juris.ax \
         problems/axioms/LOC-dpvloc-iso.ax; do
  printf "  %-46s %s\n" "$(basename $f)" \
    "$([ -f $f ] && wc -l < $f || echo MISSING)"
done

hdr "4a. provenance in the resource"
grep -E "dcterms:(source|hasVersion|issued|identifier|license)" \
  problems/resources/dpvloc-geo.ttl

hdr "4b. every bt: and bind: term, against the vocabulary"
used=$(grep -oh "bt:[A-Za-z]*\|bind:[A-Za-z]*" \
  problems/background/dpvloc-*.ttl \
  problems/resources/profile-dpvloc-*.ttl 2>/dev/null | sort -u)
for t in $used; do
  ns=${t%%:*}; name=${t#*:}
  [ -z "$name" ] && continue
  if grep -q "^$t\b" vocab/$( [ $ns = bt ] && echo background || echo binding ).ttl
  then printf "  ok   %s\n" "$t"
  else printf "  UNDEFINED %s\n" "$t"
  fi
done

hdr "4c. the resource files parse"
for f in problems/resources/dpvloc-geo.ttl \
         problems/resources/dpvloc-juris.ttl \
         problems/resources/profile-dpvloc-geo.ttl \
         problems/resources/profile-dpvloc-juris.ttl \
         problems/background/dpvloc-empty.ttl \
         problems/background/dpvloc-iso.ttl; do
  uv run python -c "
from rdflib import Graph
try:
    g = Graph().parse('$f', format='turtle')
    print(f'  ok   $(basename $f): {len(g)} triples')
except Exception as e:
    print(f'  FAIL $(basename $f): {str(e)[:60]}')
"
done

# --- 5. the axioms -----------------------------------------------------
hdr "5. the axiom files, by premise class"
for f in problems/axioms/LOC-dpvloc-*.ax; do
  printf "  %-34s total %5s  res_ %5s  bg_ %4s\n" "$(basename $f)" \
    "$(grep -c '^fof' $f)" "$(grep -c '^fof(res_' $f)" \
    "$(grep -c '^fof(bg_' $f)"
done
echo "  -> res_ is what DPV published, bg_ what the parties declared."
echo "     A resource file with bg_ assertions has mixed the two."

hdr "5a. the two readings differ where they should"
echo -n "  loc_eu in the geographic axioms (must be 0): "
grep -c "loc_eu" problems/axioms/LOC-dpvloc-geo.ax
echo -n "  loc_eu in the jurisdictional axioms (must be > 0): "
grep -c "loc_eu" problems/axioms/LOC-dpvloc-juris.ax

# --- 6. the bindings ---------------------------------------------------
hdr "6. the probes: does the binding mean what it says"
uv run generators/validate_bindings.py --probes probes \
  --axioms problems/axioms 2>&1 |
  grep -E "dpvloc|all probes|probe failure"

# --- 7. the problems ---------------------------------------------------
hdr "7. regenerating the problems"
uv run generators/gen_dpvloc.py 2>&1 | tail -3

hdr "7a. what the policies constrain"
uv run generators/survey_constraints.py 2>/dev/null |
  grep -E "spatial|^  KGC33"

# --- 8. the verdicts ---------------------------------------------------
hdr "8. the verdicts"
bash run_verdict.sh 2>/dev/null | grep -E "KGC33|KGC302"

hdr "8a. both provers, and what they cite"
uv run generators/run_certify.py --problem KGC330 2>&1 | tail -6
uv run generators/run_certify.py --problem KGC334 2>&1 | tail -6

echo
echo "=== done. Every stage above must be clean before the next one means"
echo "    anything: a wrong reading at 3 shows up as a wrong verdict at 8."