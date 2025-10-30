from pydantic import BaseModel
from datetime import datetime

class DetallePedidoBaseModel(BaseModel):
    id: int = None
    id_pedido: int
    id_producto: int 
    numero_linea: int
    cantidad_solicitada: float
    cantidad_confirmada: float 
    precio_unitario: float
    precio_total: float
    precio_extranjero: float
    precio_total_extranjero: float
    tipo_documento: str
    numero_documento: str
    estado_siguiente: int
    estado_anterior: int 
    created_at: datetime = None
    updated_at: datetime = None
    
