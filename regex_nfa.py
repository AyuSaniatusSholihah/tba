"""
regex_nfa.py
============
Fitur 2: Regex -> NFA (Thompson's Construction) + Uji String dengan Animasi Glow
"""

import streamlit as st
import streamlit.components.v1 as components
import time
from engine import regex_to_nfa, EPSILON
from utils import build_nfa_graph, render_nfa_animated


def render():
    st.header("② Regex → NFA & Uji String")
    st.caption(
        "Masukkan Regular Expression untuk di-generate menjadi NFA "
        "menggunakan **Konstruksi Thompson**. Lalu uji string dengan animasi glow."
    )

    st.markdown("""
    > **Operator yang didukung:**  
    > `|` = union/atau &nbsp;·&nbsp; `*` = Kleene star &nbsp;·&nbsp; `+` = satu atau lebih &nbsp;·&nbsp; `?` = opsional &nbsp;·&nbsp; `()` = grouping  
    > **Contoh:** `(a|b)*abb` &nbsp;·&nbsp; `a*b+` &nbsp;·&nbsp; `(ab)?c`
    """)

    regex_input = st.text_input("Regular Expression:", "a*b", key="regex_input")

    if st.button("🔨 Generate NFA", key="regex_generate"):
        try:
            nfa = regex_to_nfa(regex_input)
            st.session_state['nfa_regex'] = nfa
            st.session_state['regex_str'] = regex_input
            st.success(
                f"✅ NFA untuk `{regex_input}` berhasil dibuat! "
                f"({len(nfa.states)} state, alfabet: `{sorted(nfa.alphabet)}`)"
            )
        except ValueError as e:
            st.error(f"❌ Regex tidak valid: {e}")

    if 'nfa_regex' in st.session_state:
        nfa = st.session_state['nfa_regex']
        regex_str = st.session_state.get('regex_str', '')

        # Tampilkan NFA idle
        graph_placeholder = st.empty()
        with graph_placeholder:
            components.html(render_nfa_animated(nfa), height=390)

        # Info NFA
        with st.expander("📊 Detail NFA (Konstruksi Thompson)"):
            st.markdown(f"- **States:** `{sorted(nfa.states)}`")
            st.markdown(f"- **Alfabet:** `{sorted(nfa.alphabet)}`")
            st.markdown(f"- **Start:** `{nfa.start}`")
            st.markdown(f"- **Accepting:** `{sorted(nfa.accepts)}`")
            st.markdown("**Transisi:**")
            for (fs, sym), targets in sorted(nfa.transitions.items(), key=lambda x: (x[0][0], x[0][1])):
                s = "ε" if sym == EPSILON else sym
                st.markdown(f"  - `({fs}, {s})` → `{sorted(targets)}`")

        st.divider()
        st.subheader("🧪 Uji String")

        test_str = st.text_input(
            "String uji:", key="nfa_teststr",
            placeholder="Ketik string, contoh: aab"
        )

        col_anim, col_speed = st.columns([1, 2])
        with col_anim:
            animate = st.toggle("🎬 Animasi", value=True, key="nfa_animate")
        with col_speed:
            speed = st.slider("⏱ Kecepatan (detik/step)", 0.2, 2.0, 0.7, 0.1, key="nfa_speed")

        run_btn = st.button("▶️ Jalankan", key="nfa_run", use_container_width=True)

        status_placeholder = st.empty()
        trace_placeholder = st.empty()

        if run_btn:
            accepted, trace = nfa.run(test_str)

            if animate and len(trace) > 0:
                for step_idx, active_states in enumerate(trace):
                    is_last = (step_idx == len(trace) - 1)
                    acc_flag = accepted if is_last else None

                    # Edge aktif
                    if step_idx > 0 and step_idx - 1 < len(test_str):
                        sym = test_str[step_idx - 1]
                        prev_states = trace[step_idx - 1]
                        highlight_edges = {(s, sym) for s in prev_states}
                    else:
                        highlight_edges = None

                    html_content = render_nfa_animated(
                        nfa,
                        highlight_states=active_states,
                        highlight_edges=highlight_edges,
                        accepted=acc_flag
                    )
                    graph_placeholder.empty()
                    with graph_placeholder:
                        components.html(html_content, height=390)

                    sym_read = test_str[step_idx - 1] if step_idx > 0 and step_idx - 1 < len(test_str) else "—"
                    sisa = test_str[step_idx:] if step_idx < len(test_str) else "(selesai)"
                    status_placeholder.info(
                        f"**Step {step_idx}** &nbsp;|&nbsp; "
                        f"States aktif: `{sorted(active_states)}` &nbsp;|&nbsp; "
                        f"Simbol: `{sym_read}` &nbsp;|&nbsp; "
                        f"Sisa: `{sisa}`"
                    )

                    if not is_last:
                        time.sleep(speed)
            else:
                final_states = trace[-1] if trace else set()
                html_content = render_nfa_animated(nfa, highlight_states=final_states, accepted=accepted)
                graph_placeholder.empty()
                with graph_placeholder:
                    components.html(html_content, height=390)

            if accepted:
                st.success(f"✅ String **'{test_str}'** DITERIMA oleh Regex/NFA `{regex_str}`.")
            else:
                st.error(f"❌ String **'{test_str}'** DITOLAK oleh Regex/NFA `{regex_str}`.")

            # Trace per step
            trace_lines = []
            for i, states_set in enumerate(trace):
                sym = test_str[i - 1] if i > 0 and i - 1 < len(test_str) else "start"
                trace_lines.append(f"**Step {i}** (`{sym}`): `{sorted(states_set)}`")
            trace_placeholder.markdown("**Trace:**\n\n" + "\n\n".join(trace_lines))
