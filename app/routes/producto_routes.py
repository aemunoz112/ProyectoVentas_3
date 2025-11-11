from typing import List

from fastapi import APIRouter, status

from app.controllers.producto_controller import ProductoController
from app.models.producto_model import (
    ProductoCreateModel,
    ProductoResponseModel,
    ProductoUpdateModel,
)

router = APIRouter(prefix="/productos", tags=["productos"])
controller = ProductoController()


@router.get("/", response_model=List[ProductoResponseModel])
async def listar_productos():
    return controller.listar_productos()


@router.get("/{producto_id}", response_model=ProductoResponseModel)
async def obtener_producto(producto_id: int):
    return controller.obtener_producto(producto_id)


@router.post("/", response_model=ProductoResponseModel, status_code=status.HTTP_201_CREATED)
async def crear_producto(producto: ProductoCreateModel):
    return controller.crear_producto(producto)


@router.put("/{producto_id}", response_model=ProductoResponseModel)
async def actualizar_producto(producto_id: int, producto: ProductoUpdateModel):
    return controller.actualizar_producto(producto_id, producto)


@router.delete("/{producto_id}")
async def eliminar_producto(producto_id: int):
    return controller.eliminar_producto(producto_id)