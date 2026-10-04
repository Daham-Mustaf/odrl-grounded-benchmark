# _report_block: the minimal version

Replaces the current block in `generators/writers.py`. Nine `vrep:` terms,
all defined; nothing about premises, witnesses, or certificate types.

---

## The replacement

```python
# The verdict-to-state mapping, stated once. The vocabulary's header
# carries the same table in prose; if the two ever disagree, the
# vocabulary is right and this is the copy that drifted.
SATISFACTION_STATE = {
    "Compatible":   "report:Satisfied",
    "Incompatible": "report:Unsatisfied",
    "Unknown":      "vrep:Undetermined",
}


def _report_block(p: dict) -> str:
    """The expected report, from the problem's own fields.

    What the report carries and what it does not is the whole of this
    function's design. It carries the verdict, the two constraints it is
    about, the binding that decided the reading, and a reference to the
    evidence. It does not carry the evidence: the premises a refutation
    rests on are named inside the proof artefact, with the res_, bg_ and
    ax_ prefixes the checker reads, and writing them a second time here
    would give one fact two records that can disagree without anything
    noticing.

    Every term emitted is defined in vocab/verdict-report.ttl or
    inherited from the Compliance Report Model. That is checkable, and
    the check belongs in CI: a term in a controlled namespace that its
    schema does not define is a build failure.
    """
    pid = p["id"]
    verdict = expected_verdict(p)

    lines = [
        "### Expected result " + "#" * 55,
        "",
        f"drk:{pid}-report a vrep:OperandVerdictReport ;",
        f'    dcterms:identifier "{pid}" ;',
        f"    report:policy drk:offer-{pid[3:]} ;",
        f"    report:policyRequest drk:request-{pid[3:]} ;",
        f"    report:constraint kgc:{pid}-offer-c1 ;",
        f"    vrep:constraintRequest kgc:{pid}-request-c1 ;",
    ]

    # The binding is what fixed the reading, so a report without one
    # does not say what its verdict was relative to. Problems predating
    # the field omit it rather than name a binding that may be wrong.
    if p.get("binding"):
        lines.append(f"    vrep:binding <{p['binding']}> ;")

    lines.append(f"    report:satisfactionState "
                 f"{SATISFACTION_STATE[verdict]} ;")

    # Required exactly when the state is Undetermined, and meaningless
    # otherwise; the vocabulary makes undeterminedReason functional and
    # domains it on this class.
    if verdict == "Unknown":
        if not p.get("unknown_reason"):
            raise ValueError(
                f"{pid}: Unknown verdict with no unknown_reason. The "
                f"report cannot say whether the value failed to ground "
                f"or the queries were both satisfiable, and those are "
                f"repaired differently.")
        lines.append(f"    vrep:undeterminedReason "
                     f"vrep:{p['unknown_reason'].capitalize()} ;")

    # An ungrounded problem builds no queries, so there is no artefact
    # to point at. The value that failed is recoverable by applying the
    # binding's grounding rule to the constraint named above.
    if p.get("ungrounded"):
        lines[-1] = lines[-1].rstrip(" ;") + " ."
    else:
        which = 1 if p["expected_q1"] == "Unsatisfiable" else 2
        lines.append(f"    vrep:certificate "
                     f"<certificates/{pid}-{which}.tstp> .")

    return "\n".join(lines)
```

---

## What goes with it

**Delete `CERTIFICATE_CLASS`** at line 298. Nothing else uses it.

**The `certificate` dict in the problem data stays as it is.** Its
`kind`, `comment` and `premises` fields are read by `gen_*.py` and by
`run_certify.py`; a Python dict key is not vocabulary. What changes is
only that they no longer reach the case file.

**The TTL writers need the actor names to match.** `_ttl` in each
problem-data file currently emits `drk:bsb-offer-330` while the block
above emits `drk:offer-330`. Change `_ttl`, not the block: the shorter
name is what the earlier decision to drop institutional actors calls for
anyway.

---

## Check afterwards

```bash
uv run generators/gen_dpvloc.py
grep -oh "vrep:[A-Za-z]*" cases/*.ttl | sort -u
```

Nine terms, all in the vocabulary:

    vrep:Epistemic  vrep:OperandVerdictReport  vrep:Undetermined
    vrep:Ungrounded  vrep:binding  vrep:certificate
    vrep:constraintRequest  vrep:undeterminedReason

Anything else is a term the writer invented.

```bash
grep -c "drk:bsb-offer\|drk:bnf-request" cases/*.ttl | grep -v ":0"
```

Empty, once the actor names are unified.

---

## One thing this does not settle

`report:policy` and `report:policyRequest` are inherited from the
Compliance Report Model, and this report subclasses
`report:ConstraintReport`. Whether the parent puts those two properties
on a `PolicyReport` rather than a `ConstraintReport` is worth checking
against the model itself; if it does, they belong on a wrapping
`report:PolicyReport` node rather than here.




Yes — the comment should say what the resource does or does not publish, and what follows. Three parts: what the resource says, what the queries showed, therefore the verdict.

**KGC333, simpler:**

> DPV lists Germany and France and relates them in no way. Nothing says they are the same place and nothing says they are different, so some structures identify them and some keep them apart. The verdict is Undetermined.

**KGC330:**

> DPV places Bonaire within the Netherlands. Every structure admitting that assertion admits a use meeting both constraints, so the verdict is Satisfied.

**KGC334:**

> DPV publishes nothing that separates Germany from France. The parties adopt the rule that ISO 3166 gives one code per area, and on that rule no structure identifies them, so the verdict is Unsatisfied. Withdrawing the rule returns it to Undetermined.

**The pattern:** what the resource publishes, what that leaves open or closes, the verdict. And for a declaration, what withdrawing it would do.

**No "both queries are satisfiable"** — that is machinery, and it says nothing a reader could act on. The resource being silent is the fact; the two satisfiable queries are how the procedure found it.

**Where it goes:** the `comment` field of each problem's `certificate` dict, and `_report_block` emits it as `rdfs:comment` on the report.




# The certificate comments, final

One sentence or two. What the resource publishes, what the parties
declared if anything, and what follows for this pair.

No queries, no models, no refutations: those are how the answer was
found. The comment is what it rests on.

---

## DPV Locations

**KGC330** — isPartOf NL against eq BQ, Compatible

```python
            "comment": "DPV places Bonaire within the Netherlands. On "
                       "that published assertion alone the two "
                       "and both sides get what they asked for.",
```

**KGC331** — isPartOf EU against eq DE, Compatible, jurisdictional binding

```python
            "comment": "DPV places Germany within the European Union, and "
                       "this binding reads union membership as "
                       "containment. On that assertion the two "
                       "constraints can both be met; the geographic "
                       "binding does not read it, and there loc:EU is "
                       "not a concept at all.",
```

**KGC333** — eq DE against eq FR, Undetermined

```python
            "comment": "DPV lists Germany and France and publishes no "
                       "assertion relating or separating them, and the "
                       "parties declare none. Whether the two constraints "
                       "can both be met is therefore not settled.",
```

**KGC334** — the same pair under the ISO rule, Incompatible

```python
            "comment": "DPV publishes no assertion separating Germany from "
                       "France. The parties adopt ISO 3166's rule that one "
                       "code names one area, and on that assertion the two "
                       "constraints cannot both be met. Withdrawing the "
                       "rule returns the pair to unsettled.",
```

---

## DPV purposes

**KGC310** — isA R&D against eq SR, Compatible

```python
            "comment": "DPV places scientific research below research and "
                       "development. On that published assertion alone the "
                       "two constraints can both be met.",
```

**KGC311** — isA Purpose against eq NCR, Compatible

```python
            "comment": "DPV relates non-commercial research to purpose only "
                       "through non-commercial purpose, so the pair rests "
                       "on two published assertions and on transitivity of "
                       "the order.",
```

**KGC313** — eq Marketing against eq SR, Undetermined

```python
            "comment": "DPV lists marketing and scientific research and "
                       "publishes no assertion separating them, and the "
                       "parties declare none. Whether the two constraints "
                       "can both be met is therefore not settled.",
```

**KGC314** — the same pair under a declaration, Incompatible

```python
            "comment": "DPV publishes no assertion separating the two "
                       "purposes. The parties declare them distinct, and on "
                       "that assertion the two constraints cannot both be "
                       "met. Withdrawing the declaration returns the pair "
                       "to unsettled.",
```

**KGC315** — isA Purpose against eq RIS, Compatible

```python
            "comment": "DPV relates interview scheduling to purpose through "
                       "six published assertions and transitivity of the "
                       "order. The verdict is the same as for a single "
                       "step; what grows with the depth is what the "
                       "evidence cites.",
```

**KGC316** — isA RIS against eq Purpose, Undetermined

```python
            "comment": "DPV places interview scheduling below purpose and "
                       "publishes nothing the other way. The order runs in "
                       "one direction, so reversing the two constraints "
                       "leaves the pair unsettled.",
```

**KGC317** — isNoneOf Marketing against eq Marketing, Incompatible

```python
            "comment": "The offer excludes exactly the purpose the request "
                       "requires. No published assertion and no declaration "
                       "takes part: the two constraints contradict each "
                       "other over one concept.",
```

---

## BCP 47

**KGC370** — eq de against eq fr, declared, Incompatible

```python
            "comment": "The registry lists both subtags and publishes no "
                       "assertion separating them. The parties adopt RFC "
                       "5646's rule that one subtag names one language, and "
                       "on that assertion the two constraints cannot both "
                       "be met.",
```

**KGC371** — the same, withdrawn, Undetermined

```python
            "comment": "The registry lists both subtags and publishes no "
                       "assertion separating them, and here the parties "
                       "declare none. Whether the two constraints can both "
                       "be met is therefore not settled.",
```

**KGC372** — eq de against eq "en-US", ungrounded

```python
            "comment": "The value en-US is a well-formed language tag and "
                       "is not a concept of this slice, which holds primary "
                       "subtags. Under this binding's grounding rule it "
                       "resolves to nothing, and the constraint has no "
                       "denotation to evaluate.",
```

**KGC373** — the same, under the reducing rule, Incompatible

```python
            "comment": "Under this binding's grounding rule a tag reduces "
                       "to its primary subtag, so en-US resolves to en. "
                       "The parties' uniqueness rule separates en from de, "
                       "and on that assertion the two constraints cannot "
                       "both be met.",
```

**KGC374** — eq de against neq fr, declared, Compatible

```python
            "comment": "The registry publishes no assertion separating the "
                       "subtags. The parties adopt the uniqueness rule, and "
                       "on that assertion German is a value satisfying both "
                       "constraints. A Compatible verdict can rest on a "
                       "declaration as much as an Incompatible one.",
```

**KGC375** — the same, withdrawn, Undetermined

```python
            "comment": "Without the uniqueness rule, a structure may read "
                       "the two subtags as one language, and then German is "
                       "also French and the request excludes it. Whether "
                       "the two constraints can both be met is not settled.",
```

---

## The shape, for the ones not listed

    <what the resource publishes about these concepts>
    <what the parties declared, if anything>
    <what follows for this pair>

and for a verdict resting on a declaration, one clause on what
withdrawing it does.

Consent, legal basis, measures and file format follow the same pattern.
Their comments should be written against the actual assertions in each
resource, not adapted from these.