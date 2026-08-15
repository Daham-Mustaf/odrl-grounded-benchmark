"""
gen_denotation.py
=================

Generates DENOT000-0.ax: constraint denotation and three-valued verdict
semantics. Encodes Definition 4 (Constraint denotation, Table 2),
Definition 5 (Conservative intersection), Definition 6 (Verdict),
and Definition 7 (Forced emptiness) of the paper.

Output:
    Problems/ODRL/KGConstraints/Axioms/DENOT000-0.ax

Usage:
    uv run Generators/KGConstraints/gen_denotation.py
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from header import AXHeader, _ax_comment

VERSION = "1.3"
EXPECTED_COUNT = 15

DENOT000_BODY = """\
% ==========================================================================
% Section A: Operator-specific denotations  [Paper: def:denotation, tab:denotation]
%
% Each problem file ties its constraint tokens to the right den_* shape via
% an in_denotation(X, C) <=> den_<op>(X, G) axiom in fof_extra_decls,
% AND emits denotation_undef(C) when grounding fails (Definition 4).
%
%   eq g         -> {g}                singleton
%   neq g        -> C \\ {g}            complement of singleton (guarded)
%   isA g        -> {x | x leq g}      downward cone
%   isPartOf g   -> {x | x leq g}      downward cone (same as isA)
%   hasPart g    -> {x | g leq x}      upward cone
%   isAnyOf S    -> S                  listed grounded concepts
%   isAllOf S    -> S                  same as isAnyOf for single-valued ops
%   isNoneOf S   -> C \\ S              complement of list (guarded)
%
% Complement operators (neq, isNoneOf) require the kge_concept(X) guard
% to prevent Skolem witnesses outside the resource universe. This restricts
% the complement to the resource's declared concept set, faithful to
% Definition 4 where C is the resource's concept set.
%
% Note: complement operators are non-monotone (Remark 2 / Proposition 1
% boundary). KGC810 demonstrates the boundary via countermodel.
% ==========================================================================

fof(den_eq, axiom,
    ![X, G]:
      (den_eq(X, G) <=> X = G)).

fof(den_neq, axiom,
    ![X, G]:
      (den_neq(X, G) <=> (kge_concept(X) & X != G))).

fof(den_isa, axiom,
    ![X, G]:
      (den_isa(X, G) <=> in_downward_cone(X, G))).

fof(den_ispartof, axiom,
    ![X, G]:
      (den_ispartof(X, G) <=> in_downward_cone(X, G))).

fof(den_haspart, axiom,
    ![X, G]:
      (den_haspart(X, G) <=> in_upward_cone(X, G))).

fof(den_isanyof, axiom,
    ![X, S]:
      (den_isanyof(X, S) <=> in_list(X, S))).

fof(den_isallof, axiom,
    ![X, S]:
      (den_isallof(X, S) <=> in_list(X, S))).

fof(den_isnoneof, axiom,
    ![X, S]:
      (den_isnoneof(X, S) <=> (kge_concept(X) & ~in_list(X, S)))).

% ==========================================================================
% Section B: Forced emptiness               [Paper: def:forced-disj]
%
% Definition 7 is semantic: emptiness holds in every extension consistent
% with Assumption 1. The FOF axiomatization realizes a sound (incomplete)
% enumeration of syntactic patterns sufficient for forced_empty:
%
%   (B1) Downward-pair pattern.
%        Witness ancestors A, B with kge_disjoint(A, B), every member
%        of each denotation below A and B respectively. Under Assumption 1,
%        no concept lies below both A and B, so the intersection is empty
%        in every consistent extension. Covers eq/eq, eq/isA, isA/isA,
%        isPartOf-shaped pairs, and any case where both denotations are
%        downward-bounded.
%
%   (B2) List-vs-eq pattern.
%        c_offer's denotation is a list S, c_request's is the singleton
%        {g}, and every list member is asserted disjoint from g. The
%        intersection is empty in every consistent extension by
%        Assumption 1 applied pointwise. Covers isAnyOf/eq and isAllOf/eq
%        Conflict cases over registry-uniqueness resources (e.g., BCP 47).
%
%   (B3) neq-vs-eq pattern.
%        c_offer denotes C \\ {g} (c_neq(g)), c_request denotes {g}
%        (c_eq(g)). Intersection is empty by definition: no concept
%        equal to g lies in C \\ {g}. This is structurally forced and
%        does not require any disjointness assertion in the resource.
%
%   (B4) isNoneOf-vs-eq pattern.
%        c_offer denotes C \\ S (c_isnoneof(S)), c_request denotes {g}
%        (c_eq(g)) where g is in the list S. Intersection is empty
%        because g is excluded from c_isnoneof's denotation by
%        construction. Covers isNoneOf/eq Conflict on the listed
%        member.
%
% B1 through B4 are sufficient (one-way implications) feeding the same
% forced_empty predicate. forced_empty is not closed by a biconditional;
% it is a primitive that holds when any pattern fires. Other patterns
% (e.g., hasPart upward cones) require additional sufficient-condition
% axioms; see Remark on encoding completeness in the paper.
% ==========================================================================

fof(forced_empty_b1_downward_pair, axiom,
    ![C1, C2]:
      ((?[A, B]:
          (kge_disjoint(A, B) &
           (![X]: (in_denotation(X, C1) => in_downward_cone(X, A))) &
           (![X]: (in_denotation(X, C2) => in_downward_cone(X, B)))))
        => forced_empty(C1, C2))).

fof(forced_empty_b2_list_eq, axiom,
    ![C1, C2, S, G]:
      (((![Y]: (in_list(Y, S) => kge_disjoint(Y, G))) &
        (![X]: (in_denotation(X, C1) <=> in_list(X, S))) &
        (![X]: (in_denotation(X, C2) <=> X = G))) =>
        forced_empty(C1, C2))).

fof(forced_empty_b3_neq_eq, axiom,
    ![C1, C2, G]:
      (((![X]: (in_denotation(X, C1) <=> (kge_concept(X) & X != G))) &
        (![X]: (in_denotation(X, C2) <=> X = G))) =>
        forced_empty(C1, C2))).

fof(forced_empty_b4_isnoneof_eq, axiom,
    ![C1, C2, S, G]:
      (((![X]: (in_denotation(X, C1) <=> (kge_concept(X) & ~in_list(X, S)))) &
        (![X]: (in_denotation(X, C2) <=> X = G)) &
        in_list(G, S)) =>
        forced_empty(C1, C2))).

% ==========================================================================
% Section C: Three-valued verdict           [Paper: def:conflict, def:sqcap]
%
% Open World Assumption semantics with undef propagation:
%   Compatible : both denotations defined, witness X exists in both
%   Conflict   : both denotations defined, intersection empty, disj-forced
%   Unknown    : (a) either denotation undefined (head case of def:conflict)
%             or (b) intersection empty but not disj-forced (tail case)
% ==========================================================================

fof(verdict_compatible_def, axiom,
    ![C1, C2]:
      (verdict_compatible(C1, C2) <=>
        (~denotation_undef(C1) & ~denotation_undef(C2) &
         ?[X]: (in_denotation(X, C1) & in_denotation(X, C2))))).

fof(verdict_conflict_def, axiom,
    ![C1, C2]:
      (verdict_conflict(C1, C2) <=>
        (~denotation_undef(C1) & ~denotation_undef(C2) &
         (![X]: ~(in_denotation(X, C1) & in_denotation(X, C2))) &
         forced_empty(C1, C2)))).

fof(verdict_unknown_def, axiom,
    ![C1, C2]:
      (verdict_unknown(C1, C2) <=>
        (~verdict_compatible(C1, C2) & ~verdict_conflict(C1, C2)))).
"""


def generate_denot000() -> str:
    name = "DENOT000-0.ax"
    note = (
        "Depends on KGE000-0.ax (in_downward_cone, in_upward_cone,\n"
        "kge_disjoint, kge_disjoint_propagation, kge_concept).\n"
        "Problem files emit, in order:\n"
        "  include('Axioms/KGE000-0.ax').\n"
        "  include('Axioms/DENOT000-0.ax').\n"
        "  include('Axioms/<resource>.ax').    (added in later pass)\n"
        "Hooks expected from problem files:\n"
        "  in_denotation(X, C)    -- via den_<op>(X, G) bridge\n"
        "  grounded_as(C, G)      -- which concept C is grounded to\n"
        "  denotation_undef(C)    -- assert when grounding fails (Def 4)\n"
        "  in_list(X, S)          -- for isAnyOf/isAllOf/isNoneOf operands\n"
        "  kge_concept(X)         -- asserted by resource files for each constant\n"
        "No axiom file self-includes this file."
    )
    header = AXHeader(
        file     = name,
        domain   = "kb",
        title    = "Constraint denotation and three-valued verdict semantics",
        version  = VERSION,
        english  = (
            "Layer 1 axioms for KG-grounded constraint conflict detection.\n"
            "Section A: operator-specific denotation predicates for all\n"
            "eight operators (eq, neq, isA, isPartOf, hasPart, isAnyOf,\n"
            "isAllOf, isNoneOf). Complement operators (neq, isNoneOf) use\n"
            "the kge_concept(X) guard to restrict the complement to the\n"
            "resource's declared concept universe.\n"
            "Section B: forced emptiness (Definition 7), realized as a sound\n"
            "(incomplete) enumeration of four syntactic patterns: B1\n"
            "(downward-pair), B2 (list-vs-eq), B3 (neq-vs-eq), and B4\n"
            "(isNoneOf-vs-eq), each sufficient for forced_empty under\n"
            "Assumption 1.\n"
            "Section C: three-valued verdict (Compatible, Conflict, Unknown)\n"
            "with Open World Assumption semantics and undef propagation.\n"
            "Conflict requires both empty intersection and forced emptiness;\n"
            "absence of witness alone yields Unknown."
        ),
        refs     = ["kgc2026"],
        comments = _ax_comment(
            DENOT000_BODY,
            "8 operator denotations (eq, neq, isA, isPartOf, hasPart, isAnyOf, "
            "isAllOf, isNoneOf) + 4 forced emptiness patterns (B1 downward-pair, "
            "B2 list-vs-eq, B3 neq-vs-eq, B4 isNoneOf-vs-eq) + "
            "3 verdict predicates (compatible, conflict, unknown)",
            note,
        ),
        fof_text = DENOT000_BODY,
    ).render()
    return header + "\n" + DENOT000_BODY


def main():
    parser = argparse.ArgumentParser(description="Generate DENOT000-0.ax")
    parser.add_argument("--out-dir",
                        default="Problems/ODRL/KGConstraints/Axioms")
    parser.add_argument("--stdout", action="store_true")
    args = parser.parse_args()
    content = generate_denot000()
    actual = content.count("fof(")
    ok = "✓" if actual == EXPECTED_COUNT else "✗"
    if args.stdout:
        print(content)
        print(f"\n{actual} formulae (expected {EXPECTED_COUNT}) {ok}",
              file=sys.stderr)
        return
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "DENOT000-0.ax"
    path.write_text(content, encoding="utf-8")
    print(f"Written : {path}  ({actual} formulae, expected {EXPECTED_COUNT}) {ok}")


if __name__ == "__main__":
    main()