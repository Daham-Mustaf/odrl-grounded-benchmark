"""
gen_primitives.py
=================
Generates KGE000-0.ax, the framework axioms.

Three formulae: the order is reflexive, antisymmetric and transitive.

These are not the only quantified formulae in a query.  A disjointness
assertion of the background theory denies a common lower bound, so it is
universally quantified too.  Resource assertions, distinctness assertions and
the conjuncts of a witness condition are ground.  Bernays-Schoenfinkel
membership follows from every quantifier being universal and the signature
being function-free, not from groundness.

Profile-independent.  A profile declares which relation a resource supplies
and how the order is to be read, subsumption at tax or parthood at mer, but
the order is the same partial order either way, so one file serves all three
sorts.  This is the same observation the paper makes about isA and isPartOf:
one function on one order, differing only in the sort their operand carries.

Usage:
    uv run generators/gen_primitives.py
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from header import AXHeader, ax_comment

VERSION = "2.0"
EXPECTED_COUNT = 3

BODY = """\
% ==========================================================================
% The order.  Read as subsumption at tax and as parthood at mer, according
% to the sort the profile declares; the axioms are the same either way.
%
% Quantified content of a query: these three axioms, and the disjointness
% assertions of the background theory, which deny a common lower bound and
% are therefore universal as well.  Resource assertions, distinctness
% assertions and witness conjuncts are ground.  All quantifiers are
% universal and there are no function symbols, which is what places the
% queries in the Bernays-Schoenfinkel class.
% ==========================================================================

fof(ax_leq_reflexive, axiom,
    ![X]: kge_leq(X, X)).

fof(ax_leq_antisymmetric, axiom,
    ![X, Y]:
      ((kge_leq(X, Y) & kge_leq(Y, X)) => X = Y)).

fof(ax_leq_transitive, axiom,
    ![X, Y, Z]:
      ((kge_leq(X, Y) & kge_leq(Y, Z)) => kge_leq(X, Z))).

% ==========================================================================
% Not here, and deliberately.
%
% Disjointness has no predicate.  A disjointness assertion is written where
% it is declared, as the denial of a common lower bound:
%
%     fof(bg_disj_a_b, axiom, ~ ? [X] : (kge_leq(X, a) & kge_leq(X, b))).
%
% Symmetry, the forcing of distinctness, and the impossibility of a concept
% being disjoint from itself all follow from that shape.  A predicate with
% those three as axioms would stipulate what the semantics derives.
%
% Operator denotations have no axioms.  They are computed over the concepts
% the grounding names and emitted as ground formulae inside each query.
% Axiomatising them is what encoded the wrong quantifier structure in the
% previous version of this benchmark.
%
% There is no concept-membership predicate.  A witness condition is built
% from the named concepts, so nothing can range outside them.
%
% Equality is the provers' builtin.  A refutation therefore uses equality
% reasoning: closing the language pair needs symmetry of = over the
% distinctness assertion, and Vampire's proof of it cites a demodulation
% step.  Demodulation is not propositionally valid over the atoms, so a
% checker for these refutations must admit ground instances of the equality
% axioms among its legitimate premises, or the encoding must replace =
% by an explicit predicate carrying them.  The choice is open and it
% reaches into the paper: the certificate proposition currently says no
% theory reasoning is needed.
% ==========================================================================
"""


def generate_kge000() -> str:
    note = (
        "Included by every query file.  Includes nothing itself.\n"
        "Formula names carry provenance: res_ for resource assertions,\n"
        "bt_ for background-theory assertions, w_ for witness conjuncts,\n"
        "and ax_ for the axioms here.  A prover reports its premises by\n"
        "name, so the prefix is what a checker reads.  Only bt_ premises\n"
        "are withdrawable by a party."
    )
    header = AXHeader(
        file    = "KGE000-0.ax",
        domain  = "kb",
        title   = "Framework axioms: the order",
        version = VERSION,
        english = (
            "The order is a partial order.  A profile declares how it is to "
            "be read, as subsumption at tax or as parthood at mer, but the "
            "axioms do not depend on that reading, so one file serves every "
            "sort and every profile.\n"
            "Quantified content of a query: these three axioms and the "
            "disjointness assertions of the background theory.  Resource "
            "assertions, distinctness assertions and witness conjuncts are "
            "ground.  All quantifiers are universal and the signature is "
            "function-free."
        ),
        comments = ax_comment(
            BODY,
            "3 order axioms (reflexive, antisymmetric, transitive); no "
            "disjointness predicate, no operator denotations, no concept "
            "guard",
            note),
    ).render()
    return header + "\n" + BODY


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate KGE000-0.ax")
    ap.add_argument("--out-dir", default="problems/axioms")
    ap.add_argument("--stdout", action="store_true")
    args = ap.parse_args()

    content = generate_kge000()
    # Anchored and comment-stripped: the "not here" block shows an example
    # formula, and counting it made this check fail on its own file.
    actual = len(re.findall(r"^fof\(", content, re.M))
    ok = actual == EXPECTED_COUNT

    if args.stdout:
        print(content)
        return 0 if ok else 1

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / "KGE000-0.ax"
    path.write_text(content, encoding="utf-8")
    print(f"Written: {path}  ({actual} formulae, expected {EXPECTED_COUNT}) "
          f"{'ok' if ok else 'MISMATCH'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())