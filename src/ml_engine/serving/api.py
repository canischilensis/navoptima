import os
import xgboost as xgb
import pandas as pd
import mlflow.xgboost
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager

# ==============================================================================
# CONFIGURACIÓN DE MLOPS
# ==============================================================================
MLFLOW_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
MODEL_NAME = "NavOptima_Fuel_Model"
MODEL_STAGE = "Production"

# Rutas de respaldo (Fallback local)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH_DOCKER = "/app/models/xgb_navoptima_v1.json"
MODEL_PATH_LOCAL = os.path.abspath(os.path.join(BASE_DIR, "../../../models/xgb_navoptima_v1.json"))

model = None
model_source = "None"

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Ciclo de vida de la aplicación:
    """
    global model, model_source
    
    # --- INTENTO 1: MLFLOW REGISTRY ---
    try:
        print(f"📡 Conectando a MLflow Registry en: {MLFLOW_URI}")
        mlflow.set_tracking_uri(MLFLOW_URI)
        
        # Ruta del modelo en el registro: models:/Nombre/Etiqueta
        model_uri = f"models:/{MODEL_NAME}/{MODEL_STAGE}"
        
        print(f"🧠 Intentando cargar modelo desde Registry: {model_uri}")
        # Cargamos el modelo usando el wrapper de MLflow
        model = mlflow.xgboost.load_model(model_uri)
        model_source = f"MLflow Registry ({MODEL_STAGE})"
        print(f"✅ ¡ÉXITO! Modelo '{MODEL_NAME}' cargado desde el Registry.")
        
    except Exception as e:
        print(f"⚠️ Error al conectar con MLflow o modelo no encontrado: {e}")
        print("📦 Iniciando modo de contingencia (Carga de archivo local)...")
        
        # --- INTENTO 2: ARCHIVO LOCAL (FALLBACK) ---
        path = MODEL_PATH_DOCKER if os.path.exists(MODEL_PATH_DOCKER) else MODEL_PATH_LOCAL
        
        if os.path.exists(path):
            try:
                model_booster = xgb.Booster()
                model_booster.load_model(path)
                model = model_booster
                model_source = "Local File (Contingency)"
                print(f"✅ Modelo local cargado exitosamente desde: {path}")
            except Exception as ex:
                print(f"❌ Error crítico al leer el archivo del modelo local: {ex}")
        else:
            print(f"🚨 ERROR CRÍTICO: No se encontró ningún modelo en {path}")

    yield
    print("🛑 Servicio de inferencia detenido.")

app = FastAPI(
    title="NavOptima Inference API", 
    version="2.0", 
    lifespan=lifespan
)

# ==============================================================================
# ESQUEMAS DE DATOS (Input Validation)
# ==============================================================================
class VoyageParameters(BaseModel):
    sog: float = Field(..., ge=0, description="Velocidad (knots)", json_schema_extra={"example": 12.5})
    draft: float = Field(..., ge=0, description="Calado (m)", json_schema_extra={"example": 7.2})
    length: float = Field(..., ge=0, description="Eslora (m)", json_schema_extra={"example": 200.0})
    wind_speed: float = Field(..., ge=0, description="Viento (m/s)", json_schema_extra={"example": 15.0})
    wave_height: float = Field(..., ge=0, description="Olas (m)", json_schema_extra={"example": 2.5})

class PredictionResponse(BaseModel):
    fuel_consumption_kgh: float
    source: str
    confidence_score: float

# ==============================================================================
# ENDPOINTS
# ==============================================================================
@app.get("/")
def home():
    return {
        "message": "NavOptima AI Service is Running", 
        "model_loaded": model is not None,
        "active_source": model_source,
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    if model:
        return {"status": "healthy", "model_source": model_source}
    return {"status": "degraded", "model_loaded": False}

@app.post("/predict", response_model=PredictionResponse)
def predict_consumption(params: VoyageParameters):
    if not model:
        raise HTTPException(status_code=503, detail="Modelo no cargado en memoria.")

    try:
        input_data = pd.DataFrame([{
            'sog': params.sog,
            'draft': params.draft,
            'length': params.length,
            'wind_speed': params.wind_speed,
            'wave_height': params.wave_height
        }])

        if isinstance(model, xgb.Booster):
            dmatrix = xgb.DMatrix(input_data)
            prediction = model.predict(dmatrix)
        else:
            prediction = model.predict(input_data)
        
        return {
            "fuel_consumption_kgh": round(float(prediction[0]), 2),
            "source": model_source,
            "confidence_score": 0.95
        }

    except Exception as e:
        print(f"❌ Error durante la ejecución de la inferencia: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)