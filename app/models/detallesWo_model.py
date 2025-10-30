from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DetalleWoBaseModel(BaseModel):
    id: Optional[int] = None
    id_wo: int
    id_pedido: int
    id_producto: int
    cantidad_solicitada: float
    cantidad_producida: float
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
