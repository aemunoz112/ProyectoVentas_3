from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import mysql.connector
from app.config.db_config import get_db_connection

class DimensionProductoController:

    def create_dimension(self, dimension):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
            INSERT INTO dimensiones_producto (id_producto, ancho, espesor, diametro_interno, diametro_externo)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (
                dimension.id_producto,
                dimension.ancho,
                dimension.espesor,
                dimension.diametro_interno,
                dimension.diametro_externo
            )

            cursor.execute(query, values)
            conn.commit()

            return {"mensaje": "Dimensión creada exitosamente"}

        except mysql.connector.Error as err:
            print(f"Error al crear dimensión: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al crear dimensión")

        finally:
            conn.close()

    def get_dimension(self, dimension_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM dimensiones_producto WHERE id = %s", (dimension_id,))
            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Dimensión no encontrada")

            content = {
                "id": result[0],
                "id_producto": result[1],
                "ancho": result[2],
                "espesor": result[3],
                "diametro_interno": result[4],
                "diametro_externo": result[5],
                "created_at": str(result[6]),
                "updated_at": str(result[7])
            }

            return jsonable_encoder(content)

        except mysql.connector.Error as err:
            print(f"Error al obtener dimensión: {err}")
            raise HTTPException(status_code=500, detail="Error al obtener dimensión")

        finally:
            conn.close()

    def get_dimensiones(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM dimensiones_producto")
            result = cursor.fetchall()

            if not result:
                raise HTTPException(status_code=404, detail="No se encontraron dimensiones")

            payload = [
                {
                    "id": data[0],
                    "id_producto": data[1],
                    "ancho": data[2],
                    "espesor": data[3],
                    "diametro_interno": data[4],
                    "diametro_externo": data[5],
                    "created_at": str(data[6]),
                    "updated_at": str(data[7])
                }
                for data in result
            ]

            return {"resultado": jsonable_encoder(payload)}

        except mysql.connector.Error as err:
            print(f"Error al listar dimensiones: {err}")
            raise HTTPException(status_code=500, detail="Error al listar dimensiones")

        finally:
            conn.close()

    def update_dimension(self, dimension_id: int, dimension):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM dimensiones_producto WHERE id = %s", (dimension_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Dimensión no encontrada")

            query = """
            UPDATE dimensiones_producto
            SET id_producto = %s,
                ancho = %s,
                espesor = %s,
                diametro_interno = %s,
                diametro_externo = %s
            WHERE id = %s
            """
            values = (
                dimension.id_producto,
                dimension.ancho,
                dimension.espesor,
                dimension.diametro_interno,
                dimension.diametro_externo,
                dimension_id
            )

            cursor.execute(query, values)
            conn.commit()

            return {"mensaje": f"Dimensión con ID {dimension_id} actualizada correctamente"}

        except mysql.connector.Error as err:
            print(f"Error al actualizar dimensión: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar dimensión")

        finally:
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
            conn.close()
