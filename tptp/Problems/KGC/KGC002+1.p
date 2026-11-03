%------------------------------------------------------------------------------
% File     : KGC002+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use in German only against use in French only: no use meets both
% Version  : Especial.
% English  : A German library permits use of its manuscripts in German only. A
%            French library's policy commits to use in French only. This
%            problem states that no use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag
%            v1.1.1
% Source   : [Mus26]
% Names    : KGC300-2 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC300 is Incompatible. Its two problems state that some use
%            meets the two policies (KGC001) and that no use does (KGC002). A
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

fof(w_kgc300, axiom,
    ~ ( bcp_de = bcp_fr )).
%------------------------------------------------------------------------------
