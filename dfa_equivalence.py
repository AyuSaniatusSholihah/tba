"""
dfa_equivalence.py
Fitur 4: Cek Ekuivalensi Dua DFA
"""

import streamlit as st
from engine import DFA, dfa_equivalent
from utils import build_dfa_graph, parse_transitions_dfa, build_dfa_transition_table
from styles import render_result_banner, render_trace_chips


def input_dfa_form(prefix, label, default_states, default_alpha, default_start,
                   default_accepts, default_trans):
    st.markdown(f'<div class="section-eyebrow">{label}</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        states = st.text_input("States:", default_states, key=f"{prefix}_states")
        alpha = st.text_input("Alfabet:", default_alpha, key=f"{prefix}_alpha")
    with col2:
        start = st.text_input("Start State:", default_start, key=f"{prefix}_start")
        accepts = st.text_input("Accepting States:", default_accepts, key=f"{prefix}_accepts")
    trans = st.text_area("Transisi:", default_trans, height=140, key=f"{prefix}_trans")
    return states, alpha, start, accepts, trans


def render():
    st.markdown('<div class="section-eyebrow">MODUL 04</div>', unsafe_allow_html=True)
    st.header("Cek Ekuivalensi Dua DFA")

    col_form, col_canvas = st.columns([1, 1.6], gap="large")

    # ── Kolom Form (kiri, fixed-width, dua definisi DFA bertumpuk) ──
    with col_form:
        st.markdown('<div class="form-col-wrapper">', unsafe_allow_html=True)

        with st.form("eq_form"):
            with st.expander("Definisi DFA 1", expanded=True):
                s1, a1, i1, f1, t1 = input_dfa_form(
                    prefix="eq1", label="DFA 1",
                    default_states="q0, q1", default_alpha="a, b",
                    default_start="q0", default_accepts="q1",
                    default_trans="q0, a, q1\nq0, b, q0\nq1, a, q1\nq1, b, q0"
                )

            with st.expander("Definisi DFA 2", expanded=True):
                s2, a2, i2, f2, t2 = input_dfa_form(
                    prefix="eq2", label="DFA 2",
                    default_states="p0, p1, p2", default_alpha="a, b",
                    default_start="p0", default_accepts="p1, p2",
                    default_trans="p0, a, p1\np0, b, p0\np1, a, p2\np1, b, p0\np2, a, p2\np2, b, p0"
                )

            run_btn = st.form_submit_button("Cek Ekuivalensi", use_container_width=True)

        if run_btn:
            try:
                dfa1 = DFA(
                    states={s.strip() for s in s1.split(",") if s.strip()},
                    alphabet={a.strip() for a in a1.split(",") if a.strip()},
                    transitions=parse_transitions_dfa(t1),
                    start=i1.strip(),
                    accepts={f.strip() for f in f1.split(",") if f.strip()}
                )
                dfa2 = DFA(
                    states={s.strip() for s in s2.split(",") if s.strip()},
                    alphabet={a.strip() for a in a2.split(",") if a.strip()},
                    transitions=parse_transitions_dfa(t2),
                    start=i2.strip(),
                    accepts={f.strip() for f in f2.split(",") if f.strip()}
                )
                st.session_state['eq_dfa1'] = dfa1
                st.session_state['eq_dfa2'] = dfa2

                for label, dfa in (("DFA 1", dfa1), ("DFA 2", dfa2)):
                    if dfa.incomplete_transitions:
                        pairs = ", ".join(f"({s}, {a})" for s, a in dfa.incomplete_transitions)
                        st.warning(
                            f"{label} tidak total — transisi belum didefinisikan untuk: {pairs}. "
                            f"Pasangan ini akan diperlakukan sebagai penolakan (menuju trap state implisit)."
                        )

                is_eq, dist_str, explored_pairs = dfa_equivalent(dfa1, dfa2)
                st.session_state['eq_result'] = (is_eq, dist_str, explored_pairs)

            except Exception as e:
                st.session_state.pop('eq_dfa1', None)
                st.session_state.pop('eq_dfa2', None)
                st.session_state.pop('eq_result', None)
                st.error(f"Error: {e}")

        st.markdown('</div>', unsafe_allow_html=True)

    # ── Kolom Canvas (kanan) ──
    with col_canvas:
        if 'eq_result' not in st.session_state:
            st.markdown(
                '<div class="canvas-panel" style="padding:60px 20px; text-align:center;">'
                '<span style="color:#8A7468; font-family:\'JetBrains Mono\',monospace; font-size:13px;">'
                'Definisikan dua DFA di sebelah kiri untuk membandingkan ekuivalensinya.</span></div>',
                unsafe_allow_html=True,
            )
            return

        dfa1 = st.session_state['eq_dfa1']
        dfa2 = st.session_state['eq_dfa2']
        is_eq, dist_str, explored_pairs = st.session_state['eq_result']

        # Dua panel graph berdampingan
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown('<div class="canvas-panel">', unsafe_allow_html=True)
            st.markdown('<div class="canvas-panel-label">DFA 1</div>', unsafe_allow_html=True)
            st.graphviz_chart(build_dfa_graph(dfa1).source, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col_g2:
            st.markdown('<div class="canvas-panel">', unsafe_allow_html=True)
            st.markdown('<div class="canvas-panel-label">DFA 2</div>', unsafe_allow_html=True)
            st.graphviz_chart(build_dfa_graph(dfa2).source, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Tabel transisi DFA 1 & DFA 2, berdampingan dengan graf di atas
        with st.expander("Tabel Transisi"):
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                st.markdown("**DFA 1**")
                st.dataframe(build_dfa_transition_table(dfa1), use_container_width=True)
            with col_t2:
                st.markdown("**DFA 2**")
                st.dataframe(build_dfa_transition_table(dfa2), use_container_width=True)

        # Hasil ekuivalensi
        eq_banner = render_result_banner(
            is_eq,
            label="Kedua DFA mengenali bahasa yang sama" if is_eq
                  else "Kedua DFA mengenali bahasa yang berbeda",
            accept_text="EKUIVALEN",
            reject_text="TIDAK EKUIVALEN",
        )
        st.markdown(eq_banner, unsafe_allow_html=True)

        if is_eq:
            with st.expander("Product Construction Table"):
                alphabet = sorted(dfa1.alphabet | dfa2.alphabet)
                reachable_set = set(explored_pairs)
                DEAD = "__DEAD__"

                def step(dfa, state, symbol):
                    if state == DEAD:
                        return DEAD
                    return dfa.transitions.get((state, symbol), DEAD)

                def fmt_state(s):
                    return "∅" if s == DEAD else s

                rows = []
                for q in sorted(dfa1.states):
                    for p in sorted(dfa2.states):
                        is_reachable = (q, p) in reachable_set
                        acc1 = q in dfa1.accepts
                        acc2 = p in dfa2.accepts
                        row = {
                            "Pasangan (q,p)": f"({q},{p})",
                            "Reachable?": ("Ya (start)" if (q, p) == (dfa1.start, dfa2.start)
                                          else "Ya" if is_reachable else "Tidak"),
                            "Accept DFA1": "✓" if acc1 else "✗",
                            "Accept DFA2": "✓" if acc2 else "✗",
                            "Status": "Sama" if acc1 == acc2 else "BEDA",
                        }
                        for sym in alphabet:
                            n1 = fmt_state(step(dfa1, q, sym))
                            n2 = fmt_state(step(dfa2, p, sym))
                            row[f"δ(_,{sym})"] = f"({n1},{n2})"
                        rows.append(row)

                st.dataframe(rows, use_container_width=True, hide_index=True)

        if not is_eq and dist_str:
            st.markdown(
                f'<div class="meta-item" style="display:inline-flex; margin-bottom:14px;">'
                f'<span class="meta-label">STRING PEMBEDA</span>'
                f'<span class="meta-value">{dist_str}</span></div>',
                unsafe_allow_html=True,
            )

            if dist_str != "(string kosong / epsilon)":
                r1, trace1 = dfa1.run(dist_str)
                r2, trace2 = dfa2.run(dist_str)
            else:
                r1 = dfa1.start in dfa1.accepts
                r2 = dfa2.start in dfa2.accepts
                trace1, trace2 = [dfa1.start], [dfa2.start]

            col_r1, col_r2 = st.columns(2)
            with col_r1:
                st.markdown(render_result_banner(r1, label="DFA 1"), unsafe_allow_html=True)
                if trace1:
                    st.markdown(
                        render_trace_chips(trace1, current_index=len(trace1) - 1),
                        unsafe_allow_html=True,
                    )
                    st.graphviz_chart(
                        build_dfa_graph(dfa1, highlight_state=trace1[-1], accepted=r1).source,
                        use_container_width=True
                    )
            with col_r2:
                st.markdown(render_result_banner(r2, label="DFA 2"), unsafe_allow_html=True)
                if trace2:
                    st.markdown(
                        render_trace_chips(trace2, current_index=len(trace2) - 1),
                        unsafe_allow_html=True,
                    )
                    st.graphviz_chart(
                        build_dfa_graph(dfa2, highlight_state=trace2[-1], accepted=r2).source,
                        use_container_width=True
                    )
