"""
dfa_minimization.py
Fitur 3: Minimisasi DFA
"""

import streamlit as st
from engine import DFA, minimize_dfa
from utils import build_dfa_graph, parse_transitions_dfa, build_dfa_transition_table
from styles import render_result_banner, render_trace_chips


def render():
    st.markdown('<div class="section-eyebrow">MODUL 03</div>', unsafe_allow_html=True)
    st.header("Minimisasi DFA")

    col_form, col_canvas = st.columns([1, 1.6], gap="large")

    # ── Kolom Form (kiri, fixed-width) ──
    with col_form:
        st.markdown('<div class="form-col-wrapper">', unsafe_allow_html=True)

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

                run_btn = st.form_submit_button("Minimalkan DFA", use_container_width=True)

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
                st.session_state.pop('min_original', None)
                st.session_state.pop('min_minimized', None)
                st.error(f"Error: {e}")

        if 'min_minimized' in st.session_state:
            with st.expander("Detail DFA Minimal"):
                minimized = st.session_state['min_minimized']
                st.markdown(f"- **States:** `{sorted(minimized.states)}`")
                st.markdown(f"- **Alfabet:** `{sorted(minimized.alphabet)}`")
                st.markdown(f"- **Start:** `{minimized.start}`")
                st.markdown(f"- **Accepting:** `{sorted(minimized.accepts)}`")
                st.markdown("**Transisi:**")
                for (fs, sym), ts in sorted(minimized.transitions.items()):
                    st.markdown(f"  - `({fs}, {sym})` → `{ts}`")

            st.markdown('<div class="section-eyebrow">UJI STRING (PADA DFA MINIMAL)</div>', unsafe_allow_html=True)
            test_str = st.text_input("String uji:", key="min_teststr",
                                     placeholder="Ketik string untuk diuji...")
            test_btn = st.button("Uji", key="min_test", use_container_width=True)
        else:
            test_btn = False
            test_str = ""

        st.markdown('</div>', unsafe_allow_html=True)

    # ── Kolom Canvas (kanan) ──
    with col_canvas:
        if 'min_original' not in st.session_state:
            st.markdown(
                '<div class="canvas-panel" style="padding:60px 20px; text-align:center;">'
                '<span style="color:#8A7468; font-family:\'JetBrains Mono\',monospace; font-size:13px;">'
                'Definisikan DFA di sebelah kiri untuk melihat hasil minimisasi.</span></div>',
                unsafe_allow_html=True,
            )
            return

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

        # ── 1. State tidak reachable ──
        if minimized.unreachable_states:
            st.warning(
                f"State tidak reachable dari start (dihapus sebelum minimisasi): "
                f"`{minimized.unreachable_states}`"
            )

        # ── 2. Langkah Partisi (Partition Refinement) ──
        with st.expander("Langkah Partisi"):
            for step in minimized.partition_steps:
                group_strs = "  ".join(
                    "{" + ", ".join(g) + "}" for g in step["groups"]
                )
                st.markdown(f"**{step['label']}**  &nbsp; `{group_strs}`")

        # ── 3. Tabel Pemetaan State ──
        with st.expander("Pemetaan State"):
            mapping_rows = []
            for new_name, old_members in minimized.state_mapping.items():
                mapping_rows.append({
                    "State Baru": new_name,
                    "State Lama (anggota)": ", ".join(old_members),
                    "Status": "digabung" if len(old_members) > 1 else "tetap",
                })
            st.dataframe(mapping_rows, use_container_width=True, hide_index=True)

        # ── 4. Tabel Transisi (DFA asli & minimal) ──
        with st.expander("Tabel Transisi"):
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                st.markdown("**DFA Asli**")
                st.dataframe(build_dfa_transition_table(original), use_container_width=True)
            with col_t2:
                st.markdown("**DFA Minimal**")
                st.dataframe(build_dfa_transition_table(minimized), use_container_width=True)

        # Dua panel graph berdampingan (asli vs minimal), masing-masing dalam canvas-panel
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown('<div class="canvas-panel">', unsafe_allow_html=True)
            st.markdown('<div class="canvas-panel-label">DFA ASLI</div>', unsafe_allow_html=True)
            st.graphviz_chart(build_dfa_graph(original).source, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col_g2:
            st.markdown('<div class="canvas-panel">', unsafe_allow_html=True)
            st.markdown('<div class="canvas-panel-label">DFA MINIMAL</div>', unsafe_allow_html=True)
            st.graphviz_chart(build_dfa_graph(minimized).source, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        if test_btn:
            accepted, trace = minimized.run(test_str)
            st.markdown(
                render_result_banner(accepted, label=f"'{test_str}' pada DFA Minimal"),
                unsafe_allow_html=True,
            )
            st.markdown(
                render_trace_chips(trace, current_index=len(trace) - 1 if trace else None),
                unsafe_allow_html=True,
            )
