from pydantic import BaseModel
from datetime import datetime

class RolBaseModel(BaseModel):
    id: int | None = None
    nombre: str
    descripcion: str | None = None
    estado: str | None = "Activo"
    created_at: datetime | None = None
    updated_at: datetime | None = None


class RolModuloAssign(BaseModel):
    modulo_id: int
    permisos: list[str] | None = None
    estado: str | None = "Activo"


class RolMenuAssign(BaseModel):
    menu_item_id: int
    permisos: list[str] | None = None
    estado: str | None = "Activo"


class RolCreateModel(BaseModel):
    nombre: str
    descripcion: str | None = None
    estado: str | None = "Activo"
    modulos: list[RolModuloAssign] = []
    menu_items: list[RolMenuAssign] = []


class RolUpdateModel(RolCreateModel):
    pass