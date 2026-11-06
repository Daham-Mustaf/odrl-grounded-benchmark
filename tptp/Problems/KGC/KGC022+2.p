%------------------------------------------------------------------------------
% File     : KGC022+2 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use for scientific research or any narrower purpose against use for research and development only: no use meets both
% Version  : Especial.
%            Theorem formulation : The condition is written over the whole
%            vocabulary, as the paper's definition states; version 1 names
%            only the concepts a fixed value allows. The versions have the
%            same status.
% English  : A city's traffic data platform permits use for scientific
%            research or any narrower purpose. A company commits to use for
%            research and development. This problem states that no use meets
%            the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag v1.2
% Source   : [Mus26]
% Names    : KGC316-2 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC316 is Unknown. Its two problems state that some use meets the
%            two policies (KGC021) and that no use does (KGC022); here the
%            first is Satisfiable and the second Satisfiable. A pair of
%            policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+3.ax').

fof(w_kgc316, axiom,
    ~ ( ( ( ( kge_leq(dpv_scientific_research, dpv_scientific_research) & dpv_scientific_research = dpv_research_and_development )
    | kge_leq(dpv_research_and_development, dpv_scientific_research)
    | ( kge_leq(dpv_academic_research, dpv_scientific_research) & dpv_academic_research = dpv_research_and_development )
    | ( kge_leq(dpv_account_management, dpv_scientific_research) & dpv_account_management = dpv_research_and_development )
    | ( kge_leq(dpv_advertising, dpv_scientific_research) & dpv_advertising = dpv_research_and_development )
    | ( kge_leq(dpv_age_verification, dpv_scientific_research) & dpv_age_verification = dpv_research_and_development )
    | ( kge_leq(dpv_combat_climate_change, dpv_scientific_research) & dpv_combat_climate_change = dpv_research_and_development )
    | ( kge_leq(dpv_commercial_purpose, dpv_scientific_research) & dpv_commercial_purpose = dpv_research_and_development )
    | ( kge_leq(dpv_commercial_research, dpv_scientific_research) & dpv_commercial_research = dpv_research_and_development )
    | ( kge_leq(dpv_communication_for_customer_care, dpv_scientific_research) & dpv_communication_for_customer_care = dpv_research_and_development )
    | ( kge_leq(dpv_communication_management, dpv_scientific_research) & dpv_communication_management = dpv_research_and_development )
    | ( kge_leq(dpv_counter_money_laundering, dpv_scientific_research) & dpv_counter_money_laundering = dpv_research_and_development )
    | ( kge_leq(dpv_counterterrorism, dpv_scientific_research) & dpv_counterterrorism = dpv_research_and_development )
    | ( kge_leq(dpv_customer_care, dpv_scientific_research) & dpv_customer_care = dpv_research_and_development )
    | ( kge_leq(dpv_customer_claims_management, dpv_scientific_research) & dpv_customer_claims_management = dpv_research_and_development )
    | ( kge_leq(dpv_customer_management, dpv_scientific_research) & dpv_customer_management = dpv_research_and_development )
    | ( kge_leq(dpv_customer_order_management, dpv_scientific_research) & dpv_customer_order_management = dpv_research_and_development )
    | ( kge_leq(dpv_customer_relationship_management, dpv_scientific_research) & dpv_customer_relationship_management = dpv_research_and_development )
    | ( kge_leq(dpv_customer_solvency_monitoring, dpv_scientific_research) & dpv_customer_solvency_monitoring = dpv_research_and_development )
    | ( kge_leq(dpv_data_altruism, dpv_scientific_research) & dpv_data_altruism = dpv_research_and_development )
    | ( kge_leq(dpv_delivery_of_goods, dpv_scientific_research) & dpv_delivery_of_goods = dpv_research_and_development )
    | ( kge_leq(dpv_direct_marketing, dpv_scientific_research) & dpv_direct_marketing = dpv_research_and_development )
    | ( kge_leq(dpv_dispute_management, dpv_scientific_research) & dpv_dispute_management = dpv_research_and_development )
    | ( kge_leq(dpv_enforce_access_control, dpv_scientific_research) & dpv_enforce_access_control = dpv_research_and_development )
    | ( kge_leq(dpv_enforce_security, dpv_scientific_research) & dpv_enforce_security = dpv_research_and_development )
    | ( kge_leq(dpv_establish_contractual_agreement, dpv_scientific_research) & dpv_establish_contractual_agreement = dpv_research_and_development )
    | ( kge_leq(dpv_fraud_prevention_and_detection, dpv_scientific_research) & dpv_fraud_prevention_and_detection = dpv_research_and_development )
    | ( kge_leq(dpv_fulfilment_of_contractual_obligation, dpv_scientific_research) & dpv_fulfilment_of_contractual_obligation = dpv_research_and_development )
    | ( kge_leq(dpv_fulfilment_of_obligation, dpv_scientific_research) & dpv_fulfilment_of_obligation = dpv_research_and_development )
    | ( kge_leq(dpv_human_resource_management, dpv_scientific_research) & dpv_human_resource_management = dpv_research_and_development )
    | ( kge_leq(dpv_identity_authentication, dpv_scientific_research) & dpv_identity_authentication = dpv_research_and_development )
    | ( kge_leq(dpv_identity_verification, dpv_scientific_research) & dpv_identity_verification = dpv_research_and_development )
    | ( kge_leq(dpv_improve_existing_products_and_services, dpv_scientific_research) & dpv_improve_existing_products_and_services = dpv_research_and_development )
    | ( kge_leq(dpv_improve_healthcare, dpv_scientific_research) & dpv_improve_healthcare = dpv_research_and_development )
    | ( kge_leq(dpv_improve_internal_crm_processes, dpv_scientific_research) & dpv_improve_internal_crm_processes = dpv_research_and_development )
    | ( kge_leq(dpv_improve_public_services, dpv_scientific_research) & dpv_improve_public_services = dpv_research_and_development )
    | ( kge_leq(dpv_improve_transport_mobility, dpv_scientific_research) & dpv_improve_transport_mobility = dpv_research_and_development )
    | ( kge_leq(dpv_increase_service_robustness, dpv_scientific_research) & dpv_increase_service_robustness = dpv_research_and_development )
    | ( kge_leq(dpv_internal_resource_optimisation, dpv_scientific_research) & dpv_internal_resource_optimisation = dpv_research_and_development )
    | ( kge_leq(dpv_legal_compliance, dpv_scientific_research) & dpv_legal_compliance = dpv_research_and_development )
    | ( kge_leq(dpv_maintain_fraud_database, dpv_scientific_research) & dpv_maintain_fraud_database = dpv_research_and_development )
    | ( kge_leq(dpv_marketing, dpv_scientific_research) & dpv_marketing = dpv_research_and_development )
    | ( kge_leq(dpv_member_partner_management, dpv_scientific_research) & dpv_member_partner_management = dpv_research_and_development )
    | ( kge_leq(dpv_misuse_prevention_and_detection, dpv_scientific_research) & dpv_misuse_prevention_and_detection = dpv_research_and_development )
    | ( kge_leq(dpv_non_commercial_purpose, dpv_scientific_research) & dpv_non_commercial_purpose = dpv_research_and_development )
    | ( kge_leq(dpv_non_commercial_research, dpv_scientific_research) & dpv_non_commercial_research = dpv_research_and_development )
    | ( kge_leq(dpv_optimisation_for_consumer, dpv_scientific_research) & dpv_optimisation_for_consumer = dpv_research_and_development )
    | ( kge_leq(dpv_optimisation_for_controller, dpv_scientific_research) & dpv_optimisation_for_controller = dpv_research_and_development )
    | ( kge_leq(dpv_optimise_user_interface, dpv_scientific_research) & dpv_optimise_user_interface = dpv_research_and_development )
    | ( kge_leq(dpv_organisation_compliance_management, dpv_scientific_research) & dpv_organisation_compliance_management = dpv_research_and_development )
    | ( kge_leq(dpv_organisation_governance, dpv_scientific_research) & dpv_organisation_governance = dpv_research_and_development )
    | ( kge_leq(dpv_organisation_risk_management, dpv_scientific_research) & dpv_organisation_risk_management = dpv_research_and_development )
    | ( kge_leq(dpv_payment_management, dpv_scientific_research) & dpv_payment_management = dpv_research_and_development )
    | ( kge_leq(dpv_personalisation, dpv_scientific_research) & dpv_personalisation = dpv_research_and_development )
    | ( kge_leq(dpv_personalised_advertising, dpv_scientific_research) & dpv_personalised_advertising = dpv_research_and_development )
    | ( kge_leq(dpv_personalised_benefits, dpv_scientific_research) & dpv_personalised_benefits = dpv_research_and_development )
    | ( kge_leq(dpv_personnel_behaviour_monitoring, dpv_scientific_research) & dpv_personnel_behaviour_monitoring = dpv_research_and_development )
    | ( kge_leq(dpv_personnel_hiring, dpv_scientific_research) & dpv_personnel_hiring = dpv_research_and_development )
    | ( kge_leq(dpv_personnel_management, dpv_scientific_research) & dpv_personnel_management = dpv_research_and_development )
    | ( kge_leq(dpv_personnel_monitoring, dpv_scientific_research) & dpv_personnel_monitoring = dpv_research_and_development )
    | ( kge_leq(dpv_personnel_offboarding, dpv_scientific_research) & dpv_personnel_offboarding = dpv_research_and_development )
    | ( kge_leq(dpv_personnel_onboarding, dpv_scientific_research) & dpv_personnel_onboarding = dpv_research_and_development )
    | ( kge_leq(dpv_personnel_payment, dpv_scientific_research) & dpv_personnel_payment = dpv_research_and_development )
    | ( kge_leq(dpv_personnel_performance_evaluation, dpv_scientific_research) & dpv_personnel_performance_evaluation = dpv_research_and_development ) )
    | ( ( kge_leq(dpv_personnel_performance_management, dpv_scientific_research) & dpv_personnel_performance_management = dpv_research_and_development )
    | ( kge_leq(dpv_personnel_performance_monitoring, dpv_scientific_research) & dpv_personnel_performance_monitoring = dpv_research_and_development )
    | ( kge_leq(dpv_personnel_performance_prediction, dpv_scientific_research) & dpv_personnel_performance_prediction = dpv_research_and_development )
    | ( kge_leq(dpv_personnel_promotion_management, dpv_scientific_research) & dpv_personnel_promotion_management = dpv_research_and_development )
    | ( kge_leq(dpv_personnel_termination_management, dpv_scientific_research) & dpv_personnel_termination_management = dpv_research_and_development )
    | ( kge_leq(dpv_personnel_workload_management, dpv_scientific_research) & dpv_personnel_workload_management = dpv_research_and_development )
    | ( kge_leq(dpv_political_campaign, dpv_scientific_research) & dpv_political_campaign = dpv_research_and_development )
    | ( kge_leq(dpv_protection_of_ipr, dpv_scientific_research) & dpv_protection_of_ipr = dpv_research_and_development )
    | ( kge_leq(dpv_protection_of_national_security, dpv_scientific_research) & dpv_protection_of_national_security = dpv_research_and_development )
    | ( kge_leq(dpv_protection_of_public_security, dpv_scientific_research) & dpv_protection_of_public_security = dpv_research_and_development )
    | ( kge_leq(dpv_provide_event_recommendations, dpv_scientific_research) & dpv_provide_event_recommendations = dpv_research_and_development )
    | ( kge_leq(dpv_provide_official_statistics, dpv_scientific_research) & dpv_provide_official_statistics = dpv_research_and_development )
    | ( kge_leq(dpv_provide_personalised_recommendations, dpv_scientific_research) & dpv_provide_personalised_recommendations = dpv_research_and_development )
    | ( kge_leq(dpv_provide_product_recommendations, dpv_scientific_research) & dpv_provide_product_recommendations = dpv_research_and_development )
    | ( kge_leq(dpv_public_benefit, dpv_scientific_research) & dpv_public_benefit = dpv_research_and_development )
    | ( kge_leq(dpv_public_policy_making, dpv_scientific_research) & dpv_public_policy_making = dpv_research_and_development )
    | ( kge_leq(dpv_public_relations, dpv_scientific_research) & dpv_public_relations = dpv_research_and_development )
    | ( kge_leq(dpv_purpose, dpv_scientific_research) & dpv_purpose = dpv_research_and_development )
    | ( kge_leq(dpv_record_management, dpv_scientific_research) & dpv_record_management = dpv_research_and_development )
    | ( kge_leq(dpv_recruitment_advertising, dpv_scientific_research) & dpv_recruitment_advertising = dpv_research_and_development )
    | ( kge_leq(dpv_recruitment_applicant_background_check, dpv_scientific_research) & dpv_recruitment_applicant_background_check = dpv_research_and_development )
    | ( kge_leq(dpv_recruitment_applicant_criminal_background_check, dpv_scientific_research) & dpv_recruitment_applicant_criminal_background_check = dpv_research_and_development )
    | ( kge_leq(dpv_recruitment_applicant_information_authentication, dpv_scientific_research) & dpv_recruitment_applicant_information_authentication = dpv_research_and_development )
    | ( kge_leq(dpv_recruitment_applicant_selection, dpv_scientific_research) & dpv_recruitment_applicant_selection = dpv_research_and_development )
    | ( kge_leq(dpv_recruitment_application_analysis, dpv_scientific_research) & dpv_recruitment_application_analysis = dpv_research_and_development )
    | ( kge_leq(dpv_recruitment_application_management, dpv_scientific_research) & dpv_recruitment_application_management = dpv_research_and_development )
    | ( kge_leq(dpv_recruitment_application_screening, dpv_scientific_research) & dpv_recruitment_application_screening = dpv_research_and_development )
    | ( kge_leq(dpv_recruitment_interview_analysis, dpv_scientific_research) & dpv_recruitment_interview_analysis = dpv_research_and_development )
    | ( kge_leq(dpv_recruitment_interview_assessment, dpv_scientific_research) & dpv_recruitment_interview_assessment = dpv_research_and_development )
    | ( kge_leq(dpv_recruitment_interview_management, dpv_scientific_research) & dpv_recruitment_interview_management = dpv_research_and_development )
    | ( kge_leq(dpv_recruitment_interview_scheduling, dpv_scientific_research) & dpv_recruitment_interview_scheduling = dpv_research_and_development )
    | ( kge_leq(dpv_recruitment_management, dpv_scientific_research) & dpv_recruitment_management = dpv_research_and_development )
    | ( kge_leq(dpv_recruitment_targeted_advertising, dpv_scientific_research) & dpv_recruitment_targeted_advertising = dpv_research_and_development )
    | ( kge_leq(dpv_repair_impairments, dpv_scientific_research) & dpv_repair_impairments = dpv_research_and_development )
    | ( kge_leq(dpv_requested_service_provision, dpv_scientific_research) & dpv_requested_service_provision = dpv_research_and_development )
    | ( kge_leq(dpv_rights_fulfilment, dpv_scientific_research) & dpv_rights_fulfilment = dpv_research_and_development )
    | ( kge_leq(dpv_search_functionalities, dpv_scientific_research) & dpv_search_functionalities = dpv_research_and_development )
    | ( kge_leq(dpv_sell_data_to_third_parties, dpv_scientific_research) & dpv_sell_data_to_third_parties = dpv_research_and_development )
    | ( kge_leq(dpv_sell_insights_from_data, dpv_scientific_research) & dpv_sell_insights_from_data = dpv_research_and_development )
    | ( kge_leq(dpv_sell_products, dpv_scientific_research) & dpv_sell_products = dpv_research_and_development )
    | ( kge_leq(dpv_sell_products_to_data_subject, dpv_scientific_research) & dpv_sell_products_to_data_subject = dpv_research_and_development )
    | ( kge_leq(dpv_service_access_determination, dpv_scientific_research) & dpv_service_access_determination = dpv_research_and_development )
    | ( kge_leq(dpv_service_management, dpv_scientific_research) & dpv_service_management = dpv_research_and_development )
    | ( kge_leq(dpv_service_monitoring, dpv_scientific_research) & dpv_service_monitoring = dpv_research_and_development )
    | ( kge_leq(dpv_service_optimisation, dpv_scientific_research) & dpv_service_optimisation = dpv_research_and_development )
    | ( kge_leq(dpv_service_personalisation, dpv_scientific_research) & dpv_service_personalisation = dpv_research_and_development )
    | ( kge_leq(dpv_service_provision, dpv_scientific_research) & dpv_service_provision = dpv_research_and_development )
    | ( kge_leq(dpv_service_registration, dpv_scientific_research) & dpv_service_registration = dpv_research_and_development )
    | ( kge_leq(dpv_service_usage_analytics, dpv_scientific_research) & dpv_service_usage_analytics = dpv_research_and_development )
    | ( kge_leq(dpv_social_media_marketing, dpv_scientific_research) & dpv_social_media_marketing = dpv_research_and_development )
    | ( kge_leq(dpv_targeted_advertising, dpv_scientific_research) & dpv_targeted_advertising = dpv_research_and_development )
    | ( kge_leq(dpv_technical_service_provision, dpv_scientific_research) & dpv_technical_service_provision = dpv_research_and_development )
    | ( kge_leq(dpv_user_interface_personalisation, dpv_scientific_research) & dpv_user_interface_personalisation = dpv_research_and_development )
    | ( kge_leq(dpv_vendor_management, dpv_scientific_research) & dpv_vendor_management = dpv_research_and_development )
    | ( kge_leq(dpv_vendor_payment, dpv_scientific_research) & dpv_vendor_payment = dpv_research_and_development )
    | ( kge_leq(dpv_vendor_records_management, dpv_scientific_research) & dpv_vendor_records_management = dpv_research_and_development )
    | ( kge_leq(dpv_vendor_selection_assessment, dpv_scientific_research) & dpv_vendor_selection_assessment = dpv_research_and_development )
    | ( kge_leq(dpv_verification, dpv_scientific_research) & dpv_verification = dpv_research_and_development ) ) ) )).
%------------------------------------------------------------------------------
