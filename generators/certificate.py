"""
certificate.py
==============
Maps prover output onto the certificate vocabulary.

A prover reports a refutation by naming the formulae it used.  Formula names
in a problem file carry their provenance in the prefix, so the mapping is a
lookup:

    res_...     an assertion of the resource            vrep:fromResource
    bt_...      an assertion of the background theory   vrep:fromBackgroundTheory
    w_...       a conjunct of the witness condition     vrep:fromConstraints
    ax_...      an instance of an order axiom           vrep:fromOrderAxiom

Four sources, not two.  The refutation uses the constraint-derived conjuncts
and may use order-axiom instances; both are premises the checker must accept
as legitimate.  Contestability filters on the first two: a party may withdraw
what they declared, not what the authority published, and not the constraints
they themselves wrote.

Both provers project onto the same names, which is what makes the certificate
independent of how the query was decided.

Vampire discards formula names unless asked to keep them.  Run it as

    vampire --mode casc --proof on --output_axiom_names on <file>

or every premise comes back as `unknown` and nothing can be attributed.

Z3 needs the assertions named and cores enabled:

    (set-option :produce-unsat-cores true)
    (assert (! <formula> :named bt_de_distinct_fr))
    (check-sat)
    (get-unsat-core)
"""

import re

# Vampire:  fof(f129,axiom,( ... ), file('KGC300-1.p',bt_de_distinct_fr)).
_VAMPIRE_LEAF = re.compile(r"file\('[^']*',\s*([A-Za-z0-9_]+)\s*\)")

# Z3:  (bt_de_distinct_fr kgc300_w)
_Z3_CORE = re.compile(r"\(([^()]*)\)")

SOURCE = {
    "res": "fromResource",
    "bt":  "fromBackgroundTheory",
    "w":   "fromConstraints",
    "ax":  "fromOrderAxiom",
}

# A party may withdraw only these.
WITHDRAWABLE = {"fromBackgroundTheory"}


class NoAxiomNames(Exception):
    """Raised when a proof carries no usable formula names."""


def premises_from_vampire(proof: str) -> list[str]:
    """The leaves of a Vampire refutation, by formula name."""
    names = _VAMPIRE_LEAF.findall(proof)
    if not names:
        return []
    if all(n == "unknown" for n in names):
        raise NoAxiomNames(
            "Vampire reported every premise as 'unknown'.  Re-run with "
            "--output_axiom_names on, or provenance cannot be attributed.")
    return [n for n in dict.fromkeys(names) if n != "unknown"]


def premises_from_z3(core_output: str) -> list[str]:
    """The names in a Z3 unsatisfiable core."""
    m = _Z3_CORE.search(core_output.strip())
    if not m:
        return []
    return [n for n in m.group(1).split() if n]


def classify(names: list[str], problem_id: str) -> dict:
    """Split premise names into resource, background theory and the witness.

    An unrecognised prefix is reported rather than guessed: a premise whose
    provenance cannot be determined is a defect in the problem file, not
    something to attribute by default.
    """
    out = {v: [] for v in SOURCE.values()}
    out["unclassified"] = []
    for n in names:
        prefix = n.split("_", 1)[0]
        if prefix in SOURCE:
            out[SOURCE[prefix]].append(n)
        else:
            out["unclassified"].append(n)
    return out


def to_turtle(problem_id: str, kind: str, classified: dict,
              labels: dict | None = None, witness: str | None = None,
              artefact: str | None = None, prover: str | None = None) -> str:
    """The observed certificate, in the report vocabulary.

    The premise attribution is the certificate's contestable part.  The
    checkable derivation is a separate artefact: a prover's own proof uses
    unification and superposition, which are not the propositionally valid
    steps over ground instances the checker specification requires, so the
    raw output has to be normalised before it can be checked.  Until that
    exists, `artefact` points at the raw proof and `prover` records what
    produced it, as provenance rather than as a checked object.
    """
    labels = labels or {}
    pid = problem_id
    lines = [f"kgc:{pid}-observed a vrep:{kind} ;"]
    if prover:
        lines.append(f'    vrep:producedBy "{prover}" ;')
    if artefact:
        lines.append(f"    vrep:proofArtefact <{artefact}> ;")
    if witness:
        lines.append(f"    vrep:witness {witness} ;")
    prem = []
    for source in SOURCE.values():
        for n in classified[source]:
            label = labels.get(n, n)
            prem.append(f"    vrep:premise [ vrep:premiseSource vrep:{source} ;\n"
                        f'                   vrep:formulaName "{n}" ;\n'
                        f'                   rdfs:label "{label}"@en ]')
    if prem:
        lines.append(" ;\n".join(prem) + " .")
    else:
        lines[-1] = lines[-1].rstrip(" ;") + " ."
    return "\n".join(lines)


def compare(expected: dict, observed: dict) -> list[str]:
    """Differences between the expected and the observed premise split.

    A verdict that is right for the wrong reason shows up here and nowhere
    else, which is the point of recording certificates at all.
    """
    diffs = []
    for source in SOURCE.values():
        e, o = len(expected.get(source, [])), len(observed.get(source, []))
        if e != o:
            diffs.append(f"{source}: expected {e} premise(s), observed {o}")
    if observed["unclassified"]:
        diffs.append("unclassified premises: " + ", ".join(observed["unclassified"]))
    return diffs