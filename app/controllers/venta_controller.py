from collections import defaultdict
from decimal import Decimal
from typing import Dict, List

import mysql.connector
from fastapi import HTTPException

from app.config.db_config import get_db_connection
from app.models.venta_model import (
    VentaCreate,
    VentaDetalleCreate,
    VentaDetalleResponse,
    VentaResponse,
    VentaUpdate,
)


class VentaController:

    def listar_ventas(self) -> List[VentaResponse]:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT id, tipo_pedido, id_cliente, id_vendedor, moneda, TRM, OC_cliente,
                       condicion_pago, created_at, updated_at
                FROM encabezado_pedidos
                ORDER BY created_at DESC, id DESC
                """
            )
            encabezados = cursor.fetchall()
            if not encabezados:
                return []

            pedido_ids = [row["id"] for row in encabezados]
            detalles_por_pedido = self._obtener_detalles_por_pedido(cursor, pedido_ids)
            return [self._mapear_respuesta(encabezado, detalles_por_pedido.get(encabezado["id"], [])) for encabezado in encabezados]
        except mysql.connector.Error as err:
            print(f"Error al listar pedidos: {err}")
            raise HTTPException(status_code=500, detail="Error al obtener las ventas")
        finally:
            cursor.close()
            conn.close()

    def obtener_venta(self, venta_id: int) -> VentaResponse:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT id, tipo_pedido, id_cliente, id_vendedor, moneda, TRM, OC_cliente,
                       condicion_pago, created_at, updated_at
                FROM encabezado_pedidos
                WHERE id = %s
                """,
                (venta_id,),
            )
            encabezado = cursor.fetchone()
            if not encabezado:
                raise HTTPException(status_code=404, detail="Pedido no encontrado")

            detalles = self._obtener_detalles_por_pedido(cursor, [venta_id]).get(venta_id, [])
            return self._mapear_respuesta(encabezado, detalles)
        except mysql.connector.Error as err:
            print(f"Error al obtener pedido: {err}")
            raise HTTPException(status_code=500, detail="Error al obtener la venta")
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
                    (tipo_pedido, id_cliente, id_vendedor, moneda, TRM, OC_cliente, condicion_pago, created_at, updated_at)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                """,
                (
                    venta.tipo_pedido,
                    venta.id_cliente,
                    venta.id_vendedor,
                    venta.moneda,
                    str(venta.trm or Decimal("1")),
                    venta.oc_cliente,
                    venta.condicion_pago,
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

    def _obtener_detalles_por_pedido(self, cursor, pedido_ids: List[int]) -> Dict[int, List[dict]]:
        if not pedido_ids:
            return {}
        marcadores = ",".join(["%s"] * len(pedido_ids))
        cursor.execute(
            f"""
            SELECT d.*, p.nombre_producto
            FROM detalle_pedidos d
            LEFT JOIN productos p ON p.id = d.id_producto
            WHERE d.id_pedido IN ({marcadores})
            ORDER BY d.id_pedido, d.numero_linea
            """,
            tuple(pedido_ids),
        )
        filas = cursor.fetchall()
        agrupado: Dict[int, List[dict]] = defaultdict(list)
        for fila in filas:
            agrupado[fila["id_pedido"]].append(fila)
        return agrupado

    def _mapear_respuesta(self, encabezado: dict, detalles: List[dict]) -> VentaResponse:
        detalles_respuesta = [self._mapear_detalle(detalle) for detalle in detalles]
        return VentaResponse(
            id=encabezado["id"],
            tipo_pedido=encabezado["tipo_pedido"],
            id_cliente=encabezado["id_cliente"],
            id_vendedor=encabezado["id_vendedor"],
            moneda=encabezado["moneda"],
            trm=Decimal(str(encabezado.get("TRM") or 1)),
            oc_cliente=encabezado.get("OC_cliente"),
            condicion_pago=encabezado.get("condicion_pago"),
            created_at=encabezado.get("created_at"),
            updated_at=encabezado.get("updated_at"),
            detalles=detalles_respuesta,
        )

    def _mapear_detalle(self, detalle: dict) -> VentaDetalleResponse:
        return VentaDetalleResponse(
            id=detalle["id"],
            id_producto=detalle["id_producto"],
            cantidad_solicitada=Decimal(str(detalle["cantidad_solicitada"])),
            cantidad_confirmada=Decimal(str(detalle.get("cantidad_confirmada") or detalle["cantidad_solicitada"])),
            precio_unitario=Decimal(str(detalle.get("precio_unitario") or 0)),
            precio_total=Decimal(str(detalle.get("precio_total") or 0)),
            precio_extranjero=Decimal(str(detalle.get("precio_extranjero") or 0)),
            precio_total_extranjero=Decimal(str(detalle.get("precio_total_extranjero") or 0)),
            numero_linea=detalle.get("numero_linea"),
            numero_documento=detalle.get("numero_documento"),
            tipo_documento=detalle.get("tipo_documento"),
            estado_siguiente=detalle.get("estado_siguiente"),
            estado_anterior=detalle.get("estado_anterior"),
            producto_nombre=detalle.get("nombre_producto"),
        )

    def _insertar_detalles(
        self,
        cursor,
        pedido_id: int,
        detalles: List[VentaDetalleCreate],
        moneda: str,
        trm_valor: Decimal,
    ) -> None:
        trm = Decimal(str(trm_valor or 1))
        moneda_normalizada = (moneda or "COP").upper()
        for indice, detalle in enumerate(detalles, start=1):
            self._insertar_detalle(cursor, pedido_id, detalle, indice, moneda_normalizada, trm)

    def _insertar_detalle(
        self,
        cursor,
        pedido_id: int,
        detalle: VentaDetalleCreate,
        indice: int,
        moneda: str,
        trm: Decimal,
    ) -> None:
        cantidad = Decimal(str(detalle.cantidad_solicitada))
        precio_unitario = Decimal(str(detalle.precio_unitario))
        precio_total = cantidad * precio_unitario
        cantidad_confirmada = (
            Decimal(str(detalle.cantidad_confirmada)) if detalle.cantidad_confirmada is not None else cantidad
        )
        if moneda == "COP" or trm <= 0:
            precio_extranjero = Decimal("0")
            precio_total_extranjero = Decimal("0")
        else:
            precio_extranjero = precio_unitario / trm
            precio_total_extranjero = precio_total / trm

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
                detalle.numero_linea or indice,
                str(cantidad),
                str(cantidad_confirmada),
                str(precio_unitario),
                str(precio_total),
                str(precio_extranjero),
                str(precio_total_extranjero),
                detalle.numero_documento,
                detalle.tipo_documento,
                detalle.estado_siguiente or 1,
                detalle.estado_anterior or 1,
            ),
        )
