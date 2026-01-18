import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import os
from datetime import datetime

# ==============================================================================
# CONFIGURACIÓN (Environment Aware)
# ==============================================================================
DB_USER = os.getenv("DB_USER", "nav_user")
DB_PASS = os.getenv("DB_PASS", "nav_password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "navoptima_warehouse")

DB_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.abspath(os.path.join(BASE_DIR, '../../data/processed/df_final_enriched.csv'))

BUNKER_PRICE_PER_TON = 650.0 

def get_engine():
    return create_engine(DB_URI)

def load_gold_layer():
    print(f"🚀 Iniciando ETL a Capa Gold: {datetime.now()}")
    
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"❌ No se encuentra el archivo: {CSV_PATH}")
    
    print("   📂 Leyendo dataset procesado...")
    df = pd.read_csv(CSV_PATH)
    total_inicial = len(df)
    
    # --------------------------------------------------------------------------
    # FASE 0: LIMPIEZA PREVENTIVA (Data Quality)
    # --------------------------------------------------------------------------
    cols_not_null = ['wind_speed', 'wave_height', 'sog', 'draft', 'fuel_consumption']
    df = df.dropna(subset=cols_not_null)
    
    total_final = len(df)
    eliminados = total_inicial - total_final
    
    if eliminados > 0:
        print(f"      ⚠️ Se eliminaron {eliminados} registros corruptos (NaN en campos críticos).")
    
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    df['wind_speed_rounded'] = df['wind_speed'].round(1)
    df['wave_height_rounded'] = df['wave_height'].round(1)

    print(f"      - Filas listas para ingesta: {total_final}")

    engine = get_engine()

    with engine.connect() as conn:
        
        print("   🏗️ Dimensiones Maestras...")
        conn.execute(text("INSERT INTO gold_navoptima.dim_vessel_types (type_name) VALUES ('Unknown') ON CONFLICT (type_name) DO NOTHING;"))
        conn.commit()
        type_id = conn.execute(text("SELECT vessel_type_id FROM gold_navoptima.dim_vessel_types WHERE type_name = 'Unknown'")).scalar()

        print("   ☁️ Dimensión Clima...")
        weather_df = df[['wind_speed_rounded', 'wave_height_rounded']].drop_duplicates()
        weather_df.columns = ['wind_speed_ms', 'wave_height_m']
        weather_df['weather_category'] = 'Measured'

        existing_weather = pd.read_sql("SELECT wind_speed_ms, wave_height_m FROM gold_navoptima.dim_weather_metrics", conn)
        
        if not existing_weather.empty:
            existing_weather['wind_speed_ms'] = existing_weather['wind_speed_ms'].astype(float)
            existing_weather['wave_height_m'] = existing_weather['wave_height_m'].astype(float)

        merged_weather = pd.merge(weather_df, existing_weather, on=['wind_speed_ms', 'wave_height_m'], how='left', indicator=True)
        to_insert = merged_weather[merged_weather['_merge'] == 'left_only'][['wind_speed_ms', 'wave_height_m', 'weather_category']]

        if not to_insert.empty:
            print(f"      -> Insertando {len(to_insert)} registros climáticos nuevos.")
            to_insert.to_sql('dim_weather_metrics', engine, schema='gold_navoptima', if_exists='append', index=False)
        
        weather_map = pd.read_sql("SELECT wind_speed_ms, wave_height_m, weather_metric_id FROM gold_navoptima.dim_weather_metrics", conn)
        weather_map['wind_speed_ms'] = weather_map['wind_speed_ms'].astype(float)
        weather_map['wave_height_m'] = weather_map['wave_height_m'].astype(float)

        print("   🚢 Dimensión Buques...")
        vessels_df = df.groupby('mmsi').agg({'length': 'first', 'timestamp': 'min'}).reset_index()
        vessels_df.rename(columns={'length': 'length_m', 'timestamp': 'valid_from'}, inplace=True)
        vessels_df['vessel_type_id'] = type_id
        vessels_df['width_m'] = None
        vessels_df['valid_to'] = datetime(9999, 12, 31)
        vessels_df['is_current'] = True
        
        existing_mmsi = pd.read_sql("SELECT mmsi FROM gold_navoptima.dim_vessels", conn)['mmsi'].unique()
        new_vessels = vessels_df[~vessels_df['mmsi'].isin(existing_mmsi)]
        
        if not new_vessels.empty:
            new_vessels.to_sql('dim_vessels', engine, schema='gold_navoptima', if_exists='append', index=False)
            print(f"      -> {len(new_vessels)} buques nuevos registrados.")

        vessel_map = pd.read_sql("SELECT mmsi, vessel_sk FROM gold_navoptima.dim_vessels WHERE is_current = TRUE", conn)

        print("   📊 Tabla de Hechos...")
        
        fact_df = pd.merge(df, vessel_map, on='mmsi', how='inner')
        
        fact_df = pd.merge(
            fact_df, 
            weather_map, 
            left_on=['wind_speed_rounded', 'wave_height_rounded'], 
            right_on=['wind_speed_ms', 'wave_height_m'], 
            how='inner'
        )
        
        fact_df['timestamp_utc'] = fact_df['timestamp']
        fact_df['sog_knots'] = fact_df['sog']
        fact_df['draft_m'] = fact_df['draft']
        fact_df['fuel_consumption_kgh'] = fact_df['fuel_consumption']
        fact_df['fuel_cost_usd'] = (fact_df['fuel_consumption'] / 1000.0) * BUNKER_PRICE_PER_TON
        
        final_cols = ['timestamp_utc', 'vessel_sk', 'weather_metric_id', 'sog_knots', 'draft_m', 'fuel_consumption_kgh', 'fuel_cost_usd']
        
        final_load = fact_df[final_cols]
        total = len(final_load)
        
        if total > 0:
            print(f"      -> 💾 Insertando {total} registros (Lotes de 10k)...")
            final_load.to_sql('fact_vessel_performance', engine, schema='gold_navoptima', if_exists='append', index=False, chunksize=10000)
        else:
            print("      ⚠️ ALERTA: 0 registros para insertar. Verifica los merges.")
        
    print("✅ ¡Carga Completa!")

if __name__ == "__main__":
    load_gold_layer()