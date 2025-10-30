from pydantic import BaseModel
from datetime import datetime

class AtributoBaseModel(BaseModel):
    id: int = None
    nombre: str
    descripcion: str
    estado: str = "Activo"
    created_at: datetime = None
    updated_at: datetime = None