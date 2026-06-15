"""
main.py
=======
Entry point aplikasi Streamlit – Smart Automata Simulator
Jalankan dengan: streamlit run main.py
"""

import os
import sys

# ── Fix: tambahkan Graphviz ke PATH agar dot.exe bisa ditemukan ──────────
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

st.set_page_config(
    page_title="Smart Automata Simulator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS: dark premium theme ──────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Background */
    .stApp {
        background: linear-gradient(135deg, #1e1e2e 0%, #181825 60%, #11111b 100%);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1e2e 0%, #181825 100%);
        border-right: 1px solid #313244;
    }

    /* Title & header */
    h1 { color: #cdd6f4 !important; font-weight: 700 !important; }
    h2, h3 { color: #b4befe !important; font-weight: 600 !important; }
    p, li, label { color: #cdd6f4 !important; }
    .stCaption { color: #6c7086 !important; }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: #313244;
        border: 1px solid #45475a;
        border-radius: 12px;
        padding: 16px 20px;
    }
    [data-testid="stMetricLabel"] { color: #a6adc8 !important; }
    [data-testid="stMetricValue"] { color: #cdd6f4 !important; }
    [data-testid="stMetricDelta"] { color: #a6e3a1 !important; }

    /* Inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #313244 !important;
        border: 1px solid #45475a !important;
        border-radius: 8px !important;
        color: #cdd6f4 !important;
        font-family: 'JetBrains Mono', 'Courier New', monospace !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #89b4fa !important;
        box-shadow: 0 0 0 2px rgba(137,180,250,0.2) !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #89b4fa, #b4befe);
        color: #1e1e2e;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        font-size: 14px;
        padding: 10px 20px;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(137,180,250,0.4);
        background: linear-gradient(135deg, #b4befe, #cba6f7);
    }
    .stButton > button:active {
        transform: translateY(0px);
    }

    /* Alerts */
    .stSuccess { background: rgba(166,227,161,0.15) !important; border-left: 4px solid #a6e3a1 !important; }
    .stError   { background: rgba(243,139,168,0.15) !important; border-left: 4px solid #f38ba8 !important; }
    .stInfo    { background: rgba(137,180,250,0.12) !important; border-left: 4px solid #89b4fa !important; }
    .stWarning { background: rgba(249,226,175,0.15) !important; border-left: 4px solid #f9e2af !important; }

    /* Expander */
    [data-testid="stExpander"] {
        background: #181825 !important;
        border: 1px solid #313244 !important;
        border-radius: 12px !important;
    }

    /* Divider */
    hr { border-color: #313244 !important; }

    /* Selectbox */
    [data-testid="stSelectbox"] > div > div {
        background: #313244 !important;
        border: 1px solid #45475a !important;
        border-radius: 8px !important;
        color: #cdd6f4 !important;
    }

    /* Graphviz container */
    [data-testid="stGraphVizChart"] {
        background: #1e1e2e;
        border: 1px solid #313244;
        border-radius: 12px;
        padding: 8px;
    }

    /* Sidebar selectbox label */
    .sidebar-title {
        font-size: 13px;
        color: #6c7086;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

import dfa_testing
import regex_nfa
import dfa_minimization
import dfa_equivalence

# ── Sidebar ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🤖 Automata Simulator")
    st.markdown("<p style='color:#6c7086;font-size:12px;'>Teori Bahasa & Automata</p>", unsafe_allow_html=True)
    st.divider()

    menu = st.selectbox(
        "Pilih Fitur:",
        [
            "① Uji String pada DFA",
            "② Regex → NFA & Uji String",
            "③ Minimisasi DFA",
            "④ Cek Ekuivalensi 2 DFA",
        ],
        label_visibility="collapsed"
    )

    st.divider()
    st.markdown("""
    <div style='color:#6c7086; font-size:11px; line-height:1.8'>
    <b style='color:#a6adc8'>Algoritma yang digunakan:</b><br>
    ① Simulasi DFA + Trace<br>
    ② Konstruksi Thompson<br>
    ③ Partition Refinement<br>
    ④ Product Construction + BFS
    </div>
    """, unsafe_allow_html=True)

# ── Main content ─────────────────────────────────────────────────────────
if menu == "① Uji String pada DFA":
    dfa_testing.render()
elif menu == "② Regex → NFA & Uji String":
    regex_nfa.render()
elif menu == "③ Minimisasi DFA":
    dfa_minimization.render()
elif menu == "④ Cek Ekuivalensi 2 DFA":
    dfa_equivalence.render()
