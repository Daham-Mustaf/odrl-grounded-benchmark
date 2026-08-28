%--------------------------------------------------------------------------
% File     : KGC375-1.p
% Domain   : ODRL Policy / Knowledge-Grounded Fragment
% Problem  : language, eq de against neq fr, no declaration (witness condition asserted)
% Version  : 1.0
% English  : KGC374 with the uniqueness rule withdrawn. A structure separating de and fr admits the witness; a structure identifying them admits none, because a use in German is then a use in French. The registry decides neither, so the verdict is Unknown.
%           : 
%           : Read with KGC370 and KGC371 this completes the symmetry: the same withdrawal takes an Incompatible to Unknown there and a Compatible to Unknown here. What the declaration buys is definiteness, not a direction.
%
% Refs     : TODO. A Sorted Semantics for the Knowledge-Grounded Fragment of ODRL.
% Source   : https://github.com/Daham-Mustaf/odrl-grounded-benchmark
% Authors  : Daham Mustafa
% Names    : KGC375-1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : Query 1 of 2.  Verdict is derived from both queries.
%--------------------------------------------------------------------------
include('axioms/KGE000-0.ax').
include('axioms/BCP47000-0.ax').

% --- constants, groundings and resource hooks ----------------------------


% --- witness condition asserted ------------------------------------------
fof(w_kgc375, axiom,
    ( ( bcp_de = bcp_de & bcp_de != bcp_fr )
| ( bcp_fr = bcp_de & bcp_fr != bcp_fr ) )).
%--------------------------------------------------------------------------
