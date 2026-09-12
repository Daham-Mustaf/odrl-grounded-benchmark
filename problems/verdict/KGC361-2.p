%--------------------------------------------------------------------------
% File     : KGC361-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : measures, isAllOf(Encryption, AccessControlMethod) against isNoneOf(AccessControlMethod) (witness condition negated)
% Version  : 1.0
% English  : A controller requires encryption and access control, while a processor excludes access control.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC361-2.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 2 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-tom.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition negated -------------------------------------------
fof(w_kgc361, axiom,
    ~ ( ( tm_encryption != tm_access_control_method & tm_access_control_method != tm_access_control_method & ( tm_encryption != tm_access_control_method
| tm_access_control_method != tm_access_control_method ) ) )).
%--------------------------------------------------------------------------
