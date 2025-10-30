from pydantic import BaseModel
from datetime import datetime

class RolBaseModel(BaseModel):
    id: str = None
    nombre: str
    descripcion: str
    estado: str = None
    created_at: datetime = None
    updated_at: datetime = None