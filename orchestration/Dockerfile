FROM python:3.10-slim

WORKDIR /app

# Instalación de dependencias del sistema operativo
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Instalación de librerías de Python
RUN pip install --no-cache-dir \
    pandas \
    numpy \
    sqlalchemy \
    psycopg2-binary \
    xgboost \
    xarray \
    netCDF4 \
    fastapi \
    uvicorn \
    pydantic