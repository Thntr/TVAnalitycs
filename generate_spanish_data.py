import pandas as pd
import numpy as np
import datetime
import random

def generate_spanish_data():
    # 1. Instrucciones Sheet (Spanish Header likely 'Instrucciones' Capitalized)
    instructions_data = {
        'ID': [1, 2],
        'Pregunta de Negocio': ["¿Cuántos clientes consumen video?", "Analisis de Género"],
        'Contexto': ["Prueba de robustez", "Headers en español"]
    }
    
    # 2. Dataset Sheet (Spanish Headers + Sheet name 'Datos')
    # Mapping we want to test:
    # timestamp -> Fecha
    # user_id -> ID_Usuario
    # genre -> Género
    # watch_time_minutes -> Tiempo_Visto
    # completion_rate -> Completitud
    # region -> Región
    
    n_rows = 100
    data = []
    
    for i in range(n_rows):
        data.append({
            'ID_Usuario': f'User_{i}',
            'Fecha': datetime.datetime.now(),
            'Género': random.choice(['Accion', 'Drama']),
            'Región': 'Norte',
            'Tiempo_Visto': 45,
            'Completitud': 0.85,
            'Dispositivo': 'Movil'
        })
        
    df_dataset = pd.DataFrame(data)
    
    file_path = 'dataset_espanol.xlsx'
    
    # Using openpyxl
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        pd.DataFrame(instructions_data).to_excel(writer, sheet_name='Instrucciones', index=False)
        df_dataset.to_excel(writer, sheet_name='Datos', index=False) # NOTE: Sheet is 'Datos' not 'dataset'
        
    print(f"Spanish dataset generated at {file_path}")

if __name__ == "__main__":
    generate_spanish_data()
