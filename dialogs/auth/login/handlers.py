import logging

from aiogram_dialog import DialogManager
from aiogram.types import Message

from dao.auth import get_user, update_or_add_tg_id

logger = logging.getLogger(__name__)


async def on_pin_entered(
    message: Message, value: str, dialog_manager: DialogManager, widget
):
    """Проверяет пин код и авторизует пользователя"""
    tg_id = message.from_user.id
    # Проверка: пользователь уже авторизован
    existing = await get_user(tg_id=tg_id)
    if existing:
        await message.answer("Вы уже авторизованы. Сначала выйите из системы.")
        await dialog_manager.done()
        return
    
    user = await get_user(pin_code=value.get_value())

    if not user:
        await message.answer("ПИН-код не найден. Повторите авторизацию.")
        await dialog_manager.done()
        return

    if user.tg_id and user.tg_id != tg_id:
        await message.answer("Этот ПИН уже использован другим пользователем.")
        await dialog_manager.done()
        return

    await update_or_add_tg_id(user, tg_id)  # добавляем tg_id в БД - авторизуем
    await message.answer(f"Добро пожаловать, {user.first_name}!")
    logger.info("Пользователь авторизовался (/login)")
    await dialog_manager.done()
