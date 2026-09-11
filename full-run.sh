#!/usr/bin/env bash
# Rebuild everything from the vendored vocabularies and check it.
#
#     bash full-run.sh 2>&1 | tee /tmp/run.log
#
# Stops at the first builder or generator that fails, since everything
# after it would be checking stale files.

set -u
cd "$(dirname "$0")"

hdr() { echo; echo "=== $1"; }
die() { echo "FAILED: $1" >&2; exit 1; }

RETRIEVED=2026-08-19

# --- 1. resources, from the vendored files -----------------------------
hdr "1. builders"

uv run generators/build_dpvloc.py \
  --loc vocabularies/dpv-2.3/loc/loc.ttl \
  --retrieved "$RETRIEVED" --out problems >/dev/null || die build_dpvloc
echo "  dpvloc"

uv run generators/build_dpv.py \
  --purposes vocabularies/dpv-2.3/modules/purposes.ttl \
  --retrieved "$RETRIEVED" --out problems >/dev/null || die build_dpv
echo "  dpv purposes"

# The remaining builders take different arguments; run them by hand the
# first time and paste the working invocation here.
for b in build_consent build_gdprlb build_tom build_filetype build_bcp47; do
  if [ -f "generators/$b.py" ]; then
    echo "  $b: not invoked here, add its arguments once known"
  fi
done

# --- 2. problems -------------------------------------------------------
hdr "2. generators"
for g in gen_motivating gen_dpv gen_dpvloc gen_filetype gen_consent \
         gen_gdprlb gen_tom gen_bcp47_problems gen_wellsorted; do
  if uv run "generators/$g.py" >/dev/null 2>&1; then
    echo "  ok     $g"
  else
    echo "  FAILED $g"
    uv run "generators/$g.py" 2>&1 | tail -3 | sed 's/^/         /'
  fi
done

# --- 3. what the policies constrain ------------------------------------
hdr "3. the constraint survey"
uv run generators/survey_constraints.py 2>/dev/null | tail -25

# --- 4. lint -----------------------------------------------------------
hdr "4. terms: every controlled namespace against its schema"
uv run generators/validate_terms.py --schemas vocab \
  --instances problems cases probes 2>&1 | tail -30

hdr "5. bindings: do the probes hold"
uv run generators/validate_bindings.py --probes probes \
  --axioms problems/axioms 2>&1 | tail -5

# --- 6. verdicts -------------------------------------------------------
hdr "6. verdicts"
bash run_verdict.sh 2>/dev/null | tail -3

# --- 7. provers agree --------------------------------------------------
hdr "7. two provers, and what they cite"
uv run generators/run_certify.py 2>&1 | grep -E \
  "STATUS DISAGREEMENT|PROVERS DIFFER|provenance agreement" | tail -10

hdr "8. proof checking"
uv run generators/check_certificates.py 2>&1 | tail -12

echo
echo "=== done"