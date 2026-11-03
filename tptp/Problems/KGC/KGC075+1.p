%------------------------------------------------------------------------------
% File     : KGC075+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Distribute in German only against distribute in French only: some use meets both
% Version  : Especial.
% English  : A publisher distributes in German. A licensee's policy commits to
%            French. The registry rule that different primary subtags name
%            different languages is adopted. This problem states that some use
%            meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag
%            v1.1.1
% Source   : [Mus26]
% Names    : KGC370-1 [Mus26]

% Status   : Unsatisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC370 is Incompatible. Its two problems state that some use
%            meets the two policies (KGC075) and that no use does (KGC076). A
%            pair of policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent. Here the first is Unsatisfiable and the
%            second Satisfiable.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+1.ax').

fof(bg_dist_bcp47_de_fr, axiom,
    bcp_de != bcp_fr).

fof(w_kgc370, axiom,
    bcp_de = bcp_fr).
%------------------------------------------------------------------------------
