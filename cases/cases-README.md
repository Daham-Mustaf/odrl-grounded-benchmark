# Case files

One file per problem: the two ODRL policies, the binding that fixed the
reading, and the report the semantics produces for them.

```
KGC100-112   well-sortedness, rejected at drafting time
KGC300-302   the motivating example, one per sort
KGC303-306   spatial: exactly one of two alternatives, over GeoNames
KGC310-319   purpose, over DPV purposes
KGC320-323   fileFormat, over the EU file type table
KGC330-337   spatial, over DPV Locations
KGC340-343   consent status, over the DPV consent module
KGC348-349   consent status, under declared distinctness
KGC360-364   technical and organisational measures
KGC370-379   language, over a BCP 47 slice
KGC380-392   spatial: composition, subdivisions, exclusion
KGC393-397   purpose: the set operators
KGC398       language: isAnyOf against isAllOf
KGC399       purpose: or against a purpose under neither branch
KGC403-404   purpose: the declared twin of KGC316, and a category against a
             category
```

The policies can be read without the semantics. The binding IRI
dereferences to a profile entry under `problems/resources/`, which names
the resource, the sort, the grounding rule and the declarations.

Start with KGC310, KGC313 and KGC314: one published statement, then the
same operand where the vocabulary settles nothing, then the same pair
once the parties declare the concepts distinct.

Retired (IDs never reused, recoverable from tags pre-retire and pre-purpose)

```
KGC307   spatial: xone(eq France, isAllOf (France Germany)) against eq France
KGC350   legal basis: isAnyOf the seven Article 6(1) bases against eq consent
KGC351   the same against eq explicit consent under Article 6(1)(a)
KGC352   the same with explicit consent declared distinct from the seven
KGC353   legal basis: isA the legal-basis root against eq explicit consent
KGC384   spatial: eq NRW against eq Bavaria, Laender not separated
KGC385   the same pair under the ISO 3166-2 rule
KGC389   spatial: xone(eq NRW, eq Bavaria) against eq NRW
KGC390   the same pair under the ISO 3166-2 rule
```

An ID that appears anywhere in the git history is not reused either, retired
or not. KGC312 and KGC344 to KGC347 belong to early versions of the cases,
and KGC400 to KGC402 and the numbers from KGC410 up belong to earlier layouts
of the repository, so the new purpose cases are KGC399, KGC403 and KGC404.
