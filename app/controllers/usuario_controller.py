from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import mysql.connector
from app.config.db_config import get_db_connection

class UsuarioController:

    def create_user(self, usuario):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
            INSERT INTO usuarios (nombres, apellidos, email, telefono, cedula, contrasena, rol_id, estado, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            """
            values = (
                usuario.nombres,
                usuario.apellidos,
                usuario.email,
                usuario.telefono,
                usuario.cedula,
                usuario.contrasena,
                usuario.rol_id,
                usuario.estado
            )

            cursor.execute(query, values)
            conn.commit()

            return {"mensaje": "Usuario creado exitosamente"}

        except mysql.connector.Error as err:
            print(f"Error al crear usuario: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al crear usuario")

        finally:
            conn.close()

    def get_user(self, user_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            content = {
                "id": int(result[0]),
                "nombres": result[1],
                "apellidos": result[2],
                "email": result[3],
                "telefono": result[4],
                "cedula": result[5],
                "contrasena": result[6],
                "rol_id": int(result[7]),
                "estado": result[8],
                "created_at": str(result[9]),
                "updated_at": str(result[10])
            }

            return jsonable_encoder(content)

        except mysql.connector.Error as err:
            print(f"Error al obtener usuario: {err}")
            raise HTTPException(status_code=500, detail="Error al obtener usuario")

        finally:
            conn.close()

    def get_users(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios")
            result = cursor.fetchall()

            if not result:
                raise HTTPException(status_code=404, detail="No se encontraron usuarios")

            payload = [
                {
                    "id": data[0],
                    "nombres": data[1],
                    "apellidos": data[2],
                    "email": data[3],
                    "telefono": data[4],
                    "cedula": data[5],
                    "rol_id": data[7],
                    "estado": data[8],
                    "created_at": str(data[9]),
                    "updated_at": str(data[10])
                } for data in result
            ]

            return {"resultado": jsonable_encoder(payload)}

        except mysql.connector.Error as err:
            print(f"Error al listar usuarios: {err}")
            raise HTTPException(status_code=500, detail="Error al listar usuarios")

        finally:
            conn.close()

    def update_user(self, user_id: int, usuario):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM usuarios WHERE id = %s", (user_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            query = """
            UPDATE usuarios
            SET nombres = %s,
                apellidos = %s,
                email = %s,
                telefono = %s,
                cedula = %s,
                contrasena = %s,
                rol_id = %s,
                estado = %s,
                updated_at = NOW()
            WHERE id = %s
            """
            values = (
                usuario.nombres,
                usuario.apellidos,
                usuario.email,
                usuario.telefono,
                usuario.cedula,
                usuario.contrasena,
                usuario.rol_id,
                usuario.estado,
                user_id
            )

            cursor.execute(query, values)
            conn.commit()

            return {"mensaje": f"Usuario con ID {user_id} actualizado correctamente"}

        except mysql.connector.Error as err:
            print(f"Error al actualizar usuario: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar usuario")

        finally:
            conn.close()

    def delete_user(self, user_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM usuarios WHERE id = %s", (user_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
            conn.commit()

            return {"mensaje": f"Usuario con ID {user_id} eliminado correctamente"}

        except mysql.connector.Error as err:
            print(f"Error al eliminar usuario: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al eliminar usuario")

        finally:
            conn.close()