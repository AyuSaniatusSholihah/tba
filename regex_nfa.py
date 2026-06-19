"""
regex_nfa.py
Fitur 2: Uji String pada NFA dari Regex
"""

import streamlit as st
import streamlit.components.v1 as components
import time
from engine import regex_to_nfa, EPSILON
from utils import render_nfa_animated, epsilon_closure_with_trace
from styles import render_meta_row, render_result_banner, render_set_chip_row, render_dead_state_notice


def render():
    st.markdown('<div class="section-eyebrow">MODUL 02</div>', unsafe_allow_html=True)
    st.header("Regex → NFA & Uji String")

    col_form, col_canvas = st.columns([1, 1.6], gap="large")

    # ── Kolom Form (kiri, fixed-width) ──
    with col_form:
        st.markdown('<div class="form-col-wrapper">', unsafe_allow_html=True)

        with st.expander("Regular Expression", expanded=True):
            with st.form("regex_form"):
                regex_input = st.text_input(
                    "Pattern (contoh: (a|b)*abb):", "a*b", key="regex_input"
                )
                submitted = st.form_submit_button("Generate NFA", use_container_width=True)

            if submitted:
                try:
                    nfa = regex_to_nfa(regex_input)
                    st.session_state['nfa_regex'] = nfa
                    st.session_state['regex_str'] = regex_input
                    st.success(
                        f"NFA untuk `{regex_input}` berhasil dibuat! "
                        f"({len(nfa.states)} state, alfabet: `{sorted(nfa.alphabet)}`)"
                    )
                except ValueError as e:
                    st.session_state.pop('nfa_regex', None)
                    st.session_state.pop('regex_str', None)
                    st.error(f"Regex tidak valid: {e}")

        if 'nfa_regex' in st.session_state:
            nfa = st.session_state['nfa_regex']

            with st.expander("Detail NFA (Konstruksi Thompson)"):
                st.markdown(f"- **States:** `{sorted(nfa.states)}`")
                st.markdown(f"- **Alfabet:** `{sorted(nfa.alphabet)}`")
                st.markdown(f"- **Start:** `{nfa.start}`")
                st.markdown(f"- **Accepting:** `{sorted(nfa.accepts)}`")
                st.markdown("**Transisi:**")
                for (fs, sym), targets in sorted(nfa.transitions.items(), key=lambda x: (x[0][0], x[0][1])):
                    s = "ε" if sym == EPSILON else sym
                    st.markdown(f"  - `({fs}, {s})` → `{sorted(targets)}`")

            st.markdown('<div class="section-eyebrow">UJI STRING</div>', unsafe_allow_html=True)
            test_str = st.text_input(
                "String uji:", key="nfa_teststr",
                placeholder="Ketik string, contoh: aab"
            )
            col_anim, col_speed = st.columns([1, 2])
            with col_anim:
                animate = st.toggle("Animasi", value=True, key="nfa_animate")
            with col_speed:
                speed = st.slider("Kecepatan (detik/step)", 0.2, 2.0, 0.7, 0.1, key="nfa_speed")
            run_btn = st.button("Jalankan", key="nfa_run", use_container_width=True)
        else:
            run_btn = False
            test_str, animate, speed = "", True, 0.7

        st.markdown('</div>', unsafe_allow_html=True)

    # ── Kolom Canvas (kanan) ──
    with col_canvas:
        if 'nfa_regex' not in st.session_state:
            st.markdown(
                '<div class="canvas-panel" style="padding:60px 20px; text-align:center;">'
                '<span style="color:#8A7468; font-family:\'JetBrains Mono\',monospace; font-size:13px;">'
                'Masukkan regex di sebelah kiri untuk men-generate NFA.</span></div>',
                unsafe_allow_html=True,
            )
            return

        nfa = st.session_state['nfa_regex']
        regex_str = st.session_state.get('regex_str', '')

        st.markdown('<div class="canvas-panel">', unsafe_allow_html=True)
        st.markdown('<div class="canvas-panel-label">GRAPH</div>', unsafe_allow_html=True)
        graph_placeholder = st.empty()
        with graph_placeholder:
            components.html(render_nfa_animated(nfa), height=390)
        st.markdown('</div>', unsafe_allow_html=True)

        status_placeholder = st.empty()
        trace_placeholder = st.empty()

        if not run_btn:
            return

        accepted, trace = nfa.run(test_str)
        # NFA bisa "mati" (kehilangan semua state aktif) sebelum seluruh
        # string habis dibaca — engine berhenti lebih awal di kasus ini.
        # len(trace) - 1 = jumlah karakter yang BENAR-BENAR diproses.
        chars_consumed = len(trace) - 1 if trace else 0
        died_early = chars_consumed < len(test_str)
        unconsumed = test_str[chars_consumed:] if died_early else ""

        if animate and len(trace) > 0:
            for step_idx, active_states in enumerate(trace):
                is_last = (step_idx == len(trace) - 1)
                acc_flag = accepted if is_last else None

                if step_idx == 0:
                    # Step 0: belum baca simbol apapun. "Entry" = start state itu
                    # sendiri, sisanya (kalau ada) adalah turunan ε dari start.
                    entry_set = {nfa.start}
                    _, derived_set, epsilon_pairs = epsilon_closure_with_trace(nfa, entry_set)
                    highlight_edges = None
                elif step_idx - 1 < len(test_str):
                    sym = test_str[step_idx - 1]
                    prev_states = trace[step_idx - 1]
                    nxt = set()
                    symbol_edges = set()
                    for s in prev_states:
                        targets = nfa.transitions.get((s, sym), set())
                        if targets:
                            symbol_edges.add((s, sym))
                            nxt |= targets
                    entry_set = nxt
                    _, derived_set, epsilon_pairs = epsilon_closure_with_trace(nfa, nxt)
                    highlight_edges = symbol_edges
                else:
                    entry_set, derived_set, epsilon_pairs, highlight_edges = set(), set(), set(), None

                html_content = render_nfa_animated(
                    nfa, highlight_states=active_states, highlight_edges=highlight_edges,
                    accepted=acc_flag, derived_states=derived_set,
                    highlight_epsilon_pairs=epsilon_pairs,
                )
                graph_placeholder.empty()
                with graph_placeholder:
                    components.html(html_content, height=390)

                sym_read = test_str[step_idx - 1] if step_idx > 0 and step_idx - 1 < len(test_str) else "—"
                if is_last and died_early:
                    sisa_label = f"`{unconsumed}` (tidak diproses)"
                else:
                    sisa = test_str[step_idx:] if step_idx < len(test_str) else "(selesai)"
                    sisa_label = f"`{sisa}`"
                status_placeholder.markdown(
                    render_meta_row(step_idx, f"`{sym_read}`", sisa_label),
                    unsafe_allow_html=True,
                )
                trace_placeholder.markdown(
                    render_set_chip_row([sorted(s) for s in trace[:step_idx + 1]], current_index=step_idx),
                    unsafe_allow_html=True,
                )

                if not is_last:
                    time.sleep(speed)
        else:
            final_states = trace[-1] if trace else set()
            html_content = render_nfa_animated(nfa, highlight_states=final_states, accepted=accepted)
            graph_placeholder.empty()
            with graph_placeholder:
                components.html(html_content, height=390)
            trace_placeholder.markdown(
                render_set_chip_row([sorted(s) for s in trace], current_index=len(trace) - 1),
                unsafe_allow_html=True,
            )

        if died_early:
            st.markdown(render_dead_state_notice(unconsumed), unsafe_allow_html=True)

        st.markdown(
            render_result_banner(accepted, label=f"'{test_str}' pada regex `{regex_str}`"),
            unsafe_allow_html=True,
        )
