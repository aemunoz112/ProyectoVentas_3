from fastapi import APIRouter
from app.controllers.encabezadoPedido_controller import EncabezadoPedidosController
from app.models.encabezadoPedido_model import EncabezadoPedidoBaseModel as EncabezadoPedido

router = APIRouter()

nuevo_encabezado_pedido = EncabezadoPedidosController()

@router.post("/create_encabezado_pedido")
async def create_encabezadoPedido(encabezado: EncabezadoPedido):
    rpta = nuevo_encabezado_pedido.create_encabezadoPedido(encabezado)
    return rpta

@router.get("/get_encabezado_pedido/{encabezado_id}")
async def get_encabezadoPedido(encabezado_id: int):
    rpta = nuevo_encabezado_pedido.get_encabezadoPedido(encabezado_id)
    return rpta

@router.get("/get_encabezados_pedidos/")
async def get_encabezadosPedidos():
    rpta = nuevo_encabezado_pedido.get_encabezadosPedidos()
    return rpta

@router.get("/get_encabezados_by_cliente/{id_cliente}")
async def get_encabezadosByCliente(id_cliente: int):
    rpta = nuevo_encabezado_pedido.get_encabezadosByCliente(id_cliente)
    return rpta

@router.delete("/delete_encabezado_pedido/{encabezado_id}")
async def delete_encabezadoPedido(encabezado_id: int):
    rpta = nuevo_encabezado_pedido.delete_encabezadoPedido(encabezado_id)
    return rpta