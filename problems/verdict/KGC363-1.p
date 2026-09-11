%--------------------------------------------------------------------------
% File     : KGC363-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : measures, isAllOf {Encryption, AccessControl} against eq Encryption (witness condition asserted)
% Version  : 1.0
% English  : A provider requires both encryption and access control; a consumer commits to encryption only.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC363-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-tom.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition asserted ------------------------------------------
fof(w_kgc363, axiom,
    ( tm_encryption = tm_encryption & tm_access_control_method = tm_encryption & ( tm_encryption = tm_encryption
| tm_access_control_method = tm_encryption ) )).
%--------------------------------------------------------------------------
