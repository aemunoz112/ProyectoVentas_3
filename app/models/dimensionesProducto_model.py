from decimal import Decimal
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class DimensionesProductoBaseModel(BaseModel):
    ancho: Decimal = Field(..., ge=0)
    espesor: Decimal = Field(..., ge=0)
    diametro_interno: Decimal = Field(..., ge=0)
    diametro_externo: Decimal = Field(..., ge=0)
    estado: Optional[str] = "Activo"


class DimensionesProductoCreateModel(DimensionesProductoBaseModel):
    id_producto: int


class DimensionesProductoUpdateModel(BaseModel):
    ancho: Optional[Decimal] = Field(default=None, ge=0)
    espesor: Optional[Decimal] = Field(default=None, ge=0)
    diametro_interno: Optional[Decimal] = Field(default=None, ge=0)
    diametro_externo: Optional[Decimal] = Field(default=None, ge=0)
    estado: Optional[str] = None


class DimensionesProductoResponseModel(BaseModel):
    id: int
    id_producto: int
    ancho: Decimal = Field(default=Decimal("0"), ge=0)
    espesor: Decimal = Field(default=Decimal("0"), ge=0)
    diametro_interno: Decimal = Field(default=Decimal("0"), ge=0)
    diametro_externo: Decimal = Field(default=Decimal("0"), ge=0)
    estado: Optional[str] = "Activo"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


__all__ = [
    "DimensionesProductoBaseModel",
    "DimensionesProductoCreateModel",
    "DimensionesProductoUpdateModel",
    "DimensionesProductoResponseModel",
]