from pydantic import BaseModel
from datetime import datetime
from typing import List, Union

class ModuloXrolBaseModel(BaseModel):
    id: int = None
    rol_id: int
    modulo_id: int
    permisos: Union[str, List[str]]
    estado: str = "Activo"
    created_at: datetime = None
    updated_at: datetime = None