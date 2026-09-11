%--------------------------------------------------------------------------
% File     : KGC364-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : measures, isAllOf {Encryption, AccessControl} against eq Encryption, declared distinct (witness condition asserted)
% Version  : 1.0
% English  : As KGC363, with encryption and access control declared distinct.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC364-1.p
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
% Background theory: declared distinctness instances, stated in
% the declared theory file and instantiated here.

fof(bg_dist_tm_encryption_tm_access_control_method, axiom,
    tm_encryption != tm_access_control_method).

% --- witness condition asserted ------------------------------------------
fof(w_kgc364, axiom,
    ( tm_encryption = tm_encryption & tm_access_control_method = tm_encryption & ( tm_encryption = tm_encryption
| tm_access_control_method = tm_encryption ) )).
%--------------------------------------------------------------------------
