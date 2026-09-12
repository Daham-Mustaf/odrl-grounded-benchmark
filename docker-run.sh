#!/usr/bin/env bash
# What the container runs by default: rebuild, regenerate, decide.
#
# Everything here reads the vendored vocabularies and writes into the
# container's copy of the repository, so the host is untouched unless a
# volume is mounted.

set -u
cd /benchmark

echo "=== environment"
cat ENVIRONMENT

echo
echo "=== 1. resources, from the vendored vocabularies"
V=vocabularies

uv run generators/build_dpv.py \
  --purposes $V/dpv-2.3/modules/purposes.ttl \
  --retrieved 2026-08-19 --out problems \
  --declare-distinct Marketing ScientificResearch \
                     ResearchAndDevelopment Advertising >/dev/null \
  && echo "  purposes"

uv run generators/build_dpvloc.py \
  --loc $V/dpv-2.3/loc/loc.ttl \
  --retrieved 2026-08-19 --out problems \
  --declare-distinct DE FR >/dev/null && echo "  locations"

uv run generators/build_consent.py \
  --module $V/dpv-2.3/modules/consent_status.ttl \
  --retrieved 2026-08-19 --out problems \
  --declare-distinct ConsentGiven ConsentWithdrawn >/dev/null \
  && echo "  consent"

uv run generators/build_tom.py \
  --tom $V/dpv-2.3/modules/TOM.ttl \
  --measures $V/dpv-2.3/modules/technical_measures.ttl \
  --out problems >/dev/null && echo "  measures"

uv run generators/build_gdprlb.py \
  --core $V/dpv-2.3/modules/legal_basis.ttl \
  --gdpr $V/dpv-2.3/legal/eu/gdpr/modules/legal_basis.ttl \
  --retrieved 2026-08-19 --out problems >/dev/null && echo "  legal basis"

uv run generators/build_filetype.py \
  --table $V/eu-file-type-20260715/filetypes-skos-ap-act.rdf \
  --retrieved 2026-08-18 --out problems \
  --declare-distinct PDF PDFA1A >/dev/null && echo "  file type"

echo
echo "=== 2. problems"
for g in gen_motivating gen_dpv gen_dpvloc gen_filetype gen_consent \
         gen_gdprlb gen_tom gen_bcp47_problems gen_wellsorted; do
  if uv run "generators/$g.py" >/dev/null 2>&1; then
    echo "  ok     $g"
  else
    echo "  FAILED $g"
    uv run "generators/$g.py" 2>&1 | tail -2 | sed 's/^/         /'
  fi
done

echo
echo "=== 3. do the bindings entail what they claim"
uv run generators/validate_bindings.py --probes probes \
  --axioms problems/axioms 2>&1 | tail -1

echo
echo "=== 4. verdicts"
echo "    Each problem is two queries; the verdict follows from the pair."
time bash run_verdict.sh 2>/dev/null | tail -3

echo
echo "=== 5. premises: do the two encodings cite the same ones"
uv run generators/run_certify.py 2>&1 \
  | grep -E "STATUS DISAGREEMENT|PROVERS DIFFER|provenance agreement"

echo
echo "=== 6. proof checking"
uv run generators/check_certificates.py 2>&1 | tail -8

echo
echo "=== done"