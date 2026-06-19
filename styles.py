"""
styles.py
=========
Semua konstanta desain: warna, CSS tema, CSS animasi.
Pisahkan desain dari logika program agar mudah diubah.
"""

# Konstanta Warna
COLOR_BASE        = "#09090b"   # background utama (zinc-950)
COLOR_MANTLE      = "#11131a"   # sidebar/panel gelap
COLOR_CRUST       = "#050507"   # paling gelap
COLOR_SURFACE0    = "#181b24"   # card/input background
COLOR_SURFACE1    = "#2c3140"   # border
COLOR_OVERLAY     = "#94a3b8"   # teks sekunder/placeholder (slate-400)
COLOR_TEXT        = "#f8fafc"   # teks utama (slate-50)
COLOR_SUBTEXT     = "#cbd5e1"   # label sekunder (slate-300)
COLOR_BLUE        = "#06b6d4"   # aksen cyan
COLOR_LAVENDER    = "#3b82f6"   # aksen biru
COLOR_MAUVE       = "#8b5cf6"   # aksen ungu
COLOR_GREEN       = "#10b981"   # sukses/accepted (emerald)
COLOR_RED         = "#f43f5e"   # error/rejected (rose)
COLOR_YELLOW      = "#f59e0b"   # warning/active state (amber)
COLOR_PEACH       = "#f97316"   # orange


# CSS Animasi Graphviz
ANIM_CSS = """
<style>
@keyframes glow-active {
    0%   { stroke: #f59e0b; stroke-width: 3;   filter: drop-shadow(0 0 4px  #f59e0b) drop-shadow(0 0 10px #f59e0b80); }
    50%  { stroke: #f97316; stroke-width: 4.5; filter: drop-shadow(0 0 10px #f97316) drop-shadow(0 0 22px #f9731680); }
    100% { stroke: #f59e0b; stroke-width: 3;   filter: drop-shadow(0 0 4px  #f59e0b) drop-shadow(0 0 10px #f59e0b80); }
}
@keyframes glow-accept {
    0%   { stroke: #10b981; stroke-width: 3; filter: drop-shadow(0 0 4px  #10b981) drop-shadow(0 0 12px #10b98180); }
    50%  { stroke: #10b981; stroke-width: 5; filter: drop-shadow(0 0 14px #10b981) drop-shadow(0 0 28px #10b981b0); }
    100% { stroke: #10b981; stroke-width: 3; filter: drop-shadow(0 0 4px  #10b981) drop-shadow(0 0 12px #10b98180); }
}
@keyframes glow-reject {
    0%   { stroke: #f43f5e; stroke-width: 3; filter: drop-shadow(0 0 4px  #f43f5e) drop-shadow(0 0 10px #f43f5e80); }
    33%  { stroke: #f43f5e; stroke-width: 5; filter: drop-shadow(0 0 14px #f43f5e) drop-shadow(0 0 28px #f43f5eb0); }
    66%  { stroke: #f43f5e; stroke-width: 3; filter: drop-shadow(0 0 4px  #f43f5e) drop-shadow(0 0 10px #f43f5e80); }
    100% { stroke: #f43f5e; stroke-width: 5; filter: drop-shadow(0 0 14px #f43f5e) drop-shadow(0 0 28px #f43f5eb0); }
}
@keyframes scale-breathe {
    0%   { transform: scale(1);    }
    50%  { transform: scale(1.09); }
    100% { transform: scale(1);    }
}
.state-active ellipse, .state-active polygon {
    animation: glow-active 1s ease-in-out infinite;
    transform-origin: center;
    transform-box: fill-box;
}
.state-active text {
    animation: scale-breathe 1s ease-in-out infinite;
    transform-origin: center;
    transform-box: fill-box;
}
.state-accepted ellipse, .state-accepted polygon {
    animation: glow-accept 0.8s ease-in-out infinite;
    transform-origin: center;
    transform-box: fill-box;
}
.state-rejected ellipse, .state-rejected polygon {
    animation: glow-reject 0.5s ease-in-out 4;
    transform-origin: center;
    transform-box: fill-box;
}
svg { width: 100% !important; height: auto !important; }
</style>
"""

# Template pembungkus SVG agar background sesuai tema
SVG_WRAPPER = (
    '<div style="background:{bg}; border-radius:12px; padding:10px; '
    'border:1px solid {border}; overflow:auto; height:{height}px;">'
    '{svg}'
    '</div>'
)


# CSS Tema Streamlit

THEME_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Plus Jakarta Sans', sans-serif;
}}

h1, h2, h3, [data-testid="stHeader"] {{
    font-family: 'Outfit', sans-serif;
}}

code, pre, .stTextInput input, .stTextArea textarea {{
    font-family: 'JetBrains Mono', monospace !important;
}}

/* ── Background ── */
.stApp {{
    background: radial-gradient(circle at 50% 0%, #161530 0%, {COLOR_BASE} 70%);
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {COLOR_BASE} 0%, {COLOR_MANTLE} 100%);
    border-right: 1px solid {COLOR_SURFACE1};
}}

/* ── Typography ── */
h1 {{
    color: {COLOR_TEXT} !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #ffffff 30%, {COLOR_BLUE} 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.02em;
}}
h2, h3 {{ color: {COLOR_BLUE} !important; font-weight: 600 !important; }}
p, li, label {{ color: {COLOR_TEXT} !important; }}
.stCaption {{ color: {COLOR_OVERLAY} !important; }}

/* ── Metric cards ── */
[data-testid="stMetric"] {{
    background: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid {COLOR_SURFACE1} !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1) !important;
    backdrop-filter: blur(5px) !important;
    -webkit-backdrop-filter: blur(5px) !important;
}}
[data-testid="stMetricLabel"] {{ color: {COLOR_SUBTEXT} !important; }}
[data-testid="stMetricValue"] {{ color: {COLOR_TEXT} !important; }}
[data-testid="stMetricDelta"] {{ color: {COLOR_GREEN} !important; }}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {{
    background-color: {COLOR_SURFACE0} !important;
    border: 1px solid {COLOR_SURFACE1} !important;
    border-radius: 8px !important;
    color: {COLOR_TEXT} !important;
    font-family: 'JetBrains Mono', monospace !important;
    transition: all 0.2s ease;
}}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {{
    border-color: {COLOR_BLUE} !important;
    box-shadow: 0 0 0 2px rgba(6,182,212,0.2) !important;
}}

/* ── Buttons (termasuk tombol submit di dalam st.form) ── */
.stButton > button,
.stFormSubmitButton > button {{
    background: linear-gradient(135deg, {COLOR_BLUE}, {COLOR_LAVENDER}) !important;
    border: 2px solid transparent !important;
    border-radius: 10px;
    font-weight: 600;
    font-size: 14px;
    padding: 10px 20px;
    transition: all 0.2s ease;
}}
.stButton > button:hover,
.stFormSubmitButton > button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(6,182,212,0.4);
    background: linear-gradient(135deg, {COLOR_LAVENDER}, {COLOR_MAUVE}) !important;
}}
.stButton > button:active,
.stFormSubmitButton > button:active {{
    transform: translateY(0px);
    background: linear-gradient(135deg, {COLOR_PEACH}, {COLOR_YELLOW}) !important;
    border-color: transparent !important;
    box-shadow: inset 0 3px 5px rgba(0,0,0,0.2) !important;
}}
.stButton > button:focus,
.stFormSubmitButton > button:focus {{
    background: linear-gradient(135deg, {COLOR_PEACH}, {COLOR_YELLOW}) !important;
    border-color: transparent !important;
    box-shadow: 0 0 0 2px rgba(249,115,22,0.4) !important;
}}

/* Forcing all button text (including inside paragraphs/spans) to be dark in all states */
.stButton > button,
.stButton > button *,
.stFormSubmitButton > button,
.stFormSubmitButton > button *,
button[data-testid^="stBaseButton"],
button[data-testid^="stBaseButton"] * {{
    color: {COLOR_BASE} !important;
}}

/* ── Alerts ── */
.stSuccess {{ background: rgba(16,185,129,0.06) !important; border-left: 4px solid {COLOR_GREEN} !important; border-radius: 8px !important; }}
.stError   {{ background: rgba(244,63,94,0.06) !important; border-left: 4px solid {COLOR_RED}   !important; border-radius: 8px !important; }}
.stInfo    {{ background: rgba(6,182,212,0.06) !important; border-left: 4px solid {COLOR_BLUE}  !important; border-radius: 8px !important; }}
.stWarning {{ background: rgba(245,158,11,0.06) !important; border-left: 4px solid {COLOR_YELLOW}!important; border-radius: 8px !important; }}

/* ── Expander ── */
[data-testid="stExpander"] {{
    background: rgba(255, 255, 255, 0.01) !important;
    border: 1px solid {COLOR_SURFACE1} !important;
    border-radius: 12px !important;
    backdrop-filter: blur(5px) !important;
    -webkit-backdrop-filter: blur(5px) !important;
}}

/* ── Divider ── */
hr {{ border-color: {COLOR_SURFACE1} !important; }}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {{
    background: {COLOR_SURFACE0} !important;
    border: 1px solid {COLOR_SURFACE1} !important;
    border-radius: 8px !important;
    color: {COLOR_TEXT} !important;
}}
[data-testid="stSelectbox"] > div > div:focus,
[data-testid="stSelectbox"] > div > div:focus-within,
[data-testid="stSelectbox"] > div > div:active {{
    border-color: {COLOR_BLUE} !important;
    box-shadow: 0 0 0 2px rgba(6,182,212,0.2) !important;
}}

/* ── Selectbox Dropdown Menu (Popover) ── */
div[data-baseweb="popover"] {{
    background-color: {COLOR_MANTLE} !important;
    border: 1px solid {COLOR_SURFACE1} !important;
    border-radius: 8px !important;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5) !important;
}}
div[data-baseweb="popover"] ul {{
    background-color: {COLOR_MANTLE} !important;
    border-radius: 8px !important;
    padding: 6px !important;
}}
div[data-baseweb="popover"] li {{
    background-color: transparent !important;
    color: {COLOR_TEXT} !important;
    border-radius: 6px !important;
    padding: 8px 12px !important;
    margin: 2px 0 !important;
    transition: all 0.15s ease !important;
    font-size: 14px !important;
}}
div[data-baseweb="popover"] li:hover,
div[data-baseweb="popover"] li[aria-selected="true"] {{
    background-color: {COLOR_SURFACE0} !important;
    color: {COLOR_BLUE} !important;
    cursor: pointer !important;
}}

/* Direct Selectors for newer Streamlit selectbox listboxes */
ul[role="listbox"] {{
    background-color: {COLOR_MANTLE} !important;
    border: 1px solid {COLOR_SURFACE1} !important;
    border-radius: 8px !important;
    padding: 6px !important;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5) !important;
}}
div:has(> ul[role="listbox"]) {{
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}}
li[role="option"],
.er6m0k90 {{
    background-color: transparent !important;
    color: {COLOR_TEXT} !important;
    border-radius: 6px !important;
    padding: 8px 12px !important;
    margin: 2px 0 !important;
    transition: all 0.15s ease !important;
}}
li[role="option"] *,
.er6m0k90 * {{
    background-color: transparent !important;
    color: inherit !important;
}}
li[role="option"]:hover,
li[role="option"][aria-selected="true"],
.er6m0k90:hover,
.er6m0k90[aria-selected="true"] {{
    background-color: {COLOR_SURFACE0} !important;
    color: {COLOR_BLUE} !important;
    cursor: pointer !important;
}}


/* ── Graphviz fallback container ── */
[data-testid="stGraphVizChart"] {{
    background: {COLOR_BASE};
    border: 1px solid {COLOR_SURFACE0};
    border-radius: 12px;
    padding: 8px;
}}
</style>
"""
