from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import mysql.connector
from app.config.db_config import get_db_connection

class DetallePedidosController:

    def create_detalle_pedido(self, detalle):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
            INSERT INTO detalle_pedidos (id_pedido, id_producto, numero_linea, cantidad_solicitada, cantidad_confirmada, 
                                        precio_unitario, precio_total, precio_extranjero, precio_total_extranjero, 
                                        numero_documento, tipo_documento, estado_siguiente, estado_anterior)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                detalle.id_pedido,
                detalle.id_producto,
                detalle.numero_linea,
                detalle.cantidad_solicitada,
                detalle.cantidad_confirmada,
                detalle.precio_unitario,
                detalle.precio_total,
                detalle.precio_extranjero,
                detalle.precio_total_extranjero,
                detalle.numero_documento,
                detalle.tipo_documento,
                detalle.estado_siguiente,
                detalle.estado_anterior
            )

            cursor.execute(query, values)
            conn.commit()

            return {"mensaje": "Detalle de pedido creado exitosamente"}

        except mysql.connector.Error as err:
            print(f"Error al crear detalle de pedido: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al crear detalle de pedido")

        finally:
            conn.close()

    def get_detalle_pedido(self, detalle_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM detalle_pedidos WHERE id = %s", (detalle_id,))
            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Detalle de pedido no encontrado")

            content = {
                "id": int(result[0]),
                "id_pedido": int(result[1]),
                "id_producto": int(result[2]),
                "numero_linea": int(result[3]) if result[3] is not None else None,
                "cantidad_solicitada": float(result[4]),
                "cantidad_confirmada": float(result[5]) if result[5] is not None else None,
                "precio_unitario": float(result[6]) if result[6] is not None else None,
                "precio_total": float(result[7]) if result[7] is not None else None,
                "precio_extranjero": float(result[8]) if result[8] is not None else None,
                "precio_total_extranjero": float(result[9]) if result[9] is not None else None,
                "numero_documento": result[10],
                "tipo_documento": result[11],
                "estado_siguiente": int(result[12]),
                "estado_anterior": int(result[13]),
                "created_at": str(result[14]),
                "updated_at": str(result[15])
            }

            return jsonable_encoder(content)

        except mysql.connector.Error as err:
            print(f"Error al obtener detalle de pedido: {err}")
            raise HTTPException(status_code=500, detail="Error al obtener detalle de pedido")

        finally:
            conn.close()

    def get_detalles_pedidos(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM detalle_pedidos")
            result = cursor.fetchall()

            if not result:
                raise HTTPException(status_code=404, detail="No se encontraron detalles de pedidos")

            payload = [
                {
                    "id": data[0],
                    "id_pedido": data[1],
                    "id_producto": data[2],
                    "numero_linea": data[3],
                    "cantidad_solicitada": data[4],
                    "cantidad_confirmada": data[5],
                    "precio_unitario": data[6],
                    "precio_total": data[7],
                    "precio_extranjero": data[8],
                    "precio_total_extranjero": data[9],
                    "numero_documento": data[10],
                    "tipo_documento": data[11],
                    "estado_siguiente": data[12],
                    "estado_anterior": data[13],
                    "created_at": str(data[14]),
                    "updated_at": str(data[15])
                } for data in result
            ]

            return {"resultado": jsonable_encoder(payload)}

        except mysql.connector.Error as err:
            print(f"Error al listar detalles de pedidos: {err}")
            raise HTTPException(status_code=500, detail="Error al listar detalles de pedidos")

        finally:
            conn.close()

    def get_detalles_by_pedido(self, id_pedido: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM detalle_pedidos WHERE id_pedido = %s", (id_pedido,))
            result = cursor.fetchall()

            if not result:
                raise HTTPException(status_code=404, detail=f"No se encontraron detalles para el pedido {id_pedido}")

            payload = [
                {
                    "id": data[0],
                    "id_pedido": data[1],
                    "id_producto": data[2],
                    "numero_linea": data[3],
                    "cantidad_solicitada": data[4],
                    "cantidad_confirmada": data[5],
                    "precio_unitario": data[6],
                    "precio_total": data[7],
                    "precio_extranjero": data[8],
                    "precio_total_extranjero": data[9],
                    "numero_documento": data[10],
                    "tipo_documento": data[11],
                    "estado_siguiente": data[12],
                    "estado_anterior": data[13],
                    "created_at": str(data[14]),
                    "updated_at": str(data[15])
                } for data in result
            ]

            return {"resultado": jsonable_encoder(payload)}

        except mysql.connector.Error as err:
            print(f"Error al obtener detalles por pedido: {err}")
            raise HTTPException(status_code=500, detail="Error al obtener detalles por pedido")

        finally:
            conn.close()

    def update_detalle_pedido(self, detalle_id: int, detalle):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM detalle_pedidos WHERE id = %s", (detalle_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Detalle de pedido no encontrado")

            query = """
            UPDATE detalle_pedidos
            SET id_pedido = %s,
                id_producto = %s,
                numero_linea = %s,
                cantidad_solicitada = %s,
                cantidad_confirmada = %s,
                precio_unitario = %s,
                precio_total = %s,
                precio_extranjero = %s,
                precio_total_extranjero = %s,
                numero_documento = %s,
                tipo_documento = %s,
                estado_siguiente = %s,
                estado_anterior = %s
            WHERE id = %s
            """
            values = (
                detalle.id_pedido,
                detalle.id_producto,
                detalle.numero_linea,
                detalle.cantidad_solicitada,
                detalle.cantidad_confirmada,
                detalle.precio_unitario,
                detalle.precio_total,
                detalle.precio_extranjero,
                detalle.precio_total_extranjero,
                detalle.numero_documento,
                detalle.tipo_documento,
                detalle.estado_siguiente,
                detalle.estado_anterior,
                detalle_id
            )

            cursor.execute(query, values)
            conn.commit()

            return {"mensaje": f"Detalle de pedido con ID {detalle_id} actualizado correctamente"}

        except mysql.connector.Error as err:
            print(f"Error al actualizar detalle de pedido: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar detalle de pedido")

        finally:
            conn.close()

    def delete_detalle_pedido(self, detalle_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM detalle_pedidos WHERE id = %s", (detalle_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Detalle de pedido no encontrado")

            cursor.execute("DELETE FROM detalle_pedidos WHERE id = %s", (detalle_id,))
            conn.commit()

            return {"mensaje": f"Detalle de pedido con ID {detalle_id} eliminado correctamente"}

        except mysql.connector.Error as err:
            print(f"Error al eliminar detalle de pedido: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al eliminar detalle de pedido")

        finally:
            conn.close()