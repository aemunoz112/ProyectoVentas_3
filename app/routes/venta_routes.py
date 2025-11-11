from typing import List

from fastapi import APIRouter

from app.controllers.venta_controller import VentaController
from app.models.venta_model import VentaCreate, VentaResponse, VentaUpdate

router = APIRouter()
controller = VentaController()


@router.get("/ventas/", response_model=List[VentaResponse])
async def listar_ventas():
    return controller.listar_ventas()


@router.get("/ventas/{venta_id}", response_model=VentaResponse)
async def obtener_venta(venta_id: int):
    return controller.obtener_venta(venta_id)


@router.post("/ventas/", response_model=VentaResponse, status_code=201)
async def crear_venta(payload: VentaCreate):
    return controller.crear_venta(payload)


@router.put("/ventas/{venta_id}", response_model=VentaResponse)
async def actualizar_venta(venta_id: int, payload: VentaUpdate):
    return controller.actualizar_venta(venta_id, payload)


@router.delete("/ventas/{venta_id}")
async def eliminar_venta(venta_id: int):
    return controller.eliminar_venta(venta_id)
