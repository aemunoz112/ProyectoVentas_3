from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict

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
    departamento_id: Optional[int] = None  # ID del departamento desde la API externa
    ciudad_id: Optional[int] = None  # ID de la ciudad desde la API externa
    atributos: Optional[Dict[str, str]] = None  # Atributos dinámicos del usuario
    created_at: datetime = None
    updated_at: datetime = None