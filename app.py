import streamlit as st
import pandas as pd
import plotly.express as px
from etl import load_data
from analytics import AnalyticsEngine

# --- Configuration ---
st.set_page_config(page_title="AutoGravity 3.0 | Scientific Dashboard", layout="wide", page_icon="🪐")

# --- CUSTOM CSS (AutoGravity 3.0 Design System from code.html) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Noto+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap');

    /* Global Variables */
    :root {
        --primary: #1111d4;
        --primary-glow: #4d4dff;
        --bg-dark: #0f0f12;
        --card-dark: #181823;
        --neon-green: #0bda68;
        --glass-border: rgba(255, 255, 255, 0.08);
    }

    /* Reset & Base */
    .stApp {
        background-color: var(--bg-dark);
        font-family: 'Noto Sans', sans-serif;
        color: white;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif !important;
    }

    /* Custom Classes for HTML Components */
    .glass-panel {
        background: rgba(24, 24, 35, 0.65);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        transition: all 0.3s ease;
    }
    
    .glass-panel:hover {
        border-color: rgba(17, 17, 212, 0.3);
        box-shadow: 0 0 15px rgba(17, 17, 212, 0.1);
    }

    .neon-text {
        text-shadow: 0 0 8px rgba(17, 17, 212, 0.6);
        color: white;
    }
    
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 700;
        letter-spacing: -1px;
    }
    
    .kpi-label {
        color: #94a3b8;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Override Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111118;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    /* Tabs Customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255,255,255,0.05);
        border-radius: 8px;
        color: #94a3b8;
        border: none;
        padding: 8px 16px;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: var(--primary);
        color: white;
    }

    /* Button Overrides */
    div.stButton > button {
        background-color: rgba(255, 255, 255, 0.05);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        transition: all 0.2s;
    }
    div.stButton > button:hover {
        background-color: var(--primary);
        border-color: var(--primary);
        box-shadow: 0 0 15px rgba(17, 17, 212, 0.3);
    }

    /* Terminal Style */
    .terminal-box {
        background: #000;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 12px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: #0bda68;
        margin-top: 10px;
    }
    
    /* Neon Bubble */
    .insight-bubble {
        border: 1px solid var(--neon-green);
        background: rgba(11, 218, 104, 0.05);
        color: var(--neon-green);
        padding: 8px 16px;
        border-radius: 50px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 0 10px rgba(11, 218, 104, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---

def card_30(title, value, subtext="", icon="analytics"):
    """Renders a KPI card in AutoGravity 3.0 style."""
    st.markdown(f"""
    <div class="glass-panel" style="padding: 20px;">
        <div class="kpi-label">
            <span class="material-symbols-outlined" style="font-size: 18px;">{icon}</span> {title}
        </div>
        <div class="kpi-value neon-text">{value}</div>
        <div style="color: #64748b; font-size: 0.8rem; margin-top: 4px;">{subtext}</div>
    </div>
    """, unsafe_allow_html=True)

def insight_card_30(title, main_insight, desc, technical_data):
    """Triple Layer Insight Card (AG 3.0)."""
    with st.container():
        st.markdown(f"""
        <div class="glass-panel">
            <h4 style="margin-bottom: 12px; display:flex; align-items:center; gap:8px;">
                <span class="material-symbols-outlined" style="color:#1111d4;">lightbulb</span> {title}
            </h4>
            <div class="insight-bubble">{main_insight}</div>
            <div style="margin-top: 16px; color: #cbd5e1; font-size: 0.95rem; line-height: 1.5;">
                {desc}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Tech Layer (integrated outside HTML to use native expander logic)
        with st.expander("💻 Scientific Terminal"):
             st.markdown(f"""
             <div class="terminal-box">
             > query: {technical_data.get('formula', 'N/A')}<br>
             > result: {technical_data.get('raw', 'N/A')}
             </div>
             """, unsafe_allow_html=True)

# --- DATA LOADING ---
if 'dataset' not in st.session_state:
    st.session_state.dataset = None

with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 30px; padding-left: 10px;">
        <div style="width: 40px; height: 40px; background: rgba(17,17,212,0.2); border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(17,17,212,0.4);">
             <span style="font-size: 24px;">🪐</span>
        </div>
        <div>
            <h2 style="margin:0; font-size: 18px; font-weight: 700;">AutoGravity</h2>
            <p style="margin:0; font-size: 10px; color: #64748b; font-family: 'JetBrains Mono';">v3.0.1 // SCIENTIFIC</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    nav = st.radio("Navigation", ["Mission Control", "Analytics", "Experiments"], label_visibility="collapsed")
    
    st.markdown("---")
    uploaded_file = st.file_uploader("Upload Dataset", type=['xlsx'])
    
    # Filters
    st.markdown("### 🔭 Global Filters")
    # Placeholders for filters - logic below

data_source = uploaded_file if uploaded_file else 'autogravity_dataset.xlsx'
try:
    if st.session_state.dataset is None or uploaded_file:
        loaded = load_data(data_source)
        if loaded: st.session_state.dataset = loaded.get('dataset')
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

df = st.session_state.dataset
if df is None: st.warning("No Data"); st.stop()

# Apply Sidebar Filters
with st.sidebar:
    selected_region = st.selectbox("Region", ["All"] + list(df['region'].unique()) if 'region' in df.columns else ["All"])
    selected_device = st.selectbox("Device", ["All"] + list(df['device'].unique()) if 'device' in df.columns else ["All"])

filtered_df = df.copy()
if selected_region != "All": filtered_df = filtered_df[filtered_df['region'] == selected_region]
if selected_device != "All": filtered_df = filtered_df[filtered_df['device'] == selected_device]

ae = AnalyticsEngine(filtered_df)
kpis = ae.get_kpis()

# --- MAIN LAYOUT ---

# 1. MISSION CONTROL (The 7 Questions)
if nav == "Mission Control":
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:end; margin-bottom: 24px;">
        <div>
            <h1 style="font-size: 3rem; margin-bottom: 0;">Mission Control <span style="font-size: 0.5em; vertical-align: middle; background: rgba(17,17,212,0.2); color: #4d4dff; padding: 4px 12px; border-radius: 50px; border: 1px solid rgba(17,17,212,0.4);">LIVE</span></h1>
            <p style="color: #94a3b8;">Strategic Decision Intelligence Hub</p>
        </div>
        <div style="text-align: right; color: #0bda68; font-family: 'JetBrains Mono'; font-size: 0.8rem;">
            ● SYS: ONLINE<br>LATENCY: 12ms
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Top KPI Row
    c1, c2, c3 = st.columns(3)
    with c1: card_30("Active Users (Q1)", f"{kpis['active_customers']:,}", "Unique Identities", "group")
    with c2: card_30("Total Volume", f"{kpis['total_screentime']:,.0f}", "Minutes Watched", "schedule")
    with c3: card_30("Avg Completion", f"{kpis['avg_completion_pct']:.1f}%", "Content Stickiness", "check_circle")

    st.markdown("### 🧠 The 7 Strategic Insights")
    t1, t2 = st.tabs(["Identity & Habits (1-4)", "Market & Growth (5-7)"])
    
    with t1:
        c_a, c_b = st.columns(2)
        with c_a:
            # Q1: Already covered in KPI, but let's add context
            insight_card_30("1. Active Customers", 
                           f"{kpis['active_customers']} Identities",
                           "No contamos clics, contamos personas. Elimina el ruido de sesiones múltiples.",
                           {'formula': 'COUNT(DISTINCT user_id)', 'raw': kpis['active_customers']})
            
            # Q2: Genre
            top_genre_df = ae.get_content_intelligence()['top_genres']
            winner = top_genre_df.index[0] if not top_genre_df.empty else "N/A"
            insight_card_30("2. Dominant Genre",
                           f"{winner}",
                           "Defines your platform DNA. Are you a digital babysitter or a virtual stadium?",
                           {'formula': 'SUM(watch_time) GROUP BY genre', 'raw': winner})
        
        with c_b:
            # Q3: Devices
            ratio = ae.get_device_ratio()
            insight_card_30("3. Omnichannel Ratio",
                           f"{ratio:.2f} Dev/User",
                           ">1.0 means healthy mobility. Users are taking the app with them.",
                           {'formula': 'AVG(COUNT(DISTINCT dev))', 'raw': ratio})
            
            # Q4: Trend
            trend = ae.get_time_series()
            with st.container():
                st.markdown('<div class="glass-panel"><h5>4. Monthly Trend</h5>', unsafe_allow_html=True)
                if not trend.empty: st.line_chart(trend.set_index('day'), height=200)
                st.markdown('</div>', unsafe_allow_html=True)

    with t2:
        c_c, c_d = st.columns(2)
        with c_c:
             # Q5: Region
            geo_stats = ae.get_geographic_stats()
            top_reg = geo_stats.iloc[0]['region'] if not geo_stats.empty else "N/A"
            insight_card_30("5. Regional Leader",
                           f"{top_reg}",
                           "Prioritizes infrastructure (CDN) and local marketing campaigns.",
                           {'formula': 'SUM(watch_time) GROUP BY region', 'raw': top_reg})
            
            # Q7: Recurrence
            rec = ae.get_recurrence_metrics()
            insight_card_30("7. Recurrence Cycle",
                           f"Every {rec['avg_recurrence_days']:.1f} Days",
                           "The antidote to Churn. Measures how often users return.",
                           {'formula': 'Avg(Date_n - Date_n-1)', 'raw': rec})
            
        with c_d:
            # Q6: Top Content
            ranking = ae.get_top_content_ranking()
            top_1 = ranking.index[0] if not ranking.empty else "N/A"
            insight_card_30("6. Top Title",
                           f"#1 {top_1}",
                           "The Pareto of Attention. This single title drives your retention.",
                           {'formula': 'Ranking by WatchTime', 'raw': ranking.head(3).to_dict()})


# 2. ANALYTICS (Content Intel)
elif nav == "Analytics":
    st.markdown("<h1>Streamalytics <span style='font-weight:300;opacity:0.7'>// Content Intel</span></h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.subheader("Genre Dominance")
        top_genres = ae.get_content_intelligence()['top_genres']
        st.bar_chart(top_genres['total_watch_time'], color="#1111d4")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        card_30("Engagement Score", f"{kpis['avg_completion_pct']/10:.1f}/10", "Derived from Completion", "bolt")
        card_30("Quality Pref", "HD (1080p)", "Correlated with Long Sessions", "hd")


# 3. EXPERIMENTS (Deep Dives)
elif nav == "Experiments":
    st.markdown("<h1>Experiments <span style='font-weight:300;opacity:0.7'>// Deep Dives</span></h1>", unsafe_allow_html=True)
    
    tab_sai, tab_sim, tab_clus = st.tabs(["SAI (Targeting)", "Gravity Sim", "Clustering AI"])
    
    with tab_sai:
        if 'segment' in df.columns and 'genre' in df.columns:
            sai = ae.get_sai()
            st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
            st.plotly_chart(px.imshow(sai, text_auto=True, color_continuous_scale='RdBu_r'), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            insight_card_30("SAI Analysis", "Red Cells (>120) = Fanatics", "Relative Passion Index. Shows over-indexing regardless of volume.", {'formula':'Matrix Division', 'raw':'SAI Matrix'})

    with tab_sim:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        boost = st.slider("Boost Watch Time %", 0, 50, 10)
        base = kpis['total_screentime'] * 0.10
        new_v = base * (1 + boost/100)
        st.metric("Proj. Revenue", f"${new_v:,.0f}", delta=f"+${new_v-base:,.0f}")
        st.progress(min(100, 50+boost))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab_clus:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        try:
            c_df, ft = ae.perform_clustering()
            if not c_df.empty:
                f3 = px.scatter(c_df, x=ft[0], y=ft[1], color='cluster', title="K-Means Tribes")
                f3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
                st.plotly_chart(f3, use_container_width=True)
        except: st.error("Clustering Error")
        st.markdown('</div>', unsafe_allow_html=True)
