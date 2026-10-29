"""
operator_notes.py
=================
The DPV-ODRL usage notes, as the checker and the writer both read them.

Each dpv-odrl left operand carries a skos:note saying which operators MUST be
used with it.  A policy that uses another operator goes beyond the note.
validate_cases.py lists those policies, and the case writer adds a sentence
to the comment of each verdict case that has one, so the sentence and the
list cannot disagree.

    OPERATOR_NOTES   operand name -> the operators its note lists
    beyond           the operand's name when an operator is outside its note
    sentences        the sentence for every such pair in a case's Turtle
"""

from rdflib import Graph, Namespace, RDF

ODRL = Namespace("http://www.w3.org/ns/odrl/2/")
DPVODRL = "https://w3id.org/dpv/mappings/odrl#"

# The skos:note of each DPV-ODRL left operand: "Only the ... operators MUST
# be used."  Read again from mappings/odrl/dpv-odrl.ttl on the dev branch of
# https://github.com/w3c-cg/dpv (commit 6d20265, 26 October 2026); the
# notes of these operands are the ones the August copy (commit 8a50545,
# 6 August 2026) had.  The measure operands all carry the same note as
# TechnicalOrganisationalMeasure.
_FIVE = {"isA", "eq", "neq", "isAnyOf", "isNoneOf"}
OPERATOR_NOTES = {
    "Purpose": _FIVE,
    "Location": {"eq", "neq", "isAnyOf", "isNoneOf"},
    "Status": _FIVE,
    "TechnicalOrganisationalMeasure": _FIVE,
    "TechnicalMeasure": _FIVE,
    "OrganisationalMeasure": _FIVE,
}


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
