from fastapi import APIRouter
from app.controllers.atributo_controller import AtributoController
from app.models.atributo_model import AtributoBaseModel as Atributo

router = APIRouter()

nuevo_atributo = AtributoController()

@router.post("/create_atributo")
async def create_atributo(atributo: Atributo):
    rpta = nuevo_atributo.create_atributo(atributo)
    return rpta

@router.get("/get_atributo/{atributo_id}")
async def get_atributo(atributo_id: int):
    rpta = nuevo_atributo.get_atributo(atributo_id)
    return rpta

@router.get("/get_atributos/")
async def get_atributos():
    rpta = nuevo_atributo.get_atributos()
    return rpta

@router.get("/get_atributos_activos/")
async def get_atributos_activos():
    rpta = nuevo_atributo.get_atributos_activos()
    return rpta

@router.delete("/delete_atributo/{atributo_id}")
async def delete_atributo(atributo_id: int):
    rpta = nuevo_atributo.delete_atributo(atributo_id)
    return rpta