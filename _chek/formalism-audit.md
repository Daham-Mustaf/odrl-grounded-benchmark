# Checking the semantics against the implementation

The suite shows the definitions are implementable and that 57 problems
come out as predicted. It does not show the implementation *is* the
definitions. Five places where the two could differ, in the order that
would hurt most if they did.

---

## 1. compile.py — the denotation table

The definitions give one row per operator: what set a constraint
denotes, and in which mode it is satisfied. The compiler has the same
table in code, and nothing checks the two agree.

```bash
grep -n "isA\|isPartOf\|hasPart\|isAnyOf\|isAllOf\|isNoneOf\|\beq\b\|neq" \
  generators/compile.py | head -30
```

**Read each against Definition of the denotation.** Three specific
things to check:

- `hasPart` is the only up-set operator. Its denotation is
  `{x | r ⪯ x}`, not `{x | x ⪯ r}`.
- `isAllOf` is the only superset-mode operator: the constraint's
  denotation lies inside what the use supplies, not the reverse.
- `isNoneOf` is a complement over identity, not over the order — which
  is the finding KGC392 and KGC397 record, so the code must not quietly
  do the order version.

**And the arity table:** which operators take a set and which take one
value. `survey_constraints.py` reports what the problems use; the
signature is what admits them.

---

## 2. The witness condition

The definition says W(K) is the finite disjunction over the concepts the
grounding names, of: c lies in every subset-mode denotation, and every
superset-mode denotation lies in the use.

**Two things that could drift.**

**Which concepts it ranges over.** The definition says the candidate
set; the code builds it from the constraints. KGC318 is the known case
where those differ, and it is not yet built — the `isA NCP × isA RND`
problem that should be Compatible with non-commercial research as
witness and comes out Unknown.

```bash
grep -n "candidate\|def witness\|named_concepts" generators/compile.py
```

**And the emitted form.** The docstrings say the unsimplified
disjunction is emitted, "since that is what the definition prescribes
and what a generator produces mechanically". Check one by hand:

```bash
grep -A4 "^fof(w_kgc310" problems/verdict/KGC310-1.p
```

Against the derivation in `problem_data_dpv.py`'s docstring. They should
match character for character in structure.

---

## 3. signature.py — well-sortedness

The definition says a constraint is well sorted when the operator is
admissible at the binding's sort and the right operand has the arity
the operator takes.

```bash
cat generators/signature.py
```

**Three questions.** Is the admissibility table the one in the paper?
Does `eq` really appear at all three sorts and `isA` at tax only? And
does anything check arity, or only the operator?

The six problems KGC100–112 test three rejections and three
acceptances. That is one instance per sort, not the whole table.

**Worth adding:** a test that walks the full table — every operator at
every sort — and compares against the paper's figure. Twenty-four
cells, decided by the signature alone, in milliseconds.

---

## 4. The order axioms, in both encodings

`KGE000-0.ax` and `SMT_ORDER_AXIOMS` in `writers.py` must be the same
three axioms. The comment says so; nothing checks it.

```bash
cat problems/axioms/KGE000-0.ax
grep -A10 "SMT_ORDER_AXIOMS = " generators/writers.py
```

**Reflexive, antisymmetric, transitive, and nothing else.** An extra
axiom on one side makes the two encodings different theories, and the
prover agreement that your evaluation rests on would stop meaning
anything.

---

## 5. The grounding map

The definition says a binding names a grounding procedure that resolves
a policy value to a concept, and that a value it does not resolve makes
the constraint ungrounded.

**This is the weakest link.** `writers.py` has:

```python
def _resolve(value, p):
    """Recorded in the manifest, not computed: grounding procedures live
    in design/grounding.py and are not wired in."""
    return p.get("grounding", {}).get(value, value)
```

So grounding is asserted per problem, not computed from the binding.
KGC381 is Ungrounded because the problem says so, not because a
procedure failed.

```bash
ls design/grounding.py 2>/dev/null && grep -n "def " design/grounding.py
```

**What to decide:** whether the paper claims grounding is mechanised. If
it does, this needs wiring. If it says the procedures are declared and
the suite records their outcome, that is defensible and should be
stated.

---

## What would strengthen the argument most

**The signature table test**, because it is cheap and it covers the
whole admissibility claim rather than three instances.

**KGC318**, because it is a known divergence between the definition and
the implementation, and building it before the fix documents that the
suite finds such things.

**And a sentence in §7 about what the agreement shows.** Two provers
citing the same premises means the two encodings are one theory. It does
not mean that theory is the paper's. What connects them is that both are
generated from one table in `compile.py`, and that table is what a
reader should check against the definitions.