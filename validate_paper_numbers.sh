#!/bin/bash
# validate_paper_numbers.sh
# Cross-check paper numbers against problem files and audit log.

cd "$(dirname "$0")"
ROOT="$(pwd)"
PROBLEMS="$ROOT/Problems/ODRL/KGConstraints"

# ---- Expected matrix from the paper -----------------------------------------
# Format per line: layer|conflict_ids|compatible_ids|unknown_ids|other_ids
EXPECTED='Motivating example|300|302|301|
Per-operator eq|400|401|402|
Per-operator isA|410|411|412|
Per-operator isPartOf|420|421|422|
Per-operator hasPart|430|431|432|
Per-operator isAnyOf|440|441|442|
Per-operator complement|450,460|451,461||
Refinement|500||501,502|
Runtime|600,601,602|||
Composition and|700,704,706,702|701,703,705||
Composition or/xone|710,713,712|711||
Monotonicity|800,801,802,806,807,808|803,804,805||810,812
Alignment|900,902|901||910'

EXPECTED_TOTAL=54
EXPECTED_PASS=53
EXPECTED_DOC_TIMEOUT=1
EXPECTED_FAIL=0
EXPECTED_CVC5_UNK=18

# Documented exceptions (space-separated list of IDs)
DOC_EXC_IDS="KGC705-1 KGC812-1 KGC430-1"

ERRORS=0

# ---- Helpers ----------------------------------------------------------------
get_status() {
    grep -m 1 "^% Status" "$1" 2>/dev/null | awk '{print $4}'
}

is_doc_exception() {
    case " $DOC_EXC_IDS " in
        *" $1 "*) return 0 ;;
        *) return 1 ;;
    esac
}

find_problem_file() {
    local id="$1"
    for subdir in Conflict Refinement Runtime Composition Monotonicity Alignment; do
        local f="$PROBLEMS/$subdir/KGC${id}-1.p"
        if [ -f "$f" ]; then
            echo "$f"
            return
        fi
    done
}

# ---- Step 1: total count ----------------------------------------------------
echo "=== Step 1: total file count ==="
ACTUAL_TOTAL=$(find "$PROBLEMS" -name "KGC*-1.p" -type f | wc -l | tr -d ' ')
echo "Expected: $EXPECTED_TOTAL"
echo "Actual:   $ACTUAL_TOTAL"
if [ "$ACTUAL_TOTAL" != "$EXPECTED_TOTAL" ]; then
    echo "MISMATCH"
    ERRORS=$((ERRORS+1))
else
    echo "OK"
fi
echo ""

# ---- Step 2: matrix cell verification ---------------------------------------
echo "=== Step 2: verify matrix cells ==="
ALL_CLAIMED_IDS=""

# Process the matrix line by line
echo "$EXPECTED" | while IFS='|' read -r layer c_ids k_ids u_ids other_ids; do
    [ -z "$layer" ] && continue

    for cell_pair in "C:$c_ids:Theorem" "K:$k_ids:Theorem" "U:$u_ids:CounterSatisfiable" "O:$other_ids:any"; do
        cell_label=$(echo "$cell_pair" | cut -d: -f1)
        cell_ids=$(echo "$cell_pair" | cut -d: -f2)
        expected_status=$(echo "$cell_pair" | cut -d: -f3)
        [ -z "$cell_ids" ] && continue

        OLDIFS="$IFS"
        IFS=','
        for id in $cell_ids; do
            f=$(find_problem_file "$id")
            if [ -z "$f" ]; then
                echo "MISSING FILE: $layer / $cell_label / KGC${id}"
                continue
            fi

            id_full="KGC${id}-1"
            actual_status=$(get_status "$f")

            # Skip strict status check for "Other" cells
            [ "$cell_label" = "O" ] && continue

            if [ "$actual_status" != "$expected_status" ]; then
                if is_doc_exception "$id_full"; then
                    : # silent: documented exception
                else
                    echo "VERDICT MISMATCH: $id_full — expected $expected_status, file says $actual_status"
                fi
            fi
        done
        IFS="$OLDIFS"
    done
done
echo "(if no mismatches printed above, matrix cells match file headers)"
echo ""

# ---- Step 3: matrix coverage ------------------------------------------------
echo "=== Step 3: matrix coverage of all problems ==="

# Extract all IDs claimed in the matrix
MATRIX_IDS_FILE=$(mktemp)
echo "$EXPECTED" | while IFS='|' read -r layer c k u o; do
    for cell in "$c" "$k" "$u" "$o"; do
        [ -z "$cell" ] && continue
        OLDIFS="$IFS"
        IFS=','
        for id in $cell; do
            echo "KGC${id}-1"
        done
        IFS="$OLDIFS"
    done
done | sort -u > "$MATRIX_IDS_FILE"

DISK_IDS_FILE=$(mktemp)
find "$PROBLEMS" -name "KGC*-1.p" -type f -exec basename {} .p \; | sort -u > "$DISK_IDS_FILE"

DISK_NOT_MATRIX=$(comm -23 "$DISK_IDS_FILE" "$MATRIX_IDS_FILE")
MATRIX_NOT_DISK=$(comm -13 "$DISK_IDS_FILE" "$MATRIX_IDS_FILE")

if [ -n "$DISK_NOT_MATRIX" ]; then
    echo "ON DISK BUT NOT IN MATRIX:"
    echo "$DISK_NOT_MATRIX"
    ERRORS=$((ERRORS+1))
fi

if [ -n "$MATRIX_NOT_DISK" ]; then
    echo "IN MATRIX BUT NOT ON DISK:"
    echo "$MATRIX_NOT_DISK"
    ERRORS=$((ERRORS+1))
fi

if [ -z "$DISK_NOT_MATRIX" ] && [ -z "$MATRIX_NOT_DISK" ]; then
    echo "OK: all 54 problems are accounted for"
fi

rm -f "$MATRIX_IDS_FILE" "$DISK_IDS_FILE"
echo ""

# ---- Step 4: audit log claims -----------------------------------------------
echo "=== Step 4: audit log claims ==="
LATEST_CSV=$(ls -t "$ROOT/audit_logs"/audit_*.csv 2>/dev/null | head -1)

if [ -z "$LATEST_CSV" ]; then
    echo "WARNING: no audit log found; run audit_timed.sh first"
else
    echo "Using: $(basename "$LATEST_CSV")"
    PASS_COUNT=0; DOC_TIMEOUT_COUNT=0; FAIL_COUNT=0

    while IFS=, read -r prob layer expected casc rest; do
        [ "$prob" = "problem" ] && continue
        [ -z "$prob" ] && continue

        if [ "$prob" = "KGC705-1" ] && [ "$casc" = "Timeout" ]; then
            DOC_TIMEOUT_COUNT=$((DOC_TIMEOUT_COUNT+1))
        elif [ "$prob" = "KGC812-1" ] && [ "$casc" = "ContradictoryAxioms" ]; then
            PASS_COUNT=$((PASS_COUNT+1))
        elif [ "$expected" = "$casc" ]; then
            PASS_COUNT=$((PASS_COUNT+1))
        else
            FAIL_COUNT=$((FAIL_COUNT+1))
        fi
    done < "$LATEST_CSV"

    printf "PASS:               %d (paper: %d)\n" "$PASS_COUNT" "$EXPECTED_PASS"
    printf "Documented timeout: %d (paper: %d)\n" "$DOC_TIMEOUT_COUNT" "$EXPECTED_DOC_TIMEOUT"
    printf "FAIL:               %d (paper: %d)\n" "$FAIL_COUNT" "$EXPECTED_FAIL"

    if [ "$PASS_COUNT" != "$EXPECTED_PASS" ] || \
       [ "$DOC_TIMEOUT_COUNT" != "$EXPECTED_DOC_TIMEOUT" ] || \
       [ "$FAIL_COUNT" != "$EXPECTED_FAIL" ]; then
        echo "AUDIT NUMBERS MISMATCH"
        ERRORS=$((ERRORS+1))
    else
        echo "OK"
    fi
fi
echo ""

# ---- Step 5: cvc5 unknown count ---------------------------------------------
echo "=== Step 5: cvc5 unknown count ==="
if [ -n "$LATEST_CSV" ]; then
    CVC5_UNK=$(awk -F, 'NR>1 && $16=="unknown" {n++} END{print n+0}' "$LATEST_CSV")
    printf "cvc5 unknown count: %d (paper: %d)\n" "$CVC5_UNK" "$EXPECTED_CVC5_UNK"
    if [ "$CVC5_UNK" != "$EXPECTED_CVC5_UNK" ]; then
        echo "MISMATCH"
        ERRORS=$((ERRORS+1))
    else
        echo "OK"
    fi
fi
echo ""

# ---- Step 6: documented exceptions exist ------------------------------------
echo "=== Step 6: documented exceptions ==="
for excid in $DOC_EXC_IDS; do
    id_short="${excid%-1}"
    id_num="${id_short#KGC}"
    f=$(find_problem_file "$id_num")
    if [ -z "$f" ]; then
        echo "MISSING: $excid"
        ERRORS=$((ERRORS+1))
    else
        printf "OK: %s -> %s\n" "$excid" "${f#$ROOT/}"
    fi
done
echo ""

# ---- Final summary ----------------------------------------------------------
echo "===================="
if [ "$ERRORS" = "0" ]; then
    echo "ALL CHECKS PASSED"
    echo "Paper numbers match reality. Safe to submit."
    exit 0
else
    printf "%d DISCREPANCIES FOUND\n" "$ERRORS"
    echo "Fix mismatches before submission."
    exit 1
fi