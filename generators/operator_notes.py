"""
operator_notes.py
=================
The DPV-ODRL usage notes, as the checker and the writer both read them.

Each dpv-odrl left operand carries a skos:note saying which operators MUST be
used with it.  A policy that uses another operator goes beyond the note.
validate_cases.py lists those policies, and the case writer gives each verdict
case that has one a profile note, so the note and the list cannot disagree.

The table is read from the vendored mapping, vocabularies/dpv-odrl/dpv-odrl.ttl
(DPV dev at a fixed commit, see the README beside it), so the claim can be
checked against the source and nothing here is typed by hand.

    OPERATOR_NOTES   operand name -> the operators its note lists
    beyond           the operand's name when an operator is outside its note
    sentences        the profile note for every such pair in a case's Turtle
"""

import re
from pathlib import Path

from rdflib import Graph, Namespace, RDF
from rdflib.namespace import SKOS

ODRL = Namespace("http://www.w3.org/ns/odrl/2/")
DPVODRL = "https://w3id.org/dpv/mappings/odrl#"
VENDORED = (Path(__file__).resolve().parent.parent
            / "vocabularies" / "dpv-odrl" / "dpv-odrl.ttl")


def read_notes(path=VENDORED) -> dict:
    """Operand name -> the odrl: operators its note lists.  A note counts when
    it starts "Only the" and names operators, as the usage notes do."""
    g = Graph().parse(path, format="turtle")
    out = {}
    for s, note in g.subject_objects(SKOS.note):
        if not str(s).startswith(DPVODRL):
            continue
        text = str(note).strip()
        ops = set(re.findall(r"odrl:(\w+)", text))
        if text.startswith("Only the") and ops:
            out[str(s)[len(DPVODRL):]] = ops
    return out


OPERATOR_NOTES = read_notes()


def beyond(operand_iri, operator) -> str | None:
    """The operand's name if the operator is outside its usage note."""
    iri = str(operand_iri)
    name = iri[len(DPVODRL):] if iri.startswith(DPVODRL) else None
    allowed = OPERATOR_NOTES.get(name)
    return name if allowed is not None and operator not in allowed else None


def sentences(turtle: str) -> str:
    """One sentence for each (operand, operator) pair in the policies that is
    outside the operand's usage note, in a fixed order; empty if none is."""
    g = Graph().parse(data=turtle, format="turtle")
    pairs = set()
    for c in g.subjects(RDF.type, ODRL.Constraint):
        op = str(next(g.objects(c, ODRL.operator), "")).rsplit("/", 1)[-1]
        for lo in g.objects(c, ODRL.leftOperand):
            name = beyond(lo, op)
            if name:
                pairs.add((name, op))
    return " ".join(
        f"This policy goes beyond the DPV-ODRL usage note for {name}, "
        f"which does not list {op}." for name, op in sorted(pairs))
