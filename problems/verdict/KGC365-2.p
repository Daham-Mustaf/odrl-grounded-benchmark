%--------------------------------------------------------------------------
% File     : KGC365-2.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : measures, isAllOf {Encryption, AccessControl} against isAllOf {Encryption, AccessControl, Pseudonymisation} (witness condition negated)
% Version  : 1.0
% English  : A controller requires both encryption and access control. A processor commits to encryption, access control and pseudonymisation together.
%
% Refs     : odrl-grounded-benchmark. https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC365-2.p
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
fof(w_kgc365, axiom,
    ~ ( ( $true & $true & $true & $true & $true ) )).
%--------------------------------------------------------------------------
