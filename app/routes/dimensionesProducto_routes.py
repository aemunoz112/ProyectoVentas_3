from typing import List

from fastapi import APIRouter, status

from app.controllers.dimensionesProducto_controller import DimensionProductoController
from app.models.dimensionesProducto_model import (
    DimensionesProductoCreateModel,
    DimensionesProductoResponseModel,
    DimensionesProductoUpdateModel,
)

router = APIRouter(prefix="/dimensiones", tags=["dimensiones"])
controller = DimensionProductoController()


@router.get("/", response_model=List[DimensionesProductoResponseModel])
async def listar_dimensiones():
    return controller.get_dimensiones()


@router.get("/{dimension_id}", response_model=DimensionesProductoResponseModel)
async def obtener_dimension(dimension_id: int):
    return controller.get_dimension(dimension_id)


@router.post(
    "/",
    response_model=DimensionesProductoResponseModel,
    status_code=status.HTTP_201_CREATED,
)
async def crear_dimension(dimension: DimensionesProductoCreateModel):
    return controller.create_dimension(dimension)


@router.put("/{dimension_id}", response_model=DimensionesProductoResponseModel)
async def actualizar_dimension(dimension_id: int, dimension: DimensionesProductoUpdateModel):
    return controller.update_dimension(dimension_id, dimension)


@router.delete("/{dimension_id}")
async def eliminar_dimension(dimension_id: int):
    return controller.delete_dimension(dimension_id)
