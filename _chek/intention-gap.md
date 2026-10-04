# Sound verdicts, wrong intentions

Five problems in the suite where the evaluation is faithful to what the
policy says and contrary to what its author meant. Each names a
different cause, and together they are the strongest thing §7 has.

---

## 1. KGC392 — exclusion by identity, not by parthood

    offer    isNoneOf (loc:WF)      anywhere except Wallis and Futuna
    request  eq loc:WF-UV           in Uvea

**Compatible.** `isNoneOf` excludes the named concept. Uvea is a
different concept under the ISO rule, so it lies in the complement.

**The drafter meant** the complement of a down-set: not in Wallis and
Futuna, nor in any part of it. Uvea is a commune of Wallis and Futuna,
and DPV records it as such.

**Why it is interesting.** The exclusion clause is the most common
shape in real licensing, and it fails silently. Nothing warns the
drafter; the policy is well formed, the operator is admissible at the
sort, and the verdict is correct. What is missing is an operator, and
naming which one is a specification finding rather than a semantic one.

---

## 2. KGC397 — the same, over purposes

    offer    isNoneOf (dpv:Marketing)    any purpose except marketing
    request  eq dpv:Advertising          advertising

**Compatible**, and DPV places advertising below marketing.

**Why the pair matters more than either alone.** Two operands, two
vocabularies, two sorts, one cause. A reader seeing only KGC392 may take
it for a quirk of the locations file; seeing both, the cause is visibly
the operator.

**And it is the case for `isNotA`.** The ODRL community has discussed
an operator testing the complement of a down-set. These two problems are
the argument for it, with data.

---

## 3. KGC393 against KGC395 — one intention, two drafts

    KGC393  isAnyOf (RnD, Marketing)    x  eq ScientificResearch  -> Unknown
    KGC395  or(isA RnD, isA Marketing)  x  eq ScientificResearch  -> Compatible

**Both drafts express "use for research and development or marketing".**
The first enumerates values; the second names branches. DPV places
scientific research below research and development.

**KGC393 is Unknown** because `isAnyOf` tests identity and does not read
the order. **KGC395 is Compatible** because `isA` does.

**Why it is the most useful of the five.** It is not a defect. Both
drafts are legitimate and they behave differently under vocabulary
growth: the branch-naming draft covers a purpose DPV adds tomorrow, the
enumerating draft does not. A drafter choosing between them is choosing
whether to defer to the authority, and until now nothing made that
choice visible. The certificates do: KGC395 cites a published assertion,
KGC393 cites none.

**And KGC394 sharpens it.** Under declared distinctness, KGC393 becomes
Incompatible — the enumerating draft is not merely weaker, it is
refuted, and by a declaration a drafter would think helpful.

---

## 4. KGC396 — an intention no operator expresses

    offer    isAnyOf (RnD, Marketing)         only these purposes
    request  isAllOf (RnD, ServiceProvision)  both of these

**Compatible.** `isAnyOf` asks that one of the use's purposes is among
the offer's values. Research and development is. Service provision rides
along unexamined.

**The drafter meant** a subset: the use's purposes are among the offer's
values and no others. That is GDPR Article 5(1)(b) purpose limitation,
and it is what a purpose clause is for.

**Why it is the finding, not just a gap.** No ODRL operator says it for
a multi-valued use. `isAnyOf` is existential, `isAllOf` is a superset
requirement, and `or(eq, eq)` fails on a use with two values.

**And the remedy is in the framework's own terms.** Declaring the
operand functional — one purpose per use — makes the request ill-sorted
at drafting time, and `isAnyOf` then means "the one purpose is among
these", which is the intention. That is the multiplicity gap, and this
problem is the case for it.

---

## 5. KGC380 against KGC383 — a composition that is false

    KGC380  isPartOf loc:EU  x  eq loc:BQ     -> Compatible, and false in law
    KGC383  isPartOf loc:EU  x  eq loc:DE-NW  -> Compatible, and true

**Different from the other four.** Here the intention and the policy
agree: both drafters meant EU territory. What fails is the reading.

DPV writes `skos:broader` for territorial control (Bonaire under the
Netherlands) and for union membership (the Netherlands in the EU). The
jurisdictional binding reads both as one order, transitivity composes
them, and Bonaire is derivably in the EU. It is not: it is an overseas
country and territory under Article 355 TFEU, and EU law does not apply
there.

**Why the pair is essential and neither half works alone.** KGC383 is
the same two relations composed at the same depth, and the conclusion is
true. So the defect is not in the semantics, not in the resource, and
not in the operator: it is that composing two relations under one sort
derives claims neither publisher made.

**And it is the case that the two readings do not fix.** Under the
geographic binding `loc:EU` is not a concept and the constraint does not
ground. Neither reading gives the right answer.

---

## What to say in §7

These five are what the benchmark found, and they are findings about
ODRL and about the vocabularies rather than about the semantics. The
verdict counts show the definitions are implementable; these show what
becomes visible once they are.

**Group them by cause, not by resource:**

- Two where an operator tests identity where the drafter meant the
  order (KGC392, KGC397) — the case for `isNotA`.
- One where the same intention drafted two ways behaves differently
  (KGC393/395) — visible only because the certificates differ.
- One where no operator expresses the intention at all (KGC396) — the
  case for declaring multiplicity.
- One where the reading composes two relations into a false claim
  (KGC380/383) — the limit of one sort per operand.

**And the honest framing:** in every one the evaluation is sound
relative to the policy. Where the answer is wrong about the world or
about the intention, the fault is in what ODRL can express or in what
the binding was told to read, and the benchmark's contribution is that
the divergence is visible at all.