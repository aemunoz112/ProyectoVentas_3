from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class OrdenProduccionBaseModel(BaseModel):
    id: Optional[int] = None
    estado_siguiente: str
    estado_anterior: str
    fecha_inicio: datetime
    fecha_fin_estimada: datetime
    fecha_fin_real: datetime
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
