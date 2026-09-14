%--------------------------------------------------------------------------
% File     : KGC343-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : consent status, isA ValidForProcessing against eq ConsentWithdrawn, branches disjoint (witness condition negated)
% Version  : 1.0
% English  : As KGC342, with the valid and invalid branches declared disjoint on DPV's definitions.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC343-2.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-consent.ax').
include('axioms/DPV-consent-definitional.ax').

% --- constants, groundings and resource hooks ----------------------------
% Background theory: the branches declared disjoint, warranted
% by the module's definitions and asserted by it nowhere.

fof(bg_disj_dpv_consent_status_valid_for_processing_disjoint_dpv_consent_status_invalid_for_processing, axiom,
    ! [X] : ~ ( kge_leq(X, dpv_consent_status_valid_for_processing) & kge_leq(X, dpv_consent_status_invalid_for_processing) )).

% --- witness condition negated -------------------------------------------
fof(w_kgc343, axiom,
    ~ ( ( ( kge_leq(dpv_consent_status_valid_for_processing, dpv_consent_status_valid_for_processing) & dpv_consent_status_valid_for_processing = dpv_consent_withdrawn )
| ( kge_leq(dpv_consent_withdrawn, dpv_consent_status_valid_for_processing) & dpv_consent_withdrawn = dpv_consent_withdrawn ) ) )).
%--------------------------------------------------------------------------
