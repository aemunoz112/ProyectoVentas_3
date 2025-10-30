from pydantic import BaseModel
from datetime import datetime

class UsuarioBaseModel(BaseModel):
    id: int = None
    nombres: str
    apellidos: str
    email: str
    telefono: str
    cedula: str
    contrasena: str
    rol_id: int
    estado: str = "Activo"
    created_at: datetime = None
    updated_at: datetime = None