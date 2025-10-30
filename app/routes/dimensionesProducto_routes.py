from fastapi import APIRouter
from app.controllers.dimensionesProducto_controller import *
from app.models.dimensionesProducto_model import DimensionesProductoBaseModel as Dimension

router = APIRouter()

nuevo_dimension = DimensionProductoController()

@router.post("/create_dimension_producto")
async def create_dimension(dimension: Dimension):
    rpta = nuevo_dimension.create_dimension(dimension)
    return rpta

@router.get("/get_dimension_producto/{inventario_id}")
async def get_dimensio(dimension_id: int):
    rpta = nuevo_dimension.get_dimension(dimension_id)
    return rpta

@router.get("/get_dimensiones_productos/")
async def get_inventarios():
    rpta = nuevo_dimension.get_dimensiones()
    return rpta

@router.delete("/delete_dimension_producto/{inventario_id}")
async def delete_dimension(inventario_id: int):
    rpta = nuevo_dimension.delete_dimension(inventario_id)
    return rpta
