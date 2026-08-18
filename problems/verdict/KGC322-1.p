%--------------------------------------------------------------------------
% File     : KGC322-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : fileFormat, isAnyOf {ft:PDF, ft:PDFA1A} against eq ft:PDFA1A (witness condition asserted)
% Version  : 1.0
% English  : Offer (fileFormat, isAnyOf, {ft:PDF, ft:PDFA1A}) against request (fileFormat, eq, ft:PDFA1A).  The offer admits either format and the request requires one of them, so the two are satisfiable together whatever the table says.  Compatible, and the refutation cites the witness alone: no resource assertion, no declaration, no order axiom.  isAnyOf asks only whether concepts are the same, which is why it is admissible at nom where isA is not.
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
