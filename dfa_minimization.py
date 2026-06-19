"""
dfa_minimization.py
Fitur 3: Minimisasi DFA
"""

import streamlit as st
from engine import DFA, minimize_dfa
from utils import build_dfa_graph, parse_transitions_dfa


def render():
    st.header("3. Minimisasi DFA")

    with st.expander("Definisi DFA", expanded=True):
        with st.form("min_form"):
            col1, col2 = st.columns(2)
            with col1:
                states_input = st.text_input("States (pisah koma):", "q0, q1, q2, q3, q4", key="min_states")
                alphabet_input = st.text_input("Alfabet (pisah koma):", "a, b", key="min_alpha")
            with col2:
                start_input = st.text_input("Start State:", "q0", key="min_start")
                accepts_input = st.text_input("Accepting States (pisah koma):", "q3, q4", key="min_accepts")

            trans_default = (
                "q0, a, q1\n"
                "q0, b, q2\n"
                "q1, a, q1\n"
                "q1, b, q3\n"
                "q2, a, q2\n"
                "q2, b, q4\n"
                "q3, a, q3\n"
                "q3, b, q3\n"
                "q4, a, q4\n"
                "q4, b, q4"
            )
            trans_input = st.text_area("Transisi DFA:", value=trans_default, height=200, key="min_trans")

            run_btn = st.form_submit_button("Minimalkan DFA")

    if run_btn:
        try:
            states = {s.strip() for s in states_input.split(",") if s.strip()}
            alphabet = {a.strip() for a in alphabet_input.split(",") if a.strip()}
            accepts = {f.strip() for f in accepts_input.split(",") if f.strip()}
            transitions = parse_transitions_dfa(trans_input)

            original = DFA(states, alphabet, transitions, start_input.strip(), accepts)
            minimized = minimize_dfa(original)
            st.session_state['min_original'] = original
            st.session_state['min_minimized'] = minimized
            if original.incomplete_transitions:
                pairs = ", ".join(f"({s}, {a})" for s, a in original.incomplete_transitions)
                st.warning(
                    f"DFA tidak total — transisi belum didefinisikan untuk: {pairs}. "
                    f"Pasangan ini akan diperlakukan sebagai penolakan (menuju trap state implisit)."
                )
        except Exception as e:
            # Input tidak valid -> jangan tampilkan hasil lama yang mungkin masih tersimpan
            st.session_state.pop('min_original', None)
            st.session_state.pop('min_minimized', None)
            st.error(f"Error: {e}")

    if 'min_original' in st.session_state:
        original = st.session_state['min_original']
        minimized = st.session_state['min_minimized']

        # Ringkasan metrik
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("State Awal", len(original.states))
        col_m2.metric("State Minimal", len(minimized.states))
        reduction = len(original.states) - len(minimized.states)
        col_m3.metric("Pengurangan", f"{reduction} state")

        if reduction == 0:
            st.info("DFA ini sudah minimal! Tidak ada state yang bisa digabungkan.")
        else:
            st.success(f"DFA berhasil diminimalkan dari {len(original.states)} menjadi {len(minimized.states)} state.")

        # Tampilkan graf
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.subheader("DFA Asli")
            st.graphviz_chart(build_dfa_graph(original).source, use_container_width=True)

        with col_g2:
            st.subheader("DFA Minimal")
            st.graphviz_chart(build_dfa_graph(minimized).source, use_container_width=True)

        # Detail DFA minimal
        with st.expander("Detail DFA Minimal"):
            st.markdown(f"- **States:** `{sorted(minimized.states)}`")
            st.markdown(f"- **Alfabet:** `{sorted(minimized.alphabet)}`")
            st.markdown(f"- **Start:** `{minimized.start}`")
            st.markdown(f"- **Accepting:** `{sorted(minimized.accepts)}`")
            st.markdown("**Transisi:**")
            for (fs, sym), ts in sorted(minimized.transitions.items()):
                st.markdown(f"  - `({fs}, {sym})` → `{ts}`")

        # Uji string pada DFA minimal
        st.divider()
        st.subheader("Uji String pada DFA Minimal")
        test_str = st.text_input("String uji:", key="min_teststr",
                                 placeholder="Ketik string untuk diuji...")
        if st.button("Uji", key="min_test"):
            accepted, trace = minimized.run(test_str)
            if accepted:
                st.success(f"String **'{test_str}'** DITERIMA oleh DFA Minimal.")
            else:
                st.error(f"String **'{test_str}'** DITOLAK oleh DFA Minimal.")
            trace_str = " → ".join(f"`{s}`" for s in trace)
            st.markdown(f"**Lintasan:** {trace_str}")