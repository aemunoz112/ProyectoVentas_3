from collections import defaultdict
from decimal import Decimal
from typing import Dict, List

import mysql.connector
from fastapi import HTTPException

from app.config.db_config import get_db_connection
from app.models.dimensionesProducto_model import DimensionesProductoCreateModel, DimensionesProductoResponseModel
from app.models.producto_model import (
    ProductoCreateModel,
    ProductoResponseModel,
    ProductoUpdateModel,
)


class ProductoController:

    def listar_productos(self) -> List[ProductoResponseModel]:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT id, codigo_producto, nombre_producto, descripcion,
                       categoria, unidad_medida, estado, created_at, updated_at
                FROM productos
                ORDER BY created_at DESC, id DESC
                """
            )
            productos = cursor.fetchall() or []
            if not productos:
                return []

            ids = [prod.get("id", 0) for prod in productos if prod.get("id")]
            dimensiones = self._obtener_dimensiones(cursor, ids)
            return [self._mapear_producto(prod, dimensiones.get(prod.get("id", 0), [])) for prod in productos]
        except mysql.connector.Error as err:
            print(f"Error al listar productos: {err}")
            raise HTTPException(status_code=500, detail="Error al obtener los productos")
        finally:
            cursor.close()
            conn.close()

    def obtener_producto(self, producto_id: int) -> ProductoResponseModel:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT id, codigo_producto, nombre_producto, descripcion,
                       categoria, unidad_medida, estado, created_at, updated_at
                FROM productos
                WHERE id = %s
                """,
                (producto_id,),
            )
            producto = cursor.fetchone()
            if not producto:
                raise HTTPException(status_code=404, detail="Producto no encontrado")

            dimensiones = self._obtener_dimensiones(cursor, [producto_id]).get(producto_id, [])
            return self._mapear_producto(producto, dimensiones)
        except mysql.connector.Error as err:
            print(f"Error al obtener producto: {err}")
            raise HTTPException(status_code=500, detail="Error al obtener el producto")
        finally:
            cursor.close()
            conn.close()

    def crear_producto(self, producto: ProductoCreateModel) -> ProductoResponseModel:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            conn.start_transaction()
            cursor.execute(
                """
                INSERT INTO productos
                    (codigo_producto, nombre_producto, descripcion, categoria, unidad_medida, estado, created_at, updated_at)
                VALUES
                    (%s, %s, %s, %s, %s, %s, NOW(), NOW())
                """,
                (
                    producto.codigo_producto,
                    producto.nombre_producto,
                    producto.descripcion,
                    producto.categoria,
                    producto.unidad_medida,
                    producto.estado or "Activo",
                ),
            )
            producto_id = cursor.lastrowid
            self._insertar_dimensiones(cursor, producto_id, producto.dimensiones)
            conn.commit()
            return self.obtener_producto(producto_id)
        except mysql.connector.Error as err:
            print(f"Error al crear producto: {err}")
            conn.rollback()
            if err.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
                raise HTTPException(status_code=400, detail="El código del producto ya está registrado")
            raise HTTPException(status_code=500, detail="Error al crear el producto")
        finally:
            cursor.close()
            conn.close()

    def actualizar_producto(self, producto_id: int, producto: ProductoUpdateModel) -> ProductoResponseModel:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM productos WHERE id = %s", (producto_id,))
            actual = cursor.fetchone()
            if not actual:
                raise HTTPException(status_code=404, detail="Producto no encontrado")

            campos = []
            valores = []
            for campo in [
                "codigo_producto",
                "nombre_producto",
                "descripcion",
                "categoria",
                "unidad_medida",
                "estado",
            ]:
                valor = getattr(producto, campo, None)
                if valor is not None:
                    campos.append(f"{campo} = %s")
                    valores.append(valor)

            if campos:
                valores.extend([producto_id])
                cursor.execute(
                    f"""
                    UPDATE productos
                    SET {', '.join(campos)}, updated_at = NOW()
                    WHERE id = %s
                    """,
                    tuple(valores),
                )

            if producto.dimensiones is not None:
                cursor.execute("DELETE FROM dimensiones_producto WHERE id_producto = %s", (producto_id,))
                self._insertar_dimensiones(cursor, producto_id, producto.dimensiones)

            conn.commit()
            return self.obtener_producto(producto_id)
        except mysql.connector.Error as err:
            print(f"Error al actualizar producto: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar el producto")
        finally:
            cursor.close()
            conn.close()

    def eliminar_producto(self, producto_id: int):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM productos WHERE id = %s", (producto_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Producto no encontrado")

            cursor.execute("DELETE FROM dimensiones_producto WHERE id_producto = %s", (producto_id,))
            cursor.execute("DELETE FROM productos WHERE id = %s", (producto_id,))
            conn.commit()
            return {"mensaje": "Producto eliminado correctamente"}
        except mysql.connector.Error as err:
            print(f"Error al eliminar producto: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al eliminar el producto")
        finally:
            cursor.close()
            conn.close()

    def _obtener_dimensiones(self, cursor, ids: List[int]) -> Dict[int, List[DimensionesProductoResponseModel]]:
        if not ids:
            return {}
        marcadores = ",".join(["%s"] * len(ids))
        cursor.execute(
            f"""
            SELECT id, id_producto, ancho, espesor, diametro_interno, diametro_externo,
                   created_at, updated_at
            FROM dimensiones_producto
            WHERE id_producto IN ({marcadores})
            ORDER BY id_producto, id
            """,
            tuple(ids),
        )
        filas = cursor.fetchall() or []
        agrupado: Dict[int, List[DimensionesProductoResponseModel]] = defaultdict(list)
        for fila in filas:
            agrupado[fila.get("id_producto", 0)].append(self._mapear_dimension(fila))
        return agrupado

    def _mapear_producto(self, datos: dict, dimensiones: List[DimensionesProductoResponseModel]) -> ProductoResponseModel:
        return ProductoResponseModel(
            id=datos.get("id", 0),
            codigo_producto=datos.get("codigo_producto", ""),
            nombre_producto=datos.get("nombre_producto", ""),
            descripcion=datos.get("descripcion"),
            categoria=datos.get("categoria"),
            unidad_medida=datos.get("unidad_medida"),
            estado=datos.get("estado"),
            created_at=datos.get("created_at"),
            updated_at=datos.get("updated_at"),
            dimensiones=dimensiones,
        )

    def _mapear_dimension(self, datos: dict) -> DimensionesProductoResponseModel:
        return DimensionesProductoResponseModel(
            id=datos.get("id", 0),
            id_producto=datos.get("id_producto", 0),
            ancho=self._decimal_a_decimal(datos.get("ancho")),
            espesor=self._decimal_a_decimal(datos.get("espesor")),
            diametro_interno=self._decimal_a_decimal(datos.get("diametro_interno")),
            diametro_externo=self._decimal_a_decimal(datos.get("diametro_externo")),
            estado="Activo",
            created_at=datos.get("created_at"),
            updated_at=datos.get("updated_at"),
        )

    def _insertar_dimensiones(
        self,
        cursor,
        producto_id: int,
        dimensiones: List[DimensionesProductoCreateModel],
    ) -> None:
        for dimension in dimensiones or []:
            cursor.execute(
                """
                INSERT INTO dimensiones_producto
                    (id_producto, ancho, espesor, diametro_interno, diametro_externo, created_at, updated_at)
                VALUES
                    (%s, %s, %s, %s, %s, NOW(), NOW())
                """,
                (
                    producto_id,
                    str(dimension.ancho),
                    str(dimension.espesor),
                    str(dimension.diametro_interno),
                    str(dimension.diametro_externo),
                ),
            )

    @staticmethod
    def _decimal_a_decimal(valor) -> Decimal:
        if valor is None:
            return Decimal("0")
        if isinstance(valor, Decimal):
            return valor
        return Decimal(str(valor))