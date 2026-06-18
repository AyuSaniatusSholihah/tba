# Smart Automata Simulator

Aplikasi web interaktif untuk simulasi Teori Bahasa & Automata (TBA), dibangun dengan Python dan Streamlit.

## Fitur

| # | Fitur | Algoritma |
|---|-------|-----------|
| 1 | Uji string pada DFA | Trace sekuensial |
| 2 | Konversi Regex → NFA & uji string | Thompson's Construction + ε-closure |
| 3 | Minimisasi DFA | Partition Refinement (Myhill-Nerode) |
| 4 | Cek ekuivalensi dua DFA | Product Construction + BFS |

## Instalasi

### Prasyarat
- Python 3.10+
- [Graphviz](https://graphviz.org/download/) (wajib diinstall dan ditambahkan ke PATH)

### Langkah

```bash
# 1. Clone repository
git clone <url-repo>
cd <nama-folder>

# 2. (Opsional) Buat virtual environment
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Jalankan aplikasi
streamlit run main.py
```

Aplikasi akan terbuka otomatis di browser pada `http://localhost:8501`.

## Struktur File

```
├── main.py               # Entry point — routing sidebar ke tiap fitur
├── engine.py             # Core engine: DFA, NFA, RegexParser, minimize, equivalence
├── utils.py              # Helper: parser input, visualisasi Graphviz & animasi SVG
├── styles.py             # Tema CSS & konstanta warna
├── dfa_testing.py        # UI Fitur 1 — Uji string pada DFA
├── regex_nfa.py          # UI Fitur 2 — Regex → NFA & uji string
├── dfa_minimization.py   # UI Fitur 3 — Minimisasi DFA
├── dfa_equivalence.py    # UI Fitur 4 — Cek ekuivalensi dua DFA
├── .streamlit/
│   └── config.toml       # Konfigurasi tema Streamlit
└── requirements.txt      # Daftar dependencies Python
```

## Format Input Transisi

Tiap baris pada field transisi mengikuti format:

```
state_asal, simbol, state_tujuan
```

Contoh:

```
q0, 0, q0
q0, 1, q1
q1, 0, q2
```

Baris kosong dan baris diawali `#` diabaikan (bisa dipakai sebagai komentar).