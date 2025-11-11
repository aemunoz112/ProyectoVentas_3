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
    id: int
    precio_total: Decimal
    precio_extranjero: Decimal
    precio_total_extranjero: Decimal
    producto_nombre: Optional[str] = None


class VentaBase(BaseModel):
    tipo_pedido: str
    id_cliente: int
    id_vendedor: int
    moneda: str = Field(default="COP")
    trm: Decimal = Field(default=Decimal("1"), alias="trm")
    oc_cliente: Optional[str] = None
    condicion_pago: Optional[str] = None
    detalles: List[VentaDetalleCreate]

    class Config:
        allow_population_by_field_name = True


class VentaCreate(VentaBase):
    pass


class VentaUpdate(BaseModel):
    tipo_pedido: Optional[str] = None
    id_cliente: Optional[int] = None
    id_vendedor: Optional[int] = None
    moneda: Optional[str] = None
    trm: Optional[Decimal] = Field(default=None, alias="trm")
    oc_cliente: Optional[str] = None
    condicion_pago: Optional[str] = None
    detalles: Optional[List[VentaDetalleCreate]] = None

    class Config:
        allow_population_by_field_name = True


class VentaResponse(VentaBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    detalles: List[VentaDetalleResponse]

    class Config:
        allow_population_by_field_name = True
