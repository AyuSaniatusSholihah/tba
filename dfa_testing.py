"""
dfa_testing.py
Fitur 1: Uji String pada DFA
"""

import streamlit as st
import streamlit.components.v1 as components
import time
from engine import DFA
from utils import build_dfa_graph, render_dfa_animated


def parse_transitions_dfa(text):
    transitions = {}
    for line in text.strip().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = [p.strip() for p in line.split(',')]
        if len(parts) != 3:
            raise ValueError(f"Format salah: '{line}'. Gunakan: state,simbol,state_tujuan")
        transitions[(parts[0], parts[1])] = parts[2]
    return transitions


def render():
    st.header("1. Uji String pada DFA")

    with st.expander("Definisi DFA", expanded=True):
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

        if st.button("Buat & Tampilkan DFA", key="dfa1_build"):
            try:
                states = {s.strip() for s in states_input.split(",") if s.strip()}
                alphabet = {a.strip() for a in alphabet_input.split(",") if a.strip()}
                accepts = {f.strip() for f in accepts_input.split(",") if f.strip()}
                transitions = parse_transitions_dfa(trans_input)
                dfa = DFA(states, alphabet, transitions, start_input.strip(), accepts)
                st.session_state['dfa_1'] = dfa
                st.success("DFA berhasil dibuat!")
            except Exception as e:
                st.error(f"Error: {e}")

    if 'dfa_1' in st.session_state:
        dfa = st.session_state['dfa_1']

        graph_placeholder = st.empty()
        # Tampilkan graf awal
        with graph_placeholder:
            components.html(render_dfa_animated(dfa), height=390)

        st.divider()
        st.subheader("Uji String")

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

        status_placeholder = st.empty()
        trace_placeholder = st.empty()

        if run_btn:
            accepted, trace = dfa.run(test_str)

            if animate and len(trace) > 0:
                for step_idx, state in enumerate(trace):
                    is_last = (step_idx == len(trace) - 1)
                    acc_flag = accepted if is_last else None

                    # Edge aktif
                    if step_idx > 0 and step_idx - 1 < len(test_str):
                        prev_state = trace[step_idx - 1]
                        sym = test_str[step_idx - 1]
                        highlight_edge = (prev_state, sym)
                    else:
                        highlight_edge = None

                    # Render SVG
                    html_content = render_dfa_animated(
                        dfa,
                        highlight_state=state,
                        highlight_edge=highlight_edge,
                        accepted=acc_flag
                    )
                    graph_placeholder.empty()
                    with graph_placeholder:
                        components.html(html_content, height=390)

                    # Status
                    sym_read = test_str[step_idx - 1] if step_idx > 0 and step_idx - 1 < len(test_str) else "—"
                    sisa = test_str[step_idx:] if step_idx < len(test_str) else "(selesai)"
                    status_placeholder.info(
                        f"**Step {step_idx}** &nbsp;|&nbsp; "
                        f"State aktif: `{state}` &nbsp;|&nbsp; "
                        f"Simbol dibaca: `{sym_read}` &nbsp;|&nbsp; "
                        f"Sisa: `{sisa}`"
                    )

                    if not is_last:
                        time.sleep(speed)
            else:
                # Hasil akhir langsung
                final_state = trace[-1] if trace else dfa.start
                html_content = render_dfa_animated(dfa, highlight_state=final_state, accepted=accepted)
                graph_placeholder.empty()
                with graph_placeholder:
                    components.html(html_content, height=390)

            # Hasil akhir
            if accepted:
                st.success(f"String **'{test_str}'** DITERIMA oleh DFA.")
            else:
                st.error(f"String **'{test_str}'** DITOLAK oleh DFA.")

            trace_str = " → ".join(f"`{s}`" for s in trace)
            trace_placeholder.markdown(f"**Lintasan State:** {trace_str}")
