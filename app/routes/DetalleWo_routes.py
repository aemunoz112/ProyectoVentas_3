from fastapi import APIRouter
from app.controllers.detallesWo_controller import DetallesWoController
from app.models.detallesWo_model import DetalleWoBaseModel as DetalleWo

router = APIRouter()

nuevo_detalle = DetallesWoController()

@router.post("/create_detalle_wo")
async def create_detalleWo(detalle: DetalleWo):
    rpta = nuevo_detalle.create_detalleWo(detalle)
    return rpta

@router.get("/get_detalle_wo/{detalle_id}")
async def get_detalleWo(detalle_id: int):
    rpta = nuevo_detalle.get_detalleWo(detalle_id)
    return rpta

@router.get("/get_detalles_wo/")
async def get_detallesWo():
    rpta = nuevo_detalle.get_detallesWo()
    return rpta

@router.get("/get_detalles_by_wo/{id_wo}")
async def get_detallesByWo(id_wo: int):
    rpta = nuevo_detalle.get_detallesByWo(id_wo)
    return rpta

@router.delete("/delete_detalle_wo/{detalle_id}")
async def delete_detalleWo(detalle_id: int):
    rpta = nuevo_detalle.delete_detalleWo(detalle_id)
    return rpta