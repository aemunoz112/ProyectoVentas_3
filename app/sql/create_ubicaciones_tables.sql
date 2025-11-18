-- Script SQL para crear las tablas de departamentos y ciudades
-- Ejecuta este script en tu base de datos MySQL

-- Tabla de departamentos
CREATE TABLE IF NOT EXISTS departamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    estado VARCHAR(20) DEFAULT 'Activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_nombre (nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de ciudades
CREATE TABLE IF NOT EXISTS ciudades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    departamento_id INT NOT NULL,
    estado VARCHAR(20) DEFAULT 'Activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (departamento_id) REFERENCES departamentos(id) ON DELETE CASCADE,
    UNIQUE KEY unique_nombre_departamento (nombre, departamento_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Índices para mejorar el rendimiento
CREATE INDEX idx_departamentos_estado ON departamentos(estado);
CREATE INDEX idx_ciudades_departamento ON ciudades(departamento_id);
CREATE INDEX idx_ciudades_estado ON ciudades(estado);

-- Datos de ejemplo (opcional - descomenta si quieres datos iniciales)
/*
-- Ejemplo de departamentos
INSERT INTO departamentos (nombre, estado) VALUES
('Antioquia', 'Activo'),
('Cundinamarca', 'Activo'),
('Valle del Cauca', 'Activo'),
('Atlántico', 'Activo'),
('Santander', 'Activo');

-- Ejemplo de ciudades
INSERT INTO ciudades (nombre, departamento_id, estado) VALUES
('Medellín', 1, 'Activo'),
('Bello', 1, 'Activo'),
('Itagüí', 1, 'Activo'),
('Bogotá', 2, 'Activo'),
('Soacha', 2, 'Activo'),
('Cali', 3, 'Activo'),
('Palmira', 3, 'Activo'),
('Barranquilla', 4, 'Activo'),
('Soledad', 4, 'Activo'),
('Bucaramanga', 5, 'Activo'),
('Floridablanca', 5, 'Activo');
*/

