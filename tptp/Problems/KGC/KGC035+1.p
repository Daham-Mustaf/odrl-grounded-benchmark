%------------------------------------------------------------------------------
% File     : KGC035+1 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use in any format except PDF against use in PDF/A-1a only: some use meets both
% Version  : Especial.
% English  : A German library permits use in any format except PDF. A French
%            library's policy commits to use in PDF/A-1a only. The two formats
%            are declared distinct. This problem states that some use meets
%            the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag v1.2
% Source   : [Mus26]
% Names    : KGC323-1 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC323 is Compatible. Its two problems state that some use meets
%            the two policies (KGC035) and that no use does (KGC036); here the
%            first is Satisfiable and the second Unsatisfiable. A pair of
%            policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').

fof(bg_dist_ft_pdf_distinct_ft_pdfa1a, axiom,
    ft_pdf != ft_pdfa1a).

fof(w_kgc323, axiom,
    ft_pdfa1a != ft_pdf).
%------------------------------------------------------------------------------
