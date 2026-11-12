import OdrlGrounded.Grounding
import OdrlGrounded.Examples.Language

set_option autoImplicit false

/-!
# Running example, language row, with values

The policy names languages by value: the values `de` and `fr`, as in Figure 1.
The BCP 47 binding grounds each to the concept of the same name. The value
`klingon` names no concept of the binding.
-/

namespace OdrlGrounded.Example

inductive LangVal where
  | de
  | fr
  | klingon
  deriving DecidableEq, Repr

def langGrounding : LangVal → Option L
  | .de => some de
  | .fr => some fr
  | .klingon => none

def langOffer : ConstraintSet LangVal := [.atom (.eq .de)]

/-- The request `fr or klingon`. -/
def langRequestBad : ConstraintSet LangVal :=
  [.or [.eq .fr, .eq .klingon]]

theorem langRequestBad_ungrounded :
    ConstraintSet.ground langGrounding langRequestBad = none := by
  decide

/-- One ungrounded alternative leaves the whole request without a denotation,
so the input is rejected. The grounded offer `eq de` against the request `eq fr`
alone is `Incompatible` under the same declaration
(`language_declared_verdict`). -/
theorem ungrounded_alternative_none :
    groundedVerdict langGrounding decl langOffer langRequestBad = none :=
  groundedVerdict_of_right_none langGrounding decl langOffer langRequestBad
    langRequestBad_ungrounded

end OdrlGrounded.Example
