%------------------------------------------------------------------------------
% File     : KGC002+2 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use for non-commercial purposes or any narrower purpose against use for scientific research only: no use meets both
% Version  : Especial.
%            Theorem formulation : The condition is written over the whole
%            vocabulary, as the paper's definition states; version 1 names
%            only the concepts a fixed value allows. The versions have the
%            same status.
% English  : A German library permits use for non-commercial purposes or any
%            narrower purpose. A French library's policy commits to use for
%            scientific research only. This problem states that no use meets
%            the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag v1.2
% Source   : [Mus26]
% Names    : KGC301-2 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC301 is Unknown. Its two problems state that some use meets the
%            two policies (KGC001) and that no use does (KGC002); here the
%            first is Satisfiable and the second Satisfiable. A pair of
%            policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+3.ax').

fof(w_kgc301, axiom,
    ~ ( ( ( ( kge_leq(dpv_non_commercial_purpose, dpv_non_commercial_purpose) & dpv_non_commercial_purpose = dpv_scientific_research )
    | kge_leq(dpv_scientific_research, dpv_non_commercial_purpose)
    | ( kge_leq(dpv_academic_research, dpv_non_commercial_purpose) & dpv_academic_research = dpv_scientific_research )
    | ( kge_leq(dpv_account_management, dpv_non_commercial_purpose) & dpv_account_management = dpv_scientific_research )
    | ( kge_leq(dpv_advertising, dpv_non_commercial_purpose) & dpv_advertising = dpv_scientific_research )
    | ( kge_leq(dpv_age_verification, dpv_non_commercial_purpose) & dpv_age_verification = dpv_scientific_research )
    | ( kge_leq(dpv_combat_climate_change, dpv_non_commercial_purpose) & dpv_combat_climate_change = dpv_scientific_research )
    | ( kge_leq(dpv_commercial_purpose, dpv_non_commercial_purpose) & dpv_commercial_purpose = dpv_scientific_research )
    | ( kge_leq(dpv_commercial_research, dpv_non_commercial_purpose) & dpv_commercial_research = dpv_scientific_research )
    | ( kge_leq(dpv_communication_for_customer_care, dpv_non_commercial_purpose) & dpv_communication_for_customer_care = dpv_scientific_research )
    | ( kge_leq(dpv_communication_management, dpv_non_commercial_purpose) & dpv_communication_management = dpv_scientific_research )
    | ( kge_leq(dpv_counter_money_laundering, dpv_non_commercial_purpose) & dpv_counter_money_laundering = dpv_scientific_research )
    | ( kge_leq(dpv_counterterrorism, dpv_non_commercial_purpose) & dpv_counterterrorism = dpv_scientific_research )
    | ( kge_leq(dpv_customer_care, dpv_non_commercial_purpose) & dpv_customer_care = dpv_scientific_research )
    | ( kge_leq(dpv_customer_claims_management, dpv_non_commercial_purpose) & dpv_customer_claims_management = dpv_scientific_research )
    | ( kge_leq(dpv_customer_management, dpv_non_commercial_purpose) & dpv_customer_management = dpv_scientific_research )
    | ( kge_leq(dpv_customer_order_management, dpv_non_commercial_purpose) & dpv_customer_order_management = dpv_scientific_research )
    | ( kge_leq(dpv_customer_relationship_management, dpv_non_commercial_purpose) & dpv_customer_relationship_management = dpv_scientific_research )
    | ( kge_leq(dpv_customer_solvency_monitoring, dpv_non_commercial_purpose) & dpv_customer_solvency_monitoring = dpv_scientific_research )
    | ( kge_leq(dpv_data_altruism, dpv_non_commercial_purpose) & dpv_data_altruism = dpv_scientific_research )
    | ( kge_leq(dpv_delivery_of_goods, dpv_non_commercial_purpose) & dpv_delivery_of_goods = dpv_scientific_research )
    | ( kge_leq(dpv_direct_marketing, dpv_non_commercial_purpose) & dpv_direct_marketing = dpv_scientific_research )
    | ( kge_leq(dpv_dispute_management, dpv_non_commercial_purpose) & dpv_dispute_management = dpv_scientific_research )
    | ( kge_leq(dpv_enforce_access_control, dpv_non_commercial_purpose) & dpv_enforce_access_control = dpv_scientific_research )
    | ( kge_leq(dpv_enforce_security, dpv_non_commercial_purpose) & dpv_enforce_security = dpv_scientific_research )
    | ( kge_leq(dpv_establish_contractual_agreement, dpv_non_commercial_purpose) & dpv_establish_contractual_agreement = dpv_scientific_research )
    | ( kge_leq(dpv_fraud_prevention_and_detection, dpv_non_commercial_purpose) & dpv_fraud_prevention_and_detection = dpv_scientific_research )
    | ( kge_leq(dpv_fulfilment_of_contractual_obligation, dpv_non_commercial_purpose) & dpv_fulfilment_of_contractual_obligation = dpv_scientific_research )
    | ( kge_leq(dpv_fulfilment_of_obligation, dpv_non_commercial_purpose) & dpv_fulfilment_of_obligation = dpv_scientific_research )
    | ( kge_leq(dpv_human_resource_management, dpv_non_commercial_purpose) & dpv_human_resource_management = dpv_scientific_research )
    | ( kge_leq(dpv_identity_authentication, dpv_non_commercial_purpose) & dpv_identity_authentication = dpv_scientific_research )
    | ( kge_leq(dpv_identity_verification, dpv_non_commercial_purpose) & dpv_identity_verification = dpv_scientific_research )
    | ( kge_leq(dpv_improve_existing_products_and_services, dpv_non_commercial_purpose) & dpv_improve_existing_products_and_services = dpv_scientific_research )
    | ( kge_leq(dpv_improve_healthcare, dpv_non_commercial_purpose) & dpv_improve_healthcare = dpv_scientific_research )
    | ( kge_leq(dpv_improve_internal_crm_processes, dpv_non_commercial_purpose) & dpv_improve_internal_crm_processes = dpv_scientific_research )
    | ( kge_leq(dpv_improve_public_services, dpv_non_commercial_purpose) & dpv_improve_public_services = dpv_scientific_research )
    | ( kge_leq(dpv_improve_transport_mobility, dpv_non_commercial_purpose) & dpv_improve_transport_mobility = dpv_scientific_research )
    | ( kge_leq(dpv_increase_service_robustness, dpv_non_commercial_purpose) & dpv_increase_service_robustness = dpv_scientific_research )
    | ( kge_leq(dpv_internal_resource_optimisation, dpv_non_commercial_purpose) & dpv_internal_resource_optimisation = dpv_scientific_research )
    | ( kge_leq(dpv_legal_compliance, dpv_non_commercial_purpose) & dpv_legal_compliance = dpv_scientific_research )
    | ( kge_leq(dpv_maintain_fraud_database, dpv_non_commercial_purpose) & dpv_maintain_fraud_database = dpv_scientific_research )
    | ( kge_leq(dpv_marketing, dpv_non_commercial_purpose) & dpv_marketing = dpv_scientific_research )
    | ( kge_leq(dpv_member_partner_management, dpv_non_commercial_purpose) & dpv_member_partner_management = dpv_scientific_research )
    | ( kge_leq(dpv_misuse_prevention_and_detection, dpv_non_commercial_purpose) & dpv_misuse_prevention_and_detection = dpv_scientific_research )
    | ( kge_leq(dpv_non_commercial_research, dpv_non_commercial_purpose) & dpv_non_commercial_research = dpv_scientific_research )
    | ( kge_leq(dpv_optimisation_for_consumer, dpv_non_commercial_purpose) & dpv_optimisation_for_consumer = dpv_scientific_research )
    | ( kge_leq(dpv_optimisation_for_controller, dpv_non_commercial_purpose) & dpv_optimisation_for_controller = dpv_scientific_research )
    | ( kge_leq(dpv_optimise_user_interface, dpv_non_commercial_purpose) & dpv_optimise_user_interface = dpv_scientific_research )
    | ( kge_leq(dpv_organisation_compliance_management, dpv_non_commercial_purpose) & dpv_organisation_compliance_management = dpv_scientific_research )
    | ( kge_leq(dpv_organisation_governance, dpv_non_commercial_purpose) & dpv_organisation_governance = dpv_scientific_research )
    | ( kge_leq(dpv_organisation_risk_management, dpv_non_commercial_purpose) & dpv_organisation_risk_management = dpv_scientific_research )
    | ( kge_leq(dpv_payment_management, dpv_non_commercial_purpose) & dpv_payment_management = dpv_scientific_research )
    | ( kge_leq(dpv_personalisation, dpv_non_commercial_purpose) & dpv_personalisation = dpv_scientific_research )
    | ( kge_leq(dpv_personalised_advertising, dpv_non_commercial_purpose) & dpv_personalised_advertising = dpv_scientific_research )
    | ( kge_leq(dpv_personalised_benefits, dpv_non_commercial_purpose) & dpv_personalised_benefits = dpv_scientific_research )
    | ( kge_leq(dpv_personnel_behaviour_monitoring, dpv_non_commercial_purpose) & dpv_personnel_behaviour_monitoring = dpv_scientific_research )
    | ( kge_leq(dpv_personnel_hiring, dpv_non_commercial_purpose) & dpv_personnel_hiring = dpv_scientific_research )
    | ( kge_leq(dpv_personnel_management, dpv_non_commercial_purpose) & dpv_personnel_management = dpv_scientific_research )
    | ( kge_leq(dpv_personnel_monitoring, dpv_non_commercial_purpose) & dpv_personnel_monitoring = dpv_scientific_research )
    | ( kge_leq(dpv_personnel_offboarding, dpv_non_commercial_purpose) & dpv_personnel_offboarding = dpv_scientific_research )
    | ( kge_leq(dpv_personnel_onboarding, dpv_non_commercial_purpose) & dpv_personnel_onboarding = dpv_scientific_research )
    | ( kge_leq(dpv_personnel_payment, dpv_non_commercial_purpose) & dpv_personnel_payment = dpv_scientific_research )
    | ( kge_leq(dpv_personnel_performance_evaluation, dpv_non_commercial_purpose) & dpv_personnel_performance_evaluation = dpv_scientific_research )
    | ( kge_leq(dpv_personnel_performance_management, dpv_non_commercial_purpose) & dpv_personnel_performance_management = dpv_scientific_research ) )
    | ( ( kge_leq(dpv_personnel_performance_monitoring, dpv_non_commercial_purpose) & dpv_personnel_performance_monitoring = dpv_scientific_research )
    | ( kge_leq(dpv_personnel_performance_prediction, dpv_non_commercial_purpose) & dpv_personnel_performance_prediction = dpv_scientific_research )
    | ( kge_leq(dpv_personnel_promotion_management, dpv_non_commercial_purpose) & dpv_personnel_promotion_management = dpv_scientific_research )
    | ( kge_leq(dpv_personnel_termination_management, dpv_non_commercial_purpose) & dpv_personnel_termination_management = dpv_scientific_research )
    | ( kge_leq(dpv_personnel_workload_management, dpv_non_commercial_purpose) & dpv_personnel_workload_management = dpv_scientific_research )
    | ( kge_leq(dpv_political_campaign, dpv_non_commercial_purpose) & dpv_political_campaign = dpv_scientific_research )
    | ( kge_leq(dpv_protection_of_ipr, dpv_non_commercial_purpose) & dpv_protection_of_ipr = dpv_scientific_research )
    | ( kge_leq(dpv_protection_of_national_security, dpv_non_commercial_purpose) & dpv_protection_of_national_security = dpv_scientific_research )
    | ( kge_leq(dpv_protection_of_public_security, dpv_non_commercial_purpose) & dpv_protection_of_public_security = dpv_scientific_research )
    | ( kge_leq(dpv_provide_event_recommendations, dpv_non_commercial_purpose) & dpv_provide_event_recommendations = dpv_scientific_research )
    | ( kge_leq(dpv_provide_official_statistics, dpv_non_commercial_purpose) & dpv_provide_official_statistics = dpv_scientific_research )
    | ( kge_leq(dpv_provide_personalised_recommendations, dpv_non_commercial_purpose) & dpv_provide_personalised_recommendations = dpv_scientific_research )
    | ( kge_leq(dpv_provide_product_recommendations, dpv_non_commercial_purpose) & dpv_provide_product_recommendations = dpv_scientific_research )
    | ( kge_leq(dpv_public_benefit, dpv_non_commercial_purpose) & dpv_public_benefit = dpv_scientific_research )
    | ( kge_leq(dpv_public_policy_making, dpv_non_commercial_purpose) & dpv_public_policy_making = dpv_scientific_research )
    | ( kge_leq(dpv_public_relations, dpv_non_commercial_purpose) & dpv_public_relations = dpv_scientific_research )
    | ( kge_leq(dpv_purpose, dpv_non_commercial_purpose) & dpv_purpose = dpv_scientific_research )
    | ( kge_leq(dpv_record_management, dpv_non_commercial_purpose) & dpv_record_management = dpv_scientific_research )
    | ( kge_leq(dpv_recruitment_advertising, dpv_non_commercial_purpose) & dpv_recruitment_advertising = dpv_scientific_research )
    | ( kge_leq(dpv_recruitment_applicant_background_check, dpv_non_commercial_purpose) & dpv_recruitment_applicant_background_check = dpv_scientific_research )
    | ( kge_leq(dpv_recruitment_applicant_criminal_background_check, dpv_non_commercial_purpose) & dpv_recruitment_applicant_criminal_background_check = dpv_scientific_research )
    | ( kge_leq(dpv_recruitment_applicant_information_authentication, dpv_non_commercial_purpose) & dpv_recruitment_applicant_information_authentication = dpv_scientific_research )
    | ( kge_leq(dpv_recruitment_applicant_selection, dpv_non_commercial_purpose) & dpv_recruitment_applicant_selection = dpv_scientific_research )
    | ( kge_leq(dpv_recruitment_application_analysis, dpv_non_commercial_purpose) & dpv_recruitment_application_analysis = dpv_scientific_research )
    | ( kge_leq(dpv_recruitment_application_management, dpv_non_commercial_purpose) & dpv_recruitment_application_management = dpv_scientific_research )
    | ( kge_leq(dpv_recruitment_application_screening, dpv_non_commercial_purpose) & dpv_recruitment_application_screening = dpv_scientific_research )
    | ( kge_leq(dpv_recruitment_interview_analysis, dpv_non_commercial_purpose) & dpv_recruitment_interview_analysis = dpv_scientific_research )
    | ( kge_leq(dpv_recruitment_interview_assessment, dpv_non_commercial_purpose) & dpv_recruitment_interview_assessment = dpv_scientific_research )
    | ( kge_leq(dpv_recruitment_interview_management, dpv_non_commercial_purpose) & dpv_recruitment_interview_management = dpv_scientific_research )
    | ( kge_leq(dpv_recruitment_interview_scheduling, dpv_non_commercial_purpose) & dpv_recruitment_interview_scheduling = dpv_scientific_research )
    | ( kge_leq(dpv_recruitment_management, dpv_non_commercial_purpose) & dpv_recruitment_management = dpv_scientific_research )
    | ( kge_leq(dpv_recruitment_targeted_advertising, dpv_non_commercial_purpose) & dpv_recruitment_targeted_advertising = dpv_scientific_research )
    | ( kge_leq(dpv_repair_impairments, dpv_non_commercial_purpose) & dpv_repair_impairments = dpv_scientific_research )
    | ( kge_leq(dpv_requested_service_provision, dpv_non_commercial_purpose) & dpv_requested_service_provision = dpv_scientific_research )
    | ( kge_leq(dpv_research_and_development, dpv_non_commercial_purpose) & dpv_research_and_development = dpv_scientific_research )
    | ( kge_leq(dpv_rights_fulfilment, dpv_non_commercial_purpose) & dpv_rights_fulfilment = dpv_scientific_research )
    | ( kge_leq(dpv_search_functionalities, dpv_non_commercial_purpose) & dpv_search_functionalities = dpv_scientific_research )
    | ( kge_leq(dpv_sell_data_to_third_parties, dpv_non_commercial_purpose) & dpv_sell_data_to_third_parties = dpv_scientific_research )
    | ( kge_leq(dpv_sell_insights_from_data, dpv_non_commercial_purpose) & dpv_sell_insights_from_data = dpv_scientific_research )
    | ( kge_leq(dpv_sell_products, dpv_non_commercial_purpose) & dpv_sell_products = dpv_scientific_research )
    | ( kge_leq(dpv_sell_products_to_data_subject, dpv_non_commercial_purpose) & dpv_sell_products_to_data_subject = dpv_scientific_research )
    | ( kge_leq(dpv_service_access_determination, dpv_non_commercial_purpose) & dpv_service_access_determination = dpv_scientific_research )
    | ( kge_leq(dpv_service_management, dpv_non_commercial_purpose) & dpv_service_management = dpv_scientific_research )
    | ( kge_leq(dpv_service_monitoring, dpv_non_commercial_purpose) & dpv_service_monitoring = dpv_scientific_research )
    | ( kge_leq(dpv_service_optimisation, dpv_non_commercial_purpose) & dpv_service_optimisation = dpv_scientific_research )
    | ( kge_leq(dpv_service_personalisation, dpv_non_commercial_purpose) & dpv_service_personalisation = dpv_scientific_research )
    | ( kge_leq(dpv_service_provision, dpv_non_commercial_purpose) & dpv_service_provision = dpv_scientific_research )
    | ( kge_leq(dpv_service_registration, dpv_non_commercial_purpose) & dpv_service_registration = dpv_scientific_research )
    | ( kge_leq(dpv_service_usage_analytics, dpv_non_commercial_purpose) & dpv_service_usage_analytics = dpv_scientific_research )
    | ( kge_leq(dpv_social_media_marketing, dpv_non_commercial_purpose) & dpv_social_media_marketing = dpv_scientific_research )
    | ( kge_leq(dpv_targeted_advertising, dpv_non_commercial_purpose) & dpv_targeted_advertising = dpv_scientific_research )
    | ( kge_leq(dpv_technical_service_provision, dpv_non_commercial_purpose) & dpv_technical_service_provision = dpv_scientific_research )
    | ( kge_leq(dpv_user_interface_personalisation, dpv_non_commercial_purpose) & dpv_user_interface_personalisation = dpv_scientific_research )
    | ( kge_leq(dpv_vendor_management, dpv_non_commercial_purpose) & dpv_vendor_management = dpv_scientific_research )
    | ( kge_leq(dpv_vendor_payment, dpv_non_commercial_purpose) & dpv_vendor_payment = dpv_scientific_research )
    | ( kge_leq(dpv_vendor_records_management, dpv_non_commercial_purpose) & dpv_vendor_records_management = dpv_scientific_research )
    | ( kge_leq(dpv_vendor_selection_assessment, dpv_non_commercial_purpose) & dpv_vendor_selection_assessment = dpv_scientific_research )
    | ( kge_leq(dpv_verification, dpv_non_commercial_purpose) & dpv_verification = dpv_scientific_research ) ) ) )).
%------------------------------------------------------------------------------
