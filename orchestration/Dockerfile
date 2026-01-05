FROM python:3.10-slim

WORKDIR /app

# Instalación de dependencias del sistema operativo
# AGREGADO: 'git' para evitar el warning de MLflow
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    netcat-openbsd \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Instalación de librerías de Python
# MODIFICADO: mlflow==2.10.2 para coincidir con el servidor
RUN pip install --no-cache-dir \
    pandas \
    numpy \
    sqlalchemy \
    psycopg2-binary \
    xgboost \
    scikit-learn \
    joblib \
    xarray \
    netCDF4 \
    fastapi \
    uvicorn \
    pydantic \
    mlflow==2.10.2

# El código se monta mediante volúmenes