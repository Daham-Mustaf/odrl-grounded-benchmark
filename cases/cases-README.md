# Case files

One file per problem: the two ODRL policies, the reading of the vocabulary
that fixed the answer, and the report the semantics produces for them.

```
KGC100-112   well-sortedness, rejected at drafting time
KGC300-302   the motivating example, one per sort
KGC303-304   spatial: exactly one of two alternatives, over GeoNames
KGC308-309   spatial: one country within another, over GeoNames
KGC310-319   purpose, over DPV purposes
KGC320-323   fileFormat, over the EU file type table
KGC331-337   spatial, over DPV Locations
KGC340-343   consent status, over the DPV consent module
KGC348-349   consent status, under declared distinctness
KGC360-366   technical and organisational measures
KGC370-379   language, over a BCP 47 slice
KGC380-392   spatial: composition, subdivisions, exclusion
KGC393-397   purpose: the set operators
KGC398       language: isAnyOf against isAllOf
KGC399       purpose: or against a purpose under neither branch
KGC403-404   purpose: the declared twin of KGC316, and a category against a
             category
```

The policies can be read without the semantics. The name of the reading,
which the catalogue shows in plain words, leads to a profile entry under
`problems/`, which names the vocabulary, the kind of value, the rule for
matching values to entries and the declarations.

Start with KGC310, KGC313 and KGC314: one published statement, then the
same operand where the vocabulary decides nothing, then the same pair
once the concepts are declared distinct.

`catalogue.html` lists every case with its two policies in plain words, how
the vocabulary is read and the declarations in force with their origin, and
then the lesson, the verdict and the reason. `catalogue-blind.html` is the same page
without those three. Both are written by `generators/catalogue.py`.

## What makes a case meaningful

A case earns its place when a reader can state what it teaches and why its
verdict is what it is. The first three points are about the policies, the
rest about the case.

- Each policy is one a real party could publish. A policy that no use can
  satisfy is not one, and `check_policies.py` fails it by case ID.
- Both policies share action and target. Two policies that act on different
  things have no verdict worth reading, and `check_policies.py` checks this
  too.
- Values are concrete. A root concept appears only where the policy means
  "any", and then the title reads "any" and not "only".
- Each case states one lesson. Within a family no two cases teach the same
  thing; a twin differs from its partner in one declared thing, and names
  which.
- The reason for the verdict is given in plain words. A definite verdict
  names what it rests on, and one that rests on a declaration names the
  declaration. Every domain fact in it names its source: a DPV edge or
  definition, ISO 3166, RFC 5646, the EU file type table, GeoNames, the
  TFEU or the TEU. An Unknown names both situations in plain words: one
  where a use meets both policies, one where none does.
- Titles, lessons, reasons and the catalogue use the words of the domain,
  and none of the words of logic or of the machinery that checks the cases.
  `lint_cases.py` holds the list, and it and `catalogue.py` fail a text that
  uses one. A formula such as (purpose, isA, X) is out as well. What a
  prover is expected to cite goes in the problem's maintainer note, which
  the catalogue does not show.
- Every declaration set has an origin and covers the whole part of the
  vocabulary it applies to. Where a set ranges over a vocabulary, it lists
  all of it, less what the set names as left out, and
  `check_declarations.py` fails a set that leaves a concept out.
- Case IDs are never reused. An ID that appears anywhere in the git history,
  in any earlier layout, is taken: `git log --all --oneline --
  cases/KGC<id>.ttl` must be empty and `git log --all -p | grep -c KGC<id>`
  must be 0.

The checks run in `full-run.sh`. `lint_cases.py` holds the title wording, the
parties and target of each family, and the text rules. `check_coverage.py`
holds the grid: each of the 24 cells of operator by kind of value has a
verdict case where that kind of value admits the operator and a rejection
where it does not, and `or` and `xone` each appear for every kind of value.

Retired (IDs never reused, recoverable from tags pre-retire, pre-purpose, pre-review and pre-final)

```
KGC305   spatial: xone(isPartOf France, isPartOf Germany) against eq France, countries distinct
KGC306   the same, France and Germany declared disjoint
KGC307   spatial: xone(eq France, isAllOf (France Germany)) against eq France
KGC311   purpose: isA Purpose against eq NonCommercialResearch
KGC330   spatial: isPartOf Netherlands against eq Bonaire
KGC350   legal basis: isAnyOf the seven Article 6(1) bases against eq consent
KGC351   the same against eq explicit consent under Article 6(1)(a)
KGC352   the same with explicit consent declared distinct from the seven
KGC353   legal basis: isA the legal-basis root against eq explicit consent
KGC361   measures: isAllOf(encryption, access control) against isNoneOf(access control)
KGC384   spatial: eq NRW against eq Bavaria, Laender not separated
KGC385   the same pair under the ISO 3166-2 rule
KGC386   spatial: isNoneOf {Bavaria, Berlin} against eq Hamburg, Laender not separated
KGC387   the same pair under the ISO 3166-2 rule
KGC389   spatial: xone(eq NRW, eq Bavaria) against eq NRW
KGC390   the same pair under the ISO 3166-2 rule
```

An ID that appears anywhere in the git history is not reused either, retired
or not. KGC312 and KGC344 to KGC347 belong to early versions of the cases,
and KGC400 to KGC402 and the numbers from KGC410 up belong to earlier layouts
of the repository, so the new purpose cases are KGC399, KGC403 and KGC404.
