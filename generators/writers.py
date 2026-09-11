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
    left_operand, sort, resource, background_theory
    binding           the profile entry that fixed the reading
    includes          list of .ax file names
    fof_decls         constants, groundings, resource hooks
    fof_witness       the witness condition W(K), as a FOF formula
    expected_q1       "Satisfiable" | "Unsatisfiable"
    expected_q2       "Satisfiable" | "Unsatisfiable"
    unknown_reason    "epistemic" | "ungrounded"; required when the
                      verdict is Unknown
    smt2_decls        SMT-LIB declarations
    smt2_resource     SMT-LIB assertions for R, named res_
    smt2_background   SMT-LIB assertions for B, named bt_
    smt2_asserts      the older single field; assumed to hold R only
    smt2_witness      the witness condition, as an SMT-LIB term
    certificate       dict with comment and premises; the comment becomes
                      the report's rdfs:comment, the premises stay in the
                      proof artefact
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


def _resolve(value: str, p: dict) -> str:
    """The concept a value names under this problem's binding.

    Recorded in the manifest, not computed: grounding procedures live in
    design/grounding.py and are not wired in. A value with no entry is
    assumed already to be a concept.
    """
    return p.get("grounding", {}).get(value, value)


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
        english  = p.get("summary", p.get("description", p["name"])),
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


def write_expected_certificate(p: dict, cert_dir: Path) -> Path:
    """The certificate the problem's author says the refutation should have.

    NOT YET ENABLED. The five vrep: terms this writes are not in
    vocab/verdict-report.ttl: Certificate, fromResource,
    fromBackgroundTheory, fromConstraints, fromOrderAxiom. Define them
    there before any caller passes cert_dir, or this writes a file whose
    every term is invented.

    Written at generation time, from the problem's own declaration, so
    that run_certify can compare it against what the provers produce. A
    verdict right for the wrong reason is invisible without this file:
    the two queries still return the expected statuses, and the premises
    the refutation used are never checked against the premises the
    problem claims it needs.
    """
    cert_dir.mkdir(parents=True, exist_ok=True)
    c = p["certificate"]
    by_class = {}
    for source, description in c.get("premises", []):
        by_class.setdefault(source, []).append(description)
    lines = [
        f"# Expected certificate for {p['id']}, from the problem's own",
        f"# declaration. Compare with {p['id']}-observed.ttl.",
        "",
        "@prefix vrep:    <https://w3id.org/odrl-kb/verdict-report#> .",
        "@prefix dcterms: <http://purl.org/dc/terms/> .",
        "",
        f"<urn:certificate:{p['id']}:expected> a vrep:Certificate ;",
        f'    dcterms:identifier "{p["id"]}" ;',
    ]
    for source, descriptions in sorted(by_class.items()):
        for d in descriptions:
            lines.append(f'    vrep:{source} "{d}"@en ;')
    lines.append(f'    rdfs:comment """{c.get("comment", "")}"""@en .')
    path = cert_dir / f"{p['id']}-expected.ttl"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_problem(p: dict, out_dir: Path, cases_dir: Path,
                  cert_dir: Path | None = None) -> list[Path]:
    """Write both queries, the case file, and the expected certificate.

    The case file holds the two policies and the expected report in one
    graph, so a reader sees the question and the answer together.

    cert_dir is optional and defaults to skipping the expected certificate:
    write_problem has existing callers that do not yet pass it, and making
    it required here would break them rather than the feature landing
    incrementally.
    """
    written = []
    if not p.get("ungrounded"):
        for q in (1, 2):
            written.append(write_fof(p, q, out_dir))
            written.append(write_smt2(p, q, out_dir))
    written.append(write_case(p, cases_dir))
    if p.get("certificate") and cert_dir is not None:
        written.append(write_expected_certificate(p, cert_dir))
    return written


# SATISFACTION_STATE = {
#     "Compatible":   "report:Satisfied",
#     "Incompatible": "report:Unsatisfied",
#     "Unknown":      "vrep:Undetermined",
# }

# # vrep:Ungrounded is already the reason class used by undeterminedReason
# # (see the vocab file), so it can't also name the certificate's own type
# # without one IRI meaning two things.  Refutation and whatever the
# # Epistemic-certificate class turns out to be called don't have this
# # problem, so only Ungrounded needs remapping here.
# CERTIFICATE_CLASS = {"Ungrounded": "UngroundedCertificate"}


# The verdict-to-state mapping, stated once. The vocabulary's header
# carries the same table in prose; if the two ever disagree, the
# vocabulary is right and this is the copy that drifted.
SATISFACTION_STATE = {
    "Compatible":   "report:Satisfied",
    "Incompatible": "report:Unsatisfied",
    "Unknown":      "vrep:Undetermined",
}

def _report_block(p: dict) -> str:
    """The expected report, from the problem's own fields.

    The report carries the verdict, the two constraints it is about, the
    binding that decided the reading, one sentence saying why the verdict
    is what it is, and a reference to the evidence. It does not carry the
    evidence itself: the premises a refutation rests on are named inside
    the proof artefact, and writing them a second time here would give
    one fact two records that can disagree without anything noticing.

    The generic explanation of what a satisfaction state means lives in
    vocab/verdict-report.ttl, where it is said once. What belongs here is
    the particular: what this resource publishes about these concepts,
    and what follows from it.
    """
    pid = p["id"]
    verdict = expected_verdict(p)

    lines = [
        "### Expected result " + "#" * 55,
        "",
        f"drk:{pid}-report a vrep:OperandVerdictReport ;",
        f'    dcterms:identifier "{pid}" ;',
        f"    report:policy drk:offer-{pid[3:]} ;",
        f"    report:policyRequest drk:request-{pid[3:]} ;",
        f"    report:constraint kgc:{pid}-offer-c1 ;",
        f"    vrep:constraintRequest kgc:{pid}-request-c1 ;",
    ]

    # The binding is what fixed the reading; a report without one does
    # not say what its verdict was relative to.
    if p.get("binding"):
        lines.append(f"    vrep:binding <{p['binding']}> ;")

    # One sentence: what the resource publishes about these concepts, and
    # what follows. Not how the procedure found it.
    comment = p.get("certificate", {}).get("comment")
    if comment:
        lines.append(f'    rdfs:comment """{comment}"""@en ;')
    if p.get("summary"):
        lines.append(f'    dcterms:description """{p["summary"]}"""@en ;')

    lines.append(f"    report:satisfactionState "
                 f"{SATISFACTION_STATE[verdict]} ;")

    if verdict == "Unknown":
        if not p.get("unknown_reason"):
            raise ValueError(
                f"{pid}: Unknown verdict with no unknown_reason. The "
                f"report cannot say whether a value failed to ground or "
                f"the resource left the question open, and those are "
                f"repaired differently: the first by correcting the "
                f"policy or the binding, the second by a further "
                f"declaration.")
        lines.append(f"    vrep:undeterminedReason "
                     f"vrep:{p['unknown_reason'].capitalize()} ;")

    # An ungrounded problem builds no queries, so there is nothing to
    # point at. Which value failed is recoverable by applying the
    # binding's grounding rule to the constraint named above.
    if p.get("ungrounded"):
        lines[-1] = lines[-1].rstrip(" ;") + " ."
    else:
        which = 1 if p["expected_q1"] == "Unsatisfiable" else 2
        lines.append(f"    vrep:certificate "
                     f"<certificates/{pid}-{which}.tstp> .")

    return "\n".join(lines)


def write_case(p: dict, cases_dir: Path) -> Path:
    """The case file: the two policies and the expected report, one graph.

    A reader sees the question and the answer together, which is the
    point of keeping them in one file.
    """
    path = cases_dir / f"{p['id']}.ttl"
    body = p["ttl"].strip()

    # Prefixes the report block needs that the policy TTL did not
    # declare. Prepended once. An earlier version also ran a replace
    # that inserted rdfs: a second time, which is where the duplicate
    # @prefix rdfs: in every case file came from.
    needed = [
        ("rdfs:",
         "@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> ."),
        ("report:",
         "@prefix report:  <https://w3id.org/force/compliance-report#> ."),
        ("vrep:",
         "@prefix vrep:    <https://w3id.org/odrl-kb/verdict-report#> ."),
        ("dcterms:",
         "@prefix dcterms: <http://purl.org/dc/terms/> ."),
    ]
    missing = [line for pre, line in needed if f"@prefix {pre}" not in body]
    if missing:
        body = "\n".join(missing) + "\n" + body

    path.write_text(body + "\n\n" + _report_block(p) + "\n",
                    encoding="utf-8")
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
    """Refuse a problem naming a constant no resource declares.

    A typo in a concept name is otherwise invisible: the query is well
    formed, the prover answers, and the answer is about a constant no
    vocabulary contains.
    """
    if p.get("ungrounded"):
        return
    text = _terms_only(p["fof_decls"] + p.get("fof_witness", ""))
    unknown = sorted(set(_CONST.findall(text)) - vocabulary)
    if unknown:
        raise ValueError(
            f"{p['id']}: {', '.join(unknown)} named by the problem but "
            f"declared by no resource axiom file. Either the constant is "
            f"mistyped, or the resource it belongs to has not been built.")