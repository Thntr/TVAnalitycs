import pandas as pd
import duckdb
import numpy as np
from sklearn.cluster import KMeans
from lifelines import KaplanMeierFitter

class AnalyticsEngine:
    def __init__(self, df):
        self.df = df
        self.con = duckdb.connect(database=':memory:')
        self.con.register('video_events', df)

    def get_kpis(self):
        """
        Calculates top-level KPIs for the dashboard cards.
        """
        query = """
        SELECT
            SUM(watch_time_minutes) as total_screentime,
            COUNT(DISTINCT user_id) as active_customers,
            AVG(completion_rate) * 100 as avg_completion_pct,
            AVG(watch_time_minutes) as avg_watch_time
        FROM video_events
        """
        df = self.con.execute(query).df()
        return df.iloc[0].to_dict()

    def get_time_series(self):
        """
        Daily trend of Total Screentime for the central chart.
        """
        query = """
        SELECT
            DATE_TRUNC('day', timestamp) as day,
            SUM(watch_time_minutes) as total_screentime
        FROM video_events
        GROUP BY 1
        ORDER BY 1
        """
        return self.con.execute(query).df()

    def get_geographic_stats(self):
        """
        For the Heatmap (Region concentration).
        """
        if 'region' not in self.df.columns:
            return pd.DataFrame()
            
        query = """
        SELECT
            region,
            COUNT(*) as events,
            SUM(watch_time_minutes) as total_watch_time
        FROM video_events
        GROUP BY region
        ORDER BY total_watch_time DESC
        """
        return self.con.execute(query).df()

    def get_content_intelligence(self):
        """
        Returns multiple dataframes for Content Intel:
        1. Top Titles/Genres (Treemap/Table)
        2. Format Efficiency
        3. Language Preference
        """
        # Top Genres (for Treemap and Stickiness)
        genre_query = """
        SELECT 
            genre,
            COUNT(DISTINCT user_id) as unique_viewers,
            SUM(watch_time_minutes) as total_watch_time,
            AVG(watch_time_minutes) as avg_watch_time -- Stickiness proxy per genre
        FROM video_events
        GROUP BY genre
        ORDER BY total_watch_time DESC
        """
        top_genres = self.con.execute(genre_query).df()

        # Format Efficiency
        if 'video_format' in self.df.columns:
            format_query = """
            SELECT video_format, SUM(watch_time_minutes) as total_watch_time
            FROM video_events GROUP BY video_format ORDER BY total_watch_time DESC
            """
            format_df = self.con.execute(format_query).df()
        else:
            format_df = pd.DataFrame()

        # Language Preference
        if 'audio_lang' in self.df.columns:
            lang_query = """
            SELECT audio_lang, COUNT(*) as usage_count
            FROM video_events GROUP BY audio_lang ORDER BY usage_count DESC
            """
            lang_df = self.con.execute(lang_query).df()
        else:
            lang_df = pd.DataFrame()

        return {
            'top_genres': top_genres,
            'format_efficiency': format_df,
            'language_preference': lang_df
        }

    def get_infrastructure_insights(self):
        """
        Device Share and Quality of Experience.
        """
        # Device Share
        device_query = """
        SELECT device, COUNT(*) as count, SUM(watch_time_minutes) as watch_time
        FROM video_events GROUP BY device ORDER BY watch_time DESC
        """
        device_df = self.con.execute(device_query).df()
        
        # Quality Exp (Region x Format)
        if 'region' in self.df.columns and 'video_format' in self.df.columns:
            quality_query = """
            SELECT region, video_format, COUNT(*) as count
            FROM video_events 
            GROUP BY region, video_format
            """
            quality_df = self.con.execute(quality_query).df()
        else:
            quality_df = pd.DataFrame()

        return {'device_share': device_df, 'quality_matrix': quality_df}

    def perform_clustering(self):
        """
        Retained for 'Segmentation' deep dive.
        """
        df = self.df.copy()
        numeric_cols = [c for c in ['watch_time_minutes', 'completion_rate', 'content_duration_minutes'] if c in df.columns]
        
        if not numeric_cols:
            return df, []
            
        # Fill NA
        for c in numeric_cols:
            df[c] = df[c].fillna(0)
            
        # Normalize
        data = df[numeric_cols]
        std = data.std()
        # Avoid division by zero
        normalized = (data - data.mean()) / std.replace(0, 1) 
        normalized = normalized.fillna(0)
        
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        df['cluster'] = kmeans.fit_predict(normalized)
        
        return df, numeric_cols

    def survival_analysis(self):
        """
        Retained for Retention Curve.
        """
        kmf = KaplanMeierFitter()
        T = self.df['watch_time_minutes']
        E = np.ones(len(T))
        kmf.fit(T, event_observed=E)
        return kmf

    def get_sai(self, segment_col='segment', genre_col='genre'):
        """
        Calculates Segment Affinity Index (SAI).
        SAI = (% Genre Share in Segment / % Genre Share Global) * 100
        """
        if segment_col not in self.df.columns or genre_col not in self.df.columns:
            return pd.DataFrame()

        # 1. Global Share
        global_total = len(self.df)
        global_counts = self.df[genre_col].value_counts()
        global_share = global_counts / global_total

        # 2. Segment Share
        # Cross tab: Index=Segment, Col=Genre, Val=Count
        ct = pd.crosstab(self.df[segment_col], self.df[genre_col])
        # Percentage within row (segment)
        segment_share = ct.div(ct.sum(axis=1), axis=0)

        # 3. SAI Calculation
        # SAI = (Segment Share / Global Share) * 100
        # Global share matches columns of segment_share
        sai_matrix = segment_share.div(global_share, axis=1) * 100
        
        return sai_matrix.fillna(0)

    # --- Decision Intelligence (v2.2) ---

    def get_recurrence_metrics(self):
        """
        Calculates average time between sessions (Recurrence).
        Formula: Avg(Date_n - Date_n-1) per user.
        """
        # Ensure timestamp is ordered
        df = self.df.sort_values(['user_id', 'timestamp'])
        df['prev_date'] = df.groupby('user_id')['timestamp'].shift(1)
        df['diff_days'] = (df['timestamp'] - df['prev_date']).dt.total_seconds() / (3600 * 24)
        
        avg_recurrence = df['diff_days'].mean()
        unique_dates = df['timestamp'].dt.date.nunique()
        
        return {
            'avg_recurrence_days': avg_recurrence if not pd.isna(avg_recurrence) else 0.0,
            'unique_dates_count': unique_dates
        }

    def get_device_ratio(self):
        """
        Calculates Omnichannel Ratio: Avg Unique Devices per User.
        """
        devices_per_user = self.df.groupby('user_id')['device'].nunique()
        ratio = devices_per_user.mean()
        return ratio

    def get_format_correlation(self):
        """
        Correlation between Video Format (Ordinal/Cat) and Watch Time.
        Uses simple GroupBy Mean for determining the 'Truth' and proper correlation if mapped.
        """
        if 'video_format' not in self.df.columns:
            return None, pd.DataFrame()

        # 1. Insight: Mean Watch Time per Format
        format_performance = self.df.groupby('video_format')['watch_time_minutes'].mean().sort_values(ascending=False)
        
        # 2. Tech: Correlation (Point Biserial approximation)
        # Map formats to ordinal if possible (HD=1, 4K=2) or just use factorize
        df_coded = self.df.copy()
        df_coded['format_code'], _ = pd.factorize(df_coded['video_format'])
        
        # Pearson correlation between Code and Time
        correlation = df_coded['format_code'].corr(df_coded['watch_time_minutes'])
        
        return correlation, format_performance

    def get_cross_distribution(self, col1, col2, metric='watch_time_minutes'):
        """
        Generic Pivot Table for questions like 'Consumption by Segment and Region'.
        """
        if col1 not in self.df.columns or col2 not in self.df.columns:
            return pd.DataFrame()
            
        return self.df.pivot_table(index=col1, columns=col2, values=metric, aggfunc='mean')

    def get_top_content_ranking(self):
        """
        Returns top content by screentime.
        """
        # Assuming we might want Title if available, or Genre if not.
        # The prompt mentions "Top Titles" but dataset usually has Genre. 
        # Checking previous file view, logic uses 'category' or 'genre'.
        # If 'title' column exists, use it. Else fall back to 'genre' or 'segment'.
        
        target = 'genre' 
        # Check for title column equivalents
        candidates = ['title', 'titulo', 'content_name', 'nombre_contenido']
        for c in candidates:
            if c in self.df.columns:
                target = c
                break
                
        return self.df.groupby(target)['watch_time_minutes'].sum().sort_values(ascending=False)
