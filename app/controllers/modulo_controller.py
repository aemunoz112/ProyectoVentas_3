from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import mysql.connector
from app.config.db_config import get_db_connection

class ModulosController:

    def create_modulo(self, modulo):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
            INSERT INTO modulos (nombre, descripcion, ruta, estado)
            VALUES (%s, %s, %s, %s)
            """
            values = (
                modulo.nombre,
                modulo.descripcion,
                modulo.ruta,
                modulo.estado
            )

            cursor.execute(query, values)
            conn.commit()

            return {"mensaje": "Módulo creado exitosamente"}

        except mysql.connector.Error as err:
            print(f"Error al crear módulo: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al crear módulo")

        finally:
            conn.close()

    def get_modulo(self, modulo_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM modulos WHERE id = %s", (modulo_id,))
            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Módulo no encontrado")

            content = {
                "id": int(result[0]),
                "nombre": result[1],
                "descripcion": result[2],
                "ruta": result[3],
                "estado": result[4],
                "created_at": str(result[5]),
                "updated_at": str(result[6])
            }

            return jsonable_encoder(content)

        except mysql.connector.Error as err:
            print(f"Error al obtener módulo: {err}")
            raise HTTPException(status_code=500, detail="Error al obtener módulo")

        finally:
            conn.close()

    def get_modulos(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM modulos")
            result = cursor.fetchall()

            if not result:
                raise HTTPException(status_code=404, detail="No se encontraron módulos")

            payload = [
                {
                    "id": data[0],
                    "nombre": data[1],
                    "descripcion": data[2],
                    "ruta": data[3],
                    "estado": data[4],
                    "created_at": str(data[5]),
                    "updated_at": str(data[6])
                } for data in result
            ]

            return {"resultado": jsonable_encoder(payload)}

        except mysql.connector.Error as err:
            print(f"Error al listar módulos: {err}")
            raise HTTPException(status_code=500, detail="Error al listar módulos")

        finally:
            conn.close()

    def get_modulos_activos(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM modulos WHERE estado = 'Activo'")
            result = cursor.fetchall()

            if not result:
                raise HTTPException(status_code=404, detail="No se encontraron módulos activos")

            payload = [
                {
                    "id": data[0],
                    "nombre": data[1],
                    "descripcion": data[2],
                    "ruta": data[3],
                    "estado": data[4],
                    "created_at": str(data[5]),
                    "updated_at": str(data[6])
                } for data in result
            ]

            return {"resultado": jsonable_encoder(payload)}

        except mysql.connector.Error as err:
            print(f"Error al listar módulos activos: {err}")
            raise HTTPException(status_code=500, detail="Error al listar módulos activos")

        finally:
            conn.close()

    def update_modulo(self, modulo_id: int, modulo):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM modulos WHERE id = %s", (modulo_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Módulo no encontrado")

            query = """
            UPDATE modulos
            SET nombre = %s,
                descripcion = %s,
                ruta = %s,
                estado = %s
            WHERE id = %s
            """
            values = (
                modulo.nombre,
                modulo.descripcion,
                modulo.ruta,
                modulo.estado,
                modulo_id
            )

            cursor.execute(query, values)
            conn.commit()

            return {"mensaje": f"Módulo con ID {modulo_id} actualizado correctamente"}

        except mysql.connector.Error as err:
            print(f"Error al actualizar módulo: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar módulo")

        finally:
            conn.close()

    def delete_modulo(self, modulo_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM modulos WHERE id = %s", (modulo_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Módulo no encontrado")

            cursor.execute("DELETE FROM modulos WHERE id = %s", (modulo_id,))
            conn.commit()

            return {"mensaje": f"Módulo con ID {modulo_id} eliminado correctamente"}

        except mysql.connector.Error as err:
            print(f"Error al eliminar módulo: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al eliminar módulo")

        finally:
            conn.close()