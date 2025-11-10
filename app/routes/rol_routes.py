from fastapi import APIRouter

from app.controllers.rol_controller import RolController
from app.models.rol_model import RolCreateModel, RolUpdateModel


router = APIRouter()

rol_controller = RolController()


@router.post("/create_rol")
async def create_rol(rol: RolCreateModel):
    return rol_controller.create_rol(rol)


@router.get("/get_rol/{rol_id}")
async def get_rol(rol_id: int):
    return rol_controller.get_rol(rol_id)


@router.get("/get_roles/")
async def get_roles():
    return rol_controller.get_roles()


@router.put("/update_rol/{rol_id}")
async def update_rol(rol_id: int, rol: RolUpdateModel):
    return rol_controller.update_rol(rol_id, rol)


@router.delete("/delete_rol/{rol_id}")
async def delete_rol(rol_id: int):
    return rol_controller.delete_rol(rol_id)


