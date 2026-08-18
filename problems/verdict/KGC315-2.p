%--------------------------------------------------------------------------
% File     : KGC315-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : purpose, isA dpv:Purpose against eq dpv:RIS (witness condition negated)
% Version  : 1.0
% English  : Offer (purpose, isA, dpv:Purpose) against request (purpose, eq, dpv:RecruitmentInterviewScheduling), the deepest concept in the module.  The resource relates them only through six steps, so the refutation must chain all six.  Compatible.  The verdict is the same as KGC310's; what grows with the depth is the certificate, not the answer.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC315-2.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-milestone.ax').

% --- constants, groundings and resource hooks ----------------------------
% Background theory: empty.

% --- witness condition negated -------------------------------------------
fof(w_kgc315, axiom,
    ~ ( ( ( kge_leq(dpv_purpose, dpv_purpose) & dpv_purpose = dpv_recruitment_interview_scheduling )
| ( kge_leq(dpv_recruitment_interview_scheduling, dpv_purpose) & dpv_recruitment_interview_scheduling = dpv_recruitment_interview_scheduling ) ) )).
%--------------------------------------------------------------------------
