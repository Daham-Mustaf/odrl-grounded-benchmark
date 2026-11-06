%------------------------------------------------------------------------------
% File     : KGC019+2 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use for any DPV purpose against use for delivery of goods only: some use meets both
% Version  : Especial.
%            Theorem formulation : The condition is written over the whole
%            vocabulary, as the paper's definition states; version 1 names
%            only the concepts a fixed value allows. The versions have the
%            same status.
% English  : A city's traffic data platform permits use for any DPV purpose. A
%            logistics company commits to use for delivery of goods. This
%            problem states that some use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag v1.2
% Source   : [Mus26]
% Names    : KGC315-1 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC315 is Compatible. Its two problems state that some use meets
%            the two policies (KGC019) and that no use does (KGC020); here the
%            first is Satisfiable and the second Unsatisfiable. A pair of
%            policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+3.ax').

fof(w_kgc315, axiom,
    ( ( ( kge_leq(dpv_purpose, dpv_purpose) & dpv_purpose = dpv_delivery_of_goods )
    | kge_leq(dpv_delivery_of_goods, dpv_purpose)
    | ( kge_leq(dpv_academic_research, dpv_purpose) & dpv_academic_research = dpv_delivery_of_goods )
    | ( kge_leq(dpv_account_management, dpv_purpose) & dpv_account_management = dpv_delivery_of_goods )
    | ( kge_leq(dpv_advertising, dpv_purpose) & dpv_advertising = dpv_delivery_of_goods )
    | ( kge_leq(dpv_age_verification, dpv_purpose) & dpv_age_verification = dpv_delivery_of_goods )
    | ( kge_leq(dpv_combat_climate_change, dpv_purpose) & dpv_combat_climate_change = dpv_delivery_of_goods )
    | ( kge_leq(dpv_commercial_purpose, dpv_purpose) & dpv_commercial_purpose = dpv_delivery_of_goods )
    | ( kge_leq(dpv_commercial_research, dpv_purpose) & dpv_commercial_research = dpv_delivery_of_goods )
    | ( kge_leq(dpv_communication_for_customer_care, dpv_purpose) & dpv_communication_for_customer_care = dpv_delivery_of_goods )
    | ( kge_leq(dpv_communication_management, dpv_purpose) & dpv_communication_management = dpv_delivery_of_goods )
    | ( kge_leq(dpv_counter_money_laundering, dpv_purpose) & dpv_counter_money_laundering = dpv_delivery_of_goods )
    | ( kge_leq(dpv_counterterrorism, dpv_purpose) & dpv_counterterrorism = dpv_delivery_of_goods )
    | ( kge_leq(dpv_customer_care, dpv_purpose) & dpv_customer_care = dpv_delivery_of_goods )
    | ( kge_leq(dpv_customer_claims_management, dpv_purpose) & dpv_customer_claims_management = dpv_delivery_of_goods )
    | ( kge_leq(dpv_customer_management, dpv_purpose) & dpv_customer_management = dpv_delivery_of_goods )
    | ( kge_leq(dpv_customer_order_management, dpv_purpose) & dpv_customer_order_management = dpv_delivery_of_goods )
    | ( kge_leq(dpv_customer_relationship_management, dpv_purpose) & dpv_customer_relationship_management = dpv_delivery_of_goods )
    | ( kge_leq(dpv_customer_solvency_monitoring, dpv_purpose) & dpv_customer_solvency_monitoring = dpv_delivery_of_goods )
    | ( kge_leq(dpv_data_altruism, dpv_purpose) & dpv_data_altruism = dpv_delivery_of_goods )
    | ( kge_leq(dpv_direct_marketing, dpv_purpose) & dpv_direct_marketing = dpv_delivery_of_goods )
    | ( kge_leq(dpv_dispute_management, dpv_purpose) & dpv_dispute_management = dpv_delivery_of_goods )
    | ( kge_leq(dpv_enforce_access_control, dpv_purpose) & dpv_enforce_access_control = dpv_delivery_of_goods )
    | ( kge_leq(dpv_enforce_security, dpv_purpose) & dpv_enforce_security = dpv_delivery_of_goods )
    | ( kge_leq(dpv_establish_contractual_agreement, dpv_purpose) & dpv_establish_contractual_agreement = dpv_delivery_of_goods )
    | ( kge_leq(dpv_fraud_prevention_and_detection, dpv_purpose) & dpv_fraud_prevention_and_detection = dpv_delivery_of_goods )
    | ( kge_leq(dpv_fulfilment_of_contractual_obligation, dpv_purpose) & dpv_fulfilment_of_contractual_obligation = dpv_delivery_of_goods )
    | ( kge_leq(dpv_fulfilment_of_obligation, dpv_purpose) & dpv_fulfilment_of_obligation = dpv_delivery_of_goods )
    | ( kge_leq(dpv_human_resource_management, dpv_purpose) & dpv_human_resource_management = dpv_delivery_of_goods )
    | ( kge_leq(dpv_identity_authentication, dpv_purpose) & dpv_identity_authentication = dpv_delivery_of_goods )
    | ( kge_leq(dpv_identity_verification, dpv_purpose) & dpv_identity_verification = dpv_delivery_of_goods )
    | ( kge_leq(dpv_improve_existing_products_and_services, dpv_purpose) & dpv_improve_existing_products_and_services = dpv_delivery_of_goods )
    | ( kge_leq(dpv_improve_healthcare, dpv_purpose) & dpv_improve_healthcare = dpv_delivery_of_goods )
    | ( kge_leq(dpv_improve_internal_crm_processes, dpv_purpose) & dpv_improve_internal_crm_processes = dpv_delivery_of_goods )
    | ( kge_leq(dpv_improve_public_services, dpv_purpose) & dpv_improve_public_services = dpv_delivery_of_goods )
    | ( kge_leq(dpv_improve_transport_mobility, dpv_purpose) & dpv_improve_transport_mobility = dpv_delivery_of_goods )
    | ( kge_leq(dpv_increase_service_robustness, dpv_purpose) & dpv_increase_service_robustness = dpv_delivery_of_goods )
    | ( kge_leq(dpv_internal_resource_optimisation, dpv_purpose) & dpv_internal_resource_optimisation = dpv_delivery_of_goods )
    | ( kge_leq(dpv_legal_compliance, dpv_purpose) & dpv_legal_compliance = dpv_delivery_of_goods )
    | ( kge_leq(dpv_maintain_fraud_database, dpv_purpose) & dpv_maintain_fraud_database = dpv_delivery_of_goods )
    | ( kge_leq(dpv_marketing, dpv_purpose) & dpv_marketing = dpv_delivery_of_goods )
    | ( kge_leq(dpv_member_partner_management, dpv_purpose) & dpv_member_partner_management = dpv_delivery_of_goods )
    | ( kge_leq(dpv_misuse_prevention_and_detection, dpv_purpose) & dpv_misuse_prevention_and_detection = dpv_delivery_of_goods )
    | ( kge_leq(dpv_non_commercial_purpose, dpv_purpose) & dpv_non_commercial_purpose = dpv_delivery_of_goods )
    | ( kge_leq(dpv_non_commercial_research, dpv_purpose) & dpv_non_commercial_research = dpv_delivery_of_goods )
    | ( kge_leq(dpv_optimisation_for_consumer, dpv_purpose) & dpv_optimisation_for_consumer = dpv_delivery_of_goods )
    | ( kge_leq(dpv_optimisation_for_controller, dpv_purpose) & dpv_optimisation_for_controller = dpv_delivery_of_goods )
    | ( kge_leq(dpv_optimise_user_interface, dpv_purpose) & dpv_optimise_user_interface = dpv_delivery_of_goods )
    | ( kge_leq(dpv_organisation_compliance_management, dpv_purpose) & dpv_organisation_compliance_management = dpv_delivery_of_goods )
    | ( kge_leq(dpv_organisation_governance, dpv_purpose) & dpv_organisation_governance = dpv_delivery_of_goods )
    | ( kge_leq(dpv_organisation_risk_management, dpv_purpose) & dpv_organisation_risk_management = dpv_delivery_of_goods )
    | ( kge_leq(dpv_payment_management, dpv_purpose) & dpv_payment_management = dpv_delivery_of_goods )
    | ( kge_leq(dpv_personalisation, dpv_purpose) & dpv_personalisation = dpv_delivery_of_goods )
    | ( kge_leq(dpv_personalised_advertising, dpv_purpose) & dpv_personalised_advertising = dpv_delivery_of_goods )
    | ( kge_leq(dpv_personalised_benefits, dpv_purpose) & dpv_personalised_benefits = dpv_delivery_of_goods )
    | ( kge_leq(dpv_personnel_behaviour_monitoring, dpv_purpose) & dpv_personnel_behaviour_monitoring = dpv_delivery_of_goods )
    | ( kge_leq(dpv_personnel_hiring, dpv_purpose) & dpv_personnel_hiring = dpv_delivery_of_goods )
    | ( kge_leq(dpv_personnel_management, dpv_purpose) & dpv_personnel_management = dpv_delivery_of_goods )
    | ( kge_leq(dpv_personnel_monitoring, dpv_purpose) & dpv_personnel_monitoring = dpv_delivery_of_goods )
    | ( kge_leq(dpv_personnel_offboarding, dpv_purpose) & dpv_personnel_offboarding = dpv_delivery_of_goods )
    | ( kge_leq(dpv_personnel_onboarding, dpv_purpose) & dpv_personnel_onboarding = dpv_delivery_of_goods )
    | ( kge_leq(dpv_personnel_payment, dpv_purpose) & dpv_personnel_payment = dpv_delivery_of_goods )
    | ( kge_leq(dpv_personnel_performance_evaluation, dpv_purpose) & dpv_personnel_performance_evaluation = dpv_delivery_of_goods )
    | ( kge_leq(dpv_personnel_performance_management, dpv_purpose) & dpv_personnel_performance_management = dpv_delivery_of_goods ) )
    | ( ( kge_leq(dpv_personnel_performance_monitoring, dpv_purpose) & dpv_personnel_performance_monitoring = dpv_delivery_of_goods )
    | ( kge_leq(dpv_personnel_performance_prediction, dpv_purpose) & dpv_personnel_performance_prediction = dpv_delivery_of_goods )
    | ( kge_leq(dpv_personnel_promotion_management, dpv_purpose) & dpv_personnel_promotion_management = dpv_delivery_of_goods )
    | ( kge_leq(dpv_personnel_termination_management, dpv_purpose) & dpv_personnel_termination_management = dpv_delivery_of_goods )
    | ( kge_leq(dpv_personnel_workload_management, dpv_purpose) & dpv_personnel_workload_management = dpv_delivery_of_goods )
    | ( kge_leq(dpv_political_campaign, dpv_purpose) & dpv_political_campaign = dpv_delivery_of_goods )
    | ( kge_leq(dpv_protection_of_ipr, dpv_purpose) & dpv_protection_of_ipr = dpv_delivery_of_goods )
    | ( kge_leq(dpv_protection_of_national_security, dpv_purpose) & dpv_protection_of_national_security = dpv_delivery_of_goods )
    | ( kge_leq(dpv_protection_of_public_security, dpv_purpose) & dpv_protection_of_public_security = dpv_delivery_of_goods )
    | ( kge_leq(dpv_provide_event_recommendations, dpv_purpose) & dpv_provide_event_recommendations = dpv_delivery_of_goods )
    | ( kge_leq(dpv_provide_official_statistics, dpv_purpose) & dpv_provide_official_statistics = dpv_delivery_of_goods )
    | ( kge_leq(dpv_provide_personalised_recommendations, dpv_purpose) & dpv_provide_personalised_recommendations = dpv_delivery_of_goods )
    | ( kge_leq(dpv_provide_product_recommendations, dpv_purpose) & dpv_provide_product_recommendations = dpv_delivery_of_goods )
    | ( kge_leq(dpv_public_benefit, dpv_purpose) & dpv_public_benefit = dpv_delivery_of_goods )
    | ( kge_leq(dpv_public_policy_making, dpv_purpose) & dpv_public_policy_making = dpv_delivery_of_goods )
    | ( kge_leq(dpv_public_relations, dpv_purpose) & dpv_public_relations = dpv_delivery_of_goods )
    | ( kge_leq(dpv_record_management, dpv_purpose) & dpv_record_management = dpv_delivery_of_goods )
    | ( kge_leq(dpv_recruitment_advertising, dpv_purpose) & dpv_recruitment_advertising = dpv_delivery_of_goods )
    | ( kge_leq(dpv_recruitment_applicant_background_check, dpv_purpose) & dpv_recruitment_applicant_background_check = dpv_delivery_of_goods )
    | ( kge_leq(dpv_recruitment_applicant_criminal_background_check, dpv_purpose) & dpv_recruitment_applicant_criminal_background_check = dpv_delivery_of_goods )
    | ( kge_leq(dpv_recruitment_applicant_information_authentication, dpv_purpose) & dpv_recruitment_applicant_information_authentication = dpv_delivery_of_goods )
    | ( kge_leq(dpv_recruitment_applicant_selection, dpv_purpose) & dpv_recruitment_applicant_selection = dpv_delivery_of_goods )
    | ( kge_leq(dpv_recruitment_application_analysis, dpv_purpose) & dpv_recruitment_application_analysis = dpv_delivery_of_goods )
    | ( kge_leq(dpv_recruitment_application_management, dpv_purpose) & dpv_recruitment_application_management = dpv_delivery_of_goods )
    | ( kge_leq(dpv_recruitment_application_screening, dpv_purpose) & dpv_recruitment_application_screening = dpv_delivery_of_goods )
    | ( kge_leq(dpv_recruitment_interview_analysis, dpv_purpose) & dpv_recruitment_interview_analysis = dpv_delivery_of_goods )
    | ( kge_leq(dpv_recruitment_interview_assessment, dpv_purpose) & dpv_recruitment_interview_assessment = dpv_delivery_of_goods )
    | ( kge_leq(dpv_recruitment_interview_management, dpv_purpose) & dpv_recruitment_interview_management = dpv_delivery_of_goods )
    | ( kge_leq(dpv_recruitment_interview_scheduling, dpv_purpose) & dpv_recruitment_interview_scheduling = dpv_delivery_of_goods )
    | ( kge_leq(dpv_recruitment_management, dpv_purpose) & dpv_recruitment_management = dpv_delivery_of_goods )
    | ( kge_leq(dpv_recruitment_targeted_advertising, dpv_purpose) & dpv_recruitment_targeted_advertising = dpv_delivery_of_goods )
    | ( kge_leq(dpv_repair_impairments, dpv_purpose) & dpv_repair_impairments = dpv_delivery_of_goods )
    | ( kge_leq(dpv_requested_service_provision, dpv_purpose) & dpv_requested_service_provision = dpv_delivery_of_goods )
    | ( kge_leq(dpv_research_and_development, dpv_purpose) & dpv_research_and_development = dpv_delivery_of_goods )
    | ( kge_leq(dpv_rights_fulfilment, dpv_purpose) & dpv_rights_fulfilment = dpv_delivery_of_goods )
    | ( kge_leq(dpv_scientific_research, dpv_purpose) & dpv_scientific_research = dpv_delivery_of_goods )
    | ( kge_leq(dpv_search_functionalities, dpv_purpose) & dpv_search_functionalities = dpv_delivery_of_goods )
    | ( kge_leq(dpv_sell_data_to_third_parties, dpv_purpose) & dpv_sell_data_to_third_parties = dpv_delivery_of_goods )
    | ( kge_leq(dpv_sell_insights_from_data, dpv_purpose) & dpv_sell_insights_from_data = dpv_delivery_of_goods )
    | ( kge_leq(dpv_sell_products, dpv_purpose) & dpv_sell_products = dpv_delivery_of_goods )
    | ( kge_leq(dpv_sell_products_to_data_subject, dpv_purpose) & dpv_sell_products_to_data_subject = dpv_delivery_of_goods )
    | ( kge_leq(dpv_service_access_determination, dpv_purpose) & dpv_service_access_determination = dpv_delivery_of_goods )
    | ( kge_leq(dpv_service_management, dpv_purpose) & dpv_service_management = dpv_delivery_of_goods )
    | ( kge_leq(dpv_service_monitoring, dpv_purpose) & dpv_service_monitoring = dpv_delivery_of_goods )
    | ( kge_leq(dpv_service_optimisation, dpv_purpose) & dpv_service_optimisation = dpv_delivery_of_goods )
    | ( kge_leq(dpv_service_personalisation, dpv_purpose) & dpv_service_personalisation = dpv_delivery_of_goods )
    | ( kge_leq(dpv_service_provision, dpv_purpose) & dpv_service_provision = dpv_delivery_of_goods )
    | ( kge_leq(dpv_service_registration, dpv_purpose) & dpv_service_registration = dpv_delivery_of_goods )
    | ( kge_leq(dpv_service_usage_analytics, dpv_purpose) & dpv_service_usage_analytics = dpv_delivery_of_goods )
    | ( kge_leq(dpv_social_media_marketing, dpv_purpose) & dpv_social_media_marketing = dpv_delivery_of_goods )
    | ( kge_leq(dpv_targeted_advertising, dpv_purpose) & dpv_targeted_advertising = dpv_delivery_of_goods )
    | ( kge_leq(dpv_technical_service_provision, dpv_purpose) & dpv_technical_service_provision = dpv_delivery_of_goods )
    | ( kge_leq(dpv_user_interface_personalisation, dpv_purpose) & dpv_user_interface_personalisation = dpv_delivery_of_goods )
    | ( kge_leq(dpv_vendor_management, dpv_purpose) & dpv_vendor_management = dpv_delivery_of_goods )
    | ( kge_leq(dpv_vendor_payment, dpv_purpose) & dpv_vendor_payment = dpv_delivery_of_goods )
    | ( kge_leq(dpv_vendor_records_management, dpv_purpose) & dpv_vendor_records_management = dpv_delivery_of_goods )
    | ( kge_leq(dpv_vendor_selection_assessment, dpv_purpose) & dpv_vendor_selection_assessment = dpv_delivery_of_goods )
    | ( kge_leq(dpv_verification, dpv_purpose) & dpv_verification = dpv_delivery_of_goods ) ) )).
%------------------------------------------------------------------------------
