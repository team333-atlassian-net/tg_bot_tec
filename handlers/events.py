from aiogram import Router
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from dao.events import get_all_events
from dialogs.admin_events import AdminEventSG
from dialogs.manage_events import ManageEventSG
from utils.auth import require_admin, require_auth

router = Router()

@router.message(Command("events"))
async def show_events(message: Message):
    events = await get_all_events()
    if not events:
        await message.answer("Нет мероприятий")
        return
    text = "\n\n".join(f"🎉 <b>{e.title}</b>\n{e.description}" for e in events)
    await message.answer(text, parse_mode="HTML")

@router.message(Command("add_event"))
async def start_add_event(message, dialog_manager: DialogManager, state: FSMContext):
    user = await require_admin(message)
    if not user:
        return
    await dialog_manager.start(AdminEventSG.title, mode=StartMode.RESET_STACK)


@router.message(Command("manage_events"))
async def start_manage_events(message, dialog_manager: DialogManager):
    user = await require_auth(message)
    if not user:
        return
    await dialog_manager.start(ManageEventSG.list, mode=StartMode.RESET_STACK)