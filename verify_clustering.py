from etl import load_data
from analytics import AnalyticsEngine
import pandas as pd

try:
    print("Loading specialized dataset...")
    # This dataset has SEGMENTO, SCREENTIME, LENGTH but NO 'video_startup_time'
    data = load_data('dataset_final.xlsx') 
    df = data['dataset']
    
    print(f"Columns: {df.columns.tolist()}")
    
    ae = AnalyticsEngine(df)
    
    print("\n--- Testing Robust Clustering ---")
    clustered_df, features = ae.perform_clustering()
    
    print("SUCCESS: Clustering completed!")
    print(f"Features used: {features}")
    print("Cluster Preview:")
    print(clustered_df['cluster'].value_counts())
    
except Exception as e:
    print(f"\nFAILURE: {e}")
