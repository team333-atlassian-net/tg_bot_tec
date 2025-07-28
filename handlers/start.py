import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from states import StartSG


logger = logging.getLogger(__name__)

router = Router()

@router.message(Command("start"))
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)
