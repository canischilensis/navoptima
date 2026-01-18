-- Crear Dataset Analítico en BigQuery
CREATE SCHEMA IF NOT EXISTS navoptima_analytics;

-- 1. Tabla de Historial de Mantenimiento (Datos Fríos)
-- Se registra cuándo fue la última vez que se limpió el casco o se revisó el motor.
CREATE TABLE navoptima_analytics.vessel_maintenance_log (
    mmsi INT64,
    last_hull_cleaning DATE,
    last_engine_overhaul DATE,
    hull_condition_rating STRING -- 'Excellent', 'Good', 'Fouling Detected'
);

-- Se inserta datos de prueba para el barco con MMSI 123456789
INSERT INTO navoptima_analytics.vessel_maintenance_log 
VALUES (123456789, '2025-06-15', '2024-12-01', 'Fouling Detected'); 
-- Nota: 'Fouling Detected' implica que el casco está sucio, aumentando la fricción.

-- 2. Tabla de Clima Histórico (Referencia de Cambio Climático)
-- Promedios de oleaje para esta región en los últimos 20 años.
CREATE TABLE navoptima_analytics.historical_climate_baseline (
    month INT64,
    region_code STRING,
    avg_historical_wave_height FLOAT64, -- Promedio histórico
    avg_historical_wind_speed FLOAT64
);

-- Se Inserta la base climática de Enero (Mes 1)
INSERT INTO navoptima_analytics.historical_climate_baseline
VALUES (1, 'PACIFIC_SOUTH', 2.5, 8.0); 