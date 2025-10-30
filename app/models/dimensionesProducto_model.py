from pydantic import BaseModel
from datetime import datetime

class DimensionesProductoBaseModel(BaseModel):
    id: int = None
    id_producto: int
    ancho: float
    espesor: float
    diametro_interno: float
    diametro_externo: float
    estado: str = "Activo"
    created_at: datetime = None
    updated_at: datetime = None