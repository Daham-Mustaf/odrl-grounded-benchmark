"""
writers.py
==========
Writes the artefacts for one benchmark problem.

A problem is decided by two satisfiability queries, so each problem produces
two TPTP files and two SMT-LIB files:

    <id>-1.p / .smt2     R + B + W(K)
    <id>-2.p / .smt2     R + B + not W(K)

The verdict is a property of the pair and is not written into either file.
The harness derives it:

    q1 unsatisfiable                      -> Incompatible
    q2 unsatisfiable                      -> Compatible
    both satisfiable                      -> Unknown
    grounding undefined (no query built)  -> Unknown

Problem dict keys:
    id, name, description, subdir
    includes          list of .ax file names
    fof_decls         constants, groundings, resource hooks
    fof_witness       the witness condition W(K), as a FOF formula
    expected_q1       "Satisfiable" | "Unsatisfiable"
    expected_q2       "Satisfiable" | "Unsatisfiable"
    smt2_decls        SMT-LIB declarations
    smt2_asserts      SMT-LIB assertions for R + B
    smt2_witness      the witness condition, as an SMT-LIB term
    ttl               the ODRL policy pair, Turtle
    ungrounded        optional; if set, no query is built
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from header import Header, SMTHeader

QUERIES = {
    1: ("witness condition asserted",  "fof_witness",  "smt2_witness",  False),
    2: ("witness condition negated",   "fof_witness",  "smt2_witness",  True),
}


def _includes(p: dict) -> str:
    return "\n".join(f"include('axioms/{ax}')." for ax in p["includes"]) + "\n"


def _rule(label: str) -> str:
    return f"% --- {label} " + "-" * max(0, 68 - len(label)) + "\n"


def write_fof(p: dict, q: int, out_dir: Path) -> Path:
    """Write query q of problem p as a TPTP file."""
    label, fof_key, _, negate = QUERIES[q]
    subdir = out_dir / p["subdir"]
    subdir.mkdir(parents=True, exist_ok=True)

    witness = p[fof_key].strip()
    formula = f"~ ( {witness} )" if negate else witness
    name = f"{p['id'].lower()}_w"

    header = Header(
        file     = f"{p['id']}-{q}.p",
        domain   = "kb",
        title    = f"{p['name']} ({label})",
        english  = p.get("description", p["name"]),
        status   = p[f"expected_q{q}"],
        comments = f"Query {q} of 2.  Verdict is derived from both queries.",
    ).render()

    content = (
        header
        + _includes(p)
        + "\n"
        + _rule("constants, groundings and resource hooks")
        + p["fof_decls"].rstrip() + "\n\n"
        + _rule(label)
        + f"fof({name}, axiom,\n    {formula}).\n"
        + "%" + "-" * 74 + "\n"
    )
    path = subdir / f"{p['id']}-{q}.p"
    path.write_text(content, encoding="utf-8")
    return path


def write_smt2(p: dict, q: int, out_dir: Path) -> Path:
    """Write query q of problem p as an SMT-LIB file."""
    label, _, smt_key, negate = QUERIES[q]
    subdir = out_dir / p["subdir"]
    subdir.mkdir(parents=True, exist_ok=True)

    witness = p[smt_key].strip()
    assertion = f"(assert (not {witness}))" if negate else f"(assert {witness})"
    status = "unsat" if p[f"expected_q{q}"].lower().startswith("unsat") else "sat"

    header = SMTHeader(
        file     = f"{p['id']}-{q}.smt2",
        domain   = "kb",
        title    = f"{p['name']} ({label})",
        status   = status,
        comments = f"Query {q} of 2.  Verdict is derived from both queries.",
    ).render()

    content = "\n".join([
        header,
        f"(set-logic {p.get('smt2_logic', 'UF')})",
        p.get("smt2_decls", "").rstrip(),
        p["smt2_asserts"].rstrip(),
        f"; {label}",
        assertion,
        "(check-sat)",
        "(exit)",
        "",
    ])
    path = subdir / f"{p['id']}-{q}.smt2"
    path.write_text(content, encoding="utf-8")
    return path


def write_problem(p: dict, out_dir: Path, cases_dir: Path) -> list[Path]:
    """Write both queries and the case file.

    The case file holds the two policies and the expected report in one
    graph, so a reader sees the question and the answer together.
    """
    written = []
    if not p.get("ungrounded"):
        for q in (1, 2):
            written.append(write_fof(p, q, out_dir))
            written.append(write_smt2(p, q, out_dir))
    written.append(write_case(p, cases_dir))
    return written


def write_case(p: dict, cases_dir: Path) -> Path:
    """Policies and expected report, one graph per problem."""
    cases_dir.mkdir(parents=True, exist_ok=True)
    path = cases_dir / f"{p['id']}.ttl"
    path.write_text(p["ttl"].strip() + "\n", encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Verdict, derived from the two query outcomes
# ---------------------------------------------------------------------------

def verdict_of(q1: str, q2: str) -> str:
    """Map a pair of SZS or SMT statuses to a verdict."""
    unsat1 = q1.lower().startswith("unsat")
    unsat2 = q2.lower().startswith("unsat")
    if unsat1 and unsat2:
        raise ValueError("both queries unsatisfiable: (R, B) is inconsistent")
    if unsat1:
        return "Incompatible"
    if unsat2:
        return "Compatible"
    return "Unknown"


def expected_verdict(p: dict) -> str:
    if p.get("ungrounded"):
        return "Unknown"
    return verdict_of(p["expected_q1"], p["expected_q2"])


# ---------------------------------------------------------------------------
# Vocabulary check.  Refuses a problem naming constants no resource declares.
# ---------------------------------------------------------------------------

_CONST = re.compile(r"\b(?:gn|dpv|bcp)_[a-z0-9_]+\b")

# A formula name is the first argument of fof(...).  Names are not terms, so
# they must be removed before scanning, or an axiom called gn_france_in_europe
# is mistaken for a constant.
_LABEL = re.compile(r"(^|\n)(\s*)fof\s*\(\s*[a-zA-Z0-9_]+")


def _terms_only(text: str) -> str:
    return _LABEL.sub(r"\1\2fof(", text)


def collect_vocabulary(axioms_dir: Path) -> set[str]:
    """Constants declared by the resource axiom files, formula names excluded."""
    vocab: set[str] = set()
    for ax in ("GN000-0.ax", "DPV000-0.ax", "BCP47000-0.ax"):
        path = axioms_dir / ax
        if path.exists():
            body = _terms_only(path.read_text(encoding="utf-8"))
            vocab |= set(_CONST.findall(body))
    return vocab


def validate_problem_constants(p: dict, vocabulary: set[str]) -> None:
    """Refuse a problem naming a constant no resource declares."""
    text = _terms_only(p["fof_decls"] + p.get("fof_witness", ""))
    forbidden = set(_CONST.findall(text)) - vocabulary
    if forbidden:
        raise ValueError(
            f"Problem {p['id']}: constants not declared by any resource: "
            f"{sorted(forbidden)}.  Vocabulary has {len(vocabulary)} constants."
        )