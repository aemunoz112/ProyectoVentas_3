from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field


class VentaDetalleBase(BaseModel):
    id_producto: int
    cantidad_solicitada: Decimal = Field(..., gt=0)
    cantidad_confirmada: Optional[Decimal] = None
    precio_unitario: Decimal = Field(..., ge=0)
    numero_linea: Optional[int] = None
    numero_documento: Optional[str] = None
    tipo_documento: Optional[str] = None
    estado_siguiente: Optional[int] = 1
    estado_anterior: Optional[int] = 1


class VentaDetalleCreate(VentaDetalleBase):
    pass


class VentaDetalleResponse(VentaDetalleBase):
    id: Optional[int] = None
    id_producto: int
    precio_total: Optional[Decimal] = None
    precio_extranjero: Optional[Decimal] = None
    precio_total_extranjero: Optional[Decimal] = None
    producto_nombre: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class VentaBase(BaseModel):
    tipo_pedido: str
    id_cliente: int
    id_vendedor: int
    moneda: str = Field(default="COP")
    trm: Decimal = Field(default=Decimal("1"))
    oc_cliente: Optional[str] = None
    condicion_pago: Optional[str] = None
    direccion: Optional[str] = None
    departamento_id: Optional[int] = None  # ID del departamento desde la API externa
    ciudad_id: Optional[int] = None  # ID de la ciudad desde la API externa


class VentaCreate(VentaBase):
    detalles: List[VentaDetalleCreate] = Field(default_factory=list)


class VentaUpdate(BaseModel):
    tipo_pedido: Optional[str] = None
    id_cliente: Optional[int] = None
    id_vendedor: Optional[int] = None
    moneda: Optional[str] = None
    trm: Optional[Decimal] = None
    oc_cliente: Optional[str] = None
    condicion_pago: Optional[str] = None
    direccion: Optional[str] = None
    departamento_id: Optional[int] = None  # ID del departamento desde la API externa
    ciudad_id: Optional[int] = None  # ID de la ciudad desde la API externa
    detalles: Optional[List[VentaDetalleCreate]] = None


class VentaResponse(VentaBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    detalles: List[VentaDetalleResponse] = Field(default_factory=list)


__all__ = [
    "VentaDetalleBase",
    "VentaDetalleCreate",
    "VentaDetalleResponse",
    "VentaBase",
    "VentaCreate",
    "VentaUpdate",
    "VentaResponse",
]

