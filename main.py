"""
main.py
Entry point aplikasi Streamlit - Simulator Automata.
"""

import os

# Konfigurasi Path Graphviz
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
from styles import THEME_CSS

import dfa_testing
import regex_nfa
import dfa_minimization
import dfa_equivalence

# Konfigurasi Halaman
st.set_page_config(
    page_title="Simulator Automata",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Terapkan Tema
st.markdown(THEME_CSS, unsafe_allow_html=True)

# Navigasi Sidebar
with st.sidebar:
    st.markdown("## Simulator Automata")
    st.markdown(
        "<p style='color:#6c7086;font-size:12px;'>Teori Bahasa & Automata</p>",
        unsafe_allow_html=True,
    )
    st.divider()

    menu = st.selectbox(
        "Pilih Fitur:",
        [
            "1. Uji String pada DFA",
            "2. Regex → NFA & Uji String",
            "3. Minimisasi DFA",
            "4. Cek Ekuivalensi 2 DFA",
        ],
        label_visibility="collapsed",
    )

# Routing Fitur
if menu == "1. Uji String pada DFA":
    dfa_testing.render()
elif menu == "2. Regex → NFA & Uji String":
    regex_nfa.render()
elif menu == "3. Minimisasi DFA":
    dfa_minimization.render()
elif menu == "4. Cek Ekuivalensi 2 DFA":
    dfa_equivalence.render()
