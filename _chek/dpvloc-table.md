# DPV Locations, the sixteen cases

All at sort `mer`, all on `odrl:spatial`, all over one file: the DPV
Locations extension. What changes across the rows is the binding, the
operator, and whether the parties declared anything.

## The two bindings

Both read `skos:broader`. They differ in which of the two relations the
extension writes with it they take as the order.

| Binding | Reads | Concept set | Depth |
|---|---|---|---|
| `b-spatial-dpvloc-geo` | containment only, Bavaria within Germany | countries and subdivisions; `loc:EU` is **not** in it | two levels |
| `b-spatial-dpvloc-juris` | containment **and** union membership | adds `loc:EU`, EEA, EEA30 | four levels, unions nest |

That is the whole difference, and it is the reason the resource is in
the suite.

## The cases

| Case | Binding | Offer | Request | Verdict | What decides it |
|---|---|---|---|---|---|
| KGC330 | geo | `isPartOf NL` | `eq BQ` | Compatible | one containment edge, BQ within NL |
| KGC331 | juris | `isPartOf EU` | `eq DE` | Compatible | one membership edge, DE in EU |
| KGC333 | geo | `eq DE` | `eq FR` | Unknown | nothing separates the two codes |
| KGC334 | geo | `eq DE` | `eq FR` | Incompatible | ISO rule, declared |
| KGC380 | juris | `isPartOf EU` | `eq BQ` | Compatible | two edges plus transitivity; **false in law** |
| KGC381 | geo | `isPartOf EU` | `eq DE` | Unknown, ungrounded | `loc:EU` is not a concept of this slice |
| KGC382 | geo | `isPartOf DE` | `eq DE-NW` | Compatible | one containment edge |
| KGC383 | juris | `isPartOf EU` | `eq DE-NW` | Compatible | two edges plus transitivity; true |
| KGC384 | geo | `eq DE-NW` | `eq DE-BY` | Unknown | Laender not separated |
| KGC385 | geo | `eq DE-NW` | `eq DE-BY` | Incompatible | ISO 3166-2 rule, declared |
| KGC386 | geo | `isNoneOf {DE-BY, DE-BE}` | `eq DE-HH` | Unknown | complement needs distinctness |
| KGC387 | geo | `isNoneOf {DE-BY, DE-BE}` | `eq DE-HH` | Compatible | two rule instances |
| KGC388 | geo | `or(isPartOf DE-NW, isPartOf DE-BY)` | `eq DE-NW` | Compatible | first disjunct, reflexivity |
| KGC389 | geo | `xone(eq DE-NW, eq DE-BY)` | `eq DE-NW` | Unknown | negated literal unsettled |
| KGC390 | geo | `xone(eq DE-NW, eq DE-BY)` | `eq DE-NW` | Compatible | rule discharges the negated literal |
| KGC391 | geo | `hasPart DE-NW` | `eq DE` | Compatible | the same edge read upward |
| KGC392 | geo | `isNoneOf {WF}` | `eq WF-UV` | Compatible | **defeats the drafter's intent** |

## The pairs

Six rows exist only as the second half of a pair. A reader who takes one
without the other misses the point.

| Pair | Same | Different |
|---|---|---|
| 331 / 381 | both policies, the file | the binding: juris grounds `loc:EU`, geo does not |
| 333 / 334 | policies, binding, resource | the ISO rule is declared |
| 384 / 385 | as above | as above, over subdivision codes |
| 386 / 387 | as above | as above |
| 389 / 390 | as above | as above |
| 380 / 383 | binding, depth, both relations | the composition is false in one and true in the other |

## What Beatriz asked

She compared KGC381 against KGC380. Those differ in the binding **and**
in the request, so the comparison does not isolate anything. KGC381's
twin is KGC331: same two policies, same file, different binding,
Compatible against ungrounded.

The case file says so in its `description`, and the module docstring
says so at length. It is not in the report.