from pydantic import BaseModel
from datetime import datetime

class EstadoBaseModel(BaseModel):
    id: int = None
    nombre: str
    descripcion: str
    created_at: datetime = None
    updated_at: datetime = None
