"""
header.py
=========
TPTP and SMT-LIB header rendering for the ODRL benchmark.

Statistics (the % Syntax block) are omitted; tptp4X computes them during
TPTP library processing.

Anonymity: set ODRL_ANON=1 to render author, source and repository as
anonymous.  Nothing else in any generator changes.
"""

import os
import re
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Identity.  One switch; every generated file follows it.
# ---------------------------------------------------------------------------

ANONYMOUS = os.environ.get("ODRL_ANON", "") == "1"

_REAL = {
    "authors": "Daham Mustafa",
    "source":  "https://github.com/Daham-Mustaf/odrl-grounded-benchmark",
    "ref":     "TODO. A Sorted Semantics for the Knowledge-Grounded "
               "Fragment of ODRL.",
}

_ANON = {
    "authors": "Anonymous",
    "source":  "Anonymous artefact",
    "ref":     "Anonymous. A Sorted Semantics for the Knowledge-Grounded "
               "Fragment of ODRL. Under submission.",
}


def identity(fieldname: str) -> str:
    return (_ANON if ANONYMOUS else _REAL)[fieldname]


REFS = {"thispaper": lambda: identity("ref")}

DOMAINS = {
    "kb": "ODRL Policy / Knowledge-Grounded Fragment",
}

SPC = {
    "unsat": "FOF_UNS_RFN",
    "sat":   "FOF_SAT_RFN",
}

_SEP     = "%" + "-" * 74 + "\n"
_SMT_SEP = "; " + "-" * 73 + "\n"


# ---------------------------------------------------------------------------
# Formatting.  One implementation each; the comment character is a parameter.
# ---------------------------------------------------------------------------

def _count_formulae(text: str) -> int:
    return len(re.findall(r"^fof\s*\(", text, re.MULTILINE))


def ax_comment(body: str, breakdown: str, note: str) -> str:
    return f"{note}\n{_count_formulae(body)} axioms: {breakdown}."


def _wrap(label: str, text: str, c: str = "%") -> str:
    lines = text.strip().split("\n")
    out = f"{c} {label:<9s}: {lines[0]}"
    for line in lines[1:]:
        out += f"\n{c}{' ' * 11}: {line.strip()}"
    return out


def _refs_block(keys, c: str = "%") -> str:
    lines = []
    for i, k in enumerate(keys):
        if k not in REFS:
            raise KeyError(f"Unknown ref key {k!r}. Add it to header.REFS.")
        label = "Refs" if i == 0 else "    "
        lines.append(f"{c} {label:<9s}: {REFS[k]()}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Headers
# ---------------------------------------------------------------------------

@dataclass
class Header:
    """TPTP header for .p problem files."""
    file:     str
    domain:   str
    title:    str
    english:  str
    status:   str            # Satisfiable | Unsatisfiable
    comments: str
    version:  str = "1.0"
    refs:     list = field(default_factory=lambda: ["thispaper"])

    def _spc(self) -> str:
        return SPC["unsat"] if "unsat" in self.status.lower() else SPC["sat"]

    def render(self) -> str:
        return (
            _SEP
            + f"% File     : {self.file}\n"
            + f"% Domain   : {DOMAINS[self.domain]}\n"
            + f"% Problem  : {self.title}\n"
            + f"% Version  : {self.version}\n"
            + _wrap("English", self.english) + "\n"
            + "%\n"
            + _refs_block(self.refs) + "\n"
            + f"% Source   : {identity('source')}\n"
            + f"% Authors  : {identity('authors')}\n"
            + f"% Names    : {self.file}\n"
            + "%\n"
            + f"% Status   : {self.status}\n"
            + f"% SPC      : {self._spc()}\n"
            + "%\n"
            + _wrap("Comments", self.comments) + "\n"
            + _SEP
        )


@dataclass
class AXHeader:
    """TPTP header for .ax axiom files."""
    file:     str
    domain:   str
    title:    str
    english:  str
    comments: str
    version:  str = "1.0"
    refs:     list = field(default_factory=lambda: ["thispaper"])

    def render(self) -> str:
        return (
            _SEP
            + f"% File     : {self.file}\n"
            + f"% Domain   : {DOMAINS[self.domain]}\n"
            + f"% Axioms   : {self.title}\n"
            + f"% Version  : {self.version}\n"
            + _wrap("English", self.english) + "\n"
            + "%\n"
            + _refs_block(self.refs) + "\n"
            + f"% Source   : {identity('source')}\n"
            + f"% Authors  : {identity('authors')}\n"
            + f"% Names    : {self.file}\n"
            + "%\n"
            + "% Status   : Satisfiable\n"
            + f"% SPC      : {SPC['sat']}\n"
            + "%\n"
            + _wrap("Comments", self.comments) + "\n"
            + _SEP
        )


@dataclass
class SMTHeader:
    """SMT-LIB 2 header for .smt2 files."""
    file:     str
    domain:   str
    title:    str
    status:   str            # sat | unsat
    comments: str
    version:  str = "1.0"
    refs:     list = field(default_factory=lambda: ["thispaper"])

    def render(self) -> str:
        return (
            _SMT_SEP
            + f"; File     : {self.file}\n"
            + f"; Domain   : {DOMAINS[self.domain]}\n"
            + f"; Problem  : {self.title}\n"
            + f"; Version  : {self.version}\n"
            + _refs_block(self.refs, ";") + "\n"
            + f"; Source   : {identity('source')}\n"
            + f"; Authors  : {identity('authors')}\n"
            + f"; Names    : {self.file}\n"
            + f"; Status   : {self.status}\n"
            + _wrap("Comments", self.comments, ";") + "\n"
            + _SMT_SEP
        )


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    body = "fof(a1, axiom, ![X]: p(X)).\nfof(a2, axiom, ![X]: q(X)).\n"
    assert "2 axioms:" in ax_comment(body, "2 order", "note")

    h = Header(file="KGC300-1.p", domain="kb",
               title="Motivating example, spatial operand, first query",
               english="Query R + B + W for the spatial operand.",
               status="Satisfiable",
               comments="Two-query procedure, query 1 of 2.").render()
    print(h)
    assert all(l.startswith("%") for l in h.splitlines() if l)

    s = SMTHeader(file="KGC300-1.smt2", domain="kb",
                  title="Motivating example, spatial operand, first query",
                  status="sat",
                  comments="Two-query procedure, query 1 of 2.").render()
    print(s)
    assert all(l.startswith(";") for l in s.splitlines() if l)

    print("OK.  ANONYMOUS =", ANONYMOUS)