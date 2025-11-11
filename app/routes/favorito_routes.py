from typing import Optional

from fastapi import APIRouter, Query

from app.controllers.favorito_controller import FavoritoController
from app.models.favorito_model import FavoritoCreate, FavoritoResponse, FavoritoUpdate

router = APIRouter()
controller = FavoritoController()


@router.get("/usuarios/{usuario_id}/favoritos", response_model=list[FavoritoResponse])
async def listar_favoritos(usuario_id: int, rol_id: Optional[int] = Query(default=None)):
    return controller.listar_favoritos(usuario_id, rol_id)


@router.post(
    "/usuarios/{usuario_id}/favoritos",
    response_model=FavoritoResponse,
    status_code=201,
)
async def crear_favorito(usuario_id: int, payload: FavoritoCreate, rol_id: Optional[int] = Query(default=None)):
    return controller.crear_favorito(usuario_id, payload, rol_id)


@router.patch(
    "/usuarios/{usuario_id}/favoritos/{favorito_id}",
    response_model=FavoritoResponse,
)
async def actualizar_favorito(
    usuario_id: int,
    favorito_id: int,
    payload: FavoritoUpdate,
    rol_id: Optional[int] = Query(default=None),
):
    return controller.actualizar_favorito(usuario_id, favorito_id, payload, rol_id)


@router.delete("/usuarios/{usuario_id}/favoritos/{favorito_id}")
async def eliminar_favorito(usuario_id: int, favorito_id: int):
    return controller.eliminar_favorito(usuario_id, favorito_id)
