%------------------------------------------------------------------------------
% File     : KGC111+2 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use for public benefit or any narrower purpose against use for both data altruism and improving transport mobility: some use meets both
% Version  : Especial.
%            Theorem formulation : The condition is written over the whole
%            vocabulary, as the paper's definition states; version 1 names
%            only the concepts a fixed value allows. The two versions have the
%            same status.
% English  : A city's traffic data platform permits use for public benefit or
%            any narrower purpose. A city transport authority commits to data
%            altruism and improving transport mobility together. This problem
%            states that some use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag
%            v1.1.1
% Source   : [Mus26]
% Names    : KGC396-1 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC396 is Compatible. Its two problems state that some use meets
%            the two policies (KGC111) and that no use does (KGC112). A pair
%            of policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent. Here the first is Satisfiable and the
%            second Unsatisfiable.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+3.ax').

fof(w_kgc396, axiom,
    ( kge_leq(dpv_data_altruism, dpv_public_benefit) & kge_leq(dpv_improve_transport_mobility, dpv_public_benefit) & ( ( kge_leq(dpv_public_benefit, dpv_public_benefit)
    | kge_leq(dpv_data_altruism, dpv_public_benefit)
    | kge_leq(dpv_improve_transport_mobility, dpv_public_benefit)
    | kge_leq(dpv_academic_research, dpv_public_benefit)
    | kge_leq(dpv_account_management, dpv_public_benefit)
    | kge_leq(dpv_advertising, dpv_public_benefit)
    | kge_leq(dpv_age_verification, dpv_public_benefit)
    | kge_leq(dpv_combat_climate_change, dpv_public_benefit)
    | kge_leq(dpv_commercial_purpose, dpv_public_benefit)
    | kge_leq(dpv_commercial_research, dpv_public_benefit)
    | kge_leq(dpv_communication_for_customer_care, dpv_public_benefit)
    | kge_leq(dpv_communication_management, dpv_public_benefit)
    | kge_leq(dpv_counter_money_laundering, dpv_public_benefit)
    | kge_leq(dpv_counterterrorism, dpv_public_benefit)
    | kge_leq(dpv_customer_care, dpv_public_benefit)
    | kge_leq(dpv_customer_claims_management, dpv_public_benefit)
    | kge_leq(dpv_customer_management, dpv_public_benefit)
    | kge_leq(dpv_customer_order_management, dpv_public_benefit)
    | kge_leq(dpv_customer_relationship_management, dpv_public_benefit)
    | kge_leq(dpv_customer_solvency_monitoring, dpv_public_benefit)
    | kge_leq(dpv_delivery_of_goods, dpv_public_benefit)
    | kge_leq(dpv_direct_marketing, dpv_public_benefit)
    | kge_leq(dpv_dispute_management, dpv_public_benefit)
    | kge_leq(dpv_enforce_access_control, dpv_public_benefit)
    | kge_leq(dpv_enforce_security, dpv_public_benefit)
    | kge_leq(dpv_establish_contractual_agreement, dpv_public_benefit)
    | kge_leq(dpv_fraud_prevention_and_detection, dpv_public_benefit)
    | kge_leq(dpv_fulfilment_of_contractual_obligation, dpv_public_benefit)
    | kge_leq(dpv_fulfilment_of_obligation, dpv_public_benefit)
    | kge_leq(dpv_human_resource_management, dpv_public_benefit)
    | kge_leq(dpv_identity_authentication, dpv_public_benefit)
    | kge_leq(dpv_identity_verification, dpv_public_benefit)
    | kge_leq(dpv_improve_existing_products_and_services, dpv_public_benefit)
    | kge_leq(dpv_improve_healthcare, dpv_public_benefit)
    | kge_leq(dpv_improve_internal_crm_processes, dpv_public_benefit)
    | kge_leq(dpv_improve_public_services, dpv_public_benefit)
    | kge_leq(dpv_increase_service_robustness, dpv_public_benefit)
    | kge_leq(dpv_internal_resource_optimisation, dpv_public_benefit)
    | kge_leq(dpv_legal_compliance, dpv_public_benefit)
    | kge_leq(dpv_maintain_fraud_database, dpv_public_benefit)
    | kge_leq(dpv_marketing, dpv_public_benefit)
    | kge_leq(dpv_member_partner_management, dpv_public_benefit)
    | kge_leq(dpv_misuse_prevention_and_detection, dpv_public_benefit)
    | kge_leq(dpv_non_commercial_purpose, dpv_public_benefit)
    | kge_leq(dpv_non_commercial_research, dpv_public_benefit)
    | kge_leq(dpv_optimisation_for_consumer, dpv_public_benefit)
    | kge_leq(dpv_optimisation_for_controller, dpv_public_benefit)
    | kge_leq(dpv_optimise_user_interface, dpv_public_benefit)
    | kge_leq(dpv_organisation_compliance_management, dpv_public_benefit)
    | kge_leq(dpv_organisation_governance, dpv_public_benefit)
    | kge_leq(dpv_organisation_risk_management, dpv_public_benefit)
    | kge_leq(dpv_payment_management, dpv_public_benefit)
    | kge_leq(dpv_personalisation, dpv_public_benefit)
    | kge_leq(dpv_personalised_advertising, dpv_public_benefit)
    | kge_leq(dpv_personalised_benefits, dpv_public_benefit)
    | kge_leq(dpv_personnel_behaviour_monitoring, dpv_public_benefit)
    | kge_leq(dpv_personnel_hiring, dpv_public_benefit)
    | kge_leq(dpv_personnel_management, dpv_public_benefit)
    | kge_leq(dpv_personnel_monitoring, dpv_public_benefit)
    | kge_leq(dpv_personnel_offboarding, dpv_public_benefit)
    | kge_leq(dpv_personnel_onboarding, dpv_public_benefit)
    | kge_leq(dpv_personnel_payment, dpv_public_benefit)
    | kge_leq(dpv_personnel_performance_evaluation, dpv_public_benefit)
    | kge_leq(dpv_personnel_performance_management, dpv_public_benefit) )
    | ( kge_leq(dpv_personnel_performance_monitoring, dpv_public_benefit)
    | kge_leq(dpv_personnel_performance_prediction, dpv_public_benefit)
    | kge_leq(dpv_personnel_promotion_management, dpv_public_benefit)
    | kge_leq(dpv_personnel_termination_management, dpv_public_benefit)
    | kge_leq(dpv_personnel_workload_management, dpv_public_benefit)
    | kge_leq(dpv_political_campaign, dpv_public_benefit)
    | kge_leq(dpv_protection_of_ipr, dpv_public_benefit)
    | kge_leq(dpv_protection_of_national_security, dpv_public_benefit)
    | kge_leq(dpv_protection_of_public_security, dpv_public_benefit)
    | kge_leq(dpv_provide_event_recommendations, dpv_public_benefit)
    | kge_leq(dpv_provide_official_statistics, dpv_public_benefit)
    | kge_leq(dpv_provide_personalised_recommendations, dpv_public_benefit)
    | kge_leq(dpv_provide_product_recommendations, dpv_public_benefit)
    | kge_leq(dpv_public_policy_making, dpv_public_benefit)
    | kge_leq(dpv_public_relations, dpv_public_benefit)
    | kge_leq(dpv_purpose, dpv_public_benefit)
    | kge_leq(dpv_record_management, dpv_public_benefit)
    | kge_leq(dpv_recruitment_advertising, dpv_public_benefit)
    | kge_leq(dpv_recruitment_applicant_background_check, dpv_public_benefit)
    | kge_leq(dpv_recruitment_applicant_criminal_background_check, dpv_public_benefit)
    | kge_leq(dpv_recruitment_applicant_information_authentication, dpv_public_benefit)
    | kge_leq(dpv_recruitment_applicant_selection, dpv_public_benefit)
    | kge_leq(dpv_recruitment_application_analysis, dpv_public_benefit)
    | kge_leq(dpv_recruitment_application_management, dpv_public_benefit)
    | kge_leq(dpv_recruitment_application_screening, dpv_public_benefit)
    | kge_leq(dpv_recruitment_interview_analysis, dpv_public_benefit)
    | kge_leq(dpv_recruitment_interview_assessment, dpv_public_benefit)
    | kge_leq(dpv_recruitment_interview_management, dpv_public_benefit)
    | kge_leq(dpv_recruitment_interview_scheduling, dpv_public_benefit)
    | kge_leq(dpv_recruitment_management, dpv_public_benefit)
    | kge_leq(dpv_recruitment_targeted_advertising, dpv_public_benefit)
    | kge_leq(dpv_repair_impairments, dpv_public_benefit)
    | kge_leq(dpv_requested_service_provision, dpv_public_benefit)
    | kge_leq(dpv_research_and_development, dpv_public_benefit)
    | kge_leq(dpv_scientific_research, dpv_public_benefit)
    | kge_leq(dpv_search_functionalities, dpv_public_benefit)
    | kge_leq(dpv_sell_data_to_third_parties, dpv_public_benefit)
    | kge_leq(dpv_sell_insights_from_data, dpv_public_benefit)
    | kge_leq(dpv_sell_products, dpv_public_benefit)
    | kge_leq(dpv_sell_products_to_data_subject, dpv_public_benefit)
    | kge_leq(dpv_service_access_determination, dpv_public_benefit)
    | kge_leq(dpv_service_management, dpv_public_benefit)
    | kge_leq(dpv_service_monitoring, dpv_public_benefit)
    | kge_leq(dpv_service_optimisation, dpv_public_benefit)
    | kge_leq(dpv_service_personalisation, dpv_public_benefit)
    | kge_leq(dpv_service_provision, dpv_public_benefit)
    | kge_leq(dpv_service_registration, dpv_public_benefit)
    | kge_leq(dpv_service_usage_analytics, dpv_public_benefit)
    | kge_leq(dpv_social_media_marketing, dpv_public_benefit)
    | kge_leq(dpv_targeted_advertising, dpv_public_benefit)
    | kge_leq(dpv_technical_service_provision, dpv_public_benefit)
    | kge_leq(dpv_user_interface_personalisation, dpv_public_benefit)
    | kge_leq(dpv_vendor_management, dpv_public_benefit)
    | kge_leq(dpv_vendor_payment, dpv_public_benefit)
    | kge_leq(dpv_vendor_records_management, dpv_public_benefit)
    | kge_leq(dpv_vendor_selection_assessment, dpv_public_benefit)
    | kge_leq(dpv_verification, dpv_public_benefit) ) ) )).
%------------------------------------------------------------------------------
