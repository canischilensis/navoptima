# **🧭 NavOptima: Plataforma de Ingeniería de Datos y MLOps para Eficiencia de Combustible**

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Container-blue?style=for-the-badge&logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Postgres](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626.svg?style=for-the-badge&logo=Jupyter&logoColor=white)
![Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)
![Power Bi](https://img.shields.io/badge/power_bi-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Spark](https://img.shields.io/badge/Apache%20Spark-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white)
![Delta Lake](https://img.shields.io/badge/Delta%20Lake-black?style=for-the-badge&logo=deltalake&logoColor=white)
![Amazon S3](https://img.shields.io/badge/Amazon%20S3-569A31?style=for-the-badge&logo=amazons3&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Kubernetes](https://img.shields.io/badge/kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)

## **Copyright & License / Licencia y Derechos de Autor**

**Copyright (c) \[2026\]. All Rights Reserved.**

### **English**

This project is proprietary and confidential. Unauthorized copying, distribution, modification, or use of this source code or any associated files, via any medium, is strictly prohibited. This repository is for portfolio/demonstration purposes only.

### **Español**

Copyright (c) \[2026\]. Todos los derechos reservados.

Este proyecto es propietario y confidencial. Queda estrictamente prohibida la copia, distribución, modificación o uso no autorizado de este código fuente o cualquiera de sus archivos asociados. Este repositorio es únicamente con fines de demostración o portafolio profesional.

## **📝 Resumen del Proyecto**

**NavOptima** es una plataforma de inteligencia operativa y **MLOps** diseñada para procesar telemetría marítima y variables climáticas masivas. Su objetivo principal es optimizar el consumo de combustible de la flota mediante el uso de **Gemelos Digitales** y modelos predictivos de alta precisión.

El sistema transforma señales de posicionamiento (AIS) y datos meteorológicos (ERA5) en decisiones financieras auditables, permitiendo a la organización monitorear la eficiencia energética en tiempo real a través de una arquitectura **Lakehouse** contenerizada.

## **🏗️ 1\. Arquitectura del Sistema (Medallion \+ MLOps Lifecycle)**

La arquitectura sigue el patrón **Medallion (Bronze-Silver-Gold)** integrado con un ciclo de vida de Machine Learning moderno:

1. **Capa Bronze (Ingesta):** Ingesta idempotente de archivos AIS, Clima y precios de mercado.  
2. **Capa Silver (Procesamiento):** Limpieza, validación de esquemas con **Pydantic** y enriquecimiento espacio-temporal.  
3. **Capa Gold (Analítica & ML):** Tablas agregadas para Power BI y datasets de entrenamiento.  
4. **ML Engine (MLOps):** Entrenamiento de modelos **XGBoost** con tracking completo en **MLflow**.  
5. **Serving (Inferencia):** API REST con **FastAPI** que descarga dinámicamente modelos desde el **Model Registry**.

## **🎯 2\. Objetivos Técnicos y de Negocio**

* **📊 Auditoría Financiera:** Implementación de **SCD Tipo 2 (Slowly Changing Dimensions)** para garantizar que cada predicción de costo sea históricamente reproducible.  
* **⚙️ Orquestación con Airflow:** Automatización total de los pipelines ETL y ciclos de re-entrenamiento, minimizando la intervención manual y la entropía operativa.  
* **🧠 Gobierno de Modelos (MLflow):** Gestión centralizada de experimentos, parámetros, métricas y versionado de modelos (Stages: Staging, Production, Archived).  
* **🛡️ Infraestructura Inmutable:** Despliegue mediante **Docker Compose**, asegurando que el entorno de desarrollo sea idéntico al de producción.

## **🛠️ 3\. Pila Tecnológica (Tech Stack)**

| Categoría | Tecnologías |
| :---- | :---- |
| **Orquestación** | **Apache Airflow** (Gestión de pipelines y dependencias) |
| **Backend & Serving** | **FastAPI**, Uvicorn (Inferencia de alta velocidad) |
| **MLOps & Tracking** | **MLflow** (Experiment Tracking & Model Registry) |
| **Data Warehouse** | **PostgreSQL 16** (Arquitectura Gold / Relacional) |
| **Modelado ML** | **XGBoost**, Scikit-Learn (Regresión no lineal) |
| **Contenedores** | **Docker & Docker Compose** (Microservicios) |

## **🚀 4\. Cómo Empezar (Getting Started)**

### **4.1. Prerrequisitos**

* Docker & Docker Compose instalados.  
* Python 3.10+.

### **4.2. Despliegue de Infraestructura**

El proyecto está completamente orquestado. Para levantar el stack de datos (DB, Airflow, MLflow, API):

cd orchestration  
docker-compose up \-d \--build

### **4.3. Acceso a Servicios**

* **API de Inferencia:** http://localhost:8000/docs  
* **MLflow UI:** http://localhost:5000  
* **Airflow UI:** http://localhost:8080

## **📂 5\. Estructura del Proyecto**
```bash
navoptima/  
├── src/  
│   ├── ingestion\_worker/ \# Extracción (Capa Bronze)  
│   ├── data\_processor/  \# Transformación (Capa Silver)  
│   ├── ml\_engine/       \# Entrenamiento (MLflow) y Serving (FastAPI)  
│   └── shared/          \# Modelos de datos compartidos (Pydantic)  
├── orchestration/       \# Dockerfiles, DAGs de Airflow y docker-compose  
├── docs/                \# Whitepapers y diagramas de arquitectura  
└── notebooks/           \# EDA (Exploratory Data Analysis) inicial
```

## **📄 6\. Licencia**

Este proyecto se distribuye bajo términos propietarios de portafolio profesional. Para consultas sobre el uso de la arquitectura, contactar a: **guillermo.vidal.astudillo@gmail.com**.
