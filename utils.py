"""
utils.py
Fungsi pembantu: parsing input transisi & visualisasi Graphviz.
"""

import re
import graphviz
import pandas as pd
from engine import EPSILON


# =====================================================================
# ====================== DFA Transition Table Helper ==================
# =====================================================================

def build_dfa_transition_table(dfa):
    """
    Bangun tabel transisi DFA sebagai pandas DataFrame: baris = state,
    kolom = simbol alfabet. Sel berisi state tujuan, atau '—' kalau
    transisi tidak didefinisikan (DFA tidak total / trap state implisit).
    State start ditandai '→' dan accepting state ditandai '*' di depan
    nama barisnya (indeks), murni kosmetik untuk tabel — tidak mengubah
    data DFA sama sekali.
    """
    states = sorted(dfa.states)
    alphabet = sorted(dfa.alphabet)

    def row_label(s):
        prefix = ""
        if s == dfa.start:
            prefix += "→"
        if s in dfa.accepts:
            prefix += "*"
        return f"{prefix}{s}" if prefix else s

    data = {}
    for a in alphabet:
        data[a] = [dfa.transitions.get((s, a), "—") for s in states]

    df = pd.DataFrame(data, index=[row_label(s) for s in states])
    df.index.name = "State"
    return df


# =====================================================================
# ====================== NFA Visualization Helper =====================
# =====================================================================

def epsilon_closure_with_trace(nfa, entry_states):
    """
    Hitung ε-closure dari entry_states, SEKALIGUS lacak:
      - derived: state yang ikut aktif HANYA karena ε (bukan entry_states itu sendiri)
      - epsilon_edge_pairs: set (from_state, to_state) PERSIS yang dilewati
        (bukan cuma "from_state mana saja yang punya ε keluar" — satu state
        bisa punya beberapa target ε, dan kita cuma mau yang BENAR dilewati)

    Ini murni untuk kebutuhan VISUALISASI (membedakan node "entry langsung"
    vs "turunan ε" di graph, dan menyalakan edge ε yang relevan). Tidak
    mengubah/menggantikan NFA.epsilon_closure() di engine.py — engine.py
    tetap jadi satu-satunya sumber kebenaran untuk hasil eksekusi NFA.
    """
    stack = list(entry_states)
    closure = set(entry_states)
    epsilon_edge_pairs = set()
    while stack:
        s = stack.pop()
        for t in nfa.transitions.get((s, EPSILON), set()):
            epsilon_edge_pairs.add((s, t))
            if t not in closure:
                closure.add(t)
                stack.append(t)
    derived = closure - set(entry_states)
    return closure, derived, epsilon_edge_pairs


# =====================================================================
# ====================== Input Parser =================================
# =====================================================================

def parse_transitions_dfa(text):
    """
    Parse teks input transisi DFA menjadi dictionary Python.
    Format tiap baris: state_asal, simbol, state_tujuan
    Baris kosong dan baris diawali '#' diabaikan.

    Jika ditemukan dua baris dengan (state_asal, simbol) yang sama tapi
    state_tujuan berbeda, dianggap konflik/typo dan akan menghasilkan
    ValueError (DFA mensyaratkan transisi deterministik: satu pasangan
    (state, simbol) hanya boleh menuju satu state tujuan).
    """
    transitions = {}
    for line in text.strip().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = [p.strip() for p in line.split(',')]
        if len(parts) != 3:
            raise ValueError(
                f"Format salah: '{line}'. Gunakan: state_asal, simbol, state_tujuan"
            )
        frm, sym, to = parts
        key = (frm, sym)
        if key in transitions and transitions[key] != to:
            raise ValueError(
                f"Transisi konflik untuk ({frm}, {sym}): "
                f"sudah didefinisikan menuju '{transitions[key]}', "
                f"tapi baris lain mendefinisikan menuju '{to}'. "
                f"DFA harus deterministik — satu pasangan (state, simbol) "
                f"hanya boleh punya satu tujuan."
            )
        transitions[key] = to
    return transitions


from styles import (
    ANIM_CSS, SVG_WRAPPER,
    COLOR_BASE, COLOR_SURFACE0,
    COLOR_GREEN, COLOR_RED, COLOR_YELLOW, COLOR_PINK, COLOR_DERIVED,
    COLOR_SURFACE1, COLOR_SURFACE2, COLOR_TEXT,
)


# Helper Warna Node/Edge

def _node_colors(is_active, accepted):
    """Return (color, fillcolor, fontcolor, penwidth) untuk sebuah state node."""
    if is_active:
        if accepted is True:
            return COLOR_GREEN, COLOR_GREEN, COLOR_BASE, "3"
        elif accepted is False:
            return COLOR_RED, COLOR_RED, COLOR_BASE, "3"
        else:
            return COLOR_YELLOW, COLOR_YELLOW, COLOR_BASE, "3"
    return COLOR_PINK, COLOR_SURFACE1, COLOR_TEXT, "1.5"


def _derived_node_colors():
    """Warna untuk state yang aktif HANYA sebagai turunan ε-closure
    (bukan entry langsung via start/simbol) — redup, beda dari _node_colors aktif."""
    return COLOR_DERIVED, COLOR_DERIVED, COLOR_BASE, "2"


def _edge_color(is_active):
    return (COLOR_YELLOW, "2.5") if is_active else (COLOR_SURFACE2, "1.2")


_GRAPH_ATTRS = {"rankdir": "LR", "bgcolor": COLOR_BASE, "fontname": "JetBrains Mono,Courier New,monospace"}


# Graphviz Graph Builders

def build_dfa_graph(dfa, highlight_state=None, highlight_edge=None, accepted=None):
    """Bangun Graphviz Digraph untuk DFA, dengan optional highlight state/edge."""
    dot = graphviz.Digraph(graph_attr=_GRAPH_ATTRS)
    dot.node("__start__", shape="point", style="invis")
    dot.edge("__start__", str(dfa.start), color=COLOR_TEXT, arrowhead="vee")

    for state in dfa.states:
        is_active = str(state) == str(highlight_state)
        color, fillcolor, fontcolor, penwidth = _node_colors(is_active, accepted if is_active else None)
        dot.node(
            str(state),
            shape="doublecircle" if state in dfa.accepts else "circle",
            style="filled", fillcolor=fillcolor, color=color,
            fontcolor=fontcolor, fontname="JetBrains Mono,Courier New,monospace", penwidth=penwidth,
        )

    for (from_s, sym), to_s in dfa.transitions.items():
        is_active_edge = (
            highlight_edge is not None
            and str(from_s) == str(highlight_edge[0])
            and sym == highlight_edge[1]
        )
        ec, ep = _edge_color(is_active_edge)
        dot.edge(str(from_s), str(to_s), label=f" {sym} ",
                 color=ec, fontcolor=COLOR_TEXT, fontname="JetBrains Mono,Courier New,monospace", penwidth=ep)
    return dot


def build_nfa_graph(nfa, highlight_states=None, highlight_edges=None, accepted=None,
                    derived_states=None, highlight_epsilon_pairs=None):
    """Bangun Graphviz Digraph untuk NFA, dengan optional highlight state/edge.

    highlight_states : semua state yang aktif pada step ini (entry + turunan ε)
    derived_states    : subset dari highlight_states yang aktif HANYA karena
                        ε-closure (bukan entry langsung via start/simbol) —
                        diwarnai redup & beda supaya jejak alur ε kebaca.
    highlight_edges   : set pasangan (from_state, symbol) untuk transisi SIMBOL
                        BIASA (bukan ε) yang dilewati pada step ini.
    highlight_epsilon_pairs : set pasangan (from_state, to_state) EKSAK untuk
                        edge ε yang benar-benar dilewati. Dipisah dari
                        highlight_edges karena satu state bisa punya BEBERAPA
                        target ε sekaligus — kalau cuma dikasih (from, EPSILON)
                        tanpa target spesifik, semua targetnya akan ikut
                        ter-highlight padahal belum tentu semuanya dilewati.
    """
    dot = graphviz.Digraph(graph_attr=_GRAPH_ATTRS)
    dot.node("__start__", shape="point", style="invis")
    dot.edge("__start__", str(nfa.start), color=COLOR_TEXT, arrowhead="vee")

    active_set = {str(s) for s in highlight_states} if highlight_states else set()
    derived_set = {str(s) for s in derived_states} if derived_states else set()

    for state in nfa.states:
        s = str(state)
        is_active = s in active_set
        is_derived = is_active and s in derived_set
        if is_derived:
            color, fillcolor, fontcolor, penwidth = _derived_node_colors()
        else:
            color, fillcolor, fontcolor, penwidth = _node_colors(is_active, accepted if is_active else None)
        dot.node(
            s,
            shape="doublecircle" if state in nfa.accepts else "circle",
            style="filled", fillcolor=fillcolor, color=color,
            fontcolor=fontcolor, fontname="JetBrains Mono,Courier New,monospace", penwidth=penwidth,
        )

    # Gabungkan label edge dengan tujuan yang sama
    edge_map = {}
    for (from_s, sym), targets in nfa.transitions.items():
        label = "ε" if sym == EPSILON else sym
        for to_s in targets:
            edge_map.setdefault((str(from_s), str(to_s)), []).append(label)

    # active_edges: edge dilewati via simbol biasa (solid highlight)
    active_edges = set()
    if highlight_edges:
        for (fs, sym) in highlight_edges:
            for to_s in nfa.transitions.get((fs, sym), set()):
                active_edges.add((str(fs), str(to_s)))

    # active_epsilon_edges: pasangan (from,to) EKSAK untuk ε yang dilewati
    active_epsilon_edges = {
        (str(fs), str(ts)) for (fs, ts) in (highlight_epsilon_pairs or set())
    }

    for (from_s, to_s), labels in edge_map.items():
        pair = (from_s, to_s)
        if pair in active_epsilon_edges:
            # Edge ε yang dilewati: warna derived + style dashed (beda dari edge simbol aktif)
            ec, ep = COLOR_DERIVED, "2.2"
            edge_style = "dashed"
        else:
            is_active_edge = pair in active_edges
            ec, ep = _edge_color(is_active_edge)
            edge_style = "solid"
        dot.edge(from_s, to_s, label=f" {','.join(sorted(labels))} ",
                 color=ec, fontcolor=COLOR_TEXT, fontname="JetBrains Mono,Courier New,monospace",
                 penwidth=ep, style=edge_style)
    return dot


# Pengaturan SVG dan Animasi

def _inject_animations(svg_str, highlight_states, accepted, derived_states=None):
    """
    Suntikkan CSS animation class ke dalam SVG dari graphviz.
    Graphviz SVG: tiap node = <g id="nodeN" class="node"><title>NAMA_STATE</title>...

    highlight_states : semua state aktif (dapat class state-active/accepted/rejected)
    derived_states    : subset yang aktif HANYA karena ε-closure -> dapat
                        class state-derived (redup) sebagai pengganti, BUKAN tambahan.
    """
    if not highlight_states:
        return re.sub(r"(<svg[^>]*>)", r"\1" + ANIM_CSS, svg_str, count=1)

    active_names = {str(s) for s in highlight_states}
    derived_names = {str(s) for s in derived_states} if derived_states else set()
    entry_anim_class = (
        "state-accepted" if accepted is True
        else "state-rejected" if accepted is False
        else "state-active"
    )

    def patch_node(match):
        group = match.group(0)
        title_m = re.search(r"<title>(.*?)</title>", group, re.DOTALL)
        if title_m:
            title = (title_m.group(1)
                     .replace("&amp;", "&").replace("&lt;", "<")
                     .replace("&gt;", ">").replace("&#45;", "-").replace("&quot;", '"'))
            if title in active_names:
                anim_class = "state-derived" if title in derived_names else entry_anim_class
                group = re.sub(r'class="node"', f'class="node {anim_class}"', group, count=1)
        return group

    svg_patched = re.sub(
        r'<g id="node\d+"[^>]*class="node"[^>]*>.*?</g>',
        patch_node, svg_str, flags=re.DOTALL
    )
    return re.sub(r"(<svg[^>]*>)", r"\1" + ANIM_CSS, svg_patched, count=1)


# Fungsi Render Publik

def render_dfa_animated(dfa, highlight_state=None, highlight_edge=None,
                        accepted=None, height=380):
    """
    Render DFA → HTML string dengan animasi SVG pada state aktif.
    Gunakan: st.components.v1.html(render_dfa_animated(...), height=...)
    """
    dot = build_dfa_graph(dfa, highlight_state=highlight_state,
                          highlight_edge=highlight_edge, accepted=accepted)
    try:
        svg = dot.pipe(format="svg").decode("utf-8")
    except Exception:
        return (
            f'<div style="background:{COLOR_BASE};border-radius:12px;padding:20px;'
            f'border:1px solid {COLOR_SURFACE0};color:#E08989;font-family:monospace;">'
            f'⚠️ Graphviz tidak ditemukan. Pastikan sudah terinstall dan PATH sudah diset, '
            f'lalu restart VS Code / terminal.</div>'
        )
    animated = _inject_animations(svg, {str(highlight_state)} if highlight_state else set(), accepted)
    return SVG_WRAPPER.format(bg=COLOR_BASE, border=COLOR_SURFACE0, height=height, svg=animated)


def render_nfa_animated(nfa, highlight_states=None, highlight_edges=None,
                        accepted=None, height=380, derived_states=None,
                        highlight_epsilon_pairs=None):
    """
    Render NFA → HTML string dengan animasi SVG pada state aktif.
    Gunakan: st.components.v1.html(render_nfa_animated(...), height=...)

    derived_states : subset highlight_states yang aktif HANYA karena ε-closure
                     (bukan entry langsung) — diberi warna & animasi redup terpisah
                     supaya jejak alur ε-closure kebaca dari node mana asalnya.
    highlight_epsilon_pairs : set pasangan (from_state, to_state) EKSAK untuk
                     edge ε yang dilewati pada step ini.
    """
    dot = build_nfa_graph(nfa, highlight_states=highlight_states,
                          highlight_edges=highlight_edges, accepted=accepted,
                          derived_states=derived_states,
                          highlight_epsilon_pairs=highlight_epsilon_pairs)
    try:
        svg = dot.pipe(format="svg").decode("utf-8")
    except Exception:
        return (
            f'<div style="background:{COLOR_BASE};border-radius:12px;padding:20px;'
            f'border:1px solid {COLOR_SURFACE0};color:#E08989;font-family:monospace;">'
            f'⚠️ Graphviz tidak ditemukan. Pastikan sudah terinstall dan PATH sudah diset, '
            f'lalu restart VS Code / terminal.</div>'
        )
    animated = _inject_animations(svg, highlight_states or set(), accepted, derived_states=derived_states)
    return SVG_WRAPPER.format(bg=COLOR_BASE, border=COLOR_SURFACE0, height=height, svg=animated)