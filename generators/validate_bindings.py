"""
validate_bindings.py
====================
Checks each binding's axiom files against domain facts the author is
humanly certain of.

    uv run generators/validate_bindings.py --probes probes \
        --axioms problems/axioms

Why this exists
---------------
No theorem verifies that a binding captures its author's intent: the
semantics is correct relative to the resource and the reading
(assm:correct), and whether bcp_de means German is not a formal question.
But every concrete way a mapping goes wrong leaves a formal footprint: a
swapped edge direction makes the wrong containment derivable, a mistyped
constant makes a known concept absent, a build against the wrong slice
makes a known-absent concept present, a dropped background file loses a
distinctness.  A probe file records a handful of facts about the domain
that the author would bet on, and this script checks the built files
against them.  A failing probe localises the error to the binding, before
it surfaces three layers later as a verdict flip that looks like a
finding.

Probe files are also documentation: probes/language.json is a
machine-checked statement of what the language binding is supposed to
mean.

Probe format (JSON, one file per binding)
-----------------------------------------
    {
      "binding":  "language-strict",
      "includes": ["BCP47000-0.ax", "BCP47001-0.ax"],
      "leq":      [["loc_bq", "loc_nl"]],     entailed under the order
      "not_leq":  [["loc_nl", "loc_bq"]],     not entailed
      "distinct": [["bcp_de", "bcp_fr"]],     inequation present (either
                                              order; inequality is
                                              symmetric)
      "present":  ["bcp_de"],                 constant declared
      "absent":   ["loc_eu"]                  constant nowhere in the
                                              included files
    }

leq is decided by reachability over the parsed kge_leq edges, reflexive
and transitive, which is exactly what the declared order axioms make
derivable.  Nothing here calls a prover: probes are about the files, and
the files are finite.
"""
import argparse
import json
import re
import sys
from collections import deque
from pathlib import Path

# The same assertion shapes tree_expand.py inlines; kept textually
# identical so the two parsers cannot drift apart silently.  If
# tree_expand grows a shape, this grows it too, and the comment there
# points here.
_ASSERTION = re.compile(
    r"fof\(\s*((?:res|bt|bg)_[a-z0-9_]+)\s*,\s*axiom,\s*"
    r"(?:kge_leq\(\s*([a-z0-9_]+)\s*,\s*([a-z0-9_]+)\s*\)"
    r"|kge_concept\(\s*([a-z0-9_]+)\s*\)"
    r"|([a-z0-9_]+)\s*!=\s*([a-z0-9_]+))\s*\)\s*\.",
    re.S)


def load_axioms(includes, axioms_dir: Path):
    """Edges, distinct pairs, and every constant of the included files."""
    edges, distinct, constants = [], set(), set()
    for name in includes:
        path = axioms_dir / name
        if not path.exists():
            raise SystemExit(f"included axiom file missing: {path}")
        for m in _ASSERTION.finditer(path.read_text(encoding="utf-8")):
            if m.group(2):
                edges.append((m.group(2), m.group(3)))
                constants.update((m.group(2), m.group(3)))
            elif m.group(4):
                constants.add(m.group(4))
            else:
                a, b = m.group(5), m.group(6)
                distinct.add(frozenset((a, b)))
                constants.update((a, b))
    return edges, distinct, constants


def reachable(a: str, b: str, up: dict) -> bool:
    """a <= b under the reflexive transitive reading of the edges."""
    if a == b:
        return True
    seen = {a}
    queue = deque([a])
    while queue:
        for nxt in up.get(queue.popleft(), ()):
            if nxt == b:
                return True
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return False


def run_probe(probe: dict, axioms_dir: Path):
    """Yield (ok, description) for every check in one probe file."""
    edges, distinct, constants = load_axioms(probe["includes"], axioms_dir)
    up: dict = {}
    for a, b in edges:
        up.setdefault(a, set()).add(b)

    for a, b in probe.get("leq", ()):
        ok = reachable(a, b, up)
        yield ok, (f"{a} <= {b} derivable" if ok else
                   f"{a} <= {b} NOT derivable: missing edge, wrong "
                   f"direction, or wrong slice")
    for a, b in probe.get("not_leq", ()):
        ok = not reachable(a, b, up)
        yield ok, (f"{a} <= {b} not derivable, as intended" if ok else
                   f"{a} <= {b} IS derivable: an edge points the wrong "
                   f"way or the reading is not the one intended")
    for a, b in probe.get("distinct", ()):
        ok = frozenset((a, b)) in distinct
        yield ok, (f"{a} != {b} declared" if ok else
                   f"{a} != {b} NOT declared: background file missing "
                   f"from includes, or the pair outside the theory's "
                   f"member set")
    for c in probe.get("present", ()):
        ok = c in constants
        yield ok, (f"{c} present" if ok else
                   f"{c} ABSENT: mistyped constant or wrong slice built")
    for c in probe.get("absent", ()):
        ok = c not in constants
        yield ok, (f"{c} absent, as intended" if ok else
                   f"{c} PRESENT: the two-readings claim for this "
                   f"binding fails, or the wrong resource was included")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[3])
    ap.add_argument("--probes", default=Path("probes"), type=Path)
    ap.add_argument("--axioms", default=Path("problems/axioms"), type=Path)
    args = ap.parse_args()

    files = sorted(args.probes.glob("*.json"))
    if not files:
        print(f"no probe files in {args.probes}; a binding without probes "
              f"is a binding nobody has stated the meaning of",
              file=sys.stderr)
        return 1

    failures = 0
    for f in files:
        probe = json.loads(f.read_text(encoding="utf-8"))
        print(f"{probe.get('binding', f.stem)}  ({f.name})")
        for ok, desc in run_probe(probe, args.axioms):
            print(f"  {'ok  ' if ok else 'FAIL'} {desc}")
            failures += 0 if ok else 1
    if failures:
        print(f"\n{failures} probe failure(s): the binding does not mean "
              f"what its author says it means; fix the binding, not the "
              f"probe, unless the probe is wrong about the world")
        return 1
    print("\nall probes pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())