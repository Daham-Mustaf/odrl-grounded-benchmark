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


# The three order axioms, quantified, as SMT-LIB.  Emitted whole into every
# problem whose signature has the order, rather than instantiated at the
# concepts each problem happens to need.  Two reasons: hand-selected instances
# make the TPTP and SMT-LIB encodings different theories, so agreement between
# them stops meaning anything; and selecting exactly the instances a proof
# needs is indistinguishable, from outside, from fitting the encoding to the
# expected answer.  Quantifiers put the queries in UF rather than QF_UF, which
# costs nothing here.
SMT_ORDER_AXIOMS = """\
; Order axioms, quantified.  The same three as KGE000-0.ax, so the two
; encodings are the same theory.
(assert (forall ((x Concept)) (kge_leq x x)))
(assert (forall ((x Concept) (y Concept))
    (=> (and (kge_leq x y) (kge_leq y x)) (= x y))))
(assert (forall ((x Concept) (y Concept) (z Concept))
    (=> (and (kge_leq x y) (kge_leq y z)) (kge_leq x z))))"""


# Assertion names, in the order the axioms appear.  These have to match the
# TPTP names, since one provenance map reads both.
_AX_NAMES = ["ax_leq_reflexive", "ax_leq_antisymmetric", "ax_leq_transitive"]


def _name_asserts(block: str, default_prefix: str, p: dict) -> str:
    """Wrap each bare (assert ...) as (assert (! ... :named <n>)).

    Comments and blank lines pass through.  An assertion already carrying a
    name is left alone.  Order axioms take their TPTP names; everything else
    is numbered under the given prefix and the problem id.

    The prefix is the caller's to supply, and it must be right: a core is
    classified by prefix, so naming a background-theory assertion res_ makes
    Z3 report it as the authority's when it is the parties'.  That is not a
    cosmetic error.  It is the distinction the whole certificate rests on,
    and it showed up as a spurious disagreement between the two provers on
    the two problems whose refutations rest on a declaration.  Hence
    smt2_resource and smt2_background are separate fields, and a problem
    that puts a declaration in the resource block mislabels its own premise.
    """
    out, n, depth, buf = [], 0, 0, []
    for line in block.rstrip().splitlines():
        stripped = line.strip()
        if not buf and (not stripped or stripped.startswith(";")):
            out.append(line)
            continue
        buf.append(line)
        depth += line.count("(") - line.count(")")
        if depth > 0:
            continue
        chunk = "\n".join(buf)
        buf = []
        if ":named" in chunk or not chunk.lstrip().startswith("(assert"):
            out.append(chunk)
            continue
        body = chunk.lstrip()[len("(assert"):].rstrip()
        assert body.endswith(")")
        body = body[:-1].strip()
        if default_prefix == "ax":
            name = _AX_NAMES[n] if n < len(_AX_NAMES) else f"ax_{n}"
        else:
            name = f"{default_prefix}_{p['id'].lower()}_{n}"
        n += 1
        out.append(f"(assert (! {body} :named {name}))")
    return "\n".join(out + buf)


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
    name = f"w_{p['id'].lower()}"

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
    name = f"w_{p['id'].lower()}"
    assertion = (f"(assert (! (not {witness}) :named {name}))" if negate
                 else f"(assert (! {witness} :named {name}))")
    status = "unsat" if p[f"expected_q{q}"].lower().startswith("unsat") else "sat"

    header = SMTHeader(
        file     = f"{p['id']}-{q}.smt2",
        domain   = "kb",
        title    = f"{p['name']} ({label})",
        status   = status,
        comments = f"Query {q} of 2.  Verdict is derived from both queries.",
    ).render()

    # A problem that declares the order gets all three axioms; one that does
    # not (a purely nominal operand, where no constraint mentions the order)
    # would reference an undeclared symbol, so it gets none.
    #
    # Every assertion is named, with the same prefixes the TPTP side uses, so
    # that an unsat core from Z3 and a proof from Vampire classify through one
    # provenance map.  Two provers naming the same premises is worth more than
    # either naming them alone.
    decls = p.get("smt2_decls", "").rstrip()
    parts = [
        header,
        f"(set-logic {p.get('smt2_logic', 'UF')})",
        "(set-option :produce-unsat-cores true)",
        "(set-option :produce-models true)",
        decls,
    ]
    if "kge_leq" in decls:
        parts.append(_name_asserts(SMT_ORDER_AXIOMS, "ax", p))

    # Resource and background theory are named apart, so that an unsat core
    # attributes to the same place a TPTP proof does.  smt2_asserts is the
    # older single field: a problem still using it is assumed to hold only
    # resource assertions, and one that does not should be split.
    if "smt2_resource" in p or "smt2_background" in p:
        if p.get("smt2_resource", "").strip():
            parts.append(_name_asserts(p["smt2_resource"], "res", p))
        if p.get("smt2_background", "").strip():
            parts.append(_name_asserts(p["smt2_background"], "bt", p))
    else:
        parts.append(_name_asserts(p["smt2_asserts"], "res", p))

    content = "\n".join(parts + [
        f"; {label}",
        assertion,
        "(check-sat)",
        # An unsat query yields a core, a sat one a model.  Z3 prints an
        # error for the request that does not apply and continues, so both
        # are emitted and the reader takes whichever arrived.
        "(get-unsat-core)",
        "(get-model)",
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


VERDICT_CLASS = {
    "Compatible":   "vrep:Compatible",
    "Incompatible": "vrep:Incompatible",
    "Unknown":      "vrep:Unknown",
}

SORT_CLASS = {"nom": "vrep:nom", "tax": "vrep:tax", "mer": "vrep:mer"}


def _report_block(p: dict) -> str:
    """The expected report, generated from the problem's own fields.

    Written here rather than kept in the ttl string so it cannot drift from
    expected_q1 and expected_q2.
    """
    pid = p["id"]
    verdict = expected_verdict(p)
    cert = p.get("certificate")

    lines = [
        "### Expected result " + "#" * 55,
        "",
        f"drk:{pid}-report a vrep:OperandReport ;",
        f'    dcterms:identifier "{pid}" ;',
        f"    vrep:firstPolicy drk:offer-{pid[3:]} ;",
        f"    vrep:secondPolicy drk:request-{pid[3:]} ;",
        f"    vrep:firstConstraint kgc:{pid}-offer-c1 ;",
        f"    vrep:secondConstraint kgc:{pid}-request-c1 ;",
        f"    vrep:leftOperand odrl:{p['left_operand']} ;",
        f"    vrep:sort {SORT_CLASS[p['sort']]} ;",
        f"    vrep:resource <{p['resource']}> ;",
        f"    vrep:backgroundTheory <{p['background_theory']}> ;",
    ]
    if cert:
        lines.append(f"    vrep:verdict {VERDICT_CLASS[verdict]} ;")
        lines.append(f"    vrep:certificate drk:{pid}-certificate .")
        lines.append("")
        lines.append(f"drk:{pid}-certificate a vrep:{cert['kind']} ;")
        lines.append(f'    rdfs:comment """{cert["comment"]}"""@en ;')
        if cert.get("witness"):
            lines.append(f'    vrep:witness "{cert["witness"]}" ;')
        if cert["kind"] == "Refutation":
            lines.append(f"    vrep:clashingConstraint kgc:{pid}-offer-c1, "
                         f"kgc:{pid}-request-c1 ;")
        for i, (source, label) in enumerate(cert["premises"]):
            end = " ;" if i < len(cert["premises"]) - 1 else " ."
            lines.append(
                f"    vrep:premise [ vrep:premiseSource vrep:{source} ;\n"
                f'                   rdfs:label "{label}"@en ]{end}'
            )
        if not cert["premises"]:
            lines[-1] = lines[-1].rstrip(" ;") + " ."
    else:
        lines.append(f"    vrep:verdict {VERDICT_CLASS[verdict]} .")

    return "\n".join(lines)


def write_case(p: dict, cases_dir: Path) -> Path:
    path = cases_dir / f"{p['id']}.ttl"
    body = p["ttl"].strip()
    needed = [
        ("rdfs:", "@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> ."),
        ("vrep:", "@prefix vrep:    <https://w3id.org/odrl-verdict-report#> ."),
        ("dcterms:", "@prefix dcterms: <http://purl.org/dc/terms/> ."),
    ]
    missing = [line for pre, line in needed if f"@prefix {pre}" not in body]
    if missing:
        body = "\n".join(missing) + "\n" + body
        body = body.replace(
            "@prefix vrep:",
            "@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .\n@prefix vrep:", 1)
    path.write_text(body + "\n\n" + _report_block(p) + "\n", encoding="utf-8")
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

_CONST = re.compile(r"\b(?:gn|dpv|bcp|loc|ft|lb|tm)_[a-z0-9_]+\b")

# A formula name is the first argument of fof(...).  Names are not terms, so
# they must be removed before scanning, or an axiom called gn_france_in_europe
# is mistaken for a constant.
_LABEL = re.compile(r"(^|\n)(\s*)fof\s*\(\s*[a-zA-Z0-9_]+")


def _terms_only(text: str) -> str:
    return _LABEL.sub(r"\1\2fof(", text)


def collect_vocabulary(axioms_dir: Path) -> set[str]:
    """Constants declared by the resource axiom files, formula names excluded.

    Every .ax except the shared order axioms, which declare no constants.
    A fixed filename list was wrong here: generated slices are named per
    resource and per tag, so the validator was checking new problems against
    whatever hand-written files happened to predate the builders.
    """
    vocab: set[str] = set()
    for path in sorted(axioms_dir.glob("*.ax")):
        if path.name.startswith("KGE"):
            continue
        vocab |= set(_CONST.findall(_terms_only(path.read_text(encoding="utf-8"))))
    return vocab


def validate_problem_constants(p: dict, vocabulary: set[str]) -> None:
    """Refuse a problem naming a constant no resource declares."""
    if p.get("ungrounded"):
        return
    text = _terms_only(p["fof_decls"] + p.get("fof_witness", ""))