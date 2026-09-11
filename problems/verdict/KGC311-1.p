%--------------------------------------------------------------------------
% File     : KGC311-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : purpose, isA dpv:Purpose against eq dpv:NCR (witness condition asserted)
% Version  : 1.0
% English  : A library permits use for any DPV purpose, and a researcher requests use for non-commercial research.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC311-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-dpv-purposes.ax').

% --- constants, groundings and resource hooks ----------------------------
% Background theory: empty, as above.

% --- witness condition asserted ------------------------------------------
fof(w_kgc311, axiom,
    ( ( kge_leq(dpv_purpose, dpv_purpose) & dpv_purpose = dpv_non_commercial_research )
| ( kge_leq(dpv_non_commercial_research, dpv_purpose) & dpv_non_commercial_research = dpv_non_commercial_research ) )).
%--------------------------------------------------------------------------
