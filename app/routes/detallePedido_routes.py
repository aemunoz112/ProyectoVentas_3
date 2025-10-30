from fastapi import APIRouter
from app.controllers.detallePedido_controller import DetallePedidosController
from app.models.destallePedido_model import DetallePedidoBaseModel as DetallePedido

router = APIRouter()

nuevo_detalle_pedido = DetallePedidosController()

@router.post("/create_detalle_pedido")
async def create_detalle_pedido(detalle: DetallePedido):
    rpta = nuevo_detalle_pedido.create_detalle_pedido(detalle)
    return rpta

@router.get("/get_detalle_pedido/{detalle_id}")
async def get_detalle_pedido(detalle_id: int):
    rpta = nuevo_detalle_pedido.get_detalle_pedido(detalle_id)
    return rpta

@router.get("/get_detalles_pedidos/")
async def get_detalles_pedidos():
    rpta = nuevo_detalle_pedido.get_detalles_pedidos()
    return rpta

@router.get("/get_detalles_by_pedido/{id_pedido}")
async def get_detalles_by_pedido(id_pedido: int):
    rpta = nuevo_detalle_pedido.get_detalles_by_pedido(id_pedido)
    return rpta

@router.delete("/delete_detalle_pedido/{detalle_id}")
async def delete_detalle_pedido(detalle_id: int):
    rpta = nuevo_detalle_pedido.delete_detalle_pedido(detalle_id)
    return rpta