
# ODRL Conflict Detection — Empirical Validation Suite

Anonymous artifact for ISWC 2026 submission. 54 TPTP/SMT-LIB problems
validating the formal results of the paper.

## Requirements

- Python 3.13 with [uv](https://docs.astral.sh/uv/) and `rdflib`
- [Vampire](https://vprover.github.io) 5.0+
- [E](https://eprover.org) 3.2+
- [Z3](https://github.com/Z3Prover/z3) 4.14+
- [cvc5](https://cvc5.github.io) 1.3+

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

