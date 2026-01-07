from etl import load_data
import pandas as pd

# dataset_final.xlsx does NOT have completion_rate, but has SCREENTIME (watch_time) and LENGTH (duration)
try:
    print("Testing derived metrics on 'dataset_final.xlsx'...")
    data = load_data('dataset_final.xlsx')
    if data:
        df = data['dataset']
        if 'completion_rate' in df.columns:
             print("SUCCESS: 'completion_rate' column exists.")
             print("Sample values:")
             print(df[['watch_time_minutes', 'content_duration_minutes', 'completion_rate']].head())
        else:
             print("FAILURE: 'completion_rate' column MISSING.")
    else:
        print("FAILURE: Could not load data.")

except Exception as e:
    print(f"CRITICAL FAIL: {e}")
