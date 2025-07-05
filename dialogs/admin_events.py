from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.input import TextInput
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from dao.auth import get_all_active_users
from dao.events import create_event


class AdminEventSG(StatesGroup):
    """
    Состояния диалога для добавления нового корпоративного мероприятия.
    """
    title = State()
    description = State()


async def on_title_entered(msg: Message, value: str, dialog_manager: DialogManager, widget):
    """
    Обработчик ввода названия мероприятия.

    Сохраняет введённое название в данные диалога и переключает состояние
    на ввод описания.
    """
    dialog_manager.dialog_data["title"] = value.get_value()
    await dialog_manager.switch_to(AdminEventSG.description)


async def on_description_entered(msg: Message, value: str, dialog_manager: DialogManager, widget):
    """
    Обработчик ввода описания мероприятия.

    Сохраняет название и описание в базу данных, рассылает уведомление
    всем активным пользователям и завершает диалог.
    """
    title = dialog_manager.dialog_data["title"]
    description = value.get_value()

    # Добавляем событие в базу данных
    await create_event(title, description)

    # Получаем список всех активных пользователей для рассылки
    users = await get_all_active_users()
    text = f"🎉 <b>Новое корпоративное мероприятие</b>\n\n<b>{title}</b>\n{description}"

    # Отправляем сообщение каждому пользователю
    for user in users:
        try:
            await msg.bot.send_message(chat_id=user.tg_id, text=text)
        except Exception:
            pass  # Игнорируем ошибки при отправке сообщений

    await msg.answer("✅ Мероприятие добавлено и разослано сотрудникам.")
    await dialog_manager.done()


admin_event_dialog = Dialog(
    # Окно ввода названия мероприятия
    Window(
        Const("Введите название мероприятия:"),
        TextInput("title_input", on_success=on_title_entered),
        state=AdminEventSG.title,
    ),
    # Окно ввода описания мероприятия
    Window(
        Const("Введите описание мероприятия:"),
        TextInput("desc_input", on_success=on_description_entered),
        state=AdminEventSG.description,
    )
)
