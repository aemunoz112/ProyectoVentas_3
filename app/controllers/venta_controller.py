from typing import List
from decimal import Decimal

from fastapi import HTTPException
import mysql.connector
from app.config.db_config import get_db_connection
from app.models.venta_model import (
    VentaCreate,
    VentaResponse,
    VentaUpdate,
    VentaDetalleResponse,
)

class VentaController:

    def listar_ventas(self) -> List[VentaResponse]:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT * FROM encabezado_pedidos 
                ORDER BY created_at DESC
            """)
            encabezados = cursor.fetchall()

            ventas = []
            for enc in encabezados:
                # Obtener detalles del pedido
                cursor.execute("""
                    SELECT dp.*, p.nombre_producto as producto_nombre
                    FROM detalle_pedidos dp
                    LEFT JOIN productos p ON dp.id_producto = p.id
                    WHERE dp.id_pedido = %s
                    ORDER BY dp.numero_linea
                """, (enc.get("id"),))
                detalles_data = cursor.fetchall()

                detalles = [
                    VentaDetalleResponse(
                        id=det.get("id"),
                        id_producto=det.get("id_producto", 0),
                        cantidad_solicitada=Decimal(str(det.get("cantidad_solicitada") or 0)),
                        cantidad_confirmada=Decimal(str(det.get("cantidad_confirmada") or 0)) if det.get("cantidad_confirmada") else None,
                        precio_unitario=Decimal(str(det.get("precio_unitario") or 0)),
                        numero_linea=det.get("numero_linea"),
                        numero_documento=det.get("numero_documento"),
                        tipo_documento=det.get("tipo_documento"),
                        estado_siguiente=det.get("estado_siguiente", 1),
                        estado_anterior=det.get("estado_anterior", 1),
                        precio_total=Decimal(str(det.get("precio_total") or 0)) if det.get("precio_total") else None,
                        precio_extranjero=Decimal(str(det.get("precio_extranjero") or 0)) if det.get("precio_extranjero") else None,
                        precio_total_extranjero=Decimal(str(det.get("precio_total_extranjero") or 0)) if det.get("precio_total_extranjero") else None,
                        producto_nombre=det.get("producto_nombre"),
                        created_at=det.get("created_at"),
                        updated_at=det.get("updated_at"),
                    )
                    for det in detalles_data
                ]

                venta = VentaResponse(
                    id=enc.get("id"),
                    tipo_pedido=enc.get("tipo_pedido"),
                    id_cliente=enc.get("id_cliente"),
                    id_vendedor=enc.get("id_vendedor"),
                    moneda=enc.get("moneda"),
                    trm=Decimal(str(enc.get("TRM") or 1)),
                    oc_cliente=enc.get("OC_cliente"),
                    condicion_pago=enc.get("condicion_pago"),
                    direccion=enc.get("direccion"),
                    departamento_id=enc.get("departamento_id"),
                    ciudad_id=enc.get("ciudad_id"),
                    created_at=enc.get("created_at"),
                    updated_at=enc.get("updated_at"),
                    detalles=detalles,
                )
                ventas.append(venta)

            return ventas
        except mysql.connector.Error as err:
            print(f"Error al listar ventas: {err}")
            raise HTTPException(status_code=500, detail="Error al listar ventas")
        finally:
            cursor.close()
            conn.close()

    def obtener_venta(self, venta_id: int) -> VentaResponse:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM encabezado_pedidos WHERE id = %s", (venta_id,))
            enc = cursor.fetchone()

            if not enc:
                raise HTTPException(status_code=404, detail="Venta no encontrada")

            # Obtener detalles
            cursor.execute("""
                SELECT dp.*, p.nombre_producto as producto_nombre
                FROM detalle_pedidos dp
                LEFT JOIN productos p ON dp.id_producto = p.id
                WHERE dp.id_pedido = %s
                ORDER BY dp.numero_linea
            """, (venta_id,))
            detalles_data = cursor.fetchall()

            detalles = [
                VentaDetalleResponse(
                    id=det.get("id"),
                    id_producto=det.get("id_producto", 0),
                    cantidad_solicitada=Decimal(str(det.get("cantidad_solicitada") or 0)),
                    cantidad_confirmada=Decimal(str(det.get("cantidad_confirmada") or 0)) if det.get("cantidad_confirmada") else None,
                    precio_unitario=Decimal(str(det.get("precio_unitario") or 0)),
                    numero_linea=det.get("numero_linea"),
                    numero_documento=det.get("numero_documento"),
                    tipo_documento=det.get("tipo_documento"),
                    estado_siguiente=det.get("estado_siguiente", 1),
                    estado_anterior=det.get("estado_anterior", 1),
                    precio_total=Decimal(str(det.get("precio_total") or 0)) if det.get("precio_total") else None,
                    precio_extranjero=Decimal(str(det.get("precio_extranjero") or 0)) if det.get("precio_extranjero") else None,
                    precio_total_extranjero=Decimal(str(det.get("precio_total_extranjero") or 0)) if det.get("precio_total_extranjero") else None,
                    producto_nombre=det.get("producto_nombre"),
                    created_at=det.get("created_at"),
                    updated_at=det.get("updated_at"),
                )
                for det in detalles_data
            ]

            return VentaResponse(
                id=enc.get("id"),
                tipo_pedido=enc.get("tipo_pedido"),
                id_cliente=enc.get("id_cliente"),
                id_vendedor=enc.get("id_vendedor"),
                moneda=enc.get("moneda"),
                trm=Decimal(str(enc.get("TRM") or 1)),
                oc_cliente=enc.get("OC_cliente"),
                condicion_pago=enc.get("condicion_pago"),
                direccion=enc.get("direccion"),
                departamento_id=enc.get("departamento_id"),
                ciudad_id=enc.get("ciudad_id"),
                created_at=enc.get("created_at"),
                updated_at=enc.get("updated_at"),
                detalles=detalles,
            )
        except mysql.connector.Error as err:
            print(f"Error al obtener venta: {err}")
            raise HTTPException(status_code=500, detail="Error al obtener venta")
        finally:
            cursor.close()
            conn.close()

    def crear_venta(self, venta: VentaCreate) -> VentaResponse:
        if not venta.detalles:
            raise HTTPException(status_code=400, detail="Debe agregar al menos un producto al pedido")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            conn.start_transaction()
            cursor.execute(
                """
                INSERT INTO encabezado_pedidos
                    (tipo_pedido, id_cliente, id_vendedor, moneda, TRM, OC_cliente, condicion_pago, direccion, departamento_id, ciudad_id, created_at, updated_at)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                """,
                (
                    venta.tipo_pedido,
                    venta.id_cliente,
                    venta.id_vendedor,
                    venta.moneda,
                    str(venta.trm or Decimal("1")),
                    venta.oc_cliente,
                    venta.condicion_pago,
                    venta.direccion,
                    venta.departamento_id,
                    venta.ciudad_id,
                ),
            )
            pedido_id = cursor.lastrowid
            self._insertar_detalles(cursor, pedido_id, venta.detalles, venta.moneda, venta.trm)
            conn.commit()
            return self.obtener_venta(pedido_id)
        except mysql.connector.Error as err:
            print(f"Error al crear pedido: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al crear la venta")
        finally:
            cursor.close()
            conn.close()

    def actualizar_venta(self, venta_id: int, venta: VentaUpdate) -> VentaResponse:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM encabezado_pedidos WHERE id = %s", (venta_id,))
            actual = cursor.fetchone()
            if not actual:
                raise HTTPException(status_code=404, detail="Pedido no encontrado")

            moneda = venta.moneda if venta.moneda is not None else actual["moneda"]
            trm = Decimal(str(venta.trm)) if venta.trm is not None else Decimal(str(actual.get("TRM") or 1))

            cursor.execute(
                """
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
                """,
                (
                    venta.tipo_pedido if venta.tipo_pedido is not None else actual["tipo_pedido"],
                    venta.id_cliente if venta.id_cliente is not None else actual["id_cliente"],
                    venta.id_vendedor if venta.id_vendedor is not None else actual["id_vendedor"],
                    moneda,
                    str(trm),
                    venta.oc_cliente if venta.oc_cliente is not None else actual["OC_cliente"],
                    venta.condicion_pago if venta.condicion_pago is not None else actual["condicion_pago"],
                    venta.direccion if venta.direccion is not None else actual.get("direccion"),
                    venta.departamento_id if venta.departamento_id is not None else actual.get("departamento_id"),
                    venta.ciudad_id if venta.ciudad_id is not None else actual.get("ciudad_id"),
                    venta_id,
                ),
            )

            if venta.detalles is not None:
                cursor.execute("DELETE FROM detalle_pedidos WHERE id_pedido = %s", (venta_id,))
                if venta.detalles:
                    self._insertar_detalles(cursor, venta_id, venta.detalles, moneda, trm)
            conn.commit()
            return self.obtener_venta(venta_id)
        except mysql.connector.Error as err:
            print(f"Error al actualizar pedido: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar la venta")
        finally:
            cursor.close()
            conn.close()

    def eliminar_venta(self, venta_id: int):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM encabezado_pedidos WHERE id = %s", (venta_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Pedido no encontrado")

            cursor.execute("DELETE FROM detalle_pedidos WHERE id_pedido = %s", (venta_id,))
            cursor.execute("DELETE FROM encabezado_pedidos WHERE id = %s", (venta_id,))
            conn.commit()
            return {"mensaje": "Pedido eliminado correctamente"}
        except mysql.connector.Error as err:
            print(f"Error al eliminar pedido: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al eliminar la venta")
        finally:
            cursor.close()
            conn.close()

    def _insertar_detalles(self, cursor, pedido_id: int, detalles, moneda: str, trm: Decimal):
        """Método auxiliar para insertar los detalles del pedido"""
        for idx, detalle in enumerate(detalles, start=1):
            precio_total = detalle.cantidad_solicitada * detalle.precio_unitario
            precio_extranjero = precio_total / trm if trm and trm > 0 else precio_total
            precio_total_extranjero = precio_extranjero

            cursor.execute(
                """
                INSERT INTO detalle_pedidos
                    (id_pedido, id_producto, numero_linea, cantidad_solicitada, cantidad_confirmada,
                     precio_unitario, precio_total, precio_extranjero, precio_total_extranjero,
                     numero_documento, tipo_documento, estado_siguiente, estado_anterior, created_at, updated_at)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                """,
                (
                    pedido_id,
                    detalle.id_producto,
                    detalle.numero_linea or idx,
                    str(detalle.cantidad_solicitada),
                    str(detalle.cantidad_confirmada) if detalle.cantidad_confirmada else None,
                    str(detalle.precio_unitario),
                    str(precio_total),
                    str(precio_extranjero),
                    str(precio_total_extranjero),
                    detalle.numero_documento,
                    detalle.tipo_documento,
                    detalle.estado_siguiente,
                    detalle.estado_anterior,
                ),
            )

