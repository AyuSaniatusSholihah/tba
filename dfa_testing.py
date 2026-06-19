"""
dfa_testing.py
Fitur 1: Uji String pada DFA
"""

import streamlit as st
import streamlit.components.v1 as components
import time
from engine import DFA
from utils import render_dfa_animated, parse_transitions_dfa
from styles import render_meta_row, render_result_banner, render_trace_chips


def render():
    st.markdown('<div class="section-eyebrow">MODUL 01</div>', unsafe_allow_html=True)
    st.header("Uji String pada DFA")

    col_form, col_canvas = st.columns([1, 1.6], gap="large")

    # ── Kolom Form (kiri, fixed-width) ──
    with col_form:
        st.markdown('<div class="form-col-wrapper">', unsafe_allow_html=True)

        with st.expander("Definisi DFA", expanded=True):
            with st.form("dfa1_form"):
                col1, col2 = st.columns(2)
                with col1:
                    states_input = st.text_input("States (pisah koma):", "q0, q1, q2", key="dfa1_states")
                    alphabet_input = st.text_input("Alfabet (pisah koma):", "0, 1", key="dfa1_alpha")
                with col2:
                    start_input = st.text_input("Start State:", "q0", key="dfa1_start")
                    accepts_input = st.text_input("Accepting States (pisah koma):", "q2", key="dfa1_accepts")

                st.markdown("**Transisi** (Format: `state_asal, simbol, state_tujuan`)")
                trans_default = "q0, 0, q0\nq0, 1, q1\nq1, 0, q2\nq1, 1, q0\nq2, 0, q1\nq2, 1, q2"
                trans_input = st.text_area("Transisi DFA:", value=trans_default, height=160, key="dfa1_trans")

                submitted = st.form_submit_button("Buat & Tampilkan DFA", use_container_width=True)

            if submitted:
                try:
                    states = {s.strip() for s in states_input.split(",") if s.strip()}
                    alphabet = {a.strip() for a in alphabet_input.split(",") if a.strip()}
                    accepts = {f.strip() for f in accepts_input.split(",") if f.strip()}
                    transitions = parse_transitions_dfa(trans_input)
                    dfa = DFA(states, alphabet, transitions, start_input.strip(), accepts)
                    st.session_state['dfa_1'] = dfa
                    st.success("DFA berhasil dibuat!")
                    if dfa.incomplete_transitions:
                        pairs = ", ".join(f"({s}, {a})" for s, a in dfa.incomplete_transitions)
                        st.warning(
                            f"DFA tidak total — transisi belum didefinisikan untuk: {pairs}. "
                            f"Pasangan ini akan diperlakukan sebagai penolakan (menuju trap state implisit)."
                        )
                except Exception as e:
                    st.session_state.pop('dfa_1', None)
                    st.error(f"Error: {e}")

        if 'dfa_1' in st.session_state:
            st.markdown('<div class="section-eyebrow">UJI STRING</div>', unsafe_allow_html=True)
            test_str = st.text_input(
                "String uji:", key="dfa1_teststr",
                placeholder="Ketik string, contoh: 010"
            )
            col_anim, col_speed = st.columns([1, 2])
            with col_anim:
                animate = st.toggle("Animasi", value=True, key="dfa1_animate")
            with col_speed:
                speed = st.slider("Kecepatan (detik/step)", 0.2, 2.0, 0.7, 0.1, key="dfa1_speed")
            run_btn = st.button("Jalankan", key="dfa1_run", use_container_width=True)
        else:
            run_btn = False
            test_str, animate, speed = "", True, 0.7

        st.markdown('</div>', unsafe_allow_html=True)

    # ── Kolom Canvas (kanan: panel graph 62% + panel status/trace) ──
    with col_canvas:
        if 'dfa_1' not in st.session_state:
            st.markdown(
                '<div class="canvas-panel" style="padding:60px 20px; text-align:center;">'
                '<span style="color:#8A7468; font-family:\'JetBrains Mono\',monospace; font-size:13px;">'
                'Definisikan DFA di sebelah kiri untuk melihat visualisasi graph.</span></div>',
                unsafe_allow_html=True,
            )
            return

        dfa = st.session_state['dfa_1']

        st.markdown('<div class="canvas-panel">', unsafe_allow_html=True)
        st.markdown('<div class="canvas-panel-label">GRAPH</div>', unsafe_allow_html=True)
        graph_placeholder = st.empty()
        with graph_placeholder:
            components.html(render_dfa_animated(dfa), height=390)
        st.markdown('</div>', unsafe_allow_html=True)

        status_placeholder = st.empty()
        trace_placeholder = st.empty()

        if not run_btn:
            return

        accepted, trace = dfa.run(test_str)

        if animate and len(trace) > 0:
            for step_idx, state in enumerate(trace):
                is_last = (step_idx == len(trace) - 1)
                acc_flag = accepted if is_last else None

                if step_idx > 0 and step_idx - 1 < len(test_str):
                    prev_state = trace[step_idx - 1]
                    sym = test_str[step_idx - 1]
                    highlight_edge = (prev_state, sym)
                else:
                    highlight_edge = None

                html_content = render_dfa_animated(
                    dfa, highlight_state=state, highlight_edge=highlight_edge, accepted=acc_flag
                )
                graph_placeholder.empty()
                with graph_placeholder:
                    components.html(html_content, height=390)

                sym_read = test_str[step_idx - 1] if step_idx > 0 and step_idx - 1 < len(test_str) else "—"
                sisa = test_str[step_idx:] if step_idx < len(test_str) else "(selesai)"
                status_placeholder.markdown(
                    render_meta_row(step_idx, f"`{sym_read}`", f"`{sisa}`"),
                    unsafe_allow_html=True,
                )
                trace_placeholder.markdown(
                    render_trace_chips(trace[:step_idx + 1], current_index=step_idx),
                    unsafe_allow_html=True,
                )

                if not is_last:
                    time.sleep(speed)
        else:
            final_state = trace[-1] if trace else dfa.start
            html_content = render_dfa_animated(dfa, highlight_state=final_state, accepted=accepted)
            graph_placeholder.empty()
            with graph_placeholder:
                components.html(html_content, height=390)
            trace_placeholder.markdown(
                render_trace_chips(trace, current_index=len(trace) - 1),
                unsafe_allow_html=True,
            )

        st.markdown(
            render_result_banner(accepted, label=f"'{test_str}'"),
            unsafe_allow_html=True,
        )
