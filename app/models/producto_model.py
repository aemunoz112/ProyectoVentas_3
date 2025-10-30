from pydantic import BaseModel
from datetime import datetime

class ProductoBaseModel(BaseModel):
    id: int = None
    codigo_producto: str
    nombre_producto: str
    descripcion: str
    categoria: str
    unidad_medida: str
    estado: str = "Activo"
    created_at: datetime = None
    updated_at: datetime = None