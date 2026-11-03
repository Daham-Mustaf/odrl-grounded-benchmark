%------------------------------------------------------------------------------
% File     : KGC074+2 : placeholder, for TPTP use only
% Domain   : Semantic Web (ODRL policies), proposed
% Problem  : Use with at least one of encryption and access control in place against use with encryption at rest as the only measure: no use meets both
% Version  : Especial.
%            Theorem formulation : The condition is written over the whole
%            vocabulary, as the paper's definition states; version 1 names
%            only the concepts a fixed value allows. The two versions have the
%            same status.
% English  : A controller requires at least one of encryption and access
%            control. A processor's policy commits to encryption at rest as
%            the only measure. This problem states that no use meets the two
%            policies.

% Refs     : [Mus26] Mustafa (2026), odrl-grounded-benchmark,
%            https://github.com/Daham-Mustaf/odrl-grounded-benchmark, tag
%            v1.1.1
% Source   : [Mus26]
% Names    : KGC366-2 [Mus26]

% Status   : Satisfiable
% Rating   : left to TPTP
% Syntax   : left to TPTP
% SPC      : left to TPTP

% Comments : KGC366 is Incompatible. Its two problems state that some use
%            meets the two policies (KGC073) and that no use does (KGC074). A
%            pair of policies is Incompatible when the first is Unsatisfiable,
%            Compatible when the second is Unsatisfiable, and Unknown when
%            both are Satisfiable; a Satisfiable problem also shows the
%            statements consistent. Here the first is Unsatisfiable and the
%            second Satisfiable.
%------------------------------------------------------------------------------
include('Axioms/KGC000+0.ax').
include('Axioms/KGC000+4.ax').

fof(bg_dist_tm_encryption_tm_access_control_method, axiom,
    tm_encryption != tm_access_control_method).

fof(bg_dist_tm_encryption_tm_encryption_at_rest, axiom,
    tm_encryption != tm_encryption_at_rest).

fof(bg_dist_tm_encryption_tm_activity_monitoring, axiom,
    tm_encryption != tm_activity_monitoring).

fof(bg_dist_tm_encryption_tm_anonymisation, axiom,
    tm_encryption != tm_anonymisation).

fof(bg_dist_tm_encryption_tm_asymmetric_cryptography, axiom,
    tm_encryption != tm_asymmetric_cryptography).

fof(bg_dist_tm_encryption_tm_asymmetric_encryption, axiom,
    tm_encryption != tm_asymmetric_encryption).

fof(bg_dist_tm_encryption_tm_authentication_a_b_c, axiom,
    tm_encryption != tm_authentication_a_b_c).

fof(bg_dist_tm_encryption_tm_authentication_p_a_b_c, axiom,
    tm_encryption != tm_authentication_p_a_b_c).

fof(bg_dist_tm_encryption_tm_authentication_protocols, axiom,
    tm_encryption != tm_authentication_protocols).

fof(bg_dist_tm_encryption_tm_authorisation_protocols, axiom,
    tm_encryption != tm_authorisation_protocols).

fof(bg_dist_tm_encryption_tm_biometric_authentication, axiom,
    tm_encryption != tm_biometric_authentication).

fof(bg_dist_tm_encryption_tm_cryptographic_authentication, axiom,
    tm_encryption != tm_cryptographic_authentication).

fof(bg_dist_tm_encryption_tm_cryptographic_key_management, axiom,
    tm_encryption != tm_cryptographic_key_management).

fof(bg_dist_tm_encryption_tm_cryptographic_methods, axiom,
    tm_encryption != tm_cryptographic_methods).

fof(bg_dist_tm_encryption_tm_data_backup_protocols, axiom,
    tm_encryption != tm_data_backup_protocols).

fof(bg_dist_tm_encryption_tm_data_redaction, axiom,
    tm_encryption != tm_data_redaction).

fof(bg_dist_tm_encryption_tm_data_sanitisation_technique, axiom,
    tm_encryption != tm_data_sanitisation_technique).

fof(bg_dist_tm_encryption_tm_deidentification, axiom,
    tm_encryption != tm_deidentification).

fof(bg_dist_tm_encryption_tm_deterministic_pseudonymisation, axiom,
    tm_encryption != tm_deterministic_pseudonymisation).

fof(bg_dist_tm_encryption_tm_differential_privacy, axiom,
    tm_encryption != tm_differential_privacy).

fof(bg_dist_tm_encryption_tm_digital_rights_management, axiom,
    tm_encryption != tm_digital_rights_management).

fof(bg_dist_tm_encryption_tm_digital_signatures, axiom,
    tm_encryption != tm_digital_signatures).

fof(bg_dist_tm_encryption_tm_distributed_system_security, axiom,
    tm_encryption != tm_distributed_system_security).

fof(bg_dist_tm_encryption_tm_document_randomised_pseudonymisation, axiom,
    tm_encryption != tm_document_randomised_pseudonymisation).

fof(bg_dist_tm_encryption_tm_document_security, axiom,
    tm_encryption != tm_document_security).

fof(bg_dist_tm_encryption_tm_encryption_in_transfer, axiom,
    tm_encryption != tm_encryption_in_transfer).

fof(bg_dist_tm_encryption_tm_encryption_in_use, axiom,
    tm_encryption != tm_encryption_in_use).

fof(bg_dist_tm_encryption_tm_end_to_end_encryption, axiom,
    tm_encryption != tm_end_to_end_encryption).

fof(bg_dist_tm_encryption_tm_fail_safe_protocols, axiom,
    tm_encryption != tm_fail_safe_protocols).

fof(bg_dist_tm_encryption_tm_file_system_security, axiom,
    tm_encryption != tm_file_system_security).

fof(bg_dist_tm_encryption_tm_fully_randomised_pseudonymisation, axiom,
    tm_encryption != tm_fully_randomised_pseudonymisation).

fof(bg_dist_tm_encryption_tm_hardware_security_protocols, axiom,
    tm_encryption != tm_hardware_security_protocols).

fof(bg_dist_tm_encryption_tm_hash_functions, axiom,
    tm_encryption != tm_hash_functions).

fof(bg_dist_tm_encryption_tm_hash_message_authentication_code, axiom,
    tm_encryption != tm_hash_message_authentication_code).

fof(bg_dist_tm_encryption_tm_homomorphic_encryption, axiom,
    tm_encryption != tm_homomorphic_encryption).

fof(bg_dist_tm_encryption_tm_information_flow_control, axiom,
    tm_encryption != tm_information_flow_control).

fof(bg_dist_tm_encryption_tm_intrusion_detection_system, axiom,
    tm_encryption != tm_intrusion_detection_system).

fof(bg_dist_tm_encryption_tm_legal_measure, axiom,
    tm_encryption != tm_legal_measure).

fof(bg_dist_tm_encryption_tm_message_authentication_codes, axiom,
    tm_encryption != tm_message_authentication_codes).

fof(bg_dist_tm_encryption_tm_mobile_platform_security, axiom,
    tm_encryption != tm_mobile_platform_security).

fof(bg_dist_tm_encryption_tm_monotonic_counter_pseudonymisation, axiom,
    tm_encryption != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_encryption_tm_multi_factor_authentication, axiom,
    tm_encryption != tm_multi_factor_authentication).

fof(bg_dist_tm_encryption_tm_network_proxy_routing, axiom,
    tm_encryption != tm_network_proxy_routing).

fof(bg_dist_tm_encryption_tm_network_security_protocols, axiom,
    tm_encryption != tm_network_security_protocols).

fof(bg_dist_tm_encryption_tm_operating_system_security, axiom,
    tm_encryption != tm_operating_system_security).

fof(bg_dist_tm_encryption_tm_organisational_measure, axiom,
    tm_encryption != tm_organisational_measure).

fof(bg_dist_tm_encryption_tm_password_authentication, axiom,
    tm_encryption != tm_password_authentication).

fof(bg_dist_tm_encryption_tm_penetration_testing_methods, axiom,
    tm_encryption != tm_penetration_testing_methods).

fof(bg_dist_tm_encryption_tm_physical_measure, axiom,
    tm_encryption != tm_physical_measure).

fof(bg_dist_tm_encryption_tm_post_quantum_cryptography, axiom,
    tm_encryption != tm_post_quantum_cryptography).

fof(bg_dist_tm_encryption_tm_privacy_preserving_protocol, axiom,
    tm_encryption != tm_privacy_preserving_protocol).

fof(bg_dist_tm_encryption_tm_private_information_retrieval, axiom,
    tm_encryption != tm_private_information_retrieval).

fof(bg_dist_tm_encryption_tm_pseudonymisation, axiom,
    tm_encryption != tm_pseudonymisation).

fof(bg_dist_tm_encryption_tm_quantum_cryptography, axiom,
    tm_encryption != tm_quantum_cryptography).

fof(bg_dist_tm_encryption_tm_r_n_g_pseudonymisation, axiom,
    tm_encryption != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_encryption_tm_secret_sharing_schemes, axiom,
    tm_encryption != tm_secret_sharing_schemes).

fof(bg_dist_tm_encryption_tm_secure_multi_party_computation, axiom,
    tm_encryption != tm_secure_multi_party_computation).

fof(bg_dist_tm_encryption_tm_security_method, axiom,
    tm_encryption != tm_security_method).

fof(bg_dist_tm_encryption_tm_single_sign_on, axiom,
    tm_encryption != tm_single_sign_on).

fof(bg_dist_tm_encryption_tm_symmetric_cryptography, axiom,
    tm_encryption != tm_symmetric_cryptography).

fof(bg_dist_tm_encryption_tm_symmetric_encryption, axiom,
    tm_encryption != tm_symmetric_encryption).

fof(bg_dist_tm_encryption_tm_technical_measure, axiom,
    tm_encryption != tm_technical_measure).

fof(bg_dist_tm_encryption_tm_technical_organisational_measure, axiom,
    tm_encryption != tm_technical_organisational_measure).

fof(bg_dist_tm_encryption_tm_trusted_computing, axiom,
    tm_encryption != tm_trusted_computing).

fof(bg_dist_tm_encryption_tm_trusted_execution_environment, axiom,
    tm_encryption != tm_trusted_execution_environment).

fof(bg_dist_tm_encryption_tm_usage_control, axiom,
    tm_encryption != tm_usage_control).

fof(bg_dist_tm_encryption_tm_use_synthetic_data, axiom,
    tm_encryption != tm_use_synthetic_data).

fof(bg_dist_tm_encryption_tm_virtualisation_security, axiom,
    tm_encryption != tm_virtualisation_security).

fof(bg_dist_tm_encryption_tm_vulnerability_testing_methods, axiom,
    tm_encryption != tm_vulnerability_testing_methods).

fof(bg_dist_tm_encryption_tm_web_browser_security, axiom,
    tm_encryption != tm_web_browser_security).

fof(bg_dist_tm_encryption_tm_web_security_protocols, axiom,
    tm_encryption != tm_web_security_protocols).

fof(bg_dist_tm_encryption_tm_wireless_security_protocols, axiom,
    tm_encryption != tm_wireless_security_protocols).

fof(bg_dist_tm_encryption_tm_zero_knowledge_authentication, axiom,
    tm_encryption != tm_zero_knowledge_authentication).

fof(bg_dist_tm_access_control_method_tm_encryption_at_rest, axiom,
    tm_access_control_method != tm_encryption_at_rest).

fof(bg_dist_tm_access_control_method_tm_activity_monitoring, axiom,
    tm_access_control_method != tm_activity_monitoring).

fof(bg_dist_tm_access_control_method_tm_anonymisation, axiom,
    tm_access_control_method != tm_anonymisation).

fof(bg_dist_tm_access_control_method_tm_asymmetric_cryptography, axiom,
    tm_access_control_method != tm_asymmetric_cryptography).

fof(bg_dist_tm_access_control_method_tm_asymmetric_encryption, axiom,
    tm_access_control_method != tm_asymmetric_encryption).

fof(bg_dist_tm_access_control_method_tm_authentication_a_b_c, axiom,
    tm_access_control_method != tm_authentication_a_b_c).

fof(bg_dist_tm_access_control_method_tm_authentication_p_a_b_c, axiom,
    tm_access_control_method != tm_authentication_p_a_b_c).

fof(bg_dist_tm_access_control_method_tm_authentication_protocols, axiom,
    tm_access_control_method != tm_authentication_protocols).

fof(bg_dist_tm_access_control_method_tm_authorisation_protocols, axiom,
    tm_access_control_method != tm_authorisation_protocols).

fof(bg_dist_tm_access_control_method_tm_biometric_authentication, axiom,
    tm_access_control_method != tm_biometric_authentication).

fof(bg_dist_tm_access_control_method_tm_cryptographic_authentication, axiom,
    tm_access_control_method != tm_cryptographic_authentication).

fof(bg_dist_tm_access_control_method_tm_cryptographic_key_management, axiom,
    tm_access_control_method != tm_cryptographic_key_management).

fof(bg_dist_tm_access_control_method_tm_cryptographic_methods, axiom,
    tm_access_control_method != tm_cryptographic_methods).

fof(bg_dist_tm_access_control_method_tm_data_backup_protocols, axiom,
    tm_access_control_method != tm_data_backup_protocols).

fof(bg_dist_tm_access_control_method_tm_data_redaction, axiom,
    tm_access_control_method != tm_data_redaction).

fof(bg_dist_tm_access_control_method_tm_data_sanitisation_technique, axiom,
    tm_access_control_method != tm_data_sanitisation_technique).

fof(bg_dist_tm_access_control_method_tm_deidentification, axiom,
    tm_access_control_method != tm_deidentification).

fof(bg_dist_tm_access_control_method_tm_deterministic_pseudonymisation, axiom,
    tm_access_control_method != tm_deterministic_pseudonymisation).

fof(bg_dist_tm_access_control_method_tm_differential_privacy, axiom,
    tm_access_control_method != tm_differential_privacy).

fof(bg_dist_tm_access_control_method_tm_digital_rights_management, axiom,
    tm_access_control_method != tm_digital_rights_management).

fof(bg_dist_tm_access_control_method_tm_digital_signatures, axiom,
    tm_access_control_method != tm_digital_signatures).

fof(bg_dist_tm_access_control_method_tm_distributed_system_security, axiom,
    tm_access_control_method != tm_distributed_system_security).

fof(bg_dist_tm_access_control_method_tm_document_randomised_pseudonymisation, axiom,
    tm_access_control_method != tm_document_randomised_pseudonymisation).

fof(bg_dist_tm_access_control_method_tm_document_security, axiom,
    tm_access_control_method != tm_document_security).

fof(bg_dist_tm_access_control_method_tm_encryption_in_transfer, axiom,
    tm_access_control_method != tm_encryption_in_transfer).

fof(bg_dist_tm_access_control_method_tm_encryption_in_use, axiom,
    tm_access_control_method != tm_encryption_in_use).

fof(bg_dist_tm_access_control_method_tm_end_to_end_encryption, axiom,
    tm_access_control_method != tm_end_to_end_encryption).

fof(bg_dist_tm_access_control_method_tm_fail_safe_protocols, axiom,
    tm_access_control_method != tm_fail_safe_protocols).

fof(bg_dist_tm_access_control_method_tm_file_system_security, axiom,
    tm_access_control_method != tm_file_system_security).

fof(bg_dist_tm_access_control_method_tm_fully_randomised_pseudonymisation, axiom,
    tm_access_control_method != tm_fully_randomised_pseudonymisation).

fof(bg_dist_tm_access_control_method_tm_hardware_security_protocols, axiom,
    tm_access_control_method != tm_hardware_security_protocols).

fof(bg_dist_tm_access_control_method_tm_hash_functions, axiom,
    tm_access_control_method != tm_hash_functions).

fof(bg_dist_tm_access_control_method_tm_hash_message_authentication_code, axiom,
    tm_access_control_method != tm_hash_message_authentication_code).

fof(bg_dist_tm_access_control_method_tm_homomorphic_encryption, axiom,
    tm_access_control_method != tm_homomorphic_encryption).

fof(bg_dist_tm_access_control_method_tm_information_flow_control, axiom,
    tm_access_control_method != tm_information_flow_control).

fof(bg_dist_tm_access_control_method_tm_intrusion_detection_system, axiom,
    tm_access_control_method != tm_intrusion_detection_system).

fof(bg_dist_tm_access_control_method_tm_legal_measure, axiom,
    tm_access_control_method != tm_legal_measure).

fof(bg_dist_tm_access_control_method_tm_message_authentication_codes, axiom,
    tm_access_control_method != tm_message_authentication_codes).

fof(bg_dist_tm_access_control_method_tm_mobile_platform_security, axiom,
    tm_access_control_method != tm_mobile_platform_security).

fof(bg_dist_tm_access_control_method_tm_monotonic_counter_pseudonymisation, axiom,
    tm_access_control_method != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_access_control_method_tm_multi_factor_authentication, axiom,
    tm_access_control_method != tm_multi_factor_authentication).

fof(bg_dist_tm_access_control_method_tm_network_proxy_routing, axiom,
    tm_access_control_method != tm_network_proxy_routing).

fof(bg_dist_tm_access_control_method_tm_network_security_protocols, axiom,
    tm_access_control_method != tm_network_security_protocols).

fof(bg_dist_tm_access_control_method_tm_operating_system_security, axiom,
    tm_access_control_method != tm_operating_system_security).

fof(bg_dist_tm_access_control_method_tm_organisational_measure, axiom,
    tm_access_control_method != tm_organisational_measure).

fof(bg_dist_tm_access_control_method_tm_password_authentication, axiom,
    tm_access_control_method != tm_password_authentication).

fof(bg_dist_tm_access_control_method_tm_penetration_testing_methods, axiom,
    tm_access_control_method != tm_penetration_testing_methods).

fof(bg_dist_tm_access_control_method_tm_physical_measure, axiom,
    tm_access_control_method != tm_physical_measure).

fof(bg_dist_tm_access_control_method_tm_post_quantum_cryptography, axiom,
    tm_access_control_method != tm_post_quantum_cryptography).

fof(bg_dist_tm_access_control_method_tm_privacy_preserving_protocol, axiom,
    tm_access_control_method != tm_privacy_preserving_protocol).

fof(bg_dist_tm_access_control_method_tm_private_information_retrieval, axiom,
    tm_access_control_method != tm_private_information_retrieval).

fof(bg_dist_tm_access_control_method_tm_pseudonymisation, axiom,
    tm_access_control_method != tm_pseudonymisation).

fof(bg_dist_tm_access_control_method_tm_quantum_cryptography, axiom,
    tm_access_control_method != tm_quantum_cryptography).

fof(bg_dist_tm_access_control_method_tm_r_n_g_pseudonymisation, axiom,
    tm_access_control_method != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_access_control_method_tm_secret_sharing_schemes, axiom,
    tm_access_control_method != tm_secret_sharing_schemes).

fof(bg_dist_tm_access_control_method_tm_secure_multi_party_computation, axiom,
    tm_access_control_method != tm_secure_multi_party_computation).

fof(bg_dist_tm_access_control_method_tm_security_method, axiom,
    tm_access_control_method != tm_security_method).

fof(bg_dist_tm_access_control_method_tm_single_sign_on, axiom,
    tm_access_control_method != tm_single_sign_on).

fof(bg_dist_tm_access_control_method_tm_symmetric_cryptography, axiom,
    tm_access_control_method != tm_symmetric_cryptography).

fof(bg_dist_tm_access_control_method_tm_symmetric_encryption, axiom,
    tm_access_control_method != tm_symmetric_encryption).

fof(bg_dist_tm_access_control_method_tm_technical_measure, axiom,
    tm_access_control_method != tm_technical_measure).

fof(bg_dist_tm_access_control_method_tm_technical_organisational_measure, axiom,
    tm_access_control_method != tm_technical_organisational_measure).

fof(bg_dist_tm_access_control_method_tm_trusted_computing, axiom,
    tm_access_control_method != tm_trusted_computing).

fof(bg_dist_tm_access_control_method_tm_trusted_execution_environment, axiom,
    tm_access_control_method != tm_trusted_execution_environment).

fof(bg_dist_tm_access_control_method_tm_usage_control, axiom,
    tm_access_control_method != tm_usage_control).

fof(bg_dist_tm_access_control_method_tm_use_synthetic_data, axiom,
    tm_access_control_method != tm_use_synthetic_data).

fof(bg_dist_tm_access_control_method_tm_virtualisation_security, axiom,
    tm_access_control_method != tm_virtualisation_security).

fof(bg_dist_tm_access_control_method_tm_vulnerability_testing_methods, axiom,
    tm_access_control_method != tm_vulnerability_testing_methods).

fof(bg_dist_tm_access_control_method_tm_web_browser_security, axiom,
    tm_access_control_method != tm_web_browser_security).

fof(bg_dist_tm_access_control_method_tm_web_security_protocols, axiom,
    tm_access_control_method != tm_web_security_protocols).

fof(bg_dist_tm_access_control_method_tm_wireless_security_protocols, axiom,
    tm_access_control_method != tm_wireless_security_protocols).

fof(bg_dist_tm_access_control_method_tm_zero_knowledge_authentication, axiom,
    tm_access_control_method != tm_zero_knowledge_authentication).

fof(bg_dist_tm_encryption_at_rest_tm_activity_monitoring, axiom,
    tm_encryption_at_rest != tm_activity_monitoring).

fof(bg_dist_tm_encryption_at_rest_tm_anonymisation, axiom,
    tm_encryption_at_rest != tm_anonymisation).

fof(bg_dist_tm_encryption_at_rest_tm_asymmetric_cryptography, axiom,
    tm_encryption_at_rest != tm_asymmetric_cryptography).

fof(bg_dist_tm_encryption_at_rest_tm_asymmetric_encryption, axiom,
    tm_encryption_at_rest != tm_asymmetric_encryption).

fof(bg_dist_tm_encryption_at_rest_tm_authentication_a_b_c, axiom,
    tm_encryption_at_rest != tm_authentication_a_b_c).

fof(bg_dist_tm_encryption_at_rest_tm_authentication_p_a_b_c, axiom,
    tm_encryption_at_rest != tm_authentication_p_a_b_c).

fof(bg_dist_tm_encryption_at_rest_tm_authentication_protocols, axiom,
    tm_encryption_at_rest != tm_authentication_protocols).

fof(bg_dist_tm_encryption_at_rest_tm_authorisation_protocols, axiom,
    tm_encryption_at_rest != tm_authorisation_protocols).

fof(bg_dist_tm_encryption_at_rest_tm_biometric_authentication, axiom,
    tm_encryption_at_rest != tm_biometric_authentication).

fof(bg_dist_tm_encryption_at_rest_tm_cryptographic_authentication, axiom,
    tm_encryption_at_rest != tm_cryptographic_authentication).

fof(bg_dist_tm_encryption_at_rest_tm_cryptographic_key_management, axiom,
    tm_encryption_at_rest != tm_cryptographic_key_management).

fof(bg_dist_tm_encryption_at_rest_tm_cryptographic_methods, axiom,
    tm_encryption_at_rest != tm_cryptographic_methods).

fof(bg_dist_tm_encryption_at_rest_tm_data_backup_protocols, axiom,
    tm_encryption_at_rest != tm_data_backup_protocols).

fof(bg_dist_tm_encryption_at_rest_tm_data_redaction, axiom,
    tm_encryption_at_rest != tm_data_redaction).

fof(bg_dist_tm_encryption_at_rest_tm_data_sanitisation_technique, axiom,
    tm_encryption_at_rest != tm_data_sanitisation_technique).

fof(bg_dist_tm_encryption_at_rest_tm_deidentification, axiom,
    tm_encryption_at_rest != tm_deidentification).

fof(bg_dist_tm_encryption_at_rest_tm_deterministic_pseudonymisation, axiom,
    tm_encryption_at_rest != tm_deterministic_pseudonymisation).

fof(bg_dist_tm_encryption_at_rest_tm_differential_privacy, axiom,
    tm_encryption_at_rest != tm_differential_privacy).

fof(bg_dist_tm_encryption_at_rest_tm_digital_rights_management, axiom,
    tm_encryption_at_rest != tm_digital_rights_management).

fof(bg_dist_tm_encryption_at_rest_tm_digital_signatures, axiom,
    tm_encryption_at_rest != tm_digital_signatures).

fof(bg_dist_tm_encryption_at_rest_tm_distributed_system_security, axiom,
    tm_encryption_at_rest != tm_distributed_system_security).

fof(bg_dist_tm_encryption_at_rest_tm_document_randomised_pseudonymisation, axiom,
    tm_encryption_at_rest != tm_document_randomised_pseudonymisation).

fof(bg_dist_tm_encryption_at_rest_tm_document_security, axiom,
    tm_encryption_at_rest != tm_document_security).

fof(bg_dist_tm_encryption_at_rest_tm_encryption_in_transfer, axiom,
    tm_encryption_at_rest != tm_encryption_in_transfer).

fof(bg_dist_tm_encryption_at_rest_tm_encryption_in_use, axiom,
    tm_encryption_at_rest != tm_encryption_in_use).

fof(bg_dist_tm_encryption_at_rest_tm_end_to_end_encryption, axiom,
    tm_encryption_at_rest != tm_end_to_end_encryption).

fof(bg_dist_tm_encryption_at_rest_tm_fail_safe_protocols, axiom,
    tm_encryption_at_rest != tm_fail_safe_protocols).

fof(bg_dist_tm_encryption_at_rest_tm_file_system_security, axiom,
    tm_encryption_at_rest != tm_file_system_security).

fof(bg_dist_tm_encryption_at_rest_tm_fully_randomised_pseudonymisation, axiom,
    tm_encryption_at_rest != tm_fully_randomised_pseudonymisation).

fof(bg_dist_tm_encryption_at_rest_tm_hardware_security_protocols, axiom,
    tm_encryption_at_rest != tm_hardware_security_protocols).

fof(bg_dist_tm_encryption_at_rest_tm_hash_functions, axiom,
    tm_encryption_at_rest != tm_hash_functions).

fof(bg_dist_tm_encryption_at_rest_tm_hash_message_authentication_code, axiom,
    tm_encryption_at_rest != tm_hash_message_authentication_code).

fof(bg_dist_tm_encryption_at_rest_tm_homomorphic_encryption, axiom,
    tm_encryption_at_rest != tm_homomorphic_encryption).

fof(bg_dist_tm_encryption_at_rest_tm_information_flow_control, axiom,
    tm_encryption_at_rest != tm_information_flow_control).

fof(bg_dist_tm_encryption_at_rest_tm_intrusion_detection_system, axiom,
    tm_encryption_at_rest != tm_intrusion_detection_system).

fof(bg_dist_tm_encryption_at_rest_tm_legal_measure, axiom,
    tm_encryption_at_rest != tm_legal_measure).

fof(bg_dist_tm_encryption_at_rest_tm_message_authentication_codes, axiom,
    tm_encryption_at_rest != tm_message_authentication_codes).

fof(bg_dist_tm_encryption_at_rest_tm_mobile_platform_security, axiom,
    tm_encryption_at_rest != tm_mobile_platform_security).

fof(bg_dist_tm_encryption_at_rest_tm_monotonic_counter_pseudonymisation, axiom,
    tm_encryption_at_rest != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_encryption_at_rest_tm_multi_factor_authentication, axiom,
    tm_encryption_at_rest != tm_multi_factor_authentication).

fof(bg_dist_tm_encryption_at_rest_tm_network_proxy_routing, axiom,
    tm_encryption_at_rest != tm_network_proxy_routing).

fof(bg_dist_tm_encryption_at_rest_tm_network_security_protocols, axiom,
    tm_encryption_at_rest != tm_network_security_protocols).

fof(bg_dist_tm_encryption_at_rest_tm_operating_system_security, axiom,
    tm_encryption_at_rest != tm_operating_system_security).

fof(bg_dist_tm_encryption_at_rest_tm_organisational_measure, axiom,
    tm_encryption_at_rest != tm_organisational_measure).

fof(bg_dist_tm_encryption_at_rest_tm_password_authentication, axiom,
    tm_encryption_at_rest != tm_password_authentication).

fof(bg_dist_tm_encryption_at_rest_tm_penetration_testing_methods, axiom,
    tm_encryption_at_rest != tm_penetration_testing_methods).

fof(bg_dist_tm_encryption_at_rest_tm_physical_measure, axiom,
    tm_encryption_at_rest != tm_physical_measure).

fof(bg_dist_tm_encryption_at_rest_tm_post_quantum_cryptography, axiom,
    tm_encryption_at_rest != tm_post_quantum_cryptography).

fof(bg_dist_tm_encryption_at_rest_tm_privacy_preserving_protocol, axiom,
    tm_encryption_at_rest != tm_privacy_preserving_protocol).

fof(bg_dist_tm_encryption_at_rest_tm_private_information_retrieval, axiom,
    tm_encryption_at_rest != tm_private_information_retrieval).

fof(bg_dist_tm_encryption_at_rest_tm_pseudonymisation, axiom,
    tm_encryption_at_rest != tm_pseudonymisation).

fof(bg_dist_tm_encryption_at_rest_tm_quantum_cryptography, axiom,
    tm_encryption_at_rest != tm_quantum_cryptography).

fof(bg_dist_tm_encryption_at_rest_tm_r_n_g_pseudonymisation, axiom,
    tm_encryption_at_rest != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_encryption_at_rest_tm_secret_sharing_schemes, axiom,
    tm_encryption_at_rest != tm_secret_sharing_schemes).

fof(bg_dist_tm_encryption_at_rest_tm_secure_multi_party_computation, axiom,
    tm_encryption_at_rest != tm_secure_multi_party_computation).

fof(bg_dist_tm_encryption_at_rest_tm_security_method, axiom,
    tm_encryption_at_rest != tm_security_method).

fof(bg_dist_tm_encryption_at_rest_tm_single_sign_on, axiom,
    tm_encryption_at_rest != tm_single_sign_on).

fof(bg_dist_tm_encryption_at_rest_tm_symmetric_cryptography, axiom,
    tm_encryption_at_rest != tm_symmetric_cryptography).

fof(bg_dist_tm_encryption_at_rest_tm_symmetric_encryption, axiom,
    tm_encryption_at_rest != tm_symmetric_encryption).

fof(bg_dist_tm_encryption_at_rest_tm_technical_measure, axiom,
    tm_encryption_at_rest != tm_technical_measure).

fof(bg_dist_tm_encryption_at_rest_tm_technical_organisational_measure, axiom,
    tm_encryption_at_rest != tm_technical_organisational_measure).

fof(bg_dist_tm_encryption_at_rest_tm_trusted_computing, axiom,
    tm_encryption_at_rest != tm_trusted_computing).

fof(bg_dist_tm_encryption_at_rest_tm_trusted_execution_environment, axiom,
    tm_encryption_at_rest != tm_trusted_execution_environment).

fof(bg_dist_tm_encryption_at_rest_tm_usage_control, axiom,
    tm_encryption_at_rest != tm_usage_control).

fof(bg_dist_tm_encryption_at_rest_tm_use_synthetic_data, axiom,
    tm_encryption_at_rest != tm_use_synthetic_data).

fof(bg_dist_tm_encryption_at_rest_tm_virtualisation_security, axiom,
    tm_encryption_at_rest != tm_virtualisation_security).

fof(bg_dist_tm_encryption_at_rest_tm_vulnerability_testing_methods, axiom,
    tm_encryption_at_rest != tm_vulnerability_testing_methods).

fof(bg_dist_tm_encryption_at_rest_tm_web_browser_security, axiom,
    tm_encryption_at_rest != tm_web_browser_security).

fof(bg_dist_tm_encryption_at_rest_tm_web_security_protocols, axiom,
    tm_encryption_at_rest != tm_web_security_protocols).

fof(bg_dist_tm_encryption_at_rest_tm_wireless_security_protocols, axiom,
    tm_encryption_at_rest != tm_wireless_security_protocols).

fof(bg_dist_tm_encryption_at_rest_tm_zero_knowledge_authentication, axiom,
    tm_encryption_at_rest != tm_zero_knowledge_authentication).

fof(bg_dist_tm_activity_monitoring_tm_anonymisation, axiom,
    tm_activity_monitoring != tm_anonymisation).

fof(bg_dist_tm_activity_monitoring_tm_asymmetric_cryptography, axiom,
    tm_activity_monitoring != tm_asymmetric_cryptography).

fof(bg_dist_tm_activity_monitoring_tm_asymmetric_encryption, axiom,
    tm_activity_monitoring != tm_asymmetric_encryption).

fof(bg_dist_tm_activity_monitoring_tm_authentication_a_b_c, axiom,
    tm_activity_monitoring != tm_authentication_a_b_c).

fof(bg_dist_tm_activity_monitoring_tm_authentication_p_a_b_c, axiom,
    tm_activity_monitoring != tm_authentication_p_a_b_c).

fof(bg_dist_tm_activity_monitoring_tm_authentication_protocols, axiom,
    tm_activity_monitoring != tm_authentication_protocols).

fof(bg_dist_tm_activity_monitoring_tm_authorisation_protocols, axiom,
    tm_activity_monitoring != tm_authorisation_protocols).

fof(bg_dist_tm_activity_monitoring_tm_biometric_authentication, axiom,
    tm_activity_monitoring != tm_biometric_authentication).

fof(bg_dist_tm_activity_monitoring_tm_cryptographic_authentication, axiom,
    tm_activity_monitoring != tm_cryptographic_authentication).

fof(bg_dist_tm_activity_monitoring_tm_cryptographic_key_management, axiom,
    tm_activity_monitoring != tm_cryptographic_key_management).

fof(bg_dist_tm_activity_monitoring_tm_cryptographic_methods, axiom,
    tm_activity_monitoring != tm_cryptographic_methods).

fof(bg_dist_tm_activity_monitoring_tm_data_backup_protocols, axiom,
    tm_activity_monitoring != tm_data_backup_protocols).

fof(bg_dist_tm_activity_monitoring_tm_data_redaction, axiom,
    tm_activity_monitoring != tm_data_redaction).

fof(bg_dist_tm_activity_monitoring_tm_data_sanitisation_technique, axiom,
    tm_activity_monitoring != tm_data_sanitisation_technique).

fof(bg_dist_tm_activity_monitoring_tm_deidentification, axiom,
    tm_activity_monitoring != tm_deidentification).

fof(bg_dist_tm_activity_monitoring_tm_deterministic_pseudonymisation, axiom,
    tm_activity_monitoring != tm_deterministic_pseudonymisation).

fof(bg_dist_tm_activity_monitoring_tm_differential_privacy, axiom,
    tm_activity_monitoring != tm_differential_privacy).

fof(bg_dist_tm_activity_monitoring_tm_digital_rights_management, axiom,
    tm_activity_monitoring != tm_digital_rights_management).

fof(bg_dist_tm_activity_monitoring_tm_digital_signatures, axiom,
    tm_activity_monitoring != tm_digital_signatures).

fof(bg_dist_tm_activity_monitoring_tm_distributed_system_security, axiom,
    tm_activity_monitoring != tm_distributed_system_security).

fof(bg_dist_tm_activity_monitoring_tm_document_randomised_pseudonymisation, axiom,
    tm_activity_monitoring != tm_document_randomised_pseudonymisation).

fof(bg_dist_tm_activity_monitoring_tm_document_security, axiom,
    tm_activity_monitoring != tm_document_security).

fof(bg_dist_tm_activity_monitoring_tm_encryption_in_transfer, axiom,
    tm_activity_monitoring != tm_encryption_in_transfer).

fof(bg_dist_tm_activity_monitoring_tm_encryption_in_use, axiom,
    tm_activity_monitoring != tm_encryption_in_use).

fof(bg_dist_tm_activity_monitoring_tm_end_to_end_encryption, axiom,
    tm_activity_monitoring != tm_end_to_end_encryption).

fof(bg_dist_tm_activity_monitoring_tm_fail_safe_protocols, axiom,
    tm_activity_monitoring != tm_fail_safe_protocols).

fof(bg_dist_tm_activity_monitoring_tm_file_system_security, axiom,
    tm_activity_monitoring != tm_file_system_security).

fof(bg_dist_tm_activity_monitoring_tm_fully_randomised_pseudonymisation, axiom,
    tm_activity_monitoring != tm_fully_randomised_pseudonymisation).

fof(bg_dist_tm_activity_monitoring_tm_hardware_security_protocols, axiom,
    tm_activity_monitoring != tm_hardware_security_protocols).

fof(bg_dist_tm_activity_monitoring_tm_hash_functions, axiom,
    tm_activity_monitoring != tm_hash_functions).

fof(bg_dist_tm_activity_monitoring_tm_hash_message_authentication_code, axiom,
    tm_activity_monitoring != tm_hash_message_authentication_code).

fof(bg_dist_tm_activity_monitoring_tm_homomorphic_encryption, axiom,
    tm_activity_monitoring != tm_homomorphic_encryption).

fof(bg_dist_tm_activity_monitoring_tm_information_flow_control, axiom,
    tm_activity_monitoring != tm_information_flow_control).

fof(bg_dist_tm_activity_monitoring_tm_intrusion_detection_system, axiom,
    tm_activity_monitoring != tm_intrusion_detection_system).

fof(bg_dist_tm_activity_monitoring_tm_legal_measure, axiom,
    tm_activity_monitoring != tm_legal_measure).

fof(bg_dist_tm_activity_monitoring_tm_message_authentication_codes, axiom,
    tm_activity_monitoring != tm_message_authentication_codes).

fof(bg_dist_tm_activity_monitoring_tm_mobile_platform_security, axiom,
    tm_activity_monitoring != tm_mobile_platform_security).

fof(bg_dist_tm_activity_monitoring_tm_monotonic_counter_pseudonymisation, axiom,
    tm_activity_monitoring != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_activity_monitoring_tm_multi_factor_authentication, axiom,
    tm_activity_monitoring != tm_multi_factor_authentication).

fof(bg_dist_tm_activity_monitoring_tm_network_proxy_routing, axiom,
    tm_activity_monitoring != tm_network_proxy_routing).

fof(bg_dist_tm_activity_monitoring_tm_network_security_protocols, axiom,
    tm_activity_monitoring != tm_network_security_protocols).

fof(bg_dist_tm_activity_monitoring_tm_operating_system_security, axiom,
    tm_activity_monitoring != tm_operating_system_security).

fof(bg_dist_tm_activity_monitoring_tm_organisational_measure, axiom,
    tm_activity_monitoring != tm_organisational_measure).

fof(bg_dist_tm_activity_monitoring_tm_password_authentication, axiom,
    tm_activity_monitoring != tm_password_authentication).

fof(bg_dist_tm_activity_monitoring_tm_penetration_testing_methods, axiom,
    tm_activity_monitoring != tm_penetration_testing_methods).

fof(bg_dist_tm_activity_monitoring_tm_physical_measure, axiom,
    tm_activity_monitoring != tm_physical_measure).

fof(bg_dist_tm_activity_monitoring_tm_post_quantum_cryptography, axiom,
    tm_activity_monitoring != tm_post_quantum_cryptography).

fof(bg_dist_tm_activity_monitoring_tm_privacy_preserving_protocol, axiom,
    tm_activity_monitoring != tm_privacy_preserving_protocol).

fof(bg_dist_tm_activity_monitoring_tm_private_information_retrieval, axiom,
    tm_activity_monitoring != tm_private_information_retrieval).

fof(bg_dist_tm_activity_monitoring_tm_pseudonymisation, axiom,
    tm_activity_monitoring != tm_pseudonymisation).

fof(bg_dist_tm_activity_monitoring_tm_quantum_cryptography, axiom,
    tm_activity_monitoring != tm_quantum_cryptography).

fof(bg_dist_tm_activity_monitoring_tm_r_n_g_pseudonymisation, axiom,
    tm_activity_monitoring != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_activity_monitoring_tm_secret_sharing_schemes, axiom,
    tm_activity_monitoring != tm_secret_sharing_schemes).

fof(bg_dist_tm_activity_monitoring_tm_secure_multi_party_computation, axiom,
    tm_activity_monitoring != tm_secure_multi_party_computation).

fof(bg_dist_tm_activity_monitoring_tm_security_method, axiom,
    tm_activity_monitoring != tm_security_method).

fof(bg_dist_tm_activity_monitoring_tm_single_sign_on, axiom,
    tm_activity_monitoring != tm_single_sign_on).

fof(bg_dist_tm_activity_monitoring_tm_symmetric_cryptography, axiom,
    tm_activity_monitoring != tm_symmetric_cryptography).

fof(bg_dist_tm_activity_monitoring_tm_symmetric_encryption, axiom,
    tm_activity_monitoring != tm_symmetric_encryption).

fof(bg_dist_tm_activity_monitoring_tm_technical_measure, axiom,
    tm_activity_monitoring != tm_technical_measure).

fof(bg_dist_tm_activity_monitoring_tm_technical_organisational_measure, axiom,
    tm_activity_monitoring != tm_technical_organisational_measure).

fof(bg_dist_tm_activity_monitoring_tm_trusted_computing, axiom,
    tm_activity_monitoring != tm_trusted_computing).

fof(bg_dist_tm_activity_monitoring_tm_trusted_execution_environment, axiom,
    tm_activity_monitoring != tm_trusted_execution_environment).

fof(bg_dist_tm_activity_monitoring_tm_usage_control, axiom,
    tm_activity_monitoring != tm_usage_control).

fof(bg_dist_tm_activity_monitoring_tm_use_synthetic_data, axiom,
    tm_activity_monitoring != tm_use_synthetic_data).

fof(bg_dist_tm_activity_monitoring_tm_virtualisation_security, axiom,
    tm_activity_monitoring != tm_virtualisation_security).

fof(bg_dist_tm_activity_monitoring_tm_vulnerability_testing_methods, axiom,
    tm_activity_monitoring != tm_vulnerability_testing_methods).

fof(bg_dist_tm_activity_monitoring_tm_web_browser_security, axiom,
    tm_activity_monitoring != tm_web_browser_security).

fof(bg_dist_tm_activity_monitoring_tm_web_security_protocols, axiom,
    tm_activity_monitoring != tm_web_security_protocols).

fof(bg_dist_tm_activity_monitoring_tm_wireless_security_protocols, axiom,
    tm_activity_monitoring != tm_wireless_security_protocols).

fof(bg_dist_tm_activity_monitoring_tm_zero_knowledge_authentication, axiom,
    tm_activity_monitoring != tm_zero_knowledge_authentication).

fof(bg_dist_tm_anonymisation_tm_asymmetric_cryptography, axiom,
    tm_anonymisation != tm_asymmetric_cryptography).

fof(bg_dist_tm_anonymisation_tm_asymmetric_encryption, axiom,
    tm_anonymisation != tm_asymmetric_encryption).

fof(bg_dist_tm_anonymisation_tm_authentication_a_b_c, axiom,
    tm_anonymisation != tm_authentication_a_b_c).

fof(bg_dist_tm_anonymisation_tm_authentication_p_a_b_c, axiom,
    tm_anonymisation != tm_authentication_p_a_b_c).

fof(bg_dist_tm_anonymisation_tm_authentication_protocols, axiom,
    tm_anonymisation != tm_authentication_protocols).

fof(bg_dist_tm_anonymisation_tm_authorisation_protocols, axiom,
    tm_anonymisation != tm_authorisation_protocols).

fof(bg_dist_tm_anonymisation_tm_biometric_authentication, axiom,
    tm_anonymisation != tm_biometric_authentication).

fof(bg_dist_tm_anonymisation_tm_cryptographic_authentication, axiom,
    tm_anonymisation != tm_cryptographic_authentication).

fof(bg_dist_tm_anonymisation_tm_cryptographic_key_management, axiom,
    tm_anonymisation != tm_cryptographic_key_management).

fof(bg_dist_tm_anonymisation_tm_cryptographic_methods, axiom,
    tm_anonymisation != tm_cryptographic_methods).

fof(bg_dist_tm_anonymisation_tm_data_backup_protocols, axiom,
    tm_anonymisation != tm_data_backup_protocols).

fof(bg_dist_tm_anonymisation_tm_data_redaction, axiom,
    tm_anonymisation != tm_data_redaction).

fof(bg_dist_tm_anonymisation_tm_data_sanitisation_technique, axiom,
    tm_anonymisation != tm_data_sanitisation_technique).

fof(bg_dist_tm_anonymisation_tm_deidentification, axiom,
    tm_anonymisation != tm_deidentification).

fof(bg_dist_tm_anonymisation_tm_deterministic_pseudonymisation, axiom,
    tm_anonymisation != tm_deterministic_pseudonymisation).

fof(bg_dist_tm_anonymisation_tm_differential_privacy, axiom,
    tm_anonymisation != tm_differential_privacy).

fof(bg_dist_tm_anonymisation_tm_digital_rights_management, axiom,
    tm_anonymisation != tm_digital_rights_management).

fof(bg_dist_tm_anonymisation_tm_digital_signatures, axiom,
    tm_anonymisation != tm_digital_signatures).

fof(bg_dist_tm_anonymisation_tm_distributed_system_security, axiom,
    tm_anonymisation != tm_distributed_system_security).

fof(bg_dist_tm_anonymisation_tm_document_randomised_pseudonymisation, axiom,
    tm_anonymisation != tm_document_randomised_pseudonymisation).

fof(bg_dist_tm_anonymisation_tm_document_security, axiom,
    tm_anonymisation != tm_document_security).

fof(bg_dist_tm_anonymisation_tm_encryption_in_transfer, axiom,
    tm_anonymisation != tm_encryption_in_transfer).

fof(bg_dist_tm_anonymisation_tm_encryption_in_use, axiom,
    tm_anonymisation != tm_encryption_in_use).

fof(bg_dist_tm_anonymisation_tm_end_to_end_encryption, axiom,
    tm_anonymisation != tm_end_to_end_encryption).

fof(bg_dist_tm_anonymisation_tm_fail_safe_protocols, axiom,
    tm_anonymisation != tm_fail_safe_protocols).

fof(bg_dist_tm_anonymisation_tm_file_system_security, axiom,
    tm_anonymisation != tm_file_system_security).

fof(bg_dist_tm_anonymisation_tm_fully_randomised_pseudonymisation, axiom,
    tm_anonymisation != tm_fully_randomised_pseudonymisation).

fof(bg_dist_tm_anonymisation_tm_hardware_security_protocols, axiom,
    tm_anonymisation != tm_hardware_security_protocols).

fof(bg_dist_tm_anonymisation_tm_hash_functions, axiom,
    tm_anonymisation != tm_hash_functions).

fof(bg_dist_tm_anonymisation_tm_hash_message_authentication_code, axiom,
    tm_anonymisation != tm_hash_message_authentication_code).

fof(bg_dist_tm_anonymisation_tm_homomorphic_encryption, axiom,
    tm_anonymisation != tm_homomorphic_encryption).

fof(bg_dist_tm_anonymisation_tm_information_flow_control, axiom,
    tm_anonymisation != tm_information_flow_control).

fof(bg_dist_tm_anonymisation_tm_intrusion_detection_system, axiom,
    tm_anonymisation != tm_intrusion_detection_system).

fof(bg_dist_tm_anonymisation_tm_legal_measure, axiom,
    tm_anonymisation != tm_legal_measure).

fof(bg_dist_tm_anonymisation_tm_message_authentication_codes, axiom,
    tm_anonymisation != tm_message_authentication_codes).

fof(bg_dist_tm_anonymisation_tm_mobile_platform_security, axiom,
    tm_anonymisation != tm_mobile_platform_security).

fof(bg_dist_tm_anonymisation_tm_monotonic_counter_pseudonymisation, axiom,
    tm_anonymisation != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_anonymisation_tm_multi_factor_authentication, axiom,
    tm_anonymisation != tm_multi_factor_authentication).

fof(bg_dist_tm_anonymisation_tm_network_proxy_routing, axiom,
    tm_anonymisation != tm_network_proxy_routing).

fof(bg_dist_tm_anonymisation_tm_network_security_protocols, axiom,
    tm_anonymisation != tm_network_security_protocols).

fof(bg_dist_tm_anonymisation_tm_operating_system_security, axiom,
    tm_anonymisation != tm_operating_system_security).

fof(bg_dist_tm_anonymisation_tm_organisational_measure, axiom,
    tm_anonymisation != tm_organisational_measure).

fof(bg_dist_tm_anonymisation_tm_password_authentication, axiom,
    tm_anonymisation != tm_password_authentication).

fof(bg_dist_tm_anonymisation_tm_penetration_testing_methods, axiom,
    tm_anonymisation != tm_penetration_testing_methods).

fof(bg_dist_tm_anonymisation_tm_physical_measure, axiom,
    tm_anonymisation != tm_physical_measure).

fof(bg_dist_tm_anonymisation_tm_post_quantum_cryptography, axiom,
    tm_anonymisation != tm_post_quantum_cryptography).

fof(bg_dist_tm_anonymisation_tm_privacy_preserving_protocol, axiom,
    tm_anonymisation != tm_privacy_preserving_protocol).

fof(bg_dist_tm_anonymisation_tm_private_information_retrieval, axiom,
    tm_anonymisation != tm_private_information_retrieval).

fof(bg_dist_tm_anonymisation_tm_pseudonymisation, axiom,
    tm_anonymisation != tm_pseudonymisation).

fof(bg_dist_tm_anonymisation_tm_quantum_cryptography, axiom,
    tm_anonymisation != tm_quantum_cryptography).

fof(bg_dist_tm_anonymisation_tm_r_n_g_pseudonymisation, axiom,
    tm_anonymisation != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_anonymisation_tm_secret_sharing_schemes, axiom,
    tm_anonymisation != tm_secret_sharing_schemes).

fof(bg_dist_tm_anonymisation_tm_secure_multi_party_computation, axiom,
    tm_anonymisation != tm_secure_multi_party_computation).

fof(bg_dist_tm_anonymisation_tm_security_method, axiom,
    tm_anonymisation != tm_security_method).

fof(bg_dist_tm_anonymisation_tm_single_sign_on, axiom,
    tm_anonymisation != tm_single_sign_on).

fof(bg_dist_tm_anonymisation_tm_symmetric_cryptography, axiom,
    tm_anonymisation != tm_symmetric_cryptography).

fof(bg_dist_tm_anonymisation_tm_symmetric_encryption, axiom,
    tm_anonymisation != tm_symmetric_encryption).

fof(bg_dist_tm_anonymisation_tm_technical_measure, axiom,
    tm_anonymisation != tm_technical_measure).

fof(bg_dist_tm_anonymisation_tm_technical_organisational_measure, axiom,
    tm_anonymisation != tm_technical_organisational_measure).

fof(bg_dist_tm_anonymisation_tm_trusted_computing, axiom,
    tm_anonymisation != tm_trusted_computing).

fof(bg_dist_tm_anonymisation_tm_trusted_execution_environment, axiom,
    tm_anonymisation != tm_trusted_execution_environment).

fof(bg_dist_tm_anonymisation_tm_usage_control, axiom,
    tm_anonymisation != tm_usage_control).

fof(bg_dist_tm_anonymisation_tm_use_synthetic_data, axiom,
    tm_anonymisation != tm_use_synthetic_data).

fof(bg_dist_tm_anonymisation_tm_virtualisation_security, axiom,
    tm_anonymisation != tm_virtualisation_security).

fof(bg_dist_tm_anonymisation_tm_vulnerability_testing_methods, axiom,
    tm_anonymisation != tm_vulnerability_testing_methods).

fof(bg_dist_tm_anonymisation_tm_web_browser_security, axiom,
    tm_anonymisation != tm_web_browser_security).

fof(bg_dist_tm_anonymisation_tm_web_security_protocols, axiom,
    tm_anonymisation != tm_web_security_protocols).

fof(bg_dist_tm_anonymisation_tm_wireless_security_protocols, axiom,
    tm_anonymisation != tm_wireless_security_protocols).

fof(bg_dist_tm_anonymisation_tm_zero_knowledge_authentication, axiom,
    tm_anonymisation != tm_zero_knowledge_authentication).

fof(bg_dist_tm_asymmetric_cryptography_tm_asymmetric_encryption, axiom,
    tm_asymmetric_cryptography != tm_asymmetric_encryption).

fof(bg_dist_tm_asymmetric_cryptography_tm_authentication_a_b_c, axiom,
    tm_asymmetric_cryptography != tm_authentication_a_b_c).

fof(bg_dist_tm_asymmetric_cryptography_tm_authentication_p_a_b_c, axiom,
    tm_asymmetric_cryptography != tm_authentication_p_a_b_c).

fof(bg_dist_tm_asymmetric_cryptography_tm_authentication_protocols, axiom,
    tm_asymmetric_cryptography != tm_authentication_protocols).

fof(bg_dist_tm_asymmetric_cryptography_tm_authorisation_protocols, axiom,
    tm_asymmetric_cryptography != tm_authorisation_protocols).

fof(bg_dist_tm_asymmetric_cryptography_tm_biometric_authentication, axiom,
    tm_asymmetric_cryptography != tm_biometric_authentication).

fof(bg_dist_tm_asymmetric_cryptography_tm_cryptographic_authentication, axiom,
    tm_asymmetric_cryptography != tm_cryptographic_authentication).

fof(bg_dist_tm_asymmetric_cryptography_tm_cryptographic_key_management, axiom,
    tm_asymmetric_cryptography != tm_cryptographic_key_management).

fof(bg_dist_tm_asymmetric_cryptography_tm_cryptographic_methods, axiom,
    tm_asymmetric_cryptography != tm_cryptographic_methods).

fof(bg_dist_tm_asymmetric_cryptography_tm_data_backup_protocols, axiom,
    tm_asymmetric_cryptography != tm_data_backup_protocols).

fof(bg_dist_tm_asymmetric_cryptography_tm_data_redaction, axiom,
    tm_asymmetric_cryptography != tm_data_redaction).

fof(bg_dist_tm_asymmetric_cryptography_tm_data_sanitisation_technique, axiom,
    tm_asymmetric_cryptography != tm_data_sanitisation_technique).

fof(bg_dist_tm_asymmetric_cryptography_tm_deidentification, axiom,
    tm_asymmetric_cryptography != tm_deidentification).

fof(bg_dist_tm_asymmetric_cryptography_tm_deterministic_pseudonymisation, axiom,
    tm_asymmetric_cryptography != tm_deterministic_pseudonymisation).

fof(bg_dist_tm_asymmetric_cryptography_tm_differential_privacy, axiom,
    tm_asymmetric_cryptography != tm_differential_privacy).

fof(bg_dist_tm_asymmetric_cryptography_tm_digital_rights_management, axiom,
    tm_asymmetric_cryptography != tm_digital_rights_management).

fof(bg_dist_tm_asymmetric_cryptography_tm_digital_signatures, axiom,
    tm_asymmetric_cryptography != tm_digital_signatures).

fof(bg_dist_tm_asymmetric_cryptography_tm_distributed_system_security, axiom,
    tm_asymmetric_cryptography != tm_distributed_system_security).

fof(bg_dist_tm_asymmetric_cryptography_tm_document_randomised_pseudonymisation, axiom,
    tm_asymmetric_cryptography != tm_document_randomised_pseudonymisation).

fof(bg_dist_tm_asymmetric_cryptography_tm_document_security, axiom,
    tm_asymmetric_cryptography != tm_document_security).

fof(bg_dist_tm_asymmetric_cryptography_tm_encryption_in_transfer, axiom,
    tm_asymmetric_cryptography != tm_encryption_in_transfer).

fof(bg_dist_tm_asymmetric_cryptography_tm_encryption_in_use, axiom,
    tm_asymmetric_cryptography != tm_encryption_in_use).

fof(bg_dist_tm_asymmetric_cryptography_tm_end_to_end_encryption, axiom,
    tm_asymmetric_cryptography != tm_end_to_end_encryption).

fof(bg_dist_tm_asymmetric_cryptography_tm_fail_safe_protocols, axiom,
    tm_asymmetric_cryptography != tm_fail_safe_protocols).

fof(bg_dist_tm_asymmetric_cryptography_tm_file_system_security, axiom,
    tm_asymmetric_cryptography != tm_file_system_security).

fof(bg_dist_tm_asymmetric_cryptography_tm_fully_randomised_pseudonymisation, axiom,
    tm_asymmetric_cryptography != tm_fully_randomised_pseudonymisation).

fof(bg_dist_tm_asymmetric_cryptography_tm_hardware_security_protocols, axiom,
    tm_asymmetric_cryptography != tm_hardware_security_protocols).

fof(bg_dist_tm_asymmetric_cryptography_tm_hash_functions, axiom,
    tm_asymmetric_cryptography != tm_hash_functions).

fof(bg_dist_tm_asymmetric_cryptography_tm_hash_message_authentication_code, axiom,
    tm_asymmetric_cryptography != tm_hash_message_authentication_code).

fof(bg_dist_tm_asymmetric_cryptography_tm_homomorphic_encryption, axiom,
    tm_asymmetric_cryptography != tm_homomorphic_encryption).

fof(bg_dist_tm_asymmetric_cryptography_tm_information_flow_control, axiom,
    tm_asymmetric_cryptography != tm_information_flow_control).

fof(bg_dist_tm_asymmetric_cryptography_tm_intrusion_detection_system, axiom,
    tm_asymmetric_cryptography != tm_intrusion_detection_system).

fof(bg_dist_tm_asymmetric_cryptography_tm_legal_measure, axiom,
    tm_asymmetric_cryptography != tm_legal_measure).

fof(bg_dist_tm_asymmetric_cryptography_tm_message_authentication_codes, axiom,
    tm_asymmetric_cryptography != tm_message_authentication_codes).

fof(bg_dist_tm_asymmetric_cryptography_tm_mobile_platform_security, axiom,
    tm_asymmetric_cryptography != tm_mobile_platform_security).

fof(bg_dist_tm_asymmetric_cryptography_tm_monotonic_counter_pseudonymisation, axiom,
    tm_asymmetric_cryptography != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_asymmetric_cryptography_tm_multi_factor_authentication, axiom,
    tm_asymmetric_cryptography != tm_multi_factor_authentication).

fof(bg_dist_tm_asymmetric_cryptography_tm_network_proxy_routing, axiom,
    tm_asymmetric_cryptography != tm_network_proxy_routing).

fof(bg_dist_tm_asymmetric_cryptography_tm_network_security_protocols, axiom,
    tm_asymmetric_cryptography != tm_network_security_protocols).

fof(bg_dist_tm_asymmetric_cryptography_tm_operating_system_security, axiom,
    tm_asymmetric_cryptography != tm_operating_system_security).

fof(bg_dist_tm_asymmetric_cryptography_tm_organisational_measure, axiom,
    tm_asymmetric_cryptography != tm_organisational_measure).

fof(bg_dist_tm_asymmetric_cryptography_tm_password_authentication, axiom,
    tm_asymmetric_cryptography != tm_password_authentication).

fof(bg_dist_tm_asymmetric_cryptography_tm_penetration_testing_methods, axiom,
    tm_asymmetric_cryptography != tm_penetration_testing_methods).

fof(bg_dist_tm_asymmetric_cryptography_tm_physical_measure, axiom,
    tm_asymmetric_cryptography != tm_physical_measure).

fof(bg_dist_tm_asymmetric_cryptography_tm_post_quantum_cryptography, axiom,
    tm_asymmetric_cryptography != tm_post_quantum_cryptography).

fof(bg_dist_tm_asymmetric_cryptography_tm_privacy_preserving_protocol, axiom,
    tm_asymmetric_cryptography != tm_privacy_preserving_protocol).

fof(bg_dist_tm_asymmetric_cryptography_tm_private_information_retrieval, axiom,
    tm_asymmetric_cryptography != tm_private_information_retrieval).

fof(bg_dist_tm_asymmetric_cryptography_tm_pseudonymisation, axiom,
    tm_asymmetric_cryptography != tm_pseudonymisation).

fof(bg_dist_tm_asymmetric_cryptography_tm_quantum_cryptography, axiom,
    tm_asymmetric_cryptography != tm_quantum_cryptography).

fof(bg_dist_tm_asymmetric_cryptography_tm_r_n_g_pseudonymisation, axiom,
    tm_asymmetric_cryptography != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_asymmetric_cryptography_tm_secret_sharing_schemes, axiom,
    tm_asymmetric_cryptography != tm_secret_sharing_schemes).

fof(bg_dist_tm_asymmetric_cryptography_tm_secure_multi_party_computation, axiom,
    tm_asymmetric_cryptography != tm_secure_multi_party_computation).

fof(bg_dist_tm_asymmetric_cryptography_tm_security_method, axiom,
    tm_asymmetric_cryptography != tm_security_method).

fof(bg_dist_tm_asymmetric_cryptography_tm_single_sign_on, axiom,
    tm_asymmetric_cryptography != tm_single_sign_on).

fof(bg_dist_tm_asymmetric_cryptography_tm_symmetric_cryptography, axiom,
    tm_asymmetric_cryptography != tm_symmetric_cryptography).

fof(bg_dist_tm_asymmetric_cryptography_tm_symmetric_encryption, axiom,
    tm_asymmetric_cryptography != tm_symmetric_encryption).

fof(bg_dist_tm_asymmetric_cryptography_tm_technical_measure, axiom,
    tm_asymmetric_cryptography != tm_technical_measure).

fof(bg_dist_tm_asymmetric_cryptography_tm_technical_organisational_measure, axiom,
    tm_asymmetric_cryptography != tm_technical_organisational_measure).

fof(bg_dist_tm_asymmetric_cryptography_tm_trusted_computing, axiom,
    tm_asymmetric_cryptography != tm_trusted_computing).

fof(bg_dist_tm_asymmetric_cryptography_tm_trusted_execution_environment, axiom,
    tm_asymmetric_cryptography != tm_trusted_execution_environment).

fof(bg_dist_tm_asymmetric_cryptography_tm_usage_control, axiom,
    tm_asymmetric_cryptography != tm_usage_control).

fof(bg_dist_tm_asymmetric_cryptography_tm_use_synthetic_data, axiom,
    tm_asymmetric_cryptography != tm_use_synthetic_data).

fof(bg_dist_tm_asymmetric_cryptography_tm_virtualisation_security, axiom,
    tm_asymmetric_cryptography != tm_virtualisation_security).

fof(bg_dist_tm_asymmetric_cryptography_tm_vulnerability_testing_methods, axiom,
    tm_asymmetric_cryptography != tm_vulnerability_testing_methods).

fof(bg_dist_tm_asymmetric_cryptography_tm_web_browser_security, axiom,
    tm_asymmetric_cryptography != tm_web_browser_security).

fof(bg_dist_tm_asymmetric_cryptography_tm_web_security_protocols, axiom,
    tm_asymmetric_cryptography != tm_web_security_protocols).

fof(bg_dist_tm_asymmetric_cryptography_tm_wireless_security_protocols, axiom,
    tm_asymmetric_cryptography != tm_wireless_security_protocols).

fof(bg_dist_tm_asymmetric_cryptography_tm_zero_knowledge_authentication, axiom,
    tm_asymmetric_cryptography != tm_zero_knowledge_authentication).

fof(bg_dist_tm_asymmetric_encryption_tm_authentication_a_b_c, axiom,
    tm_asymmetric_encryption != tm_authentication_a_b_c).

fof(bg_dist_tm_asymmetric_encryption_tm_authentication_p_a_b_c, axiom,
    tm_asymmetric_encryption != tm_authentication_p_a_b_c).

fof(bg_dist_tm_asymmetric_encryption_tm_authentication_protocols, axiom,
    tm_asymmetric_encryption != tm_authentication_protocols).

fof(bg_dist_tm_asymmetric_encryption_tm_authorisation_protocols, axiom,
    tm_asymmetric_encryption != tm_authorisation_protocols).

fof(bg_dist_tm_asymmetric_encryption_tm_biometric_authentication, axiom,
    tm_asymmetric_encryption != tm_biometric_authentication).

fof(bg_dist_tm_asymmetric_encryption_tm_cryptographic_authentication, axiom,
    tm_asymmetric_encryption != tm_cryptographic_authentication).

fof(bg_dist_tm_asymmetric_encryption_tm_cryptographic_key_management, axiom,
    tm_asymmetric_encryption != tm_cryptographic_key_management).

fof(bg_dist_tm_asymmetric_encryption_tm_cryptographic_methods, axiom,
    tm_asymmetric_encryption != tm_cryptographic_methods).

fof(bg_dist_tm_asymmetric_encryption_tm_data_backup_protocols, axiom,
    tm_asymmetric_encryption != tm_data_backup_protocols).

fof(bg_dist_tm_asymmetric_encryption_tm_data_redaction, axiom,
    tm_asymmetric_encryption != tm_data_redaction).

fof(bg_dist_tm_asymmetric_encryption_tm_data_sanitisation_technique, axiom,
    tm_asymmetric_encryption != tm_data_sanitisation_technique).

fof(bg_dist_tm_asymmetric_encryption_tm_deidentification, axiom,
    tm_asymmetric_encryption != tm_deidentification).

fof(bg_dist_tm_asymmetric_encryption_tm_deterministic_pseudonymisation, axiom,
    tm_asymmetric_encryption != tm_deterministic_pseudonymisation).

fof(bg_dist_tm_asymmetric_encryption_tm_differential_privacy, axiom,
    tm_asymmetric_encryption != tm_differential_privacy).

fof(bg_dist_tm_asymmetric_encryption_tm_digital_rights_management, axiom,
    tm_asymmetric_encryption != tm_digital_rights_management).

fof(bg_dist_tm_asymmetric_encryption_tm_digital_signatures, axiom,
    tm_asymmetric_encryption != tm_digital_signatures).

fof(bg_dist_tm_asymmetric_encryption_tm_distributed_system_security, axiom,
    tm_asymmetric_encryption != tm_distributed_system_security).

fof(bg_dist_tm_asymmetric_encryption_tm_document_randomised_pseudonymisation, axiom,
    tm_asymmetric_encryption != tm_document_randomised_pseudonymisation).

fof(bg_dist_tm_asymmetric_encryption_tm_document_security, axiom,
    tm_asymmetric_encryption != tm_document_security).

fof(bg_dist_tm_asymmetric_encryption_tm_encryption_in_transfer, axiom,
    tm_asymmetric_encryption != tm_encryption_in_transfer).

fof(bg_dist_tm_asymmetric_encryption_tm_encryption_in_use, axiom,
    tm_asymmetric_encryption != tm_encryption_in_use).

fof(bg_dist_tm_asymmetric_encryption_tm_end_to_end_encryption, axiom,
    tm_asymmetric_encryption != tm_end_to_end_encryption).

fof(bg_dist_tm_asymmetric_encryption_tm_fail_safe_protocols, axiom,
    tm_asymmetric_encryption != tm_fail_safe_protocols).

fof(bg_dist_tm_asymmetric_encryption_tm_file_system_security, axiom,
    tm_asymmetric_encryption != tm_file_system_security).

fof(bg_dist_tm_asymmetric_encryption_tm_fully_randomised_pseudonymisation, axiom,
    tm_asymmetric_encryption != tm_fully_randomised_pseudonymisation).

fof(bg_dist_tm_asymmetric_encryption_tm_hardware_security_protocols, axiom,
    tm_asymmetric_encryption != tm_hardware_security_protocols).

fof(bg_dist_tm_asymmetric_encryption_tm_hash_functions, axiom,
    tm_asymmetric_encryption != tm_hash_functions).

fof(bg_dist_tm_asymmetric_encryption_tm_hash_message_authentication_code, axiom,
    tm_asymmetric_encryption != tm_hash_message_authentication_code).

fof(bg_dist_tm_asymmetric_encryption_tm_homomorphic_encryption, axiom,
    tm_asymmetric_encryption != tm_homomorphic_encryption).

fof(bg_dist_tm_asymmetric_encryption_tm_information_flow_control, axiom,
    tm_asymmetric_encryption != tm_information_flow_control).

fof(bg_dist_tm_asymmetric_encryption_tm_intrusion_detection_system, axiom,
    tm_asymmetric_encryption != tm_intrusion_detection_system).

fof(bg_dist_tm_asymmetric_encryption_tm_legal_measure, axiom,
    tm_asymmetric_encryption != tm_legal_measure).

fof(bg_dist_tm_asymmetric_encryption_tm_message_authentication_codes, axiom,
    tm_asymmetric_encryption != tm_message_authentication_codes).

fof(bg_dist_tm_asymmetric_encryption_tm_mobile_platform_security, axiom,
    tm_asymmetric_encryption != tm_mobile_platform_security).

fof(bg_dist_tm_asymmetric_encryption_tm_monotonic_counter_pseudonymisation, axiom,
    tm_asymmetric_encryption != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_asymmetric_encryption_tm_multi_factor_authentication, axiom,
    tm_asymmetric_encryption != tm_multi_factor_authentication).

fof(bg_dist_tm_asymmetric_encryption_tm_network_proxy_routing, axiom,
    tm_asymmetric_encryption != tm_network_proxy_routing).

fof(bg_dist_tm_asymmetric_encryption_tm_network_security_protocols, axiom,
    tm_asymmetric_encryption != tm_network_security_protocols).

fof(bg_dist_tm_asymmetric_encryption_tm_operating_system_security, axiom,
    tm_asymmetric_encryption != tm_operating_system_security).

fof(bg_dist_tm_asymmetric_encryption_tm_organisational_measure, axiom,
    tm_asymmetric_encryption != tm_organisational_measure).

fof(bg_dist_tm_asymmetric_encryption_tm_password_authentication, axiom,
    tm_asymmetric_encryption != tm_password_authentication).

fof(bg_dist_tm_asymmetric_encryption_tm_penetration_testing_methods, axiom,
    tm_asymmetric_encryption != tm_penetration_testing_methods).

fof(bg_dist_tm_asymmetric_encryption_tm_physical_measure, axiom,
    tm_asymmetric_encryption != tm_physical_measure).

fof(bg_dist_tm_asymmetric_encryption_tm_post_quantum_cryptography, axiom,
    tm_asymmetric_encryption != tm_post_quantum_cryptography).

fof(bg_dist_tm_asymmetric_encryption_tm_privacy_preserving_protocol, axiom,
    tm_asymmetric_encryption != tm_privacy_preserving_protocol).

fof(bg_dist_tm_asymmetric_encryption_tm_private_information_retrieval, axiom,
    tm_asymmetric_encryption != tm_private_information_retrieval).

fof(bg_dist_tm_asymmetric_encryption_tm_pseudonymisation, axiom,
    tm_asymmetric_encryption != tm_pseudonymisation).

fof(bg_dist_tm_asymmetric_encryption_tm_quantum_cryptography, axiom,
    tm_asymmetric_encryption != tm_quantum_cryptography).

fof(bg_dist_tm_asymmetric_encryption_tm_r_n_g_pseudonymisation, axiom,
    tm_asymmetric_encryption != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_asymmetric_encryption_tm_secret_sharing_schemes, axiom,
    tm_asymmetric_encryption != tm_secret_sharing_schemes).

fof(bg_dist_tm_asymmetric_encryption_tm_secure_multi_party_computation, axiom,
    tm_asymmetric_encryption != tm_secure_multi_party_computation).

fof(bg_dist_tm_asymmetric_encryption_tm_security_method, axiom,
    tm_asymmetric_encryption != tm_security_method).

fof(bg_dist_tm_asymmetric_encryption_tm_single_sign_on, axiom,
    tm_asymmetric_encryption != tm_single_sign_on).

fof(bg_dist_tm_asymmetric_encryption_tm_symmetric_cryptography, axiom,
    tm_asymmetric_encryption != tm_symmetric_cryptography).

fof(bg_dist_tm_asymmetric_encryption_tm_symmetric_encryption, axiom,
    tm_asymmetric_encryption != tm_symmetric_encryption).

fof(bg_dist_tm_asymmetric_encryption_tm_technical_measure, axiom,
    tm_asymmetric_encryption != tm_technical_measure).

fof(bg_dist_tm_asymmetric_encryption_tm_technical_organisational_measure, axiom,
    tm_asymmetric_encryption != tm_technical_organisational_measure).

fof(bg_dist_tm_asymmetric_encryption_tm_trusted_computing, axiom,
    tm_asymmetric_encryption != tm_trusted_computing).

fof(bg_dist_tm_asymmetric_encryption_tm_trusted_execution_environment, axiom,
    tm_asymmetric_encryption != tm_trusted_execution_environment).

fof(bg_dist_tm_asymmetric_encryption_tm_usage_control, axiom,
    tm_asymmetric_encryption != tm_usage_control).

fof(bg_dist_tm_asymmetric_encryption_tm_use_synthetic_data, axiom,
    tm_asymmetric_encryption != tm_use_synthetic_data).

fof(bg_dist_tm_asymmetric_encryption_tm_virtualisation_security, axiom,
    tm_asymmetric_encryption != tm_virtualisation_security).

fof(bg_dist_tm_asymmetric_encryption_tm_vulnerability_testing_methods, axiom,
    tm_asymmetric_encryption != tm_vulnerability_testing_methods).

fof(bg_dist_tm_asymmetric_encryption_tm_web_browser_security, axiom,
    tm_asymmetric_encryption != tm_web_browser_security).

fof(bg_dist_tm_asymmetric_encryption_tm_web_security_protocols, axiom,
    tm_asymmetric_encryption != tm_web_security_protocols).

fof(bg_dist_tm_asymmetric_encryption_tm_wireless_security_protocols, axiom,
    tm_asymmetric_encryption != tm_wireless_security_protocols).

fof(bg_dist_tm_asymmetric_encryption_tm_zero_knowledge_authentication, axiom,
    tm_asymmetric_encryption != tm_zero_knowledge_authentication).

fof(bg_dist_tm_authentication_a_b_c_tm_authentication_p_a_b_c, axiom,
    tm_authentication_a_b_c != tm_authentication_p_a_b_c).

fof(bg_dist_tm_authentication_a_b_c_tm_authentication_protocols, axiom,
    tm_authentication_a_b_c != tm_authentication_protocols).

fof(bg_dist_tm_authentication_a_b_c_tm_authorisation_protocols, axiom,
    tm_authentication_a_b_c != tm_authorisation_protocols).

fof(bg_dist_tm_authentication_a_b_c_tm_biometric_authentication, axiom,
    tm_authentication_a_b_c != tm_biometric_authentication).

fof(bg_dist_tm_authentication_a_b_c_tm_cryptographic_authentication, axiom,
    tm_authentication_a_b_c != tm_cryptographic_authentication).

fof(bg_dist_tm_authentication_a_b_c_tm_cryptographic_key_management, axiom,
    tm_authentication_a_b_c != tm_cryptographic_key_management).

fof(bg_dist_tm_authentication_a_b_c_tm_cryptographic_methods, axiom,
    tm_authentication_a_b_c != tm_cryptographic_methods).

fof(bg_dist_tm_authentication_a_b_c_tm_data_backup_protocols, axiom,
    tm_authentication_a_b_c != tm_data_backup_protocols).

fof(bg_dist_tm_authentication_a_b_c_tm_data_redaction, axiom,
    tm_authentication_a_b_c != tm_data_redaction).

fof(bg_dist_tm_authentication_a_b_c_tm_data_sanitisation_technique, axiom,
    tm_authentication_a_b_c != tm_data_sanitisation_technique).

fof(bg_dist_tm_authentication_a_b_c_tm_deidentification, axiom,
    tm_authentication_a_b_c != tm_deidentification).

fof(bg_dist_tm_authentication_a_b_c_tm_deterministic_pseudonymisation, axiom,
    tm_authentication_a_b_c != tm_deterministic_pseudonymisation).

fof(bg_dist_tm_authentication_a_b_c_tm_differential_privacy, axiom,
    tm_authentication_a_b_c != tm_differential_privacy).

fof(bg_dist_tm_authentication_a_b_c_tm_digital_rights_management, axiom,
    tm_authentication_a_b_c != tm_digital_rights_management).

fof(bg_dist_tm_authentication_a_b_c_tm_digital_signatures, axiom,
    tm_authentication_a_b_c != tm_digital_signatures).

fof(bg_dist_tm_authentication_a_b_c_tm_distributed_system_security, axiom,
    tm_authentication_a_b_c != tm_distributed_system_security).

fof(bg_dist_tm_authentication_a_b_c_tm_document_randomised_pseudonymisation, axiom,
    tm_authentication_a_b_c != tm_document_randomised_pseudonymisation).

fof(bg_dist_tm_authentication_a_b_c_tm_document_security, axiom,
    tm_authentication_a_b_c != tm_document_security).

fof(bg_dist_tm_authentication_a_b_c_tm_encryption_in_transfer, axiom,
    tm_authentication_a_b_c != tm_encryption_in_transfer).

fof(bg_dist_tm_authentication_a_b_c_tm_encryption_in_use, axiom,
    tm_authentication_a_b_c != tm_encryption_in_use).

fof(bg_dist_tm_authentication_a_b_c_tm_end_to_end_encryption, axiom,
    tm_authentication_a_b_c != tm_end_to_end_encryption).

fof(bg_dist_tm_authentication_a_b_c_tm_fail_safe_protocols, axiom,
    tm_authentication_a_b_c != tm_fail_safe_protocols).

fof(bg_dist_tm_authentication_a_b_c_tm_file_system_security, axiom,
    tm_authentication_a_b_c != tm_file_system_security).

fof(bg_dist_tm_authentication_a_b_c_tm_fully_randomised_pseudonymisation, axiom,
    tm_authentication_a_b_c != tm_fully_randomised_pseudonymisation).

fof(bg_dist_tm_authentication_a_b_c_tm_hardware_security_protocols, axiom,
    tm_authentication_a_b_c != tm_hardware_security_protocols).

fof(bg_dist_tm_authentication_a_b_c_tm_hash_functions, axiom,
    tm_authentication_a_b_c != tm_hash_functions).

fof(bg_dist_tm_authentication_a_b_c_tm_hash_message_authentication_code, axiom,
    tm_authentication_a_b_c != tm_hash_message_authentication_code).

fof(bg_dist_tm_authentication_a_b_c_tm_homomorphic_encryption, axiom,
    tm_authentication_a_b_c != tm_homomorphic_encryption).

fof(bg_dist_tm_authentication_a_b_c_tm_information_flow_control, axiom,
    tm_authentication_a_b_c != tm_information_flow_control).

fof(bg_dist_tm_authentication_a_b_c_tm_intrusion_detection_system, axiom,
    tm_authentication_a_b_c != tm_intrusion_detection_system).

fof(bg_dist_tm_authentication_a_b_c_tm_legal_measure, axiom,
    tm_authentication_a_b_c != tm_legal_measure).

fof(bg_dist_tm_authentication_a_b_c_tm_message_authentication_codes, axiom,
    tm_authentication_a_b_c != tm_message_authentication_codes).

fof(bg_dist_tm_authentication_a_b_c_tm_mobile_platform_security, axiom,
    tm_authentication_a_b_c != tm_mobile_platform_security).

fof(bg_dist_tm_authentication_a_b_c_tm_monotonic_counter_pseudonymisation, axiom,
    tm_authentication_a_b_c != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_authentication_a_b_c_tm_multi_factor_authentication, axiom,
    tm_authentication_a_b_c != tm_multi_factor_authentication).

fof(bg_dist_tm_authentication_a_b_c_tm_network_proxy_routing, axiom,
    tm_authentication_a_b_c != tm_network_proxy_routing).

fof(bg_dist_tm_authentication_a_b_c_tm_network_security_protocols, axiom,
    tm_authentication_a_b_c != tm_network_security_protocols).

fof(bg_dist_tm_authentication_a_b_c_tm_operating_system_security, axiom,
    tm_authentication_a_b_c != tm_operating_system_security).

fof(bg_dist_tm_authentication_a_b_c_tm_organisational_measure, axiom,
    tm_authentication_a_b_c != tm_organisational_measure).

fof(bg_dist_tm_authentication_a_b_c_tm_password_authentication, axiom,
    tm_authentication_a_b_c != tm_password_authentication).

fof(bg_dist_tm_authentication_a_b_c_tm_penetration_testing_methods, axiom,
    tm_authentication_a_b_c != tm_penetration_testing_methods).

fof(bg_dist_tm_authentication_a_b_c_tm_physical_measure, axiom,
    tm_authentication_a_b_c != tm_physical_measure).

fof(bg_dist_tm_authentication_a_b_c_tm_post_quantum_cryptography, axiom,
    tm_authentication_a_b_c != tm_post_quantum_cryptography).

fof(bg_dist_tm_authentication_a_b_c_tm_privacy_preserving_protocol, axiom,
    tm_authentication_a_b_c != tm_privacy_preserving_protocol).

fof(bg_dist_tm_authentication_a_b_c_tm_private_information_retrieval, axiom,
    tm_authentication_a_b_c != tm_private_information_retrieval).

fof(bg_dist_tm_authentication_a_b_c_tm_pseudonymisation, axiom,
    tm_authentication_a_b_c != tm_pseudonymisation).

fof(bg_dist_tm_authentication_a_b_c_tm_quantum_cryptography, axiom,
    tm_authentication_a_b_c != tm_quantum_cryptography).

fof(bg_dist_tm_authentication_a_b_c_tm_r_n_g_pseudonymisation, axiom,
    tm_authentication_a_b_c != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_authentication_a_b_c_tm_secret_sharing_schemes, axiom,
    tm_authentication_a_b_c != tm_secret_sharing_schemes).

fof(bg_dist_tm_authentication_a_b_c_tm_secure_multi_party_computation, axiom,
    tm_authentication_a_b_c != tm_secure_multi_party_computation).

fof(bg_dist_tm_authentication_a_b_c_tm_security_method, axiom,
    tm_authentication_a_b_c != tm_security_method).

fof(bg_dist_tm_authentication_a_b_c_tm_single_sign_on, axiom,
    tm_authentication_a_b_c != tm_single_sign_on).

fof(bg_dist_tm_authentication_a_b_c_tm_symmetric_cryptography, axiom,
    tm_authentication_a_b_c != tm_symmetric_cryptography).

fof(bg_dist_tm_authentication_a_b_c_tm_symmetric_encryption, axiom,
    tm_authentication_a_b_c != tm_symmetric_encryption).

fof(bg_dist_tm_authentication_a_b_c_tm_technical_measure, axiom,
    tm_authentication_a_b_c != tm_technical_measure).

fof(bg_dist_tm_authentication_a_b_c_tm_technical_organisational_measure, axiom,
    tm_authentication_a_b_c != tm_technical_organisational_measure).

fof(bg_dist_tm_authentication_a_b_c_tm_trusted_computing, axiom,
    tm_authentication_a_b_c != tm_trusted_computing).

fof(bg_dist_tm_authentication_a_b_c_tm_trusted_execution_environment, axiom,
    tm_authentication_a_b_c != tm_trusted_execution_environment).

fof(bg_dist_tm_authentication_a_b_c_tm_usage_control, axiom,
    tm_authentication_a_b_c != tm_usage_control).

fof(bg_dist_tm_authentication_a_b_c_tm_use_synthetic_data, axiom,
    tm_authentication_a_b_c != tm_use_synthetic_data).

fof(bg_dist_tm_authentication_a_b_c_tm_virtualisation_security, axiom,
    tm_authentication_a_b_c != tm_virtualisation_security).

fof(bg_dist_tm_authentication_a_b_c_tm_vulnerability_testing_methods, axiom,
    tm_authentication_a_b_c != tm_vulnerability_testing_methods).

fof(bg_dist_tm_authentication_a_b_c_tm_web_browser_security, axiom,
    tm_authentication_a_b_c != tm_web_browser_security).

fof(bg_dist_tm_authentication_a_b_c_tm_web_security_protocols, axiom,
    tm_authentication_a_b_c != tm_web_security_protocols).

fof(bg_dist_tm_authentication_a_b_c_tm_wireless_security_protocols, axiom,
    tm_authentication_a_b_c != tm_wireless_security_protocols).

fof(bg_dist_tm_authentication_a_b_c_tm_zero_knowledge_authentication, axiom,
    tm_authentication_a_b_c != tm_zero_knowledge_authentication).

fof(bg_dist_tm_authentication_p_a_b_c_tm_authentication_protocols, axiom,
    tm_authentication_p_a_b_c != tm_authentication_protocols).

fof(bg_dist_tm_authentication_p_a_b_c_tm_authorisation_protocols, axiom,
    tm_authentication_p_a_b_c != tm_authorisation_protocols).

fof(bg_dist_tm_authentication_p_a_b_c_tm_biometric_authentication, axiom,
    tm_authentication_p_a_b_c != tm_biometric_authentication).

fof(bg_dist_tm_authentication_p_a_b_c_tm_cryptographic_authentication, axiom,
    tm_authentication_p_a_b_c != tm_cryptographic_authentication).

fof(bg_dist_tm_authentication_p_a_b_c_tm_cryptographic_key_management, axiom,
    tm_authentication_p_a_b_c != tm_cryptographic_key_management).

fof(bg_dist_tm_authentication_p_a_b_c_tm_cryptographic_methods, axiom,
    tm_authentication_p_a_b_c != tm_cryptographic_methods).

fof(bg_dist_tm_authentication_p_a_b_c_tm_data_backup_protocols, axiom,
    tm_authentication_p_a_b_c != tm_data_backup_protocols).

fof(bg_dist_tm_authentication_p_a_b_c_tm_data_redaction, axiom,
    tm_authentication_p_a_b_c != tm_data_redaction).

fof(bg_dist_tm_authentication_p_a_b_c_tm_data_sanitisation_technique, axiom,
    tm_authentication_p_a_b_c != tm_data_sanitisation_technique).

fof(bg_dist_tm_authentication_p_a_b_c_tm_deidentification, axiom,
    tm_authentication_p_a_b_c != tm_deidentification).

fof(bg_dist_tm_authentication_p_a_b_c_tm_deterministic_pseudonymisation, axiom,
    tm_authentication_p_a_b_c != tm_deterministic_pseudonymisation).

fof(bg_dist_tm_authentication_p_a_b_c_tm_differential_privacy, axiom,
    tm_authentication_p_a_b_c != tm_differential_privacy).

fof(bg_dist_tm_authentication_p_a_b_c_tm_digital_rights_management, axiom,
    tm_authentication_p_a_b_c != tm_digital_rights_management).

fof(bg_dist_tm_authentication_p_a_b_c_tm_digital_signatures, axiom,
    tm_authentication_p_a_b_c != tm_digital_signatures).

fof(bg_dist_tm_authentication_p_a_b_c_tm_distributed_system_security, axiom,
    tm_authentication_p_a_b_c != tm_distributed_system_security).

fof(bg_dist_tm_authentication_p_a_b_c_tm_document_randomised_pseudonymisation, axiom,
    tm_authentication_p_a_b_c != tm_document_randomised_pseudonymisation).

fof(bg_dist_tm_authentication_p_a_b_c_tm_document_security, axiom,
    tm_authentication_p_a_b_c != tm_document_security).

fof(bg_dist_tm_authentication_p_a_b_c_tm_encryption_in_transfer, axiom,
    tm_authentication_p_a_b_c != tm_encryption_in_transfer).

fof(bg_dist_tm_authentication_p_a_b_c_tm_encryption_in_use, axiom,
    tm_authentication_p_a_b_c != tm_encryption_in_use).

fof(bg_dist_tm_authentication_p_a_b_c_tm_end_to_end_encryption, axiom,
    tm_authentication_p_a_b_c != tm_end_to_end_encryption).

fof(bg_dist_tm_authentication_p_a_b_c_tm_fail_safe_protocols, axiom,
    tm_authentication_p_a_b_c != tm_fail_safe_protocols).

fof(bg_dist_tm_authentication_p_a_b_c_tm_file_system_security, axiom,
    tm_authentication_p_a_b_c != tm_file_system_security).

fof(bg_dist_tm_authentication_p_a_b_c_tm_fully_randomised_pseudonymisation, axiom,
    tm_authentication_p_a_b_c != tm_fully_randomised_pseudonymisation).

fof(bg_dist_tm_authentication_p_a_b_c_tm_hardware_security_protocols, axiom,
    tm_authentication_p_a_b_c != tm_hardware_security_protocols).

fof(bg_dist_tm_authentication_p_a_b_c_tm_hash_functions, axiom,
    tm_authentication_p_a_b_c != tm_hash_functions).

fof(bg_dist_tm_authentication_p_a_b_c_tm_hash_message_authentication_code, axiom,
    tm_authentication_p_a_b_c != tm_hash_message_authentication_code).

fof(bg_dist_tm_authentication_p_a_b_c_tm_homomorphic_encryption, axiom,
    tm_authentication_p_a_b_c != tm_homomorphic_encryption).

fof(bg_dist_tm_authentication_p_a_b_c_tm_information_flow_control, axiom,
    tm_authentication_p_a_b_c != tm_information_flow_control).

fof(bg_dist_tm_authentication_p_a_b_c_tm_intrusion_detection_system, axiom,
    tm_authentication_p_a_b_c != tm_intrusion_detection_system).

fof(bg_dist_tm_authentication_p_a_b_c_tm_legal_measure, axiom,
    tm_authentication_p_a_b_c != tm_legal_measure).

fof(bg_dist_tm_authentication_p_a_b_c_tm_message_authentication_codes, axiom,
    tm_authentication_p_a_b_c != tm_message_authentication_codes).

fof(bg_dist_tm_authentication_p_a_b_c_tm_mobile_platform_security, axiom,
    tm_authentication_p_a_b_c != tm_mobile_platform_security).

fof(bg_dist_tm_authentication_p_a_b_c_tm_monotonic_counter_pseudonymisation, axiom,
    tm_authentication_p_a_b_c != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_authentication_p_a_b_c_tm_multi_factor_authentication, axiom,
    tm_authentication_p_a_b_c != tm_multi_factor_authentication).

fof(bg_dist_tm_authentication_p_a_b_c_tm_network_proxy_routing, axiom,
    tm_authentication_p_a_b_c != tm_network_proxy_routing).

fof(bg_dist_tm_authentication_p_a_b_c_tm_network_security_protocols, axiom,
    tm_authentication_p_a_b_c != tm_network_security_protocols).

fof(bg_dist_tm_authentication_p_a_b_c_tm_operating_system_security, axiom,
    tm_authentication_p_a_b_c != tm_operating_system_security).

fof(bg_dist_tm_authentication_p_a_b_c_tm_organisational_measure, axiom,
    tm_authentication_p_a_b_c != tm_organisational_measure).

fof(bg_dist_tm_authentication_p_a_b_c_tm_password_authentication, axiom,
    tm_authentication_p_a_b_c != tm_password_authentication).

fof(bg_dist_tm_authentication_p_a_b_c_tm_penetration_testing_methods, axiom,
    tm_authentication_p_a_b_c != tm_penetration_testing_methods).

fof(bg_dist_tm_authentication_p_a_b_c_tm_physical_measure, axiom,
    tm_authentication_p_a_b_c != tm_physical_measure).

fof(bg_dist_tm_authentication_p_a_b_c_tm_post_quantum_cryptography, axiom,
    tm_authentication_p_a_b_c != tm_post_quantum_cryptography).

fof(bg_dist_tm_authentication_p_a_b_c_tm_privacy_preserving_protocol, axiom,
    tm_authentication_p_a_b_c != tm_privacy_preserving_protocol).

fof(bg_dist_tm_authentication_p_a_b_c_tm_private_information_retrieval, axiom,
    tm_authentication_p_a_b_c != tm_private_information_retrieval).

fof(bg_dist_tm_authentication_p_a_b_c_tm_pseudonymisation, axiom,
    tm_authentication_p_a_b_c != tm_pseudonymisation).

fof(bg_dist_tm_authentication_p_a_b_c_tm_quantum_cryptography, axiom,
    tm_authentication_p_a_b_c != tm_quantum_cryptography).

fof(bg_dist_tm_authentication_p_a_b_c_tm_r_n_g_pseudonymisation, axiom,
    tm_authentication_p_a_b_c != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_authentication_p_a_b_c_tm_secret_sharing_schemes, axiom,
    tm_authentication_p_a_b_c != tm_secret_sharing_schemes).

fof(bg_dist_tm_authentication_p_a_b_c_tm_secure_multi_party_computation, axiom,
    tm_authentication_p_a_b_c != tm_secure_multi_party_computation).

fof(bg_dist_tm_authentication_p_a_b_c_tm_security_method, axiom,
    tm_authentication_p_a_b_c != tm_security_method).

fof(bg_dist_tm_authentication_p_a_b_c_tm_single_sign_on, axiom,
    tm_authentication_p_a_b_c != tm_single_sign_on).

fof(bg_dist_tm_authentication_p_a_b_c_tm_symmetric_cryptography, axiom,
    tm_authentication_p_a_b_c != tm_symmetric_cryptography).

fof(bg_dist_tm_authentication_p_a_b_c_tm_symmetric_encryption, axiom,
    tm_authentication_p_a_b_c != tm_symmetric_encryption).

fof(bg_dist_tm_authentication_p_a_b_c_tm_technical_measure, axiom,
    tm_authentication_p_a_b_c != tm_technical_measure).

fof(bg_dist_tm_authentication_p_a_b_c_tm_technical_organisational_measure, axiom,
    tm_authentication_p_a_b_c != tm_technical_organisational_measure).

fof(bg_dist_tm_authentication_p_a_b_c_tm_trusted_computing, axiom,
    tm_authentication_p_a_b_c != tm_trusted_computing).

fof(bg_dist_tm_authentication_p_a_b_c_tm_trusted_execution_environment, axiom,
    tm_authentication_p_a_b_c != tm_trusted_execution_environment).

fof(bg_dist_tm_authentication_p_a_b_c_tm_usage_control, axiom,
    tm_authentication_p_a_b_c != tm_usage_control).

fof(bg_dist_tm_authentication_p_a_b_c_tm_use_synthetic_data, axiom,
    tm_authentication_p_a_b_c != tm_use_synthetic_data).

fof(bg_dist_tm_authentication_p_a_b_c_tm_virtualisation_security, axiom,
    tm_authentication_p_a_b_c != tm_virtualisation_security).

fof(bg_dist_tm_authentication_p_a_b_c_tm_vulnerability_testing_methods, axiom,
    tm_authentication_p_a_b_c != tm_vulnerability_testing_methods).

fof(bg_dist_tm_authentication_p_a_b_c_tm_web_browser_security, axiom,
    tm_authentication_p_a_b_c != tm_web_browser_security).

fof(bg_dist_tm_authentication_p_a_b_c_tm_web_security_protocols, axiom,
    tm_authentication_p_a_b_c != tm_web_security_protocols).

fof(bg_dist_tm_authentication_p_a_b_c_tm_wireless_security_protocols, axiom,
    tm_authentication_p_a_b_c != tm_wireless_security_protocols).

fof(bg_dist_tm_authentication_p_a_b_c_tm_zero_knowledge_authentication, axiom,
    tm_authentication_p_a_b_c != tm_zero_knowledge_authentication).

fof(bg_dist_tm_authentication_protocols_tm_authorisation_protocols, axiom,
    tm_authentication_protocols != tm_authorisation_protocols).

fof(bg_dist_tm_authentication_protocols_tm_biometric_authentication, axiom,
    tm_authentication_protocols != tm_biometric_authentication).

fof(bg_dist_tm_authentication_protocols_tm_cryptographic_authentication, axiom,
    tm_authentication_protocols != tm_cryptographic_authentication).

fof(bg_dist_tm_authentication_protocols_tm_cryptographic_key_management, axiom,
    tm_authentication_protocols != tm_cryptographic_key_management).

fof(bg_dist_tm_authentication_protocols_tm_cryptographic_methods, axiom,
    tm_authentication_protocols != tm_cryptographic_methods).

fof(bg_dist_tm_authentication_protocols_tm_data_backup_protocols, axiom,
    tm_authentication_protocols != tm_data_backup_protocols).

fof(bg_dist_tm_authentication_protocols_tm_data_redaction, axiom,
    tm_authentication_protocols != tm_data_redaction).

fof(bg_dist_tm_authentication_protocols_tm_data_sanitisation_technique, axiom,
    tm_authentication_protocols != tm_data_sanitisation_technique).

fof(bg_dist_tm_authentication_protocols_tm_deidentification, axiom,
    tm_authentication_protocols != tm_deidentification).

fof(bg_dist_tm_authentication_protocols_tm_deterministic_pseudonymisation, axiom,
    tm_authentication_protocols != tm_deterministic_pseudonymisation).

fof(bg_dist_tm_authentication_protocols_tm_differential_privacy, axiom,
    tm_authentication_protocols != tm_differential_privacy).

fof(bg_dist_tm_authentication_protocols_tm_digital_rights_management, axiom,
    tm_authentication_protocols != tm_digital_rights_management).

fof(bg_dist_tm_authentication_protocols_tm_digital_signatures, axiom,
    tm_authentication_protocols != tm_digital_signatures).

fof(bg_dist_tm_authentication_protocols_tm_distributed_system_security, axiom,
    tm_authentication_protocols != tm_distributed_system_security).

fof(bg_dist_tm_authentication_protocols_tm_document_randomised_pseudonymisation, axiom,
    tm_authentication_protocols != tm_document_randomised_pseudonymisation).

fof(bg_dist_tm_authentication_protocols_tm_document_security, axiom,
    tm_authentication_protocols != tm_document_security).

fof(bg_dist_tm_authentication_protocols_tm_encryption_in_transfer, axiom,
    tm_authentication_protocols != tm_encryption_in_transfer).

fof(bg_dist_tm_authentication_protocols_tm_encryption_in_use, axiom,
    tm_authentication_protocols != tm_encryption_in_use).

fof(bg_dist_tm_authentication_protocols_tm_end_to_end_encryption, axiom,
    tm_authentication_protocols != tm_end_to_end_encryption).

fof(bg_dist_tm_authentication_protocols_tm_fail_safe_protocols, axiom,
    tm_authentication_protocols != tm_fail_safe_protocols).

fof(bg_dist_tm_authentication_protocols_tm_file_system_security, axiom,
    tm_authentication_protocols != tm_file_system_security).

fof(bg_dist_tm_authentication_protocols_tm_fully_randomised_pseudonymisation, axiom,
    tm_authentication_protocols != tm_fully_randomised_pseudonymisation).

fof(bg_dist_tm_authentication_protocols_tm_hardware_security_protocols, axiom,
    tm_authentication_protocols != tm_hardware_security_protocols).

fof(bg_dist_tm_authentication_protocols_tm_hash_functions, axiom,
    tm_authentication_protocols != tm_hash_functions).

fof(bg_dist_tm_authentication_protocols_tm_hash_message_authentication_code, axiom,
    tm_authentication_protocols != tm_hash_message_authentication_code).

fof(bg_dist_tm_authentication_protocols_tm_homomorphic_encryption, axiom,
    tm_authentication_protocols != tm_homomorphic_encryption).

fof(bg_dist_tm_authentication_protocols_tm_information_flow_control, axiom,
    tm_authentication_protocols != tm_information_flow_control).

fof(bg_dist_tm_authentication_protocols_tm_intrusion_detection_system, axiom,
    tm_authentication_protocols != tm_intrusion_detection_system).

fof(bg_dist_tm_authentication_protocols_tm_legal_measure, axiom,
    tm_authentication_protocols != tm_legal_measure).

fof(bg_dist_tm_authentication_protocols_tm_message_authentication_codes, axiom,
    tm_authentication_protocols != tm_message_authentication_codes).

fof(bg_dist_tm_authentication_protocols_tm_mobile_platform_security, axiom,
    tm_authentication_protocols != tm_mobile_platform_security).

fof(bg_dist_tm_authentication_protocols_tm_monotonic_counter_pseudonymisation, axiom,
    tm_authentication_protocols != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_authentication_protocols_tm_multi_factor_authentication, axiom,
    tm_authentication_protocols != tm_multi_factor_authentication).

fof(bg_dist_tm_authentication_protocols_tm_network_proxy_routing, axiom,
    tm_authentication_protocols != tm_network_proxy_routing).

fof(bg_dist_tm_authentication_protocols_tm_network_security_protocols, axiom,
    tm_authentication_protocols != tm_network_security_protocols).

fof(bg_dist_tm_authentication_protocols_tm_operating_system_security, axiom,
    tm_authentication_protocols != tm_operating_system_security).

fof(bg_dist_tm_authentication_protocols_tm_organisational_measure, axiom,
    tm_authentication_protocols != tm_organisational_measure).

fof(bg_dist_tm_authentication_protocols_tm_password_authentication, axiom,
    tm_authentication_protocols != tm_password_authentication).

fof(bg_dist_tm_authentication_protocols_tm_penetration_testing_methods, axiom,
    tm_authentication_protocols != tm_penetration_testing_methods).

fof(bg_dist_tm_authentication_protocols_tm_physical_measure, axiom,
    tm_authentication_protocols != tm_physical_measure).

fof(bg_dist_tm_authentication_protocols_tm_post_quantum_cryptography, axiom,
    tm_authentication_protocols != tm_post_quantum_cryptography).

fof(bg_dist_tm_authentication_protocols_tm_privacy_preserving_protocol, axiom,
    tm_authentication_protocols != tm_privacy_preserving_protocol).

fof(bg_dist_tm_authentication_protocols_tm_private_information_retrieval, axiom,
    tm_authentication_protocols != tm_private_information_retrieval).

fof(bg_dist_tm_authentication_protocols_tm_pseudonymisation, axiom,
    tm_authentication_protocols != tm_pseudonymisation).

fof(bg_dist_tm_authentication_protocols_tm_quantum_cryptography, axiom,
    tm_authentication_protocols != tm_quantum_cryptography).

fof(bg_dist_tm_authentication_protocols_tm_r_n_g_pseudonymisation, axiom,
    tm_authentication_protocols != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_authentication_protocols_tm_secret_sharing_schemes, axiom,
    tm_authentication_protocols != tm_secret_sharing_schemes).

fof(bg_dist_tm_authentication_protocols_tm_secure_multi_party_computation, axiom,
    tm_authentication_protocols != tm_secure_multi_party_computation).

fof(bg_dist_tm_authentication_protocols_tm_security_method, axiom,
    tm_authentication_protocols != tm_security_method).

fof(bg_dist_tm_authentication_protocols_tm_single_sign_on, axiom,
    tm_authentication_protocols != tm_single_sign_on).

fof(bg_dist_tm_authentication_protocols_tm_symmetric_cryptography, axiom,
    tm_authentication_protocols != tm_symmetric_cryptography).

fof(bg_dist_tm_authentication_protocols_tm_symmetric_encryption, axiom,
    tm_authentication_protocols != tm_symmetric_encryption).

fof(bg_dist_tm_authentication_protocols_tm_technical_measure, axiom,
    tm_authentication_protocols != tm_technical_measure).

fof(bg_dist_tm_authentication_protocols_tm_technical_organisational_measure, axiom,
    tm_authentication_protocols != tm_technical_organisational_measure).

fof(bg_dist_tm_authentication_protocols_tm_trusted_computing, axiom,
    tm_authentication_protocols != tm_trusted_computing).

fof(bg_dist_tm_authentication_protocols_tm_trusted_execution_environment, axiom,
    tm_authentication_protocols != tm_trusted_execution_environment).

fof(bg_dist_tm_authentication_protocols_tm_usage_control, axiom,
    tm_authentication_protocols != tm_usage_control).

fof(bg_dist_tm_authentication_protocols_tm_use_synthetic_data, axiom,
    tm_authentication_protocols != tm_use_synthetic_data).

fof(bg_dist_tm_authentication_protocols_tm_virtualisation_security, axiom,
    tm_authentication_protocols != tm_virtualisation_security).

fof(bg_dist_tm_authentication_protocols_tm_vulnerability_testing_methods, axiom,
    tm_authentication_protocols != tm_vulnerability_testing_methods).

fof(bg_dist_tm_authentication_protocols_tm_web_browser_security, axiom,
    tm_authentication_protocols != tm_web_browser_security).

fof(bg_dist_tm_authentication_protocols_tm_web_security_protocols, axiom,
    tm_authentication_protocols != tm_web_security_protocols).

fof(bg_dist_tm_authentication_protocols_tm_wireless_security_protocols, axiom,
    tm_authentication_protocols != tm_wireless_security_protocols).

fof(bg_dist_tm_authentication_protocols_tm_zero_knowledge_authentication, axiom,
    tm_authentication_protocols != tm_zero_knowledge_authentication).

fof(bg_dist_tm_authorisation_protocols_tm_biometric_authentication, axiom,
    tm_authorisation_protocols != tm_biometric_authentication).

fof(bg_dist_tm_authorisation_protocols_tm_cryptographic_authentication, axiom,
    tm_authorisation_protocols != tm_cryptographic_authentication).

fof(bg_dist_tm_authorisation_protocols_tm_cryptographic_key_management, axiom,
    tm_authorisation_protocols != tm_cryptographic_key_management).

fof(bg_dist_tm_authorisation_protocols_tm_cryptographic_methods, axiom,
    tm_authorisation_protocols != tm_cryptographic_methods).

fof(bg_dist_tm_authorisation_protocols_tm_data_backup_protocols, axiom,
    tm_authorisation_protocols != tm_data_backup_protocols).

fof(bg_dist_tm_authorisation_protocols_tm_data_redaction, axiom,
    tm_authorisation_protocols != tm_data_redaction).

fof(bg_dist_tm_authorisation_protocols_tm_data_sanitisation_technique, axiom,
    tm_authorisation_protocols != tm_data_sanitisation_technique).

fof(bg_dist_tm_authorisation_protocols_tm_deidentification, axiom,
    tm_authorisation_protocols != tm_deidentification).

fof(bg_dist_tm_authorisation_protocols_tm_deterministic_pseudonymisation, axiom,
    tm_authorisation_protocols != tm_deterministic_pseudonymisation).

fof(bg_dist_tm_authorisation_protocols_tm_differential_privacy, axiom,
    tm_authorisation_protocols != tm_differential_privacy).

fof(bg_dist_tm_authorisation_protocols_tm_digital_rights_management, axiom,
    tm_authorisation_protocols != tm_digital_rights_management).

fof(bg_dist_tm_authorisation_protocols_tm_digital_signatures, axiom,
    tm_authorisation_protocols != tm_digital_signatures).

fof(bg_dist_tm_authorisation_protocols_tm_distributed_system_security, axiom,
    tm_authorisation_protocols != tm_distributed_system_security).

fof(bg_dist_tm_authorisation_protocols_tm_document_randomised_pseudonymisation, axiom,
    tm_authorisation_protocols != tm_document_randomised_pseudonymisation).

fof(bg_dist_tm_authorisation_protocols_tm_document_security, axiom,
    tm_authorisation_protocols != tm_document_security).

fof(bg_dist_tm_authorisation_protocols_tm_encryption_in_transfer, axiom,
    tm_authorisation_protocols != tm_encryption_in_transfer).

fof(bg_dist_tm_authorisation_protocols_tm_encryption_in_use, axiom,
    tm_authorisation_protocols != tm_encryption_in_use).

fof(bg_dist_tm_authorisation_protocols_tm_end_to_end_encryption, axiom,
    tm_authorisation_protocols != tm_end_to_end_encryption).

fof(bg_dist_tm_authorisation_protocols_tm_fail_safe_protocols, axiom,
    tm_authorisation_protocols != tm_fail_safe_protocols).

fof(bg_dist_tm_authorisation_protocols_tm_file_system_security, axiom,
    tm_authorisation_protocols != tm_file_system_security).

fof(bg_dist_tm_authorisation_protocols_tm_fully_randomised_pseudonymisation, axiom,
    tm_authorisation_protocols != tm_fully_randomised_pseudonymisation).

fof(bg_dist_tm_authorisation_protocols_tm_hardware_security_protocols, axiom,
    tm_authorisation_protocols != tm_hardware_security_protocols).

fof(bg_dist_tm_authorisation_protocols_tm_hash_functions, axiom,
    tm_authorisation_protocols != tm_hash_functions).

fof(bg_dist_tm_authorisation_protocols_tm_hash_message_authentication_code, axiom,
    tm_authorisation_protocols != tm_hash_message_authentication_code).

fof(bg_dist_tm_authorisation_protocols_tm_homomorphic_encryption, axiom,
    tm_authorisation_protocols != tm_homomorphic_encryption).

fof(bg_dist_tm_authorisation_protocols_tm_information_flow_control, axiom,
    tm_authorisation_protocols != tm_information_flow_control).

fof(bg_dist_tm_authorisation_protocols_tm_intrusion_detection_system, axiom,
    tm_authorisation_protocols != tm_intrusion_detection_system).

fof(bg_dist_tm_authorisation_protocols_tm_legal_measure, axiom,
    tm_authorisation_protocols != tm_legal_measure).

fof(bg_dist_tm_authorisation_protocols_tm_message_authentication_codes, axiom,
    tm_authorisation_protocols != tm_message_authentication_codes).

fof(bg_dist_tm_authorisation_protocols_tm_mobile_platform_security, axiom,
    tm_authorisation_protocols != tm_mobile_platform_security).

fof(bg_dist_tm_authorisation_protocols_tm_monotonic_counter_pseudonymisation, axiom,
    tm_authorisation_protocols != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_authorisation_protocols_tm_multi_factor_authentication, axiom,
    tm_authorisation_protocols != tm_multi_factor_authentication).

fof(bg_dist_tm_authorisation_protocols_tm_network_proxy_routing, axiom,
    tm_authorisation_protocols != tm_network_proxy_routing).

fof(bg_dist_tm_authorisation_protocols_tm_network_security_protocols, axiom,
    tm_authorisation_protocols != tm_network_security_protocols).

fof(bg_dist_tm_authorisation_protocols_tm_operating_system_security, axiom,
    tm_authorisation_protocols != tm_operating_system_security).

fof(bg_dist_tm_authorisation_protocols_tm_organisational_measure, axiom,
    tm_authorisation_protocols != tm_organisational_measure).

fof(bg_dist_tm_authorisation_protocols_tm_password_authentication, axiom,
    tm_authorisation_protocols != tm_password_authentication).

fof(bg_dist_tm_authorisation_protocols_tm_penetration_testing_methods, axiom,
    tm_authorisation_protocols != tm_penetration_testing_methods).

fof(bg_dist_tm_authorisation_protocols_tm_physical_measure, axiom,
    tm_authorisation_protocols != tm_physical_measure).

fof(bg_dist_tm_authorisation_protocols_tm_post_quantum_cryptography, axiom,
    tm_authorisation_protocols != tm_post_quantum_cryptography).

fof(bg_dist_tm_authorisation_protocols_tm_privacy_preserving_protocol, axiom,
    tm_authorisation_protocols != tm_privacy_preserving_protocol).

fof(bg_dist_tm_authorisation_protocols_tm_private_information_retrieval, axiom,
    tm_authorisation_protocols != tm_private_information_retrieval).

fof(bg_dist_tm_authorisation_protocols_tm_pseudonymisation, axiom,
    tm_authorisation_protocols != tm_pseudonymisation).

fof(bg_dist_tm_authorisation_protocols_tm_quantum_cryptography, axiom,
    tm_authorisation_protocols != tm_quantum_cryptography).

fof(bg_dist_tm_authorisation_protocols_tm_r_n_g_pseudonymisation, axiom,
    tm_authorisation_protocols != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_authorisation_protocols_tm_secret_sharing_schemes, axiom,
    tm_authorisation_protocols != tm_secret_sharing_schemes).

fof(bg_dist_tm_authorisation_protocols_tm_secure_multi_party_computation, axiom,
    tm_authorisation_protocols != tm_secure_multi_party_computation).

fof(bg_dist_tm_authorisation_protocols_tm_security_method, axiom,
    tm_authorisation_protocols != tm_security_method).

fof(bg_dist_tm_authorisation_protocols_tm_single_sign_on, axiom,
    tm_authorisation_protocols != tm_single_sign_on).

fof(bg_dist_tm_authorisation_protocols_tm_symmetric_cryptography, axiom,
    tm_authorisation_protocols != tm_symmetric_cryptography).

fof(bg_dist_tm_authorisation_protocols_tm_symmetric_encryption, axiom,
    tm_authorisation_protocols != tm_symmetric_encryption).

fof(bg_dist_tm_authorisation_protocols_tm_technical_measure, axiom,
    tm_authorisation_protocols != tm_technical_measure).

fof(bg_dist_tm_authorisation_protocols_tm_technical_organisational_measure, axiom,
    tm_authorisation_protocols != tm_technical_organisational_measure).

fof(bg_dist_tm_authorisation_protocols_tm_trusted_computing, axiom,
    tm_authorisation_protocols != tm_trusted_computing).

fof(bg_dist_tm_authorisation_protocols_tm_trusted_execution_environment, axiom,
    tm_authorisation_protocols != tm_trusted_execution_environment).

fof(bg_dist_tm_authorisation_protocols_tm_usage_control, axiom,
    tm_authorisation_protocols != tm_usage_control).

fof(bg_dist_tm_authorisation_protocols_tm_use_synthetic_data, axiom,
    tm_authorisation_protocols != tm_use_synthetic_data).

fof(bg_dist_tm_authorisation_protocols_tm_virtualisation_security, axiom,
    tm_authorisation_protocols != tm_virtualisation_security).

fof(bg_dist_tm_authorisation_protocols_tm_vulnerability_testing_methods, axiom,
    tm_authorisation_protocols != tm_vulnerability_testing_methods).

fof(bg_dist_tm_authorisation_protocols_tm_web_browser_security, axiom,
    tm_authorisation_protocols != tm_web_browser_security).

fof(bg_dist_tm_authorisation_protocols_tm_web_security_protocols, axiom,
    tm_authorisation_protocols != tm_web_security_protocols).

fof(bg_dist_tm_authorisation_protocols_tm_wireless_security_protocols, axiom,
    tm_authorisation_protocols != tm_wireless_security_protocols).

fof(bg_dist_tm_authorisation_protocols_tm_zero_knowledge_authentication, axiom,
    tm_authorisation_protocols != tm_zero_knowledge_authentication).

fof(bg_dist_tm_biometric_authentication_tm_cryptographic_authentication, axiom,
    tm_biometric_authentication != tm_cryptographic_authentication).

fof(bg_dist_tm_biometric_authentication_tm_cryptographic_key_management, axiom,
    tm_biometric_authentication != tm_cryptographic_key_management).

fof(bg_dist_tm_biometric_authentication_tm_cryptographic_methods, axiom,
    tm_biometric_authentication != tm_cryptographic_methods).

fof(bg_dist_tm_biometric_authentication_tm_data_backup_protocols, axiom,
    tm_biometric_authentication != tm_data_backup_protocols).

fof(bg_dist_tm_biometric_authentication_tm_data_redaction, axiom,
    tm_biometric_authentication != tm_data_redaction).

fof(bg_dist_tm_biometric_authentication_tm_data_sanitisation_technique, axiom,
    tm_biometric_authentication != tm_data_sanitisation_technique).

fof(bg_dist_tm_biometric_authentication_tm_deidentification, axiom,
    tm_biometric_authentication != tm_deidentification).

fof(bg_dist_tm_biometric_authentication_tm_deterministic_pseudonymisation, axiom,
    tm_biometric_authentication != tm_deterministic_pseudonymisation).

fof(bg_dist_tm_biometric_authentication_tm_differential_privacy, axiom,
    tm_biometric_authentication != tm_differential_privacy).

fof(bg_dist_tm_biometric_authentication_tm_digital_rights_management, axiom,
    tm_biometric_authentication != tm_digital_rights_management).

fof(bg_dist_tm_biometric_authentication_tm_digital_signatures, axiom,
    tm_biometric_authentication != tm_digital_signatures).

fof(bg_dist_tm_biometric_authentication_tm_distributed_system_security, axiom,
    tm_biometric_authentication != tm_distributed_system_security).

fof(bg_dist_tm_biometric_authentication_tm_document_randomised_pseudonymisation, axiom,
    tm_biometric_authentication != tm_document_randomised_pseudonymisation).

fof(bg_dist_tm_biometric_authentication_tm_document_security, axiom,
    tm_biometric_authentication != tm_document_security).

fof(bg_dist_tm_biometric_authentication_tm_encryption_in_transfer, axiom,
    tm_biometric_authentication != tm_encryption_in_transfer).

fof(bg_dist_tm_biometric_authentication_tm_encryption_in_use, axiom,
    tm_biometric_authentication != tm_encryption_in_use).

fof(bg_dist_tm_biometric_authentication_tm_end_to_end_encryption, axiom,
    tm_biometric_authentication != tm_end_to_end_encryption).

fof(bg_dist_tm_biometric_authentication_tm_fail_safe_protocols, axiom,
    tm_biometric_authentication != tm_fail_safe_protocols).

fof(bg_dist_tm_biometric_authentication_tm_file_system_security, axiom,
    tm_biometric_authentication != tm_file_system_security).

fof(bg_dist_tm_biometric_authentication_tm_fully_randomised_pseudonymisation, axiom,
    tm_biometric_authentication != tm_fully_randomised_pseudonymisation).

fof(bg_dist_tm_biometric_authentication_tm_hardware_security_protocols, axiom,
    tm_biometric_authentication != tm_hardware_security_protocols).

fof(bg_dist_tm_biometric_authentication_tm_hash_functions, axiom,
    tm_biometric_authentication != tm_hash_functions).

fof(bg_dist_tm_biometric_authentication_tm_hash_message_authentication_code, axiom,
    tm_biometric_authentication != tm_hash_message_authentication_code).

fof(bg_dist_tm_biometric_authentication_tm_homomorphic_encryption, axiom,
    tm_biometric_authentication != tm_homomorphic_encryption).

fof(bg_dist_tm_biometric_authentication_tm_information_flow_control, axiom,
    tm_biometric_authentication != tm_information_flow_control).

fof(bg_dist_tm_biometric_authentication_tm_intrusion_detection_system, axiom,
    tm_biometric_authentication != tm_intrusion_detection_system).

fof(bg_dist_tm_biometric_authentication_tm_legal_measure, axiom,
    tm_biometric_authentication != tm_legal_measure).

fof(bg_dist_tm_biometric_authentication_tm_message_authentication_codes, axiom,
    tm_biometric_authentication != tm_message_authentication_codes).

fof(bg_dist_tm_biometric_authentication_tm_mobile_platform_security, axiom,
    tm_biometric_authentication != tm_mobile_platform_security).

fof(bg_dist_tm_biometric_authentication_tm_monotonic_counter_pseudonymisation, axiom,
    tm_biometric_authentication != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_biometric_authentication_tm_multi_factor_authentication, axiom,
    tm_biometric_authentication != tm_multi_factor_authentication).

fof(bg_dist_tm_biometric_authentication_tm_network_proxy_routing, axiom,
    tm_biometric_authentication != tm_network_proxy_routing).

fof(bg_dist_tm_biometric_authentication_tm_network_security_protocols, axiom,
    tm_biometric_authentication != tm_network_security_protocols).

fof(bg_dist_tm_biometric_authentication_tm_operating_system_security, axiom,
    tm_biometric_authentication != tm_operating_system_security).

fof(bg_dist_tm_biometric_authentication_tm_organisational_measure, axiom,
    tm_biometric_authentication != tm_organisational_measure).

fof(bg_dist_tm_biometric_authentication_tm_password_authentication, axiom,
    tm_biometric_authentication != tm_password_authentication).

fof(bg_dist_tm_biometric_authentication_tm_penetration_testing_methods, axiom,
    tm_biometric_authentication != tm_penetration_testing_methods).

fof(bg_dist_tm_biometric_authentication_tm_physical_measure, axiom,
    tm_biometric_authentication != tm_physical_measure).

fof(bg_dist_tm_biometric_authentication_tm_post_quantum_cryptography, axiom,
    tm_biometric_authentication != tm_post_quantum_cryptography).

fof(bg_dist_tm_biometric_authentication_tm_privacy_preserving_protocol, axiom,
    tm_biometric_authentication != tm_privacy_preserving_protocol).

fof(bg_dist_tm_biometric_authentication_tm_private_information_retrieval, axiom,
    tm_biometric_authentication != tm_private_information_retrieval).

fof(bg_dist_tm_biometric_authentication_tm_pseudonymisation, axiom,
    tm_biometric_authentication != tm_pseudonymisation).

fof(bg_dist_tm_biometric_authentication_tm_quantum_cryptography, axiom,
    tm_biometric_authentication != tm_quantum_cryptography).

fof(bg_dist_tm_biometric_authentication_tm_r_n_g_pseudonymisation, axiom,
    tm_biometric_authentication != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_biometric_authentication_tm_secret_sharing_schemes, axiom,
    tm_biometric_authentication != tm_secret_sharing_schemes).

fof(bg_dist_tm_biometric_authentication_tm_secure_multi_party_computation, axiom,
    tm_biometric_authentication != tm_secure_multi_party_computation).

fof(bg_dist_tm_biometric_authentication_tm_security_method, axiom,
    tm_biometric_authentication != tm_security_method).

fof(bg_dist_tm_biometric_authentication_tm_single_sign_on, axiom,
    tm_biometric_authentication != tm_single_sign_on).

fof(bg_dist_tm_biometric_authentication_tm_symmetric_cryptography, axiom,
    tm_biometric_authentication != tm_symmetric_cryptography).

fof(bg_dist_tm_biometric_authentication_tm_symmetric_encryption, axiom,
    tm_biometric_authentication != tm_symmetric_encryption).

fof(bg_dist_tm_biometric_authentication_tm_technical_measure, axiom,
    tm_biometric_authentication != tm_technical_measure).

fof(bg_dist_tm_biometric_authentication_tm_technical_organisational_measure, axiom,
    tm_biometric_authentication != tm_technical_organisational_measure).

fof(bg_dist_tm_biometric_authentication_tm_trusted_computing, axiom,
    tm_biometric_authentication != tm_trusted_computing).

fof(bg_dist_tm_biometric_authentication_tm_trusted_execution_environment, axiom,
    tm_biometric_authentication != tm_trusted_execution_environment).

fof(bg_dist_tm_biometric_authentication_tm_usage_control, axiom,
    tm_biometric_authentication != tm_usage_control).

fof(bg_dist_tm_biometric_authentication_tm_use_synthetic_data, axiom,
    tm_biometric_authentication != tm_use_synthetic_data).

fof(bg_dist_tm_biometric_authentication_tm_virtualisation_security, axiom,
    tm_biometric_authentication != tm_virtualisation_security).

fof(bg_dist_tm_biometric_authentication_tm_vulnerability_testing_methods, axiom,
    tm_biometric_authentication != tm_vulnerability_testing_methods).

fof(bg_dist_tm_biometric_authentication_tm_web_browser_security, axiom,
    tm_biometric_authentication != tm_web_browser_security).

fof(bg_dist_tm_biometric_authentication_tm_web_security_protocols, axiom,
    tm_biometric_authentication != tm_web_security_protocols).

fof(bg_dist_tm_biometric_authentication_tm_wireless_security_protocols, axiom,
    tm_biometric_authentication != tm_wireless_security_protocols).

fof(bg_dist_tm_biometric_authentication_tm_zero_knowledge_authentication, axiom,
    tm_biometric_authentication != tm_zero_knowledge_authentication).

fof(bg_dist_tm_cryptographic_authentication_tm_cryptographic_key_management, axiom,
    tm_cryptographic_authentication != tm_cryptographic_key_management).

fof(bg_dist_tm_cryptographic_authentication_tm_cryptographic_methods, axiom,
    tm_cryptographic_authentication != tm_cryptographic_methods).

fof(bg_dist_tm_cryptographic_authentication_tm_data_backup_protocols, axiom,
    tm_cryptographic_authentication != tm_data_backup_protocols).

fof(bg_dist_tm_cryptographic_authentication_tm_data_redaction, axiom,
    tm_cryptographic_authentication != tm_data_redaction).

fof(bg_dist_tm_cryptographic_authentication_tm_data_sanitisation_technique, axiom,
    tm_cryptographic_authentication != tm_data_sanitisation_technique).

fof(bg_dist_tm_cryptographic_authentication_tm_deidentification, axiom,
    tm_cryptographic_authentication != tm_deidentification).

fof(bg_dist_tm_cryptographic_authentication_tm_deterministic_pseudonymisation, axiom,
    tm_cryptographic_authentication != tm_deterministic_pseudonymisation).

fof(bg_dist_tm_cryptographic_authentication_tm_differential_privacy, axiom,
    tm_cryptographic_authentication != tm_differential_privacy).

fof(bg_dist_tm_cryptographic_authentication_tm_digital_rights_management, axiom,
    tm_cryptographic_authentication != tm_digital_rights_management).

fof(bg_dist_tm_cryptographic_authentication_tm_digital_signatures, axiom,
    tm_cryptographic_authentication != tm_digital_signatures).

fof(bg_dist_tm_cryptographic_authentication_tm_distributed_system_security, axiom,
    tm_cryptographic_authentication != tm_distributed_system_security).

fof(bg_dist_tm_cryptographic_authentication_tm_document_randomised_pseudonymisation, axiom,
    tm_cryptographic_authentication != tm_document_randomised_pseudonymisation).

fof(bg_dist_tm_cryptographic_authentication_tm_document_security, axiom,
    tm_cryptographic_authentication != tm_document_security).

fof(bg_dist_tm_cryptographic_authentication_tm_encryption_in_transfer, axiom,
    tm_cryptographic_authentication != tm_encryption_in_transfer).

fof(bg_dist_tm_cryptographic_authentication_tm_encryption_in_use, axiom,
    tm_cryptographic_authentication != tm_encryption_in_use).

fof(bg_dist_tm_cryptographic_authentication_tm_end_to_end_encryption, axiom,
    tm_cryptographic_authentication != tm_end_to_end_encryption).

fof(bg_dist_tm_cryptographic_authentication_tm_fail_safe_protocols, axiom,
    tm_cryptographic_authentication != tm_fail_safe_protocols).

fof(bg_dist_tm_cryptographic_authentication_tm_file_system_security, axiom,
    tm_cryptographic_authentication != tm_file_system_security).

fof(bg_dist_tm_cryptographic_authentication_tm_fully_randomised_pseudonymisation, axiom,
    tm_cryptographic_authentication != tm_fully_randomised_pseudonymisation).

fof(bg_dist_tm_cryptographic_authentication_tm_hardware_security_protocols, axiom,
    tm_cryptographic_authentication != tm_hardware_security_protocols).

fof(bg_dist_tm_cryptographic_authentication_tm_hash_functions, axiom,
    tm_cryptographic_authentication != tm_hash_functions).

fof(bg_dist_tm_cryptographic_authentication_tm_hash_message_authentication_code, axiom,
    tm_cryptographic_authentication != tm_hash_message_authentication_code).

fof(bg_dist_tm_cryptographic_authentication_tm_homomorphic_encryption, axiom,
    tm_cryptographic_authentication != tm_homomorphic_encryption).

fof(bg_dist_tm_cryptographic_authentication_tm_information_flow_control, axiom,
    tm_cryptographic_authentication != tm_information_flow_control).

fof(bg_dist_tm_cryptographic_authentication_tm_intrusion_detection_system, axiom,
    tm_cryptographic_authentication != tm_intrusion_detection_system).

fof(bg_dist_tm_cryptographic_authentication_tm_legal_measure, axiom,
    tm_cryptographic_authentication != tm_legal_measure).

fof(bg_dist_tm_cryptographic_authentication_tm_message_authentication_codes, axiom,
    tm_cryptographic_authentication != tm_message_authentication_codes).

fof(bg_dist_tm_cryptographic_authentication_tm_mobile_platform_security, axiom,
    tm_cryptographic_authentication != tm_mobile_platform_security).

fof(bg_dist_tm_cryptographic_authentication_tm_monotonic_counter_pseudonymisation, axiom,
    tm_cryptographic_authentication != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_cryptographic_authentication_tm_multi_factor_authentication, axiom,
    tm_cryptographic_authentication != tm_multi_factor_authentication).

fof(bg_dist_tm_cryptographic_authentication_tm_network_proxy_routing, axiom,
    tm_cryptographic_authentication != tm_network_proxy_routing).

fof(bg_dist_tm_cryptographic_authentication_tm_network_security_protocols, axiom,
    tm_cryptographic_authentication != tm_network_security_protocols).

fof(bg_dist_tm_cryptographic_authentication_tm_operating_system_security, axiom,
    tm_cryptographic_authentication != tm_operating_system_security).

fof(bg_dist_tm_cryptographic_authentication_tm_organisational_measure, axiom,
    tm_cryptographic_authentication != tm_organisational_measure).

fof(bg_dist_tm_cryptographic_authentication_tm_password_authentication, axiom,
    tm_cryptographic_authentication != tm_password_authentication).

fof(bg_dist_tm_cryptographic_authentication_tm_penetration_testing_methods, axiom,
    tm_cryptographic_authentication != tm_penetration_testing_methods).

fof(bg_dist_tm_cryptographic_authentication_tm_physical_measure, axiom,
    tm_cryptographic_authentication != tm_physical_measure).

fof(bg_dist_tm_cryptographic_authentication_tm_post_quantum_cryptography, axiom,
    tm_cryptographic_authentication != tm_post_quantum_cryptography).

fof(bg_dist_tm_cryptographic_authentication_tm_privacy_preserving_protocol, axiom,
    tm_cryptographic_authentication != tm_privacy_preserving_protocol).

fof(bg_dist_tm_cryptographic_authentication_tm_private_information_retrieval, axiom,
    tm_cryptographic_authentication != tm_private_information_retrieval).

fof(bg_dist_tm_cryptographic_authentication_tm_pseudonymisation, axiom,
    tm_cryptographic_authentication != tm_pseudonymisation).

fof(bg_dist_tm_cryptographic_authentication_tm_quantum_cryptography, axiom,
    tm_cryptographic_authentication != tm_quantum_cryptography).

fof(bg_dist_tm_cryptographic_authentication_tm_r_n_g_pseudonymisation, axiom,
    tm_cryptographic_authentication != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_cryptographic_authentication_tm_secret_sharing_schemes, axiom,
    tm_cryptographic_authentication != tm_secret_sharing_schemes).

fof(bg_dist_tm_cryptographic_authentication_tm_secure_multi_party_computation, axiom,
    tm_cryptographic_authentication != tm_secure_multi_party_computation).

fof(bg_dist_tm_cryptographic_authentication_tm_security_method, axiom,
    tm_cryptographic_authentication != tm_security_method).

fof(bg_dist_tm_cryptographic_authentication_tm_single_sign_on, axiom,
    tm_cryptographic_authentication != tm_single_sign_on).

fof(bg_dist_tm_cryptographic_authentication_tm_symmetric_cryptography, axiom,
    tm_cryptographic_authentication != tm_symmetric_cryptography).

fof(bg_dist_tm_cryptographic_authentication_tm_symmetric_encryption, axiom,
    tm_cryptographic_authentication != tm_symmetric_encryption).

fof(bg_dist_tm_cryptographic_authentication_tm_technical_measure, axiom,
    tm_cryptographic_authentication != tm_technical_measure).

fof(bg_dist_tm_cryptographic_authentication_tm_technical_organisational_measure, axiom,
    tm_cryptographic_authentication != tm_technical_organisational_measure).

fof(bg_dist_tm_cryptographic_authentication_tm_trusted_computing, axiom,
    tm_cryptographic_authentication != tm_trusted_computing).

fof(bg_dist_tm_cryptographic_authentication_tm_trusted_execution_environment, axiom,
    tm_cryptographic_authentication != tm_trusted_execution_environment).

fof(bg_dist_tm_cryptographic_authentication_tm_usage_control, axiom,
    tm_cryptographic_authentication != tm_usage_control).

fof(bg_dist_tm_cryptographic_authentication_tm_use_synthetic_data, axiom,
    tm_cryptographic_authentication != tm_use_synthetic_data).

fof(bg_dist_tm_cryptographic_authentication_tm_virtualisation_security, axiom,
    tm_cryptographic_authentication != tm_virtualisation_security).

fof(bg_dist_tm_cryptographic_authentication_tm_vulnerability_testing_methods, axiom,
    tm_cryptographic_authentication != tm_vulnerability_testing_methods).

fof(bg_dist_tm_cryptographic_authentication_tm_web_browser_security, axiom,
    tm_cryptographic_authentication != tm_web_browser_security).

fof(bg_dist_tm_cryptographic_authentication_tm_web_security_protocols, axiom,
    tm_cryptographic_authentication != tm_web_security_protocols).

fof(bg_dist_tm_cryptographic_authentication_tm_wireless_security_protocols, axiom,
    tm_cryptographic_authentication != tm_wireless_security_protocols).

fof(bg_dist_tm_cryptographic_authentication_tm_zero_knowledge_authentication, axiom,
    tm_cryptographic_authentication != tm_zero_knowledge_authentication).

fof(bg_dist_tm_cryptographic_key_management_tm_cryptographic_methods, axiom,
    tm_cryptographic_key_management != tm_cryptographic_methods).

fof(bg_dist_tm_cryptographic_key_management_tm_data_backup_protocols, axiom,
    tm_cryptographic_key_management != tm_data_backup_protocols).

fof(bg_dist_tm_cryptographic_key_management_tm_data_redaction, axiom,
    tm_cryptographic_key_management != tm_data_redaction).

fof(bg_dist_tm_cryptographic_key_management_tm_data_sanitisation_technique, axiom,
    tm_cryptographic_key_management != tm_data_sanitisation_technique).

fof(bg_dist_tm_cryptographic_key_management_tm_deidentification, axiom,
    tm_cryptographic_key_management != tm_deidentification).

fof(bg_dist_tm_cryptographic_key_management_tm_deterministic_pseudonymisation, axiom,
    tm_cryptographic_key_management != tm_deterministic_pseudonymisation).

fof(bg_dist_tm_cryptographic_key_management_tm_differential_privacy, axiom,
    tm_cryptographic_key_management != tm_differential_privacy).

fof(bg_dist_tm_cryptographic_key_management_tm_digital_rights_management, axiom,
    tm_cryptographic_key_management != tm_digital_rights_management).

fof(bg_dist_tm_cryptographic_key_management_tm_digital_signatures, axiom,
    tm_cryptographic_key_management != tm_digital_signatures).

fof(bg_dist_tm_cryptographic_key_management_tm_distributed_system_security, axiom,
    tm_cryptographic_key_management != tm_distributed_system_security).

fof(bg_dist_tm_cryptographic_key_management_tm_document_randomised_pseudonymisation, axiom,
    tm_cryptographic_key_management != tm_document_randomised_pseudonymisation).

fof(bg_dist_tm_cryptographic_key_management_tm_document_security, axiom,
    tm_cryptographic_key_management != tm_document_security).

fof(bg_dist_tm_cryptographic_key_management_tm_encryption_in_transfer, axiom,
    tm_cryptographic_key_management != tm_encryption_in_transfer).

fof(bg_dist_tm_cryptographic_key_management_tm_encryption_in_use, axiom,
    tm_cryptographic_key_management != tm_encryption_in_use).

fof(bg_dist_tm_cryptographic_key_management_tm_end_to_end_encryption, axiom,
    tm_cryptographic_key_management != tm_end_to_end_encryption).

fof(bg_dist_tm_cryptographic_key_management_tm_fail_safe_protocols, axiom,
    tm_cryptographic_key_management != tm_fail_safe_protocols).

fof(bg_dist_tm_cryptographic_key_management_tm_file_system_security, axiom,
    tm_cryptographic_key_management != tm_file_system_security).

fof(bg_dist_tm_cryptographic_key_management_tm_fully_randomised_pseudonymisation, axiom,
    tm_cryptographic_key_management != tm_fully_randomised_pseudonymisation).

fof(bg_dist_tm_cryptographic_key_management_tm_hardware_security_protocols, axiom,
    tm_cryptographic_key_management != tm_hardware_security_protocols).

fof(bg_dist_tm_cryptographic_key_management_tm_hash_functions, axiom,
    tm_cryptographic_key_management != tm_hash_functions).

fof(bg_dist_tm_cryptographic_key_management_tm_hash_message_authentication_code, axiom,
    tm_cryptographic_key_management != tm_hash_message_authentication_code).

fof(bg_dist_tm_cryptographic_key_management_tm_homomorphic_encryption, axiom,
    tm_cryptographic_key_management != tm_homomorphic_encryption).

fof(bg_dist_tm_cryptographic_key_management_tm_information_flow_control, axiom,
    tm_cryptographic_key_management != tm_information_flow_control).

fof(bg_dist_tm_cryptographic_key_management_tm_intrusion_detection_system, axiom,
    tm_cryptographic_key_management != tm_intrusion_detection_system).

fof(bg_dist_tm_cryptographic_key_management_tm_legal_measure, axiom,
    tm_cryptographic_key_management != tm_legal_measure).

fof(bg_dist_tm_cryptographic_key_management_tm_message_authentication_codes, axiom,
    tm_cryptographic_key_management != tm_message_authentication_codes).

fof(bg_dist_tm_cryptographic_key_management_tm_mobile_platform_security, axiom,
    tm_cryptographic_key_management != tm_mobile_platform_security).

fof(bg_dist_tm_cryptographic_key_management_tm_monotonic_counter_pseudonymisation, axiom,
    tm_cryptographic_key_management != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_cryptographic_key_management_tm_multi_factor_authentication, axiom,
    tm_cryptographic_key_management != tm_multi_factor_authentication).

fof(bg_dist_tm_cryptographic_key_management_tm_network_proxy_routing, axiom,
    tm_cryptographic_key_management != tm_network_proxy_routing).

fof(bg_dist_tm_cryptographic_key_management_tm_network_security_protocols, axiom,
    tm_cryptographic_key_management != tm_network_security_protocols).

fof(bg_dist_tm_cryptographic_key_management_tm_operating_system_security, axiom,
    tm_cryptographic_key_management != tm_operating_system_security).

fof(bg_dist_tm_cryptographic_key_management_tm_organisational_measure, axiom,
    tm_cryptographic_key_management != tm_organisational_measure).

fof(bg_dist_tm_cryptographic_key_management_tm_password_authentication, axiom,
    tm_cryptographic_key_management != tm_password_authentication).

fof(bg_dist_tm_cryptographic_key_management_tm_penetration_testing_methods, axiom,
    tm_cryptographic_key_management != tm_penetration_testing_methods).

fof(bg_dist_tm_cryptographic_key_management_tm_physical_measure, axiom,
    tm_cryptographic_key_management != tm_physical_measure).

fof(bg_dist_tm_cryptographic_key_management_tm_post_quantum_cryptography, axiom,
    tm_cryptographic_key_management != tm_post_quantum_cryptography).

fof(bg_dist_tm_cryptographic_key_management_tm_privacy_preserving_protocol, axiom,
    tm_cryptographic_key_management != tm_privacy_preserving_protocol).

fof(bg_dist_tm_cryptographic_key_management_tm_private_information_retrieval, axiom,
    tm_cryptographic_key_management != tm_private_information_retrieval).

fof(bg_dist_tm_cryptographic_key_management_tm_pseudonymisation, axiom,
    tm_cryptographic_key_management != tm_pseudonymisation).

fof(bg_dist_tm_cryptographic_key_management_tm_quantum_cryptography, axiom,
    tm_cryptographic_key_management != tm_quantum_cryptography).

fof(bg_dist_tm_cryptographic_key_management_tm_r_n_g_pseudonymisation, axiom,
    tm_cryptographic_key_management != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_cryptographic_key_management_tm_secret_sharing_schemes, axiom,
    tm_cryptographic_key_management != tm_secret_sharing_schemes).

fof(bg_dist_tm_cryptographic_key_management_tm_secure_multi_party_computation, axiom,
    tm_cryptographic_key_management != tm_secure_multi_party_computation).

fof(bg_dist_tm_cryptographic_key_management_tm_security_method, axiom,
    tm_cryptographic_key_management != tm_security_method).

fof(bg_dist_tm_cryptographic_key_management_tm_single_sign_on, axiom,
    tm_cryptographic_key_management != tm_single_sign_on).

fof(bg_dist_tm_cryptographic_key_management_tm_symmetric_cryptography, axiom,
    tm_cryptographic_key_management != tm_symmetric_cryptography).

fof(bg_dist_tm_cryptographic_key_management_tm_symmetric_encryption, axiom,
    tm_cryptographic_key_management != tm_symmetric_encryption).

fof(bg_dist_tm_cryptographic_key_management_tm_technical_measure, axiom,
    tm_cryptographic_key_management != tm_technical_measure).

fof(bg_dist_tm_cryptographic_key_management_tm_technical_organisational_measure, axiom,
    tm_cryptographic_key_management != tm_technical_organisational_measure).

fof(bg_dist_tm_cryptographic_key_management_tm_trusted_computing, axiom,
    tm_cryptographic_key_management != tm_trusted_computing).

fof(bg_dist_tm_cryptographic_key_management_tm_trusted_execution_environment, axiom,
    tm_cryptographic_key_management != tm_trusted_execution_environment).

fof(bg_dist_tm_cryptographic_key_management_tm_usage_control, axiom,
    tm_cryptographic_key_management != tm_usage_control).

fof(bg_dist_tm_cryptographic_key_management_tm_use_synthetic_data, axiom,
    tm_cryptographic_key_management != tm_use_synthetic_data).

fof(bg_dist_tm_cryptographic_key_management_tm_virtualisation_security, axiom,
    tm_cryptographic_key_management != tm_virtualisation_security).

fof(bg_dist_tm_cryptographic_key_management_tm_vulnerability_testing_methods, axiom,
    tm_cryptographic_key_management != tm_vulnerability_testing_methods).

fof(bg_dist_tm_cryptographic_key_management_tm_web_browser_security, axiom,
    tm_cryptographic_key_management != tm_web_browser_security).

fof(bg_dist_tm_cryptographic_key_management_tm_web_security_protocols, axiom,
    tm_cryptographic_key_management != tm_web_security_protocols).

fof(bg_dist_tm_cryptographic_key_management_tm_wireless_security_protocols, axiom,
    tm_cryptographic_key_management != tm_wireless_security_protocols).

fof(bg_dist_tm_cryptographic_key_management_tm_zero_knowledge_authentication, axiom,
    tm_cryptographic_key_management != tm_zero_knowledge_authentication).

fof(bg_dist_tm_cryptographic_methods_tm_data_backup_protocols, axiom,
    tm_cryptographic_methods != tm_data_backup_protocols).

fof(bg_dist_tm_cryptographic_methods_tm_data_redaction, axiom,
    tm_cryptographic_methods != tm_data_redaction).

fof(bg_dist_tm_cryptographic_methods_tm_data_sanitisation_technique, axiom,
    tm_cryptographic_methods != tm_data_sanitisation_technique).

fof(bg_dist_tm_cryptographic_methods_tm_deidentification, axiom,
    tm_cryptographic_methods != tm_deidentification).

fof(bg_dist_tm_cryptographic_methods_tm_deterministic_pseudonymisation, axiom,
    tm_cryptographic_methods != tm_deterministic_pseudonymisation).

fof(bg_dist_tm_cryptographic_methods_tm_differential_privacy, axiom,
    tm_cryptographic_methods != tm_differential_privacy).

fof(bg_dist_tm_cryptographic_methods_tm_digital_rights_management, axiom,
    tm_cryptographic_methods != tm_digital_rights_management).

fof(bg_dist_tm_cryptographic_methods_tm_digital_signatures, axiom,
    tm_cryptographic_methods != tm_digital_signatures).

fof(bg_dist_tm_cryptographic_methods_tm_distributed_system_security, axiom,
    tm_cryptographic_methods != tm_distributed_system_security).

fof(bg_dist_tm_cryptographic_methods_tm_document_randomised_pseudonymisation, axiom,
    tm_cryptographic_methods != tm_document_randomised_pseudonymisation).

fof(bg_dist_tm_cryptographic_methods_tm_document_security, axiom,
    tm_cryptographic_methods != tm_document_security).

fof(bg_dist_tm_cryptographic_methods_tm_encryption_in_transfer, axiom,
    tm_cryptographic_methods != tm_encryption_in_transfer).

fof(bg_dist_tm_cryptographic_methods_tm_encryption_in_use, axiom,
    tm_cryptographic_methods != tm_encryption_in_use).

fof(bg_dist_tm_cryptographic_methods_tm_end_to_end_encryption, axiom,
    tm_cryptographic_methods != tm_end_to_end_encryption).

fof(bg_dist_tm_cryptographic_methods_tm_fail_safe_protocols, axiom,
    tm_cryptographic_methods != tm_fail_safe_protocols).

fof(bg_dist_tm_cryptographic_methods_tm_file_system_security, axiom,
    tm_cryptographic_methods != tm_file_system_security).

fof(bg_dist_tm_cryptographic_methods_tm_fully_randomised_pseudonymisation, axiom,
    tm_cryptographic_methods != tm_fully_randomised_pseudonymisation).

fof(bg_dist_tm_cryptographic_methods_tm_hardware_security_protocols, axiom,
    tm_cryptographic_methods != tm_hardware_security_protocols).

fof(bg_dist_tm_cryptographic_methods_tm_hash_functions, axiom,
    tm_cryptographic_methods != tm_hash_functions).

fof(bg_dist_tm_cryptographic_methods_tm_hash_message_authentication_code, axiom,
    tm_cryptographic_methods != tm_hash_message_authentication_code).

fof(bg_dist_tm_cryptographic_methods_tm_homomorphic_encryption, axiom,
    tm_cryptographic_methods != tm_homomorphic_encryption).

fof(bg_dist_tm_cryptographic_methods_tm_information_flow_control, axiom,
    tm_cryptographic_methods != tm_information_flow_control).

fof(bg_dist_tm_cryptographic_methods_tm_intrusion_detection_system, axiom,
    tm_cryptographic_methods != tm_intrusion_detection_system).

fof(bg_dist_tm_cryptographic_methods_tm_legal_measure, axiom,
    tm_cryptographic_methods != tm_legal_measure).

fof(bg_dist_tm_cryptographic_methods_tm_message_authentication_codes, axiom,
    tm_cryptographic_methods != tm_message_authentication_codes).

fof(bg_dist_tm_cryptographic_methods_tm_mobile_platform_security, axiom,
    tm_cryptographic_methods != tm_mobile_platform_security).

fof(bg_dist_tm_cryptographic_methods_tm_monotonic_counter_pseudonymisation, axiom,
    tm_cryptographic_methods != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_cryptographic_methods_tm_multi_factor_authentication, axiom,
    tm_cryptographic_methods != tm_multi_factor_authentication).

fof(bg_dist_tm_cryptographic_methods_tm_network_proxy_routing, axiom,
    tm_cryptographic_methods != tm_network_proxy_routing).

fof(bg_dist_tm_cryptographic_methods_tm_network_security_protocols, axiom,
    tm_cryptographic_methods != tm_network_security_protocols).

fof(bg_dist_tm_cryptographic_methods_tm_operating_system_security, axiom,
    tm_cryptographic_methods != tm_operating_system_security).

fof(bg_dist_tm_cryptographic_methods_tm_organisational_measure, axiom,
    tm_cryptographic_methods != tm_organisational_measure).

fof(bg_dist_tm_cryptographic_methods_tm_password_authentication, axiom,
    tm_cryptographic_methods != tm_password_authentication).

fof(bg_dist_tm_cryptographic_methods_tm_penetration_testing_methods, axiom,
    tm_cryptographic_methods != tm_penetration_testing_methods).

fof(bg_dist_tm_cryptographic_methods_tm_physical_measure, axiom,
    tm_cryptographic_methods != tm_physical_measure).

fof(bg_dist_tm_cryptographic_methods_tm_post_quantum_cryptography, axiom,
    tm_cryptographic_methods != tm_post_quantum_cryptography).

fof(bg_dist_tm_cryptographic_methods_tm_privacy_preserving_protocol, axiom,
    tm_cryptographic_methods != tm_privacy_preserving_protocol).

fof(bg_dist_tm_cryptographic_methods_tm_private_information_retrieval, axiom,
    tm_cryptographic_methods != tm_private_information_retrieval).

fof(bg_dist_tm_cryptographic_methods_tm_pseudonymisation, axiom,
    tm_cryptographic_methods != tm_pseudonymisation).

fof(bg_dist_tm_cryptographic_methods_tm_quantum_cryptography, axiom,
    tm_cryptographic_methods != tm_quantum_cryptography).

fof(bg_dist_tm_cryptographic_methods_tm_r_n_g_pseudonymisation, axiom,
    tm_cryptographic_methods != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_cryptographic_methods_tm_secret_sharing_schemes, axiom,
    tm_cryptographic_methods != tm_secret_sharing_schemes).

fof(bg_dist_tm_cryptographic_methods_tm_secure_multi_party_computation, axiom,
    tm_cryptographic_methods != tm_secure_multi_party_computation).

fof(bg_dist_tm_cryptographic_methods_tm_security_method, axiom,
    tm_cryptographic_methods != tm_security_method).

fof(bg_dist_tm_cryptographic_methods_tm_single_sign_on, axiom,
    tm_cryptographic_methods != tm_single_sign_on).

fof(bg_dist_tm_cryptographic_methods_tm_symmetric_cryptography, axiom,
    tm_cryptographic_methods != tm_symmetric_cryptography).

fof(bg_dist_tm_cryptographic_methods_tm_symmetric_encryption, axiom,
    tm_cryptographic_methods != tm_symmetric_encryption).

fof(bg_dist_tm_cryptographic_methods_tm_technical_measure, axiom,
    tm_cryptographic_methods != tm_technical_measure).

fof(bg_dist_tm_cryptographic_methods_tm_technical_organisational_measure, axiom,
    tm_cryptographic_methods != tm_technical_organisational_measure).

fof(bg_dist_tm_cryptographic_methods_tm_trusted_computing, axiom,
    tm_cryptographic_methods != tm_trusted_computing).

fof(bg_dist_tm_cryptographic_methods_tm_trusted_execution_environment, axiom,
    tm_cryptographic_methods != tm_trusted_execution_environment).

fof(bg_dist_tm_cryptographic_methods_tm_usage_control, axiom,
    tm_cryptographic_methods != tm_usage_control).

fof(bg_dist_tm_cryptographic_methods_tm_use_synthetic_data, axiom,
    tm_cryptographic_methods != tm_use_synthetic_data).

fof(bg_dist_tm_cryptographic_methods_tm_virtualisation_security, axiom,
    tm_cryptographic_methods != tm_virtualisation_security).

fof(bg_dist_tm_cryptographic_methods_tm_vulnerability_testing_methods, axiom,
    tm_cryptographic_methods != tm_vulnerability_testing_methods).

fof(bg_dist_tm_cryptographic_methods_tm_web_browser_security, axiom,
    tm_cryptographic_methods != tm_web_browser_security).

fof(bg_dist_tm_cryptographic_methods_tm_web_security_protocols, axiom,
    tm_cryptographic_methods != tm_web_security_protocols).

fof(bg_dist_tm_cryptographic_methods_tm_wireless_security_protocols, axiom,
    tm_cryptographic_methods != tm_wireless_security_protocols).

fof(bg_dist_tm_cryptographic_methods_tm_zero_knowledge_authentication, axiom,
    tm_cryptographic_methods != tm_zero_knowledge_authentication).

fof(bg_dist_tm_data_backup_protocols_tm_data_redaction, axiom,
    tm_data_backup_protocols != tm_data_redaction).

fof(bg_dist_tm_data_backup_protocols_tm_data_sanitisation_technique, axiom,
    tm_data_backup_protocols != tm_data_sanitisation_technique).

fof(bg_dist_tm_data_backup_protocols_tm_deidentification, axiom,
    tm_data_backup_protocols != tm_deidentification).

fof(bg_dist_tm_data_backup_protocols_tm_deterministic_pseudonymisation, axiom,
    tm_data_backup_protocols != tm_deterministic_pseudonymisation).

fof(bg_dist_tm_data_backup_protocols_tm_differential_privacy, axiom,
    tm_data_backup_protocols != tm_differential_privacy).

fof(bg_dist_tm_data_backup_protocols_tm_digital_rights_management, axiom,
    tm_data_backup_protocols != tm_digital_rights_management).

fof(bg_dist_tm_data_backup_protocols_tm_digital_signatures, axiom,
    tm_data_backup_protocols != tm_digital_signatures).

fof(bg_dist_tm_data_backup_protocols_tm_distributed_system_security, axiom,
    tm_data_backup_protocols != tm_distributed_system_security).

fof(bg_dist_tm_data_backup_protocols_tm_document_randomised_pseudonymisation, axiom,
    tm_data_backup_protocols != tm_document_randomised_pseudonymisation).

fof(bg_dist_tm_data_backup_protocols_tm_document_security, axiom,
    tm_data_backup_protocols != tm_document_security).

fof(bg_dist_tm_data_backup_protocols_tm_encryption_in_transfer, axiom,
    tm_data_backup_protocols != tm_encryption_in_transfer).

fof(bg_dist_tm_data_backup_protocols_tm_encryption_in_use, axiom,
    tm_data_backup_protocols != tm_encryption_in_use).

fof(bg_dist_tm_data_backup_protocols_tm_end_to_end_encryption, axiom,
    tm_data_backup_protocols != tm_end_to_end_encryption).

fof(bg_dist_tm_data_backup_protocols_tm_fail_safe_protocols, axiom,
    tm_data_backup_protocols != tm_fail_safe_protocols).

fof(bg_dist_tm_data_backup_protocols_tm_file_system_security, axiom,
    tm_data_backup_protocols != tm_file_system_security).

fof(bg_dist_tm_data_backup_protocols_tm_fully_randomised_pseudonymisation, axiom,
    tm_data_backup_protocols != tm_fully_randomised_pseudonymisation).

fof(bg_dist_tm_data_backup_protocols_tm_hardware_security_protocols, axiom,
    tm_data_backup_protocols != tm_hardware_security_protocols).

fof(bg_dist_tm_data_backup_protocols_tm_hash_functions, axiom,
    tm_data_backup_protocols != tm_hash_functions).

fof(bg_dist_tm_data_backup_protocols_tm_hash_message_authentication_code, axiom,
    tm_data_backup_protocols != tm_hash_message_authentication_code).

fof(bg_dist_tm_data_backup_protocols_tm_homomorphic_encryption, axiom,
    tm_data_backup_protocols != tm_homomorphic_encryption).

fof(bg_dist_tm_data_backup_protocols_tm_information_flow_control, axiom,
    tm_data_backup_protocols != tm_information_flow_control).

fof(bg_dist_tm_data_backup_protocols_tm_intrusion_detection_system, axiom,
    tm_data_backup_protocols != tm_intrusion_detection_system).

fof(bg_dist_tm_data_backup_protocols_tm_legal_measure, axiom,
    tm_data_backup_protocols != tm_legal_measure).

fof(bg_dist_tm_data_backup_protocols_tm_message_authentication_codes, axiom,
    tm_data_backup_protocols != tm_message_authentication_codes).

fof(bg_dist_tm_data_backup_protocols_tm_mobile_platform_security, axiom,
    tm_data_backup_protocols != tm_mobile_platform_security).

fof(bg_dist_tm_data_backup_protocols_tm_monotonic_counter_pseudonymisation, axiom,
    tm_data_backup_protocols != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_data_backup_protocols_tm_multi_factor_authentication, axiom,
    tm_data_backup_protocols != tm_multi_factor_authentication).

fof(bg_dist_tm_data_backup_protocols_tm_network_proxy_routing, axiom,
    tm_data_backup_protocols != tm_network_proxy_routing).

fof(bg_dist_tm_data_backup_protocols_tm_network_security_protocols, axiom,
    tm_data_backup_protocols != tm_network_security_protocols).

fof(bg_dist_tm_data_backup_protocols_tm_operating_system_security, axiom,
    tm_data_backup_protocols != tm_operating_system_security).

fof(bg_dist_tm_data_backup_protocols_tm_organisational_measure, axiom,
    tm_data_backup_protocols != tm_organisational_measure).

fof(bg_dist_tm_data_backup_protocols_tm_password_authentication, axiom,
    tm_data_backup_protocols != tm_password_authentication).

fof(bg_dist_tm_data_backup_protocols_tm_penetration_testing_methods, axiom,
    tm_data_backup_protocols != tm_penetration_testing_methods).

fof(bg_dist_tm_data_backup_protocols_tm_physical_measure, axiom,
    tm_data_backup_protocols != tm_physical_measure).

fof(bg_dist_tm_data_backup_protocols_tm_post_quantum_cryptography, axiom,
    tm_data_backup_protocols != tm_post_quantum_cryptography).

fof(bg_dist_tm_data_backup_protocols_tm_privacy_preserving_protocol, axiom,
    tm_data_backup_protocols != tm_privacy_preserving_protocol).

fof(bg_dist_tm_data_backup_protocols_tm_private_information_retrieval, axiom,
    tm_data_backup_protocols != tm_private_information_retrieval).

fof(bg_dist_tm_data_backup_protocols_tm_pseudonymisation, axiom,
    tm_data_backup_protocols != tm_pseudonymisation).

fof(bg_dist_tm_data_backup_protocols_tm_quantum_cryptography, axiom,
    tm_data_backup_protocols != tm_quantum_cryptography).

fof(bg_dist_tm_data_backup_protocols_tm_r_n_g_pseudonymisation, axiom,
    tm_data_backup_protocols != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_data_backup_protocols_tm_secret_sharing_schemes, axiom,
    tm_data_backup_protocols != tm_secret_sharing_schemes).

fof(bg_dist_tm_data_backup_protocols_tm_secure_multi_party_computation, axiom,
    tm_data_backup_protocols != tm_secure_multi_party_computation).

fof(bg_dist_tm_data_backup_protocols_tm_security_method, axiom,
    tm_data_backup_protocols != tm_security_method).

fof(bg_dist_tm_data_backup_protocols_tm_single_sign_on, axiom,
    tm_data_backup_protocols != tm_single_sign_on).

fof(bg_dist_tm_data_backup_protocols_tm_symmetric_cryptography, axiom,
    tm_data_backup_protocols != tm_symmetric_cryptography).

fof(bg_dist_tm_data_backup_protocols_tm_symmetric_encryption, axiom,
    tm_data_backup_protocols != tm_symmetric_encryption).

fof(bg_dist_tm_data_backup_protocols_tm_technical_measure, axiom,
    tm_data_backup_protocols != tm_technical_measure).

fof(bg_dist_tm_data_backup_protocols_tm_technical_organisational_measure, axiom,
    tm_data_backup_protocols != tm_technical_organisational_measure).

fof(bg_dist_tm_data_backup_protocols_tm_trusted_computing, axiom,
    tm_data_backup_protocols != tm_trusted_computing).

fof(bg_dist_tm_data_backup_protocols_tm_trusted_execution_environment, axiom,
    tm_data_backup_protocols != tm_trusted_execution_environment).

fof(bg_dist_tm_data_backup_protocols_tm_usage_control, axiom,
    tm_data_backup_protocols != tm_usage_control).

fof(bg_dist_tm_data_backup_protocols_tm_use_synthetic_data, axiom,
    tm_data_backup_protocols != tm_use_synthetic_data).

fof(bg_dist_tm_data_backup_protocols_tm_virtualisation_security, axiom,
    tm_data_backup_protocols != tm_virtualisation_security).

fof(bg_dist_tm_data_backup_protocols_tm_vulnerability_testing_methods, axiom,
    tm_data_backup_protocols != tm_vulnerability_testing_methods).

fof(bg_dist_tm_data_backup_protocols_tm_web_browser_security, axiom,
    tm_data_backup_protocols != tm_web_browser_security).

fof(bg_dist_tm_data_backup_protocols_tm_web_security_protocols, axiom,
    tm_data_backup_protocols != tm_web_security_protocols).

fof(bg_dist_tm_data_backup_protocols_tm_wireless_security_protocols, axiom,
    tm_data_backup_protocols != tm_wireless_security_protocols).

fof(bg_dist_tm_data_backup_protocols_tm_zero_knowledge_authentication, axiom,
    tm_data_backup_protocols != tm_zero_knowledge_authentication).

fof(bg_dist_tm_data_redaction_tm_data_sanitisation_technique, axiom,
    tm_data_redaction != tm_data_sanitisation_technique).

fof(bg_dist_tm_data_redaction_tm_deidentification, axiom,
    tm_data_redaction != tm_deidentification).

fof(bg_dist_tm_data_redaction_tm_deterministic_pseudonymisation, axiom,
    tm_data_redaction != tm_deterministic_pseudonymisation).

fof(bg_dist_tm_data_redaction_tm_differential_privacy, axiom,
    tm_data_redaction != tm_differential_privacy).

fof(bg_dist_tm_data_redaction_tm_digital_rights_management, axiom,
    tm_data_redaction != tm_digital_rights_management).

fof(bg_dist_tm_data_redaction_tm_digital_signatures, axiom,
    tm_data_redaction != tm_digital_signatures).

fof(bg_dist_tm_data_redaction_tm_distributed_system_security, axiom,
    tm_data_redaction != tm_distributed_system_security).

fof(bg_dist_tm_data_redaction_tm_document_randomised_pseudonymisation, axiom,
    tm_data_redaction != tm_document_randomised_pseudonymisation).

fof(bg_dist_tm_data_redaction_tm_document_security, axiom,
    tm_data_redaction != tm_document_security).

fof(bg_dist_tm_data_redaction_tm_encryption_in_transfer, axiom,
    tm_data_redaction != tm_encryption_in_transfer).

fof(bg_dist_tm_data_redaction_tm_encryption_in_use, axiom,
    tm_data_redaction != tm_encryption_in_use).

fof(bg_dist_tm_data_redaction_tm_end_to_end_encryption, axiom,
    tm_data_redaction != tm_end_to_end_encryption).

fof(bg_dist_tm_data_redaction_tm_fail_safe_protocols, axiom,
    tm_data_redaction != tm_fail_safe_protocols).

fof(bg_dist_tm_data_redaction_tm_file_system_security, axiom,
    tm_data_redaction != tm_file_system_security).

fof(bg_dist_tm_data_redaction_tm_fully_randomised_pseudonymisation, axiom,
    tm_data_redaction != tm_fully_randomised_pseudonymisation).

fof(bg_dist_tm_data_redaction_tm_hardware_security_protocols, axiom,
    tm_data_redaction != tm_hardware_security_protocols).

fof(bg_dist_tm_data_redaction_tm_hash_functions, axiom,
    tm_data_redaction != tm_hash_functions).

fof(bg_dist_tm_data_redaction_tm_hash_message_authentication_code, axiom,
    tm_data_redaction != tm_hash_message_authentication_code).

fof(bg_dist_tm_data_redaction_tm_homomorphic_encryption, axiom,
    tm_data_redaction != tm_homomorphic_encryption).

fof(bg_dist_tm_data_redaction_tm_information_flow_control, axiom,
    tm_data_redaction != tm_information_flow_control).

fof(bg_dist_tm_data_redaction_tm_intrusion_detection_system, axiom,
    tm_data_redaction != tm_intrusion_detection_system).

fof(bg_dist_tm_data_redaction_tm_legal_measure, axiom,
    tm_data_redaction != tm_legal_measure).

fof(bg_dist_tm_data_redaction_tm_message_authentication_codes, axiom,
    tm_data_redaction != tm_message_authentication_codes).

fof(bg_dist_tm_data_redaction_tm_mobile_platform_security, axiom,
    tm_data_redaction != tm_mobile_platform_security).

fof(bg_dist_tm_data_redaction_tm_monotonic_counter_pseudonymisation, axiom,
    tm_data_redaction != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_data_redaction_tm_multi_factor_authentication, axiom,
    tm_data_redaction != tm_multi_factor_authentication).

fof(bg_dist_tm_data_redaction_tm_network_proxy_routing, axiom,
    tm_data_redaction != tm_network_proxy_routing).

fof(bg_dist_tm_data_redaction_tm_network_security_protocols, axiom,
    tm_data_redaction != tm_network_security_protocols).

fof(bg_dist_tm_data_redaction_tm_operating_system_security, axiom,
    tm_data_redaction != tm_operating_system_security).

fof(bg_dist_tm_data_redaction_tm_organisational_measure, axiom,
    tm_data_redaction != tm_organisational_measure).

fof(bg_dist_tm_data_redaction_tm_password_authentication, axiom,
    tm_data_redaction != tm_password_authentication).

fof(bg_dist_tm_data_redaction_tm_penetration_testing_methods, axiom,
    tm_data_redaction != tm_penetration_testing_methods).

fof(bg_dist_tm_data_redaction_tm_physical_measure, axiom,
    tm_data_redaction != tm_physical_measure).

fof(bg_dist_tm_data_redaction_tm_post_quantum_cryptography, axiom,
    tm_data_redaction != tm_post_quantum_cryptography).

fof(bg_dist_tm_data_redaction_tm_privacy_preserving_protocol, axiom,
    tm_data_redaction != tm_privacy_preserving_protocol).

fof(bg_dist_tm_data_redaction_tm_private_information_retrieval, axiom,
    tm_data_redaction != tm_private_information_retrieval).

fof(bg_dist_tm_data_redaction_tm_pseudonymisation, axiom,
    tm_data_redaction != tm_pseudonymisation).

fof(bg_dist_tm_data_redaction_tm_quantum_cryptography, axiom,
    tm_data_redaction != tm_quantum_cryptography).

fof(bg_dist_tm_data_redaction_tm_r_n_g_pseudonymisation, axiom,
    tm_data_redaction != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_data_redaction_tm_secret_sharing_schemes, axiom,
    tm_data_redaction != tm_secret_sharing_schemes).

fof(bg_dist_tm_data_redaction_tm_secure_multi_party_computation, axiom,
    tm_data_redaction != tm_secure_multi_party_computation).

fof(bg_dist_tm_data_redaction_tm_security_method, axiom,
    tm_data_redaction != tm_security_method).

fof(bg_dist_tm_data_redaction_tm_single_sign_on, axiom,
    tm_data_redaction != tm_single_sign_on).

fof(bg_dist_tm_data_redaction_tm_symmetric_cryptography, axiom,
    tm_data_redaction != tm_symmetric_cryptography).

fof(bg_dist_tm_data_redaction_tm_symmetric_encryption, axiom,
    tm_data_redaction != tm_symmetric_encryption).

fof(bg_dist_tm_data_redaction_tm_technical_measure, axiom,
    tm_data_redaction != tm_technical_measure).

fof(bg_dist_tm_data_redaction_tm_technical_organisational_measure, axiom,
    tm_data_redaction != tm_technical_organisational_measure).

fof(bg_dist_tm_data_redaction_tm_trusted_computing, axiom,
    tm_data_redaction != tm_trusted_computing).

fof(bg_dist_tm_data_redaction_tm_trusted_execution_environment, axiom,
    tm_data_redaction != tm_trusted_execution_environment).

fof(bg_dist_tm_data_redaction_tm_usage_control, axiom,
    tm_data_redaction != tm_usage_control).

fof(bg_dist_tm_data_redaction_tm_use_synthetic_data, axiom,
    tm_data_redaction != tm_use_synthetic_data).

fof(bg_dist_tm_data_redaction_tm_virtualisation_security, axiom,
    tm_data_redaction != tm_virtualisation_security).

fof(bg_dist_tm_data_redaction_tm_vulnerability_testing_methods, axiom,
    tm_data_redaction != tm_vulnerability_testing_methods).

fof(bg_dist_tm_data_redaction_tm_web_browser_security, axiom,
    tm_data_redaction != tm_web_browser_security).

fof(bg_dist_tm_data_redaction_tm_web_security_protocols, axiom,
    tm_data_redaction != tm_web_security_protocols).

fof(bg_dist_tm_data_redaction_tm_wireless_security_protocols, axiom,
    tm_data_redaction != tm_wireless_security_protocols).

fof(bg_dist_tm_data_redaction_tm_zero_knowledge_authentication, axiom,
    tm_data_redaction != tm_zero_knowledge_authentication).

fof(bg_dist_tm_data_sanitisation_technique_tm_deidentification, axiom,
    tm_data_sanitisation_technique != tm_deidentification).

fof(bg_dist_tm_data_sanitisation_technique_tm_deterministic_pseudonymisation, axiom,
    tm_data_sanitisation_technique != tm_deterministic_pseudonymisation).

fof(bg_dist_tm_data_sanitisation_technique_tm_differential_privacy, axiom,
    tm_data_sanitisation_technique != tm_differential_privacy).

fof(bg_dist_tm_data_sanitisation_technique_tm_digital_rights_management, axiom,
    tm_data_sanitisation_technique != tm_digital_rights_management).

fof(bg_dist_tm_data_sanitisation_technique_tm_digital_signatures, axiom,
    tm_data_sanitisation_technique != tm_digital_signatures).

fof(bg_dist_tm_data_sanitisation_technique_tm_distributed_system_security, axiom,
    tm_data_sanitisation_technique != tm_distributed_system_security).

fof(bg_dist_tm_data_sanitisation_technique_tm_document_randomised_pseudonymisation, axiom,
    tm_data_sanitisation_technique != tm_document_randomised_pseudonymisation).

fof(bg_dist_tm_data_sanitisation_technique_tm_document_security, axiom,
    tm_data_sanitisation_technique != tm_document_security).

fof(bg_dist_tm_data_sanitisation_technique_tm_encryption_in_transfer, axiom,
    tm_data_sanitisation_technique != tm_encryption_in_transfer).

fof(bg_dist_tm_data_sanitisation_technique_tm_encryption_in_use, axiom,
    tm_data_sanitisation_technique != tm_encryption_in_use).

fof(bg_dist_tm_data_sanitisation_technique_tm_end_to_end_encryption, axiom,
    tm_data_sanitisation_technique != tm_end_to_end_encryption).

fof(bg_dist_tm_data_sanitisation_technique_tm_fail_safe_protocols, axiom,
    tm_data_sanitisation_technique != tm_fail_safe_protocols).

fof(bg_dist_tm_data_sanitisation_technique_tm_file_system_security, axiom,
    tm_data_sanitisation_technique != tm_file_system_security).

fof(bg_dist_tm_data_sanitisation_technique_tm_fully_randomised_pseudonymisation, axiom,
    tm_data_sanitisation_technique != tm_fully_randomised_pseudonymisation).

fof(bg_dist_tm_data_sanitisation_technique_tm_hardware_security_protocols, axiom,
    tm_data_sanitisation_technique != tm_hardware_security_protocols).

fof(bg_dist_tm_data_sanitisation_technique_tm_hash_functions, axiom,
    tm_data_sanitisation_technique != tm_hash_functions).

fof(bg_dist_tm_data_sanitisation_technique_tm_hash_message_authentication_code, axiom,
    tm_data_sanitisation_technique != tm_hash_message_authentication_code).

fof(bg_dist_tm_data_sanitisation_technique_tm_homomorphic_encryption, axiom,
    tm_data_sanitisation_technique != tm_homomorphic_encryption).

fof(bg_dist_tm_data_sanitisation_technique_tm_information_flow_control, axiom,
    tm_data_sanitisation_technique != tm_information_flow_control).

fof(bg_dist_tm_data_sanitisation_technique_tm_intrusion_detection_system, axiom,
    tm_data_sanitisation_technique != tm_intrusion_detection_system).

fof(bg_dist_tm_data_sanitisation_technique_tm_legal_measure, axiom,
    tm_data_sanitisation_technique != tm_legal_measure).

fof(bg_dist_tm_data_sanitisation_technique_tm_message_authentication_codes, axiom,
    tm_data_sanitisation_technique != tm_message_authentication_codes).

fof(bg_dist_tm_data_sanitisation_technique_tm_mobile_platform_security, axiom,
    tm_data_sanitisation_technique != tm_mobile_platform_security).

fof(bg_dist_tm_data_sanitisation_technique_tm_monotonic_counter_pseudonymisation, axiom,
    tm_data_sanitisation_technique != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_data_sanitisation_technique_tm_multi_factor_authentication, axiom,
    tm_data_sanitisation_technique != tm_multi_factor_authentication).

fof(bg_dist_tm_data_sanitisation_technique_tm_network_proxy_routing, axiom,
    tm_data_sanitisation_technique != tm_network_proxy_routing).

fof(bg_dist_tm_data_sanitisation_technique_tm_network_security_protocols, axiom,
    tm_data_sanitisation_technique != tm_network_security_protocols).

fof(bg_dist_tm_data_sanitisation_technique_tm_operating_system_security, axiom,
    tm_data_sanitisation_technique != tm_operating_system_security).

fof(bg_dist_tm_data_sanitisation_technique_tm_organisational_measure, axiom,
    tm_data_sanitisation_technique != tm_organisational_measure).

fof(bg_dist_tm_data_sanitisation_technique_tm_password_authentication, axiom,
    tm_data_sanitisation_technique != tm_password_authentication).

fof(bg_dist_tm_data_sanitisation_technique_tm_penetration_testing_methods, axiom,
    tm_data_sanitisation_technique != tm_penetration_testing_methods).

fof(bg_dist_tm_data_sanitisation_technique_tm_physical_measure, axiom,
    tm_data_sanitisation_technique != tm_physical_measure).

fof(bg_dist_tm_data_sanitisation_technique_tm_post_quantum_cryptography, axiom,
    tm_data_sanitisation_technique != tm_post_quantum_cryptography).

fof(bg_dist_tm_data_sanitisation_technique_tm_privacy_preserving_protocol, axiom,
    tm_data_sanitisation_technique != tm_privacy_preserving_protocol).

fof(bg_dist_tm_data_sanitisation_technique_tm_private_information_retrieval, axiom,
    tm_data_sanitisation_technique != tm_private_information_retrieval).

fof(bg_dist_tm_data_sanitisation_technique_tm_pseudonymisation, axiom,
    tm_data_sanitisation_technique != tm_pseudonymisation).

fof(bg_dist_tm_data_sanitisation_technique_tm_quantum_cryptography, axiom,
    tm_data_sanitisation_technique != tm_quantum_cryptography).

fof(bg_dist_tm_data_sanitisation_technique_tm_r_n_g_pseudonymisation, axiom,
    tm_data_sanitisation_technique != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_data_sanitisation_technique_tm_secret_sharing_schemes, axiom,
    tm_data_sanitisation_technique != tm_secret_sharing_schemes).

fof(bg_dist_tm_data_sanitisation_technique_tm_secure_multi_party_computation, axiom,
    tm_data_sanitisation_technique != tm_secure_multi_party_computation).

fof(bg_dist_tm_data_sanitisation_technique_tm_security_method, axiom,
    tm_data_sanitisation_technique != tm_security_method).

fof(bg_dist_tm_data_sanitisation_technique_tm_single_sign_on, axiom,
    tm_data_sanitisation_technique != tm_single_sign_on).

fof(bg_dist_tm_data_sanitisation_technique_tm_symmetric_cryptography, axiom,
    tm_data_sanitisation_technique != tm_symmetric_cryptography).

fof(bg_dist_tm_data_sanitisation_technique_tm_symmetric_encryption, axiom,
    tm_data_sanitisation_technique != tm_symmetric_encryption).

fof(bg_dist_tm_data_sanitisation_technique_tm_technical_measure, axiom,
    tm_data_sanitisation_technique != tm_technical_measure).

fof(bg_dist_tm_data_sanitisation_technique_tm_technical_organisational_measure, axiom,
    tm_data_sanitisation_technique != tm_technical_organisational_measure).

fof(bg_dist_tm_data_sanitisation_technique_tm_trusted_computing, axiom,
    tm_data_sanitisation_technique != tm_trusted_computing).

fof(bg_dist_tm_data_sanitisation_technique_tm_trusted_execution_environment, axiom,
    tm_data_sanitisation_technique != tm_trusted_execution_environment).

fof(bg_dist_tm_data_sanitisation_technique_tm_usage_control, axiom,
    tm_data_sanitisation_technique != tm_usage_control).

fof(bg_dist_tm_data_sanitisation_technique_tm_use_synthetic_data, axiom,
    tm_data_sanitisation_technique != tm_use_synthetic_data).

fof(bg_dist_tm_data_sanitisation_technique_tm_virtualisation_security, axiom,
    tm_data_sanitisation_technique != tm_virtualisation_security).

fof(bg_dist_tm_data_sanitisation_technique_tm_vulnerability_testing_methods, axiom,
    tm_data_sanitisation_technique != tm_vulnerability_testing_methods).

fof(bg_dist_tm_data_sanitisation_technique_tm_web_browser_security, axiom,
    tm_data_sanitisation_technique != tm_web_browser_security).

fof(bg_dist_tm_data_sanitisation_technique_tm_web_security_protocols, axiom,
    tm_data_sanitisation_technique != tm_web_security_protocols).

fof(bg_dist_tm_data_sanitisation_technique_tm_wireless_security_protocols, axiom,
    tm_data_sanitisation_technique != tm_wireless_security_protocols).

fof(bg_dist_tm_data_sanitisation_technique_tm_zero_knowledge_authentication, axiom,
    tm_data_sanitisation_technique != tm_zero_knowledge_authentication).

fof(bg_dist_tm_deidentification_tm_deterministic_pseudonymisation, axiom,
    tm_deidentification != tm_deterministic_pseudonymisation).

fof(bg_dist_tm_deidentification_tm_differential_privacy, axiom,
    tm_deidentification != tm_differential_privacy).

fof(bg_dist_tm_deidentification_tm_digital_rights_management, axiom,
    tm_deidentification != tm_digital_rights_management).

fof(bg_dist_tm_deidentification_tm_digital_signatures, axiom,
    tm_deidentification != tm_digital_signatures).

fof(bg_dist_tm_deidentification_tm_distributed_system_security, axiom,
    tm_deidentification != tm_distributed_system_security).

fof(bg_dist_tm_deidentification_tm_document_randomised_pseudonymisation, axiom,
    tm_deidentification != tm_document_randomised_pseudonymisation).

fof(bg_dist_tm_deidentification_tm_document_security, axiom,
    tm_deidentification != tm_document_security).

fof(bg_dist_tm_deidentification_tm_encryption_in_transfer, axiom,
    tm_deidentification != tm_encryption_in_transfer).

fof(bg_dist_tm_deidentification_tm_encryption_in_use, axiom,
    tm_deidentification != tm_encryption_in_use).

fof(bg_dist_tm_deidentification_tm_end_to_end_encryption, axiom,
    tm_deidentification != tm_end_to_end_encryption).

fof(bg_dist_tm_deidentification_tm_fail_safe_protocols, axiom,
    tm_deidentification != tm_fail_safe_protocols).

fof(bg_dist_tm_deidentification_tm_file_system_security, axiom,
    tm_deidentification != tm_file_system_security).

fof(bg_dist_tm_deidentification_tm_fully_randomised_pseudonymisation, axiom,
    tm_deidentification != tm_fully_randomised_pseudonymisation).

fof(bg_dist_tm_deidentification_tm_hardware_security_protocols, axiom,
    tm_deidentification != tm_hardware_security_protocols).

fof(bg_dist_tm_deidentification_tm_hash_functions, axiom,
    tm_deidentification != tm_hash_functions).

fof(bg_dist_tm_deidentification_tm_hash_message_authentication_code, axiom,
    tm_deidentification != tm_hash_message_authentication_code).

fof(bg_dist_tm_deidentification_tm_homomorphic_encryption, axiom,
    tm_deidentification != tm_homomorphic_encryption).

fof(bg_dist_tm_deidentification_tm_information_flow_control, axiom,
    tm_deidentification != tm_information_flow_control).

fof(bg_dist_tm_deidentification_tm_intrusion_detection_system, axiom,
    tm_deidentification != tm_intrusion_detection_system).

fof(bg_dist_tm_deidentification_tm_legal_measure, axiom,
    tm_deidentification != tm_legal_measure).

fof(bg_dist_tm_deidentification_tm_message_authentication_codes, axiom,
    tm_deidentification != tm_message_authentication_codes).

fof(bg_dist_tm_deidentification_tm_mobile_platform_security, axiom,
    tm_deidentification != tm_mobile_platform_security).

fof(bg_dist_tm_deidentification_tm_monotonic_counter_pseudonymisation, axiom,
    tm_deidentification != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_deidentification_tm_multi_factor_authentication, axiom,
    tm_deidentification != tm_multi_factor_authentication).

fof(bg_dist_tm_deidentification_tm_network_proxy_routing, axiom,
    tm_deidentification != tm_network_proxy_routing).

fof(bg_dist_tm_deidentification_tm_network_security_protocols, axiom,
    tm_deidentification != tm_network_security_protocols).

fof(bg_dist_tm_deidentification_tm_operating_system_security, axiom,
    tm_deidentification != tm_operating_system_security).

fof(bg_dist_tm_deidentification_tm_organisational_measure, axiom,
    tm_deidentification != tm_organisational_measure).

fof(bg_dist_tm_deidentification_tm_password_authentication, axiom,
    tm_deidentification != tm_password_authentication).

fof(bg_dist_tm_deidentification_tm_penetration_testing_methods, axiom,
    tm_deidentification != tm_penetration_testing_methods).

fof(bg_dist_tm_deidentification_tm_physical_measure, axiom,
    tm_deidentification != tm_physical_measure).

fof(bg_dist_tm_deidentification_tm_post_quantum_cryptography, axiom,
    tm_deidentification != tm_post_quantum_cryptography).

fof(bg_dist_tm_deidentification_tm_privacy_preserving_protocol, axiom,
    tm_deidentification != tm_privacy_preserving_protocol).

fof(bg_dist_tm_deidentification_tm_private_information_retrieval, axiom,
    tm_deidentification != tm_private_information_retrieval).

fof(bg_dist_tm_deidentification_tm_pseudonymisation, axiom,
    tm_deidentification != tm_pseudonymisation).

fof(bg_dist_tm_deidentification_tm_quantum_cryptography, axiom,
    tm_deidentification != tm_quantum_cryptography).

fof(bg_dist_tm_deidentification_tm_r_n_g_pseudonymisation, axiom,
    tm_deidentification != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_deidentification_tm_secret_sharing_schemes, axiom,
    tm_deidentification != tm_secret_sharing_schemes).

fof(bg_dist_tm_deidentification_tm_secure_multi_party_computation, axiom,
    tm_deidentification != tm_secure_multi_party_computation).

fof(bg_dist_tm_deidentification_tm_security_method, axiom,
    tm_deidentification != tm_security_method).

fof(bg_dist_tm_deidentification_tm_single_sign_on, axiom,
    tm_deidentification != tm_single_sign_on).

fof(bg_dist_tm_deidentification_tm_symmetric_cryptography, axiom,
    tm_deidentification != tm_symmetric_cryptography).

fof(bg_dist_tm_deidentification_tm_symmetric_encryption, axiom,
    tm_deidentification != tm_symmetric_encryption).

fof(bg_dist_tm_deidentification_tm_technical_measure, axiom,
    tm_deidentification != tm_technical_measure).

fof(bg_dist_tm_deidentification_tm_technical_organisational_measure, axiom,
    tm_deidentification != tm_technical_organisational_measure).

fof(bg_dist_tm_deidentification_tm_trusted_computing, axiom,
    tm_deidentification != tm_trusted_computing).

fof(bg_dist_tm_deidentification_tm_trusted_execution_environment, axiom,
    tm_deidentification != tm_trusted_execution_environment).

fof(bg_dist_tm_deidentification_tm_usage_control, axiom,
    tm_deidentification != tm_usage_control).

fof(bg_dist_tm_deidentification_tm_use_synthetic_data, axiom,
    tm_deidentification != tm_use_synthetic_data).

fof(bg_dist_tm_deidentification_tm_virtualisation_security, axiom,
    tm_deidentification != tm_virtualisation_security).

fof(bg_dist_tm_deidentification_tm_vulnerability_testing_methods, axiom,
    tm_deidentification != tm_vulnerability_testing_methods).

fof(bg_dist_tm_deidentification_tm_web_browser_security, axiom,
    tm_deidentification != tm_web_browser_security).

fof(bg_dist_tm_deidentification_tm_web_security_protocols, axiom,
    tm_deidentification != tm_web_security_protocols).

fof(bg_dist_tm_deidentification_tm_wireless_security_protocols, axiom,
    tm_deidentification != tm_wireless_security_protocols).

fof(bg_dist_tm_deidentification_tm_zero_knowledge_authentication, axiom,
    tm_deidentification != tm_zero_knowledge_authentication).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_differential_privacy, axiom,
    tm_deterministic_pseudonymisation != tm_differential_privacy).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_digital_rights_management, axiom,
    tm_deterministic_pseudonymisation != tm_digital_rights_management).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_digital_signatures, axiom,
    tm_deterministic_pseudonymisation != tm_digital_signatures).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_distributed_system_security, axiom,
    tm_deterministic_pseudonymisation != tm_distributed_system_security).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_document_randomised_pseudonymisation, axiom,
    tm_deterministic_pseudonymisation != tm_document_randomised_pseudonymisation).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_document_security, axiom,
    tm_deterministic_pseudonymisation != tm_document_security).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_encryption_in_transfer, axiom,
    tm_deterministic_pseudonymisation != tm_encryption_in_transfer).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_encryption_in_use, axiom,
    tm_deterministic_pseudonymisation != tm_encryption_in_use).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_end_to_end_encryption, axiom,
    tm_deterministic_pseudonymisation != tm_end_to_end_encryption).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_fail_safe_protocols, axiom,
    tm_deterministic_pseudonymisation != tm_fail_safe_protocols).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_file_system_security, axiom,
    tm_deterministic_pseudonymisation != tm_file_system_security).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_fully_randomised_pseudonymisation, axiom,
    tm_deterministic_pseudonymisation != tm_fully_randomised_pseudonymisation).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_hardware_security_protocols, axiom,
    tm_deterministic_pseudonymisation != tm_hardware_security_protocols).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_hash_functions, axiom,
    tm_deterministic_pseudonymisation != tm_hash_functions).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_hash_message_authentication_code, axiom,
    tm_deterministic_pseudonymisation != tm_hash_message_authentication_code).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_homomorphic_encryption, axiom,
    tm_deterministic_pseudonymisation != tm_homomorphic_encryption).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_information_flow_control, axiom,
    tm_deterministic_pseudonymisation != tm_information_flow_control).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_intrusion_detection_system, axiom,
    tm_deterministic_pseudonymisation != tm_intrusion_detection_system).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_legal_measure, axiom,
    tm_deterministic_pseudonymisation != tm_legal_measure).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_message_authentication_codes, axiom,
    tm_deterministic_pseudonymisation != tm_message_authentication_codes).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_mobile_platform_security, axiom,
    tm_deterministic_pseudonymisation != tm_mobile_platform_security).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_monotonic_counter_pseudonymisation, axiom,
    tm_deterministic_pseudonymisation != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_multi_factor_authentication, axiom,
    tm_deterministic_pseudonymisation != tm_multi_factor_authentication).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_network_proxy_routing, axiom,
    tm_deterministic_pseudonymisation != tm_network_proxy_routing).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_network_security_protocols, axiom,
    tm_deterministic_pseudonymisation != tm_network_security_protocols).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_operating_system_security, axiom,
    tm_deterministic_pseudonymisation != tm_operating_system_security).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_organisational_measure, axiom,
    tm_deterministic_pseudonymisation != tm_organisational_measure).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_password_authentication, axiom,
    tm_deterministic_pseudonymisation != tm_password_authentication).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_penetration_testing_methods, axiom,
    tm_deterministic_pseudonymisation != tm_penetration_testing_methods).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_physical_measure, axiom,
    tm_deterministic_pseudonymisation != tm_physical_measure).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_post_quantum_cryptography, axiom,
    tm_deterministic_pseudonymisation != tm_post_quantum_cryptography).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_privacy_preserving_protocol, axiom,
    tm_deterministic_pseudonymisation != tm_privacy_preserving_protocol).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_private_information_retrieval, axiom,
    tm_deterministic_pseudonymisation != tm_private_information_retrieval).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_pseudonymisation, axiom,
    tm_deterministic_pseudonymisation != tm_pseudonymisation).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_quantum_cryptography, axiom,
    tm_deterministic_pseudonymisation != tm_quantum_cryptography).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_r_n_g_pseudonymisation, axiom,
    tm_deterministic_pseudonymisation != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_secret_sharing_schemes, axiom,
    tm_deterministic_pseudonymisation != tm_secret_sharing_schemes).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_secure_multi_party_computation, axiom,
    tm_deterministic_pseudonymisation != tm_secure_multi_party_computation).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_security_method, axiom,
    tm_deterministic_pseudonymisation != tm_security_method).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_single_sign_on, axiom,
    tm_deterministic_pseudonymisation != tm_single_sign_on).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_symmetric_cryptography, axiom,
    tm_deterministic_pseudonymisation != tm_symmetric_cryptography).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_symmetric_encryption, axiom,
    tm_deterministic_pseudonymisation != tm_symmetric_encryption).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_technical_measure, axiom,
    tm_deterministic_pseudonymisation != tm_technical_measure).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_technical_organisational_measure, axiom,
    tm_deterministic_pseudonymisation != tm_technical_organisational_measure).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_trusted_computing, axiom,
    tm_deterministic_pseudonymisation != tm_trusted_computing).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_trusted_execution_environment, axiom,
    tm_deterministic_pseudonymisation != tm_trusted_execution_environment).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_usage_control, axiom,
    tm_deterministic_pseudonymisation != tm_usage_control).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_use_synthetic_data, axiom,
    tm_deterministic_pseudonymisation != tm_use_synthetic_data).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_virtualisation_security, axiom,
    tm_deterministic_pseudonymisation != tm_virtualisation_security).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_vulnerability_testing_methods, axiom,
    tm_deterministic_pseudonymisation != tm_vulnerability_testing_methods).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_web_browser_security, axiom,
    tm_deterministic_pseudonymisation != tm_web_browser_security).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_web_security_protocols, axiom,
    tm_deterministic_pseudonymisation != tm_web_security_protocols).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_wireless_security_protocols, axiom,
    tm_deterministic_pseudonymisation != tm_wireless_security_protocols).

fof(bg_dist_tm_deterministic_pseudonymisation_tm_zero_knowledge_authentication, axiom,
    tm_deterministic_pseudonymisation != tm_zero_knowledge_authentication).

fof(bg_dist_tm_differential_privacy_tm_digital_rights_management, axiom,
    tm_differential_privacy != tm_digital_rights_management).

fof(bg_dist_tm_differential_privacy_tm_digital_signatures, axiom,
    tm_differential_privacy != tm_digital_signatures).

fof(bg_dist_tm_differential_privacy_tm_distributed_system_security, axiom,
    tm_differential_privacy != tm_distributed_system_security).

fof(bg_dist_tm_differential_privacy_tm_document_randomised_pseudonymisation, axiom,
    tm_differential_privacy != tm_document_randomised_pseudonymisation).

fof(bg_dist_tm_differential_privacy_tm_document_security, axiom,
    tm_differential_privacy != tm_document_security).

fof(bg_dist_tm_differential_privacy_tm_encryption_in_transfer, axiom,
    tm_differential_privacy != tm_encryption_in_transfer).

fof(bg_dist_tm_differential_privacy_tm_encryption_in_use, axiom,
    tm_differential_privacy != tm_encryption_in_use).

fof(bg_dist_tm_differential_privacy_tm_end_to_end_encryption, axiom,
    tm_differential_privacy != tm_end_to_end_encryption).

fof(bg_dist_tm_differential_privacy_tm_fail_safe_protocols, axiom,
    tm_differential_privacy != tm_fail_safe_protocols).

fof(bg_dist_tm_differential_privacy_tm_file_system_security, axiom,
    tm_differential_privacy != tm_file_system_security).

fof(bg_dist_tm_differential_privacy_tm_fully_randomised_pseudonymisation, axiom,
    tm_differential_privacy != tm_fully_randomised_pseudonymisation).

fof(bg_dist_tm_differential_privacy_tm_hardware_security_protocols, axiom,
    tm_differential_privacy != tm_hardware_security_protocols).

fof(bg_dist_tm_differential_privacy_tm_hash_functions, axiom,
    tm_differential_privacy != tm_hash_functions).

fof(bg_dist_tm_differential_privacy_tm_hash_message_authentication_code, axiom,
    tm_differential_privacy != tm_hash_message_authentication_code).

fof(bg_dist_tm_differential_privacy_tm_homomorphic_encryption, axiom,
    tm_differential_privacy != tm_homomorphic_encryption).

fof(bg_dist_tm_differential_privacy_tm_information_flow_control, axiom,
    tm_differential_privacy != tm_information_flow_control).

fof(bg_dist_tm_differential_privacy_tm_intrusion_detection_system, axiom,
    tm_differential_privacy != tm_intrusion_detection_system).

fof(bg_dist_tm_differential_privacy_tm_legal_measure, axiom,
    tm_differential_privacy != tm_legal_measure).

fof(bg_dist_tm_differential_privacy_tm_message_authentication_codes, axiom,
    tm_differential_privacy != tm_message_authentication_codes).

fof(bg_dist_tm_differential_privacy_tm_mobile_platform_security, axiom,
    tm_differential_privacy != tm_mobile_platform_security).

fof(bg_dist_tm_differential_privacy_tm_monotonic_counter_pseudonymisation, axiom,
    tm_differential_privacy != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_differential_privacy_tm_multi_factor_authentication, axiom,
    tm_differential_privacy != tm_multi_factor_authentication).

fof(bg_dist_tm_differential_privacy_tm_network_proxy_routing, axiom,
    tm_differential_privacy != tm_network_proxy_routing).

fof(bg_dist_tm_differential_privacy_tm_network_security_protocols, axiom,
    tm_differential_privacy != tm_network_security_protocols).

fof(bg_dist_tm_differential_privacy_tm_operating_system_security, axiom,
    tm_differential_privacy != tm_operating_system_security).

fof(bg_dist_tm_differential_privacy_tm_organisational_measure, axiom,
    tm_differential_privacy != tm_organisational_measure).

fof(bg_dist_tm_differential_privacy_tm_password_authentication, axiom,
    tm_differential_privacy != tm_password_authentication).

fof(bg_dist_tm_differential_privacy_tm_penetration_testing_methods, axiom,
    tm_differential_privacy != tm_penetration_testing_methods).

fof(bg_dist_tm_differential_privacy_tm_physical_measure, axiom,
    tm_differential_privacy != tm_physical_measure).

fof(bg_dist_tm_differential_privacy_tm_post_quantum_cryptography, axiom,
    tm_differential_privacy != tm_post_quantum_cryptography).

fof(bg_dist_tm_differential_privacy_tm_privacy_preserving_protocol, axiom,
    tm_differential_privacy != tm_privacy_preserving_protocol).

fof(bg_dist_tm_differential_privacy_tm_private_information_retrieval, axiom,
    tm_differential_privacy != tm_private_information_retrieval).

fof(bg_dist_tm_differential_privacy_tm_pseudonymisation, axiom,
    tm_differential_privacy != tm_pseudonymisation).

fof(bg_dist_tm_differential_privacy_tm_quantum_cryptography, axiom,
    tm_differential_privacy != tm_quantum_cryptography).

fof(bg_dist_tm_differential_privacy_tm_r_n_g_pseudonymisation, axiom,
    tm_differential_privacy != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_differential_privacy_tm_secret_sharing_schemes, axiom,
    tm_differential_privacy != tm_secret_sharing_schemes).

fof(bg_dist_tm_differential_privacy_tm_secure_multi_party_computation, axiom,
    tm_differential_privacy != tm_secure_multi_party_computation).

fof(bg_dist_tm_differential_privacy_tm_security_method, axiom,
    tm_differential_privacy != tm_security_method).

fof(bg_dist_tm_differential_privacy_tm_single_sign_on, axiom,
    tm_differential_privacy != tm_single_sign_on).

fof(bg_dist_tm_differential_privacy_tm_symmetric_cryptography, axiom,
    tm_differential_privacy != tm_symmetric_cryptography).

fof(bg_dist_tm_differential_privacy_tm_symmetric_encryption, axiom,
    tm_differential_privacy != tm_symmetric_encryption).

fof(bg_dist_tm_differential_privacy_tm_technical_measure, axiom,
    tm_differential_privacy != tm_technical_measure).

fof(bg_dist_tm_differential_privacy_tm_technical_organisational_measure, axiom,
    tm_differential_privacy != tm_technical_organisational_measure).

fof(bg_dist_tm_differential_privacy_tm_trusted_computing, axiom,
    tm_differential_privacy != tm_trusted_computing).

fof(bg_dist_tm_differential_privacy_tm_trusted_execution_environment, axiom,
    tm_differential_privacy != tm_trusted_execution_environment).

fof(bg_dist_tm_differential_privacy_tm_usage_control, axiom,
    tm_differential_privacy != tm_usage_control).

fof(bg_dist_tm_differential_privacy_tm_use_synthetic_data, axiom,
    tm_differential_privacy != tm_use_synthetic_data).

fof(bg_dist_tm_differential_privacy_tm_virtualisation_security, axiom,
    tm_differential_privacy != tm_virtualisation_security).

fof(bg_dist_tm_differential_privacy_tm_vulnerability_testing_methods, axiom,
    tm_differential_privacy != tm_vulnerability_testing_methods).

fof(bg_dist_tm_differential_privacy_tm_web_browser_security, axiom,
    tm_differential_privacy != tm_web_browser_security).

fof(bg_dist_tm_differential_privacy_tm_web_security_protocols, axiom,
    tm_differential_privacy != tm_web_security_protocols).

fof(bg_dist_tm_differential_privacy_tm_wireless_security_protocols, axiom,
    tm_differential_privacy != tm_wireless_security_protocols).

fof(bg_dist_tm_differential_privacy_tm_zero_knowledge_authentication, axiom,
    tm_differential_privacy != tm_zero_knowledge_authentication).

fof(bg_dist_tm_digital_rights_management_tm_digital_signatures, axiom,
    tm_digital_rights_management != tm_digital_signatures).

fof(bg_dist_tm_digital_rights_management_tm_distributed_system_security, axiom,
    tm_digital_rights_management != tm_distributed_system_security).

fof(bg_dist_tm_digital_rights_management_tm_document_randomised_pseudonymisation, axiom,
    tm_digital_rights_management != tm_document_randomised_pseudonymisation).

fof(bg_dist_tm_digital_rights_management_tm_document_security, axiom,
    tm_digital_rights_management != tm_document_security).

fof(bg_dist_tm_digital_rights_management_tm_encryption_in_transfer, axiom,
    tm_digital_rights_management != tm_encryption_in_transfer).

fof(bg_dist_tm_digital_rights_management_tm_encryption_in_use, axiom,
    tm_digital_rights_management != tm_encryption_in_use).

fof(bg_dist_tm_digital_rights_management_tm_end_to_end_encryption, axiom,
    tm_digital_rights_management != tm_end_to_end_encryption).

fof(bg_dist_tm_digital_rights_management_tm_fail_safe_protocols, axiom,
    tm_digital_rights_management != tm_fail_safe_protocols).

fof(bg_dist_tm_digital_rights_management_tm_file_system_security, axiom,
    tm_digital_rights_management != tm_file_system_security).

fof(bg_dist_tm_digital_rights_management_tm_fully_randomised_pseudonymisation, axiom,
    tm_digital_rights_management != tm_fully_randomised_pseudonymisation).

fof(bg_dist_tm_digital_rights_management_tm_hardware_security_protocols, axiom,
    tm_digital_rights_management != tm_hardware_security_protocols).

fof(bg_dist_tm_digital_rights_management_tm_hash_functions, axiom,
    tm_digital_rights_management != tm_hash_functions).

fof(bg_dist_tm_digital_rights_management_tm_hash_message_authentication_code, axiom,
    tm_digital_rights_management != tm_hash_message_authentication_code).

fof(bg_dist_tm_digital_rights_management_tm_homomorphic_encryption, axiom,
    tm_digital_rights_management != tm_homomorphic_encryption).

fof(bg_dist_tm_digital_rights_management_tm_information_flow_control, axiom,
    tm_digital_rights_management != tm_information_flow_control).

fof(bg_dist_tm_digital_rights_management_tm_intrusion_detection_system, axiom,
    tm_digital_rights_management != tm_intrusion_detection_system).

fof(bg_dist_tm_digital_rights_management_tm_legal_measure, axiom,
    tm_digital_rights_management != tm_legal_measure).

fof(bg_dist_tm_digital_rights_management_tm_message_authentication_codes, axiom,
    tm_digital_rights_management != tm_message_authentication_codes).

fof(bg_dist_tm_digital_rights_management_tm_mobile_platform_security, axiom,
    tm_digital_rights_management != tm_mobile_platform_security).

fof(bg_dist_tm_digital_rights_management_tm_monotonic_counter_pseudonymisation, axiom,
    tm_digital_rights_management != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_digital_rights_management_tm_multi_factor_authentication, axiom,
    tm_digital_rights_management != tm_multi_factor_authentication).

fof(bg_dist_tm_digital_rights_management_tm_network_proxy_routing, axiom,
    tm_digital_rights_management != tm_network_proxy_routing).

fof(bg_dist_tm_digital_rights_management_tm_network_security_protocols, axiom,
    tm_digital_rights_management != tm_network_security_protocols).

fof(bg_dist_tm_digital_rights_management_tm_operating_system_security, axiom,
    tm_digital_rights_management != tm_operating_system_security).

fof(bg_dist_tm_digital_rights_management_tm_organisational_measure, axiom,
    tm_digital_rights_management != tm_organisational_measure).

fof(bg_dist_tm_digital_rights_management_tm_password_authentication, axiom,
    tm_digital_rights_management != tm_password_authentication).

fof(bg_dist_tm_digital_rights_management_tm_penetration_testing_methods, axiom,
    tm_digital_rights_management != tm_penetration_testing_methods).

fof(bg_dist_tm_digital_rights_management_tm_physical_measure, axiom,
    tm_digital_rights_management != tm_physical_measure).

fof(bg_dist_tm_digital_rights_management_tm_post_quantum_cryptography, axiom,
    tm_digital_rights_management != tm_post_quantum_cryptography).

fof(bg_dist_tm_digital_rights_management_tm_privacy_preserving_protocol, axiom,
    tm_digital_rights_management != tm_privacy_preserving_protocol).

fof(bg_dist_tm_digital_rights_management_tm_private_information_retrieval, axiom,
    tm_digital_rights_management != tm_private_information_retrieval).

fof(bg_dist_tm_digital_rights_management_tm_pseudonymisation, axiom,
    tm_digital_rights_management != tm_pseudonymisation).

fof(bg_dist_tm_digital_rights_management_tm_quantum_cryptography, axiom,
    tm_digital_rights_management != tm_quantum_cryptography).

fof(bg_dist_tm_digital_rights_management_tm_r_n_g_pseudonymisation, axiom,
    tm_digital_rights_management != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_digital_rights_management_tm_secret_sharing_schemes, axiom,
    tm_digital_rights_management != tm_secret_sharing_schemes).

fof(bg_dist_tm_digital_rights_management_tm_secure_multi_party_computation, axiom,
    tm_digital_rights_management != tm_secure_multi_party_computation).

fof(bg_dist_tm_digital_rights_management_tm_security_method, axiom,
    tm_digital_rights_management != tm_security_method).

fof(bg_dist_tm_digital_rights_management_tm_single_sign_on, axiom,
    tm_digital_rights_management != tm_single_sign_on).

fof(bg_dist_tm_digital_rights_management_tm_symmetric_cryptography, axiom,
    tm_digital_rights_management != tm_symmetric_cryptography).

fof(bg_dist_tm_digital_rights_management_tm_symmetric_encryption, axiom,
    tm_digital_rights_management != tm_symmetric_encryption).

fof(bg_dist_tm_digital_rights_management_tm_technical_measure, axiom,
    tm_digital_rights_management != tm_technical_measure).

fof(bg_dist_tm_digital_rights_management_tm_technical_organisational_measure, axiom,
    tm_digital_rights_management != tm_technical_organisational_measure).

fof(bg_dist_tm_digital_rights_management_tm_trusted_computing, axiom,
    tm_digital_rights_management != tm_trusted_computing).

fof(bg_dist_tm_digital_rights_management_tm_trusted_execution_environment, axiom,
    tm_digital_rights_management != tm_trusted_execution_environment).

fof(bg_dist_tm_digital_rights_management_tm_usage_control, axiom,
    tm_digital_rights_management != tm_usage_control).

fof(bg_dist_tm_digital_rights_management_tm_use_synthetic_data, axiom,
    tm_digital_rights_management != tm_use_synthetic_data).

fof(bg_dist_tm_digital_rights_management_tm_virtualisation_security, axiom,
    tm_digital_rights_management != tm_virtualisation_security).

fof(bg_dist_tm_digital_rights_management_tm_vulnerability_testing_methods, axiom,
    tm_digital_rights_management != tm_vulnerability_testing_methods).

fof(bg_dist_tm_digital_rights_management_tm_web_browser_security, axiom,
    tm_digital_rights_management != tm_web_browser_security).

fof(bg_dist_tm_digital_rights_management_tm_web_security_protocols, axiom,
    tm_digital_rights_management != tm_web_security_protocols).

fof(bg_dist_tm_digital_rights_management_tm_wireless_security_protocols, axiom,
    tm_digital_rights_management != tm_wireless_security_protocols).

fof(bg_dist_tm_digital_rights_management_tm_zero_knowledge_authentication, axiom,
    tm_digital_rights_management != tm_zero_knowledge_authentication).

fof(bg_dist_tm_digital_signatures_tm_distributed_system_security, axiom,
    tm_digital_signatures != tm_distributed_system_security).

fof(bg_dist_tm_digital_signatures_tm_document_randomised_pseudonymisation, axiom,
    tm_digital_signatures != tm_document_randomised_pseudonymisation).

fof(bg_dist_tm_digital_signatures_tm_document_security, axiom,
    tm_digital_signatures != tm_document_security).

fof(bg_dist_tm_digital_signatures_tm_encryption_in_transfer, axiom,
    tm_digital_signatures != tm_encryption_in_transfer).

fof(bg_dist_tm_digital_signatures_tm_encryption_in_use, axiom,
    tm_digital_signatures != tm_encryption_in_use).

fof(bg_dist_tm_digital_signatures_tm_end_to_end_encryption, axiom,
    tm_digital_signatures != tm_end_to_end_encryption).

fof(bg_dist_tm_digital_signatures_tm_fail_safe_protocols, axiom,
    tm_digital_signatures != tm_fail_safe_protocols).

fof(bg_dist_tm_digital_signatures_tm_file_system_security, axiom,
    tm_digital_signatures != tm_file_system_security).

fof(bg_dist_tm_digital_signatures_tm_fully_randomised_pseudonymisation, axiom,
    tm_digital_signatures != tm_fully_randomised_pseudonymisation).

fof(bg_dist_tm_digital_signatures_tm_hardware_security_protocols, axiom,
    tm_digital_signatures != tm_hardware_security_protocols).

fof(bg_dist_tm_digital_signatures_tm_hash_functions, axiom,
    tm_digital_signatures != tm_hash_functions).

fof(bg_dist_tm_digital_signatures_tm_hash_message_authentication_code, axiom,
    tm_digital_signatures != tm_hash_message_authentication_code).

fof(bg_dist_tm_digital_signatures_tm_homomorphic_encryption, axiom,
    tm_digital_signatures != tm_homomorphic_encryption).

fof(bg_dist_tm_digital_signatures_tm_information_flow_control, axiom,
    tm_digital_signatures != tm_information_flow_control).

fof(bg_dist_tm_digital_signatures_tm_intrusion_detection_system, axiom,
    tm_digital_signatures != tm_intrusion_detection_system).

fof(bg_dist_tm_digital_signatures_tm_legal_measure, axiom,
    tm_digital_signatures != tm_legal_measure).

fof(bg_dist_tm_digital_signatures_tm_message_authentication_codes, axiom,
    tm_digital_signatures != tm_message_authentication_codes).

fof(bg_dist_tm_digital_signatures_tm_mobile_platform_security, axiom,
    tm_digital_signatures != tm_mobile_platform_security).

fof(bg_dist_tm_digital_signatures_tm_monotonic_counter_pseudonymisation, axiom,
    tm_digital_signatures != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_digital_signatures_tm_multi_factor_authentication, axiom,
    tm_digital_signatures != tm_multi_factor_authentication).

fof(bg_dist_tm_digital_signatures_tm_network_proxy_routing, axiom,
    tm_digital_signatures != tm_network_proxy_routing).

fof(bg_dist_tm_digital_signatures_tm_network_security_protocols, axiom,
    tm_digital_signatures != tm_network_security_protocols).

fof(bg_dist_tm_digital_signatures_tm_operating_system_security, axiom,
    tm_digital_signatures != tm_operating_system_security).

fof(bg_dist_tm_digital_signatures_tm_organisational_measure, axiom,
    tm_digital_signatures != tm_organisational_measure).

fof(bg_dist_tm_digital_signatures_tm_password_authentication, axiom,
    tm_digital_signatures != tm_password_authentication).

fof(bg_dist_tm_digital_signatures_tm_penetration_testing_methods, axiom,
    tm_digital_signatures != tm_penetration_testing_methods).

fof(bg_dist_tm_digital_signatures_tm_physical_measure, axiom,
    tm_digital_signatures != tm_physical_measure).

fof(bg_dist_tm_digital_signatures_tm_post_quantum_cryptography, axiom,
    tm_digital_signatures != tm_post_quantum_cryptography).

fof(bg_dist_tm_digital_signatures_tm_privacy_preserving_protocol, axiom,
    tm_digital_signatures != tm_privacy_preserving_protocol).

fof(bg_dist_tm_digital_signatures_tm_private_information_retrieval, axiom,
    tm_digital_signatures != tm_private_information_retrieval).

fof(bg_dist_tm_digital_signatures_tm_pseudonymisation, axiom,
    tm_digital_signatures != tm_pseudonymisation).

fof(bg_dist_tm_digital_signatures_tm_quantum_cryptography, axiom,
    tm_digital_signatures != tm_quantum_cryptography).

fof(bg_dist_tm_digital_signatures_tm_r_n_g_pseudonymisation, axiom,
    tm_digital_signatures != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_digital_signatures_tm_secret_sharing_schemes, axiom,
    tm_digital_signatures != tm_secret_sharing_schemes).

fof(bg_dist_tm_digital_signatures_tm_secure_multi_party_computation, axiom,
    tm_digital_signatures != tm_secure_multi_party_computation).

fof(bg_dist_tm_digital_signatures_tm_security_method, axiom,
    tm_digital_signatures != tm_security_method).

fof(bg_dist_tm_digital_signatures_tm_single_sign_on, axiom,
    tm_digital_signatures != tm_single_sign_on).

fof(bg_dist_tm_digital_signatures_tm_symmetric_cryptography, axiom,
    tm_digital_signatures != tm_symmetric_cryptography).

fof(bg_dist_tm_digital_signatures_tm_symmetric_encryption, axiom,
    tm_digital_signatures != tm_symmetric_encryption).

fof(bg_dist_tm_digital_signatures_tm_technical_measure, axiom,
    tm_digital_signatures != tm_technical_measure).

fof(bg_dist_tm_digital_signatures_tm_technical_organisational_measure, axiom,
    tm_digital_signatures != tm_technical_organisational_measure).

fof(bg_dist_tm_digital_signatures_tm_trusted_computing, axiom,
    tm_digital_signatures != tm_trusted_computing).

fof(bg_dist_tm_digital_signatures_tm_trusted_execution_environment, axiom,
    tm_digital_signatures != tm_trusted_execution_environment).

fof(bg_dist_tm_digital_signatures_tm_usage_control, axiom,
    tm_digital_signatures != tm_usage_control).

fof(bg_dist_tm_digital_signatures_tm_use_synthetic_data, axiom,
    tm_digital_signatures != tm_use_synthetic_data).

fof(bg_dist_tm_digital_signatures_tm_virtualisation_security, axiom,
    tm_digital_signatures != tm_virtualisation_security).

fof(bg_dist_tm_digital_signatures_tm_vulnerability_testing_methods, axiom,
    tm_digital_signatures != tm_vulnerability_testing_methods).

fof(bg_dist_tm_digital_signatures_tm_web_browser_security, axiom,
    tm_digital_signatures != tm_web_browser_security).

fof(bg_dist_tm_digital_signatures_tm_web_security_protocols, axiom,
    tm_digital_signatures != tm_web_security_protocols).

fof(bg_dist_tm_digital_signatures_tm_wireless_security_protocols, axiom,
    tm_digital_signatures != tm_wireless_security_protocols).

fof(bg_dist_tm_digital_signatures_tm_zero_knowledge_authentication, axiom,
    tm_digital_signatures != tm_zero_knowledge_authentication).

fof(bg_dist_tm_distributed_system_security_tm_document_randomised_pseudonymisation, axiom,
    tm_distributed_system_security != tm_document_randomised_pseudonymisation).

fof(bg_dist_tm_distributed_system_security_tm_document_security, axiom,
    tm_distributed_system_security != tm_document_security).

fof(bg_dist_tm_distributed_system_security_tm_encryption_in_transfer, axiom,
    tm_distributed_system_security != tm_encryption_in_transfer).

fof(bg_dist_tm_distributed_system_security_tm_encryption_in_use, axiom,
    tm_distributed_system_security != tm_encryption_in_use).

fof(bg_dist_tm_distributed_system_security_tm_end_to_end_encryption, axiom,
    tm_distributed_system_security != tm_end_to_end_encryption).

fof(bg_dist_tm_distributed_system_security_tm_fail_safe_protocols, axiom,
    tm_distributed_system_security != tm_fail_safe_protocols).

fof(bg_dist_tm_distributed_system_security_tm_file_system_security, axiom,
    tm_distributed_system_security != tm_file_system_security).

fof(bg_dist_tm_distributed_system_security_tm_fully_randomised_pseudonymisation, axiom,
    tm_distributed_system_security != tm_fully_randomised_pseudonymisation).

fof(bg_dist_tm_distributed_system_security_tm_hardware_security_protocols, axiom,
    tm_distributed_system_security != tm_hardware_security_protocols).

fof(bg_dist_tm_distributed_system_security_tm_hash_functions, axiom,
    tm_distributed_system_security != tm_hash_functions).

fof(bg_dist_tm_distributed_system_security_tm_hash_message_authentication_code, axiom,
    tm_distributed_system_security != tm_hash_message_authentication_code).

fof(bg_dist_tm_distributed_system_security_tm_homomorphic_encryption, axiom,
    tm_distributed_system_security != tm_homomorphic_encryption).

fof(bg_dist_tm_distributed_system_security_tm_information_flow_control, axiom,
    tm_distributed_system_security != tm_information_flow_control).

fof(bg_dist_tm_distributed_system_security_tm_intrusion_detection_system, axiom,
    tm_distributed_system_security != tm_intrusion_detection_system).

fof(bg_dist_tm_distributed_system_security_tm_legal_measure, axiom,
    tm_distributed_system_security != tm_legal_measure).

fof(bg_dist_tm_distributed_system_security_tm_message_authentication_codes, axiom,
    tm_distributed_system_security != tm_message_authentication_codes).

fof(bg_dist_tm_distributed_system_security_tm_mobile_platform_security, axiom,
    tm_distributed_system_security != tm_mobile_platform_security).

fof(bg_dist_tm_distributed_system_security_tm_monotonic_counter_pseudonymisation, axiom,
    tm_distributed_system_security != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_distributed_system_security_tm_multi_factor_authentication, axiom,
    tm_distributed_system_security != tm_multi_factor_authentication).

fof(bg_dist_tm_distributed_system_security_tm_network_proxy_routing, axiom,
    tm_distributed_system_security != tm_network_proxy_routing).

fof(bg_dist_tm_distributed_system_security_tm_network_security_protocols, axiom,
    tm_distributed_system_security != tm_network_security_protocols).

fof(bg_dist_tm_distributed_system_security_tm_operating_system_security, axiom,
    tm_distributed_system_security != tm_operating_system_security).

fof(bg_dist_tm_distributed_system_security_tm_organisational_measure, axiom,
    tm_distributed_system_security != tm_organisational_measure).

fof(bg_dist_tm_distributed_system_security_tm_password_authentication, axiom,
    tm_distributed_system_security != tm_password_authentication).

fof(bg_dist_tm_distributed_system_security_tm_penetration_testing_methods, axiom,
    tm_distributed_system_security != tm_penetration_testing_methods).

fof(bg_dist_tm_distributed_system_security_tm_physical_measure, axiom,
    tm_distributed_system_security != tm_physical_measure).

fof(bg_dist_tm_distributed_system_security_tm_post_quantum_cryptography, axiom,
    tm_distributed_system_security != tm_post_quantum_cryptography).

fof(bg_dist_tm_distributed_system_security_tm_privacy_preserving_protocol, axiom,
    tm_distributed_system_security != tm_privacy_preserving_protocol).

fof(bg_dist_tm_distributed_system_security_tm_private_information_retrieval, axiom,
    tm_distributed_system_security != tm_private_information_retrieval).

fof(bg_dist_tm_distributed_system_security_tm_pseudonymisation, axiom,
    tm_distributed_system_security != tm_pseudonymisation).

fof(bg_dist_tm_distributed_system_security_tm_quantum_cryptography, axiom,
    tm_distributed_system_security != tm_quantum_cryptography).

fof(bg_dist_tm_distributed_system_security_tm_r_n_g_pseudonymisation, axiom,
    tm_distributed_system_security != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_distributed_system_security_tm_secret_sharing_schemes, axiom,
    tm_distributed_system_security != tm_secret_sharing_schemes).

fof(bg_dist_tm_distributed_system_security_tm_secure_multi_party_computation, axiom,
    tm_distributed_system_security != tm_secure_multi_party_computation).

fof(bg_dist_tm_distributed_system_security_tm_security_method, axiom,
    tm_distributed_system_security != tm_security_method).

fof(bg_dist_tm_distributed_system_security_tm_single_sign_on, axiom,
    tm_distributed_system_security != tm_single_sign_on).

fof(bg_dist_tm_distributed_system_security_tm_symmetric_cryptography, axiom,
    tm_distributed_system_security != tm_symmetric_cryptography).

fof(bg_dist_tm_distributed_system_security_tm_symmetric_encryption, axiom,
    tm_distributed_system_security != tm_symmetric_encryption).

fof(bg_dist_tm_distributed_system_security_tm_technical_measure, axiom,
    tm_distributed_system_security != tm_technical_measure).

fof(bg_dist_tm_distributed_system_security_tm_technical_organisational_measure, axiom,
    tm_distributed_system_security != tm_technical_organisational_measure).

fof(bg_dist_tm_distributed_system_security_tm_trusted_computing, axiom,
    tm_distributed_system_security != tm_trusted_computing).

fof(bg_dist_tm_distributed_system_security_tm_trusted_execution_environment, axiom,
    tm_distributed_system_security != tm_trusted_execution_environment).

fof(bg_dist_tm_distributed_system_security_tm_usage_control, axiom,
    tm_distributed_system_security != tm_usage_control).

fof(bg_dist_tm_distributed_system_security_tm_use_synthetic_data, axiom,
    tm_distributed_system_security != tm_use_synthetic_data).

fof(bg_dist_tm_distributed_system_security_tm_virtualisation_security, axiom,
    tm_distributed_system_security != tm_virtualisation_security).

fof(bg_dist_tm_distributed_system_security_tm_vulnerability_testing_methods, axiom,
    tm_distributed_system_security != tm_vulnerability_testing_methods).

fof(bg_dist_tm_distributed_system_security_tm_web_browser_security, axiom,
    tm_distributed_system_security != tm_web_browser_security).

fof(bg_dist_tm_distributed_system_security_tm_web_security_protocols, axiom,
    tm_distributed_system_security != tm_web_security_protocols).

fof(bg_dist_tm_distributed_system_security_tm_wireless_security_protocols, axiom,
    tm_distributed_system_security != tm_wireless_security_protocols).

fof(bg_dist_tm_distributed_system_security_tm_zero_knowledge_authentication, axiom,
    tm_distributed_system_security != tm_zero_knowledge_authentication).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_document_security, axiom,
    tm_document_randomised_pseudonymisation != tm_document_security).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_encryption_in_transfer, axiom,
    tm_document_randomised_pseudonymisation != tm_encryption_in_transfer).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_encryption_in_use, axiom,
    tm_document_randomised_pseudonymisation != tm_encryption_in_use).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_end_to_end_encryption, axiom,
    tm_document_randomised_pseudonymisation != tm_end_to_end_encryption).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_fail_safe_protocols, axiom,
    tm_document_randomised_pseudonymisation != tm_fail_safe_protocols).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_file_system_security, axiom,
    tm_document_randomised_pseudonymisation != tm_file_system_security).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_fully_randomised_pseudonymisation, axiom,
    tm_document_randomised_pseudonymisation != tm_fully_randomised_pseudonymisation).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_hardware_security_protocols, axiom,
    tm_document_randomised_pseudonymisation != tm_hardware_security_protocols).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_hash_functions, axiom,
    tm_document_randomised_pseudonymisation != tm_hash_functions).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_hash_message_authentication_code, axiom,
    tm_document_randomised_pseudonymisation != tm_hash_message_authentication_code).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_homomorphic_encryption, axiom,
    tm_document_randomised_pseudonymisation != tm_homomorphic_encryption).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_information_flow_control, axiom,
    tm_document_randomised_pseudonymisation != tm_information_flow_control).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_intrusion_detection_system, axiom,
    tm_document_randomised_pseudonymisation != tm_intrusion_detection_system).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_legal_measure, axiom,
    tm_document_randomised_pseudonymisation != tm_legal_measure).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_message_authentication_codes, axiom,
    tm_document_randomised_pseudonymisation != tm_message_authentication_codes).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_mobile_platform_security, axiom,
    tm_document_randomised_pseudonymisation != tm_mobile_platform_security).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_monotonic_counter_pseudonymisation, axiom,
    tm_document_randomised_pseudonymisation != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_multi_factor_authentication, axiom,
    tm_document_randomised_pseudonymisation != tm_multi_factor_authentication).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_network_proxy_routing, axiom,
    tm_document_randomised_pseudonymisation != tm_network_proxy_routing).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_network_security_protocols, axiom,
    tm_document_randomised_pseudonymisation != tm_network_security_protocols).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_operating_system_security, axiom,
    tm_document_randomised_pseudonymisation != tm_operating_system_security).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_organisational_measure, axiom,
    tm_document_randomised_pseudonymisation != tm_organisational_measure).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_password_authentication, axiom,
    tm_document_randomised_pseudonymisation != tm_password_authentication).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_penetration_testing_methods, axiom,
    tm_document_randomised_pseudonymisation != tm_penetration_testing_methods).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_physical_measure, axiom,
    tm_document_randomised_pseudonymisation != tm_physical_measure).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_post_quantum_cryptography, axiom,
    tm_document_randomised_pseudonymisation != tm_post_quantum_cryptography).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_privacy_preserving_protocol, axiom,
    tm_document_randomised_pseudonymisation != tm_privacy_preserving_protocol).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_private_information_retrieval, axiom,
    tm_document_randomised_pseudonymisation != tm_private_information_retrieval).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_pseudonymisation, axiom,
    tm_document_randomised_pseudonymisation != tm_pseudonymisation).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_quantum_cryptography, axiom,
    tm_document_randomised_pseudonymisation != tm_quantum_cryptography).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_r_n_g_pseudonymisation, axiom,
    tm_document_randomised_pseudonymisation != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_secret_sharing_schemes, axiom,
    tm_document_randomised_pseudonymisation != tm_secret_sharing_schemes).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_secure_multi_party_computation, axiom,
    tm_document_randomised_pseudonymisation != tm_secure_multi_party_computation).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_security_method, axiom,
    tm_document_randomised_pseudonymisation != tm_security_method).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_single_sign_on, axiom,
    tm_document_randomised_pseudonymisation != tm_single_sign_on).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_symmetric_cryptography, axiom,
    tm_document_randomised_pseudonymisation != tm_symmetric_cryptography).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_symmetric_encryption, axiom,
    tm_document_randomised_pseudonymisation != tm_symmetric_encryption).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_technical_measure, axiom,
    tm_document_randomised_pseudonymisation != tm_technical_measure).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_technical_organisational_measure, axiom,
    tm_document_randomised_pseudonymisation != tm_technical_organisational_measure).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_trusted_computing, axiom,
    tm_document_randomised_pseudonymisation != tm_trusted_computing).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_trusted_execution_environment, axiom,
    tm_document_randomised_pseudonymisation != tm_trusted_execution_environment).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_usage_control, axiom,
    tm_document_randomised_pseudonymisation != tm_usage_control).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_use_synthetic_data, axiom,
    tm_document_randomised_pseudonymisation != tm_use_synthetic_data).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_virtualisation_security, axiom,
    tm_document_randomised_pseudonymisation != tm_virtualisation_security).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_vulnerability_testing_methods, axiom,
    tm_document_randomised_pseudonymisation != tm_vulnerability_testing_methods).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_web_browser_security, axiom,
    tm_document_randomised_pseudonymisation != tm_web_browser_security).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_web_security_protocols, axiom,
    tm_document_randomised_pseudonymisation != tm_web_security_protocols).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_wireless_security_protocols, axiom,
    tm_document_randomised_pseudonymisation != tm_wireless_security_protocols).

fof(bg_dist_tm_document_randomised_pseudonymisation_tm_zero_knowledge_authentication, axiom,
    tm_document_randomised_pseudonymisation != tm_zero_knowledge_authentication).

fof(bg_dist_tm_document_security_tm_encryption_in_transfer, axiom,
    tm_document_security != tm_encryption_in_transfer).

fof(bg_dist_tm_document_security_tm_encryption_in_use, axiom,
    tm_document_security != tm_encryption_in_use).

fof(bg_dist_tm_document_security_tm_end_to_end_encryption, axiom,
    tm_document_security != tm_end_to_end_encryption).

fof(bg_dist_tm_document_security_tm_fail_safe_protocols, axiom,
    tm_document_security != tm_fail_safe_protocols).

fof(bg_dist_tm_document_security_tm_file_system_security, axiom,
    tm_document_security != tm_file_system_security).

fof(bg_dist_tm_document_security_tm_fully_randomised_pseudonymisation, axiom,
    tm_document_security != tm_fully_randomised_pseudonymisation).

fof(bg_dist_tm_document_security_tm_hardware_security_protocols, axiom,
    tm_document_security != tm_hardware_security_protocols).

fof(bg_dist_tm_document_security_tm_hash_functions, axiom,
    tm_document_security != tm_hash_functions).

fof(bg_dist_tm_document_security_tm_hash_message_authentication_code, axiom,
    tm_document_security != tm_hash_message_authentication_code).

fof(bg_dist_tm_document_security_tm_homomorphic_encryption, axiom,
    tm_document_security != tm_homomorphic_encryption).

fof(bg_dist_tm_document_security_tm_information_flow_control, axiom,
    tm_document_security != tm_information_flow_control).

fof(bg_dist_tm_document_security_tm_intrusion_detection_system, axiom,
    tm_document_security != tm_intrusion_detection_system).

fof(bg_dist_tm_document_security_tm_legal_measure, axiom,
    tm_document_security != tm_legal_measure).

fof(bg_dist_tm_document_security_tm_message_authentication_codes, axiom,
    tm_document_security != tm_message_authentication_codes).

fof(bg_dist_tm_document_security_tm_mobile_platform_security, axiom,
    tm_document_security != tm_mobile_platform_security).

fof(bg_dist_tm_document_security_tm_monotonic_counter_pseudonymisation, axiom,
    tm_document_security != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_document_security_tm_multi_factor_authentication, axiom,
    tm_document_security != tm_multi_factor_authentication).

fof(bg_dist_tm_document_security_tm_network_proxy_routing, axiom,
    tm_document_security != tm_network_proxy_routing).

fof(bg_dist_tm_document_security_tm_network_security_protocols, axiom,
    tm_document_security != tm_network_security_protocols).

fof(bg_dist_tm_document_security_tm_operating_system_security, axiom,
    tm_document_security != tm_operating_system_security).

fof(bg_dist_tm_document_security_tm_organisational_measure, axiom,
    tm_document_security != tm_organisational_measure).

fof(bg_dist_tm_document_security_tm_password_authentication, axiom,
    tm_document_security != tm_password_authentication).

fof(bg_dist_tm_document_security_tm_penetration_testing_methods, axiom,
    tm_document_security != tm_penetration_testing_methods).

fof(bg_dist_tm_document_security_tm_physical_measure, axiom,
    tm_document_security != tm_physical_measure).

fof(bg_dist_tm_document_security_tm_post_quantum_cryptography, axiom,
    tm_document_security != tm_post_quantum_cryptography).

fof(bg_dist_tm_document_security_tm_privacy_preserving_protocol, axiom,
    tm_document_security != tm_privacy_preserving_protocol).

fof(bg_dist_tm_document_security_tm_private_information_retrieval, axiom,
    tm_document_security != tm_private_information_retrieval).

fof(bg_dist_tm_document_security_tm_pseudonymisation, axiom,
    tm_document_security != tm_pseudonymisation).

fof(bg_dist_tm_document_security_tm_quantum_cryptography, axiom,
    tm_document_security != tm_quantum_cryptography).

fof(bg_dist_tm_document_security_tm_r_n_g_pseudonymisation, axiom,
    tm_document_security != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_document_security_tm_secret_sharing_schemes, axiom,
    tm_document_security != tm_secret_sharing_schemes).

fof(bg_dist_tm_document_security_tm_secure_multi_party_computation, axiom,
    tm_document_security != tm_secure_multi_party_computation).

fof(bg_dist_tm_document_security_tm_security_method, axiom,
    tm_document_security != tm_security_method).

fof(bg_dist_tm_document_security_tm_single_sign_on, axiom,
    tm_document_security != tm_single_sign_on).

fof(bg_dist_tm_document_security_tm_symmetric_cryptography, axiom,
    tm_document_security != tm_symmetric_cryptography).

fof(bg_dist_tm_document_security_tm_symmetric_encryption, axiom,
    tm_document_security != tm_symmetric_encryption).

fof(bg_dist_tm_document_security_tm_technical_measure, axiom,
    tm_document_security != tm_technical_measure).

fof(bg_dist_tm_document_security_tm_technical_organisational_measure, axiom,
    tm_document_security != tm_technical_organisational_measure).

fof(bg_dist_tm_document_security_tm_trusted_computing, axiom,
    tm_document_security != tm_trusted_computing).

fof(bg_dist_tm_document_security_tm_trusted_execution_environment, axiom,
    tm_document_security != tm_trusted_execution_environment).

fof(bg_dist_tm_document_security_tm_usage_control, axiom,
    tm_document_security != tm_usage_control).

fof(bg_dist_tm_document_security_tm_use_synthetic_data, axiom,
    tm_document_security != tm_use_synthetic_data).

fof(bg_dist_tm_document_security_tm_virtualisation_security, axiom,
    tm_document_security != tm_virtualisation_security).

fof(bg_dist_tm_document_security_tm_vulnerability_testing_methods, axiom,
    tm_document_security != tm_vulnerability_testing_methods).

fof(bg_dist_tm_document_security_tm_web_browser_security, axiom,
    tm_document_security != tm_web_browser_security).

fof(bg_dist_tm_document_security_tm_web_security_protocols, axiom,
    tm_document_security != tm_web_security_protocols).

fof(bg_dist_tm_document_security_tm_wireless_security_protocols, axiom,
    tm_document_security != tm_wireless_security_protocols).

fof(bg_dist_tm_document_security_tm_zero_knowledge_authentication, axiom,
    tm_document_security != tm_zero_knowledge_authentication).

fof(bg_dist_tm_encryption_in_transfer_tm_encryption_in_use, axiom,
    tm_encryption_in_transfer != tm_encryption_in_use).

fof(bg_dist_tm_encryption_in_transfer_tm_end_to_end_encryption, axiom,
    tm_encryption_in_transfer != tm_end_to_end_encryption).

fof(bg_dist_tm_encryption_in_transfer_tm_fail_safe_protocols, axiom,
    tm_encryption_in_transfer != tm_fail_safe_protocols).

fof(bg_dist_tm_encryption_in_transfer_tm_file_system_security, axiom,
    tm_encryption_in_transfer != tm_file_system_security).

fof(bg_dist_tm_encryption_in_transfer_tm_fully_randomised_pseudonymisation, axiom,
    tm_encryption_in_transfer != tm_fully_randomised_pseudonymisation).

fof(bg_dist_tm_encryption_in_transfer_tm_hardware_security_protocols, axiom,
    tm_encryption_in_transfer != tm_hardware_security_protocols).

fof(bg_dist_tm_encryption_in_transfer_tm_hash_functions, axiom,
    tm_encryption_in_transfer != tm_hash_functions).

fof(bg_dist_tm_encryption_in_transfer_tm_hash_message_authentication_code, axiom,
    tm_encryption_in_transfer != tm_hash_message_authentication_code).

fof(bg_dist_tm_encryption_in_transfer_tm_homomorphic_encryption, axiom,
    tm_encryption_in_transfer != tm_homomorphic_encryption).

fof(bg_dist_tm_encryption_in_transfer_tm_information_flow_control, axiom,
    tm_encryption_in_transfer != tm_information_flow_control).

fof(bg_dist_tm_encryption_in_transfer_tm_intrusion_detection_system, axiom,
    tm_encryption_in_transfer != tm_intrusion_detection_system).

fof(bg_dist_tm_encryption_in_transfer_tm_legal_measure, axiom,
    tm_encryption_in_transfer != tm_legal_measure).

fof(bg_dist_tm_encryption_in_transfer_tm_message_authentication_codes, axiom,
    tm_encryption_in_transfer != tm_message_authentication_codes).

fof(bg_dist_tm_encryption_in_transfer_tm_mobile_platform_security, axiom,
    tm_encryption_in_transfer != tm_mobile_platform_security).

fof(bg_dist_tm_encryption_in_transfer_tm_monotonic_counter_pseudonymisation, axiom,
    tm_encryption_in_transfer != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_encryption_in_transfer_tm_multi_factor_authentication, axiom,
    tm_encryption_in_transfer != tm_multi_factor_authentication).

fof(bg_dist_tm_encryption_in_transfer_tm_network_proxy_routing, axiom,
    tm_encryption_in_transfer != tm_network_proxy_routing).

fof(bg_dist_tm_encryption_in_transfer_tm_network_security_protocols, axiom,
    tm_encryption_in_transfer != tm_network_security_protocols).

fof(bg_dist_tm_encryption_in_transfer_tm_operating_system_security, axiom,
    tm_encryption_in_transfer != tm_operating_system_security).

fof(bg_dist_tm_encryption_in_transfer_tm_organisational_measure, axiom,
    tm_encryption_in_transfer != tm_organisational_measure).

fof(bg_dist_tm_encryption_in_transfer_tm_password_authentication, axiom,
    tm_encryption_in_transfer != tm_password_authentication).

fof(bg_dist_tm_encryption_in_transfer_tm_penetration_testing_methods, axiom,
    tm_encryption_in_transfer != tm_penetration_testing_methods).

fof(bg_dist_tm_encryption_in_transfer_tm_physical_measure, axiom,
    tm_encryption_in_transfer != tm_physical_measure).

fof(bg_dist_tm_encryption_in_transfer_tm_post_quantum_cryptography, axiom,
    tm_encryption_in_transfer != tm_post_quantum_cryptography).

fof(bg_dist_tm_encryption_in_transfer_tm_privacy_preserving_protocol, axiom,
    tm_encryption_in_transfer != tm_privacy_preserving_protocol).

fof(bg_dist_tm_encryption_in_transfer_tm_private_information_retrieval, axiom,
    tm_encryption_in_transfer != tm_private_information_retrieval).

fof(bg_dist_tm_encryption_in_transfer_tm_pseudonymisation, axiom,
    tm_encryption_in_transfer != tm_pseudonymisation).

fof(bg_dist_tm_encryption_in_transfer_tm_quantum_cryptography, axiom,
    tm_encryption_in_transfer != tm_quantum_cryptography).

fof(bg_dist_tm_encryption_in_transfer_tm_r_n_g_pseudonymisation, axiom,
    tm_encryption_in_transfer != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_encryption_in_transfer_tm_secret_sharing_schemes, axiom,
    tm_encryption_in_transfer != tm_secret_sharing_schemes).

fof(bg_dist_tm_encryption_in_transfer_tm_secure_multi_party_computation, axiom,
    tm_encryption_in_transfer != tm_secure_multi_party_computation).

fof(bg_dist_tm_encryption_in_transfer_tm_security_method, axiom,
    tm_encryption_in_transfer != tm_security_method).

fof(bg_dist_tm_encryption_in_transfer_tm_single_sign_on, axiom,
    tm_encryption_in_transfer != tm_single_sign_on).

fof(bg_dist_tm_encryption_in_transfer_tm_symmetric_cryptography, axiom,
    tm_encryption_in_transfer != tm_symmetric_cryptography).

fof(bg_dist_tm_encryption_in_transfer_tm_symmetric_encryption, axiom,
    tm_encryption_in_transfer != tm_symmetric_encryption).

fof(bg_dist_tm_encryption_in_transfer_tm_technical_measure, axiom,
    tm_encryption_in_transfer != tm_technical_measure).

fof(bg_dist_tm_encryption_in_transfer_tm_technical_organisational_measure, axiom,
    tm_encryption_in_transfer != tm_technical_organisational_measure).

fof(bg_dist_tm_encryption_in_transfer_tm_trusted_computing, axiom,
    tm_encryption_in_transfer != tm_trusted_computing).

fof(bg_dist_tm_encryption_in_transfer_tm_trusted_execution_environment, axiom,
    tm_encryption_in_transfer != tm_trusted_execution_environment).

fof(bg_dist_tm_encryption_in_transfer_tm_usage_control, axiom,
    tm_encryption_in_transfer != tm_usage_control).

fof(bg_dist_tm_encryption_in_transfer_tm_use_synthetic_data, axiom,
    tm_encryption_in_transfer != tm_use_synthetic_data).

fof(bg_dist_tm_encryption_in_transfer_tm_virtualisation_security, axiom,
    tm_encryption_in_transfer != tm_virtualisation_security).

fof(bg_dist_tm_encryption_in_transfer_tm_vulnerability_testing_methods, axiom,
    tm_encryption_in_transfer != tm_vulnerability_testing_methods).

fof(bg_dist_tm_encryption_in_transfer_tm_web_browser_security, axiom,
    tm_encryption_in_transfer != tm_web_browser_security).

fof(bg_dist_tm_encryption_in_transfer_tm_web_security_protocols, axiom,
    tm_encryption_in_transfer != tm_web_security_protocols).

fof(bg_dist_tm_encryption_in_transfer_tm_wireless_security_protocols, axiom,
    tm_encryption_in_transfer != tm_wireless_security_protocols).

fof(bg_dist_tm_encryption_in_transfer_tm_zero_knowledge_authentication, axiom,
    tm_encryption_in_transfer != tm_zero_knowledge_authentication).

fof(bg_dist_tm_encryption_in_use_tm_end_to_end_encryption, axiom,
    tm_encryption_in_use != tm_end_to_end_encryption).

fof(bg_dist_tm_encryption_in_use_tm_fail_safe_protocols, axiom,
    tm_encryption_in_use != tm_fail_safe_protocols).

fof(bg_dist_tm_encryption_in_use_tm_file_system_security, axiom,
    tm_encryption_in_use != tm_file_system_security).

fof(bg_dist_tm_encryption_in_use_tm_fully_randomised_pseudonymisation, axiom,
    tm_encryption_in_use != tm_fully_randomised_pseudonymisation).

fof(bg_dist_tm_encryption_in_use_tm_hardware_security_protocols, axiom,
    tm_encryption_in_use != tm_hardware_security_protocols).

fof(bg_dist_tm_encryption_in_use_tm_hash_functions, axiom,
    tm_encryption_in_use != tm_hash_functions).

fof(bg_dist_tm_encryption_in_use_tm_hash_message_authentication_code, axiom,
    tm_encryption_in_use != tm_hash_message_authentication_code).

fof(bg_dist_tm_encryption_in_use_tm_homomorphic_encryption, axiom,
    tm_encryption_in_use != tm_homomorphic_encryption).

fof(bg_dist_tm_encryption_in_use_tm_information_flow_control, axiom,
    tm_encryption_in_use != tm_information_flow_control).

fof(bg_dist_tm_encryption_in_use_tm_intrusion_detection_system, axiom,
    tm_encryption_in_use != tm_intrusion_detection_system).

fof(bg_dist_tm_encryption_in_use_tm_legal_measure, axiom,
    tm_encryption_in_use != tm_legal_measure).

fof(bg_dist_tm_encryption_in_use_tm_message_authentication_codes, axiom,
    tm_encryption_in_use != tm_message_authentication_codes).

fof(bg_dist_tm_encryption_in_use_tm_mobile_platform_security, axiom,
    tm_encryption_in_use != tm_mobile_platform_security).

fof(bg_dist_tm_encryption_in_use_tm_monotonic_counter_pseudonymisation, axiom,
    tm_encryption_in_use != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_encryption_in_use_tm_multi_factor_authentication, axiom,
    tm_encryption_in_use != tm_multi_factor_authentication).

fof(bg_dist_tm_encryption_in_use_tm_network_proxy_routing, axiom,
    tm_encryption_in_use != tm_network_proxy_routing).

fof(bg_dist_tm_encryption_in_use_tm_network_security_protocols, axiom,
    tm_encryption_in_use != tm_network_security_protocols).

fof(bg_dist_tm_encryption_in_use_tm_operating_system_security, axiom,
    tm_encryption_in_use != tm_operating_system_security).

fof(bg_dist_tm_encryption_in_use_tm_organisational_measure, axiom,
    tm_encryption_in_use != tm_organisational_measure).

fof(bg_dist_tm_encryption_in_use_tm_password_authentication, axiom,
    tm_encryption_in_use != tm_password_authentication).

fof(bg_dist_tm_encryption_in_use_tm_penetration_testing_methods, axiom,
    tm_encryption_in_use != tm_penetration_testing_methods).

fof(bg_dist_tm_encryption_in_use_tm_physical_measure, axiom,
    tm_encryption_in_use != tm_physical_measure).

fof(bg_dist_tm_encryption_in_use_tm_post_quantum_cryptography, axiom,
    tm_encryption_in_use != tm_post_quantum_cryptography).

fof(bg_dist_tm_encryption_in_use_tm_privacy_preserving_protocol, axiom,
    tm_encryption_in_use != tm_privacy_preserving_protocol).

fof(bg_dist_tm_encryption_in_use_tm_private_information_retrieval, axiom,
    tm_encryption_in_use != tm_private_information_retrieval).

fof(bg_dist_tm_encryption_in_use_tm_pseudonymisation, axiom,
    tm_encryption_in_use != tm_pseudonymisation).

fof(bg_dist_tm_encryption_in_use_tm_quantum_cryptography, axiom,
    tm_encryption_in_use != tm_quantum_cryptography).

fof(bg_dist_tm_encryption_in_use_tm_r_n_g_pseudonymisation, axiom,
    tm_encryption_in_use != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_encryption_in_use_tm_secret_sharing_schemes, axiom,
    tm_encryption_in_use != tm_secret_sharing_schemes).

fof(bg_dist_tm_encryption_in_use_tm_secure_multi_party_computation, axiom,
    tm_encryption_in_use != tm_secure_multi_party_computation).

fof(bg_dist_tm_encryption_in_use_tm_security_method, axiom,
    tm_encryption_in_use != tm_security_method).

fof(bg_dist_tm_encryption_in_use_tm_single_sign_on, axiom,
    tm_encryption_in_use != tm_single_sign_on).

fof(bg_dist_tm_encryption_in_use_tm_symmetric_cryptography, axiom,
    tm_encryption_in_use != tm_symmetric_cryptography).

fof(bg_dist_tm_encryption_in_use_tm_symmetric_encryption, axiom,
    tm_encryption_in_use != tm_symmetric_encryption).

fof(bg_dist_tm_encryption_in_use_tm_technical_measure, axiom,
    tm_encryption_in_use != tm_technical_measure).

fof(bg_dist_tm_encryption_in_use_tm_technical_organisational_measure, axiom,
    tm_encryption_in_use != tm_technical_organisational_measure).

fof(bg_dist_tm_encryption_in_use_tm_trusted_computing, axiom,
    tm_encryption_in_use != tm_trusted_computing).

fof(bg_dist_tm_encryption_in_use_tm_trusted_execution_environment, axiom,
    tm_encryption_in_use != tm_trusted_execution_environment).

fof(bg_dist_tm_encryption_in_use_tm_usage_control, axiom,
    tm_encryption_in_use != tm_usage_control).

fof(bg_dist_tm_encryption_in_use_tm_use_synthetic_data, axiom,
    tm_encryption_in_use != tm_use_synthetic_data).

fof(bg_dist_tm_encryption_in_use_tm_virtualisation_security, axiom,
    tm_encryption_in_use != tm_virtualisation_security).

fof(bg_dist_tm_encryption_in_use_tm_vulnerability_testing_methods, axiom,
    tm_encryption_in_use != tm_vulnerability_testing_methods).

fof(bg_dist_tm_encryption_in_use_tm_web_browser_security, axiom,
    tm_encryption_in_use != tm_web_browser_security).

fof(bg_dist_tm_encryption_in_use_tm_web_security_protocols, axiom,
    tm_encryption_in_use != tm_web_security_protocols).

fof(bg_dist_tm_encryption_in_use_tm_wireless_security_protocols, axiom,
    tm_encryption_in_use != tm_wireless_security_protocols).

fof(bg_dist_tm_encryption_in_use_tm_zero_knowledge_authentication, axiom,
    tm_encryption_in_use != tm_zero_knowledge_authentication).

fof(bg_dist_tm_end_to_end_encryption_tm_fail_safe_protocols, axiom,
    tm_end_to_end_encryption != tm_fail_safe_protocols).

fof(bg_dist_tm_end_to_end_encryption_tm_file_system_security, axiom,
    tm_end_to_end_encryption != tm_file_system_security).

fof(bg_dist_tm_end_to_end_encryption_tm_fully_randomised_pseudonymisation, axiom,
    tm_end_to_end_encryption != tm_fully_randomised_pseudonymisation).

fof(bg_dist_tm_end_to_end_encryption_tm_hardware_security_protocols, axiom,
    tm_end_to_end_encryption != tm_hardware_security_protocols).

fof(bg_dist_tm_end_to_end_encryption_tm_hash_functions, axiom,
    tm_end_to_end_encryption != tm_hash_functions).

fof(bg_dist_tm_end_to_end_encryption_tm_hash_message_authentication_code, axiom,
    tm_end_to_end_encryption != tm_hash_message_authentication_code).

fof(bg_dist_tm_end_to_end_encryption_tm_homomorphic_encryption, axiom,
    tm_end_to_end_encryption != tm_homomorphic_encryption).

fof(bg_dist_tm_end_to_end_encryption_tm_information_flow_control, axiom,
    tm_end_to_end_encryption != tm_information_flow_control).

fof(bg_dist_tm_end_to_end_encryption_tm_intrusion_detection_system, axiom,
    tm_end_to_end_encryption != tm_intrusion_detection_system).

fof(bg_dist_tm_end_to_end_encryption_tm_legal_measure, axiom,
    tm_end_to_end_encryption != tm_legal_measure).

fof(bg_dist_tm_end_to_end_encryption_tm_message_authentication_codes, axiom,
    tm_end_to_end_encryption != tm_message_authentication_codes).

fof(bg_dist_tm_end_to_end_encryption_tm_mobile_platform_security, axiom,
    tm_end_to_end_encryption != tm_mobile_platform_security).

fof(bg_dist_tm_end_to_end_encryption_tm_monotonic_counter_pseudonymisation, axiom,
    tm_end_to_end_encryption != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_end_to_end_encryption_tm_multi_factor_authentication, axiom,
    tm_end_to_end_encryption != tm_multi_factor_authentication).

fof(bg_dist_tm_end_to_end_encryption_tm_network_proxy_routing, axiom,
    tm_end_to_end_encryption != tm_network_proxy_routing).

fof(bg_dist_tm_end_to_end_encryption_tm_network_security_protocols, axiom,
    tm_end_to_end_encryption != tm_network_security_protocols).

fof(bg_dist_tm_end_to_end_encryption_tm_operating_system_security, axiom,
    tm_end_to_end_encryption != tm_operating_system_security).

fof(bg_dist_tm_end_to_end_encryption_tm_organisational_measure, axiom,
    tm_end_to_end_encryption != tm_organisational_measure).

fof(bg_dist_tm_end_to_end_encryption_tm_password_authentication, axiom,
    tm_end_to_end_encryption != tm_password_authentication).

fof(bg_dist_tm_end_to_end_encryption_tm_penetration_testing_methods, axiom,
    tm_end_to_end_encryption != tm_penetration_testing_methods).

fof(bg_dist_tm_end_to_end_encryption_tm_physical_measure, axiom,
    tm_end_to_end_encryption != tm_physical_measure).

fof(bg_dist_tm_end_to_end_encryption_tm_post_quantum_cryptography, axiom,
    tm_end_to_end_encryption != tm_post_quantum_cryptography).

fof(bg_dist_tm_end_to_end_encryption_tm_privacy_preserving_protocol, axiom,
    tm_end_to_end_encryption != tm_privacy_preserving_protocol).

fof(bg_dist_tm_end_to_end_encryption_tm_private_information_retrieval, axiom,
    tm_end_to_end_encryption != tm_private_information_retrieval).

fof(bg_dist_tm_end_to_end_encryption_tm_pseudonymisation, axiom,
    tm_end_to_end_encryption != tm_pseudonymisation).

fof(bg_dist_tm_end_to_end_encryption_tm_quantum_cryptography, axiom,
    tm_end_to_end_encryption != tm_quantum_cryptography).

fof(bg_dist_tm_end_to_end_encryption_tm_r_n_g_pseudonymisation, axiom,
    tm_end_to_end_encryption != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_end_to_end_encryption_tm_secret_sharing_schemes, axiom,
    tm_end_to_end_encryption != tm_secret_sharing_schemes).

fof(bg_dist_tm_end_to_end_encryption_tm_secure_multi_party_computation, axiom,
    tm_end_to_end_encryption != tm_secure_multi_party_computation).

fof(bg_dist_tm_end_to_end_encryption_tm_security_method, axiom,
    tm_end_to_end_encryption != tm_security_method).

fof(bg_dist_tm_end_to_end_encryption_tm_single_sign_on, axiom,
    tm_end_to_end_encryption != tm_single_sign_on).

fof(bg_dist_tm_end_to_end_encryption_tm_symmetric_cryptography, axiom,
    tm_end_to_end_encryption != tm_symmetric_cryptography).

fof(bg_dist_tm_end_to_end_encryption_tm_symmetric_encryption, axiom,
    tm_end_to_end_encryption != tm_symmetric_encryption).

fof(bg_dist_tm_end_to_end_encryption_tm_technical_measure, axiom,
    tm_end_to_end_encryption != tm_technical_measure).

fof(bg_dist_tm_end_to_end_encryption_tm_technical_organisational_measure, axiom,
    tm_end_to_end_encryption != tm_technical_organisational_measure).

fof(bg_dist_tm_end_to_end_encryption_tm_trusted_computing, axiom,
    tm_end_to_end_encryption != tm_trusted_computing).

fof(bg_dist_tm_end_to_end_encryption_tm_trusted_execution_environment, axiom,
    tm_end_to_end_encryption != tm_trusted_execution_environment).

fof(bg_dist_tm_end_to_end_encryption_tm_usage_control, axiom,
    tm_end_to_end_encryption != tm_usage_control).

fof(bg_dist_tm_end_to_end_encryption_tm_use_synthetic_data, axiom,
    tm_end_to_end_encryption != tm_use_synthetic_data).

fof(bg_dist_tm_end_to_end_encryption_tm_virtualisation_security, axiom,
    tm_end_to_end_encryption != tm_virtualisation_security).

fof(bg_dist_tm_end_to_end_encryption_tm_vulnerability_testing_methods, axiom,
    tm_end_to_end_encryption != tm_vulnerability_testing_methods).

fof(bg_dist_tm_end_to_end_encryption_tm_web_browser_security, axiom,
    tm_end_to_end_encryption != tm_web_browser_security).

fof(bg_dist_tm_end_to_end_encryption_tm_web_security_protocols, axiom,
    tm_end_to_end_encryption != tm_web_security_protocols).

fof(bg_dist_tm_end_to_end_encryption_tm_wireless_security_protocols, axiom,
    tm_end_to_end_encryption != tm_wireless_security_protocols).

fof(bg_dist_tm_end_to_end_encryption_tm_zero_knowledge_authentication, axiom,
    tm_end_to_end_encryption != tm_zero_knowledge_authentication).

fof(bg_dist_tm_fail_safe_protocols_tm_file_system_security, axiom,
    tm_fail_safe_protocols != tm_file_system_security).

fof(bg_dist_tm_fail_safe_protocols_tm_fully_randomised_pseudonymisation, axiom,
    tm_fail_safe_protocols != tm_fully_randomised_pseudonymisation).

fof(bg_dist_tm_fail_safe_protocols_tm_hardware_security_protocols, axiom,
    tm_fail_safe_protocols != tm_hardware_security_protocols).

fof(bg_dist_tm_fail_safe_protocols_tm_hash_functions, axiom,
    tm_fail_safe_protocols != tm_hash_functions).

fof(bg_dist_tm_fail_safe_protocols_tm_hash_message_authentication_code, axiom,
    tm_fail_safe_protocols != tm_hash_message_authentication_code).

fof(bg_dist_tm_fail_safe_protocols_tm_homomorphic_encryption, axiom,
    tm_fail_safe_protocols != tm_homomorphic_encryption).

fof(bg_dist_tm_fail_safe_protocols_tm_information_flow_control, axiom,
    tm_fail_safe_protocols != tm_information_flow_control).

fof(bg_dist_tm_fail_safe_protocols_tm_intrusion_detection_system, axiom,
    tm_fail_safe_protocols != tm_intrusion_detection_system).

fof(bg_dist_tm_fail_safe_protocols_tm_legal_measure, axiom,
    tm_fail_safe_protocols != tm_legal_measure).

fof(bg_dist_tm_fail_safe_protocols_tm_message_authentication_codes, axiom,
    tm_fail_safe_protocols != tm_message_authentication_codes).

fof(bg_dist_tm_fail_safe_protocols_tm_mobile_platform_security, axiom,
    tm_fail_safe_protocols != tm_mobile_platform_security).

fof(bg_dist_tm_fail_safe_protocols_tm_monotonic_counter_pseudonymisation, axiom,
    tm_fail_safe_protocols != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_fail_safe_protocols_tm_multi_factor_authentication, axiom,
    tm_fail_safe_protocols != tm_multi_factor_authentication).

fof(bg_dist_tm_fail_safe_protocols_tm_network_proxy_routing, axiom,
    tm_fail_safe_protocols != tm_network_proxy_routing).

fof(bg_dist_tm_fail_safe_protocols_tm_network_security_protocols, axiom,
    tm_fail_safe_protocols != tm_network_security_protocols).

fof(bg_dist_tm_fail_safe_protocols_tm_operating_system_security, axiom,
    tm_fail_safe_protocols != tm_operating_system_security).

fof(bg_dist_tm_fail_safe_protocols_tm_organisational_measure, axiom,
    tm_fail_safe_protocols != tm_organisational_measure).

fof(bg_dist_tm_fail_safe_protocols_tm_password_authentication, axiom,
    tm_fail_safe_protocols != tm_password_authentication).

fof(bg_dist_tm_fail_safe_protocols_tm_penetration_testing_methods, axiom,
    tm_fail_safe_protocols != tm_penetration_testing_methods).

fof(bg_dist_tm_fail_safe_protocols_tm_physical_measure, axiom,
    tm_fail_safe_protocols != tm_physical_measure).

fof(bg_dist_tm_fail_safe_protocols_tm_post_quantum_cryptography, axiom,
    tm_fail_safe_protocols != tm_post_quantum_cryptography).

fof(bg_dist_tm_fail_safe_protocols_tm_privacy_preserving_protocol, axiom,
    tm_fail_safe_protocols != tm_privacy_preserving_protocol).

fof(bg_dist_tm_fail_safe_protocols_tm_private_information_retrieval, axiom,
    tm_fail_safe_protocols != tm_private_information_retrieval).

fof(bg_dist_tm_fail_safe_protocols_tm_pseudonymisation, axiom,
    tm_fail_safe_protocols != tm_pseudonymisation).

fof(bg_dist_tm_fail_safe_protocols_tm_quantum_cryptography, axiom,
    tm_fail_safe_protocols != tm_quantum_cryptography).

fof(bg_dist_tm_fail_safe_protocols_tm_r_n_g_pseudonymisation, axiom,
    tm_fail_safe_protocols != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_fail_safe_protocols_tm_secret_sharing_schemes, axiom,
    tm_fail_safe_protocols != tm_secret_sharing_schemes).

fof(bg_dist_tm_fail_safe_protocols_tm_secure_multi_party_computation, axiom,
    tm_fail_safe_protocols != tm_secure_multi_party_computation).

fof(bg_dist_tm_fail_safe_protocols_tm_security_method, axiom,
    tm_fail_safe_protocols != tm_security_method).

fof(bg_dist_tm_fail_safe_protocols_tm_single_sign_on, axiom,
    tm_fail_safe_protocols != tm_single_sign_on).

fof(bg_dist_tm_fail_safe_protocols_tm_symmetric_cryptography, axiom,
    tm_fail_safe_protocols != tm_symmetric_cryptography).

fof(bg_dist_tm_fail_safe_protocols_tm_symmetric_encryption, axiom,
    tm_fail_safe_protocols != tm_symmetric_encryption).

fof(bg_dist_tm_fail_safe_protocols_tm_technical_measure, axiom,
    tm_fail_safe_protocols != tm_technical_measure).

fof(bg_dist_tm_fail_safe_protocols_tm_technical_organisational_measure, axiom,
    tm_fail_safe_protocols != tm_technical_organisational_measure).

fof(bg_dist_tm_fail_safe_protocols_tm_trusted_computing, axiom,
    tm_fail_safe_protocols != tm_trusted_computing).

fof(bg_dist_tm_fail_safe_protocols_tm_trusted_execution_environment, axiom,
    tm_fail_safe_protocols != tm_trusted_execution_environment).

fof(bg_dist_tm_fail_safe_protocols_tm_usage_control, axiom,
    tm_fail_safe_protocols != tm_usage_control).

fof(bg_dist_tm_fail_safe_protocols_tm_use_synthetic_data, axiom,
    tm_fail_safe_protocols != tm_use_synthetic_data).

fof(bg_dist_tm_fail_safe_protocols_tm_virtualisation_security, axiom,
    tm_fail_safe_protocols != tm_virtualisation_security).

fof(bg_dist_tm_fail_safe_protocols_tm_vulnerability_testing_methods, axiom,
    tm_fail_safe_protocols != tm_vulnerability_testing_methods).

fof(bg_dist_tm_fail_safe_protocols_tm_web_browser_security, axiom,
    tm_fail_safe_protocols != tm_web_browser_security).

fof(bg_dist_tm_fail_safe_protocols_tm_web_security_protocols, axiom,
    tm_fail_safe_protocols != tm_web_security_protocols).

fof(bg_dist_tm_fail_safe_protocols_tm_wireless_security_protocols, axiom,
    tm_fail_safe_protocols != tm_wireless_security_protocols).

fof(bg_dist_tm_fail_safe_protocols_tm_zero_knowledge_authentication, axiom,
    tm_fail_safe_protocols != tm_zero_knowledge_authentication).

fof(bg_dist_tm_file_system_security_tm_fully_randomised_pseudonymisation, axiom,
    tm_file_system_security != tm_fully_randomised_pseudonymisation).

fof(bg_dist_tm_file_system_security_tm_hardware_security_protocols, axiom,
    tm_file_system_security != tm_hardware_security_protocols).

fof(bg_dist_tm_file_system_security_tm_hash_functions, axiom,
    tm_file_system_security != tm_hash_functions).

fof(bg_dist_tm_file_system_security_tm_hash_message_authentication_code, axiom,
    tm_file_system_security != tm_hash_message_authentication_code).

fof(bg_dist_tm_file_system_security_tm_homomorphic_encryption, axiom,
    tm_file_system_security != tm_homomorphic_encryption).

fof(bg_dist_tm_file_system_security_tm_information_flow_control, axiom,
    tm_file_system_security != tm_information_flow_control).

fof(bg_dist_tm_file_system_security_tm_intrusion_detection_system, axiom,
    tm_file_system_security != tm_intrusion_detection_system).

fof(bg_dist_tm_file_system_security_tm_legal_measure, axiom,
    tm_file_system_security != tm_legal_measure).

fof(bg_dist_tm_file_system_security_tm_message_authentication_codes, axiom,
    tm_file_system_security != tm_message_authentication_codes).

fof(bg_dist_tm_file_system_security_tm_mobile_platform_security, axiom,
    tm_file_system_security != tm_mobile_platform_security).

fof(bg_dist_tm_file_system_security_tm_monotonic_counter_pseudonymisation, axiom,
    tm_file_system_security != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_file_system_security_tm_multi_factor_authentication, axiom,
    tm_file_system_security != tm_multi_factor_authentication).

fof(bg_dist_tm_file_system_security_tm_network_proxy_routing, axiom,
    tm_file_system_security != tm_network_proxy_routing).

fof(bg_dist_tm_file_system_security_tm_network_security_protocols, axiom,
    tm_file_system_security != tm_network_security_protocols).

fof(bg_dist_tm_file_system_security_tm_operating_system_security, axiom,
    tm_file_system_security != tm_operating_system_security).

fof(bg_dist_tm_file_system_security_tm_organisational_measure, axiom,
    tm_file_system_security != tm_organisational_measure).

fof(bg_dist_tm_file_system_security_tm_password_authentication, axiom,
    tm_file_system_security != tm_password_authentication).

fof(bg_dist_tm_file_system_security_tm_penetration_testing_methods, axiom,
    tm_file_system_security != tm_penetration_testing_methods).

fof(bg_dist_tm_file_system_security_tm_physical_measure, axiom,
    tm_file_system_security != tm_physical_measure).

fof(bg_dist_tm_file_system_security_tm_post_quantum_cryptography, axiom,
    tm_file_system_security != tm_post_quantum_cryptography).

fof(bg_dist_tm_file_system_security_tm_privacy_preserving_protocol, axiom,
    tm_file_system_security != tm_privacy_preserving_protocol).

fof(bg_dist_tm_file_system_security_tm_private_information_retrieval, axiom,
    tm_file_system_security != tm_private_information_retrieval).

fof(bg_dist_tm_file_system_security_tm_pseudonymisation, axiom,
    tm_file_system_security != tm_pseudonymisation).

fof(bg_dist_tm_file_system_security_tm_quantum_cryptography, axiom,
    tm_file_system_security != tm_quantum_cryptography).

fof(bg_dist_tm_file_system_security_tm_r_n_g_pseudonymisation, axiom,
    tm_file_system_security != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_file_system_security_tm_secret_sharing_schemes, axiom,
    tm_file_system_security != tm_secret_sharing_schemes).

fof(bg_dist_tm_file_system_security_tm_secure_multi_party_computation, axiom,
    tm_file_system_security != tm_secure_multi_party_computation).

fof(bg_dist_tm_file_system_security_tm_security_method, axiom,
    tm_file_system_security != tm_security_method).

fof(bg_dist_tm_file_system_security_tm_single_sign_on, axiom,
    tm_file_system_security != tm_single_sign_on).

fof(bg_dist_tm_file_system_security_tm_symmetric_cryptography, axiom,
    tm_file_system_security != tm_symmetric_cryptography).

fof(bg_dist_tm_file_system_security_tm_symmetric_encryption, axiom,
    tm_file_system_security != tm_symmetric_encryption).

fof(bg_dist_tm_file_system_security_tm_technical_measure, axiom,
    tm_file_system_security != tm_technical_measure).

fof(bg_dist_tm_file_system_security_tm_technical_organisational_measure, axiom,
    tm_file_system_security != tm_technical_organisational_measure).

fof(bg_dist_tm_file_system_security_tm_trusted_computing, axiom,
    tm_file_system_security != tm_trusted_computing).

fof(bg_dist_tm_file_system_security_tm_trusted_execution_environment, axiom,
    tm_file_system_security != tm_trusted_execution_environment).

fof(bg_dist_tm_file_system_security_tm_usage_control, axiom,
    tm_file_system_security != tm_usage_control).

fof(bg_dist_tm_file_system_security_tm_use_synthetic_data, axiom,
    tm_file_system_security != tm_use_synthetic_data).

fof(bg_dist_tm_file_system_security_tm_virtualisation_security, axiom,
    tm_file_system_security != tm_virtualisation_security).

fof(bg_dist_tm_file_system_security_tm_vulnerability_testing_methods, axiom,
    tm_file_system_security != tm_vulnerability_testing_methods).

fof(bg_dist_tm_file_system_security_tm_web_browser_security, axiom,
    tm_file_system_security != tm_web_browser_security).

fof(bg_dist_tm_file_system_security_tm_web_security_protocols, axiom,
    tm_file_system_security != tm_web_security_protocols).

fof(bg_dist_tm_file_system_security_tm_wireless_security_protocols, axiom,
    tm_file_system_security != tm_wireless_security_protocols).

fof(bg_dist_tm_file_system_security_tm_zero_knowledge_authentication, axiom,
    tm_file_system_security != tm_zero_knowledge_authentication).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_hardware_security_protocols, axiom,
    tm_fully_randomised_pseudonymisation != tm_hardware_security_protocols).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_hash_functions, axiom,
    tm_fully_randomised_pseudonymisation != tm_hash_functions).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_hash_message_authentication_code, axiom,
    tm_fully_randomised_pseudonymisation != tm_hash_message_authentication_code).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_homomorphic_encryption, axiom,
    tm_fully_randomised_pseudonymisation != tm_homomorphic_encryption).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_information_flow_control, axiom,
    tm_fully_randomised_pseudonymisation != tm_information_flow_control).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_intrusion_detection_system, axiom,
    tm_fully_randomised_pseudonymisation != tm_intrusion_detection_system).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_legal_measure, axiom,
    tm_fully_randomised_pseudonymisation != tm_legal_measure).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_message_authentication_codes, axiom,
    tm_fully_randomised_pseudonymisation != tm_message_authentication_codes).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_mobile_platform_security, axiom,
    tm_fully_randomised_pseudonymisation != tm_mobile_platform_security).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_monotonic_counter_pseudonymisation, axiom,
    tm_fully_randomised_pseudonymisation != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_multi_factor_authentication, axiom,
    tm_fully_randomised_pseudonymisation != tm_multi_factor_authentication).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_network_proxy_routing, axiom,
    tm_fully_randomised_pseudonymisation != tm_network_proxy_routing).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_network_security_protocols, axiom,
    tm_fully_randomised_pseudonymisation != tm_network_security_protocols).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_operating_system_security, axiom,
    tm_fully_randomised_pseudonymisation != tm_operating_system_security).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_organisational_measure, axiom,
    tm_fully_randomised_pseudonymisation != tm_organisational_measure).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_password_authentication, axiom,
    tm_fully_randomised_pseudonymisation != tm_password_authentication).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_penetration_testing_methods, axiom,
    tm_fully_randomised_pseudonymisation != tm_penetration_testing_methods).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_physical_measure, axiom,
    tm_fully_randomised_pseudonymisation != tm_physical_measure).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_post_quantum_cryptography, axiom,
    tm_fully_randomised_pseudonymisation != tm_post_quantum_cryptography).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_privacy_preserving_protocol, axiom,
    tm_fully_randomised_pseudonymisation != tm_privacy_preserving_protocol).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_private_information_retrieval, axiom,
    tm_fully_randomised_pseudonymisation != tm_private_information_retrieval).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_pseudonymisation, axiom,
    tm_fully_randomised_pseudonymisation != tm_pseudonymisation).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_quantum_cryptography, axiom,
    tm_fully_randomised_pseudonymisation != tm_quantum_cryptography).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_r_n_g_pseudonymisation, axiom,
    tm_fully_randomised_pseudonymisation != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_secret_sharing_schemes, axiom,
    tm_fully_randomised_pseudonymisation != tm_secret_sharing_schemes).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_secure_multi_party_computation, axiom,
    tm_fully_randomised_pseudonymisation != tm_secure_multi_party_computation).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_security_method, axiom,
    tm_fully_randomised_pseudonymisation != tm_security_method).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_single_sign_on, axiom,
    tm_fully_randomised_pseudonymisation != tm_single_sign_on).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_symmetric_cryptography, axiom,
    tm_fully_randomised_pseudonymisation != tm_symmetric_cryptography).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_symmetric_encryption, axiom,
    tm_fully_randomised_pseudonymisation != tm_symmetric_encryption).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_technical_measure, axiom,
    tm_fully_randomised_pseudonymisation != tm_technical_measure).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_technical_organisational_measure, axiom,
    tm_fully_randomised_pseudonymisation != tm_technical_organisational_measure).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_trusted_computing, axiom,
    tm_fully_randomised_pseudonymisation != tm_trusted_computing).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_trusted_execution_environment, axiom,
    tm_fully_randomised_pseudonymisation != tm_trusted_execution_environment).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_usage_control, axiom,
    tm_fully_randomised_pseudonymisation != tm_usage_control).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_use_synthetic_data, axiom,
    tm_fully_randomised_pseudonymisation != tm_use_synthetic_data).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_virtualisation_security, axiom,
    tm_fully_randomised_pseudonymisation != tm_virtualisation_security).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_vulnerability_testing_methods, axiom,
    tm_fully_randomised_pseudonymisation != tm_vulnerability_testing_methods).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_web_browser_security, axiom,
    tm_fully_randomised_pseudonymisation != tm_web_browser_security).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_web_security_protocols, axiom,
    tm_fully_randomised_pseudonymisation != tm_web_security_protocols).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_wireless_security_protocols, axiom,
    tm_fully_randomised_pseudonymisation != tm_wireless_security_protocols).

fof(bg_dist_tm_fully_randomised_pseudonymisation_tm_zero_knowledge_authentication, axiom,
    tm_fully_randomised_pseudonymisation != tm_zero_knowledge_authentication).

fof(bg_dist_tm_hardware_security_protocols_tm_hash_functions, axiom,
    tm_hardware_security_protocols != tm_hash_functions).

fof(bg_dist_tm_hardware_security_protocols_tm_hash_message_authentication_code, axiom,
    tm_hardware_security_protocols != tm_hash_message_authentication_code).

fof(bg_dist_tm_hardware_security_protocols_tm_homomorphic_encryption, axiom,
    tm_hardware_security_protocols != tm_homomorphic_encryption).

fof(bg_dist_tm_hardware_security_protocols_tm_information_flow_control, axiom,
    tm_hardware_security_protocols != tm_information_flow_control).

fof(bg_dist_tm_hardware_security_protocols_tm_intrusion_detection_system, axiom,
    tm_hardware_security_protocols != tm_intrusion_detection_system).

fof(bg_dist_tm_hardware_security_protocols_tm_legal_measure, axiom,
    tm_hardware_security_protocols != tm_legal_measure).

fof(bg_dist_tm_hardware_security_protocols_tm_message_authentication_codes, axiom,
    tm_hardware_security_protocols != tm_message_authentication_codes).

fof(bg_dist_tm_hardware_security_protocols_tm_mobile_platform_security, axiom,
    tm_hardware_security_protocols != tm_mobile_platform_security).

fof(bg_dist_tm_hardware_security_protocols_tm_monotonic_counter_pseudonymisation, axiom,
    tm_hardware_security_protocols != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_hardware_security_protocols_tm_multi_factor_authentication, axiom,
    tm_hardware_security_protocols != tm_multi_factor_authentication).

fof(bg_dist_tm_hardware_security_protocols_tm_network_proxy_routing, axiom,
    tm_hardware_security_protocols != tm_network_proxy_routing).

fof(bg_dist_tm_hardware_security_protocols_tm_network_security_protocols, axiom,
    tm_hardware_security_protocols != tm_network_security_protocols).

fof(bg_dist_tm_hardware_security_protocols_tm_operating_system_security, axiom,
    tm_hardware_security_protocols != tm_operating_system_security).

fof(bg_dist_tm_hardware_security_protocols_tm_organisational_measure, axiom,
    tm_hardware_security_protocols != tm_organisational_measure).

fof(bg_dist_tm_hardware_security_protocols_tm_password_authentication, axiom,
    tm_hardware_security_protocols != tm_password_authentication).

fof(bg_dist_tm_hardware_security_protocols_tm_penetration_testing_methods, axiom,
    tm_hardware_security_protocols != tm_penetration_testing_methods).

fof(bg_dist_tm_hardware_security_protocols_tm_physical_measure, axiom,
    tm_hardware_security_protocols != tm_physical_measure).

fof(bg_dist_tm_hardware_security_protocols_tm_post_quantum_cryptography, axiom,
    tm_hardware_security_protocols != tm_post_quantum_cryptography).

fof(bg_dist_tm_hardware_security_protocols_tm_privacy_preserving_protocol, axiom,
    tm_hardware_security_protocols != tm_privacy_preserving_protocol).

fof(bg_dist_tm_hardware_security_protocols_tm_private_information_retrieval, axiom,
    tm_hardware_security_protocols != tm_private_information_retrieval).

fof(bg_dist_tm_hardware_security_protocols_tm_pseudonymisation, axiom,
    tm_hardware_security_protocols != tm_pseudonymisation).

fof(bg_dist_tm_hardware_security_protocols_tm_quantum_cryptography, axiom,
    tm_hardware_security_protocols != tm_quantum_cryptography).

fof(bg_dist_tm_hardware_security_protocols_tm_r_n_g_pseudonymisation, axiom,
    tm_hardware_security_protocols != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_hardware_security_protocols_tm_secret_sharing_schemes, axiom,
    tm_hardware_security_protocols != tm_secret_sharing_schemes).

fof(bg_dist_tm_hardware_security_protocols_tm_secure_multi_party_computation, axiom,
    tm_hardware_security_protocols != tm_secure_multi_party_computation).

fof(bg_dist_tm_hardware_security_protocols_tm_security_method, axiom,
    tm_hardware_security_protocols != tm_security_method).

fof(bg_dist_tm_hardware_security_protocols_tm_single_sign_on, axiom,
    tm_hardware_security_protocols != tm_single_sign_on).

fof(bg_dist_tm_hardware_security_protocols_tm_symmetric_cryptography, axiom,
    tm_hardware_security_protocols != tm_symmetric_cryptography).

fof(bg_dist_tm_hardware_security_protocols_tm_symmetric_encryption, axiom,
    tm_hardware_security_protocols != tm_symmetric_encryption).

fof(bg_dist_tm_hardware_security_protocols_tm_technical_measure, axiom,
    tm_hardware_security_protocols != tm_technical_measure).

fof(bg_dist_tm_hardware_security_protocols_tm_technical_organisational_measure, axiom,
    tm_hardware_security_protocols != tm_technical_organisational_measure).

fof(bg_dist_tm_hardware_security_protocols_tm_trusted_computing, axiom,
    tm_hardware_security_protocols != tm_trusted_computing).

fof(bg_dist_tm_hardware_security_protocols_tm_trusted_execution_environment, axiom,
    tm_hardware_security_protocols != tm_trusted_execution_environment).

fof(bg_dist_tm_hardware_security_protocols_tm_usage_control, axiom,
    tm_hardware_security_protocols != tm_usage_control).

fof(bg_dist_tm_hardware_security_protocols_tm_use_synthetic_data, axiom,
    tm_hardware_security_protocols != tm_use_synthetic_data).

fof(bg_dist_tm_hardware_security_protocols_tm_virtualisation_security, axiom,
    tm_hardware_security_protocols != tm_virtualisation_security).

fof(bg_dist_tm_hardware_security_protocols_tm_vulnerability_testing_methods, axiom,
    tm_hardware_security_protocols != tm_vulnerability_testing_methods).

fof(bg_dist_tm_hardware_security_protocols_tm_web_browser_security, axiom,
    tm_hardware_security_protocols != tm_web_browser_security).

fof(bg_dist_tm_hardware_security_protocols_tm_web_security_protocols, axiom,
    tm_hardware_security_protocols != tm_web_security_protocols).

fof(bg_dist_tm_hardware_security_protocols_tm_wireless_security_protocols, axiom,
    tm_hardware_security_protocols != tm_wireless_security_protocols).

fof(bg_dist_tm_hardware_security_protocols_tm_zero_knowledge_authentication, axiom,
    tm_hardware_security_protocols != tm_zero_knowledge_authentication).

fof(bg_dist_tm_hash_functions_tm_hash_message_authentication_code, axiom,
    tm_hash_functions != tm_hash_message_authentication_code).

fof(bg_dist_tm_hash_functions_tm_homomorphic_encryption, axiom,
    tm_hash_functions != tm_homomorphic_encryption).

fof(bg_dist_tm_hash_functions_tm_information_flow_control, axiom,
    tm_hash_functions != tm_information_flow_control).

fof(bg_dist_tm_hash_functions_tm_intrusion_detection_system, axiom,
    tm_hash_functions != tm_intrusion_detection_system).

fof(bg_dist_tm_hash_functions_tm_legal_measure, axiom,
    tm_hash_functions != tm_legal_measure).

fof(bg_dist_tm_hash_functions_tm_message_authentication_codes, axiom,
    tm_hash_functions != tm_message_authentication_codes).

fof(bg_dist_tm_hash_functions_tm_mobile_platform_security, axiom,
    tm_hash_functions != tm_mobile_platform_security).

fof(bg_dist_tm_hash_functions_tm_monotonic_counter_pseudonymisation, axiom,
    tm_hash_functions != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_hash_functions_tm_multi_factor_authentication, axiom,
    tm_hash_functions != tm_multi_factor_authentication).

fof(bg_dist_tm_hash_functions_tm_network_proxy_routing, axiom,
    tm_hash_functions != tm_network_proxy_routing).

fof(bg_dist_tm_hash_functions_tm_network_security_protocols, axiom,
    tm_hash_functions != tm_network_security_protocols).

fof(bg_dist_tm_hash_functions_tm_operating_system_security, axiom,
    tm_hash_functions != tm_operating_system_security).

fof(bg_dist_tm_hash_functions_tm_organisational_measure, axiom,
    tm_hash_functions != tm_organisational_measure).

fof(bg_dist_tm_hash_functions_tm_password_authentication, axiom,
    tm_hash_functions != tm_password_authentication).

fof(bg_dist_tm_hash_functions_tm_penetration_testing_methods, axiom,
    tm_hash_functions != tm_penetration_testing_methods).

fof(bg_dist_tm_hash_functions_tm_physical_measure, axiom,
    tm_hash_functions != tm_physical_measure).

fof(bg_dist_tm_hash_functions_tm_post_quantum_cryptography, axiom,
    tm_hash_functions != tm_post_quantum_cryptography).

fof(bg_dist_tm_hash_functions_tm_privacy_preserving_protocol, axiom,
    tm_hash_functions != tm_privacy_preserving_protocol).

fof(bg_dist_tm_hash_functions_tm_private_information_retrieval, axiom,
    tm_hash_functions != tm_private_information_retrieval).

fof(bg_dist_tm_hash_functions_tm_pseudonymisation, axiom,
    tm_hash_functions != tm_pseudonymisation).

fof(bg_dist_tm_hash_functions_tm_quantum_cryptography, axiom,
    tm_hash_functions != tm_quantum_cryptography).

fof(bg_dist_tm_hash_functions_tm_r_n_g_pseudonymisation, axiom,
    tm_hash_functions != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_hash_functions_tm_secret_sharing_schemes, axiom,
    tm_hash_functions != tm_secret_sharing_schemes).

fof(bg_dist_tm_hash_functions_tm_secure_multi_party_computation, axiom,
    tm_hash_functions != tm_secure_multi_party_computation).

fof(bg_dist_tm_hash_functions_tm_security_method, axiom,
    tm_hash_functions != tm_security_method).

fof(bg_dist_tm_hash_functions_tm_single_sign_on, axiom,
    tm_hash_functions != tm_single_sign_on).

fof(bg_dist_tm_hash_functions_tm_symmetric_cryptography, axiom,
    tm_hash_functions != tm_symmetric_cryptography).

fof(bg_dist_tm_hash_functions_tm_symmetric_encryption, axiom,
    tm_hash_functions != tm_symmetric_encryption).

fof(bg_dist_tm_hash_functions_tm_technical_measure, axiom,
    tm_hash_functions != tm_technical_measure).

fof(bg_dist_tm_hash_functions_tm_technical_organisational_measure, axiom,
    tm_hash_functions != tm_technical_organisational_measure).

fof(bg_dist_tm_hash_functions_tm_trusted_computing, axiom,
    tm_hash_functions != tm_trusted_computing).

fof(bg_dist_tm_hash_functions_tm_trusted_execution_environment, axiom,
    tm_hash_functions != tm_trusted_execution_environment).

fof(bg_dist_tm_hash_functions_tm_usage_control, axiom,
    tm_hash_functions != tm_usage_control).

fof(bg_dist_tm_hash_functions_tm_use_synthetic_data, axiom,
    tm_hash_functions != tm_use_synthetic_data).

fof(bg_dist_tm_hash_functions_tm_virtualisation_security, axiom,
    tm_hash_functions != tm_virtualisation_security).

fof(bg_dist_tm_hash_functions_tm_vulnerability_testing_methods, axiom,
    tm_hash_functions != tm_vulnerability_testing_methods).

fof(bg_dist_tm_hash_functions_tm_web_browser_security, axiom,
    tm_hash_functions != tm_web_browser_security).

fof(bg_dist_tm_hash_functions_tm_web_security_protocols, axiom,
    tm_hash_functions != tm_web_security_protocols).

fof(bg_dist_tm_hash_functions_tm_wireless_security_protocols, axiom,
    tm_hash_functions != tm_wireless_security_protocols).

fof(bg_dist_tm_hash_functions_tm_zero_knowledge_authentication, axiom,
    tm_hash_functions != tm_zero_knowledge_authentication).

fof(bg_dist_tm_hash_message_authentication_code_tm_homomorphic_encryption, axiom,
    tm_hash_message_authentication_code != tm_homomorphic_encryption).

fof(bg_dist_tm_hash_message_authentication_code_tm_information_flow_control, axiom,
    tm_hash_message_authentication_code != tm_information_flow_control).

fof(bg_dist_tm_hash_message_authentication_code_tm_intrusion_detection_system, axiom,
    tm_hash_message_authentication_code != tm_intrusion_detection_system).

fof(bg_dist_tm_hash_message_authentication_code_tm_legal_measure, axiom,
    tm_hash_message_authentication_code != tm_legal_measure).

fof(bg_dist_tm_hash_message_authentication_code_tm_message_authentication_codes, axiom,
    tm_hash_message_authentication_code != tm_message_authentication_codes).

fof(bg_dist_tm_hash_message_authentication_code_tm_mobile_platform_security, axiom,
    tm_hash_message_authentication_code != tm_mobile_platform_security).

fof(bg_dist_tm_hash_message_authentication_code_tm_monotonic_counter_pseudonymisation, axiom,
    tm_hash_message_authentication_code != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_hash_message_authentication_code_tm_multi_factor_authentication, axiom,
    tm_hash_message_authentication_code != tm_multi_factor_authentication).

fof(bg_dist_tm_hash_message_authentication_code_tm_network_proxy_routing, axiom,
    tm_hash_message_authentication_code != tm_network_proxy_routing).

fof(bg_dist_tm_hash_message_authentication_code_tm_network_security_protocols, axiom,
    tm_hash_message_authentication_code != tm_network_security_protocols).

fof(bg_dist_tm_hash_message_authentication_code_tm_operating_system_security, axiom,
    tm_hash_message_authentication_code != tm_operating_system_security).

fof(bg_dist_tm_hash_message_authentication_code_tm_organisational_measure, axiom,
    tm_hash_message_authentication_code != tm_organisational_measure).

fof(bg_dist_tm_hash_message_authentication_code_tm_password_authentication, axiom,
    tm_hash_message_authentication_code != tm_password_authentication).

fof(bg_dist_tm_hash_message_authentication_code_tm_penetration_testing_methods, axiom,
    tm_hash_message_authentication_code != tm_penetration_testing_methods).

fof(bg_dist_tm_hash_message_authentication_code_tm_physical_measure, axiom,
    tm_hash_message_authentication_code != tm_physical_measure).

fof(bg_dist_tm_hash_message_authentication_code_tm_post_quantum_cryptography, axiom,
    tm_hash_message_authentication_code != tm_post_quantum_cryptography).

fof(bg_dist_tm_hash_message_authentication_code_tm_privacy_preserving_protocol, axiom,
    tm_hash_message_authentication_code != tm_privacy_preserving_protocol).

fof(bg_dist_tm_hash_message_authentication_code_tm_private_information_retrieval, axiom,
    tm_hash_message_authentication_code != tm_private_information_retrieval).

fof(bg_dist_tm_hash_message_authentication_code_tm_pseudonymisation, axiom,
    tm_hash_message_authentication_code != tm_pseudonymisation).

fof(bg_dist_tm_hash_message_authentication_code_tm_quantum_cryptography, axiom,
    tm_hash_message_authentication_code != tm_quantum_cryptography).

fof(bg_dist_tm_hash_message_authentication_code_tm_r_n_g_pseudonymisation, axiom,
    tm_hash_message_authentication_code != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_hash_message_authentication_code_tm_secret_sharing_schemes, axiom,
    tm_hash_message_authentication_code != tm_secret_sharing_schemes).

fof(bg_dist_tm_hash_message_authentication_code_tm_secure_multi_party_computation, axiom,
    tm_hash_message_authentication_code != tm_secure_multi_party_computation).

fof(bg_dist_tm_hash_message_authentication_code_tm_security_method, axiom,
    tm_hash_message_authentication_code != tm_security_method).

fof(bg_dist_tm_hash_message_authentication_code_tm_single_sign_on, axiom,
    tm_hash_message_authentication_code != tm_single_sign_on).

fof(bg_dist_tm_hash_message_authentication_code_tm_symmetric_cryptography, axiom,
    tm_hash_message_authentication_code != tm_symmetric_cryptography).

fof(bg_dist_tm_hash_message_authentication_code_tm_symmetric_encryption, axiom,
    tm_hash_message_authentication_code != tm_symmetric_encryption).

fof(bg_dist_tm_hash_message_authentication_code_tm_technical_measure, axiom,
    tm_hash_message_authentication_code != tm_technical_measure).

fof(bg_dist_tm_hash_message_authentication_code_tm_technical_organisational_measure, axiom,
    tm_hash_message_authentication_code != tm_technical_organisational_measure).

fof(bg_dist_tm_hash_message_authentication_code_tm_trusted_computing, axiom,
    tm_hash_message_authentication_code != tm_trusted_computing).

fof(bg_dist_tm_hash_message_authentication_code_tm_trusted_execution_environment, axiom,
    tm_hash_message_authentication_code != tm_trusted_execution_environment).

fof(bg_dist_tm_hash_message_authentication_code_tm_usage_control, axiom,
    tm_hash_message_authentication_code != tm_usage_control).

fof(bg_dist_tm_hash_message_authentication_code_tm_use_synthetic_data, axiom,
    tm_hash_message_authentication_code != tm_use_synthetic_data).

fof(bg_dist_tm_hash_message_authentication_code_tm_virtualisation_security, axiom,
    tm_hash_message_authentication_code != tm_virtualisation_security).

fof(bg_dist_tm_hash_message_authentication_code_tm_vulnerability_testing_methods, axiom,
    tm_hash_message_authentication_code != tm_vulnerability_testing_methods).

fof(bg_dist_tm_hash_message_authentication_code_tm_web_browser_security, axiom,
    tm_hash_message_authentication_code != tm_web_browser_security).

fof(bg_dist_tm_hash_message_authentication_code_tm_web_security_protocols, axiom,
    tm_hash_message_authentication_code != tm_web_security_protocols).

fof(bg_dist_tm_hash_message_authentication_code_tm_wireless_security_protocols, axiom,
    tm_hash_message_authentication_code != tm_wireless_security_protocols).

fof(bg_dist_tm_hash_message_authentication_code_tm_zero_knowledge_authentication, axiom,
    tm_hash_message_authentication_code != tm_zero_knowledge_authentication).

fof(bg_dist_tm_homomorphic_encryption_tm_information_flow_control, axiom,
    tm_homomorphic_encryption != tm_information_flow_control).

fof(bg_dist_tm_homomorphic_encryption_tm_intrusion_detection_system, axiom,
    tm_homomorphic_encryption != tm_intrusion_detection_system).

fof(bg_dist_tm_homomorphic_encryption_tm_legal_measure, axiom,
    tm_homomorphic_encryption != tm_legal_measure).

fof(bg_dist_tm_homomorphic_encryption_tm_message_authentication_codes, axiom,
    tm_homomorphic_encryption != tm_message_authentication_codes).

fof(bg_dist_tm_homomorphic_encryption_tm_mobile_platform_security, axiom,
    tm_homomorphic_encryption != tm_mobile_platform_security).

fof(bg_dist_tm_homomorphic_encryption_tm_monotonic_counter_pseudonymisation, axiom,
    tm_homomorphic_encryption != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_homomorphic_encryption_tm_multi_factor_authentication, axiom,
    tm_homomorphic_encryption != tm_multi_factor_authentication).

fof(bg_dist_tm_homomorphic_encryption_tm_network_proxy_routing, axiom,
    tm_homomorphic_encryption != tm_network_proxy_routing).

fof(bg_dist_tm_homomorphic_encryption_tm_network_security_protocols, axiom,
    tm_homomorphic_encryption != tm_network_security_protocols).

fof(bg_dist_tm_homomorphic_encryption_tm_operating_system_security, axiom,
    tm_homomorphic_encryption != tm_operating_system_security).

fof(bg_dist_tm_homomorphic_encryption_tm_organisational_measure, axiom,
    tm_homomorphic_encryption != tm_organisational_measure).

fof(bg_dist_tm_homomorphic_encryption_tm_password_authentication, axiom,
    tm_homomorphic_encryption != tm_password_authentication).

fof(bg_dist_tm_homomorphic_encryption_tm_penetration_testing_methods, axiom,
    tm_homomorphic_encryption != tm_penetration_testing_methods).

fof(bg_dist_tm_homomorphic_encryption_tm_physical_measure, axiom,
    tm_homomorphic_encryption != tm_physical_measure).

fof(bg_dist_tm_homomorphic_encryption_tm_post_quantum_cryptography, axiom,
    tm_homomorphic_encryption != tm_post_quantum_cryptography).

fof(bg_dist_tm_homomorphic_encryption_tm_privacy_preserving_protocol, axiom,
    tm_homomorphic_encryption != tm_privacy_preserving_protocol).

fof(bg_dist_tm_homomorphic_encryption_tm_private_information_retrieval, axiom,
    tm_homomorphic_encryption != tm_private_information_retrieval).

fof(bg_dist_tm_homomorphic_encryption_tm_pseudonymisation, axiom,
    tm_homomorphic_encryption != tm_pseudonymisation).

fof(bg_dist_tm_homomorphic_encryption_tm_quantum_cryptography, axiom,
    tm_homomorphic_encryption != tm_quantum_cryptography).

fof(bg_dist_tm_homomorphic_encryption_tm_r_n_g_pseudonymisation, axiom,
    tm_homomorphic_encryption != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_homomorphic_encryption_tm_secret_sharing_schemes, axiom,
    tm_homomorphic_encryption != tm_secret_sharing_schemes).

fof(bg_dist_tm_homomorphic_encryption_tm_secure_multi_party_computation, axiom,
    tm_homomorphic_encryption != tm_secure_multi_party_computation).

fof(bg_dist_tm_homomorphic_encryption_tm_security_method, axiom,
    tm_homomorphic_encryption != tm_security_method).

fof(bg_dist_tm_homomorphic_encryption_tm_single_sign_on, axiom,
    tm_homomorphic_encryption != tm_single_sign_on).

fof(bg_dist_tm_homomorphic_encryption_tm_symmetric_cryptography, axiom,
    tm_homomorphic_encryption != tm_symmetric_cryptography).

fof(bg_dist_tm_homomorphic_encryption_tm_symmetric_encryption, axiom,
    tm_homomorphic_encryption != tm_symmetric_encryption).

fof(bg_dist_tm_homomorphic_encryption_tm_technical_measure, axiom,
    tm_homomorphic_encryption != tm_technical_measure).

fof(bg_dist_tm_homomorphic_encryption_tm_technical_organisational_measure, axiom,
    tm_homomorphic_encryption != tm_technical_organisational_measure).

fof(bg_dist_tm_homomorphic_encryption_tm_trusted_computing, axiom,
    tm_homomorphic_encryption != tm_trusted_computing).

fof(bg_dist_tm_homomorphic_encryption_tm_trusted_execution_environment, axiom,
    tm_homomorphic_encryption != tm_trusted_execution_environment).

fof(bg_dist_tm_homomorphic_encryption_tm_usage_control, axiom,
    tm_homomorphic_encryption != tm_usage_control).

fof(bg_dist_tm_homomorphic_encryption_tm_use_synthetic_data, axiom,
    tm_homomorphic_encryption != tm_use_synthetic_data).

fof(bg_dist_tm_homomorphic_encryption_tm_virtualisation_security, axiom,
    tm_homomorphic_encryption != tm_virtualisation_security).

fof(bg_dist_tm_homomorphic_encryption_tm_vulnerability_testing_methods, axiom,
    tm_homomorphic_encryption != tm_vulnerability_testing_methods).

fof(bg_dist_tm_homomorphic_encryption_tm_web_browser_security, axiom,
    tm_homomorphic_encryption != tm_web_browser_security).

fof(bg_dist_tm_homomorphic_encryption_tm_web_security_protocols, axiom,
    tm_homomorphic_encryption != tm_web_security_protocols).

fof(bg_dist_tm_homomorphic_encryption_tm_wireless_security_protocols, axiom,
    tm_homomorphic_encryption != tm_wireless_security_protocols).

fof(bg_dist_tm_homomorphic_encryption_tm_zero_knowledge_authentication, axiom,
    tm_homomorphic_encryption != tm_zero_knowledge_authentication).

fof(bg_dist_tm_information_flow_control_tm_intrusion_detection_system, axiom,
    tm_information_flow_control != tm_intrusion_detection_system).

fof(bg_dist_tm_information_flow_control_tm_legal_measure, axiom,
    tm_information_flow_control != tm_legal_measure).

fof(bg_dist_tm_information_flow_control_tm_message_authentication_codes, axiom,
    tm_information_flow_control != tm_message_authentication_codes).

fof(bg_dist_tm_information_flow_control_tm_mobile_platform_security, axiom,
    tm_information_flow_control != tm_mobile_platform_security).

fof(bg_dist_tm_information_flow_control_tm_monotonic_counter_pseudonymisation, axiom,
    tm_information_flow_control != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_information_flow_control_tm_multi_factor_authentication, axiom,
    tm_information_flow_control != tm_multi_factor_authentication).

fof(bg_dist_tm_information_flow_control_tm_network_proxy_routing, axiom,
    tm_information_flow_control != tm_network_proxy_routing).

fof(bg_dist_tm_information_flow_control_tm_network_security_protocols, axiom,
    tm_information_flow_control != tm_network_security_protocols).

fof(bg_dist_tm_information_flow_control_tm_operating_system_security, axiom,
    tm_information_flow_control != tm_operating_system_security).

fof(bg_dist_tm_information_flow_control_tm_organisational_measure, axiom,
    tm_information_flow_control != tm_organisational_measure).

fof(bg_dist_tm_information_flow_control_tm_password_authentication, axiom,
    tm_information_flow_control != tm_password_authentication).

fof(bg_dist_tm_information_flow_control_tm_penetration_testing_methods, axiom,
    tm_information_flow_control != tm_penetration_testing_methods).

fof(bg_dist_tm_information_flow_control_tm_physical_measure, axiom,
    tm_information_flow_control != tm_physical_measure).

fof(bg_dist_tm_information_flow_control_tm_post_quantum_cryptography, axiom,
    tm_information_flow_control != tm_post_quantum_cryptography).

fof(bg_dist_tm_information_flow_control_tm_privacy_preserving_protocol, axiom,
    tm_information_flow_control != tm_privacy_preserving_protocol).

fof(bg_dist_tm_information_flow_control_tm_private_information_retrieval, axiom,
    tm_information_flow_control != tm_private_information_retrieval).

fof(bg_dist_tm_information_flow_control_tm_pseudonymisation, axiom,
    tm_information_flow_control != tm_pseudonymisation).

fof(bg_dist_tm_information_flow_control_tm_quantum_cryptography, axiom,
    tm_information_flow_control != tm_quantum_cryptography).

fof(bg_dist_tm_information_flow_control_tm_r_n_g_pseudonymisation, axiom,
    tm_information_flow_control != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_information_flow_control_tm_secret_sharing_schemes, axiom,
    tm_information_flow_control != tm_secret_sharing_schemes).

fof(bg_dist_tm_information_flow_control_tm_secure_multi_party_computation, axiom,
    tm_information_flow_control != tm_secure_multi_party_computation).

fof(bg_dist_tm_information_flow_control_tm_security_method, axiom,
    tm_information_flow_control != tm_security_method).

fof(bg_dist_tm_information_flow_control_tm_single_sign_on, axiom,
    tm_information_flow_control != tm_single_sign_on).

fof(bg_dist_tm_information_flow_control_tm_symmetric_cryptography, axiom,
    tm_information_flow_control != tm_symmetric_cryptography).

fof(bg_dist_tm_information_flow_control_tm_symmetric_encryption, axiom,
    tm_information_flow_control != tm_symmetric_encryption).

fof(bg_dist_tm_information_flow_control_tm_technical_measure, axiom,
    tm_information_flow_control != tm_technical_measure).

fof(bg_dist_tm_information_flow_control_tm_technical_organisational_measure, axiom,
    tm_information_flow_control != tm_technical_organisational_measure).

fof(bg_dist_tm_information_flow_control_tm_trusted_computing, axiom,
    tm_information_flow_control != tm_trusted_computing).

fof(bg_dist_tm_information_flow_control_tm_trusted_execution_environment, axiom,
    tm_information_flow_control != tm_trusted_execution_environment).

fof(bg_dist_tm_information_flow_control_tm_usage_control, axiom,
    tm_information_flow_control != tm_usage_control).

fof(bg_dist_tm_information_flow_control_tm_use_synthetic_data, axiom,
    tm_information_flow_control != tm_use_synthetic_data).

fof(bg_dist_tm_information_flow_control_tm_virtualisation_security, axiom,
    tm_information_flow_control != tm_virtualisation_security).

fof(bg_dist_tm_information_flow_control_tm_vulnerability_testing_methods, axiom,
    tm_information_flow_control != tm_vulnerability_testing_methods).

fof(bg_dist_tm_information_flow_control_tm_web_browser_security, axiom,
    tm_information_flow_control != tm_web_browser_security).

fof(bg_dist_tm_information_flow_control_tm_web_security_protocols, axiom,
    tm_information_flow_control != tm_web_security_protocols).

fof(bg_dist_tm_information_flow_control_tm_wireless_security_protocols, axiom,
    tm_information_flow_control != tm_wireless_security_protocols).

fof(bg_dist_tm_information_flow_control_tm_zero_knowledge_authentication, axiom,
    tm_information_flow_control != tm_zero_knowledge_authentication).

fof(bg_dist_tm_intrusion_detection_system_tm_legal_measure, axiom,
    tm_intrusion_detection_system != tm_legal_measure).

fof(bg_dist_tm_intrusion_detection_system_tm_message_authentication_codes, axiom,
    tm_intrusion_detection_system != tm_message_authentication_codes).

fof(bg_dist_tm_intrusion_detection_system_tm_mobile_platform_security, axiom,
    tm_intrusion_detection_system != tm_mobile_platform_security).

fof(bg_dist_tm_intrusion_detection_system_tm_monotonic_counter_pseudonymisation, axiom,
    tm_intrusion_detection_system != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_intrusion_detection_system_tm_multi_factor_authentication, axiom,
    tm_intrusion_detection_system != tm_multi_factor_authentication).

fof(bg_dist_tm_intrusion_detection_system_tm_network_proxy_routing, axiom,
    tm_intrusion_detection_system != tm_network_proxy_routing).

fof(bg_dist_tm_intrusion_detection_system_tm_network_security_protocols, axiom,
    tm_intrusion_detection_system != tm_network_security_protocols).

fof(bg_dist_tm_intrusion_detection_system_tm_operating_system_security, axiom,
    tm_intrusion_detection_system != tm_operating_system_security).

fof(bg_dist_tm_intrusion_detection_system_tm_organisational_measure, axiom,
    tm_intrusion_detection_system != tm_organisational_measure).

fof(bg_dist_tm_intrusion_detection_system_tm_password_authentication, axiom,
    tm_intrusion_detection_system != tm_password_authentication).

fof(bg_dist_tm_intrusion_detection_system_tm_penetration_testing_methods, axiom,
    tm_intrusion_detection_system != tm_penetration_testing_methods).

fof(bg_dist_tm_intrusion_detection_system_tm_physical_measure, axiom,
    tm_intrusion_detection_system != tm_physical_measure).

fof(bg_dist_tm_intrusion_detection_system_tm_post_quantum_cryptography, axiom,
    tm_intrusion_detection_system != tm_post_quantum_cryptography).

fof(bg_dist_tm_intrusion_detection_system_tm_privacy_preserving_protocol, axiom,
    tm_intrusion_detection_system != tm_privacy_preserving_protocol).

fof(bg_dist_tm_intrusion_detection_system_tm_private_information_retrieval, axiom,
    tm_intrusion_detection_system != tm_private_information_retrieval).

fof(bg_dist_tm_intrusion_detection_system_tm_pseudonymisation, axiom,
    tm_intrusion_detection_system != tm_pseudonymisation).

fof(bg_dist_tm_intrusion_detection_system_tm_quantum_cryptography, axiom,
    tm_intrusion_detection_system != tm_quantum_cryptography).

fof(bg_dist_tm_intrusion_detection_system_tm_r_n_g_pseudonymisation, axiom,
    tm_intrusion_detection_system != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_intrusion_detection_system_tm_secret_sharing_schemes, axiom,
    tm_intrusion_detection_system != tm_secret_sharing_schemes).

fof(bg_dist_tm_intrusion_detection_system_tm_secure_multi_party_computation, axiom,
    tm_intrusion_detection_system != tm_secure_multi_party_computation).

fof(bg_dist_tm_intrusion_detection_system_tm_security_method, axiom,
    tm_intrusion_detection_system != tm_security_method).

fof(bg_dist_tm_intrusion_detection_system_tm_single_sign_on, axiom,
    tm_intrusion_detection_system != tm_single_sign_on).

fof(bg_dist_tm_intrusion_detection_system_tm_symmetric_cryptography, axiom,
    tm_intrusion_detection_system != tm_symmetric_cryptography).

fof(bg_dist_tm_intrusion_detection_system_tm_symmetric_encryption, axiom,
    tm_intrusion_detection_system != tm_symmetric_encryption).

fof(bg_dist_tm_intrusion_detection_system_tm_technical_measure, axiom,
    tm_intrusion_detection_system != tm_technical_measure).

fof(bg_dist_tm_intrusion_detection_system_tm_technical_organisational_measure, axiom,
    tm_intrusion_detection_system != tm_technical_organisational_measure).

fof(bg_dist_tm_intrusion_detection_system_tm_trusted_computing, axiom,
    tm_intrusion_detection_system != tm_trusted_computing).

fof(bg_dist_tm_intrusion_detection_system_tm_trusted_execution_environment, axiom,
    tm_intrusion_detection_system != tm_trusted_execution_environment).

fof(bg_dist_tm_intrusion_detection_system_tm_usage_control, axiom,
    tm_intrusion_detection_system != tm_usage_control).

fof(bg_dist_tm_intrusion_detection_system_tm_use_synthetic_data, axiom,
    tm_intrusion_detection_system != tm_use_synthetic_data).

fof(bg_dist_tm_intrusion_detection_system_tm_virtualisation_security, axiom,
    tm_intrusion_detection_system != tm_virtualisation_security).

fof(bg_dist_tm_intrusion_detection_system_tm_vulnerability_testing_methods, axiom,
    tm_intrusion_detection_system != tm_vulnerability_testing_methods).

fof(bg_dist_tm_intrusion_detection_system_tm_web_browser_security, axiom,
    tm_intrusion_detection_system != tm_web_browser_security).

fof(bg_dist_tm_intrusion_detection_system_tm_web_security_protocols, axiom,
    tm_intrusion_detection_system != tm_web_security_protocols).

fof(bg_dist_tm_intrusion_detection_system_tm_wireless_security_protocols, axiom,
    tm_intrusion_detection_system != tm_wireless_security_protocols).

fof(bg_dist_tm_intrusion_detection_system_tm_zero_knowledge_authentication, axiom,
    tm_intrusion_detection_system != tm_zero_knowledge_authentication).

fof(bg_dist_tm_legal_measure_tm_message_authentication_codes, axiom,
    tm_legal_measure != tm_message_authentication_codes).

fof(bg_dist_tm_legal_measure_tm_mobile_platform_security, axiom,
    tm_legal_measure != tm_mobile_platform_security).

fof(bg_dist_tm_legal_measure_tm_monotonic_counter_pseudonymisation, axiom,
    tm_legal_measure != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_legal_measure_tm_multi_factor_authentication, axiom,
    tm_legal_measure != tm_multi_factor_authentication).

fof(bg_dist_tm_legal_measure_tm_network_proxy_routing, axiom,
    tm_legal_measure != tm_network_proxy_routing).

fof(bg_dist_tm_legal_measure_tm_network_security_protocols, axiom,
    tm_legal_measure != tm_network_security_protocols).

fof(bg_dist_tm_legal_measure_tm_operating_system_security, axiom,
    tm_legal_measure != tm_operating_system_security).

fof(bg_dist_tm_legal_measure_tm_organisational_measure, axiom,
    tm_legal_measure != tm_organisational_measure).

fof(bg_dist_tm_legal_measure_tm_password_authentication, axiom,
    tm_legal_measure != tm_password_authentication).

fof(bg_dist_tm_legal_measure_tm_penetration_testing_methods, axiom,
    tm_legal_measure != tm_penetration_testing_methods).

fof(bg_dist_tm_legal_measure_tm_physical_measure, axiom,
    tm_legal_measure != tm_physical_measure).

fof(bg_dist_tm_legal_measure_tm_post_quantum_cryptography, axiom,
    tm_legal_measure != tm_post_quantum_cryptography).

fof(bg_dist_tm_legal_measure_tm_privacy_preserving_protocol, axiom,
    tm_legal_measure != tm_privacy_preserving_protocol).

fof(bg_dist_tm_legal_measure_tm_private_information_retrieval, axiom,
    tm_legal_measure != tm_private_information_retrieval).

fof(bg_dist_tm_legal_measure_tm_pseudonymisation, axiom,
    tm_legal_measure != tm_pseudonymisation).

fof(bg_dist_tm_legal_measure_tm_quantum_cryptography, axiom,
    tm_legal_measure != tm_quantum_cryptography).

fof(bg_dist_tm_legal_measure_tm_r_n_g_pseudonymisation, axiom,
    tm_legal_measure != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_legal_measure_tm_secret_sharing_schemes, axiom,
    tm_legal_measure != tm_secret_sharing_schemes).

fof(bg_dist_tm_legal_measure_tm_secure_multi_party_computation, axiom,
    tm_legal_measure != tm_secure_multi_party_computation).

fof(bg_dist_tm_legal_measure_tm_security_method, axiom,
    tm_legal_measure != tm_security_method).

fof(bg_dist_tm_legal_measure_tm_single_sign_on, axiom,
    tm_legal_measure != tm_single_sign_on).

fof(bg_dist_tm_legal_measure_tm_symmetric_cryptography, axiom,
    tm_legal_measure != tm_symmetric_cryptography).

fof(bg_dist_tm_legal_measure_tm_symmetric_encryption, axiom,
    tm_legal_measure != tm_symmetric_encryption).

fof(bg_dist_tm_legal_measure_tm_technical_measure, axiom,
    tm_legal_measure != tm_technical_measure).

fof(bg_dist_tm_legal_measure_tm_technical_organisational_measure, axiom,
    tm_legal_measure != tm_technical_organisational_measure).

fof(bg_dist_tm_legal_measure_tm_trusted_computing, axiom,
    tm_legal_measure != tm_trusted_computing).

fof(bg_dist_tm_legal_measure_tm_trusted_execution_environment, axiom,
    tm_legal_measure != tm_trusted_execution_environment).

fof(bg_dist_tm_legal_measure_tm_usage_control, axiom,
    tm_legal_measure != tm_usage_control).

fof(bg_dist_tm_legal_measure_tm_use_synthetic_data, axiom,
    tm_legal_measure != tm_use_synthetic_data).

fof(bg_dist_tm_legal_measure_tm_virtualisation_security, axiom,
    tm_legal_measure != tm_virtualisation_security).

fof(bg_dist_tm_legal_measure_tm_vulnerability_testing_methods, axiom,
    tm_legal_measure != tm_vulnerability_testing_methods).

fof(bg_dist_tm_legal_measure_tm_web_browser_security, axiom,
    tm_legal_measure != tm_web_browser_security).

fof(bg_dist_tm_legal_measure_tm_web_security_protocols, axiom,
    tm_legal_measure != tm_web_security_protocols).

fof(bg_dist_tm_legal_measure_tm_wireless_security_protocols, axiom,
    tm_legal_measure != tm_wireless_security_protocols).

fof(bg_dist_tm_legal_measure_tm_zero_knowledge_authentication, axiom,
    tm_legal_measure != tm_zero_knowledge_authentication).

fof(bg_dist_tm_message_authentication_codes_tm_mobile_platform_security, axiom,
    tm_message_authentication_codes != tm_mobile_platform_security).

fof(bg_dist_tm_message_authentication_codes_tm_monotonic_counter_pseudonymisation, axiom,
    tm_message_authentication_codes != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_message_authentication_codes_tm_multi_factor_authentication, axiom,
    tm_message_authentication_codes != tm_multi_factor_authentication).

fof(bg_dist_tm_message_authentication_codes_tm_network_proxy_routing, axiom,
    tm_message_authentication_codes != tm_network_proxy_routing).

fof(bg_dist_tm_message_authentication_codes_tm_network_security_protocols, axiom,
    tm_message_authentication_codes != tm_network_security_protocols).

fof(bg_dist_tm_message_authentication_codes_tm_operating_system_security, axiom,
    tm_message_authentication_codes != tm_operating_system_security).

fof(bg_dist_tm_message_authentication_codes_tm_organisational_measure, axiom,
    tm_message_authentication_codes != tm_organisational_measure).

fof(bg_dist_tm_message_authentication_codes_tm_password_authentication, axiom,
    tm_message_authentication_codes != tm_password_authentication).

fof(bg_dist_tm_message_authentication_codes_tm_penetration_testing_methods, axiom,
    tm_message_authentication_codes != tm_penetration_testing_methods).

fof(bg_dist_tm_message_authentication_codes_tm_physical_measure, axiom,
    tm_message_authentication_codes != tm_physical_measure).

fof(bg_dist_tm_message_authentication_codes_tm_post_quantum_cryptography, axiom,
    tm_message_authentication_codes != tm_post_quantum_cryptography).

fof(bg_dist_tm_message_authentication_codes_tm_privacy_preserving_protocol, axiom,
    tm_message_authentication_codes != tm_privacy_preserving_protocol).

fof(bg_dist_tm_message_authentication_codes_tm_private_information_retrieval, axiom,
    tm_message_authentication_codes != tm_private_information_retrieval).

fof(bg_dist_tm_message_authentication_codes_tm_pseudonymisation, axiom,
    tm_message_authentication_codes != tm_pseudonymisation).

fof(bg_dist_tm_message_authentication_codes_tm_quantum_cryptography, axiom,
    tm_message_authentication_codes != tm_quantum_cryptography).

fof(bg_dist_tm_message_authentication_codes_tm_r_n_g_pseudonymisation, axiom,
    tm_message_authentication_codes != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_message_authentication_codes_tm_secret_sharing_schemes, axiom,
    tm_message_authentication_codes != tm_secret_sharing_schemes).

fof(bg_dist_tm_message_authentication_codes_tm_secure_multi_party_computation, axiom,
    tm_message_authentication_codes != tm_secure_multi_party_computation).

fof(bg_dist_tm_message_authentication_codes_tm_security_method, axiom,
    tm_message_authentication_codes != tm_security_method).

fof(bg_dist_tm_message_authentication_codes_tm_single_sign_on, axiom,
    tm_message_authentication_codes != tm_single_sign_on).

fof(bg_dist_tm_message_authentication_codes_tm_symmetric_cryptography, axiom,
    tm_message_authentication_codes != tm_symmetric_cryptography).

fof(bg_dist_tm_message_authentication_codes_tm_symmetric_encryption, axiom,
    tm_message_authentication_codes != tm_symmetric_encryption).

fof(bg_dist_tm_message_authentication_codes_tm_technical_measure, axiom,
    tm_message_authentication_codes != tm_technical_measure).

fof(bg_dist_tm_message_authentication_codes_tm_technical_organisational_measure, axiom,
    tm_message_authentication_codes != tm_technical_organisational_measure).

fof(bg_dist_tm_message_authentication_codes_tm_trusted_computing, axiom,
    tm_message_authentication_codes != tm_trusted_computing).

fof(bg_dist_tm_message_authentication_codes_tm_trusted_execution_environment, axiom,
    tm_message_authentication_codes != tm_trusted_execution_environment).

fof(bg_dist_tm_message_authentication_codes_tm_usage_control, axiom,
    tm_message_authentication_codes != tm_usage_control).

fof(bg_dist_tm_message_authentication_codes_tm_use_synthetic_data, axiom,
    tm_message_authentication_codes != tm_use_synthetic_data).

fof(bg_dist_tm_message_authentication_codes_tm_virtualisation_security, axiom,
    tm_message_authentication_codes != tm_virtualisation_security).

fof(bg_dist_tm_message_authentication_codes_tm_vulnerability_testing_methods, axiom,
    tm_message_authentication_codes != tm_vulnerability_testing_methods).

fof(bg_dist_tm_message_authentication_codes_tm_web_browser_security, axiom,
    tm_message_authentication_codes != tm_web_browser_security).

fof(bg_dist_tm_message_authentication_codes_tm_web_security_protocols, axiom,
    tm_message_authentication_codes != tm_web_security_protocols).

fof(bg_dist_tm_message_authentication_codes_tm_wireless_security_protocols, axiom,
    tm_message_authentication_codes != tm_wireless_security_protocols).

fof(bg_dist_tm_message_authentication_codes_tm_zero_knowledge_authentication, axiom,
    tm_message_authentication_codes != tm_zero_knowledge_authentication).

fof(bg_dist_tm_mobile_platform_security_tm_monotonic_counter_pseudonymisation, axiom,
    tm_mobile_platform_security != tm_monotonic_counter_pseudonymisation).

fof(bg_dist_tm_mobile_platform_security_tm_multi_factor_authentication, axiom,
    tm_mobile_platform_security != tm_multi_factor_authentication).

fof(bg_dist_tm_mobile_platform_security_tm_network_proxy_routing, axiom,
    tm_mobile_platform_security != tm_network_proxy_routing).

fof(bg_dist_tm_mobile_platform_security_tm_network_security_protocols, axiom,
    tm_mobile_platform_security != tm_network_security_protocols).

fof(bg_dist_tm_mobile_platform_security_tm_operating_system_security, axiom,
    tm_mobile_platform_security != tm_operating_system_security).

fof(bg_dist_tm_mobile_platform_security_tm_organisational_measure, axiom,
    tm_mobile_platform_security != tm_organisational_measure).

fof(bg_dist_tm_mobile_platform_security_tm_password_authentication, axiom,
    tm_mobile_platform_security != tm_password_authentication).

fof(bg_dist_tm_mobile_platform_security_tm_penetration_testing_methods, axiom,
    tm_mobile_platform_security != tm_penetration_testing_methods).

fof(bg_dist_tm_mobile_platform_security_tm_physical_measure, axiom,
    tm_mobile_platform_security != tm_physical_measure).

fof(bg_dist_tm_mobile_platform_security_tm_post_quantum_cryptography, axiom,
    tm_mobile_platform_security != tm_post_quantum_cryptography).

fof(bg_dist_tm_mobile_platform_security_tm_privacy_preserving_protocol, axiom,
    tm_mobile_platform_security != tm_privacy_preserving_protocol).

fof(bg_dist_tm_mobile_platform_security_tm_private_information_retrieval, axiom,
    tm_mobile_platform_security != tm_private_information_retrieval).

fof(bg_dist_tm_mobile_platform_security_tm_pseudonymisation, axiom,
    tm_mobile_platform_security != tm_pseudonymisation).

fof(bg_dist_tm_mobile_platform_security_tm_quantum_cryptography, axiom,
    tm_mobile_platform_security != tm_quantum_cryptography).

fof(bg_dist_tm_mobile_platform_security_tm_r_n_g_pseudonymisation, axiom,
    tm_mobile_platform_security != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_mobile_platform_security_tm_secret_sharing_schemes, axiom,
    tm_mobile_platform_security != tm_secret_sharing_schemes).

fof(bg_dist_tm_mobile_platform_security_tm_secure_multi_party_computation, axiom,
    tm_mobile_platform_security != tm_secure_multi_party_computation).

fof(bg_dist_tm_mobile_platform_security_tm_security_method, axiom,
    tm_mobile_platform_security != tm_security_method).

fof(bg_dist_tm_mobile_platform_security_tm_single_sign_on, axiom,
    tm_mobile_platform_security != tm_single_sign_on).

fof(bg_dist_tm_mobile_platform_security_tm_symmetric_cryptography, axiom,
    tm_mobile_platform_security != tm_symmetric_cryptography).

fof(bg_dist_tm_mobile_platform_security_tm_symmetric_encryption, axiom,
    tm_mobile_platform_security != tm_symmetric_encryption).

fof(bg_dist_tm_mobile_platform_security_tm_technical_measure, axiom,
    tm_mobile_platform_security != tm_technical_measure).

fof(bg_dist_tm_mobile_platform_security_tm_technical_organisational_measure, axiom,
    tm_mobile_platform_security != tm_technical_organisational_measure).

fof(bg_dist_tm_mobile_platform_security_tm_trusted_computing, axiom,
    tm_mobile_platform_security != tm_trusted_computing).

fof(bg_dist_tm_mobile_platform_security_tm_trusted_execution_environment, axiom,
    tm_mobile_platform_security != tm_trusted_execution_environment).

fof(bg_dist_tm_mobile_platform_security_tm_usage_control, axiom,
    tm_mobile_platform_security != tm_usage_control).

fof(bg_dist_tm_mobile_platform_security_tm_use_synthetic_data, axiom,
    tm_mobile_platform_security != tm_use_synthetic_data).

fof(bg_dist_tm_mobile_platform_security_tm_virtualisation_security, axiom,
    tm_mobile_platform_security != tm_virtualisation_security).

fof(bg_dist_tm_mobile_platform_security_tm_vulnerability_testing_methods, axiom,
    tm_mobile_platform_security != tm_vulnerability_testing_methods).

fof(bg_dist_tm_mobile_platform_security_tm_web_browser_security, axiom,
    tm_mobile_platform_security != tm_web_browser_security).

fof(bg_dist_tm_mobile_platform_security_tm_web_security_protocols, axiom,
    tm_mobile_platform_security != tm_web_security_protocols).

fof(bg_dist_tm_mobile_platform_security_tm_wireless_security_protocols, axiom,
    tm_mobile_platform_security != tm_wireless_security_protocols).

fof(bg_dist_tm_mobile_platform_security_tm_zero_knowledge_authentication, axiom,
    tm_mobile_platform_security != tm_zero_knowledge_authentication).

fof(bg_dist_tm_monotonic_counter_pseudonymisation_tm_multi_factor_authentication, axiom,
    tm_monotonic_counter_pseudonymisation != tm_multi_factor_authentication).

fof(bg_dist_tm_monotonic_counter_pseudonymisation_tm_network_proxy_routing, axiom,
    tm_monotonic_counter_pseudonymisation != tm_network_proxy_routing).

fof(bg_dist_tm_monotonic_counter_pseudonymisation_tm_network_security_protocols, axiom,
    tm_monotonic_counter_pseudonymisation != tm_network_security_protocols).

fof(bg_dist_tm_monotonic_counter_pseudonymisation_tm_operating_system_security, axiom,
    tm_monotonic_counter_pseudonymisation != tm_operating_system_security).

fof(bg_dist_tm_monotonic_counter_pseudonymisation_tm_organisational_measure, axiom,
    tm_monotonic_counter_pseudonymisation != tm_organisational_measure).

fof(bg_dist_tm_monotonic_counter_pseudonymisation_tm_password_authentication, axiom,
    tm_monotonic_counter_pseudonymisation != tm_password_authentication).

fof(bg_dist_tm_monotonic_counter_pseudonymisation_tm_penetration_testing_methods, axiom,
    tm_monotonic_counter_pseudonymisation != tm_penetration_testing_methods).

fof(bg_dist_tm_monotonic_counter_pseudonymisation_tm_physical_measure, axiom,
    tm_monotonic_counter_pseudonymisation != tm_physical_measure).

fof(bg_dist_tm_monotonic_counter_pseudonymisation_tm_post_quantum_cryptography, axiom,
    tm_monotonic_counter_pseudonymisation != tm_post_quantum_cryptography).

fof(bg_dist_tm_monotonic_counter_pseudonymisation_tm_privacy_preserving_protocol, axiom,
    tm_monotonic_counter_pseudonymisation != tm_privacy_preserving_protocol).

fof(bg_dist_tm_monotonic_counter_pseudonymisation_tm_private_information_retrieval, axiom,
    tm_monotonic_counter_pseudonymisation != tm_private_information_retrieval).

fof(bg_dist_tm_monotonic_counter_pseudonymisation_tm_pseudonymisation, axiom,
    tm_monotonic_counter_pseudonymisation != tm_pseudonymisation).

fof(bg_dist_tm_monotonic_counter_pseudonymisation_tm_quantum_cryptography, axiom,
    tm_monotonic_counter_pseudonymisation != tm_quantum_cryptography).

fof(bg_dist_tm_monotonic_counter_pseudonymisation_tm_r_n_g_pseudonymisation, axiom,
    tm_monotonic_counter_pseudonymisation != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_monotonic_counter_pseudonymisation_tm_secret_sharing_schemes, axiom,
    tm_monotonic_counter_pseudonymisation != tm_secret_sharing_schemes).

fof(bg_dist_tm_monotonic_counter_pseudonymisation_tm_secure_multi_party_computation, axiom,
    tm_monotonic_counter_pseudonymisation != tm_secure_multi_party_computation).

fof(bg_dist_tm_monotonic_counter_pseudonymisation_tm_security_method, axiom,
    tm_monotonic_counter_pseudonymisation != tm_security_method).

fof(bg_dist_tm_monotonic_counter_pseudonymisation_tm_single_sign_on, axiom,
    tm_monotonic_counter_pseudonymisation != tm_single_sign_on).

fof(bg_dist_tm_monotonic_counter_pseudonymisation_tm_symmetric_cryptography, axiom,
    tm_monotonic_counter_pseudonymisation != tm_symmetric_cryptography).

fof(bg_dist_tm_monotonic_counter_pseudonymisation_tm_symmetric_encryption, axiom,
    tm_monotonic_counter_pseudonymisation != tm_symmetric_encryption).

fof(bg_dist_tm_monotonic_counter_pseudonymisation_tm_technical_measure, axiom,
    tm_monotonic_counter_pseudonymisation != tm_technical_measure).

fof(bg_dist_tm_monotonic_counter_pseudonymisation_tm_technical_organisational_measure, axiom,
    tm_monotonic_counter_pseudonymisation != tm_technical_organisational_measure).

fof(bg_dist_tm_monotonic_counter_pseudonymisation_tm_trusted_computing, axiom,
    tm_monotonic_counter_pseudonymisation != tm_trusted_computing).

fof(bg_dist_tm_monotonic_counter_pseudonymisation_tm_trusted_execution_environment, axiom,
    tm_monotonic_counter_pseudonymisation != tm_trusted_execution_environment).

fof(bg_dist_tm_monotonic_counter_pseudonymisation_tm_usage_control, axiom,
    tm_monotonic_counter_pseudonymisation != tm_usage_control).

fof(bg_dist_tm_monotonic_counter_pseudonymisation_tm_use_synthetic_data, axiom,
    tm_monotonic_counter_pseudonymisation != tm_use_synthetic_data).

fof(bg_dist_tm_monotonic_counter_pseudonymisation_tm_virtualisation_security, axiom,
    tm_monotonic_counter_pseudonymisation != tm_virtualisation_security).

fof(bg_dist_tm_monotonic_counter_pseudonymisation_tm_vulnerability_testing_methods, axiom,
    tm_monotonic_counter_pseudonymisation != tm_vulnerability_testing_methods).

fof(bg_dist_tm_monotonic_counter_pseudonymisation_tm_web_browser_security, axiom,
    tm_monotonic_counter_pseudonymisation != tm_web_browser_security).

fof(bg_dist_tm_monotonic_counter_pseudonymisation_tm_web_security_protocols, axiom,
    tm_monotonic_counter_pseudonymisation != tm_web_security_protocols).

fof(bg_dist_tm_monotonic_counter_pseudonymisation_tm_wireless_security_protocols, axiom,
    tm_monotonic_counter_pseudonymisation != tm_wireless_security_protocols).

fof(bg_dist_tm_monotonic_counter_pseudonymisation_tm_zero_knowledge_authentication, axiom,
    tm_monotonic_counter_pseudonymisation != tm_zero_knowledge_authentication).

fof(bg_dist_tm_multi_factor_authentication_tm_network_proxy_routing, axiom,
    tm_multi_factor_authentication != tm_network_proxy_routing).

fof(bg_dist_tm_multi_factor_authentication_tm_network_security_protocols, axiom,
    tm_multi_factor_authentication != tm_network_security_protocols).

fof(bg_dist_tm_multi_factor_authentication_tm_operating_system_security, axiom,
    tm_multi_factor_authentication != tm_operating_system_security).

fof(bg_dist_tm_multi_factor_authentication_tm_organisational_measure, axiom,
    tm_multi_factor_authentication != tm_organisational_measure).

fof(bg_dist_tm_multi_factor_authentication_tm_password_authentication, axiom,
    tm_multi_factor_authentication != tm_password_authentication).

fof(bg_dist_tm_multi_factor_authentication_tm_penetration_testing_methods, axiom,
    tm_multi_factor_authentication != tm_penetration_testing_methods).

fof(bg_dist_tm_multi_factor_authentication_tm_physical_measure, axiom,
    tm_multi_factor_authentication != tm_physical_measure).

fof(bg_dist_tm_multi_factor_authentication_tm_post_quantum_cryptography, axiom,
    tm_multi_factor_authentication != tm_post_quantum_cryptography).

fof(bg_dist_tm_multi_factor_authentication_tm_privacy_preserving_protocol, axiom,
    tm_multi_factor_authentication != tm_privacy_preserving_protocol).

fof(bg_dist_tm_multi_factor_authentication_tm_private_information_retrieval, axiom,
    tm_multi_factor_authentication != tm_private_information_retrieval).

fof(bg_dist_tm_multi_factor_authentication_tm_pseudonymisation, axiom,
    tm_multi_factor_authentication != tm_pseudonymisation).

fof(bg_dist_tm_multi_factor_authentication_tm_quantum_cryptography, axiom,
    tm_multi_factor_authentication != tm_quantum_cryptography).

fof(bg_dist_tm_multi_factor_authentication_tm_r_n_g_pseudonymisation, axiom,
    tm_multi_factor_authentication != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_multi_factor_authentication_tm_secret_sharing_schemes, axiom,
    tm_multi_factor_authentication != tm_secret_sharing_schemes).

fof(bg_dist_tm_multi_factor_authentication_tm_secure_multi_party_computation, axiom,
    tm_multi_factor_authentication != tm_secure_multi_party_computation).

fof(bg_dist_tm_multi_factor_authentication_tm_security_method, axiom,
    tm_multi_factor_authentication != tm_security_method).

fof(bg_dist_tm_multi_factor_authentication_tm_single_sign_on, axiom,
    tm_multi_factor_authentication != tm_single_sign_on).

fof(bg_dist_tm_multi_factor_authentication_tm_symmetric_cryptography, axiom,
    tm_multi_factor_authentication != tm_symmetric_cryptography).

fof(bg_dist_tm_multi_factor_authentication_tm_symmetric_encryption, axiom,
    tm_multi_factor_authentication != tm_symmetric_encryption).

fof(bg_dist_tm_multi_factor_authentication_tm_technical_measure, axiom,
    tm_multi_factor_authentication != tm_technical_measure).

fof(bg_dist_tm_multi_factor_authentication_tm_technical_organisational_measure, axiom,
    tm_multi_factor_authentication != tm_technical_organisational_measure).

fof(bg_dist_tm_multi_factor_authentication_tm_trusted_computing, axiom,
    tm_multi_factor_authentication != tm_trusted_computing).

fof(bg_dist_tm_multi_factor_authentication_tm_trusted_execution_environment, axiom,
    tm_multi_factor_authentication != tm_trusted_execution_environment).

fof(bg_dist_tm_multi_factor_authentication_tm_usage_control, axiom,
    tm_multi_factor_authentication != tm_usage_control).

fof(bg_dist_tm_multi_factor_authentication_tm_use_synthetic_data, axiom,
    tm_multi_factor_authentication != tm_use_synthetic_data).

fof(bg_dist_tm_multi_factor_authentication_tm_virtualisation_security, axiom,
    tm_multi_factor_authentication != tm_virtualisation_security).

fof(bg_dist_tm_multi_factor_authentication_tm_vulnerability_testing_methods, axiom,
    tm_multi_factor_authentication != tm_vulnerability_testing_methods).

fof(bg_dist_tm_multi_factor_authentication_tm_web_browser_security, axiom,
    tm_multi_factor_authentication != tm_web_browser_security).

fof(bg_dist_tm_multi_factor_authentication_tm_web_security_protocols, axiom,
    tm_multi_factor_authentication != tm_web_security_protocols).

fof(bg_dist_tm_multi_factor_authentication_tm_wireless_security_protocols, axiom,
    tm_multi_factor_authentication != tm_wireless_security_protocols).

fof(bg_dist_tm_multi_factor_authentication_tm_zero_knowledge_authentication, axiom,
    tm_multi_factor_authentication != tm_zero_knowledge_authentication).

fof(bg_dist_tm_network_proxy_routing_tm_network_security_protocols, axiom,
    tm_network_proxy_routing != tm_network_security_protocols).

fof(bg_dist_tm_network_proxy_routing_tm_operating_system_security, axiom,
    tm_network_proxy_routing != tm_operating_system_security).

fof(bg_dist_tm_network_proxy_routing_tm_organisational_measure, axiom,
    tm_network_proxy_routing != tm_organisational_measure).

fof(bg_dist_tm_network_proxy_routing_tm_password_authentication, axiom,
    tm_network_proxy_routing != tm_password_authentication).

fof(bg_dist_tm_network_proxy_routing_tm_penetration_testing_methods, axiom,
    tm_network_proxy_routing != tm_penetration_testing_methods).

fof(bg_dist_tm_network_proxy_routing_tm_physical_measure, axiom,
    tm_network_proxy_routing != tm_physical_measure).

fof(bg_dist_tm_network_proxy_routing_tm_post_quantum_cryptography, axiom,
    tm_network_proxy_routing != tm_post_quantum_cryptography).

fof(bg_dist_tm_network_proxy_routing_tm_privacy_preserving_protocol, axiom,
    tm_network_proxy_routing != tm_privacy_preserving_protocol).

fof(bg_dist_tm_network_proxy_routing_tm_private_information_retrieval, axiom,
    tm_network_proxy_routing != tm_private_information_retrieval).

fof(bg_dist_tm_network_proxy_routing_tm_pseudonymisation, axiom,
    tm_network_proxy_routing != tm_pseudonymisation).

fof(bg_dist_tm_network_proxy_routing_tm_quantum_cryptography, axiom,
    tm_network_proxy_routing != tm_quantum_cryptography).

fof(bg_dist_tm_network_proxy_routing_tm_r_n_g_pseudonymisation, axiom,
    tm_network_proxy_routing != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_network_proxy_routing_tm_secret_sharing_schemes, axiom,
    tm_network_proxy_routing != tm_secret_sharing_schemes).

fof(bg_dist_tm_network_proxy_routing_tm_secure_multi_party_computation, axiom,
    tm_network_proxy_routing != tm_secure_multi_party_computation).

fof(bg_dist_tm_network_proxy_routing_tm_security_method, axiom,
    tm_network_proxy_routing != tm_security_method).

fof(bg_dist_tm_network_proxy_routing_tm_single_sign_on, axiom,
    tm_network_proxy_routing != tm_single_sign_on).

fof(bg_dist_tm_network_proxy_routing_tm_symmetric_cryptography, axiom,
    tm_network_proxy_routing != tm_symmetric_cryptography).

fof(bg_dist_tm_network_proxy_routing_tm_symmetric_encryption, axiom,
    tm_network_proxy_routing != tm_symmetric_encryption).

fof(bg_dist_tm_network_proxy_routing_tm_technical_measure, axiom,
    tm_network_proxy_routing != tm_technical_measure).

fof(bg_dist_tm_network_proxy_routing_tm_technical_organisational_measure, axiom,
    tm_network_proxy_routing != tm_technical_organisational_measure).

fof(bg_dist_tm_network_proxy_routing_tm_trusted_computing, axiom,
    tm_network_proxy_routing != tm_trusted_computing).

fof(bg_dist_tm_network_proxy_routing_tm_trusted_execution_environment, axiom,
    tm_network_proxy_routing != tm_trusted_execution_environment).

fof(bg_dist_tm_network_proxy_routing_tm_usage_control, axiom,
    tm_network_proxy_routing != tm_usage_control).

fof(bg_dist_tm_network_proxy_routing_tm_use_synthetic_data, axiom,
    tm_network_proxy_routing != tm_use_synthetic_data).

fof(bg_dist_tm_network_proxy_routing_tm_virtualisation_security, axiom,
    tm_network_proxy_routing != tm_virtualisation_security).

fof(bg_dist_tm_network_proxy_routing_tm_vulnerability_testing_methods, axiom,
    tm_network_proxy_routing != tm_vulnerability_testing_methods).

fof(bg_dist_tm_network_proxy_routing_tm_web_browser_security, axiom,
    tm_network_proxy_routing != tm_web_browser_security).

fof(bg_dist_tm_network_proxy_routing_tm_web_security_protocols, axiom,
    tm_network_proxy_routing != tm_web_security_protocols).

fof(bg_dist_tm_network_proxy_routing_tm_wireless_security_protocols, axiom,
    tm_network_proxy_routing != tm_wireless_security_protocols).

fof(bg_dist_tm_network_proxy_routing_tm_zero_knowledge_authentication, axiom,
    tm_network_proxy_routing != tm_zero_knowledge_authentication).

fof(bg_dist_tm_network_security_protocols_tm_operating_system_security, axiom,
    tm_network_security_protocols != tm_operating_system_security).

fof(bg_dist_tm_network_security_protocols_tm_organisational_measure, axiom,
    tm_network_security_protocols != tm_organisational_measure).

fof(bg_dist_tm_network_security_protocols_tm_password_authentication, axiom,
    tm_network_security_protocols != tm_password_authentication).

fof(bg_dist_tm_network_security_protocols_tm_penetration_testing_methods, axiom,
    tm_network_security_protocols != tm_penetration_testing_methods).

fof(bg_dist_tm_network_security_protocols_tm_physical_measure, axiom,
    tm_network_security_protocols != tm_physical_measure).

fof(bg_dist_tm_network_security_protocols_tm_post_quantum_cryptography, axiom,
    tm_network_security_protocols != tm_post_quantum_cryptography).

fof(bg_dist_tm_network_security_protocols_tm_privacy_preserving_protocol, axiom,
    tm_network_security_protocols != tm_privacy_preserving_protocol).

fof(bg_dist_tm_network_security_protocols_tm_private_information_retrieval, axiom,
    tm_network_security_protocols != tm_private_information_retrieval).

fof(bg_dist_tm_network_security_protocols_tm_pseudonymisation, axiom,
    tm_network_security_protocols != tm_pseudonymisation).

fof(bg_dist_tm_network_security_protocols_tm_quantum_cryptography, axiom,
    tm_network_security_protocols != tm_quantum_cryptography).

fof(bg_dist_tm_network_security_protocols_tm_r_n_g_pseudonymisation, axiom,
    tm_network_security_protocols != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_network_security_protocols_tm_secret_sharing_schemes, axiom,
    tm_network_security_protocols != tm_secret_sharing_schemes).

fof(bg_dist_tm_network_security_protocols_tm_secure_multi_party_computation, axiom,
    tm_network_security_protocols != tm_secure_multi_party_computation).

fof(bg_dist_tm_network_security_protocols_tm_security_method, axiom,
    tm_network_security_protocols != tm_security_method).

fof(bg_dist_tm_network_security_protocols_tm_single_sign_on, axiom,
    tm_network_security_protocols != tm_single_sign_on).

fof(bg_dist_tm_network_security_protocols_tm_symmetric_cryptography, axiom,
    tm_network_security_protocols != tm_symmetric_cryptography).

fof(bg_dist_tm_network_security_protocols_tm_symmetric_encryption, axiom,
    tm_network_security_protocols != tm_symmetric_encryption).

fof(bg_dist_tm_network_security_protocols_tm_technical_measure, axiom,
    tm_network_security_protocols != tm_technical_measure).

fof(bg_dist_tm_network_security_protocols_tm_technical_organisational_measure, axiom,
    tm_network_security_protocols != tm_technical_organisational_measure).

fof(bg_dist_tm_network_security_protocols_tm_trusted_computing, axiom,
    tm_network_security_protocols != tm_trusted_computing).

fof(bg_dist_tm_network_security_protocols_tm_trusted_execution_environment, axiom,
    tm_network_security_protocols != tm_trusted_execution_environment).

fof(bg_dist_tm_network_security_protocols_tm_usage_control, axiom,
    tm_network_security_protocols != tm_usage_control).

fof(bg_dist_tm_network_security_protocols_tm_use_synthetic_data, axiom,
    tm_network_security_protocols != tm_use_synthetic_data).

fof(bg_dist_tm_network_security_protocols_tm_virtualisation_security, axiom,
    tm_network_security_protocols != tm_virtualisation_security).

fof(bg_dist_tm_network_security_protocols_tm_vulnerability_testing_methods, axiom,
    tm_network_security_protocols != tm_vulnerability_testing_methods).

fof(bg_dist_tm_network_security_protocols_tm_web_browser_security, axiom,
    tm_network_security_protocols != tm_web_browser_security).

fof(bg_dist_tm_network_security_protocols_tm_web_security_protocols, axiom,
    tm_network_security_protocols != tm_web_security_protocols).

fof(bg_dist_tm_network_security_protocols_tm_wireless_security_protocols, axiom,
    tm_network_security_protocols != tm_wireless_security_protocols).

fof(bg_dist_tm_network_security_protocols_tm_zero_knowledge_authentication, axiom,
    tm_network_security_protocols != tm_zero_knowledge_authentication).

fof(bg_dist_tm_operating_system_security_tm_organisational_measure, axiom,
    tm_operating_system_security != tm_organisational_measure).

fof(bg_dist_tm_operating_system_security_tm_password_authentication, axiom,
    tm_operating_system_security != tm_password_authentication).

fof(bg_dist_tm_operating_system_security_tm_penetration_testing_methods, axiom,
    tm_operating_system_security != tm_penetration_testing_methods).

fof(bg_dist_tm_operating_system_security_tm_physical_measure, axiom,
    tm_operating_system_security != tm_physical_measure).

fof(bg_dist_tm_operating_system_security_tm_post_quantum_cryptography, axiom,
    tm_operating_system_security != tm_post_quantum_cryptography).

fof(bg_dist_tm_operating_system_security_tm_privacy_preserving_protocol, axiom,
    tm_operating_system_security != tm_privacy_preserving_protocol).

fof(bg_dist_tm_operating_system_security_tm_private_information_retrieval, axiom,
    tm_operating_system_security != tm_private_information_retrieval).

fof(bg_dist_tm_operating_system_security_tm_pseudonymisation, axiom,
    tm_operating_system_security != tm_pseudonymisation).

fof(bg_dist_tm_operating_system_security_tm_quantum_cryptography, axiom,
    tm_operating_system_security != tm_quantum_cryptography).

fof(bg_dist_tm_operating_system_security_tm_r_n_g_pseudonymisation, axiom,
    tm_operating_system_security != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_operating_system_security_tm_secret_sharing_schemes, axiom,
    tm_operating_system_security != tm_secret_sharing_schemes).

fof(bg_dist_tm_operating_system_security_tm_secure_multi_party_computation, axiom,
    tm_operating_system_security != tm_secure_multi_party_computation).

fof(bg_dist_tm_operating_system_security_tm_security_method, axiom,
    tm_operating_system_security != tm_security_method).

fof(bg_dist_tm_operating_system_security_tm_single_sign_on, axiom,
    tm_operating_system_security != tm_single_sign_on).

fof(bg_dist_tm_operating_system_security_tm_symmetric_cryptography, axiom,
    tm_operating_system_security != tm_symmetric_cryptography).

fof(bg_dist_tm_operating_system_security_tm_symmetric_encryption, axiom,
    tm_operating_system_security != tm_symmetric_encryption).

fof(bg_dist_tm_operating_system_security_tm_technical_measure, axiom,
    tm_operating_system_security != tm_technical_measure).

fof(bg_dist_tm_operating_system_security_tm_technical_organisational_measure, axiom,
    tm_operating_system_security != tm_technical_organisational_measure).

fof(bg_dist_tm_operating_system_security_tm_trusted_computing, axiom,
    tm_operating_system_security != tm_trusted_computing).

fof(bg_dist_tm_operating_system_security_tm_trusted_execution_environment, axiom,
    tm_operating_system_security != tm_trusted_execution_environment).

fof(bg_dist_tm_operating_system_security_tm_usage_control, axiom,
    tm_operating_system_security != tm_usage_control).

fof(bg_dist_tm_operating_system_security_tm_use_synthetic_data, axiom,
    tm_operating_system_security != tm_use_synthetic_data).

fof(bg_dist_tm_operating_system_security_tm_virtualisation_security, axiom,
    tm_operating_system_security != tm_virtualisation_security).

fof(bg_dist_tm_operating_system_security_tm_vulnerability_testing_methods, axiom,
    tm_operating_system_security != tm_vulnerability_testing_methods).

fof(bg_dist_tm_operating_system_security_tm_web_browser_security, axiom,
    tm_operating_system_security != tm_web_browser_security).

fof(bg_dist_tm_operating_system_security_tm_web_security_protocols, axiom,
    tm_operating_system_security != tm_web_security_protocols).

fof(bg_dist_tm_operating_system_security_tm_wireless_security_protocols, axiom,
    tm_operating_system_security != tm_wireless_security_protocols).

fof(bg_dist_tm_operating_system_security_tm_zero_knowledge_authentication, axiom,
    tm_operating_system_security != tm_zero_knowledge_authentication).

fof(bg_dist_tm_organisational_measure_tm_password_authentication, axiom,
    tm_organisational_measure != tm_password_authentication).

fof(bg_dist_tm_organisational_measure_tm_penetration_testing_methods, axiom,
    tm_organisational_measure != tm_penetration_testing_methods).

fof(bg_dist_tm_organisational_measure_tm_physical_measure, axiom,
    tm_organisational_measure != tm_physical_measure).

fof(bg_dist_tm_organisational_measure_tm_post_quantum_cryptography, axiom,
    tm_organisational_measure != tm_post_quantum_cryptography).

fof(bg_dist_tm_organisational_measure_tm_privacy_preserving_protocol, axiom,
    tm_organisational_measure != tm_privacy_preserving_protocol).

fof(bg_dist_tm_organisational_measure_tm_private_information_retrieval, axiom,
    tm_organisational_measure != tm_private_information_retrieval).

fof(bg_dist_tm_organisational_measure_tm_pseudonymisation, axiom,
    tm_organisational_measure != tm_pseudonymisation).

fof(bg_dist_tm_organisational_measure_tm_quantum_cryptography, axiom,
    tm_organisational_measure != tm_quantum_cryptography).

fof(bg_dist_tm_organisational_measure_tm_r_n_g_pseudonymisation, axiom,
    tm_organisational_measure != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_organisational_measure_tm_secret_sharing_schemes, axiom,
    tm_organisational_measure != tm_secret_sharing_schemes).

fof(bg_dist_tm_organisational_measure_tm_secure_multi_party_computation, axiom,
    tm_organisational_measure != tm_secure_multi_party_computation).

fof(bg_dist_tm_organisational_measure_tm_security_method, axiom,
    tm_organisational_measure != tm_security_method).

fof(bg_dist_tm_organisational_measure_tm_single_sign_on, axiom,
    tm_organisational_measure != tm_single_sign_on).

fof(bg_dist_tm_organisational_measure_tm_symmetric_cryptography, axiom,
    tm_organisational_measure != tm_symmetric_cryptography).

fof(bg_dist_tm_organisational_measure_tm_symmetric_encryption, axiom,
    tm_organisational_measure != tm_symmetric_encryption).

fof(bg_dist_tm_organisational_measure_tm_technical_measure, axiom,
    tm_organisational_measure != tm_technical_measure).

fof(bg_dist_tm_organisational_measure_tm_technical_organisational_measure, axiom,
    tm_organisational_measure != tm_technical_organisational_measure).

fof(bg_dist_tm_organisational_measure_tm_trusted_computing, axiom,
    tm_organisational_measure != tm_trusted_computing).

fof(bg_dist_tm_organisational_measure_tm_trusted_execution_environment, axiom,
    tm_organisational_measure != tm_trusted_execution_environment).

fof(bg_dist_tm_organisational_measure_tm_usage_control, axiom,
    tm_organisational_measure != tm_usage_control).

fof(bg_dist_tm_organisational_measure_tm_use_synthetic_data, axiom,
    tm_organisational_measure != tm_use_synthetic_data).

fof(bg_dist_tm_organisational_measure_tm_virtualisation_security, axiom,
    tm_organisational_measure != tm_virtualisation_security).

fof(bg_dist_tm_organisational_measure_tm_vulnerability_testing_methods, axiom,
    tm_organisational_measure != tm_vulnerability_testing_methods).

fof(bg_dist_tm_organisational_measure_tm_web_browser_security, axiom,
    tm_organisational_measure != tm_web_browser_security).

fof(bg_dist_tm_organisational_measure_tm_web_security_protocols, axiom,
    tm_organisational_measure != tm_web_security_protocols).

fof(bg_dist_tm_organisational_measure_tm_wireless_security_protocols, axiom,
    tm_organisational_measure != tm_wireless_security_protocols).

fof(bg_dist_tm_organisational_measure_tm_zero_knowledge_authentication, axiom,
    tm_organisational_measure != tm_zero_knowledge_authentication).

fof(bg_dist_tm_password_authentication_tm_penetration_testing_methods, axiom,
    tm_password_authentication != tm_penetration_testing_methods).

fof(bg_dist_tm_password_authentication_tm_physical_measure, axiom,
    tm_password_authentication != tm_physical_measure).

fof(bg_dist_tm_password_authentication_tm_post_quantum_cryptography, axiom,
    tm_password_authentication != tm_post_quantum_cryptography).

fof(bg_dist_tm_password_authentication_tm_privacy_preserving_protocol, axiom,
    tm_password_authentication != tm_privacy_preserving_protocol).

fof(bg_dist_tm_password_authentication_tm_private_information_retrieval, axiom,
    tm_password_authentication != tm_private_information_retrieval).

fof(bg_dist_tm_password_authentication_tm_pseudonymisation, axiom,
    tm_password_authentication != tm_pseudonymisation).

fof(bg_dist_tm_password_authentication_tm_quantum_cryptography, axiom,
    tm_password_authentication != tm_quantum_cryptography).

fof(bg_dist_tm_password_authentication_tm_r_n_g_pseudonymisation, axiom,
    tm_password_authentication != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_password_authentication_tm_secret_sharing_schemes, axiom,
    tm_password_authentication != tm_secret_sharing_schemes).

fof(bg_dist_tm_password_authentication_tm_secure_multi_party_computation, axiom,
    tm_password_authentication != tm_secure_multi_party_computation).

fof(bg_dist_tm_password_authentication_tm_security_method, axiom,
    tm_password_authentication != tm_security_method).

fof(bg_dist_tm_password_authentication_tm_single_sign_on, axiom,
    tm_password_authentication != tm_single_sign_on).

fof(bg_dist_tm_password_authentication_tm_symmetric_cryptography, axiom,
    tm_password_authentication != tm_symmetric_cryptography).

fof(bg_dist_tm_password_authentication_tm_symmetric_encryption, axiom,
    tm_password_authentication != tm_symmetric_encryption).

fof(bg_dist_tm_password_authentication_tm_technical_measure, axiom,
    tm_password_authentication != tm_technical_measure).

fof(bg_dist_tm_password_authentication_tm_technical_organisational_measure, axiom,
    tm_password_authentication != tm_technical_organisational_measure).

fof(bg_dist_tm_password_authentication_tm_trusted_computing, axiom,
    tm_password_authentication != tm_trusted_computing).

fof(bg_dist_tm_password_authentication_tm_trusted_execution_environment, axiom,
    tm_password_authentication != tm_trusted_execution_environment).

fof(bg_dist_tm_password_authentication_tm_usage_control, axiom,
    tm_password_authentication != tm_usage_control).

fof(bg_dist_tm_password_authentication_tm_use_synthetic_data, axiom,
    tm_password_authentication != tm_use_synthetic_data).

fof(bg_dist_tm_password_authentication_tm_virtualisation_security, axiom,
    tm_password_authentication != tm_virtualisation_security).

fof(bg_dist_tm_password_authentication_tm_vulnerability_testing_methods, axiom,
    tm_password_authentication != tm_vulnerability_testing_methods).

fof(bg_dist_tm_password_authentication_tm_web_browser_security, axiom,
    tm_password_authentication != tm_web_browser_security).

fof(bg_dist_tm_password_authentication_tm_web_security_protocols, axiom,
    tm_password_authentication != tm_web_security_protocols).

fof(bg_dist_tm_password_authentication_tm_wireless_security_protocols, axiom,
    tm_password_authentication != tm_wireless_security_protocols).

fof(bg_dist_tm_password_authentication_tm_zero_knowledge_authentication, axiom,
    tm_password_authentication != tm_zero_knowledge_authentication).

fof(bg_dist_tm_penetration_testing_methods_tm_physical_measure, axiom,
    tm_penetration_testing_methods != tm_physical_measure).

fof(bg_dist_tm_penetration_testing_methods_tm_post_quantum_cryptography, axiom,
    tm_penetration_testing_methods != tm_post_quantum_cryptography).

fof(bg_dist_tm_penetration_testing_methods_tm_privacy_preserving_protocol, axiom,
    tm_penetration_testing_methods != tm_privacy_preserving_protocol).

fof(bg_dist_tm_penetration_testing_methods_tm_private_information_retrieval, axiom,
    tm_penetration_testing_methods != tm_private_information_retrieval).

fof(bg_dist_tm_penetration_testing_methods_tm_pseudonymisation, axiom,
    tm_penetration_testing_methods != tm_pseudonymisation).

fof(bg_dist_tm_penetration_testing_methods_tm_quantum_cryptography, axiom,
    tm_penetration_testing_methods != tm_quantum_cryptography).

fof(bg_dist_tm_penetration_testing_methods_tm_r_n_g_pseudonymisation, axiom,
    tm_penetration_testing_methods != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_penetration_testing_methods_tm_secret_sharing_schemes, axiom,
    tm_penetration_testing_methods != tm_secret_sharing_schemes).

fof(bg_dist_tm_penetration_testing_methods_tm_secure_multi_party_computation, axiom,
    tm_penetration_testing_methods != tm_secure_multi_party_computation).

fof(bg_dist_tm_penetration_testing_methods_tm_security_method, axiom,
    tm_penetration_testing_methods != tm_security_method).

fof(bg_dist_tm_penetration_testing_methods_tm_single_sign_on, axiom,
    tm_penetration_testing_methods != tm_single_sign_on).

fof(bg_dist_tm_penetration_testing_methods_tm_symmetric_cryptography, axiom,
    tm_penetration_testing_methods != tm_symmetric_cryptography).

fof(bg_dist_tm_penetration_testing_methods_tm_symmetric_encryption, axiom,
    tm_penetration_testing_methods != tm_symmetric_encryption).

fof(bg_dist_tm_penetration_testing_methods_tm_technical_measure, axiom,
    tm_penetration_testing_methods != tm_technical_measure).

fof(bg_dist_tm_penetration_testing_methods_tm_technical_organisational_measure, axiom,
    tm_penetration_testing_methods != tm_technical_organisational_measure).

fof(bg_dist_tm_penetration_testing_methods_tm_trusted_computing, axiom,
    tm_penetration_testing_methods != tm_trusted_computing).

fof(bg_dist_tm_penetration_testing_methods_tm_trusted_execution_environment, axiom,
    tm_penetration_testing_methods != tm_trusted_execution_environment).

fof(bg_dist_tm_penetration_testing_methods_tm_usage_control, axiom,
    tm_penetration_testing_methods != tm_usage_control).

fof(bg_dist_tm_penetration_testing_methods_tm_use_synthetic_data, axiom,
    tm_penetration_testing_methods != tm_use_synthetic_data).

fof(bg_dist_tm_penetration_testing_methods_tm_virtualisation_security, axiom,
    tm_penetration_testing_methods != tm_virtualisation_security).

fof(bg_dist_tm_penetration_testing_methods_tm_vulnerability_testing_methods, axiom,
    tm_penetration_testing_methods != tm_vulnerability_testing_methods).

fof(bg_dist_tm_penetration_testing_methods_tm_web_browser_security, axiom,
    tm_penetration_testing_methods != tm_web_browser_security).

fof(bg_dist_tm_penetration_testing_methods_tm_web_security_protocols, axiom,
    tm_penetration_testing_methods != tm_web_security_protocols).

fof(bg_dist_tm_penetration_testing_methods_tm_wireless_security_protocols, axiom,
    tm_penetration_testing_methods != tm_wireless_security_protocols).

fof(bg_dist_tm_penetration_testing_methods_tm_zero_knowledge_authentication, axiom,
    tm_penetration_testing_methods != tm_zero_knowledge_authentication).

fof(bg_dist_tm_physical_measure_tm_post_quantum_cryptography, axiom,
    tm_physical_measure != tm_post_quantum_cryptography).

fof(bg_dist_tm_physical_measure_tm_privacy_preserving_protocol, axiom,
    tm_physical_measure != tm_privacy_preserving_protocol).

fof(bg_dist_tm_physical_measure_tm_private_information_retrieval, axiom,
    tm_physical_measure != tm_private_information_retrieval).

fof(bg_dist_tm_physical_measure_tm_pseudonymisation, axiom,
    tm_physical_measure != tm_pseudonymisation).

fof(bg_dist_tm_physical_measure_tm_quantum_cryptography, axiom,
    tm_physical_measure != tm_quantum_cryptography).

fof(bg_dist_tm_physical_measure_tm_r_n_g_pseudonymisation, axiom,
    tm_physical_measure != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_physical_measure_tm_secret_sharing_schemes, axiom,
    tm_physical_measure != tm_secret_sharing_schemes).

fof(bg_dist_tm_physical_measure_tm_secure_multi_party_computation, axiom,
    tm_physical_measure != tm_secure_multi_party_computation).

fof(bg_dist_tm_physical_measure_tm_security_method, axiom,
    tm_physical_measure != tm_security_method).

fof(bg_dist_tm_physical_measure_tm_single_sign_on, axiom,
    tm_physical_measure != tm_single_sign_on).

fof(bg_dist_tm_physical_measure_tm_symmetric_cryptography, axiom,
    tm_physical_measure != tm_symmetric_cryptography).

fof(bg_dist_tm_physical_measure_tm_symmetric_encryption, axiom,
    tm_physical_measure != tm_symmetric_encryption).

fof(bg_dist_tm_physical_measure_tm_technical_measure, axiom,
    tm_physical_measure != tm_technical_measure).

fof(bg_dist_tm_physical_measure_tm_technical_organisational_measure, axiom,
    tm_physical_measure != tm_technical_organisational_measure).

fof(bg_dist_tm_physical_measure_tm_trusted_computing, axiom,
    tm_physical_measure != tm_trusted_computing).

fof(bg_dist_tm_physical_measure_tm_trusted_execution_environment, axiom,
    tm_physical_measure != tm_trusted_execution_environment).

fof(bg_dist_tm_physical_measure_tm_usage_control, axiom,
    tm_physical_measure != tm_usage_control).

fof(bg_dist_tm_physical_measure_tm_use_synthetic_data, axiom,
    tm_physical_measure != tm_use_synthetic_data).

fof(bg_dist_tm_physical_measure_tm_virtualisation_security, axiom,
    tm_physical_measure != tm_virtualisation_security).

fof(bg_dist_tm_physical_measure_tm_vulnerability_testing_methods, axiom,
    tm_physical_measure != tm_vulnerability_testing_methods).

fof(bg_dist_tm_physical_measure_tm_web_browser_security, axiom,
    tm_physical_measure != tm_web_browser_security).

fof(bg_dist_tm_physical_measure_tm_web_security_protocols, axiom,
    tm_physical_measure != tm_web_security_protocols).

fof(bg_dist_tm_physical_measure_tm_wireless_security_protocols, axiom,
    tm_physical_measure != tm_wireless_security_protocols).

fof(bg_dist_tm_physical_measure_tm_zero_knowledge_authentication, axiom,
    tm_physical_measure != tm_zero_knowledge_authentication).

fof(bg_dist_tm_post_quantum_cryptography_tm_privacy_preserving_protocol, axiom,
    tm_post_quantum_cryptography != tm_privacy_preserving_protocol).

fof(bg_dist_tm_post_quantum_cryptography_tm_private_information_retrieval, axiom,
    tm_post_quantum_cryptography != tm_private_information_retrieval).

fof(bg_dist_tm_post_quantum_cryptography_tm_pseudonymisation, axiom,
    tm_post_quantum_cryptography != tm_pseudonymisation).

fof(bg_dist_tm_post_quantum_cryptography_tm_quantum_cryptography, axiom,
    tm_post_quantum_cryptography != tm_quantum_cryptography).

fof(bg_dist_tm_post_quantum_cryptography_tm_r_n_g_pseudonymisation, axiom,
    tm_post_quantum_cryptography != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_post_quantum_cryptography_tm_secret_sharing_schemes, axiom,
    tm_post_quantum_cryptography != tm_secret_sharing_schemes).

fof(bg_dist_tm_post_quantum_cryptography_tm_secure_multi_party_computation, axiom,
    tm_post_quantum_cryptography != tm_secure_multi_party_computation).

fof(bg_dist_tm_post_quantum_cryptography_tm_security_method, axiom,
    tm_post_quantum_cryptography != tm_security_method).

fof(bg_dist_tm_post_quantum_cryptography_tm_single_sign_on, axiom,
    tm_post_quantum_cryptography != tm_single_sign_on).

fof(bg_dist_tm_post_quantum_cryptography_tm_symmetric_cryptography, axiom,
    tm_post_quantum_cryptography != tm_symmetric_cryptography).

fof(bg_dist_tm_post_quantum_cryptography_tm_symmetric_encryption, axiom,
    tm_post_quantum_cryptography != tm_symmetric_encryption).

fof(bg_dist_tm_post_quantum_cryptography_tm_technical_measure, axiom,
    tm_post_quantum_cryptography != tm_technical_measure).

fof(bg_dist_tm_post_quantum_cryptography_tm_technical_organisational_measure, axiom,
    tm_post_quantum_cryptography != tm_technical_organisational_measure).

fof(bg_dist_tm_post_quantum_cryptography_tm_trusted_computing, axiom,
    tm_post_quantum_cryptography != tm_trusted_computing).

fof(bg_dist_tm_post_quantum_cryptography_tm_trusted_execution_environment, axiom,
    tm_post_quantum_cryptography != tm_trusted_execution_environment).

fof(bg_dist_tm_post_quantum_cryptography_tm_usage_control, axiom,
    tm_post_quantum_cryptography != tm_usage_control).

fof(bg_dist_tm_post_quantum_cryptography_tm_use_synthetic_data, axiom,
    tm_post_quantum_cryptography != tm_use_synthetic_data).

fof(bg_dist_tm_post_quantum_cryptography_tm_virtualisation_security, axiom,
    tm_post_quantum_cryptography != tm_virtualisation_security).

fof(bg_dist_tm_post_quantum_cryptography_tm_vulnerability_testing_methods, axiom,
    tm_post_quantum_cryptography != tm_vulnerability_testing_methods).

fof(bg_dist_tm_post_quantum_cryptography_tm_web_browser_security, axiom,
    tm_post_quantum_cryptography != tm_web_browser_security).

fof(bg_dist_tm_post_quantum_cryptography_tm_web_security_protocols, axiom,
    tm_post_quantum_cryptography != tm_web_security_protocols).

fof(bg_dist_tm_post_quantum_cryptography_tm_wireless_security_protocols, axiom,
    tm_post_quantum_cryptography != tm_wireless_security_protocols).

fof(bg_dist_tm_post_quantum_cryptography_tm_zero_knowledge_authentication, axiom,
    tm_post_quantum_cryptography != tm_zero_knowledge_authentication).

fof(bg_dist_tm_privacy_preserving_protocol_tm_private_information_retrieval, axiom,
    tm_privacy_preserving_protocol != tm_private_information_retrieval).

fof(bg_dist_tm_privacy_preserving_protocol_tm_pseudonymisation, axiom,
    tm_privacy_preserving_protocol != tm_pseudonymisation).

fof(bg_dist_tm_privacy_preserving_protocol_tm_quantum_cryptography, axiom,
    tm_privacy_preserving_protocol != tm_quantum_cryptography).

fof(bg_dist_tm_privacy_preserving_protocol_tm_r_n_g_pseudonymisation, axiom,
    tm_privacy_preserving_protocol != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_privacy_preserving_protocol_tm_secret_sharing_schemes, axiom,
    tm_privacy_preserving_protocol != tm_secret_sharing_schemes).

fof(bg_dist_tm_privacy_preserving_protocol_tm_secure_multi_party_computation, axiom,
    tm_privacy_preserving_protocol != tm_secure_multi_party_computation).

fof(bg_dist_tm_privacy_preserving_protocol_tm_security_method, axiom,
    tm_privacy_preserving_protocol != tm_security_method).

fof(bg_dist_tm_privacy_preserving_protocol_tm_single_sign_on, axiom,
    tm_privacy_preserving_protocol != tm_single_sign_on).

fof(bg_dist_tm_privacy_preserving_protocol_tm_symmetric_cryptography, axiom,
    tm_privacy_preserving_protocol != tm_symmetric_cryptography).

fof(bg_dist_tm_privacy_preserving_protocol_tm_symmetric_encryption, axiom,
    tm_privacy_preserving_protocol != tm_symmetric_encryption).

fof(bg_dist_tm_privacy_preserving_protocol_tm_technical_measure, axiom,
    tm_privacy_preserving_protocol != tm_technical_measure).

fof(bg_dist_tm_privacy_preserving_protocol_tm_technical_organisational_measure, axiom,
    tm_privacy_preserving_protocol != tm_technical_organisational_measure).

fof(bg_dist_tm_privacy_preserving_protocol_tm_trusted_computing, axiom,
    tm_privacy_preserving_protocol != tm_trusted_computing).

fof(bg_dist_tm_privacy_preserving_protocol_tm_trusted_execution_environment, axiom,
    tm_privacy_preserving_protocol != tm_trusted_execution_environment).

fof(bg_dist_tm_privacy_preserving_protocol_tm_usage_control, axiom,
    tm_privacy_preserving_protocol != tm_usage_control).

fof(bg_dist_tm_privacy_preserving_protocol_tm_use_synthetic_data, axiom,
    tm_privacy_preserving_protocol != tm_use_synthetic_data).

fof(bg_dist_tm_privacy_preserving_protocol_tm_virtualisation_security, axiom,
    tm_privacy_preserving_protocol != tm_virtualisation_security).

fof(bg_dist_tm_privacy_preserving_protocol_tm_vulnerability_testing_methods, axiom,
    tm_privacy_preserving_protocol != tm_vulnerability_testing_methods).

fof(bg_dist_tm_privacy_preserving_protocol_tm_web_browser_security, axiom,
    tm_privacy_preserving_protocol != tm_web_browser_security).

fof(bg_dist_tm_privacy_preserving_protocol_tm_web_security_protocols, axiom,
    tm_privacy_preserving_protocol != tm_web_security_protocols).

fof(bg_dist_tm_privacy_preserving_protocol_tm_wireless_security_protocols, axiom,
    tm_privacy_preserving_protocol != tm_wireless_security_protocols).

fof(bg_dist_tm_privacy_preserving_protocol_tm_zero_knowledge_authentication, axiom,
    tm_privacy_preserving_protocol != tm_zero_knowledge_authentication).

fof(bg_dist_tm_private_information_retrieval_tm_pseudonymisation, axiom,
    tm_private_information_retrieval != tm_pseudonymisation).

fof(bg_dist_tm_private_information_retrieval_tm_quantum_cryptography, axiom,
    tm_private_information_retrieval != tm_quantum_cryptography).

fof(bg_dist_tm_private_information_retrieval_tm_r_n_g_pseudonymisation, axiom,
    tm_private_information_retrieval != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_private_information_retrieval_tm_secret_sharing_schemes, axiom,
    tm_private_information_retrieval != tm_secret_sharing_schemes).

fof(bg_dist_tm_private_information_retrieval_tm_secure_multi_party_computation, axiom,
    tm_private_information_retrieval != tm_secure_multi_party_computation).

fof(bg_dist_tm_private_information_retrieval_tm_security_method, axiom,
    tm_private_information_retrieval != tm_security_method).

fof(bg_dist_tm_private_information_retrieval_tm_single_sign_on, axiom,
    tm_private_information_retrieval != tm_single_sign_on).

fof(bg_dist_tm_private_information_retrieval_tm_symmetric_cryptography, axiom,
    tm_private_information_retrieval != tm_symmetric_cryptography).

fof(bg_dist_tm_private_information_retrieval_tm_symmetric_encryption, axiom,
    tm_private_information_retrieval != tm_symmetric_encryption).

fof(bg_dist_tm_private_information_retrieval_tm_technical_measure, axiom,
    tm_private_information_retrieval != tm_technical_measure).

fof(bg_dist_tm_private_information_retrieval_tm_technical_organisational_measure, axiom,
    tm_private_information_retrieval != tm_technical_organisational_measure).

fof(bg_dist_tm_private_information_retrieval_tm_trusted_computing, axiom,
    tm_private_information_retrieval != tm_trusted_computing).

fof(bg_dist_tm_private_information_retrieval_tm_trusted_execution_environment, axiom,
    tm_private_information_retrieval != tm_trusted_execution_environment).

fof(bg_dist_tm_private_information_retrieval_tm_usage_control, axiom,
    tm_private_information_retrieval != tm_usage_control).

fof(bg_dist_tm_private_information_retrieval_tm_use_synthetic_data, axiom,
    tm_private_information_retrieval != tm_use_synthetic_data).

fof(bg_dist_tm_private_information_retrieval_tm_virtualisation_security, axiom,
    tm_private_information_retrieval != tm_virtualisation_security).

fof(bg_dist_tm_private_information_retrieval_tm_vulnerability_testing_methods, axiom,
    tm_private_information_retrieval != tm_vulnerability_testing_methods).

fof(bg_dist_tm_private_information_retrieval_tm_web_browser_security, axiom,
    tm_private_information_retrieval != tm_web_browser_security).

fof(bg_dist_tm_private_information_retrieval_tm_web_security_protocols, axiom,
    tm_private_information_retrieval != tm_web_security_protocols).

fof(bg_dist_tm_private_information_retrieval_tm_wireless_security_protocols, axiom,
    tm_private_information_retrieval != tm_wireless_security_protocols).

fof(bg_dist_tm_private_information_retrieval_tm_zero_knowledge_authentication, axiom,
    tm_private_information_retrieval != tm_zero_knowledge_authentication).

fof(bg_dist_tm_pseudonymisation_tm_quantum_cryptography, axiom,
    tm_pseudonymisation != tm_quantum_cryptography).

fof(bg_dist_tm_pseudonymisation_tm_r_n_g_pseudonymisation, axiom,
    tm_pseudonymisation != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_pseudonymisation_tm_secret_sharing_schemes, axiom,
    tm_pseudonymisation != tm_secret_sharing_schemes).

fof(bg_dist_tm_pseudonymisation_tm_secure_multi_party_computation, axiom,
    tm_pseudonymisation != tm_secure_multi_party_computation).

fof(bg_dist_tm_pseudonymisation_tm_security_method, axiom,
    tm_pseudonymisation != tm_security_method).

fof(bg_dist_tm_pseudonymisation_tm_single_sign_on, axiom,
    tm_pseudonymisation != tm_single_sign_on).

fof(bg_dist_tm_pseudonymisation_tm_symmetric_cryptography, axiom,
    tm_pseudonymisation != tm_symmetric_cryptography).

fof(bg_dist_tm_pseudonymisation_tm_symmetric_encryption, axiom,
    tm_pseudonymisation != tm_symmetric_encryption).

fof(bg_dist_tm_pseudonymisation_tm_technical_measure, axiom,
    tm_pseudonymisation != tm_technical_measure).

fof(bg_dist_tm_pseudonymisation_tm_technical_organisational_measure, axiom,
    tm_pseudonymisation != tm_technical_organisational_measure).

fof(bg_dist_tm_pseudonymisation_tm_trusted_computing, axiom,
    tm_pseudonymisation != tm_trusted_computing).

fof(bg_dist_tm_pseudonymisation_tm_trusted_execution_environment, axiom,
    tm_pseudonymisation != tm_trusted_execution_environment).

fof(bg_dist_tm_pseudonymisation_tm_usage_control, axiom,
    tm_pseudonymisation != tm_usage_control).

fof(bg_dist_tm_pseudonymisation_tm_use_synthetic_data, axiom,
    tm_pseudonymisation != tm_use_synthetic_data).

fof(bg_dist_tm_pseudonymisation_tm_virtualisation_security, axiom,
    tm_pseudonymisation != tm_virtualisation_security).

fof(bg_dist_tm_pseudonymisation_tm_vulnerability_testing_methods, axiom,
    tm_pseudonymisation != tm_vulnerability_testing_methods).

fof(bg_dist_tm_pseudonymisation_tm_web_browser_security, axiom,
    tm_pseudonymisation != tm_web_browser_security).

fof(bg_dist_tm_pseudonymisation_tm_web_security_protocols, axiom,
    tm_pseudonymisation != tm_web_security_protocols).

fof(bg_dist_tm_pseudonymisation_tm_wireless_security_protocols, axiom,
    tm_pseudonymisation != tm_wireless_security_protocols).

fof(bg_dist_tm_pseudonymisation_tm_zero_knowledge_authentication, axiom,
    tm_pseudonymisation != tm_zero_knowledge_authentication).

fof(bg_dist_tm_quantum_cryptography_tm_r_n_g_pseudonymisation, axiom,
    tm_quantum_cryptography != tm_r_n_g_pseudonymisation).

fof(bg_dist_tm_quantum_cryptography_tm_secret_sharing_schemes, axiom,
    tm_quantum_cryptography != tm_secret_sharing_schemes).

fof(bg_dist_tm_quantum_cryptography_tm_secure_multi_party_computation, axiom,
    tm_quantum_cryptography != tm_secure_multi_party_computation).

fof(bg_dist_tm_quantum_cryptography_tm_security_method, axiom,
    tm_quantum_cryptography != tm_security_method).

fof(bg_dist_tm_quantum_cryptography_tm_single_sign_on, axiom,
    tm_quantum_cryptography != tm_single_sign_on).

fof(bg_dist_tm_quantum_cryptography_tm_symmetric_cryptography, axiom,
    tm_quantum_cryptography != tm_symmetric_cryptography).

fof(bg_dist_tm_quantum_cryptography_tm_symmetric_encryption, axiom,
    tm_quantum_cryptography != tm_symmetric_encryption).

fof(bg_dist_tm_quantum_cryptography_tm_technical_measure, axiom,
    tm_quantum_cryptography != tm_technical_measure).

fof(bg_dist_tm_quantum_cryptography_tm_technical_organisational_measure, axiom,
    tm_quantum_cryptography != tm_technical_organisational_measure).

fof(bg_dist_tm_quantum_cryptography_tm_trusted_computing, axiom,
    tm_quantum_cryptography != tm_trusted_computing).

fof(bg_dist_tm_quantum_cryptography_tm_trusted_execution_environment, axiom,
    tm_quantum_cryptography != tm_trusted_execution_environment).

fof(bg_dist_tm_quantum_cryptography_tm_usage_control, axiom,
    tm_quantum_cryptography != tm_usage_control).

fof(bg_dist_tm_quantum_cryptography_tm_use_synthetic_data, axiom,
    tm_quantum_cryptography != tm_use_synthetic_data).

fof(bg_dist_tm_quantum_cryptography_tm_virtualisation_security, axiom,
    tm_quantum_cryptography != tm_virtualisation_security).

fof(bg_dist_tm_quantum_cryptography_tm_vulnerability_testing_methods, axiom,
    tm_quantum_cryptography != tm_vulnerability_testing_methods).

fof(bg_dist_tm_quantum_cryptography_tm_web_browser_security, axiom,
    tm_quantum_cryptography != tm_web_browser_security).

fof(bg_dist_tm_quantum_cryptography_tm_web_security_protocols, axiom,
    tm_quantum_cryptography != tm_web_security_protocols).

fof(bg_dist_tm_quantum_cryptography_tm_wireless_security_protocols, axiom,
    tm_quantum_cryptography != tm_wireless_security_protocols).

fof(bg_dist_tm_quantum_cryptography_tm_zero_knowledge_authentication, axiom,
    tm_quantum_cryptography != tm_zero_knowledge_authentication).

fof(bg_dist_tm_r_n_g_pseudonymisation_tm_secret_sharing_schemes, axiom,
    tm_r_n_g_pseudonymisation != tm_secret_sharing_schemes).

fof(bg_dist_tm_r_n_g_pseudonymisation_tm_secure_multi_party_computation, axiom,
    tm_r_n_g_pseudonymisation != tm_secure_multi_party_computation).

fof(bg_dist_tm_r_n_g_pseudonymisation_tm_security_method, axiom,
    tm_r_n_g_pseudonymisation != tm_security_method).

fof(bg_dist_tm_r_n_g_pseudonymisation_tm_single_sign_on, axiom,
    tm_r_n_g_pseudonymisation != tm_single_sign_on).

fof(bg_dist_tm_r_n_g_pseudonymisation_tm_symmetric_cryptography, axiom,
    tm_r_n_g_pseudonymisation != tm_symmetric_cryptography).

fof(bg_dist_tm_r_n_g_pseudonymisation_tm_symmetric_encryption, axiom,
    tm_r_n_g_pseudonymisation != tm_symmetric_encryption).

fof(bg_dist_tm_r_n_g_pseudonymisation_tm_technical_measure, axiom,
    tm_r_n_g_pseudonymisation != tm_technical_measure).

fof(bg_dist_tm_r_n_g_pseudonymisation_tm_technical_organisational_measure, axiom,
    tm_r_n_g_pseudonymisation != tm_technical_organisational_measure).

fof(bg_dist_tm_r_n_g_pseudonymisation_tm_trusted_computing, axiom,
    tm_r_n_g_pseudonymisation != tm_trusted_computing).

fof(bg_dist_tm_r_n_g_pseudonymisation_tm_trusted_execution_environment, axiom,
    tm_r_n_g_pseudonymisation != tm_trusted_execution_environment).

fof(bg_dist_tm_r_n_g_pseudonymisation_tm_usage_control, axiom,
    tm_r_n_g_pseudonymisation != tm_usage_control).

fof(bg_dist_tm_r_n_g_pseudonymisation_tm_use_synthetic_data, axiom,
    tm_r_n_g_pseudonymisation != tm_use_synthetic_data).

fof(bg_dist_tm_r_n_g_pseudonymisation_tm_virtualisation_security, axiom,
    tm_r_n_g_pseudonymisation != tm_virtualisation_security).

fof(bg_dist_tm_r_n_g_pseudonymisation_tm_vulnerability_testing_methods, axiom,
    tm_r_n_g_pseudonymisation != tm_vulnerability_testing_methods).

fof(bg_dist_tm_r_n_g_pseudonymisation_tm_web_browser_security, axiom,
    tm_r_n_g_pseudonymisation != tm_web_browser_security).

fof(bg_dist_tm_r_n_g_pseudonymisation_tm_web_security_protocols, axiom,
    tm_r_n_g_pseudonymisation != tm_web_security_protocols).

fof(bg_dist_tm_r_n_g_pseudonymisation_tm_wireless_security_protocols, axiom,
    tm_r_n_g_pseudonymisation != tm_wireless_security_protocols).

fof(bg_dist_tm_r_n_g_pseudonymisation_tm_zero_knowledge_authentication, axiom,
    tm_r_n_g_pseudonymisation != tm_zero_knowledge_authentication).

fof(bg_dist_tm_secret_sharing_schemes_tm_secure_multi_party_computation, axiom,
    tm_secret_sharing_schemes != tm_secure_multi_party_computation).

fof(bg_dist_tm_secret_sharing_schemes_tm_security_method, axiom,
    tm_secret_sharing_schemes != tm_security_method).

fof(bg_dist_tm_secret_sharing_schemes_tm_single_sign_on, axiom,
    tm_secret_sharing_schemes != tm_single_sign_on).

fof(bg_dist_tm_secret_sharing_schemes_tm_symmetric_cryptography, axiom,
    tm_secret_sharing_schemes != tm_symmetric_cryptography).

fof(bg_dist_tm_secret_sharing_schemes_tm_symmetric_encryption, axiom,
    tm_secret_sharing_schemes != tm_symmetric_encryption).

fof(bg_dist_tm_secret_sharing_schemes_tm_technical_measure, axiom,
    tm_secret_sharing_schemes != tm_technical_measure).

fof(bg_dist_tm_secret_sharing_schemes_tm_technical_organisational_measure, axiom,
    tm_secret_sharing_schemes != tm_technical_organisational_measure).

fof(bg_dist_tm_secret_sharing_schemes_tm_trusted_computing, axiom,
    tm_secret_sharing_schemes != tm_trusted_computing).

fof(bg_dist_tm_secret_sharing_schemes_tm_trusted_execution_environment, axiom,
    tm_secret_sharing_schemes != tm_trusted_execution_environment).

fof(bg_dist_tm_secret_sharing_schemes_tm_usage_control, axiom,
    tm_secret_sharing_schemes != tm_usage_control).

fof(bg_dist_tm_secret_sharing_schemes_tm_use_synthetic_data, axiom,
    tm_secret_sharing_schemes != tm_use_synthetic_data).

fof(bg_dist_tm_secret_sharing_schemes_tm_virtualisation_security, axiom,
    tm_secret_sharing_schemes != tm_virtualisation_security).

fof(bg_dist_tm_secret_sharing_schemes_tm_vulnerability_testing_methods, axiom,
    tm_secret_sharing_schemes != tm_vulnerability_testing_methods).

fof(bg_dist_tm_secret_sharing_schemes_tm_web_browser_security, axiom,
    tm_secret_sharing_schemes != tm_web_browser_security).

fof(bg_dist_tm_secret_sharing_schemes_tm_web_security_protocols, axiom,
    tm_secret_sharing_schemes != tm_web_security_protocols).

fof(bg_dist_tm_secret_sharing_schemes_tm_wireless_security_protocols, axiom,
    tm_secret_sharing_schemes != tm_wireless_security_protocols).

fof(bg_dist_tm_secret_sharing_schemes_tm_zero_knowledge_authentication, axiom,
    tm_secret_sharing_schemes != tm_zero_knowledge_authentication).

fof(bg_dist_tm_secure_multi_party_computation_tm_security_method, axiom,
    tm_secure_multi_party_computation != tm_security_method).

fof(bg_dist_tm_secure_multi_party_computation_tm_single_sign_on, axiom,
    tm_secure_multi_party_computation != tm_single_sign_on).

fof(bg_dist_tm_secure_multi_party_computation_tm_symmetric_cryptography, axiom,
    tm_secure_multi_party_computation != tm_symmetric_cryptography).

fof(bg_dist_tm_secure_multi_party_computation_tm_symmetric_encryption, axiom,
    tm_secure_multi_party_computation != tm_symmetric_encryption).

fof(bg_dist_tm_secure_multi_party_computation_tm_technical_measure, axiom,
    tm_secure_multi_party_computation != tm_technical_measure).

fof(bg_dist_tm_secure_multi_party_computation_tm_technical_organisational_measure, axiom,
    tm_secure_multi_party_computation != tm_technical_organisational_measure).

fof(bg_dist_tm_secure_multi_party_computation_tm_trusted_computing, axiom,
    tm_secure_multi_party_computation != tm_trusted_computing).

fof(bg_dist_tm_secure_multi_party_computation_tm_trusted_execution_environment, axiom,
    tm_secure_multi_party_computation != tm_trusted_execution_environment).

fof(bg_dist_tm_secure_multi_party_computation_tm_usage_control, axiom,
    tm_secure_multi_party_computation != tm_usage_control).

fof(bg_dist_tm_secure_multi_party_computation_tm_use_synthetic_data, axiom,
    tm_secure_multi_party_computation != tm_use_synthetic_data).

fof(bg_dist_tm_secure_multi_party_computation_tm_virtualisation_security, axiom,
    tm_secure_multi_party_computation != tm_virtualisation_security).

fof(bg_dist_tm_secure_multi_party_computation_tm_vulnerability_testing_methods, axiom,
    tm_secure_multi_party_computation != tm_vulnerability_testing_methods).

fof(bg_dist_tm_secure_multi_party_computation_tm_web_browser_security, axiom,
    tm_secure_multi_party_computation != tm_web_browser_security).

fof(bg_dist_tm_secure_multi_party_computation_tm_web_security_protocols, axiom,
    tm_secure_multi_party_computation != tm_web_security_protocols).

fof(bg_dist_tm_secure_multi_party_computation_tm_wireless_security_protocols, axiom,
    tm_secure_multi_party_computation != tm_wireless_security_protocols).

fof(bg_dist_tm_secure_multi_party_computation_tm_zero_knowledge_authentication, axiom,
    tm_secure_multi_party_computation != tm_zero_knowledge_authentication).

fof(bg_dist_tm_security_method_tm_single_sign_on, axiom,
    tm_security_method != tm_single_sign_on).

fof(bg_dist_tm_security_method_tm_symmetric_cryptography, axiom,
    tm_security_method != tm_symmetric_cryptography).

fof(bg_dist_tm_security_method_tm_symmetric_encryption, axiom,
    tm_security_method != tm_symmetric_encryption).

fof(bg_dist_tm_security_method_tm_technical_measure, axiom,
    tm_security_method != tm_technical_measure).

fof(bg_dist_tm_security_method_tm_technical_organisational_measure, axiom,
    tm_security_method != tm_technical_organisational_measure).

fof(bg_dist_tm_security_method_tm_trusted_computing, axiom,
    tm_security_method != tm_trusted_computing).

fof(bg_dist_tm_security_method_tm_trusted_execution_environment, axiom,
    tm_security_method != tm_trusted_execution_environment).

fof(bg_dist_tm_security_method_tm_usage_control, axiom,
    tm_security_method != tm_usage_control).

fof(bg_dist_tm_security_method_tm_use_synthetic_data, axiom,
    tm_security_method != tm_use_synthetic_data).

fof(bg_dist_tm_security_method_tm_virtualisation_security, axiom,
    tm_security_method != tm_virtualisation_security).

fof(bg_dist_tm_security_method_tm_vulnerability_testing_methods, axiom,
    tm_security_method != tm_vulnerability_testing_methods).

fof(bg_dist_tm_security_method_tm_web_browser_security, axiom,
    tm_security_method != tm_web_browser_security).

fof(bg_dist_tm_security_method_tm_web_security_protocols, axiom,
    tm_security_method != tm_web_security_protocols).

fof(bg_dist_tm_security_method_tm_wireless_security_protocols, axiom,
    tm_security_method != tm_wireless_security_protocols).

fof(bg_dist_tm_security_method_tm_zero_knowledge_authentication, axiom,
    tm_security_method != tm_zero_knowledge_authentication).

fof(bg_dist_tm_single_sign_on_tm_symmetric_cryptography, axiom,
    tm_single_sign_on != tm_symmetric_cryptography).

fof(bg_dist_tm_single_sign_on_tm_symmetric_encryption, axiom,
    tm_single_sign_on != tm_symmetric_encryption).

fof(bg_dist_tm_single_sign_on_tm_technical_measure, axiom,
    tm_single_sign_on != tm_technical_measure).

fof(bg_dist_tm_single_sign_on_tm_technical_organisational_measure, axiom,
    tm_single_sign_on != tm_technical_organisational_measure).

fof(bg_dist_tm_single_sign_on_tm_trusted_computing, axiom,
    tm_single_sign_on != tm_trusted_computing).

fof(bg_dist_tm_single_sign_on_tm_trusted_execution_environment, axiom,
    tm_single_sign_on != tm_trusted_execution_environment).

fof(bg_dist_tm_single_sign_on_tm_usage_control, axiom,
    tm_single_sign_on != tm_usage_control).

fof(bg_dist_tm_single_sign_on_tm_use_synthetic_data, axiom,
    tm_single_sign_on != tm_use_synthetic_data).

fof(bg_dist_tm_single_sign_on_tm_virtualisation_security, axiom,
    tm_single_sign_on != tm_virtualisation_security).

fof(bg_dist_tm_single_sign_on_tm_vulnerability_testing_methods, axiom,
    tm_single_sign_on != tm_vulnerability_testing_methods).

fof(bg_dist_tm_single_sign_on_tm_web_browser_security, axiom,
    tm_single_sign_on != tm_web_browser_security).

fof(bg_dist_tm_single_sign_on_tm_web_security_protocols, axiom,
    tm_single_sign_on != tm_web_security_protocols).

fof(bg_dist_tm_single_sign_on_tm_wireless_security_protocols, axiom,
    tm_single_sign_on != tm_wireless_security_protocols).

fof(bg_dist_tm_single_sign_on_tm_zero_knowledge_authentication, axiom,
    tm_single_sign_on != tm_zero_knowledge_authentication).

fof(bg_dist_tm_symmetric_cryptography_tm_symmetric_encryption, axiom,
    tm_symmetric_cryptography != tm_symmetric_encryption).

fof(bg_dist_tm_symmetric_cryptography_tm_technical_measure, axiom,
    tm_symmetric_cryptography != tm_technical_measure).

fof(bg_dist_tm_symmetric_cryptography_tm_technical_organisational_measure, axiom,
    tm_symmetric_cryptography != tm_technical_organisational_measure).

fof(bg_dist_tm_symmetric_cryptography_tm_trusted_computing, axiom,
    tm_symmetric_cryptography != tm_trusted_computing).

fof(bg_dist_tm_symmetric_cryptography_tm_trusted_execution_environment, axiom,
    tm_symmetric_cryptography != tm_trusted_execution_environment).

fof(bg_dist_tm_symmetric_cryptography_tm_usage_control, axiom,
    tm_symmetric_cryptography != tm_usage_control).

fof(bg_dist_tm_symmetric_cryptography_tm_use_synthetic_data, axiom,
    tm_symmetric_cryptography != tm_use_synthetic_data).

fof(bg_dist_tm_symmetric_cryptography_tm_virtualisation_security, axiom,
    tm_symmetric_cryptography != tm_virtualisation_security).

fof(bg_dist_tm_symmetric_cryptography_tm_vulnerability_testing_methods, axiom,
    tm_symmetric_cryptography != tm_vulnerability_testing_methods).

fof(bg_dist_tm_symmetric_cryptography_tm_web_browser_security, axiom,
    tm_symmetric_cryptography != tm_web_browser_security).

fof(bg_dist_tm_symmetric_cryptography_tm_web_security_protocols, axiom,
    tm_symmetric_cryptography != tm_web_security_protocols).

fof(bg_dist_tm_symmetric_cryptography_tm_wireless_security_protocols, axiom,
    tm_symmetric_cryptography != tm_wireless_security_protocols).

fof(bg_dist_tm_symmetric_cryptography_tm_zero_knowledge_authentication, axiom,
    tm_symmetric_cryptography != tm_zero_knowledge_authentication).

fof(bg_dist_tm_symmetric_encryption_tm_technical_measure, axiom,
    tm_symmetric_encryption != tm_technical_measure).

fof(bg_dist_tm_symmetric_encryption_tm_technical_organisational_measure, axiom,
    tm_symmetric_encryption != tm_technical_organisational_measure).

fof(bg_dist_tm_symmetric_encryption_tm_trusted_computing, axiom,
    tm_symmetric_encryption != tm_trusted_computing).

fof(bg_dist_tm_symmetric_encryption_tm_trusted_execution_environment, axiom,
    tm_symmetric_encryption != tm_trusted_execution_environment).

fof(bg_dist_tm_symmetric_encryption_tm_usage_control, axiom,
    tm_symmetric_encryption != tm_usage_control).

fof(bg_dist_tm_symmetric_encryption_tm_use_synthetic_data, axiom,
    tm_symmetric_encryption != tm_use_synthetic_data).

fof(bg_dist_tm_symmetric_encryption_tm_virtualisation_security, axiom,
    tm_symmetric_encryption != tm_virtualisation_security).

fof(bg_dist_tm_symmetric_encryption_tm_vulnerability_testing_methods, axiom,
    tm_symmetric_encryption != tm_vulnerability_testing_methods).

fof(bg_dist_tm_symmetric_encryption_tm_web_browser_security, axiom,
    tm_symmetric_encryption != tm_web_browser_security).

fof(bg_dist_tm_symmetric_encryption_tm_web_security_protocols, axiom,
    tm_symmetric_encryption != tm_web_security_protocols).

fof(bg_dist_tm_symmetric_encryption_tm_wireless_security_protocols, axiom,
    tm_symmetric_encryption != tm_wireless_security_protocols).

fof(bg_dist_tm_symmetric_encryption_tm_zero_knowledge_authentication, axiom,
    tm_symmetric_encryption != tm_zero_knowledge_authentication).

fof(bg_dist_tm_technical_measure_tm_technical_organisational_measure, axiom,
    tm_technical_measure != tm_technical_organisational_measure).

fof(bg_dist_tm_technical_measure_tm_trusted_computing, axiom,
    tm_technical_measure != tm_trusted_computing).

fof(bg_dist_tm_technical_measure_tm_trusted_execution_environment, axiom,
    tm_technical_measure != tm_trusted_execution_environment).

fof(bg_dist_tm_technical_measure_tm_usage_control, axiom,
    tm_technical_measure != tm_usage_control).

fof(bg_dist_tm_technical_measure_tm_use_synthetic_data, axiom,
    tm_technical_measure != tm_use_synthetic_data).

fof(bg_dist_tm_technical_measure_tm_virtualisation_security, axiom,
    tm_technical_measure != tm_virtualisation_security).

fof(bg_dist_tm_technical_measure_tm_vulnerability_testing_methods, axiom,
    tm_technical_measure != tm_vulnerability_testing_methods).

fof(bg_dist_tm_technical_measure_tm_web_browser_security, axiom,
    tm_technical_measure != tm_web_browser_security).

fof(bg_dist_tm_technical_measure_tm_web_security_protocols, axiom,
    tm_technical_measure != tm_web_security_protocols).

fof(bg_dist_tm_technical_measure_tm_wireless_security_protocols, axiom,
    tm_technical_measure != tm_wireless_security_protocols).

fof(bg_dist_tm_technical_measure_tm_zero_knowledge_authentication, axiom,
    tm_technical_measure != tm_zero_knowledge_authentication).

fof(bg_dist_tm_technical_organisational_measure_tm_trusted_computing, axiom,
    tm_technical_organisational_measure != tm_trusted_computing).

fof(bg_dist_tm_technical_organisational_measure_tm_trusted_execution_environment, axiom,
    tm_technical_organisational_measure != tm_trusted_execution_environment).

fof(bg_dist_tm_technical_organisational_measure_tm_usage_control, axiom,
    tm_technical_organisational_measure != tm_usage_control).

fof(bg_dist_tm_technical_organisational_measure_tm_use_synthetic_data, axiom,
    tm_technical_organisational_measure != tm_use_synthetic_data).

fof(bg_dist_tm_technical_organisational_measure_tm_virtualisation_security, axiom,
    tm_technical_organisational_measure != tm_virtualisation_security).

fof(bg_dist_tm_technical_organisational_measure_tm_vulnerability_testing_methods, axiom,
    tm_technical_organisational_measure != tm_vulnerability_testing_methods).

fof(bg_dist_tm_technical_organisational_measure_tm_web_browser_security, axiom,
    tm_technical_organisational_measure != tm_web_browser_security).

fof(bg_dist_tm_technical_organisational_measure_tm_web_security_protocols, axiom,
    tm_technical_organisational_measure != tm_web_security_protocols).

fof(bg_dist_tm_technical_organisational_measure_tm_wireless_security_protocols, axiom,
    tm_technical_organisational_measure != tm_wireless_security_protocols).

fof(bg_dist_tm_technical_organisational_measure_tm_zero_knowledge_authentication, axiom,
    tm_technical_organisational_measure != tm_zero_knowledge_authentication).

fof(bg_dist_tm_trusted_computing_tm_trusted_execution_environment, axiom,
    tm_trusted_computing != tm_trusted_execution_environment).

fof(bg_dist_tm_trusted_computing_tm_usage_control, axiom,
    tm_trusted_computing != tm_usage_control).

fof(bg_dist_tm_trusted_computing_tm_use_synthetic_data, axiom,
    tm_trusted_computing != tm_use_synthetic_data).

fof(bg_dist_tm_trusted_computing_tm_virtualisation_security, axiom,
    tm_trusted_computing != tm_virtualisation_security).

fof(bg_dist_tm_trusted_computing_tm_vulnerability_testing_methods, axiom,
    tm_trusted_computing != tm_vulnerability_testing_methods).

fof(bg_dist_tm_trusted_computing_tm_web_browser_security, axiom,
    tm_trusted_computing != tm_web_browser_security).

fof(bg_dist_tm_trusted_computing_tm_web_security_protocols, axiom,
    tm_trusted_computing != tm_web_security_protocols).

fof(bg_dist_tm_trusted_computing_tm_wireless_security_protocols, axiom,
    tm_trusted_computing != tm_wireless_security_protocols).

fof(bg_dist_tm_trusted_computing_tm_zero_knowledge_authentication, axiom,
    tm_trusted_computing != tm_zero_knowledge_authentication).

fof(bg_dist_tm_trusted_execution_environment_tm_usage_control, axiom,
    tm_trusted_execution_environment != tm_usage_control).

fof(bg_dist_tm_trusted_execution_environment_tm_use_synthetic_data, axiom,
    tm_trusted_execution_environment != tm_use_synthetic_data).

fof(bg_dist_tm_trusted_execution_environment_tm_virtualisation_security, axiom,
    tm_trusted_execution_environment != tm_virtualisation_security).

fof(bg_dist_tm_trusted_execution_environment_tm_vulnerability_testing_methods, axiom,
    tm_trusted_execution_environment != tm_vulnerability_testing_methods).

fof(bg_dist_tm_trusted_execution_environment_tm_web_browser_security, axiom,
    tm_trusted_execution_environment != tm_web_browser_security).

fof(bg_dist_tm_trusted_execution_environment_tm_web_security_protocols, axiom,
    tm_trusted_execution_environment != tm_web_security_protocols).

fof(bg_dist_tm_trusted_execution_environment_tm_wireless_security_protocols, axiom,
    tm_trusted_execution_environment != tm_wireless_security_protocols).

fof(bg_dist_tm_trusted_execution_environment_tm_zero_knowledge_authentication, axiom,
    tm_trusted_execution_environment != tm_zero_knowledge_authentication).

fof(bg_dist_tm_usage_control_tm_use_synthetic_data, axiom,
    tm_usage_control != tm_use_synthetic_data).

fof(bg_dist_tm_usage_control_tm_virtualisation_security, axiom,
    tm_usage_control != tm_virtualisation_security).

fof(bg_dist_tm_usage_control_tm_vulnerability_testing_methods, axiom,
    tm_usage_control != tm_vulnerability_testing_methods).

fof(bg_dist_tm_usage_control_tm_web_browser_security, axiom,
    tm_usage_control != tm_web_browser_security).

fof(bg_dist_tm_usage_control_tm_web_security_protocols, axiom,
    tm_usage_control != tm_web_security_protocols).

fof(bg_dist_tm_usage_control_tm_wireless_security_protocols, axiom,
    tm_usage_control != tm_wireless_security_protocols).

fof(bg_dist_tm_usage_control_tm_zero_knowledge_authentication, axiom,
    tm_usage_control != tm_zero_knowledge_authentication).

fof(bg_dist_tm_use_synthetic_data_tm_virtualisation_security, axiom,
    tm_use_synthetic_data != tm_virtualisation_security).

fof(bg_dist_tm_use_synthetic_data_tm_vulnerability_testing_methods, axiom,
    tm_use_synthetic_data != tm_vulnerability_testing_methods).

fof(bg_dist_tm_use_synthetic_data_tm_web_browser_security, axiom,
    tm_use_synthetic_data != tm_web_browser_security).

fof(bg_dist_tm_use_synthetic_data_tm_web_security_protocols, axiom,
    tm_use_synthetic_data != tm_web_security_protocols).

fof(bg_dist_tm_use_synthetic_data_tm_wireless_security_protocols, axiom,
    tm_use_synthetic_data != tm_wireless_security_protocols).

fof(bg_dist_tm_use_synthetic_data_tm_zero_knowledge_authentication, axiom,
    tm_use_synthetic_data != tm_zero_knowledge_authentication).

fof(bg_dist_tm_virtualisation_security_tm_vulnerability_testing_methods, axiom,
    tm_virtualisation_security != tm_vulnerability_testing_methods).

fof(bg_dist_tm_virtualisation_security_tm_web_browser_security, axiom,
    tm_virtualisation_security != tm_web_browser_security).

fof(bg_dist_tm_virtualisation_security_tm_web_security_protocols, axiom,
    tm_virtualisation_security != tm_web_security_protocols).

fof(bg_dist_tm_virtualisation_security_tm_wireless_security_protocols, axiom,
    tm_virtualisation_security != tm_wireless_security_protocols).

fof(bg_dist_tm_virtualisation_security_tm_zero_knowledge_authentication, axiom,
    tm_virtualisation_security != tm_zero_knowledge_authentication).

fof(bg_dist_tm_vulnerability_testing_methods_tm_web_browser_security, axiom,
    tm_vulnerability_testing_methods != tm_web_browser_security).

fof(bg_dist_tm_vulnerability_testing_methods_tm_web_security_protocols, axiom,
    tm_vulnerability_testing_methods != tm_web_security_protocols).

fof(bg_dist_tm_vulnerability_testing_methods_tm_wireless_security_protocols, axiom,
    tm_vulnerability_testing_methods != tm_wireless_security_protocols).

fof(bg_dist_tm_vulnerability_testing_methods_tm_zero_knowledge_authentication, axiom,
    tm_vulnerability_testing_methods != tm_zero_knowledge_authentication).

fof(bg_dist_tm_web_browser_security_tm_web_security_protocols, axiom,
    tm_web_browser_security != tm_web_security_protocols).

fof(bg_dist_tm_web_browser_security_tm_wireless_security_protocols, axiom,
    tm_web_browser_security != tm_wireless_security_protocols).

fof(bg_dist_tm_web_browser_security_tm_zero_knowledge_authentication, axiom,
    tm_web_browser_security != tm_zero_knowledge_authentication).

fof(bg_dist_tm_web_security_protocols_tm_wireless_security_protocols, axiom,
    tm_web_security_protocols != tm_wireless_security_protocols).

fof(bg_dist_tm_web_security_protocols_tm_zero_knowledge_authentication, axiom,
    tm_web_security_protocols != tm_zero_knowledge_authentication).

fof(bg_dist_tm_wireless_security_protocols_tm_zero_knowledge_authentication, axiom,
    tm_wireless_security_protocols != tm_zero_knowledge_authentication).

fof(w_kgc366, axiom,
    ~ ( ( ( tm_encryption = tm_encryption_at_rest
    | tm_access_control_method = tm_encryption_at_rest
    | tm_encryption_at_rest = tm_encryption
    | tm_encryption_at_rest = tm_access_control_method
    | ( tm_activity_monitoring = tm_encryption_at_rest & ( tm_activity_monitoring = tm_encryption
    | tm_activity_monitoring = tm_access_control_method ) )
    | ( tm_anonymisation = tm_encryption_at_rest & ( tm_anonymisation = tm_encryption
    | tm_anonymisation = tm_access_control_method ) )
    | ( tm_asymmetric_cryptography = tm_encryption_at_rest & ( tm_asymmetric_cryptography = tm_encryption
    | tm_asymmetric_cryptography = tm_access_control_method ) )
    | ( tm_asymmetric_encryption = tm_encryption_at_rest & ( tm_asymmetric_encryption = tm_encryption
    | tm_asymmetric_encryption = tm_access_control_method ) )
    | ( tm_authentication_a_b_c = tm_encryption_at_rest & ( tm_authentication_a_b_c = tm_encryption
    | tm_authentication_a_b_c = tm_access_control_method ) )
    | ( tm_authentication_p_a_b_c = tm_encryption_at_rest & ( tm_authentication_p_a_b_c = tm_encryption
    | tm_authentication_p_a_b_c = tm_access_control_method ) )
    | ( tm_authentication_protocols = tm_encryption_at_rest & ( tm_authentication_protocols = tm_encryption
    | tm_authentication_protocols = tm_access_control_method ) )
    | ( tm_authorisation_protocols = tm_encryption_at_rest & ( tm_authorisation_protocols = tm_encryption
    | tm_authorisation_protocols = tm_access_control_method ) )
    | ( tm_biometric_authentication = tm_encryption_at_rest & ( tm_biometric_authentication = tm_encryption
    | tm_biometric_authentication = tm_access_control_method ) )
    | ( tm_cryptographic_authentication = tm_encryption_at_rest & ( tm_cryptographic_authentication = tm_encryption
    | tm_cryptographic_authentication = tm_access_control_method ) )
    | ( tm_cryptographic_key_management = tm_encryption_at_rest & ( tm_cryptographic_key_management = tm_encryption
    | tm_cryptographic_key_management = tm_access_control_method ) )
    | ( tm_cryptographic_methods = tm_encryption_at_rest & ( tm_cryptographic_methods = tm_encryption
    | tm_cryptographic_methods = tm_access_control_method ) )
    | ( tm_data_backup_protocols = tm_encryption_at_rest & ( tm_data_backup_protocols = tm_encryption
    | tm_data_backup_protocols = tm_access_control_method ) )
    | ( tm_data_redaction = tm_encryption_at_rest & ( tm_data_redaction = tm_encryption
    | tm_data_redaction = tm_access_control_method ) )
    | ( tm_data_sanitisation_technique = tm_encryption_at_rest & ( tm_data_sanitisation_technique = tm_encryption
    | tm_data_sanitisation_technique = tm_access_control_method ) )
    | ( tm_deidentification = tm_encryption_at_rest & ( tm_deidentification = tm_encryption
    | tm_deidentification = tm_access_control_method ) )
    | ( tm_deterministic_pseudonymisation = tm_encryption_at_rest & ( tm_deterministic_pseudonymisation = tm_encryption
    | tm_deterministic_pseudonymisation = tm_access_control_method ) )
    | ( tm_differential_privacy = tm_encryption_at_rest & ( tm_differential_privacy = tm_encryption
    | tm_differential_privacy = tm_access_control_method ) )
    | ( tm_digital_rights_management = tm_encryption_at_rest & ( tm_digital_rights_management = tm_encryption
    | tm_digital_rights_management = tm_access_control_method ) )
    | ( tm_digital_signatures = tm_encryption_at_rest & ( tm_digital_signatures = tm_encryption
    | tm_digital_signatures = tm_access_control_method ) )
    | ( tm_distributed_system_security = tm_encryption_at_rest & ( tm_distributed_system_security = tm_encryption
    | tm_distributed_system_security = tm_access_control_method ) )
    | ( tm_document_randomised_pseudonymisation = tm_encryption_at_rest & ( tm_document_randomised_pseudonymisation = tm_encryption
    | tm_document_randomised_pseudonymisation = tm_access_control_method ) )
    | ( tm_document_security = tm_encryption_at_rest & ( tm_document_security = tm_encryption
    | tm_document_security = tm_access_control_method ) )
    | ( tm_encryption_in_transfer = tm_encryption_at_rest & ( tm_encryption_in_transfer = tm_encryption
    | tm_encryption_in_transfer = tm_access_control_method ) )
    | ( tm_encryption_in_use = tm_encryption_at_rest & ( tm_encryption_in_use = tm_encryption
    | tm_encryption_in_use = tm_access_control_method ) )
    | ( tm_end_to_end_encryption = tm_encryption_at_rest & ( tm_end_to_end_encryption = tm_encryption
    | tm_end_to_end_encryption = tm_access_control_method ) )
    | ( tm_fail_safe_protocols = tm_encryption_at_rest & ( tm_fail_safe_protocols = tm_encryption
    | tm_fail_safe_protocols = tm_access_control_method ) )
    | ( tm_file_system_security = tm_encryption_at_rest & ( tm_file_system_security = tm_encryption
    | tm_file_system_security = tm_access_control_method ) )
    | ( tm_fully_randomised_pseudonymisation = tm_encryption_at_rest & ( tm_fully_randomised_pseudonymisation = tm_encryption
    | tm_fully_randomised_pseudonymisation = tm_access_control_method ) )
    | ( tm_hardware_security_protocols = tm_encryption_at_rest & ( tm_hardware_security_protocols = tm_encryption
    | tm_hardware_security_protocols = tm_access_control_method ) )
    | ( tm_hash_functions = tm_encryption_at_rest & ( tm_hash_functions = tm_encryption
    | tm_hash_functions = tm_access_control_method ) )
    | ( tm_hash_message_authentication_code = tm_encryption_at_rest & ( tm_hash_message_authentication_code = tm_encryption
    | tm_hash_message_authentication_code = tm_access_control_method ) )
    | ( tm_homomorphic_encryption = tm_encryption_at_rest & ( tm_homomorphic_encryption = tm_encryption
    | tm_homomorphic_encryption = tm_access_control_method ) )
    | ( tm_information_flow_control = tm_encryption_at_rest & ( tm_information_flow_control = tm_encryption
    | tm_information_flow_control = tm_access_control_method ) )
    | ( tm_intrusion_detection_system = tm_encryption_at_rest & ( tm_intrusion_detection_system = tm_encryption
    | tm_intrusion_detection_system = tm_access_control_method ) )
    | ( tm_legal_measure = tm_encryption_at_rest & ( tm_legal_measure = tm_encryption
    | tm_legal_measure = tm_access_control_method ) )
    | ( tm_message_authentication_codes = tm_encryption_at_rest & ( tm_message_authentication_codes = tm_encryption
    | tm_message_authentication_codes = tm_access_control_method ) )
    | ( tm_mobile_platform_security = tm_encryption_at_rest & ( tm_mobile_platform_security = tm_encryption
    | tm_mobile_platform_security = tm_access_control_method ) )
    | ( tm_monotonic_counter_pseudonymisation = tm_encryption_at_rest & ( tm_monotonic_counter_pseudonymisation = tm_encryption
    | tm_monotonic_counter_pseudonymisation = tm_access_control_method ) )
    | ( tm_multi_factor_authentication = tm_encryption_at_rest & ( tm_multi_factor_authentication = tm_encryption
    | tm_multi_factor_authentication = tm_access_control_method ) )
    | ( tm_network_proxy_routing = tm_encryption_at_rest & ( tm_network_proxy_routing = tm_encryption
    | tm_network_proxy_routing = tm_access_control_method ) )
    | ( tm_network_security_protocols = tm_encryption_at_rest & ( tm_network_security_protocols = tm_encryption
    | tm_network_security_protocols = tm_access_control_method ) )
    | ( tm_operating_system_security = tm_encryption_at_rest & ( tm_operating_system_security = tm_encryption
    | tm_operating_system_security = tm_access_control_method ) )
    | ( tm_organisational_measure = tm_encryption_at_rest & ( tm_organisational_measure = tm_encryption
    | tm_organisational_measure = tm_access_control_method ) )
    | ( tm_password_authentication = tm_encryption_at_rest & ( tm_password_authentication = tm_encryption
    | tm_password_authentication = tm_access_control_method ) )
    | ( tm_penetration_testing_methods = tm_encryption_at_rest & ( tm_penetration_testing_methods = tm_encryption
    | tm_penetration_testing_methods = tm_access_control_method ) )
    | ( tm_physical_measure = tm_encryption_at_rest & ( tm_physical_measure = tm_encryption
    | tm_physical_measure = tm_access_control_method ) )
    | ( tm_post_quantum_cryptography = tm_encryption_at_rest & ( tm_post_quantum_cryptography = tm_encryption
    | tm_post_quantum_cryptography = tm_access_control_method ) )
    | ( tm_privacy_preserving_protocol = tm_encryption_at_rest & ( tm_privacy_preserving_protocol = tm_encryption
    | tm_privacy_preserving_protocol = tm_access_control_method ) )
    | ( tm_private_information_retrieval = tm_encryption_at_rest & ( tm_private_information_retrieval = tm_encryption
    | tm_private_information_retrieval = tm_access_control_method ) )
    | ( tm_pseudonymisation = tm_encryption_at_rest & ( tm_pseudonymisation = tm_encryption
    | tm_pseudonymisation = tm_access_control_method ) )
    | ( tm_quantum_cryptography = tm_encryption_at_rest & ( tm_quantum_cryptography = tm_encryption
    | tm_quantum_cryptography = tm_access_control_method ) )
    | ( tm_r_n_g_pseudonymisation = tm_encryption_at_rest & ( tm_r_n_g_pseudonymisation = tm_encryption
    | tm_r_n_g_pseudonymisation = tm_access_control_method ) )
    | ( tm_secret_sharing_schemes = tm_encryption_at_rest & ( tm_secret_sharing_schemes = tm_encryption
    | tm_secret_sharing_schemes = tm_access_control_method ) )
    | ( tm_secure_multi_party_computation = tm_encryption_at_rest & ( tm_secure_multi_party_computation = tm_encryption
    | tm_secure_multi_party_computation = tm_access_control_method ) )
    | ( tm_security_method = tm_encryption_at_rest & ( tm_security_method = tm_encryption
    | tm_security_method = tm_access_control_method ) )
    | ( tm_single_sign_on = tm_encryption_at_rest & ( tm_single_sign_on = tm_encryption
    | tm_single_sign_on = tm_access_control_method ) )
    | ( tm_symmetric_cryptography = tm_encryption_at_rest & ( tm_symmetric_cryptography = tm_encryption
    | tm_symmetric_cryptography = tm_access_control_method ) )
    | ( tm_symmetric_encryption = tm_encryption_at_rest & ( tm_symmetric_encryption = tm_encryption
    | tm_symmetric_encryption = tm_access_control_method ) )
    | ( tm_technical_measure = tm_encryption_at_rest & ( tm_technical_measure = tm_encryption
    | tm_technical_measure = tm_access_control_method ) ) )
    | ( ( tm_technical_organisational_measure = tm_encryption_at_rest & ( tm_technical_organisational_measure = tm_encryption
    | tm_technical_organisational_measure = tm_access_control_method ) )
    | ( tm_trusted_computing = tm_encryption_at_rest & ( tm_trusted_computing = tm_encryption
    | tm_trusted_computing = tm_access_control_method ) )
    | ( tm_trusted_execution_environment = tm_encryption_at_rest & ( tm_trusted_execution_environment = tm_encryption
    | tm_trusted_execution_environment = tm_access_control_method ) )
    | ( tm_usage_control = tm_encryption_at_rest & ( tm_usage_control = tm_encryption
    | tm_usage_control = tm_access_control_method ) )
    | ( tm_use_synthetic_data = tm_encryption_at_rest & ( tm_use_synthetic_data = tm_encryption
    | tm_use_synthetic_data = tm_access_control_method ) )
    | ( tm_virtualisation_security = tm_encryption_at_rest & ( tm_virtualisation_security = tm_encryption
    | tm_virtualisation_security = tm_access_control_method ) )
    | ( tm_vulnerability_testing_methods = tm_encryption_at_rest & ( tm_vulnerability_testing_methods = tm_encryption
    | tm_vulnerability_testing_methods = tm_access_control_method ) )
    | ( tm_web_browser_security = tm_encryption_at_rest & ( tm_web_browser_security = tm_encryption
    | tm_web_browser_security = tm_access_control_method ) )
    | ( tm_web_security_protocols = tm_encryption_at_rest & ( tm_web_security_protocols = tm_encryption
    | tm_web_security_protocols = tm_access_control_method ) )
    | ( tm_wireless_security_protocols = tm_encryption_at_rest & ( tm_wireless_security_protocols = tm_encryption
    | tm_wireless_security_protocols = tm_access_control_method ) )
    | ( tm_zero_knowledge_authentication = tm_encryption_at_rest & ( tm_zero_knowledge_authentication = tm_encryption
    | tm_zero_knowledge_authentication = tm_access_control_method ) ) ) ) )).
%------------------------------------------------------------------------------
