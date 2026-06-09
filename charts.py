"""
charts.py – All 10 required chart functions for the Netflix Dashboard.
Each function accepts the filtered DataFrame and returns a Matplotlib Figure.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# ── Theme ────────────────────────────────────────────────────────────────────
NETFLIX_RED   = "#E50914"
NETFLIX_DARK  = "#141414"
NETFLIX_GRAY  = "#333333"
ACCENT_COLORS = ["#E50914", "#831010", "#FF6B6B", "#FFB3B3",
                 "#C0392B", "#922B21", "#7B241C", "#641E16"]
PALETTE_10    = ["#E50914","#FF6B35","#F7C59F","#EFEFD0","#004E89",
                 "#1A936F","#88D498","#C6DABF","#FFC857","#2E4057"]

def _style_ax(ax, title="", xlabel="", ylabel=""):
    """Apply dark Netflix styling to a Matplotlib Axes."""
    ax.set_facecolor(NETFLIX_DARK)
    ax.figure.patch.set_facecolor(NETFLIX_DARK)
    ax.tick_params(colors="#cccccc", labelsize=9)
    ax.xaxis.label.set_color("#cccccc")
    ax.yaxis.label.set_color("#cccccc")
    for spine in ax.spines.values():
        spine.set_edgecolor(NETFLIX_GRAY)
    if title:
        ax.set_title(title, color="white", fontsize=12, fontweight="bold", pad=10)
    if xlabel:
        ax.set_xlabel(xlabel, color="#aaaaaa", fontsize=9)
    if ylabel:
        ax.set_ylabel(ylabel, color="#aaaaaa", fontsize=9)
    ax.grid(axis="y", color=NETFLIX_GRAY, linewidth=0.5, alpha=0.5)


# ── 1. Pie Chart ──────────────────────────────────────────────────────────────
def plot_pie_chart(df: pd.DataFrame) -> plt.Figure:
    counts = df["type"].value_counts()
    if counts.empty:
        return _empty_fig("No data for pie chart")
    fig, ax = plt.subplots(figsize=(5, 4), facecolor=NETFLIX_DARK)
    wedges, texts, autotexts = ax.pie(
        counts,
        labels=counts.index,
        autopct="%1.1f%%",
        colors=[NETFLIX_RED, "#444444"],
        startangle=90,
        wedgeprops={"edgecolor": "#222", "linewidth": 1.5},
        textprops={"color": "white", "fontsize": 11}
    )
    for at in autotexts:
        at.set_fontsize(10)
        at.set_color("white")
    ax.set_title("Movies vs TV Shows", color="white", fontsize=12, fontweight="bold")
    fig.patch.set_facecolor(NETFLIX_DARK)
    return fig


# ── 2. Histogram ──────────────────────────────────────────────────────────────
def plot_histogram(df: pd.DataFrame) -> plt.Figure:
    movies = df[df["type"] == "Movie"]["duration_clean"]
    movies = movies[(movies > 0) & (movies < 300)]
    fig, ax = plt.subplots(figsize=(6, 4), facecolor=NETFLIX_DARK)
    if movies.empty:
        return _empty_fig("No movie duration data")
    ax.hist(movies, bins=30, color=NETFLIX_RED, edgecolor="#222", alpha=0.85)
    ax.axvline(movies.mean(), color="#FFB3B3", linestyle="--", linewidth=1.5,
               label=f"Mean: {movies.mean():.0f} min")
    ax.axvline(movies.median(), color="#FF6B35", linestyle=":", linewidth=1.5,
               label=f"Median: {movies.median():.0f} min")
    legend = ax.legend(fontsize=8, facecolor=NETFLIX_GRAY, labelcolor="white")
    _style_ax(ax, xlabel="Duration (minutes)", ylabel="Number of Movies")
    return fig


# ── 3. Line Chart ─────────────────────────────────────────────────────────────
def plot_line_chart(df: pd.DataFrame) -> plt.Figure:
    yearly = df.groupby(["release_year", "type"]).size().unstack(fill_value=0).reset_index()
    yearly = yearly[yearly["release_year"] >= 1990]
    fig, ax = plt.subplots(figsize=(6, 4), facecolor=NETFLIX_DARK)
    if yearly.empty:
        return _empty_fig("No yearly data")
    for col, color in zip([c for c in yearly.columns if c != "release_year"],
                          [NETFLIX_RED, "#4FC3F7"]):
        ax.plot(yearly["release_year"], yearly[col], color=color,
                linewidth=2, label=col, marker="o", markersize=3)
    _style_ax(ax, xlabel="Release Year", ylabel="Number of Titles")
    ax.legend(facecolor=NETFLIX_GRAY, labelcolor="white", fontsize=8)
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    return fig


# ── 4. Bar Chart ──────────────────────────────────────────────────────────────
def plot_bar_chart(df: pd.DataFrame) -> plt.Figure:
    top = df["country"].value_counts().head(10)
    if top.empty:
        return _empty_fig("No country data")
    fig, ax = plt.subplots(figsize=(6, 4), facecolor=NETFLIX_DARK)
    bars = ax.barh(top.index[::-1], top.values[::-1],
                   color=ACCENT_COLORS[:len(top)], edgecolor="none")
    for bar, val in zip(bars, top.values[::-1]):
        ax.text(val + 5, bar.get_y() + bar.get_height()/2,
                str(val), va="center", color="#cccccc", fontsize=8)
    _style_ax(ax, xlabel="Number of Titles", ylabel="")
    ax.tick_params(axis="y", labelsize=8)
    ax.grid(axis="x", color=NETFLIX_GRAY, linewidth=0.5, alpha=0.5)
    ax.grid(axis="y", visible=False)
    return fig


# ── 5. Scatter Plot ───────────────────────────────────────────────────────────
def plot_scatter(df: pd.DataFrame) -> plt.Figure:
    movies = df[(df["type"] == "Movie") & (df["duration_clean"] > 0)]
    if movies.empty:
        return _empty_fig("No scatter data")
    fig, ax = plt.subplots(figsize=(6, 4), facecolor=NETFLIX_DARK)
    sc = ax.scatter(
        movies["release_year"], movies["duration_clean"],
        c=movies["duration_clean"], cmap="Reds", alpha=0.5,
        s=18, edgecolors="none"
    )
    cbar = fig.colorbar(sc, ax=ax)
    cbar.ax.tick_params(colors="#cccccc", labelsize=8)
    cbar.set_label("Duration (min)", color="#aaaaaa", fontsize=8)
    _style_ax(ax, xlabel="Release Year", ylabel="Duration (min)")
    return fig


# ── 6. Box Plot ───────────────────────────────────────────────────────────────
def plot_box_plot(df: pd.DataFrame) -> plt.Figure:
    movies = df[(df["type"] == "Movie") & (df["duration_clean"] > 0) & (df["duration_clean"] < 300)]
    top_ratings = movies["rating"].value_counts().head(6).index
    sub = movies[movies["rating"].isin(top_ratings)]
    if sub.empty:
        return _empty_fig("No box plot data")
    fig, ax = plt.subplots(figsize=(6, 4), facecolor=NETFLIX_DARK)
    groups = [sub[sub["rating"] == r]["duration_clean"].values for r in top_ratings]
    bp = ax.boxplot(groups, patch_artist=True, labels=top_ratings,
                    medianprops={"color": "white", "linewidth": 2},
                    whiskerprops={"color": "#aaa"},
                    capprops={"color": "#aaa"},
                    flierprops={"marker": "o", "markersize": 3,
                                "markerfacecolor": NETFLIX_RED, "alpha": 0.4})
    for patch, color in zip(bp["boxes"], ACCENT_COLORS):
        patch.set_facecolor(color)
        patch.set_alpha(0.75)
    _style_ax(ax, xlabel="Rating", ylabel="Duration (min)")
    ax.tick_params(axis="x", labelsize=8, rotation=20)
    return fig


# ── 7. Heatmap ─────────────────────────────────────────────────────────────────
def plot_heatmap(df: pd.DataFrame) -> plt.Figure:
    num_cols = ["release_year", "duration_clean", "is_movie", "decade"]
    available = [c for c in num_cols if c in df.columns]
    sub = df[available].dropna()
    if sub.empty or len(available) < 2:
        return _empty_fig("Not enough numeric data for heatmap")
    corr = sub.corr()
    rename = {
        "release_year" : "Release Year",
        "duration_clean": "Duration",
        "is_movie"      : "Is Movie",
        "decade"        : "Decade"
    }
    corr.rename(index=rename, columns=rename, inplace=True)
    fig, ax = plt.subplots(figsize=(5, 4), facecolor=NETFLIX_DARK)
    sns.heatmap(
        corr, annot=True, fmt=".2f", cmap="Reds",
        ax=ax, linewidths=0.5, linecolor="#222",
        cbar_kws={"shrink": 0.8},
        annot_kws={"size": 9, "color": "white"}
    )
    ax.set_facecolor(NETFLIX_DARK)
    ax.tick_params(colors="#cccccc", labelsize=8)
    ax.figure.patch.set_facecolor(NETFLIX_DARK)
    plt.setp(ax.get_xticklabels(), rotation=25, ha="right")
    plt.setp(ax.get_yticklabels(), rotation=0)
    ax.collections[0].colorbar.ax.tick_params(colors="#cccccc", labelsize=7)
    return fig


# ── 8. Area Chart ─────────────────────────────────────────────────────────────
def plot_area_chart(df: pd.DataFrame) -> plt.Figure:
    yearly = df.groupby(["release_year", "type"]).size().unstack(fill_value=0).reset_index()
    yearly = yearly[yearly["release_year"] >= 1990]
    for col in ["Movie", "TV Show"]:
        if col not in yearly.columns:
            yearly[col] = 0
    yearly["Movie_cum"]  = yearly["Movie"].cumsum()
    yearly["TV_cum"]     = yearly["TV Show"].cumsum()
    fig, ax = plt.subplots(figsize=(6, 4), facecolor=NETFLIX_DARK)
    ax.fill_between(yearly["release_year"], yearly["Movie_cum"],
                    alpha=0.6, color=NETFLIX_RED, label="Movie")
    ax.fill_between(yearly["release_year"], yearly["TV_cum"],
                    alpha=0.4, color="#4FC3F7", label="TV Show")
    _style_ax(ax, xlabel="Release Year", ylabel="Cumulative Titles")
    ax.legend(facecolor=NETFLIX_GRAY, labelcolor="white", fontsize=8)
    return fig


# ── 9. Count Plot ─────────────────────────────────────────────────────────────
def plot_count_plot(df: pd.DataFrame) -> plt.Figure:
    top_ratings = df["rating"].value_counts().head(8)
    if top_ratings.empty:
        return _empty_fig("No rating data")
    fig, ax = plt.subplots(figsize=(6, 4), facecolor=NETFLIX_DARK)
    bars = ax.bar(top_ratings.index, top_ratings.values,
                  color=PALETTE_10[:len(top_ratings)], edgecolor="none")
    for bar, val in zip(bars, top_ratings.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                str(val), ha="center", color="#cccccc", fontsize=8)
    _style_ax(ax, xlabel="Rating", ylabel="Count")
    ax.tick_params(axis="x", rotation=30, labelsize=8)
    return fig


# ── 10. Violin Plot ───────────────────────────────────────────────────────────
def plot_violin_plot(df: pd.DataFrame) -> plt.Figure:
    data = df[(df["duration_clean"] > 0) & (df["duration_clean"] < 300)]
    if data.empty:
        return _empty_fig("No violin data")
    fig, ax = plt.subplots(figsize=(6, 4), facecolor=NETFLIX_DARK)
    types = data["type"].unique()
    groups = [data[data["type"] == t]["duration_clean"].values for t in types]
    parts = ax.violinplot(groups, positions=range(len(types)),
                          showmedians=True, showextrema=True)
    for i, (pc, color) in enumerate(zip(parts["bodies"],
                                        [NETFLIX_RED, "#4FC3F7"])):
        pc.set_facecolor(color)
        pc.set_alpha(0.6)
    parts["cmedians"].set_color("white")
    parts["cmins"].set_color("#aaa")
    parts["cmaxes"].set_color("#aaa")
    parts["cbars"].set_color("#aaa")
    ax.set_xticks(range(len(types)))
    ax.set_xticklabels(types, color="#cccccc", fontsize=9)
    _style_ax(ax, xlabel="Content Type", ylabel="Duration (min)")
    return fig


# ── Helper ────────────────────────────────────────────────────────────────────
def _empty_fig(msg: str) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(5, 3), facecolor=NETFLIX_DARK)
    ax.set_facecolor(NETFLIX_DARK)
    ax.text(0.5, 0.5, msg, transform=ax.transAxes,
            ha="center", va="center", color="#aaaaaa", fontsize=11)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    return fig
