import OdrlGrounded.Grounding
import OdrlGrounded.Examples.Language

set_option autoImplicit false

/-!
# Figure 1, language row, with values

The policy names languages by value. The BCP 47 binding grounds `german` to
`de` and `french` to `fr`. The value `klingon` names no concept of the binding.
-/

namespace OdrlGrounded.Example

inductive LangVal where
  | german
  | french
  | klingon
  deriving DecidableEq, Repr

def langGrounding : LangVal → Option L
  | .german => some de
  | .french => some fr
  | .klingon => none

def langOffer : ConstraintSet LangVal := [.atom (.eq .german)]

/-- The request `french or klingon`. -/
def langRequestBad : ConstraintSet LangVal :=
  [.or [.eq .french, .eq .klingon]]

theorem langRequestBad_ungrounded :
    ConstraintSet.ground langGrounding langRequestBad = none := by
  decide

/-- One ungrounded alternative leaves the whole request without a denotation,
so the verdict is `Unknown`. The grounded offer `eq de` against the request
`eq fr` alone is `Incompatible` under the same declaration
(`language_declared_verdict`). -/
theorem ungrounded_alternative_unknown :
    groundedVerdict langGrounding decl langOffer langRequestBad =
      Verdict.unknown :=
  groundedVerdict_of_right_none langGrounding decl langOffer langRequestBad
    langRequestBad_ungrounded

end OdrlGrounded.Example
