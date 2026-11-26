"""
policy.py
=========
Reads ODRL policies out of Turtle, as the trees the compiler uses.

A tree has one item per constraint of the policy's permission, a
compile.Constraint, or an And, an Or or a Xone for a Logical Constraint.  Each
atomic constraint records the policy it belongs to, and a list of right
operands is the values of one constraint, in order.  What has no such reading
is refused, and never read as the conjunction of its parts: odrl:andSequence;
a Logical Constraint within another, or over several left operands; several
rules, a prohibition or an obligation; a constraint of a duty, or a refinement.
"""

try:
    from rdflib import BNode, Graph, Namespace, RDF
    from rdflib.collection import Collection
except ImportError:                                   # pragma: no cover
    Graph = None

from compile import SET_OPERATORS, And, Constraint, Or, Xone

ODRL = "http://www.w3.org/ns/odrl/2/"

RULES = ("permission", "prohibition", "obligation")

# The connectives of ODRL, and the tree item of each.  andSequence has none.
CONNECTIVES = {"and": And, "or": Or, "xone": Xone, "andSequence": None}


class PolicyError(Exception):
    """A policy that does not read as a tree."""


def _slug(iri: str) -> str:
    """A TPTP constant for an IRI.  Stable, lowercase, prefix preserved."""
    tail = iri.rstrip("/").rsplit("/", 1)[-1].rsplit("#", 1)[-1]
    return "".join(ch if ch.isalnum() else "_" for ch in tail).lower()


def _local(uri) -> str:
    s = str(uri)
    return s.rsplit("#", 1)[-1].rsplit("/", 1)[-1]


def policies(g) -> list:
    """The policies of a graph: every subject of a rule, in order of its IRI."""
    O = Namespace(ODRL)
    return sorted({p for kind in RULES for p in g.subjects(O[kind], None)},
                  key=str)


def read_policy(source, side: str, policy=None, constant=None) -> dict:
    """The tree of one policy: each left operand, and its items in conjunction.

    source is a Turtle file or a graph.  policy names the policy to read, and
    without it the source must hold one.  side is the policy of each atomic
    constraint, as the tree records it.  constant turns a value into the
    constant that stands for it.

    The items of a rule have no order in RDF; they are read in the order of
    their IRIs.  The constraints of a Logical Constraint and the values of a
    set operator are lists, and keep their order.
    """
    g = source if isinstance(source, Graph) else \
        Graph().parse(source, format="turtle")
    O = Namespace(ODRL)
    constant = constant or (lambda v: _slug(str(v)))
    every = policies(g)
    if policy is None:
        if len(every) != 1:
            raise PolicyError(f"{len(every)} policies, where one is read")
        policy = every[0]
    elif policy not in every:
        raise PolicyError(f"no policy {policy}")

    rules = [(kind, r) for kind in RULES for r in g.objects(policy, O[kind])]
    if [kind for kind, _ in rules] != ["permission"]:
        raise PolicyError(
            f"{policy}: its rules are {', '.join(k for k, _ in rules)}; a tree "
            f"is read from one permission")
    stray = _constraints(g).difference(*(_reached(g, p) for p in every))
    if stray:
        raise PolicyError(
            f"{', '.join(sorted(map(_name, stray)))}: not a constraint of a "
            f"rule (a refinement, a duty's constraint, or one no rule names)")

    tree = {}
    for node in sorted(g.objects(rules[0][1], O.constraint), key=str):
        operand, item = _item(g, node, side, constant)
        tree.setdefault(operand, []).append(item)
    return tree


def _constraints(g) -> set:
    """Every node written as a constraint, atomic or logical."""
    O = Namespace(ODRL)
    return {s for p in ("leftOperand", *CONNECTIVES)
            for s in g.subjects(O[p], None)}


def _reached(g, policy) -> set:
    """The constraints of a policy's rules, and those they combine."""
    O = Namespace(ODRL)
    todo = [c for kind in RULES for r in g.objects(policy, O[kind])
            for c in g.objects(r, O.constraint)]
    seen = set()
    while todo:
        node = todo.pop()
        if node not in seen:
            seen.add(node)
            todo += [m for conn in CONNECTIVES
                     for head in g.objects(node, O[conn])
                     for m in (Collection(g, head) if _is_list(g, head)
                               else [head])]
    return seen


def _item(g, node, side, constant):
    """(left operand, item) of one constraint of a rule."""
    O = Namespace(ODRL)
    used = [conn for conn in CONNECTIVES if (node, O[conn], None) in g]
    if not used:
        return _atom(g, node, side, constant)
    if len(used) > 1 or (node, O.leftOperand, None) in g:
        raise PolicyError(f"{_name(node)}: a constraint is atomic, or has one "
                          f"connective")
    kind = CONNECTIVES[used[0]]
    if kind is None:
        raise PolicyError(f"{_name(node)}: odrl:{used[0]} has no tree")
    head = _one(g, node, O[used[0]])
    members = list(Collection(g, head)) if _is_list(g, head) else []
    if not members:
        raise PolicyError(f"{_name(node)}: odrl:{used[0]} is not a list of "
                          f"constraints")
    for m in members:
        if any((m, O[conn], None) in g for conn in CONNECTIVES):
            raise PolicyError(f"{_name(node)}: combines a Logical Constraint, "
                              f"{_name(m)}; it combines atomic constraints")
    parts = [_atom(g, m, side, constant) for m in members]
    operands = sorted({operand for operand, _ in parts})
    if len(operands) > 1:
        raise PolicyError(f"{_name(node)}: combines constraints on "
                          f"{' and '.join(operands)}; a tree is on one left "
                          f"operand")
    return operands[0], kind(tuple(c for _, c in parts))


def _atom(g, node, side, constant):
    """(left operand, Constraint) of one atomic constraint."""
    O = Namespace(ODRL)
    operand = _one(g, node, O.leftOperand)
    operator = _one(g, node, O.operator)
    if not str(operator).startswith(ODRL):
        raise PolicyError(f"{_name(node)}: {operator} is not an ODRL operator")
    op = _local(operator)
    right = sorted(g.objects(node, O.rightOperand), key=str)
    if any(_is_list(g, v) for v in right):
        if len(right) > 1 or op not in SET_OPERATORS:
            raise PolicyError(f"{_name(node)}: {op} with a list where it takes "
                              f"one value, or with a list and another value")
        right = list(Collection(g, right[0]))
    if not right or any(isinstance(v, BNode) for v in right):
        raise PolicyError(f"{_name(node)}: no right operand, or one that is "
                          f"neither an IRI nor a literal")
    return _local(operand), Constraint(op, tuple(map(constant, right)), side)


def _one(g, node, prop):
    found = list(g.objects(node, prop))
    if len(found) != 1:
        raise PolicyError(f"{_name(node)}: {len(found)} values of "
                          f"odrl:{_local(prop)}, where one is read")
    return found[0]


def _is_list(g, node) -> bool:
    return node == RDF.nil or (node, RDF.first, None) in g


def _name(node) -> str:
    return "a constraint without an IRI" if isinstance(node, BNode) else str(node)


def atoms(items) -> list:
    """The atomic constraints of a tree, in order."""
    return [c for item in items
            for c in (item.alts if isinstance(item, (And, Or, Xone)) else (item,))]


def by_operand(*trees):
    """The trees of several policies as one: each left operand, and the items
    of every policy on it in conjunction."""
    out = {}
    for tree in trees:
        for operand, items in tree.items():
            out.setdefault(operand, []).extend(items)
    return out
