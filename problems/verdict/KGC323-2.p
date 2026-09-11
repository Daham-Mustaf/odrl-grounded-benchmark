%--------------------------------------------------------------------------
% File     : KGC323-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : fileFormat, neq ft:PDF against eq ft:PDFA1A, under a declared distinctness (witness condition negated)
% Version  : 1.0
% English  : A library excludes PDF, while a researcher requests PDF/A-1a, with the two formats declared distinct.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC323-2.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/EUFT-filetype.ax').
include('axioms/EUFT-filetype-declared.ax').

% --- constants, groundings and resource hooks ----------------------------
% Resource: no order assertions.
% Background theory: ft:PDF and ft:PDFA1A are declared distinct.

% --- witness condition negated -------------------------------------------
fof(w_kgc323, axiom,
    ~ ( ( ( ft_pdf != ft_pdf & ft_pdf = ft_pdfa1a )
| ( ft_pdfa1a != ft_pdf & ft_pdfa1a = ft_pdfa1a ) ) )).
%--------------------------------------------------------------------------
