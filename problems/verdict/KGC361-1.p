%--------------------------------------------------------------------------
% File     : KGC361-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : measures, isAllOf(Encryption, AccessControlMethod) against isNoneOf(AccessControlMethod) (witness condition asserted)
% Version  : 1.0
% English  : The same requirement against a processor that does not apply access control. The requirement needs access control among the measures the use supplies and the exclusion keeps it out, so no structure admits a common use and the verdict is Incompatible.
%           : 
%           : It is definite without any declaration by the parties, which is unlike the legal-basis problems: there an Incompatible verdict needed the parties to declare two concepts distinct, because the question was whether two names denote one thing. Here the two constraints name the same concept and pull against each other over it, so the vocabulary is not consulted and the certificate cites the constraints alone.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC361-1.p
%
% Status   : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/DPV-tom.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition asserted ------------------------------------------
fof(w_kgc361, axiom,
    ( tm_encryption != tm_access_control_method & tm_access_control_method != tm_access_control_method & ( tm_encryption != tm_access_control_method
| tm_access_control_method != tm_access_control_method ) )).
%--------------------------------------------------------------------------
