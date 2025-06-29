from aiogram import Router
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode
from dialogs.admin_events import AdminEventSG
from dialogs.view_events import ViewEventSG
from utils.auth import require_admin, require_auth

router = Router()

@router.message(Command("add_event"))
async def start_add_event(message, dialog_manager: DialogManager):
    user = await require_admin(message)
    if not user:
        return
    await dialog_manager.start(AdminEventSG.title, mode=StartMode.RESET_STACK)


@router.message(Command("events"))
async def start_view_events(message, dialog_manager: DialogManager):
    user = await require_auth(message)
    if not user:
        return
    await dialog_manager.start(ViewEventSG.main, mode=StartMode.RESET_STACK)