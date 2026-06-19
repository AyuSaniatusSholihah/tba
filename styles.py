"""
styles.py
=========
Semua konstanta desain: warna, CSS tema, CSS animasi, dan komponen
HTML kecil yang dipakai berulang 

"""

# =====================================================================
# Konstanta Warna 
# =====================================================================
COLOR_BASE        = "#1A1210"   # background utama — hampir hitam kecoklatan
COLOR_MANTLE      = "#221814"   # sidebar / topbar
COLOR_CRUST       = "#120C0A"   # paling gelap (shadow, well/inset)
COLOR_SURFACE0    = "#2A1E19"   # card / input background
COLOR_SURFACE1    = "#3D2C24"   # border
COLOR_SURFACE2    = "#4A372D"   # border hover / lebih terang
COLOR_OVERLAY     = "#8A7468"   # teks placeholder / disabled
COLOR_TEXT        = "#F0E6DC"   # teks utama
COLOR_SUBTEXT     = "#B8A599"   # teks sekunder / label

COLOR_PINK        = "#E8A3B0"   # aksen utama (dusty pink)
COLOR_BEIGE       = "#D9C4A8"   # aksen sekunder
COLOR_RED         = "#E08989"   # reject / error (soft red)
COLOR_GREEN       = "#A8C99A"   # accept / sukses (warm sage, selaras coffee tone)
COLOR_YELLOW      = "#E0B989"   # active / processing (warm amber) — entry state langsung
COLOR_DERIVED     = "#A8916B"   # state turunan ε-closure (redup, bukan entry langsung)

# Alias kompatibilitas (dipakai utils.py lama) -> dipetakan ke palet baru
COLOR_BLUE        = COLOR_PINK
COLOR_LAVENDER    = COLOR_BEIGE
COLOR_MAUVE       = COLOR_PINK
COLOR_PEACH       = COLOR_YELLOW


# =====================================================================
# Tipografi
# =====================================================================
FONT_SANS = "'Inter', -apple-system, sans-serif"
FONT_MONO = "'JetBrains Mono', 'Courier New', monospace"

FONT_IMPORT = (
    "@import url('https://fonts.googleapis.com/css2?"
    "family=Inter:wght@400;500;600;700;800"
    "&family=JetBrains+Mono:wght@400;500;600;700"
    "&display=swap');"
)


# =====================================================================
# Layout constants
# =====================================================================
TOPBAR_HEIGHT = 52
SIDEBAR_WIDTH = 220
FORM_COL_WIDTH = 420


# =====================================================================
# CSS Animasi Graphviz (SVG state highlight)
# =====================================================================
ANIM_CSS = f"""
<style>
@keyframes glow-active {{
    0%   {{ stroke: {COLOR_YELLOW}; stroke-width: 3;   filter: drop-shadow(0 0 4px  {COLOR_YELLOW}) drop-shadow(0 0 10px {COLOR_YELLOW}80); }}
    50%  {{ stroke: {COLOR_PINK};   stroke-width: 4.5; filter: drop-shadow(0 0 10px {COLOR_PINK})   drop-shadow(0 0 22px {COLOR_PINK}80); }}
    100% {{ stroke: {COLOR_YELLOW}; stroke-width: 3;   filter: drop-shadow(0 0 4px  {COLOR_YELLOW}) drop-shadow(0 0 10px {COLOR_YELLOW}80); }}
}}
@keyframes glow-derived {{
    0%   {{ stroke: {COLOR_DERIVED}; stroke-width: 2;   filter: drop-shadow(0 0 2px {COLOR_DERIVED}60); }}
    50%  {{ stroke: {COLOR_DERIVED}; stroke-width: 2.5; filter: drop-shadow(0 0 5px {COLOR_DERIVED}90); }}
    100% {{ stroke: {COLOR_DERIVED}; stroke-width: 2;   filter: drop-shadow(0 0 2px {COLOR_DERIVED}60); }}
}}
@keyframes glow-accept {{
    0%   {{ stroke: {COLOR_GREEN}; stroke-width: 3; filter: drop-shadow(0 0 4px  {COLOR_GREEN}) drop-shadow(0 0 12px {COLOR_GREEN}80); }}
    50%  {{ stroke: {COLOR_GREEN}; stroke-width: 5; filter: drop-shadow(0 0 14px {COLOR_GREEN}) drop-shadow(0 0 28px {COLOR_GREEN}b0); }}
    100% {{ stroke: {COLOR_GREEN}; stroke-width: 3; filter: drop-shadow(0 0 4px  {COLOR_GREEN}) drop-shadow(0 0 12px {COLOR_GREEN}80); }}
}}
@keyframes glow-reject {{
    0%   {{ stroke: {COLOR_RED}; stroke-width: 3; filter: drop-shadow(0 0 4px  {COLOR_RED}) drop-shadow(0 0 10px {COLOR_RED}80); }}
    33%  {{ stroke: {COLOR_RED}; stroke-width: 5; filter: drop-shadow(0 0 14px {COLOR_RED}) drop-shadow(0 0 28px {COLOR_RED}b0); }}
    66%  {{ stroke: {COLOR_RED}; stroke-width: 3; filter: drop-shadow(0 0 4px  {COLOR_RED}) drop-shadow(0 0 10px {COLOR_RED}80); }}
    100% {{ stroke: {COLOR_RED}; stroke-width: 5; filter: drop-shadow(0 0 14px {COLOR_RED}) drop-shadow(0 0 28px {COLOR_RED}b0); }}
}}
@keyframes scale-breathe {{
    0%   {{ transform: scale(1);    }}
    50%  {{ transform: scale(1.09); }}
    100% {{ transform: scale(1);    }}
}}
.state-active ellipse, .state-active polygon {{
    animation: glow-active 1s ease-in-out infinite;
    transform-origin: center;
    transform-box: fill-box;
}}
.state-active text {{
    animation: scale-breathe 1s ease-in-out infinite;
    transform-origin: center;
    transform-box: fill-box;
}}
.state-derived ellipse, .state-derived polygon {{
    animation: glow-derived 1.6s ease-in-out infinite;
    transform-origin: center;
    transform-box: fill-box;
}}
.state-accepted ellipse, .state-accepted polygon {{
    animation: glow-accept 0.8s ease-in-out infinite;
    transform-origin: center;
    transform-box: fill-box;
}}
.state-rejected ellipse, .state-rejected polygon {{
    animation: glow-reject 0.5s ease-in-out 4;
    transform-origin: center;
    transform-box: fill-box;
}}
.edge-epsilon-path path {{
    stroke-dasharray: 4 3;
    animation: dash-flow 0.6s linear infinite;
}}
@keyframes dash-flow {{
    0%   {{ stroke-dashoffset: 14; }}
    100% {{ stroke-dashoffset: 0; }}
}}
svg {{ width: 100% !important; height: auto !important; }}
</style>
"""

# Template pembungkus SVG agar background sesuai tema
SVG_WRAPPER = (
    '<div style="background:{bg}; border-radius:12px; padding:10px; '
    'border:1px solid {border}; overflow:auto; height:{height}px; '
    'display:flex; align-items:center; justify-content:center;">'
    '{svg}'
    '</div>'
)


# =====================================================================
# Komponen HTML kecil yang dipakai berulang di semua modul fitur
# =====================================================================

def render_dead_state_notice(remaining_input):
    """
    Notice kecil saat NFA kehilangan semua state aktif (mati) sebelum seluruh
    string habis dibaca — animasi berhenti BUKAN karena string selesai, tapi
    karena tidak ada lagi transisi yang valid. Sisa input tidak diproses
    karena hasilnya sudah pasti tertolak.
    """
    return f"""
    <div class="dead-state-notice">
        <span class="dead-state-icon">⊘</span>
        <span class="dead-state-text">
            NFA kehabisan state aktif (mati) sebelum string selesai dibaca.
            Sisa input <code>{remaining_input}</code> tidak diproses karena hasil sudah pasti DITOLAK.
        </span>
    </div>
    """


def render_meta_row(step, symbol, remainder):
    """Baris meta info: step saat ini, simbol dibaca, sisa input — 3 chip terpisah."""
    return f"""
    <div class="meta-row">
        <div class="meta-item">
            <span class="meta-label">STEP</span>
            <span class="meta-value">{step}</span>
        </div>
        <div class="meta-item">
            <span class="meta-label">SIMBOL</span>
            <span class="meta-value">{symbol}</span>
        </div>
        <div class="meta-item">
            <span class="meta-label">SISA INPUT</span>
            <span class="meta-value">{remainder}</span>
        </div>
    </div>
    """


def render_result_banner(accepted, label="", accept_text="DITERIMA", reject_text="DITOLAK"):
    """Banner hasil akhir accept/reject, full-width, warna sesuai status.
    accept_text/reject_text bisa dioverride untuk konteks non-DFA-run,
    misal 'EKUIVALEN' / 'TIDAK EKUIVALEN' pada modul ekuivalensi.
    """
    if accepted is None:
        return ""
    if accepted:
        return f"""
        <div class="result-banner banner-accept">
            <span class="banner-icon">✓</span>
            <span class="banner-text">{accept_text}{(' — ' + label) if label else ''}</span>
        </div>
        """
    return f"""
    <div class="result-banner banner-reject">
        <span class="banner-icon">✕</span>
        <span class="banner-text">{reject_text}{(' — ' + label) if label else ''}</span>
    </div>
    """


def render_trace_chips(states, current_index=None, edge_symbols=None):
    """
    Render lintasan state sebagai chip-chip berurutan dengan panah mono di antaranya.
    states: list label state (str) berurutan
    current_index: index chip yang dianggap "current" (highlight beda)
    edge_symbols: list simbol antar-state (len = len(states)-1), ditampilkan kecil di atas panah
    """
    parts = []
    for i, s in enumerate(states):
        cls = "trace-chip"
        if current_index is not None and i == current_index:
            cls += " trace-chip-current"
        parts.append(f'<span class="{cls}">{s}</span>')
        if i < len(states) - 1:
            sym_label = ""
            if edge_symbols and i < len(edge_symbols):
                sym_label = f'<span class="trace-arrow-sym">{edge_symbols[i]}</span>'
            parts.append(f'<span class="trace-arrow">{sym_label}→</span>')
    return f'<div class="trace-chip-row">{"".join(parts)}</div>'


def render_set_chip_row(label_sets, current_index=None):
    """
    Untuk NFA: tiap step punya SET state aktif, bukan satu state.
    label_sets: list of list-of-str, tiap elemen adalah set state aktif pada step itu.
    """
    parts = []
    for i, group in enumerate(label_sets):
        cls = "trace-group"
        if current_index is not None and i == current_index:
            cls += " trace-group-current"
        inner = "".join(f'<span class="trace-chip trace-chip-sm">{g}</span>' for g in sorted(group)) or '<span class="trace-chip trace-chip-empty">∅</span>'
        parts.append(f'<div class="{cls}">{inner}</div>')
        if i < len(label_sets) - 1:
            parts.append('<span class="trace-arrow">→</span>')
    return f'<div class="trace-chip-row trace-chip-row-wrap">{"".join(parts)}</div>'


# =====================================================================
# CSS Tema Streamlit — Layout shell (topbar, sidebar, columns, components)
# =====================================================================

THEME_CSS = f"""
<style>
{FONT_IMPORT}

html, body, [class*="css"] {{
    font-family: {FONT_SANS};
}}

h1, h2, h3, h4 {{
    font-family: {FONT_MONO};
    letter-spacing: -0.01em;
}}

code, pre, .stTextInput input, .stTextArea textarea {{
    font-family: {FONT_MONO} !important;
}}

/* ── Base app background ── */
.stApp {{
    background: {COLOR_BASE};
}}

/* Hilangkan padding atas default supaya topbar custom menempel rapi */
.main .block-container {{
    padding-top: {TOPBAR_HEIGHT + 24}px !important;
    max-width: 100% !important;
}}

/* Sembunyikan header bawaan Streamlit (kosong, dipakai topbar custom) */
[data-testid="stHeader"] {{
    background: transparent !important;
    height: 0px !important;
}}
[data-testid="stToolbar"] {{
    display: none !important;
}}

/* ── Topbar custom (52px, sticky) ── */
.app-topbar {{
    position: fixed;
    top: 0; left: 0; right: 0;
    height: {TOPBAR_HEIGHT}px;
    background: {COLOR_MANTLE};
    border-bottom: 1px solid {COLOR_SURFACE1};
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 24px;
    z-index: 999999;
}}
.app-topbar .brand {{
    display: flex;
    align-items: center;
    gap: 10px;
}}
.app-topbar .brand-mark {{
    width: 22px; height: 22px;
    border-radius: 6px;
    background: linear-gradient(135deg, {COLOR_PINK}, {COLOR_BEIGE});
    display: flex; align-items: center; justify-content: center;
    font-family: {FONT_MONO};
    font-weight: 700;
    font-size: 12px;
    color: {COLOR_BASE};
}}
.app-topbar .brand-name {{
    font-family: {FONT_MONO};
    font-weight: 600;
    font-size: 14px;
    color: {COLOR_TEXT};
    letter-spacing: -0.01em;
}}
.app-topbar .brand-sub {{
    font-family: {FONT_SANS};
    font-size: 11px;
    color: {COLOR_SUBTEXT};
    margin-left: 4px;
}}

/* ── Sidebar (220px fixed) ── */
[data-testid="stSidebar"] {{
    background: {COLOR_MANTLE} !important;
    border-right: 1px solid {COLOR_SURFACE1} !important;
    min-width: {SIDEBAR_WIDTH}px !important;
    max-width: {SIDEBAR_WIDTH}px !important;
    margin-top: {TOPBAR_HEIGHT}px;
}}
[data-testid="stSidebar"] > div {{
    padding-top: 20px;
}}
.sidebar-eyebrow {{
    font-family: {FONT_MONO};
    font-size: 10px;
    letter-spacing: 0.12em;
    color: {COLOR_OVERLAY};
    padding: 0 8px 12px 8px;
    text-transform: uppercase;
}}

/* Nav item: secondary = inactive, primary = active modul saat ini */
[data-testid="stSidebar"] .stButton > button {{
    width: 100%;
    text-align: left;
    border-radius: 8px;
    font-family: {FONT_MONO} !important;
    font-size: 13px;
    font-weight: 500;
    padding: 9px 12px;
    margin-bottom: 2px;
    box-shadow: none !important;
    transition: all 0.15s ease;
}}
[data-testid="stSidebar"] .stButton > button p {{
    font-family: {FONT_MONO} !important;
    text-align: left;
}}
/* Secondary (inactive nav item) */
[data-testid="stSidebar"] button[kind="secondary"] {{
    background: transparent !important;
    border: 1px solid transparent !important;
    color: {COLOR_SUBTEXT} !important;
}}
[data-testid="stSidebar"] button[kind="secondary"]:hover {{
    background: {COLOR_SURFACE0} !important;
    color: {COLOR_TEXT} !important;
    transform: none !important;
}}
[data-testid="stSidebar"] button[kind="secondary"] * {{
    color: inherit !important;
    background: transparent !important;
}}
/* Primary (active nav item) */
[data-testid="stSidebar"] button[kind="primary"] {{
    background: {COLOR_SURFACE0} !important;
    border: 1px solid {COLOR_SURFACE2} !important;
    color: {COLOR_PINK} !important;
}}
[data-testid="stSidebar"] button[kind="primary"]:hover {{
    background: {COLOR_SURFACE0} !important;
    border-color: {COLOR_PINK} !important;
    transform: none !important;
}}
[data-testid="stSidebar"] button[kind="primary"] * {{
    color: {COLOR_PINK} !important;
    background: transparent !important;
}}

/* ── Typography ── */
h1 {{
    color: {COLOR_TEXT} !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em;
}}
h2, h3 {{ color: {COLOR_PINK} !important; font-weight: 600 !important; }}
p, li, label {{ color: {COLOR_TEXT} !important; font-family: {FONT_SANS}; }}
.stCaption {{ color: {COLOR_OVERLAY} !important; }}

/* ── Fixed-width form column helper ── */
.form-col-wrapper {{
    max-width: {FORM_COL_WIDTH}px;
}}

/* ── Section eyebrow (numbering label gaya mono) ── */
.section-eyebrow {{
    font-family: {FONT_MONO};
    font-size: 11px;
    letter-spacing: 0.1em;
    color: {COLOR_BEIGE};
    text-transform: uppercase;
    margin-bottom: 4px;
}}

/* ── Meta row (3 info chip: step / simbol / sisa) ── */
.meta-row {{
    display: flex;
    gap: 10px;
    margin: 14px 0;
}}
.meta-item {{
    flex: 1;
    background: {COLOR_SURFACE0};
    border: 1px solid {COLOR_SURFACE1};
    border-radius: 8px;
    padding: 8px 12px;
    display: flex;
    flex-direction: column;
    gap: 2px;
}}
.meta-label {{
    font-family: {FONT_MONO};
    font-size: 9px;
    letter-spacing: 0.1em;
    color: {COLOR_OVERLAY};
}}
.meta-value {{
    font-family: {FONT_MONO};
    font-size: 14px;
    font-weight: 600;
    color: {COLOR_TEXT};
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}}

/* ── Result banner (accept/reject) ── */
.result-banner {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 14px 18px;
    border-radius: 10px;
    margin: 14px 0;
    font-family: {FONT_MONO};
    font-weight: 600;
    font-size: 14px;
}}
.banner-accept {{
    background: rgba(168, 201, 154, 0.12);
    border: 1px solid {COLOR_GREEN};
    color: {COLOR_GREEN};
}}
.banner-reject {{
    background: rgba(224, 137, 137, 0.12);
    border: 1px solid {COLOR_RED};
    color: {COLOR_RED};
}}
.banner-icon {{
    font-size: 16px;
}}

/* ── Dead-state notice (NFA kehabisan state aktif sebelum string selesai) ── */
.dead-state-notice {{
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 10px 14px;
    border-radius: 8px;
    margin: 10px 0;
    background: rgba(224, 137, 137, 0.06);
    border: 1px dashed {COLOR_RED};
}}
.dead-state-icon {{
    font-size: 14px;
    color: {COLOR_RED};
    line-height: 1.4;
}}
.dead-state-text {{
    font-family: {FONT_SANS};
    font-size: 12px;
    color: {COLOR_SUBTEXT};
    line-height: 1.5;
}}
.dead-state-text code {{
    font-family: {FONT_MONO};
    color: {COLOR_BEIGE};
    background: {COLOR_MANTLE};
    padding: 1px 5px;
    border-radius: 4px;
}}

/* ── Trace chips ── */
.trace-chip-row {{
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 4px;
    padding: 12px;
    background: {COLOR_SURFACE0};
    border: 1px solid {COLOR_SURFACE1};
    border-radius: 8px;
    margin: 10px 0;
}}
.trace-chip-row-wrap {{
    align-items: center;
}}
.trace-chip {{
    font-family: {FONT_MONO};
    font-size: 12px;
    font-weight: 600;
    color: {COLOR_SUBTEXT};
    background: {COLOR_MANTLE};
    border: 1px solid {COLOR_SURFACE1};
    border-radius: 6px;
    padding: 4px 10px;
}}
.trace-chip-sm {{
    font-size: 11px;
    padding: 2px 7px;
}}
.trace-chip-current {{
    color: {COLOR_BASE};
    background: {COLOR_PINK};
    border-color: {COLOR_PINK};
}}
.trace-chip-empty {{
    color: {COLOR_OVERLAY};
    font-style: italic;
}}
.trace-group {{
    display: flex;
    gap: 3px;
    padding: 4px;
    border-radius: 6px;
    flex-wrap: wrap;
    align-content: center;
}}
.trace-group-current {{
    background: rgba(232, 163, 176, 0.1);
    border: 1px dashed {COLOR_PINK};
}}
.trace-arrow {{
    font-family: {FONT_MONO};
    color: {COLOR_OVERLAY};
    font-size: 12px;
    display: flex;
    flex-direction: column;
    align-items: center;
    align-self: center;
    line-height: 1;
    padding: 0 2px;
}}
.trace-arrow-sym {{
    font-size: 9px;
    color: {COLOR_BEIGE};
    margin-bottom: 1px;
}}

/* ── Metric cards ── */
[data-testid="stMetric"] {{
    background: {COLOR_SURFACE0} !important;
    border: 1px solid {COLOR_SURFACE1} !important;
    border-radius: 10px !important;
    padding: 14px 18px !important;
}}
[data-testid="stMetricLabel"] {{ color: {COLOR_SUBTEXT} !important; font-family: {FONT_MONO} !important; }}
[data-testid="stMetricValue"] {{ color: {COLOR_TEXT} !important; font-family: {FONT_MONO} !important; }}
[data-testid="stMetricDelta"] {{ color: {COLOR_GREEN} !important; }}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {{
    background-color: {COLOR_SURFACE0} !important;
    border: 1px solid {COLOR_SURFACE1} !important;
    border-radius: 8px !important;
    color: {COLOR_TEXT} !important;
    font-family: {FONT_MONO} !important;
    transition: all 0.2s ease;
}}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {{
    border-color: {COLOR_PINK} !important;
    box-shadow: 0 0 0 2px rgba(232,163,176,0.2) !important;
}}
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {{
    color: {COLOR_OVERLAY} !important;
}}

/* ── Buttons (termasuk tombol submit di dalam st.form) ── */
.stButton > button,
.stFormSubmitButton > button {{
    background: linear-gradient(135deg, {COLOR_PINK}, {COLOR_BEIGE}) !important;
    border: 2px solid transparent !important;
    border-radius: 8px;
    font-weight: 600;
    font-family: {FONT_MONO};
    font-size: 13px;
    padding: 10px 20px;
    transition: all 0.2s ease;
}}
.stButton > button:hover,
.stFormSubmitButton > button:hover {{
    transform: translateY(-1px);
    box-shadow: 0 6px 18px rgba(232,163,176,0.3);
}}
.stButton > button:active,
.stFormSubmitButton > button:active {{
    transform: translateY(0px);
    box-shadow: inset 0 3px 5px rgba(0,0,0,0.2) !important;
}}
.stButton > button:focus,
.stFormSubmitButton > button:focus {{
    box-shadow: 0 0 0 2px rgba(232,163,176,0.4) !important;
}}
.stButton > button, .stButton > button *,
.stFormSubmitButton > button, .stFormSubmitButton > button *,
button[data-testid^="stBaseButton"], button[data-testid^="stBaseButton"] * {{
    color: {COLOR_BASE} !important;
}}

/* (styling tombol aksi gradient pink di atas TIDAK berlaku untuk sidebar nav —
   sidebar nav sudah di-override penuh oleh blok button[kind="secondary"/"primary"] di atas) */

/* ── Alerts (fallback untuk st.success/error/info/warning bawaan) ── */
.stSuccess {{ background: rgba(168,201,154,0.08) !important; border-left: 4px solid {COLOR_GREEN}  !important; border-radius: 8px !important; }}
.stError   {{ background: rgba(224,137,137,0.08) !important; border-left: 4px solid {COLOR_RED}    !important; border-radius: 8px !important; }}
.stInfo    {{ background: rgba(217,196,168,0.08) !important; border-left: 4px solid {COLOR_BEIGE}  !important; border-radius: 8px !important; }}
.stWarning {{ background: rgba(224,185,137,0.08) !important; border-left: 4px solid {COLOR_YELLOW} !important; border-radius: 8px !important; }}

/* ── Expander ── */
[data-testid="stExpander"] {{
    background: {COLOR_SURFACE0} !important;
    border: 1px solid {COLOR_SURFACE1} !important;
    border-radius: 10px !important;
}}
[data-testid="stExpander"] summary {{
    font-family: {FONT_MONO} !important;
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
[data-testid="stSelectbox"] > div > div:focus-within {{
    border-color: {COLOR_PINK} !important;
    box-shadow: 0 0 0 2px rgba(232,163,176,0.2) !important;
}}
div[data-baseweb="popover"] {{
    background-color: {COLOR_MANTLE} !important;
    border: 1px solid {COLOR_SURFACE1} !important;
    border-radius: 8px !important;
    box-shadow: 0 10px 25px rgba(0,0,0,0.5) !important;
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
    font-size: 14px !important;
}}
div[data-baseweb="popover"] li:hover,
div[data-baseweb="popover"] li[aria-selected="true"] {{
    background-color: {COLOR_SURFACE0} !important;
    color: {COLOR_PINK} !important;
}}
ul[role="listbox"] {{
    background-color: {COLOR_MANTLE} !important;
    border: 1px solid {COLOR_SURFACE1} !important;
    border-radius: 8px !important;
    padding: 6px !important;
    box-shadow: 0 10px 25px rgba(0,0,0,0.5) !important;
}}
div:has(> ul[role="listbox"]) {{
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}}
li[role="option"] {{
    background-color: transparent !important;
    color: {COLOR_TEXT} !important;
    border-radius: 6px !important;
    padding: 8px 12px !important;
    margin: 2px 0 !important;
}}
li[role="option"] * {{ background-color: transparent !important; color: inherit !important; }}
li[role="option"]:hover,
li[role="option"][aria-selected="true"] {{
    background-color: {COLOR_SURFACE0} !important;
    color: {COLOR_PINK} !important;
}}

/* ── Slider / Toggle ── */
[data-testid="stSlider"] [role="slider"] {{
    background-color: {COLOR_PINK} !important;
}}
[data-testid="stSlider"] > div > div > div > div {{
    background: linear-gradient(90deg, {COLOR_PINK}, {COLOR_BEIGE}) !important;
}}
[data-testid="stTickBarMin"], [data-testid="stTickBarMax"] {{ color: {COLOR_OVERLAY} !important; }}
[data-baseweb="checkbox"] {{ accent-color: {COLOR_PINK}; }}

/* ── Graphviz fallback container ── */
[data-testid="stGraphVizChart"] {{
    background: {COLOR_BASE};
    border: 1px solid {COLOR_SURFACE0};
    border-radius: 12px;
    padding: 8px;
}}

/* ── Canvas panel wrapper (graph 62% / status sisanya) ── */
.canvas-panel {{
    background: {COLOR_SURFACE0};
    border: 1px solid {COLOR_SURFACE1};
    border-radius: 12px;
    padding: 4px;
    margin-bottom: 14px;
}}
.canvas-panel-label {{
    font-family: {FONT_MONO};
    font-size: 10px;
    letter-spacing: 0.1em;
    color: {COLOR_OVERLAY};
    text-transform: uppercase;
    padding: 8px 12px 0 12px;
}}

/* ── FINAL OVERRIDE: sidebar nav text color ──
   Diletakkan di akhir stylesheet supaya pasti menang dari aturan umum
   tombol aksi (yang memaksa warna teks ke COLOR_BASE untuk tombol gradient). */
[data-testid="stSidebar"] button[kind="secondary"],
[data-testid="stSidebar"] button[kind="secondary"] p,
[data-testid="stSidebar"] button[kind="secondary"] span {{
    color: {COLOR_SUBTEXT} !important;
}}
[data-testid="stSidebar"] button[kind="secondary"]:hover,
[data-testid="stSidebar"] button[kind="secondary"]:hover p,
[data-testid="stSidebar"] button[kind="secondary"]:hover span {{
    color: {COLOR_TEXT} !important;
}}
[data-testid="stSidebar"] button[kind="primary"],
[data-testid="stSidebar"] button[kind="primary"] p,
[data-testid="stSidebar"] button[kind="primary"] span {{
    color: {COLOR_PINK} !important;
    background: {COLOR_SURFACE0} !important;
}}
</style>
"""
