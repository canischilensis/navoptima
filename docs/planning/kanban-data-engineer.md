# 📋 KANBAN NAVOPTIMA: Roadmap de Ingeniería & MLOps

### ✅ COLUMNA: DONE (Implementado & Desplegado)
*El MVP funcional que ya reside en tu repositorio.*

| Tarjeta | Estado | Entregable | Logros Técnicos |
| :--- | :--- | :--- | :--- |
| **Tarjeta 1: Infraestructura como Código (Docker)** | Completado | `docker-compose.yml` funcional | <ul><li>[x] Contenerización de servicios: Airflow, Postgres, MLflow, FastAPI.</li><li>[x] Definición de redes internas (`navoptima_network`) para seguridad entre contenedores.</li><li>[x] Persistencia de datos mediante Docker Volumes.</li></ul> |
| **Tarjeta 2: Orquestación de Datos (Airflow)** | Completado | DAGs de Ingesta y Re-entrenamiento | <ul><li>[x] Implementación de patrón Strategy para ingesta desacoplada.</li><li>[x] Pipeline automatizado: Ingesta -> Procesamiento -> Carga en DB (Gold).</li><li>[x] Manejo de dependencias y reintentos automáticos.</li></ul> |
| **Tarjeta 3: Gobierno de Modelos (MLflow)** | Completado | Servidor de Tracking y Model Registry | <ul><li>[x] Entrenamiento de modelo XGBoost con registro de métricas ($R^2$, RMSE).</li><li>[x] Versionado de modelos (v1, v2) y asignación de Stages (Staging/Production).</li><li>[x] Trazabilidad de hiperparámetros.</li></ul> |
| **Tarjeta 4: API de Inferencia (Serving)** | Completado | Microservicio `fastapi_app` | <ul><li>[x] Endpoint `/predict` recibiendo JSON y retornando predicción + confianza.</li><li>[x] Integración dinámica: La API descarga el modelo "Production" desde MLflow al iniciar.</li><li>[x] Documentación automática con Swagger UI.</li></ul> |
| **Tarjeta 5: Diseño de Arquitectura (ADR & Diagramas)** | Completado | README.md y Diagramas | <ul><li>[x] Definición de Arquitectura Medallion (Bronze/Silver/Gold).</li><li>[x] Modelo de Datos Relacional con soporte SCD Tipo 2 (Auditabilidad).</li></ul> |

---

### 🚧 COLUMNA: IN PROGRESS (Afinando Detalles)
*Lo que estás puliendo esta semana para la presentación.*

| Tarjeta | Prioridad | Acción | Criterios de Aceptación |
| :--- | :--- | :--- | :--- |
| **Tarjeta 6: Visualización de Negocio (Power BI)** | Alta | Conectar Power BI a PostgreSQL y generar Dashboard | <ul><li>[ ] Gráfico de dispersión: Curva teórica vs. Real vs. Predicción AI.</li><li>[ ] KPIs financieros: Costo total de combustible y Ahorro potencial.</li><li>[ ] Filtros dinámicos por fecha y barco.</li></ul> |
| **Tarjeta 7: Estrategia de Difusión (LinkedIn)** | Alta | Generar los activos de marketing personal | <ul><li>[ ] Crear Carrusel PDF "Problema vs Solución".</li><li>[ ] Grabar GIF/Video demostrativo de `docker up` y predicción de API.</li><li>[ ] Redactar posts siguiendo la estrategia de storytelling.</li></ul> |

---

### 📋 COLUMNA: BACKLOG (To Do - Próximos Pasos Senior)
*Tareas para llevar el proyecto de "MVP" a "Production Grade Enterprise".*

| Tarjeta | Etiqueta | Acción | Criterios de Aceptación |
| :--- | :--- | :--- | :--- |
| **Tarjeta 8: Calidad de Datos (Great Expectations / Soda)** | Data Quality | Implementar "Circuit Breakers" en el pipeline de Airflow | <ul><li>[ ] El pipeline se detiene si más del 5% de los datos de velocidad son nulos o negativos.</li><li>[ ] Validación de esquema estricto antes de entrar a la capa Silver.</li></ul> |
| **Tarjeta 9: Testing Automatizado (Pytest)** | QA Engineering | Crear suite de tests unitarios y de integración | <ul><li>[ ] **Unit Test:** Probar que la función de "Resistencia del Viento" calcula correctamente según la fórmula física.</li><li>[ ] **Integration Test:** Verificar que la API responde 200 OK cuando MLflow está arriba.</li><li>[ ] **Data Drift Test:** Alerta si la distribución de datos de entrada cambia significativamente (ej. climas nunca vistos).</li></ul> |
| **Tarjeta 10: CI/CD Pipelines (GitHub Actions)** | DevOps | Automatizar el despliegue al hacer push a `main` | <ul><li>[ ] Pipeline que ejecuta `pytest` automáticamente en cada Pull Request.</li><li>[ ] Construcción y subida automática de imágenes Docker a Docker Hub o AWS ECR.</li></ul> |
| **Tarjeta 11: Despliegue en Cloud (AWS/Azure/GCP)** | Infrastructure | Mover el proyecto de `localhost` a la nube (Capa gratuita) | <ul><li>[ ] Desplegar la API en un servicio Serverless (Cloud Run o Azure Container Apps).</li><li>[ ] Mover la base de datos a un servicio gestionado (RDS o Cloud SQL) o mantenerla en contenedor con volumen persistente en nube.</li></ul> |