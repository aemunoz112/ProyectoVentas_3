-- Estructura para menú jerárquico dinámico (hasta 5 niveles)

CREATE TABLE IF NOT EXISTS menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    modulo_id INT NULL,
    parent_id INT NULL,
    nombre VARCHAR(150) NOT NULL,
    descripcion VARCHAR(255) NULL,
    ruta VARCHAR(255) NULL,
    icono VARCHAR(64) NULL,
    tipo VARCHAR(50) NOT NULL DEFAULT 'pagina',
    nivel INT NOT NULL DEFAULT 1,
    orden INT NOT NULL DEFAULT 0,
    estado VARCHAR(20) NOT NULL DEFAULT 'Activo',
    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_menu_items_modulos FOREIGN KEY (modulo_id) REFERENCES modulos(id) ON DELETE SET NULL,
    CONSTRAINT fk_menu_items_parent FOREIGN KEY (parent_id) REFERENCES menu_items(id) ON DELETE CASCADE,
    /*!80016 CONSTRAINT chk_menu_items_nivel CHECK (nivel BETWEEN 1 AND 5) */
);

CREATE INDEX idx_menu_items_parent ON menu_items(parent_id);
CREATE INDEX idx_menu_items_nivel ON menu_items(nivel);

CREATE TABLE IF NOT EXISTS menu_itemXrol (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rol_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    puede_ver TINYINT(1) NOT NULL DEFAULT 1,
    puede_crear TINYINT(1) NOT NULL DEFAULT 0,
    puede_editar TINYINT(1) NOT NULL DEFAULT 0,
    puede_eliminar TINYINT(1) NOT NULL DEFAULT 0,
    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_menuXrol_rol FOREIGN KEY (rol_id) REFERENCES roles(id) ON DELETE CASCADE,
    CONSTRAINT fk_menuXrol_menu FOREIGN KEY (menu_item_id) REFERENCES menu_items(id) ON DELETE CASCADE,
    CONSTRAINT uk_menuXrol UNIQUE (rol_id, menu_item_id)
);

-- Datos base sugeridos para módulos raíz (ajustar según catálogo actual)
INSERT INTO menu_items (modulo_id, parent_id, nombre, descripcion, ruta, icono, tipo, nivel, orden, estado)
VALUES
    (NULL, NULL, 'Comercial', 'Módulo Comercial', '/ventas', '💼', 'modulo', 1, 1, 'Activo'),
    (NULL, NULL, 'Inventario', 'Módulo de Inventario', '/productos', '📦', 'modulo', 1, 2, 'Activo'),
    (NULL, NULL, 'Producción', 'Módulo de Producción', '/produccion', '🏭', 'modulo', 1, 3, 'Activo'),
    (NULL, NULL, 'Logística', 'Módulo de Logística', '/logistica', '🚚', 'modulo', 1, 4, 'Activo'),
    (NULL, NULL, 'Administración del Sistema', 'Configuración avanzada', '/roles', '⚙️', 'modulo', 1, 5, 'Activo')
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre);

