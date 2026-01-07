import pandas as pd
import numpy as np
import datetime
import random

def generate_final_data():
    # 1. Instrucciones Sheet
    instructions_data = {
        'ID': [1], 
        'Pregunta de Negocio': ["¿Cuál es el género más visto?"], 
        'Contexto': ["Validacion final"]
    }
    
    # 2. Dataset Sheet - EXACT USER SCHEMA
    # DATE, CUSTOMER_ID, REGION, DEVICE, TITLE, GENRE, SCREENTIME, LENGTH, VIDEO_FORMAT, AUDIO_LANGUAGE, SEGMENTO
    
    n_rows = 200
    data = []
    
    start_date = datetime.date(2025, 1, 1)
    
    for i in range(n_rows):
        day_offset = random.randint(0, 180)
        date_val = start_date + datetime.timedelta(days=day_offset)
        
        screentime = random.randint(5, 120)
        length = screentime + random.randint(0, 20)
        
        data.append({
            'DATE': date_val,
            'CUSTOMER_ID': f'Cust_{random.randint(1000, 9999)}',
            'REGION': random.choice(['Norte', 'Sur', 'Centro']),
            'DEVICE': random.choice(['Smart TV', 'Mobile']),
            'TITLE': f'Video {i}',
            'GENRE': random.choice(['Drama', 'Comedia', 'Documental']),
            'SCREENTIME': screentime,
            'LENGTH': length,
            'VIDEO_FORMAT': 'HD',
            'AUDIO_LANGUAGE': 'ES',
            'SEGMENTO': random.choice(['A', 'B', 'C'])
        })
        
    df_dataset = pd.DataFrame(data)
    
    file_path = 'dataset_final.xlsx'
    
    # Using openpyxl
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        pd.DataFrame(instructions_data).to_excel(writer, sheet_name='instrucciones', index=False)
        df_dataset.to_excel(writer, sheet_name='dataset', index=False)
        
    print(f"Final specialized dataset generated at {file_path}")

if __name__ == "__main__":
    generate_final_data()
