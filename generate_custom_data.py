import pandas as pd
import numpy as np
import datetime
import random

def generate_custom_data():
    # 1. Instrucciones
    instructions_data = {
        'ID': [1], 'Pregunta de Negocio': ["¿Cuántos clientes consumen video?"], 'Contexto': ["Test Mapping"]
    }
    
    # 2. Dataset with WEIRD columns
    n_rows = 100
    data = []
    
    for i in range(n_rows):
        data.append({
            'CUSTOMER_ID': f'Cust_{i}',
            'DATE': datetime.datetime.now(),
            'TITLE': 'Video A',
            'GENRE': 'Action',
            'REGION': 'MX',
            'SCREENTIME': 120,    # Map to watch_time_minutes
            'COMPLETION': 1.0
        })
        
    df = pd.DataFrame(data)
    
    file_path = 'dataset_custom.xlsx'
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        pd.DataFrame(instructions_data).to_excel(writer, sheet_name='instrucciones', index=False)
        df.to_excel(writer, sheet_name='dataset', index=False)
        
    print(f"Custom dataset generated at {file_path}")

if __name__ == "__main__":
    generate_custom_data()
