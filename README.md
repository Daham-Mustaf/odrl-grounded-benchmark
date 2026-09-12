# odrl-grounded-benchmark

Constraint pairs over published vocabularies, each with the verdict a
formal semantics for ODRL predicts, and a certificate saying what that
verdict rests on.

This is not a workload for policy engines. No engine competes on it and
no performance is reported. It exists to test whether the formal
semantics can be instantiated on vocabularies as their publishers write
them, and whether the implementation produces the verdicts the
definitions prescribe.

---

## What a problem is

Two ODRL policies, an offer and a request, whose constraints share one
left operand. A binding says which resource that operand is read
against, at which sort, under which grounding rule, and with which
background theory. From these the generator derives two satisfiability
queries, and the verdict follows from the pair:

```
query 1 unsatisfiable, query 2 satisfiable    Incompatible
query 1 satisfiable, query 2 unsatisfiable    Compatible
both satisfiable                              Unknown
a value that does not ground                  Unknown, no query built
```

Each completed query is written independently as TPTP and SMT-LIB and
checked by Vampire and Z3. Where a verdict is definite, the two
encodings are compared by the premises their proofs cite, not only by
the status they return.

---

## The files for one problem

Take KGC350. Six files, in three directories.

```
cases/KGC350.ttl                 the two policies, and the verdict
                                 the semantics predicts for them

problems/verdict/KGC350-1.p      query 1, TPTP
problems/verdict/KGC350-1.smt2   query 1, SMT-LIB
problems/verdict/KGC350-2.p      query 2, TPTP
problems/verdict/KGC350-2.smt2   query 2, SMT-LIB

certificates/KGC350-2.tstp       Vampire's proof
certificates/KGC350-2.core       Z3's named unsat core
```

Query 1 asserts the witness condition, the claim that some use
satisfies both constraints. Query 2 negates it.

Only the refuted query has a certificate, and the suffix says which.
KGC350's certificate is for query 2, so query 2 was unsatisfiable and
the verdict is Compatible. An Unknown problem has no certificate: both
queries were satisfiable, so neither was refuted.

The case file references its certificate, so a reader can follow one
link from the verdict to the evidence.

---

## Layout

```
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
design/           modules written against the definitions and not yet
                  wired into the pipeline
```

---

## The problems

```
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
KGC380-392   spatial: composition, subdivisions, exclusion
KGC393-397   purpose: the set operators
```

Start with KGC310, KGC313 and KGC314: one published assertion, then the
same operand where the vocabulary settles nothing, then the same pair
once the parties declare the concepts distinct.

---

## Running it

Vocabularies first, then problems, then the harnesses.

```bash
# resources, from the vendored files
uv run generators/build_dpv.py \
  --purposes vocabularies/dpv-2.3/modules/purposes.ttl \
  --retrieved 2026-08-19 --out problems \
  --declare-distinct Marketing ScientificResearch \
                     ResearchAndDevelopment Advertising

uv run generators/build_dpvloc.py \
  --loc vocabularies/dpv-2.3/loc/loc.ttl \
  --retrieved 2026-08-19 --out problems \
  --declare-distinct DE FR

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
  --retrieved 2026-08-18 --out problems \
  --declare-distinct PDF PDFA1A

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

### In a container

Vampire has no package in most distributions, so the artefact ships a
Dockerfile that pins both provers:

```bash
docker build -t odrl-benchmark .
docker run --rm odrl-benchmark
```

This rebuilds every resource from the vendored vocabularies,
regenerates the problems, and runs both provers over all of them. The
image records the prover versions it holds in `/benchmark/ENVIRONMENT`.

---

## Verdict reports

Expected reports use the [Compliance Report Model](https://w3id.org/force/compliance-report)
(Slabbinck and Esteves, 2024) and extend it with `vrep:`, defined in
`vocab/verdict-report.ttl`. The parent supplies the report structure;
`vrep:` adds only what the semantics needs and the parent lacks:

```
Compatible     report:Satisfied
Incompatible   report:Unsatisfied
Unknown        vrep:Undetermined, with vrep:undeterminedReason
               vrep:Epistemic or vrep:Ungrounded
```

`vrep:OperandVerdictReport` extends `report:ConstraintReport` with the
request-side constraint (`vrep:constraintRequest`), the binding the
verdict was read under (`vrep:binding`), and the evidence
(`vrep:certificate`). `vrep:Undetermined` is a new satisfaction state,
not the parent's `report:Unknown`, which is a performance state.

`validate_terms.py` fails any report using a term neither vocabulary
defines.

---

## Certificates

A definite verdict carries a certificate recording the premises and the
proof artefact it was obtained from. What the certificate is depends on
the result:

```
Incompatible   a refutation of query 1: no use satisfies both
               constraints

Compatible     a refutation of query 2: no admissible structure lacks
               such a use

Unknown        both queries complete satisfiable; the case is open
               under what is published and declared

ungrounded     the value that names no concept of the bound resource;
               no query is built
```

A refutation names the premises it uses, and the prefix says where each
came from:

```
res_      published by the resource
bg_       declared by the parties
ax_       an order axiom: reflexivity, antisymmetry, transitivity
w_        the witness condition, generated from the two constraints
```

So a certificate records what a verdict rests on. KGC310 rests on a
published assertion. KGC314 rests on a party declaration, and
withdrawing that declaration returns the pair to Unknown, which is
KGC313.

`check_certificates.py` reads each refutation and checks whether each
supported step follows from its parent formulas in ground first-order
logic with equality, and that every cited premise occurs in the query.
It invokes no prover. It reports one of:

```
FULLY_CHECKED       every supported step was verified
PARTIALLY_CHECKED   the proof uses machinery the checker does not
                    verify, such as Vampire's AVATAR splitting; the
                    verified steps are still reported
REJECTED            a checked step does not follow, or a cited premise
                    is not in the query
```

Under `certificates/`:

```
<id>-1.tstp / <id>-2.tstp   Vampire's proof for query 1 or 2
<id>-<q>.core               Z3's named unsat core for query q
<id>-observed.ttl           the premises, by provenance class
```

An Unknown verdict's certificate is a pair of satisfying structures.
`run_certify.py` computes the pair and reports which constant the two
models differ on; it does not yet serialise them, so no file is written
and the report names none.

The two encodings are an additional cross-check. TPTP and SMT-LIB are
generated from the same problem data and checked separately, so their
statuses and cited premises can be compared. A disagreement is an
encoding or implementation fault to investigate, not evidence about the
semantics.

---

## What the benchmark found

**An exclusion clause admits a part of what it excludes.** `isNoneOf`
compares values by identity, so "anywhere except Wallis and Futuna"
permits use in Uvea, which the resource places within Wallis and
Futuna. KGC392, and KGC397 for the same over purposes.

**One intention drafted two ways behaves differently.** Enumerating the
accepted values and naming the branch that holds them are both
legitimate, but `isAnyOf` checks the listed values by identity while
the taxonomic branches read the published order. KGC393 against KGC395.

**"Only these purposes" is not expressible for a multi-valued use.**
`isAnyOf` is existential, and `isAllOf` requires the listed denotation
to be contained in the valuation. Neither says what the drafter meant.
KGC396.

**A verdict is relative to its semantic inputs.** DPV places Bonaire
under the Netherlands and the Netherlands in the EU; under the selected
binding, transitivity gives Bonaire in the EU. That is not a statement
about EU territorial law. KGC380, with KGC383 as the control where the
same composition holds.

---

## Licence

The code and the artefacts generated solely from this project's own
source material are released under **CC BY 4.0**.

The vendored vocabularies are not ours and retain their own terms.

**Data Privacy Vocabulary 2.3 and its extensions.** The vendored files
carry licence information in their metadata and source distribution.
The benchmark contains derived resource slices, not verbatim copies.
Before public release of those slices, record the applicable permission
or other clearance from the DPV Community Group. Until that is
recorded, treat the DPV-derived slices as review artefacts rather than
cleared redistributable material.

**EU file type authority table**, Publications Office of the European
Union. Reuse is subject to the terms the Publications Office states for
the dataset. Confirm the applicable terms for the vendored snapshot
before public release and retain the required source acknowledgement.

**IANA Language Subtag Registry.** IANA and IETF state that the
protocol registries may be freely used and that applicable rights held
by IANA or IETF are subject to the CC0 1.0 dedication. That statement
does not eliminate possible third-party rights. See
https://www.iana.org/help/licensing-terms

Each generated resource file carries the source, version, retrieval
date and licence information where available. Those headers are the
authoritative record for the snapshots actually used.

*Before publication, record here who reviewed the reuse terms, on what
basis, and when.*

---

## References

### Standards and vocabularies

* R. Iannella, S. Villata (eds.). *ODRL Information Model 2.2.* W3C
  Recommendation, 15 February 2018.
  https://www.w3.org/TR/odrl-model/

* R. Iannella, M. Steidl, S. Myles, V. Rodríguez-Doncel (eds.).
  *ODRL Vocabulary & Expression 2.2.* W3C Recommendation, 15 February
  2018.
  https://www.w3.org/TR/odrl-vocab/

* A. Miles, S. Bechhofer (eds.). *SKOS Simple Knowledge Organization
  System Reference.* W3C Recommendation, 18 August 2009.
  https://www.w3.org/TR/skos-reference/

* H. J. Pandit, B. Esteves, G. P. Krog, P. Ryan, D. Golpayegani,
  J. Flake. *Data Privacy Vocabulary (DPV), Version 2.0.* In
  *The Semantic Web, ISWC 2024*, LNCS, Springer, 2024, pp. 171-193.
  https://doi.org/10.1007/978-3-031-77847-6_10
  Version 2.3 is used here: https://w3id.org/dpv/2.3

* B. Esteves, H. J. Pandit. *Bridging DPV and ODRL for
  Legally-Oriented Usage Control in Data Spaces.* In *Semantics in
  Dataspaces (SDS)*, CEUR Workshop Proceedings.
  Mapping: https://w3id.org/dpv/mappings/odrl

* W. Slabbinck, B. Esteves. *Compliance Report Model*, Version 0.9.0,
  2024. https://doi.org/10.5281/zenodo.14193486
  The verdict-report vocabulary in `vocab/` extends this model.

* A. Phillips, M. Davis (eds.). *Tags for Identifying Languages.*
  BCP 47, RFC 5646, IETF, September 2009.
  https://www.rfc-editor.org/rfc/rfc5646
  Registry: https://www.iana.org/assignments/language-subtag-registry

* Publications Office of the European Union. *Named Authority List:
  File type.*
  http://publications.europa.eu/resource/authority/file-type

### Tools and formats

* L. Kovács, A. Voronkov. *First-Order Theorem Proving and Vampire.*
  In *CAV 2013*, LNCS 8044, Springer, 2013, pp. 1-35.

* L. de Moura, N. Bjørner. *Z3: An Efficient SMT Solver.* In
  *TACAS 2008*, LNCS 4963, Springer, 2008, pp. 337-340.

* G. Sutcliffe. *The TPTP Problem Library and Associated
  Infrastructure: From CNF to TH0, TPTP v6.4.0.* *Journal of Automated
  Reasoning* 59(4), 2017, pp. 483-502.

* G. Sutcliffe. *The SZS Ontologies for Automated Reasoning Software.*
  In *LPAR 2008 Workshops*, CEUR Vol. 418, 2008.

* C. Barrett, P. Fontaine, C. Tinelli. *The SMT-LIB Standard: Version
  2.6.* 2017. https://smt-lib.org
