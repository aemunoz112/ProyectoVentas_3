from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import mysql.connector
from app.config.db_config import get_db_connection
from typing import Dict, Optional
import traceback

class UsuarioController:

    def _cargar_atributos_usuario(self, cursor, usuario_id: int) -> Dict[str, str]:
        """Método auxiliar para cargar los atributos de un usuario"""
        try:
            # El cursor ya está configurado como dictionary=True desde el método que lo llama
            cursor.execute("""
                SELECT a.nombre, axu.valor
                FROM atributoXusuario axu
                INNER JOIN atributos a ON axu.atributo_id = a.id
                WHERE axu.usuario_id = %s AND axu.estado = 'Activo'
            """, (usuario_id,))
            resultados = cursor.fetchall()
            
            atributos_dict = {}
            for row in resultados:
                # El cursor está en modo dictionary=True, así que accedemos por nombre
                nombre_atributo = row.get("nombre") if isinstance(row, dict) else (row[0] if row else None)
                valor = row.get("valor") if isinstance(row, dict) else (row[1] if row and len(row) > 1 else None)
                if nombre_atributo and valor:
                    atributos_dict[nombre_atributo] = valor
            
            return atributos_dict
        except Exception as e:
            print(f"Error al cargar atributos del usuario {usuario_id}: {e}")
            print(traceback.format_exc())
            return {}

    def _guardar_atributos_usuario(self, cursor, usuario_id: int, atributos: Optional[Dict[str, str]]):
        """Método auxiliar para guardar los atributos de un usuario"""
        if not atributos:
            return
        
        try:
            for nombre_atributo, valor in atributos.items():
                if not valor or not nombre_atributo:  # Saltar valores vacíos
                    continue
                
                # Buscar o crear el atributo
                cursor.execute("SELECT id FROM atributos WHERE nombre = %s", (nombre_atributo,))
                atributo_result = cursor.fetchone()
                
                atributo_id = None
                if atributo_result:
                    atributo_id = atributo_result.get("id") if isinstance(atributo_result, dict) else atributo_result[0]
                else:
                    # Crear nuevo atributo si no existe
                    cursor.execute("""
                        INSERT INTO atributos (nombre, descripcion, estado)
                        VALUES (%s, %s, 'Activo')
                    """, (nombre_atributo, f"Atributo {nombre_atributo}"))
                    atributo_id = cursor.lastrowid
                
                # Verificar si ya existe una relación para este usuario y atributo
                cursor.execute("""
                    SELECT id FROM atributoXusuario 
                    WHERE usuario_id = %s AND atributo_id = %s
                """, (usuario_id, atributo_id))
                existe = cursor.fetchone()
                
                if existe:
                    # Actualizar valor existente
                    cursor.execute("""
                        UPDATE atributoXusuario
                        SET valor = %s, updated_at = NOW()
                        WHERE usuario_id = %s AND atributo_id = %s
                    """, (valor, usuario_id, atributo_id))
                else:
                    # Crear nueva relación
                    cursor.execute("""
                        INSERT INTO atributoXusuario (usuario_id, atributo_id, tipo, valor, estado)
                        VALUES (%s, %s, 'texto', %s, 'Activo')
                    """, (usuario_id, atributo_id, valor))
        except Exception as e:
            print(f"Error al guardar atributos del usuario {usuario_id}: {e}")
            print(traceback.format_exc())
            raise  # Re-lanzar la excepción para que sea capturada en create_user

    def create_user(self, usuario):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            conn.start_transaction()

            # Si viene cedula en atributos, usarla también en el campo cedula
            cedula_valor = usuario.cedula
            if usuario.atributos:
                # Si hay "Cédula" o "Cedula" en atributos, usar ese valor
                if 'Cédula' in usuario.atributos and usuario.atributos['Cédula']:
                    cedula_valor = usuario.atributos['Cédula']
                elif 'Cedula' in usuario.atributos and usuario.atributos['Cedula']:
                    cedula_valor = usuario.atributos['Cedula']

            query = """
            INSERT INTO usuarios (nombres, apellidos, email, telefono, cedula, contrasena, rol_id, estado, departamento_id, ciudad_id, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            """
            values = (
                usuario.nombres,
                usuario.apellidos,
                usuario.email,
                usuario.telefono,
                cedula_valor,
                usuario.contrasena,
                usuario.rol_id,
                usuario.estado,
                usuario.departamento_id,
                usuario.ciudad_id
            )

            cursor.execute(query, values)
            usuario_id = cursor.lastrowid

            # Guardar atributos si existen
            if usuario.atributos:
                self._guardar_atributos_usuario(cursor, usuario_id, usuario.atributos)

            conn.commit()
            return {"mensaje": "Usuario creado exitosamente"}

        except mysql.connector.Error as err:
            print(f"Error MySQL al crear usuario: {err}")
            print(f"Error completo: {traceback.format_exc()}")
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear usuario: {str(err)}")
        except Exception as e:
            print(f"Error inesperado al crear usuario: {e}")
            print(f"Error completo: {traceback.format_exc()}")
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear usuario: {str(e)}")
        finally:
            if conn:
                conn.close()

    def get_user(self, user_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            # Cargar atributos del usuario
            atributos_dict = self._cargar_atributos_usuario(cursor, user_id)

            # Si hay cédula en atributos, también ponerla en el campo cedula
            cedula_valor = result["cedula"]
            if 'Cédula' in atributos_dict and atributos_dict['Cédula']:
                cedula_valor = atributos_dict['Cédula']
            elif 'Cedula' in atributos_dict and atributos_dict['Cedula']:
                cedula_valor = atributos_dict['Cedula']

            # Manejar campos opcionales (departamento_id y ciudad_id pueden no existir aún)
            content = {
                "id": int(result["id"]),
                "nombres": result["nombres"],
                "apellidos": result["apellidos"],
                "email": result["email"],
                "telefono": result["telefono"],
                "cedula": cedula_valor,
                "contrasena": result["contrasena"],
                "rol_id": int(result["rol_id"]),
                "estado": result["estado"],
                "departamento_id": int(result["departamento_id"]) if result.get("departamento_id") is not None else None,
                "ciudad_id": int(result["ciudad_id"]) if result.get("ciudad_id") is not None else None,
                "atributos": atributos_dict,
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

            payload = []
            for data in result:
                # Cargar atributos de cada usuario
                atributos_dict = self._cargar_atributos_usuario(cursor, data["id"])

                # Si hay cédula en atributos, también ponerla en el campo cedula
                cedula_valor = data["cedula"]
                if 'Cédula' in atributos_dict and atributos_dict['Cédula']:
                    cedula_valor = atributos_dict['Cédula']
                elif 'Cedula' in atributos_dict and atributos_dict['Cedula']:
                    cedula_valor = atributos_dict['Cedula']

                usuario_dict = {
                    "id": int(data["id"]),
                    "nombres": data["nombres"],
                    "apellidos": data["apellidos"],
                    "email": data["email"],
                    "telefono": data["telefono"],
                    "cedula": cedula_valor,
                    "rol_id": int(data["rol_id"]),
                    "estado": data["estado"],
                    "departamento_id": int(data["departamento_id"]) if data.get("departamento_id") is not None else None,
                    "ciudad_id": int(data["ciudad_id"]) if data.get("ciudad_id") is not None else None,
                    "atributos": atributos_dict,
                    "created_at": str(data["created_at"]) if data.get("created_at") else None,
                    "updated_at": str(data["updated_at"]) if data.get("updated_at") else None
                }
                payload.append(usuario_dict)

            return {"resultado": jsonable_encoder(payload)}

        except mysql.connector.Error as err:
            print(f"Error al listar usuarios: {err}")
            raise HTTPException(status_code=500, detail="Error al listar usuarios")

        finally:
            conn.close()

    def update_user(self, user_id: int, usuario):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            conn.start_transaction()

            cursor.execute("SELECT id FROM usuarios WHERE id = %s", (user_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            # Si viene cedula en atributos, usarla también en el campo cedula
            cedula_valor = usuario.cedula
            if usuario.atributos:
                # Si hay "Cédula" o "Cedula" en atributos, usar ese valor
                if 'Cédula' in usuario.atributos and usuario.atributos['Cédula']:
                    cedula_valor = usuario.atributos['Cédula']
                elif 'Cedula' in usuario.atributos and usuario.atributos['Cedula']:
                    cedula_valor = usuario.atributos['Cedula']

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
                cedula_valor,
                usuario.contrasena,
                usuario.rol_id,
                usuario.estado,
                usuario.departamento_id,
                usuario.ciudad_id,
                user_id
            )

            cursor.execute(query, values)

            # Eliminar atributos existentes del usuario (solo los que están activos)
            if usuario.atributos is not None:
                cursor.execute("""
                    DELETE FROM atributoXusuario 
                    WHERE usuario_id = %s
                """, (user_id,))
                
                # Guardar nuevos atributos
                self._guardar_atributos_usuario(cursor, user_id, usuario.atributos)

            conn.commit()

            return {"mensaje": f"Usuario con ID {user_id} actualizado correctamente"}

        except mysql.connector.Error as err:
            print(f"Error MySQL al actualizar usuario: {err}")
            print(f"Error completo: {traceback.format_exc()}")
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar usuario: {str(err)}")
        except Exception as e:
            print(f"Error inesperado al actualizar usuario: {e}")
            print(f"Error completo: {traceback.format_exc()}")
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar usuario: {str(e)}")
        finally:
            if conn:
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