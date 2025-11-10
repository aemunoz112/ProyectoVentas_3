from fastapi import APIRouter

from app.controllers.auth_controller import AuthController
from app.models.auth_model import LoginModel


router = APIRouter()

auth_controller = AuthController()


@router.post("/auth/login")
async def login(credentials: LoginModel):
    return auth_controller.login(credentials)


