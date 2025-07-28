from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from dao.auth import delete_tg_id, get_user
from states import AuthDialogSG

router = Router()

@router.message(Command("login"))
async def start_auth_dialog(message: Message, dialog_manager: DialogManager):
    await dialog_manager.reset_stack()
    tg_id = message.from_user.id
    existing_user = await get_user(tg_id=tg_id)

    if existing_user:
        await message.answer("Вы уже авторизованы.")
        return
    
    await dialog_manager.start(AuthDialogSG.enter_pin, mode=StartMode.RESET_STACK)

@router.message(Command("logout"))
async def handle_logout(message: Message):
    """Хэндлер выхода из аккаунта. Очищает tg_id у пользователя"""
    tg_id = message.from_user.id
    user = await get_user(tg_id=tg_id)
    if user:
        await delete_tg_id(tg_id)
        await message.answer("Вы вышли из аккаунта. Чтобы войти снова — используйте /login.")
    else:
        await message.answer("Вы не авторизованы.")

