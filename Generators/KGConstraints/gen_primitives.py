"""
gen_primitives.py
=================
Generates KGE000-0.ax: generic knowledge-graph primitives for grounding
resources.  Encodes Definition 3 (grounding resource R = (C, leq, disjoint, gamma))
and Assumption 1 (disjointness propagation) of the paper.

Output:
    Problems/ODRL/KGConstraints/Axioms/KGE000-0.ax
Usage:
    uv run Generators/KGConstraints/gen_primitives.py
"""
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from header import AXHeader, _ax_comment

VERSION = "1.1"
EXPECTED_COUNT = 8

KGE000_BODY = """\
% ==========================================================================
% Partial order kge_leq(X, Y)                [Paper: def:resource]
% Read "X is at-or-below Y" taxonomically (rdfs:subClassOf*) or
% mereologically (geo:sfWithin) depending on the grounding resource.
% ==========================================================================
fof(kge_leq_reflexive, axiom,
    ![X]: kge_leq(X, X)).

fof(kge_leq_transitive, axiom,
    ![X, Y, Z]:
      ((kge_leq(X, Y) & kge_leq(Y, Z)) => kge_leq(X, Z))).

fof(kge_leq_antisymmetric, axiom,
    ![X, Y]:
      ((kge_leq(X, Y) & kge_leq(Y, X)) => X = Y)).

% ==========================================================================
% Asserted disjointness kge_disjoint(X, Y)   [Paper: def:resource]
% Primitive, not derived from the order.  Open-world: silence in kge_leq
% is not evidence of disjointness.
% ==========================================================================
fof(kge_disjoint_symmetric, axiom,
    ![X, Y]:
      (kge_disjoint(X, Y) <=> kge_disjoint(Y, X))).

fof(kge_disjoint_irreflexive, axiom,
    ![X]: ~ kge_disjoint(X, X)).

% ==========================================================================
% Disjointness propagation                   [Paper: assm:disj-prop]
% If two concepts are asserted disjoint, no concept can lie below both.
% Coherence condition between kge_disjoint and kge_leq.  Load-bearing for
% forced_empty in DENOT000-0.ax and hence Theorem 1 soundness.
% ==========================================================================
fof(kge_disjoint_propagation, axiom,
    ![A, B, X]:
      ((kge_disjoint(A, B) & kge_leq(X, A) & kge_leq(X, B)) => $false)).

% ==========================================================================
% Cones used by isA / isPartOf (downward) and hasPart (upward)
% ==========================================================================
fof(kge_downward_cone, axiom,
    ![X, G]:
      (in_downward_cone(X, G) <=> kge_leq(X, G))).

fof(kge_upward_cone, axiom,
    ![X, G]:
      (in_upward_cone(X, G) <=> kge_leq(G, X))).

% ==========================================================================
% Concept membership kge_concept(X)          [Paper: def:resource]
%
% Predicate kge_concept/1 declares which terms are members of the
% grounding resource's universe of concepts. Open-world: no closure
% axiom here. Each grounding resource (BCP47000, DPV000, GN000)
% asserts kge_concept(c) for every constant c it declares.
%
% Used by:
%   - den_neq, den_isnoneof in DENOT000-0.ax (concept-membership guard
%     preventing Skolem witnesses outside the resource).
%   - in_concepts_R, in_concepts_R_prime in MONO000-0.ax (lifted to the
%     two-resource extension setting).
%
% No axiom emitted at this layer; the predicate is purely declarative.
% ==========================================================================
"""


def generate_kge000() -> str:
    name = "KGE000-0.ax"
    note = (
        "Loaded directly by every problem file (flat include architecture).\n"
        "Problems also include DENOT000-0.ax and a resource-specific\n"
        "knowledge file (added in a later pass).\n"
        "The grounding function gamma : V -> C of Definition 3 is realized\n"
        "per problem via grounded_as/2 hooks, not at the foundation level.\n"
        "No axiom file self-includes this file."
    )
    header = AXHeader(
        file     = name,
        domain   = "kb",
        title    = "Generic knowledge-graph primitives for grounding resources",
        version  = VERSION,
        english  = (
            "Foundation axioms for KG-grounded ODRL constraints.\n"
            "Defines the two primitive relations every grounding resource\n"
            "must provide: kge_leq/2 (partial order, taxonomic or\n"
            "mereological) and kge_disjoint/2 (symmetric irreflexive),\n"
            "the disjointness propagation coherence condition (Assumption 1),\n"
            "and downward and upward cone predicates used by isA, isPartOf,\n"
            "and hasPart denotations. Declares kge_concept/1 for resource\n"
            "universe membership (asserted per constant by resource files).\n"
            "The grounding function gamma is realized per problem via\n"
            "grounded_as/2. Concrete grounding resources (GeoNames, DPV,\n"
            "BCP 47) are added in a later pass and extend these primitives\n"
            "with resource-specific facts."
        ),
        refs     = ["kgc2026"],
comments = _ax_comment(
        KGE000_BODY,
        "3 order (reflexive, transitive, antisymmetric) + "
        "2 disjointness (symmetric, irreflexive) + "
        "1 disjointness propagation (Assumption 1) + "
        "2 cones (downward, upward) + "
        "kge_concept/1 namespace declaration",
        note,
    ),
        fof_text = KGE000_BODY,
    ).render()
    return header + "\n" + KGE000_BODY


def main():
    parser = argparse.ArgumentParser(description="Generate KGE000-0.ax")
    parser.add_argument("--out-dir",
                        default="Problems/ODRL/KGConstraints/Axioms")
    parser.add_argument("--stdout", action="store_true")
    args = parser.parse_args()
    content = generate_kge000()
    actual = content.count("fof(")
    ok = "✓" if actual == EXPECTED_COUNT else "✗"
    if args.stdout:
        print(content)
        print(f"\n{actual} formulae (expected {EXPECTED_COUNT}) {ok}",
              file=sys.stderr)
        return
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "KGE000-0.ax"
    path.write_text(content, encoding="utf-8")
    print(f"Written : {path}  ({actual} formulae, expected {EXPECTED_COUNT}) {ok}")


if __name__ == "__main__":
    main()