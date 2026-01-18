SELECT 
    -- Datos del Barco (Vienen de AlloyDB)
    live_data.mmsi,
    live_data.timestamp_utc,
    live_data.current_fuel_consumption,
    live_data.current_wave_height,
    
    -- Contexto de Mantenimiento (Viene de BigQuery)
    main.last_hull_cleaning,
    main.hull_condition_rating,
    DATE_DIFF(CURRENT_DATE(), main.last_hull_cleaning, DAY) as days_since_cleaning,

    -- Contexto Climático Histórico (Viene de BigQuery)
    climate.avg_historical_wave_height,
    
    -- ANÁLISIS AUTOMÁTICO (Business Logic)
    CASE 
        WHEN live_data.current_wave_height > (climate.avg_historical_wave_height * 1.5) THEN 'ALERTA: Clima Extremo (Cambio Climático)'
        WHEN main.hull_condition_rating = 'Fouling Detected' THEN 'ALERTA: Casco Sucio (Requiere Limpieza)'
        ELSE 'Operación Normal'
    END as root_cause_analysis

FROM 
    -- 1. LA CONSULTA FEDERADA A ALLOYDB (Operativa)
    -- Usamos EXTERNAL_QUERY para pedirle a Postgres solo lo que necesitamos
    EXTERNAL_QUERY("projects/TU_PROYECTO/locations/TU_REGION/connections/navoptima-alloydb-conn",
        '''
        SELECT 
            v.mmsi, 
            f.timestamp_utc, 
            f.fuel_consumption_kgh as current_fuel_consumption,
            w.wave_height_m as current_wave_height,
            f.sog_knots
        FROM gold_navoptima.fact_vessel_performance f
        JOIN gold_navoptima.dim_vessels v ON f.vessel_sk = v.vessel_sk
        JOIN gold_navoptima.dim_weather_metrics w ON f.weather_metric_id = w.weather_metric_id
        WHERE f.timestamp_utc > NOW() - INTERVAL '1 hour' -- Solo última hora
        '''
    ) as live_data

-- 2. JOIN con Mantenimiento (BigQuery)
LEFT JOIN navoptima_analytics.vessel_maintenance_log main 
    ON live_data.mmsi = main.mmsi

-- 3. JOIN con Clima Histórico (BigQuery) - Asumiendo Enero y Región Pacífico
CROSS JOIN navoptima_analytics.historical_climate_baseline climate
WHERE climate.month = 1 AND climate.region_code = 'PACIFIC_SOUTH';