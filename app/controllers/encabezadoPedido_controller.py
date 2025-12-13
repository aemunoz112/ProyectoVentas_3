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
            INSERT INTO encabezado_pedidos (tipo_pedido, id_cliente, id_vendedor, moneda, TRM, OC_cliente, condicion_pago, direccion, departamento_id, ciudad_id, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            """
            values = (
                encabezado.tipo_pedido,
                encabezado.id_cliente,
                encabezado.id_vendedor,
                encabezado.moneda,
                encabezado.TRM,
                encabezado.OC_cliente,
                encabezado.condicion_pago,
                encabezado.direccion,
                encabezado.departamento_id,
                encabezado.ciudad_id
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
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM encabezado_pedidos WHERE id = %s", (encabezado_id,))
            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Encabezado de pedido no encontrado")

            content = {
                "id": int(result["id"]),
                "tipo_pedido": result["tipo_pedido"],
                "id_cliente": int(result["id_cliente"]),
                "id_vendedor": int(result["id_vendedor"]),
                "moneda": result["moneda"],
                "TRM": float(result["TRM"]) if result.get("TRM") is not None else None,
                "OC_cliente": result.get("OC_cliente"),
                "condicion_pago": result.get("condicion_pago"),
                "direccion": result.get("direccion"),
                "departamento_id": int(result["departamento_id"]) if result.get("departamento_id") is not None else None,
                "ciudad_id": int(result["ciudad_id"]) if result.get("ciudad_id") is not None else None,
                "created_at": str(result["created_at"]) if result.get("created_at") else None,
                "updated_at": str(result["updated_at"]) if result.get("updated_at") else None
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
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM encabezado_pedidos")
            result = cursor.fetchall()

            if not result:
                raise HTTPException(status_code=404, detail="No se encontraron encabezados de pedidos")

            payload = [
                {
                    "id": int(data["id"]),
                    "tipo_pedido": data["tipo_pedido"],
                    "id_cliente": int(data["id_cliente"]),
                    "id_vendedor": int(data["id_vendedor"]),
                    "moneda": data["moneda"],
                    "TRM": float(data["TRM"]) if data.get("TRM") is not None else None,
                    "OC_cliente": data.get("OC_cliente"),
                    "condicion_pago": data.get("condicion_pago"),
                    "direccion": data.get("direccion"),
                    "departamento_id": int(data["departamento_id"]) if data.get("departamento_id") is not None else None,
                    "ciudad_id": int(data["ciudad_id"]) if data.get("ciudad_id") is not None else None,
                    "created_at": str(data["created_at"]) if data.get("created_at") else None,
                    "updated_at": str(data["updated_at"]) if data.get("updated_at") else None
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
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM encabezado_pedidos WHERE id_cliente = %s", (id_cliente,))
            result = cursor.fetchall()

            if not result:
                raise HTTPException(status_code=404, detail=f"No se encontraron pedidos para el cliente {id_cliente}")

            payload = [
                {
                    "id": int(data["id"]),
                    "tipo_pedido": data["tipo_pedido"],
                    "id_cliente": int(data["id_cliente"]),
                    "id_vendedor": int(data["id_vendedor"]),
                    "moneda": data["moneda"],
                    "TRM": float(data["TRM"]) if data.get("TRM") is not None else None,
                    "OC_cliente": data.get("OC_cliente"),
                    "condicion_pago": data.get("condicion_pago"),
                    "direccion": data.get("direccion"),
                    "departamento_id": int(data["departamento_id"]) if data.get("departamento_id") is not None else None,
                    "ciudad_id": int(data["ciudad_id"]) if data.get("ciudad_id") is not None else None,
                    "created_at": str(data["created_at"]) if data.get("created_at") else None,
                    "updated_at": str(data["updated_at"]) if data.get("updated_at") else None
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
                condicion_pago = %s,
                direccion = %s,
                departamento_id = %s,
                ciudad_id = %s,
                updated_at = NOW()
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
                encabezado.direccion,
                encabezado.departamento_id,
                encabezado.ciudad_id,
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