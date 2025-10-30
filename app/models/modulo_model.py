from pydantic import BaseModel
from datetime import datetime

class ModuloBaseModel(BaseModel):
    id: int = None
    nombre: str
    descripcion: str
    ruta: str
    estado: str = "Activo"
    created_at: datetime = None
    updated_at: datetime = None