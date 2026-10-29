%--------------------------------------------------------------------------
% File     : KGC366-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : measures, isAnyOf {Encryption, AccessControl} against eq EncryptionAtRest, declared distinct (witness condition asserted)
% Version  : 1.0
% English  : A controller requires at least one of encryption and access control. A processor's policy commits to encryption at rest as the only measure.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC366-1.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-tom.ax').
include('axioms/DPV-tom-declared.ax').

% --- constants, groundings and resource hooks ----------------------------
% Declarations: declared distinctness instances, stated in
% the declarations file and instantiated here.

fof(bg_dist_tm_encryption_tm_encryption_at_rest, axiom,
    tm_encryption != tm_encryption_at_rest).
fof(bg_dist_tm_access_control_method_tm_encryption_at_rest, axiom,
    tm_access_control_method != tm_encryption_at_rest).

% --- witness condition asserted ------------------------------------------
fof(w_kgc366, axiom,
    ( ( tm_encryption = tm_encryption_at_rest
| tm_access_control_method = tm_encryption_at_rest
| tm_encryption_at_rest = tm_encryption_at_rest ) & ( ( tm_encryption = tm_encryption_at_rest & ( tm_encryption = tm_encryption
| tm_encryption = tm_access_control_method ) )
| ( tm_access_control_method = tm_encryption_at_rest & ( tm_access_control_method = tm_encryption
| tm_access_control_method = tm_access_control_method ) )
| ( tm_encryption_at_rest = tm_encryption_at_rest & ( tm_encryption_at_rest = tm_encryption
| tm_encryption_at_rest = tm_access_control_method ) ) ) )).
%--------------------------------------------------------------------------
