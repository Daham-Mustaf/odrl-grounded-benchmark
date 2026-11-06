%------------------------------------------------------------------------------
% File     : KGC033+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use in at least one of PDF and PDF/A-1a against use in PDF/A-1a only: some use meets both
% Version  : Especial.
% English  : A German library permits use in at least one of PDF and PDF/A-1a.
%            A French library's policy commits to use in PDF/A-1a only. This
%            problem states that some use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag v1.2
% Source   : [Mus26]
% Names    : KGC322-1 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC322 is Compatible. Its two problems state that some use meets
%            the two policies (KGC033) and that no use does (KGC034); here the
%            first is Satisfiable and the second Unsatisfiable. A pair of
%            policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').

fof(w_kgc322, axiom,
    $true).
%------------------------------------------------------------------------------
