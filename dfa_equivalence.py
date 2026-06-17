"""
dfa_equivalence.py
==================
Fitur 4: Cek Ekuivalensi Dua DFA menggunakan Product Construction + BFS
"""

import streamlit as st
from engine import DFA, dfa_equivalent
from utils import build_dfa_graph


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


def input_dfa_form(prefix, label, default_states, default_alpha, default_start,
                   default_accepts, default_trans):
    st.subheader(label)
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
    st.header("④ Cek Ekuivalensi Dua DFA")
    st.caption(
        "Periksa apakah dua DFA mengenali **bahasa yang persis sama** "
        "menggunakan **Product Construction + BFS**. "
        "Jika tidak ekuivalen, program akan menampilkan string pembeda."
    )

    # --- DFA 1 ---
    with st.expander("⚙️ Definisi DFA 1", expanded=True):
        s1, a1, i1, f1, t1 = input_dfa_form(
            prefix="eq1",
            label="DFA 1",
            default_states="q0, q1",
            default_alpha="a, b",
            default_start="q0",
            default_accepts="q1",
            default_trans="q0, a, q1\nq0, b, q0\nq1, a, q1\nq1, b, q0"
        )

    # --- DFA 2 ---
    with st.expander("⚙️ Definisi DFA 2", expanded=True):
        s2, a2, i2, f2, t2 = input_dfa_form(
            prefix="eq2",
            label="DFA 2",
            default_states="p0, p1, p2",
            default_alpha="a, b",
            default_start="p0",
            default_accepts="p1, p2",
            default_trans="p0, a, p1\np0, b, p0\np1, a, p2\np1, b, p0\np2, a, p2\np2, b, p0"
        )

    run_btn = st.button("🔍 Cek Ekuivalensi", key="eq_run", use_container_width=True)

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

            is_eq, dist_str = dfa_equivalent(dfa1, dfa2)
            st.session_state['eq_result'] = (is_eq, dist_str)

        except Exception as e:
            st.error(f"❌ Error: {e}")

    if 'eq_result' in st.session_state:
        dfa1 = st.session_state['eq_dfa1']
        dfa2 = st.session_state['eq_dfa2']
        is_eq, dist_str = st.session_state['eq_result']

        st.divider()

        # Visualisasi kedua DFA
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown("**DFA 1**")
            st.graphviz_chart(build_dfa_graph(dfa1).source, use_container_width=True)
        with col_g2:
            st.markdown("**DFA 2**")
            st.graphviz_chart(build_dfa_graph(dfa2).source, use_container_width=True)

        st.divider()

        # Hasil
        if is_eq:
            st.success("✅ **EKUIVALEN** — Kedua DFA mengenali bahasa yang persis sama.")
        else:
            st.error("❌ **TIDAK EKUIVALEN** — Kedua DFA mengenali bahasa yang berbeda.")

            if dist_str:
                st.markdown(f"**String Pembeda:** `{dist_str}`")

                # Tunjukkan perbedaan
                if dist_str != "(string kosong / epsilon)":
                    r1, trace1 = dfa1.run(dist_str)
                    r2, trace2 = dfa2.run(dist_str)
                else:
                    r1 = dist_str in dfa1.accepts if not dist_str else False
                    r2 = dist_str in dfa2.accepts if not dist_str else False
                    trace1, trace2 = [], []

                col_r1, col_r2 = st.columns(2)
                with col_r1:
                    if r1:
                        st.success(f"DFA 1: **DITERIMA** `{dist_str}`")
                    else:
                        st.error(f"DFA 1: **DITOLAK** `{dist_str}`")
                    if trace1:
                        st.markdown("Lintasan: " + " → ".join(f"`{s}`" for s in trace1))
                        st.graphviz_chart(
                            build_dfa_graph(dfa1, highlight_state=trace1[-1], accepted=r1).source,
                            use_container_width=True
                        )

                with col_r2:
                    if r2:
                        st.success(f"DFA 2: **DITERIMA** `{dist_str}`")
                    else:
                        st.error(f"DFA 2: **DITOLAK** `{dist_str}`")
                    if trace2:
                        st.markdown("Lintasan: " + " → ".join(f"`{s}`" for s in trace2))
                        st.graphviz_chart(
                            build_dfa_graph(dfa2, highlight_state=trace2[-1], accepted=r2).source,
                            use_container_width=True
                        )
