"""
writers.py — KGConstraints
==========================
Writes .p (FOF/TPTP), .smt2 (SMT-LIB), and .ttl (Turtle) files
for the KGConstraints tier of the ODRL benchmark.

Difference from AxisDecomposition/writers.py:
  Axis problems hardcode ORD000 + AXIS000 (+ optional ORD001) includes.
  KGConstraints problems take their full include list from the problem
  dict, since different problems use different combinations of theory
  axioms (DENOT, COMPOSE, SUBSUME, ...) and resource axioms (GN, DPV,
  BCP47).
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from header import problem_header, SMTHeader


def _render_includes(p: dict) -> str:
    """Emit include() lines in the order listed in p['includes']."""
    lines = [f"include('Axioms/{ax}')." for ax in p["includes"]]
    return "\n".join(lines) + "\n"


def write_fof_problem(p: dict, out_dir: Path) -> Path:
    subdir = out_dir / p["subdir"]
    subdir.mkdir(parents=True, exist_ok=True)

    includes = _render_includes(p)
    conj_id = p["id"].lower()

    conjecture_fof = (
        f"fof({conj_id}, conjecture,\n"
        f"    {p['fof_conjecture']}).\n"
    )

    header = problem_header(p, "kb", "")

    content = (
        header
        + includes
        + "\n"
        + "% ─── Constraint tokens, groundings, and resource hooks "
        + "─" * 19 + "\n"
        + p["fof_extra_decls"]
        + "% ─── Conjecture "
        + "─" * 52 + "\n"
        + conjecture_fof
        + "%--------------------------------------------------------------------------\n"
    )

    path = subdir / f"{p['id']}-1.p"
    path.write_text(content, encoding="utf-8")
    return path


def write_smt2_problem(p: dict, out_dir: Path) -> Path:
    subdir = out_dir / p["subdir"]
    subdir.mkdir(parents=True, exist_ok=True)

    logic   = p.get("smt2_logic", "UF")
    decls   = p.get("smt2_decls", "")
    asserts = p["smt2_asserts"].strip()

    smt_header = SMTHeader(
        file     = f"{p['id']}-1.smt2",
        domain   = "kb",
        title    = p["name"],
        version  = "1.0",
        refs     = ["kgc2026"],
        comments = (
            f"Verdict: {p.get('verdict', '?')}  "
            f"Category: {p['subdir']}  "
            f"Difficulty: {p.get('difficulty', 'Easy')}"
        ),
        status   = p["status_smt"],
        verdict  = p.get("verdict", ""),
    ).render()

    content = "\n".join([
        smt_header,
        f"(set-logic {logic})",
        decls,
        asserts,
        "(check-sat)",
        "(exit)",
        "",
    ])

    path = subdir / f"{p['id']}-1.smt2"
    path.write_text(content, encoding="utf-8")
    return path


def write_ttl_policy(p: dict, policies_dir: Path) -> Path:
    policies_dir.mkdir(parents=True, exist_ok=True)
    path = policies_dir / f"{p['id']}-policy.ttl"
    path.write_text(p["ttl"].strip() + "\n", encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Vocabulary check — refuses to write a problem that references constants
# not present in the included axiom files (no hallucination).
# ---------------------------------------------------------------------------
def _extract_constants_from_ax(ax_path: Path) -> set[str]:
    """Read an axiom file, return all constants matching ^(gn|dpv|bcp)_\\w+$."""
    text = ax_path.read_text(encoding="utf-8")
    return set(re.findall(r"\b(?:gn|dpv|bcp)_[a-z0-9_]+\b", text))


def collect_vocabulary(axioms_dir: Path) -> set[str]:
    """Union of all (gn|dpv|bcp)_* constants found in the resource .ax files."""
    vocab: set[str] = set()
    for ax_name in ("GN000-0.ax", "DPV000-0.ax", "BCP47000-0.ax"):
        ax_path = axioms_dir / ax_name
        if ax_path.exists():
            vocab |= _extract_constants_from_ax(ax_path)
    return vocab


def validate_problem_constants(p: dict, vocabulary: set[str]) -> None:
    """Refuse a problem that references constants outside the vocabulary."""
    text = p["fof_extra_decls"] + (p.get("fof_conjecture") or "")
    used = set(re.findall(r"\b(?:gn|dpv|bcp)_[a-z0-9_]+\b", text))
    forbidden = used - vocabulary
    if forbidden:
        raise ValueError(
            f"Problem {p['id']}: hallucinated constants not in vocabulary: "
            f"{sorted(forbidden)}.\n"
            f"  Vocabulary has {len(vocabulary)} known constants from "
            f"GN000/DPV000/BCP47000."
        )