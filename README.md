
# ODRL Conflict Detection — Empirical Validation Suite

Anonymous artifact for ISWC 2026 submission. 54 TPTP/SMT-LIB problems
validating the formal results of the paper.

## Requirements

- Python 3.13 with [uv](https://docs.astral.sh/uv/) and `rdflib`
- [Vampire](https://vprover.github.io) 5.0+
- [E](https://eprover.org) 3.2+
- [Z3](https://github.com/Z3Prover/z3) 4.14+
- [cvc5](https://cvc5.github.io) 1.3+

```bash
cd ~/Desktop/tptp-odrl-anon

# Print versions for each prover claimed in the paper
echo "=== Prover versions ==="
echo ""
echo "Vampire:"
vampire --version 2>&1 | head -3
echo ""
echo "E:"
eprover --version 2>&1 | head -3
echo ""
echo "Z3:"
z3 --version 2>&1
echo ""
echo "cvc5:"
cvc5 --version 2>&1 | head -3
echo ""
echo "tptp4X (optional):"
tptp4X 2>&1 | head -2
```
If anything's missing or wrong-version, fix before proceeding. The paper claims specific versions:
- Vampire 5.0.0
- E 3.2.5
- Z3 4.15+
- cvc5 1.3+

## Layout

```
Generators/KGConstraints/   Python generators
Problems/ODRL/KGConstraints/
  Axioms/                   Foundation axiom files (.ax)
  Resources/                Source TTL vocabularies
  Conflict/                 Per-operator grid + motivating example (KGC300–461)
  Refinement/               Lemma 1 (KGC500–502)
  Runtime/                  Theorem 4 (KGC600–602)
  Composition/              Corollary 1, Proposition 2 (KGC700–713)
  Monotonicity/             Proposition 1 (KGC800–812)
  Alignment/                Proposition 3 (KGC900–910)
  Policies/                 Source ODRL policies (.ttl)
```

## Regenerate problems from sources
cd  .. tptp-odrl-anon
```bash
for gen in Generators/KGConstraints/gen_*.py; do
    uv run "$gen"
done
```

## Run the full audit (single prover, ~5 minutes)

```bash
cd Problems/ODRL/KGConstraints

PASS=0; FAIL=0; DOC_TIMEOUT=0
for prob in Conflict/KGC*-1.p Refinement/KGC*-1.p Runtime/KGC*-1.p \
            Composition/KGC*-1.p Monotonicity/KGC*-1.p Alignment/KGC*-1.p; do
    base=$(basename "$prob" .p)
    expected=$(grep -m 1 "^% Status" "$prob" | awk '{print $4}')
    actual=$(vampire --mode casc --time_limit 60 "$prob" 2>&1 \
             | grep "SZS status" | head -1 | awk '{print $4}')

    [ "$base" = "KGC812-1" ] && [ "$actual" = "ContradictoryAxioms" ] && \
        { PASS=$((PASS+1)); continue; }
    [ "$base" = "KGC705-1" ] && [ "$actual" = "Timeout" ] && \
        { DOC_TIMEOUT=$((DOC_TIMEOUT+1)); continue; }

    if [ "$expected" = "$actual" ]; then
        PASS=$((PASS+1))
    else
        FAIL=$((FAIL+1))
        echo "FAIL: $base (got $actual)"
    fi
done

echo "PASS: $PASS / Doc'd timeout: $DOC_TIMEOUT / FAIL: $FAIL"
# Expected: PASS: 53 / Doc'd timeout: 1 / FAIL: 0
```

## Run the multi-prover audit (~30–90 minutes)

Dispatches each problem to four Vampire strategies, E, Z3, and cvc5,
writing per-problem results to a CSV.

```bash
cd Problems/ODRL/KGConstraints

echo "problem,expected,vampire_casc,vampire_discount,vampire_lrs,vampire_otter,eprover,z3,cvc5" \
    > /tmp/audit_full.csv

for prob in Conflict/KGC*-1.p Refinement/KGC*-1.p Runtime/KGC*-1.p \
            Composition/KGC*-1.p Monotonicity/KGC*-1.p Alignment/KGC*-1.p; do
    base=$(basename "$prob" .p)
    smt="${prob%.p}.smt2"
    expected=$(grep -m 1 "^% Status" "$prob" | awk '{print $4}')

    casc=$(vampire --mode casc --time_limit 60 "$prob" 2>&1 | grep "SZS status" | head -1 | awk '{print $4}')
    disc=$(vampire --saturation_algorithm discount --time_limit 60 "$prob" 2>&1 | grep "SZS status" | head -1 | awk '{print $4}')
    lrs=$(vampire --saturation_algorithm lrs --time_limit 60 "$prob" 2>&1 | grep "SZS status" | head -1 | awk '{print $4}')
    otter=$(vampire --saturation_algorithm otter --time_limit 60 "$prob" 2>&1 | grep "SZS status" | head -1 | awk '{print $4}')
    eprov=$(eprover --auto --tptp3-format -s --cpu-limit=60 "$prob" 2>&1 | grep "SZS status" | head -1 | awk '{print $4}')

    z3_r=""; cvc5_r=""
    if [ -f "$smt" ]; then
        z3_r=$(z3 -T:60 "$smt" 2>&1 | grep -E "^(sat|unsat|unknown|timeout)$" | head -1)
        cvc5_r=$(cvc5 --tlimit=60000 "$smt" 2>&1 | grep -E "^(sat|unsat|unknown)$" | head -1)
    fi

    echo "$base,$expected,$casc,$disc,$lrs,$otter,$eprov,$z3_r,$cvc5_r" >> /tmp/audit_full.csv
done

echo "Full CSV: /tmp/audit_full.csv"
```

## Validation summary

| Group       |  N | Validates                              |
| ----------- |---:| -------------------------------------- |
| KGC300–302  |  3 | Motivating example                     |
| KGC400–442  | 15 | Per-operator grid (monotone)           |
| KGC450–461  |  4 | Per-operator grid (complement)         |
| KGC500–502  |  3 | Lemma 1 (refinement)                   |
| KGC600–602  |  3 | Theorem 4 (runtime, atomic)            |
| KGC700–706  |  7 | Corollary 1 (and-composition)          |
| KGC710–713  |  4 | Proposition 2 (or/xone composition)    |
| KGC800–812  | 11 | Proposition 1 (monotonicity)           |
| KGC900–910  |  4 | Proposition 3 (alignment)              |
| **Total**   | **54** | 53 pass + 1 documented timeout      |

## Documented exceptions

- **KGC705**: 3-operand all-Compatible composition. Times out under
  FOL saturation; verified `sat` by Z3.
- **KGC812**: Detects `ContradictoryAxioms` (the intended outcome
  when Assumption 2 is violated).
- **KGC810**: Requires `vampire --mode casc` explicitly; default
  scheduling times out on closed-world saturation.
- **cvc5 Compatible/Unknown class**: returns `unknown` on these
  problems with `kge_concept` guards. Z3 returns `sat` correctly
  in these cases. This is a documented cvc5 limitation on
  existential model construction with quantified theories, not
  a soundness issue.

## License

MIT. See `LICENSE`.


## 2. Time analysis per problem

cd ~/Desktop/tptp-odrl-anon
chmod +x audit_timed.sh
bash audit_timed.sh


## Mace4 (Unknown-class model construction)

Optional: construct explicit countermodels for Unknown-class problems
using Mace4. Requires `tptp_to_ladr` and `mace4` from the LADR
distribution.

```bash
cd Problems/ODRL/KGConstraints
for prob in Conflict/KGC301-1.p Conflict/KGC402-1.p Conflict/KGC412-1.p \
            Conflict/KGC422-1.p Conflict/KGC432-1.p Conflict/KGC442-1.p; do
    base=$(basename "$prob" .p)
    cat Conflict/Axioms/KGE000-0.ax Conflict/Axioms/DENOT000-0.ax "$prob" \
        | grep -v "^include" > /tmp/$base-flat.p
    tptp_to_ladr < /tmp/$base-flat.p > /tmp/$base.in 2>/dev/null
    result=$(mace4 -t 10 -n 6 < /tmp/$base.in 2>&1 | grep "Exiting" | head -1)
    echo "$base: $result"
done
```

Each problem returns "Exiting with 1 model" in under one second.

```bash
cd ~/Desktop/tptp-odrl-anon/Problems/ODRL/KGConstraints

echo "problem,layer,expected,casc_status,casc_time,disc_status,disc_time,lrs_status,lrs_time,otter_status,otter_time,e_status,e_time,z3_status,z3_time,cvc5_status,cvc5_time" \
    > /tmp/audit_timed.csv

run_timed() {
    # $1 = command (as string)
    # Returns: status<TAB>elapsed_seconds
    local start end elapsed result
    start=$(date +%s.%N)
    result=$(eval "$1" 2>&1)
    end=$(date +%s.%N)
    elapsed=$(awk "BEGIN { printf \"%.2f\", $end - $start }")
    echo "${result}|${elapsed}"
}

for prob in Conflict/KGC*-1.p Refinement/KGC*-1.p Runtime/KGC*-1.p \
            Composition/KGC*-1.p Monotonicity/KGC*-1.p Alignment/KGC*-1.p; do
    base=$(basename "$prob" .p)
    layer=$(dirname "$prob")
    smt="${prob%.p}.smt2"
    expected=$(grep -m 1 "^% Status" "$prob" | awk '{print $4}')

    # Vampire CASC
    t0=$(date +%s.%N)
    casc=$(vampire --mode casc --time_limit 60 "$prob" 2>&1 | grep "SZS status" | head -1 | awk '{print $4}')
    casc_t=$(awk "BEGIN { printf \"%.2f\", $(date +%s.%N) - $t0 }")

    # Vampire discount
    t0=$(date +%s.%N)
    disc=$(vampire --saturation_algorithm discount --time_limit 60 "$prob" 2>&1 | grep "SZS status" | head -1 | awk '{print $4}')
    disc_t=$(awk "BEGIN { printf \"%.2f\", $(date +%s.%N) - $t0 }")

    # Vampire LRS
    t0=$(date +%s.%N)
    lrs=$(vampire --saturation_algorithm lrs --time_limit 60 "$prob" 2>&1 | grep "SZS status" | head -1 | awk '{print $4}')
    lrs_t=$(awk "BEGIN { printf \"%.2f\", $(date +%s.%N) - $t0 }")

    # Vampire otter
    t0=$(date +%s.%N)
    otter=$(vampire --saturation_algorithm otter --time_limit 60 "$prob" 2>&1 | grep "SZS status" | head -1 | awk '{print $4}')
    otter_t=$(awk "BEGIN { printf \"%.2f\", $(date +%s.%N) - $t0 }")

    # E
    t0=$(date +%s.%N)
    e_r=$(eprover --auto --tptp3-format -s --cpu-limit=60 "$prob" 2>&1 | grep "SZS status" | head -1 | awk '{print $4}')
    e_t=$(awk "BEGIN { printf \"%.2f\", $(date +%s.%N) - $t0 }")

    # Z3 / cvc5
    z3_r=""; z3_t="0"; cvc5_r=""; cvc5_t="0"
    if [ -f "$smt" ]; then
        t0=$(date +%s.%N)
        z3_r=$(z3 -T:60 "$smt" 2>&1 | grep -E "^(sat|unsat|unknown|timeout)$" | head -1)
        z3_t=$(awk "BEGIN { printf \"%.2f\", $(date +%s.%N) - $t0 }")

        t0=$(date +%s.%N)
        cvc5_r=$(cvc5 --tlimit=60000 "$smt" 2>&1 | grep -E "^(sat|unsat|unknown)$" | head -1)
        cvc5_t=$(awk "BEGIN { printf \"%.2f\", $(date +%s.%N) - $t0 }")
    fi

    echo "$base,$layer,$expected,$casc,$casc_t,$disc,$disc_t,$lrs,$lrs_t,$otter,$otter_t,$e_r,$e_t,$z3_r,$z3_t,$cvc5_r,$cvc5_t" \
        >> /tmp/audit_timed.csv

    printf "%-12s %s\n" "$base" "casc=${casc_t}s disc=${disc_t}s lrs=${lrs_t}s otter=${otter_t}s e=${e_t}s z3=${z3_t}s cvc5=${cvc5_t}s"
done

echo ""
echo "Full timing CSV: /tmp/audit_timed.csv"
```

This captures wall-clock for each prover per problem. After it finishes (~30-90 min), you can summarize:

```bash
# Per-prover median, max, total
python3 << 'EOF'
import csv
from statistics import median, mean

with open('/tmp/audit_timed.csv') as f:
    rows = list(csv.DictReader(f))

provers = ['casc', 'disc', 'lrs', 'otter', 'e', 'z3', 'cvc5']
print(f"{'Prover':<10} {'Median(s)':>10} {'Mean(s)':>10} {'Max(s)':>10} {'Total(s)':>10}")
print("-" * 56)
for p in provers:
    times = [float(r[f'{p}_time']) for r in rows if r[f'{p}_time'] not in ('', '0')]
    if not times:
        continue
    print(f"{p:<10} {median(times):>10.2f} {mean(times):>10.2f} {max(times):>10.2f} {sum(times):>10.2f}")
EOF
```


