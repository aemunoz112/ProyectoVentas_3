from typing import List, Optional

from pydantic import BaseModel, Field


class FavoritoBase(BaseModel):
    menu_item_id: int
    alias: Optional[str] = Field(default=None, max_length=150)
    orden: Optional[int] = None


class FavoritoCreate(FavoritoBase):
    pass


class FavoritoUpdate(BaseModel):
    alias: Optional[str] = Field(default=None, max_length=150)
    orden: Optional[int] = None


class FavoritoResponse(BaseModel):
    id: int
    usuario_id: int
    menu_item_id: int
    alias: Optional[str] = None
    orden: Optional[int] = None
    nombre_menu: Optional[str] = None
    descripcion_menu: Optional[str] = None
    ruta: Optional[str] = None
    icono: Optional[str] = None
    permisos: List[str] = Field(default_factory=list)

    class Config:
        orm_mode = True
