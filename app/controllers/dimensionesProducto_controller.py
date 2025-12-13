from decimal import Decimal
from typing import List

import mysql.connector
from fastapi import HTTPException

from app.config.db_config import get_db_connection
from app.models.dimensionesProducto_model import (
    DimensionesProductoCreateModel,
    DimensionesProductoResponseModel,
    DimensionesProductoUpdateModel,
)


class DimensionProductoController:

    def create_dimension(self, dimension: DimensionesProductoCreateModel) -> DimensionesProductoResponseModel:
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id FROM productos WHERE id = %s", (dimension.id_producto,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Producto asociado no encontrado")

            cursor.execute(
                """
                INSERT INTO dimensiones_producto
                    (id_producto, ancho, espesor, diametro_interno, diametro_externo, created_at, updated_at)
                VALUES
                    (%s, %s, %s, %s, %s, NOW(), NOW())
                """,
                (
                    dimension.id_producto,
                    str(dimension.ancho),
                    str(dimension.espesor),
                    str(dimension.diametro_interno),
                    str(dimension.diametro_externo),
                ),
            )
            conn.commit()
            nuevo_id = cursor.lastrowid
            return self.get_dimension(nuevo_id)
        except mysql.connector.Error as err:
            print(f"Error al crear dimensión: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al crear dimensión")
        finally:
            cursor.close()
            conn.close()

    def get_dimension(self, dimension_id: int) -> DimensionesProductoResponseModel:
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM dimensiones_producto WHERE id = %s", (dimension_id,))
            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Dimensión no encontrada")

            return self._mapear_dimension(result)
        except mysql.connector.Error as err:
            print(f"Error al obtener dimensión: {err}")
            raise HTTPException(status_code=500, detail="Error al obtener dimensión")
        finally:
            cursor.close()
            conn.close()

    def get_dimensiones(self) -> List[DimensionesProductoResponseModel]:
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM dimensiones_producto")
            result = cursor.fetchall() or []
            return [self._mapear_dimension(data) for data in result]
        except mysql.connector.Error as err:
            print(f"Error al listar dimensiones: {err}")
            raise HTTPException(status_code=500, detail="Error al listar dimensiones")
        finally:
            cursor.close()
            conn.close()

    def update_dimension(self, dimension_id: int, dimension: DimensionesProductoUpdateModel) -> DimensionesProductoResponseModel:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM dimensiones_producto WHERE id = %s", (dimension_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Dimensión no encontrada")

            campos = []
            valores = []
            for campo in [
                "ancho",
                "espesor",
                "diametro_interno",
                "diametro_externo",
                "estado",
            ]:
                valor = getattr(dimension, campo, None)
                if valor is not None:
                    campos.append(f"{campo} = %s")
                    valores.append(str(valor) if isinstance(valor, Decimal) else valor)

            if campos:
                valores.extend([dimension_id])
                cursor.execute(
                    f"""
                    UPDATE dimensiones_producto
                    SET {', '.join(campos)}, updated_at = NOW()
                    WHERE id = %s
                    """,
                    tuple(valores),
                )
                conn.commit()

            return self.get_dimension(dimension_id)
        except mysql.connector.Error as err:
            print(f"Error al actualizar dimensión: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar dimensión")
        finally:
            cursor.close()
            conn.close()

    def delete_dimension(self, dimension_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM dimensiones_producto WHERE id = %s", (dimension_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Dimensión no encontrada")

            cursor.execute("DELETE FROM dimensiones_producto WHERE id = %s", (dimension_id,))
            conn.commit()
            return {"mensaje": f"Dimensión con ID {dimension_id} eliminada correctamente"}
        except mysql.connector.Error as err:
            print(f"Error al eliminar dimensión: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al eliminar dimensión")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def _decimal_a_decimal(valor) -> Decimal:
        """Convierte un valor a Decimal, manejando None y otros tipos."""
        if valor is None:
            return Decimal("0")
        if isinstance(valor, Decimal):
            return valor
        return Decimal(str(valor))

    @staticmethod
    def _mapear_dimension(datos: dict) -> DimensionesProductoResponseModel:
        return DimensionesProductoResponseModel(
            id=datos.get("id", 0),
            id_producto=datos.get("id_producto", 0),
            ancho=DimensionProductoController._decimal_a_decimal(datos.get("ancho")),
            espesor=DimensionProductoController._decimal_a_decimal(datos.get("espesor")),
            diametro_interno=DimensionProductoController._decimal_a_decimal(datos.get("diametro_interno")),
            diametro_externo=DimensionProductoController._decimal_a_decimal(datos.get("diametro_externo")),
            estado="Activo",
            created_at=datos.get("created_at"),
            updated_at=datos.get("updated_at"),
        )
