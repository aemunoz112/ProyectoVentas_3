from fastapi import APIRouter
from app.controllers.moduloXrol_controller import ModuloXRolController
from app.models.moduloXrol_model import ModuloXrolBaseModel as ModuloXrol

router = APIRouter()

nuevo_modulo_x_rol = ModuloXRolController()

@router.post("/create_modulo_x_rol")
async def create_modulo_x_rol(modulo_rol: ModuloXrol):
    rpta = nuevo_modulo_x_rol.create_modulo_x_rol(modulo_rol)
    return rpta

@router.get("/get_modulo_x_rol/{modulo_rol_id}")
async def get_modulo_x_rol(modulo_rol_id: int):
    rpta = nuevo_modulo_x_rol.get_modulo_x_rol(modulo_rol_id)
    return rpta

@router.get("/get_modulos_x_rol/")
async def get_modulos_x_rol():
    rpta = nuevo_modulo_x_rol.get_modulos_x_rol()
    return rpta

@router.get("/get_modulos_by_rol/{rol_id}")
async def get_modulos_by_rol(rol_id: int):
    rpta = nuevo_modulo_x_rol.get_modulos_by_rol(rol_id)
    return rpta

@router.get("/get_roles_by_modulo/{modulo_id}")
async def get_roles_by_modulo(modulo_id: int):
    rpta = nuevo_modulo_x_rol.get_roles_by_modulo(modulo_id)
    return rpta


@router.delete("/delete_modulo_x_rol/{modulo_rol_id}")
async def delete_modulo_x_rol(modulo_rol_id: int):
    rpta = nuevo_modulo_x_rol.delete_modulo_x_rol(modulo_rol_id)
    return rpta