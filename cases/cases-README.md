# Case files

One file per problem: the two ODRL policies, the binding that fixed the
reading, and the report the semantics produces for them.

```
KGC100-112   well-sortedness, rejected at drafting time
KGC300-302   the motivating example, one per sort
KGC310-317   purpose, over DPV purposes
KGC320-323   fileFormat, over the EU file type table
KGC330-334   spatial, over DPV Locations
KGC340-347   consent status, over the DPV consent module
KGC350-353   legal basis, over DPV and its GDPR extension
KGC360-364   technical and organisational measures
KGC370-375   language, over a BCP 47 slice
KGC380-392   spatial: composition, subdivisions, exclusion
KGC393-397   purpose: the set operators
```

The policies can be read without the semantics. The binding IRI
dereferences to a profile entry under `problems/resources/`, which names
the resource, the sort, the grounding rule and the background theory.

Start with KGC310, KGC313 and KGC314: one published assertion, then the
same operand where the vocabulary settles nothing, then the same pair
once the parties declare the concepts distinct.