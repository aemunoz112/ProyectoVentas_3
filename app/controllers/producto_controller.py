from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import mysql.connector
from app.config.db_config import get_db_connection

class ProductoController:

    def create_producto(self, producto):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
            INSERT INTO productos (codigo_producto, nombre_producto, descripcion, categoria, unidad_medida, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (
                producto.codigo_producto,
                producto.nombre_producto,
                producto.descripcion,
                producto.categoria,
                producto.unidad_medida,
                producto.estado
            )

            cursor.execute(query, values)
            conn.commit()

            return {"mensaje": "Producto creado exitosamente"}

        except mysql.connector.Error as err:
            print(f"Error al crear producto: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al crear producto")

        finally:
            conn.close()

    def get_producto(self, producto_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos WHERE id = %s", (producto_id,))
            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Producto no encontrado")

            content = {
                "id": int(result[0]),
                "codigo_producto": result[1],
                "nombre_producto": result[2],
                "descripcion": result[3],
                "categoria": result[4],
                "unidad_medida": result[5],
                "estado": str(result[6]),
                "created_at": str(result[7]),
                "updated_at": str(result[8])
            }

            return jsonable_encoder(content)

        except mysql.connector.Error as err:
            print(f"Error al obtener producto: {err}")
            raise HTTPException(status_code=500, detail="Error al obtener producto")

        finally:
            conn.close()

    def get_productos(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos")
            result = cursor.fetchall()

            if not result:
                raise HTTPException(status_code=404, detail="No se encontraron productos")

            payload = [
                {
                    "id": data[0],
                    "codigo_producto": data[1],
                    "nombre_producto": data[2],
                    "descripcion": data[3],
                    "categoria": data[4],
                    "unidad_medida": data[5],
                    "estado": data[6],
                    "created_at": str(data[7]),
                    "updated_at": str(data[8])
                } for data in result
            ]

            return {"resultado": jsonable_encoder(payload)}

        except mysql.connector.Error as err:
            print(f"Error al listar productos: {err}")
            raise HTTPException(status_code=500, detail="Error al listar productos")

        finally:
            conn.close()

    def update_producto(self, producto_id: int, producto):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM productos WHERE id = %s", (producto_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Producto no encontrado")

            query = """
            UPDATE productos
            SET codigo_producto = %s,
                nombre_producto = %s,
                descripcion = %s,
                categoria = %s,
                unidad_medida = %s,
                estado = %s
            WHERE id = %s
            """
            values = (
                producto.codigo_producto,
                producto.nombre_producto,
                producto.descripcion,
                producto.categoria,
                producto.unidad_medida,
                producto.estado,
                producto_id
            )

            cursor.execute(query, values)
            conn.commit()

            return {"mensaje": f"Producto con ID {producto_id} actualizado correctamente"}

        except mysql.connector.Error as err:
            print(f"Error al actualizar producto: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar producto")

        finally:
            conn.close()

    def delete_producto(self, producto_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM productos WHERE id = %s", (producto_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Producto no encontrado")

            cursor.execute("DELETE FROM productos WHERE id = %s", (producto_id,))
            conn.commit()

            return {"mensaje": f"Producto con ID {producto_id} eliminado correctamente"}

        except mysql.connector.Error as err:
            print(f"Error al eliminar producto: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al eliminar producto")

        finally:
            conn.close()