"""
certificate.py
==============
Maps prover output onto the certificate vocabulary.

Attribution, not verification
-----------------------------
This module records *which assertions a refutation used*.  It does not
produce a checkable derivation.  A prover's proof uses unification,
demodulation and superposition; the certificate proposition asks for
propositionally valid steps over ground instances.  Turning one into the
other is a normalisation step that does not exist yet.

The distinction has a consequence for the vocabulary.  A quantified
assertion the prover reports, an order axiom or a disjointness assertion of
the background theory, is not itself a legitimate premise for the checker;
its ground instances are, and only the ones the refutation used.  So the
names harvested here are written as `vrep:attributedAssertion`, not as
`vrep:premise`.  `vrep:premise` is reserved for the checker-level ground
instances a normaliser would produce.

Attribution is nonetheless the half a party needs: they withdraw an
assertion, not an instance of one, so naming the quantified formula is
correct at that level.

Provenance by prefix
--------------------
    res_    an assertion of the resource               fromResource
    bt_     an assertion of the background theory      fromBackgroundTheory
    w_      a conjunct of the witness condition        fromConstraints
    ax_     an order axiom                             fromOrderAxiom
    eq_     an equality axiom                          fromEqualityAxiom

The last is reserved and nothing emits it yet.  A refutation closing an
identity literal against a distinctness assertion uses equality reasoning:
Vampire's proof of the language pair cites a demodulation step.  Whether
those instances become legitimate premises, or the encoding replaces builtin
equality with a predicate, is open, and it reaches into the paper.

Only `bt_` assertions are withdrawable.  The resource is the authority's, the
constraints are the parties' own, and the axioms are the framework's.

Running the provers
-------------------
Vampire discards formula names unless asked to keep them, and the schedule
mode does not always propagate the flag to its children:

    vampire --mode vampire --proof tptp --output_axiom_names on <file>

Z3 needs named assertions and cores enabled:

    (set-option :produce-unsat-cores true)
    (assert (! <formula> :named bt_de_distinct_fr))
    (check-sat)
    (get-unsat-core)
"""

import re

SOURCE = {
    "res": "fromResource",
    "bt":  "fromBackgroundTheory",
    "w":   "fromConstraints",
    "ax":  "fromOrderAxiom",
    "eq":  "fromEqualityAxiom",     # reserved; nothing emits it yet
}

WITHDRAWABLE = {"fromBackgroundTheory"}

# Vampire delimits its proof; anything outside is echoed input or diagnostics.
_PROOF_BLOCK = re.compile(
    r"% SZS output start Proof.*?% SZS output end Proof", re.S)

# fof(f129, axiom, ( ... ), file('KGE000-0.ax', ax_leq_transitive)).
_LEAF = re.compile(r"file\(\s*'[^']*'\s*,\s*([A-Za-z0-9_]+)\s*\)")


class NoProof(Exception):
    """The output contains no proof block."""


class NoAxiomNames(Exception):
    """The proof carries no usable formula names."""


def premises_from_vampire(output: str) -> list[str]:
    """Leaf formula names from a Vampire refutation.

    Reads the proof block only.  A leaf whose name was lost is kept as the
    literal 'unknown' rather than dropped: dropping it would understate the
    premise count and make a comparison fail on the wrong side.
    """
    m = _PROOF_BLOCK.search(output)
    if not m:
        raise NoProof(
            "no proof block in the output.  Either the query was satisfiable, "
            "or --proof was not in effect.")
    names = list(dict.fromkeys(_LEAF.findall(m.group(0))))
    if names and all(n == "unknown" for n in names):
        raise NoAxiomNames(
            "every premise reported as 'unknown'.  Re-run with "
            "--output_axiom_names on; with --mode casc the flag may not "
            "reach the child strategy, so --mode vampire is safer.")
    return names


def premises_from_z3(output: str) -> tuple[str, list[str]]:
    """The status and the core names from Z3.

    Returns ("unsat", names) with names possibly empty: an unsatisfiable
    query with an empty core is a real state, meaning the witness condition
    is contradictory on its own.  Anything else returns the status and no
    names, so a solver error is not mistaken for a core.
    """
    lines = [l.strip() for l in output.splitlines() if l.strip()]
    status = next((l for l in lines if l in ("sat", "unsat", "unknown")), None)
    if status != "unsat":
        return (status or "no-status"), []
    i = lines.index("unsat")
    for line in lines[i + 1:]:
        if line.startswith("(") and not line.startswith("(error"):
            return "unsat", [n for n in line.strip("()").split() if n]
    return "unsat", []


def classify(names: list[str]) -> dict:
    """Split names by provenance prefix.

    An unrecognised prefix, and a name the prover lost, both land in
    `unclassified`.  Neither is attributed by default: a premise whose origin
    cannot be determined is a defect to report, not a guess to make.
    """
    out = {v: [] for v in SOURCE.values()}
    out["unclassified"] = []
    for n in names:
        prefix = n.split("_", 1)[0]
        out.setdefault(SOURCE.get(prefix, "unclassified"), []).append(n) \
            if prefix in SOURCE else out["unclassified"].append(n)
    return out


def withdrawable(classified: dict) -> list[str]:
    return [n for src in WITHDRAWABLE for n in classified[src]]


def to_turtle(problem_id: str, kind: str, classified: dict,
              labels: dict | None = None, witness: str | None = None,
              artefact: str | None = None, prover: str | None = None) -> str:
    """The observed certificate.

    Writes `vrep:attributedAssertion`, not `vrep:premise`: these are the
    assertions the refutation used, not the ground instances a checker would
    replay.  `artefact` points at the raw proof, as provenance rather than as
    a checked object.
    """
    labels = labels or {}
    lines = [f"kgc:{problem_id}-observed a vrep:{kind} ;"]
    if prover:
        lines.append(f'    vrep:producedBy "{prover}" ;')
    if artefact:
        lines.append(f"    vrep:proofArtefact <{artefact}> ;")
    if witness:
        lines.append(f"    vrep:witness {witness} ;")

    entries = []
    for source in SOURCE.values():
        for n in classified[source]:
            entries.append(
                f"    vrep:attributedAssertion [\n"
                f"        vrep:premiseSource vrep:{source} ;\n"
                f'        vrep:formulaName "{n}" ;\n'
                f'        rdfs:label "{labels.get(n, n)}"@en ]')
    for n in classified["unclassified"]:
        entries.append(
            f"    vrep:attributedAssertion [\n"
            f"        vrep:premiseSource vrep:unclassified ;\n"
            f'        vrep:formulaName "{n}" ]')

    if entries:
        lines.append(" ;\n".join(entries) + " .")
    else:
        lines[-1] = lines[-1].rstrip(" ;") + " ."
    return "\n".join(lines)


def compare(expected: dict, observed: dict) -> list[str]:
    """Differences between the expected and observed attribution.

    A verdict right for the wrong reason shows up here and nowhere else.
    """
    diffs = []
    for source in SOURCE.values():
        e, o = len(expected.get(source, [])), len(observed.get(source, []))
        if e != o:
            diffs.append(f"{source}: expected {e}, observed {o}")
    if observed["unclassified"]:
        diffs.append("unattributable: " + ", ".join(observed["unclassified"]))
    return diffs