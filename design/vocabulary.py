"""
vocabulary.py
=============
The four enumerations the rest of the benchmark is written in.

Nothing here has logic beyond one mapping function.  Every other module
imports these names rather than writing the strings, so that a value can be
misspelled in exactly one place and caught there.

Why these four and not others
-----------------------------
Each of them separates two things that were sharing a column.

A *verdict* is a claim about every admissible structure: Incompatible says
no structure admits a common use, Compatible says every structure does.  A
*run status* is what one solver reported about one file on one machine on
one day.  The two look alike in a table and are nothing alike in what they
mean, and the whole benchmark exists to keep them apart.  Hence Verdict and
RunStatus, and hence the fact that RunStatus has no member named after a
verdict and Verdict has no member named after a status.

Unknown has two causes that a reader cannot tell apart from the verdict
alone.  A value that grounds to no concept is a failure to interpret the
policy, repaired by fixing the policy or the binding.  Two satisfiable
queries are a statement about what the resource leaves open, settled by a
declaration.  A bare Unknown conflates them, so UnknownReason is required
wherever Unknown is claimed.

And a premise has a provenance that decides who may withdraw it.  Resource
assertions are the authority's and stand until the authority changes them;
declared background is the parties' and can be withdrawn, which returns a
definite verdict to Unknown; the order and equality axioms are neither, they
are constitutive of the sort.  Presenting the first two classes without the
third misattributes the axioms to a party.
"""

from __future__ import annotations

from enum import Enum


class Verdict(Enum):
    """A claim about every admissible structure.

    Not a solver output.  A verdict is only ever produced by
    :func:`derive_verdict` from a pair of run statuses, or read from a
    manifest as an expectation.
    """

    COMPATIBLE = "Compatible"
    INCOMPATIBLE = "Incompatible"
    UNKNOWN = "Unknown"

    def __str__(self) -> str:
        return self.value

    @property
    def is_definite(self) -> bool:
        """Whether the verdict is stable under extension of the resource.

        Compatible and Incompatible quantify over the admissible structures
        and survive when that class shrinks; Unknown does not.
        """
        return self is not Verdict.UNKNOWN


class RunStatus(Enum):
    """What one solver reported about one query.

    Lowercase throughout, to keep it visually distinct from a verdict in
    logs and tables.  UNDETERMINED is ours rather than any solver's: it
    covers the cases where the run produced nothing usable, and it exists so
    that no caller has to decide whether a timeout is a kind of unknown.
    """

    SAT = "sat"
    UNSAT = "unsat"
    UNKNOWN = "unknown"          # the solver's own, never a verdict
    TIMEOUT = "timeout"
    ERROR = "error"
    UNDETERMINED = "undetermined"

    def __str__(self) -> str:
        return self.value

    @property
    def is_conclusive(self) -> bool:
        return self in (RunStatus.SAT, RunStatus.UNSAT)


class UnknownReason(Enum):
    """Why a verdict is Unknown.

    Required wherever Unknown is claimed.  The two are repaired
    differently: an ungrounded value needs the policy or the binding fixed,
    an epistemic Unknown needs a declaration from the parties.  A reader
    given only the verdict cannot tell which, so the schema does not permit
    a bare Unknown.
    """

    UNGROUNDED = "ungrounded"    # a value the grounding does not resolve
    EPISTEMIC = "epistemic"      # both queries satisfiable

    def __str__(self) -> str:
        return self.value


class PremiseClass(Enum):
    """Where a premise comes from, and therefore who may withdraw it.

    The prefix is what appears in a formula name, so a proof or an unsat
    core classifies by string prefix without any table lookup.  Longer
    prefixes are listed first in :meth:`from_name` so that ``bg_dist``
    matches before ``bg``.

    Distinctness and disjointness are separate classes although both are
    declared: distinctness is ground and says two concepts are not the same,
    disjointness is quantified and says nothing lies below both.  The
    decidability argument turns on that difference, since disjointness is
    the only quantified part of the background theory.
    """

    RESOURCE = "res"             # published by the authority
    BG_DISTINCTNESS = "bg_dist"  # declared, ground, withdrawable
    BG_DISJOINTNESS = "bg_disj"  # declared, quantified, withdrawable
    AX_ORDER = "ax_order"        # constitutive of the sort
    AX_EQUALITY = "ax_eq"        # constitutive; identity reasoning
    WITNESS = "wc"               # the witness condition itself

    def __str__(self) -> str:
        return self.value

    @property
    def is_withdrawable(self) -> bool:
        """Whether withdrawing this premise can change a definite verdict.

        Only the parties' declarations.  The resource is the authority's,
        the witness condition is the parties' own constraints, and the
        axioms belong to the sort.
        """
        return self in (PremiseClass.BG_DISTINCTNESS,
                        PremiseClass.BG_DISJOINTNESS)

    @property
    def is_constitutive(self) -> bool:
        """Whether this premise comes from the sort rather than from anyone."""
        return self in (PremiseClass.AX_ORDER, PremiseClass.AX_EQUALITY)

    @classmethod
    def from_name(cls, formula_name: str) -> "PremiseClass | None":
        """The class a formula name declares, or None if it declares none.

        None is not a default class.  A premise whose origin cannot be
        determined is a defect to report, and callers are expected to say so
        rather than to guess.
        """
        for member in sorted(cls, key=lambda m: -len(m.value)):
            if formula_name.startswith(member.value + "_"):
                return member
        return None


# The one place a pair of statuses becomes a verdict.  Everything that needs
# a verdict from a run calls this; nothing reproduces the table.
#
# The two queries are R u B u {W} and R u B u {not W}.  The first being
# unsatisfiable says no admissible structure admits a witness, which is
# Incompatible; the second being unsatisfiable says every admissible
# structure does, which is Compatible.  Both satisfiable is Unknown.
#
# Both unsatisfiable cannot happen when R u B is consistent, and consistency
# is checked once per fixture rather than per problem.  It is raised rather
# than returned because it means the fixture is wrong, not the problem.

class InconsistentFixture(Exception):
    """Both queries unsatisfiable: R u B has no model at all."""


def derive_verdict(inc: RunStatus, comp: RunStatus
                   ) -> tuple[Verdict | None, UnknownReason | None]:
    """The verdict a pair of run statuses gives, or None if they give none.

    ``inc`` is the status of R u B u {W}, ``comp`` that of R u B u {not W}.

    Returning None is the point of this signature: a run that timed out has
    no verdict, and the caller must carry the absence rather than fill it
    from an expectation.  The report keeps the expected verdict and the
    derived verdict in separate columns for the same reason.
    """
    if inc is RunStatus.UNSAT and comp is RunStatus.UNSAT:
        raise InconsistentFixture(
            "both queries unsatisfiable: the resource and background theory "
            "have no model together, so no problem over them has a verdict")
    if not (inc.is_conclusive and comp.is_conclusive):
        return None, None
    if inc is RunStatus.UNSAT:
        return Verdict.INCOMPATIBLE, None
    if comp is RunStatus.UNSAT:
        return Verdict.COMPATIBLE, None
    return Verdict.UNKNOWN, UnknownReason.EPISTEMIC


def ungrounded_verdict() -> tuple[Verdict, UnknownReason]:
    """The verdict when a right-operand value grounds to no concept.

    No query is built in this case, so there is no pair of statuses to give
    to :func:`derive_verdict`.  The verdict is Unknown and its reason is
    ungrounded, and the certificate is the offending value.
    """
    return Verdict.UNKNOWN, UnknownReason.UNGROUNDED