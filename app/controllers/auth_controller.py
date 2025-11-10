from fastapi import HTTPException
import mysql.connector
import json

from app.config.db_config import get_db_connection
from app.controllers.menu_controller import MenuController


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

            menu_controller = MenuController()
            try:
                menu_tree = menu_controller.get_menu_tree_by_role(rol_data["id"])
            except HTTPException as menu_error:
                # Si la tabla aún no existe o no hay configuración, permitimos el ingreso sin menú
                print(f"Advertencia al obtener menú para el rol {rol_data['id']}: {menu_error.detail}")
                menu_tree = []

            return {
                "usuario": usuario_data,
                "rol": rol_data,
                "menu": menu_tree,
                "modulos": menu_tree
            }

        except mysql.connector.Error as err:
            print(f"Error en autenticación (MySQL): {err}")
            raise HTTPException(status_code=500, detail="Error al autenticar usuario")
        except Exception as err:
            print(f"Error inesperado en autenticación: {err}")
            raise HTTPException(status_code=500, detail="Error inesperado al autenticar")

        finally:
            conn.close()

