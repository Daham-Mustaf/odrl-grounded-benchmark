"""
check_certificates.py
=====================
Independently verify Vampire refutations for the suite, step by step.

    uv run generators/check_certificates.py --problem KGC330
    uv run generators/check_certificates.py
    uv run generators/check_certificates.py --no-avatar --json report.json

What "checked" means here
-------------------------
A refutation is a DAG of steps.  This checker accepts a step only if the
cited parent formulas semantically entail the conclusion, decided by this
script's own machinery: ground, function-free first-order logic with
equality, no unique-names assumption.  The rule name Vampire attached is
recorded but never trusted; a step whose conclusion does not follow from
its parents is rejected whatever its label.  Steps produced by mechanisms
that are not entailments (AVATAR splitting, definition introduction, RAT)
are tried anyway, since some are propositional entailments of their cited
parents, and reported as UNSUPPORTED with the reason when they are not.

Input premises are not trusted either.  Every leaf cited as
file(path, name) is checked for logical equivalence against the formula of
that name parsed from the query file itself (includes resolved under
--include), so a premise the prover renamed or altered is caught.  Premise
names are classified by prefix so the report can say whether an
Incompatible verdict rests on resource premises or on declared background.

Per problem the result is one of
  FULLY_CHECKED       every step verified, every leaf a legal premise
                      matching the query, a verified $false present
  PARTIALLY_CHECKED   all verifiable steps pass, but some steps are
                      UNSUPPORTED, so the chain to $false is not closed
  REJECTED            a step failed verification, a leaf does not match
                      the query, or no $false step exists
  SATISFIABLE / TIMEOUT / NO_STATUS / PARSE_ERROR as encountered

The expected verdicts of the benchmark are never read.  Entailment is
decided by enumerating partitions of the step's constants (the equality
interpretations) and truth assignments over the resulting atoms; steps
exceeding the small budgets this needs are reported UNSUPPORTED(budget),
never guessed.
"""
import argparse
import itertools
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

# ---------------------------------------------------------------------
# budgets and rule knowledge
# ---------------------------------------------------------------------

MAX_CONSTANTS = 7        # partitions of 7 elements: 877
MAX_ATOMS = 16
MAX_INSTANCES = 4000

NON_ENTAILMENT_RULES = {
    "avatar splitting", "avatar split clause", "avatar component clause",
    "avatar definition", "avatar sat refutation", "sat conversion", "rat",
    "definition folding", "definition unfolding", "skolemisation",
    "choice axiom", "avatar contradiction clause",
}

PREMISE_CLASSES = [
    ("res_", "resource"),
    ("bg_dist", "background distinctness"),
    ("bg_disj", "background disjointness"),
    ("bg_", "background"),
    ("ax_order", "order axiom"),
    ("ax_eq", "equality axiom"),
    ("ax_", "axiom"),
    ("bt_", "background declaration"),
    ("wc_", "witness condition"),
    ("w_", "witness condition"),
]

_SZS = re.compile(r"SZS status (\w+)")
_PROOF = re.compile(r"% SZS output start Proof.*?% SZS output end Proof",
                    re.S)

VAMPIRE = ["--mode", "vampire", "--proof", "tptp",
           "--output_axiom_names", "on", "--proof_extra", "full"]


# ---------------------------------------------------------------------
# TPTP tokenizer and parser (formulas and sources; no imports from the
# benchmark compiler)
# ---------------------------------------------------------------------

_SYMBOLS = ["<=>", "<~>", "=>", "<=", "!=", "~&", "~|",
            "(", ")", "[", "]", ",", ":", ".", "~", "&", "|", "!", "?", "="]


class ParseError(Exception):
    pass


def tokenize(text: str):
    toks, i, n = [], 0, len(text)
    while i < n:
        c = text[i]
        if c.isspace():
            i += 1
            continue
        if c == "%":
            while i < n and text[i] != "\n":
                i += 1
            continue
        if c == "'":
            j = i + 1
            buf = []
            while j < n and text[j] != "'":
                if text[j] == "\\" and j + 1 < n:
                    buf.append(text[j + 1])
                    j += 2
                else:
                    buf.append(text[j])
                    j += 1
            if j >= n:
                raise ParseError("unterminated quoted atom")
            toks.append(("id", "".join(buf)))
            i = j + 1
            continue
        if c.isalnum() or c in "_$":
            j = i
            while j < n and (text[j].isalnum() or text[j] in "_$"):
                j += 1
            word = text[i:j]
            kind = "var" if word[0].isupper() else "id"
            toks.append((kind, word))
            i = j
            continue
        for s in _SYMBOLS:
            if text.startswith(s, i):
                toks.append(("sym", s))
                i += len(s)
                break
        else:
            raise ParseError(f"cannot tokenize at ...{text[i:i+20]!r}")
    return toks


class Parser:
    def __init__(self, toks):
        self.toks = toks
        self.i = 0

    def peek(self):
        return self.toks[self.i] if self.i < len(self.toks) else ("eof", "")

    def next(self):
        t = self.peek()
        self.i += 1
        return t

    def expect(self, kind, val=None):
        k, v = self.next()
        if k != kind or (val is not None and v != val):
            raise ParseError(f"expected {val or kind}, got {v!r}")
        return v

    # ---- terms (also used for sources; lists allowed) ----
    def term(self):
        k, v = self.next()
        if k == "sym" and v == "[":
            items = []
            if not (self.peek() == ("sym", "]")):
                items.append(self.term())
                while self.peek() == ("sym", ","):
                    self.next()
                    items.append(self.term())
            self.expect("sym", "]")
            return ("list", items)
        if k == "var":
            return ("v", v)
        if k == "id":
            if self.peek() == ("sym", "("):
                self.next()
                args = [self.term()]
                while self.peek() == ("sym", ","):
                    self.next()
                    args.append(self.term())
                self.expect("sym", ")")
                return ("f", v, args)
            return ("c", v)
        raise ParseError(f"bad term start {v!r}")

    # ---- formulas ----
    def unit(self):
        k, v = self.peek()
        if (k, v) in (("sym", "!"), ("sym", "?")):
            self.next()
            self.expect("sym", "[")
            vs = [self.expect("var")]
            while self.peek() == ("sym", ","):
                self.next()
                vs.append(self.expect("var"))
            self.expect("sym", "]")
            self.expect("sym", ":")
            body = self.unit()
            return ("forall" if v == "!" else "exists", vs, body)
        if (k, v) == ("sym", "~"):
            self.next()
            return ("not", self.unit())
        if (k, v) == ("sym", "("):
            self.next()
            f = self.formula()
            self.expect("sym", ")")
            return f
        if k == "id" and v == "$false":
            self.next()
            return ("false",)
        if k == "id" and v == "$true":
            self.next()
            return ("true",)
        t = self.term()
        if self.peek() in (("sym", "="), ("sym", "!=")):
            _, op = self.next()
            t2 = self.term()
            eq = ("eq", t, t2)
            return eq if op == "=" else ("not", eq)
        if t[0] == "f":
            return ("atom", t[1], t[2])
        if t[0] == "c":
            return ("atom", t[1], [])
        raise ParseError("variable cannot stand as a formula")

    def formula(self):
        left = self.unit()
        k, v = self.peek()
        if (k, v) in (("sym", "&"), ("sym", "|")):
            conn = v
            items = [left]
            while self.peek() == ("sym", conn):
                self.next()
                items.append(self.unit())
            k2, v2 = self.peek()
            if (k2, v2) in (("sym", "&"), ("sym", "|")) and v2 != conn:
                raise ParseError("mixed & and | without parentheses")
            return ("and" if conn == "&" else "or", items)
        if (k, v) == ("sym", "=>"):
            self.next()
            return ("or", [("not", left), self.unit()])
        if (k, v) == ("sym", "<="):
            self.next()
            return ("or", [left, ("not", self.unit())])
        if (k, v) == ("sym", "<=>"):
            self.next()
            r = self.unit()
            return ("iff", left, r)
        if (k, v) == ("sym", "<~>"):
            self.next()
            r = self.unit()
            return ("not", ("iff", left, r))
        return left


def parse_statements(text: str):
    """All fof/cnf statements in text as (name, role, formula, source)."""
    out = []
    toks = tokenize(text)
    p = Parser(toks)
    while p.peek()[0] != "eof":
        k, v = p.next()
        if k == "id" and v == "include":
            p.expect("sym", "(")
            path = p.next()[1]
            p.expect("sym", ")")
            p.expect("sym", ".")
            out.append(("include", path, None, None))
            continue
        if not (k == "id" and v in ("fof", "cnf", "tff")):
            raise ParseError(f"expected fof/cnf, got {v!r}")
        p.expect("sym", "(")
        name = p.next()[1]
        p.expect("sym", ",")
        role = p.expect("id")
        p.expect("sym", ",")
        formula = p.formula()
        source = None
        while p.peek() == ("sym", ","):
            p.next()
            t = p.term()
            if source is None:
                source = t
        p.expect("sym", ")")
        p.expect("sym", ".")
        out.append((name, role, formula, source))
    return out


# ---------------------------------------------------------------------
# semantics: ground FO with equality over the step's constants
# ---------------------------------------------------------------------

def free_vars(f, bound=frozenset()):
    tag = f[0]
    if tag in ("false", "true"):
        return set()
    if tag == "atom":
        return {a[1] for a in f[2] if a[0] == "v"} - bound
    if tag == "eq":
        return {t[1] for t in (f[1], f[2]) if t[0] == "v"} - bound
    if tag == "not":
        return free_vars(f[1], bound)
    if tag in ("and", "or"):
        return set().union(*(free_vars(g, bound) for g in f[1]))
    if tag == "iff":
        return free_vars(f[1], bound) | free_vars(f[2], bound)
    if tag in ("forall", "exists"):
        return free_vars(f[2], bound | set(f[1]))
    raise ParseError(f"unknown node {tag}")


def strip_universal(f):
    """Leading universal quantifiers plus free variables, and the body."""
    vs = []
    while f[0] == "forall":
        vs.extend(f[1])
        f = f[2]
    return vs + sorted(free_vars(f) - set(vs)), f


def has_quantifier(f):
    tag = f[0]
    if tag in ("forall", "exists"):
        return True
    if tag == "not":
        return has_quantifier(f[1])
    if tag in ("and", "or"):
        return any(has_quantifier(g) for g in f[1])
    if tag == "iff":
        return has_quantifier(f[1]) or has_quantifier(f[2])
    return False


def substitute(f, sub):
    tag = f[0]
    if tag in ("false", "true"):
        return f
    if tag == "atom":
        return ("atom", f[1],
                [sub.get(a[1], a) if a[0] == "v" else a for a in f[2]])
    if tag == "eq":
        s = sub.get(f[1][1], f[1]) if f[1][0] == "v" else f[1]
        t = sub.get(f[2][1], f[2]) if f[2][0] == "v" else f[2]
        return ("eq", s, t)
    if tag == "not":
        return ("not", substitute(f[1], sub))
    if tag in ("and", "or"):
        return (tag, [substitute(g, sub) for g in f[1]])
    if tag == "iff":
        return ("iff", substitute(f[1], sub), substitute(f[2], sub))
    raise ParseError("substitution under quantifier")


def constants_in(f, acc):
    tag = f[0]
    if tag == "atom":
        for a in f[2]:
            if a[0] == "c":
                acc.add(a[1])
    elif tag == "eq":
        for t in (f[1], f[2]):
            if t[0] == "c":
                acc.add(t[1])
    elif tag == "not":
        constants_in(f[1], acc)
    elif tag in ("and", "or"):
        for g in f[1]:
            constants_in(g, acc)
    elif tag == "iff":
        constants_in(f[1], acc)
        constants_in(f[2], acc)
    elif tag in ("forall", "exists"):
        constants_in(f[2], acc)


def partitions(items):
    """All partitions, as dicts item -> block id (restricted growth)."""
    items = list(items)
    if not items:
        yield {}
        return
    n = len(items)
    rgs = [0] * n
    maxes = [0] * n
    while True:
        yield {items[i]: rgs[i] for i in range(n)}
        i = n - 1
        while i > 0:
            if rgs[i] <= maxes[i - 1]:
                rgs[i] += 1
                maxes[i] = max(maxes[i - 1], rgs[i])
                for j in range(i + 1, n):
                    rgs[j] = 0
                    maxes[j] = maxes[i]
                break
            i -= 1
        else:
            return


def evaluate(f, block, val):
    tag = f[0]
    if tag == "false":
        return False
    if tag == "true":
        return True
    if tag == "eq":
        return block[f[1][1]] == block[f[2][1]]
    if tag == "atom":
        return val[(f[1], tuple(block[a[1]] for a in f[2]))]
    if tag == "not":
        return not evaluate(f[1], block, val)
    if tag == "and":
        return all(evaluate(g, block, val) for g in f[1])
    if tag == "or":
        return any(evaluate(g, block, val) for g in f[1])
    if tag == "iff":
        return evaluate(f[1], block, val) == evaluate(f[2], block, val)
    raise ParseError("quantifier at evaluation")


def entails(parents, conclusion):
    """('ok'|'fail'|'unsupported', detail) for parents |= conclusion."""
    cvars, cbody = strip_universal(conclusion)
    if has_quantifier(cbody):
        return "unsupported", "quantifier inside conclusion"
    fresh = {v: ("c", f"$sk_{i}") for i, v in enumerate(cvars)}
    cbody = substitute(cbody, fresh) if fresh else cbody

    pool: set = set()
    constants_in(cbody, pool)
    stripped = []
    for p in parents:
        pv, pb = strip_universal(p)
        if has_quantifier(pb):
            return "unsupported", "quantifier inside parent"
        stripped.append((pv, pb))
        constants_in(pb, pool)
    if not pool:
        pool = {"$hb_0"}
    if len(pool) > MAX_CONSTANTS:
        return "unsupported", f"{len(pool)} constants exceeds budget"
    pool = sorted(pool)

    ground = []
    for pv, pb in stripped:
        if not pv:
            ground.append(pb)
            continue
        combos = itertools.product(pool, repeat=len(pv))
        for combo in combos:
            ground.append(substitute(pb, {v: ("c", c)
                                          for v, c in zip(pv, combo)}))
            if len(ground) > MAX_INSTANCES:
                return "unsupported", "instantiation budget exceeded"

    for block in partitions(pool):
        atoms = set()

        def collect(g):
            tag = g[0]
            if tag == "atom":
                atoms.add((g[1], tuple(block[a[1]] for a in g[2])))
            elif tag == "not":
                collect(g[1])
            elif tag in ("and", "or"):
                for h in g[1]:
                    collect(h)
            elif tag == "iff":
                collect(g[1])
                collect(g[2])

        for g in ground:
            collect(g)
        collect(cbody)
        atoms = sorted(atoms)
        if len(atoms) > MAX_ATOMS:
            return "unsupported", f"{len(atoms)} atoms exceeds budget"
        for bits in itertools.product((False, True), repeat=len(atoms)):
            val = dict(zip(atoms, bits))
            if all(evaluate(g, block, val) for g in ground) \
                    and not evaluate(cbody, block, val):
                return "fail", "countermodel found"
    return "ok", ""


def equivalent(f, g):
    a, da = entails([f], g)
    if a != "ok":
        return a, da
    return entails([g], f)


# ---------------------------------------------------------------------
# query loading (premise ground truth) and proof checking
# ---------------------------------------------------------------------

def load_query(path: Path, include_root: Path, seen=None):
    seen = seen or set()
    if path in seen:
        return {}
    seen.add(path)
    named = {}
    for name, role, formula, _src in parse_statements(path.read_text()):
        if name == "include":
            inc = include_root / role
            named.update(load_query(inc, include_root, seen))
        else:
            named[name] = formula
    return named


def classify_premise(name: str) -> str:
    for prefix, cls in PREMISE_CLASSES:
        if name.startswith(prefix):
            return cls
    return "unclassified"


def source_kind(src):
    if src is None:
        return ("none",)
    if src[0] == "f" and src[1] == "file":
        args = src[2]
        pname = args[1][1] if len(args) > 1 else "?"
        return ("premise", pname)
    if src[0] == "f" and src[1] == "inference":
        rule = src[2][0]
        rule = (rule[1] if rule[0] in ("c", "f") else "?")
        parents, nested = [], []

        def walk(t):
            if t[0] == "c":
                parents.append(t[1])
            elif t[0] == "f" and t[1] == "inference":
                nested.append(t[2][0][1].replace("_", " "))
                for u in t[2][2][1]:
                    walk(u)
            elif t[0] == "list":
                for u in t[1]:
                    walk(u)

        if len(src[2]) > 2:
            walk(src[2][2])
        return ("inference", rule.replace("_", " "), parents, nested)
    if src[0] in ("f", "c"):
        return ("introduced", src[1])
    return ("other",)


def check_proof(proof_text: str, query: dict):
    steps = parse_statements(proof_text)
    results = []          # (id, kind, rule, status, detail)
    formulas = {}
    unsupported_rules = Counter()
    premise_classes = Counter()
    false_verified = False
    rejected = False

    for name, role, formula, src in steps:
        if name == "include":
            continue
        formulas[name] = formula
        kind = source_kind(src)
        if kind[0] == "premise":
            pname = kind[1]
            premise_classes[classify_premise(pname)] += 1
            if pname not in query:
                results.append((name, "premise", pname, "REJECTED",
                                "name not found in query"))
                rejected = True
                continue
            st, d = equivalent(formula, query[pname])
            if st == "ok":
                results.append((name, "premise", pname, "ok", ""))
            elif st == "unsupported":
                results.append((name, "premise", pname, "UNSUPPORTED", d))
                unsupported_rules["premise equivalence " + d] += 1
            else:
                results.append((name, "premise", pname, "REJECTED",
                                "differs from query formula"))
                rejected = True
        elif kind[0] == "inference":
            rule, parents, nested = kind[1], kind[2], kind[3]
            missing = [p for p in parents if p not in formulas]
            if missing:
                results.append((name, "inference", rule, "REJECTED",
                                f"missing parents {missing}"))
                rejected = True
                continue
            st, d = entails([formulas[p] for p in parents], formula)
            label = rule + (" + " + " + ".join(nested) if nested else "")
            if st == "ok":
                results.append((name, "inference", label, "ok", ""))
                if formula == ("false",):
                    false_verified = True
            elif st == "unsupported" or \
                    rule in NON_ENTAILMENT_RULES or \
                    any(nr in NON_ENTAILMENT_RULES for nr in nested):
                results.append((name, "inference", label, "UNSUPPORTED", d))
                unsupported_rules[label] += 1
            else:
                results.append((name, "inference", label, "REJECTED",
                                f"conclusion not entailed ({d})"))
                rejected = True
        elif kind[0] == "introduced":
            results.append((name, "introduced", kind[1], "UNSUPPORTED",
                            "symbol or clause introduced, not entailed"))
            unsupported_rules["introduced " + kind[1]] += 1
        else:
            results.append((name, "?", "?", "UNSUPPORTED", "unknown source"))
            unsupported_rules["unknown source"] += 1

    if rejected:
        verdict = "REJECTED"
    elif any(r[3] == "UNSUPPORTED" for r in results):
        verdict = "PARTIALLY_CHECKED"
    elif false_verified:
        verdict = "FULLY_CHECKED"
    else:
        verdict = "REJECTED" if results else "PARSE_ERROR"
        if verdict == "REJECTED":
            results.append(("-", "-", "-", "REJECTED",
                            "no verified $false step"))
    return verdict, results, unsupported_rules, premise_classes


# ---------------------------------------------------------------------
# driver
# ---------------------------------------------------------------------

def obtain_proof(path: Path, args):
    if args.proofs:
        pf = args.proofs / (path.stem + ".proof")
        if not pf.exists():
            return "no-proof-file", ""
        text = pf.read_text()
    else:
        cmd = [args.binary, "--include", str(args.include)] + VAMPIRE \
            + (["--avatar", "off"] if args.no_avatar else []) \
            + ["-t", str(args.limit), str(path)]
        try:
            text = subprocess.run(cmd, capture_output=True, text=True,
                                  timeout=args.limit + 5).stdout
        except subprocess.TimeoutExpired:
            return "timeout", ""
    m = _SZS.search(text)
    status = m.group(1).lower() if m else "no-status"
    if status not in ("unsatisfiable", "contradictoryaxioms"):
        return status, ""
    proof = _PROOF.search(text)
    if not proof:
        return "unsat-no-proof", ""
    if args.save_proofs:
        args.save_proofs.mkdir(parents=True, exist_ok=True)
        (args.save_proofs / (path.stem + ".proof")).write_text(
            proof.group(0))
    return status, proof.group(0)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[3])
    ap.add_argument("--dir", default="problems/verdict", type=Path)
    ap.add_argument("--binary", default="vampire")
    ap.add_argument("--limit", type=int, default=30)
    ap.add_argument("--include", default="problems", type=Path,
                    help="root for include() directives; run_verdict.sh "
                         "passes the same")
    ap.add_argument("--no-avatar", action="store_true",
                    help="run Vampire with --avatar off")
    ap.add_argument("--proofs", type=Path,
                    help="read saved <stem>.proof files instead of running "
                         "Vampire")
    ap.add_argument("--save-proofs", type=Path,
                    help="save extracted proof blocks here")
    ap.add_argument("--problem", help="one problem id, both queries")
    ap.add_argument("--show", action="store_true",
                    help="print every step result, not only failures")
    ap.add_argument("--json", type=Path, help="write the report here")
    args = ap.parse_args()

    files = sorted(args.dir.glob("*.p"))
    if args.problem:
        files = [f for f in files if f.stem.startswith(args.problem)]
    if not files:
        print(f"no .p files in {args.dir}", file=sys.stderr)
        return 1

    report = {}
    suite_unsupported = defaultdict(set)
    suite_premises = Counter()
    counts = Counter()

    for f in files:
        status, proof = obtain_proof(f, args)
        if not proof:
            report[f.stem] = {"result": status.upper()}
            counts[status.upper()] += 1
            print(f"{f.stem:16} {status.upper()}")
            continue
        try:
            query = load_query(f, args.include)
            verdict, results, unsup, pclasses = check_proof(proof, query)
        except ParseError as e:
            report[f.stem] = {"result": "PARSE_ERROR", "detail": str(e)}
            counts["PARSE_ERROR"] += 1
            print(f"{f.stem:16} PARSE_ERROR      {e}")
            continue
        counts[verdict] += 1
        suite_premises.update(pclasses)
        for rule in unsup:
            suite_unsupported[rule].add(f.stem)
        nsteps = len(results)
        nbad = sum(1 for r in results if r[3] != "ok")
        print(f"{f.stem:16} {verdict:17} {nsteps:4} steps, "
              f"{nbad} not verified")
        shown = results if args.show else \
            [r for r in results if r[3] != "ok"]
        for sid, kind, rule, st, d in shown:
            print(f"    {sid:8} {kind:10} {rule:34} {st:10} {d}")
        report[f.stem] = {
            "result": verdict,
            "steps": nsteps,
            "unverified": nbad,
            "premise_classes": dict(pclasses),
            "failures": [
                {"step": sid, "kind": kind, "rule": rule,
                 "status": st, "detail": d}
                for sid, kind, rule, st, d in results if st != "ok"],
        }

    print()
    print("suite summary")
    for k in ("FULLY_CHECKED", "PARTIALLY_CHECKED", "REJECTED"):
        print(f"  {k:18} {counts.get(k, 0)}")
    other = {k: v for k, v in counts.items()
             if k not in ("FULLY_CHECKED", "PARTIALLY_CHECKED", "REJECTED")}
    if other:
        print(f"  other              {dict(other)}")
    if suite_unsupported:
        print()
        print("unsupported mechanisms and the problems needing them")
        for rule, ids in sorted(suite_unsupported.items(),
                                key=lambda kv: -len(kv[1])):
            names = ", ".join(sorted(ids)[:6])
            more = " ..." if len(ids) > 6 else ""
            print(f"  {len(ids):3}  {rule:40} {names}{more}")
    print()
    print("premise classes cited across all checked refutations")
    for cls, n in suite_premises.most_common():
        flag = "  <- review naming" if cls == "unclassified" else ""
        print(f"  {n:5}  {cls}{flag}")

    if args.json:
        args.json.write_text(json.dumps({
            "problems": report,
            "summary": dict(counts),
            "unsupported": {r: sorted(ids)
                            for r, ids in suite_unsupported.items()},
            "premise_classes": dict(suite_premises),
        }, indent=2))
        print(f"\nreport written to {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())