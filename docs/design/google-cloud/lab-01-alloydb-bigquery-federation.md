# Laboratorio: Consultas Federadas con NavOptima en Google Cloud

## **Visión General**

Se explotará el poder de las consultas federadas para obtener insights en tiempo real conectando directamente desde la base de datos operativa (**AlloyDB**) desde el almacén de datos analítico (**BigQuery**).

Asi se va a demostrar la union de la **telemetría en tiempo real de los buques** (alojada en AlloyDB) con **datos históricos de mantenimiento y patrones climáticos** (alojados nativamente en BigQuery). Esto elimina la necesidad de pipelines ETL complejos para respuestas inmediatas.

Este ejercicio demuestra una capacidad clave del **NavOptima Lakehouse**: la habilidad de responder preguntas complejas como: *"¿El aumento de consumo de combustible del Buque 'A' se debe a la falta de limpieza del casco (Mantenimiento) o a que el oleaje actual es anómalamente alto comparado con el promedio de los últimos 10 años (Cambio Climático)?"*

---

## **Objetivos**

1. Crear una conexión a la instancia **NavOptima-Operational** (AlloyDB) desde BigQuery.
2. Otorgar permisos IAM para que BigQuery pueda "leer" los datos de telemetría.
3. Crear tablas analíticas de referencia (Mantenimiento y Clima Histórico) en BigQuery.
4. Escribir una consulta SQL usando `EXTERNAL_QUERY` para cruzar ambos mundos.

---

## **Paso 1: Crear la conexión a AlloyDB**

Se establecerá el puente seguro entre el mundo analítico y el operativo.

1. En la consola de Google Cloud, ir a **Menú de Navegación** > **BigQuery** > **Studio**.
2. Hacer clic en **+ AGREGAR (ADD DATA)**.
3. Seleccionar **Fuentes de datos externas (External data sources)**.
4. Eligir **Google Cloud AlloyDB**.
5. Configurar los siguientes valores (basados en tu arquitectura):
    * **Tipo de Conexión:** AlloyDB
    * **ID de Conexión:** `navoptima-alloydb-conn`
    * **Tipo de Ubicación:** Región (ej. `us-central1`)
    * **Nombre Amistoso:** `Conexión a Telemetría NavOptima`
    * **ID de Base de Datos:** `postgres` (Donde vive el esquema `gold_navoptima`)
    * **Instancia AlloyDB:** (Selecciona la instancia desplegada de NavOptima)
6. Hacer clic en **Crear conexión**.

---

## **Paso 2: Configurar Permisos IAM**

BigQuery necesita una "identidad" para entrar a AlloyDB.

1. En el panel explorador de BigQuery, expandir el proyecto y buscar **External Connections**.
2. Hacer clic en `navoptima-alloydb-conn`.
3. Copiar el **ID de la Cuenta de Servicio** que aparece en los detalles (ej: `...`).
4. Ir al menú **IAM y Administración** > **IAM**.
5. Hacer clic en **+ CONCEDER ACCESO (GRANT ACCESS)**.
6. Pegar la cuenta de servicio en "Nuevos principales".
7. Asignar los siguientes roles:
    * **AlloyDB Client** (Para conectar la base).
    * **BigQuery Connection User** (Para usar la conexión).
8. Haz clic en **Guardar**.

---

## **Paso 3: Preparar el Contexto Histórico en BigQuery**

Antes de federar, se necesita crear los datos "fríos" en BigQuery (Mantenimiento y Clima Histórico) para poder cruzarlos con la telemetría en vivo.

1. Abrir una nueva pestaña de consulta en **BigQuery Studio**.
2. Ejecutar el script `src/data_processor/gold/bigquery_analytics_schema.sql` para crear el dataset analítico y las tablas de contexto.
---

## **Paso 4: Ejecutar la Consulta Federada **

Ahora responder a la pregunta de negocio: **¿Por qué el consumo es alto actualmente?**
Para respodner a esta pregutna se desarrollara:

* 🔴 **AlloyDB:** Telemetría en vivo (`fact_vessel_performance` + `dim_weather_metrics`).
* 🔵 **BigQuery:** Historial de Mantenimiento + Línea base climática.

Copiar y ejecutar la siguiente consulta en BigQuery ubicada en `src/data_processor/gold/view_federated_fuel_analysis.sql`

---

## **Análisis de Resultados**

Al ejecutar la consulta, `se obtendrá una tabla unificada.

**Escenario de Ejemplo:**

* Si el `current_wave_height` (AlloyDB) es 3.0m, pero el `avg_historical` (BigQuery) es 2.5m, y el `hull_condition` es "Fouling Detected", el campo `root_cause_analysis` te dirá exactamente qué está pasando.

**Conclusión del Laboratorio:**
- Se ha logrado implementar una arquitectura **Data Lakehouse**. 
- No se tuvo que mover los gigabytes de datos históricos a AlloyDB (lo cual sería caro y lento), ni exportar la telemetría en tiempo real a BigQuery (lo cual tendría latencia). 
- Se unio uniste en el momento de la consulta para tomar decisiones tácticas inmediatas.