from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EncabezadoPedidoBaseModel(BaseModel):
    id: int = None
    tipo_pedido: str
    id_cliente: int
    id_vendedor: int
    moneda: str = "COP"
    TRM: float 
    OC_cliente: str
    condicion_pago: str = None
    direccion: Optional[str] = None
    departamento_id: Optional[int] = None  # ID del departamento desde la API externa
    ciudad_id: Optional[int] = None  # ID de la ciudad desde la API externa
    created_at: datetime = None
    updated_at: datetime = None