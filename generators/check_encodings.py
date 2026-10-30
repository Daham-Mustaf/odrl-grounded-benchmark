"""
check_encodings.py
==================
Fails when the two encodings of a problem disagree.

    uv run generators/check_encodings.py                 # all problems
    uv run generators/check_encodings.py --names-only    # premises only, no provers

Exit status is 0 when every problem passes all three checks and 1 otherwise.
Intended for CI, where the point is that a divergence stops the build rather
than appearing in a table someone may or may not read.

The two encodings
-----------------
TPTP is the reference encoding.  A .p file includes whole axiom files, so it
carries every statement of the resource.  An .smt2 file carries the slice the
tree reaches: the statements about the constants the tree names, written out
by tree_expand.  A TPTP statement the SMT-LIB file leaves out is therefore not
a difference, and the checks run in the direction that matters.

The three checks
----------------
  (i)   every premise name an .smt2 file carries exists on the TPTP side, in
        the .p file or in an axiom file it includes, with the same formula;
  (ii)  every statement written inline in a .p file is in its .smt2 file, with
        the same formula;
  (iii) the two encodings give the same status on each query, with the
        includes resolved.

Formulas are compared after parsing both syntaxes into one normal form:
equality is symmetric, a != b and (distinct a b) are the negation of an
equality, and/or are flattened and unordered, and bound variables are
numbered by binding order.  Spelling and layout therefore do not matter;
structure does.

What this tests, and what it does not
-------------------------------------
The paper defines what a constraint denotes and what a witness condition
is; the generator emits two encodings of that condition, one TPTP and one
SMT-LIB.  Nothing states, and nothing has ever checked, that either encoding
means what the definition means.  That obligation is a translation-adequacy
lemma the paper does not yet carry.

This is the weaker, checkable shadow of it: not that each encoding is
faithful to the definition, but that the two agree with each other.  An
encoding bug on one side and not the other shows up here.  A bug both sides
share does not, and no amount of running will find it; only the lemma will.

It is worth having anyway, because the bug that actually occurred was of the
first kind.  A multi-valued isAnyOf in the meets conjunct produced an
unparenthesised disjunction that the TPTP conjunction then swallowed; the
SMT side, being prefix, was unaffected.  Two provers returned different
verdicts on the same problem and the difference was the encoding rather than
either prover.  It was noticed because someone read the table.
"""

import argparse
import re
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

# Problems whose two sides are known to differ.  Each entry is a defect to
# fix, not an accepted difference.  There are none.
KNOWN_GAPS: dict = {}

# casc, as run_verdict.sh runs it: a status is all this check needs, and the
# schedule mode answers the large Location queries in a fraction of the time.
# The seconds per query are given with --limit; full-run.sh passes the
# PROVER_LIMIT that stages 6 to 8 use.
VAMPIRE = ["vampire", "--mode", "casc", "--time_limit"]
Z3 = ["z3"]

_SZS = re.compile(r"SZS status (\w+)")


# --- the statuses ----------------------------------------------------------

def run_fof(path: Path, include: Path, limit: int) -> str:
    try:
        out = subprocess.run(VAMPIRE + [str(limit), "--include", str(include),
                                        str(path)],
                             capture_output=True, text=True,
                             timeout=limit + 30).stdout
    except subprocess.TimeoutExpired:
        return "timeout"
    m = _SZS.search(out)
    if not m:
        return "no-status"
    s = m.group(1).lower()
    return {"unsatisfiable": "unsat", "satisfiable": "sat",
            "countersatisfiable": "sat"}.get(s, s)


def run_smt(path: Path, limit: int) -> str:
    try:
        out = subprocess.run(Z3 + [f"-T:{limit}", str(path)], capture_output=True,
                             text=True, timeout=limit + 30).stdout
    except subprocess.TimeoutExpired:
        return "timeout"
    for line in out.splitlines():
        line = line.strip()
        if line in ("sat", "unsat", "unknown"):
            return line
    return "no-status"


def verdict(q1: str, q2: str) -> str:
    """The verdict the pair of statuses gives, or why it gives none."""
    if q1 == "unsat" and q2 == "unsat":
        return "INCONSISTENT"
    if q1 == "unsat":
        return "Incompatible"
    if q2 == "unsat":
        return "Compatible"
    if q1 == q2 == "sat":
        return "Unknown"
    return f"undecided({q1},{q2})"


# --- one normal form for both syntaxes -------------------------------------

def _nary(op, xs):
    flat = []
    for x in xs:
        flat.extend(x[1] if x[0] == op else [x])
    if len(flat) == 1:
        return flat[0]
    return (op, tuple(sorted(flat, key=repr)))


def _eq(a, b):
    return ("eq",) + tuple(sorted((a, b)))


_TPTP_TOKEN = re.compile(
    r"\s*(\$true|\$false|<=>|=>|!=|[()\[\],:&|~!?=]|[A-Za-z_][A-Za-z0-9_]*)")


def _tptp_tokens(s):
    s, pos, out = s.strip(), 0, []
    while pos < len(s):
        m = _TPTP_TOKEN.match(s, pos)
        if not m:
            raise ValueError(f"cannot read {s[pos:pos + 30]!r}")
        out.append(m.group(1))
        pos = m.end()
        while pos < len(s) and s[pos].isspace():
            pos += 1
    return out


class _Tptp:
    """Recursive descent over the TPTP FOF the emitters write."""

    def __init__(self, text):
        self.t, self.i = _tptp_tokens(text), 0

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else None

    def take(self, want=None):
        tok = self.peek()
        if tok is None or (want is not None and tok != want):
            raise ValueError(f"expected {want!r}, found {tok!r}")
        self.i += 1
        return tok

    def formula(self, env):
        lhs = self.or_(env)
        if self.peek() == "=>":
            self.take()
            return ("imp", lhs, self.or_(env))
        return lhs

    def or_(self, env):
        xs = [self.and_(env)]
        while self.peek() == "|":
            self.take()
            xs.append(self.and_(env))
        return _nary("or", xs)

    def and_(self, env):
        xs = [self.unary(env)]
        while self.peek() == "&":
            self.take()
            xs.append(self.unary(env))
        return _nary("and", xs)

    def unary(self, env):
        tok = self.peek()
        if tok == "~":
            self.take()
            return ("not", self.unary(env))
        if tok in ("!", "?"):
            self.take()
            self.take("[")
            names = [self.take()]
            while self.peek() == ",":
                self.take()
                names.append(self.take())
            self.take("]")
            self.take(":")
            inner = dict(env)
            for n in names:
                inner[n] = f"_v{len(inner)}"
            return ("forall" if tok == "!" else "exists", len(names),
                    self.unary(inner))
        if tok == "(":
            self.take()
            f = self.formula(env)
            self.take(")")
            return f
        if tok in ("$true", "$false"):
            self.take()
            return ("true",) if tok == "$true" else ("false",)
        name = self.take()
        if self.peek() == "(":
            self.take("(")
            args = [self.term(env)]
            while self.peek() == ",":
                self.take()
                args.append(self.term(env))
            self.take(")")
            return ("p", name, tuple(args))
        a, op, b = env.get(name, name), self.take(), self.term(env)
        if op not in ("=", "!="):
            raise ValueError(f"expected = or !=, found {op!r}")
        return _eq(a, b) if op == "=" else ("not", _eq(a, b))

    def term(self, env):
        tok = self.take()
        return env.get(tok, tok)


def parse_tptp(text):
    p = _Tptp(text)
    f = p.formula({})
    if p.peek() is not None:
        raise ValueError(f"trailing {p.peek()!r}")
    return f


def _read_sexp(text):
    toks = re.findall(r"\(|\)|[^\s()]+", text)

    def read(i):
        if toks[i] == "(":
            out, i = [], i + 1
            while toks[i] != ")":
                x, i = read(i)
                out.append(x)
            return out, i + 1
        return toks[i], i + 1

    return read(0)[0]


def _smt(x, env):
    term = lambda a: env.get(a, a)
    if isinstance(x, str):
        return ("true",) if x == "true" else ("false",) if x == "false" else x
    head = x[0]
    if head in ("and", "or"):
        return _nary(head, [_smt(a, env) for a in x[1:]])
    if head == "not":
        return ("not", _smt(x[1], env))
    if head == "=>":
        return ("imp", _smt(x[1], env), _smt(x[2], env))
    if head == "=":
        return _eq(term(x[1]), term(x[2]))
    if head == "distinct" and len(x) == 3:
        return ("not", _eq(term(x[1]), term(x[2])))
    if head in ("kge_leq", "kge_concept"):
        return ("p", head, tuple(term(a) for a in x[1:]))
    if head == "forall":
        inner = dict(env)
        for b in x[1]:
            inner[b[0]] = f"_v{len(inner)}"
        return ("forall", len(x[1]), _smt(x[2], inner))
    raise ValueError(f"cannot read {head!r}")


def parse_smt(text):
    return _smt(_read_sexp(text), {})


# --- what each side carries ------------------------------------------------

def _strip(text, marker):
    return "\n".join(l for l in text.split("\n")
                     if not l.lstrip().startswith(marker))


def _balanced(text, start):
    """Index just past the parenthesis that closes the one before `start`."""
    depth, j = 1, start
    while depth:
        depth += (text[j] == "(") - (text[j] == ")")
        j += 1
    return j


@lru_cache(maxsize=None)
def tptp_statements(path: Path) -> dict:
    """name -> formula text, for every fof of a file.  Comments are skipped."""
    text = _strip(path.read_text(encoding="utf-8"), "%")
    out = {}
    for m in re.finditer(r"(?m)^\s*fof\(", text):
        inner = text[m.end():_balanced(text, m.end()) - 1]
        name, _, formula = (s.strip() for s in inner.split(",", 2))
        out[name] = formula
    return out


def tptp_side(p_file: Path):
    """(inline, included): the statements written in the .p file, and those
    of the axiom files it includes."""
    inline = tptp_statements(p_file)
    included = {}
    text = _strip(p_file.read_text(encoding="utf-8"), "%")
    for inc in re.findall(r"include\('([^']+)'\)", text):
        ax = p_file.parent.parent / inc
        if ax.exists():
            for k, v in tptp_statements(ax).items():
                included.setdefault(k, v)
    return inline, included


def smt_premises(smt_file: Path):
    """(named, unnamed): name -> formula text, and a count of statements with
    no name."""
    text = _strip(smt_file.read_text(encoding="utf-8"), ";")
    named, unnamed, i = {}, 0, 0
    while True:
        i = text.find("(assert", i)
        if i < 0:
            return named, unnamed
        j = _balanced(text, i + 1)
        x = _read_sexp(text[i:j])
        body = x[1]
        if isinstance(body, list) and body[0] == "!" and ":named" in body:
            named[body[body.index(":named") + 1]] = body[1]
        else:
            unnamed += 1
        i = j


def _show(f, limit=90):
    s = repr(f)
    return s if len(s) <= limit else s[:limit] + "..."


def compare(pid, q, d: Path):
    """The failures of checks (i) and (ii) for one query, as (check, text)."""
    p_file, s_file = d / f"{pid}-{q}.p", d / f"{pid}-{q}.smt2"
    inline, included = tptp_side(p_file)
    on_tptp = {**included, **inline}
    named, unnamed = smt_premises(s_file)
    out = []
    if unnamed:
        out.append(("i", f"{unnamed} SMT-LIB statement(s) carry no name"))
    for name, body in sorted(named.items()):
        if name not in on_tptp:
            out.append(("i", f"{name}: in the SMT-LIB file, not on the TPTP side"))
            continue
        try:
            a, b = parse_tptp(on_tptp[name]), _smt(body, {})
        except ValueError as e:
            out.append(("i", f"{name}: {e}"))
            continue
        if a != b:
            out.append(("i", f"{name}: formulas differ  TPTP {_show(a)}  SMT {_show(b)}"))
    for name in sorted(inline):
        if name not in named:
            out.append(("ii", f"{name}: written in the .p file, not in the SMT-LIB file"))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[3])
    ap.add_argument("--dir", default="problems/verdict", type=Path)
    ap.add_argument("--allow-known", action="store_true",
                    help="exit 0 despite the divergences listed in "
                         "KNOWN_GAPS; they are still printed")
    ap.add_argument("--names-only", action="store_true",
                    help="check (i) and (ii) and skip the provers")
    ap.add_argument("--limit", type=int, default=60,
                    help="seconds a prover may take on one query")
    args = ap.parse_args()

    ids = sorted({p.stem.rsplit("-", 1)[0] for p in args.dir.glob("*-1.p")})
    if not ids:
        print(f"no problems in {args.dir}", file=sys.stderr)
        return 1
    root = args.dir.resolve().parent

    diverged, gapped = [], []
    fails = {"i": 0, "ii": 0, "iii": 0}
    print(f"{'problem':10} {'TPTP':>14} {'SMT-LIB':>14}   checks")
    for pid in ids:
        problems = []
        for q in (1, 2):
            problems += [(c, f"query {q}: {t}") for c, t in compare(pid, q, args.dir)]
        # the same finding on both queries is one finding
        problems = list(dict.fromkeys(problems))
        for c in {c for c, _ in problems}:
            fails[c] += 1

        f = s = ""
        if not args.names_only:
            ft = [run_fof(args.dir / f"{pid}-{q}.p", root, args.limit)
                  for q in (1, 2)]
            sm = [run_smt(args.dir / f"{pid}-{q}.smt2", args.limit)
                  for q in (1, 2)]
            f, s = verdict(*ft), verdict(*sm)
            if ft != sm:
                problems.append(("iii", f"statuses differ  TPTP {ft}  SMT-LIB {sm}"))
                fails["iii"] += 1
        note = ("fail " + ",".join(sorted({c for c, _ in problems}))
                if problems else "ok")
        print(f"{pid:10} {f:>14} {s:>14}   {note}")
        if problems:
            (gapped if pid in KNOWN_GAPS else diverged).append((pid, problems))

    print()
    for pid, problems in gapped:
        print(f"known gap  {pid}: {KNOWN_GAPS[pid]}")
    for pid, problems in diverged:
        for c, text in problems:
            print(f"DIVERGENT  {pid} ({c}): {text}")

    print()
    print(f"problems checked: {len(ids)}   failing (i): {fails['i']}   "
          f"(ii): {fails['ii']}   (iii): {fails['iii']}")
    if diverged:
        print(f"\n{len(diverged)} problem(s) encode differently in the two "
              f"languages.\nThe verdict is a property of the constraints and "
              f"the resource, so a\ndifference between the encodings is a "
              f"defect in one of them.")
        return 1
    if gapped and not args.allow_known:
        print(f"\n{len(gapped)} known gap(s); pass --allow-known to "
              f"tolerate them.")
        return 1
    print("the two encodings agree on every problem.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
