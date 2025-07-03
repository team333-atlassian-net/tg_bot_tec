from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.input import TextInput
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram_dialog.widgets.kbd import Select, Button
from aiogram_dialog.widgets.text import Format
from dao.auth import get_all_active_users
from dao.events import create_event, delete_event, get_all_events, update_event


class AdminEventSG(StatesGroup):
    title = State()
    description = State()


##########################################################
async def on_title_entered(msg: Message, value: str, dialog_manager: DialogManager, widget):
    dialog_manager.dialog_data["title"] = value.get_value()
    await dialog_manager.switch_to(AdminEventSG.description)

async def on_description_entered(msg: Message, value: str, dialog_manager: DialogManager, widget):
    title = dialog_manager.dialog_data["title"]
    description = value.get_value()

    # Добавляем событие в БД
    await create_event(title, description)

    # Рассылка
    users = await get_all_active_users()
    text = f"🎉 <b>Новое корпоративное мероприятие</b>\n\n<b>{title}</b>\n{description}"
    for user in users:
        try:
            await msg.bot.send_message(chat_id=user.tg_id, text=text)
        except Exception:
            pass 

    await msg.answer("✅ Мероприятие добавлено и разослано сотрудникам.")
    await dialog_manager.done()
##############################################################################


admin_event_dialog = Dialog(
    # Добавление нового
    Window(
        Const("Введите название мероприятия:"),
        TextInput("title_input", on_success=on_title_entered),
        state=AdminEventSG.title,
    ),
    Window(
        Const("Введите описание мероприятия:"),
        TextInput("desc_input", on_success=on_description_entered),
        state=AdminEventSG.description,
    )
)
