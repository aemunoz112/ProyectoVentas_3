from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import mysql.connector
from app.config.db_config import get_db_connection

class EncabezadoPedidosController:

    def create_encabezadoPedido(self, encabezado):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
            INSERT INTO encabezado_pedidos (tipo_pedido, id_cliente, id_vendedor, moneda, TRM, OC_cliente, condicion_pago)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                encabezado.tipo_pedido,
                encabezado.id_cliente,
                encabezado.id_vendedor,
                encabezado.moneda,
                encabezado.TRM,
                encabezado.OC_cliente,
                encabezado.condicion_pago
            )

            cursor.execute(query, values)
            conn.commit()

            return {"mensaje": "Encabezado de pedido creado exitosamente"}

        except mysql.connector.Error as err:
            print(f"Error al crear encabezado de pedido: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al crear encabezado de pedido")

        finally:
            conn.close()

    def get_encabezadoPedido(self, encabezado_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM encabezado_pedidos WHERE id = %s", (encabezado_id,))
            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Encabezado de pedido no encontrado")

            content = {
                "id": int(result[0]),
                "tipo_pedido": result[1],
                "id_cliente": int(result[2]),
                "id_vendedor": int(result[3]),
                "moneda": result[4],
                "TRM": float(result[5]) if result[5] is not None else None,
                "OC_cliente": result[6],
                "condicion_pago": result[7],
                "created_at": str(result[8]),
                "updated_at": str(result[9])
            }

            return jsonable_encoder(content)

        except mysql.connector.Error as err:
            print(f"Error al obtener encabezado de pedido: {err}")
            raise HTTPException(status_code=500, detail="Error al obtener encabezado de pedido")

        finally:
            conn.close()

    def get_encabezadosPedidos(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM encabezado_pedidos")
            result = cursor.fetchall()

            if not result:
                raise HTTPException(status_code=404, detail="No se encontraron encabezados de pedidos")

            payload = [
                {
                    "id": data[0],
                    "tipo_pedido": data[1],
                    "id_cliente": data[2],
                    "id_vendedor": data[3],
                    "moneda": data[4],
                    "TRM": data[5],
                    "OC_cliente": data[6],
                    "condicion_pago": data[7],
                    "created_at": str(data[8]),
                    "updated_at": str(data[9])
                } for data in result
            ]

            return {"resultado": jsonable_encoder(payload)}

        except mysql.connector.Error as err:
            print(f"Error al listar encabezados de pedidos: {err}")
            raise HTTPException(status_code=500, detail="Error al listar encabezados de pedidos")

        finally:
            conn.close()

    def get_encabezadosByCliente(self, id_cliente: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM encabezado_pedidos WHERE id_cliente = %s", (id_cliente,))
            result = cursor.fetchall()

            if not result:
                raise HTTPException(status_code=404, detail=f"No se encontraron pedidos para el cliente {id_cliente}")

            payload = [
                {
                    "id": data[0],
                    "tipo_pedido": data[1],
                    "id_cliente": data[2],
                    "id_vendedor": data[3],
                    "moneda": data[4],
                    "TRM": data[5],
                    "OC_cliente": data[6],
                    "condicion_pago": data[7],
                    "created_at": str(data[8]),
                    "updated_at": str(data[9])
                } for data in result
            ]

            return {"resultado": jsonable_encoder(payload)}

        except mysql.connector.Error as err:
            print(f"Error al obtener pedidos por cliente: {err}")
            raise HTTPException(status_code=500, detail="Error al obtener pedidos por cliente")

        finally:
            conn.close()

    def update_encabezadoPedido(self, encabezado_id: int, encabezado):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM encabezado_pedidos WHERE id = %s", (encabezado_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Encabezado de pedido no encontrado")

            query = """
            UPDATE encabezado_pedidos
            SET tipo_pedido = %s,
                id_cliente = %s,
                id_vendedor = %s,
                moneda = %s,
                TRM = %s,
                OC_cliente = %s,
                condicion_pago = %s
            WHERE id = %s
            """
            values = (
                encabezado.tipo_pedido,
                encabezado.id_cliente,
                encabezado.id_vendedor,
                encabezado.moneda,
                encabezado.TRM,
                encabezado.OC_cliente,
                encabezado.condicion_pago,
                encabezado_id
            )

            cursor.execute(query, values)
            conn.commit()

            return {"mensaje": f"Encabezado de pedido con ID {encabezado_id} actualizado correctamente"}

        except mysql.connector.Error as err:
            print(f"Error al actualizar encabezado de pedido: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar encabezado de pedido")

        finally:
            conn.close()

    def delete_encabezadoPedido(self, encabezado_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM encabezado_pedidos WHERE id = %s", (encabezado_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Encabezado de pedido no encontrado")

            cursor.execute("DELETE FROM encabezado_pedidos WHERE id = %s", (encabezado_id,))
            conn.commit()

            return {"mensaje": f"Encabezado de pedido con ID {encabezado_id} eliminado correctamente"}

        except mysql.connector.Error as err:
            print(f"Error al eliminar encabezado de pedido: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al eliminar encabezado de pedido")

        finally:
            conn.close()