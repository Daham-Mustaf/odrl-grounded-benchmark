%--------------------------------------------------------------------------
% File     : KGC315-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : purpose, isA dpv:Purpose against eq dpv:RIS (witness condition asserted)
% Version  : 1.0
% English  : A library permits use for any DPV purpose, and a researcher requests use for recruitment interview scheduling.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC315-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-dpv-purposes.ax').

% --- constants, groundings and resource hooks ----------------------------
% Background theory: empty.

% --- witness condition asserted ------------------------------------------
fof(w_kgc315, axiom,
    ( ( kge_leq(dpv_purpose, dpv_purpose) & dpv_purpose = dpv_recruitment_interview_scheduling )
| ( kge_leq(dpv_recruitment_interview_scheduling, dpv_purpose) & dpv_recruitment_interview_scheduling = dpv_recruitment_interview_scheduling ) )).
%--------------------------------------------------------------------------
