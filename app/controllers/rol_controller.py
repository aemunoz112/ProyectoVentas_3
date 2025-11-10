from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import mysql.connector
import json

from app.config.db_config import get_db_connection


class RolController:

    def create_rol(self, rol):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            insert_query = """
            INSERT INTO roles (nombre, descripcion, estado, created_at, updated_at)
            VALUES (%s, %s, %s, NOW(), NOW())
            """
            cursor.execute(insert_query, (rol.nombre, rol.descripcion, rol.estado or "Activo"))
            conn.commit()
            rol_id = cursor.lastrowid

            if rol.modulos:
                self._sincronizar_modulos(cursor, rol_id, rol.modulos, reemplazar=False)
                conn.commit()

            return {"mensaje": "Rol creado exitosamente", "id": rol_id}

        except mysql.connector.Error as err:
            print(f"Error al crear rol: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al crear rol")

        finally:
            conn.close()

    def get_rol(self, rol_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, descripcion, estado, created_at, updated_at FROM roles WHERE id = %s", (rol_id,))
            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Rol no encontrado")

            content = {
                "id": int(result[0]),
                "nombre": result[1],
                "descripcion": result[2],
                "estado": result[3],
                "created_at": str(result[4]),
                "updated_at": str(result[5]),
                "modulos": self._obtener_modulos_por_rol(cursor, rol_id)
            }

            return jsonable_encoder(content)

        except mysql.connector.Error as err:
            print(f"Error al obtener rol: {err}")
            raise HTTPException(status_code=500, detail="Error al obtener rol")

        finally:
            conn.close()

    def get_roles(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, descripcion, estado, created_at, updated_at FROM roles")
            result = cursor.fetchall()

            if not result:
                raise HTTPException(status_code=404, detail="No se encontraron roles")

            payload = []
            for data in result:
                rol_id = data[0]
                payload.append(
                    {
                        "id": rol_id,
                        "nombre": data[1],
                        "descripcion": data[2],
                        "estado": data[3],
                        "created_at": str(data[4]),
                        "updated_at": str(data[5]),
                        "modulos": self._obtener_modulos_por_rol(cursor, rol_id)
                    }
                )

            return {"resultado": jsonable_encoder(payload)}

        except mysql.connector.Error as err:
            print(f"Error al listar roles: {err}")
            raise HTTPException(status_code=500, detail="Error al listar roles")

        finally:
            conn.close()

    def update_rol(self, rol_id: int, rol):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM roles WHERE id = %s", (rol_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Rol no encontrado")

            update_query = """
            UPDATE roles
            SET nombre = %s,
                descripcion = %s,
                estado = %s,
                updated_at = NOW()
            WHERE id = %s
            """
            cursor.execute(update_query, (rol.nombre, rol.descripcion, rol.estado or "Activo", rol_id))

            self._sincronizar_modulos(cursor, rol_id, rol.modulos, reemplazar=True)

            conn.commit()

            return {"mensaje": f"Rol con ID {rol_id} actualizado correctamente"}

        except mysql.connector.Error as err:
            print(f"Error al actualizar rol: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar rol")

        finally:
            conn.close()

    def delete_rol(self, rol_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM roles WHERE id = %s", (rol_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Rol no encontrado")

            cursor.execute("DELETE FROM moduloXrol WHERE rol_id = %s", (rol_id,))
            cursor.execute("DELETE FROM roles WHERE id = %s", (rol_id,))
            conn.commit()

            return {"mensaje": f"Rol con ID {rol_id} eliminado correctamente"}

        except mysql.connector.Error as err:
            print(f"Error al eliminar rol: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al eliminar rol")

        finally:
            conn.close()

    def _obtener_modulos_por_rol(self, cursor, rol_id: int):
        cursor.execute("""
            SELECT mxr.id, mxr.modulo_id, m.nombre, mxr.permisos, mxr.estado, mxr.created_at, mxr.updated_at
            FROM moduloXrol mxr
            JOIN modulos m ON m.id = mxr.modulo_id
            WHERE mxr.rol_id = %s
        """, (rol_id,))
        modulos = cursor.fetchall()

        payload = []
        for data in modulos:
            permisos = data[3]
            if isinstance(permisos, str):
                try:
                    permisos = json.loads(permisos)
                except json.JSONDecodeError:
                    permisos = [permisos]

            payload.append(
                {
                    "id": data[0],
                    "modulo_id": data[1],
                    "nombre_modulo": data[2],
                    "permisos": permisos or [],
                    "estado": data[4],
                    "created_at": str(data[5]) if data[5] else None,
                    "updated_at": str(data[6]) if data[6] else None
                }
            )
        return payload

    def _sincronizar_modulos(self, cursor, rol_id: int, modulos, reemplazar: bool = False):
        if reemplazar:
            cursor.execute("DELETE FROM moduloXrol WHERE rol_id = %s", (rol_id,))

        if not modulos:
            return

        insert_query = """
        INSERT INTO moduloXrol (rol_id, modulo_id, permisos, estado, created_at, updated_at)
        VALUES (%s, %s, %s, %s, NOW(), NOW())
        """
        for modulo in modulos:
            permisos = modulo.permisos if modulo.permisos else []
            cursor.execute(
                insert_query,
                (
                    rol_id,
                    modulo.modulo_id,
                    json.dumps(permisos),
                    modulo.estado or "Activo"
                )
            )

