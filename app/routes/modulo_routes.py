from fastapi import APIRouter
from app.controllers.modulo_controller import ModulosController
from app.models.modulo_model import ModuloBaseModel as Modulo

router = APIRouter()

nuevo_modulo = ModulosController()

@router.post("/create_modulo")
async def create_modulo(modulo: Modulo):
    rpta = nuevo_modulo.create_modulo(modulo)
    return rpta

@router.get("/get_modulo/{modulo_id}")
async def get_modulo(modulo_id: int):
    rpta = nuevo_modulo.get_modulo(modulo_id)
    return rpta

@router.get("/get_modulos/")
async def get_modulos():
    rpta = nuevo_modulo.get_modulos()
    return rpta

@router.get("/get_modulos_activos/")
async def get_modulos_activos():
    rpta = nuevo_modulo.get_modulos_activos()
    return rpta

@router.delete("/delete_modulo/{modulo_id}")
async def delete_modulo(modulo_id: int):
    rpta = nuevo_modulo.delete_modulo(modulo_id)
    return rpta

@router.put("/update_modulo/{modulo_id}")
async def update_modulo(modulo_id: int, modulo: Modulo):
    rpta = nuevo_modulo.update_modulo(modulo_id, modulo)
    return rpta