import streamlit as st
import pandas as pd
import json
from pathlib import Path

# ─────────────────────────────────────────────
#  PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="EXPLORE AH | Crime Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
.stApp { background-color: #F8FAFC; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(170deg, #1a3558 0%, #25507d 60%, #1e4570 100%);
}
[data-testid="stSidebar"] .stRadio label { color: #CBD8E8 !important; font-size: 13px !important; }
[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {
    color: #CBD8E8; font-size: 13px;
}

/* ── Metric cards ── */
.metric-card {
    background: white; border-radius: 14px; padding: 20px 22px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07); border: 1px solid #EEF2F7;
}
.metric-label { font-size: 11px; font-weight: 600; color: #64748B;
    text-transform: uppercase; letter-spacing: 0.7px; margin-bottom: 6px; }
.metric-value { font-size: 28px; font-weight: 800; color: #1a3558; line-height: 1; }
.metric-sub { font-size: 12px; color: #94A3B8; margin-top: 5px; }
.badge { display:inline-block; padding:2px 9px; border-radius:20px;
    font-size:11px; font-weight:600; margin-top:6px; }
.badge-red { background:#FEE2E2; color:#DC2626; }
.badge-green { background:#DCFCE7; color:#16A34A; }
.badge-blue { background:#DBEAFE; color:#2563EB; }
.badge-orange { background:#FEF3C7; color:#D97706; }
.badge-purple { background:#F3E8FF; color:#7C3AED; }

/* ── Section headers ── */
.page-title { font-size:26px; font-weight:800; color:#1a3558; }
.page-sub { font-size:14px; color:#64748B; margin-top:2px; margin-bottom:22px; }
.sec-title { font-size:16px; font-weight:700; color:#1a3558;
    padding-bottom:8px; border-bottom:2px solid #E2EAF4; margin-bottom:6px; }
.sec-sub { font-size:12px; color:#64748B; margin-bottom:14px; }

/* ── Content cards ── */
.card {
    background:white; border-radius:12px; padding:18px 20px;
    box-shadow:0 1px 4px rgba(0,0,0,0.06); border:1px solid #EEF2F7; margin-bottom:12px;
}
.card h4 { font-size:14px; font-weight:600; color:#1a3558; margin:0 0 8px 0; }
.card p  { font-size:13px; color:#475569; margin:0; line-height:1.65; }

/* ── Highlight boxes ── */
.box-blue {
    background: linear-gradient(135deg,#EFF6FF,#DBEAFE);
    border-left:4px solid #3B82F6; border-radius:0 8px 8px 0;
    padding:13px 16px; margin:10px 0;
}
.box-blue p { font-size:13px; color:#1e3a5f; margin:0; line-height:1.65; }
.box-warn {
    background: linear-gradient(135deg,#FFFBEB,#FEF3C7);
    border-left:4px solid #F59E0B; border-radius:0 8px 8px 0;
    padding:13px 16px; margin:10px 0;
}
.box-warn p { font-size:13px; color:#78350F; margin:0; line-height:1.65; }
.box-green {
    background: linear-gradient(135deg,#F0FDF4,#DCFCE7);
    border-left:4px solid #22C55E; border-radius:0 8px 8px 0;
    padding:13px 16px; margin:10px 0;
}
.box-green p { font-size:13px; color:#14532D; margin:0; line-height:1.65; }

/* ── Image card ── */
.img-card {
    background:white; border-radius:12px; padding:14px;
    box-shadow:0 1px 4px rgba(0,0,0,0.06); border:1px solid #EEF2F7;
}
.img-cap { font-size:11px; color:#94A3B8; text-align:center;
    margin-top:8px; font-style:italic; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap:4px; background:#F1F5F9; border-radius:10px; padding:4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius:7px; padding:7px 15px; font-size:13px;
    font-weight:500; color:#64748B;
}
.stTabs [aria-selected="true"] {
    background:white !important; color:#1a3558 !important;
    font-weight:600; box-shadow:0 1px 4px rgba(0,0,0,0.1);
}

/* ── Misc ── */
#MainMenu{visibility:hidden;} footer{visibility:hidden;} header{visibility:hidden;}
.stDeployButton{display:none;}
.divider { height:1px; background:linear-gradient(90deg,#E2EAF4,transparent); margin:18px 0; }

/* ── Sidebar brand ── */
.brand-title { font-size:22px; font-weight:800; color:white; letter-spacing:-0.5px; }
.brand-sub { font-size:10px; color:#93C5FD; font-weight:500;
    letter-spacing:1.2px; text-transform:uppercase; }
.sidebar-footer { font-size:11px; color:#93C5FD; text-align:center; line-height:1.7; }
.sidebar-footer strong { color:white; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PATHS
# ─────────────────────────────────────────────
BASE = Path(".")
def p(*args): return BASE.joinpath(*args)

# ─────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────
def show_image(path, caption=None):
    fp = Path(path)
    if fp.exists():
        st.markdown('<div class="img-card">', unsafe_allow_html=True)
        st.image(str(fp), use_container_width=True)
        if caption:
            st.markdown(f'<div class="img-cap">{caption}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info(f"Gambar tidak ditemukan: {fp.name}")

def load_csv(path, **kw):
    fp = Path(path)
    if fp.exists():
        try:
            return pd.read_csv(fp, **kw)
        except Exception as e:
            st.warning(f"Gagal membaca {fp.name}: {e}")
    return None

def load_json(path):
    fp = Path(path)
    if fp.exists():
        try:
            with open(fp) as f:
                return json.load(f)
        except Exception as e:
            st.warning(f"Gagal membaca {fp.name}: {e}")
    return None

def metric_card(label, value, sub=None, badge=None, btype="blue"):
    badge_html = f'<div class="badge badge-{btype}">{badge}</div>' if badge else ""
    sub_html   = f'<div class="metric-sub">{sub}</div>' if sub else ""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {sub_html}{badge_html}
    </div>""", unsafe_allow_html=True)

def section(title, sub=None):
    st.markdown(f'<div class="sec-title">{title}</div>', unsafe_allow_html=True)
    if sub:
        st.markdown(f'<div class="sec-sub">{sub}</div>', unsafe_allow_html=True)

def page_header(title, sub=None):
    st.markdown(f'<div class="page-title">{title}</div>', unsafe_allow_html=True)
    if sub:
        st.markdown(f'<div class="page-sub">{sub}</div>', unsafe_allow_html=True)

def box(text, kind="blue"):
    cls = {"blue": "box-blue", "warn": "box-warn", "green": "box-green"}.get(kind, "box-blue")
    st.markdown(f'<div class="{cls}"><p>{text}</p></div>', unsafe_allow_html=True)

def card(title, body):
    st.markdown(f'<div class="card"><h4>{title}</h4><p>{body}</p></div>',
                unsafe_allow_html=True)

def divider():
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SIDEBAR NAVIGATION
# ─────────────────────────────────────────────
PAGES = [
    "Overview",
    "Exploratory Data Analysis",
    "Clustering Spasiotemporal",
    "Association Rule Mining",
    "Klasifikasi Prediktif",
    "Analisis Spasial",
    "Forecasting",
    "Causal Inference",
    "Survival Analysis",
    "Fairness Audit",
    "Tentang Penelitian",
]

with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:10px 0 18px 0;">
        <div class="brand-title">EXPLORE AH</div>
        <div class="brand-sub">Crime Analytics Dashboard</div>
    </div>
    <hr style="border-color:rgba(255,255,255,0.12);margin:0 0 10px 0;">
    """, unsafe_allow_html=True)

    selected = st.radio("nav", PAGES, label_visibility="collapsed")

    st.markdown("""
    <hr style="border-color:rgba(255,255,255,0.12);margin:12px 0 10px 0;">
    <div class="sidebar-footer">
        <strong>Tim Juara di Malang</strong><br>
        Nazril &amp; Habib<br>
        S1 Sains Data &mdash; Unesa<br>
        <span style="color:#60A5FA;font-size:10px;">EXPLORE AH 2024</span>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  PAGE: OVERVIEW
# ══════════════════════════════════════════════
def page_overview():
    page_header(
        "Los Angeles Crime Analytics",
        "Analisis komprehensif data kejahatan LAPD 2020-2024 menggunakan pendekatan data mining multi-pilar"
    )

    # KPI row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Total Kasus Tercatat", "982.638",
                    "Januari 2020 - September 2024", "LAPD Dataset", "blue")
    with c2:
        metric_card("Kasus Valid (Setelah Cleaning)", "980.376",
                    "99,77% data retention", "Data Bersih", "green")
    with c3:
        metric_card("Tingkat Penangkapan", "9,01%",
                    "Dari total kasus tercatat", "Sangat Rendah", "red")
    with c4:
        metric_card("Kasus Melibatkan Senjata", "33,18%",
                    "Dari total kasus", "Perlu Perhatian", "orange")

    st.markdown("<br>", unsafe_allow_html=True)

    # Summary insight
    col_left, col_right = st.columns([3, 2])
    with col_left:
        section("Ringkasan Penelitian",
                "Kerangka analisis data mining multi-pilar pada data kejahatan Los Angeles")

        box(
            "Penelitian ini menganalisis <strong>982.638 kejadian kejahatan nyata</strong> di Los Angeles "
            "menggunakan 5 metode utama data mining yang diperkuat 3 analisis tambahan, "
            "seluruhnya divisualisasikan dalam dashboard interaktif sebagai Decision Support System (DSS).",
            "blue"
        )

        st.markdown("<br>", unsafe_allow_html=True)
        m1, m2 = st.columns(2)
        with m1:
            card("Clustering Spasiotemporal",
                 "Perbandingan UMAP+HDBSCAN vs PCA+K-Means untuk identifikasi zona hotspot kejahatan berdasarkan Silhouette Score dan Davies-Bouldin Index.")
            card("Association Rule Mining",
                 "FP-Growth algorithm untuk menemukan pola co-occurrence antar atribut kejahatan yang dapat diinterpretasikan secara operasional.")
            card("Klasifikasi Prediktif",
                 "LightGBM, Logistic Regression, dan Stacking Ensemble untuk prediksi probabilitas penangkapan pelaku (arrest) pada data imbalanced.")
        with m2:
            card("Analisis Spasial Statistik",
                 "Global Moran's I, peta LISA, dan Getis-Ord Gi* untuk membuktikan autokorelasi spasial dan identifikasi cluster hotspot/coldspot.")
            card("Time Series Forecasting",
                 "Prophet dan SARIMA untuk proyeksi volume kejahatan bulanan dengan perbandingan MAPE dan RMSE.")
            card("Analisis Tambahan",
                 "Causal Inference (DiD), Survival Analysis (Cox PH), dan Fairness Audit (Fairlearn) untuk insight yang lebih komprehensif.")

    with col_right:
        section("Statistik Kunci", "Temuan utama dari dataset LAPD")

        st.markdown("<br>", unsafe_allow_html=True)
        metric_card("Rata-rata Kasus Harian", "550+",
                    "Selama hampir 5 tahun berturut-turut", "Konsisten Tinggi", "red")
        st.markdown("<br>", unsafe_allow_html=True)
        metric_card("Wilayah Administratif", "21",
                    "Area Central mencatat kasus tertinggi", "Area Terpetakan", "blue")
        st.markdown("<br>", unsafe_allow_html=True)
        metric_card("Kasus Tidak Terselesaikan", ">90%",
                    "Lebih dari 9 dari 10 kasus tanpa penangkapan", "Darurat Penegakan", "red")
        st.markdown("<br>", unsafe_allow_html=True)
        metric_card("Target SDGs", "Nomor 16",
                    "Peace, Justice and Strong Institutions", "Relevansi Global", "purple")

        divider()
        box(
            "<strong>Relevansi SDGs:</strong> Kondisi ini bertentangan dengan SDG 16 yang menyerukan "
            "pengurangan signifikan kejahatan, penguatan lembaga penegak hukum, dan akses keadilan "
            "yang merata pada 2030.",
            "warn"
        )

    divider()

    # Pipeline overview
    section("Alur Penelitian", "Pipeline analisis data dari sumber hingga Decision Support System")
    st.markdown("<br>", unsafe_allow_html=True)

    cols = st.columns(5)
    steps = [
        ("1. Data Collection", "LAPD Open Data Portal\n982.638 kasus\nJan 2020 - Sep 2024"),
        ("2. Preprocessing", "Data cleaning\nFeature engineering\n980.376 baris valid"),
        ("3. EDA", "17 visualisasi\nStatistik deskriptif\nPattern discovery"),
        ("4. Modeling", "5 metode utama\n3 analisis tambahan\nMulti-pilar approach"),
        ("5. DSS Dashboard", "Visualisasi interaktif\nActionable insights\nDecision support"),
    ]
    for col, (title, body) in zip(cols, steps):
        with col:
            st.markdown(f"""
            <div class="card" style="text-align:center;min-height:110px;">
                <h4 style="font-size:13px;">{title}</h4>
                <p style="font-size:12px;white-space:pre-line;">{body}</p>
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  PAGE: EDA
# ══════════════════════════════════════════════
def page_eda():
    page_header(
        "Exploratory Data Analysis",
        "Pemahaman mendalam terhadap distribusi, tren, dan pola dalam data kejahatan LAPD"
    )

    # Load summary stats
    stats = load_json(p("eda", "eda_summary_stats.json"))
    if stats:
        keys = list(stats.keys())[:4]
        cols = st.columns(4)
        for i, (col, k) in enumerate(zip(cols, keys)):
            val = stats[k]
            with col:
                if isinstance(val, float):
                    metric_card(k.replace("_", " ").title(), f"{val:,.2f}")
                elif isinstance(val, int):
                    metric_card(k.replace("_", " ").title(), f"{val:,}")
                else:
                    metric_card(k.replace("_", " ").title(), str(val))
        st.markdown("<br>", unsafe_allow_html=True)

    tabs = st.tabs([
        "Distribusi & Tren", "Temporal", "Spasial & Demografis", "Senjata & Korelasi", "Data Quality"
    ])

    with tabs[0]:
        section("Distribusi Kategori Kejahatan & Tren Bulanan")
        c1, c2 = st.columns(2)
        with c1:
            show_image(p("eda", "01_crime_category_distribution.png"),
                       "Gambar 1. Distribusi Kategori Kejahatan")
        with c2:
            show_image(p("eda", "02_monthly_crime_trend.png"),
                       "Gambar 2. Tren Bulanan Volume Kejahatan")
        box(
            "Distribusi kejahatan menunjukkan konsentrasi pada kategori tertentu. "
            "Tren bulanan memperlihatkan fluktuasi signifikan, termasuk penurunan tajam saat lockdown COVID-19 "
            "pada awal 2020.",
            "blue"
        )

    with tabs[1]:
        section("Analisis Temporal: Tren, Jam, dan Hari")
        c1, c2 = st.columns(2)
        with c1:
            show_image(p("eda", "03_monthly_trend_by_category.png"),
                       "Gambar 3. Tren Bulanan per Kategori Kejahatan")
        with c2:
            show_image(p("eda", "04_hourly_distribution.png"),
                       "Gambar 4. Distribusi Kejahatan per Jam")
        st.markdown("<br>", unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        with c3:
            show_image(p("eda", "05_heatmap_day_hour.png"),
                       "Gambar 5. Heatmap Hari vs Jam Kejadian")
        with c4:
            show_image(p("eda", "14_time_of_day_analysis.png"),
                       "Gambar 6. Analisis Waktu dalam Sehari")
        box(
            "Kejahatan memiliki pola temporal yang kuat. Jam-jam tertentu (terutama malam dan dini hari) "
            "menunjukkan frekuensi lebih tinggi, dan pola ini konsisten lintas hari dalam seminggu.",
            "blue"
        )

    with tabs[2]:
        section("Distribusi Spasial dan Demografis")
        c1, c2 = st.columns(2)
        with c1:
            show_image(p("eda", "06_crime_by_area.png"),
                       "Gambar 7. Kejahatan per Wilayah (Area)")
        with c2:
            show_image(p("eda", "07_arrest_rate_by_area.png"),
                       "Gambar 8. Tingkat Penangkapan per Wilayah")
        st.markdown("<br>", unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        with c3:
            show_image(p("eda", "08_victim_age_by_category.png"),
                       "Gambar 9. Usia Korban per Kategori Kejahatan")
        with c4:
            show_image(p("eda", "09_victim_gender_distribution.png"),
                       "Gambar 10. Distribusi Gender Korban")
        st.markdown("<br>", unsafe_allow_html=True)
        c5, c6 = st.columns(2)
        with c5:
            show_image(p("eda", "16_yearly_comparison.png"),
                       "Gambar 11. Perbandingan Tahunan")
        with c6:
            show_image(p("eda", "17_victim_descent.png"),
                       "Gambar 12. Distribusi Latar Belakang Etnis Korban")
        box(
            "Area Central mencatat kasus tertinggi namun tingkat penangkapan bervariasi antar wilayah. "
            "Distribusi korban berdasarkan usia, gender, dan etnis memberikan gambaran profil demografis "
            "yang penting untuk kebijakan intervensi.",
            "blue"
        )

    with tabs[3]:
        section("Analisis Senjata dan Korelasi Fitur")
        c1, c2 = st.columns(2)
        with c1:
            show_image(p("eda", "10_weapon_analysis.png"),
                       "Gambar 13. Analisis Penggunaan Senjata")
        with c2:
            show_image(p("eda", "12_correlation_heatmap.png"),
                       "Gambar 14. Heatmap Korelasi Antar Fitur")
        st.markdown("<br>", unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        with c3:
            show_image(p("eda", "11_spatial_scatter.png"),
                       "Gambar 15. Scatter Plot Spasial Kejahatan")
        with c4:
            show_image(p("eda", "15_premis_analysis.png"),
                       "Gambar 16. Analisis Lokasi Kejadian (Premis)")
        box(
            "33,18% kasus melibatkan senjata. Korelasi antar fitur mengungkap hubungan penting "
            "antara jenis kejahatan, lokasi, dan penggunaan senjata yang relevan untuk model prediktif.",
            "warn"
        )

    with tabs[4]:
        section("Kualitas Data dan Keterlambatan Pelaporan")
        c1, c2 = st.columns(2)
        with c1:
            show_image(p("eda", "13_report_delay_analysis.png"),
                       "Gambar 17. Analisis Keterlambatan Pelaporan")
        with c2:
            mv = load_csv(p("eda", "missing_values_analysis.csv"))
            if mv is not None:
                section("Missing Values per Kolom")
                st.dataframe(mv, use_container_width=True)
            show_image(p("eda", "missing_values_barplot.png"),
                       "Gambar 18. Visualisasi Missing Values")
        box(
            "Analisis kualitas data mengidentifikasi pola missing values dan keterlambatan pelaporan "
            "yang perlu dipertimbangkan dalam interpretasi hasil. "
            "Proses cleaning menghasilkan 980.376 baris valid dari 982.638 total kasus.",
            "green"
        )


# ══════════════════════════════════════════════
#  PAGE: CLUSTERING
# ══════════════════════════════════════════════
def page_clustering():
    page_header(
        "Clustering Spasiotemporal",
        "Identifikasi zona konsentrasi kejahatan menggunakan perbandingan UMAP+HDBSCAN dan PCA+K-Means"
    )

    # Comparison metrics
    comp = load_csv(p("clustering", "clustering_comparison.csv"))
    if comp is not None:
        section("Perbandingan Metrik Evaluasi Clustering")
        st.dataframe(comp, use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)

    tabs = st.tabs(["Hasil Clustering", "Perbandingan Metode", "Peta Cluster Spasial", "Profil Cluster"])

    with tabs[0]:
        section("Visualisasi Hasil Clustering")
        c1, c2 = st.columns(2)
        with c1:
            show_image(p("clustering", "clustering_comparison_scatter.png"),
                       "Gambar 1. Scatter Plot Perbandingan Hasil Clustering")
        with c2:
            show_image(p("clustering", "elbow_method.png"),
                       "Gambar 2. Elbow Method untuk Penentuan K Optimal")
        box(
            "Eksperimen perbandingan dilakukan untuk menentukan metode terbaik berdasarkan "
            "<strong>Silhouette Score</strong> (semakin tinggi semakin baik) dan "
            "<strong>Davies-Bouldin Index</strong> (semakin rendah semakin baik).",
            "blue"
        )

    with tabs[1]:
        section("Perbandingan UMAP+HDBSCAN vs PCA+K-Means")
        c1, c2 = st.columns(2)
        with c1:
            card("UMAP + HDBSCAN",
                 "Metode non-linear yang mampu menangkap struktur kompleks dalam data berdimensi tinggi. "
                 "HDBSCAN secara otomatis menentukan jumlah cluster dan mengidentifikasi noise/outlier, "
                 "cocok untuk distribusi kejahatan yang tidak teratur secara spasial.")
            box("Keunggulan: Tidak perlu menentukan K di awal, mampu deteksi noise, "
                "cocok untuk distribusi non-uniform.", "green")
        with c2:
            card("PCA + K-Means",
                 "Pendekatan linear klasik yang efisien secara komputasi. PCA mereduksi dimensi "
                 "sebelum K-Means mengelompokkan data. Mudah diinterpretasikan dan direplikasi, "
                 "namun mengasumsikan cluster berbentuk spherical.")
            box("Keunggulan: Cepat, deterministik, mudah diinterpretasikan, "
                "dan stabil untuk deployment.", "blue")

    with tabs[2]:
        section("Peta Distribusi Cluster Spasial")
        show_image(p("clustering", "spatial_clusters_map.png"),
                   "Gambar 3. Peta Spasial Zona Cluster Kejahatan Los Angeles")
        box(
            "Peta cluster spasial mengungkap zona-zona konsentrasi kejahatan yang dapat langsung "
            "digunakan sebagai dasar alokasi patroli dan intervensi kepolisian. Area dengan kepadatan "
            "cluster tinggi menjadi prioritas operasional.",
            "warn"
        )

    with tabs[3]:
        section("Profil Tiap Cluster")
        profiles = load_csv(p("clustering", "cluster_profiles.csv"))
        if profiles is not None:
            st.dataframe(profiles, use_container_width=True)
            box(
                "Profil cluster memberikan karakterisasi tiap zona: jenis kejahatan dominan, "
                "waktu kejadian, tingkat penangkapan, dan distribusi demografis korban. "
                "Informasi ini esensial untuk strategi respons yang terdeferensiasi.",
                "blue"
            )
        else:
            st.info("File cluster_profiles.csv tidak ditemukan.")


# ══════════════════════════════════════════════
#  PAGE: ASSOCIATION
# ══════════════════════════════════════════════
def page_association():
    page_header(
        "Association Rule Mining",
        "Penemuan pola co-occurrence antar atribut kejahatan menggunakan algoritma FP-Growth"
    )

    tabs = st.tabs(["Visualisasi Rules", "Tabel Rules", "Frequent Itemsets", "Interpretasi"])

    with tabs[0]:
        section("Visualisasi Association Rules")
        show_image(p("association", "association_rules_viz.png"),
                   "Gambar 1. Network Visualisasi Association Rules Kejahatan")
        box(
            "Setiap titik merepresentasikan itemset (kombinasi atribut kejahatan), dan garis "
            "menunjukkan arah aturan asosiasi. Ketebalan garis merepresentasikan nilai "
            "<strong>lift</strong>  semakin tebal, semakin kuat hubungan kedua itemset tersebut.",
            "blue"
        )

    with tabs[1]:
        section("Tabel Association Rules")
        rules = load_csv(p("association", "association_rules.csv"))
        if rules is not None:
            # Display metrics
            c1, c2, c3 = st.columns(3)
            with c1:
                metric_card("Total Rules Ditemukan", str(len(rules)), "Strong rules yang valid", "FP-Growth", "blue")
            if "confidence" in rules.columns:
                with c2:
                    metric_card("Avg Confidence", f"{rules['confidence'].mean():.3f}",
                                "Rata-rata kepercayaan rule", "Metrik", "green")
            if "lift" in rules.columns:
                with c3:
                    metric_card("Max Lift", f"{rules['lift'].max():.3f}",
                                "Lift tertinggi yang ditemukan", "Kekuatan Asosiasi", "orange")
            st.markdown("<br>", unsafe_allow_html=True)
            col_order = ["antecedents", "consequents", "support", "confidence", "lift"]
            display_cols = [c for c in col_order if c in rules.columns]
            st.dataframe(
                rules[display_cols].sort_values("lift", ascending=False) if "lift" in rules.columns else rules[display_cols],
                use_container_width=True
            )
        else:
            st.info("File association_rules.csv tidak ditemukan.")

    with tabs[2]:
        section("Frequent Itemsets")
        fi = load_csv(p("association", "frequent_itemsets.csv"))
        if fi is not None:
            if "support" in fi.columns:
                metric_card("Total Frequent Itemsets", str(len(fi)),
                            f"Min support threshold terpenuhi", "FP-Growth Output", "blue")
                st.markdown("<br>", unsafe_allow_html=True)
                st.dataframe(fi.sort_values("support", ascending=False), use_container_width=True)
        else:
            st.info("File frequent_itemsets.csv tidak ditemukan.")

    with tabs[3]:
        section("Interpretasi Operasional")
        c1, c2 = st.columns(2)
        with c1:
            card("Definisi Metrik",
                 "<strong>Support:</strong> Seberapa sering kombinasi atribut muncul dalam dataset.<br>"
                 "<strong>Confidence:</strong> Probabilitas consequent muncul jika antecedent terjadi.<br>"
                 "<strong>Lift:</strong> Kekuatan asosiasi dibanding kemunculan acak (>1 = positif).")
            card("Kegunaan Operasional",
                 "Strong rules dengan lift tinggi mengindikasikan kombinasi atribut yang "
                 "sering muncul bersama  informasi ini dapat digunakan untuk "
                 "profiling kejahatan dan antisipasi jenis kejahatan berikutnya di lokasi tertentu.")
        with c2:
            box(
                "<strong>Contoh Interpretasi:</strong> Jika ditemukan rule dengan confidence tinggi antara "
                "jenis kejahatan tertentu, waktu malam, dan kawasan tertentu  maka kepolisian dapat "
                "meningkatkan patroli di area dan waktu tersebut secara proaktif.",
                "green"
            )
            box(
                "<strong>Algoritma FP-Growth</strong> dipilih karena lebih efisien dari Apriori "
                "pada dataset berskala besar, dengan kompleksitas O(n) tanpa kebutuhan "
                "generate candidate itemsets secara eksplisit.",
                "blue"
            )


# ══════════════════════════════════════════════
#  PAGE: CLASSIFICATION
# ══════════════════════════════════════════════
def page_classification():
    page_header(
        "Klasifikasi Prediktif",
        "Prediksi probabilitas penangkapan pelaku (arrest)  F1-Score & ROC-AUC pada data imbalanced"
    )

    tabs = st.tabs(["Perbandingan Model", "Confusion Matrix", "Feature Importance", "SHAP & ROC-PR", "Bootstrap CI"])

    with tabs[0]:
        section("Perbandingan Performa Model")
        comp = load_csv(p("classification", "classification_comparison.csv"))
        if comp is not None:
            # Key metrics summary
            if all(c in comp.columns for c in ["Model", "F1_Score", "ROC_AUC"]):
                best_f1 = comp.loc[comp["F1_Score"].idxmax()]
                best_auc = comp.loc[comp["ROC_AUC"].idxmax()]
                c1, c2, c3 = st.columns(3)
                with c1:
                    metric_card("Model Terbaik (F1)", str(best_f1.get("Model", "-")),
                                f"F1 = {best_f1['F1_Score']:.4f}", "Champion Model", "green")
                with c2:
                    metric_card("Model Terbaik (AUC)", str(best_auc.get("Model", "-")),
                                f"AUC = {best_auc['ROC_AUC']:.4f}", "Best AUC", "blue")
                with c3:
                    metric_card("Arrest Rate (Imbalanced)", "9,01%",
                                "Minority class proportion", "Class Imbalance", "red")
                st.markdown("<br>", unsafe_allow_html=True)
            st.dataframe(comp, use_container_width=True)
        else:
            st.info("File classification_comparison.csv tidak ditemukan.")

        box(
            "Ketiga model (LightGBM, Logistic Regression, Stacking Ensemble) dievaluasi pada data "
            "yang sangat imbalanced (arrest rate 9,01%). Fokus evaluasi pada <strong>F1-Score</strong> "
            "dan <strong>ROC-AUC</strong> karena akurasi tidak representatif pada kondisi class imbalance.",
            "warn"
        )

        report = load_csv(p("classification", "classification_report_stacking.csv"))
        if report is not None:
            st.markdown("<br>", unsafe_allow_html=True)
            section("Classification Report  Stacking Ensemble")
            st.dataframe(report, use_container_width=True)

    with tabs[1]:
        section("Confusion Matrix  Stacking Ensemble")
        show_image(p("classification", "confusion_matrix_stacking.png"),
                   "Gambar 1. Confusion Matrix Model Stacking Ensemble")
        box(
            "Confusion matrix menunjukkan distribusi prediksi benar dan salah untuk kelas arrest (1) "
            "dan non-arrest (0). Perhatikan trade-off antara False Negative "
            "(kasus arrest yang tidak terprediksi) dan False Positive.",
            "blue"
        )

    with tabs[2]:
        section("Feature Importance")
        c1, c2 = st.columns(2)
        with c1:
            show_image(p("classification", "feature_importance_lgbm.png"),
                       "Gambar 2. Feature Importance LightGBM (Built-in)")
        with c2:
            fi_df = load_csv(p("classification", "feature_importance.csv"))
            if fi_df is not None:
                st.dataframe(fi_df, use_container_width=True)
        box(
            "Fitur dengan importance tinggi merupakan prediktor kuat dalam menentukan kemungkinan "
            "penangkapan. Informasi ini membantu prioritasi pengumpulan data dan pemahaman "
            "faktor-faktor yang mempengaruhi keberhasilan investigasi.",
            "blue"
        )

    with tabs[3]:
        section("SHAP Summary Plot & ROC-PR Curves")
        c1, c2 = st.columns(2)
        with c1:
            show_image(p("classification", "shap_summary_plot.png"),
                       "Gambar 3. SHAP Summary Plot  Interpretasi Model LightGBM")
        with c2:
            show_image(p("classification", "roc_pr_curves.png"),
                       "Gambar 4. ROC Curve dan Precision-Recall Curve")
        box(
            "<strong>SHAP (SHapley Additive exPlanations)</strong> memberikan interpretabilitas "
            "pada level prediksi individual  menunjukkan fitur mana yang mendorong prediksi "
            "ke arah arrest atau non-arrest untuk setiap kasus.",
            "blue"
        )

    with tabs[4]:
        section("Bootstrap Confidence Intervals")
        bci = load_csv(p("classification", "bootstrap_confidence_intervals.csv"))
        if bci is not None:
            st.dataframe(bci, use_container_width=True)
            box(
                "Bootstrap confidence intervals memberikan estimasi ketidakpastian pada metrik "
                "performa model. Interval yang sempit mengindikasikan stabilitas model yang baik.",
                "green"
            )
        else:
            st.info("File bootstrap_confidence_intervals.csv tidak ditemukan.")


# ══════════════════════════════════════════════
#  PAGE: SPATIAL
# ══════════════════════════════════════════════
def page_spatial():
    page_header(
        "Analisis Spasial Statistik",
        "Autokorelasi spasial kejahatan menggunakan Global Moran's I, LISA, dan Getis-Ord Gi*"
    )

    # Load spatial results
    sar = load_csv(p("spatial", "spatial_analysis_results.csv"))
    gmi = load_csv(p("spatial", "global_morans_i.csv"))

    if gmi is not None:
        c1, c2, c3 = st.columns(3)
        with c1:
            val = gmi.iloc[0, 1] if len(gmi) > 0 and len(gmi.columns) > 1 else "-"
            metric_card("Global Moran's I", str(val) if not isinstance(val, float) else f"{val:.4f}",
                        "Indeks autokorelasi spasial global", "Spasial", "blue")
        with c2:
            metric_card("Metode Utama", "LISA",
                        "Local Indicators of Spatial Association", "Analisis Lokal", "green")
        with c3:
            metric_card("Metode Tambahan", "Getis-Ord Gi*",
                        "Identifikasi hotspot/coldspot signifikan", "Getis-Ord", "orange")
        st.markdown("<br>", unsafe_allow_html=True)

    tabs = st.tabs(["Global Moran's I", "Peta LISA", "Getis-Ord Gi*", "Tabel Hasil"])

    with tabs[0]:
        section("Global Moran's I  Autokorelasi Spasial Global")
        if gmi is not None:
            st.dataframe(gmi, use_container_width=True)
        box(
            "<strong>Global Moran's I</strong> mengukur apakah distribusi kejahatan di Los Angeles "
            "bersifat terkluster (clustered), tersebar (dispersed), atau acak (random). "
            "Nilai mendekati +1 menunjukkan kluster spasial yang kuat, sementara nilai mendekati -1 "
            "menunjukkan pola tersebar.",
            "blue"
        )
        c1, c2 = st.columns(2)
        with c1:
            card("Hipotesis",
                 "H0: Distribusi kejahatan bersifat acak (no spatial autocorrelation).<br>"
                 "H1: Terdapat pola kluster spasial yang signifikan secara statistik.")
        with c2:
            card("Implikasi",
                 "Jika terbukti terdapat autokorelasi spasial, maka intervensi kepolisian harus "
                 "mempertimbangkan efek spillover antar wilayah bertetangga, bukan hanya "
                 "fokus pada area isolasi.")

    with tabs[1]:
        section("Peta LISA  Local Indicators of Spatial Association")
        show_image(p("spatial", "lisa_map.png"),
                   "Gambar 1. Peta LISA  Identifikasi Cluster Lokal dan Outlier Spasial")
        box(
            "Peta LISA mengklasifikasikan tiap wilayah ke dalam 4 kategori: "
            "<strong>High-High</strong> (hotspot  area kejahatan tinggi dikelilingi area tinggi), "
            "<strong>Low-Low</strong> (coldspot), "
            "<strong>High-Low</strong> (outlier positif), dan "
            "<strong>Low-High</strong> (outlier negatif  area rendah dikelilingi area tinggi, "
            "kandidat intervensi komunitas).",
            "warn"
        )

    with tabs[2]:
        section("Getis-Ord Gi*  Hotspot dan Coldspot Analysis")
        show_image(p("spatial", "hotspot_map_gi_star.png"),
                   "Gambar 2. Peta Getis-Ord Gi*  Hotspot dan Coldspot Kejahatan")
        box(
            "<strong>Getis-Ord Gi*</strong> mengidentifikasi area dengan konsentrasi nilai tinggi "
            "(hotspot) atau rendah (coldspot) yang secara statistik signifikan. "
            "Berbeda dari LISA, Gi* memberikan nilai z-score lokal yang menunjukkan "
            "derajat kepentingan setiap lokasi.",
            "blue"
        )

    with tabs[3]:
        section("Tabel Hasil Analisis Spasial")
        if sar is not None:
            st.dataframe(sar, use_container_width=True)
        else:
            st.info("File spatial_analysis_results.csv tidak ditemukan.")
        box(
            "Hasil analisis spasial statistik memberikan landasan ilmiah untuk alokasi sumber daya "
            "berbasis bukti, menggantikan pendekatan heuristik konvensional dalam perencanaan patroli.",
            "green"
        )


# ══════════════════════════════════════════════
#  PAGE: FORECASTING
# ══════════════════════════════════════════════
def page_forecasting():
    page_header(
        "Forecasting Deret Waktu",
        "Proyeksi volume kejahatan bulanan menggunakan Prophet dan SARIMA"
    )

    comp = load_csv(p("forecasting", "forecasting_comparison.csv"))
    if comp is not None:
        cols = st.columns(min(len(comp), 4))
        for i, row in comp.iterrows():
            if i < 4:
                model_name = row.get("Model", row.iloc[0])
                with cols[i]:
                    mape_val = row.get("MAPE", None)
                    rmse_val = row.get("RMSE", None)
                    sub = ""
                    if mape_val is not None:
                        sub += f"MAPE: {mape_val:.4f}"
                    if rmse_val is not None:
                        sub += f" | RMSE: {rmse_val:.2f}"
                    metric_card(str(model_name), f"#{i+1}", sub if sub else None,
                                "Terbaik" if i == 0 else None, "green" if i == 0 else "blue")
        st.markdown("<br>", unsafe_allow_html=True)

    tabs = st.tabs(["Forecast Plot", "Komponen Prophet", "Perbandingan Model", "Interpretasi"])

    with tabs[0]:
        section("Visualisasi Hasil Forecasting")
        show_image(p("forecasting", "forecast_comparison_plot.png"),
                   "Gambar 1. Perbandingan Forecast Prophet vs SARIMA vs Data Aktual")
        box(
            "Plot menampilkan perbandingan prediksi Prophet dan SARIMA terhadap data aktual, "
            "disertai confidence interval. Area bayangan menunjukkan rentang ketidakpastian "
            "prediksi pada periode forecasting.",
            "blue"
        )

    with tabs[1]:
        section("Komponen Dekomposisi Prophet")
        show_image(p("forecasting", "prophet_components.png"),
                   "Gambar 2. Komponen Prophet: Trend, Seasonality, dan Holiday Effects")
        box(
            "Prophet secara otomatis mengdekomposisi deret waktu menjadi komponen trend, "
            "weekly seasonality, yearly seasonality, dan holiday effects. "
            "Dekomposisi ini memudahkan interpretasi pola kejahatan secara musiman.",
            "blue"
        )

    with tabs[2]:
        section("Perbandingan Metrik Evaluasi")
        if comp is not None:
            st.dataframe(comp, use_container_width=True)
        c1, c2 = st.columns(2)
        with c1:
            card("Prophet",
                 "Model time series additive yang dikembangkan Facebook/Meta. Unggul dalam menangani "
                 "data dengan multiple seasonality, missing values, dan outlier. "
                 "Tidak memerlukan stasionaritas data.")
        with c2:
            card("SARIMA",
                 "Seasonal AutoRegressive Integrated Moving Average  model klasik yang kuat "
                 "untuk data musiman. Memerlukan stasionaritas dan pemilihan parameter (p,d,q)(P,D,Q,s) "
                 "yang cermat melalui ACF/PACF analysis.")
        box(
            "Perbandingan berdasarkan <strong>MAPE</strong> (Mean Absolute Percentage Error) dan "
            "<strong>RMSE</strong> (Root Mean Square Error). Model dengan MAPE lebih rendah lebih "
            "akurat dalam persentase relatif, sementara RMSE sensitif terhadap outlier.",
            "blue"
        )

    with tabs[3]:
        section("Interpretasi untuk Pengambilan Keputusan")
        c1, c2 = st.columns(2)
        with c1:
            card("Perencanaan Operasional",
                 "Proyeksi volume kejahatan bulanan memungkinkan kepolisian mengalokasikan "
                 "personil secara proaktif sebelum periode puncak kejahatan terjadi.")
            card("Anggaran dan Sumber Daya",
                 "Pemerintah daerah dapat menggunakan proyeksi ini sebagai dasar perencanaan "
                 "anggaran keamanan publik untuk periode mendatang.")
        with c2:
            box(
                "<strong>Catatan Penting:</strong> Forecast adalah proyeksi berdasarkan pola historis. "
                "Kejadian luar biasa seperti pandemi, kebijakan baru, atau perubahan demografis "
                "dapat menyebabkan deviasi signifikan dari proyeksi.",
                "warn"
            )
            box(
                "Hasil forecasting sebaiknya dikombinasikan dengan domain knowledge kepolisian "
                "dan informasi kontekstual terkini untuk pengambilan keputusan yang optimal.",
                "blue"
            )


# ══════════════════════════════════════════════
#  PAGE: CAUSAL INFERENCE
# ══════════════════════════════════════════════
def page_causal():
    page_header(
        "Causal Inference  Difference-in-Differences",
        "Mengukur dampak kausal lockdown COVID-19 terhadap volume kejahatan"
    )

    tabs = st.tabs(["Parallel Trends", "Regression Summary", "Hasil DiD", "Metodologi"])

    with tabs[0]:
        section("Uji Parallel Trends Assumption")
        show_image(p("causal_inference", "did_parallel_trends.png"),
                   "Gambar 1. Visualisasi Parallel Trends  Validasi Asumsi DiD")
        box(
            "Asumsi <strong>parallel trends</strong> adalah syarat utama validitas DiD: "
            "kelompok treatment dan control harus menunjukkan tren yang sejajar sebelum "
            "intervensi (lockdown). Visualisasi ini memvalidasi asumsi tersebut.",
            "blue"
        )

    with tabs[1]:
        section("Regression Summary DiD")
        reg_path = p("causal_inference", "did_regression_summary.txt")
        if reg_path.exists():
            with open(reg_path) as f:
                content = f.read()
            st.code(content, language="text")
        else:
            st.info("File did_regression_summary.txt tidak ditemukan.")
        box(
            "Hasil regresi DiD menampilkan koefisien interaction term (Treated × Post) yang "
            "merupakan estimasi dampak kausal lockdown terhadap volume kejahatan, "
            "dikontrol terhadap efek fixed period dan group.",
            "blue"
        )

    with tabs[2]:
        section("Hasil Analisis DiD")
        did = load_csv(p("causal_inference", "did_results.csv"))
        if did is not None:
            st.dataframe(did, use_container_width=True)
        box(
            "Metode DiD memisahkan dampak kausal kebijakan dari confounding factors "
            "dengan membandingkan perubahan kelompok treatment (terdampak lockdown) "
            "terhadap kelompok control (baseline komparator) sebelum dan sesudah intervensi.",
            "green"
        )

    with tabs[3]:
        section("Metodologi Difference-in-Differences")
        c1, c2 = st.columns(2)
        with c1:
            card("Desain Penelitian",
                 "DiD membandingkan perubahan outcome (volume kejahatan) antara kelompok treatment "
                 "(terdampak lockdown COVID-19 Maret 2020) dan kelompok control, "
                 "sebelum (pre) dan sesudah (post) lockdown diberlakukan.")
            card("Formula DiD",
                 "ATT = (Y_treat,post - Y_treat,pre) - (Y_control,post - Y_control,pre). "
                 "Interaction term (β₃) pada model regresi merupakan estimator dampak kausal.")
        with c2:
            card("Keunggulan atas Korelasi",
             "DiD memungkinkan inferensi kausal (bukan sekadar korelatif) karena mengontrol "
             "confounding tidak teramati yang konstan dalam waktu (time-invariant confounders).")
            box(
                "<strong>Implikasi Kebijakan:</strong> Hasil DiD memberikan bukti kuantitatif "
                "bagaimana kebijakan pembatasan mobilitas berdampak terhadap pola kejahatan, "
                "informasi penting untuk desain kebijakan keamanan publik di masa depan.",
                "green"
            )


# ══════════════════════════════════════════════
#  PAGE: SURVIVAL
# ══════════════════════════════════════════════
def page_survival():
    page_header(
        "Survival Analysis",
        "Pemodelan waktu hingga penangkapan menggunakan Cox Proportional Hazards dan Kaplan-Meier"
    )

    tabs = st.tabs(["Kaplan-Meier Curves", "Cox Hazard Ratios", "Cox PH Summary", "Interpretasi"])

    with tabs[0]:
        section("Kurva Kaplan-Meier")
        show_image(p("survival_analysis", "kaplan_meier_curves.png"),
                   "Gambar 1. Kaplan-Meier Survival Curves  Estimasi Waktu Hingga Penangkapan")
        box(
            "Kurva Kaplan-Meier mengestimasi fungsi survival (probabilitas kasus belum berakhir "
            "dengan penangkapan) sepanjang waktu. Perbedaan antar kurva dapat diuji signifikansinya "
            "menggunakan log-rank test.",
            "blue"
        )

    with tabs[1]:
        section("Cox Hazard Ratios")
        show_image(p("survival_analysis", "cox_hazard_ratios.png"),
                   "Gambar 2. Forest Plot Cox Proportional Hazards Ratios")
        box(
            "<strong>Hazard Ratio (HR) > 1</strong>: Faktor meningkatkan peluang penangkapan.<br>"
            "<strong>HR < 1</strong>: Faktor menurunkan peluang penangkapan.<br>"
            "<strong>HR = 1</strong>: Tidak ada efek. Confidence interval yang tidak melintasi 1 "
            "mengindikasikan signifikansi statistik.",
            "warn"
        )

    with tabs[2]:
        section("Cox PH Model Summary")
        cox = load_csv(p("survival_analysis", "cox_ph_summary.csv"))
        if cox is not None:
            st.dataframe(cox, use_container_width=True)
        else:
            st.info("File cox_ph_summary.csv tidak ditemukan.")

    with tabs[3]:
        section("Interpretasi untuk Kepolisian")
        c1, c2 = st.columns(2)
        with c1:
            card("Apa yang Diukur?",
                 "Survival analysis mengukur 'waktu hingga kejadian'  dalam konteks ini, "
                 "berapa lama hingga sebuah kasus berakhir dengan penangkapan. "
                 "Kasus yang tidak berakhir dengan penangkapan diperlakukan sebagai 'censored'.")
            card("Faktor yang Mempengaruhi",
                 "Cox PH mengidentifikasi faktor-faktor (jenis kejahatan, lokasi, waktu, "
                 "penggunaan senjata) yang secara signifikan mempengaruhi kecepatan penangkapan, "
                 "dikontrol terhadap faktor lainnya secara simultan.")
        with c2:
            box(
                "<strong>Implikasi Operasional:</strong> Faktor dengan HR tinggi mengidentifikasi "
                "kondisi di mana penangkapan lebih cepat terjadi. Kepolisian dapat memprioritaskan "
                "sumber daya investigasi berdasarkan profil kasus.",
                "green"
            )
            box(
                "<strong>Prioritasi Investigasi:</strong> Kasus dengan karakteristik tertentu "
                "(identifiable dari hazard ratio) sebaiknya diprioritaskan agar penangkapan "
                "dapat dilakukan sebelum bukti hilang.",
                "blue"
            )


# ══════════════════════════════════════════════
#  PAGE: FAIRNESS AUDIT
# ══════════════════════════════════════════════
def page_fairness():
    page_header(
        "Fairness Audit",
        "Evaluasi potensi bias model prediktif terhadap kelompok demografis menggunakan Fairlearn"
    )

    tabs = st.tabs(["Visualisasi Fairness", "Fairness by Ethnicity", "Fairness by Gender", "Metodologi"])

    with tabs[0]:
        section("Fairness Audit Overview")
        show_image(p("fairness_audit", "fairness_audit_visualization.png"),
                   "Gambar 1. Visualisasi Komprehensif Fairness Audit  Fairlearn")
        box(
            "Fairness audit mengevaluasi apakah model prediktif menghasilkan performa yang setara "
            "antar kelompok demografis. Ketidaksetaraan performa mengindikasikan potensi bias "
            "algoritmis yang dapat berdampak diskriminatif.",
            "warn"
        )

    with tabs[1]:
        section("Fairness Berdasarkan Etnis")
        fe = load_csv(p("fairness_audit", "fairness_ethnicity.csv"))
        if fe is not None:
            st.dataframe(fe, use_container_width=True)
        box(
            "Disparitas performa antar kelompok etnis diukur menggunakan metrik fairness standar. "
            "Perbedaan yang signifikan mengindikasikan perlunya penyesuaian model atau "
            "kebijakan penggunaan model untuk mencegah bias sistemik.",
            "blue"
        )

    with tabs[2]:
        section("Fairness Berdasarkan Gender")
        fg = load_csv(p("fairness_audit", "fairness_gender.csv"))
        if fg is not None:
            st.dataframe(fg, use_container_width=True)
        box(
            "Evaluasi fairness berdasarkan gender memastikan bahwa prediksi arrest tidak "
            "secara sistematis bias terhadap kelompok gender tertentu, sesuai prinsip "
            "algorithmic fairness dalam responsible AI.",
            "blue"
        )

    with tabs[3]:
        section("Metodologi Fairness Audit")
        c1, c2 = st.columns(2)
        with c1:
            card("Metrik Fairness yang Digunakan",
                 "<strong>Demographic Parity:</strong> Probabilitas prediksi positif sama antar grup.<br>"
                 "<strong>Equalized Odds:</strong> TPR dan FPR sama antar grup.<br>"
                 "<strong>Equal Opportunity:</strong> TPR sama antar grup (fokus pada kelas positif).")
            card("Tool: Fairlearn",
                 "Fairlearn adalah library open-source Microsoft untuk menilai dan memitigasi "
                 "ketidakadilan dalam model machine learning, sesuai standar responsible AI.")
        with c2:
            card("Relevansi Etis",
                 "Sebagaimana ditegaskan Alikhademi et al. (2022), keadilan algoritmis adalah "
                 "syarat mutlak dalam sistem predictive policing yang bertanggung jawab. "
                 "Model yang bias dapat melanggengkan diskriminasi sistemik.")
            box(
                "<strong>Rekomendasi:</strong> Jika ditemukan disparitas signifikan, "
                "dapat dipertimbangkan teknik mitigasi seperti reweighting, threshold adjustment, "
                "atau adversarial debiasing sebelum model digunakan secara operasional.",
                "green"
            )


# ══════════════════════════════════════════════
#  PAGE: ABOUT
# ══════════════════════════════════════════════
def page_about():
    page_header(
        "Tentang Penelitian",
        "Informasi lengkap mengenai tim, metodologi, dataset, dan referensi"
    )

    c1, c2 = st.columns([2, 1])

    with c1:
        section("Deskripsi Penelitian")
        st.markdown("""
        <div class="card">
            <p>
            Penelitian ini menganalisis <strong>982.638 kasus kejahatan nyata</strong> yang tercatat
            oleh Los Angeles Police Department (LAPD) dari Januari 2020 hingga September 2024.
            Menggunakan kerangka analisis <em>multi-pilar</em> yang mengintegrasikan 5 metode utama
            <em>data mining</em> diperkuat 3 analisis tambahan, seluruh insight divisualisasikan
            dalam web dashboard interaktif sebagai Decision Support System (DSS).
            </p>
        </div>
        """, unsafe_allow_html=True)

        divider()
        section("Tim Peneliti")
        t1, t2 = st.columns(2)
        with t1:
            st.markdown("""
            <div class="card" style="text-align:center;">
                <h4 style="font-size:16px;">Nazril</h4>
                <p>S1 Sains Data<br>Universitas Negeri Surabaya (Unesa)<br>
                <span style="color:#2563EB;font-weight:600;">Tim Juara di Malang</span></p>
            </div>""", unsafe_allow_html=True)
        with t2:
            st.markdown("""
            <div class="card" style="text-align:center;">
                <h4 style="font-size:16px;">Habib</h4>
                <p>S1 Sains Data<br>Universitas Negeri Surabaya (Unesa)<br>
                <span style="color:#2563EB;font-weight:600;">Tim Juara di Malang</span></p>
            </div>""", unsafe_allow_html=True)

        divider()
        section("Metode Analisis")
        methods = [
            ("Clustering Spasiotemporal", "UMAP+HDBSCAN vs PCA+K-Means | Silhouette Score, Davies-Bouldin Index"),
            ("Association Rule Mining", "FP-Growth Algorithm | Support, Confidence, Lift"),
            ("Klasifikasi Prediktif", "LightGBM, Logistic Regression, Stacking Ensemble | F1-Score, ROC-AUC"),
            ("Analisis Spasial", "Global Moran's I, LISA, Getis-Ord Gi* | Autokorelasi Spasial"),
            ("Time Series Forecasting", "Prophet, SARIMA | MAPE, RMSE"),
            ("Causal Inference", "Difference-in-Differences (DiD) | Dampak Lockdown COVID-19"),
            ("Survival Analysis", "Kaplan-Meier, Cox Proportional Hazards | Waktu Hingga Penangkapan"),
            ("Fairness Audit", "Fairlearn | Demographic Parity, Equalized Odds"),
        ]
        for name, detail in methods:
            st.markdown(f"""
            <div class="card" style="padding:12px 16px;margin-bottom:8px;">
                <h4 style="margin-bottom:3px;">{name}</h4>
                <p style="font-size:12px;">{detail}</p>
            </div>""", unsafe_allow_html=True)

    with c2:
        section("Informasi Lomba")
        st.markdown("""
        <div class="card" style="text-align:center;padding:24px;">
            <div style="font-size:20px;font-weight:800;color:#1a3558;margin-bottom:4px;">EXPLORE AH</div>
            <div style="font-size:12px;color:#64748B;margin-bottom:16px;">Kompetisi Data Mining</div>
            <div style="height:1px;background:#EEF2F7;margin:12px 0;"></div>
            <div style="font-size:13px;color:#475569;line-height:1.8;">
                <strong>Tim:</strong> Juara di Malang<br>
                <strong>Anggota:</strong> Nazril &amp; Habib<br>
                <strong>Program Studi:</strong> S1 Sains Data<br>
                <strong>Institusi:</strong> Unesa<br>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        section("Dataset")
        st.markdown("""
        <div class="card">
            <h4>LAPD Crime Data 2020-2024</h4>
            <p>
                <strong>Sumber:</strong> Los Angeles Open Data Portal<br>
                <strong>Total Kasus:</strong> 982.638 kejadian<br>
                <strong>Setelah Cleaning:</strong> 980.376 baris valid<br>
                <strong>Periode:</strong> Januari 2020 - September 2024<br>
                <strong>Wilayah:</strong> 21 area administratif LAPD
            </p>
        </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        section("Relevansi SDGs")
        st.markdown("""
        <div class="card">
            <h4>SDG 16  Peace, Justice and Strong Institutions</h4>
            <p>
                Penelitian ini berkontribusi pada SDG 16 dengan menyediakan
                landasan berbasis data untuk kebijakan keamanan publik yang lebih
                cerdas, berkeadilan, dan terukur dampaknya.
            </p>
        </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        section("Struktur Folder Hasil")
        box(
            "<strong>EXPLORE_AH_DataMining_Results/</strong><br>"
            "association/ &nbsp;|&nbsp; causal_inference/<br>"
            "classification/ &nbsp;|&nbsp; clustering/<br>"
            "eda/ &nbsp;|&nbsp; fairness_audit/<br>"
            "forecasting/ &nbsp;|&nbsp; spatial/<br>"
            "survival_analysis/",
            "blue"
        )


# ─────────────────────────────────────────────
#  ROUTER
# ─────────────────────────────────────────────
router = {
    "Overview":                  page_overview,
    "Exploratory Data Analysis": page_eda,
    "Clustering Spasiotemporal": page_clustering,
    "Association Rule Mining":   page_association,
    "Klasifikasi Prediktif":     page_classification,
    "Analisis Spasial":          page_spatial,
    "Forecasting":               page_forecasting,
    "Causal Inference":          page_causal,
    "Survival Analysis":         page_survival,
    "Fairness Audit":            page_fairness,
    "Tentang Penelitian":        page_about,
}

router[selected]()
