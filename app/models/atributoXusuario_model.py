from pydantic import BaseModel
from datetime import datetime


class AtributoXUsuarioBaseModel(BaseModel):
    id: int = None
    usuario_id: int
    atributo_id: int
    tipo: str  
    valor: str = None
    estado: str = "Activo"
    created_at: datetime = None
    updated_at: datetime = None