import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode
from aiogram.types import Message

from states import FeedbackAdminSG, FeedbackUserSG
from utils.auth import require_admin, require_auth

logger = logging.getLogger(__name__)

router = Router()


@router.message(Command("feedback"))
async def show_guides(message: Message, dialog_manager: DialogManager):
    user = await require_auth(message)
    if not user:
        return
    await dialog_manager.start(FeedbackUserSG.text, mode=StartMode.RESET_STACK)


@router.message(Command("manage_feedback"))
async def start_manage_guides(message, dialog_manager: DialogManager):
    user = await require_admin(message)
    if not user:
        return
    await dialog_manager.start(
        FeedbackAdminSG.list,
        mode=StartMode.RESET_STACK,
        data={"unread_flag": True},
    )
