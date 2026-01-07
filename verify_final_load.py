from etl import load_data
import pandas as pd

try:
    print("Testing load of 'dataset_final.xlsx'...")
    data = load_data('dataset_final.xlsx')
    
    df = data['dataset']
    print("\n--- Loaded Dataset Columns (Normalized) ---")
    print(df.columns)
    
    # We expect 'customer_id' -> 'user_id'
    # 'screentime' -> 'watch_time_minutes'
    # 'date' -> 'timestamp'
    
    required_map = {
        'user_id': 'CUSTOMER_ID',
        'watch_time_minutes': 'SCREENTIME',
        'timestamp': 'DATE'
    }
    
    success = True
    for internal, original in required_map.items():
        if internal in df.columns:
            print(f"PASSED: Found specific column for {internal} (was {original})")
        else:
            print(f"FAILED: Did not find {internal} (expected from {original})")
            success = False
            
    if success: 
        print("\nSUCCESS: Auto-specialization working!")
    else:
        print("\nFAILURE: Mapping incomplete.")

except Exception as e:
    print(f"\nCRITICAL FAIL: {e}")
