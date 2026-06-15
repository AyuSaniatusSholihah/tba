"""
utils.py
========
Fungsi visualisasi Graphviz untuk DFA dan NFA.
Mendukung animasi CSS pada state aktif via SVG injection.
"""

import re
import graphviz
from engine import EPSILON


# ── Graphviz graph builder (untuk st.graphviz_chart / static) ────────────

def build_dfa_graph(dfa, highlight_state=None, highlight_edge=None, accepted=None):
    dot = graphviz.Digraph(graph_attr={'rankdir': 'LR', 'bgcolor': '#1e1e2e', 'fontname': 'Helvetica'})
    dot.node('__start__', shape='point', style='invis')
    dot.edge('__start__', str(dfa.start), color='#cdd6f4', arrowhead='vee')

    for state in dfa.states:
        is_final = state in dfa.accepts
        is_active = str(state) == str(highlight_state)

        if is_active:
            if accepted is True:
                color, fillcolor, fontcolor = '#a6e3a1', '#a6e3a1', '#1e1e2e'
            elif accepted is False:
                color, fillcolor, fontcolor = '#f38ba8', '#f38ba8', '#1e1e2e'
            else:
                color, fillcolor, fontcolor = '#f9e2af', '#f9e2af', '#1e1e2e'
            penwidth = '3'
        else:
            color, fillcolor, fontcolor = '#89b4fa', '#313244', '#cdd6f4'
            penwidth = '1.5'

        dot.node(str(state), shape='doublecircle' if is_final else 'circle',
                 style='filled', fillcolor=fillcolor, color=color,
                 fontcolor=fontcolor, fontname='Helvetica', penwidth=penwidth)

    for (from_s, sym), to_s in dfa.transitions.items():
        is_active_edge = (highlight_edge and str(from_s) == str(highlight_edge[0]) and sym == highlight_edge[1])
        dot.edge(str(from_s), str(to_s), label=f' {sym} ',
                 color='#f9e2af' if is_active_edge else '#6c7086',
                 fontcolor='#cdd6f4', fontname='Helvetica',
                 penwidth='2.5' if is_active_edge else '1.2')
    return dot


def build_nfa_graph(nfa, highlight_states=None, highlight_edges=None, accepted=None):
    dot = graphviz.Digraph(graph_attr={'rankdir': 'LR', 'bgcolor': '#1e1e2e', 'fontname': 'Helvetica'})
    dot.node('__start__', shape='point', style='invis')
    dot.edge('__start__', str(nfa.start), color='#cdd6f4', arrowhead='vee')

    active_set = {str(s) for s in highlight_states} if highlight_states else set()

    for state in nfa.states:
        is_final = state in nfa.accepts
        is_active = str(state) in active_set

        if is_active:
            if accepted is True:
                color, fillcolor, fontcolor = '#a6e3a1', '#a6e3a1', '#1e1e2e'
            elif accepted is False:
                color, fillcolor, fontcolor = '#f38ba8', '#f38ba8', '#1e1e2e'
            else:
                color, fillcolor, fontcolor = '#f9e2af', '#f9e2af', '#1e1e2e'
            penwidth = '3'
        else:
            color, fillcolor, fontcolor = '#89b4fa', '#313244', '#cdd6f4'
            penwidth = '1.5'

        dot.node(str(state), shape='doublecircle' if is_final else 'circle',
                 style='filled', fillcolor=fillcolor, color=color,
                 fontcolor=fontcolor, fontname='Helvetica', penwidth=penwidth)

    edge_map = {}
    for (from_s, sym), targets in nfa.transitions.items():
        label = 'ε' if sym == EPSILON else sym
        for to_s in targets:
            edge_map.setdefault((str(from_s), str(to_s)), []).append(label)

    active_edges = set()
    if highlight_edges:
        for (fs, sym) in highlight_edges:
            for to_s in nfa.transitions.get((fs, sym), set()):
                active_edges.add((str(fs), str(to_s)))

    for (from_s, to_s), labels in edge_map.items():
        is_active_edge = (from_s, to_s) in active_edges
        dot.edge(from_s, to_s, label=f' {",".join(sorted(labels))} ',
                 color='#f9e2af' if is_active_edge else '#6c7086',
                 fontcolor='#cdd6f4', fontname='Helvetica',
                 penwidth='2.5' if is_active_edge else '1.2')
    return dot


# ── CSS Animation Injection ──────────────────────────────────────────────

_ANIM_CSS = """
<style>
@keyframes glow-active {
    0%   { stroke: #f9e2af; stroke-width: 3; filter: drop-shadow(0 0 4px #f9e2af) drop-shadow(0 0 10px #f9e2af80); }
    50%  { stroke: #fab387; stroke-width: 4.5; filter: drop-shadow(0 0 10px #fab387) drop-shadow(0 0 22px #fab38780); }
    100% { stroke: #f9e2af; stroke-width: 3; filter: drop-shadow(0 0 4px #f9e2af) drop-shadow(0 0 10px #f9e2af80); }
}
@keyframes glow-accept {
    0%   { stroke: #a6e3a1; stroke-width: 3; filter: drop-shadow(0 0 4px #a6e3a1) drop-shadow(0 0 12px #a6e3a180); }
    50%  { stroke: #a6e3a1; stroke-width: 5; filter: drop-shadow(0 0 14px #a6e3a1) drop-shadow(0 0 28px #a6e3a1b0); }
    100% { stroke: #a6e3a1; stroke-width: 3; filter: drop-shadow(0 0 4px #a6e3a1) drop-shadow(0 0 12px #a6e3a180); }
}
@keyframes glow-reject {
    0%   { stroke: #f38ba8; stroke-width: 3; filter: drop-shadow(0 0 4px #f38ba8) drop-shadow(0 0 10px #f38ba880); }
    33%  { stroke: #f38ba8; stroke-width: 5; filter: drop-shadow(0 0 14px #f38ba8) drop-shadow(0 0 28px #f38ba8b0); }
    66%  { stroke: #f38ba8; stroke-width: 3; filter: drop-shadow(0 0 4px #f38ba8) drop-shadow(0 0 10px #f38ba880); }
    100% { stroke: #f38ba8; stroke-width: 5; filter: drop-shadow(0 0 14px #f38ba8) drop-shadow(0 0 28px #f38ba8b0); }
}
@keyframes scale-breathe {
    0%   { transform: scale(1);    }
    50%  { transform: scale(1.09); }
    100% { transform: scale(1);    }
}
.state-active ellipse, .state-active polygon {
    animation: glow-active 1s ease-in-out infinite;
    transform-origin: center;
    transform-box: fill-box;
}
.state-active text {
    animation: scale-breathe 1s ease-in-out infinite;
    transform-origin: center;
    transform-box: fill-box;
}
.state-accepted ellipse, .state-accepted polygon {
    animation: glow-accept 0.8s ease-in-out infinite;
    transform-origin: center;
    transform-box: fill-box;
}
.state-rejected ellipse, .state-rejected polygon {
    animation: glow-reject 0.5s ease-in-out 4;
    transform-origin: center;
    transform-box: fill-box;
}
svg { width: 100% !important; height: auto !important; }
</style>
"""


def _inject_animations(svg_str, highlight_states, accepted):
    """
    Parse SVG dari graphviz, tambahkan CSS animation class ke node yang aktif.
    Graphviz SVG: tiap node adalah <g id="nodeN" class="node"><title>STATE_NAME</title>...
    """
    if not highlight_states:
        svg_with_css = re.sub(r'(<svg[^>]*>)', r'\1' + _ANIM_CSS, svg_str, count=1)
        return svg_with_css

    active_names = {str(s) for s in highlight_states}

    if accepted is True:
        anim_class = 'state-accepted'
    elif accepted is False:
        anim_class = 'state-rejected'
    else:
        anim_class = 'state-active'

    def patch_node(m):
        group = m.group(0)
        title_m = re.search(r'<title>(.*?)</title>', group, re.DOTALL)
        if title_m:
            raw_title = title_m.group(1)
            # unescape HTML entities
            title = (raw_title
                     .replace('&amp;', '&').replace('&lt;', '<')
                     .replace('&gt;', '>').replace('&#45;', '-')
                     .replace('&quot;', '"'))
            if title in active_names:
                group = re.sub(r'class="node"', f'class="node {anim_class}"', group, count=1)
        return group

    # Match each node group (non-greedy, DOTALL)
    svg_str_patched = re.sub(
        r'<g id="node\d+"[^>]*class="node"[^>]*>.*?</g>',
        patch_node,
        svg_str,
        flags=re.DOTALL
    )

    # Inject CSS after opening <svg ...> tag
    svg_with_css = re.sub(r'(<svg[^>]*>)', r'\1' + _ANIM_CSS, svg_str_patched, count=1)
    return svg_with_css


def render_dfa_animated(dfa, highlight_state=None, highlight_edge=None, accepted=None, height=380):
    """
    Render DFA sebagai HTML dengan animasi CSS glow pada state aktif.
    Return: HTML string (gunakan dengan st.components.v1.html())
    """
    dot = build_dfa_graph(dfa, highlight_state=highlight_state,
                          highlight_edge=highlight_edge, accepted=accepted)
    svg_bytes = dot.pipe(format='svg')
    svg_str = svg_bytes.decode('utf-8')

    highlight_states = {str(highlight_state)} if highlight_state is not None else set()
    animated_svg = _inject_animations(svg_str, highlight_states, accepted)

    return f"""
    <div style="background:#1e1e2e; border-radius:12px; padding:10px;
                border:1px solid #313244; overflow:auto; height:{height}px;">
        {animated_svg}
    </div>
    """


def render_nfa_animated(nfa, highlight_states=None, highlight_edges=None, accepted=None, height=380):
    """
    Render NFA sebagai HTML dengan animasi CSS glow pada state aktif.
    Return: HTML string (gunakan dengan st.components.v1.html())
    """
    dot = build_nfa_graph(nfa, highlight_states=highlight_states,
                          highlight_edges=highlight_edges, accepted=accepted)
    svg_bytes = dot.pipe(format='svg')
    svg_str = svg_bytes.decode('utf-8')

    animated_svg = _inject_animations(svg_str, highlight_states or set(), accepted)

    return f"""
    <div style="background:#1e1e2e; border-radius:12px; padding:10px;
                border:1px solid #313244; overflow:auto; height:{height}px;">
        {animated_svg}
    </div>
    """
