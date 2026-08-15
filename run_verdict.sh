#!/usr/bin/env bash
# Runs both queries of each problem and derives the verdict from the pair.
# Usage:  bash run_verdict.sh [problem-glob]
set -u
cd "$(git rev-parse --show-toplevel)/problems" 2>/dev/null || cd .
GLOB="${1:-verdict/KGC*-1.p}"
TIMEOUT="${TIMEOUT:-30}"

norm () {  # SZS status -> sat | unsat | other
  case "$1" in
    Satisfiable|CounterSatisfiable) echo sat ;;
    Unsatisfiable|Theorem|ContradictoryAxioms) echo unsat ;;
    *) echo "$1" ;;
  esac
}

verdict () {  # $1 $2 = normalised statuses of query 1 and query 2
  if   [ "$1" = unsat ] && [ "$2" = unsat ]; then echo "INCONSISTENT"
  elif [ "$1" = unsat ]; then echo "Incompatible"
  elif [ "$2" = unsat ]; then echo "Compatible"
  elif [ "$1" = sat ] && [ "$2" = sat ]; then echo "Unknown"
  else echo "undecided($1,$2)"; fi
}

printf "%-10s %-22s %-22s %-14s %s\n" PROBLEM QUERY-1 QUERY-2 VERDICT CHECK
PASS=0; FAIL=0
for q1 in $GLOB; do
  base="${q1%-1.p}"; id="$(basename "$base")"
  q2="${base}-2.p"
  [ -f "$q2" ] || { echo "$id: missing query 2"; continue; }

  e1=$(norm "$(grep -m1 '^% Status' "$q1" | awk '{print $4}')")
  e2=$(norm "$(grep -m1 '^% Status' "$q2" | awk '{print $4}')")
  a1=$(norm "$(vampire --mode casc --time_limit $TIMEOUT "$q1" 2>&1 \
        | grep 'SZS status' | head -1 | awk '{print $4}')")
  a2=$(norm "$(vampire --mode casc --time_limit $TIMEOUT "$q2" 2>&1 \
        | grep 'SZS status' | head -1 | awk '{print $4}')")

  exp=$(verdict "$e1" "$e2"); got=$(verdict "$a1" "$a2")
  if [ "$exp" = "$got" ]; then mark="ok"; PASS=$((PASS+1))
  else mark="MISMATCH"; FAIL=$((FAIL+1)); fi
  printf "%-10s %-22s %-22s %-14s %s\n" \
    "$id" "$e1/$a1" "$e2/$a2" "$got" "$mark"
done
echo
echo "pass $PASS   fail $FAIL"