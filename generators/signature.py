"""
signature.py
============
The signature: which operators each sort admits, and what shape of right
operand each requires.  This is the table of the paper, and the whole of the
drafting-time check.

Nothing here reads a resource.  Well-sortedness depends on the operator, the
arity and the operand's sort, and on nothing else, which is what makes the
check possible before any vocabulary is opened.
"""

NOM, TAX, MER = "nom", "tax", "mer"

RELATION = {NOM: "identity", TAX: "subsumption", MER: "parthood"}

# operator -> (sorts admitting it, arity)
SIGNATURE = {
    "eq":        ({NOM, TAX, MER}, 1),
    "neq":       ({NOM, TAX, MER}, 1),
    "isAnyOf":   ({NOM, TAX, MER}, "n"),
    "isAllOf":   ({NOM, TAX, MER}, "n"),
    "isNoneOf":  ({NOM, TAX, MER}, "n"),
    "isA":       ({TAX},           1),
    "isPartOf":  ({MER},           1),
    "hasPart":   ({MER},           1),
}

REQUIRES = {"isA": "subsumption", "isPartOf": "parthood", "hasPart": "parthood"}


class NotWellSorted(Exception):
    """Raised with the reason a constraint fails the check."""


def check(operator: str, sort: str, arity) -> None:
    """Raise NotWellSorted if the constraint may not be written.

    One lookup in SIGNATURE.  No model, no value, no resource contents.
    """
    if operator not in SIGNATURE:
        raise NotWellSorted(
            f"{operator} is not an operator of the fragment")
    sorts, want = SIGNATURE[operator]
    if sort not in sorts:
        needs = REQUIRES.get(operator, "identity")
        raise NotWellSorted(
            f"{operator} requires {needs}; the operand is {sort}, whose "
            f"resource supplies {RELATION[sort]}")
    if arity != want:
        shape = "a single value" if want == 1 else "a set of values"
        raise NotWellSorted(
            f"{operator} takes {shape}")


def is_well_sorted(operator: str, sort: str, arity) -> tuple[bool, str]:
    try:
        check(operator, sort, arity)
        return True, ""
    except NotWellSorted as e:
        return False, str(e)