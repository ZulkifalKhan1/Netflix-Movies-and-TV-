import pandas as pd
import numpy as np
import streamlit as st


@st.cache_data
def load_data():
    """Load and clean the Netflix dataset."""
    try:
        df = pd.read_csv("data/netflix_titles.csv")
    except FileNotFoundError:
        # Fallback: download directly via URL (no login required)
        url = "https://raw.githubusercontent.com/dsrscientist/dataset1/master/netflix_titles.csv"
        try:
            df = pd.read_csv(url)
        except Exception:
            # Generate realistic sample data if network is unavailable
            df = _generate_sample_data()

    df = _clean_data(df)
    return df


def _clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and preprocess the Netflix DataFrame."""
    df = df.copy()

    # Standardise column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Drop full duplicates
    df.drop_duplicates(subset=["title", "type", "release_year"], keep="first", inplace=True)

    # Fill missing values
    df["director"].fillna("Unknown", inplace=True)
    df["cast"].fillna("Unknown", inplace=True)
    df["country"].fillna("Unknown", inplace=True)
    df["rating"].fillna("Not Rated", inplace=True)
    df["duration"].fillna("0 min", inplace=True)
    df.dropna(subset=["title", "type", "release_year"], inplace=True)

    # Extract duration in minutes for Movies
    df["duration_clean"] = df.apply(_parse_duration, axis=1)

    # Extract primary country (first listed)
    df["country"] = df["country"].str.split(",").str[0].str.strip()

    # date_added → year_added
    df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
    df["year_added"] = df["date_added"].dt.year

    # release_year as int
    df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce").fillna(0).astype(int)

    # Create numeric columns for correlation heatmap
    df["is_movie"] = (df["type"] == "Movie").astype(int)
    df["decade"] = (df["release_year"] // 10) * 10

    return df


def _parse_duration(row):
    """Return numeric duration. Movies → minutes; TV Shows → seasons × 10."""
    try:
        val = str(row["duration"])
        if "min" in val.lower():
            return int(val.lower().replace("min", "").strip())
        elif "season" in val.lower():
            n = int(val.lower().replace("seasons", "").replace("season", "").strip())
            return n * 10  # encode seasons as proxy minutes
        return 0
    except Exception:
        return 0


def _generate_sample_data():
    """Return a small realistic sample when the CSV is unavailable."""
    import random, datetime
    types   = ["Movie", "TV Show"]
    ratings = ["TV-MA", "TV-14", "TV-PG", "PG-13", "R", "PG", "TV-Y7", "TV-G", "G", "NR"]
    countries = [
        "United States", "India", "United Kingdom", "Canada", "France",
        "Germany", "Japan", "South Korea", "Australia", "Spain"
    ]
    genres = [
        "Dramas, International Movies", "Comedies, Romantic Movies",
        "Action & Adventure, Thrillers", "Documentaries",
        "Children & Family Movies", "Horror Movies",
        "Stand-Up Comedy", "TV Dramas, International TV Shows",
        "Reality TV", "Crime TV Shows, Docuseries"
    ]
    n = 3000
    random.seed(42)
    rows = []
    for i in range(n):
        t = random.choice(types)
        year = random.randint(1995, 2021)
        dur  = f"{random.randint(70,180)} min" if t == "Movie" else f"{random.randint(1,5)} Season{'s' if random.randint(1,5)>1 else ''}"
        rows.append({
            "show_id"     : f"s{i+1}",
            "type"        : t,
            "title"       : f"Title {i+1}",
            "director"    : f"Director {random.randint(1,200)}",
            "cast"        : f"Actor {random.randint(1,500)}, Actor {random.randint(1,500)}",
            "country"     : random.choice(countries),
            "date_added"  : f"{random.choice(['January','March','June','September','November'])} {random.randint(1,28)}, {random.randint(2014,2021)}",
            "release_year": year,
            "rating"      : random.choice(ratings),
            "duration"    : dur,
            "listed_in"   : random.choice(genres),
            "description" : "Sample description."
        })
    return pd.DataFrame(rows)


def apply_filters(
    df: pd.DataFrame,
    selected_type: str,
    selected_ratings: list,
    selected_countries: list,
    year_range: tuple,
    duration_range: tuple,
    search_text: str
) -> pd.DataFrame:
    """Apply all sidebar filters and return the filtered DataFrame."""
    filtered = df.copy()

    # 1. Content type
    if selected_type != "All":
        filtered = filtered[filtered["type"] == selected_type]

    # 2. Age rating
    if selected_ratings:
        filtered = filtered[filtered["rating"].isin(selected_ratings)]

    # 3. Country
    if selected_countries:
        filtered = filtered[filtered["country"].isin(selected_countries)]

    # 4. Release year range
    filtered = filtered[
        (filtered["release_year"] >= year_range[0]) &
        (filtered["release_year"] <= year_range[1])
    ]

    # 5. Duration range (movies only; TV shows pass through)
    movies_mask  = filtered["type"] == "Movie"
    dur_mask     = (filtered["duration_clean"] >= duration_range[0]) & \
                   (filtered["duration_clean"] <= duration_range[1])
    filtered = filtered[~movies_mask | (movies_mask & dur_mask)]

    # 6. Text search (title, director, cast)
    if search_text.strip():
        q = search_text.strip().lower()
        text_mask = (
            filtered["title"].str.lower().str.contains(q, na=False) |
            filtered["director"].str.lower().str.contains(q, na=False) |
            filtered["cast"].str.lower().str.contains(q, na=False)
        )
        filtered = filtered[text_mask]

    return filtered.reset_index(drop=True)
