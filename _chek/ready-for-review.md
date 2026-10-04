# Getting the policies ready for review

Beatriz will read case files. Each should stand alone: the two policies,
the binding, the verdict, and one sentence saying why. What follows is
what is missing, in the order that unblocks the most.

---

## 1. Two generators still fail

Until they run, their case files are from before today's changes and she
would read old policies.

    problem_data_filetype.py   KGC320   "unknown_reason": "epistemic",
    problem_data_gdprlb.py     KGC351   "unknown_reason": "epistemic",

Both are epistemic: the resource lists the concepts and separates
nothing.

Then check the third:

```bash
uv run generators/gen_bcp47_problems.py 2>&1 | tail -3
```

It failed earlier on an undefined `EMPTY_BT`.

---

## 2. The legal-basis problems, first

She raised `isAnyOf` over Article 6, so KGC350 to KGC353 are where she
will start. They need what the newer problems have.

```bash
grep -c '"summary"\|"binding"' generators/problem_data_gdprlb.py
```

**Zero means all four lack both.** Each needs:

- `"binding": BINDING` with the profile IRI the profile file defines
- `"summary"`, two sentences: what the controller permits, what the
  processor commits to
- titles without BSB and BnF, if they still carry them
- and the certificate comment in the plain register: what the resource
  publishes, what the parties declared, what follows

**And one thing to decide before she reads them.** The docstring says
the offer is taken verbatim from the ODRL regulatory profile. That is
the right defence of `isAnyOf` and it should be visible in the case file
too, not only in the Python source. Either the summary says it, or the
policy carries `odrl:profile` naming the regulatory profile — which it
should anyway, since it uses that profile's encoding.

---

## 3. Everything regenerates and passes

```bash
for g in gen_motivating gen_dpv gen_dpvloc gen_filetype gen_consent \
         gen_gdprlb gen_tom gen_bcp47_problems gen_wellsorted; do
  uv run generators/$g.py >/dev/null 2>&1 || echo "FAILED $g"
done
bash run_verdict.sh 2>/dev/null | tail -2
uv run generators/validate_terms.py --schemas vocab --instances cases
```

Three clean outputs: no FAILED, `fail 0`, and every term defined.

---

## 4. A README in cases/

She will open a directory of sixty files. One page saying what a case
file is, and which to read first.

```markdown
# Case files

One file per problem. Each holds two ODRL policies, an offer and a
request, and the report the semantics produces for them: the verdict,
the binding that fixed the reading, and one sentence saying what the
resource publishes about the concepts involved and what follows.

The policies can be read without the semantics. The binding IRI
dereferences to a profile entry in problems/resources/, which names the
resource, the sort, the grounding rule and the background theory.

## Where to start

KGC310  purpose, one published assertion, Compatible
KGC313  the same operand where the vocabulary settles nothing
KGC314  and the same pair once the parties declare the concepts distinct

## The legal-basis problems

KGC350 to KGC353 take their offer verbatim from the ODRL regulatory
compliance profile's encoding of Article 6(1). The constraint under test
is one a published profile wrote.

## What the benchmark found

KGC392, KGC397   isNoneOf excludes by identity, so an exclusion clause
                 admits a part of the excluded concept
KGC393, KGC395   one intention drafted two ways, behaving differently
KGC396           "only these purposes" is expressible by no operator
KGC380, KGC383   the same composition, false in one case and true in
                 the other
```

---

## 5. What not to do before sending

**Do not change the legal-basis problems' operators.** Whether `isAnyOf`
stays is her question, and presenting a fixed version pre-empts the
answer she offered to give.

**Do not add TOM's KGC362 to 364.** They are unbuilt and unreviewed, and
three more problems is not what she asked for.

**Do not rewrite the older descriptions wholesale.** The ones from
earlier sessions are longer and in a different register than today's,
and that inconsistency is visible but harmless. Fix the four she will
read; leave the rest.

---

## Order

1. Two `unknown_reason` lines, and whatever `gen_bcp47_problems` needs.
2. The four legal-basis problems: binding, summary, titles, comment.
3. Regenerate, run, check terms.
4. README in `cases/`.
5. Push, and reply to her.