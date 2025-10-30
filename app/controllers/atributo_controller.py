from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import mysql.connector
from app.config.db_config import get_db_connection

class AtributoController:

    def create_atributo(self, atributo):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
            INSERT INTO atributos (nombre, descripcion, estado)
            VALUES (%s, %s, %s)
            """
            values = (
                atributo.nombre,
                atributo.descripcion,
                atributo.estado
            )

            cursor.execute(query, values)
            conn.commit()

            return {"mensaje": "Atributo creado exitosamente"}

        except mysql.connector.Error as err:
            print(f"Error al crear atributo: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al crear atributo")

        finally:
            conn.close()

    def get_atributo(self, atributo_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM atributos WHERE id = %s", (atributo_id,))
            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Atributo no encontrado")

            content = {
                "id": int(result[0]),
                "nombre": result[1],
                "descripcion": result[2],
                "estado": result[3],
                "created_at": str(result[4]),
                "updated_at": str(result[5])
            }

            return jsonable_encoder(content)

        except mysql.connector.Error as err:
            print(f"Error al obtener atributo: {err}")
            raise HTTPException(status_code=500, detail="Error al obtener atributo")

        finally:
            conn.close()

    def get_atributos(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM atributos")
            result = cursor.fetchall()

            if not result:
                raise HTTPException(status_code=404, detail="No se encontraron atributos")

            payload = [
                {
                    "id": data[0],
                    "nombre": data[1],
                    "descripcion": data[2],
                    "estado": data[3],
                    "created_at": str(data[4]),
                    "updated_at": str(data[5])
                } for data in result
            ]

            return {"resultado": jsonable_encoder(payload)}

        except mysql.connector.Error as err:
            print(f"Error al listar atributos: {err}")
            raise HTTPException(status_code=500, detail="Error al listar atributos")

        finally:
            conn.close()

    def get_atributos_activos(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM atributos WHERE estado = 'Activo'")
            result = cursor.fetchall()

            if not result:
                raise HTTPException(status_code=404, detail="No se encontraron atributos activos")

            payload = [
                {
                    "id": data[0],
                    "nombre": data[1],
                    "descripcion": data[2],
                    "estado": data[3],
                    "created_at": str(data[4]),
                    "updated_at": str(data[5])
                } for data in result
            ]

            return {"resultado": jsonable_encoder(payload)}

        except mysql.connector.Error as err:
            print(f"Error al listar atributos activos: {err}")
            raise HTTPException(status_code=500, detail="Error al listar atributos activos")

        finally:
            conn.close()

    def update_atributo(self, atributo_id: int, atributo):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM atributos WHERE id = %s", (atributo_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Atributo no encontrado")

            query = """
            UPDATE atributos
            SET nombre = %s,
                descripcion = %s,
                estado = %s
            WHERE id = %s
            """
            values = (
                atributo.nombre,
                atributo.descripcion,
                atributo.estado,
                atributo_id
            )

            cursor.execute(query, values)
            conn.commit()

            return {"mensaje": f"Atributo con ID {atributo_id} actualizado correctamente"}

        except mysql.connector.Error as err:
            print(f"Error al actualizar atributo: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar atributo")

        finally:
            conn.close()

    def delete_atributo(self, atributo_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM atributos WHERE id = %s", (atributo_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Atributo no encontrado")

            cursor.execute("DELETE FROM atributos WHERE id = %s", (atributo_id,))
            conn.commit()

            return {"mensaje": f"Atributo con ID {atributo_id} eliminado correctamente"}

        except mysql.connector.Error as err:
            print(f"Error al eliminar atributo: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al eliminar atributo")

        finally:
            conn.close()