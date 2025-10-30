from pydantic import BaseModel
from datetime import datetime

class InventarioBaseModel(BaseModel):
    id: int = None
    id_producto: int
    lote: str 
    cantidad_disponible: float
    created_at: datetime = None
    updated_at: datetime = None