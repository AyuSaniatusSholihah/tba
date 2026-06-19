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

def validate_dfa(states, alphabet, transitions, start, accepts):
    """
    Validasi konsistensi definisi DFA.
    Mengembalikan list pasangan (state, simbol) yang transisinya belum
    didefinisikan (DFA tidak total -> dianggap implisit menuju trap/reject).
    Melempar ValueError jika ditemukan inkonsistensi fatal:
      - states/alfabet kosong
      - start state tidak terdaftar di states
      - ada accepting state yang tidak terdaftar di states
      - ada state asal/tujuan pada transisi yang tidak terdaftar di states
      - ada simbol pada transisi yang tidak terdaftar di alfabet
    """
    errors = []

    if not states:
        errors.append("Himpunan states tidak boleh kosong.")
    if not alphabet:
        errors.append("Alfabet tidak boleh kosong.")

    if not start:
        errors.append("Start state tidak boleh kosong.")
    elif start not in states:
        errors.append(
            f"Start state '{start}' tidak terdaftar pada himpunan states {sorted(states)}."
        )

    invalid_accepts = set(accepts) - set(states)
    if invalid_accepts:
        errors.append(
            f"Accepting state {sorted(invalid_accepts)} tidak terdaftar pada himpunan "
            f"states {sorted(states)}. Periksa kembali ejaan nama state."
        )

    invalid_from, invalid_to, invalid_symbols = set(), set(), set()
    for (frm, sym), to in transitions.items():
        if frm not in states:
            invalid_from.add(frm)
        if to not in states:
            invalid_to.add(to)
        if sym not in alphabet:
            invalid_symbols.add(sym)

    if invalid_from:
        errors.append(
            f"State asal pada transisi tidak terdaftar di states: {sorted(invalid_from)}."
        )
    if invalid_to:
        errors.append(
            f"State tujuan pada transisi tidak terdaftar di states: {sorted(invalid_to)}."
        )
    if invalid_symbols:
        errors.append(
            f"Simbol pada transisi tidak terdaftar di alfabet: {sorted(invalid_symbols)}."
        )

    if errors:
        raise ValueError(" | ".join(errors))

    # Pengecekan lunak (tidak fatal): kelengkapan fungsi transisi.
    # DFA yang tidak total tetap diizinkan (pasangan yang hilang dianggap
    # menuju trap state implisit / reject), tapi dilaporkan agar user sadar.
    missing = [
        (s, a) for s in sorted(states) for a in sorted(alphabet)
        if (s, a) not in transitions
    ]
    return missing


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
        self.incomplete_transitions = validate_dfa(
            self.states, self.alphabet, self.transitions, self.start, self.accepts
        )

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
    p = pattern.replace(" ", "")

    # Validasi sebelum parsing: tangkap pola yang parser terima
    # tapi secara semantik hampir pasti typo.
    if pyre.search(r'\|[\s]*[)|]|\|[\s]*$|^[\s]*\|', p):
        raise ValueError(
            "Operator '|' membutuhkan operand di kedua sisinya "
            "(contoh: 'a|' atau '|b' atau 'a||b' tidak valid)."
        )
    if pyre.search(r'[*+?]{2,}', p):
        raise ValueError(
            "Kuantifier tidak boleh berurutan "
            "(contoh: 'a**', 'a+*', 'a?+' tidak valid)."
        )

    parser = RegexParser(pattern)
    ast = parser.parse()
    return parser.to_nfa(ast)


# =====================================================================
# =================== Minimisasi DFA ==================================
# =====================================================================

class MinimizationResult(DFA):
    """
    Hasil minimisasi DFA. Subclass dari DFA (bukan wrapper terpisah) supaya
    semua kode yang sudah memakai hasil minimize_dfa() sebagai objek DFA
    biasa (mis. minimized.states, minimized.run(), build_dfa_graph(minimized))
    tetap berfungsi tanpa perubahan apapun — isinstance(result, DFA) == True,
    dan seluruh atribut/method DFA tetap tersedia persis seperti sebelumnya.

    Field tambahan (murni informasional, tidak memengaruhi behavior DFA):
      unreachable_states : list state pada DFA asli yang dihapus karena
                           tidak reachable dari start state, SEBELUM proses
                           partition refinement dimulai.
      partition_steps    : list of dict, satu entri per iterasi refinement.
                           Tiap entri: {"label": "P0", "groups": [["q0","q1"], ["q2"]]}
                           P0 = partisi awal (accepting vs non-accepting),
                           P1, P2, ... = hasil tiap iterasi split berikutnya,
                           sampai partisi stabil (tidak ada split lagi).
      state_mapping       : dict {nama_state_baru: list(state_lama_anggota)},
                           urutan key mengikuti urutan pembuatan state baru.
    """
    def __init__(self, states, alphabet, transitions, start, accepts,
                unreachable_states, partition_steps, state_mapping):
        super().__init__(states, alphabet, transitions, start, accepts)
        self.unreachable_states = unreachable_states
        self.partition_steps = partition_steps
        self.state_mapping = state_mapping


def minimize_dfa(dfa: DFA):
    """Minimisasi DFA menggunakan algoritma Partition Refinement (Table-Filling).

    PENTING: algoritma inti (langkah 1-4 di bawah) TIDAK DIUBAH SAMA SEKALI
    dari versi sebelumnya — DFA minimal yang dihasilkan persis identik.
    Yang baru hanyalah PENCATATAN proses (state tak-reachable yang dibuang,
    partisi tiap iterasi, pemetaan state baru->lama) untuk ditampilkan di UI.
    Return value berubah dari DFA murni menjadi MinimizationResult (subclass
    DFA), supaya kode lama yang memperlakukan hasilnya sebagai objek DFA
    biasa tetap berfungsi tanpa perubahan.
    """
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
    unreachable_states = sorted(s for s in states if s not in reachable)
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

    def snapshot(label, groups):
        return {
            "label": label,
            "groups": [sorted(g) for g in groups],
        }

    partition_steps = [snapshot("P0", partitions)]

    # 3. Refinement loop
    changed = True
    iteration = 1
    while changed:
        changed = False
        new_partitions = []
        for group in partitions:
            splitter = {}
            for s in sorted(group):
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
        if changed:
            partition_steps.append(snapshot(f"P{iteration}", partitions))
            iteration += 1

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

    state_mapping = {name: sorted(g) for g, name in group_name.items()}

    return MinimizationResult(
        set(group_name.values()), dfa.alphabet, new_transitions, new_start, new_accepts,
        unreachable_states=unreachable_states,
        partition_steps=partition_steps,
        state_mapping=state_mapping,
    )


# =====================================================================
# =================== Ekuivalensi DFA =================================
# =====================================================================

def dfa_equivalent(dfa1: DFA, dfa2: DFA):
    """
    Cek ekuivalensi dua DFA menggunakan Product Construction + BFS.

    PENTING: logika inti (kapan return False, kapan return True, isi
    distinguishing_string) TIDAK DIUBAH dari versi sebelumnya — hasilnya
    identik. Yang baru adalah pencatatan explored_pairs untuk ditampilkan
    di UI sebagai bukti BFS sudah mengeksplorasi seluruh pasangan state
    yang reachable tanpa menemukan perbedaan status accept.

    Return (is_equivalent: bool, distinguishing_string: str or None,
            explored_pairs: list of (s1, s2) dalam urutan dieksplorasi BFS)
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
    explored_pairs = []

    while queue:
        s1, s2, path = queue.pop(0)
        explored_pairs.append((s1, s2))
        if is_accept(dfa1, s1) != is_accept(dfa2, s2):
            return False, (path if path != "" else "(string kosong / epsilon)"), explored_pairs
        for sym in alphabet:
            n1 = step(dfa1, s1, sym)
            n2 = step(dfa2, s2, sym)
            pair = (n1, n2)
            if pair not in visited:
                visited.add(pair)
                queue.append((n1, n2, path + sym))

    return True, None, explored_pairs
