from fastapi import HTTPException
import mysql.connector
import json

from app.config.db_config import get_db_connection


class AuthController:

    def login(self, credenciales):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Buscar usuario activo con email y contraseña suministrados
            cursor.execute(
                """
                SELECT id, nombres, apellidos, email, telefono, cedula, rol_id, estado
                FROM usuarios
                WHERE email = %s AND contrasena = %s AND estado = 'Activo'
                """,
                (credenciales.email, credenciales.password)
            )
            usuario = cursor.fetchone()

            if not usuario:
                raise HTTPException(status_code=401, detail="Credenciales inválidas")

            usuario_data = {
                "id": int(usuario[0]),
                "nombres": usuario[1],
                "apellidos": usuario[2],
                "email": usuario[3],
                "telefono": usuario[4],
                "cedula": usuario[5],
                "rol_id": int(usuario[6]),
                "estado": usuario[7]
            }

            # Información del rol
            cursor.execute(
                """
                SELECT id, nombre, descripcion, estado
                FROM roles
                WHERE id = %s
                """,
                (usuario_data["rol_id"],)
            )
            rol = cursor.fetchone()

            if not rol:
                raise HTTPException(status_code=500, detail="El rol asignado no existe")

            rol_data = {
                "id": int(rol[0]),
                "nombre": rol[1],
                "descripcion": rol[2],
                "estado": rol[3]
            }

            # Modulos asociados al rol
            cursor.execute(
                """
                SELECT
                    mxr.id,
                    m.id,
                    m.nombre,
                    m.descripcion,
                    m.ruta,
                    mxr.permisos,
                    mxr.estado
                FROM moduloXrol mxr
                JOIN modulos m ON m.id = mxr.modulo_id
                WHERE mxr.rol_id = %s
                """,
                (rol_data["id"],)
            )
            modulos_result = cursor.fetchall()

            modulos = []
            for modulo in modulos_result:
                permisos_raw = modulo[5] or "[]"
                if isinstance(permisos_raw, str):
                    try:
                        permisos = json.loads(permisos_raw)
                    except json.JSONDecodeError:
                        permisos = [permisos_raw]
                else:
                    permisos = permisos_raw

                modulos.append(
                    {
                        "id": modulo[0],
                        "modulo_id": modulo[1],
                        "nombre_modulo": modulo[2],
                        "descripcion": modulo[3],
                        "ruta": modulo[4],
                        "permisos": permisos,
                        "estado": modulo[6]
                    }
                )

            return {
                "usuario": usuario_data,
                "rol": rol_data,
                "modulos": modulos
            }

        except mysql.connector.Error as err:
            print(f"Error en autenticación (MySQL): {err}")
            raise HTTPException(status_code=500, detail="Error al autenticar usuario")
        except Exception as err:
            print(f"Error inesperado en autenticación: {err}")
            raise HTTPException(status_code=500, detail="Error inesperado al autenticar")

        finally:
            conn.close()

