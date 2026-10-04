# Distinctness and disjointness: where it goes and what it says

Two kinds of declaration, and only one is constrained by what the
resource publishes. The paper currently treats them as one thing, and
the suite now has four instances that show they are not.

---

## The difference, stated once

**Distinctness.** Two concepts are not one concept: `a ≠ b`. It says
nothing about what lies below either.

**Disjointness.** Nothing lies below both:
`¬∃x (x ⪯ a ∧ x ⪯ b)`. It is a claim about the whole down-set of each.

Disjointness implies distinctness where the order is reflexive, since
`a ⪯ a`. The converse fails, and the failure is what matters here.

---

## Why only one is constrained

A resource publishes an order. Distinctness adds a fact the order does
not settle, and no order refutes it: one concept may lie below another
and still be a different concept. `ScientificResearch ⪯
ResearchAndDevelopment` and `ScientificResearch ≠
ResearchAndDevelopment` hold together in any structure where the two are
different elements.

Disjointness is refutable by the resource. Where the resource publishes
a concept below both, the declaration and the resource have no common
model. Every verdict over the pair is then vacuous: both queries come
back unsatisfiable, and the harness raises rather than returning a
verdict, since Compatible and Incompatible are simultaneously true of
the empty set of admissible structures.

**So the same problem does not arise for distinctness.** It is
admissible over any resource. The only way to make a distinctness
inconsistent is to declare two concepts distinct that the resource
identifies, and no resource in the suite publishes identity except DPV
Locations, whose ISO rule is applied to the quotient for exactly that
reason.

---

## Where it goes in the paper

**One paragraph in the background-theory section**, where declarations
are introduced. Not in the resource section: the constraint is on what
the parties may adopt, not on what the publisher may write.

Draft:

> A background theory is the parties' to adopt, and not theirs to adopt
> in a form the resource contradicts. Two kinds of assertion are
> available and they differ in this respect. Distinctness, that two
> concepts are not one, is admissible over any order: a concept may lie
> below another and still be a different concept. Disjointness, that
> nothing lies below both, is not. Where the resource publishes a
> concept below both, the theory and the resource have no common model,
> and the three verdicts of \cref{def:verdict} are vacuously true
> together; the evaluation reports an inconsistent binding rather than a
> verdict.
>
> The distinction has consequences a drafter meets. DPV's purposes
> module is a directed acyclic graph rather than a tree: eleven of its
> concepts have two parents, so eleven pairs of purposes cannot be
> declared disjoint. `NonCommercialResearch` lies below both
> `NonCommercialPurpose` and `ResearchAndDevelopment`, and a party
> separating those two would be refuted by the vocabulary. Nothing in
> the branching implies that the two overlap in any other sense, and
> distinctness over the same pair remains available and is what the
> operators of the fragment actually test.

**And one sentence in the evaluation**, with the counts:

> Of the four resources carrying a declared theory, one declares
> disjointness and three declare distinctness. The disjointness is the
> consent module's two branches, where the definitions warrant it and
> no state lies below both. The purposes and measures modules publish
> concepts below two parents, so disjointness over those pairs is
> unavailable; distinctness is what their theories declare.

---

## The examples worth naming

**Where disjointness is warranted and load-bearing.** DPV consent
status: `ConsentStatusValidForProcessing` and
`ConsentStatusInvalidForProcessing`. The definitions say "states that
can be used as valid justifications" and "states that cannot", and no
state lies below both. KGC343 and KGC347 rest on it, and it is the only
disjointness in the suite.

**Where disjointness is unavailable.** DPV purposes:
`NonCommercialPurpose` and `ResearchAndDevelopment`, with
`NonCommercialResearch` below both. Ten more pairs in the same module.

**And in the measures module**, one pair: `AuthenticationProtocols` and
`CryptographicMethods`, with `CryptographicAuthentication` and
`ZeroKnowledgeAuthentication` below both.

**Where distinctness is what is needed and disjointness would be
overkill.** Every `eq`, `neq` and `isNoneOf` problem in the suite. Those
operators test identity, so a declaration that two concepts are not one
settles them; nothing asks what lies below both.

**And the reason no operator needs disjointness** is worth one clause:
`isNoneOf` excludes by identity rather than by parthood, which is the
finding KGC392 and KGC397 record. An operator testing the complement of
a down-set would need disjointness to be decidable, and ODRL has none.

---

## What the builders should do

**Refuse an inadmissible disjointness at build time**, naming the common
child. Catching it there beats catching it at query time, where it
surfaces as two unsatisfiable queries and a raised exception with no
indication of which concept caused it.

`build_dpv.py` now reports the pairs; it does not yet refuse, because it
offers no disjointness option. A builder that does should check first.

**And say in each theory's header which kind it declares**, since a
reader cannot tell from the file: 2701 inequations look the same whether
the author meant distinctness or disjointness, and only the header says
which claim is being made.