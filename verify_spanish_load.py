from etl import load_data
import pandas as pd

try:
    print("Testing load of 'dataset_espanol.xlsx'...")
    data = load_data('dataset_espanol.xlsx')
    
    df = data['dataset']
    print("\n--- Loaded Dataset Columns (Normalized) ---")
    print(df.columns)
    
    print("\n--- Sample Row ---")
    print(df.iloc[0])
    
    required = ['timestamp', 'user_id', 'genre', 'watch_time_minutes']
    if all(c in df.columns for c in required):
        print("\nSUCCESS: All required columns mapped correctly!")
    else:
        print(f"\nFAILURE: Missing columns. Found: {df.columns}")

except Exception as e:
    print(f"\nCRITICAL FAIL: {e}")
