# **🧭 NavOptima: Plataforma de Ingeniería de Datos y MLOps para Eficiencia de Combustible**

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Container-blue?style=for-the-badge&logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Postgres](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-Model-red?style=for-the-badge&logo=xgboost&logoColor=white)
![MLflow](https://img.shields.io/badge/MLflow-Tracking-blue?style=for-the-badge&logo=mlflow&logoColor=white)
![Airflow](https://img.shields.io/badge/Apache%20Airflow-Orchestration-blue?style=for-the-badge&logo=apache-airflow&logoColor=white)

## **Copyright & License / Licencia**

**Copyright (c) [2026]. Todos los derechos reservados.**

Este proyecto es propietario y confidencial. Queda estrictamente prohibida la copia, distribución, modificación o uso no autorizado de este código fuente. Este repositorio es únicamente con fines de demostración o portafolio profesional.

---

## **📝 Resumen del Proyecto**

**NavOptima** es una plataforma de inteligencia operativa y **MLOps** diseñada para procesar telemetría marítima y variables climáticas masivas. Su objetivo principal es optimizar el consumo de combustible de la flota mediante el uso de **Gemelos Digitales** y modelos predictivos de alta precisión.

El sistema implementa una arquitectura **Lakehouse** que transforma señales de posicionamiento (AIS) y datos meteorológicos (ERA5) en decisiones financieras auditables, permitiendo monitorear la eficiencia energética en tiempo real.

## **🏗️ Arquitectura del Sistema (Medallion + MLOps)**

La arquitectura sigue el patrón **Medallion (Bronze-Silver-Gold)** orquestado completamente por Docker Compose y Apache Airflow.

```mermaid
graph LR
    A[Fuentes: AIS + ERA5] -->|Ingesta Batch (Airflow)| B(Ingestion Worker - Python)
    B -->|Limpieza & Validación| C[(PostgreSQL DW - Capa Silver)]
    C -->|Agregación SCD2| D[(Capa Gold - Analítica)]
    D -->|Entrenamiento| E{ML Engine - MLflow}
    E -->|Modelo Versionado| F[Inference API - FastAPI]
    F -->|Predicción Real-Time| G[Dashboard Power BI]

```

### Flujo de Datos

1. **Capa Bronze (Ingesta):** Ingesta idempotente de archivos AIS y Clima.
2. **Capa Silver (Procesamiento):** Validación de esquemas con **Pydantic** y enriquecimiento espacio-temporal.
3. **Capa Gold (Analítica & ML):** Tablas con **SCD Tipo 2** para auditoría histórica y datasets de entrenamiento.
4. **Serving:** API REST que descarga dinámicamente modelos desde el **Model Registry** de MLflow.

## **🛠️ Pila Tecnológica (Tech Stack)**

| Categoría | Tecnologías | Función Principal |
| --- | --- | --- |
| **Orquestación** | **Apache Airflow** | Gestión de pipelines ETL y dependencias. |
| **Backend** | **FastAPI** | API de inferencia de alta velocidad. |
| **MLOps** | **MLflow** | Experiment Tracking & Model Registry. |
| **Data Warehouse** | **PostgreSQL 16** | Arquitectura 3FN/Estrella con PostGIS. |
| **Modelado ML** | **XGBoost** | Regresión no lineal para consumo de combustible. |
| **Visualización** | **Power BI** | Dashboards ejecutivos. |

## **🚀 Guía de Inicio Rápido (Getting Started)**

### 1. Requisitos Previos

* Docker Desktop & Docker Compose.
* Git.
* Python 3.10+ (opcional para desarrollo local).

### 2. Despliegue de Infraestructura

Levantar todo el stack (Airflow, DB, MLflow, API) con un solo comando:

```bash
cd orchestration
docker compose up -d --build

```

### 3. Acceso a Servicios

Una vez desplegados los contenedores, accede a las interfaces:

* **API de Inferencia (Swagger):** `http://localhost:8000/docs`
* **MLflow UI (Tracking):** `http://localhost:5000`
* **Airflow UI (Pipelines):** `http://localhost:8080`

## **📊 Modelo de Datos & ML**

El núcleo analítico está diseñado para soportar auditoría financiera:

* **`fact_vessel_performance`**: Tabla central de hechos. Métricas físicas y financieras.
* **`dim_vessels`**: Dimensión con **SCD Tipo 2** para trazabilidad de cambios en la flota.
* **Modelo XGBoost:** Entrenado con features de Velocidad, Calado, Viento y Olas, logrando un RMSE de ~2.73 kg/h en pruebas.

## **📂 Estructura del Proyecto**

```text
navoptima/
├── data/                  # Data Lake local (Raw, Processed)
├── docs/                  # Documentación (ADR, DDL, Arquitectura)
├── notebooks/             # EDA y Prototipado (Jupyter)
├── orchestration/         # Docker Compose, Airflow DAGs y Dockerfiles
├── src/                   # Código Fuente Modular
│   ├── ingestion_worker   # Extracción (Capa Bronze)
│   ├── data_processor     # Transformación ETL (Capa Silver/Gold)
│   ├── ml_engine          # Entrenamiento (MLflow) y Serving (FastAPI)
│   └── shared             # Schemas Pydantic y utilidades comunes
└── README.md              # Documentación principal

```