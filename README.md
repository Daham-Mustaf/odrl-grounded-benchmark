# odrl-grounded-benchmark

Constraint pairs over published vocabularies, each with the verdict a
formal semantics for ODRL predicts, and a certificate saying what that
verdict rests on.

This is not a workload for policy engines. No engine competes on it and
no performance is reported. It exists to show that a semantics for
ODRL's constraint fragment can be applied to vocabularies as their
publishers actually write them, and that the answers it yields are the
ones the definitions give.

---

## What a problem is

Two ODRL policies, an offer and a request, whose constraints share one
left operand. A binding says which resource that operand is read
against, at which sort, under which grounding rule, and with which
background theory. From those the generator derives two satisfiability
queries, and the verdict follows from the pair:

    query 1 unsatisfiable, query 2 satisfiable    Incompatible
    query 1 satisfiable, query 2 unsatisfiable    Compatible
    both satisfiable                              Unknown
    a value that does not ground                  Unknown, no query built

Each query is written twice, as TPTP and as SMT-LIB, from one table. Two
provers run both. Where a verdict is definite, their proofs are compared
by the premises they cite, not only by the status they return.

---

## Layout

    vocabularies/     the published files, vendored at a stated version
    generators/       builders (vocabulary to resource) and generators
                      (problem data to queries and cases)
    problems/
      resources/      one slice per resource, plus its profile entry
      background/     what the parties declared, as Turtle
      axioms/         the same, as TPTP
      verdict/        the queries, .p and .smt2
    cases/            one file per problem: the two policies and the
                      expected report
    certificates/     what the provers produced, and what they cited
    vocab/            the schemas for the terms this project mints
    probes/           assertions each binding must and must not entail

---

## Running it

Vocabularies first, then problems, then the two harnesses.

```bash
# resources, from the vendored files
uv run generators/build_dpv.py \
  --purposes vocabularies/dpv-2.3/modules/purposes.ttl \
  --retrieved 2026-08-19 --out problems \
  --declare-distinct Marketing ScientificResearch \
                     ResearchAndDevelopment Advertising

uv run generators/build_dpvloc.py \
  --loc vocabularies/dpv-2.3/loc/loc.ttl \
  --retrieved 2026-08-19 --out problems --declare-distinct DE FR

uv run generators/build_consent.py \
  --module vocabularies/dpv-2.3/modules/consent_status.ttl \
  --retrieved 2026-08-19 --out problems \
  --declare-distinct ConsentGiven ConsentWithdrawn

uv run generators/build_tom.py \
  --tom vocabularies/dpv-2.3/modules/TOM.ttl \
  --measures vocabularies/dpv-2.3/modules/technical_measures.ttl \
  --out problems

uv run generators/build_gdprlb.py \
  --core vocabularies/dpv-2.3/modules/legal_basis.ttl \
  --gdpr vocabularies/dpv-2.3/legal/eu/gdpr/modules/legal_basis.ttl \
  --retrieved 2026-08-19 --out problems

uv run generators/build_filetype.py \
  --table vocabularies/eu-file-type-20260715/filetypes-skos-ap-act.rdf \
  --retrieved 2026-08-18 --out problems --declare-distinct PDF PDFA1A

# problems
for g in gen_motivating gen_dpv gen_dpvloc gen_filetype gen_consent \
         gen_gdprlb gen_tom gen_bcp47_problems gen_wellsorted; do
  uv run generators/$g.py || echo "FAILED $g"
done

# verdicts, and what the refutations cite
bash run_verdict.sh
uv run generators/run_certify.py
uv run generators/check_certificates.py
```

Needs `vampire` and `z3` on the path, and `uv` for the Python.

---

## The problems

    KGC100-112   well-sortedness: six constraints, three rejected at
                 drafting time by the signature alone
    KGC300-302   the motivating example, one per sort
    KGC310-317   purpose, over DPV purposes
    KGC320-323   fileFormat, over the EU file type table
    KGC330-334   spatial, over DPV Locations
    KGC340-347   consent status, over the DPV consent module
    KGC350-353   legal basis, over DPV and its GDPR extension
    KGC360-364   technical and organisational measures
    KGC370-375   language, over a BCP 47 slice
    KGC380-392   spatial again: composition, subdivisions, exclusion
    KGC393-397   purpose again: the set operators

Start with KGC310, KGC313 and KGC314: one published assertion, then the
same operand where the vocabulary settles nothing, then the same pair
once the parties declare the concepts distinct.

---

## What the benchmark found

**An exclusion clause admits a part of what it excludes.** `isNoneOf`
compares by identity, so "anywhere except Wallis and Futuna" permits use
in Uvea, a commune of Wallis and Futuna. KGC392, and KGC397 for the same
over purposes.

**One intention drafted two ways behaves differently.** Enumerating the
accepted values and naming the branch that holds them are both
legitimate, and only the second covers a value the publisher adds later.
KGC393 against KGC395.

**"Only these purposes" is expressible by no ODRL operator** for a use
carrying several. KGC396.

**And a sound verdict can be false about the world.** DPV places Bonaire
under the Netherlands and the Netherlands in the EU; transitivity gives
Bonaire in the EU, which is not the case in law. KGC380, with KGC383 as
the control where the same composition is true.

---

## Licence

The code and the generated artefacts in this repository are released
under **CC BY 4.0**.

The vendored vocabularies are not ours and carry their own terms:

**Data Privacy Vocabulary 2.3** and its extensions, W3C Document
License 2023. The slices under `problems/resources/` are derived from
it.

**EU file type authority table**, Publications Office of the European
Union, CC BY 4.0.

**IANA Language Subtag Registry**, in the public domain as an IETF
registry.

Each generated resource file carries the licence of its source in its
header, with the version and the date it was retrieved.

*[Record here who reviewed the reuse question, on what basis, and when,
so that the next reader does not reopen it.]*

---

## Citing

*[Paper reference once it has one.]*