# The benchmark pipeline, end to end

Nine stages. Each has a file that does it and a command that checks it.
The order matters: every stage reads what the one before it wrote, so a
defect at stage 2 surfaces as a wrong verdict at stage 7.

---

## 1. The published vocabulary

**What.** A file as its authority publishes it, vendored unchanged.

    vocabularies/dpv-2.3/loc/loc.ttl
    vocabularies/dpv-2.3/modules/purposes.ttl
    vocabularies/bcp47-20260826/language-subtag-registry.txt
    vocabularies/eu-file-type-20260715/filetypes-skos-ap-act.rdf

**Check.** Is it there, and is it the version the resource claims?

    ls -la vocabularies/*/
    grep -rn "sha256\|dcterms:issued" problems/resources/*.ttl | head

**Known gap.** GeoNames has no vendored source. Its slices were built
from files that no longer exist.

---

## 2. The census

**What.** Measures the file before anything reads it: how many concepts,
which predicates could be an order, how deep, what identity and
separation it publishes.

    generators/census.py

**Check.**

    uv run generators/census.py vocabularies/dpv-2.3/loc/loc.ttl

**Why it is first.** Every number in a builder's `EXPECT` block and every
count in the paper comes from here. A claim not measured here is a claim
nobody measured.

---

## 3. The builder: vocabulary to resource

**What.** Reads the vendored file, decides which published relations to
take, and writes three things: the resource, its axioms, and a profile.

    generators/build_dpvloc.py    -> problems/resources/dpvloc-{geo,juris}.ttl
                                     problems/axioms/LOC-dpvloc-{geo,juris}.ax
                                     problems/resources/profile-dpvloc-*.ttl
                                     problems/background/dpvloc-{empty,iso}.ttl
    generators/build_bcp47.py     -> the same shape for BCP 47

**This is where the paper's central decision is made.** DPV publishes
`skos:broader` for five different things; the builder partitions them and
the profile declares which partition is read as the order.

**Check.**

    uv run generators/build_dpvloc.py \
      --loc vocabularies/dpv-2.3/loc/loc.ttl \
      --retrieved 2026-08-19 --out problems

It must complete and print the partition. An `EXPECT` mismatch aborts it,
which is the point: the description would otherwise be false of the file.

---

## 4. The binding

**What.** A profile file says, for one operand: which resource, at which
sort, under which grounding rule, with which background theory.

    problems/resources/profile-*.ttl

**Check that they parse and that nothing dangles.**

    uv run generators/validate_bindings.py --probes probes \
      --axioms problems/axioms

The probes are the binding's stated meaning, checked against the files:
Bonaire is within the Netherlands and not the reverse, `loc:EU` is absent
from the geographic reading, and so on.

---

## 5. The problem

**What.** A pair of constraint sets, a declared expectation, and the TTL
of the two policies.

    generators/problem_data_*.py

Each problem names its `resource`, `sort`, `background_theory`,
`binding`, and `includes`. The `tree` is the constraints; the `ttl` is
what the case file shows.

**Check that the two agree.**

    uv run generators/survey_constraints.py

It reads the case files, so a tree and a TTL that disagree show up as an
operand or operator the survey reports and the problem data does not.

---

## 6. Compilation: constraints to a formula

**What.** The witness condition, built from the tree and the sort.

    generators/compile.py       the denotations and the witness condition
    generators/tree_expand.py   grounding, constants, the SMT blocks
    generators/signature.py     which operators are well sorted at which sort

**The order inside `expand_tree`:** apply the grounding map, collect the
constants, check they are well-formed, compile the witness, derive the
SMT resource and background blocks from the included axiom files.

**This is where the Definition 9 question lives.** The witness ranges
over the constants the constraints name; whether it should range over the
resource's concepts is the open repair.

---

## 7. Writing the queries

**What.** Two query files per problem in each encoding.

    generators/writers.py    -> problems/verdict/<id>-1.p    R + B + W
                                problems/verdict/<id>-1.smt2
                                problems/verdict/<id>-2.p    R + B + not W
                                problems/verdict/<id>-2.smt2
                                cases/<id>.ttl

**The TPTP side gets the axioms by `include`; the SMT side has no
include**, so the assertions are inlined by `assertions_for`. When those
two disagree, the provers disagree, which is what happened to eight
problems until this was fixed.

**Check.**

    for g in gen_motivating gen_dpv gen_dpvloc gen_filetype gen_consent \
             gen_gdprlb gen_tom gen_bcp47_problems gen_wellsorted; do
      uv run generators/$g.py >/dev/null 2>&1 || echo "FAILED $g"
    done

---

## 8. Deciding

**What.** Both queries, both provers, the verdict read off the pair.

    run_verdict.sh              the regression: 36 problems, expected verdicts
    generators/run_certify.py   both provers, premises, disagreements

**Check.**

    bash run_verdict.sh | tail -3
    uv run generators/run_certify.py 2>&1 | grep -c "STATUS DISAGREEMENT"

`pass 36 fail 0` means each problem's derived verdict matches its
declared one. It does **not** mean the two provers agree on how they got
there; that is the second command.

---

## 9. What the paper reports

Verdicts by sort and resource, the withdrawal pairs, the two readings of
one file, the ungrounded pair, and the two-prover agreement.

---

## The check that runs the whole thing

    uv run generators/census.py vocabularies/dpv-2.3/loc/loc.ttl
    uv run generators/build_dpvloc.py --loc vocabularies/dpv-2.3/loc/loc.ttl \
      --retrieved 2026-08-19 --out problems
    uv run generators/build_bcp47.py ...
    for g in generators/gen_*.py; do uv run $g >/dev/null || echo "FAILED $g"; done
    uv run generators/validate_bindings.py --probes probes --axioms problems/axioms
    uv run generators/survey_constraints.py
    bash run_verdict.sh | tail -3
    uv run generators/run_certify.py 2>&1 | grep -c "STATUS DISAGREEMENT"

**Seven commands.** If all seven are clean, the artefact is coherent from
the vendored file to the verdict.

---

## Where each kind of defect shows up

**A wrong reading of the vocabulary** -> stage 3, and the probes at stage
4 catch it.

**A tree and a TTL that disagree** -> stage 5, and only the survey catches
it.

**An assertion on one encoding and not the other** -> stage 7, and it
surfaces as a prover disagreement at stage 8.

**A wrong expectation** -> stage 8, as a failing problem.

**And a verdict right for the wrong reason** -> nothing catches it. That
is what the certificate comparison would have done.