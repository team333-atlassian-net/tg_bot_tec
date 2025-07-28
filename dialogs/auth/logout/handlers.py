from aiogram_dialog import DialogManager
from aiogram.types import CallbackQuery
from dao.auth import delete_tg_id

async def on_logout(callback: CallbackQuery, button, dialog_manager: DialogManager):
    tg_id = callback.from_user.id
    await delete_tg_id(tg_id)
    await callback.message.answer("Вы вышли из аккаунта")
    await dialog_manager.done()
