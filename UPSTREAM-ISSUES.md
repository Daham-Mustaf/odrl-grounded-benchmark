# Issues filed upstream

Questions this benchmark raised about what DPV 2.3 publishes, filed with the
DPV Community Group. The benchmark reads DPV 2.3 as published: it corrects
nothing, and every verdict holds for the file as vendored under
`vocabularies/`. The test cases are found from the case files, by the concepts
their constraints name.

| Issue | The problem | What the benchmark does | Bindings and test cases |
|---|---|---|---|
| [w3c-cg/dpv#485](https://github.com/w3c-cg/dpv/issues/485) | LOC writes its identity links with `skos:sameAs`, which is not a SKOS term. | Reads `skos:sameAs` as identity for all 30 pairs (60 directed statements), and would read `owl:sameAs` the same way. | `b-spatial-dpvloc-geo`, `b-spatial-dpvloc-juris`. KGC380 names a code of one pair (NL-BQ1). No proof cites an identity statement. |
| [w3c-cg/dpv#494](https://github.com/w3c-cg/dpv/issues/494) | LOC links BQ to NL-BQ1, NL-BQ2 and NL-BQ3, and SJ to NO-21 and NO-22, as one area, though each is a group of those islands; GL and DK-GL, and JE and GB-JSY, are one area with two codes and no link. | Reads the 5 BQ and SJ pairs as identities, so the bindings merge those islands with one another, and keeps GL and DK-GL, and JE and GB-JSY, as two concepts each. | `b-spatial-dpvloc-geo`, `b-spatial-dpvloc-juris`. Only KGC380 names one of the codes (NL-BQ1). It stays Compatible without the 5 statements, under both provers, and no proof cites an identity statement. |
| [w3c-cg/dpv#496](https://github.com/w3c-cg/dpv/issues/496) | CommercialPurpose and NonCommercialPurpose overlap under their definitions, and so do CommercialResearch and NonCommercialResearch. | Reads the definitions as prose and the order as published. DPV states no disjointness, so none is read, and the declarations of the purposes state distinctness only. | `b-purpose`. Verdicts: KGC301, KGC319, KGC393, KGC394, KGC395, KGC399, KGC404. Rejected: KGC101, KGC105. Control: KGC111. |
| [w3c-cg/dpv#489](https://github.com/w3c-cg/dpv/issues/489) | LOC section 1.2, inverse jurisdictions: it calls `skos:broader` and `skos:narrower` transitive, and tests a location by a path that some locations satisfy for both a jurisdiction and its inverse. | The builder reads none of the complement edges, so no inverse jurisdiction is a concept of either resource. | None. |
| [w3c-cg/dpv#486](https://github.com/w3c-cg/dpv/issues/486) | `dpv:RightsFulfilment` is a purpose whose `skos:broader` is `dpv:LegalObligation`, a legal basis in another module. | Keeps RightsFulfilment as a concept of the purposes resource. The edge leaves the module and is not read, so it is a root there. | `b-purpose`. Test cases: none. The formula of KGC404 lists it with every other purpose. |
| [w3c-cg/dpv#495](https://github.com/w3c-cg/dpv/issues/495) | The scope note of `dpv:ServiceOptimisation` still calls it a subclass of ServiceProvision, and its published parent is ServiceManagement. | Reads `skos:broader`, which gives ServiceManagement. No scope note is read. | `b-purpose`. Test cases: none. The formula of KGC404 lists it with every other purpose. |
