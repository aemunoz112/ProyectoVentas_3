from fastapi import APIRouter
from app.controllers.inventario_controller import *
from app.models.inventario_model import InventarioBaseModel as Inventario

router = APIRouter()

nuevo_inventario = InventarioController()

@router.post("/create_inventario")
async def create_inventario(inventario: Inventario):
    rpta = nuevo_inventario.create_inventario(inventario)
    return rpta

@router.get("/get_inventario/{inventario_id}")
async def get_inventario(inventario_id: int):
    rpta = nuevo_inventario.get_inventario(inventario_id)
    return rpta

@router.get("/get_inventarios/")
async def get_inventarios():
    rpta = nuevo_inventario.get_inventarios()
    return rpta

@router.delete("/delete_inventario/{inventario_id}")
async def delete_inventario(inventario_id: int):
    rpta = nuevo_inventario.delete_inventario(inventario_id)
    return rpta
