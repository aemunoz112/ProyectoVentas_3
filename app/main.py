from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
from app.routes.auth_routes import router as auth_router
from app.routes.menu_routes import router as menu_router
from app.routes.rol_routes import router as rol_router
from app.routes.atributo_routes import router as atributo_router
from app.routes.atributoXusuario_routes import router as atributoXusuario_router
from app.routes.estado_routes import router as estado_router
from app.routes.favorito_routes import router as favorito_router
from app.routes.venta_routes import router as venta_router

app = FastAPI()

# ⭐ CONFIGURACIÓN DE CORS
# Permite solicitudes desde el frontend Angular en desarrollo y ngrok
origins = [
    "http://localhost",
    "http://localhost:4200",  # Frontend Angular en desarrollo
    "http://127.0.0.1:4200",
    # Permite acceso desde cualquier dominio de ngrok
    "https://*.ngrok-free.app",
    "https://*.ngrok.io",
    # "https://tu-dominio.com",  # Agregar en producción
    # "http://localhost:8080",  # Si usas otro puerto
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite acceso desde cualquier origen (incluye ngrok)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos los headers
)

app.include_router(usuario_router)
app.include_router(rol_router)
app.include_router(auth_router)
app.include_router(modulo_router)
app.include_router(moduloXrol_router)
app.include_router(menu_router)
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
app.include_router(favorito_router)
app.include_router(venta_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
