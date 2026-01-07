import pandas as pd
import numpy as np
import datetime
import random

def generate_data():
    # 1. Instrucciones Sheet
    instructions_data = {
        'ID': [1, 2, 3],
        'Pregunta de Negocio': [
            "¿Cuántos clientes consumen video al mes? (MAU)",
            "¿Cuál es el género más visto considerando tiempo y finalización?",
            "¿Existe relación entre la región y el género visto?"
        ],
        'Contexto': [
            "Necesitamos medir el alcance real de la plataforma.",
            "Las vistas simples son engañosas; buscamos engagement real.",
            "Marketing quiere segmentar campañas por zona geográfica."
        ]
    }
    df_instructions = pd.read_json(pd.DataFrame(instructions_data).to_json()) # normalize

    # 2. Dataset Sheet
    n_rows = 5000
    user_ids = [f'User_{i}' for i in range(1, 501)] # 500 unique users
    genres = ['Action', 'Drama', 'Comedy', 'Sci-Fi', 'Romance', 'Documentary']
    regions = ['North', 'South', 'East', 'West', 'Central']
    devices = ['Smart TV', 'Mobile', 'Desktop', 'Tablet']
    
    data = []
    
    start_date = datetime.date(2025, 1, 1)
    end_date = datetime.date(2025, 6, 30)
    
    for _ in range(n_rows):
        uid = random.choice(user_ids)
        # Random date in range
        day_offset = random.randint(0, (end_date - start_date).days)
        date_event = start_date + datetime.timedelta(days=day_offset)
        
        # Add time component for Peak Hour analysis
        hour = int(np.random.normal(20, 3)) % 24 # Peak around 20:00
        timestamp = datetime.datetime.combine(date_event, datetime.time(hour, random.randint(0, 59)))
        
        genre = random.choice(genres)
        
        # Correlate Genre with Region slightly for Chi-Square to find something
        region = random.choice(regions)
        if region == 'North' and random.random() > 0.7:
            genre = 'Action'
        
        watch_time = max(1, int(np.random.normal(30, 15))) # Minutes
        duration = watch_time + int(abs(np.random.normal(5, 5)))
        completion = min(1.0, watch_time / duration)
        
        vst = abs(np.random.normal(1.5, 0.5)) # Video Startup Time (sec)
        rebuffer = random.random() < 0.1 # 10% rebuffer
        
        data.append({
            'user_id': uid,
            'timestamp': timestamp,
            'genre': genre,
            'region': region,
            'device': random.choice(devices),
            'watch_time_minutes': watch_time,
            'content_duration_minutes': duration,
            'completion_rate': completion,
            'video_startup_time_sec': vst,
            'had_rebuffer': rebuffer
        })
        
    df_dataset = pd.DataFrame(data)
    
    # Write to Excel
    file_path = 'autogravity_dataset.xlsx'
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        pd.DataFrame(instructions_data).to_excel(writer, sheet_name='instrucciones', index=False)
        df_dataset.to_excel(writer, sheet_name='dataset', index=False)
        
    print(f"Dataset generated at {file_path}")

if __name__ == "__main__":
    generate_data()
