from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import mysql.connector
from app.config.db_config import get_db_connection

class AtributoXUsuarioController:

    def create_atributo_x_usuario(self, atributo_usuario):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
            INSERT INTO atributoXusuario (usuario_id, atributo_id, tipo, valor, estado)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (
                atributo_usuario.usuario_id,
                atributo_usuario.atributo_id,
                atributo_usuario.tipo,
                atributo_usuario.valor,
                atributo_usuario.estado
            )

            cursor.execute(query, values)
            conn.commit()

            return {"mensaje": "Relación atributo-usuario creada exitosamente"}

        except mysql.connector.Error as err:
            print(f"Error al crear relación atributo-usuario: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al crear relación atributo-usuario")

        finally:
            conn.close()

    def get_atributo_x_usuario(self, atributo_usuario_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM atributoXusuario WHERE id = %s", (atributo_usuario_id,))
            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Relación atributo-usuario no encontrada")

            content = {
                "id": int(result[0]),
                "usuario_id": int(result[1]),
                "atributo_id": int(result[2]),
                "tipo": result[3],
                "valor": result[4],
                "estado": result[5],
                "created_at": str(result[6]),
                "updated_at": str(result[7])
            }

            return jsonable_encoder(content)

        except mysql.connector.Error as err:
            print(f"Error al obtener relación atributo-usuario: {err}")
            raise HTTPException(status_code=500, detail="Error al obtener relación atributo-usuario")

        finally:
            conn.close()

    def get_atributos_x_usuario(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM atributoXusuario")
            result = cursor.fetchall()

            if not result:
                raise HTTPException(status_code=404, detail="No se encontraron relaciones atributo-usuario")

            payload = [
                {
                    "id": data[0],
                    "usuario_id": data[1],
                    "atributo_id": data[2],
                    "tipo": data[3],
                    "valor": data[4],
                    "estado": data[5],
                    "created_at": str(data[6]),
                    "updated_at": str(data[7])
                } for data in result
            ]

            return {"resultado": jsonable_encoder(payload)}

        except mysql.connector.Error as err:
            print(f"Error al listar relaciones atributo-usuario: {err}")
            raise HTTPException(status_code=500, detail="Error al listar relaciones atributo-usuario")

        finally:
            conn.close()

    def get_atributos_by_usuario(self, usuario_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM atributoXusuario WHERE usuario_id = %s", (usuario_id,))
            result = cursor.fetchall()

            if not result:
                raise HTTPException(status_code=404, detail=f"No se encontraron atributos para el usuario {usuario_id}")

            payload = [
                {
                    "id": data[0],
                    "usuario_id": data[1],
                    "atributo_id": data[2],
                    "tipo": data[3],
                    "valor": data[4],
                    "estado": data[5],
                    "created_at": str(data[6]),
                    "updated_at": str(data[7])
                } for data in result
            ]

            return {"resultado": jsonable_encoder(payload)}

        except mysql.connector.Error as err:
            print(f"Error al obtener atributos por usuario: {err}")
            raise HTTPException(status_code=500, detail="Error al obtener atributos por usuario")

        finally:
            conn.close()

    def get_usuarios_by_atributo(self, atributo_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM atributoXusuario WHERE atributo_id = %s", (atributo_id,))
            result = cursor.fetchall()

            if not result:
                raise HTTPException(status_code=404, detail=f"No se encontraron usuarios para el atributo {atributo_id}")

            payload = [
                {
                    "id": data[0],
                    "usuario_id": data[1],
                    "atributo_id": data[2],
                    "tipo": data[3],
                    "valor": data[4],
                    "estado": data[5],
                    "created_at": str(data[6]),
                    "updated_at": str(data[7])
                } for data in result
            ]

            return {"resultado": jsonable_encoder(payload)}

        except mysql.connector.Error as err:
            print(f"Error al obtener usuarios por atributo: {err}")
            raise HTTPException(status_code=500, detail="Error al obtener usuarios por atributo")

        finally:
            conn.close()

    def update_atributo_x_usuario(self, atributo_usuario_id: int, atributo_usuario):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM atributoXusuario WHERE id = %s", (atributo_usuario_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Relación atributo-usuario no encontrada")

            query = """
            UPDATE atributoXusuario
            SET usuario_id = %s,
                atributo_id = %s,
                tipo = %s,
                valor = %s,
                estado = %s
            WHERE id = %s
            """
            values = (
                atributo_usuario.usuario_id,
                atributo_usuario.atributo_id,
                atributo_usuario.tipo,
                atributo_usuario.valor,
                atributo_usuario.estado,
                atributo_usuario_id
            )

            cursor.execute(query, values)
            conn.commit()

            return {"mensaje": f"Relación atributo-usuario con ID {atributo_usuario_id} actualizada correctamente"}

        except mysql.connector.Error as err:
            print(f"Error al actualizar relación atributo-usuario: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar relación atributo-usuario")

        finally:
            conn.close()

    def delete_atributo_x_usuario(self, atributo_usuario_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM atributoXusuario WHERE id = %s", (atributo_usuario_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Relación atributo-usuario no encontrada")

            cursor.execute("DELETE FROM atributoXusuario WHERE id = %s", (atributo_usuario_id,))
            conn.commit()

            return {"mensaje": f"Relación atributo-usuario con ID {atributo_usuario_id} eliminada correctamente"}

        except mysql.connector.Error as err:
            print(f"Error al eliminar relación atributo-usuario: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al eliminar relación atributo-usuario")

        finally:
            conn.close()