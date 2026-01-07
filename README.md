# 🪐 AutoGravity Analytics
### Decision Intelligence Platform (Educational Edition)

**AutoGravity Analytics** is a next-generation dashboard designed not just to display data, but to calculate decisions. It transforms raw streaming metrics into strategic insights using a **Triple Layer Methodology** that combines raw data, pedagogical context, and technical implementation details.

![Status](https://img.shields.io/badge/Status-Production%20Ready-success)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Stack](https://img.shields.io/badge/Stack-Streamlit%20|%20DuckDB%20|%20Sklearn-purple)

---

## 🧠 The Triple Layer Philosophy
Almost every component in this application delivers value in three dimensions:
1.  **The Answer (Neon)**: The immediate business fact (e.g., "$1.2M Revenue").
2.  **Pedagogy (Professor Mode)**: A toggle explaining *why* this metric matters for business strategy.
3.  **Technical (Scientific Terminal)**: An expander revealing the exact SQL/Python math behind the number.

---

## ✨ Key Features

### 1. The 7 Master Questions
We answer the critical business questions for a streaming platform:
1.  **Identity**: "What is the most watched genre?" (Niñera Digital vs. Estadio Virtual).
2.  **Omnichannel**: "Do users use more than one device?" (Device Ratio > 1.0).
3.  **Cultural DNA**: "Is there a relation between Region and Genre?" (Heatmap).
4.  **Seasonality**: "How is consumption during the month?" (Time Series).
5.  **Geography**: "Consumption by Region?" (Infrastructure prioritization).
6.  **Hierarchy**: "Top Most Watched Titles" (Pareto of attention).
7.  **Habit**: "Recurrence of consumption" (The antidote to Churn).

### 2. Deep Dives & Simulations
*   **🔮 Gravity Simulator (What-If)**: A financial projection tool. Adjust the "Average Watch Time" slider to see the exponential impact on LTV and Revenue using a linear elasticity model.
*   **🎯 SAI (Segment Affinity Index)**: A custom metric that detects "Fanatic Niches". It highlights segments that over-index on specific genres (SAI > 120) regardless of total volume.
*   **🤖 Clustering (Unsupervised Metrics)**: Uses **K-Means** to automatically detect hidden user tribes based on Watch Time, Completion Rate, and Content Duration.

---

## 🛠️ Technical Architecture
*   **Frontend**: Streamlit with custom CSS (Glassmorphism, Neon UI, Bento Grid).
*   **Backend**: `AnalyticsEngine` class powered by **DuckDB** for in-memory ultra-fast SQL querying.
*   **ML**: Scikit-Learn (KMeans) and Lifelines (Survival Analysis fallback).
*   **Viz**: Plotly Express for interactive heatmaps and 3D scatter plots.

---

## 🚀 Installation & Usage

### Prerequisites
*   Python 3.8+
*   pip

### Setup
1.  Clone the repository:
    ```bash
    git clone https://github.com/yourusername/autogravity-analytics.git
    cd autogravity-analytics
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the App
```bash
streamlit run app.py
```
The application will launch in your default browser at `http://localhost:8501`.

### Data Format
The app expects an Excel file with columns: `user_id`, `watch_time_minutes`, `genre`, `region`, `device`, `timestamp`, `video_format`. (A sample dataset generator is included in `etl.py`).

---

## 📂 Project Structure
```
autogravity_analytics/
├── app.py              # Main Frontend (Streamlit)
├── analytics.py        # Core Logic (DuckDB + ML Class)
├── etl.py              # Data Loading & Normalization
├── requirements.txt    # Dependencies
├── README.md           # Documentation
└── dataset/            # Place your .xlsx files here
```

---

*Designed for Data Scientists and Executives who want to bridge the gap between Code and Strategy.*
