%--------------------------------------------------------------------------
% File     : KGC320-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : fileFormat, eq ft:PDF against eq ft:PDFA1A (witness condition asserted)
% Version  : 1.0
% English  : Offer (fileFormat, eq, ft:PDF) against request (fileFormat, eq, ft:PDFA1A).  The authority lists both formats and relates them in no way, so nothing settles whether the two names denote one format: Unknown.  A PDF/A-1a file is a PDF, and the table does not say so; nor could the fragment read it if the table did, since conformance to a profile of a standard is not identity, subsumption or parthood.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC320-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/EUFT-filetype.ax').

% --- constants, groundings and resource hooks ----------------------------
% Resource: no order assertions.  The table publishes none.
% Background theory: empty.  The table separates nothing either.

% --- witness condition asserted ------------------------------------------
fof(w_kgc320, axiom,
    ( ( ft_pdf = ft_pdf & ft_pdf = ft_pdfa1a )
| ( ft_pdfa1a = ft_pdf & ft_pdfa1a = ft_pdfa1a ) )).
%--------------------------------------------------------------------------
