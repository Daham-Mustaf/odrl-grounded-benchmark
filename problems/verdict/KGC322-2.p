%--------------------------------------------------------------------------
% File     : KGC322-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : fileFormat, isAnyOf {ft:PDF, ft:PDFA1A} against eq ft:PDFA1A (witness condition negated)
% Version  : 1.0
% English  : A German library permits use in at least one of PDF and PDF/A-1a. A French library's policy commits to use in PDF/A-1a only.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC322-2.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/EUFT-filetype.ax').

% --- constants, groundings and resource hooks ----------------------------
% Resource: no order statements.
% Declarations: empty.  Neither is needed: the verdict follows from
% reflexivity of equality.

% --- witness condition negated -------------------------------------------
fof(w_kgc322, axiom,
    ~ ( ( ( ft_pdf = ft_pdfa1a
| ft_pdfa1a = ft_pdfa1a ) & ( ( ft_pdf = ft_pdfa1a & ( ft_pdf = ft_pdf
| ft_pdf = ft_pdfa1a ) )
| ( ft_pdfa1a = ft_pdfa1a & ( ft_pdfa1a = ft_pdf
| ft_pdfa1a = ft_pdfa1a ) ) ) ) )).
%--------------------------------------------------------------------------
