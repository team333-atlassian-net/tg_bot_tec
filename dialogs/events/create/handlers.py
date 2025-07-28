import logging

from aiogram.types import Message, CallbackQuery

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput

from dao.auth import get_all_active_users
from dao.events import create_event
from states import EventCreationSG

logger = logging.getLogger(__name__)


async def on_title_input(
    message: Message,
    widget: TextInput,
    dialog: DialogManager,
):
    """
    Обработчик успешного ввода заголовка.
    Сохраняет заголовок в dialog_data и переключается на состояние ввода описания.
    """
    dialog.dialog_data["title"] = message.text
    await dialog.switch_to(EventCreationSG.description)


async def on_description_input(
    message: Message, widget: TextInput, dialog: DialogManager
):
    """
    Обработчик ввода описания.
    """
    dialog.dialog_data["description"] = message.text
    await dialog.switch_to(EventCreationSG.confirm)


async def on_confirm_press(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs
):
    title = dialog_manager.dialog_data.get("title")
    description = dialog_manager.dialog_data.get("description")

    if not title or not description:
        await callback.message.answer("❌ Не удалось получить данные мероприятия.")
        return

    # Добавляем событие в базу
    await create_event(title, description)

    # Получаем пользователей
    users = await get_all_active_users()
    text = f"🎉 <b>Новое корпоративное мероприятие</b>\n\n<b>{title}</b>\n{description}"

    for user in users:
        try:
            await callback.bot.send_message(chat_id=user.tg_id, text=text)
        except Exception:
            pass

    await callback.message.answer("✅ Мероприятие добавлено и разослано сотрудникам.")
    logger.info("Администратор добавил новое мероприятие (/add_event)")
    await dialog_manager.done()


async def send_file_callback(c, button, manager: DialogManager):
    telegram_file_id = button.widget_id.split("_", 1)[-1]
    await c.message.answer_document(telegram_file_id)
