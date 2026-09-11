%--------------------------------------------------------------------------
% File     : KGC362-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : measures, isAnyOf {Encryption, AccessControl} against eq Encryption (witness condition negated)
% Version  : 1.0
% English  : A provider requires at least one of encryption and access control; a consumer commits to encryption.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC362-2.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-tom.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition negated -------------------------------------------
fof(w_kgc362, axiom,
    ~ ( ( ( tm_encryption = tm_encryption
| tm_access_control_method = tm_encryption ) & ( ( tm_encryption = tm_encryption & ( tm_encryption = tm_encryption
| tm_encryption = tm_access_control_method ) )
| ( tm_access_control_method = tm_encryption & ( tm_access_control_method = tm_encryption
| tm_access_control_method = tm_access_control_method ) ) ) ) )).
%--------------------------------------------------------------------------
