from typing import List, Optional

import mysql.connector
from fastapi import HTTPException

from app.config.db_config import get_db_connection
from app.models.favorito_model import FavoritoCreate, FavoritoResponse, FavoritoUpdate


class FavoritoController:

    def listar_favoritos(self, usuario_id: int, rol_id: Optional[int] = None) -> List[FavoritoResponse]:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            params: List[int] = [usuario_id]
            rol_join_condition = ""
            if rol_id is not None:
                rol_join_condition = "AND mxr.rol_id = %s"
                params.insert(0, rol_id)
            query = f"""
                SELECT
                    f.id,
                    f.usuario_id,
                    f.menu_item_id,
                    f.alias,
                    f.orden,
                    mi.nombre   AS nombre_menu,
                    mi.descripcion AS descripcion_menu,
                    mi.ruta,
                    mi.icono,
                    mxr.puede_ver,
                    mxr.puede_crear,
                    mxr.puede_editar,
                    mxr.puede_eliminar
                FROM usuario_favoritos f
                JOIN menu_items mi ON mi.id = f.menu_item_id
                LEFT JOIN menu_itemXrol mxr ON mxr.menu_item_id = f.menu_item_id {rol_join_condition}
                WHERE f.usuario_id = %s AND mi.estado = 'Activo'
                ORDER BY
                    CASE WHEN f.orden IS NULL THEN 1 ELSE 0 END,
                    f.orden,
                    mi.nombre
            """
            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()
            favoritos: List[FavoritoResponse] = []
            for row in rows:
                favoritos.append(self._row_a_favorito(row))
            return favoritos
        except mysql.connector.Error as err:
            print(f"Error al listar favoritos: {err}")
            raise HTTPException(status_code=500, detail="Error al obtener favoritos")
        finally:
            cursor.close()
            conn.close()

    def crear_favorito(
        self,
        usuario_id: int,
        data: FavoritoCreate,
        rol_id: Optional[int] = None,
    ) -> FavoritoResponse:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id FROM usuarios WHERE id = %s", (usuario_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            cursor.execute("SELECT id, estado FROM menu_items WHERE id = %s", (data.menu_item_id,))
            menu = cursor.fetchone()
            if not menu:
                raise HTTPException(status_code=404, detail="Elemento de menú no encontrado")
            if menu.get("estado") != "Activo":
                raise HTTPException(status_code=400, detail="El elemento de menú no está activo")

            cursor.execute(
                "SELECT id FROM usuario_favoritos WHERE usuario_id = %s AND menu_item_id = %s",
                (usuario_id, data.menu_item_id),
            )
            existente = cursor.fetchone()
            if existente:
                raise HTTPException(status_code=409, detail="El favorito ya existe")

            orden = data.orden
            if orden is None:
                cursor.execute(
                    "SELECT COALESCE(MAX(orden), 0) + 1 AS siguiente FROM usuario_favoritos WHERE usuario_id = %s",
                    (usuario_id,),
                )
                orden_row = cursor.fetchone()
                orden = orden_row["siguiente"] if orden_row and orden_row.get("siguiente") else 1

            cursor.execute(
                """
                INSERT INTO usuario_favoritos (usuario_id, menu_item_id, alias, orden, created_at, updated_at)
                VALUES (%s, %s, %s, %s, NOW(), NOW())
                """,
                (usuario_id, data.menu_item_id, data.alias, orden),
            )
            conn.commit()
            nuevo_id = cursor.lastrowid
            return self.obtener_favorito(cursor, nuevo_id, usuario_id, rol_id)
        except mysql.connector.Error as err:
            print(f"Error al crear favorito: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al crear favorito")
        finally:
            cursor.close()
            conn.close()

    def actualizar_favorito(
        self,
        usuario_id: int,
        favorito_id: int,
        data: FavoritoUpdate,
        rol_id: Optional[int] = None,
    ) -> FavoritoResponse:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT id FROM usuario_favoritos WHERE id = %s AND usuario_id = %s",
                (favorito_id, usuario_id),
            )
            favorito = cursor.fetchone()
            if not favorito:
                raise HTTPException(status_code=404, detail="Favorito no encontrado")

            campos = []
            valores = []
            if data.alias is not None:
                campos.append("alias = %s")
                valores.append(data.alias or None)
            if data.orden is not None:
                campos.append("orden = %s")
                valores.append(data.orden)

            if campos:
                valores.extend([favorito_id, usuario_id])
                cursor.execute(
                    f"""
                    UPDATE usuario_favoritos
                    SET {', '.join(campos)}, updated_at = NOW()
                    WHERE id = %s AND usuario_id = %s
                    """,
                    tuple(valores),
                )
                conn.commit()

            return self.obtener_favorito(cursor, favorito_id, usuario_id, rol_id)
        except mysql.connector.Error as err:
            print(f"Error al actualizar favorito: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar favorito")
        finally:
            cursor.close()
            conn.close()

    def eliminar_favorito(self, usuario_id: int, favorito_id: int):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT id FROM usuario_favoritos WHERE id = %s AND usuario_id = %s",
                (favorito_id, usuario_id),
            )
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Favorito no encontrado")

            cursor.execute(
                "DELETE FROM usuario_favoritos WHERE id = %s AND usuario_id = %s",
                (favorito_id, usuario_id),
            )
            conn.commit()
            return {"mensaje": "Favorito eliminado correctamente"}
        except mysql.connector.Error as err:
            print(f"Error al eliminar favorito: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al eliminar favorito")
        finally:
            cursor.close()
            conn.close()

    def obtener_favorito(
        self,
        cursor,
        favorito_id: int,
        usuario_id: int,
        rol_id: Optional[int] = None,
    ) -> FavoritoResponse:
        params: List[int] = [favorito_id, usuario_id]
        rol_join_condition = ""
        if rol_id is not None:
            rol_join_condition = "AND mxr.rol_id = %s"
            params.insert(0, rol_id)
        query = f"""
            SELECT
                f.id,
                f.usuario_id,
                f.menu_item_id,
                f.alias,
                f.orden,
                mi.nombre   AS nombre_menu,
                mi.descripcion AS descripcion_menu,
                mi.ruta,
                mi.icono,
                mxr.puede_ver,
                mxr.puede_crear,
                mxr.puede_editar,
                mxr.puede_eliminar
            FROM usuario_favoritos f
            JOIN menu_items mi ON mi.id = f.menu_item_id
            LEFT JOIN menu_itemXrol mxr ON mxr.menu_item_id = f.menu_item_id {rol_join_condition}
            WHERE f.id = %s AND f.usuario_id = %s
        """
        cursor.execute(query, tuple(params))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Favorito no encontrado")
        return self._row_a_favorito(row)

    @staticmethod
    def _row_a_favorito(row: dict) -> FavoritoResponse:
        permisos = []
        if row.get("puede_ver"):
            permisos.append("ver")
        if row.get("puede_crear"):
            permisos.append("crear")
        if row.get("puede_editar"):
            permisos.append("editar")
        if row.get("puede_eliminar"):
            permisos.append("eliminar")
        return FavoritoResponse(
            id=row["id"],
            usuario_id=row["usuario_id"],
            menu_item_id=row["menu_item_id"],
            alias=row.get("alias"),
            orden=row.get("orden"),
            nombre_menu=row.get("nombre_menu"),
            descripcion_menu=row.get("descripcion_menu"),
            ruta=row.get("ruta"),
            icono=row.get("icono"),
            permisos=permisos,
        )
