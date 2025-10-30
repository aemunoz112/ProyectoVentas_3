from fastapi import APIRouter
from app.controllers.ordenesProduccion_controller import OrdenesProduccionController
from app.models.ordenesProduccion_model import OrdenProduccionBaseModel as OrdenProduccion

router = APIRouter()

nueva_orden_produccion = OrdenesProduccionController()

@router.post("/create_orden_produccion")
async def create_ordenProduccion(orden: OrdenProduccion):
    rpta = nueva_orden_produccion.create_ordenProduccion(orden)
    return rpta

@router.get("/get_orden_produccion/{orden_id}")
async def get_ordenProduccion(orden_id: int):
    rpta = nueva_orden_produccion.get_ordenProduccion(orden_id)
    return rpta

@router.get("/get_ordenes_produccion/")
async def get_ordenesProduccion():
    rpta = nueva_orden_produccion.get_ordenesProduccion()
    return rpta

@router.delete("/delete_orden_produccion/{orden_id}")
async def delete_ordenProduccion(orden_id: int):
    rpta = nueva_orden_produccion.delete_ordenProduccion(orden_id)
    return rpta