-- 1. Crear Dataset Analítico
CREATE SCHEMA IF NOT EXISTS navoptima_analytics;

-- 2. Tabla de Historial de Mantenimiento (Datos Fríos)
-- Fuente: CSVs históricos o ingresos manuales del equipo de mantenimiento
CREATE TABLE IF NOT EXISTS navoptima_analytics.vessel_maintenance_log (
    mmsi INT64,
    last_hull_cleaning DATE,
    last_engine_overhaul DATE,
    hull_condition_rating STRING -- 'Excellent', 'Good', 'Fouling Detected'
    maintenance_provider STRING
);

-- 3. Tabla de Clima Histórico (Referencia de Cambio Climático)
-- Fuente: NOAA / ECMWF (Promedios de 20 años)
CREATE TABLE IF NOT EXISTS navoptima_analytics.historical_climate_baseline (
    month INT64,
    region_code STRING, -- ej: 'PACIFIC_SOUTH'
    avg_historical_wave_height FLOAT64,
    avg_historical_wind_speed FLOAT64,
    extreme_weather_threshold_waves FLOAT64 -- Umbral para alertas
);