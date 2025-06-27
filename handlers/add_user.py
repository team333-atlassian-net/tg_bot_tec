from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode
from dialogs.add_user import AddUserSG

router = Router()

@router.message(Command("add_user"))
async def start_auth_dialog(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(AddUserSG.method, mode=StartMode.RESET_STACK)
