from fastapi import APIRouter
from app.controllers.usuario_controller import *
from app.models.usuario_model import UsuarioBaseModel as Usuario


router = APIRouter()

nuevo_usuario = UsuarioController()


@router.post("/create_user")
async def create_user(user: Usuario):
    rpta = nuevo_usuario.create_user(user)
    return rpta


@router.get("/get_user/{user_id}")
async def get_user(user_id: int):
    rpta = nuevo_usuario.get_user(user_id)
    return rpta

@router.get("/get_users/")
async def get_users():
    rpta = nuevo_usuario.get_users()
    return rpta

@router.delete("/delete_user/{user_id}")
async def delete_user(user_id: int):
    rpta = nuevo_usuario.delete_user(user_id)
    return rpta


@router.put("/update_user/{user_id}")
async def update_user(user_id: int, user: Usuario):
    rpta = nuevo_usuario.update_user(user_id, user)
    return rpta