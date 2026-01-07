import pandas as pd
import duckdb

def normalize_sheet_name(sheet_names, target):
    """Finds the actual sheet name doing a case-insensitive match."""
    target_lower = target.lower()
    for name in sheet_names:
        if name.lower() == target_lower:
            return name
    # Fallback: Try partial match if exact fail? E.g. "Instrucciones v2"
    for name in sheet_names:
        if target_lower in name.lower():
            return name
    return None

def normalize_columns(df):
    """
    Maps varied column names (Spanish, etc.) to standard English names required by AnalyticsEngine.
    """
    column_map = {
        'timestamp': ['fecha', 'date', 'timestamp', 'time', 'hora', 'marca_temporal', 'fecha_evento'],
        'user_id': ['user_id', 'usuario', 'id_usuario', 'cliente', 'id_cliente', 'usuario_id', 'customer_id'],
        'genre': ['genre', 'genero', 'género', 'categoria', 'tipo_video'],
        'region': ['region', 'región', 'zona', 'ubicacion', 'territorio'],
        'device': ['device', 'dispositivo', 'plataforma'],
        'watch_time_minutes': ['watch_time', 'watch_time_minutes', 'tiempo_visto', 'minutos_vistos', 'duracion_real', 'minutos_reproducidos', 'tiempo_visualizacion', 'screentime'],
        'completion_rate': ['completion', 'completion_rate', 'completitud', 'tasa_completado', '%_visto', 'porcentaje_completado'],
        'video_startup_time_sec': ['vst', 'video_startup_time', 'tiempo_inicio', 'startup_time', 'segundos_inicio'],
        # Special User Schema
        'content_duration_minutes': ['duration', 'duracion', 'duración', 'largo_total', 'length'],
        'segment': ['segment', 'segmento', 'grupo'],
        # New Autogravity 2.0 Columns
        'video_format': ['video_format', 'format', 'formato', 'calidad', 'resolution', 'resolucion'],
        'audio_lang': ['audio_lang', 'audio', 'language', 'idioma', 'lenguaje']
    }

    # Normalize existing columns to lowercase
    df.columns = [c.strip().lower() for c in df.columns]
    
    # Create a mapping from current -> target
    rename_dict = {}
    found_targets = set()
    
    for target, aliases in column_map.items():
        for alias in aliases:
            if alias in df.columns:
                rename_dict[alias] = target
                found_targets.add(target)
                break # Found a match for this target, stop looking aliases
    
    if rename_dict:
        df = df.rename(columns=rename_dict)
        # print(f"Renamed columns: {rename_dict}")
        
    # Validation
    required = ['timestamp', 'user_id', 'genre', 'watch_time_minutes']
    missing = [col for col in required if col not in df.columns]
    
    if missing:
        # Don't raise error, just warn and return. The UI will handle mapping.
        # print(f"Warning: Missing columns {missing}. UI should handle this.")
        pass

    return df

def load_data(file):
    """
    Loads the Excel file. 
    Returns a dictionary of DataFrames: {'instrucciones': df, 'dataset': df}
    """
    try:
        # Load sheets. If file is None, returns None.
        if file is None:
            return None
        
        xls = pd.ExcelFile(file)
        sheet_names = xls.sheet_names
        # print(f"Found sheets: {sheet_names}")
        
        data = {}
        
        # 1. Load Instrucciones
        instr_sheet = normalize_sheet_name(sheet_names, 'instrucciones')
        if instr_sheet:
            data['instrucciones'] = pd.read_excel(xls, sheet_name=instr_sheet)
        else:
            # print("Warning: 'Instrucciones' sheet not found.")
            pass
            
        # 2. Load Dataset
        dataset_sheet = normalize_sheet_name(sheet_names, 'dataset')
        # Fallback: if no sheet named dataset, maybe it's named 'Datos' or 'Data'
        if not dataset_sheet:
             dataset_sheet = normalize_sheet_name(sheet_names, 'datos')
             
        if dataset_sheet:
            df = pd.read_excel(xls, sheet_name=dataset_sheet)
            
            # Smart Cleaning & Mapping
            df = normalize_columns(df)
            
            # Type Enforcement
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
            
            if 'genre' in df.columns:
                df['genre'] = df['genre'].astype(str).str.strip().str.title()
                
            # Derived Metrics
            if 'completion_rate' not in df.columns:
                 if 'watch_time_minutes' in df.columns and 'content_duration_minutes' in df.columns:
                     # print("Calculating 'completion_rate' from Watch Time and Content Duration...")
                     # Avoid division by zero
                     df['content_duration_minutes'] = pd.to_numeric(df['content_duration_minutes'], errors='coerce').replace(0, pd.NA)
                     df['watch_time_minutes'] = pd.to_numeric(df['watch_time_minutes'], errors='coerce')
                     
                     df['completion_rate'] = df['watch_time_minutes'] / df['content_duration_minutes']
                     # Fill NaNs (div by zero or missing) with 0
                     df['completion_rate'] = df['completion_rate'].fillna(0)
                     # Clip to range [0, 1] (in case watch time > duration)
                     df['completion_rate'] = df['completion_rate'].clip(0, 1)

            # Numeric conversion
            for col in ['watch_time_minutes', 'completion_rate', 'content_duration_minutes']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

            data['dataset'] = df
        else:
             raise ValueError("Could not find a sheet named 'Dataset', 'Datos', or similar.")
            
        return data
    except Exception as e:
        # Log error but re-raise so App can show it
        # print(f"Error loading data: {e}")
        raise e

def get_duckdb_connection(df_dataset):
    """
    Returns a duckdb connection with the dataset registered as a table 'video_events'.
    """
    con = duckdb.connect(database=':memory:')
    con.register('video_events', df_dataset)
    return con
