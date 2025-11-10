from typing import List, Optional

from pydantic import BaseModel, Field


class MenuItemBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    ruta: Optional[str] = None
    icono: Optional[str] = None
    tipo: Optional[str] = "pagina"
    modulo_id: Optional[int] = None
    parent_id: Optional[int] = None
    orden: Optional[int] = 0
    estado: Optional[str] = "Activo"


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    ruta: Optional[str] = None
    icono: Optional[str] = None
    tipo: Optional[str] = None
    modulo_id: Optional[int] = None
    parent_id: Optional[int] = None
    orden: Optional[int] = None
    estado: Optional[str] = None


class MenuAssignment(BaseModel):
    rol_id: int
    puede_ver: bool = True
    puede_crear: bool = False
    puede_editar: bool = False
    puede_eliminar: bool = False


class MenuItemTree(BaseModel):
    id: int
    modulo_id: Optional[int]
    parent_id: Optional[int]
    nombre: str
    descripcion: Optional[str]
    ruta: Optional[str]
    icono: Optional[str]
    tipo: Optional[str]
    nivel: int
    orden: int
    estado: str
    permisos: List[str] = Field(default_factory=list)
    hijos: List["MenuItemTree"] = Field(default_factory=list)

    class Config:
        orm_mode = True


MenuItemTree.update_forward_refs()


