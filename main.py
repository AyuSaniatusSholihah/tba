"""
main.py
=======
Entry point aplikasi Streamlit – Smart Automata Simulator.
Bertugas HANYA untuk:
  1. Setup Graphviz PATH
  2. Konfigurasi halaman
  3. Menerapkan tema (dari styles.py)
  4. Routing sidebar → modul fitur

Jalankan dengan: streamlit run main.py
"""

import os

# ── Fix: tambahkan Graphviz ke PATH agar dot.exe bisa ditemukan ──────
_GRAPHVIZ_CANDIDATES = [
    r"C:\Program Files (x86)\Graphviz\bin",
    r"C:\Program Files\Graphviz\bin",
    r"C:\Graphviz\bin",
]
for _gvpath in _GRAPHVIZ_CANDIDATES:
    if os.path.isfile(os.path.join(_gvpath, "dot.exe")):
        if _gvpath not in os.environ.get("PATH", ""):
            os.environ["PATH"] = _gvpath + os.pathsep + os.environ.get("PATH", "")
        break

import streamlit as st
from styles import THEME_CSS  # ← semua CSS diambil dari sini

import dfa_testing
import regex_nfa
import dfa_minimization
import dfa_equivalence

# ── Konfigurasi halaman ───────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Automata Simulator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Terapkan tema ─────────────────────────────────────────────────────
st.markdown(THEME_CSS, unsafe_allow_html=True)

# ── Sidebar: navigasi ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🤖 Automata Simulator")
    st.markdown(
        "<p style='color:#6c7086;font-size:12px;'>Teori Bahasa & Automata</p>",
        unsafe_allow_html=True,
    )
    st.divider()

    menu = st.selectbox(
        "Pilih Fitur:",
        [
            "① Uji String pada DFA",
            "② Regex → NFA & Uji String",
            "③ Minimisasi DFA",
            "④ Cek Ekuivalensi 2 DFA",
        ],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown(
        """
        <div style='color:#6c7086; font-size:11px; line-height:1.8'>
        <b style='color:#a6adc8'>Algoritma yang digunakan:</b><br>
        ① Simulasi DFA + Trace<br>
        ② Konstruksi Thompson<br>
        ③ Partition Refinement<br>
        ④ Product Construction + BFS
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Routing ke modul fitur ────────────────────────────────────────────
if menu == "① Uji String pada DFA":
    dfa_testing.render()
elif menu == "② Regex → NFA & Uji String":
    regex_nfa.render()
elif menu == "③ Minimisasi DFA":
    dfa_minimization.render()
elif menu == "④ Cek Ekuivalensi 2 DFA":
    dfa_equivalence.render()
