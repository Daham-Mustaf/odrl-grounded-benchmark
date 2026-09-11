%--------------------------------------------------------------------------
% File     : KGC320-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : fileFormat, eq ft:PDF against eq ft:PDFA1A (witness condition negated)
% Version  : 1.0
% English  : A library permits PDF, while a researcher requests PDF/A-1a.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC320-2.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/EUFT-filetype.ax').

% --- constants, groundings and resource hooks ----------------------------
% Resource: no order assertions.  The table publishes none.
% Background theory: empty.  The table separates nothing either.

% --- witness condition negated -------------------------------------------
fof(w_kgc320, axiom,
    ~ ( ( ( ft_pdf = ft_pdf & ft_pdf = ft_pdfa1a )
| ( ft_pdfa1a = ft_pdf & ft_pdfa1a = ft_pdfa1a ) ) )).
%--------------------------------------------------------------------------
