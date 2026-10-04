# Language: what was done, what was computed, what to check by hand

Everything below is checkable in one command or by reading one file. The
right-hand column is what you should see.

---

## 1. The registry snapshot

    head -1 vocabularies/bcp47-20260826/language-subtag-registry.txt
    sha256sum vocabularies/bcp47-20260826/language-subtag-registry.txt | cut -c1-16

Expect `File-Date: 2026-08-08` and `be21e91b6851f750`.

**Why it matters:** the resource header cites both. If they do not match,
the axiom file describes a snapshot nobody has.

---

## 2. The slice, and whether it is clean

    F=vocabularies/bcp47-20260826/language-subtag-registry.txt
    for t in bg cs da de el en es fi fr hu it nl pl pt sv; do
      awk -v RS='%%' -v t="$t" '$0 ~ "Subtag: "t"\n"' $F |
        grep -cE "^(Deprecated|Preferred-Value|Macrolanguage|Scope):" |
        tr '\n' ' '
    done; echo

Expect fifteen zeros.

**Why it matters:** the distinctness rule is false for a deprecated subtag
with a Preferred-Value (the he/iw case), and the nominal sort is wrong for
a subtag with a Macrolanguage. The builder aborts on either, so a clean
result here is what makes both claims true rather than assumed.

---

## 3. The two axiom files

    grep -c "^fof" problems/axioms/BCP47000-0.ax    # 15
    grep -c "^fof" problems/axioms/BCP47001-0.ax    # 105
    grep -c "kge_leq" problems/axioms/BCP47000-0.ax # 0
    grep -m1 "^fof" problems/axioms/BCP47001-0.ax

The last should read `bg_dist_bcp47_bg_cs, axiom, bcp_bg != bcp_cs`.

**Why it matters:** zero `kge_leq` is the claim that a registry publishes
no order, made checkable. The `bg_dist_` prefix is what makes a refutation
citing one of these visibly rest on a declaration rather than on IANA.

**What changed:** the old file had 105 `kge_disjoint` facts in the same
file as the concepts. `kge_disjoint` is not declared in KGE000-0.ax, so a
prover read them as an uninterpreted predicate and learned nothing:

    grep -c "kge_disjoint" problems/axioms/KGE000-0.ax   # 0

They were also stored one direction only, which would have needed a
symmetry axiom that does not exist. Built-in `!=` is symmetric for free.

---

## 4. The census

    uv run generators/census.py problems/resources/bcp47.ttl

Expect: 15 declared concepts, no order candidate, 0 separation
assertions, 0 retired.

**Why it matters:** this is the nominal row of the resource table, and it
is the first time the file has been surveyed at all. Before the SKOS
conversion, `census.py` could not see it: the concepts were typed
`odrlkb:LanguageTag`, which the tool does not recognise, so it would have
reported one concept.

---

## 5. The four problems

    bash run_verdict.sh | grep KGC37

Expect:

    KGC370   unsat/unsat   sat/sat     Incompatible   ok
    KGC371   sat/sat       sat/sat     Unknown        ok
    KGC373   unsat/unsat   sat/sat     Incompatible   ok

KGC372 does not appear. It has no queries:

    ls problems/verdict/KGC372*        # nothing
    ls cases/KGC372.ttl                # exists

**Why it matters:** an ungrounded problem produces zero queries by design.
If KGC372 had a tree, the value would become a constant of the signature,
both queries would be satisfiable, and the verdict would be Unknown for
the epistemic reason instead of the ungrounded one. The test would pass
while demonstrating the opposite of what it exists for.

---

## 6. The three pairs, by hand

**370 against 371** — the same policies, one include line apart:

    diff <(grep include problems/verdict/KGC370-1.p) \
         <(grep include problems/verdict/KGC371-1.p)

One line: `BCP47001-0.ax`. That single line is the difference between
Incompatible and Unknown.

**372 against 373** — the same policies, one binding apart:

    diff cases/KGC372.ttl cases/KGC373.ttl

Should differ only in identifiers and in which profile is cited. Under the
exact rule "en-US" resolves to nothing; under the reducing rule it
resolves to `bcp_en`.

**371 against 372** — two Unknowns:

    grep -h "undeterminedReason\|unknownReason" cases/KGC371.ttl cases/KGC372.ttl

One epistemic, one ungrounded. A declaration settles the first and does
nothing for the second.

---

## 7. Numbers, and where each came from

| number | value | source |
|---|---|---|
| concepts in the slice | 15 | counted from the TTL by the builder |
| distinctness pairs | 105 | 15 choose 2, checked against `bt:pairCount` |
| order assertions | 0 | the builder emits none and verifies why |
| language subtags in the registry | 8276 | `grep -c "^Type: language"` |
| Macrolanguage fields | 453 | counted by the builder over language records |

**The last one is worth noting.** A grep for `^Macrolanguage:` gives 545,
because `extlang` records carry the field too. 453 is the count over
language subtags, which is the relevant one, and the builder computes it
each run rather than carrying a typed number.

---

## 8. What is claimed but not yet verified

**That "en-US" is really ungrounded.** The problem asserts it and the
pipeline believes it. Nothing applies the binding's grounding rule to the
value and confirms it resolves to nothing, because grounding procedures
live in `design/grounding.py` and are not wired in.

**That KGC373's `bcp_en` came from the reduction.** The tree names the
constant directly, so the compiled problem never runs the rule it exists
to exercise. Making it honest means recording the resolution in the
manifest and having the generator apply it.

**And the report blocks in the case files use undefined terms.** That is
`_report_block` in `writers.py`, and it needs `vocab/verdict-report.ttl`
to exist first.

Those three are the language work that is not finished. Everything above
them is.