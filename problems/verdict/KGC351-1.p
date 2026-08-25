%--------------------------------------------------------------------------
% File     : KGC351-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : legal basis, isAnyOf Article 6(1) against eq A6-1-a-explicit-consent (witness condition asserted)
% Version  : 1.0
% English  : The same offer against a processor naming explicit consent under Article 6(1)(a). That is a legal basis the Article provides, and the extension places it below the Article 6(1)(a) concept, below consent, below the legal-basis root. The enumeration does not reach it: isAnyOf compares by identity and explicit consent is not one of the seven names. The verdict is Unknown rather than Incompatible, because nothing published declares the two apart and a structure may interpret explicit consent and consent as one concept.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC351-1.p
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
fof(w_kgc351, axiom,
    ( ( lb_dpv_consent = lb_gdpr_a6_1_a_explicit_consent
| lb_dpv_contract = lb_gdpr_a6_1_a_explicit_consent
| lb_dpv_legal_obligation = lb_gdpr_a6_1_a_explicit_consent
| lb_dpv_vital_interest = lb_gdpr_a6_1_a_explicit_consent
| lb_dpv_public_interest = lb_gdpr_a6_1_a_explicit_consent
| lb_dpv_official_authority_of_controller = lb_gdpr_a6_1_a_explicit_consent
| lb_dpv_legitimate_interest = lb_gdpr_a6_1_a_explicit_consent
| lb_gdpr_a6_1_a_explicit_consent = lb_gdpr_a6_1_a_explicit_consent ) & ( ( lb_dpv_consent = lb_gdpr_a6_1_a_explicit_consent & ( lb_dpv_consent = lb_dpv_consent
| lb_dpv_consent = lb_dpv_contract
| lb_dpv_consent = lb_dpv_legal_obligation
| lb_dpv_consent = lb_dpv_vital_interest
| lb_dpv_consent = lb_dpv_public_interest
| lb_dpv_consent = lb_dpv_official_authority_of_controller
| lb_dpv_consent = lb_dpv_legitimate_interest ) )
| ( lb_dpv_contract = lb_gdpr_a6_1_a_explicit_consent & ( lb_dpv_contract = lb_dpv_consent
| lb_dpv_contract = lb_dpv_contract
| lb_dpv_contract = lb_dpv_legal_obligation
| lb_dpv_contract = lb_dpv_vital_interest
| lb_dpv_contract = lb_dpv_public_interest
| lb_dpv_contract = lb_dpv_official_authority_of_controller
| lb_dpv_contract = lb_dpv_legitimate_interest ) )
| ( lb_dpv_legal_obligation = lb_gdpr_a6_1_a_explicit_consent & ( lb_dpv_legal_obligation = lb_dpv_consent
| lb_dpv_legal_obligation = lb_dpv_contract
| lb_dpv_legal_obligation = lb_dpv_legal_obligation
| lb_dpv_legal_obligation = lb_dpv_vital_interest
| lb_dpv_legal_obligation = lb_dpv_public_interest
| lb_dpv_legal_obligation = lb_dpv_official_authority_of_controller
| lb_dpv_legal_obligation = lb_dpv_legitimate_interest ) )
| ( lb_dpv_vital_interest = lb_gdpr_a6_1_a_explicit_consent & ( lb_dpv_vital_interest = lb_dpv_consent
| lb_dpv_vital_interest = lb_dpv_contract
| lb_dpv_vital_interest = lb_dpv_legal_obligation
| lb_dpv_vital_interest = lb_dpv_vital_interest
| lb_dpv_vital_interest = lb_dpv_public_interest
| lb_dpv_vital_interest = lb_dpv_official_authority_of_controller
| lb_dpv_vital_interest = lb_dpv_legitimate_interest ) )
| ( lb_dpv_public_interest = lb_gdpr_a6_1_a_explicit_consent & ( lb_dpv_public_interest = lb_dpv_consent
| lb_dpv_public_interest = lb_dpv_contract
| lb_dpv_public_interest = lb_dpv_legal_obligation
| lb_dpv_public_interest = lb_dpv_vital_interest
| lb_dpv_public_interest = lb_dpv_public_interest
| lb_dpv_public_interest = lb_dpv_official_authority_of_controller
| lb_dpv_public_interest = lb_dpv_legitimate_interest ) )
| ( lb_dpv_official_authority_of_controller = lb_gdpr_a6_1_a_explicit_consent & ( lb_dpv_official_authority_of_controller = lb_dpv_consent
| lb_dpv_official_authority_of_controller = lb_dpv_contract
| lb_dpv_official_authority_of_controller = lb_dpv_legal_obligation
| lb_dpv_official_authority_of_controller = lb_dpv_vital_interest
| lb_dpv_official_authority_of_controller = lb_dpv_public_interest
| lb_dpv_official_authority_of_controller = lb_dpv_official_authority_of_controller
| lb_dpv_official_authority_of_controller = lb_dpv_legitimate_interest ) )
| ( lb_dpv_legitimate_interest = lb_gdpr_a6_1_a_explicit_consent & ( lb_dpv_legitimate_interest = lb_dpv_consent
| lb_dpv_legitimate_interest = lb_dpv_contract
| lb_dpv_legitimate_interest = lb_dpv_legal_obligation
| lb_dpv_legitimate_interest = lb_dpv_vital_interest
| lb_dpv_legitimate_interest = lb_dpv_public_interest
| lb_dpv_legitimate_interest = lb_dpv_official_authority_of_controller
| lb_dpv_legitimate_interest = lb_dpv_legitimate_interest ) )
| ( lb_gdpr_a6_1_a_explicit_consent = lb_gdpr_a6_1_a_explicit_consent & ( lb_gdpr_a6_1_a_explicit_consent = lb_dpv_consent
| lb_gdpr_a6_1_a_explicit_consent = lb_dpv_contract
| lb_gdpr_a6_1_a_explicit_consent = lb_dpv_legal_obligation
| lb_gdpr_a6_1_a_explicit_consent = lb_dpv_vital_interest
| lb_gdpr_a6_1_a_explicit_consent = lb_dpv_public_interest
| lb_gdpr_a6_1_a_explicit_consent = lb_dpv_official_authority_of_controller
| lb_gdpr_a6_1_a_explicit_consent = lb_dpv_legitimate_interest ) ) ) )).
%--------------------------------------------------------------------------
