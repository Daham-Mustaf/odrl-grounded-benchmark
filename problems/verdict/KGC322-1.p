%--------------------------------------------------------------------------
% File     : KGC322-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : fileFormat, isAnyOf {ft:PDF, ft:PDFA1A} against eq ft:PDFA1A (witness condition asserted)
% Version  : 1.0
% English  : A library permits either PDF or PDF/A-1a, while a researcher requests PDF/A-1a.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC322-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/EUFT-filetype.ax').

% --- constants, groundings and resource hooks ----------------------------
% Resource: no order assertions.
% Background theory: empty.  Neither is needed: the verdict follows from
% reflexivity of equality.

% --- witness condition asserted ------------------------------------------
fof(w_kgc322, axiom,
    ( ( ( ft_pdf = ft_pdf | ft_pdf = ft_pdfa1a ) & ft_pdf = ft_pdfa1a )
| ( ( ft_pdfa1a = ft_pdf | ft_pdfa1a = ft_pdfa1a ) & ft_pdfa1a = ft_pdfa1a ) )).
%--------------------------------------------------------------------------
