%------------------------------------------------------------------------------
% File     : KGC064+2 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use with both encryption and access control in place against applies technical measures only, no organisational ones: no use meets both
% Version  : Especial.
%            Theorem formulation : The condition is written over the whole
%            vocabulary, as the paper's definition states; version 1 names
%            only the concepts a fixed value allows. The two versions have the
%            same status.
% English  : A controller permits use where encryption and access control are
%            both in place. A processor states that it applies technical
%            measures only, no organisational ones. This problem states that
%            no use meets the two policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag
%            v1.1.1
% Source   : [Mus26]
% Names    : KGC360-2 [Mus26]

% Status   : Unsatisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC360 is Compatible. Its two problems state that some use meets
%            the two policies (KGC063) and that no use does (KGC064). A pair
%            of policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent. Here the first is Satisfiable and the
%            second Unsatisfiable.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+4.ax').

fof(w_kgc360, axiom,
    ~ ( ( kge_leq(tm_encryption, tm_technical_measure) & kge_leq(tm_access_control_method, tm_technical_measure) & ( ( kge_leq(tm_encryption, tm_technical_measure)
    | kge_leq(tm_access_control_method, tm_technical_measure)
    | kge_leq(tm_technical_measure, tm_technical_measure)
    | kge_leq(tm_activity_monitoring, tm_technical_measure)
    | kge_leq(tm_anonymisation, tm_technical_measure)
    | kge_leq(tm_asymmetric_cryptography, tm_technical_measure)
    | kge_leq(tm_asymmetric_encryption, tm_technical_measure)
    | kge_leq(tm_authentication_a_b_c, tm_technical_measure)
    | kge_leq(tm_authentication_p_a_b_c, tm_technical_measure)
    | kge_leq(tm_authentication_protocols, tm_technical_measure)
    | kge_leq(tm_authorisation_protocols, tm_technical_measure)
    | kge_leq(tm_biometric_authentication, tm_technical_measure)
    | kge_leq(tm_cryptographic_authentication, tm_technical_measure)
    | kge_leq(tm_cryptographic_key_management, tm_technical_measure)
    | kge_leq(tm_cryptographic_methods, tm_technical_measure)
    | kge_leq(tm_data_backup_protocols, tm_technical_measure)
    | kge_leq(tm_data_redaction, tm_technical_measure)
    | kge_leq(tm_data_sanitisation_technique, tm_technical_measure)
    | kge_leq(tm_deidentification, tm_technical_measure)
    | kge_leq(tm_deterministic_pseudonymisation, tm_technical_measure)
    | kge_leq(tm_differential_privacy, tm_technical_measure)
    | kge_leq(tm_digital_rights_management, tm_technical_measure)
    | kge_leq(tm_digital_signatures, tm_technical_measure)
    | kge_leq(tm_distributed_system_security, tm_technical_measure)
    | kge_leq(tm_document_randomised_pseudonymisation, tm_technical_measure)
    | kge_leq(tm_document_security, tm_technical_measure)
    | kge_leq(tm_encryption_at_rest, tm_technical_measure)
    | kge_leq(tm_encryption_in_transfer, tm_technical_measure)
    | kge_leq(tm_encryption_in_use, tm_technical_measure)
    | kge_leq(tm_end_to_end_encryption, tm_technical_measure)
    | kge_leq(tm_fail_safe_protocols, tm_technical_measure)
    | kge_leq(tm_file_system_security, tm_technical_measure)
    | kge_leq(tm_fully_randomised_pseudonymisation, tm_technical_measure)
    | kge_leq(tm_hardware_security_protocols, tm_technical_measure)
    | kge_leq(tm_hash_functions, tm_technical_measure)
    | kge_leq(tm_hash_message_authentication_code, tm_technical_measure)
    | kge_leq(tm_homomorphic_encryption, tm_technical_measure)
    | kge_leq(tm_information_flow_control, tm_technical_measure)
    | kge_leq(tm_intrusion_detection_system, tm_technical_measure)
    | kge_leq(tm_legal_measure, tm_technical_measure)
    | kge_leq(tm_message_authentication_codes, tm_technical_measure)
    | kge_leq(tm_mobile_platform_security, tm_technical_measure)
    | kge_leq(tm_monotonic_counter_pseudonymisation, tm_technical_measure)
    | kge_leq(tm_multi_factor_authentication, tm_technical_measure)
    | kge_leq(tm_network_proxy_routing, tm_technical_measure)
    | kge_leq(tm_network_security_protocols, tm_technical_measure)
    | kge_leq(tm_operating_system_security, tm_technical_measure)
    | kge_leq(tm_organisational_measure, tm_technical_measure)
    | kge_leq(tm_password_authentication, tm_technical_measure)
    | kge_leq(tm_penetration_testing_methods, tm_technical_measure)
    | kge_leq(tm_physical_measure, tm_technical_measure)
    | kge_leq(tm_post_quantum_cryptography, tm_technical_measure)
    | kge_leq(tm_privacy_preserving_protocol, tm_technical_measure)
    | kge_leq(tm_private_information_retrieval, tm_technical_measure)
    | kge_leq(tm_pseudonymisation, tm_technical_measure)
    | kge_leq(tm_quantum_cryptography, tm_technical_measure)
    | kge_leq(tm_r_n_g_pseudonymisation, tm_technical_measure)
    | kge_leq(tm_secret_sharing_schemes, tm_technical_measure)
    | kge_leq(tm_secure_multi_party_computation, tm_technical_measure)
    | kge_leq(tm_security_method, tm_technical_measure)
    | kge_leq(tm_single_sign_on, tm_technical_measure)
    | kge_leq(tm_symmetric_cryptography, tm_technical_measure)
    | kge_leq(tm_symmetric_encryption, tm_technical_measure)
    | kge_leq(tm_technical_organisational_measure, tm_technical_measure) )
    | ( kge_leq(tm_trusted_computing, tm_technical_measure)
    | kge_leq(tm_trusted_execution_environment, tm_technical_measure)
    | kge_leq(tm_usage_control, tm_technical_measure)
    | kge_leq(tm_use_synthetic_data, tm_technical_measure)
    | kge_leq(tm_virtualisation_security, tm_technical_measure)
    | kge_leq(tm_vulnerability_testing_methods, tm_technical_measure)
    | kge_leq(tm_web_browser_security, tm_technical_measure)
    | kge_leq(tm_web_security_protocols, tm_technical_measure)
    | kge_leq(tm_wireless_security_protocols, tm_technical_measure)
    | kge_leq(tm_zero_knowledge_authentication, tm_technical_measure) ) ) ) )).
%------------------------------------------------------------------------------
