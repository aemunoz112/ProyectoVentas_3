# Integración de API de Departamentos y Ciudades - Backend

## ⚠️ IMPORTANTE: Base de Datos Separada

Este sistema está configurado para usar una **base de datos separada** para departamentos y ciudades. Si ya tienes una BD con estos datos, debes configurar la conexión en `app/config/db_config.py`.

**Ver la guía completa de configuración en:** `CONFIGURACION_BD_UBICACIONES.md`

## ✅ Archivos Creados

### Modelos
- `app/models/departamento_model.py` - Modelo Pydantic para Departamentos
- `app/models/ciudad_model.py` - Modelo Pydantic para Ciudades

### Controladores
- `app/controllers/departamento_controller.py` - Lógica de negocio para Departamentos
- `app/controllers/ciudad_controller.py` - Lógica de negocio para Ciudades

### Rutas
- `app/routes/departamento_routes.py` - Endpoints REST para Departamentos
- `app/routes/ciudad_routes.py` - Endpoints REST para Ciudades

### Scripts SQL
- `app/sql/create_ubicaciones_tables.sql` - Script para crear las tablas en MySQL
- `app/sql/README_UBICACIONES.md` - Documentación de las tablas

### Archivos Actualizados
- `app/main.py` - Agregadas las rutas de departamentos y ciudades

## 📋 Endpoints Disponibles

### Departamentos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/departamentos/` | Lista todos los departamentos |
| GET | `/departamentos/activos/` | Lista solo departamentos activos |
| GET | `/departamentos/{id}` | Obtiene un departamento por ID |
| POST | `/departamentos/` | Crea un nuevo departamento |
| PUT | `/departamentos/{id}` | Actualiza un departamento |
| DELETE | `/departamentos/{id}` | Elimina un departamento |

### Ciudades

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/ciudades/` | Lista todas las ciudades |
| GET | `/ciudades/{id}` | Obtiene una ciudad por ID |
| GET | `/ciudades/departamento/{id}` | Lista ciudades de un departamento |
| GET | `/ciudades/departamento/{id}/activas` | Lista ciudades activas de un departamento |
| POST | `/ciudades/` | Crea una nueva ciudad |
| PUT | `/ciudades/{id}` | Actualiza una ciudad |
| DELETE | `/ciudades/{id}` | Elimina una ciudad |

## 🗄️ Estructura de Base de Datos

### Tabla: `departamentos`
```sql
- id: INT (AUTO_INCREMENT, PRIMARY KEY)
- nombre: VARCHAR(100) NOT NULL
- estado: VARCHAR(20) DEFAULT 'Activo'
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
```

### Tabla: `ciudades`
```sql
- id: INT (AUTO_INCREMENT, PRIMARY KEY)
- nombre: VARCHAR(100) NOT NULL
- departamento_id: INT NOT NULL (FOREIGN KEY)
- estado: VARCHAR(20) DEFAULT 'Activo'
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
```

## 🚀 Pasos para Completar la Integración

### 1. Configurar la Conexión a la Base de Datos de Ubicaciones

**Si ya tienes una BD con departamentos y ciudades:**

Edita `app/config/db_config.py` y modifica la función `get_ubicaciones_db_connection()` con los datos de tu BD:

```python
def get_ubicaciones_db_connection():
    return mysql.connector.connect(
        host="TU_HOST",           # Ejemplo: "localhost"
        user="TU_USUARIO",        # Ejemplo: "root"
        password="TU_PASSWORD",    # Tu contraseña
        database="TU_BD",         # Nombre de tu BD de ubicaciones
        port=3306                 # Puerto MySQL
    )
```

**Ver guía completa:** `CONFIGURACION_BD_UBICACIONES.md`

### 2. (Opcional) Crear las Tablas si No Existen

Si necesitas crear las tablas desde cero, ejecuta el script SQL:

```bash
mysql -u root -p railway < app/sql/create_ubicaciones_tables.sql
```

O desde MySQL Workbench o cualquier cliente MySQL, ejecuta el contenido del archivo `app/sql/create_ubicaciones_tables.sql`.

### 3. Verificar que el Servidor Funciona

Inicia el servidor FastAPI:

```bash
python -m uvicorn app.main:app --reload
```

O si estás usando el método directo:

```bash
python app/main.py
```

### 4. Probar los Endpoints

Puedes probar los endpoints usando:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Postman** o cualquier cliente HTTP

### 5. Ejemplo de Uso

#### Crear un Departamento
```bash
POST http://localhost:8000/departamentos/
Content-Type: application/json

{
  "nombre": "Antioquia",
  "estado": "Activo"
}
```

#### Crear una Ciudad
```bash
POST http://localhost:8000/ciudades/
Content-Type: application/json

{
  "nombre": "Medellín",
  "departamento_id": 1,
  "estado": "Activo"
}
```

#### Obtener Ciudades por Departamento
```bash
GET http://localhost:8000/ciudades/departamento/1/activas
```

## 📝 Notas Importantes

1. **Relaciones**: Las ciudades tienen una relación de clave foránea con departamentos. Si eliminas un departamento, se eliminarán automáticamente sus ciudades (CASCADE).

2. **Validaciones**: 
   - El controlador valida que el departamento exista antes de crear/actualizar una ciudad
   - Los nombres de departamentos son únicos
   - Los nombres de ciudades son únicos dentro de cada departamento

3. **Estados**: Los valores de estado pueden ser "Activo" o "Inactivo". Por defecto es "Activo".

4. **CORS**: El servidor ya está configurado para aceptar peticiones desde `http://localhost:4200` (Angular).

## 🔍 Verificación

Una vez que hayas creado las tablas y iniciado el servidor, puedes verificar que todo funciona:

1. Ve a `http://localhost:8000/docs`
2. Busca los endpoints de `/departamentos` y `/ciudades`
3. Prueba crear un departamento y luego una ciudad
4. Verifica que puedes obtener ciudades por departamento

## 🐛 Solución de Problemas

### Error: "Table 'departamentos' doesn't exist"
- **Solución**: Ejecuta el script SQL `create_ubicaciones_tables.sql`

### Error: "Foreign key constraint fails"
- **Solución**: Asegúrate de que el `departamento_id` existe antes de crear una ciudad

### Error: "Duplicate entry"
- **Solución**: El nombre del departamento o ciudad ya existe. Usa un nombre diferente.

### Los endpoints no aparecen en Swagger
- **Solución**: Verifica que las rutas estén importadas y registradas en `app/main.py`

