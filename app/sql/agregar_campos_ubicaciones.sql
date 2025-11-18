-- Script para agregar campos de ubicación a las tablas existentes
-- Estos campos almacenarán los IDs de departamentos y ciudades que vienen de la API externa

-- Agregar campos a la tabla usuarios
ALTER TABLE usuarios 
ADD COLUMN IF NOT EXISTS departamento_id INT NULL,
ADD COLUMN IF NOT EXISTS ciudad_id INT NULL;

-- Agregar campos a la tabla encabezado_pedidos (si es donde guardas las ventas)
ALTER TABLE encabezado_pedidos 
ADD COLUMN IF NOT EXISTS departamento_id INT NULL,
ADD COLUMN IF NOT EXISTS ciudad_id INT NULL;

-- Nota: Si tienes otras tablas donde necesites estos campos, agrega más ALTER TABLE aquí
-- Ejemplo:
-- ALTER TABLE otra_tabla 
-- ADD COLUMN IF NOT EXISTS departamento_id INT NULL,
-- ADD COLUMN IF NOT EXISTS ciudad_id INT NULL;

-- Los campos son NULL porque son opcionales y se llenarán con datos de la API externa

