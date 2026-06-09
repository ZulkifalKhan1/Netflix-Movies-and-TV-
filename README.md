# 🎬 Netflix Content Dashboard

**Course:** Exploratory Data Analysis | **Instructor:** Ali Hassan Sherazi

---

## Dataset

Place the file `netflix_titles.csv` inside the `data/` folder.  
*(If absent the app auto-downloads it from a public mirror.)*

---

## Installation

```bash
pip install -r requirements.txt
```

## Run Locally

```bash
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

## Project Structure

```
dashboard_project/
├── data/
│   └── netflix_titles.csv       ← exact file name, do NOT rename
├── notebooks/
│   └── analysis.ipynb           ← EDA notebook
├── app.py                       ← main Streamlit dashboard
├── charts.py                    ← all 10 chart functions
├── filters.py                   ← data loading + filter logic
├── requirements.txt
└── README.md
```

---

## Features

### Charts (10 required)
| # | Chart | Purpose |
|---|-------|---------|
| 1 | Pie Chart | Movies vs TV Shows ratio |
| 2 | Histogram | Movie duration frequency |
| 3 | Line Chart | Yearly content trends |
| 4 | Bar Chart | Top 10 countries by content |
| 5 | Scatter Plot | Release year vs duration |
| 6 | Box Plot | Duration spread by rating |
| 7 | Heatmap | Feature correlation matrix |
| 8 | Area Chart | Cumulative content growth |
| 9 | Count Plot | Content count by rating |
| 10 | Violin Plot | Duration distribution by type |

### Filters (6)
- **Content Type** – Movie / TV Show dropdown
- **Age Rating** – Multi-select
- **Country** – Multi-select (top 20)
- **Release Year** – Range slider
- **Movie Duration** – Range slider
- **Text Search** – Title / Director / Cast
- **Reset Button** – Clears all filters

### KPI Cards
Total Titles · Movies · TV Shows · Avg Release Year · Countries

---

## Key Insights

- **Movies dominate** (~70% of Netflix content).
- **United States** produces the most content by far, followed by India and the UK.
- **Content growth accelerated** sharply after 2015.
- **TV-MA** is the most common rating — Netflix targets adult audiences.
- Typical movie length clusters around **90–100 minutes**.
- Strong positive correlation between *Release Year* and the volume of available content.

---

## Deployment

See `Deployment_Guide_Vercel_Render_Railway.pdf` for full instructions.

**Quick deploy on Render:**
```
Build command : pip install -r requirements.txt
Start command : streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

---

*Built with Python 3.x · Streamlit · Pandas · NumPy · Matplotlib · Seaborn*
