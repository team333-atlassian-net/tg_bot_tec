from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from dialogs.login import AuthDialogSG

router = Router()

@router.message(Command("login"))
async def start_auth_dialog(message: Message, dialog_manager: DialogManager):
    await dialog_manager.reset_stack()
    await dialog_manager.start(AuthDialogSG.enter_pin, mode=StartMode.RESET_STACK)
