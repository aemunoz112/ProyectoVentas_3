from fastapi import APIRouter

from app.controllers.menu_controller import MenuController
from app.models.menu_model import MenuAssignment, MenuItemCreate, MenuItemUpdate


router = APIRouter()

menu_controller = MenuController()


@router.get("/menu/tree/{rol_id}")
async def get_menu_by_role(rol_id: int):
    return menu_controller.get_menu_tree_by_role(rol_id)


@router.get("/menu/tree")
async def get_full_menu():
    return menu_controller.get_full_menu_tree()


@router.get("/menu/items")
async def list_menu_items():
    return menu_controller.list_menu_items()


@router.post("/menu/items")
async def create_menu_item(item: MenuItemCreate):
    return menu_controller.create_menu_item(item)


@router.put("/menu/items/{item_id}")
async def update_menu_item(item_id: int, item: MenuItemUpdate):
    return menu_controller.update_menu_item(item_id, item)


@router.delete("/menu/items/{item_id}")
async def delete_menu_item(item_id: int):
    return menu_controller.delete_menu_item(item_id)


@router.post("/menu/items/{item_id}/assign")
async def assign_menu_item(item_id: int, assignment: MenuAssignment):
    return menu_controller.assign_menu_item(item_id, assignment)


