from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import mysql.connector
from app.config.db_config import get_db_connection

class OrdenesProduccionController:

    def create_ordenProduccion(self, orden):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
            INSERT INTO ordenes_produccion (estado_siguiente, estado_anterior, fecha_inicio, fecha_fin_estimada, fecha_fin_real)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (
                orden.estado_siguiente,
                orden.estado_anterior,
                orden.fecha_inicio,
                orden.fecha_fin_estimada,
                orden.fecha_fin_real
            )

            cursor.execute(query, values)
            conn.commit()

            return {"mensaje": "Orden de producción creada exitosamente"}

        except mysql.connector.Error as err:
            print(f"Error al crear orden de producción: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al crear orden de producción")

        finally:
            conn.close()

    def get_ordenProduccion(self, orden_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ordenes_produccion WHERE id = %s", (orden_id,))
            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Orden de producción no encontrada")

            content = {
                "id": int(result[0]),
                "estado_siguiente": result[1],
                "estado_anterior": result[2],
                "fecha_inicio": str(result[3]) if result[3] is not None else None,
                "fecha_fin_estimada": str(result[4]) if result[4] is not None else None,
                "fecha_fin_real": str(result[5]) if result[5] is not None else None,
                "created_at": str(result[6]),
                "updated_at": str(result[7])
            }

            return jsonable_encoder(content)

        except mysql.connector.Error as err:
            print(f"Error al obtener orden de producción: {err}")
            raise HTTPException(status_code=500, detail="Error al obtener orden de producción")

        finally:
            conn.close()

    def get_ordenesProduccion(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ordenes_produccion")
            result = cursor.fetchall()

            if not result:
                raise HTTPException(status_code=404, detail="No se encontraron órdenes de producción")

            payload = [
                {
                    "id": data[0],
                    "estado_siguiente": data[1],
                    "estado_anterior": data[2],
                    "fecha_inicio": str(data[3]) if data[3] is not None else None,
                    "fecha_fin_estimada": str(data[4]) if data[4] is not None else None,
                    "fecha_fin_real": str(data[5]) if data[5] is not None else None,
                    "created_at": str(data[6]),
                    "updated_at": str(data[7])
                } for data in result
            ]

            return {"resultado": jsonable_encoder(payload)}

        except mysql.connector.Error as err:
            print(f"Error al listar órdenes de producción: {err}")
            raise HTTPException(status_code=500, detail="Error al listar órdenes de producción")

        finally:
            conn.close()

    def update_ordenProduccion(self, orden_id: int, orden):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM ordenes_produccion WHERE id = %s", (orden_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Orden de producción no encontrada")

            query = """
            UPDATE ordenes_produccion
            SET estado_siguiente = %s,
                estado_anterior = %s,
                fecha_inicio = %s,
                fecha_fin_estimada = %s,
                fecha_fin_real = %s
            WHERE id = %s
            """
            values = (
                orden.estado_siguiente,
                orden.estado_anterior,
                orden.fecha_inicio,
                orden.fecha_fin_estimada,
                orden.fecha_fin_real,
                orden_id
            )

            cursor.execute(query, values)
            conn.commit()

            return {"mensaje": f"Orden de producción con ID {orden_id} actualizada correctamente"}

        except mysql.connector.Error as err:
            print(f"Error al actualizar orden de producción: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar orden de producción")

        finally:
            conn.close()

    def delete_ordenProduccion(self, orden_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM ordenes_produccion WHERE id = %s", (orden_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Orden de producción no encontrada")

            cursor.execute("DELETE FROM ordenes_produccion WHERE id = %s", (orden_id,))
            conn.commit()

            return {"mensaje": f"Orden de producción con ID {orden_id} eliminada correctamente"}

        except mysql.connector.Error as err:
            print(f"Error al eliminar orden de producción: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al eliminar orden de producción")

        finally:
            conn.close()