%------------------------------------------------------------------------------
% File     : KGC086+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Distribute in both Dutch and French against distribute in Dutch only: no use meets both
% Version  : Especial.
% English  : A Belgian federal publisher requires distribution in both Dutch
%            and French. The licensee distributes in Dutch only. The registry
%            rule that different primary subtags name different languages is
%            adopted. This problem states that no use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag
%            v1.1.1
% Source   : [Mus26]
% Names    : KGC376-2 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC376 is Incompatible. Its two problems state that some use
%            meets the two policies (KGC085) and that no use does (KGC086). A
%            pair of policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent. Here the first is Unsatisfiable and the
%            second Satisfiable.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+1.ax').

fof(bg_dist_bcp47_nl_fr, axiom,
    bcp_nl != bcp_fr).

fof(w_kgc376, axiom,
    ~ ( bcp_fr = bcp_nl )).
%------------------------------------------------------------------------------
