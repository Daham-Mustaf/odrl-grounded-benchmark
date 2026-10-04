# File type: what to fix, and the prose to review

The resource is verified: 228 concepts, no relation of any kind, and
the fifteen PDF names read from the table. Three defects and three
missing fields.

---

## 1. The profile does not parse

`head -c 20 problems/resources/profile-filetype.ttl` will show a
leading backslash. `profile_ttl()` was pasted with `"""\\` where Python
needs `"""\`, so the escape landed in the output.

**In `build_filetype.py`, `profile_ttl()`:** the first line after
`return` must be

```python
    return """\
```

one backslash, and the closing `"""` on its own line.

**Check by parsing, not by eye:**

```bash
uv run python -c "
from rdflib import Graph
print(len(Graph().parse('problems/resources/profile-filetype.ttl',
                        format='turtle')), 'triples')
"
```

Six.

---

## 2. Three fields missing from the three case files

`grep -c 'vrep:binding' cases/KGC32*.ttl` returns 0 for all three.

**In `problem_data_filetype.py`:**

```python
BINDING = "https://w3id.org/odrl-kb/profile/b-fileformat"
```

and `"binding": BINDING,` in each of KGC320, KGC321, KGC322.

**And a `summary` each.** Two sentences: what the offer permits, what
the request commits to. No verdict, no vocabulary.

```python
# KGC320 and KGC321
"summary": ("A library offers material in PDF; a researcher will use "
            "PDF/A-1a. The EU file type table lists both formats and "
            "relates them in no way."),

# KGC322
"summary": ("A library offers material in PDF or PDF/A-1a; a "
            "researcher will use PDF/A-1a."),
```

KGC321's can be shorter, as the consent file does it: "As KGC320, with
the two formats declared distinct."

---

## 3. The titles still name institutions that are not the actors

Six lines. The actors are `drk:library` and `drk:researcher`; the
titles say BSB and BnF.

```
KGC320  Offer: use of material in PDF
        Request: use of material in PDF/A-1a
KGC321  the same two
KGC322  Offer: use of material in PDF or PDF/A-1a
        Request: use of material in PDF/A-1a
```

---

## The prose, reviewed

### KGC320

**Comment, as it stands:**

> Both queries are satisfiable. The models differ on whether the two
> names denote one format. No assertion in the table bears on the
> question, so the verdict reports the authority's silence rather than
> resolving it.

**It opens with the procedure.** "Both queries are satisfiable" is how
the answer was found, not what it rests on, and the rest of the suite
now leads with the resource. Shorter:

> The table lists both formats and relates them in no way, so nothing
> settles whether the two names denote one format.

**The "authority's silence" clause is good** and belongs in
`description`, which already says it.

### KGC321

**Comment, as it stands:**

> The two constraints require one format to be both concepts, and the
> declaration holds them apart. Compare KGC314, where a declaration
> moved a verdict over a resource that also published an order: here
> the declaration is doing all of the work, because the table publishes
> nothing at all.

**The comparison is the best observation in the file** and it is in the
wrong field. A comment says what this verdict rests on; a cross-
reference to another problem is `description`.

**Comment:**

> The parties declare the two formats distinct, so no one format is
> both and the two constraints cannot both be met.

**And move the KGC314 comparison into `description`**, where the
existing text already gestures at it.

### KGC322

**Comment, as it stands:**

> The requested format is among those the offer admits, so the two
> constraints hold together in every structure. Nothing the authority
> published and nothing the parties declared takes part, which is what
> a verdict looks like when identity alone settles it.

**First sentence: keep.** Second: "which is what a verdict looks like
when identity alone settles it" is a general remark about the
framework, not about this problem. Cut it; the `description` makes the
point at length and better.

> The requested format is among those the offer admits, so the two
> constraints hold together. Neither the table nor any declaration
> takes part.

---

## One thing in the docstring worth adding

The claim that the table publishes no relations is now measured, and
the docstring should say how:

> Both serialisations were parsed: filetypes-skos.rdf at 6373 triples
> and filetypes-skos-ap-act.rdf at 22236, each carrying skos:inScheme
> over 228 concepts and no skos:broader, narrower, related, exactMatch
> or broadMatch between any of them.

**And the fifteen PDF concepts were read from the table**, not
recalled. One clause saying so.

---

## Then

```bash
uv run generators/build_filetype.py \
  --table vocabularies/eu-file-type-20260715/filetypes-skos-ap-act.rdf \
  --retrieved 2026-08-18 --out problems --declare-distinct PDF PDFA1A
uv run generators/gen_filetype.py
bash run_verdict.sh 2>/dev/null | grep KGC32
cat cases/KGC321.ttl
```

Three `ok`, and the last one read end to end.