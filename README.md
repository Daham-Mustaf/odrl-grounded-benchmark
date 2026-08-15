# A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL

Artefact for the paper. Each problem is decided by two satisfiability
queries, and each answer carries a certificate that can be checked without
repeating the decision.

## What is here

    generators/          the code that writes everything below
    problems/
      axioms/            the shared theory and the resource axiom files
      resources/         R, what each authority published
      background/        B, what the parties declare
      verdict/           two queries per problem
      wellsorted/        the drafting-time check; no queries
      stability/         paired runs under a growing background theory
    cases/               one file per problem: the two policies and the
                         expected report, in one graph
    ontology/            the verdict-report vocabulary

## Requirements

Python 3.13 with [uv](https://docs.astral.sh/uv/) and `rdflib`, plus at least
one prover:

    Vampire 5.0+     https://vprover.github.io
    E 3.2+           https://eprover.org
    Z3 4.14+         https://github.com/Z3Prover/z3
    cvc5 1.3+        https://cvc5.github.io

## The two queries

A verdict is not asserted in the theory. It is read off two satisfiability
results, where `W` is the witness condition for the constraints on one
operand:

    R + B + W        unsatisfiable   ->  Incompatible
    R + B + not W    unsatisfiable   ->  Compatible
    both satisfiable                 ->  Unknown
    grounding fails, no query built  ->  Unknown

A solver reporting `unknown` is an implementation outcome and is not the
verdict Unknown. The queries lie in the Bernays-Schoenfinkel class and are
decidable; an implementation may still impose resource limits.

## Run

    uv run generators/gen_all_axioms.py
    uv run generators/gen_motivating.py
    bash run_verdict.sh

`run_verdict.sh` runs both queries of each problem, derives the verdict from
the pair, and compares it with the expected verdict recorded in the problem
headers.

    PROBLEM    QUERY-1        QUERY-2        VERDICT        CHECK
    KGC300     unsat/unsat    sat/sat        Incompatible   ok
    KGC301     sat/sat        sat/sat        Unknown        ok
    KGC302     sat/sat        unsat/unsat    Compatible     ok

These three are the motivating example of the paper, one per sort.

## Certificates

Every verdict carries evidence. Run a query with proof output to see it:

    cd problems
    vampire --mode casc --proof on verdict/KGC300-1.p

The refutation of the language pair uses two premises: the witness condition
and one background-theory assertion, that `bcp:de` and `bcp:fr` are distinct.
No premise comes from the resource. A party may withdraw the registry
uniqueness rule and reopen the verdict without disputing the registry, which
is what the paper means by contesting a convention.

`cases/KGC300.ttl` records the same thing as RDF, with `vrep:premiseSource`
distinguishing resource premises from background-theory premises.

## Resources

Three slices, one per sort, each with its publication metadata.

    bcp47        nom   15 primary language subtags, no relations
    dpv-purpose  tax   15 purposes under subsumption
    geonames     mer   15 regions under containment

Each resource holds only what its authority published. Rules the parties
adopt, such as registry uniqueness or sibling disjointness, live in
`problems/background/`. Keeping them apart is what lets a refutation say
which of its premises a party could withdraw.

## Anonymity

    ODRL_ANON=1 uv run generators/gen_motivating.py

renders author, source and citation as anonymous in every generated file.

## License

MIT.