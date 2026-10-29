# DPV-ODRL mapping

`dpv-odrl.ttl` is `mappings/odrl/dpv-odrl.ttl` of the W3C Data Privacy
Vocabularies CG repository (https://github.com/w3c-cg/dpv), branch `dev`, at
commit `8a5054540351fb0dfe492ca54eaffb3d107a0d76` (6 August 2026). The file
itself was last changed in that branch by commit
`61cdb927f7e26a01983657e4d6219a3ff3d11873` (23 March 2026). Its Git blob id
is `bd24074423fcd847921fb0f4bdd373b2b7642e69` and the SHA-256 of the file as
vendored is:

    0541f2a0fed030cd5e850ede2bc09ae24a903d1f8379ca1a4f7c63b501af934c  dpv-odrl.ttl

`generators/operator_notes.py` reads the `skos:note` of each left operand in
this file to find which operators its usage note lists. The sentence "This
policy goes beyond the DPV-ODRL usage note for X, which does not list Y" in a
case's profile note is checked against it.

The notes were first read from commit `6d20265` of the same branch (26 October
2026). For the operands the cases use, Purpose, Location, Status and the three
measure operands, the notes in that commit are the same as in this file.
