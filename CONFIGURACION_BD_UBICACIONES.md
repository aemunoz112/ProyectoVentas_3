# Configuración de Base de Datos Separada para Ubicaciones

## 📋 Descripción

El sistema está configurado para usar una **base de datos separada** para departamentos y ciudades. Esto permite mantener los datos de ubicaciones en una BD independiente de la BD principal del sistema.

## ⚙️ Configuración

### Opción 1: Modificar directamente el archivo de configuración

Edita el archivo `app/config/db_config.py` y modifica la función `get_ubicaciones_db_connection()`:

```python
def get_ubicaciones_db_connection():
    return mysql.connector.connect(
        host="TU_HOST",           # Ejemplo: "localhost" o "192.168.1.100"
        user="TU_USUARIO",        # Ejemplo: "root" o "ubicaciones_user"
        password="TU_PASSWORD",   # Tu contraseña
        database="TU_BD",         # Nombre de tu BD de ubicaciones
        port=3306                 # Puerto de MySQL (por defecto 3306)
    )
```

**Ejemplo con valores reales:**

```python
def get_ubicaciones_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mi_password_123",
        database="bd_ubicaciones_colombia",
        port=3306
    )
```

### Opción 2: Usar variables de entorno (Recomendado)

Puedes configurar las variables de entorno antes de ejecutar el servidor:

**En Windows (PowerShell):**
```powershell
$env:UBICACIONES_DB_HOST="localhost"
$env:UBICACIONES_DB_USER="root"
$env:UBICACIONES_DB_PASSWORD="tu_password"
$env:UBICACIONES_DB_NAME="bd_ubicaciones"
$env:UBICACIONES_DB_PORT="3306"
python -m uvicorn app.main:app --reload
```

**En Windows (CMD):**
```cmd
set UBICACIONES_DB_HOST=localhost
set UBICACIONES_DB_USER=root
set UBICACIONES_DB_PASSWORD=tu_password
set UBICACIONES_DB_NAME=bd_ubicaciones
set UBICACIONES_DB_PORT=3306
python -m uvicorn app.main:app --reload
```

**En Linux/Mac:**
```bash
export UBICACIONES_DB_HOST="localhost"
export UBICACIONES_DB_USER="root"
export UBICACIONES_DB_PASSWORD="tu_password"
export UBICACIONES_DB_NAME="bd_ubicaciones"
export UBICACIONES_DB_PORT="3306"
python -m uvicorn app.main:app --reload
```

### Opción 3: Archivo .env (Más seguro)

Crea un archivo `.env` en la raíz del proyecto:

```env
UBICACIONES_DB_HOST=localhost
UBICACIONES_DB_USER=root
UBICACIONES_DB_PASSWORD=tu_password
UBICACIONES_DB_NAME=bd_ubicaciones
UBICACIONES_DB_PORT=3306
```

Y luego instala `python-dotenv` si no lo tienes:

```bash
pip install python-dotenv
```

Y modifica `app/config/db_config.py` para cargar el archivo `.env`:

```python
from dotenv import load_dotenv
load_dotenv()

# ... resto del código ...
```

## 🗄️ Estructura Esperada de las Tablas

El código espera que las tablas en tu BD de ubicaciones tengan esta estructura:

### Tabla: `departamentos`
```sql
- id: INT (PRIMARY KEY)
- nombre: VARCHAR
- estado: VARCHAR (opcional, puede ser NULL)
- created_at: TIMESTAMP (opcional)
- updated_at: TIMESTAMP (opcional)
```

### Tabla: `ciudades`
```sql
- id: INT (PRIMARY KEY)
- nombre: VARCHAR
- departamento_id: INT (FOREIGN KEY a departamentos.id)
- estado: VARCHAR (opcional, puede ser NULL)
- created_at: TIMESTAMP (opcional)
- updated_at: TIMESTAMP (opcional)
```

## 🔍 Verificar la Conexión

Para verificar que la conexión funciona, puedes:

1. **Probar los endpoints en Swagger:**
   - Inicia el servidor: `python -m uvicorn app.main:app --reload`
   - Ve a `http://localhost:8000/docs`
   - Prueba el endpoint `GET /departamentos/`

2. **Verificar los logs:**
   - Si hay un error de conexión, aparecerá en la consola
   - Revisa que los datos de conexión sean correctos

## ⚠️ Notas Importantes

1. **Nombres de tablas**: El código busca tablas llamadas exactamente `departamentos` y `ciudades`. Si tus tablas tienen otros nombres, deberás modificar las consultas SQL en los controladores.

2. **Nombres de columnas**: Si tus columnas tienen nombres diferentes (por ejemplo, `departamento` en lugar de `nombre`), deberás ajustar las consultas SQL.

3. **Campos opcionales**: Los campos `estado`, `created_at` y `updated_at` son opcionales. Si no existen en tu BD, el código funcionará igual, pero las consultas que filtren por `estado` pueden fallar.

4. **Mismo servidor, diferente BD**: Si tu BD de ubicaciones está en el mismo servidor MySQL pero con un nombre diferente, solo necesitas cambiar el parámetro `database` en la configuración.

5. **Servidor diferente**: Si la BD está en un servidor completamente diferente, cambia el `host` y posiblemente el `port`.

## 🔧 Personalización Avanzada

Si tu estructura de tablas es diferente, puedes modificar las consultas SQL en:

- `app/controllers/departamento_controller.py`
- `app/controllers/ciudad_controller.py`

**Ejemplo:** Si tu tabla se llama `departamento` (singular) en lugar de `departamentos`:

```python
# En departamento_controller.py, cambiar:
cursor.execute("SELECT * FROM departamentos ORDER BY nombre")
# Por:
cursor.execute("SELECT * FROM departamento ORDER BY nombre")
```

## 📝 Ejemplo de Configuración Completa

```python
# app/config/db_config.py

def get_ubicaciones_db_connection():
    """
    Conexión a la BD de ubicaciones en servidor separado
    """
    return mysql.connector.connect(
        host="192.168.1.50",              # IP del servidor de ubicaciones
        user="ubicaciones_user",           # Usuario específico
        password="password_seguro_123",    # Contraseña
        database="colombia_ubicaciones",   # Nombre de la BD
        port=3306                          # Puerto MySQL
    )
```

## 🐛 Solución de Problemas

### Error: "Access denied for user"
- Verifica que el usuario y contraseña sean correctos
- Asegúrate de que el usuario tenga permisos en la BD

### Error: "Unknown database"
- Verifica que el nombre de la base de datos sea correcto
- Asegúrate de que la BD existe en el servidor

### Error: "Can't connect to MySQL server"
- Verifica que el host y puerto sean correctos
- Asegúrate de que el servidor MySQL esté corriendo
- Verifica que no haya un firewall bloqueando la conexión

### Error: "Table 'departamentos' doesn't exist"
- Verifica que las tablas existan en la BD
- Si las tablas tienen otros nombres, modifica las consultas SQL

