"""
styles.py
=========
Semua konstanta desain: warna, CSS tema, CSS animasi.
Pisahkan desain dari logika program agar mudah diubah.
"""

# =====================================================================
# ========================= WARNA / TOKENS ============================
# =====================================================================

# Palette: Catppuccin Mocha
COLOR_BASE        = "#1e1e2e"   # background utama
COLOR_MANTLE      = "#181825"   # sidebar/panel gelap
COLOR_CRUST       = "#11111b"   # paling gelap
COLOR_SURFACE0    = "#313244"   # card/input background
COLOR_SURFACE1    = "#45475a"   # border
COLOR_OVERLAY     = "#6c7086"   # teks sekunder/placeholder
COLOR_TEXT        = "#cdd6f4"   # teks utama
COLOR_SUBTEXT     = "#a6adc8"   # label sekunder
COLOR_BLUE        = "#89b4fa"   # aksen biru
COLOR_LAVENDER    = "#b4befe"   # aksen lavender
COLOR_MAUVE       = "#cba6f7"   # aksen ungu
COLOR_GREEN       = "#a6e3a1"   # sukses/accepted
COLOR_RED         = "#f38ba8"   # error/rejected
COLOR_YELLOW      = "#f9e2af"   # warning/active state
COLOR_PEACH       = "#fab387"   # highlight edge


# =====================================================================
# ================== CSS ANIMASI GRAPHVIZ (SVG) =======================
# =====================================================================

ANIM_CSS = """
<style>
@keyframes glow-active {
    0%   { stroke: #f9e2af; stroke-width: 3;   filter: drop-shadow(0 0 4px  #f9e2af) drop-shadow(0 0 10px #f9e2af80); }
    50%  { stroke: #fab387; stroke-width: 4.5; filter: drop-shadow(0 0 10px #fab387) drop-shadow(0 0 22px #fab38780); }
    100% { stroke: #f9e2af; stroke-width: 3;   filter: drop-shadow(0 0 4px  #f9e2af) drop-shadow(0 0 10px #f9e2af80); }
}
@keyframes glow-accept {
    0%   { stroke: #a6e3a1; stroke-width: 3; filter: drop-shadow(0 0 4px  #a6e3a1) drop-shadow(0 0 12px #a6e3a180); }
    50%  { stroke: #a6e3a1; stroke-width: 5; filter: drop-shadow(0 0 14px #a6e3a1) drop-shadow(0 0 28px #a6e3a1b0); }
    100% { stroke: #a6e3a1; stroke-width: 3; filter: drop-shadow(0 0 4px  #a6e3a1) drop-shadow(0 0 12px #a6e3a180); }
}
@keyframes glow-reject {
    0%   { stroke: #f38ba8; stroke-width: 3; filter: drop-shadow(0 0 4px  #f38ba8) drop-shadow(0 0 10px #f38ba880); }
    33%  { stroke: #f38ba8; stroke-width: 5; filter: drop-shadow(0 0 14px #f38ba8) drop-shadow(0 0 28px #f38ba8b0); }
    66%  { stroke: #f38ba8; stroke-width: 3; filter: drop-shadow(0 0 4px  #f38ba8) drop-shadow(0 0 10px #f38ba880); }
    100% { stroke: #f38ba8; stroke-width: 5; filter: drop-shadow(0 0 14px #f38ba8) drop-shadow(0 0 28px #f38ba8b0); }
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


# =====================================================================
# =================== CSS TEMA STREAMLIT ==============================
# =====================================================================

THEME_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

/* ── Background ── */
.stApp {{
    background: linear-gradient(135deg, {COLOR_BASE} 0%, {COLOR_MANTLE} 60%, {COLOR_CRUST} 100%);
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {COLOR_BASE} 0%, {COLOR_MANTLE} 100%);
    border-right: 1px solid {COLOR_SURFACE0};
}}

/* ── Typography ── */
h1 {{ color: {COLOR_TEXT} !important; font-weight: 700 !important; }}
h2, h3 {{ color: {COLOR_LAVENDER} !important; font-weight: 600 !important; }}
p, li, label {{ color: {COLOR_TEXT} !important; }}
.stCaption {{ color: {COLOR_OVERLAY} !important; }}

/* ── Metric cards ── */
[data-testid="stMetric"] {{
    background: {COLOR_SURFACE0};
    border: 1px solid {COLOR_SURFACE1};
    border-radius: 12px;
    padding: 16px 20px;
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
    font-family: 'JetBrains Mono', 'Courier New', monospace !important;
}}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {{
    border-color: {COLOR_BLUE} !important;
    box-shadow: 0 0 0 2px rgba(137,180,250,0.2) !important;
}}

/* ── Buttons ── */
.stButton > button {{
    background: linear-gradient(135deg, {COLOR_BLUE}, {COLOR_LAVENDER}) !important;
    border: 2px solid transparent !important;
    border-radius: 10px;
    font-weight: 600;
    font-size: 14px;
    padding: 10px 20px;
    transition: all 0.2s ease;
}}
.stButton > button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(137,180,250,0.4);
    background: linear-gradient(135deg, {COLOR_LAVENDER}, {COLOR_MAUVE}) !important;
}}
.stButton > button:active {{
    transform: translateY(0px);
    background: linear-gradient(135deg, {COLOR_PEACH}, {COLOR_YELLOW}) !important;
    border-color: transparent !important;
    box-shadow: inset 0 3px 5px rgba(0,0,0,0.2) !important;
}}
.stButton > button:focus {{
    background: linear-gradient(135deg, {COLOR_PEACH}, {COLOR_YELLOW}) !important;
    border-color: transparent !important;
    box-shadow: 0 0 0 2px rgba(254,179,135,0.4) !important;
}}

/* Forcing all button text (including inside paragraphs/spans) to be dark in all states */
.stButton > button,
.stButton > button *,
button[data-testid^="stBaseButton"],
button[data-testid^="stBaseButton"] * {{
    color: {COLOR_BASE} !important;
}}

/* ── Alerts ── */
.stSuccess {{ background: rgba(166,227,161,0.15) !important; border-left: 4px solid {COLOR_GREEN} !important; }}
.stError   {{ background: rgba(243,139,168,0.15) !important; border-left: 4px solid {COLOR_RED}   !important; }}
.stInfo    {{ background: rgba(137,180,250,0.12) !important; border-left: 4px solid {COLOR_BLUE}  !important; }}
.stWarning {{ background: rgba(249,226,175,0.15) !important; border-left: 4px solid {COLOR_YELLOW}!important; }}

/* ── Expander ── */
[data-testid="stExpander"] {{
    background: {COLOR_MANTLE} !important;
    border: 1px solid {COLOR_SURFACE0} !important;
    border-radius: 12px !important;
}}

/* ── Divider ── */
hr {{ border-color: {COLOR_SURFACE0} !important; }}

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
    box-shadow: 0 0 0 2px rgba(137,180,250,0.2) !important;
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
