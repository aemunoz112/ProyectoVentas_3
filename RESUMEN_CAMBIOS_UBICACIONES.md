# Resumen: Campos de Ubicación en el Backend

## ✅ Cambios Realizados

Se han agregado campos `departamento_id` y `ciudad_id` a las tablas existentes para almacenar referencias a los datos que vienen de la API externa.

### 📝 Archivos Modificados

#### Modelos
- ✅ `app/models/usuario_model.py` - Agregados campos `departamento_id` y `ciudad_id`
- ✅ `app/models/venta_model.py` - Agregados campos en `VentaBase` y `VentaUpdate`
- ✅ `app/models/encabezadoPedido_model.py` - Agregados campos `departamento_id` y `ciudad_id`

#### Controladores
- ✅ `app/controllers/usuario_controller.py` - Actualizado para incluir los nuevos campos en INSERT, UPDATE y SELECT
- ✅ `app/controllers/venta_controller.py` - Actualizado para incluir los nuevos campos en INSERT y UPDATE

### 📄 Script SQL

- ✅ `app/sql/agregar_campos_ubicaciones.sql` - Script para agregar las columnas a las tablas existentes

## 🗄️ Cambios en la Base de Datos

### Tabla: `usuarios`
```sql
ALTER TABLE usuarios 
ADD COLUMN departamento_id INT NULL,
ADD COLUMN ciudad_id INT NULL;
```

### Tabla: `encabezado_pedidos`
```sql
ALTER TABLE encabezado_pedidos 
ADD COLUMN departamento_id INT NULL,
ADD COLUMN ciudad_id INT NULL;
```

## 🚀 Pasos para Aplicar los Cambios

### 1. Ejecutar el Script SQL

Ejecuta el script para agregar las columnas a las tablas:

```bash
mysql -u root -p railway < app/sql/agregar_campos_ubicaciones.sql
```

O desde MySQL Workbench, ejecuta el contenido del archivo `app/sql/agregar_campos_ubicaciones.sql`.

### 2. Verificar que Todo Funciona

Inicia el servidor y prueba los endpoints:

```bash
python -m uvicorn app.main:app --reload
```

Luego prueba en Swagger (`http://localhost:8000/docs`):
- Crear/actualizar un usuario con `departamento_id` y `ciudad_id`
- Crear/actualizar una venta con `departamento_id` y `ciudad_id`

## 📋 Uso desde el Frontend

El frontend ya tiene el servicio `ubicaciones.service.ts` que consume la API externa. Ahora puedes:

1. Obtener departamentos y ciudades de la API externa
2. Al crear/actualizar un usuario o venta, enviar los `departamento_id` y `ciudad_id` al backend
3. El backend guardará estos IDs en las columnas correspondientes

### Ejemplo de Request desde el Frontend

```typescript
// Al crear un usuario
const usuario = {
  nombres: "Juan",
  apellidos: "Pérez",
  email: "juan@example.com",
  // ... otros campos
  departamento_id: 1,  // ID de la API externa
  ciudad_id: 5         // ID de la API externa
};
```

## ⚠️ Notas Importantes

1. **Campos Opcionales**: Los campos `departamento_id` y `ciudad_id` son opcionales (pueden ser `NULL`). Esto permite que los registros existentes sigan funcionando.

2. **No hay Validación de Foreign Key**: Estos campos NO tienen claves foráneas porque los datos vienen de una API externa. Solo almacenan los IDs como referencia.

3. **Compatibilidad**: Los registros existentes seguirán funcionando normalmente, los nuevos campos serán `NULL` para ellos.

4. **No se Crearon Tablas**: Solo se agregaron campos a las tablas existentes. No se crearon tablas de `departamentos` ni `ciudades` en tu BD.

## 🔍 Verificación

Para verificar que los cambios funcionan:

1. Ejecuta el script SQL
2. Inicia el servidor
3. Prueba crear un usuario/venta con `departamento_id` y `ciudad_id`
4. Verifica en la BD que los valores se guardaron correctamente

