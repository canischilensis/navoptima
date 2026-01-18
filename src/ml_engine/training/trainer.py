import os
import pandas as pd
import numpy as np
import xgboost as xgb
import mlflow
import mlflow.xgboost
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# ==============================================================================
# CONFIGURACIÓN (Conexión a la Bóveda de Datos)
# ==============================================================================
DB_USER = os.getenv("DB_USER", "nav_user")
DB_PASS = os.getenv("DB_PASS", "nav_password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "navoptima_warehouse")

DB_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

MLFLOW_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
EXPERIMENT_NAME = "NavOptima_Fuel_Prediction"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../../models"))
MODEL_JSON = os.path.join(MODEL_DIR, "xgb_navoptima_v1.json")
MODEL_PKL = os.path.join(MODEL_DIR, "xgb_navoptima_v1.pkl")

def get_training_data():
    """
    """
    print("🔌 Conectando al Data Warehouse...")
    engine = create_engine(DB_URI)
    
    query = """
    SELECT 
        f.sog_knots as sog,
        f.draft_m as draft,
        v.length_m as length,
        w.wind_speed_ms as wind_speed,
        w.wave_height_m as wave_height,
        f.fuel_consumption_kgh as fuel_consumption
    FROM gold_navoptima.fact_vessel_performance f
    JOIN gold_navoptima.dim_vessels v ON f.vessel_sk = v.vessel_sk
    JOIN gold_navoptima.dim_weather_metrics w ON f.weather_metric_id = w.weather_metric_id
    ORDER BY f.timestamp_utc ASC
    """
    
    print("📥 Ejecutando consulta SQL de extracción...")
    df = pd.read_sql(query, engine)
    print(f"📊 Datos extraídos: {len(df)} registros.")
    return df

def train_model():
    print(f"🚀 Iniciando Pipeline MLOps hacia {MLFLOW_URI}...")
    
    mlflow.set_tracking_uri(MLFLOW_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)
    
    df = get_training_data()
    if df.empty:
        raise ValueError("❌ La base de datos está vacía. Ejecuta loader.py primero.")

    X = df[['sog', 'draft', 'length', 'wind_speed', 'wave_height']]
    y = df['fuel_consumption']
    
    split_idx = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
    
    print(f"🧠 Entrenando con {len(X_train)} registros...")

    with mlflow.start_run(run_name="XGBoost_Production_Retrain"):
        
        params = {
            "n_estimators": 50,      
            "learning_rate": 0.05,   
            "max_depth": 3,          
            "random_state": 42,
            "n_jobs": -1
        }

        
        mlflow.log_params(params)
        
        model = xgb.XGBRegressor(**params)
        model.fit(X_train, y_train)
        
        predictions = model.predict(X_test)
        
        mse = mean_squared_error(y_test, predictions)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, predictions)
        
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2_score", r2)
        
        print(f"✅ Resultados: RMSE={rmse:.2f}, R2={r2:.2%}")
        
        mlflow.xgboost.log_model(model, "model")
        
        if not os.path.exists(MODEL_DIR):
            os.makedirs(MODEL_DIR)
            
        print(f"💾 Actualizando modelo para API en: {MODEL_JSON}")
        model.save_model(MODEL_JSON)
        joblib.dump(model, MODEL_PKL)

    print("✨ ¡Entrenamiento y Registro MLOps completado!")

if __name__ == "__main__":
    train_model()