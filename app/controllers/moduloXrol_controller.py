from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import mysql.connector
import json
from app.config.db_config import get_db_connection

class ModuloXRolController:

    def create_modulo_x_rol(self, modulo_rol):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
            INSERT INTO moduloXrol (rol_id, modulo_id, permisos, estado)
            VALUES (%s, %s, %s, %s)
            """
            values = (
                modulo_rol.rol_id,
                modulo_rol.modulo_id,
                json.dumps(modulo_rol.permisos) if isinstance(modulo_rol.permisos, list) else modulo_rol.permisos,
                modulo_rol.estado
            )

            cursor.execute(query, values)
            conn.commit()

            return {"mensaje": "Relación módulo-rol creada exitosamente"}

        except mysql.connector.Error as err:
            print(f"Error al crear relación módulo-rol: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al crear relación módulo-rol")

        finally:
            conn.close()

    def get_modulo_x_rol(self, modulo_rol_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM moduloXrol WHERE id = %s", (modulo_rol_id,))
            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Relación módulo-rol no encontrada")

            content = {
                "id": int(result[0]),
                "rol_id": int(result[1]),
                "modulo_id": int(result[2]),
                "permisos": result[3],
                "estado": result[4],
                "created_at": str(result[5]),
                "updated_at": str(result[6])
            }

            return jsonable_encoder(content)

        except mysql.connector.Error as err:
            print(f"Error al obtener relación módulo-rol: {err}")
            raise HTTPException(status_code=500, detail="Error al obtener relación módulo-rol")

        finally:
            conn.close()

    def get_modulos_x_rol(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM moduloXrol")
            result = cursor.fetchall()

            if not result:
                raise HTTPException(status_code=404, detail="No se encontraron relaciones módulo-rol")

            payload = [
                {
                    "id": data[0],
                    "rol_id": data[1],
                    "modulo_id": data[2],
                    "permisos": data[3],
                    "estado": data[4],
                    "created_at": str(data[5]),
                    "updated_at": str(data[6])
                } for data in result
            ]

            return {"resultado": jsonable_encoder(payload)}

        except mysql.connector.Error as err:
            print(f"Error al listar relaciones módulo-rol: {err}")
            raise HTTPException(status_code=500, detail="Error al listar relaciones módulo-rol")

        finally:
            conn.close()

    def get_modulos_by_rol(self, rol_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM moduloXrol WHERE rol_id = %s", (rol_id,))
            result = cursor.fetchall()

            if not result:
                raise HTTPException(status_code=404, detail=f"No se encontraron módulos para el rol {rol_id}")

            payload = [
                {
                    "id": data[0],
                    "rol_id": data[1],
                    "modulo_id": data[2],
                    "permisos": data[3],
                    "estado": data[4],
                    "created_at": str(data[5]),
                    "updated_at": str(data[6])
                } for data in result
            ]

            return {"resultado": jsonable_encoder(payload)}

        except mysql.connector.Error as err:
            print(f"Error al obtener módulos por rol: {err}")
            raise HTTPException(status_code=500, detail="Error al obtener módulos por rol")

        finally:
            conn.close()

    def get_roles_by_modulo(self, modulo_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM moduloXrol WHERE modulo_id = %s", (modulo_id,))
            result = cursor.fetchall()

            if not result:
                raise HTTPException(status_code=404, detail=f"No se encontraron roles para el módulo {modulo_id}")

            payload = [
                {
                    "id": data[0],
                    "rol_id": data[1],
                    "modulo_id": data[2],
                    "permisos": data[3],
                    "estado": data[4],
                    "created_at": str(data[5]),
                    "updated_at": str(data[6])
                } for data in result
            ]

            return {"resultado": jsonable_encoder(payload)}

        except mysql.connector.Error as err:
            print(f"Error al obtener roles por módulo: {err}")
            raise HTTPException(status_code=500, detail="Error al obtener roles por módulo")

        finally:
            conn.close()

    def update_modulo_x_rol(self, modulo_rol_id: int, modulo_rol):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM moduloXrol WHERE id = %s", (modulo_rol_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Relación módulo-rol no encontrada")

            query = """
            UPDATE moduloXrol
            SET rol_id = %s,
                modulo_id = %s,
                permisos = %s,
                estado = %s
            WHERE id = %s
            """
            values = (
                modulo_rol.rol_id,
                modulo_rol.modulo_id,
                modulo_rol.permisos,
                modulo_rol.estado,
                modulo_rol_id
            )

            cursor.execute(query, values)
            conn.commit()

            return {"mensaje": f"Relación módulo-rol con ID {modulo_rol_id} actualizada correctamente"}

        except mysql.connector.Error as err:
            print(f"Error al actualizar relación módulo-rol: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar relación módulo-rol")

        finally:
            conn.close()

    def delete_modulo_x_rol(self, modulo_rol_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM moduloXrol WHERE id = %s", (modulo_rol_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Relación módulo-rol no encontrada")

            cursor.execute("DELETE FROM moduloXrol WHERE id = %s", (modulo_rol_id,))
            conn.commit()

            return {"mensaje": f"Relación módulo-rol con ID {modulo_rol_id} eliminada correctamente"}

        except mysql.connector.Error as err:
            print(f"Error al eliminar relación módulo-rol: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al eliminar relación módulo-rol")

        finally:
            conn.close()