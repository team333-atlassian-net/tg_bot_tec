import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode
from aiogram.types import Message

from dialogs.canteen.add_canteen_info import CanteenInfoCreationSG
from dialogs.canteen.manage_canteen_info import ManageCanteenSG
from dialogs.canteen.view_canteen_info import CanteenViewSG
from utils.auth import require_admin, require_auth

logger = logging.getLogger(__name__)

router = Router()

@router.message(Command("canteen"))
async def show_canteen_info(message: Message, dialog_manager: DialogManager):
    user = await require_auth(message)
    if not user:
        return
    logger.info("Пользователь запросил информацию по столовой или меню (/canteen)")
    await dialog_manager.start(CanteenViewSG.start, mode=StartMode.RESET_STACK)


@router.message(Command("add_canteen_info"))
async def start_add_canteen_info(message, dialog_manager: DialogManager):
    user = await require_admin(message)
    if not user:
        return
    await dialog_manager.start(CanteenInfoCreationSG.choice, mode=StartMode.RESET_STACK)


@router.message(Command("manage_canteen_info"))
async def start_manage_canteen_info(message, dialog_manager: DialogManager):
    user = await require_admin(message)
    if not user:
        return
    await dialog_manager.start(ManageCanteenSG.choice, mode=StartMode.RESET_STACK)