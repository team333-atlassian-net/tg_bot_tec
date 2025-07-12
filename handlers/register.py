from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from dialogs.auth.register import RegisterDialogSG

router = Router()

@router.message(Command("register"))
async def start_auth_dialog(message: Message, dialog_manager: DialogManager):
    await dialog_manager.reset_stack()
    await dialog_manager.start(RegisterDialogSG.first, mode=StartMode.RESET_STACK)
