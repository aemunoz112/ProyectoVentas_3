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
            INSERT INTO usuarios (nombres, apellidos, email, telefono, cedula, contrasena, rol_id, estado, departamento_id, ciudad_id, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
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
                usuario.departamento_id,
                usuario.ciudad_id
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
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            # Manejar campos opcionales (departamento_id y ciudad_id pueden no existir aún)
            content = {
                "id": int(result["id"]),
                "nombres": result["nombres"],
                "apellidos": result["apellidos"],
                "email": result["email"],
                "telefono": result["telefono"],
                "cedula": result["cedula"],
                "contrasena": result["contrasena"],
                "rol_id": int(result["rol_id"]),
                "estado": result["estado"],
                "departamento_id": int(result["departamento_id"]) if result.get("departamento_id") is not None else None,
                "ciudad_id": int(result["ciudad_id"]) if result.get("ciudad_id") is not None else None,
                "created_at": str(result["created_at"]) if result.get("created_at") else None,
                "updated_at": str(result["updated_at"]) if result.get("updated_at") else None
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
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios")
            result = cursor.fetchall()

            if not result:
                raise HTTPException(status_code=404, detail="No se encontraron usuarios")

            payload = [
                {
                    "id": int(data["id"]),
                    "nombres": data["nombres"],
                    "apellidos": data["apellidos"],
                    "email": data["email"],
                    "telefono": data["telefono"],
                    "cedula": data["cedula"],
                    "rol_id": int(data["rol_id"]),
                    "estado": data["estado"],
                    "departamento_id": int(data["departamento_id"]) if data.get("departamento_id") is not None else None,
                    "ciudad_id": int(data["ciudad_id"]) if data.get("ciudad_id") is not None else None,
                    "created_at": str(data["created_at"]) if data.get("created_at") else None,
                    "updated_at": str(data["updated_at"]) if data.get("updated_at") else None
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
                departamento_id = %s,
                ciudad_id = %s,
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
                usuario.departamento_id,
                usuario.ciudad_id,
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