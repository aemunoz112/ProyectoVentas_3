from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import mysql.connector
from app.config.db_config import get_db_connection

class DetallesWoController:

    def create_detalleWo(self, detalle):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
            INSERT INTO detalle_Wo (id_wo, id_pedido, id_producto, cantidad_solicitada, cantidad_producida)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (
                detalle.id_wo,
                detalle.id_pedido,
                detalle.id_producto,
                detalle.cantidad_solicitada,
                detalle.cantidad_producida
            )

            cursor.execute(query, values)
            conn.commit()

            return {"mensaje": "Detalle de WO creado exitosamente"}

        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear detalle de WO: {err}")

        finally:
            conn.close()

    def get_detalleWo(self, detalle_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM detalle_Wo WHERE id = %s", (detalle_id,))
            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Detalle de WO no encontrado")

            content = {
                "id": result[0],
                "id_wo": result[1],
                "id_pedido": result[2],
                "id_producto": result[3],
                "cantidad_solicitada": result[4],
                "cantidad_producida": result[5],
                "created_at": str(result[6]),
                "updated_at": str(result[7])
            }

            return jsonable_encoder(content)

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener detalle de WO: {err}")

        finally:
            conn.close()

    def get_detallesWo(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM detalle_Wo")
            result = cursor.fetchall()

            if not result:
                return {"resultado": []}

            payload = [
                {
                    "id": data[0],
                    "id_wo": data[1],
                    "id_pedido": data[2],
                    "id_producto": data[3],
                    "cantidad_solicitada": data[4],
                    "cantidad_producida": data[5],
                    "created_at": str(data[6]),
                    "updated_at": str(data[7])
                } for data in result
            ]

            return {"resultado": jsonable_encoder(payload)}

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al listar detalles de WO: {err}")

        finally:
            conn.close()

    def get_detallesByWo(self, id_wo: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM detalle_Wo WHERE id_wo = %s", (id_wo,))
            result = cursor.fetchall()

            if not result:
                raise HTTPException(status_code=404, detail=f"No se encontraron detalles para WO {id_wo}")

            payload = [
                {
                    "id": data[0],
                    "id_wo": data[1],
                    "id_pedido": data[2],
                    "id_producto": data[3],
                    "cantidad_solicitada": data[4],
                    "cantidad_producida": data[5],
                    "created_at": str(data[6]),
                    "updated_at": str(data[7])
                } for data in result
            ]

            return {"resultado": jsonable_encoder(payload)}

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener detalles por WO: {err}")

        finally:
            conn.close()

    def update_detalleWo(self, detalle_id: int, detalle):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM detalle_Wo WHERE id = %s", (detalle_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Detalle de WO no encontrado")

            query = """
            UPDATE detalle_Wo
            SET id_wo = %s,
                id_pedido = %s,
                id_producto = %s,
                cantidad_solicitada = %s,
                cantidad_producida = %s
            WHERE id = %s
            """
            values = (
                detalle.id_wo,
                detalle.id_pedido,
                detalle.id_producto,
                detalle.cantidad_solicitada,
                detalle.cantidad_producida,
                detalle_id
            )

            cursor.execute(query, values)
            conn.commit()

            return {"mensaje": f"Detalle de WO con ID {detalle_id} actualizado correctamente"}

        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar detalle de WO: {err}")

        finally:
            conn.close()

    def delete_detalleWo(self, detalle_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM detalle_Wo WHERE id = %s", (detalle_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Detalle de WO no encontrado")

            cursor.execute("DELETE FROM detalle_Wo WHERE id = %s", (detalle_id,))
            conn.commit()

            return {"mensaje": f"Detalle de WO con ID {detalle_id} eliminado correctamente"}

        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al eliminar detalle de WO: {err}")

        finally:
            conn.close()
