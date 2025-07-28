from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode
from states import AddUserSG
from utils.auth import require_admin

router = Router()


@router.message(Command("add_user"))
async def start_auth_dialog(message: Message, dialog_manager: DialogManager):
    user = await require_admin(message)
    if not user:
        return
    await dialog_manager.reset_stack()
    await dialog_manager.start(AddUserSG.method, mode=StartMode.RESET_STACK)
