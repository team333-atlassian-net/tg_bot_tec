import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode
from aiogram.types import Message

from states import EventCreationSG, ManageEventSG, EventsViewSG
from utils.auth import require_admin, require_auth

logger = logging.getLogger(__name__)

router = Router()


@router.message(Command("events"))
async def show_virtual_excursions(message: Message, dialog_manager: DialogManager):
    user = await require_auth(message)
    if not user:
        return
    logger.info("Пользователь запросил список мероприятий (/events)")
    await dialog_manager.start(EventsViewSG.list, mode=StartMode.RESET_STACK)


@router.message(Command("add_event"))
async def start_add_event(message, dialog_manager: DialogManager):
    user = await require_admin(message)
    if not user:
        return
    await dialog_manager.start(EventCreationSG.title, mode=StartMode.RESET_STACK)


@router.message(Command("manage_events"))
async def start_manage_events(message, dialog_manager: DialogManager):
    user = await require_admin(message)
    if not user:
        return
    await dialog_manager.start(ManageEventSG.list, mode=StartMode.RESET_STACK)
