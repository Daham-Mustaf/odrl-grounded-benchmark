#!/bin/bash
# Audit all 54 problems through 7 prover configurations.
# Runs each problem from its own directory so includes resolve correctly.

set -u
ROOT="$(cd "$(dirname "$0")" && pwd)"
PROBLEMS="$ROOT/Problems/ODRL/KGConstraints"
mkdir -p "$ROOT/audit_logs"
TS=$(date +%Y%m%d-%H%M%S)
CSV="$ROOT/audit_logs/audit_${TS}.csv"

echo "problem,layer,expected,casc,casc_t,disc,disc_t,lrs,lrs_t,otter,otter_t,e,e_t,z3,z3_t,cvc5,cvc5_t" > "$CSV"

run_vampire() {
    local strat="$1" file="$2"
    local flag
    if [ "$strat" = "casc" ]; then
        flag="--mode casc"
    else
        flag="--saturation_algorithm $strat"
    fi
    local t0=$(date +%s.%N)
    local out=$(vampire $flag --time_limit 10s "$file" 2>&1)
    local t1=$(date +%s.%N)
    local res=$(echo "$out" | grep -E "^% SZS status" | head -1 | awk '{print $4}')
    local elapsed=$(awk "BEGIN { printf \"%.2f\", $t1 - $t0 }")
    [ -z "$res" ] && res="Timeout"
    echo "$res,$elapsed"
}

run_eprover() {
    local file="$1"
    local t0=$(date +%s.%N)
    local res=$(eprover --auto --tptp3-format -s --cpu-limit=10 "$file" 2>&1 | \
                grep "SZS status" | head -1 | awk '{print $4}')
    local t1=$(date +%s.%N)
    local elapsed=$(awk "BEGIN { printf \"%.2f\", $t1 - $t0 }")
    [ -z "$res" ] && res="Timeout"
    echo "$res,$elapsed"
}

run_smt() {
    local cmd="$1" file="$2"
    local t0=$(date +%s.%N)
    local res=$($cmd "$file" 2>&1 | grep -E "^(sat|unsat|unknown)$" | head -1)
    local t1=$(date +%s.%N)
    local elapsed=$(awk "BEGIN { printf \"%.2f\", $t1 - $t0 }")
    [ -z "$res" ] && res="timeout"
    echo "$res,$elapsed"
}

count=0
for prob in $(find "$PROBLEMS" -name "KGC*-1.p" -type f | sort); do
    count=$((count+1))
    base=$(basename "$prob" .p)
    layer=$(basename "$(dirname "$prob")")
    smt="${prob%.p}.smt2"
    expected=$(grep -m 1 "^% Status" "$prob" | awk '{print $4}')

    # Run each problem from its own directory so include paths resolve
    probdir=$(dirname "$prob")
    probname=$(basename "$prob")
    smtname=$(basename "$smt")

    pushd "$probdir" >/dev/null

    casc=$(run_vampire casc "$probname")
    disc=$(run_vampire discount "$probname")
    lrs=$(run_vampire lrs "$probname")
    otter=$(run_vampire otter "$probname")
    e=$(run_eprover "$probname")
    z3=$(run_smt "z3 -T:10" "$smtname")
    cvc5=$(run_smt "cvc5 --tlimit=10000" "$smtname")

    popd >/dev/null

    echo "$base,$layer,$expected,$casc,$disc,$lrs,$otter,$e,$z3,$cvc5" >> "$CSV"

    casc_status="${casc%%,*}"
    if [ "$casc_status" = "$expected" ]; then
        printf "[%2d/54] %-12s %-12s expected=%-20s casc=%-20s OK\n" \
            "$count" "$base" "$layer" "$expected" "$casc_status"
    else
        printf "[%2d/54] %-12s %-12s expected=%-20s casc=%-20s CHECK\n" \
            "$count" "$base" "$layer" "$expected" "$casc_status"
    fi
done

echo ""
echo "Audit complete. Log: $CSV"
echo "Total problems: $count"
