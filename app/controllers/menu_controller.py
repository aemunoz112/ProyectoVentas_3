from typing import Dict, List, Optional

from fastapi import HTTPException
import mysql.connector

from app.config.db_config import get_db_connection
from app.models.menu_model import (
    MenuAssignment,
    MenuItemCreate,
    MenuItemTree,
    MenuItemUpdate,
)


class MenuController:

    def get_menu_tree_by_role(self, rol_id: int) -> List[MenuItemTree]:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT
                    mi.id,
                    mi.modulo_id,
                    mi.parent_id,
                    mi.nombre,
                    mi.descripcion,
                    mi.ruta,
                    mi.icono,
                    mi.tipo,
                    mi.nivel,
                    mi.orden,
                    mi.estado,
                    mxr.puede_ver,
                    mxr.puede_crear,
                    mxr.puede_editar,
                    mxr.puede_eliminar
                FROM menu_items mi
                JOIN menu_itemXrol mxr ON mxr.menu_item_id = mi.id
                WHERE mxr.rol_id = %s AND mi.estado = 'Activo'
                ORDER BY mi.nivel, mi.orden, mi.nombre
                """,
                (rol_id,),
            )
            rows = cursor.fetchall()
            return self._build_tree(rows, include_permissions=True)
        except mysql.connector.Error as err:
            print(f"Error al obtener menú por rol: {err}")
            raise HTTPException(status_code=500, detail="Error al obtener menú por rol")
        finally:
            cursor.close()
            conn.close()

    def get_full_menu_tree(self) -> List[MenuItemTree]:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT
                    mi.id,
                    mi.modulo_id,
                    mi.parent_id,
                    mi.nombre,
                    mi.descripcion,
                    mi.ruta,
                    mi.icono,
                    mi.tipo,
                    mi.nivel,
                    mi.orden,
                    mi.estado,
                    NULL AS puede_ver,
                    NULL AS puede_crear,
                    NULL AS puede_editar,
                    NULL AS puede_eliminar
                FROM menu_items mi
                ORDER BY mi.nivel, mi.orden, mi.nombre
                """
            )
            rows = cursor.fetchall()
            return self._build_tree(rows, include_permissions=False)
        except mysql.connector.Error as err:
            print(f"Error al obtener el árbol completo de menú: {err}")
            raise HTTPException(status_code=500, detail="Error al obtener el menú")
        finally:
            cursor.close()
            conn.close()

    def list_menu_items(self) -> Dict[str, List[Dict]]:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT
                    mi.id,
                    mi.nombre,
                    mi.parent_id,
                    mi.modulo_id,
                    mi.nivel,
                    mi.orden,
                    mi.estado
                FROM menu_items mi
                ORDER BY mi.nivel, mi.orden, mi.nombre
                """
            )
            rows = cursor.fetchall()
            return {"resultado": rows}
        except mysql.connector.Error as err:
            print(f"Error al listar elementos de menú: {err}")
            raise HTTPException(status_code=500, detail="Error al listar menú")
        finally:
            cursor.close()
            conn.close()

    def create_menu_item(self, item: MenuItemCreate):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            nivel = 1
            if item.parent_id:
                cursor.execute(
                    "SELECT nivel FROM menu_items WHERE id = %s", (item.parent_id,)
                )
                parent = cursor.fetchone()
                if not parent:
                    raise HTTPException(status_code=404, detail="Elemento padre no encontrado")
                nivel = int(parent[0]) + 1
                if nivel > 5:
                    raise HTTPException(status_code=400, detail="No se permite un nivel mayor a 5")

            cursor.execute(
                """
                INSERT INTO menu_items
                (modulo_id, parent_id, nombre, descripcion, ruta, icono, tipo, nivel, orden, estado, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                """,
                (
                    item.modulo_id,
                    item.parent_id,
                    item.nombre,
                    item.descripcion,
                    item.ruta,
                    item.icono,
                    item.tipo or "pagina",
                    nivel,
                    item.orden or 0,
                    item.estado or "Activo",
                ),
            )
            conn.commit()
            return {"mensaje": "Elemento de menú creado correctamente"}
        except mysql.connector.Error as err:
            print(f"Error al crear elemento de menú: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al crear elemento de menú")
        finally:
            cursor.close()
            conn.close()

    def update_menu_item(self, item_id: int, item: MenuItemUpdate):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM menu_items WHERE id = %s", (item_id,))
            current = cursor.fetchone()
            if not current:
                raise HTTPException(status_code=404, detail="Elemento de menú no encontrado")

            parent_id = item.parent_id if item.parent_id is not None else current["parent_id"]
            if parent_id == item_id:
                raise HTTPException(status_code=400, detail="Un elemento no puede ser su propio padre")
            nivel = current["nivel"]

            if parent_id:
                cursor.execute("SELECT nivel FROM menu_items WHERE id = %s", (parent_id,))
                parent = cursor.fetchone()
                if not parent:
                    raise HTTPException(status_code=404, detail="Elemento padre no encontrado")
                nivel_parent = parent["nivel"] if isinstance(parent, dict) else parent[0]
                nivel = int(nivel_parent) + 1
                if nivel > 5:
                    raise HTTPException(status_code=400, detail="No se permite un nivel mayor a 5")
            else:
                nivel = 1

            cursor.execute(
                """
                UPDATE menu_items
                SET modulo_id = %s,
                    parent_id = %s,
                    nombre = %s,
                    descripcion = %s,
                    ruta = %s,
                    icono = %s,
                    tipo = %s,
                    nivel = %s,
                    orden = %s,
                    estado = %s,
                    updated_at = NOW()
                WHERE id = %s
                """,
                (
                    item.modulo_id if item.modulo_id is not None else current["modulo_id"],
                    parent_id,
                    item.nombre if item.nombre is not None else current["nombre"],
                    item.descripcion if item.descripcion is not None else current["descripcion"],
                    item.ruta if item.ruta is not None else current["ruta"],
                    item.icono if item.icono is not None else current["icono"],
                    item.tipo if item.tipo is not None else current["tipo"],
                    nivel,
                    item.orden if item.orden is not None else current["orden"],
                    item.estado if item.estado is not None else current["estado"],
                    item_id,
                ),
            )
            conn.commit()
            return {"mensaje": "Elemento de menú actualizado correctamente"}
        except mysql.connector.Error as err:
            print(f"Error al actualizar elemento de menú: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al actualizar elemento de menú")
        finally:
            cursor.close()
            conn.close()

    def delete_menu_item(self, item_id: int):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM menu_items WHERE id = %s", (item_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Elemento de menú no encontrado")

            cursor.execute("DELETE FROM menu_items WHERE id = %s", (item_id,))
            conn.commit()
            return {"mensaje": "Elemento de menú eliminado correctamente"}
        except mysql.connector.Error as err:
            print(f"Error al eliminar elemento de menú: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al eliminar elemento de menú")
        finally:
            cursor.close()
            conn.close()

    def assign_menu_item(self, item_id: int, assignment: MenuAssignment):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM menu_items WHERE id = %s", (item_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Elemento de menú no encontrado")

            cursor.execute(
                """
                INSERT INTO menu_itemXrol
                (rol_id, menu_item_id, puede_ver, puede_crear, puede_editar, puede_eliminar, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
                ON DUPLICATE KEY UPDATE
                    puede_ver = VALUES(puede_ver),
                    puede_crear = VALUES(puede_crear),
                    puede_editar = VALUES(puede_editar),
                    puede_eliminar = VALUES(puede_eliminar),
                    updated_at = NOW()
                """,
                (
                    assignment.rol_id,
                    item_id,
                    assignment.puede_ver,
                    assignment.puede_crear,
                    assignment.puede_editar,
                    assignment.puede_eliminar,
                ),
            )
            conn.commit()
            return {"mensaje": "Permisos asignados correctamente"}
        except mysql.connector.Error as err:
            print(f"Error al asignar menú a rol: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error al asignar permisos al menú")
        finally:
            cursor.close()
            conn.close()

    def _build_tree(self, rows: List[Dict], include_permissions: bool) -> List[MenuItemTree]:
        nodes: Dict[int, Dict] = {}
        for row in rows:
            permisos = self._permisos_desde_row(row) if include_permissions else []
            nodes[row["id"]] = {
                "id": row["id"],
                "modulo_id": row["modulo_id"],
                "parent_id": row["parent_id"],
                "nombre": row["nombre"],
                "descripcion": row["descripcion"],
                "ruta": row["ruta"],
                "icono": row["icono"],
                "tipo": row["tipo"],
                "nivel": row["nivel"],
                "orden": row["orden"],
                "estado": row["estado"],
                "permisos": permisos,
                "hijos": [],
            }

        tree: List[Dict] = []
        for node in nodes.values():
            parent_id = node["parent_id"]
            if parent_id and parent_id in nodes:
                nodes[parent_id]["hijos"].append(node)
            else:
                tree.append(node)

        return self._filtrar_y_ordenar(tree, include_permissions)

    def _filtrar_y_ordenar(self, nodes: List[Dict], include_permissions: bool) -> List[MenuItemTree]:
        resultado: List[MenuItemTree] = []
        for node in nodes:
            hijos = self._filtrar_y_ordenar(node["hijos"], include_permissions)
            node["hijos"] = hijos

            permisos = node.get("permisos", [])
            visible = True
            if include_permissions:
                visible = ("ver" in permisos) or bool(hijos)

            if visible:
                hijos_sorted = sorted(hijos, key=lambda h: (h.orden, h.nombre.lower()))
                node["hijos"] = hijos_sorted
                resultado.append(MenuItemTree(**node))

        return sorted(resultado, key=lambda n: (n.orden, n.nombre.lower()))

    @staticmethod
    def _permisos_desde_row(row: Dict) -> List[str]:
        permisos = []
        if row.get("puede_ver"):
            permisos.append("ver")
        if row.get("puede_crear"):
            permisos.append("crear")
        if row.get("puede_editar"):
            permisos.append("editar")
        if row.get("puede_eliminar"):
            permisos.append("eliminar")
        return permisos

