import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from filters import apply_filters, load_data
from charts import (
    plot_pie_chart, plot_histogram, plot_line_chart, plot_bar_chart,
    plot_scatter, plot_box_plot, plot_heatmap, plot_area_chart,
    plot_count_plot, plot_violin_plot
)

st.set_page_config(
    page_title="Netflix Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0d0d0d; color: #e5e5e5; }
    .stApp { background-color: #141414; }
    section[data-testid="stSidebar"] { background-color: #1a1a1a; }
    .metric-card {
        background: #1f1f1f;
        border: 1px solid #E50914;
        border-radius: 10px;
        padding: 16px 20px;
        text-align: center;
    }
    .metric-val { font-size: 30px; font-weight: 700; color: #E50914; }
    .metric-lbl { font-size: 13px; color: #aaa; margin-top: 4px; }
    h1, h2, h3, h4 { color: #ffffff !important; }
    .stSelectbox label, .stMultiSelect label,
    .stSlider label, .stTextInput label { color: #cccccc !important; }
    div[data-testid="stMetricValue"] { color: #E50914; }
    .chart-title { color: #ffffff; font-size: 16px; font-weight: 600; margin-bottom: 6px; }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style='background: linear-gradient(90deg,#E50914,#831010); padding:20px 28px; border-radius:12px; margin-bottom:18px;'>
    <h1 style='color:white;margin:0;font-size:2rem;'>🎬 Netflix Content Dashboard</h1>
    <p style='color:#ffcccc;margin:6px 0 0;font-size:14px;'>
        Exploratory Data Analysis — Movies & TV Shows (EDA Course Project)
    </p>
</div>
""", unsafe_allow_html=True)

# ── Load Data ────────────────────────────────────────────────────────────────
df_raw = load_data()

# ── Sidebar Filters ──────────────────────────────────────────────────────────
st.sidebar.markdown("## 🎛️ Dashboard Filters")
st.sidebar.markdown("---")

# 1. Type filter (category)
type_options = ["All"] + sorted(df_raw["type"].dropna().unique().tolist())
selected_type = st.sidebar.selectbox("📺 Content Type", type_options)

# 2. Multi-select: Rating
all_ratings = sorted(df_raw["rating"].dropna().unique().tolist())
selected_ratings = st.sidebar.multiselect("🔞 Age Rating", all_ratings, default=all_ratings)

# 3. Multi-select: Country
top_countries = df_raw["country"].value_counts().head(20).index.tolist()
selected_countries = st.sidebar.multiselect("🌍 Country (Top 20)", top_countries, default=top_countries)

# 4. Year range slider
min_year = int(df_raw["release_year"].min())
max_year = int(df_raw["release_year"].max())
year_range = st.sidebar.slider("📅 Release Year Range", min_year, max_year, (2010, max_year))

# 5. Duration slider (movies only — in minutes)
min_dur, max_dur = 1, 300
duration_range = st.sidebar.slider("⏱️ Movie Duration (min)", min_dur, max_dur, (min_dur, max_dur))

# 6. Text search
search_text = st.sidebar.text_input("🔍 Search by Title / Director / Cast", "")

# 7. Reset
if st.sidebar.button("🔄 Reset All Filters"):
    st.rerun()

# ── Apply Filters ────────────────────────────────────────────────────────────
df = apply_filters(
    df_raw, selected_type, selected_ratings,
    selected_countries, year_range, duration_range, search_text
)

# ── KPI Cards ────────────────────────────────────────────────────────────────
total      = len(df)
n_movies   = len(df[df["type"] == "Movie"])
n_tv       = len(df[df["type"] == "TV Show"])
avg_year   = int(df["release_year"].mean()) if total > 0 else "—"
n_countries = df["country"].nunique()

c1, c2, c3, c4, c5 = st.columns(5)
for col, val, lbl in zip(
    [c1, c2, c3, c4, c5],
    [f"{total:,}", f"{n_movies:,}", f"{n_tv:,}", str(avg_year), str(n_countries)],
    ["Total Titles", "Movies", "TV Shows", "Avg Release Year", "Countries"]
):
    col.markdown(f"""
    <div class='metric-card'>
        <div class='metric-val'>{val}</div>
        <div class='metric-lbl'>{lbl}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Row 1: Pie + Bar ─────────────────────────────────────────────────────────
st.markdown("### 📊 Content Distribution")
col1, col2 = st.columns(2)

with col1:
    st.markdown("<p class='chart-title'>Movies vs TV Shows</p>", unsafe_allow_html=True)
    fig = plot_pie_chart(df)
    st.pyplot(fig, use_container_width=True)
    plt.close()

with col2:
    st.markdown("<p class='chart-title'>Top 10 Countries by Content</p>", unsafe_allow_html=True)
    fig = plot_bar_chart(df)
    st.pyplot(fig, use_container_width=True)
    plt.close()

# ── Row 2: Line + Area ───────────────────────────────────────────────────────
st.markdown("### 📈 Trends Over Time")
col3, col4 = st.columns(2)

with col3:
    st.markdown("<p class='chart-title'>Content Added per Year</p>", unsafe_allow_html=True)
    fig = plot_line_chart(df)
    st.pyplot(fig, use_container_width=True)
    plt.close()

with col4:
    st.markdown("<p class='chart-title'>Cumulative Content Growth</p>", unsafe_allow_html=True)
    fig = plot_area_chart(df)
    st.pyplot(fig, use_container_width=True)
    plt.close()

# ── Row 3: Histogram + Count Plot ────────────────────────────────────────────
st.markdown("### 📉 Distributions")
col5, col6 = st.columns(2)

with col5:
    st.markdown("<p class='chart-title'>Movie Duration Distribution</p>", unsafe_allow_html=True)
    fig = plot_histogram(df)
    st.pyplot(fig, use_container_width=True)
    plt.close()

with col6:
    st.markdown("<p class='chart-title'>Content Count by Rating</p>", unsafe_allow_html=True)
    fig = plot_count_plot(df)
    st.pyplot(fig, use_container_width=True)
    plt.close()

# ── Row 4: Scatter + Box ─────────────────────────────────────────────────────
st.markdown("### 🔬 Statistical Analysis")
col7, col8 = st.columns(2)

with col7:
    st.markdown("<p class='chart-title'>Release Year vs Duration (Movies)</p>", unsafe_allow_html=True)
    fig = plot_scatter(df)
    st.pyplot(fig, use_container_width=True)
    plt.close()

with col8:
    st.markdown("<p class='chart-title'>Movie Duration by Rating</p>", unsafe_allow_html=True)
    fig = plot_box_plot(df)
    st.pyplot(fig, use_container_width=True)
    plt.close()

# ── Row 5: Heatmap + Violin ──────────────────────────────────────────────────
st.markdown("### 🌡️ Correlations & Density")
col9, col10 = st.columns(2)

with col9:
    st.markdown("<p class='chart-title'>Feature Correlation Heatmap</p>", unsafe_allow_html=True)
    fig = plot_heatmap(df)
    st.pyplot(fig, use_container_width=True)
    plt.close()

with col10:
    st.markdown("<p class='chart-title'>Duration Distribution by Content Type</p>", unsafe_allow_html=True)
    fig = plot_violin_plot(df)
    st.pyplot(fig, use_container_width=True)
    plt.close()

# ── Data Table ───────────────────────────────────────────────────────────────
st.markdown("### 📋 Filtered Data Table")
st.markdown(f"Showing **{len(df):,}** records after applying filters.")
display_cols = ["title", "type", "country", "release_year", "rating", "duration", "listed_in"]
st.dataframe(
    df[display_cols].reset_index(drop=True),
    use_container_width=True,
    height=320
)

st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#555;font-size:12px;'>"
    "EDA Dashboard | Netflix Dataset | Built with Streamlit, Pandas, Matplotlib & Seaborn"
    "</p>",
    unsafe_allow_html=True
)
