"""
utils.py
========
Fungsi visualisasi: membangun Graphviz graph dan meng-inject animasi ke SVG.
Tidak mengandung CSS langsung — semua desain diimpor dari styles.py.
"""

import re
import graphviz
from engine import EPSILON
from styles import (
    ANIM_CSS, SVG_WRAPPER,
    COLOR_BASE, COLOR_SURFACE0,
    COLOR_GREEN, COLOR_RED, COLOR_YELLOW, COLOR_BLUE,
    COLOR_SURFACE1, COLOR_TEXT,
)


# =====================================================================
# =================== Helper warna node/edge ==========================
# =====================================================================

def _node_colors(is_active, accepted):
    """Return (color, fillcolor, fontcolor, penwidth) untuk sebuah state node."""
    if is_active:
        if accepted is True:
            return COLOR_GREEN, COLOR_GREEN, COLOR_BASE, "3"
        elif accepted is False:
            return COLOR_RED, COLOR_RED, COLOR_BASE, "3"
        else:
            return COLOR_YELLOW, COLOR_YELLOW, COLOR_BASE, "3"
    return COLOR_BLUE, COLOR_SURFACE1, COLOR_TEXT, "1.5"


def _edge_color(is_active):
    return (COLOR_YELLOW, "2.5") if is_active else ("#6c7086", "1.2")


_GRAPH_ATTRS = {"rankdir": "LR", "bgcolor": COLOR_BASE, "fontname": "Helvetica"}


# =====================================================================
# =================== Graphviz graph builders =========================
# =====================================================================

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
            fontcolor=fontcolor, fontname="Helvetica", penwidth=penwidth,
        )

    for (from_s, sym), to_s in dfa.transitions.items():
        is_active_edge = (
            highlight_edge is not None
            and str(from_s) == str(highlight_edge[0])
            and sym == highlight_edge[1]
        )
        ec, ep = _edge_color(is_active_edge)
        dot.edge(str(from_s), str(to_s), label=f" {sym} ",
                 color=ec, fontcolor=COLOR_TEXT, fontname="Helvetica", penwidth=ep)
    return dot


def build_nfa_graph(nfa, highlight_states=None, highlight_edges=None, accepted=None):
    """Bangun Graphviz Digraph untuk NFA, dengan optional highlight state/edge."""
    dot = graphviz.Digraph(graph_attr=_GRAPH_ATTRS)
    dot.node("__start__", shape="point", style="invis")
    dot.edge("__start__", str(nfa.start), color=COLOR_TEXT, arrowhead="vee")

    active_set = {str(s) for s in highlight_states} if highlight_states else set()

    for state in nfa.states:
        is_active = str(state) in active_set
        color, fillcolor, fontcolor, penwidth = _node_colors(is_active, accepted if is_active else None)
        dot.node(
            str(state),
            shape="doublecircle" if state in nfa.accepts else "circle",
            style="filled", fillcolor=fillcolor, color=color,
            fontcolor=fontcolor, fontname="Helvetica", penwidth=penwidth,
        )

    # Gabungkan label edge dengan tujuan yang sama
    edge_map = {}
    for (from_s, sym), targets in nfa.transitions.items():
        label = "ε" if sym == EPSILON else sym
        for to_s in targets:
            edge_map.setdefault((str(from_s), str(to_s)), []).append(label)

    active_edges = set()
    if highlight_edges:
        for (fs, sym) in highlight_edges:
            for to_s in nfa.transitions.get((fs, sym), set()):
                active_edges.add((str(fs), str(to_s)))

    for (from_s, to_s), labels in edge_map.items():
        ec, ep = _edge_color((from_s, to_s) in active_edges)
        dot.edge(from_s, to_s, label=f" {','.join(sorted(labels))} ",
                 color=ec, fontcolor=COLOR_TEXT, fontname="Helvetica", penwidth=ep)
    return dot


# =====================================================================
# =================== SVG + Animasi CSS ================================
# =====================================================================

def _inject_animations(svg_str, highlight_states, accepted):
    """
    Suntikkan CSS animation class ke dalam SVG dari graphviz.
    Graphviz SVG: tiap node = <g id="nodeN" class="node"><title>NAMA_STATE</title>...
    """
    if not highlight_states:
        return re.sub(r"(<svg[^>]*>)", r"\1" + ANIM_CSS, svg_str, count=1)

    active_names = {str(s) for s in highlight_states}
    anim_class = (
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
                group = re.sub(r'class="node"', f'class="node {anim_class}"', group, count=1)
        return group

    svg_patched = re.sub(
        r'<g id="node\d+"[^>]*class="node"[^>]*>.*?</g>',
        patch_node, svg_str, flags=re.DOTALL
    )
    return re.sub(r"(<svg[^>]*>)", r"\1" + ANIM_CSS, svg_patched, count=1)


# =====================================================================
# =================== Public render functions =========================
# =====================================================================

def render_dfa_animated(dfa, highlight_state=None, highlight_edge=None,
                        accepted=None, height=380):
    """
    Render DFA → HTML string dengan animasi SVG pada state aktif.
    Gunakan: st.components.v1.html(render_dfa_animated(...), height=...)
    """
    dot = build_dfa_graph(dfa, highlight_state=highlight_state,
                          highlight_edge=highlight_edge, accepted=accepted)
    svg = dot.pipe(format="svg").decode("utf-8")
    animated = _inject_animations(svg, {str(highlight_state)} if highlight_state else set(), accepted)
    return SVG_WRAPPER.format(bg=COLOR_BASE, border=COLOR_SURFACE0, height=height, svg=animated)


def render_nfa_animated(nfa, highlight_states=None, highlight_edges=None,
                        accepted=None, height=380):
    """
    Render NFA → HTML string dengan animasi SVG pada state aktif.
    Gunakan: st.components.v1.html(render_nfa_animated(...), height=...)
    """
    dot = build_nfa_graph(nfa, highlight_states=highlight_states,
                          highlight_edges=highlight_edges, accepted=accepted)
    svg = dot.pipe(format="svg").decode("utf-8")
    animated = _inject_animations(svg, highlight_states or set(), accepted)
    return SVG_WRAPPER.format(bg=COLOR_BASE, border=COLOR_SURFACE0, height=height, svg=animated)
