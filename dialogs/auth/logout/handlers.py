from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from dao.auth import get_user, delete_tg_id


async def on_logout_click(
    callback: CallbackQuery, widget, dialog_manager: DialogManager
):
    """Хэндлер выхода из аккаунта. Очищает tg_id у пользователя"""
    tg_id = callback.message.from_user.id
    await delete_tg_id(tg_id)
    await callback.answer("Вы вышли из аккаунта")
    await dialog_manager.done()