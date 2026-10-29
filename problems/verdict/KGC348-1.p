%--------------------------------------------------------------------------
% File     : KGC348-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : consent status, isA ValidForProcessing against eq ConsentWithdrawn, states declared distinct (witness condition asserted)
% Version  : 1.0
% English  : As KGC342, with the consent states declared distinct from one another.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC348-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-consent.ax').
include('axioms/DPV-consent-declared.ax').

% --- constants, groundings and resource hooks ----------------------------
% Declarations: declared distinctness instances, stated in
% the declarations file and instantiated here.

fof(bg_dist_dpv_consent_status_valid_for_processing_dpv_consent_withdrawn, axiom,
    dpv_consent_status_valid_for_processing != dpv_consent_withdrawn).

% --- witness condition asserted ------------------------------------------
fof(w_kgc348, axiom,
    ( ( kge_leq(dpv_consent_status_valid_for_processing, dpv_consent_status_valid_for_processing) & dpv_consent_status_valid_for_processing = dpv_consent_withdrawn )
| ( kge_leq(dpv_consent_withdrawn, dpv_consent_status_valid_for_processing) & dpv_consent_withdrawn = dpv_consent_withdrawn ) )).
%--------------------------------------------------------------------------
