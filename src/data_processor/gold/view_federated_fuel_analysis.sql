-- Federated View: Real-time Operational Data (AlloyDB) + Historical Context (BigQuery)
-- Logic: Detect anomalies comparing Live Telemetry vs. 20-year Weather Baseline

CREATE OR REPLACE VIEW navoptima_analytics.view_fuel_efficiency_audit AS
SELECT 
    -- 1. Datos Vivos (Vienen de AlloyDB mediante Conexión Federada)
    live_data.mmsi,
    live_data.timestamp_utc,
    live_data.current_fuel_consumption,
    live_data.current_wave_height,
    live_data.speed_over_ground,
    
    -- 2. Contexto Mantenimiento (Nativo BigQuery)
    main.last_hull_cleaning,
    main.hull_condition_rating,
    DATE_DIFF(CURRENT_DATE(), main.last_hull_cleaning, DAY) as days_since_cleaning,

    -- 3. Contexto Climático (Nativo BigQuery)
    climate.avg_historical_wave_height,
    
    -- 4. Motor de Reglas (Business Logic)
    CASE 
        -- Si hay olas gigantes hoy vs el promedio histórico -> Culpa del Clima
        WHEN live_data.current_wave_height > (climate.avg_historical_wave_height * 1.5) 
            THEN 'EXTERNAL_FACTOR: Extreme Weather / Climate Change'
        
        -- Si el casco está sucio -> Culpa de Mantenimiento
        WHEN main.hull_condition_rating = 'Fouling Detected' 
             OR DATE_DIFF(CURRENT_DATE(), main.last_hull_cleaning, DAY) > 180
            THEN 'INTERNAL_FACTOR: Hull Fouling / Maintenance Required'
            
        ELSE 'NORMAL_OPERATION'
    END as root_cause_analysis

FROM 
    -- CONSULTA EXTERNA A ALLOYDB (PostgreSQL)
    -- Ajustar 'TU_PROYECTO' y región al desplegar
    EXTERNAL_QUERY("projects/TU_PROYECTO/locations/us-central1/connections/navoptima-alloydb-conn",
        '''
        SELECT 
            v.mmsi, 
            f.timestamp_utc, 
            f.fuel_consumption_kgh as current_fuel_consumption, 
            w.wave_height_m as current_wave_height,
            f.sog_knots as speed_over_ground
        FROM gold_navoptima.fact_vessel_performance f
        JOIN gold_navoptima.dim_vessels v ON f.vessel_sk = v.vessel_sk
        JOIN gold_navoptima.dim_weather_metrics w ON f.weather_metric_id = w.weather_metric_id
        WHERE f.timestamp_utc >= NOW() - INTERVAL '2 hours'
        '''
    ) as live_data

-- Cruce con tablas de BigQuery
LEFT JOIN navoptima_analytics.vessel_maintenance_log main 
    ON live_data.mmsi = main.mmsi

CROSS JOIN navoptima_analytics.historical_climate_baseline climate 
WHERE climate.month = EXTRACT(MONTH FROM CURRENT_DATE())
  AND climate.region_code = 'PACIFIC_SOUTH'; -- Se podría parametrizar según lat/lon del barco