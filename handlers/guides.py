import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode
from aiogram.types import Message

from states import GuideCreationSG, GuideViewSG, GuideEditSG
from utils.auth import require_admin, require_auth

logger = logging.getLogger(__name__)

router = Router()


@router.message(Command("guides"))
async def show_guides(message: Message, dialog_manager: DialogManager):
    user = await require_auth(message)
    if not user:
        return
    await dialog_manager.start(GuideViewSG.documents, mode=StartMode.RESET_STACK)


@router.message(Command("manage_guides"))
async def start_manage_guides(message, dialog_manager: DialogManager):
    user = await require_admin(message)
    if not user:
        return
    await dialog_manager.start(GuideEditSG.documents, mode=StartMode.RESET_STACK)


@router.message(Command("add_guide"))
async def start_add_guide(message, dialog_manager: DialogManager):
    user = await require_admin(message)
    if not user:
        return
    await dialog_manager.start(GuideCreationSG.document, mode=StartMode.RESET_STACK)
