%------------------------------------------------------------------------------
% File     : KGC033+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use in PDF only against use in PDF/A-1a only: some use meets both
% Version  : Especial.
% English  : As KGC320, with the two formats declared distinct. This problem
%            states that some use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag
%            v1.1.1
% Source   : [Mus26]
% Names    : KGC321-1 [Mus26]

% Status   : Unsatisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC321 is Incompatible. Its two problems state that some use
%            meets the two policies (KGC033) and that no use does (KGC034). A
%            pair of policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent. Here the first is Unsatisfiable and the
%            second Satisfiable.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').

fof(bg_dist_ft_pdf_distinct_ft_pdfa1a, axiom,
    ft_pdf != ft_pdfa1a).

fof(w_kgc321, axiom,
    ft_pdf = ft_pdfa1a).
%------------------------------------------------------------------------------
