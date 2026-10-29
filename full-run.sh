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

# A check that fails sets this and the run goes on, so one run reports every
# failure; the exit status at the end says whether there was one.
FAILED=0

# Seconds a prover may take on one query, for the verdict run (stage 6) and
# the proof checker (stage 8) alike.  The checker runs Vampire in a mode that
# is slower on satisfiable queries than the one stage 6 uses; KGC331-1 takes
# about 35 seconds there.  Set PROVER_LIMIT to change it.
PROVER_LIMIT="${PROVER_LIMIT:-60}"

RETRIEVED=2026-08-19

# --- 1. resources, from the vendored files -----------------------------
hdr "1. builders"

# The framework axioms every query includes.  Regenerated here so the file
# cannot drift from its generator.
uv run generators/gen_primitives.py >/dev/null || die gen_primitives
echo "  framework axioms"

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
for b in build_consent build_tom build_filetype build_bcp47; do
  if [ -f "generators/$b.py" ]; then
    echo "  $b: not invoked here, add its arguments once known"
  fi
done

# --- 2. problems -------------------------------------------------------
hdr "2. generators"
for g in gen_motivating gen_geonames gen_dpv gen_dpvloc gen_filetype \
         gen_consent gen_tom gen_bcp47_problems gen_wellsorted; do
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

hdr "4b. case files: the agreed shape"
uv run generators/validate_cases.py 2>&1 | tail -40

hdr "4c. no placeholders left in generated files"
if grep -rIn -E 'GENERATOR_|TODO' cases problems certificates; then
  die "GENERATOR_ or TODO left in a generated file (listed above)"
fi
echo "  none"

hdr "4d. declarations: the RDF of each set, its axioms and the queries that carry it"
uv run generators/check_declarations.py || die "a set of declarations disagrees with its axioms or queries"

hdr "4e. cases: shape lint, what each policy asks, coverage of the grid"
cases_ok=0
lint_out=$(uv run generators/lint_cases.py 2>&1) || cases_ok=1
echo "$lint_out" | sed -n '/^FAILURES:/,$p;/^lint clean/p'
uv run generators/check_policies.py || cases_ok=1
uv run generators/check_coverage.py || cases_ok=1
if [ "$cases_ok" != 0 ]; then
  echo "FAILED: a case did not pass 4e (listed above, by case ID)" >&2
  FAILED=1
fi

hdr "5. bindings: do the probes hold"
uv run generators/validate_bindings.py --probes probes \
  --axioms problems/axioms 2>&1 | tail -5
[ "${PIPESTATUS[0]}" -eq 0 ] || { echo "FAILED: a binding probe does not hold" >&2; FAILED=1; }

# --- 6. verdicts -------------------------------------------------------
hdr "6. verdicts"
TIMEOUT="$PROVER_LIMIT" bash run_verdict.sh 2>/dev/null | tail -3

# --- 6b. the two encodings agree ---------------------------------------
hdr "6b. encodings: TPTP and SMT-LIB give the same status"
uv run generators/check_encodings.py 2>&1 | tail -4

# --- 7. provers agree --------------------------------------------------
hdr "7. two provers, and what they cite"
uv run generators/run_certify.py 2>&1 | grep -E \
  "STATUS DISAGREEMENT|STATUS INCONCLUSIVE|PROVERS DIFFER|provenance agreement" | tail -10

hdr "8. proof checking"
cert_out=$(mktemp)
uv run generators/check_certificates.py --limit "$PROVER_LIMIT" > "$cert_out" 2>&1
grep -E "^(suite summary|  (FULLY_CHECKED|PARTIALLY_CHECKED|REJECTED|other) )" "$cert_out"
echo
grep -E -A40 "^(unsupported mechanisms|premise classes)" "$cert_out"
if ! grep -qE "^  REJECTED +0$" "$cert_out"; then
  echo "FAILED: the checker rejected a refutation, or did not finish" >&2
  FAILED=1
fi
if grep -E "^  other " "$cert_out" | grep -qE "NO-STATUS|TIMEOUT|PARSE"; then
  echo "FAILED: a query got no status within ${PROVER_LIMIT} seconds" >&2
  FAILED=1
fi
rm -f "$cert_out"

hdr "9. figures for the paper"
uv run generators/table_data.py --suite-numbers 2>&1 | tail -6

hdr "10. catalogue of the cases"
uv run generators/catalogue.py || FAILED=1
uv run generators/catalogue.py --blind || FAILED=1

echo
echo "=== done"
if [ "$FAILED" != 0 ]; then
  echo "FAILED: a check above did not pass" >&2
  exit 1
fi