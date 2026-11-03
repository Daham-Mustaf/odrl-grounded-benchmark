%------------------------------------------------------------------------------
% File     : KGC031+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use in PDF only against use in PDF/A-1a only: some use meets both
% Version  : Especial.
% English  : A German library permits use in PDF only. A French library's
%            policy commits to use in PDF/A-1a only. This problem states that
%            some use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag
%            v1.1.1
% Source   : [Mus26]
% Names    : KGC320-1 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC320 is Unknown. Its two problems state that some use meets the
%            two policies (KGC031) and that no use does (KGC032). A pair of
%            policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent. Here the first is Satisfiable and the
%            second Satisfiable.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').

fof(w_kgc320, axiom,
    ft_pdf = ft_pdfa1a).
%------------------------------------------------------------------------------
