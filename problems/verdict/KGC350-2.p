%--------------------------------------------------------------------------
% File     : KGC350-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : legal basis, isAnyOf Article 6(1) against eq dpv:Consent (witness condition negated)
% Version  : 1.0
% English  : A controller permits processing under any of the seven Article 6(1) legal bases, and a processor requests processing on the basis of consent.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC350-2.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-gdprlb.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition negated -------------------------------------------
fof(w_kgc350, axiom,
    ~ ( ( ( lb_dpv_consent = lb_dpv_consent
| lb_dpv_contract = lb_dpv_consent
| lb_dpv_legal_obligation = lb_dpv_consent
| lb_dpv_vital_interest = lb_dpv_consent
| lb_dpv_public_interest = lb_dpv_consent
| lb_dpv_official_authority_of_controller = lb_dpv_consent
| lb_dpv_legitimate_interest = lb_dpv_consent ) & ( ( lb_dpv_consent = lb_dpv_consent & ( lb_dpv_consent = lb_dpv_consent
| lb_dpv_consent = lb_dpv_contract
| lb_dpv_consent = lb_dpv_legal_obligation
| lb_dpv_consent = lb_dpv_vital_interest
| lb_dpv_consent = lb_dpv_public_interest
| lb_dpv_consent = lb_dpv_official_authority_of_controller
| lb_dpv_consent = lb_dpv_legitimate_interest ) )
| ( lb_dpv_contract = lb_dpv_consent & ( lb_dpv_contract = lb_dpv_consent
| lb_dpv_contract = lb_dpv_contract
| lb_dpv_contract = lb_dpv_legal_obligation
| lb_dpv_contract = lb_dpv_vital_interest
| lb_dpv_contract = lb_dpv_public_interest
| lb_dpv_contract = lb_dpv_official_authority_of_controller
| lb_dpv_contract = lb_dpv_legitimate_interest ) )
| ( lb_dpv_legal_obligation = lb_dpv_consent & ( lb_dpv_legal_obligation = lb_dpv_consent
| lb_dpv_legal_obligation = lb_dpv_contract
| lb_dpv_legal_obligation = lb_dpv_legal_obligation
| lb_dpv_legal_obligation = lb_dpv_vital_interest
| lb_dpv_legal_obligation = lb_dpv_public_interest
| lb_dpv_legal_obligation = lb_dpv_official_authority_of_controller
| lb_dpv_legal_obligation = lb_dpv_legitimate_interest ) )
| ( lb_dpv_vital_interest = lb_dpv_consent & ( lb_dpv_vital_interest = lb_dpv_consent
| lb_dpv_vital_interest = lb_dpv_contract
| lb_dpv_vital_interest = lb_dpv_legal_obligation
| lb_dpv_vital_interest = lb_dpv_vital_interest
| lb_dpv_vital_interest = lb_dpv_public_interest
| lb_dpv_vital_interest = lb_dpv_official_authority_of_controller
| lb_dpv_vital_interest = lb_dpv_legitimate_interest ) )
| ( lb_dpv_public_interest = lb_dpv_consent & ( lb_dpv_public_interest = lb_dpv_consent
| lb_dpv_public_interest = lb_dpv_contract
| lb_dpv_public_interest = lb_dpv_legal_obligation
| lb_dpv_public_interest = lb_dpv_vital_interest
| lb_dpv_public_interest = lb_dpv_public_interest
| lb_dpv_public_interest = lb_dpv_official_authority_of_controller
| lb_dpv_public_interest = lb_dpv_legitimate_interest ) )
| ( lb_dpv_official_authority_of_controller = lb_dpv_consent & ( lb_dpv_official_authority_of_controller = lb_dpv_consent
| lb_dpv_official_authority_of_controller = lb_dpv_contract
| lb_dpv_official_authority_of_controller = lb_dpv_legal_obligation
| lb_dpv_official_authority_of_controller = lb_dpv_vital_interest
| lb_dpv_official_authority_of_controller = lb_dpv_public_interest
| lb_dpv_official_authority_of_controller = lb_dpv_official_authority_of_controller
| lb_dpv_official_authority_of_controller = lb_dpv_legitimate_interest ) )
| ( lb_dpv_legitimate_interest = lb_dpv_consent & ( lb_dpv_legitimate_interest = lb_dpv_consent
| lb_dpv_legitimate_interest = lb_dpv_contract
| lb_dpv_legitimate_interest = lb_dpv_legal_obligation
| lb_dpv_legitimate_interest = lb_dpv_vital_interest
| lb_dpv_legitimate_interest = lb_dpv_public_interest
| lb_dpv_legitimate_interest = lb_dpv_official_authority_of_controller
| lb_dpv_legitimate_interest = lb_dpv_legitimate_interest ) ) ) ) )).
%--------------------------------------------------------------------------
