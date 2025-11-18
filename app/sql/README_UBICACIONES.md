# Scripts SQL para Ubicaciones

## Instalación

Ejecuta el script `create_ubicaciones_tables.sql` en tu base de datos MySQL para crear las tablas necesarias:

```bash
mysql -u root -p railway < app/sql/create_ubicaciones_tables.sql
```

O desde MySQL Workbench o cualquier cliente MySQL, ejecuta el contenido del archivo.

## Estructura de Tablas

### Tabla: `departamentos`
- `id`: INT (AUTO_INCREMENT, PRIMARY KEY)
- `nombre`: VARCHAR(100) NOT NULL
- `estado`: VARCHAR(20) DEFAULT 'Activo'
- `created_at`: TIMESTAMP
- `updated_at`: TIMESTAMP

### Tabla: `ciudades`
- `id`: INT (AUTO_INCREMENT, PRIMARY KEY)
- `nombre`: VARCHAR(100) NOT NULL
- `departamento_id`: INT NOT NULL (FOREIGN KEY a departamentos)
- `estado`: VARCHAR(20) DEFAULT 'Activo'
- `created_at`: TIMESTAMP
- `updated_at`: TIMESTAMP

## Relaciones

- Una ciudad pertenece a un departamento (relación muchos a uno)
- Si se elimina un departamento, se eliminan sus ciudades (CASCADE)

## Notas

- El script incluye datos de ejemplo comentados que puedes descomentar si necesitas datos iniciales
- Los índices están optimizados para consultas por estado y por departamento
- Los nombres de departamentos son únicos
- Los nombres de ciudades son únicos dentro de cada departamento

