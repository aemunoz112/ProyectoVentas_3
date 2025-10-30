from fastapi import APIRouter
from app.controllers.atributoXusuario_controlles import AtributoXUsuarioController
from app.models.atributoXusuario_model import AtributoXUsuarioBaseModel as AtributoXUsuario

router = APIRouter()

nuevo_atributo_x_usuario = AtributoXUsuarioController()

@router.post("/create_atributo_x_usuario")
async def create_atributo_x_usuario(atributo_usuario: AtributoXUsuario):
    rpta = nuevo_atributo_x_usuario.create_atributo_x_usuario(atributo_usuario)
    return rpta

@router.get("/get_atributo_x_usuario/{atributo_usuario_id}")
async def get_atributo_x_usuario(atributo_usuario_id: int):
    rpta = nuevo_atributo_x_usuario.get_atributo_x_usuario(atributo_usuario_id)
    return rpta

@router.get("/get_atributos_x_usuario/")
async def get_atributos_x_usuario():
    rpta = nuevo_atributo_x_usuario.get_atributos_x_usuario()
    return rpta

@router.get("/get_atributos_by_usuario/{usuario_id}")
async def get_atributos_by_usuario(usuario_id: int):
    rpta = nuevo_atributo_x_usuario.get_atributos_by_usuario(usuario_id)
    return rpta

@router.get("/get_usuarios_by_atributo/{atributo_id}")
async def get_usuarios_by_atributo(atributo_id: int):
    rpta = nuevo_atributo_x_usuario.get_usuarios_by_atributo(atributo_id)
    return rpta

@router.delete("/delete_atributo_x_usuario/{atributo_usuario_id}")
async def delete_atributo_x_usuario(atributo_usuario_id: int):
    rpta = nuevo_atributo_x_usuario.delete_atributo_x_usuario(atributo_usuario_id)
    return rpta