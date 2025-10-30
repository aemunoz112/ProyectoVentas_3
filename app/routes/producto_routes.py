from fastapi import APIRouter
from app.controllers.producto_controller import *
from app.models.producto_model import ProductoBaseModel as Producto

router = APIRouter()

nuevo_producto = ProductoController()

@router.post("/create_producto")
async def create_producto(producto: Producto):
    rpta = nuevo_producto.create_producto(producto)
    return rpta

@router.get("/get_producto/{producto_id}")
async def get_producto(producto_id: int):
    rpta = nuevo_producto.get_producto(producto_id)
    return rpta

@router.get("/get_productos/")
async def get_productos():
    rpta = nuevo_producto.get_productos()
    return rpta

@router.delete("/delete_producto/{producto_id}")
async def delete_producto(producto_id: int):
    rpta = nuevo_producto.delete_producto(producto_id)
    return rpta