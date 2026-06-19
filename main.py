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

# Topbar custom (52px, sticky di atas semua konten)
st.markdown(
    """
    <div class="app-topbar">
        <div class="brand">
            <div class="brand-mark">SA</div>
            <span class="brand-name">Simulator Automata</span>
            <span class="brand-sub">Teori Bahasa &amp; Automata</span>
        </div>
        <a class="topbar-link" href="https://graphviz.org/documentation/" target="_blank">
            Dokumentasi ↗
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)

# Definisi menu navigasi (numbering 01-04)
MENU_ITEMS = [
    ("01", "Uji String DFA"),
    ("02", "Regex → NFA"),
    ("03", "Minimisasi DFA"),
    ("04", "Ekuivalensi DFA"),
]

if "active_menu" not in st.session_state:
    st.session_state["active_menu"] = 0

# Navigasi Sidebar — numbered mono list menggantikan st.selectbox
active = st.session_state["active_menu"]

with st.sidebar:
    st.markdown('<div class="sidebar-eyebrow">Modul</div>', unsafe_allow_html=True)

    for idx, (num, label) in enumerate(MENU_ITEMS):
        is_active = idx == active
        label_text = f"{num}  {label}"
        if st.button(label_text, key=f"nav_{idx}", use_container_width=True,
                     type="primary" if is_active else "secondary"):
            st.session_state["active_menu"] = idx
            st.rerun()

# Routing Fitur
active = st.session_state["active_menu"]
if active == 0:
    dfa_testing.render()
elif active == 1:
    regex_nfa.render()
elif active == 2:
    dfa_minimization.render()
elif active == 3:
    dfa_equivalence.render()
