"""
engine.py
=========
Implementasi manual DFA, NFA, Minimisasi, dan Ekuivalensi.
Tidak menggunakan library automata-lib – semua algoritma ditulis sendiri.
"""

import itertools
import re as pyre

EPSILON = "ε"


# =====================================================================
# ============================= DFA ===================================
# =====================================================================

class DFA:
    def __init__(self, states, alphabet, transitions, start, accepts):
        """
        states      : set/list of state names (string)
        alphabet    : set/list of symbols (string)
        transitions : dict {(state, symbol): next_state}
        start       : start state
        accepts     : set of accepting states
        """
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.transitions = dict(transitions)
        self.start = start
        self.accepts = set(accepts)

    def run(self, string):
        """
        Jalankan DFA pada string.
        Return (accepted: bool, trace: list of states)
        """
        current = self.start
        trace = [current]
        for ch in string:
            if ch not in self.alphabet:
                return False, trace
            key = (current, ch)
            if key not in self.transitions:
                return False, trace
            current = self.transitions[key]
            trace.append(current)
        return (current in self.accepts), trace


# =====================================================================
# ============================= NFA ===================================
# =====================================================================

class NFA:
    def __init__(self, states, alphabet, transitions, start, accepts):
        """
        transitions : dict {(state, symbol): set(states)}  symbol bisa EPSILON
        """
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.transitions = dict(transitions)
        self.start = start
        self.accepts = set(accepts)

    def epsilon_closure(self, states):
        stack = list(states)
        closure = set(states)
        while stack:
            s = stack.pop()
            for t in self.transitions.get((s, EPSILON), set()):
                if t not in closure:
                    closure.add(t)
                    stack.append(t)
        return frozenset(closure)

    def run(self, string):
        """
        Jalankan NFA pada string.
        Return (accepted: bool, trace: list of frozenset of states per step)
        """
        current = self.epsilon_closure({self.start})
        trace = [current]
        for ch in string:
            nxt = set()
            for s in current:
                for t in self.transitions.get((s, ch), set()):
                    nxt.add(t)
            current = self.epsilon_closure(nxt)
            trace.append(current)
            if not current:
                return False, trace
        accepted = any(s in self.accepts for s in current)
        return accepted, trace


# =====================================================================
# ============== Regex -> NFA (Thompson's Construction) ===============
# =====================================================================

class RegexParser:
    """Parser regex sederhana -> AST -> NFA via Thompson's construction."""

    def __init__(self, pattern):
        self.pattern = pattern.replace(" ", "")
        self.pos = 0
        self.counter = itertools.count()

    def new_state(self):
        return f"s{next(self.counter)}"

    def peek(self):
        if self.pos < len(self.pattern):
            return self.pattern[self.pos]
        return None

    def advance(self):
        ch = self.pattern[self.pos]
        self.pos += 1
        return ch

    def parse(self):
        ast = self.parse_regex()
        if self.pos != len(self.pattern):
            raise ValueError(f"Karakter tak terduga di posisi {self.pos}: '{self.pattern[self.pos:]}'")
        return ast

    def parse_regex(self):
        node = self.parse_term()
        while self.peek() == '|':
            self.advance()
            right = self.parse_term()
            node = ('union', node, right)
        return node

    def parse_term(self):
        factors = []
        while self.peek() is not None and self.peek() not in '|)':
            factors.append(self.parse_factor())
        if not factors:
            return ('epsilon',)
        node = factors[0]
        for f in factors[1:]:
            node = ('concat', node, f)
        return node

    def parse_factor(self):
        node = self.parse_base()
        while self.peek() in ('*', '+', '?'):
            op = self.advance()
            if op == '*':
                node = ('star', node)
            elif op == '+':
                node = ('plus', node)
            elif op == '?':
                node = ('optional', node)
        return node

    def parse_base(self):
        ch = self.peek()
        if ch == '(':
            self.advance()
            node = self.parse_regex()
            if self.peek() != ')':
                raise ValueError("Tanda kurung tidak seimbang, kurang ')'")
            self.advance()
            return node
        elif ch is not None and ch not in ('|', ')', '*', '+', '?', '(', EPSILON, '@'):
            self.advance()
            return ('symbol', ch)
        elif ch == EPSILON or ch == '@':
            self.advance()
            return ('epsilon',)
        else:
            raise ValueError(f"Karakter tidak valid di posisi {self.pos}: '{ch}'")

    def to_nfa(self, ast):
        states = set()
        transitions = {}
        alphabet = set()

        def add_trans(frm, sym, to):
            transitions.setdefault((frm, sym), set()).add(to)

        def build(node):
            kind = node[0]
            if kind == 'symbol':
                s = self.new_state()
                t = self.new_state()
                states.update([s, t])
                alphabet.add(node[1])
                add_trans(s, node[1], t)
                return s, t
            elif kind == 'epsilon':
                s = self.new_state()
                t = self.new_state()
                states.update([s, t])
                add_trans(s, EPSILON, t)
                return s, t
            elif kind == 'concat':
                s1, t1 = build(node[1])
                s2, t2 = build(node[2])
                add_trans(t1, EPSILON, s2)
                return s1, t2
            elif kind == 'union':
                s1, t1 = build(node[1])
                s2, t2 = build(node[2])
                s = self.new_state()
                t = self.new_state()
                states.update([s, t])
                add_trans(s, EPSILON, s1)
                add_trans(s, EPSILON, s2)
                add_trans(t1, EPSILON, t)
                add_trans(t2, EPSILON, t)
                return s, t
            elif kind == 'star':
                s1, t1 = build(node[1])
                s = self.new_state()
                t = self.new_state()
                states.update([s, t])
                add_trans(s, EPSILON, s1)
                add_trans(t1, EPSILON, t)
                add_trans(s, EPSILON, t)
                add_trans(t1, EPSILON, s1)
                return s, t
            elif kind == 'plus':
                s1, t1 = build(node[1])
                s = self.new_state()
                t = self.new_state()
                states.update([s, t])
                add_trans(s, EPSILON, s1)
                add_trans(t1, EPSILON, t)
                add_trans(t1, EPSILON, s1)
                return s, t
            elif kind == 'optional':
                s1, t1 = build(node[1])
                s = self.new_state()
                t = self.new_state()
                states.update([s, t])
                add_trans(s, EPSILON, s1)
                add_trans(t1, EPSILON, t)
                add_trans(s, EPSILON, t)
                return s, t
            else:
                raise ValueError(f"Node AST tidak dikenal: {kind}")

        start, end = build(ast)
        return NFA(states, alphabet, transitions, start, {end})


def regex_to_nfa(pattern):
    parser = RegexParser(pattern)
    ast = parser.parse()
    return parser.to_nfa(ast)


# =====================================================================
# =================== Minimisasi DFA ==================================
# =====================================================================

def minimize_dfa(dfa: DFA):
    """Minimisasi DFA menggunakan algoritma Partition Refinement (Table-Filling)."""
    states = sorted(dfa.states)
    alphabet = sorted(dfa.alphabet)

    # 1. Hilangkan state yang tidak reachable
    reachable = {dfa.start}
    frontier = [dfa.start]
    while frontier:
        s = frontier.pop()
        for a in alphabet:
            t = dfa.transitions.get((s, a))
            if t is not None and t not in reachable:
                reachable.add(t)
                frontier.append(t)
    states = [s for s in states if s in reachable]

    # 2. Partisi awal: accepting vs non-accepting
    accept_set = frozenset(s for s in states if s in dfa.accepts)
    nonaccept_set = frozenset(s for s in states if s not in dfa.accepts)
    partitions = [p for p in [accept_set, nonaccept_set] if p]

    def find_group(state, groups):
        for g in groups:
            if state in g:
                return g
        return None

    # 3. Refinement loop
    changed = True
    while changed:
        changed = False
        new_partitions = []
        for group in partitions:
            splitter = {}
            for s in group:
                signature = tuple(
                    find_group(dfa.transitions.get((s, a)), partitions)
                    for a in alphabet
                )
                splitter.setdefault(signature, set()).add(s)

            if len(splitter) == 1:
                new_partitions.append(group)
            else:
                changed = True
                for sub in splitter.values():
                    new_partitions.append(frozenset(sub))
        partitions = new_partitions

    # 4. Bangun DFA baru
    group_name = {g: f"q{i}" for i, g in enumerate(partitions)}

    def group_of(state):
        return find_group(state, partitions)

    new_start = group_name[group_of(dfa.start)]
    new_accepts = {name for g, name in group_name.items() if any(s in dfa.accepts for s in g)}
    new_transitions = {}
    for g, name in group_name.items():
        rep = next(iter(g))
        for a in alphabet:
            t = dfa.transitions.get((rep, a))
            if t is not None:
                new_transitions[(name, a)] = group_name[group_of(t)]

    return DFA(set(group_name.values()), dfa.alphabet, new_transitions, new_start, new_accepts)


# =====================================================================
# =================== Ekuivalensi DFA =================================
# =====================================================================

def dfa_equivalent(dfa1: DFA, dfa2: DFA):
    """
    Cek ekuivalensi dua DFA menggunakan Product Construction + BFS.
    Return (is_equivalent: bool, distinguishing_string: str or None)
    """
    alphabet = sorted(dfa1.alphabet | dfa2.alphabet)
    DEAD = "__DEAD__"

    def step(dfa, state, symbol):
        if state == DEAD:
            return DEAD
        return dfa.transitions.get((state, symbol), DEAD)

    def is_accept(dfa, state):
        return state != DEAD and state in dfa.accepts

    queue = [(dfa1.start, dfa2.start, "")]
    visited = {(dfa1.start, dfa2.start)}

    while queue:
        s1, s2, path = queue.pop(0)
        if is_accept(dfa1, s1) != is_accept(dfa2, s2):
            return False, (path if path != "" else "(string kosong / epsilon)")
        for sym in alphabet:
            n1 = step(dfa1, s1, sym)
            n2 = step(dfa2, s2, sym)
            pair = (n1, n2)
            if pair not in visited:
                visited.add(pair)
                queue.append((n1, n2, path + sym))

    return True, None
