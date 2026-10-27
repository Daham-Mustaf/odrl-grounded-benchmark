# Glossary

One definition per term. The third column gives the name a term replaced, or
the name it still carries inside the code and the files.

| Term | Meaning | Former or internal names |
|---|---|---|
| resource | A versioned slice of a published vocabulary, with its provenance. A binding reads its concepts and the statements it publishes about them. Example: the fifteen-subtag slice of the IANA Language Subtag Registry. | |
| binding | The pairing of an ODRL left operand with a resource, the sort at which the resource's statements are read, and the grounding rule that maps a policy value to a concept. The sort belongs to the binding, not to the operand or to the resource. | |
| statement | One thing a resource or a set of declarations says about its concepts: that one lies below another, that two are the same, that two are distinct, or that two are disjoint. | Former name: assertion. Lean: `Assertion`. |
| declaration | A statement the parties declare over and above what the resource publishes, and may withdraw. Declarations come in sets, one set per file. Every set with statements records its origin: a practice rule, which is a rule of the resource's practice such as RFC 5646 registry uniqueness, or a prose definition, which is a definition the resource's RDF does not state. A report names the set it was computed under with `vrep:declarations`. The empty set has no statements and no origin. | Former name: background theory. Lean: B. Internal key: `background_theory`. Directory: `problems/background/`. |
| verdict | The result of comparing the constraints two policies place on one left operand, relative to a binding and its declarations. Compatible: every structure the resource and the declarations admit has a use satisfying both. Incompatible: none has. Unknown: some have and some do not. A constraint that is ill sorted, or whose value does not ground, is rejected and has no verdict. | |
| certificate | The evidence for a definite verdict: a refutation of one of the two queries, with each premise it cites classified by where it came from (the resource, the declarations, an order axiom or the witness condition). An Unknown verdict has no refutation. | |
| provider | The party of the first policy of a case, `drk:policy-NNN-1`, written with `odrl:assigner`. The verdict is symmetric, so provider and consumer only fix the order in which a report names the policies. | Internal name: offer (`compile.py`). |
| consumer | The party of the second policy of a case, `drk:policy-NNN-2`. 22 second policies name no `odrl:assignee` yet. Both policies of a case are `odrl:Set`, and the case files use neither `odrl:Offer` nor `odrl:Request`. | Internal name: request (`compile.py`). |
