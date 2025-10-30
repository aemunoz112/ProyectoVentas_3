from fastapi import FastAPI

from app.routes.usuario_routes import router as usuario_router
from app.routes.producto_routes import router as producto_router
from app.routes.inventario_routes import router as inventario_router
from app.routes.dimensionesProducto_routes import router as dimension_router
from app.routes.DetalleWo_routes import router as detalle_router
from app.routes.ordenesProduccion_routes import router as ordenes_router
from app.routes.encabezadoPedido_routes import router as encabezado_router
from app.routes.detallePedido_routes import router as detallePedido_router
from app.routes.modulo_routes import router as modulo_router
from app.routes.moduloXrol_routes import router as moduloXrol_router
from app.routes.atributo_routes import router as atributo_router
from app.routes.atributoXusuario_routes import router as atributoXusuario_router
from app.routes.estado_routes import router as estado_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    #"http://localhost.tiangolo.com",
    #"https://localhost.tiangolo.com",
    "http://localhost"
    #"http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuario_router)
app.include_router(modulo_router)
app.include_router(moduloXrol_router)
app.include_router(atributo_router)
app.include_router(atributoXusuario_router)
app.include_router(estado_router)
app.include_router(producto_router)
app.include_router(inventario_router)
app.include_router(dimension_router)
app.include_router(encabezado_router)
app.include_router(detallePedido_router)
app.include_router(ordenes_router)
app.include_router(detalle_router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)