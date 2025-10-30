from pydantic import BaseModel
from datetime import datetime

class EncabezadoPedidoBaseModel(BaseModel):
    id: int = None
    tipo_pedido: str
    id_cliente: int
    id_vendedor: int
    moneda: str = "COP"
    TRM: float 
    OC_cliente: str
    condicion_pago: str = None 
    created_at: datetime = None
    updated_at: datetime = None