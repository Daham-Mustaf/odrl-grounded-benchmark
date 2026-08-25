%--------------------------------------------------------------------------
% File     : KGC350-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : legal basis, isAnyOf Article 6(1) against eq dpv:Consent (witness condition asserted)
% Version  : 1.0
% English  : The controller permits processing on any of the seven legal bases of Article 6(1), as the Regulatory Compliance Profile encodes them, and the processor names consent. The offer names the requested basis, so the verdict is Compatible and the certificate cites no assertion of the vocabulary: the constraints settle it between themselves.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC350-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-gdprlb.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition asserted ------------------------------------------
fof(w_kgc350, axiom,
    ( ( lb_dpv_consent = lb_dpv_consent
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
| lb_dpv_legitimate_interest = lb_dpv_legitimate_interest ) ) ) )).
%--------------------------------------------------------------------------
