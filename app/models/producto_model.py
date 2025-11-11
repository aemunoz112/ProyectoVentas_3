from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.dimensionesProducto_model import (
    DimensionesProductoBaseModel,
    DimensionesProductoCreateModel,
    DimensionesProductoResponseModel,
)


class ProductoBaseModel(BaseModel):
    codigo_producto: str
    nombre_producto: str
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    unidad_medida: Optional[str] = None
    estado: Optional[str] = "Activo"


class ProductoCreateModel(ProductoBaseModel):
    dimensiones: List[DimensionesProductoCreateModel] = Field(default_factory=list)


class ProductoUpdateModel(BaseModel):
    codigo_producto: Optional[str] = None
    nombre_producto: Optional[str] = None
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    unidad_medida: Optional[str] = None
    estado: Optional[str] = None
    dimensiones: Optional[List[DimensionesProductoCreateModel]] = None


class ProductoResponseModel(ProductoBaseModel):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    dimensiones: List[DimensionesProductoResponseModel] = Field(default_factory=list)


__all__ = [
    "ProductoBaseModel",
    "ProductoCreateModel",
    "ProductoUpdateModel",
    "ProductoResponseModel",
]