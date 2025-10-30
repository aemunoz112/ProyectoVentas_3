from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import mysql.connector
from app.config.db_config import get_db_connection

class InventarioController:

    def create_inventario(self, inventario):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
            INSERT INTO inventario (id_producto, lote, cantidad_disponible)
            VALUES (%s, %s, %s)
            """
            values = (
                inventario.id_producto,
                inventario.lote,
                inventario.cantidad_disponible
            )

            cursor.execute(query, values)
            conn.commit()

            return {"mensaje": "Inventario creado exitosamente"}

        except mysql.connector.Error as err:
            print(f"Error al crear inventario: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al crear inventario")

        finally:
            conn.close()

    def get_inventario(self, inventario_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM inventario WHERE id = %s", (inventario_id,))
            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Inventario no encontrado")

            content = {
                "id": int(result[0]),
                "id_producto": int(result[1]),
                "lote": result[2],
                "cantidad_disponible": float(result[3]),
                "created_at": str(result[4]),
                "updated_at": str(result[5])
            }

            return jsonable_encoder(content)

        except mysql.connector.Error as err:
            print(f"Error al obtener inventario: {err}")
            raise HTTPException(status_code=500, detail="Error al obtener inventario")

        finally:
            conn.close()

    def get_inventarios(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM inventario")
            result = cursor.fetchall()

            if not result:
                raise HTTPException(status_code=404, detail="No se encontraron registros de inventario")

            payload = [
                {
                    "id": data[0],
                    "id_producto": data[1],
                    "lote": data[2],
                    "cantidad_disponible": data[3],
                    "created_at": str(data[4]),
                    "updated_at": str(data[5])
                } for data in result
            ]

            return {"resultado": jsonable_encoder(payload)}

        except mysql.connector.Error as err:
            print(f"Error al listar inventario: {err}")
            raise HTTPException(status_code=500, detail="Error al listar inventario")

        finally:
            conn.close()

    def update_inventario(self, inventario_id: int, inventario):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM inventario WHERE id = %s", (inventario_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Inventario no encontrado")

            query = """
            UPDATE inventario
            SET id_producto = %s,
                lote = %s,
                cantidad_disponible = %s
            WHERE id = %s
            """
            values = (
                inventario.id_producto,
                inventario.lote,
                inventario.cantidad_disponible,
                inventario_id
            )

            cursor.execute(query, values)
            conn.commit()

            return {"mensaje": f"Inventario con ID {inventario_id} actualizado correctamente"}

        except mysql.connector.Error as err:
            print(f"Error al actualizar inventario: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar inventario")

        finally:
            conn.close()

    def delete_inventario(self, inventario_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM inventario WHERE id = %s", (inventario_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Inventario no encontrado")

            cursor.execute("DELETE FROM inventario WHERE id = %s", (inventario_id,))
            conn.commit()

            return {"mensaje": f"Inventario con ID {inventario_id} eliminado correctamente"}

        except mysql.connector.Error as err:
            print(f"Error al eliminar inventario: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al eliminar inventario")

        finally:
            conn.close()